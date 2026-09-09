"""Deterministic synthetic adapter for the frozen XON check-email contract.

This module deliberately accepts an already captured in-memory transport
attempt.  It does not create a request, resolve a name, open a socket, or
perform any other I/O.  Transport metadata and response bytes remain
untrusted; identity and source-contract values come only from local context.
"""

from __future__ import annotations

import json
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal

from personal_watchdog.r1 import DiagnosticMetadata, SourceCheck, SourceIdentity
from personal_watchdog.r2_adapter import (
    MAX_INPUT_BYTES,
    TrustedContext,
    normalize_response,
)

MAX_XON_BODY_BYTES = 16_384
MAX_XON_HEADER_COUNT = 16
MAX_XON_HEADER_NAME_BYTES = 64
MAX_XON_HEADER_VALUE_BYTES = 512
MAX_XON_RETAINED_HEADER_BYTES = 8_192
MAX_XON_EMAIL_CODEPOINTS = 128
MAX_XON_BREACH_NAMES = 16
MAX_XON_BREACH_NAME_CODEPOINTS = 64

XON_SOURCE_ID = "xposedornot.free.check-email"
XON_CANONICAL_SCOPE = (
    "GET /v1/check-email/{email}",
    "include_details=false",
)
XON_ADAPTER_ID = "xposedornot-check-email"
XON_ADAPTER_VERSION = "1"
XON_SCHEMA_VERSION = 1
XON_NORMALIZATION_VERSION = 1

XON_SOURCE = SourceIdentity(
    source_id=XON_SOURCE_ID,
    canonical_scope=XON_CANONICAL_SCOPE,
    adapter_id=XON_ADAPTER_ID,
    adapter_version=XON_ADAPTER_VERSION,
    schema_version=XON_SCHEMA_VERSION,
    normalization_version=XON_NORMALIZATION_VERSION,
    set_like_fields=frozenset(),
    material_fields=frozenset(),
)

BodyState = Literal["complete", "incomplete", "over_limit", "absent"]
FailurePhase = Literal["before_status", "after_status"]


class TransportConstructionError(ValueError):
    """Raised for an invalid locally constructed experiment envelope."""


class R2EnvelopeTooLargeError(TransportConstructionError):
    """Raised before R2 when generated envelope bytes exceed its bound."""


class _UntrustedMetadataError(ValueError):
    """An untrusted HTTP metadata value cannot establish XON success."""


class TransportDisposition(StrEnum):
    READY = "ready"
    FAILED = "failed"
    INCOMPLETE = "incomplete"
    UNVERIFIABLE = "unverifiable"


@dataclass(frozen=True, slots=True)
class Header:
    """One bounded raw header entry; its bytes are never trusted as identity."""

    name_bytes: bytes
    value_bytes: bytes

    def __post_init__(self) -> None:
        if type(self.name_bytes) is not bytes:
            raise TransportConstructionError("header name must be bytes")
        if type(self.value_bytes) is not bytes:
            raise TransportConstructionError("header value must be bytes")
        if len(self.name_bytes) > MAX_XON_HEADER_NAME_BYTES:
            raise TransportConstructionError("header name exceeds the local bound")
        if len(self.value_bytes) > MAX_XON_HEADER_VALUE_BYTES:
            raise TransportConstructionError("header value exceeds the local bound")


def _validate_context(context: TrustedContext) -> None:
    if not isinstance(context, TrustedContext):
        raise TransportConstructionError("trusted_context must be TrustedContext")
    if context.source != XON_SOURCE:
        raise TransportConstructionError("trusted context has the wrong XON identity")


