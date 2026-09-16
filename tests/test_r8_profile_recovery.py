"""Tests for the conservative R8 profile retention and recovery boundary."""

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


def _add_username(state_dir: Path, number: int) -> None:
    profiles.add_profile(
        state_dir,
        kind="username",
        value=f"r8-user-{number:03d}",
        purpose="retention-test",
    )


def test_missing_profile_store_fails_closed_without_history_rewrite(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    profile_path = state_dir / profiles.PROFILE_FILE
    profile_path.unlink()
    before = (state_dir / "history.json").read_bytes()

    assert _invoke(state_dir, "profile", "list", "--json") == 2
    assert "local profiles are missing" in capsys.readouterr().err
    assert not profile_path.exists()
    assert (state_dir / "history.json").read_bytes() == before


def _malformed_payloads() -> list[tuple[str, str]]:
    valid_profile = {
        "subject_ref": "r7-subject-001",
        "kind": "username",
        "value": "r8-user-001",
        "approved": True,
        "enabled": True,
        "purpose": "retention-test",
        "created_at": "2026-09-16T00:00:00+00:00",
    }
    unsupported_fields = dict(valid_profile)
    unsupported_fields["unexpected"] = "value"
    return [
        ("{", "cannot read local profiles"),
        ("[]", "local profiles are malformed"),
        (
            json.dumps(
                {
                    "profiles_version": "unknown",
                    "next_subject_number": 1,
                    "profiles": [],
                }
            ),
            "unsupported local profiles version",
        ),
        (
            json.dumps(
                {
                    "profiles_version": profiles.PROFILE_VERSION,
                    "next_subject_number": 2,
                    "profiles": [unsupported_fields],
                }
            ),
            "local profile has unsupported fields",
        ),
    ]


@pytest.mark.parametrize(("payload", "message"), _malformed_payloads())
def test_malformed_profile_store_fails_closed_without_becoming_empty(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    payload: str,
    message: str,
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    profile_path = state_dir / profiles.PROFILE_FILE
    profile_path.write_text(payload, encoding="utf-8")
    before = profile_path.read_bytes()
    history_before = (state_dir / "history.json").read_bytes()

    assert _invoke(state_dir, "profile", "list", "--json") == 2
    assert message in capsys.readouterr().err
    assert profile_path.read_bytes() == before
    assert (state_dir / "history.json").read_bytes() == history_before


def test_interrupted_profile_write_keeps_previous_valid_target(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add_username(state_dir, 1)
    profile_path = state_dir / profiles.PROFILE_FILE
    before = profile_path.read_bytes()
    original_replace = Path.replace

    def fail_temporary_replace(source: Path, target: Path) -> Path:
        if source.name == ".profiles.json.tmp":
            raise OSError("injected interruption")
        return original_replace(source, target)

    monkeypatch.setattr(Path, "replace", fail_temporary_replace)
    with pytest.raises(profiles.ProfileError, match="cannot write local profiles"):
        _add_username(state_dir, 2)

    assert profile_path.read_bytes() == before
    assert not (state_dir / ".profiles.json.tmp").exists()
    assert len(profiles.load_profiles(state_dir)["profiles"]) == 1


def test_stale_temporary_file_does_not_override_valid_profile_store(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add_username(state_dir, 1)
    temporary = state_dir / ".profiles.json.tmp"
    temporary.write_text("{", encoding="utf-8")
    profile_path = state_dir / profiles.PROFILE_FILE
    before = profile_path.read_bytes()

    assert _invoke(state_dir, "profile", "list", "--json") == 0
    listed = capsys.readouterr().out
    assert "r7-subject-001" in listed
    assert profile_path.read_bytes() == before
    assert temporary.exists()


def test_profile_and_history_bounds_remain_independent(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    for number in range(1, profiles.MAX_PROFILES + 1):
        _add_username(state_dir, number)
    with pytest.raises(profiles.ProfileError, match="profile limit reached"):
        _add_username(state_dir, profiles.MAX_PROFILES + 1)

    for _ in range(cli.MAX_RETAINED_SCANS + 1):
        assert (
            _invoke(
                state_dir,
                "scan",
                "--adapter",
                "fixture",
                "--fixture",
                "unchanged",
            )
            == 0
        )
    capsys.readouterr()
    history = json.loads((state_dir / "history.json").read_text(encoding="utf-8"))
    assert len(history["scans"]) == cli.MAX_RETAINED_SCANS
    assert len(profiles.load_profiles(state_dir)["profiles"]) == profiles.MAX_PROFILES
