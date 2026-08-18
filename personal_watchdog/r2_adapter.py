"""The bounded, synthetic R2 adapter boundary.

This module accepts only an untrusted response as bytes and returns one R1
``SourceCheck``.  It has no I/O, persistence, comparison, or event behavior.
"""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass, field
from typing import Any

from personal_watchdog.r1 import (
    DiagnosticMetadata,
    InvalidObservationError,
    Observation,
    R1Error,
    SourceCheck,
    SourceIdentity,
)

MAX_INPUT_BYTES = 65_536
MAX_RESULTS = 100
MAX_ARRAY_ITEMS = 100
MAX_OBJECT_MEMBERS = 16
MAX_NESTING_DEPTH = 8
MAX_STRING_LENGTH = 256
MAX_DIAGNOSTIC_TEXT = 512
MAX_REASON_CODES = 8
MAX_REASON_CODE_LENGTH = 64
MAX_DIAGNOSTIC_DURATION_MS = 86_400_000
MAX_RETRY_COUNT = 100

SUPPORTED_CONTRACT = "fixture-response/1"

REASON_CODES = frozenset(
    {
        "input_too_large",
        "blank_input",
        "invalid_utf8",
        "invalid_json",
        "duplicate_json_key",
        "nonstandard_json_constant",
        "nesting_too_deep",
        "wrong_top_level_type",
        "missing_field",
        "unknown_field",
        "invalid_field_type",
        "invalid_string",
        "collection_too_large",
        "too_many_results",
        "unsupported_response_contract",
        "response_source_mismatch",
        "response_outcome_mismatch",
        "malformed_envelope",
        "malformed_result",
        "unsupported_value_type",
        "duplicate_finding_key_deduplicated",
        "conflicting_duplicate_finding_key",
        "partial_candidates_discarded",
        "response_failed",
        "response_unverifiable",
        "response_incomplete",
    }
)

_ENVELOPE_KEYS = frozenset({"contract_version", "source_id", "outcome", "results"})
_RESULT_KEYS = frozenset({"finding_key", "kind", "locator", "material"})
_OUTCOMES = frozenset({"completed", "failed", "unverifiable", "incomplete"})


@dataclass(frozen=True, slots=True)
class TrustedContext:
    """Locally constructed identity and diagnostics for one R1 source check."""

    scan_id: str
    source_check_id: str
    subject_ref: str
    source: SourceIdentity
    diagnostics: DiagnosticMetadata = field(
        default_factory=lambda: DiagnosticMetadata("synthetic-time")
    )

    def __post_init__(self) -> None:
        _validate_trusted_string(self.scan_id, "scan_id")
        _validate_trusted_string(self.source_check_id, "source_check_id")
        _validate_trusted_string(self.subject_ref, "subject_ref")
        if not isinstance(self.source, SourceIdentity):
            raise R1Error("trusted source must be a SourceIdentity")
        _validate_trusted_identity(self.source)
        if not isinstance(self.diagnostics, DiagnosticMetadata):
            raise R1Error("trusted diagnostics must be DiagnosticMetadata")
        _validate_trusted_string(
            self.diagnostics.recorded_at, "diagnostics.recorded_at"
        )
        _validate_trusted_string(
            self.diagnostics.text,
            "diagnostics.text",
            max_length=MAX_DIAGNOSTIC_TEXT,
            allow_empty=True,
        )
        _validate_exact_integer(self.diagnostics.duration_ms, "diagnostics.duration_ms")
        _validate_exact_integer(self.diagnostics.retry_count, "diagnostics.retry_count")
        if not 0 <= self.diagnostics.duration_ms <= MAX_DIAGNOSTIC_DURATION_MS:
            raise R1Error("diagnostics.duration_ms is outside the R2 limit")
        if not 0 <= self.diagnostics.retry_count <= MAX_RETRY_COUNT:
            raise R1Error("diagnostics.retry_count is outside the R2 limit")


class _DuplicateJSONKey(Exception):
    pass


class _NonStandardJSONConstant(Exception):
    pass


class _ValidationFailure(Exception):
    def __init__(self, reason_code: str) -> None:
        self.reason_code = reason_code


def _validate_exact_integer(value: object, field_name: str) -> None:
    if type(value) is not int:  # noqa: E721 - exact typing is the rule here
        raise R1Error(f"{field_name} must be an exact integer")


def _validate_text(
    value: object,
    field_name: str,
    *,
    max_length: int = MAX_STRING_LENGTH,
    allow_empty: bool = False,
) -> str:
    if type(value) is not str:
        raise _ValidationFailure("invalid_field_type")
    if not value and not allow_empty:
        raise _ValidationFailure("invalid_string")
    if len(value) > max_length or any(
        0xD800 <= ord(character) <= 0xDFFF for character in value
    ):
        raise _ValidationFailure("invalid_string")
    if unicodedata.normalize("NFC", value) != value:
        raise _ValidationFailure("invalid_string")
    return value


