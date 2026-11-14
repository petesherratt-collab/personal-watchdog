"""Fail when a tracked text file contains a non-synthetic email address.

R10 publication guard. It scans the files git tracks and reports the file and
line of each email address whose domain is not an allow-listed reserved
domain. It never prints the matched address. It detects email addresses only:
usernames, phone numbers, and free-text names are out of scope, and a passing
check does not make the repository safe for real data.

Usage: python scripts/check_synthetic_identifiers.py [--root PATH]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

# Reserved by RFC 2606 / RFC 6761 for documentation and testing.
ALLOWED_DOMAINS = frozenset(
    {"example.invalid", "example.com", "example.org", "example.net"}
)
ALLOWED_TOP_LEVEL_DOMAINS = frozenset({"test"})

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})(?![A-Za-z0-9-])",
    re.ASCII,
)


def is_allowed_domain(domain: str) -> bool:
    folded = domain.lower().rstrip(".")
    if folded.rsplit(".", 1)[-1] in ALLOWED_TOP_LEVEL_DOMAINS:
        return True
    return any(
        folded == allowed or folded.endswith(f".{allowed}")
        for allowed in ALLOWED_DOMAINS
    )


def scan_text(text: str) -> list[int]:
    """Return 1-based line numbers holding a non-synthetic email address."""

    lines: list[int] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if any(
            not is_allowed_domain(match.group(1))
            for match in EMAIL_PATTERN.finditer(line)
        ):
            lines.append(number)
    return lines


def _read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan_paths(root: Path, relative_paths: Iterable[str]) -> list[tuple[str, int]]:
    """Return (path, line) locations; binary and unreadable files are skipped."""

    findings: list[tuple[str, int]] = []
    for relative in relative_paths:
        text = _read_text(root / relative)
        if text is None:
            continue
        findings.extend((relative, line) for line in scan_text(text))
    return findings


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [item for item in result.stdout.decode("utf-8").split("\0") if item]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail on non-synthetic email addresses in tracked files."
    )
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    root: Path = args.root
    try:
        paths = tracked_files(root)
    except (OSError, subprocess.CalledProcessError):
        print("ERROR cannot list tracked files", file=sys.stderr)
        return 2
    findings = scan_paths(root, paths)
    for path, line in findings:
        print(f"{path}:{line}: non-synthetic email address")
    if findings:
        print(f"FAILED lines={len(findings)} files_scanned={len(paths)}")
        return 1
    print(f"PASSED files_scanned={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
