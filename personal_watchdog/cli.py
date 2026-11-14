"""Minimal local R6 workflow over the existing R1 and R2 boundaries.

This module is deliberately an offline workflow prototype.  It stores only
bounded structured scan records in a local JSON state directory, uses one
synthetic fixture source, and never opens a network connection.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from personal_watchdog.comparison import (
    ComparisonReport,
    ComparisonResult,
    DiagnosticMetadata,
    ExposureEvent,
    FrozenList,
    FrozenObject,
    GuardingEvent,
    Observation,
    ScanAttempt,
    ScanPlan,
    SourceCheck,
    SourceIdentity,
    SourceStatus,
    compare_scans,
)
from personal_watchdog.profiles import (
    PROFILE_KINDS,
    ProfileError,
    ProfileKind,
    add_profile,
    current_subject_refs,
    delete_profile,
    disable_profile,
    enable_profile,
    ensure_profiles,
    is_profile_subject_ref,
    read_value_from_stdin,
    redacted_profiles,
    selected_profile,
)
from personal_watchdog.response_normalizer import TrustedContext, normalize_response
from personal_watchdog.xon_live import (
    LIVE_HOST,
    LiveCaptureError,
    _Opener,
    capture_check_email,
)
from personal_watchdog.xposedornot_check_email_adapter import (
    XON_SOURCE,
    classify_transport,
    make_trusted_context,
    normalize_check_email,
    serialize_r2_envelope,
)

STATE_VERSION = "local-workflow/2"
MAX_RETAINED_SCANS = 32
FIXTURE_ADAPTER = "fixture"
LIVE_ADAPTER = "xposedornot"
ADAPTER_NAMES = (FIXTURE_ADAPTER, LIVE_ADAPTER)
DEFAULT_SUBJECT_REF = "fixture-subject-01"
SUBJECT_REF_PATTERN = re.compile(r"^fixture-[a-z0-9][a-z0-9-]{0,62}$", re.ASCII)
FixtureName = Literal[
    "baseline",
    "unchanged",
    "changed",
    "disappeared",
    "failed",
    "unverifiable",
]
FIXTURE_NAMES: tuple[FixtureName, ...] = (
    "baseline",
    "unchanged",
    "changed",
    "disappeared",
    "failed",
    "unverifiable",
)

FIXTURE_SOURCE = SourceIdentity(
    source_id="fixture-source",
    canonical_scope=("synthetic-fixture-v1",),
    adapter_id="synthetic-r2-adapter",
    adapter_version="1",
    schema_version=1,
    normalization_version=1,
    material_fields=frozenset({"display_state", "labels", "ordered"}),
    set_like_fields=frozenset({"labels"}),
)


class WorkflowError(ValueError):
    """A safe, user-facing local workflow error."""


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _state_path(state_dir: Path, name: str) -> Path:
    return state_dir / name


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise WorkflowError(f"cannot read local state file {path.name}") from error
    if type(value) is not dict:
        raise WorkflowError(f"local state file {path.name} is not an object")
    return cast(dict[str, Any], value)


def _atomic_write_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        temporary.write_text(_canonical_json(value) + "\n", encoding="utf-8")
        temporary.replace(path)
    except OSError as error:
        raise WorkflowError(f"cannot write local state file {path.name}") from error
    finally:
        if temporary.exists():
            temporary.unlink()


def _source_to_dict(source: SourceIdentity) -> dict[str, object]:
    return {
        "source_id": source.source_id,
        "canonical_scope": list(source.canonical_scope),
        "adapter_id": source.adapter_id,
        "adapter_version": source.adapter_version,
        "schema_version": source.schema_version,
        "normalization_version": source.normalization_version,
        "material_fields": sorted(source.material_fields),
        "set_like_fields": sorted(source.set_like_fields),
    }


def _source_from_dict(value: object) -> SourceIdentity:
    if type(value) is not dict:
        raise WorkflowError("local source configuration is malformed")
    source = cast(dict[str, Any], value)
    try:
        return SourceIdentity(
            source_id=cast(str, source["source_id"]),
            canonical_scope=tuple(cast(list[str], source["canonical_scope"])),
            adapter_id=cast(str, source["adapter_id"]),
            adapter_version=cast(str, source["adapter_version"]),
            schema_version=cast(int, source["schema_version"]),
            normalization_version=cast(int, source["normalization_version"]),
            material_fields=frozenset(cast(list[str], source["material_fields"])),
            set_like_fields=frozenset(cast(list[str], source["set_like_fields"])),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise WorkflowError("local source configuration is malformed") from error


def _canonical_to_json(value: object) -> object:
    if isinstance(value, FrozenObject):
        return {key: _canonical_to_json(child) for key, child in value.items}
    if isinstance(value, FrozenList):
        return [_canonical_to_json(child) for child in value.values]
    return value


def _observation_to_dict(observation: Observation) -> dict[str, object]:
    return {
        "finding_key": observation.finding_key,
        "kind": observation.kind,
        "locator": observation.locator,
        "material": _canonical_to_json(observation.material),
        "context": _canonical_to_json(observation.context),
    }


def _diagnostics_to_dict(diagnostics: DiagnosticMetadata) -> dict[str, object]:
    return {
        "recorded_at": diagnostics.recorded_at,
        "duration_ms": diagnostics.duration_ms,
        "retry_count": diagnostics.retry_count,
        "text": diagnostics.text,
    }


def _check_to_dict(check: SourceCheck) -> dict[str, object]:
    return {
        "source_check_id": check.source_check_id,
        "scan_id": check.scan_id,
        "subject_ref": check.subject_ref,
        "source": _source_to_dict(check.source),
        "status": check.status.value,
        "observations": [_observation_to_dict(item) for item in check.observations],
        "reason_codes": list(check.reason_codes),
        "diagnostics": _diagnostics_to_dict(check.diagnostics),
    }


def _scan_to_dict(scan: ScanAttempt) -> dict[str, object]:
    return {
        "scan_id": scan.scan_id,
        "plan": {
            "subject_ref": scan.plan.subject_ref,
            "sources": [_source_to_dict(item) for item in scan.plan.sources],
            "execution_order": list(scan.plan.execution_order),
        },
        "source_checks": [_check_to_dict(item) for item in scan.source_checks],
        "outcome": scan.outcome.value,
    }


def _diagnostics_from_dict(value: object) -> DiagnosticMetadata:
    if type(value) is not dict:
        raise WorkflowError("local diagnostics are malformed")
    data = cast(dict[str, Any], value)
    try:
        return DiagnosticMetadata(
            recorded_at=cast(str, data["recorded_at"]),
            duration_ms=cast(int, data["duration_ms"]),
            retry_count=cast(int, data["retry_count"]),
            text=cast(str, data["text"]),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise WorkflowError("local diagnostics are malformed") from error


def _observation_from_dict(value: object, source: SourceIdentity) -> Observation:
    if type(value) is not dict:
        raise WorkflowError("local observation is malformed")
    data = cast(dict[str, Any], value)
    context = data.get("context")
    if context is not None and type(context) is not dict:
        raise WorkflowError("local observation context is malformed")
    try:
        return source.observation(
            finding_key=cast(str, data["finding_key"]),
            kind=cast(str, data["kind"]),
            locator=cast(str, data["locator"]),
            material=cast(Mapping[str, object], data["material"]),
            context=cast(Mapping[str, object] | None, context),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise WorkflowError("local observation is malformed") from error


def _check_from_dict(value: object) -> SourceCheck:
    if type(value) is not dict:
        raise WorkflowError("local source check is malformed")
    data = cast(dict[str, Any], value)
    try:
        source = _source_from_dict(data["source"])
        source_check_id = cast(str, data["source_check_id"])
        scan_id = cast(str, data["scan_id"])
        subject_ref = cast(str, data["subject_ref"])
        diagnostics = _diagnostics_from_dict(data["diagnostics"])
        status = cast(str, data["status"])
        reasons = cast(list[str], data["reason_codes"])
        if status == SourceStatus.COMPLETED.value:
            observations = tuple(
                _observation_from_dict(item, source)
                for item in cast(list[object], data["observations"])
            )
            return SourceCheck.completed(
                source_check_id=source_check_id,
                scan_id=scan_id,
                subject_ref=subject_ref,
                source=source,
                diagnostics=diagnostics,
                observations=observations,
                reason_codes=reasons,
            )
        if status == SourceStatus.FAILED.value:
            return SourceCheck.failed(
                source_check_id=source_check_id,
                scan_id=scan_id,
                subject_ref=subject_ref,
                source=source,
                diagnostics=diagnostics,
                reason_codes=reasons,
            )
        if status == SourceStatus.UNVERIFIABLE.value:
            return SourceCheck.unverifiable(
                source_check_id=source_check_id,
                scan_id=scan_id,
                subject_ref=subject_ref,
                source=source,
                diagnostics=diagnostics,
                reason_codes=reasons,
            )
    except (KeyError, TypeError, ValueError) as error:
        raise WorkflowError("local source check is malformed") from error
    raise WorkflowError("local source check has an unsupported status")


def _scan_from_dict(value: object) -> ScanAttempt:
    if type(value) is not dict:
        raise WorkflowError("local scan is malformed")
    data = cast(dict[str, Any], value)
    try:
        plan_data = cast(dict[str, Any], data["plan"])
        plan = ScanPlan.create(
            subject_ref=cast(str, plan_data["subject_ref"]),
            sources=(
                _source_from_dict(item)
                for item in cast(list[object], plan_data["sources"])
            ),
            execution_order=cast(list[str], plan_data["execution_order"]),
        )
        checks = tuple(
            _check_from_dict(item) for item in cast(list[object], data["source_checks"])
        )
        return ScanAttempt.create(
            scan_id=cast(str, data["scan_id"]),
            plan=plan,
            source_checks=checks,
        )
    except (KeyError, TypeError, ValueError) as error:
        raise WorkflowError("local scan is malformed") from error


def _comparison_to_dict(
    value: ComparisonReport | ComparisonResult | ExposureEvent | GuardingEvent,
) -> dict[str, object]:
    if isinstance(value, ComparisonReport):
        return {
            "baseline_created_sources": list(value.baseline_created_sources),
            "comparisons": [_comparison_to_dict(item) for item in value.comparisons],
            "exposure_events": [
                _comparison_to_dict(item) for item in value.exposure_events
            ],
            "guarding_events": [
                _comparison_to_dict(item) for item in value.guarding_events
            ],
        }
    if isinstance(value, ComparisonResult):
        return {
            "comparison_id": value.comparison_id,
            "subject_ref": value.subject_ref,
            "source_id": value.source_id,
            "baseline_scan_id": value.baseline_scan_id,
            "current_scan_id": value.current_scan_id,
            "finding_key": value.finding_key,
            "kind": value.kind.value,
            "changed_field_paths": list(value.changed_field_paths),
            "reason_codes": list(value.reason_codes),
        }
    if isinstance(value, GuardingEvent):
        return {
            "guard_id": value.guard_id,
            "subject_ref": value.subject_ref,
            "source_id": value.source_id,
            "baseline_scan_id": value.baseline_scan_id,
            "current_scan_id": value.current_scan_id,
            "guard_kind": value.guard_kind.value,
            "prior_status": (
                value.prior_status.value if value.prior_status is not None else None
            ),
            "current_status": value.current_status.value,
            "reason_codes": list(value.reason_codes),
        }
    if isinstance(value, ExposureEvent):
        return {
            "comparison_id": value.comparison_id,
            "subject_ref": value.subject_ref,
            "source_id": value.source_id,
            "finding_key": value.finding_key,
            "kind": value.kind.value,
            "changed_field_paths": list(value.changed_field_paths),
        }
    raise TypeError("unsupported comparison record")


def _config(subject_ref: str = DEFAULT_SUBJECT_REF) -> dict[str, object]:
    return {
        "config_version": STATE_VERSION,
        "subject_ref": subject_ref,
        "sources": [_source_to_dict(FIXTURE_SOURCE)],
        "retention": {"max_scans": MAX_RETAINED_SCANS},
    }


def _load_config(state_dir: Path) -> tuple[dict[str, Any], SourceIdentity]:
    value = _read_json(_state_path(state_dir, "config.json"))
    try:
        if value["config_version"] != STATE_VERSION:
            raise WorkflowError("unsupported local configuration version")
        subject_ref = cast(str, value["subject_ref"])
        if SUBJECT_REF_PATTERN.fullmatch(subject_ref) is None:
            raise WorkflowError("local subject_ref is outside the synthetic scope")
        sources = cast(list[object], value["sources"])
        if len(sources) != 1:
            raise WorkflowError("local configuration must contain one source")
        source = _source_from_dict(sources[0])
        if source != FIXTURE_SOURCE:
            raise WorkflowError("local configuration has an unsupported source")
        return value, source
    except (KeyError, TypeError, ValueError) as error:
        if isinstance(error, WorkflowError):
            raise
        raise WorkflowError("local configuration is malformed") from error


def _load_history(state_dir: Path) -> dict[str, Any]:
    value = _read_json(_state_path(state_dir, "history.json"))
    if value.get("history_version") != STATE_VERSION:
        raise WorkflowError("unsupported local history version")
    if type(value.get("scans")) is not list:
        raise WorkflowError("local history scans are malformed")
    return value


def _ensure_state(state_dir: Path) -> None:
    if (
        not _state_path(state_dir, "config.json").is_file()
        or not _state_path(state_dir, "history.json").is_file()
    ):
        raise WorkflowError("local state is not initialized; run init first")


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _fixture_envelope(name: FixtureName) -> bytes:
    if name in {"baseline", "unchanged"}:
        material = {
            "display_state": "present",
            "labels": ["example"],
            "ordered": ["first"],
        }
        results = [
            {
                "finding_key": "fixture-finding-1",
                "kind": "exposure",
                "locator": "fixture-locator-1",
                "material": material,
            }
        ]
        outcome = "completed"
    elif name == "changed":
        results = [
            {
                "finding_key": "fixture-finding-1",
                "kind": "exposure",
                "locator": "fixture-locator-1",
                "material": {
                    "display_state": "changed",
                    "labels": ["example", "changed"],
                    "ordered": ["first", "second"],
                },
            }
        ]
        outcome = "completed"
    elif name == "disappeared":
        results = []
        outcome = "completed"
    else:
        results = []
        outcome = name
    return json.dumps(
        {
            "contract_version": "fixture-response/1",
            "source_id": FIXTURE_SOURCE.source_id,
            "outcome": outcome,
            "results": results,
        },
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _make_scan(
    *,
    scan_id: str,
    subject_ref: str,
    source: SourceIdentity,
    fixture: FixtureName,
) -> ScanAttempt:
    context = TrustedContext(
        scan_id=scan_id,
        source_check_id=f"{scan_id}:{source.source_id}",
        subject_ref=subject_ref,
        source=source,
        diagnostics=DiagnosticMetadata(_now()),
    )
    check = normalize_response(_fixture_envelope(fixture), context)
    plan = ScanPlan.create(subject_ref=subject_ref, sources=(source,))
    return ScanAttempt.create(scan_id=scan_id, plan=plan, source_checks=(check,))


def _record(
    scan: ScanAttempt, report: ComparisonReport, fixture: FixtureName | None
) -> dict[str, object]:
    record: dict[str, object] = {
        "fixture": fixture,
        "scan": _scan_to_dict(scan),
        "comparison": _comparison_to_dict(report),
    }
    if fixture is None:
        record["adapter"] = LIVE_ADAPTER
    return record


def _origin(record: Mapping[str, object]) -> str:
    """Describe where a stored scan came from: a named fixture or a live adapter."""

    if record.get("fixture") is None:
        return f"adapter={record.get('adapter', 'unknown')}"
    return f"fixture={record['fixture']}"


def _baseline_for(
    records: Sequence[Mapping[str, Any]], scan: ScanAttempt
) -> ScanAttempt | None:
    """Pick the baseline for one subject and source from retained history.

    Scans of other subjects or other sources are never a baseline. The most
    recent completed check is preferred, so a failed or unverifiable scan in
    between does not erase the comparison point; without one, the most recent
    earlier attempt is used and the comparison model treats it as no baseline.
    """

    source_id = scan.source_checks[0].source.source_id
    fallback: ScanAttempt | None = None
    for record in reversed(records):
        stored = cast(dict[str, Any], record["scan"])
        if stored["plan"]["subject_ref"] != scan.plan.subject_ref:
            continue
        checks = cast(list[dict[str, Any]], stored["source_checks"])
        match = [item for item in checks if item["source"]["source_id"] == source_id]
        if not match:
            continue
        if match[0]["status"] == SourceStatus.COMPLETED.value:
            return _scan_from_dict(stored)
        if fallback is None:
            fallback = _scan_from_dict(stored)
    return fallback


def _make_live_scan(
    *,
    scan_id: str,
    subject_ref: str,
    email: str,
    opener: _Opener | None,
) -> tuple[ScanAttempt, str]:
    """Run one live check; every failure becomes a recorded non-clean check.

    Also returns a display-only transport line holding the HTTP status and
    classification. It never contains the address, URL, headers, or body.
    """

    context = make_trusted_context(
        scan_id=scan_id,
        source_check_id=f"{scan_id}:{XON_SOURCE.source_id}",
        subject_ref=subject_ref,
        diagnostics=DiagnosticMetadata(_now()),
    )
    try:
        attempt = capture_check_email(email=email, context=context, opener=opener)
        check = normalize_check_email(attempt)
        transport = classify_transport(attempt)
        status = "none" if attempt.http_status is None else str(attempt.http_status)
        line = (
            f"TRANSPORT http_status={status} "
            f"disposition={transport.disposition.value} reason={transport.reason}"
        )
    except LiveCaptureError:
        check = normalize_response(
            serialize_r2_envelope(outcome="unverifiable"), context
        )
        line = (
            "TRANSPORT http_status=unknown disposition=unverifiable "
            "reason=unreadable_response_metadata"
        )
    plan = ScanPlan.create(subject_ref=subject_ref, sources=(XON_SOURCE,))
    scan = ScanAttempt.create(scan_id=scan_id, plan=plan, source_checks=(check,))
    return scan, line


def _load_records(history: dict[str, Any]) -> list[dict[str, Any]]:
    return [cast(dict[str, Any], item) for item in cast(list[object], history["scans"])]


def _human_report(record: Mapping[str, object]) -> str:
    scan = cast(dict[str, Any], record["scan"])
    check = cast(dict[str, Any], cast(list[object], scan["source_checks"])[0])
    comparison = cast(dict[str, Any], record["comparison"])
    finding_keys = [item["finding_key"] for item in check["observations"]]
    lines = [
        f"SCAN scan_id={scan['scan_id']} subject_ref={scan['plan']['subject_ref']} "
        f"outcome={scan['outcome']} {_origin(record)}",
        f"SOURCE source_id={check['source']['source_id']} status={check['status']} "
        f"reason_codes={_canonical_json(check['reason_codes'])} "
        f"finding_keys={_canonical_json(finding_keys)}",
    ]
    for source_id in comparison["baseline_created_sources"]:
        lines.append(f"BASELINE_CREATED source_id={source_id}")
    for item in comparison["comparisons"]:
        lines.append(
            f"COMPARISON kind={item['kind']} source_id={item['source_id']} "
            f"finding_key={item['finding_key']} "
            f"reason_codes={_canonical_json(item['reason_codes'])}"
        )
    for item in comparison["exposure_events"]:
        lines.append(
            f"EXPOSURE_EVENT kind={item['kind']} source_id={item['source_id']} "
            f"finding_key={item['finding_key']}"
        )
    for item in comparison["guarding_events"]:
        lines.append(
            f"GUARDING_EVENT kind={item['guard_kind']} source_id={item['source_id']} "
            f"current_status={item['current_status']} "
            f"reason_codes={_canonical_json(item['reason_codes'])}"
        )
    return "\n".join(lines) + "\n"


def _cmd_init(state_dir: Path) -> int:
    if (
        _state_path(state_dir, "config.json").exists()
        or _state_path(state_dir, "history.json").exists()
    ):
        raise WorkflowError("local state already exists")
    state_dir.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(state_dir / "config.json", _config())
    _atomic_write_json(
        state_dir / "history.json",
        {"history_version": STATE_VERSION, "next_scan_number": 1, "scans": []},
    )
    ensure_profiles(state_dir)
    print(f"INITIALIZED subject_ref={DEFAULT_SUBJECT_REF} source_id=fixture-source")
    return 0


def _cmd_scan(
    state_dir: Path,
    adapter: str,
    fixture: FixtureName | None,
    subject_ref: str | None,
    confirm_live: str | None = None,
    opener: _Opener | None = None,
) -> int:
    if adapter not in ADAPTER_NAMES:
        raise WorkflowError("unknown adapter")
    live = adapter == LIVE_ADAPTER
    if live:
        if fixture is not None:
            raise WorkflowError("--fixture cannot be used with a live adapter")
        if subject_ref is None:
            raise WorkflowError("a live scan requires --subject-ref")
        if confirm_live is None or confirm_live != subject_ref:
            raise WorkflowError(
                "a live scan sends the profile's email address to "
                f"{LIVE_HOST}; confirm with --confirm-live matching --subject-ref"
            )
    elif confirm_live is not None:
        raise WorkflowError("--confirm-live applies only to a live adapter")
    _ensure_state(state_dir)
    config, source = _load_config(state_dir)
    history = _load_history(state_dir)
    records = _load_records(history)
    selected_ref = cast(str, config["subject_ref"])
    selected: dict[str, Any] | None = None
    transport_line = ""
    if subject_ref is not None:
        try:
            selected = selected_profile(state_dir, subject_ref)
        except ProfileError as error:
            raise WorkflowError(str(error)) from error
        selected_ref = cast(str, selected["subject_ref"])
    number = cast(int, history.get("next_scan_number"))
    scan_id = f"scan-{number:03d}"
    if live:
        assert selected is not None
        if selected["kind"] != "email":
            raise WorkflowError("a live scan requires an email profile")
        print(
            f"LIVE_REQUEST destination={LIVE_HOST} source_id={XON_SOURCE.source_id} "
            f"subject_ref={selected_ref} sends=email-address requests=1"
        )
        scan, transport_line = _make_live_scan(
            scan_id=scan_id,
            subject_ref=selected_ref,
            email=cast(str, selected["value"]),
            opener=opener,
        )
    else:
        scan = _make_scan(
            scan_id=scan_id,
            subject_ref=selected_ref,
            source=source,
            fixture=fixture or "baseline",
        )
    report = compare_scans(_baseline_for(records, scan), scan)
    records.append(_record(scan, report, None if live else fixture or "baseline"))
    retained = records[-MAX_RETAINED_SCANS:]
    _atomic_write_json(
        _state_path(state_dir, "history.json"),
        {
            "history_version": STATE_VERSION,
            "next_scan_number": number + 1,
            "scans": retained,
        },
    )
    if live:
        print(transport_line)
    print(_human_report(retained[-1]), end="")
    if live and scan.source_checks[0].status is not SourceStatus.COMPLETED:
        print(
            "NOTE this check did not complete; it is not a clean result and "
            "says nothing about exposure"
        )
    return 0


def _cmd_profile_add(
    state_dir: Path,
    kind: ProfileKind,
    purpose: str,
    approve: bool,
    value_stdin: bool,
) -> int:
    _ensure_state(state_dir)
    if not approve:
        raise WorkflowError("profile add requires explicit --approve")
    if not value_stdin:
        raise WorkflowError("profile add requires --value-stdin")
    try:
        profile = add_profile(
            state_dir,
            kind=kind,
            value=read_value_from_stdin(),
            purpose=purpose,
        )
    except ProfileError as error:
        raise WorkflowError(str(error)) from error
    print(
        f"PROFILE_ADDED subject_ref={profile['subject_ref']} kind={profile['kind']} "
        f"approved={str(profile['approved']).upper()} "
        f"enabled={str(profile['enabled']).upper()}"
    )
    return 0


def _cmd_profile_list(state_dir: Path, json_mode: bool) -> int:
    _ensure_state(state_dir)
    try:
        profiles = redacted_profiles(state_dir)
    except ProfileError as error:
        raise WorkflowError(str(error)) from error
    if json_mode:
        print(_canonical_json({"profiles": profiles}))
    else:
        for profile in profiles:
            print(
                f"PROFILE subject_ref={profile['subject_ref']} kind={profile['kind']} "
                f"approved={str(profile['approved']).upper()} "
                f"enabled={str(profile['enabled']).upper()} "
                f"purpose={profile['purpose']}"
            )
        print(f"PROFILES count={len(profiles)}")
    return 0


def _cmd_profile_disable(state_dir: Path, subject_ref: str) -> int:
    _ensure_state(state_dir)
    try:
        disable_profile(state_dir, subject_ref)
    except ProfileError as error:
        raise WorkflowError(str(error)) from error
    print(f"PROFILE_DISABLED subject_ref={subject_ref}")
    return 0


def _cmd_profile_enable(
    state_dir: Path, subject_ref: str, confirm_ref: str | None
) -> int:
    _ensure_state(state_dir)
    try:
        enable_profile(state_dir, subject_ref, confirm_ref=confirm_ref)
    except ProfileError as error:
        raise WorkflowError(str(error)) from error
    print(f"PROFILE_ENABLED subject_ref={subject_ref}")
    return 0


def _cmd_profile_delete(state_dir: Path, subject_ref: str, confirm: bool) -> int:
    _ensure_state(state_dir)
    if not confirm:
        raise WorkflowError("profile delete requires explicit --confirm")
    try:
        delete_profile(state_dir, subject_ref)
    except ProfileError as error:
        raise WorkflowError(str(error)) from error
    print(f"PROFILE_REMOVED subject_ref={subject_ref} (not securely erased)")
    return 0


def _cmd_report(state_dir: Path, json_mode: bool) -> int:
    _ensure_state(state_dir)
    history = _load_history(state_dir)
    records = _load_records(history)
    if not records:
        raise WorkflowError("no scans are available; run scan first")
    record = records[-1]
    if json_mode:
        print(_canonical_json(record))
    else:
        print(_human_report(record), end="")
        note = _profile_note(state_dir, record)
        if note is not None:
            print(note)
    return 0


def _profile_note(state_dir: Path, record: Mapping[str, object]) -> str | None:
    """Derive a display-only note about the scanned profile from current state.

    The stored record is never changed, and the profile value is never read
    into the output. Only approved-profile references are annotated; the
    default fixture subject has no profile record.
    """

    scan = cast(dict[str, Any], record["scan"])
    subject_ref = cast(str, scan["plan"]["subject_ref"])
    if not is_profile_subject_ref(subject_ref):
        return None
    try:
        current = current_subject_refs(state_dir)
    except ProfileError:
        return f"PROFILE_NOTE subject_ref={subject_ref} profile status unavailable"
    if subject_ref in current:
        return None
    return f"PROFILE_NOTE subject_ref={subject_ref} profile since removed"


def _cmd_history(state_dir: Path, json_mode: bool) -> int:
    _ensure_state(state_dir)
    history = _load_history(state_dir)
    records = _load_records(history)
    if json_mode:
        print(_canonical_json({"history_version": STATE_VERSION, "scans": records}))
    else:
        for record in records:
            scan = cast(dict[str, Any], record["scan"])
            check = cast(dict[str, Any], cast(list[object], scan["source_checks"])[0])
            print(
                f"SCAN scan_id={scan['scan_id']} {_origin(record)} "
                f"status={check['status']} outcome={scan['outcome']}"
            )
        print(f"HISTORY scans={len(records)} retained_max={MAX_RETAINED_SCANS}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local R6 watchdog workflow")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="create local synthetic workflow state")
    init.add_argument("--state-dir", type=Path, default=Path(".watchdog"))

    scan = commands.add_parser(
        "scan", help="run one offline fixture scan or one confirmed live check"
    )
    scan.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    scan.add_argument("--adapter", choices=ADAPTER_NAMES, required=True)
    scan.add_argument("--fixture", choices=FIXTURE_NAMES)
    scan.add_argument("--subject-ref")
    scan.add_argument(
        "--confirm-live",
        dest="confirm_live",
        help=(
            "type the subject reference again to send that profile's email "
            f"address in one request to {LIVE_HOST}"
        ),
    )

    profile = commands.add_parser("profile", help="manage local approved profiles")
    profile_commands = profile.add_subparsers(dest="profile_command", required=True)
    profile_add = profile_commands.add_parser("add", help="add one approved profile")
    profile_add.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    profile_add.add_argument("--kind", choices=PROFILE_KINDS, required=True)
    profile_add.add_argument("--purpose", default="personal-watchdog")
    profile_add.add_argument("--approve", action="store_true")
    profile_add.add_argument("--value-stdin", action="store_true")
    profile_list = profile_commands.add_parser("list", help="list redacted profiles")
    profile_list.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    profile_list.add_argument("--json", action="store_true", dest="json_mode")
    profile_disable = profile_commands.add_parser(
        "disable", help="disable one profile without rewriting history"
    )
    profile_disable.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    profile_disable.add_argument("--subject-ref", required=True)
    profile_enable = profile_commands.add_parser(
        "enable", help="re-enable one profile with fresh approval"
    )
    profile_enable.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    profile_enable.add_argument("--subject-ref", required=True)
    profile_enable.add_argument(
        "--confirm-ref",
        dest="confirm_ref",
        help="type the subject reference again to confirm re-enable",
    )
    profile_delete = profile_commands.add_parser(
        "delete",
        help="remove one disabled profile from the local store (not secure erasure)",
    )
    profile_delete.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    profile_delete.add_argument("--subject-ref", required=True)
    profile_delete.add_argument("--confirm", action="store_true")

    report = commands.add_parser("report", help="render the latest local report")
    report.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    report.add_argument("--latest", action="store_true")
    report.add_argument("--json", action="store_true", dest="json_mode")

    history = commands.add_parser("history", help="render retained local history")
    history.add_argument("--state-dir", type=Path, default=Path(".watchdog"))
    history.add_argument("--json", action="store_true", dest="json_mode")
    return parser


def main(argv: Sequence[str] | None = None, *, opener: _Opener | None = None) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "init":
            return _cmd_init(args.state_dir)
        if args.command == "scan":
            return _cmd_scan(
                args.state_dir,
                args.adapter,
                cast("FixtureName | None", args.fixture),
                args.subject_ref,
                args.confirm_live,
                opener,
            )
        if args.command == "profile":
            if args.profile_command == "add":
                return _cmd_profile_add(
                    args.state_dir,
                    cast(ProfileKind, args.kind),
                    args.purpose,
                    args.approve,
                    args.value_stdin,
                )
            if args.profile_command == "list":
                return _cmd_profile_list(args.state_dir, args.json_mode)
            if args.profile_command == "disable":
                return _cmd_profile_disable(args.state_dir, args.subject_ref)
            if args.profile_command == "enable":
                return _cmd_profile_enable(
                    args.state_dir, args.subject_ref, args.confirm_ref
                )
            if args.profile_command == "delete":
                return _cmd_profile_delete(
                    args.state_dir, args.subject_ref, args.confirm
                )
            raise WorkflowError("unknown profile command")
        if args.command == "report":
            if not args.latest:
                raise WorkflowError("report requires --latest")
            return _cmd_report(args.state_dir, args.json_mode)
        if args.command == "history":
            return _cmd_history(args.state_dir, args.json_mode)
        raise WorkflowError("unknown command")
    except (ProfileError, WorkflowError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