def _validate_trusted_string(
    value: object,
    field_name: str,
    *,
    max_length: int = MAX_STRING_LENGTH,
    allow_empty: bool = False,
) -> str:
    if type(value) is not str:
        raise R1Error(f"{field_name} must be a string")
    if not value and not allow_empty:
        raise R1Error(f"{field_name} must not be empty")
    if len(value) > max_length or any(
        0xD800 <= ord(character) <= 0xDFFF for character in value
    ):
        raise R1Error(f"{field_name} exceeds the R2 string rule")
    if unicodedata.normalize("NFC", value) != value:
        raise R1Error(f"{field_name} must be NFC-normalized")
    return value


def _validate_trusted_identity(source: SourceIdentity) -> None:
    _validate_trusted_string(source.source_id, "source.source_id")
    _validate_trusted_string(source.adapter_id, "source.adapter_id")
    _validate_trusted_string(source.adapter_version, "source.adapter_version")
    _validate_exact_integer(source.schema_version, "source.schema_version")
    _validate_exact_integer(
        source.normalization_version, "source.normalization_version"
    )
    if source.schema_version < 1 or source.normalization_version < 1:
        raise R1Error("trusted schema versions must be positive")
    if len(source.canonical_scope) > MAX_ARRAY_ITEMS:
        raise R1Error("trusted canonical scope is too large")
    for item in source.canonical_scope:
        _validate_trusted_string(item, "source.canonical_scope item")
    for field_name in source.material_fields:
        _validate_trusted_string(field_name, "source.material_fields item")
    for field_name in source.set_like_fields:
        _validate_trusted_string(field_name, "source.set_like_fields item")
    if len(source.material_fields) > MAX_OBJECT_MEMBERS:
        raise R1Error("trusted material policy is too large")
    if len(source.set_like_fields) > MAX_OBJECT_MEMBERS:
        raise R1Error("trusted set-like policy is too large")


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJSONKey
        result[key] = value
    return result


def _reject_constant(_value: str) -> float:
    raise _NonStandardJSONConstant


def _parse(raw: bytes) -> object:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise _ValidationFailure("invalid_utf8") from error
    if not text.strip():
        raise _ValidationFailure("blank_input")
    try:
        return json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_constant=_reject_constant,
        )
    except _DuplicateJSONKey as error:
        raise _ValidationFailure("duplicate_json_key") from error
    except _NonStandardJSONConstant as error:
        raise _ValidationFailure("nonstandard_json_constant") from error
    except RecursionError as error:
        raise _ValidationFailure("nesting_too_deep") from error
    except json.JSONDecodeError as error:
        raise _ValidationFailure("invalid_json") from error
    except ValueError as error:
        raise _ValidationFailure("invalid_json") from error


def _validate_json_tree(
    value: object, depth: int = 0, path: tuple[object, ...] = ()
) -> None:
    if depth > MAX_NESTING_DEPTH:
        raise _ValidationFailure("nesting_too_deep")
    if type(value) is dict:
        if len(value) > MAX_OBJECT_MEMBERS:
            raise _ValidationFailure("collection_too_large")
        for key, child in value.items():
            _validate_text(key, "object key")
            child_depth = depth + 1 if type(child) in (dict, list) else depth
            _validate_json_tree(child, child_depth, (*path, key))
        return
    if type(value) is list:
        if len(value) > MAX_ARRAY_ITEMS:
            reason = (
                "too_many_results" if path == ("results",) else "collection_too_large"
            )
            raise _ValidationFailure(reason)
        for index, child in enumerate(value):
            child_depth = depth + 1 if type(child) in (dict, list) else depth
            _validate_json_tree(child, child_depth, (*path, index))
        return
    if type(value) is str:
        _validate_text(value, "string value")
        return
    if value is None or type(value) is bool or type(value) is int:
        return
    raise _ValidationFailure("unsupported_value_type")


def _exact_keys(value: object, expected: frozenset[str]) -> dict[str, Any]:
    if type(value) is not dict:
        raise _ValidationFailure("malformed_result")
    keys = frozenset(value)
    if expected - keys:
        raise _ValidationFailure("missing_field")
    if keys - expected:
        raise _ValidationFailure("unknown_field")
    return value


def _material_value(value: object) -> None:
    if value is None or type(value) is bool or type(value) is int:
        return
    if type(value) is str:
        _validate_text(value, "material value")
        return
    if type(value) is list:
        for child in value:
            _material_value(child)
        return
    raise _ValidationFailure("unsupported_value_type")


def _validate_material(value: object, source: SourceIdentity) -> dict[str, Any]:
    if type(value) is not dict:
        raise _ValidationFailure("invalid_field_type")
    unknown = frozenset(value) - source.material_fields
    if unknown:
        raise _ValidationFailure("unknown_field")
    for key, item in value.items():
        _validate_text(key, "material field")
        if key in source.set_like_fields and type(item) is not list:
            raise _ValidationFailure("invalid_field_type")
        _material_value(item)
    return value