@dataclass(frozen=True, slots=True)
class TransportAttempt:
    """A bounded, locally constructed representation of one transport attempt."""

    http_status: int | None
    bounded_headers: tuple[Header, ...]
    body_bytes: bytes
    body_state: BodyState
    transport_failure: Literal["transport"] | None = None
    timed_out: bool = False
    failure_phase: FailurePhase | None = None
    trusted_context: TrustedContext = field(kw_only=True)

    def __post_init__(self) -> None:
        _validate_context(self.trusted_context)
        if type(self.http_status) is not int and self.http_status is not None:
            raise TransportConstructionError("http_status must be an exact integer")
        if self.http_status is not None and not 100 <= self.http_status <= 599:
            raise TransportConstructionError("http_status is outside 100..599")
        if type(self.body_bytes) is not bytes:
            raise TransportConstructionError("body_bytes must be bytes")
        if type(self.timed_out) is not bool:
            raise TransportConstructionError("timed_out must be a boolean")
        if self.transport_failure not in (None, "transport"):
            raise TransportConstructionError("unknown transport failure")
        if self.failure_phase not in (None, "before_status", "after_status"):
            raise TransportConstructionError("unknown failure phase")
        if type(self.bounded_headers) is not tuple:
            raise TransportConstructionError("bounded_headers must be a tuple")
        if len(self.bounded_headers) > MAX_XON_HEADER_COUNT:
            raise TransportConstructionError("too many retained headers")
        total_header_bytes = 0
        for header in self.bounded_headers:
            if not isinstance(header, Header):
                raise TransportConstructionError(
                    "bounded_headers contains a non-header"
                )
            total_header_bytes += (
                len(header.name_bytes) + 1 + len(header.value_bytes) + 1
            )
        if total_header_bytes > MAX_XON_RETAINED_HEADER_BYTES:
            raise TransportConstructionError("retained headers exceed the local bound")

        active_failure = self.transport_failure is not None or self.timed_out
        if (self.failure_phase is None) != (not active_failure):
            raise TransportConstructionError("failure phase contradicts failure flags")
        if self.transport_failure is not None and self.timed_out:
            raise TransportConstructionError("transport failure and timeout conflict")

        if self.failure_phase == "before_status":
            if (
                self.http_status is not None
                or self.body_state != "absent"
                or self.body_bytes
                or self.bounded_headers
                or not active_failure
            ):
                raise TransportConstructionError("invalid pre-status failure envelope")
            return

        if self.failure_phase == "after_status":
            if (
                self.http_status is None
                or self.body_state != "incomplete"
                or len(self.body_bytes) > MAX_XON_BODY_BYTES
                or not active_failure
            ):
                raise TransportConstructionError("invalid post-status failure envelope")
            return

        if self.body_state not in ("complete", "over_limit", "absent"):
            raise TransportConstructionError("unknown body state")
        if self.http_status is None:
            raise TransportConstructionError("a complete response needs an HTTP status")
        if active_failure:
            raise TransportConstructionError("complete response cannot have a failure")
        if self.body_state == "complete" and len(self.body_bytes) > MAX_XON_BODY_BYTES:
            raise TransportConstructionError("complete body exceeds the local bound")
        if (
            self.body_state == "over_limit"
            and len(self.body_bytes) != MAX_XON_BODY_BYTES
        ):
            raise TransportConstructionError(
                "over-limit body must retain the full prefix"
            )
        if self.body_state == "absent" and self.body_bytes:
            raise TransportConstructionError("absent body must have no bytes")

    @property
    def normalized_content_type(self) -> str | None:
        """Derive the accepted media type from raw headers, never independently."""

        try:
            return _derive_content_type(self.bounded_headers)
        except _UntrustedMetadataError:
            return None


@dataclass(frozen=True, slots=True)
class TransportClassification:
    """Transport result before XON body parsing."""

    disposition: TransportDisposition
    reason: str
    normalized_content_type: str | None


def make_trusted_context(
    *,
    scan_id: str,
    source_check_id: str,
    subject_ref: str,
    diagnostics: DiagnosticMetadata | None = None,
) -> TrustedContext:
    """Construct the only trusted context accepted by this selected adapter."""

    return TrustedContext(
        scan_id=scan_id,
        source_check_id=source_check_id,
        subject_ref=subject_ref,
        source=XON_SOURCE,
        diagnostics=diagnostics or DiagnosticMetadata("synthetic-time"),
    )


def _ascii_lower(value: bytes) -> bytes:
    if any(byte > 0x7F for byte in value):
        raise _UntrustedMetadataError("header name is not ASCII")
    return bytes(byte + 0x20 if 0x41 <= byte <= 0x5A else byte for byte in value)


