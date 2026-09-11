"""Tests for the visible R3.5 synthetic XON scenario runner."""

# The golden outputs are required to remain literal byte-exact strings.
# ruff: noqa: E501

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import pytest

from personal_watchdog import offline_simulator as simulator
from personal_watchdog.r1 import SourceCheck
from personal_watchdog.r1 import compare_scans as r1_compare_scans
from personal_watchdog.r2_adapter import normalize_response as r2_normalize_response
from personal_watchdog.xposedornot_check_email_adapter import (
    TransportAttempt,
    TransportClassification,
    TransportDisposition,
)
from personal_watchdog.xposedornot_check_email_adapter import (
    classify_transport as xon_classify_transport,
)
from personal_watchdog.xposedornot_check_email_adapter import (
    normalize_check_email as xon_normalize_check_email,
)

from .fixtures_r3_5_xon_scenarios import (
    OVERLONG_INTEGER_BODY_SHA256,
    ROOT,
    SCENARIO_FILENAME_TO_ID,
    SCENARIO_IDS,
    SCENARIO_NAMES,
    SCENARIO_SHA256,
    read_scenario,
    run_cli,
    scenario_paths,
)

VALID_PATHS = scenario_paths()[:15] + scenario_paths()[16:]

SCENARIO_17_HUMAN_GOLDEN = """SCENARIO "r35-s17-xon-failure-mixed-source-change" result=PASS
SUBJECT "subject-r35-17"
SCAN order=1 total=2 scan_id="r35-s17-xon-failure-mixed-source-change:scan-001" outcome="completed" expectation=PASS
TRANSPORT source_ref="X1" source_id="xposedornot.free.check-email" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-001:check-X1" http_status=200 header_count=1 body_bytes=77 body_state="complete" transport_failure=null timed_out=FALSE failure_phase=null normalized_content_type="application/json" disposition="ready" reason="ready"
XON source_ref="X1" source_id="xposedornot.free.check-email" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-001:check-X1" classification="success_predicate_accepted"
SOURCE_CHECK source_ref="X1" source_id="xposedornot.free.check-email" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-001:check-X1" input_kind="transport_attempt" input_bytes=77 r2_invoked=TRUE r2_status="completed" r2_reason_codes=[] r2_finding_keys=["breach:Example Breach"] status="completed" reason_codes=[] finding_keys=["breach:Example Breach"]
TRANSPORT source_ref="B1" source_id="synthetic-source-b" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-001:check-B1" http_status=null header_count=0 body_bytes=271 body_state="not_applicable" transport_failure=null timed_out=FALSE failure_phase=null normalized_content_type=null disposition="not_applicable" reason="not_applicable"
XON source_ref="B1" source_id="synthetic-source-b" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-001:check-B1" classification="not_applicable"
SOURCE_CHECK source_ref="B1" source_id="synthetic-source-b" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-001:check-B1" input_kind="r2_bytes_hex" input_bytes=271 r2_invoked=TRUE r2_status="completed" r2_reason_codes=[] r2_finding_keys=["finding-b"] status="completed" reason_codes=[] finding_keys=["finding-b"]
BASELINE_CREATED source_id="synthetic-source-b"
BASELINE_CREATED source_id="xposedornot.free.check-email"
EXPOSURE_SILENCE actual=TRUE
SCAN order=2 total=2 scan_id="r35-s17-xon-failure-mixed-source-change:scan-002" outcome="incomplete" expectation=PASS
TRANSPORT source_ref="X1" source_id="xposedornot.free.check-email" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-002:check-X1" http_status=503 header_count=1 body_bytes=0 body_state="complete" transport_failure=null timed_out=FALSE failure_phase=null normalized_content_type=null disposition="failed" reason="http_failure"
XON source_ref="X1" source_id="xposedornot.free.check-email" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-002:check-X1" classification="not_entered"
SOURCE_CHECK source_ref="X1" source_id="xposedornot.free.check-email" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-002:check-X1" input_kind="transport_attempt" input_bytes=0 r2_invoked=TRUE r2_status="failed" r2_reason_codes=["response_failed"] r2_finding_keys=[] status="failed" reason_codes=["response_failed"] finding_keys=[]
TRANSPORT source_ref="B1" source_id="synthetic-source-b" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-002:check-B1" http_status=null header_count=0 body_bytes=272 body_state="not_applicable" transport_failure=null timed_out=FALSE failure_phase=null normalized_content_type=null disposition="not_applicable" reason="not_applicable"
XON source_ref="B1" source_id="synthetic-source-b" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-002:check-B1" classification="not_applicable"
SOURCE_CHECK source_ref="B1" source_id="synthetic-source-b" source_check_id="r35-s17-xon-failure-mixed-source-change:scan-002:check-B1" input_kind="r2_bytes_hex" input_bytes=272 r2_invoked=TRUE r2_status="completed" r2_reason_codes=[] r2_finding_keys=["finding-b"] status="completed" reason_codes=[] finding_keys=["finding-b"]
COMPARISON comparison_id="r35-s17-xon-failure-mixed-source-change:scan-002:synthetic-source-b:finding-b:changed" subject_ref="subject-r35-17" source_id="synthetic-source-b" baseline_scan_id="r35-s17-xon-failure-mixed-source-change:scan-001" current_scan_id="r35-s17-xon-failure-mixed-source-change:scan-002" finding_key="finding-b" kind="changed" changed_field_paths=["display_state"] reason_codes=[]
COMPARISON comparison_id="r35-s17-xon-failure-mixed-source-change:scan-002:xposedornot.free.check-email:source:not_comparable" subject_ref="subject-r35-17" source_id="xposedornot.free.check-email" baseline_scan_id="r35-s17-xon-failure-mixed-source-change:scan-001" current_scan_id="r35-s17-xon-failure-mixed-source-change:scan-002" finding_key=null kind="not_comparable" changed_field_paths=[] reason_codes=["response_failed"]
EXPOSURE_EVENT comparison_id="r35-s17-xon-failure-mixed-source-change:scan-002:synthetic-source-b:finding-b:changed" subject_ref="subject-r35-17" source_id="synthetic-source-b" finding_key="finding-b" kind="exposure-changed" changed_field_paths=["display_state"]
GUARDING_EVENT guard_id="r35-s17-xon-failure-mixed-source-change:scan-002:xposedornot.free.check-email:guarding_failed" subject_ref="subject-r35-17" source_id="xposedornot.free.check-email" baseline_scan_id="r35-s17-xon-failure-mixed-source-change:scan-001" current_scan_id="r35-s17-xon-failure-mixed-source-change:scan-002" guard_kind="guarding_failed" prior_status="completed" current_status="failed" reason_codes=["response_failed"]
EXPOSURE_SILENCE actual=FALSE
SUMMARY scans=2 source_checks=4 comparisons=2 exposure_events=1 guarding_events=1 mismatches=0
"""
SCENARIO_17_JSON_GOLDEN = '{"diagnostic":null,"mismatches":[],"result":"pass","runner_version":"r3.5-visible-xon-scenarios/1","scans":[{"exposure_silence":true,"outcome":"completed","r1":{"baseline_created_sources":["synthetic-source-b","xposedornot.free.check-email"],"comparisons":[],"exposure_events":[],"guarding_events":[]},"scan_id":"r35-s17-xon-failure-mixed-source-change:scan-001","scan_order":1,"source_checks":[{"adapter_id":"xposedornot-check-email","input_bytes":77,"input_kind":"transport_attempt","r1":{"finding_keys":["breach:Example Breach"],"reason_codes":[],"status":"completed"},"r2":{"finding_keys":["breach:Example Breach"],"reason_codes":[],"status":"completed"},"r2_invoked":true,"source_check_id":"r35-s17-xon-failure-mixed-source-change:scan-001:check-X1","source_id":"xposedornot.free.check-email","source_ref":"X1","transport":{"body_bytes":77,"body_state":"complete","disposition":"ready","failure_phase":null,"header_count":1,"http_status":200,"normalized_content_type":"application/json","reason":"ready","timed_out":false,"transport_failure":null},"xon":{"classification":"success_predicate_accepted"}},{"adapter_id":"synthetic-r2-adapter","input_bytes":271,"input_kind":"r2_bytes_hex","r1":{"finding_keys":["finding-b"],"reason_codes":[],"status":"completed"},"r2":{"finding_keys":["finding-b"],"reason_codes":[],"status":"completed"},"r2_invoked":true,"source_check_id":"r35-s17-xon-failure-mixed-source-change:scan-001:check-B1","source_id":"synthetic-source-b","source_ref":"B1","transport":null,"xon":null}],"source_order":["X1","B1"]},{"exposure_silence":false,"outcome":"incomplete","r1":{"baseline_created_sources":[],"comparisons":[{"baseline_scan_id":"r35-s17-xon-failure-mixed-source-change:scan-001","changed_field_paths":["display_state"],"comparison_id":"r35-s17-xon-failure-mixed-source-change:scan-002:synthetic-source-b:finding-b:changed","current_scan_id":"r35-s17-xon-failure-mixed-source-change:scan-002","finding_key":"finding-b","kind":"changed","reason_codes":[],"source_id":"synthetic-source-b","subject_ref":"subject-r35-17"},{"baseline_scan_id":"r35-s17-xon-failure-mixed-source-change:scan-001","changed_field_paths":[],"comparison_id":"r35-s17-xon-failure-mixed-source-change:scan-002:xposedornot.free.check-email:source:not_comparable","current_scan_id":"r35-s17-xon-failure-mixed-source-change:scan-002","finding_key":null,"kind":"not_comparable","reason_codes":["response_failed"],"source_id":"xposedornot.free.check-email","subject_ref":"subject-r35-17"}],"exposure_events":[{"changed_field_paths":["display_state"],"comparison_id":"r35-s17-xon-failure-mixed-source-change:scan-002:synthetic-source-b:finding-b:changed","finding_key":"finding-b","kind":"exposure-changed","source_id":"synthetic-source-b","subject_ref":"subject-r35-17"}],"guarding_events":[{"baseline_scan_id":"r35-s17-xon-failure-mixed-source-change:scan-001","current_scan_id":"r35-s17-xon-failure-mixed-source-change:scan-002","current_status":"failed","guard_id":"r35-s17-xon-failure-mixed-source-change:scan-002:xposedornot.free.check-email:guarding_failed","guard_kind":"guarding_failed","prior_status":"completed","reason_codes":["response_failed"],"source_id":"xposedornot.free.check-email","subject_ref":"subject-r35-17"}]},"scan_id":"r35-s17-xon-failure-mixed-source-change:scan-002","scan_order":2,"source_checks":[{"adapter_id":"xposedornot-check-email","input_bytes":0,"input_kind":"transport_attempt","r1":{"finding_keys":[],"reason_codes":["response_failed"],"status":"failed"},"r2":{"finding_keys":[],"reason_codes":["response_failed"],"status":"failed"},"r2_invoked":true,"source_check_id":"r35-s17-xon-failure-mixed-source-change:scan-002:check-X1","source_id":"xposedornot.free.check-email","source_ref":"X1","transport":{"body_bytes":0,"body_state":"complete","disposition":"failed","failure_phase":null,"header_count":1,"http_status":503,"normalized_content_type":null,"reason":"http_failure","timed_out":false,"transport_failure":null},"xon":{"classification":"not_entered"}},{"adapter_id":"synthetic-r2-adapter","input_bytes":272,"input_kind":"r2_bytes_hex","r1":{"finding_keys":["finding-b"],"reason_codes":[],"status":"completed"},"r2":{"finding_keys":["finding-b"],"reason_codes":[],"status":"completed"},"r2_invoked":true,"source_check_id":"r35-s17-xon-failure-mixed-source-change:scan-002:check-B1","source_id":"synthetic-source-b","source_ref":"B1","transport":null,"xon":null}],"source_order":["X1","B1"]}],"scenario_id":"r35-s17-xon-failure-mixed-source-change"}\n'


