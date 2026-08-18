"""The in-memory, deterministic comparison model for Research Experiment R1.

This module deliberately has no I/O boundary.  It contains only immutable
records, source-contract canonicalization, and a pure comparison operation.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum


class R1Error(ValueError):
    """Base class for invalid R1 records or plans."""


class InvalidScanPlanError(R1Error):
    """Raised when a scan plan cannot describe a valid requested scope."""


class InvalidObservationError(R1Error):
    """Raised when an observation is not a valid canonical record."""


class InvalidSourceCheckError(R1Error):
    """Raised when a source check violates its status contract."""


@dataclass(frozen=True, slots=True)
class FrozenList:
    """An immutable list whose order is meaningful unless a contract sorts it."""

    values: tuple[CanonicalValue, ...]


@dataclass(frozen=True, slots=True)
class FrozenObject:
    """An immutable object with deterministic key ordering."""

    items: tuple[tuple[str, CanonicalValue], ...]


CanonicalValue = str | int | bool | None | FrozenList | FrozenObject


def _stable_key(value: CanonicalValue) -> tuple[str, str]:
    """Return an ordering key independent of hash randomization."""

    return (type(value).__name__, repr(value))


def _validate_text(value: str, field_name: str) -> str:
    if not value:
        raise R1Error(f"{field_name} must not be empty")
    if unicodedata.normalize("NFC", value) != value:
        raise R1Error(f"{field_name} must be NFC-normalized")
    return value


def _canonical_value(value: object) -> CanonicalValue:
    if value is None or isinstance(value, (bool, int, str)):
        if isinstance(value, str):
            _validate_text(value, "string value")
        return value
    if isinstance(value, float):
        raise InvalidObservationError("floating-point values are not supported")
    if isinstance(value, (list, tuple)):
        return FrozenList(tuple(_canonical_value(item) for item in value))
    if isinstance(value, Mapping):
        items: list[tuple[str, CanonicalValue]] = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise InvalidObservationError("object keys must be strings")
            _validate_text(key, "object key")
            items.append((key, _canonical_value(item)))
        return FrozenObject(tuple(sorted(items, key=lambda pair: pair[0])))
    raise InvalidObservationError(f"unsupported value type: {type(value).__name__}")


def _canonical_material(
    material: Mapping[str, object],
    set_like_fields: frozenset[str],
    material_fields: frozenset[str],
) -> FrozenObject:
    items: list[tuple[str, CanonicalValue]] = []
    for key, raw_value in material.items():
        _validate_text(key, "material field")
        if key not in material_fields:
            raise InvalidObservationError(f"undeclared material field: {key}")
        if key in set_like_fields:
            if not isinstance(raw_value, (list, tuple)):
                raise InvalidObservationError(
                    f"set-like field {key!r} must be a list or tuple"
                )
            values = [_canonical_value(item) for item in raw_value]
            values.sort(key=_stable_key)
            if any(
                left == right for left, right in zip(values, values[1:], strict=False)
            ):
                raise InvalidObservationError(
                    f"set-like field {key!r} contains duplicate values"
                )
            canonical: CanonicalValue = FrozenList(tuple(values))
        else:
            canonical = _canonical_value(raw_value)
        items.append((key, canonical))
    return FrozenObject(tuple(sorted(items, key=lambda pair: pair[0])))


def _canonical_context(context: Mapping[str, object] | None) -> FrozenObject:
    if context is None:
        return FrozenObject(())
    value = _canonical_value(context)
    if not isinstance(value, FrozenObject):
        raise InvalidObservationError("context must be an object")
    return value


def _object_dict(value: FrozenObject) -> dict[str, CanonicalValue]:
    return dict(value.items)


def _changed_paths(
    before: CanonicalValue, after: CanonicalValue, prefix: str = ""
) -> list[str]:
    if isinstance(before, FrozenObject) and isinstance(after, FrozenObject):
        before_items = _object_dict(before)
        after_items = _object_dict(after)
        paths: list[str] = []
        for key in sorted(set(before_items) | set(after_items)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in before_items or key not in after_items:
                paths.append(path)
            else:
                paths.extend(_changed_paths(before_items[key], after_items[key], path))
        return paths
    if before != after:
        return [prefix]
    return []


class SourceStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    UNVERIFIABLE = "unverifiable"


class AggregateOutcome(StrEnum):
    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
    FAILED = "failed"


class ComparisonKind(StrEnum):
    NEW = "new"
    UNCHANGED = "unchanged"
    CHANGED = "changed"
    DISAPPEARED = "disappeared"
    NOT_COMPARABLE = "not_comparable"


class GuardKind(StrEnum):
    FAILED = "guarding_failed"
    UNVERIFIABLE = "guarding_unverifiable"


class ExposureKind(StrEnum):
    NEW = "exposure-new"
    CHANGED = "exposure-changed"
    DISAPPEARED = "exposure-disappeared"


def _sorted_unique(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    canonical = tuple(sorted(values))
    if any(not value for value in canonical):
        raise R1Error(f"{field_name} cannot contain empty values")
    if any(
        left == right for left, right in zip(canonical, canonical[1:], strict=False)
    ):
        raise R1Error(f"{field_name} must be unique")
    return canonical


@dataclass(frozen=True, slots=True)
class SourceIdentity:
    """The exact source identity required for comparability."""

    source_id: str
    canonical_scope: tuple[str, ...]
    adapter_id: str
    adapter_version: str
    schema_version: int
    normalization_version: int
    set_like_fields: frozenset[str] = field(default_factory=frozenset)
    material_fields: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _validate_text(self.source_id, "source_id")
        _validate_text(self.adapter_id, "adapter_id")
        _validate_text(self.adapter_version, "adapter_version")
        if self.schema_version < 1 or self.normalization_version < 1:
            raise R1Error("schema and normalization versions must be positive")
        object.__setattr__(
            self,
            "canonical_scope",
            _sorted_unique(self.canonical_scope, "canonical_scope"),
        )
        object.__setattr__(
            self,
            "set_like_fields",
            frozenset(_sorted_unique(self.set_like_fields, "set_like_fields")),
        )
        object.__setattr__(
            self,
            "material_fields",
            frozenset(_sorted_unique(self.material_fields, "material_fields")),
        )
        if not self.set_like_fields <= self.material_fields:
            raise R1Error("set-like fields must be declared material fields")

    def observation(
        self,
        *,
        finding_key: str,
        kind: str,
        locator: str,
        material: Mapping[str, object],
        context: Mapping[str, object] | None = None,
    ) -> Observation:
        """Create a canonical observation under this source contract."""

        return Observation(
            finding_key=_validate_text(finding_key, "finding_key"),
            kind=_validate_text(kind, "kind"),
            locator=_validate_text(locator, "locator"),
            material=_canonical_material(
                material, self.set_like_fields, self.material_fields
            ),
            context=_canonical_context(context),
            set_like_fields=self.set_like_fields,
            material_fields=self.material_fields,
        )


@dataclass(frozen=True, slots=True)
class ScanPlan:
    """An immutable non-empty declared source scope."""

    subject_ref: str
    sources: tuple[SourceIdentity, ...]
    execution_order: tuple[str, ...]

    @classmethod
    def create(
        cls,
        *,
        subject_ref: str,
        sources: Iterable[SourceIdentity],
        execution_order: Iterable[str] | None = None,
    ) -> ScanPlan:
        source_tuple = tuple(sources)
        if not source_tuple:
            raise InvalidScanPlanError("declared scope must not be empty")
        order = (
            tuple(execution_order)
            if execution_order is not None
            else tuple(source.source_id for source in source_tuple)
        )
        return cls(subject_ref, source_tuple, order)

    def __post_init__(self) -> None:
        _validate_text(self.subject_ref, "subject_ref")
        if not self.sources:
            raise InvalidScanPlanError("declared scope must not be empty")
        source_ids = [source.source_id for source in self.sources]
        if len(set(source_ids)) != len(source_ids):
            raise InvalidScanPlanError("a plan cannot declare a source twice")
        object.__setattr__(
            self, "sources", tuple(sorted(self.sources, key=lambda s: s.source_id))
        )
        if any(not item for item in self.execution_order):
            raise InvalidScanPlanError("execution_order cannot contain empty values")


@dataclass(frozen=True, slots=True)
class DiagnosticMetadata:
    """Bounded synthetic diagnostic information excluded from fingerprints."""

    recorded_at: str
    duration_ms: int = 0
    retry_count: int = 0
    text: str = ""

    def __post_init__(self) -> None:
        _validate_text(self.recorded_at, "recorded_at")
        if self.duration_ms < 0 or self.retry_count < 0:
            raise R1Error("diagnostic counters cannot be negative")


@dataclass(frozen=True, slots=True)
class Observation:
    """An immutable source observation with separate non-material context."""

    finding_key: str
    kind: str
    locator: str
    material: FrozenObject
    context: FrozenObject
    set_like_fields: frozenset[str]
    material_fields: frozenset[str]


@dataclass(frozen=True, slots=True)
class SourceCheck:
    """A terminal source result; only completed checks may contain observations."""

    source_check_id: str
    scan_id: str
    subject_ref: str
    source: SourceIdentity
    status: SourceStatus
    observations: tuple[Observation, ...] = ()
    reason_codes: tuple[str, ...] = ()
    diagnostics: DiagnosticMetadata = field(
        default_factory=lambda: DiagnosticMetadata("synthetic-time")
    )

    @classmethod
    def completed(
        cls,
        *,
        source_check_id: str,
        scan_id: str,
        subject_ref: str,
        source: SourceIdentity,
        observations: Iterable[Observation] = (),
        reason_codes: Iterable[str] = (),
        diagnostics: DiagnosticMetadata | None = None,
    ) -> SourceCheck:
        return cls(
            source_check_id=source_check_id,
            scan_id=scan_id,
            subject_ref=subject_ref,
            source=source,
            status=SourceStatus.COMPLETED,
            observations=tuple(observations),
            reason_codes=tuple(reason_codes),
            diagnostics=diagnostics or DiagnosticMetadata("synthetic-time"),
        )

    @classmethod
    def failed(
        cls,
        *,
        source_check_id: str,
        scan_id: str,
        subject_ref: str,
        source: SourceIdentity,
        reason_codes: Iterable[str],
        diagnostics: DiagnosticMetadata | None = None,
    ) -> SourceCheck:
        return cls._guarded(
            source_check_id=source_check_id,
            scan_id=scan_id,
            subject_ref=subject_ref,
            source=source,
            status=SourceStatus.FAILED,
            reason_codes=reason_codes,
            diagnostics=diagnostics,
        )

    @classmethod
    def unverifiable(
        cls,
        *,
        source_check_id: str,
        scan_id: str,
        subject_ref: str,
        source: SourceIdentity,
        reason_codes: Iterable[str],
        diagnostics: DiagnosticMetadata | None = None,
    ) -> SourceCheck:
        return cls._guarded(
            source_check_id=source_check_id,
            scan_id=scan_id,
            subject_ref=subject_ref,
            source=source,
            status=SourceStatus.UNVERIFIABLE,
            reason_codes=reason_codes,
            diagnostics=diagnostics,
        )

    @classmethod
    def _guarded(
        cls,
        *,
        source_check_id: str,
        scan_id: str,
        subject_ref: str,
        source: SourceIdentity,
        status: SourceStatus,
        reason_codes: Iterable[str],
        diagnostics: DiagnosticMetadata | None,
    ) -> SourceCheck:
        return cls(
            source_check_id=source_check_id,
            scan_id=scan_id,
            subject_ref=subject_ref,
            source=source,
            status=status,
            reason_codes=tuple(reason_codes),
            diagnostics=diagnostics or DiagnosticMetadata("synthetic-time"),
        )

    def __post_init__(self) -> None:
        _validate_text(self.source_check_id, "source_check_id")
        _validate_text(self.scan_id, "scan_id")
        _validate_text(self.subject_ref, "subject_ref")
        if self.status is not SourceStatus.COMPLETED and not self.reason_codes:
            raise InvalidSourceCheckError(
                "failed and unverifiable checks require a reason code"
            )
        reason_codes = _sorted_unique(self.reason_codes, "reason_codes")
        object.__setattr__(self, "reason_codes", reason_codes)
        ordered = tuple(sorted(self.observations, key=lambda item: item.finding_key))
        if len({item.finding_key for item in ordered}) != len(ordered):
            raise InvalidSourceCheckError("finding_key values must be unique")
        if self.status is not SourceStatus.COMPLETED and ordered:
            raise InvalidSourceCheckError(
                "failed or unverifiable checks cannot contain observations"
            )
        for observation in ordered:
            if (
                observation.set_like_fields != self.source.set_like_fields
                or observation.material_fields != self.source.material_fields
            ):
                raise InvalidSourceCheckError(
                    "observation contract does not match source contract"
                )
        object.__setattr__(self, "observations", ordered)


@dataclass(frozen=True, slots=True)
class ScanAttempt:
    """An immutable aggregate of terminal source checks for one plan."""

    scan_id: str
    plan: ScanPlan
    source_checks: tuple[SourceCheck, ...]
    outcome: AggregateOutcome

    @classmethod
    def create(
        cls,
        *,
        scan_id: str,
        plan: ScanPlan,
        source_checks: Iterable[SourceCheck],
    ) -> ScanAttempt:
        checks_by_source: dict[str, SourceCheck] = {}
        for check in source_checks:
            if check.source.source_id in checks_by_source:
                raise InvalidSourceCheckError("a source has more than one check")
            if check.scan_id != scan_id:
                raise InvalidSourceCheckError("source check scan_id does not match")
            if check.subject_ref != plan.subject_ref:
                raise InvalidSourceCheckError(
                    "source check subject does not match plan"
                )
            declared = {source.source_id: source for source in plan.sources}
            if check.source.source_id not in declared:
                raise InvalidSourceCheckError("source check is outside declared scope")
            if check.source != declared[check.source.source_id]:
                raise InvalidSourceCheckError(
                    "source check identity does not match plan"
                )
            checks_by_source[check.source.source_id] = check

        for source in plan.sources:
            if source.source_id not in checks_by_source:
                checks_by_source[source.source_id] = SourceCheck.failed(
                    source_check_id=f"{scan_id}:{source.source_id}:missing",
                    scan_id=scan_id,
                    subject_ref=plan.subject_ref,
                    source=source,
                    reason_codes=("missing_source_check",),
                    diagnostics=DiagnosticMetadata(
                        "synthetic-time", text="missing terminal source check"
                    ),
                )
        ordered = tuple(checks_by_source[key] for key in sorted(checks_by_source))
        statuses = {check.status for check in ordered}
        completed_count = sum(
            check.status is SourceStatus.COMPLETED for check in ordered
        )
        if completed_count == len(ordered):
            outcome = AggregateOutcome.COMPLETED
        elif completed_count:
            outcome = AggregateOutcome.INCOMPLETE
        else:
            outcome = AggregateOutcome.FAILED
        if not statuses:
            raise InvalidScanPlanError("a scan requires a non-empty declared scope")
        return cls(scan_id, plan, ordered, outcome)

    def __post_init__(self) -> None:
        _validate_text(self.scan_id, "scan_id")

    def check_for(self, source_id: str) -> SourceCheck | None:
        return next(
            (
                check
                for check in self.source_checks
                if check.source.source_id == source_id
            ),
            None,
        )


@dataclass(frozen=True, slots=True)
class ComparisonResult:
    """A comparison classification and its non-material reason codes."""

    comparison_id: str
    subject_ref: str
    source_id: str
    baseline_scan_id: str | None
    current_scan_id: str
    finding_key: str | None
    kind: ComparisonKind
    changed_field_paths: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExposureEvent:
    """A bark derived only from a comparable material comparison."""

    comparison_id: str
    subject_ref: str
    source_id: str
    finding_key: str
    kind: ExposureKind
    changed_field_paths: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class GuardingEvent:
    """A non-exposure event explaining why a source could not be guarded."""

    guard_id: str
    subject_ref: str
    source_id: str
    baseline_scan_id: str | None
    current_scan_id: str
    guard_kind: GuardKind
    prior_status: SourceStatus | None
    current_status: SourceStatus
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ComparisonReport:
    """Pure comparator output with separate result and event collections."""

    baseline_created_sources: tuple[str, ...]
    comparisons: tuple[ComparisonResult, ...]
    exposure_events: tuple[ExposureEvent, ...]
    guarding_events: tuple[GuardingEvent, ...]


def _identity_reasons(baseline: SourceCheck, current: SourceCheck) -> tuple[str, ...]:
    reasons: list[str] = []
    if baseline.subject_ref != current.subject_ref:
        reasons.append("subject_ref_mismatch")
    if baseline.source.source_id != current.source.source_id:
        reasons.append("source_id_mismatch")
    if baseline.source.canonical_scope != current.source.canonical_scope:
        reasons.append("canonical_scope_mismatch")
    if baseline.source.adapter_id != current.source.adapter_id:
        reasons.append("adapter_id_mismatch")
    if baseline.source.adapter_version != current.source.adapter_version:
        reasons.append("adapter_version_mismatch")
    if baseline.source.schema_version != current.source.schema_version:
        reasons.append("schema_version_mismatch")
    if baseline.source.normalization_version != current.source.normalization_version:
        reasons.append("normalization_version_mismatch")
    if baseline.source.set_like_fields != current.source.set_like_fields:
        reasons.append("material_policy_mismatch")
    if baseline.source.material_fields != current.source.material_fields:
        reasons.append("material_policy_mismatch")
    if baseline.status is not SourceStatus.COMPLETED:
        reasons.append("baseline_not_completed")
    if current.status is not SourceStatus.COMPLETED:
        reasons.append("current_not_completed")
    return _sorted_unique(reasons, "reason_codes")


def _comparison_id(
    current: ScanAttempt, source_id: str, finding_key: str | None, kind: ComparisonKind
) -> str:
    key = finding_key if finding_key is not None else "source"
    return f"{current.scan_id}:{source_id}:{key}:{kind.value}"


def _result(
    *,
    baseline: ScanAttempt | None,
    current: ScanAttempt,
    check: SourceCheck,
    kind: ComparisonKind,
    finding_key: str | None = None,
    changed_field_paths: Iterable[str] = (),
    reason_codes: Iterable[str] = (),
) -> ComparisonResult:
    return ComparisonResult(
        comparison_id=_comparison_id(
            current, check.source.source_id, finding_key, kind
        ),
        subject_ref=check.subject_ref,
        source_id=check.source.source_id,
        baseline_scan_id=baseline.scan_id if baseline is not None else None,
        current_scan_id=current.scan_id,
        finding_key=finding_key,
        kind=kind,
        changed_field_paths=_sorted_unique(changed_field_paths, "changed_field_paths"),
        reason_codes=_sorted_unique(reason_codes, "reason_codes"),
    )


def _guard(
    *, baseline: ScanAttempt | None, current: ScanAttempt, check: SourceCheck
) -> GuardingEvent:
    guard_kind = (
        GuardKind.FAILED
        if check.status is SourceStatus.FAILED
        else GuardKind.UNVERIFIABLE
    )
    prior = baseline.check_for(check.source.source_id) if baseline is not None else None
    return GuardingEvent(
        guard_id=f"{current.scan_id}:{check.source.source_id}:{guard_kind.value}",
        subject_ref=check.subject_ref,
        source_id=check.source.source_id,
        baseline_scan_id=baseline.scan_id if baseline is not None else None,
        current_scan_id=current.scan_id,
        guard_kind=guard_kind,
        prior_status=prior.status if prior is not None else None,
        current_status=check.status,
        reason_codes=check.reason_codes,
    )


def _exposure(result: ComparisonResult) -> ExposureEvent | None:
    mapping = {
        ComparisonKind.NEW: ExposureKind.NEW,
        ComparisonKind.CHANGED: ExposureKind.CHANGED,
        ComparisonKind.DISAPPEARED: ExposureKind.DISAPPEARED,
    }
    kind = mapping.get(result.kind)
    if kind is None or result.finding_key is None:
        return None
    return ExposureEvent(
        comparison_id=result.comparison_id,
        subject_ref=result.subject_ref,
        source_id=result.source_id,
        finding_key=result.finding_key,
        kind=kind,
        changed_field_paths=result.changed_field_paths,
    )


def _compare_observations(
    *,
    baseline: ScanAttempt,
    current: ScanAttempt,
    before: SourceCheck,
    after: SourceCheck,
) -> tuple[tuple[ComparisonResult, ...], tuple[ExposureEvent, ...]]:
    before_by_key = {
        observation.finding_key: observation for observation in before.observations
    }
    after_by_key = {
        observation.finding_key: observation for observation in after.observations
    }
    results: list[ComparisonResult] = []
    for finding_key in sorted(set(before_by_key) | set(after_by_key)):
        old = before_by_key.get(finding_key)
        new = after_by_key.get(finding_key)
        if old is None:
            results.append(
                _result(
                    baseline=baseline,
                    current=current,
                    check=after,
                    kind=ComparisonKind.NEW,
                    finding_key=finding_key,
                )
            )
        elif new is None:
            results.append(
                _result(
                    baseline=baseline,
                    current=current,
                    check=after,
                    kind=ComparisonKind.DISAPPEARED,
                    finding_key=finding_key,
                )
            )
        elif old.kind != new.kind or old.locator != new.locator:
            results.append(
                _result(
                    baseline=baseline,
                    current=current,
                    check=after,
                    kind=ComparisonKind.DISAPPEARED,
                    finding_key=finding_key,
                )
            )
            results.append(
                _result(
                    baseline=baseline,
                    current=current,
                    check=after,
                    kind=ComparisonKind.NEW,
                    finding_key=finding_key,
                )
            )
        else:
            paths = _changed_paths(old.material, new.material)
            results.append(
                _result(
                    baseline=baseline,
                    current=current,
                    check=after,
                    kind=ComparisonKind.CHANGED if paths else ComparisonKind.UNCHANGED,
                    finding_key=finding_key,
                    changed_field_paths=paths,
                )
            )
    ordered = tuple(
        sorted(
            results,
            key=lambda item: (
                item.source_id,
                item.finding_key or "",
                0 if item.kind is ComparisonKind.DISAPPEARED else 1,
            ),
        )
    )
    exposures = tuple(event for event in (_exposure(item) for item in ordered) if event)
    return ordered, exposures


def compare_scans(
    baseline: ScanAttempt | None, current: ScanAttempt
) -> ComparisonReport:
    """Compare scans without mutation, I/O, persistence, or external calls."""

    baseline_by_source = (
        {check.source.source_id: check for check in baseline.source_checks}
        if baseline is not None
        else {}
    )
    comparisons: list[ComparisonResult] = []
    exposure_events: list[ExposureEvent] = []
    guarding_events: list[GuardingEvent] = []
    baseline_created: list[str] = []

    for current_check in current.source_checks:
        before = baseline_by_source.get(current_check.source.source_id)
        if current_check.status is not SourceStatus.COMPLETED:
            result = _result(
                baseline=baseline,
                current=current,
                check=current_check,
                kind=ComparisonKind.NOT_COMPARABLE,
                reason_codes=current_check.reason_codes,
            )
            comparisons.append(result)
            guarding_events.append(
                _guard(baseline=baseline, current=current, check=current_check)
            )
            continue

        if before is None and baseline is not None:
            comparisons.append(
                _result(
                    baseline=baseline,
                    current=current,
                    check=current_check,
                    kind=ComparisonKind.NOT_COMPARABLE,
                    reason_codes=("source_id_mismatch",),
                )
            )
            continue

        if before is None or before.status is not SourceStatus.COMPLETED:
            baseline_created.append(current_check.source.source_id)
            continue

        reasons = _identity_reasons(before, current_check)
        if reasons:
            comparisons.append(
                _result(
                    baseline=baseline,
                    current=current,
                    check=current_check,
                    kind=ComparisonKind.NOT_COMPARABLE,
                    reason_codes=reasons,
                )
            )
            continue

        if baseline is None:
            raise AssertionError(
                "a completed current check cannot have a baseline match"
            )
        results, exposures = _compare_observations(
            baseline=baseline,
            current=current,
            before=before,
            after=current_check,
        )
        comparisons.extend(results)
        exposure_events.extend(exposures)

    comparisons.sort(
        key=lambda item: (
            item.source_id,
            item.finding_key or "",
            0 if item.kind is ComparisonKind.DISAPPEARED else 1,
            item.kind.value,
        )
    )
    exposure_events.sort(
        key=lambda item: (
            item.source_id,
            item.finding_key,
            item.kind.value,
        )
    )
    guarding_events.sort(key=lambda item: (item.source_id, item.guard_kind.value))
    return ComparisonReport(
        baseline_created_sources=tuple(sorted(baseline_created)),
        comparisons=tuple(comparisons),
        exposure_events=tuple(exposure_events),
        guarding_events=tuple(guarding_events),
    )