def _validate_header_shape(header: Header) -> bytes:
    lowered = _ascii_lower(header.name_bytes)
    token_bytes = (
        b"!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    )
    if not lowered or any(byte not in token_bytes for byte in header.name_bytes):
        raise _UntrustedMetadataError("header name is malformed")
    if b"\r" in header.value_bytes or b"\n" in header.value_bytes:
        raise _UntrustedMetadataError("header value is malformed")
    return lowered


def _derive_content_type(headers: tuple[Header, ...]) -> str | None:
    names: set[bytes] = set()
    content_types: list[bytes] = []
    allowed = {
        b"content-type",
        b"content-length",
        b"retry-after",
        b"date",
        b"etag",
        b"last-modified",
        b"location",
        b"server",
    }
    for header in headers:
        name = _validate_header_shape(header)
        if name in names:
            raise _UntrustedMetadataError("duplicate header name")
        names.add(name)
        if name not in allowed:
            raise _UntrustedMetadataError("unsupported retained header name")
        if name == b"content-type":
            content_types.append(header.value_bytes)
    if not content_types:
        return None
    value = content_types[0].strip(b" \t")
    if any(byte > 0x7F for byte in value):
        raise _UntrustedMetadataError("content type is not ASCII")
    if b";" in value:
        raise _UntrustedMetadataError("content type has parameters")
    if value.lower() != b"application/json":
        raise _UntrustedMetadataError("content type is not application/json")
    return "application/json"


def classify_transport(attempt: TransportAttempt) -> TransportClassification:
    """Classify transport state without interpreting response observations."""

    if attempt.failure_phase == "before_status":
        return TransportClassification(
            TransportDisposition.FAILED, "pre_status_failure", None
        )
    status = attempt.http_status
    assert status is not None
    if status >= 400:
        return TransportClassification(
            TransportDisposition.FAILED, "http_failure", None
        )
    if attempt.failure_phase == "after_status":
        return TransportClassification(
            TransportDisposition.INCOMPLETE, "post_status_body_failure", None
        )
    if attempt.body_state == "over_limit":
        return TransportClassification(
            TransportDisposition.INCOMPLETE, "body_over_limit", None
        )

    try:
        content_type = _derive_content_type(attempt.bounded_headers)
    except _UntrustedMetadataError as error:
        return TransportClassification(
            TransportDisposition.UNVERIFIABLE, str(error), None
        )

    if status != 200:
        return TransportClassification(
            TransportDisposition.UNVERIFIABLE, "unsupported_http_status", content_type
        )
    if attempt.body_state == "absent":
        return TransportClassification(
            TransportDisposition.UNVERIFIABLE, "absent_body", content_type
        )
    if content_type != "application/json":
        return TransportClassification(
            TransportDisposition.UNVERIFIABLE, "incompatible_content_type", content_type
        )
    return TransportClassification(TransportDisposition.READY, "ready", content_type)


class _XONBodyError(ValueError):
    pass


class _DuplicateJSONKey(Exception):
    pass


class _NonStandardJSONConstant(Exception):
    pass


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJSONKey
        result[key] = value
    return result


def _reject_constant(_value: str) -> float:
    raise _NonStandardJSONConstant


def _xon_text(value: object, *, maximum: int, field_name: str) -> str:
    if type(value) is not str:
        raise _XONBodyError(f"{field_name} is not a string")
    if not 1 <= len(value) <= maximum:
        raise _XONBodyError(f"{field_name} is outside its bound")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise _XONBodyError(f"{field_name} contains a surrogate")
    if unicodedata.normalize("NFC", value) != value:
        raise _XONBodyError(f"{field_name} is not NFC")
    return value


def _parse_xon_body(raw: bytes, trusted_context: TrustedContext) -> list[str]:
    try:
        text = raw.decode("utf-8", errors="strict")
        decoded = json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, _DuplicateJSONKey):
        raise _XONBodyError("invalid JSON or duplicate key") from None
    except _NonStandardJSONConstant:
        raise _XONBodyError("non-standard JSON constant") from None
    except RecursionError:
        raise _XONBodyError("JSON nesting is too deep") from None
    except ValueError:
        raise _XONBodyError("invalid JSON value") from None

    if type(decoded) is not dict:
        raise _XONBodyError("top level is not an object")
    if set(decoded) != {"breaches", "email", "status"}:
        raise _XONBodyError("top-level keys are not exact")
    status = decoded["status"]
    if type(status) is not str or status != "success":
        raise _XONBodyError("status is not success")
    email = _xon_text(
        decoded["email"], maximum=MAX_XON_EMAIL_CODEPOINTS, field_name="email"
    )
    if email != trusted_context.subject_ref:
        raise _XONBodyError("response email does not match the local request")
    breaches = decoded["breaches"]
    if type(breaches) is not list or len(breaches) != 1:
        raise _XONBodyError("breaches must contain one inner array")
    names = breaches[0]
    if type(names) is not list or not 1 <= len(names) <= MAX_XON_BREACH_NAMES:
        raise _XONBodyError("breach-name collection is empty or outside its bound")
    return [
        _xon_text(
            name,
            maximum=MAX_XON_BREACH_NAME_CODEPOINTS,
            field_name="breach name",
        )
        for name in names
    ]


