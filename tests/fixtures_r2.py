"""Synthetic response and trusted-context helpers for the R2 experiment."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence

from personal_watchdog.r1 import (
    DiagnosticMetadata,
    ScanAttempt,
    ScanPlan,
    SourceIdentity,
)
from personal_watchdog.r2_adapter import TrustedContext, normalize_response

SOURCE_R2_A = SourceIdentity(
    source_id="synthetic-source-a",
    canonical_scope=("synthetic-scope-v1",),
    adapter_id="synthetic-r2-adapter",
    adapter_version="1.0",
    schema_version=1,
    normalization_version=1,
    set_like_fields=frozenset({"labels"}),
    material_fields=frozenset({"display_state", "labels", "ordered"}),
)
SOURCE_R2_B = SourceIdentity(
    source_id="synthetic-source-b",
    canonical_scope=("synthetic-scope-v1",),
    adapter_id="synthetic-r2-adapter",
    adapter_version="1.0",
    schema_version=1,
    normalization_version=1,
    set_like_fields=frozenset({"labels"}),
    material_fields=frozenset({"display_state", "labels", "ordered"}),
)


def result(
    finding_key: str = "finding-a",
    *,
    kind: str = "synthetic-profile",
    locator: str = "locator-a",
    material: Mapping[str, object] | None = None,
) -> dict[str, object]:
    return {
        "finding_key": finding_key,
        "kind": kind,
        "locator": locator,
        "material": dict(
            material
            if material is not None
            else {
                "display_state": "active",
                "labels": ["alpha", "beta"],
                "ordered": ["first", "second"],
            }
        ),
    }


def envelope(
    source_id: str = SOURCE_R2_A.source_id,
    *,
    outcome: str = "completed",
    results: Sequence[Mapping[str, object]] = (),
) -> dict[str, object]:
    return {
        "contract_version": "fixture-response/1",
        "source_id": source_id,
        "outcome": outcome,
        "results": [dict(item) for item in results],
    }


def payload(value: Mapping[str, object]) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def context(
    *,
    scan_id: str = "scan-r2",
    source_check_id: str = "check-r2",
    subject_ref: str = "subject-r2-a",
    source: SourceIdentity = SOURCE_R2_A,
    diagnostics: DiagnosticMetadata | None = None,
) -> TrustedContext:
    return TrustedContext(
        scan_id=scan_id,
        source_check_id=source_check_id,
        subject_ref=subject_ref,
        source=source,
        diagnostics=diagnostics or DiagnosticMetadata("synthetic-time"),
    )


def normalize_scan(
    scan_id: str,
    value: Mapping[str, object],
    *,
    subject_ref: str = "subject-r2-a",
    source: SourceIdentity = SOURCE_R2_A,
) -> ScanAttempt:
    check = normalize_response(
        payload(value),
        context(
            scan_id=scan_id,
            source_check_id=f"check-{scan_id}",
            subject_ref=subject_ref,
            source=source,
        ),
    )
    plan = ScanPlan.create(subject_ref=subject_ref, sources=(source,))
    return ScanAttempt.create(scan_id=scan_id, plan=plan, source_checks=(check,))
