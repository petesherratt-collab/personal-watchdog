"""Synthetic matrix and R1 integration tests for the XON check-email adapter."""

from __future__ import annotations

import ast
import json
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import pytest

from personal_watchdog.r1 import (
    ComparisonKind,
    GuardKind,
    SourceStatus,
    compare_scans,
)
from personal_watchdog.r2_adapter import MAX_INPUT_BYTES
from personal_watchdog.xposedornot_check_email_adapter import (
    MAX_XON_BODY_BYTES,
    MAX_XON_HEADER_COUNT,
    MAX_XON_HEADER_NAME_BYTES,
    MAX_XON_HEADER_VALUE_BYTES,
    MAX_XON_RETAINED_HEADER_BYTES,
    XON_SOURCE,
    Header,
    R2EnvelopeTooLargeError,
    TransportAttempt,
    TransportConstructionError,
    TransportDisposition,
    classify_transport,
    normalize_check_email,
    serialize_r2_envelope,
)
from tests.fixtures_xposedornot_check_email import (
    SYNTHETIC_REQUEST_IDENTIFIER,
    attempt,
    headers,
    json_body,
    scan_from_check,
)


def assert_status(attempt_value: TransportAttempt, status: SourceStatus) -> None:
    check = normalize_check_email(attempt_value)
    assert check.status is status
    assert check.observations == () or status is SourceStatus.COMPLETED


def test_exact_success_uses_trusted_context_and_frozen_candidate_fields() -> None:
    check = normalize_check_email(attempt(json_body()))

    assert check.status is SourceStatus.COMPLETED
    assert len(check.observations) == 1
    observation = check.observations[0]
    assert observation.finding_key == "breach:Example Breach"
    assert observation.kind == "breach"
    assert observation.locator == "breach:Example Breach"
    assert observation.material.items == ()
    assert check.source == XON_SOURCE
    assert check.subject_ref == SYNTHETIC_REQUEST_IDENTIFIER


def test_success_preserves_names_without_sorting_or_casefolding() -> None:
    check = normalize_check_email(attempt(json_body(breaches=(("zeta", "Alpha"),))))

    assert [item.finding_key for item in check.observations] == [
        "breach:Alpha",
        "breach:zeta",
    ]


def test_exact_duplicate_names_use_existing_r2_deduplication() -> None:
    check = normalize_check_email(
        attempt(json_body(breaches=(("Example Breach", "Example Breach"),)))
    )

    assert check.status is SourceStatus.COMPLETED
    assert len(check.observations) == 1
    assert check.reason_codes == ("duplicate_finding_key_deduplicated",)


@pytest.mark.parametrize(
    "breaches",
    [[], [[]], [[""]], [["e\u0301"]], [[None]], [[1]]],
)
def test_zero_or_invalid_finding_bodies_are_unverifiable(breaches: object) -> None:
    check = normalize_check_email(attempt(json_body(breaches=breaches)))

    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.observations == ()


def test_echo_mismatch_is_unverifiable_and_cannot_replace_trusted_subject() -> None:
    check = normalize_check_email(attempt(json_body(email="other@example.invalid")))

    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.subject_ref == SYNTHETIC_REQUEST_IDENTIFIER


@pytest.mark.parametrize(
    "body",
    [
        b"{",
        b"\xff",
        b"NaN",
        b'{"breaches":[["x"]],"email":"r3-subject@example.invalid",'
        b'"status":"success","status":"success"}',
    ],
)
def test_malformed_utf8_json_duplicate_keys_and_constants_are_unverifiable(
    body: bytes,
) -> None:
    assert_status(normalize_attempt(body), SourceStatus.UNVERIFIABLE)


def test_bounded_hostile_integer_is_unverifiable_without_raising() -> None:
    hostile = (
        b'{"breaches":[["x"]],"email":"r3-subject@example.invalid",'
        b'"status":"success","hostile":' + b"1" * 5_000 + b"}"
    )
    assert len(hostile) < MAX_XON_BODY_BYTES

    check = normalize_check_email(attempt(hostile))

    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.reason_codes == ("response_unverifiable",)
    assert check.observations == ()


def normalize_attempt(body: bytes) -> TransportAttempt:
    return attempt(body)


