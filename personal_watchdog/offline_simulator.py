"""A bounded, deterministic runner for the frozen R2.5 scenarios.

The runner owns only scenario parsing, scan orchestration, projections, and
literal expectation comparison.  R2 owns response interpretation and R1 owns
scan aggregation, comparisons, IDs, and events.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn, cast

from personal_watchdog.r1 import (
    AggregateOutcome,
    ComparisonKind,
    DiagnosticMetadata,
    ExposureKind,
    GuardKind,
    ScanAttempt,
    ScanPlan,
    SourceCheck,
    SourceIdentity,
    SourceStatus,
    compare_scans,
)
from personal_watchdog.r2_adapter import TrustedContext, normalize_response

SCENARIO_VERSION = "r2.5-visible-offline-simulator/1"
RUNNER_VERSION = "r2.5-visible-offline-simulator/1"
SCENARIO_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$", re.ASCII)

MAX_SCENARIO_BYTES = 262_144
MAX_SCENARIO_NESTING = 12
MAX_SOURCES = 8
MAX_SCANS = 32
MAX_CHECKS_PER_SCAN = 8
MAX_STRING_CODEPOINTS = 256
MAX_CANONICAL_SCOPE_ITEMS = 16
MAX_MATERIAL_FIELDS = 16
MAX_EXPECTED_RECORDS_PER_CHECK = 100
MAX_EXPECTED_RECORDS_PER_SCAN = 256
MAX_RESPONSE_BYTES = 65_536

_DIAGNOSTIC_MESSAGES = {
    "invalid_json": "scenario JSON is invalid",
    "duplicate_json_key": "scenario JSON contains a duplicate object key",
    "unknown_field": "scenario contains an unknown field",
    "missing_field": "scenario is missing a required field",
    "invalid_type": "scenario field has an invalid type",
    "invalid_value": "scenario field has an invalid value",
    "bounds_exceeded": "scenario exceeds a fixed safety bound",
    "reference_error": "scenario contains an invalid reference",
    "construction_error": "scenario could not construct an R1 record",
}

_STATUS_VALUES = {status.value for status in SourceStatus}
_COMPARISON_VALUES = {kind.value for kind in ComparisonKind}
_EXPOSURE_VALUES = {kind.value for kind in ExposureKind}
_GUARD_VALUES = {kind.value for kind in GuardKind}
_OUTCOME_VALUES = {outcome.value for outcome in AggregateOutcome}


class ScenarioInvalid(Exception):
    """A safe, user-facing scenario validation failure."""

    def __init__(self, code: str, path: str, message: str | None = None) -> None:
        self.code = code
        self.path = path
        self.message = message or _DIAGNOSTIC_MESSAGES[code]
        super().__init__(self.message)


class _DuplicateKey(Exception):
    pass


class _NonStandardConstant(Exception):
    pass


def _fail(code: str, path: str) -> NoReturn:
    raise ScenarioInvalid(code, path)


def _pointer(path: str, part: str) -> str:
    escaped = part.replace("~", "~0").replace("/", "~1")
    return f"/{escaped}" if not path else f"{path}/{escaped}"


def _expect_object(value: object, path: str) -> dict[str, Any]:
    if type(value) is not dict:  # noqa: E721 - JSON object validation is exact
        _fail("invalid_type", path)
    return cast(dict[str, Any], value)


def _expect_list(value: object, path: str) -> list[Any]:
    if type(value) is not list:  # noqa: E721 - JSON array validation is exact
        _fail("invalid_type", path)
    return value


def _expect_keys(value: object, expected: set[str], path: str) -> dict[str, Any]:
    obj = _expect_object(value, path)
    unknown = sorted(set(obj) - expected)
    if unknown:
        _fail("unknown_field", _pointer(path, unknown[0]))
    missing = sorted(expected - set(obj))
    if missing:
        _fail("missing_field", _pointer(path, missing[0]))
    return obj


def _exact_int(value: object, path: str, *, minimum: int, maximum: int) -> int:
    if type(value) is not int:  # noqa: E721 - booleans must not pass as integers
        _fail("invalid_type", path)
    integer = value
    if not minimum <= integer <= maximum:
        _fail("invalid_value", path)
    return integer


def _text(value: object, path: str, *, allow_empty: bool = False) -> str:
    if type(value) is not str:  # noqa: E721 - exact JSON string validation
        _fail("invalid_type", path)
    text = value
    if not allow_empty and not text:
        _fail("invalid_value", path)
    if len(text) > MAX_STRING_CODEPOINTS:
        _fail("bounds_exceeded", path)
    if any(0xD800 <= ord(character) <= 0xDFFF for character in text):
        _fail("invalid_value", path)
    if unicodedata.normalize("NFC", text) != text:
        _fail("invalid_value", path)
    return text


def _untrusted_text(value: object, path: str) -> str:
    if type(value) is not str:  # noqa: E721 - exact JSON string validation
        _fail("invalid_type", path)
    text = value
    if any(0xD800 <= ord(character) <= 0xDFFF for character in text):
        _fail("invalid_value", path)
    return text


def _string_list(
    value: object,
    path: str,
    *,
    maximum: int,
    allow_empty: bool = False,
    require_sorted_unique: bool = False,
) -> list[str]:
    values = _expect_list(value, path)
    if len(values) > maximum:
        _fail("bounds_exceeded", path)
    result = [
        _text(item, _pointer(path, str(index)), allow_empty=allow_empty)
        for index, item in enumerate(values)
    ]
    if require_sorted_unique and result != sorted(set(result)):
        _fail("invalid_value", path)
    return result


def _parse_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey
        result[key] = value
    return result


def _reject_constant(_value: str) -> float:
    raise _NonStandardConstant


def _validate_depth(value: object, path: str = "", depth: int = 0) -> None:
    if depth > MAX_SCENARIO_NESTING:
        _fail("bounds_exceeded", path or "/")
    if isinstance(value, dict):
        for key, child in value.items():
            _validate_depth(child, _pointer(path, key), depth + 1)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_depth(child, _pointer(path, str(index)), depth + 1)


def _parse_json(raw: bytes) -> dict[str, Any]:
    if len(raw) > MAX_SCENARIO_BYTES:
        _fail("bounds_exceeded", "/")
    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=_parse_pairs,
            parse_constant=_reject_constant,
        )
    except _DuplicateKey:
        _fail("duplicate_json_key", "/")
    except (UnicodeDecodeError, json.JSONDecodeError, _NonStandardConstant):
        _fail("invalid_json", "/")
    except RecursionError:
        _fail("bounds_exceeded", "/")
    _validate_depth(value)
    return _expect_object(value, "/")


@dataclass(frozen=True, slots=True)
class _CheckSpec:
    source_ref: str
    input_kind: str
    raw: bytes | None
    expected_r2: dict[str, Any] | None


@dataclass(frozen=True, slots=True)
class _ScanSpec:
    scan_order: int
    source_order: tuple[str, ...]
    checks: tuple[_CheckSpec, ...]
    expected_r1: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ScenarioSpec:
    scenario_id: str
    subject_ref: str
    sources: dict[str, SourceIdentity]
    scans: tuple[_ScanSpec, ...]


def _decode_input(value: object, path: str) -> tuple[str, bytes | None]:
    obj = _expect_object(value, path)
    keys = set(obj)
    if keys == {"utf8_text"}:
        text = _untrusted_text(obj["utf8_text"], _pointer(path, "utf8_text"))
        try:
            raw = text.encode("utf-8", errors="strict")
        except UnicodeEncodeError:
            _fail("invalid_value", _pointer(path, "utf8_text"))
        if len(raw) > MAX_RESPONSE_BYTES:
            _fail("bounds_exceeded", _pointer(path, "utf8_text"))
        return "utf8_text", raw
    if keys == {"raw_bytes_hex"}:
        encoded = _untrusted_text(obj["raw_bytes_hex"], _pointer(path, "raw_bytes_hex"))
        if len(encoded) % 2 or re.fullmatch(r"[0-9a-fA-F]*", encoded) is None:
            _fail("invalid_value", _pointer(path, "raw_bytes_hex"))
        raw = bytes.fromhex(encoded)
        if len(raw) > MAX_RESPONSE_BYTES:
            _fail("bounds_exceeded", _pointer(path, "raw_bytes_hex"))
        return "raw_bytes_hex", raw
    if keys == {"local_construction_error"}:
        marker_path = _pointer(path, "local_construction_error")
        marker = _text(obj["local_construction_error"], marker_path)
        if marker != "synthetic-local-construction-error":
            _fail("invalid_value", marker_path)
        return "local_construction_error", None
    unknown = sorted(keys - {"utf8_text", "raw_bytes_hex", "local_construction_error"})
    if unknown:
        _fail("unknown_field", _pointer(path, unknown[0]))
    _fail("missing_field", path)


def _validate_expected_r2(value: object, path: str) -> dict[str, Any] | None:
    if value is None:
        return None
    obj = _expect_keys(value, {"status", "reason_codes", "finding_keys"}, path)
    status = _text(obj["status"], _pointer(path, "status"))
    if status not in _STATUS_VALUES:
        _fail("invalid_value", _pointer(path, "status"))
    reasons = _string_list(
        obj["reason_codes"], _pointer(path, "reason_codes"), maximum=8
    )
    finding_keys = _string_list(
        obj["finding_keys"],
        _pointer(path, "finding_keys"),
        maximum=MAX_EXPECTED_RECORDS_PER_CHECK,
    )
    return {"status": status, "reason_codes": reasons, "finding_keys": finding_keys}


def _nullable_text(value: object, path: str) -> str | None:
    if value is None:
        return None
    return _text(value, path)


def _validate_comparison(value: object, path: str) -> dict[str, Any]:
    keys = {
        "comparison_id",
        "subject_ref",
        "source_id",
        "baseline_scan_id",
        "current_scan_id",
        "finding_key",
        "kind",
        "changed_field_paths",
        "reason_codes",
    }
    obj = _expect_keys(value, keys, path)
    comparison = {
        "comparison_id": _text(obj["comparison_id"], _pointer(path, "comparison_id")),
        "subject_ref": _text(obj["subject_ref"], _pointer(path, "subject_ref")),
        "source_id": _text(obj["source_id"], _pointer(path, "source_id")),
        "baseline_scan_id": _nullable_text(
            obj["baseline_scan_id"], _pointer(path, "baseline_scan_id")
        ),
        "current_scan_id": _text(
            obj["current_scan_id"], _pointer(path, "current_scan_id")
        ),
        "finding_key": _nullable_text(
            obj["finding_key"], _pointer(path, "finding_key")
        ),
        "kind": _text(obj["kind"], _pointer(path, "kind")),
        "changed_field_paths": _string_list(
            obj["changed_field_paths"],
            _pointer(path, "changed_field_paths"),
            maximum=MAX_EXPECTED_RECORDS_PER_CHECK,
        ),
        "reason_codes": _string_list(
            obj["reason_codes"],
            _pointer(path, "reason_codes"),
            maximum=MAX_EXPECTED_RECORDS_PER_CHECK,
        ),
    }
    if comparison["kind"] not in _COMPARISON_VALUES:
        _fail("invalid_value", _pointer(path, "kind"))
    return comparison


def _validate_exposure(value: object, path: str) -> dict[str, Any]:
    keys = {
        "comparison_id",
        "subject_ref",
        "source_id",
        "finding_key",
        "kind",
        "changed_field_paths",
    }
    obj = _expect_keys(value, keys, path)
    result = {
        "comparison_id": _text(obj["comparison_id"], _pointer(path, "comparison_id")),
        "subject_ref": _text(obj["subject_ref"], _pointer(path, "subject_ref")),
        "source_id": _text(obj["source_id"], _pointer(path, "source_id")),
        "finding_key": _text(obj["finding_key"], _pointer(path, "finding_key")),
        "kind": _text(obj["kind"], _pointer(path, "kind")),
        "changed_field_paths": _string_list(
            obj["changed_field_paths"],
            _pointer(path, "changed_field_paths"),
            maximum=MAX_EXPECTED_RECORDS_PER_CHECK,
        ),
    }
    if result["kind"] not in _EXPOSURE_VALUES:
        _fail("invalid_value", _pointer(path, "kind"))
    return result


def _validate_guard(value: object, path: str) -> dict[str, Any]:
    keys = {
        "guard_id",
        "subject_ref",
        "source_id",
        "baseline_scan_id",
        "current_scan_id",
        "guard_kind",
        "prior_status",
        "current_status",
        "reason_codes",
    }
    obj = _expect_keys(value, keys, path)
    result = {
        "guard_id": _text(obj["guard_id"], _pointer(path, "guard_id")),
        "subject_ref": _text(obj["subject_ref"], _pointer(path, "subject_ref")),
        "source_id": _text(obj["source_id"], _pointer(path, "source_id")),
        "baseline_scan_id": _nullable_text(
            obj["baseline_scan_id"], _pointer(path, "baseline_scan_id")
        ),
        "current_scan_id": _text(
            obj["current_scan_id"], _pointer(path, "current_scan_id")
        ),
        "guard_kind": _text(obj["guard_kind"], _pointer(path, "guard_kind")),
        "prior_status": _nullable_text(
            obj["prior_status"], _pointer(path, "prior_status")
        ),
        "current_status": _text(
            obj["current_status"], _pointer(path, "current_status")
        ),
        "reason_codes": _string_list(
            obj["reason_codes"],
            _pointer(path, "reason_codes"),
            maximum=MAX_EXPECTED_RECORDS_PER_CHECK,
        ),
    }
    if result["guard_kind"] not in _GUARD_VALUES:
        _fail("invalid_value", _pointer(path, "guard_kind"))
    if (
        result["prior_status"] is not None
        and result["prior_status"] not in _STATUS_VALUES
    ):
        _fail("invalid_value", _pointer(path, "prior_status"))
    if result["current_status"] not in _STATUS_VALUES:
        _fail("invalid_value", _pointer(path, "current_status"))
    return result


def _validate_expected_r1(value: object, path: str) -> dict[str, Any]:
    obj = _expect_keys(
        value,
        {
            "baseline_created_sources",
            "comparisons",
            "exposure_events",
            "guarding_events",
        },
        path,
    )
    baseline = _string_list(
        obj["baseline_created_sources"],
        _pointer(path, "baseline_created_sources"),
        maximum=MAX_EXPECTED_RECORDS_PER_SCAN,
    )
    comparisons_raw = _expect_list(obj["comparisons"], _pointer(path, "comparisons"))
    exposures_raw = _expect_list(
        obj["exposure_events"], _pointer(path, "exposure_events")
    )
    guards_raw = _expect_list(obj["guarding_events"], _pointer(path, "guarding_events"))
    if len(comparisons_raw) > MAX_EXPECTED_RECORDS_PER_SCAN:
        _fail("bounds_exceeded", _pointer(path, "comparisons"))
    if len(exposures_raw) > MAX_EXPECTED_RECORDS_PER_SCAN:
        _fail("bounds_exceeded", _pointer(path, "exposure_events"))
    if len(guards_raw) > MAX_EXPECTED_RECORDS_PER_SCAN:
        _fail("bounds_exceeded", _pointer(path, "guarding_events"))
    total = len(baseline) + len(comparisons_raw) + len(exposures_raw) + len(guards_raw)
    if total > MAX_EXPECTED_RECORDS_PER_SCAN:
        _fail("bounds_exceeded", path)
    return {
        "baseline_created_sources": baseline,
        "comparisons": [
            _validate_comparison(
                item, _pointer(_pointer(path, "comparisons"), str(index))
            )
            for index, item in enumerate(comparisons_raw)
        ],
        "exposure_events": [
            _validate_exposure(
                item, _pointer(_pointer(path, "exposure_events"), str(index))
            )
            for index, item in enumerate(exposures_raw)
        ],
        "guarding_events": [
            _validate_guard(
                item, _pointer(_pointer(path, "guarding_events"), str(index))
            )
            for index, item in enumerate(guards_raw)
        ],
    }


def parse_scenario_bytes(raw: bytes) -> ScenarioSpec:
    """Parse and validate one bounded scenario file."""

    root = _parse_json(raw)
    obj = _expect_keys(
        root,
        {"scenario_version", "scenario_id", "subject_ref", "sources", "scans"},
        "/",
    )
    if _text(obj["scenario_version"], "/scenario_version") != SCENARIO_VERSION:
        _fail("invalid_value", "/scenario_version")
    scenario_id = _text(obj["scenario_id"], "/scenario_id")
    if SCENARIO_ID_PATTERN.fullmatch(scenario_id) is None:
        _fail("invalid_value", "/scenario_id")
    subject_ref = _text(obj["subject_ref"], "/subject_ref")

    source_values = _expect_list(obj["sources"], "/sources")
    if not 1 <= len(source_values) <= MAX_SOURCES:
        _fail("bounds_exceeded", "/sources")
    sources: dict[str, SourceIdentity] = {}
    source_refs: list[str] = []
    for index, value in enumerate(source_values):
        path = f"/sources/{index}"
        source = _expect_keys(
            value,
            {
                "source_ref",
                "source_id",
                "canonical_scope",
                "adapter_id",
                "adapter_version",
                "schema_version",
                "normalization_version",
                "material_fields",
                "set_like_fields",
            },
            path,
        )
        source_ref = _text(source["source_ref"], _pointer(path, "source_ref"))
        if source_ref in sources:
            _fail("invalid_value", _pointer(path, "source_ref"))
        source_refs.append(source_ref)
        canonical_scope = _string_list(
            source["canonical_scope"],
            _pointer(path, "canonical_scope"),
            maximum=MAX_CANONICAL_SCOPE_ITEMS,
            require_sorted_unique=True,
        )
        if not canonical_scope:
            _fail("invalid_value", _pointer(path, "canonical_scope"))
        material_fields = _string_list(
            source["material_fields"],
            _pointer(path, "material_fields"),
            maximum=MAX_MATERIAL_FIELDS,
            require_sorted_unique=True,
        )
        set_like_fields = _string_list(
            source["set_like_fields"],
            _pointer(path, "set_like_fields"),
            maximum=MAX_MATERIAL_FIELDS,
            require_sorted_unique=True,
        )
        if not set(set_like_fields) <= set(material_fields):
            _fail("invalid_value", _pointer(path, "set_like_fields"))
        try:
            identity = SourceIdentity(
                source_id=_text(source["source_id"], _pointer(path, "source_id")),
                canonical_scope=tuple(canonical_scope),
                adapter_id=_text(source["adapter_id"], _pointer(path, "adapter_id")),
                adapter_version=_text(
                    source["adapter_version"], _pointer(path, "adapter_version")
                ),
                schema_version=_exact_int(
                    source["schema_version"],
                    _pointer(path, "schema_version"),
                    minimum=1,
                    maximum=64,
                ),
                normalization_version=_exact_int(
                    source["normalization_version"],
                    _pointer(path, "normalization_version"),
                    minimum=1,
                    maximum=64,
                ),
                material_fields=frozenset(material_fields),
                set_like_fields=frozenset(set_like_fields),
            )
        except ScenarioInvalid:
            raise
        except Exception:
            _fail("construction_error", path)
        sources[source_ref] = identity
    if source_refs != sorted(source_refs):
        _fail("invalid_value", "/sources")

    scan_values = _expect_list(obj["scans"], "/scans")
    if not 1 <= len(scan_values) <= MAX_SCANS:
        _fail("bounds_exceeded", "/scans")
    scans: list[_ScanSpec] = []
    for index, value in enumerate(scan_values):
        path = f"/scans/{index}"
        scan = _expect_keys(
            value, {"scan_order", "source_order", "checks", "expected"}, path
        )
        scan_order = _exact_int(
            scan["scan_order"],
            _pointer(path, "scan_order"),
            minimum=1,
            maximum=MAX_SCANS,
        )
        source_order_values = _expect_list(
            scan["source_order"], _pointer(path, "source_order")
        )
        if not 1 <= len(source_order_values) <= MAX_CHECKS_PER_SCAN:
            _fail("bounds_exceeded", _pointer(path, "source_order"))
        source_order = tuple(
            _text(item, _pointer(_pointer(path, "source_order"), str(item_index)))
            for item_index, item in enumerate(source_order_values)
        )
        if len(set(source_order)) != len(source_order):
            _fail("reference_error", _pointer(path, "source_order"))
        for source_ref in source_order:
            if source_ref not in sources:
                _fail("reference_error", _pointer(path, "source_order"))
        resolved_ids = [sources[source_ref].source_id for source_ref in source_order]
        if len(set(resolved_ids)) != len(resolved_ids):
            _fail("reference_error", _pointer(path, "source_order"))
        check_values = _expect_list(scan["checks"], _pointer(path, "checks"))
        if not 1 <= len(check_values) <= MAX_CHECKS_PER_SCAN:
            _fail("bounds_exceeded", _pointer(path, "checks"))
        if len(check_values) != len(source_order):
            _fail("invalid_value", _pointer(path, "checks"))
        checks: list[_CheckSpec] = []
        for check_index, check_value in enumerate(check_values):
            check_path = f"{path}/checks/{check_index}"
            check = _expect_keys(
                check_value, {"source_ref", "input", "expected"}, check_path
            )
            source_ref = _text(check["source_ref"], _pointer(check_path, "source_ref"))
            if source_ref != source_order[check_index]:
                _fail("reference_error", _pointer(check_path, "source_ref"))
            input_kind, raw_input = _decode_input(
                check["input"], _pointer(check_path, "input")
            )
            expected = _expect_keys(
                check["expected"], {"r2"}, _pointer(check_path, "expected")
            )
            expected_r2 = _validate_expected_r2(
                expected["r2"], _pointer(_pointer(check_path, "expected"), "r2")
            )
            if input_kind == "local_construction_error" and expected_r2 is not None:
                _fail("invalid_value", _pointer(_pointer(check_path, "expected"), "r2"))
            if input_kind != "local_construction_error" and expected_r2 is None:
                _fail("invalid_value", _pointer(_pointer(check_path, "expected"), "r2"))
            checks.append(_CheckSpec(source_ref, input_kind, raw_input, expected_r2))
        expected = _expect_keys(scan["expected"], {"r1"}, _pointer(path, "expected"))
        expected_r1 = _validate_expected_r1(
            expected["r1"], _pointer(_pointer(path, "expected"), "r1")
        )
        scans.append(_ScanSpec(scan_order, source_order, tuple(checks), expected_r1))
    if [scan.scan_order for scan in scans] != list(range(1, len(scans) + 1)):
        _fail("invalid_value", "/scans")
    return ScenarioSpec(scenario_id, subject_ref, sources, tuple(scans))


def load_scenario(path: str | Path) -> ScenarioSpec:
    """Read and validate a scenario without exposing filesystem exceptions."""

    try:
        with Path(path).open("rb") as stream:
            raw = stream.read(MAX_SCENARIO_BYTES + 1)
    except OSError:
        _fail("construction_error", "/")
    if len(raw) > MAX_SCENARIO_BYTES:
        _fail("bounds_exceeded", "/")
    return parse_scenario_bytes(raw)


def _check_projection(check: SourceCheck) -> dict[str, Any]:
    return {
        "status": check.status.value,
        "reason_codes": list(check.reason_codes),
        "finding_keys": [observation.finding_key for observation in check.observations],
    }


def _comparison_projection(result: Any) -> dict[str, Any]:
    return {
        "comparison_id": result.comparison_id,
        "subject_ref": result.subject_ref,
        "source_id": result.source_id,
        "baseline_scan_id": result.baseline_scan_id,
        "current_scan_id": result.current_scan_id,
        "finding_key": result.finding_key,
        "kind": result.kind.value,
        "changed_field_paths": list(result.changed_field_paths),
        "reason_codes": list(result.reason_codes),
    }


def _exposure_projection(event: Any) -> dict[str, Any]:
    return {
        "comparison_id": event.comparison_id,
        "subject_ref": event.subject_ref,
        "source_id": event.source_id,
        "finding_key": event.finding_key,
        "kind": event.kind.value,
        "changed_field_paths": list(event.changed_field_paths),
    }


def _guard_projection(event: Any) -> dict[str, Any]:
    return {
        "guard_id": event.guard_id,
        "subject_ref": event.subject_ref,
        "source_id": event.source_id,
        "baseline_scan_id": event.baseline_scan_id,
        "current_scan_id": event.current_scan_id,
        "guard_kind": event.guard_kind.value,
        "prior_status": event.prior_status.value if event.prior_status else None,
        "current_status": event.current_status.value,
        "reason_codes": list(event.reason_codes),
    }


def _report_projection(report: Any) -> dict[str, Any]:
    return {
        "baseline_created_sources": list(report.baseline_created_sources),
        "comparisons": [_comparison_projection(item) for item in report.comparisons],
        "exposure_events": [
            _exposure_projection(item) for item in report.exposure_events
        ],
        "guarding_events": [_guard_projection(item) for item in report.guarding_events],
    }


def _compare_value(
    expected: Any, actual: Any, path: str, mismatches: list[dict[str, Any]]
) -> None:
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in sorted(set(expected) | set(actual)):
            child = _pointer(path, key)
            if key not in actual:
                mismatches.append(
                    {"path": child, "expected": expected[key], "actual": None}
                )
            else:
                _compare_value(expected[key], actual[key], child, mismatches)
        return
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            mismatches.append({"path": path, "expected": expected, "actual": actual})
            return
        for index, (expected_item, actual_item) in enumerate(
            zip(expected, actual, strict=True)
        ):
            _compare_value(
                expected_item, actual_item, _pointer(path, str(index)), mismatches
            )
        return
    if expected != actual:
        mismatches.append({"path": path, "expected": expected, "actual": actual})


@dataclass(frozen=True, slots=True)
class ScenarioRun:
    output: dict[str, Any]
    human_scans: tuple[dict[str, Any], ...]
    subject_ref: str


def run_scenario(scenario: ScenarioSpec) -> ScenarioRun:
    """Execute a validated scenario using R2 and R1 as the only semantics."""

    scan_records: list[dict[str, Any]] = []
    all_mismatches: list[dict[str, Any]] = []
    baseline: ScanAttempt | None = None
    for scan in scenario.scans:
        scan_id = f"{scenario.scenario_id}:scan-{scan.scan_order:03d}"
        source_checks: list[SourceCheck] = []
        source_records: list[dict[str, Any]] = []
        for check_spec in scan.checks:
            source = scenario.sources[check_spec.source_ref]
            source_check_id = f"{scan_id}:check-{check_spec.source_ref}"
            diagnostics = DiagnosticMetadata("synthetic-time")
            invoked = check_spec.input_kind != "local_construction_error"
            if check_spec.input_kind == "local_construction_error":
                check = SourceCheck.failed(
                    source_check_id=source_check_id,
                    scan_id=scan_id,
                    subject_ref=scenario.subject_ref,
                    source=source,
                    reason_codes=("local_construction_error",),
                    diagnostics=diagnostics,
                )
                r2_projection = None
            else:
                context = TrustedContext(
                    scan_id=scan_id,
                    source_check_id=source_check_id,
                    subject_ref=scenario.subject_ref,
                    source=source,
                    diagnostics=diagnostics,
                )
                check = normalize_response(cast(bytes, check_spec.raw), context)
                r2_projection = _check_projection(check)
            source_checks.append(check)
            source_records.append(
                {
                    "source_ref": check_spec.source_ref,
                    "source_id": source.source_id,
                    "source_check_id": source_check_id,
                    "input_kind": check_spec.input_kind,
                    "input_bytes": len(check_spec.raw or b""),
                    "r2_invoked": invoked,
                    "r2": r2_projection,
                    "r1": _check_projection(check),
                }
            )

        plan = ScanPlan.create(
            subject_ref=scenario.subject_ref,
            sources=tuple(scenario.sources[ref] for ref in scan.source_order),
            execution_order=tuple(
                scenario.sources[ref].source_id for ref in scan.source_order
            ),
        )
        current = ScanAttempt.create(
            scan_id=scan_id, plan=plan, source_checks=tuple(source_checks)
        )
        report = compare_scans(baseline, current)
        r1_projection = _report_projection(report)
        actual_scan = {
            "scan_id": scan_id,
            "scan_order": scan.scan_order,
            "source_order": list(scan.source_order),
            "outcome": current.outcome.value,
            "source_checks": source_records,
            "r1": r1_projection,
            "exposure_silence": not bool(report.exposure_events),
        }
        scan_records.append(actual_scan)

        scan_index = scan.scan_order - 1
        for check_index, check_spec in enumerate(scan.checks):
            source_path = _pointer(
                _pointer(_pointer("", "scans"), str(scan_index)),
                "checks",
            )
            source_path = _pointer(source_path, str(check_index))
            source_record = source_records[check_index]
            _compare_value(
                check_spec.expected_r2,
                source_record["r2"],
                _pointer(_pointer(source_path, "expected"), "r2"),
                all_mismatches,
            )
        _compare_value(
            scan.expected_r1,
            r1_projection,
            _pointer(
                _pointer(
                    _pointer(_pointer("", "scans"), str(scan.scan_order - 1)),
                    "expected",
                ),
                "r1",
            ),
            all_mismatches,
        )
        baseline = current

    result = "PASS" if not all_mismatches else "EXPECTATION_MISMATCH"
    output = {
        "runner_version": RUNNER_VERSION,
        "scenario_id": scenario.scenario_id,
        "result": result.lower(),
        "scans": scan_records,
        "mismatches": all_mismatches,
        "diagnostic": None,
    }
    return ScenarioRun(output, tuple(scan_records), scenario.subject_ref)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _human_line_string(value: object) -> str:
    return _canonical_json(value)


def render_human(run: ScenarioRun) -> str:
    output = run.output
    lines = [
        "SCENARIO "
        f"{_human_line_string(output['scenario_id'])} "
        f"result={output['result'].upper()}",
        f"SUBJECT {_human_line_string(run.subject_ref)}",
    ]
    total_checks = 0
    total_comparisons = 0
    total_exposures = 0
    total_guards = 0
    for scan in run.human_scans:
        checks = scan["source_checks"]
        report = scan["r1"]
        total_checks += len(checks)
        total_comparisons += len(report["comparisons"])
        total_exposures += len(report["exposure_events"])
        total_guards += len(report["guarding_events"])
        scan_mismatch = any(
            item["path"].startswith(f"/scans/{scan['scan_order'] - 1}/")
            for item in output["mismatches"]
        )
        lines.append(
            f"SCAN order={scan['scan_order']} total={len(run.human_scans)} "
            f"scan_id={_human_line_string(scan['scan_id'])} "
            f"outcome={_human_line_string(scan['outcome'])} "
            f"expectation={'MISMATCH' if scan_mismatch else 'PASS'}"
        )
        for check in checks:
            r2 = check["r2"]
            r1 = check["r1"]
            lines.append(
                f"SOURCE_CHECK source_ref={_human_line_string(check['source_ref'])} "
                f"source_id={_human_line_string(check['source_id'])} "
                f"source_check_id={_human_line_string(check['source_check_id'])} "
                f"input_kind={_human_line_string(check['input_kind'])} "
                f"input_bytes={check['input_bytes']} "
                f"r2_invoked={'TRUE' if check['r2_invoked'] else 'FALSE'} "
                f"r2_status={_human_line_string(r2['status'] if r2 else None)} "
                f"r2_reason_codes="
                f"{_human_line_string(r2['reason_codes'] if r2 else [])} "
                f"r2_finding_keys="
                f"{_human_line_string(r2['finding_keys'] if r2 else [])} "
                f"status={_human_line_string(r1['status'])} "
                f"reason_codes={_human_line_string(r1['reason_codes'])} "
                f"finding_keys={_human_line_string(r1['finding_keys'])}"
            )
        for source_id in report["baseline_created_sources"]:
            lines.append(f"BASELINE_CREATED source_id={_human_line_string(source_id)}")
        for comparison in report["comparisons"]:
            lines.append(
                "COMPARISON "
                f"comparison_id={_human_line_string(comparison['comparison_id'])} "
                f"subject_ref={_human_line_string(comparison['subject_ref'])} "
                f"source_id={_human_line_string(comparison['source_id'])} "
                f"baseline_scan_id="
                f"{_human_line_string(comparison['baseline_scan_id'])} "
                f"current_scan_id={_human_line_string(comparison['current_scan_id'])} "
                f"finding_key={_human_line_string(comparison['finding_key'])} "
                f"kind={_human_line_string(comparison['kind'])} "
                f"changed_field_paths="
                f"{_canonical_json(comparison['changed_field_paths'])} "
                f"reason_codes={_canonical_json(comparison['reason_codes'])}"
            )
        for exposure in report["exposure_events"]:
            lines.append(
                "EXPOSURE_EVENT "
                f"comparison_id={_human_line_string(exposure['comparison_id'])} "
                f"subject_ref={_human_line_string(exposure['subject_ref'])} "
                f"source_id={_human_line_string(exposure['source_id'])} "
                f"finding_key={_human_line_string(exposure['finding_key'])} "
                f"kind={_human_line_string(exposure['kind'])} "
                f"changed_field_paths={_canonical_json(exposure['changed_field_paths'])}"
            )
        for guard in report["guarding_events"]:
            lines.append(
                "GUARDING_EVENT "
                f"guard_id={_human_line_string(guard['guard_id'])} "
                f"subject_ref={_human_line_string(guard['subject_ref'])} "
                f"source_id={_human_line_string(guard['source_id'])} "
                f"baseline_scan_id={_human_line_string(guard['baseline_scan_id'])} "
                f"current_scan_id={_human_line_string(guard['current_scan_id'])} "
                f"guard_kind={_human_line_string(guard['guard_kind'])} "
                f"prior_status={_human_line_string(guard['prior_status'])} "
                f"current_status={_human_line_string(guard['current_status'])} "
                f"reason_codes={_canonical_json(guard['reason_codes'])}"
            )
        lines.append(
            f"EXPOSURE_SILENCE actual={'TRUE' if scan['exposure_silence'] else 'FALSE'}"
        )
        for mismatch in output["mismatches"]:
            if mismatch["path"].startswith(f"/scans/{scan['scan_order'] - 1}/"):
                lines.append(
                    f"MISMATCH path={_human_line_string(mismatch['path'])} "
                    f"expected={_canonical_json(mismatch['expected'])} "
                    f"actual={_canonical_json(mismatch['actual'])}"
                )
    lines.append(
        f"SUMMARY scans={len(run.human_scans)} source_checks={total_checks} "
        f"comparisons={total_comparisons} exposure_events={total_exposures} "
        f"guarding_events={total_guards} mismatches={len(output['mismatches'])}"
    )
    return "\n".join(lines) + "\n"


def _invalid_output(error: ScenarioInvalid, json_mode: bool) -> int:
    diagnostic = {"code": error.code, "path": error.path, "message": error.message}
    if json_mode:
        print(
            _canonical_json(
                {
                    "runner_version": RUNNER_VERSION,
                    "scenario_id": None,
                    "result": "invalid_scenario",
                    "scans": [],
                    "mismatches": [],
                    "diagnostic": diagnostic,
                }
            )
        )
    else:
        print(
            f"INVALID_SCENARIO code={error.code} path={_human_line_string(error.path)} "
            f"message={_human_line_string(error.message)}",
            file=sys.stderr,
        )
    return 2


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    json_mode = False
    if args and args[0] == "--json":
        json_mode = True
        args.pop(0)
    if len(args) != 1:
        return _invalid_output(ScenarioInvalid("invalid_value", "/"), json_mode)
    try:
        scenario = load_scenario(args[0])
        run = run_scenario(scenario)
    except ScenarioInvalid as error:
        return _invalid_output(error, json_mode)
    except Exception:
        return _invalid_output(ScenarioInvalid("construction_error", "/"), json_mode)
    if json_mode:
        print(_canonical_json(run.output))
    else:
        print(render_human(run), end="")
    return 0 if run.output["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
