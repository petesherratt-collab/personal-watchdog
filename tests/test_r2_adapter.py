"""Hostile-input and R1 integration tests for the R2 adapter boundary."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import cast

import pytest

from personal_watchdog.r1 import (
    AggregateOutcome,
    ComparisonKind,
    DiagnosticMetadata,
    ExposureKind,
    R1Error,
    ScanAttempt,
    ScanPlan,
    SourceCheck,
    SourceIdentity,
    SourceStatus,
    compare_scans,
)
from personal_watchdog.r2_adapter import (
    MAX_ARRAY_ITEMS,
    MAX_DIAGNOSTIC_DURATION_MS,
    MAX_DIAGNOSTIC_TEXT,
    MAX_INPUT_BYTES,
    MAX_NESTING_DEPTH,
    MAX_OBJECT_MEMBERS,
    MAX_RESULTS,
    MAX_RETRY_COUNT,
    MAX_STRING_LENGTH,
    REASON_CODES,
    TrustedContext,
    normalize_response,
)
from tests.fixtures_r2 import (
    SOURCE_R2_A,
    SOURCE_R2_B,
    context,
    envelope,
    normalize_scan,
    payload,
    result,
)


def normalize(
    value: Mapping[str, object],
    *,
    subject_ref: str = "subject-r2-a",
    source: SourceIdentity = SOURCE_R2_A,
) -> SourceCheck:
    return normalize_response(
        payload(value), context(subject_ref=subject_ref, source=source)
    )


def assert_unverifiable(check: SourceCheck, reason: str) -> None:
    assert check.status is SourceStatus.UNVERIFIABLE
    assert reason in check.reason_codes
    assert check.observations == ()


def test_valid_completed_and_completed_empty_are_distinct() -> None:
    completed = normalize(envelope(results=(result(),)))
    empty = normalize(envelope())

    assert completed.status is SourceStatus.COMPLETED
    assert len(completed.observations) == 1
    assert empty.status is SourceStatus.COMPLETED
    assert empty.observations == ()
    assert empty != normalize(envelope(outcome="failed"))


@pytest.mark.parametrize(
    ("raw", "reason"),
    [
        (b"", "blank_input"),
        (b" \n\t ", "blank_input"),
        (b"{", "invalid_json"),
        (b"\xff", "invalid_utf8"),
        (b"NaN", "nonstandard_json_constant"),
        (b"Infinity", "nonstandard_json_constant"),
        (b"-Infinity", "nonstandard_json_constant"),
        (b"[]", "wrong_top_level_type"),
        (b"null", "wrong_top_level_type"),
        (b'"synthetic"', "wrong_top_level_type"),
    ],
)
def test_parser_hostile_inputs_are_unverifiable(raw: bytes, reason: str) -> None:
    assert_unverifiable(normalize_response(raw, context()), reason)


def test_non_bytes_are_programmer_errors() -> None:
    with pytest.raises(TypeError):
        normalize_response("{}", context())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        normalize_response(bytearray(b"{}"), context())  # type: ignore[arg-type]


def test_size_limit_is_checked_before_utf8_decoding() -> None:
    oversized_invalid_utf8 = b"\xff" * (MAX_INPUT_BYTES + 1)
    check = normalize_response(oversized_invalid_utf8, context())
    assert_unverifiable(check, "input_too_large")


def test_exact_input_limit_is_accepted_and_first_byte_over_is_rejected() -> None:
    valid = payload(envelope())
    at_limit = valid + b" " * (MAX_INPUT_BYTES - len(valid))
    assert len(at_limit) == MAX_INPUT_BYTES
    assert normalize_response(at_limit, context()).status is SourceStatus.COMPLETED

    over_limit = at_limit + b" "
    assert_unverifiable(normalize_response(over_limit, context()), "input_too_large")


@pytest.mark.parametrize(
    "raw",
    [
        b'{"contract_version":"fixture-response/1","source_id":"synthetic-source-a","source_id":"synthetic-source-a","outcome":"completed","results":[]}',
        b'{"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[{"finding_key":"finding-a","kind":"synthetic-profile","kind":"synthetic-profile","locator":"locator-a","material":{}}]}',
        b'{"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[{"finding_key":"finding-a","kind":"synthetic-profile","locator":"locator-a","material":{"display_state":"active","display_state":"active"}}]}',
    ],
)
def test_duplicate_json_object_keys_are_rejected_at_every_object_level(
    raw: bytes,
) -> None:
    assert_unverifiable(normalize_response(raw, context()), "duplicate_json_key")


@pytest.mark.parametrize("contract", ["fixture-response/2", "other-contract"])
def test_unsupported_contract_is_distinct_and_unverifiable(contract: str) -> None:
    value = envelope()
    value["contract_version"] = contract
    check = normalize(value)
    assert_unverifiable(check, "unsupported_response_contract")
    assert check.source == SOURCE_R2_A


def test_source_mismatch_cannot_change_trusted_source() -> None:
    check = normalize(envelope(source_id=SOURCE_R2_B.source_id))
    assert_unverifiable(check, "response_source_mismatch")
    assert check.source is SOURCE_R2_A
    assert check.subject_ref == "subject-r2-a"


@pytest.mark.parametrize(
    "field",
    [
        "subject_ref",
        "canonical_scope",
        "adapter_id",
        "adapter_version",
        "schema_version",
        "normalization_version",
    ],
)
def test_untrusted_identity_fields_are_not_envelope_fields(field: str) -> None:
    value = envelope()
    value[field] = "attacker-controlled"
    check = normalize(value)
    assert_unverifiable(check, "unknown_field")
    assert check.subject_ref == "subject-r2-a"
    assert check.source is SOURCE_R2_A


def test_untrusted_result_context_is_rejected() -> None:
    candidate = result()
    candidate["context"] = {"subject_ref": "attacker-controlled"}
    check = normalize(envelope(results=(candidate,)))
    assert_unverifiable(check, "unknown_field")


@pytest.mark.parametrize(
    ("mutate", "reason"),
    [
        (lambda value: value.pop("results"), "missing_field"),
        (lambda value: value.update(extra="x"), "unknown_field"),
    ],
)
def test_envelope_key_set_is_exact(mutate: object, reason: str) -> None:
    value = envelope()
    mutate(value)  # type: ignore[operator]
    assert_unverifiable(normalize(value), reason)


def test_result_key_set_is_exact() -> None:
    missing = result()
    missing.pop("locator")
    unknown = result()
    unknown["extra"] = "x"
    assert_unverifiable(normalize(envelope(results=(missing,))), "missing_field")
    assert_unverifiable(normalize(envelope(results=(unknown,))), "unknown_field")


def test_material_key_set_is_declared_and_missing_declared_fields_are_allowed() -> None:
    partial = result(material={"display_state": "active"})
    unknown = result(material={"display_state": "active", "not_declared": "x"})
    assert normalize(envelope(results=(partial,))).status is SourceStatus.COMPLETED
    assert_unverifiable(normalize(envelope(results=(unknown,))), "unknown_field")


@pytest.mark.parametrize(
    ("field_value", "reason"),
    [
        (True, "invalid_field_type"),
        (False, "invalid_field_type"),
        (1.0, "unsupported_value_type"),
        (None, "invalid_field_type"),
        ([], "invalid_field_type"),
    ],
)
def test_envelope_field_types_are_checked(field_value: object, reason: str) -> None:
    value = envelope()
    value["contract_version"] = field_value
    check = normalize(value)
    assert_unverifiable(check, reason)


def test_boolean_is_a_boolean_material_value_not_an_integer() -> None:
    check = normalize(envelope(results=(result(material={"display_state": True}),)))
    assert check.status is SourceStatus.COMPLETED
    assert check.observations[0].material.items == (("display_state", True),)


def test_trusted_integer_fields_reject_booleans() -> None:
    source = replace(SOURCE_R2_A, schema_version=True)
    with pytest.raises(R1Error):
        context(source=source)
    with pytest.raises(R1Error):
        context(diagnostics=DiagnosticMetadata("synthetic-time", duration_ms=True))
    with pytest.raises(R1Error):
        context(diagnostics=DiagnosticMetadata("synthetic-time", retry_count=True))


@pytest.mark.parametrize(
    "value",
    [
        result(finding_key=""),
        result(finding_key="e\u0301"),
        result(finding_key="x" * (MAX_STRING_LENGTH + 1)),
    ],
)
def test_required_payload_strings_are_nonempty_nfc_and_bounded(
    value: dict[str, object],
) -> None:
    assert_unverifiable(normalize(envelope(results=(value,))), "invalid_string")


def test_required_payload_string_exact_length_boundary_is_accepted() -> None:
    check = normalize(envelope(results=(result(finding_key="x" * MAX_STRING_LENGTH),)))
    assert check.status is SourceStatus.COMPLETED


def test_surrogate_escaped_string_is_rejected() -> None:
    raw = (
        b'{"contract_version":"fixture-response/1",'
        b'"source_id":"synthetic-source-a","outcome":"completed",'
        b'"results":[{"finding_key":"finding-a",'
        b'"kind":"synthetic-profile","locator":"locator-a",'
        b'"material":{"display_state":"\\ud800"}}]}'
    )
    assert_unverifiable(normalize_response(raw, context()), "invalid_string")


def test_unsupported_material_types_are_rejected() -> None:
    float_value = normalize(
        envelope(results=(result(material={"display_state": 1.5}),))
    )
    nested_object = normalize(
        envelope(results=(result(material={"display_state": {"nested": "x"}}),))
    )
    scalar_set_like = normalize(
        envelope(results=(result(material={"labels": "not-an-array"}),))
    )
    duplicate_set_member = normalize(
        envelope(results=(result(material={"labels": ["same", "same"]}),))
    )
    assert_unverifiable(float_value, "unsupported_value_type")
    assert_unverifiable(nested_object, "unsupported_value_type")
    assert_unverifiable(scalar_set_like, "invalid_field_type")
    assert_unverifiable(duplicate_set_member, "malformed_result")


def test_result_count_boundary() -> None:
    accepted = tuple(
        result(finding_key=f"finding-{index}") for index in range(MAX_RESULTS)
    )
    rejected = accepted + (result(finding_key="finding-over"),)
    assert len(accepted) == MAX_RESULTS
    assert normalize(envelope(results=accepted)).status is SourceStatus.COMPLETED
    assert_unverifiable(normalize(envelope(results=rejected)), "too_many_results")


def test_nested_array_count_boundary() -> None:
    accepted_labels = [f"label-{index}" for index in range(MAX_ARRAY_ITEMS)]
    rejected_labels = accepted_labels + ["label-over"]
    accepted = normalize(
        envelope(results=(result(material={"labels": accepted_labels}),))
    )
    rejected = normalize(
        envelope(results=(result(material={"labels": rejected_labels}),))
    )
    assert accepted.status is SourceStatus.COMPLETED
    assert_unverifiable(rejected, "collection_too_large")


def test_object_member_count_boundary() -> None:
    fields = {f"material-{index}": f"value-{index}" for index in range(16)}
    source = SourceIdentity(
        source_id="synthetic-wide-source",
        canonical_scope=("synthetic-scope-v1",),
        adapter_id="synthetic-r2-adapter",
        adapter_version="1.0",
        schema_version=1,
        normalization_version=1,
        material_fields=frozenset(fields),
    )
    accepted = normalize(
        envelope(source_id=source.source_id, results=(result(material=fields),)),
        source=source,
    )
    too_many = dict(fields)
    too_many["material-over"] = "value-over"
    rejected = normalize(
        envelope(source_id=source.source_id, results=(result(material=too_many),)),
        source=source,
    )
    assert len(fields) == MAX_OBJECT_MEMBERS
    assert accepted.status is SourceStatus.COMPLETED
    assert_unverifiable(rejected, "collection_too_large")


def _nested_array(levels: int) -> object:
    value: object = "leaf"
    for _ in range(levels):
        value = [value]
    return value


def test_nesting_depth_boundary() -> None:
    accepted = normalize(
        envelope(results=(result(material={"ordered": _nested_array(5)}),))
    )
    rejected = normalize(
        envelope(results=(result(material={"ordered": _nested_array(6)}),))
    )
    assert accepted.status is SourceStatus.COMPLETED
    assert_unverifiable(rejected, "nesting_too_deep")
    assert MAX_NESTING_DEPTH == 8


def test_trusted_diagnostic_boundaries_are_enforced() -> None:
    accepted = context(
        diagnostics=DiagnosticMetadata(
            recorded_at="t" * MAX_STRING_LENGTH,
            duration_ms=MAX_DIAGNOSTIC_DURATION_MS,
            retry_count=MAX_RETRY_COUNT,
            text="d" * MAX_DIAGNOSTIC_TEXT,
        )
    )
    assert accepted.diagnostics.duration_ms == MAX_DIAGNOSTIC_DURATION_MS
    assert accepted.diagnostics.retry_count == MAX_RETRY_COUNT
    with pytest.raises(R1Error):
        context(
            diagnostics=DiagnosticMetadata(
                "t", duration_ms=MAX_DIAGNOSTIC_DURATION_MS + 1
            )
        )
    with pytest.raises(R1Error):
        context(diagnostics=DiagnosticMetadata("t", retry_count=MAX_RETRY_COUNT + 1))
    with pytest.raises(R1Error):
        context(
            diagnostics=DiagnosticMetadata("t", text="d" * (MAX_DIAGNOSTIC_TEXT + 1))
        )


@pytest.mark.parametrize("outcome", ["failed", "unverifiable"])
def test_explicit_failed_and_unverifiable_empty_responses_guard_in_r1(
    outcome: str,
) -> None:
    check = normalize(envelope(outcome=outcome))
    expected_status = (
        SourceStatus.FAILED if outcome == "failed" else SourceStatus.UNVERIFIABLE
    )
    expected_reason = f"response_{outcome}"
    assert check.status is expected_status
    assert check.reason_codes == (expected_reason,)
    report = compare_scans(
        None, normalize_scan("scan-guard", envelope(outcome=outcome))
    )
    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.guarding_events[0].current_status is expected_status


def test_incomplete_always_maps_to_unverifiable_and_discards_candidates() -> None:
    check = normalize(envelope(outcome="incomplete", results=(result(),)))
    assert_unverifiable(check, "response_incomplete")
    assert "response_outcome_mismatch" in check.reason_codes
    assert "partial_candidates_discarded" in check.reason_codes
    assert "finding-a" not in repr(check)


@pytest.mark.parametrize("outcome", ["failed", "unverifiable"])
def test_noncompleted_candidates_are_never_accepted(outcome: str) -> None:
    check = normalize(envelope(outcome=outcome, results=(result(),)))
    assert_unverifiable(check, f"response_{outcome}")
    assert "response_outcome_mismatch" in check.reason_codes
    assert "partial_candidates_discarded" in check.reason_codes


def test_exact_duplicate_results_are_deduplicated_after_normalization() -> None:
    first = result()
    second = result(
        material={
            "labels": ["beta", "alpha"],
            "display_state": "active",
            "ordered": ["first", "second"],
        }
    )
    check = normalize(envelope(results=(first, second)))
    assert check.status is SourceStatus.COMPLETED
    assert len(check.observations) == 1
    assert check.reason_codes == ("duplicate_finding_key_deduplicated",)


def test_conflicting_duplicate_results_invalidate_the_entire_response() -> None:
    first = result()
    second = result(material={"display_state": "changed"})
    check = normalize(envelope(results=(first, second)))
    assert_unverifiable(check, "conflicting_duplicate_finding_key")
    assert check.observations == ()


def test_object_and_result_order_do_not_change_normalized_results() -> None:
    first = envelope(
        results=(
            result("finding-b"),
            result("finding-a"),
        )
    )
    second = {
        "results": [
            {
                "material": {
                    "ordered": ["first", "second"],
                    "labels": ["beta", "alpha"],
                    "display_state": "active",
                },
                "locator": "locator-a",
                "kind": "synthetic-profile",
                "finding_key": "finding-a",
            },
            result("finding-b"),
        ],
        "outcome": "completed",
        "source_id": "synthetic-source-a",
        "contract_version": "fixture-response/1",
    }
    left = normalize(first)
    right = normalize(second)
    assert left.observations == right.observations


def test_ordered_material_lists_remain_material() -> None:
    baseline = normalize_scan(
        "scan-order-a",
        envelope(results=(result(material={"ordered": ["first", "second"]}),)),
    )
    current = normalize_scan(
        "scan-order-b",
        envelope(results=(result(material={"ordered": ["second", "first"]}),)),
    )
    report = compare_scans(baseline, current)
    assert report.comparisons[0].kind is ComparisonKind.CHANGED
    assert report.exposure_events[0].kind is ExposureKind.CHANGED


def test_diagnostics_do_not_change_observation_fingerprints() -> None:
    value = envelope(results=(result(),))
    first = normalize_response(
        payload(value),
        context(
            scan_id="scan-diagnostic-a",
            source_check_id="check-diagnostic-a",
            diagnostics=DiagnosticMetadata(
                "synthetic-time-a", duration_ms=1, retry_count=0, text="first"
            ),
        ),
    )
    second = normalize_response(
        payload(value),
        context(
            scan_id="scan-diagnostic-b",
            source_check_id="check-diagnostic-b",
            diagnostics=DiagnosticMetadata(
                "synthetic-time-b", duration_ms=2, retry_count=1, text="second"
            ),
        ),
    )
    assert first.observations == second.observations
    assert first.diagnostics != second.diagnostics


def test_adapter_returns_only_an_r1_source_check() -> None:
    check = normalize(envelope(results=(result(),)))
    assert type(check) is SourceCheck
    assert not hasattr(check, "comparisons")
    assert not hasattr(check, "exposure_events")
    assert not hasattr(check, "guarding_events")


def test_r1_baseline_new_and_disappearance_integrations() -> None:
    baseline = normalize_scan("scan-baseline", envelope(results=(result(),)))
    assert compare_scans(None, baseline).baseline_created_sources == (
        SOURCE_R2_A.source_id,
    )

    new_current = normalize_scan(
        "scan-new",
        envelope(results=(result(), result("finding-b"))),
    )
    new_report = compare_scans(baseline, new_current)
    assert any(item.kind is ComparisonKind.NEW for item in new_report.comparisons)
    assert any(item.kind is ExposureKind.NEW for item in new_report.exposure_events)

    empty_current = normalize_scan("scan-empty", envelope())
    disappearance = compare_scans(baseline, empty_current)
    assert disappearance.comparisons[0].kind is ComparisonKind.DISAPPEARED
    assert disappearance.exposure_events[0].kind is ExposureKind.DISAPPEARED


def test_r1_guarding_integration_never_becomes_disappearance() -> None:
    baseline = normalize_scan("scan-guard-baseline", envelope(results=(result(),)))
    current = normalize_scan("scan-guard-current", envelope(outcome="incomplete"))
    report = compare_scans(baseline, current)
    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.guarding_events[0].current_status is SourceStatus.UNVERIFIABLE
    assert report.exposure_events == ()


def test_completed_source_remains_comparable_in_incomplete_aggregate() -> None:
    baseline_a = normalize_response(
        payload(envelope(results=(result(),))),
        context(
            scan_id="aggregate-baseline", source_check_id="check-a", source=SOURCE_R2_A
        ),
    )
    baseline_b = normalize_response(
        payload(envelope(source_id=SOURCE_R2_B.source_id, results=(result(),))),
        context(
            scan_id="aggregate-baseline", source_check_id="check-b", source=SOURCE_R2_B
        ),
    )
    current_a = normalize_response(
        payload(envelope(results=(result(),))),
        context(
            scan_id="aggregate-current", source_check_id="check-a", source=SOURCE_R2_A
        ),
    )
    current_b = normalize_response(
        payload(envelope(source_id=SOURCE_R2_B.source_id, outcome="incomplete")),
        context(
            scan_id="aggregate-current", source_check_id="check-b", source=SOURCE_R2_B
        ),
    )
    baseline_plan = ScanPlan.create(
        subject_ref="subject-r2-a", sources=(SOURCE_R2_A, SOURCE_R2_B)
    )
    current_plan = ScanPlan.create(
        subject_ref="subject-r2-a", sources=(SOURCE_R2_A, SOURCE_R2_B)
    )
    baseline = ScanAttempt.create(
        scan_id="aggregate-baseline",
        plan=baseline_plan,
        source_checks=(baseline_a, baseline_b),
    )
    current = ScanAttempt.create(
        scan_id="aggregate-current",
        plan=current_plan,
        source_checks=(current_a, current_b),
    )
    report = compare_scans(baseline, current)
    assert current.outcome is AggregateOutcome.INCOMPLETE
    assert any(
        item.source_id == SOURCE_R2_A.source_id
        and item.kind is ComparisonKind.UNCHANGED
        for item in report.comparisons
    )
    assert any(
        event.source_id == SOURCE_R2_B.source_id
        and event.current_status is SourceStatus.UNVERIFIABLE
        for event in report.guarding_events
    )


def test_identity_and_version_incompatibility_stays_in_r1_comparison() -> None:
    changed_source = replace(SOURCE_R2_A, adapter_version="2.0")
    baseline = normalize_scan(
        "scan-identity-baseline", envelope(results=(result(),)), source=SOURCE_R2_A
    )
    current = normalize_scan(
        "scan-identity-current",
        envelope(results=(result(),)),
        source=changed_source,
    )
    report = compare_scans(baseline, current)
    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.comparisons[0].reason_codes == ("adapter_version_mismatch",)
    assert report.exposure_events == ()


@pytest.mark.parametrize(
    ("field_name", "changed_value", "reason"),
    [
        ("adapter_id", "other-r2-adapter", "adapter_id_mismatch"),
        ("schema_version", 2, "schema_version_mismatch"),
        ("normalization_version", 2, "normalization_version_mismatch"),
        ("canonical_scope", ("other-scope-v1",), "canonical_scope_mismatch"),
    ],
)
def test_each_remaining_r1_identity_mismatch_stays_non_comparable(
    field_name: str, changed_value: object, reason: str
) -> None:
    if field_name == "adapter_id":
        assert isinstance(changed_value, str)
        changed_source = replace(SOURCE_R2_A, adapter_id=changed_value)
    elif field_name == "schema_version":
        assert type(changed_value) is int
        changed_source = replace(SOURCE_R2_A, schema_version=changed_value)
    elif field_name == "normalization_version":
        assert type(changed_value) is int
        changed_source = replace(SOURCE_R2_A, normalization_version=changed_value)
    else:
        changed_source = replace(
            SOURCE_R2_A,
            canonical_scope=cast(tuple[str, ...], changed_value),
        )
    baseline = normalize_scan(
        "scan-identity-baseline",
        envelope(results=(result(),)),
        source=SOURCE_R2_A,
    )
    current = normalize_scan(
        "scan-identity-current",
        envelope(results=(result(),)),
        source=changed_source,
    )
    report = compare_scans(baseline, current)
    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.comparisons[0].reason_codes == (reason,)


def test_subject_isolation_is_enforced_by_r1() -> None:
    baseline = normalize_scan(
        "scan-subject-a", envelope(results=(result(),)), subject_ref="subject-r2-a"
    )
    current = normalize_scan(
        "scan-subject-b", envelope(results=()), subject_ref="subject-r2-b"
    )
    report = compare_scans(baseline, current)
    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.comparisons[0].reason_codes == ("subject_ref_mismatch",)
    assert report.exposure_events == ()


def test_generated_reason_codes_are_fixed_and_bounded() -> None:
    check = normalize(envelope(outcome="incomplete", results=(result(),)))
    assert len(check.reason_codes) <= 8
    assert all(len(code) <= 64 for code in check.reason_codes)
    assert set(check.reason_codes) <= REASON_CODES
    assert "finding-a" not in repr(check)


def test_invalid_trusted_context_is_not_an_adapter_result() -> None:
    with pytest.raises(R1Error):
        TrustedContext(
            scan_id="scan-r2",
            source_check_id="check-r2",
            subject_ref="",
            source=SOURCE_R2_A,
        )


def test_json_object_order_is_not_reintroduced_as_material_order() -> None:
    first = normalize(
        envelope(results=(result(material={"ordered": ["first", "second"]}),))
    )
    second = normalize(
        envelope(results=(result(material={"ordered": ["first", "second"]}),))
    )
    assert first.observations == second.observations