@pytest.mark.parametrize(
    "body_value",
    [
        {"breaches": [["x"]], "email": SYNTHETIC_REQUEST_IDENTIFIER},
        {
            "breaches": [["x"]],
            "email": SYNTHETIC_REQUEST_IDENTIFIER,
            "status": "error",
        },
        {
            "breaches": [["x"]],
            "email": SYNTHETIC_REQUEST_IDENTIFIER,
            "status": True,
        },
        {
            "breaches": [["x"]],
            "email": SYNTHETIC_REQUEST_IDENTIFIER,
            "status": "success",
            "undocumented": True,
        },
    ],
)
def test_schema_drift_and_http_200_error_bodies_are_unverifiable(
    body_value: dict[str, object],
) -> None:
    check = normalize_check_email(attempt(json.dumps(body_value).encode("utf-8")))
    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.observations == ()


@pytest.mark.parametrize(
    "content_type",
    [b"text/plain", b"application/json; charset=utf-8", b"application/json\x80"],
)
def test_wrong_parameterized_and_non_ascii_content_types_are_unverifiable(
    content_type: bytes,
) -> None:
    check = normalize_check_email(
        attempt(json_body(), header_values=headers(content_type))
    )
    assert check.status is SourceStatus.UNVERIFIABLE


def test_content_type_trim_and_ascii_case_rule_are_exact() -> None:
    accepted = attempt(
        json_body(),
        header_values=headers(b" \tAPPLICATION/JSON\t "),
    )
    assert accepted.normalized_content_type == "application/json"
    assert normalize_check_email(accepted).status is SourceStatus.COMPLETED

    internal_whitespace = attempt(
        json_body(), header_values=headers(b"application/ json")
    )
    assert (
        normalize_check_email(internal_whitespace).status is SourceStatus.UNVERIFIABLE
    )


def test_missing_and_duplicate_content_type_metadata_are_unverifiable() -> None:
    missing = attempt(json_body(), header_values=headers(None))
    duplicate = attempt(
        json_body(),
        header_values=(
            Header(b"Content-Type", b"application/json"),
            Header(b"content-type", b"application/json"),
        ),
    )

    assert normalize_check_email(missing).status is SourceStatus.UNVERIFIABLE
    assert normalize_check_email(duplicate).status is SourceStatus.UNVERIFIABLE
    assert duplicate.normalized_content_type is None


@pytest.mark.parametrize("status", [201, 204, 299])
def test_other_2xx_statuses_are_unverifiable(status: int) -> None:
    check = normalize_check_email(attempt(json_body(), status=status))
    assert check.status is SourceStatus.UNVERIFIABLE


@pytest.mark.parametrize("status", [401, 404, 422, 429, 500, 503])
def test_auth_rate_limit_not_found_and_server_statuses_are_failed(status: int) -> None:
    check = normalize_check_email(attempt(b"", status=status, header_values=headers()))
    assert check.status is SourceStatus.FAILED
    assert check.observations == ()


def test_absent_http_200_body_is_unverifiable() -> None:
    check = normalize_check_email(attempt(b"", body_state="absent"))
    assert check.status is SourceStatus.UNVERIFIABLE


def test_simultaneous_fault_precedence_is_exact() -> None:
    duplicate_headers = (
        Header(b"Content-Type", b"application/json"),
        Header(b"content-type", b"application/json"),
    )
    cases = (
        (
            attempt(json_body(), status=503, header_values=duplicate_headers),
            TransportDisposition.FAILED,
            "http_failure",
            SourceStatus.FAILED,
            ("response_failed",),
        ),
        (
            attempt(
                b"{" * MAX_XON_BODY_BYTES,
                status=503,
                body_state="over_limit",
            ),
            TransportDisposition.FAILED,
            "http_failure",
            SourceStatus.FAILED,
            ("response_failed",),
        ),
        (
            attempt(
                b"partial",
                status=503,
                body_state="incomplete",
                transport_failure="transport",
                failure_phase="after_status",
            ),
            TransportDisposition.FAILED,
            "http_failure",
            SourceStatus.FAILED,
            ("response_failed",),
        ),
        (
            attempt(
                b"partial",
                status=200,
                body_state="incomplete",
                transport_failure="transport",
                failure_phase="after_status",
            ),
            TransportDisposition.INCOMPLETE,
            "post_status_body_failure",
            SourceStatus.UNVERIFIABLE,
            ("response_incomplete",),
        ),
        (
            attempt(
                b"{" * MAX_XON_BODY_BYTES,
                status=200,
                body_state="over_limit",
            ),
            TransportDisposition.INCOMPLETE,
            "body_over_limit",
            SourceStatus.UNVERIFIABLE,
            ("response_incomplete",),
        ),
        (
            attempt(json_body(), status=200, header_values=duplicate_headers),
            TransportDisposition.UNVERIFIABLE,
            "duplicate header name",
            SourceStatus.UNVERIFIABLE,
            ("response_unverifiable",),
        ),
    )
    for value, disposition, reason, status, r2_reasons in cases:
        classification = classify_transport(value)
        check = normalize_check_email(value)
        assert value.http_status in {200, 503}
        assert classification.disposition is disposition
        assert classification.reason == reason
        assert check.status is status
        assert check.reason_codes == r2_reasons


