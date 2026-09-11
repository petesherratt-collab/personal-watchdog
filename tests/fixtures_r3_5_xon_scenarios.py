"""Paths and subprocess helpers for the frozen R3.5 scenario family."""

# Literal digests and raw-byte aliases intentionally exceed the project line limit.
# ruff: noqa: E501

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "scenarios" / "r3_5_xon"
SCENARIO_NAMES = tuple(
    f"{number:02d}_{name}.json"
    for number, name in (
        (1, "first_finding_baseline"),
        (2, "identical_finding"),
        (3, "additional_breach"),
        (4, "one_disappears_one_remains"),
        (5, "multiple_simultaneous_findings"),
        (6, "zero_finding_unverifiable"),
        (7, "http_404_failed"),
        (8, "http_429_503_failed"),
        (9, "invalid_utf8_malformed_json"),
        (10, "content_type_metadata"),
        (11, "incomplete_body"),
        (12, "over_limit_body"),
        (13, "echo_mismatch"),
        (14, "hostile_unknown_field"),
        (15, "overlong_json_integer"),
        (16, "contradictory_transport_invalid"),
        (17, "xon_failure_mixed_source_change"),
    )
)
SCENARIO_IDS = (
    "r35-s01-first-finding-baseline",
    "r35-s02-identical-finding",
    "r35-s03-additional-breach",
    "r35-s04-one-disappears-one-remains",
    "r35-s05-multiple-simultaneous-findings",
    "r35-s06-zero-finding-unverifiable",
    "r35-s07-http-404-failed",
    "r35-s08-http-429-503-failed",
    "r35-s09-invalid-utf8-malformed-json",
    "r35-s10-content-type-metadata",
    "r35-s11-incomplete-body",
    "r35-s12-over-limit-body",
    "r35-s13-echo-mismatch",
    "r35-s14-hostile-unknown-field",
    "r35-s15-overlong-json-integer",
    "r35-s16-contradictory-transport-invalid",
    "r35-s17-xon-failure-mixed-source-change",
)
SCENARIO_FILENAME_TO_ID = {
    "01_first_finding_baseline.json": "r35-s01-first-finding-baseline",
    "02_identical_finding.json": "r35-s02-identical-finding",
    "03_additional_breach.json": "r35-s03-additional-breach",
    "04_one_disappears_one_remains.json": "r35-s04-one-disappears-one-remains",
    "05_multiple_simultaneous_findings.json": "r35-s05-multiple-simultaneous-findings",
    "06_zero_finding_unverifiable.json": "r35-s06-zero-finding-unverifiable",
    "07_http_404_failed.json": "r35-s07-http-404-failed",
    "08_http_429_503_failed.json": "r35-s08-http-429-503-failed",
    "09_invalid_utf8_malformed_json.json": "r35-s09-invalid-utf8-malformed-json",
    "10_content_type_metadata.json": "r35-s10-content-type-metadata",
    "11_incomplete_body.json": "r35-s11-incomplete-body",
    "12_over_limit_body.json": "r35-s12-over-limit-body",
    "13_echo_mismatch.json": "r35-s13-echo-mismatch",
    "14_hostile_unknown_field.json": "r35-s14-hostile-unknown-field",
    "15_overlong_json_integer.json": "r35-s15-overlong-json-integer",
    "16_contradictory_transport_invalid.json": "r35-s16-contradictory-transport-invalid",
    "17_xon_failure_mixed_source_change.json": "r35-s17-xon-failure-mixed-source-change",
}
SCENARIO_SHA256 = {
    "01_first_finding_baseline.json": "9630415e0819512104a18c03f63f38ec9048f9366fb6564948138b4de95648b6",
    "02_identical_finding.json": "14108a6633f1c52edc2263a0a4b0b61e11735044288fb80259f9fe180bd09431",
    "03_additional_breach.json": "f23152beb17d50709fe8537ec1e70998608ef4e616714234871146bec379e806",
    "04_one_disappears_one_remains.json": "2c45ba4792b58ca7c308c21b51ce302e7afb1539880b728553cf71b690dbb3a6",
    "05_multiple_simultaneous_findings.json": "5bc3476eabb2d64308ab61d1a45a28ff10d87b33ddb5984bef91cefd47a25a0a",
    "06_zero_finding_unverifiable.json": "09a4828df800056d0541f60983a26c9a00b335e2e6735247d459094678893a2c",
    "07_http_404_failed.json": "505ccdd1f17d83edc3047fe3fec9f80fac8f3b3e899e13aecff01ac46353ee4f",
    "08_http_429_503_failed.json": "33b207371dcb0006b4a8233227140fd061a5917f64c164594fc14c6e73fe846f",
    "09_invalid_utf8_malformed_json.json": "3730ff8bcdf26e84b3a9e29efad2bf347d4b1d6295ca4c595a8f8d74123053a2",
    "10_content_type_metadata.json": "fd6fa9de778777183444bb3969f74cce4cde319a76b247aece1020d84f1adc25",
    "11_incomplete_body.json": "5f327bed9d51903b1c7f3831711535ed6039fff73d1a1b9898a5a4ebe0e1dbe1",
    "12_over_limit_body.json": "9a1f9b8f6456bb675d78767acd195370a77097de13f5a169dd4370a1f631ac7e",
    "13_echo_mismatch.json": "7c8bfb9ae566c8fc5a8088cdb75418413bb3fea8df2a8e5adf828f39a946e7fa",
    "14_hostile_unknown_field.json": "744a89c679a1a34bbc1d2aec0d137ef13d4c55d8a0f30dcbe40804353ae082dc",
    "15_overlong_json_integer.json": "4ac932b4298005c14ce567016eafebb4ce2d13a25696db71f233f9130de565d5",
    "16_contradictory_transport_invalid.json": "aec3405e73b787c51ac064be84987c1818f5d8f2125326aa697bf78c79b3abdc",
    "17_xon_failure_mixed_source_change.json": "c6b26e683f8cb399168c78d601d61ae71e89d4474d67baa28358e82bd9d7f305",
}

OVERLONG_INTEGER_BODY_SHA256 = (
    "b3a38dae68c7ac2295a774ec4d07c3e55bb0bc0ca182abb783e8afbe1a358e5b"
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
