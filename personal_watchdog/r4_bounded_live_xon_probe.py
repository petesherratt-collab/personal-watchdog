"""One-shot, bounded live probe for the frozen R3 XON check-email contract.

This module is deliberately a probe, not a collector.  It makes at most one
request for the fixed reserved-domain synthetic subject, retains only bounded
transport bytes in memory, and delegates all transport/XON/R2 semantics to
the committed R3 adapter.  It does not persist data, retry, follow redirects,
compare scans, or send notifications.
"""

from __future__ import annotations

import json
import socket
import ssl
import time
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from email.message import Message
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
)

from personal_watchdog.r1 import DiagnosticMetadata, SourceCheck
from personal_watchdog.xposedornot_check_email_adapter import (
    MAX_XON_BODY_BYTES,
    Header,
    TransportAttempt,
    TransportClassification,
    classify_transport,
    make_trusted_context,
    normalize_check_email,
)

PROBE_VERSION = "r4-bounded-live-xon-probe/1"
PROBE_SUBJECT = "r4-probe-01@example.invalid"
PROBE_SUBJECT_REF = "r4-probe-01"
PROBE_BASE_URL = "https://api.xposedornot.com/v1/check-email/"
PROBE_QUERY = "include_details=false"
PROBE_TIMEOUT_SECONDS = 5.0
PROBE_TOTAL_TIMEOUT_SECONDS = 15.0
PROBE_CHUNK_BYTES = 4096

_RETAINED_HEADER_NAMES = frozenset(
    {
        "content-type",
        "content-length",
        "retry-after",
        "date",
        "etag",
        "last-modified",
        "location",
        "server",
    }
)


class ProbeCaptureError(ValueError):
    """Raised when live response metadata cannot form a bounded attempt."""


class _Opener(Protocol):
    def open(self, request: Request, timeout: float) -> object: ...


class _NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, *_args: object, **_kwargs: object) -> Request | None:
        return None


def _is_timeout(error: BaseException) -> bool:
    if isinstance(error, URLError) and isinstance(error.reason, BaseException):
        return _is_timeout(error.reason)
    return isinstance(error, (TimeoutError, socket.timeout))


def _response_headers(response: object) -> tuple[Header, ...]:
    headers = getattr(response, "headers", None)
    if not isinstance(headers, Message):
        raise ProbeCaptureError("response headers are not a message")

    retained: list[Header] = []
    total_bytes = 0
    for name, value in headers.raw_items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise ProbeCaptureError("response header is not text")
        if name.lower() not in _RETAINED_HEADER_NAMES:
            continue
        try:
            name_bytes = name.encode("latin-1")
            value_bytes = value.encode("latin-1")
        except UnicodeEncodeError as error:
            raise ProbeCaptureError("response header is not latin-1") from error
        retained.append(Header(name_bytes, value_bytes))
        total_bytes += len(name_bytes) + 1 + len(value_bytes) + 1

    if len(retained) > 16 or total_bytes > 8192:
        raise ProbeCaptureError("retained response headers exceed the R3 bound")
    return tuple(retained)


def _status(response: object) -> int:
    value = getattr(response, "status", None)
    if type(value) is int and 100 <= value <= 599:
        return value
    getcode = getattr(response, "getcode", None)
    if callable(getcode):
        value = getcode()
    if type(value) is not int or not 100 <= value <= 599:
        raise ProbeCaptureError("response did not provide an HTTP status")
    return value


def _attempt(
    *,
    status: int | None,
    headers: Iterable[Header],
    body: bytes,
    body_state: str,
    transport_failure: str | None = None,
    timed_out: bool = False,
    failure_phase: str | None = None,
) -> TransportAttempt:
    context = make_trusted_context(
        scan_id="r4-live:scan-001",
        source_check_id="r4-live:scan-001:check-X1",
        subject_ref=PROBE_SUBJECT,
        diagnostics=DiagnosticMetadata(
            datetime.now(UTC).isoformat(), text=PROBE_VERSION
        ),
    )
    return TransportAttempt(
        http_status=status,
        bounded_headers=tuple(headers),
        body_bytes=body,
        body_state=body_state,  # type: ignore[arg-type]
        transport_failure=transport_failure,  # type: ignore[arg-type]
        timed_out=timed_out,
        failure_phase=failure_phase,  # type: ignore[arg-type]
        trusted_context=context,
    )


def _before_status_failure(error: BaseException) -> TransportAttempt:
    if _is_timeout(error):
        return _attempt(
            status=None,
            headers=(),
            body=b"",
            body_state="absent",
            timed_out=True,
            failure_phase="before_status",
        )
    return _attempt(
        status=None,
        headers=(),
        body=b"",
        body_state="absent",
        transport_failure="transport",
        failure_phase="before_status",
    )