def _normalize_results(
    results: list[object], source: SourceIdentity
) -> tuple[tuple[Observation, ...], bool]:
    observations: dict[str, Observation] = {}
    deduplicated = False
    for result in results:
        record = _exact_keys(result, _RESULT_KEYS)
        finding_key = _validate_text(record["finding_key"], "finding_key")
        kind = _validate_text(record["kind"], "kind")
        locator = _validate_text(record["locator"], "locator")
        material = _validate_material(record["material"], source)
        try:
            observation = source.observation(
                finding_key=finding_key,
                kind=kind,
                locator=locator,
                material=material,
            )
        except InvalidObservationError as error:
            raise _ValidationFailure("malformed_result") from error
        previous = observations.get(finding_key)
        if previous is None:
            observations[finding_key] = observation
        elif previous == observation:
            deduplicated = True
        else:
            raise _ValidationFailure("conflicting_duplicate_finding_key")
    return tuple(observations.values()), deduplicated


def _bounded_reasons(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    unique = tuple(dict.fromkeys(reason_codes))
    if len(unique) > MAX_REASON_CODES:
        raise RuntimeError("R2 generated too many reason codes")
    if any(
        code not in REASON_CODES or len(code) > MAX_REASON_CODE_LENGTH
        for code in unique
    ):
        raise RuntimeError("R2 generated an invalid reason code")
    return unique


def _unverifiable(
    context: TrustedContext, reason_codes: tuple[str, ...]
) -> SourceCheck:
    return SourceCheck.unverifiable(
        source_check_id=context.source_check_id,
        scan_id=context.scan_id,
        subject_ref=context.subject_ref,
        source=context.source,
        reason_codes=_bounded_reasons(reason_codes),
        diagnostics=context.diagnostics,
    )


def _failed(context: TrustedContext, reason_codes: tuple[str, ...]) -> SourceCheck:
    return SourceCheck.failed(
        source_check_id=context.source_check_id,
        scan_id=context.scan_id,
        subject_ref=context.subject_ref,
        source=context.source,
        reason_codes=_bounded_reasons(reason_codes),
        diagnostics=context.diagnostics,
    )


def normalize_response(raw: bytes, trusted_context: TrustedContext) -> SourceCheck:
    """Normalize one synthetic response into an R1 source check."""

    if not isinstance(raw, bytes):
        raise TypeError("R2 response input must be bytes")
    if not isinstance(trusted_context, TrustedContext):
        raise R1Error("trusted_context must be TrustedContext")
    if len(raw) > MAX_INPUT_BYTES:
        return _unverifiable(trusted_context, ("input_too_large",))
    try:
        decoded = _parse(raw)
        if type(decoded) is not dict:
            raise _ValidationFailure("wrong_top_level_type")
        _validate_json_tree(decoded)
        envelope = _exact_keys(decoded, _ENVELOPE_KEYS)
        contract_version = _validate_text(
            envelope["contract_version"], "contract_version"
        )
        source_id = _validate_text(envelope["source_id"], "source_id")
        outcome = _validate_text(envelope["outcome"], "outcome")
        if type(envelope["results"]) is not list:
            raise _ValidationFailure("invalid_field_type")
        results = envelope["results"]
        if contract_version != SUPPORTED_CONTRACT:
            return _unverifiable(trusted_context, ("unsupported_response_contract",))
        if source_id != trusted_context.source.source_id:
            return _unverifiable(trusted_context, ("response_source_mismatch",))
        if outcome not in _OUTCOMES:
            raise _ValidationFailure("invalid_field_type")

        if outcome != "completed":
            base_reason = {
                "failed": "response_failed",
                "unverifiable": "response_unverifiable",
                "incomplete": "response_incomplete",
            }[outcome]
            if results:
                try:
                    _normalize_results(results, trusted_context.source)
                except _ValidationFailure as failure:
                    return _unverifiable(
                        trusted_context,
                        (
                            base_reason,
                            failure.reason_code,
                            "response_outcome_mismatch",
                            "partial_candidates_discarded",
                        ),
                    )
                return _unverifiable(
                    trusted_context,
                    (
                        base_reason,
                        "response_outcome_mismatch",
                        "partial_candidates_discarded",
                    ),
                )
            if outcome == "failed":
                return _failed(trusted_context, ("response_failed",))
            return _unverifiable(trusted_context, (base_reason,))

        observations, deduplicated = _normalize_results(results, trusted_context.source)
        reason_codes = ("duplicate_finding_key_deduplicated",) if deduplicated else ()
        return SourceCheck.completed(
            source_check_id=trusted_context.source_check_id,
            scan_id=trusted_context.scan_id,
            subject_ref=trusted_context.subject_ref,
            source=trusted_context.source,
            observations=observations,
            reason_codes=_bounded_reasons(reason_codes),
            diagnostics=trusted_context.diagnostics,
        )
    except _ValidationFailure as failure:
        return _unverifiable(trusted_context, (failure.reason_code,))
    except RecursionError:
        return _unverifiable(trusted_context, ("nesting_too_deep",))