def _write_json(tmp_path: Path, value: object, name: str = "scenario.json") -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_exactly_seventeen_literal_scenarios_and_sixteen_valid() -> None:
    assert len(scenario_paths()) == 17
    assert all(path.is_file() for path in scenario_paths())
    assert len(VALID_PATHS) == 16
    assert [read_scenario(path)["scenario_id"] for path in scenario_paths()] == list(
        SCENARIO_IDS
    )


def test_scenario_files_have_frozen_raw_digests_and_literal_aliases() -> None:
    assert set(SCENARIO_SHA256) == set(SCENARIO_NAMES)
    assert set(SCENARIO_FILENAME_TO_ID) == set(SCENARIO_NAMES)
    for path in scenario_paths():
        assert (
            hashlib.sha256(path.read_bytes()).hexdigest() == SCENARIO_SHA256[path.name]
        )
        assert read_scenario(path)["scenario_id"] == SCENARIO_FILENAME_TO_ID[path.name]

    scenario_01 = read_scenario(scenario_paths()[0])
    body = bytes.fromhex(
        scenario_01["scans"][0]["checks"][0]["input"]["transport_attempt"][
            "body_bytes_hex"
        ]
    )
    assert body == (
        b'{"breaches":[["Example Breach"]],"email":"subject-r35-01","status":"success"}'
    )
    assert len(body) == 77
    assert scenario_01["scans"][0]["checks"][0]["input"]["transport_attempt"][
        "bounded_headers"
    ] == [
        {
            "name_bytes_hex": "436f6e74656e742d54797065",
            "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e",
        }
    ]

    scenario_03 = read_scenario(scenario_paths()[2])
    assert (
        bytes.fromhex(
            scenario_03["scans"][1]["checks"][0]["input"]["transport_attempt"][
                "body_bytes_hex"
            ]
        )
        == b'{"breaches":[["Example Breach","Another Breach"]],"email":"subject-r35-03","status":"success"}'
    )
    scenario_05 = read_scenario(scenario_paths()[4])
    assert (
        bytes.fromhex(
            scenario_05["scans"][1]["checks"][0]["input"]["transport_attempt"][
                "body_bytes_hex"
            ]
        )
        == b'{"breaches":[["Example Breach","Another Breach","Third Breach"]],"email":"subject-r35-05","status":"success"}'
    )
    scenario_06 = read_scenario(scenario_paths()[5])
    assert (
        bytes.fromhex(
            scenario_06["scans"][1]["checks"][0]["input"]["transport_attempt"][
                "body_bytes_hex"
            ]
        )
        == b'{"breaches":[],"email":"subject-r35-06","status":"success"}'
    )

    scenario_09 = read_scenario(scenario_paths()[8])
    scenario_09_bodies = [
        bytes.fromhex(check["input"]["transport_attempt"]["body_bytes_hex"])
        for scan in scenario_09["scans"]
        for check in scan["checks"]
    ]
    assert scenario_09_bodies[1] == b"\xff"
    assert scenario_09_bodies[2] == (
        b'{"breaches":[["Example Breach"]],"email":"subject-r35-09","status":"success"'
    )

    scenario_10 = read_scenario(scenario_paths()[9])
    header_rows = [
        scan["checks"][0]["input"]["transport_attempt"]["bounded_headers"]
        for scan in scenario_10["scans"][1:]
    ]
    assert header_rows == [
        [
            {
                "name_bytes_hex": "436f6e74656e742d54797065",
                "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e",
            }
        ],
        [
            {
                "name_bytes_hex": "436f6e74656e742d54797065",
                "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e3b20636861727365743d7574662d38",
            }
        ],
        [
            {
                "name_bytes_hex": "436f6e74656e742d54797065",
                "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e",
            },
            {
                "name_bytes_hex": "436f6e74656e742d54797065",
                "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e",
            },
        ],
        [
            {
                "name_bytes_hex": "436f6e74656e742d54797065",
                "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e80",
            }
        ],
        [
            {
                "name_bytes_hex": "436f6e74656e742d54797065",
                "value_bytes_hex": "746578742f706c61696e",
            }
        ],
        [{"name_bytes_hex": "780a", "value_bytes_hex": "79"}],
    ]

    scenario_12 = read_scenario(scenario_paths()[11])
    over_limit_body = bytes.fromhex(
        scenario_12["scans"][1]["checks"][0]["input"]["transport_attempt"][
            "body_bytes_hex"
        ]
    )
    assert over_limit_body == bytes.fromhex("7b" * 16_384)
    assert len(over_limit_body) == 16_384
    scenario_13 = read_scenario(scenario_paths()[12])
    assert (
        bytes.fromhex(
            scenario_13["scans"][1]["checks"][0]["input"]["transport_attempt"][
                "body_bytes_hex"
            ]
        )
        == b'{"breaches":[["Example Breach"]],"email":"other-subject","status":"success"}'
    )
    scenario_14 = read_scenario(scenario_paths()[13])
    assert (
        bytes.fromhex(
            scenario_14["scans"][1]["checks"][0]["input"]["transport_attempt"][
                "body_bytes_hex"
            ]
        )
        == b'{"breaches":[],"email":"subject-r35-14","status":"success","extra":"attacker-clean"}'
    )
    scenario_15 = read_scenario(scenario_paths()[14])
    hostile_body = bytes.fromhex(
        scenario_15["scans"][1]["checks"][0]["input"]["transport_attempt"][
            "body_bytes_hex"
        ]
    )
    assert len(hostile_body) == 5_088
    assert hashlib.sha256(hostile_body).hexdigest() == OVERLONG_INTEGER_BODY_SHA256


