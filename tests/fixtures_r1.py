"""Synthetic, non-personal records used by the R1 tests."""

from collections.abc import Iterable

from personal_watchdog.r1 import (
    DiagnosticMetadata,
    InvalidScanPlanError,
    Observation,
    ScanAttempt,
    ScanPlan,
    SourceCheck,
    SourceIdentity,
    SourceStatus,
)


def source(
    *,
    source_id: str = "fixture-source-a",
    canonical_scope: tuple[str, ...] = ("public-profile-v1",),
    adapter_id: str = "fixture-adapter",
    adapter_version: str = "1.0",
    schema_version: int = 1,
    normalization_version: int = 1,
    set_like_fields: frozenset[str] = frozenset({"labels"}),
    material_fields: frozenset[str] = frozenset({"display_state", "labels", "ordered"}),
) -> SourceIdentity:
    return SourceIdentity(
        source_id=source_id,
        canonical_scope=canonical_scope,
        adapter_id=adapter_id,
        adapter_version=adapter_version,
        schema_version=schema_version,
        normalization_version=normalization_version,
        set_like_fields=set_like_fields,
        material_fields=material_fields,
    )


SOURCE_A = source()
SOURCE_B = source(source_id="fixture-source-b", canonical_scope=("username-v1",))


def observation(
    source_identity: SourceIdentity = SOURCE_A,
    *,
    finding_key: str = "finding-a",
    display_state: str = "active",
    labels: tuple[str, ...] = ("alpha", "beta"),
    ordered: tuple[str, ...] = ("first", "second"),
    context: dict[str, object] | None = None,
) -> Observation:
    return source_identity.observation(
        finding_key=finding_key,
        kind="synthetic-profile",
        locator=f"locator-{finding_key}",
        material={
            "display_state": display_state,
            "labels": list(labels),
            "ordered": list(ordered),
        },
        context=context or {"observed_at": "synthetic-time", "label": "fixture"},
    )


def completed_scan(
    scan_id: str,
    *,
    subject_ref: str = "subject-r1-a",
    source_identity: SourceIdentity = SOURCE_A,
    observations: Iterable[Observation] = (),
    reason_codes: tuple[str, ...] = (),
    duration_ms: int = 1,
    retry_count: int = 0,
    diagnostic_text: str = "completed",
) -> ScanAttempt:
    plan = ScanPlan.create(subject_ref=subject_ref, sources=(source_identity,))
    check = SourceCheck.completed(
        source_check_id=f"check-{scan_id}-{source_identity.source_id}",
        scan_id=scan_id,
        subject_ref=subject_ref,
        source=source_identity,
        observations=observations,
        reason_codes=reason_codes,
        diagnostics=DiagnosticMetadata(
            recorded_at=f"time-{scan_id}",
            duration_ms=duration_ms,
            retry_count=retry_count,
            text=diagnostic_text,
        ),
    )
    return ScanAttempt.create(scan_id=scan_id, plan=plan, source_checks=(check,))


def guarded_scan(
    scan_id: str,
    *,
    status: SourceStatus,
    subject_ref: str = "subject-r1-a",
    source_identity: SourceIdentity = SOURCE_A,
    reason_codes: tuple[str, ...] = ("synthetic-blocked",),
    partial_diagnostic: str = "no accepted candidate",
) -> ScanAttempt:
    plan = ScanPlan.create(subject_ref=subject_ref, sources=(source_identity,))
    diagnostics = DiagnosticMetadata(
        recorded_at=f"time-{scan_id}", text=partial_diagnostic
    )
    check = (
        SourceCheck.failed(
            source_check_id=f"check-{scan_id}-{source_identity.source_id}",
            scan_id=scan_id,
            subject_ref=subject_ref,
            source=source_identity,
            reason_codes=reason_codes,
            diagnostics=diagnostics,
        )
        if status is SourceStatus.FAILED
        else SourceCheck.unverifiable(
            source_check_id=f"check-{scan_id}-{source_identity.source_id}",
            scan_id=scan_id,
            subject_ref=subject_ref,
            source=source_identity,
            reason_codes=reason_codes,
            diagnostics=diagnostics,
        )
    )
    return ScanAttempt.create(scan_id=scan_id, plan=plan, source_checks=(check,))


def aggregate_scan(
    scan_id: str,
    *,
    subject_ref: str,
    sources: tuple[SourceIdentity, ...],
    checks: tuple[SourceCheck, ...],
) -> ScanAttempt:
    if not sources:
        raise InvalidScanPlanError("fixture helper requires a non-empty scope")
    plan = ScanPlan.create(subject_ref=subject_ref, sources=sources)
    return ScanAttempt.create(scan_id=scan_id, plan=plan, source_checks=checks)
