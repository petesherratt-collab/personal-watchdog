"""Synthetic fixtures for the frozen XON check-email experiment."""

from __future__ import annotations

import json
from collections.abc import Sequence

from personal_watchdog.r1 import ScanAttempt, ScanPlan, SourceCheck
from personal_watchdog.r2_adapter import TrustedContext
from personal_watchdog.xposedornot_check_email_adapter import (
    Header,
    TransportAttempt,
    make_trusted_context,
)

SYNTHETIC_REQUEST_IDENTIFIER = "r3-subject@example.invalid"


def context(
    *,
    scan_id: str = "xon-scan-001",
    source_check_id: str = "xon-check-001",
    subject_ref: str = SYNTHETIC_REQUEST_IDENTIFIER,
) -> TrustedContext:
    return make_trusted_context(
        scan_id=scan_id,
        source_check_id=source_check_id,
        subject_ref=subject_ref,
    )


def json_body(
    *,
    email: str = SYNTHETIC_REQUEST_IDENTIFIER,
    breaches: object = (("Example Breach",),),
    status: object = "success",
    extra: dict[str, object] | None = None,
    ensure_ascii: bool = False,
) -> bytes:
    value: dict[str, object] = {
        "breaches": breaches,
        "email": email,
        "status": status,
    }
    if extra:
        value.update(extra)
    return json.dumps(value, ensure_ascii=ensure_ascii, separators=(",", ":")).encode(
        "utf-8"
    )


def headers(
    content_type: bytes | None = b"application/json",
    *,
    extra: Sequence[Header] = (),
) -> tuple[Header, ...]:
    values = list(extra)
    if content_type is not None:
        values.insert(0, Header(b"Content-Type", content_type))
    return tuple(values)


def attempt(
    body: bytes = b"",
    *,
    status: int | None = 200,
    header_values: tuple[Header, ...] | None = None,
    body_state: str = "complete",
    transport_failure: str | None = None,
    timed_out: bool = False,
    failure_phase: str | None = None,
    subject_ref: str = SYNTHETIC_REQUEST_IDENTIFIER,
    scan_id: str = "xon-scan-001",
    source_check_id: str = "xon-check-001",
) -> TransportAttempt:
    return TransportAttempt(
        http_status=status,
        bounded_headers=(headers() if header_values is None else header_values),
        body_bytes=body,
        body_state=body_state,  # type: ignore[arg-type]
        transport_failure=transport_failure,  # type: ignore[arg-type]
        timed_out=timed_out,
        failure_phase=failure_phase,  # type: ignore[arg-type]
        trusted_context=context(
            scan_id=scan_id,
            source_check_id=source_check_id,
            subject_ref=subject_ref,
        ),
    )


def scan_from_check(check: SourceCheck) -> ScanAttempt:
    plan = ScanPlan.create(
        subject_ref=check.subject_ref,
        sources=(check.source,),
    )
    return ScanAttempt.create(
        scan_id=check.scan_id,
        plan=plan,
        source_checks=(check,),
    )
