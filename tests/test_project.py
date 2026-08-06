"""Milestone 0 repository policy smoke tests."""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_requires_supported_python() -> None:
    """The project metadata must preserve the Python 3.12 minimum."""
    with (ROOT / "pyproject.toml").open("rb") as project_file:
        project = tomllib.load(project_file)

    assert project["project"]["requires-python"] == ">=3.12"
    assert project["project"]["dependencies"] == []


def test_required_policy_documents_exist() -> None:
    """Durable safety and privacy rules must be present from the first commit."""
    required = {"AGENTS.md", "README.md", "SECURITY.md", "PRIVACY.md"}

    assert required <= {path.name for path in ROOT.iterdir()}


def test_truthful_no_findings_language_is_documented() -> None:
    """Documentation must not imply that an empty result proves safety."""
    privacy = (ROOT / "PRIVACY.md").read_text(encoding="utf-8")

    assert "successful scans" in privacy
    normalized_privacy = " ".join(privacy.casefold().split())
    assert "does not establish that an identity is safe" in normalized_privacy