@pytest.mark.parametrize("timed_out", [False, True])
def test_pre_status_failure_and_timeout_are_failed(timed_out: bool) -> None:
    check = normalize_check_email(
        attempt(
            b"",
            status=None,
            header_values=(),
            body_state="absent",
            timed_out=timed_out,
            transport_failure=None if timed_out else "transport",
            failure_phase="before_status",
        )
    )
    assert check.status is SourceStatus.FAILED


@pytest.mark.parametrize("timed_out", [False, True])
def test_post_status_failure_and_timeout_preserve_status_and_discard_prefix(
    timed_out: bool,
) -> None:
    value = attempt(
        b'{"breaches":',
        body_state="incomplete",
        timed_out=timed_out,
        transport_failure=None if timed_out else "transport",
        failure_phase="after_status",
    )
    classification = classify_transport(value)
    assert value.http_status == 200
    assert value.body_bytes == b'{"breaches":'
    assert classification.disposition is TransportDisposition.INCOMPLETE
    assert normalize_check_email(value).status is SourceStatus.UNVERIFIABLE


def test_over_limit_body_is_incomplete_and_prefix_is_never_parsed() -> None:
    value = attempt(
        b"{" * MAX_XON_BODY_BYTES,
        body_state="over_limit",
    )
    assert classify_transport(value).disposition is TransportDisposition.INCOMPLETE
    assert normalize_check_email(value).status is SourceStatus.UNVERIFIABLE


@pytest.mark.parametrize(
    "kwargs",
    [
        {"http_status": None, "body_state": "complete", "body_bytes": b""},
        {
            "http_status": None,
            "body_state": "incomplete",
            "body_bytes": b"",
            "transport_failure": "transport",
            "failure_phase": "after_status",
        },
        {
            "http_status": 200,
            "body_state": "complete",
            "body_bytes": b"",
            "transport_failure": "transport",
            "failure_phase": "before_status",
        },
        {
            "http_status": 200,
            "body_state": "complete",
            "body_bytes": b"",
            "transport_failure": "transport",
            "failure_phase": "after_status",
        },
        {
            "http_status": 200,
            "body_state": "over_limit",
            "body_bytes": b"",
        },
        {
            "http_status": 200,
            "body_state": "complete",
            "body_bytes": b"x" * (MAX_XON_BODY_BYTES + 1),
        },
        {
            "http_status": 200,
            "body_state": "complete",
            "body_bytes": b"",
            "transport_failure": "transport",
            "timed_out": True,
            "failure_phase": "after_status",
        },
    ],
)
def test_contradictory_transport_states_are_visible_construction_errors(
    kwargs: dict[str, object],
) -> None:
    with pytest.raises(TransportConstructionError):
        TransportAttempt(
            bounded_headers=(),
            trusted_context=attempt().trusted_context,
            **cast(dict[str, Any], kwargs),
        )


def test_header_bounds_and_accounting_are_exact() -> None:
    header = Header(b"x" * MAX_XON_HEADER_NAME_BYTES, b"y" * MAX_XON_HEADER_VALUE_BYTES)
    exact_total = len(header.name_bytes) + 1 + len(header.value_bytes) + 1
    assert exact_total == MAX_XON_HEADER_NAME_BYTES + MAX_XON_HEADER_VALUE_BYTES + 2
    with pytest.raises(TransportConstructionError):
        Header(b"x" * (MAX_XON_HEADER_NAME_BYTES + 1), b"")
    with pytest.raises(TransportConstructionError):
        Header(b"x", b"y" * (MAX_XON_HEADER_VALUE_BYTES + 1))
    with pytest.raises(TransportConstructionError):
        TransportAttempt(
            http_status=200,
            bounded_headers=tuple(
                Header(b"x", b"y" * MAX_XON_HEADER_VALUE_BYTES)
                for _ in range(MAX_XON_HEADER_COUNT)
            ),
            body_bytes=b"",
            body_state="complete",
            trusted_context=attempt().trusted_context,
        )
    assert MAX_XON_RETAINED_HEADER_BYTES == 8_192


