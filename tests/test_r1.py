"""Synthetic behavioural tests for Research Experiment R1."""

from dataclasses import replace

import pytest

from personal_watchdog.r1 import (
    AggregateOutcome,
    ComparisonKind,
    GuardKind,
    InvalidObservationError,
    InvalidScanPlanError,
    InvalidSourceCheckError,
    ScanPlan,
    SourceCheck,
    SourceIdentity,
    SourceStatus,
    compare_scans,
)
from tests.fixtures_r1 import (
    SOURCE_A,
    SOURCE_B,
    aggregate_scan,
    completed_scan,
    guarded_scan,
    observation,
)


def test_first_completed_scan_creates_baseline_without_bark() -> None:
    report = compare_scans(None, completed_scan("scan-001"))

    assert report.baseline_created_sources == ("fixture-source-a",)
    assert report.comparisons == ()
    assert report.exposure_events == ()
    assert report.guarding_events == ()


def test_first_completed_scan_with_observation_is_still_silent() -> None:
    current = completed_scan("scan-001", observations=(observation(),))

    report = compare_scans(None, current)

    assert report.baseline_created_sources == ("fixture-source-a",)
    assert report.exposure_events == ()


def test_identical_observation_with_set_like_reordering_is_unchanged() -> None:
    baseline = completed_scan(
        "scan-001", observations=(observation(labels=("alpha", "beta")),)
    )
    current = completed_scan(
        "scan-002", observations=(observation(labels=("beta", "alpha")),)
    )

    report = compare_scans(baseline, current)

    assert [item.kind for item in report.comparisons] == [ComparisonKind.UNCHANGED]
    assert report.exposure_events == ()


def test_new_finding_produces_one_exposure_event() -> None:
    baseline = completed_scan("scan-001")
    current = completed_scan("scan-002", observations=(observation(),))

    report = compare_scans(baseline, current)

    assert [(item.finding_key, item.kind) for item in report.comparisons] == [
        ("finding-a", ComparisonKind.NEW)
    ]
    assert [item.kind.value for item in report.exposure_events] == ["exposure-new"]


def test_material_change_names_changed_field_and_barks() -> None:
    baseline = completed_scan("scan-001", observations=(observation(),))
    current = completed_scan(
        "scan-002", observations=(observation(display_state="removed"),)
    )

    report = compare_scans(baseline, current)

    assert report.comparisons[0].kind is ComparisonKind.CHANGED
    assert report.comparisons[0].changed_field_paths == ("display_state",)
    assert report.exposure_events[0].kind.value == "exposure-changed"


def test_timestamp_context_and_diagnostics_are_non_material() -> None:
    baseline = completed_scan(
        "scan-001",
        observations=(
            observation(context={"observed_at": "time-a", "label": "first context"}),
        ),
        reason_codes=("diagnostic-a",),
        duration_ms=1,
        retry_count=0,
        diagnostic_text="first diagnostic",
    )
    current = completed_scan(
        "scan-002",
        observations=(
            observation(context={"observed_at": "time-b", "label": "second context"}),
        ),
        reason_codes=("diagnostic-b",),
        duration_ms=999,
        retry_count=4,
        diagnostic_text="different diagnostic",
    )

    report = compare_scans(baseline, current)

    assert report.comparisons[0].kind is ComparisonKind.UNCHANGED
    assert report.exposure_events == ()
    assert report.guarding_events == ()


def test_completed_zero_observations_can_produce_disappeared() -> None:
    baseline = completed_scan("scan-001", observations=(observation(),))
    current = completed_scan("scan-002")

    report = compare_scans(baseline, current)

    assert report.comparisons[0].kind is ComparisonKind.DISAPPEARED
    assert report.exposure_events[0].kind.value == "exposure-disappeared"


def test_failed_source_is_not_comparable_and_emits_only_failed_guard() -> None:
    report = compare_scans(None, guarded_scan("scan-001", status=SourceStatus.FAILED))

    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.comparisons[0].reason_codes == ("synthetic-blocked",)
    assert report.guarding_events[0].guard_kind is GuardKind.FAILED
    assert report.guarding_events[0].baseline_scan_id is None
    assert report.exposure_events == ()


def test_unverifiable_source_is_not_comparable_and_emits_only_unverifiable_guard() -> (
    None
):
    report = compare_scans(
        None, guarded_scan("scan-001", status=SourceStatus.UNVERIFIABLE)
    )

    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.guarding_events[0].guard_kind is GuardKind.UNVERIFIABLE
    assert report.exposure_events == ()


