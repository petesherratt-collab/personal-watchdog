# Personal Watchdog

Personal Watchdog is a planned local-first diagnostic CLI for monitoring a
consenting user's explicitly approved email addresses and usernames. Version
0.1 will normalize known-breach observations and public username candidates,
retain a local baseline, and report changes between comparable scans.

This is not a comprehensive "dark web scanner." A lack of findings will mean
only that configured sources returned no findings during successful scans. It
must not be interpreted as proof that an identity is safe.

## Current status

The R6 offline workflow is implemented as a local module. It supports one
synthetic subject, one fixture source, bounded JSON state, deterministic R1
comparison, local reports, and local history. It does not perform live source
checks, store raw response payloads, schedule scans, or send notifications.

Run it from the repository with:

```text
python -m personal_watchdog.cli init
python -m personal_watchdog.cli scan --adapter fixture --fixture baseline
python -m personal_watchdog.cli scan --adapter fixture --fixture changed
python -m personal_watchdog.cli report --latest
python -m personal_watchdog.cli history
```

The default local state directory is `.watchdog/`; use `--state-dir PATH` to
choose another location. Available offline fixtures are `baseline`,
`unchanged`, `changed`, `disappeared`, `failed`, and `unverifiable`. The
planned installed `watchdog` executable, live adapters, scheduling, and
notifications remain deferred.

## Development

Python 3.12 or later is required. Create an isolated environment and install
the approved development dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pytest ruff mypy
```

Run all Milestone 0 checks:

```bash
.venv/bin/python -m pytest
.venv/bin/ruff format --check .
.venv/bin/ruff check .
.venv/bin/mypy .
git diff --check
```

The development dependencies are pytest (tests), Ruff (formatting/linting), and
mypy (type checking). All three are distributed under the MIT licence. There
are no runtime dependencies in Milestone 0.

See [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), and
[AGENTS.md](AGENTS.md) before contributing.