def test_exact_header_count_boundary_is_constructible_then_rejected() -> None:
    sixteen = tuple(Header(b"content-length", b"1") for _ in range(16))
    value = attempt(b"", header_values=sixteen)
    assert len(value.bounded_headers) == MAX_XON_HEADER_COUNT
    assert normalize_check_email(value).reason_codes == ("response_unverifiable",)

    with pytest.raises(TransportConstructionError):
        attempt(
            b"",
            header_values=sixteen + (Header(b"content-length", b"1"),),
        )


def test_exact_retained_header_bytes_boundary_is_constructible_then_rejected() -> None:
    full = Header(b"x" * 64, b"y" * 512)
    exact = tuple([full] * 14) + (Header(b"x" * 64, b"y" * 34),)
    over = tuple([full] * 14) + (Header(b"x" * 64, b"y" * 35),)

    exact_total = sum(
        len(item.name_bytes) + 1 + len(item.value_bytes) + 1 for item in exact
    )
    assert exact_total == 8_192
    assert len(attempt(b"", header_values=exact).bounded_headers) == 15
    with pytest.raises(TransportConstructionError):
        attempt(b"", header_values=over)


def test_exact_body_byte_boundary_is_constructible_then_rejected() -> None:
    exact = attempt(b"x" * MAX_XON_BODY_BYTES)
    assert len(exact.body_bytes) == 16_384
    assert normalize_check_email(exact).status is SourceStatus.UNVERIFIABLE
    with pytest.raises(TransportConstructionError):
        attempt(b"x" * (MAX_XON_BODY_BYTES + 1))


def test_exact_breach_name_collection_boundary_is_accepted_then_rejected() -> None:
    sixteen = tuple(f"breach-{index:02d}" for index in range(16))
    seventeen = sixteen + ("breach-16",)

    assert (
        normalize_check_email(attempt(json_body(breaches=(sixteen,)))).status
        is SourceStatus.COMPLETED
    )
    assert (
        normalize_check_email(attempt(json_body(breaches=(seventeen,)))).status
        is SourceStatus.UNVERIFIABLE
    )


def test_exact_breach_name_codepoint_boundary_is_accepted_then_rejected() -> None:
    accepted = "x" * 64
    rejected = "x" * 65

    assert (
        normalize_check_email(attempt(json_body(breaches=((accepted,),)))).status
        is SourceStatus.COMPLETED
    )
    assert (
        normalize_check_email(attempt(json_body(breaches=((rejected,),)))).status
        is SourceStatus.UNVERIFIABLE
    )


def test_exact_echoed_email_codepoint_boundary_is_accepted_then_rejected() -> None:
    accepted = "a" * 128
    rejected = "a" * 129

    accepted_check = normalize_check_email(
        attempt(
            json_body(email=accepted),
            subject_ref=accepted,
            scan_id="xon-scan-email-128",
            source_check_id="xon-check-email-128",
        )
    )
    rejected_check = normalize_check_email(
        attempt(
            json_body(email=rejected),
            subject_ref=rejected,
            scan_id="xon-scan-email-129",
            source_check_id="xon-check-email-129",
        )
    )

    assert accepted_check.status is SourceStatus.COMPLETED
    assert rejected_check.status is SourceStatus.UNVERIFIABLE


def test_trusted_context_cannot_be_replaced_by_response_bytes() -> None:
    context_value = attempt().trusted_context
    wrong_source = replace(context_value, source=replace(XON_SOURCE, source_id="other"))
    with pytest.raises(TransportConstructionError):
        TransportAttempt(
            http_status=200,
            bounded_headers=headers(),
            body_bytes=json_body(email="other@example.invalid"),
            body_state="complete",
            trusted_context=wrong_source,
        )


def test_serialization_is_compact_ascii_escaped_and_bounded() -> None:
    raw = serialize_r2_envelope(
        outcome="completed",
        results=(
            {
                "finding_key": "breach:é",
                "kind": "breach",
                "locator": "breach:é",
                "material": {},
            },
        ),
    )
    assert b"\\u00e9" in raw
    assert b" " not in raw
    assert raw.startswith(b'{"contract_version":"fixture-response/1"')
    assert len(raw) <= MAX_INPUT_BYTES
    with pytest.raises(R2EnvelopeTooLargeError):
        serialize_r2_envelope(
            outcome="completed",
            results=(
                {
                    "finding_key": "x" * MAX_INPUT_BYTES,
                    "kind": "breach",
                    "locator": "x",
                    "material": {},
                },
            ),
        )