def test_completed_source_inside_incomplete_scan_remains_comparable() -> None:
    baseline_a = SourceCheck.completed(
        source_check_id="check-base-a",
        scan_id="scan-base",
        subject_ref="subject-r1-a",
        source=SOURCE_A,
        observations=(observation(SOURCE_A),),
    )
    baseline_b = SourceCheck.completed(
        source_check_id="check-base-b",
        scan_id="scan-base",
        subject_ref="subject-r1-a",
        source=SOURCE_B,
    )
    current_a = SourceCheck.completed(
        source_check_id="check-current-a",
        scan_id="scan-current",
        subject_ref="subject-r1-a",
        source=SOURCE_A,
        observations=(observation(SOURCE_A, display_state="changed"),),
    )
    current_b = SourceCheck.unverifiable(
        source_check_id="check-current-b",
        scan_id="scan-current",
        subject_ref="subject-r1-a",
        source=SOURCE_B,
        reason_codes=("blocked",),
    )
    baseline = aggregate_scan(
        "scan-base",
        subject_ref="subject-r1-a",
        sources=(SOURCE_A, SOURCE_B),
        checks=(baseline_b, baseline_a),
    )
    current = aggregate_scan(
        "scan-current",
        subject_ref="subject-r1-a",
        sources=(SOURCE_A, SOURCE_B),
        checks=(current_b, current_a),
    )

    report = compare_scans(baseline, current)

    assert baseline.outcome is AggregateOutcome.COMPLETED
    assert current.outcome is AggregateOutcome.INCOMPLETE
    assert [(item.source_id, item.kind) for item in report.comparisons] == [
        ("fixture-source-a", ComparisonKind.CHANGED),
        ("fixture-source-b", ComparisonKind.NOT_COMPARABLE),
    ]
    assert report.exposure_events[0].source_id == "fixture-source-a"
    assert report.guarding_events[0].source_id == "fixture-source-b"


@pytest.mark.parametrize(
    ("field_name", "reason"),
    (
        ("subject_ref", "subject_ref_mismatch"),
        ("source_id", "source_id_mismatch"),
        ("canonical_scope", "canonical_scope_mismatch"),
        ("adapter_id", "adapter_id_mismatch"),
        ("adapter_version", "adapter_version_mismatch"),
        ("schema_version", "schema_version_mismatch"),
        ("normalization_version", "normalization_version_mismatch"),
    ),
)
def test_identity_mismatch_is_not_compared(field_name: str, reason: str) -> None:
    baseline = completed_scan("scan-001", observations=(observation(),))
    if field_name == "subject_ref":
        current = completed_scan(
            "scan-002", subject_ref="subject-r1-b", observations=(observation(),)
        )
    else:
        current_source = _mismatched_source(field_name)
        current = completed_scan(
            "scan-002",
            source_identity=current_source,
            observations=(observation(current_source),),
        )

    report = compare_scans(baseline, current)

    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert reason in report.comparisons[0].reason_codes
    assert report.exposure_events == ()


def _mismatched_source(field_name: str) -> SourceIdentity:
    if field_name == "source_id":
        return replace(SOURCE_A, source_id="fixture-source-z")
    if field_name == "canonical_scope":
        return replace(SOURCE_A, canonical_scope=("public-profile-v2",))
    if field_name == "adapter_id":
        return replace(SOURCE_A, adapter_id="fixture-adapter-z")
    if field_name == "adapter_version":
        return replace(SOURCE_A, adapter_version="2.0")
    if field_name == "schema_version":
        return replace(SOURCE_A, schema_version=2)
    if field_name == "normalization_version":
        return replace(SOURCE_A, normalization_version=2)
    raise AssertionError(f"unexpected identity field: {field_name}")


def test_failed_and_unverifiable_candidates_cannot_enter_records() -> None:
    candidate = observation()
    with pytest.raises(InvalidSourceCheckError):
        SourceCheck(
            source_check_id="check-invalid",
            scan_id="scan-invalid",
            subject_ref="subject-r1-a",
            source=SOURCE_A,
            status=SourceStatus.FAILED,
            observations=(candidate,),
            reason_codes=("timeout",),
        )


def test_undeclared_material_field_is_rejected() -> None:
    with pytest.raises(InvalidObservationError):
        SOURCE_A.observation(
            finding_key="finding-a",
            kind="synthetic-profile",
            locator="locator-finding-a",
            material={"not_declared": "value"},
        )


def test_ordered_observation_list_reordering_is_material() -> None:
    baseline = completed_scan(
        "scan-001", observations=(observation(ordered=("first", "second")),)
    )
    current = completed_scan(
        "scan-002", observations=(observation(ordered=("second", "first")),)
    )

    report = compare_scans(baseline, current)

    assert report.comparisons[0].kind is ComparisonKind.CHANGED
    assert report.comparisons[0].changed_field_paths == ("ordered",)


def test_empty_declared_scope_is_invalid_before_any_event() -> None:
    with pytest.raises(InvalidScanPlanError):
        ScanPlan.create(subject_ref="subject-r1-a", sources=())


