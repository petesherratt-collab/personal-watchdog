"""Bounded live transport for the XposedOrNot free check-email endpoint.

One call makes at most one HTTPS GET, follows no redirect, never retries,
keeps only bounded response bytes in memory, and returns a ``TransportAttempt``
for the existing adapter to interpret. It does not persist, compare, or print
anything.

What leaves the machine: the single email address being checked, in the URL
path of one request to ``api.xposedornot.com``. Nothing else is sent.
"""

from __future__ import annotations

import http.client
import socket
import ssl
import time
from collections.abc import Iterable
from dataclasses import dataclass
from email.message import Message
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

from personal_watchdog.response_normalizer import TrustedContext
from personal_watchdog.xposedornot_check_email_adapter import (
    MAX_XON_BODY_BYTES,
    Header,
    TransportAttempt,
)

LIVE_HOST = "api.xposedornot.com"
LIVE_BASE_URL = f"https://{LIVE_HOST}/v1/check-email/"
LIVE_QUERY = "include_details=false"
LIVE_TIMEOUT_SECONDS = 5.0
LIVE_TOTAL_TIMEOUT_SECONDS = 15.0
LIVE_CHUNK_BYTES = 4096
LIVE_USER_AGENT = "Personal-Watchdog/0.1"

_TRANSPORT_ERRORS = (
    OSError,
    URLError,
    ssl.SSLError,
    TimeoutError,
    http.client.HTTPException,
)


@dataclass(frozen=True, slots=True)
class _LiveRequest:
    email: str
    context: TrustedContext


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


class LiveCaptureError(ValueError):
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
        raise LiveCaptureError("response headers are not a message")

    retained: list[Header] = []
    total_bytes = 0
    for name, value in headers.raw_items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise LiveCaptureError("response header is not text")
        if name.lower() not in _RETAINED_HEADER_NAMES:
            continue
        try:
            name_bytes = name.encode("latin-1")
            value_bytes = value.encode("latin-1")
        except UnicodeEncodeError as error:
            raise LiveCaptureError("response header is not latin-1") from error
        retained.append(Header(name_bytes, value_bytes))
        total_bytes += len(name_bytes) + 1 + len(value_bytes) + 1

    if len(retained) > 16 or total_bytes > 8192:
        raise LiveCaptureError("retained response headers exceed the R3 bound")
    return tuple(retained)


def _status(response: object) -> int:
    value = getattr(response, "status", None)
    if type(value) is int and 100 <= value <= 599:
        return value
    getcode = getattr(response, "getcode", None)
    if callable(getcode):
        value = getcode()
    if type(value) is not int or not 100 <= value <= 599:
        raise LiveCaptureError("response did not provide an HTTP status")
    return value


def _attempt(
    request: _LiveRequest,
    *,
    status: int | None,
    headers: Iterable[Header],
    body: bytes,
    body_state: str,
    transport_failure: str | None = None,
    timed_out: bool = False,
    failure_phase: str | None = None,
) -> TransportAttempt:
    return TransportAttempt(
        http_status=status,
        bounded_headers=tuple(headers),
        body_bytes=body,
        body_state=body_state,  # type: ignore[arg-type]
        transport_failure=transport_failure,  # type: ignore[arg-type]
        timed_out=timed_out,
        failure_phase=failure_phase,  # type: ignore[arg-type]
        trusted_context=request.context,
        request_email=request.email,
    )


def _before_status_failure(
    request: _LiveRequest, error: BaseException
) -> TransportAttempt:
    if _is_timeout(error):
        return _attempt(
            request,
            status=None,
            headers=(),
            body=b"",
            body_state="absent",
            timed_out=True,
            failure_phase="before_status",
        )
    return _attempt(
        request,
        status=None,
        headers=(),
        body=b"",
        body_state="absent",
        transport_failure="transport",
        failure_phase="before_status",
    )


def _read_complete_response(
    request: _LiveRequest, response: object, headers: tuple[Header, ...]
) -> TransportAttempt:
    status = _status(response)
    if status >= 400:
        return _attempt(
            request,
            status=status,
            headers=headers,
            body=b"",
            body_state="absent",
        )

    body = bytearray()
    deadline = time.monotonic() + LIVE_TOTAL_TIMEOUT_SECONDS
    read = getattr(response, "read", None)
    if not callable(read):
        raise LiveCaptureError("response has no body reader")
    while True:
        if time.monotonic() >= deadline:
            return _attempt(
                request,
                status=status,
                headers=headers,
                body=bytes(body),
                body_state="incomplete",
                timed_out=True,
                failure_phase="after_status",
            )
        try:
            chunk = read(min(LIVE_CHUNK_BYTES, MAX_XON_BODY_BYTES + 1 - len(body)))
        except BaseException as error:
            if not isinstance(error, _TRANSPORT_ERRORS):
                raise
            return _attempt(
                request,
                status=status,
                headers=headers,
                body=bytes(body),
                body_state="incomplete",
                timed_out=_is_timeout(error),
                transport_failure=None if _is_timeout(error) else "transport",
                failure_phase="after_status",
            )
        if not isinstance(chunk, bytes):
            raise LiveCaptureError("response body reader returned non-bytes")
        body.extend(chunk)
        if len(body) > MAX_XON_BODY_BYTES:
            return _attempt(
                request,
                status=status,
                headers=headers,
                body=bytes(body[:MAX_XON_BODY_BYTES]),
                body_state="over_limit",
            )
        if not chunk:
            return _attempt(
                request,
                status=status,
                headers=headers,
                body=bytes(body),
                body_state="complete",
            )


def capture_check_email(
    *,
    email: str,
    context: TrustedContext,
    opener: _Opener | None = None,
    user_agent: str = LIVE_USER_AGENT,
) -> TransportAttempt:
    """Make exactly one request and return one bounded transport attempt.

    The address is placed only in the request URL and in the in-memory
    attempt. No exception text from the transport is returned or raised,
    because such text can contain the request URL.
    """

    live = _LiveRequest(email=email, context=context)
    url = f"{LIVE_BASE_URL}{quote(email, safe='')}?{LIVE_QUERY}"
    try:
        request = Request(
            url,
            headers={"Accept": "application/json", "User-Agent": user_agent},
            method="GET",
        )
    except ValueError:
        return _before_status_failure(live, OSError("request construction failed"))
    active_opener = opener or build_opener(_NoRedirectHandler())
    try:
        response = active_opener.open(request, timeout=LIVE_TIMEOUT_SECONDS)
    except HTTPError as error:
        try:
            return _attempt(
                live,
                status=_status(error),
                headers=_response_headers(error),
                body=b"",
                body_state="absent",
            )
        finally:
            error.close()
    except _TRANSPORT_ERRORS as error:
        return _before_status_failure(live, error)

    try:
        headers = _response_headers(response)
        return _read_complete_response(live, response, headers)
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()


__all__ = [
    "LIVE_BASE_URL",
    "LIVE_HOST",
    "LIVE_QUERY",
    "LIVE_TIMEOUT_SECONDS",
    "LIVE_TOTAL_TIMEOUT_SECONDS",
    "LIVE_USER_AGENT",
    "LiveCaptureError",
    "capture_check_email",
]