def test_frozen_size_calculation_is_inside_existing_r2_limit() -> None:
    maximum_name = "😀" * 64
    maximum_email = "😀" * 128
    names = tuple(maximum_name for _ in range(16))
    raw_xon = json_body(
        email=maximum_email,
        breaches=(names,),
        ensure_ascii=True,
    )
    raw_r2 = serialize_r2_envelope(
        outcome="completed",
        results=tuple(
            {
                "finding_key": f"breach:{name}",
                "kind": "breach",
                "locator": f"breach:{name}",
                "material": {},
            }
            for name in names
        ),
    )
    assert raw_xon.decode("utf-8")
    assert raw_r2.decode("utf-8")
    assert b"\\ud83d\\ude00" in raw_xon
    assert b"\\ud83d\\ude00" in raw_r2
    assert len(raw_xon) == 13_918
    assert len(raw_r2) == 25_910
    assert len(raw_r2) < MAX_INPUT_BYTES


def test_r1_guards_failed_incomplete_and_unverifiable_without_disappearance() -> None:
    baseline = scan_from_check(
        normalize_check_email(
            attempt(
                json_body(),
                scan_id="xon-scan-baseline",
                source_check_id="xon-check-baseline",
            )
        )
    )
    cases = (
        attempt(
            b"",
            status=None,
            header_values=(),
            body_state="absent",
            transport_failure="transport",
            failure_phase="before_status",
            scan_id="xon-scan-failed",
            source_check_id="xon-check-failed",
        ),
        attempt(
            b"partial",
            body_state="incomplete",
            transport_failure="transport",
            failure_phase="after_status",
            scan_id="xon-scan-incomplete",
            source_check_id="xon-check-incomplete",
        ),
        attempt(
            json_body(breaches=[]),
            scan_id="xon-scan-unverifiable",
            source_check_id="xon-check-unverifiable",
        ),
    )
    expected = (
        (SourceStatus.FAILED, GuardKind.FAILED, ("response_failed",)),
        (SourceStatus.UNVERIFIABLE, GuardKind.UNVERIFIABLE, ("response_incomplete",)),
        (
            SourceStatus.UNVERIFIABLE,
            GuardKind.UNVERIFIABLE,
            ("response_unverifiable",),
        ),
    )
    for value, (status, guard_kind, reasons) in zip(cases, expected, strict=True):
        current_check = normalize_check_email(value)
        current = scan_from_check(current_check)
        assert current_check.scan_id != baseline.scan_id
        assert (
            current_check.source_check_id != baseline.source_checks[0].source_check_id
        )
        assert current_check.status is status
        assert current_check.reason_codes == reasons
        report = compare_scans(baseline, current)
        assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
        assert report.exposure_events == ()
        assert report.guarding_events[0].guard_kind is guard_kind
        assert report.guarding_events[0].prior_status is SourceStatus.COMPLETED
        assert report.guarding_events[0].reason_codes == reasons


def test_failed_or_unverifiable_first_check_cannot_create_an_empty_baseline() -> None:
    cases = (
        (
            attempt(
                json_body(breaches=[]),
                scan_id="xon-scan-first-unverifiable",
                source_check_id="xon-check-first-unverifiable",
            ),
            GuardKind.UNVERIFIABLE,
        ),
        (
            attempt(
                b"",
                status=None,
                header_values=(),
                body_state="absent",
                timed_out=True,
                failure_phase="before_status",
                scan_id="xon-scan-first-timeout",
                source_check_id="xon-check-first-timeout",
            ),
            GuardKind.FAILED,
        ),
        (
            attempt(
                b"partial",
                body_state="incomplete",
                transport_failure="transport",
                failure_phase="after_status",
                scan_id="xon-scan-first-incomplete",
                source_check_id="xon-check-first-incomplete",
            ),
            GuardKind.UNVERIFIABLE,
        ),
    )
    for value, guard_kind in cases:
        current = scan_from_check(normalize_check_email(value))
        report = compare_scans(None, current)
        assert report.baseline_created_sources == ()
        assert report.exposure_events == ()
        assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
        assert report.guarding_events[0].guard_kind is guard_kind


def test_adapter_has_no_network_capable_imports_or_calls() -> None:
    path = (
        Path(__file__).parents[1]
        / "personal_watchdog/xposedornot_check_email_adapter.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported.update(
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
        for alias in node.names
    )
    assert not imported & {"socket", "ssl", "http", "requests", "urllib", "httpx"}