def test_subjects_cannot_collide_on_finding_identity() -> None:
    baseline = completed_scan("scan-001", observations=(observation(),))
    current = completed_scan(
        "scan-002", subject_ref="subject-r1-b", observations=(observation(),)
    )

    report = compare_scans(baseline, current)

    assert report.comparisons[0].kind is ComparisonKind.NOT_COMPARABLE
    assert report.exposure_events == ()


def test_multiple_changes_have_one_sorted_result_per_logical_finding() -> None:
    baseline = completed_scan(
        "scan-001",
        observations=(
            observation(finding_key="finding-b"),
            observation(finding_key="finding-a"),
        ),
    )
    current = completed_scan(
        "scan-002",
        observations=(
            observation(finding_key="finding-b", display_state="changed"),
            observation(finding_key="finding-c"),
        ),
    )

    report = compare_scans(baseline, current)

    assert [(item.finding_key, item.kind) for item in report.comparisons] == [
        ("finding-a", ComparisonKind.DISAPPEARED),
        ("finding-b", ComparisonKind.CHANGED),
        ("finding-c", ComparisonKind.NEW),
    ]
    assert [item.finding_key for item in report.exposure_events] == [
        "finding-a",
        "finding-b",
        "finding-c",
    ]


def test_input_collection_order_does_not_change_output_order() -> None:
    baseline_a = SourceCheck.completed(
        source_check_id="check-base-a",
        scan_id="scan-base",
        subject_ref="subject-r1-a",
        source=SOURCE_A,
        observations=(observation(),),
    )
    baseline_b = SourceCheck.completed(
        source_check_id="check-base-b",
        scan_id="scan-base",
        subject_ref="subject-r1-a",
        source=SOURCE_B,
        observations=(observation(SOURCE_B),),
    )
    current_a = SourceCheck.completed(
        source_check_id="check-current-a",
        scan_id="scan-current",
        subject_ref="subject-r1-a",
        source=SOURCE_A,
        observations=(observation(display_state="changed"),),
    )
    current_b = SourceCheck.completed(
        source_check_id="check-current-b",
        scan_id="scan-current",
        subject_ref="subject-r1-a",
        source=SOURCE_B,
        observations=(observation(SOURCE_B),),
    )
    baseline = aggregate_scan(
        "scan-base",
        subject_ref="subject-r1-a",
        sources=(SOURCE_A, SOURCE_B),
        checks=(baseline_b, baseline_a),
    )
    current = aggregate_scan(
        "scan-current",
        subject_ref="subject-r1-a",
        sources=(SOURCE_A, SOURCE_B),
        checks=(current_b, current_a),
    )

    report = compare_scans(baseline, current)

    assert [(item.source_id, item.finding_key) for item in report.comparisons] == [
        ("fixture-source-a", "finding-a"),
        ("fixture-source-b", "finding-a"),
    ]


def test_aggregate_outcomes_distinguish_completed_incomplete_and_failed() -> None:
    completed = completed_scan("scan-completed")

    mixed = aggregate_scan(
        "scan-mixed",
        subject_ref="subject-r1-a",
        sources=(SOURCE_A, SOURCE_B),
        checks=(
            SourceCheck.completed(
                source_check_id="check-mixed-a",
                scan_id="scan-mixed",
                subject_ref="subject-r1-a",
                source=SOURCE_A,
            ),
            SourceCheck.failed(
                source_check_id="check-mixed-b",
                scan_id="scan-mixed",
                subject_ref="subject-r1-a",
                source=SOURCE_B,
                reason_codes=("timeout",),
            ),
        ),
    )
    failed_a = SourceCheck.failed(
        source_check_id="check-failed-a",
        scan_id="scan-failed-both",
        subject_ref="subject-r1-a",
        source=SOURCE_A,
        reason_codes=("timeout",),
    )
    unverifiable_b = SourceCheck.unverifiable(
        source_check_id="check-failed-b",
        scan_id="scan-failed-both",
        subject_ref="subject-r1-a",
        source=SOURCE_B,
        reason_codes=("blocked",),
    )

    assert completed.outcome is AggregateOutcome.COMPLETED
    assert mixed.outcome is AggregateOutcome.INCOMPLETE
    assert (
        aggregate_scan(
            "scan-failed-both",
            subject_ref="subject-r1-a",
            sources=(SOURCE_A, SOURCE_B),
            checks=(
                failed_a,
                unverifiable_b,
            ),
        ).outcome
        is AggregateOutcome.FAILED
    )


def test_first_failed_then_completed_creates_baseline_without_bark() -> None:
    failed = guarded_scan("scan-001", status=SourceStatus.FAILED)
    completed = completed_scan("scan-002", observations=(observation(),))

    failed_report = compare_scans(None, failed)
    completed_report = compare_scans(failed, completed)

    assert failed_report.guarding_events[0].guard_kind is GuardKind.FAILED
    assert completed_report.baseline_created_sources == ("fixture-source-a",)
    assert completed_report.comparisons == ()
    assert completed_report.exposure_events == ()
