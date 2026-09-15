"""Tests for the bounded offline R6 local workflow."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from personal_watchdog import cli


def _invoke(state_dir: Path, *arguments: str) -> int:
    return cli.main([*arguments, "--state-dir", str(state_dir)])


def _init(state_dir: Path) -> None:
    assert _invoke(state_dir, "init") == 0


def test_init_scan_report_and_history_round_trip(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _init(tmp_path / "state")
    capsys.readouterr()

    assert (
        _invoke(
            tmp_path / "state",
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            "baseline",
        )
        == 0
    )
    baseline_output = capsys.readouterr().out
    assert "BASELINE_CREATED source_id=fixture-source" in baseline_output

    assert (
        _invoke(
            tmp_path / "state",
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            "changed",
        )
        == 0
    )
    changed_output = capsys.readouterr().out
    assert "COMPARISON kind=changed" in changed_output
    assert "EXPOSURE_EVENT kind=exposure-changed" in changed_output

    assert _invoke(tmp_path / "state", "report", "--latest", "--json") == 0
    report = json.loads(capsys.readouterr().out)
    assert report["scan"]["scan_id"] == "r6-scan-002"
    assert report["comparison"]["exposure_events"][0]["kind"] == ("exposure-changed")

    assert _invoke(tmp_path / "state", "history", "--json") == 0
    history = json.loads(capsys.readouterr().out)
    assert [item["scan"]["scan_id"] for item in history["scans"]] == [
        "r6-scan-001",
        "r6-scan-002",
    ]

    state_text = (tmp_path / "state" / "history.json").read_text(encoding="utf-8")
    assert "contract_version" not in state_text
    assert "body_bytes" not in state_text
    assert "r4-probe-01@example.invalid" not in state_text


def test_completed_absence_after_completed_baseline_is_disappeared(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir)
    capsys.readouterr()
    _invoke(state_dir, "scan", "--adapter", "fixture", "--fixture", "baseline")
    capsys.readouterr()

    assert (
        _invoke(
            state_dir,
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            "disappeared",
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "COMPARISON kind=disappeared" in output
    assert "EXPOSURE_EVENT kind=exposure-disappeared" in output


@pytest.mark.parametrize(
    ("fixture", "guard_kind", "reason"),
    [
        ("failed", "guarding_failed", "response_failed"),
        ("unverifiable", "guarding_unverifiable", "response_unverifiable"),
    ],
)
def test_non_comparable_current_source_never_disappears(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    fixture: str,
    guard_kind: str,
    reason: str,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir)
    capsys.readouterr()
    _invoke(state_dir, "scan", "--adapter", "fixture", "--fixture", "baseline")
    capsys.readouterr()

    assert (
        _invoke(
            state_dir,
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            fixture,
        )
        == 0
    )
    output = capsys.readouterr().out
    assert f"GUARDING_EVENT kind={guard_kind}" in output
    assert f'"{reason}"' in output
    assert "COMPARISON kind=disappeared" not in output


def test_commands_require_initialized_state(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"

    assert (
        _invoke(
            state_dir,
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            "baseline",
        )
        == 2
    )
    assert "not initialized" in capsys.readouterr().err

    assert _invoke(state_dir, "report", "--latest") == 2
    assert "not initialized" in capsys.readouterr().err
