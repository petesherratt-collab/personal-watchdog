"""Tests for R10 lifecycle refinements and the publication guard."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path
from types import ModuleType

import pytest

from personal_watchdog import cli, profiles

ROOT = Path(__file__).resolve().parents[1]


def _invoke(state_dir: Path, *arguments: str) -> int:
    return cli.main([*arguments, "--state-dir", str(state_dir)])


def _init(state_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _invoke(state_dir, "init") == 0
    capsys.readouterr()


def _add(state_dir: Path, value: str) -> str:
    result = profiles.add_profile(
        state_dir, kind="username", value=value, purpose="r10-test"
    )
    return str(result["subject_ref"])


def _fill_to_cap(state_dir: Path) -> list[str]:
    return [_add(state_dir, f"r10-user-{index:03d}") for index in range(8)]


def _profile_bytes(state_dir: Path) -> bytes:
    return (state_dir / profiles.PROFILE_FILE).read_bytes()


def _set_counter(state_dir: Path, value: int) -> None:
    path = state_dir / profiles.PROFILE_FILE
    stored = json.loads(path.read_text(encoding="utf-8"))
    stored["next_subject_number"] = value
    path.write_text(json.dumps(stored), encoding="utf-8")


def _scan(state_dir: Path, subject_ref: str | None = None) -> None:
    arguments = ["scan", "--adapter", "fixture", "--fixture", "baseline"]
    if subject_ref is not None:
        arguments += ["--subject-ref", subject_ref]
    assert _invoke(state_dir, *arguments) == 0


# A. Profile cap counts stored profiles, enabled and disabled alike.


def test_add_at_cap_is_refused_and_store_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _fill_to_cap(state_dir)
    before = _profile_bytes(state_dir)
    with pytest.raises(profiles.ProfileError, match="limit reached"):
        _add(state_dir, "r10-user-extra")
    assert _profile_bytes(state_dir) == before


def test_disabled_profile_still_counts_toward_cap(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    refs = _fill_to_cap(state_dir)
    profiles.disable_profile(state_dir, refs[0])
    before = _profile_bytes(state_dir)
    with pytest.raises(profiles.ProfileError, match="limit reached"):
        _add(state_dir, "r10-user-extra")
    assert _profile_bytes(state_dir) == before


def test_removal_at_cap_frees_slot_with_fresh_reference(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    refs = _fill_to_cap(state_dir)
    profiles.disable_profile(state_dir, refs[0])
    profiles.delete_profile(state_dir, refs[0])
    new_ref = _add(state_dir, "r10-user-extra")
    assert new_ref == "profile-009"
    assert new_ref not in refs
    stored = profiles.current_subject_refs(state_dir)
    assert refs[0] not in stored
    assert len(stored) == profiles.MAX_PROFILES


# B. Reference exhaustion is refused before writing.


def test_last_reference_is_issued_and_store_stays_loadable(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _set_counter(state_dir, 999)
    assert _add(state_dir, "r10-user-last") == "profile-999"
    loaded = profiles.load_profiles(state_dir)
    assert loaded["next_subject_number"] == profiles.EXHAUSTED_SUBJECT_NUMBER
    assert _invoke(state_dir, "profile", "list") == 0
    assert "PROFILES count=1" in capsys.readouterr().out


def test_exhausted_counter_refuses_add_before_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _set_counter(state_dir, 999)
    _add(state_dir, "r10-user-last")
    before = _profile_bytes(state_dir)

    with pytest.raises(profiles.ProfileError, match="references are exhausted"):
        _add(state_dir, "r10-user-after")

    assert _profile_bytes(state_dir) == before
    assert not (state_dir / ".profiles.json.tmp").exists()
    profiles.load_profiles(state_dir)
    assert _invoke(state_dir, "profile", "list", "--json") == 0
    listed = json.loads(capsys.readouterr().out)["profiles"]
    assert [item["subject_ref"] for item in listed] == ["profile-999"]


@pytest.mark.parametrize("value", [0, profiles.EXHAUSTED_SUBJECT_NUMBER + 1])
def test_counter_outside_bounds_still_fails_closed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], value: int
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _set_counter(state_dir, value)
    with pytest.raises(profiles.ProfileError, match="sequence is invalid"):
        profiles.load_profiles(state_dir)


# C. Re-enable requires the reference to be typed again.


@pytest.mark.parametrize(
    "confirmation",
    [(), ("--confirm-ref", "profile-002"), ("--confirm-ref", "profile-01")],
)
def test_enable_without_matching_confirmation_changes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], confirmation: tuple[str, ...]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add(state_dir, "r10-user-001")
    _add(state_dir, "r10-user-002")
    profiles.disable_profile(state_dir, "profile-001")
    before = _profile_bytes(state_dir)

    assert (
        _invoke(
            state_dir,
            "profile",
            "enable",
            "--subject-ref",
            "profile-001",
            *confirmation,
        )
        == 2
    )
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "requires --confirm-ref matching --subject-ref" in captured.err
    assert _profile_bytes(state_dir) == before


def test_bare_approve_flag_is_no_longer_accepted_for_enable(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add(state_dir, "r10-user-001")
    profiles.disable_profile(state_dir, "profile-001")
    before = _profile_bytes(state_dir)
    with pytest.raises(SystemExit):
        _invoke(
            state_dir,
            "profile",
            "enable",
            "--subject-ref",
            "profile-001",
            "--approve",
        )
    capsys.readouterr()
    assert _profile_bytes(state_dir) == before


# D. Removal wording is truthful about erasure.


def test_removal_output_states_no_secure_erasure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = "r10-user-001"
    _add(state_dir, value)
    profiles.disable_profile(state_dir, "profile-001")
    assert (
        _invoke(
            state_dir,
            "profile",
            "delete",
            "--subject-ref",
            "profile-001",
            "--confirm",
        )
        == 0
    )
    output = capsys.readouterr().out
    assert output == "PROFILE_REMOVED subject_ref=profile-001 (not securely erased)\n"
    assert value not in output


def test_documents_describe_removal_without_erasure_claim() -> None:
    readme = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
    privacy = " ".join((ROOT / "PRIVACY.md").read_text(encoding="utf-8").split())
    assert "--confirm-ref profile-001" in readme
    assert "does not securely erase" in readme
    assert "does not securely erase" in privacy


# E. Display-only history annotation.


def test_report_annotates_removed_profile_without_value_or_mutation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    value = "r10-user-001"
    _add(state_dir, value)
    _scan(state_dir, "profile-001")
    profiles.disable_profile(state_dir, "profile-001")
    profiles.delete_profile(state_dir, "profile-001")
    capsys.readouterr()
    history_before = (state_dir / "history.json").read_bytes()

    assert _invoke(state_dir, "report", "--latest") == 0
    output = capsys.readouterr().out
    assert "subject_ref=profile-001" in output
    assert output.endswith(
        "PROFILE_NOTE subject_ref=profile-001 profile since removed\n"
    )
    assert value not in output
    assert (state_dir / "history.json").read_bytes() == history_before

    assert _invoke(state_dir, "report", "--latest", "--json") == 0
    json_output = capsys.readouterr().out
    assert "PROFILE_NOTE" not in json_output
    assert "since removed" not in json_output
    stored = json.loads(history_before)["scans"][-1]
    assert json.loads(json_output) == stored


@pytest.mark.parametrize("disable", [False, True])
def test_report_for_current_profile_has_no_annotation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], disable: bool
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add(state_dir, "r10-user-001")
    _scan(state_dir, "profile-001")
    if disable:
        profiles.disable_profile(state_dir, "profile-001")
    capsys.readouterr()
    assert _invoke(state_dir, "report", "--latest") == 0
    assert "PROFILE_NOTE" not in capsys.readouterr().out


def test_report_for_default_subject_has_no_annotation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _scan(state_dir)
    capsys.readouterr()
    assert _invoke(state_dir, "report", "--latest") == 0
    output = capsys.readouterr().out
    assert "subject_ref=fixture-subject-01" in output
    assert "PROFILE_NOTE" not in output


def test_report_with_unreadable_profiles_does_not_claim_profile_is_live(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = tmp_path / "state"
    _init(state_dir, capsys)
    _add(state_dir, "r10-user-001")
    _scan(state_dir, "profile-001")
    (state_dir / profiles.PROFILE_FILE).write_text("{", encoding="utf-8")
    capsys.readouterr()
    assert _invoke(state_dir, "report", "--latest") == 0
    assert capsys.readouterr().out.endswith(
        "PROFILE_NOTE subject_ref=profile-001 profile status unavailable\n"
    )


# F. Publication guard.


def _guard() -> ModuleType:
    path = ROOT / "scripts" / "check_synthetic_identifiers.py"
    spec = importlib.util.spec_from_file_location("check_synthetic_identifiers", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Built at runtime so this file never contains a non-reserved address itself.
# ".zz" is an unassigned top-level domain.
_PROBE = "probe-user" + "@" + "watchdog-guard-probe.zz"


@pytest.mark.parametrize(
    "domain",
    [
        "example.invalid",
        "EXAMPLE.INVALID",
        "example.com",
        "example.org",
        "example.net",
        "mail.example.com",
        "fixture.test",
    ],
)
def test_guard_allows_reserved_domains(domain: str) -> None:
    assert _guard().scan_text(f"contact: someone@{domain}\n") == []


@pytest.mark.parametrize(
    "domain",
    ["watchdog-guard-probe.zz", "example.invalid.zz", "notexample.com", "test.zz"],
)
def test_guard_rejects_non_reserved_domains(domain: str) -> None:
    text = "first line\n" + "user" + "@" + domain + "\n"
    assert _guard().scan_text(text) == [2]


def _git_repo(path: Path, files: dict[str, str | bytes]) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    for name, content in files.items():
        target = path / name
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    return path


def test_guard_passes_repo_with_only_reserved_addresses(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _git_repo(tmp_path / "repo", {"a.md": "user@example.invalid\n"})
    assert _guard().main(["--root", str(repo)]) == 0
    assert capsys.readouterr().out == "PASSED files_scanned=1\n"


def test_guard_reports_location_only_and_ignores_untracked(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _git_repo(
        tmp_path / "repo",
        {
            "clean.md": "user@example.invalid\n",
            "leak.md": "line one\nline two\n" + _PROBE + "\n",
            "blob.bin": b"\x00" + _PROBE.encode("ascii"),
        },
    )
    (repo / "untracked.md").write_text(_PROBE + "\n", encoding="utf-8")

    assert _guard().main(["--root", str(repo)]) == 1
    captured = capsys.readouterr()
    assert captured.out == (
        "leak.md:3: non-synthetic email address\nFAILED lines=1 files_scanned=3\n"
    )
    assert _PROBE not in captured.out + captured.err
    assert "watchdog-guard-probe" not in captured.out + captured.err


def test_guard_fails_closed_outside_a_repository(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _guard().main(["--root", str(tmp_path / "missing")]) == 2
    assert "cannot list tracked files" in capsys.readouterr().err


def test_repository_tracked_files_contain_only_synthetic_addresses(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert _guard().main(["--root", str(ROOT)]) == 0
    assert capsys.readouterr().out.startswith("PASSED ")
