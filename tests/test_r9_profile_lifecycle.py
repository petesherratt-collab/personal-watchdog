"""Tests for the explicit R9 approved-profile lifecycle."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from personal_watchdog import cli, profiles


def _invoke(state_dir: Path, *arguments: str) -> int:
    return cli.main([*arguments, "--state-dir", str(state_dir)])


def _init(state_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _invoke(state_dir, "init") == 0
    capsys.readouterr()


def _add_profile(state_dir: Path, number: int = 1) -> str:
    value = f"r9-user-{number:03d}"
    result = profiles.add_profile(
        state_dir,
        kind="username",
        value=value,
        purpose="lifecycle-test",
    )
    assert result["subject_ref"] == f"r7-subject-{number:03d}"
    return value


def test_reenable_requires_fresh_approval_and_preserves_history(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = _add_profile(state_dir)

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
    scan_output = capsys.readouterr().out
    assert value not in scan_output
    history_before = (state_dir / "history.json").read_bytes()

    assert (
        _invoke(state_dir, "profile", "disable", "--subject-ref", "r7-subject-001") == 0
    )
    capsys.readouterr()
    assert (
        _invoke(state_dir, "profile", "enable", "--subject-ref", "r7-subject-001") == 2
    )
    assert "requires explicit --approve" in capsys.readouterr().err

    assert (
        _invoke(
            state_dir,
            "profile",
            "enable",
            "--subject-ref",
            "r7-subject-001",
            "--approve",
        )
        == 0
    )
    assert capsys.readouterr().out == "PROFILE_ENABLED subject_ref=r7-subject-001\n"
    assert (state_dir / "history.json").read_bytes() == history_before

    assert _invoke(state_dir, "profile", "list", "--json") == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed["profiles"][0]["enabled"] is True


def test_delete_requires_disabled_profile_and_confirmation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = _add_profile(state_dir)
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
    capsys.readouterr()
    history_before = (state_dir / "history.json").read_bytes()

    assert (
        _invoke(
            state_dir,
            "profile",
            "delete",
            "--subject-ref",
            "r7-subject-001",
            "--confirm",
        )
        == 2
    )
    assert "must be disabled before deletion" in capsys.readouterr().err

    assert (
        _invoke(state_dir, "profile", "disable", "--subject-ref", "r7-subject-001") == 0
    )
    capsys.readouterr()
    assert (
        _invoke(state_dir, "profile", "delete", "--subject-ref", "r7-subject-001") == 2
    )
    assert "requires explicit --confirm" in capsys.readouterr().err

    assert (
        _invoke(
            state_dir,
            "profile",
            "delete",
            "--subject-ref",
            "r7-subject-001",
            "--confirm",
        )
        == 0
    )
    assert capsys.readouterr().out == "PROFILE_DELETED subject_ref=r7-subject-001\n"
    assert (state_dir / "history.json").read_bytes() == history_before
    assert value not in (state_dir / profiles.PROFILE_FILE).read_text(encoding="utf-8")
    assert _invoke(state_dir, "profile", "list", "--json") == 0
    assert json.loads(capsys.readouterr().out) == {"profiles": []}


def test_deleted_subject_reference_is_never_reused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add_profile(state_dir, 1)
    profiles.disable_profile(state_dir, "r7-subject-001")
    profiles.delete_profile(state_dir, "r7-subject-001")
    result = profiles.add_profile(
        state_dir,
        kind="username",
        value="r9-user-002",
        purpose="lifecycle-test",
    )
    assert result["subject_ref"] == "r7-subject-002"
    assert _invoke(state_dir, "profile", "list", "--json") == 0
    assert json.loads(capsys.readouterr().out)["profiles"][0]["subject_ref"] == (
        "r7-subject-002"
    )


def test_interrupted_delete_keeps_previous_valid_profile_store(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add_profile(state_dir)
    profiles.disable_profile(state_dir, "r7-subject-001")
    profile_path = state_dir / profiles.PROFILE_FILE
    before = profile_path.read_bytes()
    original_replace = Path.replace

    def fail_temporary_replace(source: Path, target: Path) -> Path:
        if source.name == ".profiles.json.tmp":
            raise OSError("injected interruption")
        return original_replace(source, target)

    monkeypatch.setattr(Path, "replace", fail_temporary_replace)
    with pytest.raises(profiles.ProfileError, match="cannot write local profiles"):
        profiles.delete_profile(state_dir, "r7-subject-001")

    assert profile_path.read_bytes() == before
    assert not (state_dir / ".profiles.json.tmp").exists()
    stored = profiles.load_profiles(state_dir)["profiles"]
    assert len(stored) == 1
    assert stored[0]["enabled"] is False
