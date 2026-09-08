"""Contract tests for the visible deterministic R2.5 runner."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from personal_watchdog.offline_simulator import (
    MAX_CANONICAL_SCOPE_ITEMS,
    MAX_CHECKS_PER_SCAN,
    MAX_EXPECTED_RECORDS_PER_CHECK,
    MAX_EXPECTED_RECORDS_PER_SCAN,
    MAX_MATERIAL_FIELDS,
    MAX_RESPONSE_BYTES,
    MAX_SCANS,
    MAX_SCENARIO_BYTES,
    MAX_SCENARIO_NESTING,
    MAX_SOURCES,
    MAX_STRING_CODEPOINTS,
    ScenarioInvalid,
    load_scenario,
    main,
    run_scenario,
)
from personal_watchdog.r1 import SourceStatus
from personal_watchdog.r2_adapter import normalize_response
from tests.fixtures_r2_5 import ROOT, read_scenario, run_cli, scenario_paths


@pytest.mark.parametrize("path", scenario_paths(), ids=lambda path: path.stem)
def test_curated_scenarios_pass_in_human_and_json_modes(path: Path) -> None:
    human = run_cli(path)
    machine = run_cli(path, json_mode=True)
    assert human.returncode == 0
    assert human.stderr == ""
    assert human.stdout.startswith("SCENARIO ")
    assert "EXPOSURE_SILENCE actual=" in human.stdout
    assert machine.returncode == 0
    assert machine.stderr == ""
    output = json.loads(machine.stdout)
    assert output["result"] == "pass"
    assert output["diagnostic"] is None
    assert set(output) == {
        "runner_version",
        "scenario_id",
        "result",
        "scans",
        "mismatches",
        "diagnostic",
    }


def test_curated_ids_are_unique_across_fixture_files() -> None:
    ids = [read_scenario(path)["scenario_id"] for path in scenario_paths()]
    assert len(ids) == 10
    assert len(set(ids)) == len(ids)


def test_repeated_machine_output_is_byte_identical() -> None:
    path = scenario_paths()[9]
    first = run_cli(path, json_mode=True)
    second = run_cli(path, json_mode=True)
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == ""


def test_repeated_human_output_is_byte_identical() -> None:
    path = scenario_paths()[9]
    first = run_cli(path)
    second = run_cli(path)
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == ""


def test_exact_golden_human_report() -> None:
    expected = (
        "\n".join(
            [
                'SCENARIO "r25-s01-baseline-silence" result=PASS',
                'SUBJECT "subject-r25-01"',
                'SCAN order=1 total=2 scan_id="r25-s01-baseline-silence:scan-001" '
                'outcome="completed" expectation=PASS',
                'SOURCE_CHECK source_ref="A1" source_id="synthetic-source-a" '
                'source_check_id="r25-s01-baseline-silence:scan-001:check-A1" '
                'input_kind="utf8_text" input_bytes=278 r2_invoked=TRUE '
                'r2_status="completed" r2_reason_codes=[] '
                'r2_finding_keys=["finding-a"] status="completed" reason_codes=[] '
                'finding_keys=["finding-a"]',
                'BASELINE_CREATED source_id="synthetic-source-a"',
                "EXPOSURE_SILENCE actual=TRUE",
                'SCAN order=2 total=2 scan_id="r25-s01-baseline-silence:scan-002" '
                'outcome="completed" expectation=PASS',
                'SOURCE_CHECK source_ref="A1" source_id="synthetic-source-a" '
                'source_check_id="r25-s01-baseline-silence:scan-002:check-A1" '
                'input_kind="utf8_text" input_bytes=278 r2_invoked=TRUE '
                'r2_status="completed" r2_reason_codes=[] '
                'r2_finding_keys=["finding-a"] status="completed" reason_codes=[] '
                'finding_keys=["finding-a"]',
                'COMPARISON comparison_id="r25-s01-baseline-silence:scan-002:'
                'synthetic-source-a:finding-a:unchanged" subject_ref="subject-r25-01" '
                'source_id="synthetic-source-a" '
                'baseline_scan_id="r25-s01-baseline-silence:'
                'scan-001" current_scan_id="r25-s01-baseline-silence:scan-002" '
                'finding_key="finding-a" kind="unchanged" changed_field_paths=[] '
                "reason_codes=[]",
                "EXPOSURE_SILENCE actual=TRUE",
                "SUMMARY scans=2 source_checks=2 comparisons=1 exposure_events=0 "
                "guarding_events=0 mismatches=0",
            ]
        )
        + "\n"
    )
    result = run_cli(ROOT / "scenarios/r2_5_baseline_silence.json")
    assert result.returncode == 0
    assert result.stdout == expected


def test_invalid_human_diagnostic_is_exact(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{", encoding="utf-8")
    result = run_cli(path)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == (
        'INVALID_SCENARIO code=invalid_json path="/" '
        'message="scenario JSON is invalid"\n'
    )


def test_machine_output_is_canonical_compact_json_with_one_terminal_lf() -> None:
    result = run_cli(scenario_paths()[0], json_mode=True)
    assert result.stdout.endswith("\n")
    assert result.stdout.count("\n") == 1
    canonical = (
        json.dumps(
            json.loads(result.stdout),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    )
    assert result.stdout == canonical


def test_machine_nested_key_sets_are_exact() -> None:
    output = json.loads(run_cli(scenario_paths()[9], json_mode=True).stdout)
    assert set(output) == {
        "runner_version",
        "scenario_id",
        "result",
        "scans",
        "mismatches",
        "diagnostic",
    }
    scan = output["scans"][1]
    assert set(scan) == {
        "scan_id",
        "scan_order",
        "source_order",
        "outcome",
        "source_checks",
        "r1",
        "exposure_silence",
    }
    source = scan["source_checks"][0]
    assert set(source) == {
        "source_ref",
        "source_id",
        "source_check_id",
        "input_kind",
        "input_bytes",
        "r2_invoked",
        "r2",
        "r1",
    }
    assert set(source["r2"]) == {"status", "reason_codes", "finding_keys"}
    assert set(source["r1"]) == {"status", "reason_codes", "finding_keys"}
    assert set(scan["r1"]) == {
        "baseline_created_sources",
        "comparisons",
        "exposure_events",
        "guarding_events",
    }
    assert set(scan["r1"]["comparisons"][0]) == {
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
    assert set(scan["r1"]["exposure_events"][0]) == {
        "comparison_id",
        "subject_ref",
        "source_id",
        "finding_key",
        "kind",
        "changed_field_paths",
    }
    failure = json.loads(
        run_cli(ROOT / "scenarios/r2_5_source_failure.json", json_mode=True).stdout
    )
    assert set(failure["scans"][1]["r1"]["guarding_events"][0]) == {
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


def test_hostile_content_is_absent_from_both_output_modes() -> None:
    path = ROOT / "scenarios/r2_5_hostile_false_clean.json"
    for json_mode in (False, True):
        result = run_cli(path, json_mode=json_mode)
        assert result.returncode == 0
        assert "attacker-clean" not in result.stdout


def test_wrong_expected_comparison_id_is_exit_one(tmp_path: Path) -> None:
    value = read_scenario(ROOT / "scenarios/r2_5_material_change.json")
    value["scans"][1]["expected"]["r1"]["comparisons"][0]["comparison_id"] = (
        "oracle-wrong-id"
    )
    path = tmp_path / "wrong.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    result = run_cli(path, json_mode=True)
    assert result.returncode == 1
    output = json.loads(result.stdout)
    assert output["result"] == "expectation_mismatch"
    assert output["mismatches"][0]["expected"] == "oracle-wrong-id"
    assert result.stderr == ""


def test_expected_r2_change_is_exit_one_without_changing_actual_r2(
    tmp_path: Path,
) -> None:
    original = run_cli(scenario_paths()[0], json_mode=True)
    value = read_scenario(scenario_paths()[0])
    value["scans"][1]["checks"][0]["expected"]["r2"]["finding_keys"] = []
    path = tmp_path / "wrong-r2.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    changed = run_cli(path, json_mode=True)
    assert original.returncode == 0
    assert changed.returncode == 1
    original_output = json.loads(original.stdout)
    changed_output = json.loads(changed.stdout)
    assert changed_output["scans"] == original_output["scans"]
    assert changed_output["scans"][1]["source_checks"][0]["r2"]["finding_keys"] == [
        "finding-a"
    ]


def test_mismatch_order_and_paths_ignore_expected_object_key_order(
    tmp_path: Path,
) -> None:
    value = read_scenario(scenario_paths()[9])
    expected = value["scans"][1]["expected"]["r1"]
    comparison = expected["comparisons"][0]
    comparison["comparison_id"] = "wrong-comparison"
    comparison["kind"] = "unchanged"
    expected["exposure_events"][0]["comparison_id"] = "wrong-exposure"
    first_path = tmp_path / "mismatch-first.json"
    first_path.write_text(json.dumps(value), encoding="utf-8")

    reordered = read_scenario(scenario_paths()[9])
    expected = reordered["scans"][1]["expected"]["r1"]
    comparison = expected["comparisons"][0]
    comparison["comparison_id"] = "wrong-comparison"
    comparison["kind"] = "unchanged"
    expected["exposure_events"][0]["comparison_id"] = "wrong-exposure"
    # Reinsert records with the same values but adversarial object insertion order.
    expected["comparisons"][0] = {
        key: expected["comparisons"][0][key]
        for key in reversed(list(expected["comparisons"][0]))
    }
    expected["exposure_events"][0] = {
        key: expected["exposure_events"][0][key]
        for key in reversed(list(expected["exposure_events"][0]))
    }
    second_path = tmp_path / "mismatch-reordered.json"
    second_path.write_text(json.dumps(reordered), encoding="utf-8")

    first = json.loads(run_cli(first_path, json_mode=True).stdout)
    second = json.loads(run_cli(second_path, json_mode=True).stdout)
    assert first["result"] == second["result"] == "expectation_mismatch"
    assert first["mismatches"] == second["mismatches"]
    assert [item["path"] for item in first["mismatches"]] == [
        "/scans/1/expected/r1/comparisons/0/comparison_id",
        "/scans/1/expected/r1/comparisons/0/kind",
        "/scans/1/expected/r1/exposure_events/0/comparison_id",
    ]


def test_source_order_does_not_replace_r1_canonical_order(tmp_path: Path) -> None:
    value = read_scenario(ROOT / "scenarios/r2_5_mixed_source_failure_and_change.json")
    scan = value["scans"][1]
    scan["source_order"] = ["B1", "A1"]
    scan["checks"] = [scan["checks"][1], scan["checks"][0]]
    path = tmp_path / "reordered.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    result = run_cli(path, json_mode=True)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    current = output["scans"][1]
    assert [item["source_ref"] for item in current["source_checks"]] == ["B1", "A1"]
    assert [item["source_id"] for item in current["r1"]["comparisons"]] == [
        "synthetic-source-a",
        "synthetic-source-b",
    ]


def test_local_construction_error_does_not_invoke_r2() -> None:
    scenario = load_scenario(
        ROOT / "scenarios/r2_5_mixed_source_failure_and_change.json"
    )
    with patch(
        "personal_watchdog.offline_simulator.normalize_response",
        wraps=normalize_response,
    ) as mocked:
        run = run_scenario(scenario)
    assert mocked.call_count == 3
    local = run.output["scans"][1]["source_checks"][0]
    assert local["r2_invoked"] is False
    assert local["r2"] is None
    assert local["r1"]["status"] == SourceStatus.FAILED.value


def test_failure_unverifiable_and_hostile_response_remain_visible() -> None:
    failure = json.loads(
        run_cli(ROOT / "scenarios/r2_5_source_failure.json", json_mode=True).stdout
    )
    unverifiable = json.loads(
        run_cli(ROOT / "scenarios/r2_5_unverifiable_source.json", json_mode=True).stdout
    )
    hostile = json.loads(
        run_cli(ROOT / "scenarios/r2_5_hostile_false_clean.json", json_mode=True).stdout
    )
    for output in (failure, unverifiable, hostile):
        check = output["scans"][1]["source_checks"][0]
        assert check["r1"]["status"] in {"failed", "unverifiable"}
        assert output["scans"][1]["r1"]["comparisons"][0]["kind"] == "not_comparable"
        assert output["scans"][1]["r1"]["exposure_events"] == []
        assert output["scans"][1]["exposure_silence"] is True
    assert (
        "attacker-clean"
        not in run_cli(ROOT / "scenarios/r2_5_hostile_false_clean.json").stdout
    )
    assert unverifiable["scans"][1]["source_checks"][0]["r2"]["reason_codes"] == [
        "invalid_utf8"
    ]
    assert hostile["scans"][1]["source_checks"][0]["r2"]["reason_codes"] == [
        "unknown_field"
    ]


def test_invalid_utf8_raw_bytes_are_not_disclosed() -> None:
    result = run_cli(ROOT / "scenarios/r2_5_unverifiable_source.json")
    assert result.returncode == 0
    assert "ff" not in result.stdout.lower()
    assert "invalid_utf8" in result.stdout


def _invalid_result(path: Path, *, json_mode: bool = False) -> tuple[int, str, str]:
    result = run_cli(path, json_mode=json_mode)
    return result.returncode, result.stdout, result.stderr


def test_duplicate_keys_unknown_fields_missing_fields_and_boolean_integer(
    tmp_path: Path,
) -> None:
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        '{"scenario_version":"x","scenario_version":"y"}', encoding="utf-8"
    )
    code, stdout, stderr = _invalid_result(duplicate)
    assert code == 2 and stdout == "" and "code=duplicate_json_key" in stderr

    base = read_scenario(scenario_paths()[0])
    base["unknown"] = True
    unknown = tmp_path / "unknown.json"
    unknown.write_text(json.dumps(base), encoding="utf-8")
    assert _invalid_result(unknown)[0] == 2
    del base["unknown"]
    del base["subject_ref"]
    missing = tmp_path / "missing.json"
    missing.write_text(json.dumps(base), encoding="utf-8")
    assert _invalid_result(missing)[0] == 2

    typed = read_scenario(scenario_paths()[0])
    typed["sources"][0]["schema_version"] = True
    boolean = tmp_path / "boolean.json"
    boolean.write_text(json.dumps(typed), encoding="utf-8")
    assert "code=invalid_type" in _invalid_result(boolean)[2]


@pytest.mark.parametrize(
    "kind",
    [
        "bytes",
        "nesting",
        "sources",
        "scans",
        "checks",
        "strings",
        "canonical_scope",
        "material_fields",
        "set_like_fields",
        "expected_check_records",
        "expected_scan_records",
        "utf8_response_bytes",
        "hex_response_bytes",
    ],
)
def test_every_fixed_outer_bound_is_rejected(tmp_path: Path, kind: str) -> None:
    if kind == "bytes":
        path = tmp_path / "bytes.json"
        path.write_bytes(b"x" * (MAX_SCENARIO_BYTES + 1))
    elif kind == "nesting":
        path = tmp_path / "nesting.json"
        path.write_text(
            "[" * (MAX_SCENARIO_NESTING + 2) + "0" + "]" * (MAX_SCENARIO_NESTING + 2),
            encoding="utf-8",
        )
    else:
        value = read_scenario(scenario_paths()[0])
        if kind == "sources":
            source = dict(value["sources"][0])
            source["source_ref"] = "Z1"
            value["sources"] = value["sources"] * MAX_SOURCES + [source]
        elif kind == "scans":
            value["scans"] = value["scans"] * MAX_SCANS + [value["scans"][0]]
        elif kind == "checks":
            scan = value["scans"][0]
            scan["source_order"] = ["A1"] * (MAX_CHECKS_PER_SCAN + 1)
            scan["checks"] = scan["checks"] * (MAX_CHECKS_PER_SCAN + 1)
        elif kind == "strings":
            value["subject_ref"] = "x" * (MAX_STRING_CODEPOINTS + 1)
        elif kind == "canonical_scope":
            value["sources"][0]["canonical_scope"] = [
                f"scope-{index:02d}" for index in range(MAX_CANONICAL_SCOPE_ITEMS + 1)
            ]
        elif kind == "material_fields":
            value["sources"][0]["material_fields"] = [
                f"field-{index:02d}" for index in range(MAX_MATERIAL_FIELDS + 1)
            ]
        elif kind == "set_like_fields":
            value["sources"][0]["set_like_fields"] = [
                f"field-{index:02d}" for index in range(MAX_MATERIAL_FIELDS + 1)
            ]
        elif kind == "expected_check_records":
            value["scans"][0]["checks"][0]["expected"]["r2"]["finding_keys"] = [
                "finding-a"
            ] * (MAX_EXPECTED_RECORDS_PER_CHECK + 1)
        elif kind == "expected_scan_records":
            value["scans"][0]["expected"]["r1"]["comparisons"] = [{}] * (
                MAX_EXPECTED_RECORDS_PER_SCAN + 1
            )
        elif kind == "utf8_response_bytes":
            value["scans"][0]["checks"][0]["input"] = {
                "utf8_text": "x" * (MAX_RESPONSE_BYTES + 1)
            }
        elif kind == "hex_response_bytes":
            value["scans"][0]["checks"][0]["input"] = {
                "raw_bytes_hex": "00" * (MAX_RESPONSE_BYTES + 1)
            }
        path = tmp_path / f"{kind}.json"
        path.write_text(json.dumps(value), encoding="utf-8")
    code, _stdout, stderr = _invalid_result(path)
    assert code == 2
    assert "INVALID_SCENARIO" in stderr


def test_canonical_scope_rules_and_duplicate_source_identity_reference(
    tmp_path: Path,
) -> None:
    value = read_scenario(scenario_paths()[0])
    value["sources"][0]["canonical_scope"] = ["b", "a"]
    path = tmp_path / "scope-order.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert _invalid_result(path)[0] == 2

    duplicate = read_scenario(
        ROOT / "scenarios/r2_5_r1_trusted_identity_incompatibility.json"
    )
    duplicate["scans"][1]["source_order"] = ["A1", "A2"]
    duplicate["scans"][1]["checks"] = [duplicate["scans"][1]["checks"][0]] * 2
    path = tmp_path / "duplicate-source-id.json"
    path.write_text(json.dumps(duplicate), encoding="utf-8")
    code, stdout, stderr = _invalid_result(path)
    assert code == 2 and stdout == "" and "code=reference_error" in stderr


def test_local_construction_error_marker_diagnostic_has_exact_path(
    tmp_path: Path,
) -> None:
    value = read_scenario(scenario_paths()[6])
    value["scans"][1]["checks"][0]["input"]["local_construction_error"] = "wrong"
    path = tmp_path / "bad-local-error.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    result = run_cli(path)
    assert result.returncode == 2
    assert result.stderr == (
        "INVALID_SCENARIO code=invalid_value "
        'path="/scans/1/checks/0/input/local_construction_error" '
        'message="scenario field has an invalid value"\n'
    )


def test_file_read_is_bounded_before_parsing() -> None:
    class BoundedReader:
        amount: int | None = None

        def __enter__(self) -> BoundedReader:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self, amount: int) -> bytes:
            self.amount = amount
            return b"x" * amount

    reader = BoundedReader()
    with (
        patch.object(Path, "open", return_value=reader),
        pytest.raises(ScenarioInvalid) as error,
    ):
        load_scenario(Path("synthetic-large-scenario.json"))
    assert reader.amount == MAX_SCENARIO_BYTES + 1
    assert error.value.code == "bounds_exceeded"
    assert error.value.path == "/"


def test_nfc_sorted_unique_reference_order_and_exact_integers(
    tmp_path: Path,
) -> None:
    value = read_scenario(scenario_paths()[0])
    value["subject_ref"] = "e\u0301"
    path = tmp_path / "nfc.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert "code=invalid_value" in _invalid_result(path)[2]

    for field in ("material_fields", "set_like_fields"):
        value = read_scenario(scenario_paths()[0])
        value["sources"][0][field] = ["labels", "labels"]
        path = tmp_path / f"duplicate-{field}.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        assert "code=invalid_value" in _invalid_result(path)[2]

    value = read_scenario(scenario_paths()[0])
    value["scans"][1]["checks"][0]["source_ref"] = "unknown"
    path = tmp_path / "check-order.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert "code=reference_error" in _invalid_result(path)[2]

    value = read_scenario(scenario_paths()[0])
    value["scans"][1]["scan_order"] = 3
    path = tmp_path / "non-contiguous.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert "code=invalid_value" in _invalid_result(path)[2]

    value = read_scenario(scenario_paths()[0])
    value["scans"][0]["scan_order"] = True
    path = tmp_path / "boolean-scan-order.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert "code=invalid_type" in _invalid_result(path)[2]


def test_fixture_identifiers_are_synthetic_and_not_email_like() -> None:
    email_pattern = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
    for path in scenario_paths():
        text = path.read_text(encoding="utf-8")
        assert "@" not in text
        assert email_pattern.search(text) is None
        value = read_scenario(path)
        assert value["scenario_id"].startswith("r25-")
        assert value["subject_ref"].startswith("subject-r25-")
        for source in value["sources"]:
            assert source["source_id"].startswith("synthetic-source-")
            assert source["adapter_id"].startswith("synthetic-")
            assert all(
                scope.startswith("synthetic-") for scope in source["canonical_scope"]
            )
        assert unicodedata.normalize("NFC", text) == text


def test_invalid_json_mode_has_exact_safe_shape(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{", encoding="utf-8")
    code, stdout, stderr = _invalid_result(path, json_mode=True)
    assert code == 2 and stderr == ""
    output = json.loads(stdout)
    assert set(output) == {
        "runner_version",
        "scenario_id",
        "result",
        "scans",
        "mismatches",
        "diagnostic",
    }
    assert output["result"] == "invalid_scenario"
    assert output["scenario_id"] is None
    assert set(output["diagnostic"]) == {"code", "path", "message"}


def test_main_returns_expectation_mismatch_without_exception_text(
    tmp_path: Path, capsys: Any
) -> None:
    value = read_scenario(scenario_paths()[0])
    value["scans"][1]["expected"]["r1"]["comparisons"][0] = {}
    path = tmp_path / "mismatch.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert main(["--json", str(path)]) == 2
    captured = capsys.readouterr()
    assert "Traceback" not in captured.out + captured.err