@pytest.mark.parametrize("path", VALID_PATHS, ids=lambda path: path.name)
def test_all_valid_curated_scenarios_pass_in_human_and_json_modes(path: Path) -> None:
    human = run_cli(path)
    machine = run_cli(path, json_mode=True)
    assert human.returncode == 0
    assert human.stderr == ""
    assert "PASS" in human.stdout
    assert machine.returncode == 0
    assert machine.stderr == ""
    output = json.loads(machine.stdout)
    assert output["result"] == "pass"
    assert output["runner_version"] == "r3.5-visible-xon-scenarios/1"


def test_scenario_17_human_golden_and_repeated_output_are_byte_identical() -> None:
    first = run_cli(scenario_paths()[16])
    second = run_cli(scenario_paths()[16])
    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    assert first.stdout == SCENARIO_17_HUMAN_GOLDEN
    assert second.stdout == first.stdout


def test_scenario_17_json_golden_is_byte_exact() -> None:
    result = run_cli(scenario_paths()[16], json_mode=True)
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == SCENARIO_17_JSON_GOLDEN


def test_scenario_17_machine_schema_is_complete_at_every_nested_projection() -> None:
    output = json.loads(run_cli(scenario_paths()[16], json_mode=True).stdout)
    assert set(output) == {
        "runner_version",
        "scenario_id",
        "result",
        "scans",
        "mismatches",
        "diagnostic",
    }
    scan_keys = {
        "exposure_silence",
        "outcome",
        "r1",
        "scan_id",
        "scan_order",
        "source_checks",
        "source_order",
    }
    source_check_keys = {
        "source_ref",
        "source_id",
        "adapter_id",
        "source_check_id",
        "input_kind",
        "input_bytes",
        "transport",
        "xon",
        "r2_invoked",
        "r2",
        "r1",
    }
    transport_keys = {
        "http_status",
        "header_count",
        "body_bytes",
        "body_state",
        "transport_failure",
        "timed_out",
        "failure_phase",
        "normalized_content_type",
        "disposition",
        "reason",
    }
    check_projection_keys = {"status", "reason_codes", "finding_keys"}
    comparison_keys = {
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
    exposure_keys = {
        "comparison_id",
        "subject_ref",
        "source_id",
        "finding_key",
        "kind",
        "changed_field_paths",
    }
    guarding_keys = {
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
    for scan in output["scans"]:
        assert set(scan) == scan_keys
        assert set(scan["r1"]) == {
            "baseline_created_sources",
            "comparisons",
            "exposure_events",
            "guarding_events",
        }
        for comparison in scan["r1"]["comparisons"]:
            assert set(comparison) == comparison_keys
        for exposure in scan["r1"]["exposure_events"]:
            assert set(exposure) == exposure_keys
        for guarding in scan["r1"]["guarding_events"]:
            assert set(guarding) == guarding_keys
        assert len(scan["source_checks"]) == 2
        for check in scan["source_checks"]:
            assert set(check) == source_check_keys
            assert set(check["r2"]) == check_projection_keys
            assert set(check["r1"]) == check_projection_keys
            if check["adapter_id"] == "xposedornot-check-email":
                assert set(check["transport"]) == transport_keys
                assert set(check["xon"]) == {"classification"}
                assert check["input_kind"] == "transport_attempt"
            else:
                assert check["adapter_id"] == "synthetic-r2-adapter"
                assert check["input_kind"] == "r2_bytes_hex"
                assert check["transport"] is None
                assert check["xon"] is None


def test_xon_oracles_are_strictly_present_and_synthetic_r2_oracles_are_null() -> None:
    for path in VALID_PATHS:
        scenario = read_scenario(path)
        for scan in scenario["scans"]:
            for check in scan["checks"]:
                expected = check["expected"]
                if "transport_attempt" in check["input"]:
                    assert expected["r3_transport"] is not None
                    assert expected["xon"] is not None
                    assert expected["r2"] is not None
                else:
                    assert check["input"].keys() == {"r2_bytes_hex"}
                    assert expected["r3_transport"] is None
                    assert expected["xon"] is None
                    assert expected["r2"] is not None
    invalid = read_scenario(scenario_paths()[15])
    expected = invalid["scans"][0]["checks"][0]["expected"]
    assert expected == {"r3_transport": None, "xon": None, "r2": None}


def test_invalid_transport_scenario_has_exact_human_contract() -> None:
    result = run_cli(scenario_paths()[15])
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == (
        "INVALID_SCENARIO code=construction_error "
        'path="/scans/0/checks/0/input/transport_attempt" '
        'message="scenario could not construct an R1 record"\n'
    )


def test_invalid_transport_scenario_has_exact_machine_contract() -> None:
    result = run_cli(scenario_paths()[15], json_mode=True)
    assert result.returncode == 2
    assert result.stderr == ""
    assert result.stdout == (
        '{"diagnostic":{"code":"construction_error",'
        '"message":"scenario could not construct an R1 record",'
        '"path":"/scans/0/checks/0/input/transport_attempt"},'
        '"mismatches":[],"result":"invalid_scenario",'
        '"runner_version":"r3.5-visible-xon-scenarios/1",'
        '"scans":[],"scenario_id":null}\n'
    )


def test_controlled_expectation_mismatch_is_exit_one(tmp_path: Path) -> None:
    value = read_scenario(scenario_paths()[2])
    value["scans"][1]["expected"]["r1"]["comparisons"][0]["kind"] = "unchanged"
    result = run_cli(_write_json(tmp_path, value), json_mode=True)
    assert result.returncode == 1
    assert result.stderr == ""
    output = json.loads(result.stdout)
    assert output["result"] == "expectation_mismatch"
    assert output["scans"][1]["r1"]["comparisons"][0]["kind"] == "new"
    assert output["mismatches"][0]["path"].endswith("/kind")


def test_xon_projection_invariant_has_exact_human_and_machine_contract(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    scenario = scenario_paths()[0]
    loaded = simulator.load_scenario(scenario)

    def failed_result(attempt: TransportAttempt) -> SourceCheck:
        context = attempt.trusted_context
        return SourceCheck.failed(
            source_check_id=context.source_check_id,
            scan_id=context.scan_id,
            subject_ref=context.subject_ref,
            source=context.source,
            reason_codes=("response_failed",),
        )

    monkeypatch.setattr(simulator, "normalize_check_email", failed_result)
    assert isinstance(loaded, simulator.R35ScenarioSpec)
    assert simulator.main([str(scenario)]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == (
        "INTERNAL_ERROR code=xon_projection_invariant "
        'path="/scans/0/checks/0" '
        'message="XON adapter result contradicts its READY transport projection"\n'
    )

    assert simulator.main(["--json", str(scenario)]) == 2
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == (
        '{"diagnostic":{"code":"xon_projection_invariant",'
        '"message":"XON adapter result contradicts its READY transport projection",'
        '"path":"/scans/0/checks/0"},"mismatches":[],'
        '"result":"internal_error",'
        '"runner_version":"r3.5-visible-xon-scenarios/1",'
        '"scans":[],"scenario_id":"r35-s01-first-finding-baseline"}\n'
    )


def test_runner_delegates_transport_xon_r2_and_r1(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scenario_path = scenario_paths()[16]
    with (
        patch.object(
            simulator, "classify_transport", wraps=xon_classify_transport
        ) as classify,
        patch.object(
            simulator,
            "normalize_check_email",
            wraps=xon_normalize_check_email,
        ) as xon,
        patch.object(
            simulator, "normalize_response", wraps=r2_normalize_response
        ) as r2,
        patch.object(simulator, "compare_scans", wraps=r1_compare_scans) as r1,
    ):
        loaded = simulator.load_scenario(scenario_path)
        assert isinstance(loaded, simulator.R35ScenarioSpec)
        result = simulator.run_r35_scenario(loaded)
    assert result.output["result"] == "pass"
    assert classify.call_count == 2
    assert xon.call_count == 2
    assert r2.call_count == 2
    assert r1.call_count == 2


def test_all_valid_xon_checks_delegate_once_and_synthetic_r2_stays_local(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_xon = 0
    expected_r2 = 0
    for path in VALID_PATHS:
        scenario = read_scenario(path)
        for scan in scenario["scans"]:
            for check in scan["checks"]:
                if "transport_attempt" in check["input"]:
                    expected_xon += 1
                else:
                    expected_r2 += 1
    with (
        patch.object(
            simulator, "classify_transport", wraps=xon_classify_transport
        ) as classify,
        patch.object(
            simulator,
            "normalize_check_email",
            wraps=xon_normalize_check_email,
        ) as xon,
        patch.object(
            simulator, "normalize_response", wraps=r2_normalize_response
        ) as r2,
    ):
        for path in VALID_PATHS:
            loaded = simulator.load_scenario(path)
            assert isinstance(loaded, simulator.R35ScenarioSpec)
            assert simulator.run_r35_scenario(loaded).output["result"] == "pass"
    assert classify.call_count == expected_xon
    assert xon.call_count == expected_xon
    assert r2.call_count == expected_r2


def test_invalid_construction_calls_no_xon_boundary() -> None:
    with (
        patch.object(simulator, "classify_transport", side_effect=AssertionError),
        patch.object(simulator, "normalize_check_email", side_effect=AssertionError),
    ):
        loaded = simulator.load_scenario(scenario_paths()[15])
        assert isinstance(loaded, simulator.R35ScenarioSpec)
        with pytest.raises(simulator.ScenarioInvalid):
            simulator.run_r35_scenario(loaded)


def test_compare_scans_receives_the_exact_immediate_prior_attempt_objects() -> None:
    loaded = simulator.load_scenario(scenario_paths()[16])
    assert isinstance(loaded, simulator.R35ScenarioSpec)
    with patch.object(simulator, "compare_scans", wraps=r1_compare_scans) as compare:
        assert simulator.run_r35_scenario(loaded).output["result"] == "pass"
    assert len(compare.call_args_list) == 2
    first_baseline, first_current = compare.call_args_list[0].args
    second_baseline, second_current = compare.call_args_list[1].args
    assert first_baseline is None
    assert second_baseline is first_current
    assert first_current is not second_current
    assert first_current.scan_id.endswith("scan-001")
    assert second_current.scan_id.endswith("scan-002")


def test_runner_contains_no_xon_body_or_r2_semantic_reimplementation() -> None:
    source = (ROOT / "personal_watchdog" / "offline_simulator.py").read_text(
        encoding="utf-8"
    )
    forbidden = (
        "_parse_xon_body",
        "_xon_text",
        '"breaches"',
        '"fixture-response/1"',
        '"breach:',
        "SourceCheck.completed",
    )
    for token in forbidden:
        assert token not in source


def test_transport_projection_uses_classification_return_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loaded = simulator.load_scenario(scenario_paths()[6])
    assert isinstance(loaded, simulator.R35ScenarioSpec)
    replacement = TransportClassification(
        TransportDisposition.UNVERIFIABLE, "spy_reason", "application/json"
    )
    monkeypatch.setattr(simulator, "classify_transport", lambda _attempt: replacement)
    result = simulator.run_r35_scenario(loaded)
    actual = result.output["scans"][1]["source_checks"][0]["transport"]
    assert actual["disposition"] == "unverifiable"
    assert actual["reason"] == "spy_reason"
    assert actual["normalized_content_type"] == "application/json"


def test_forged_adapter_result_does_not_get_replaced_by_expectations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loaded = simulator.load_scenario(scenario_paths()[0])
    assert isinstance(loaded, simulator.R35ScenarioSpec)

    def forged(attempt: TransportAttempt) -> SourceCheck:
        context = attempt.trusted_context
        return SourceCheck.completed(
            source_check_id=context.source_check_id,
            scan_id=context.scan_id,
            subject_ref=context.subject_ref,
            source=context.source,
        )

    monkeypatch.setattr(simulator, "normalize_check_email", forged)
    result = simulator.run_r35_scenario(loaded)
    source_check = result.output["scans"][0]["source_checks"][0]
    assert result.output["result"] == "expectation_mismatch"
    assert source_check["r2"]["status"] == "completed"
    assert source_check["r2"]["finding_keys"] == []
    assert result.output["scans"][0]["r1"]["baseline_created_sources"] == [
        "xposedornot.free.check-email"
    ]


def test_r2_5_scenarios_and_runner_output_remain_unchanged() -> None:
    old = ROOT / "scenarios" / "r2_5_mixed_source_failure_and_change.json"
    result = run_cli(old, json_mode=True)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["runner_version"] == "r2.5-visible-offline-simulator/1"
    assert output["scans"][1]["source_checks"][0]["input_kind"] == (
        "local_construction_error"
    )


def test_mixed_source_human_projection_is_complete() -> None:
    result = run_cli(scenario_paths()[16])
    assert result.returncode == 0
    b_line = next(
        line
        for line in result.stdout.splitlines()
        if line.startswith('TRANSPORT source_ref="B1"')
    )
    assert b_line == (
        'TRANSPORT source_ref="B1" source_id="synthetic-source-b" '
        'source_check_id="r35-s17-xon-failure-mixed-source-change:scan-001:check-B1" '
        "http_status=null header_count=0 body_bytes=271 "
        'body_state="not_applicable" transport_failure=null timed_out=FALSE '
        "failure_phase=null normalized_content_type=null "
        'disposition="not_applicable" reason="not_applicable"'
    )
    assert 'classification="not_applicable"' in result.stdout


def test_immediate_prior_failure_displaces_successful_baseline() -> None:
    output = json.loads(run_cli(scenario_paths()[7], json_mode=True).stdout)
    scan_three = output["scans"][2]["r1"]["guarding_events"][0]
    assert scan_three["baseline_scan_id"].endswith("scan-002")
    assert scan_three["prior_status"] == "failed"
    assert output["scans"][3]["r1"]["baseline_created_sources"] == [
        "xposedornot.free.check-email"
    ]


def test_disappearance_is_only_from_a_completed_nonempty_success() -> None:
    disappearance = json.loads(run_cli(scenario_paths()[3], json_mode=True).stdout)
    assert disappearance["scans"][1]["r1"]["comparisons"][1]["kind"] == "disappeared"
    for index in (5, 6, 8, 10, 11, 12, 13, 14):
        output = json.loads(run_cli(scenario_paths()[index], json_mode=True).stdout)
        assert all(
            comparison["kind"] != "disappeared"
            for scan in output["scans"]
            for comparison in scan["r1"]["comparisons"]
        )


def test_frozen_hostile_and_retained_body_byte_counts() -> None:
    hostile = read_scenario(scenario_paths()[14])
    hostile_hex = hostile["scans"][1]["checks"][0]["input"]["transport_attempt"][
        "body_bytes_hex"
    ]
    assert len(bytes.fromhex(hostile_hex)) == 5_088
    over_limit = read_scenario(scenario_paths()[11])
    prefix = over_limit["scans"][1]["checks"][0]["input"]["transport_attempt"][
        "body_bytes_hex"
    ]
    assert len(bytes.fromhex(prefix)) == 16_384


@pytest.mark.parametrize(
    ("field", "value"),
    [("adapter_version", 1), ("schema_version", "1")],
)
def test_trusted_identity_json_types_are_exact(
    tmp_path: Path, field: str, value: object
) -> None:
    scenario = read_scenario(scenario_paths()[16])
    scenario["sources"][0][field] = value
    result = run_cli(_write_json(tmp_path, scenario), json_mode=True)
    assert result.returncode == 2
    assert json.loads(result.stdout)["diagnostic"]["code"] == "invalid_type"


def test_machine_output_is_canonical_and_byte_identical() -> None:
    path = scenario_paths()[2]
    first = run_cli(path, json_mode=True)
    second = run_cli(path, json_mode=True)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert first.stdout.endswith("\n")
    output = json.loads(first.stdout)
    assert set(output) == {
        "runner_version",
        "scenario_id",
        "result",
        "scans",
        "mismatches",
        "diagnostic",
    }
    check = output["scans"][0]["source_checks"][0]
    assert set(check) == {
        "source_ref",
        "source_id",
        "adapter_id",
        "source_check_id",
        "input_kind",
        "input_bytes",
        "transport",
        "xon",
        "r2_invoked",
        "r2",
        "r1",
    }


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (
            lambda value: value["scans"][0]["checks"][0]["input"][
                "transport_attempt"
            ].update(body_bytes_hex="0g"),
            "invalid_value",
        ),
        (
            lambda value: value["scans"][0]["checks"][0]["input"]["transport_attempt"][
                "bounded_headers"
            ].extend(
                [
                    {
                        "name_bytes_hex": "436f6e74656e742d54797065",
                        "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e",
                    }
                ]
                * 16
            ),
            "bounds_exceeded",
        ),
        (
            lambda value: value["scans"][0]["source_order"].__setitem__(0, "missing"),
            "reference_error",
        ),
    ],
)
def test_invalid_scenario_diagnostics_are_visible(
    tmp_path: Path, mutation: Callable[[dict[str, object]], None], code: str
) -> None:
    value = read_scenario(scenario_paths()[0])
    mutation(value)
    result = run_cli(_write_json(tmp_path, value), json_mode=True)
    assert result.returncode == 2
    output = json.loads(result.stdout)
    assert output["runner_version"] == "r3.5-visible-xon-scenarios/1"
    diagnostic = output["diagnostic"]
    assert diagnostic["code"] == code


def test_duplicate_json_keys_are_rejected(tmp_path: Path) -> None:
    raw = scenario_paths()[0].read_text(encoding="utf-8")
    raw = raw.replace(
        '"scenario_version":"r3.5-visible-xon-scenarios/1",',
        '"scenario_version":"r3.5-visible-xon-scenarios/1","scenario_version":"r3.5-visible-xon-scenarios/1",',
        1,
    )
    path = tmp_path / "duplicate.json"
    path.write_text(raw, encoding="utf-8")
    result = run_cli(path, json_mode=True)
    assert result.returncode == 2
    assert json.loads(result.stdout)["diagnostic"]["code"] == "duplicate_json_key"