def serialize_r2_envelope(
    *, outcome: str, results: Sequence[Mapping[str, object]] = ()
) -> bytes:
    """Build the deterministic existing-R2 envelope and enforce its byte guard."""

    if outcome not in {"completed", "failed", "unverifiable", "incomplete"}:
        raise TransportConstructionError("unsupported generated R2 outcome")
    ordered_results: list[dict[str, object]] = []
    for result in results:
        if set(result) != {"finding_key", "kind", "locator", "material"}:
            raise TransportConstructionError("generated result keys are not exact")
        ordered_results.append(
            {
                "finding_key": result["finding_key"],
                "kind": result["kind"],
                "locator": result["locator"],
                "material": result["material"],
            }
        )
    envelope = {
        "contract_version": "fixture-response/1",
        "source_id": XON_SOURCE_ID,
        "outcome": outcome,
        "results": ordered_results,
    }
    try:
        encoded = json.dumps(
            envelope,
            ensure_ascii=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise TransportConstructionError("generated R2 envelope is not JSON") from error
    if len(encoded) > MAX_INPUT_BYTES:
        raise R2EnvelopeTooLargeError("generated R2 envelope exceeds MAX_INPUT_BYTES")
    return encoded


def _normalize_r2(
    context: TrustedContext,
    *,
    outcome: str,
    results: Sequence[Mapping[str, object]] = (),
) -> SourceCheck:
    return normalize_response(
        serialize_r2_envelope(outcome=outcome, results=results), context
    )


def normalize_check_email(attempt: TransportAttempt) -> SourceCheck:
    """Normalize one frozen synthetic check-email attempt through existing R2."""

    classification = classify_transport(attempt)
    context = attempt.trusted_context
    if classification.disposition is TransportDisposition.FAILED:
        return _normalize_r2(context, outcome="failed")
    if classification.disposition is TransportDisposition.INCOMPLETE:
        return _normalize_r2(context, outcome="incomplete")
    if classification.disposition is TransportDisposition.UNVERIFIABLE:
        return _normalize_r2(context, outcome="unverifiable")

    try:
        names = _parse_xon_body(attempt.body_bytes, context)
    except _XONBodyError:
        return _normalize_r2(context, outcome="unverifiable")
    results = tuple(
        {
            "finding_key": f"breach:{name}",
            "kind": "breach",
            "locator": f"breach:{name}",
            "material": {},
        }
        for name in names
    )
    return _normalize_r2(context, outcome="completed", results=results)


__all__ = [
    "BodyState",
    "FailurePhase",
    "Header",
    "MAX_XON_BODY_BYTES",
    "MAX_XON_BREACH_NAME_CODEPOINTS",
    "MAX_XON_BREACH_NAMES",
    "MAX_XON_EMAIL_CODEPOINTS",
    "MAX_XON_HEADER_COUNT",
    "MAX_XON_HEADER_NAME_BYTES",
    "MAX_XON_HEADER_VALUE_BYTES",
    "MAX_XON_RETAINED_HEADER_BYTES",
    "R2EnvelopeTooLargeError",
    "TransportAttempt",
    "TransportClassification",
    "TransportConstructionError",
    "TransportDisposition",
    "XON_ADAPTER_ID",
    "XON_ADAPTER_VERSION",
    "XON_CANONICAL_SCOPE",
    "XON_NORMALIZATION_VERSION",
    "XON_SCHEMA_VERSION",
    "XON_SOURCE",
    "XON_SOURCE_ID",
    "classify_transport",
    "make_trusted_context",
    "normalize_check_email",
    "serialize_r2_envelope",
]
