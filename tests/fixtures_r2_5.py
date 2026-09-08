"""Shared paths and helpers for the R2.5 offline simulator tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "scenarios"
SCENARIO_NAMES = (
    "r2_5_baseline_silence.json",
    "r2_5_new_exposure.json",
    "r2_5_material_change.json",
    "r2_5_genuine_disappearance.json",
    "r2_5_source_failure.json",
    "r2_5_unverifiable_source.json",
    "r2_5_mixed_source_failure_and_change.json",
    "r2_5_r1_trusted_identity_incompatibility.json",
    "r2_5_hostile_false_clean.json",
    "r2_5_simultaneous_findings.json",
)


def scenario_paths() -> tuple[Path, ...]:
    return tuple(SCENARIO_DIR / name for name in SCENARIO_NAMES)


def read_scenario(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def run_cli(path: Path, *, json_mode: bool = False) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, "-m", "personal_watchdog.offline_simulator"]
    if json_mode:
        args.append("--json")
    args.append(str(path))
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
