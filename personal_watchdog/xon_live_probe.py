"""One-shot, bounded live probe for the frozen R3 XON check-email contract.

This module is deliberately a probe, not a collector.  It makes at most one
request for the fixed reserved-domain synthetic subject, retains only bounded
transport bytes in memory, and delegates all transport/XON/R2 semantics to
the committed R3 adapter.  It does not persist data, retry, follow redirects,
compare scans, or send notifications.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from personal_watchdog.comparison import DiagnosticMetadata, SourceCheck
from personal_watchdog.xon_live import (
    LIVE_BASE_URL,
    LIVE_QUERY,
    LIVE_TIMEOUT_SECONDS,
    LIVE_TOTAL_TIMEOUT_SECONDS,
    _Opener,
    capture_check_email,
)
from personal_watchdog.xon_live import LiveCaptureError as ProbeCaptureError
from personal_watchdog.xposedornot_check_email_adapter import (
    TransportAttempt,
    TransportClassification,
    classify_transport,
    make_trusted_context,
    normalize_check_email,
)

PROBE_VERSION = "r4-bounded-live-xon-probe/1"
PROBE_SUBJECT = "r4-probe-01@example.invalid"
PROBE_SUBJECT_REF = "r4-probe-01"
PROBE_BASE_URL = LIVE_BASE_URL
PROBE_QUERY = LIVE_QUERY
PROBE_TIMEOUT_SECONDS = LIVE_TIMEOUT_SECONDS
PROBE_TOTAL_TIMEOUT_SECONDS = LIVE_TOTAL_TIMEOUT_SECONDS


def capture_attempt(opener: _Opener | None = None) -> TransportAttempt:
    """Make the one approved request and return one bounded R3 attempt."""

    context = make_trusted_context(
        scan_id="r4-live:scan-001",
        source_check_id="r4-live:scan-001:check-X1",
        subject_ref=PROBE_SUBJECT,
        diagnostics=DiagnosticMetadata(
            datetime.now(UTC).isoformat(), text=PROBE_VERSION
        ),
    )
    return capture_check_email(
        email=PROBE_SUBJECT,
        context=context,
        opener=opener,
        user_agent="Personal-Watchdog-R4/1",
    )


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
