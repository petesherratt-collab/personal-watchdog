"""Tests for the bounded local R7 approved-profile workflow."""

from __future__ import annotations

import io
import json
import stat
import sys
from pathlib import Path

import pytest

from personal_watchdog import cli


def _invoke(state_dir: Path, *arguments: str) -> int:
    return cli.main([*arguments, "--state-dir", str(state_dir)])


def _init(state_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _invoke(state_dir, "init") == 0
    capsys.readouterr()


def _add_email(
    state_dir: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> str:
    value = "r7-synthetic-user" + "@example.invalid"
    monkeypatch.setattr(sys, "stdin", io.StringIO(value + "\n"))
    assert (
        _invoke(
            state_dir,
            "profile",
            "add",
            "--kind",
            "email",
            "--purpose",
            "offline-test",
            "--approve",
            "--value-stdin",
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "PROFILE_ADDED subject_ref=r7-subject-001" in output
    assert value not in output
    return value


def test_profile_add_list_and_reload_are_redacted_and_private(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = _add_email(state_dir, capsys, monkeypatch)

    profile_path = state_dir / "profiles.json"
    assert stat.S_IMODE(profile_path.stat().st_mode) == 0o600
    stored = json.loads(profile_path.read_text(encoding="utf-8"))
    assert stored["profiles"][0]["value"] == value

    assert _invoke(state_dir, "profile", "list", "--json") == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed == {
        "profiles": [
            {
                "approved": True,
                "created_at": stored["profiles"][0]["created_at"],
                "enabled": True,
                "kind": "email",
                "purpose": "offline-test",
                "subject_ref": "r7-subject-001",
            }
        ]
    }
    assert value not in json.dumps(listed)


def test_synthetic_username_profile_can_be_added(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = "r7-synthetic-name"
    monkeypatch.setattr(sys, "stdin", io.StringIO(value + "\n"))

    assert (
        _invoke(
            state_dir,
            "profile",
            "add",
            "--kind",
            "username",
            "--approve",
            "--value-stdin",
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "PROFILE_ADDED subject_ref=r7-subject-001 kind=username" in output
    assert value not in output


def test_profile_scan_uses_opaque_subject_ref_and_preserves_r6_state_shape(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = _add_email(state_dir, capsys, monkeypatch)

    assert (
        _invoke(
            state_dir,
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            "baseline",
            "--subject-ref",
            "r7-subject-001",
        )
        == 0
    )
    baseline_output = capsys.readouterr().out
    assert "subject_ref=r7-subject-001" in baseline_output
    assert value not in baseline_output

    assert (
        _invoke(
            state_dir,
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            "changed",
            "--subject-ref",
            "r7-subject-001",
        )
        == 0
    )
    changed_output = capsys.readouterr().out
    assert "COMPARISON kind=changed" in changed_output
    assert value not in changed_output

    config = json.loads((state_dir / "config.json").read_text(encoding="utf-8"))
    assert config["subject_ref"] == "r6-subject-01"
    history_text = (state_dir / "history.json").read_text(encoding="utf-8")
    assert value not in history_text
    assert "contract_version" not in history_text


def test_duplicate_profile_value_is_rejected(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = _add_email(state_dir, capsys, monkeypatch)
    monkeypatch.setattr(sys, "stdin", io.StringIO(value + "\n"))

    assert (
        _invoke(
            state_dir,
            "profile",
            "add",
            "--kind",
            "email",
            "--approve",
            "--value-stdin",
        )
        == 2
    )
    assert "profile already exists" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("extra_arguments", "input_value", "message"),
    [
        (("--value-stdin",), "r7-user-01", "requires explicit --approve"),
        (("--approve",), "r7-user-01", "requires --value-stdin"),
        (("--approve", "--value-stdin"), "bad username!", "username value is invalid"),
    ],
)
def test_profile_add_requires_explicit_approval_and_valid_input(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    extra_arguments: tuple[str, ...],
    input_value: str,
    message: str,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    monkeypatch.setattr(sys, "stdin", io.StringIO(input_value + "\n"))

    assert (
        _invoke(
            state_dir,
            "profile",
            "add",
            "--kind",
            "username",
            *extra_arguments,
        )
        == 2
    )
    assert message in capsys.readouterr().err
    profile_path = state_dir / "profiles.json"
    stored = json.loads(profile_path.read_text(encoding="utf-8"))
    assert stored["profiles"] == []


def test_disabled_profile_cannot_scan_and_does_not_rewrite_history(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add_email(state_dir, capsys, monkeypatch)
    assert (
        _invoke(state_dir, "profile", "disable", "--subject-ref", "r7-subject-001") == 0
    )
    assert capsys.readouterr().out == "PROFILE_DISABLED subject_ref=r7-subject-001\n"

    before = (state_dir / "history.json").read_bytes()
    assert (
        _invoke(
            state_dir,
            "scan",
            "--adapter",
            "fixture",
            "--fixture",
            "baseline",
            "--subject-ref",
            "r7-subject-001",
        )
        == 2
    )
    assert "profile is disabled" in capsys.readouterr().err
    assert (state_dir / "history.json").read_bytes() == before
