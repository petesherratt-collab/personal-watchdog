"""Offline R5 reconciliation tests for one observed XON response shape."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from personal_watchdog.r1 import SourceStatus
from personal_watchdog.xposedornot_check_email_adapter import (
    Header,
    TransportAttempt,
    TransportDisposition,
    classify_transport,
    make_trusted_context,
    normalize_check_email,
)

FIXTURE_PATH = (
    Path(__file__).parents[1]
    / "scenarios"
    / "r5_xon"
    / "01_observed_http_200_not_found.json"
)


def _fixture() -> dict[str, Any]:
    value = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert type(value) is dict
    return cast(dict[str, Any], value)


def _attempt_from_fixture(fixture: dict[str, Any]) -> TransportAttempt:
    assert set(fixture) == {
        "fixture_version",
        "fixture_id",
        "provenance",
        "trusted_context",
        "transport_attempt",
    }
    assert fixture["fixture_version"] == ("r5-offline-xon-contract-reconciliation/1")
    assert fixture["fixture_id"] == "r5-01-observed-http-200-not-found"
    assert fixture["provenance"] == {
        "experiment": "R4",
        "stage": "3",
        "observed_on": "2026-09-13",
    }

    context = cast(dict[str, Any], fixture["trusted_context"])
    assert set(context) == {"scan_id", "source_check_id", "subject_ref"}
    transport = cast(dict[str, Any], fixture["transport_attempt"])
    assert set(transport) == {
        "http_status",
        "bounded_headers",
        "body_bytes_hex",
        "body_state",
        "transport_failure",
        "timed_out",
        "failure_phase",
    }
    headers = tuple(
        Header(
            bytes.fromhex(cast(str, header["name_bytes_hex"])),
            bytes.fromhex(cast(str, header["value_bytes_hex"])),
        )
        for header in cast(list[dict[str, Any]], transport["bounded_headers"])
    )
    return TransportAttempt(
        http_status=cast(int, transport["http_status"]),
        bounded_headers=headers,
        body_bytes=bytes.fromhex(cast(str, transport["body_bytes_hex"])),
        body_state=cast(str, transport["body_state"]),  # type: ignore[arg-type]
        transport_failure=cast(str | None, transport["transport_failure"]),  # type: ignore[arg-type]
        timed_out=cast(bool, transport["timed_out"]),
        failure_phase=cast(str | None, transport["failure_phase"]),  # type: ignore[arg-type]
        trusted_context=make_trusted_context(
            scan_id=cast(str, context["scan_id"]),
            source_check_id=cast(str, context["source_check_id"]),
            subject_ref=cast(str, context["subject_ref"]),
        ),
    )


def test_observed_r4_body_reproduces_unverifiable_without_findings() -> None:
    attempt = _attempt_from_fixture(_fixture())

    transport = classify_transport(attempt)
    check = normalize_check_email(attempt)

    assert transport.disposition is TransportDisposition.READY
    assert transport.reason == "ready"
    assert transport.normalized_content_type == "application/json"
    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.reason_codes == ("response_unverifiable",)
    assert check.observations == ()


def test_fixture_is_bounded_and_contains_no_identifier_or_request_url() -> None:
    raw = FIXTURE_PATH.read_text(encoding="utf-8")
    body_hex = cast(str, _fixture()["transport_attempt"]["body_bytes_hex"])

    assert len(bytes.fromhex(body_hex)) == 34
    assert "@" not in raw
    assert "http://" not in raw
    assert "https://" not in raw
    assert "r4-probe-01" not in raw