def _read_complete_response(
    response: object, headers: tuple[Header, ...]
) -> TransportAttempt:
    status = _status(response)
    if status >= 400:
        return _attempt(
            status=status,
            headers=headers,
            body=b"",
            body_state="absent",
        )

    body = bytearray()
    deadline = time.monotonic() + PROBE_TOTAL_TIMEOUT_SECONDS
    read = getattr(response, "read", None)
    if not callable(read):
        raise ProbeCaptureError("response has no body reader")
    while True:
        if time.monotonic() >= deadline:
            return _attempt(
                status=status,
                headers=headers,
                body=bytes(body),
                body_state="incomplete",
                timed_out=True,
                failure_phase="after_status",
            )
        try:
            chunk = read(min(PROBE_CHUNK_BYTES, MAX_XON_BODY_BYTES + 1 - len(body)))
        except BaseException as error:
            if not isinstance(error, (OSError, URLError, TimeoutError, socket.timeout)):
                raise
            return _attempt(
                status=status,
                headers=headers,
                body=bytes(body),
                body_state="incomplete",
                timed_out=_is_timeout(error),
                transport_failure=None if _is_timeout(error) else "transport",
                failure_phase="after_status",
            )
        if not isinstance(chunk, bytes):
            raise ProbeCaptureError("response body reader returned non-bytes")
        body.extend(chunk)
        if len(body) > MAX_XON_BODY_BYTES:
            return _attempt(
                status=status,
                headers=headers,
                body=bytes(body[:MAX_XON_BODY_BYTES]),
                body_state="over_limit",
            )
        if not chunk:
            return _attempt(
                status=status,
                headers=headers,
                body=bytes(body),
                body_state="complete",
            )


def capture_attempt(opener: _Opener | None = None) -> TransportAttempt:
    """Make the one approved request and return one bounded R3 attempt."""

    encoded_subject = quote(PROBE_SUBJECT, safe="")
    url = f"{PROBE_BASE_URL}{encoded_subject}?{PROBE_QUERY}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Personal-Watchdog-R4/1",
        },
        method="GET",
    )
    active_opener = opener or build_opener(_NoRedirectHandler())
    try:
        response = active_opener.open(request, timeout=PROBE_TIMEOUT_SECONDS)
    except HTTPError as error:
        headers = _response_headers(error)
        return _attempt(
            status=_status(error),
            headers=headers,
            body=b"",
            body_state="absent",
        )
    except (OSError, URLError, ssl.SSLError, TimeoutError) as error:
        return _before_status_failure(error)

    try:
        headers = _response_headers(response)
        return _read_complete_response(response, headers)
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()


@dataclass(frozen=True, slots=True)
class ProbeResult:
    """Bounded local projection of one live attempt and its R3 result."""

    attempt: TransportAttempt
    transport: TransportClassification
    source_check: SourceCheck
    started_at: str
    ended_at: str

    def as_dict(self, *, include_diagnostic_body: bool = False) -> dict[str, object]:
        check = self.source_check
        result: dict[str, object] = {
            "probe_version": PROBE_VERSION,
            "subject_ref": PROBE_SUBJECT_REF,
            "source_id": check.source.source_id,
            "canonical_scope": list(check.source.canonical_scope),
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "request_count": 1,
            "http_status": self.attempt.http_status,
            "header_count": len(self.attempt.bounded_headers),
            "body_bytes": len(self.attempt.body_bytes),
            "body_state": self.attempt.body_state,
            "transport_failure": self.attempt.transport_failure,
            "timed_out": self.attempt.timed_out,
            "failure_phase": self.attempt.failure_phase,
            "normalized_content_type": self.transport.normalized_content_type,
            "transport_disposition": self.transport.disposition.value,
            "transport_reason": self.transport.reason,
            "source_status": check.status.value,
            "reason_codes": list(check.reason_codes),
            "finding_keys": [
                observation.finding_key for observation in check.observations
            ],
        }
        if include_diagnostic_body:
            result["diagnostic_body_hex"] = self.attempt.body_bytes.hex()
        return result


def run_probe(opener: _Opener | None = None) -> ProbeResult:
    """Run the single bounded probe without comparison or persistence."""

    started = datetime.now(UTC)
    attempt = capture_attempt(opener)
    transport = classify_transport(attempt)
    source_check = normalize_check_email(attempt)
    ended = datetime.now(UTC)
    return ProbeResult(
        attempt=attempt,
        transport=transport,
        source_check=source_check,
        started_at=started.isoformat(),
        ended_at=ended.isoformat(),
    )


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run the bounded R4 XON probe")
    parser.add_argument(
        "--diagnostic",
        action="store_true",
        help="include the bounded response bytes as lowercase hex",
    )
    arguments = parser.parse_args(argv)
    result = run_probe()
    print(
        json.dumps(
            result.as_dict(include_diagnostic_body=arguments.diagnostic),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "PROBE_BASE_URL",
    "PROBE_QUERY",
    "PROBE_SUBJECT",
    "PROBE_SUBJECT_REF",
    "PROBE_TIMEOUT_SECONDS",
    "PROBE_TOTAL_TIMEOUT_SECONDS",
    "PROBE_VERSION",
    "ProbeCaptureError",
    "ProbeResult",
    "capture_attempt",
    "run_probe",
]
