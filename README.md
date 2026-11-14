# Personal Watchdog

Personal Watchdog is a planned local-first diagnostic CLI for monitoring a
consenting user's explicitly approved email addresses and usernames. Version
0.1 will normalize known-breach observations and public username candidates,
retain a local baseline, and report changes between comparable scans.

This is not a comprehensive "dark web scanner." A lack of findings will mean
only that configured sources returned no findings during successful scans. It
must not be interpreted as proof that an identity is safe.

## Current status

The tool runs a local workflow over bounded profiles of explicitly approved
identifiers, shown only as opaque references such as `profile-001`. It keeps
local history, compares each scan with the last completed scan of the same
profile and source, and reports new, changed, and disappeared findings. A
failed, blocked, or unverifiable check is recorded as such and is never
reported as clean. There is one offline fixture source and one live source
(XposedOrNot check-email). It does not schedule scans or send notifications.
See [ROADMAP.md](ROADMAP.md) for what is verified and what comes next.

### Offline fixture workflow

```text
python -m personal_watchdog.cli init
python -m personal_watchdog.cli scan --adapter fixture --fixture baseline
python -m personal_watchdog.cli scan --adapter fixture --fixture changed
python -m personal_watchdog.cli report --latest
python -m personal_watchdog.cli history
```

Available fixtures are `baseline`, `unchanged`, `changed`, `disappeared`,
`failed`, and `unverifiable`.

### Profiles

Run the add command and enter the value at the non-echo prompt. The value is
never placed on the command line:

```text
python -m personal_watchdog.cli profile add --kind email --purpose monitoring --approve --value-stdin
python -m personal_watchdog.cli profile list --json
python -m personal_watchdog.cli profile disable --subject-ref profile-001
python -m personal_watchdog.cli profile enable --subject-ref profile-001 --confirm-ref profile-001
python -m personal_watchdog.cli profile delete --subject-ref profile-001 --confirm
```

Re-enabling requires typing the reference again with `--confirm-ref`; this is
an intent signal, not proof of consent or ownership. Deletion requires prior
disablement and explicit confirmation. It removes the record from the local
profile store and prints `PROFILE_REMOVED ... (not securely erased)`: it does
not securely erase data from disk, journals, or backups, and it does not
rewrite historical scan records. A human-readable report of a scan whose
profile has since been removed adds a display-only
`PROFILE_NOTE ... profile since removed` line. References run from
`profile-001` to `profile-999` and are never reused.

### Live check (XposedOrNot)

Only add an address you own. A live check sends that one email address, in a
single HTTPS request, to `api.xposedornot.com`; see [PRIVACY.md](PRIVACY.md)
for exactly what leaves the machine. Each check needs the reference typed
again:

```text
python -m personal_watchdog.cli scan --adapter xposedornot --subject-ref profile-001 --confirm-live profile-001
```

The output never contains the address. A `TRANSPORT` line gives the HTTP
status and classification so a failure can be understood. Known limits:

- The service's "no breach found" response is not yet accepted as a completed
  result, so an address with no known breaches currently reports
  `unverifiable`, not clean. This is deliberate until that response is
  understood well enough to rule out a false clean.
- Enter the address exactly as the service returns it (normally lower case);
  a response for a differently spelled address is rejected as unverifiable.
- One request per run, with no retry. Wait before repeating a failed check.

### Local state

The default state directory is `.watchdog/`; use `--state-dir PATH` to choose
another. It is ignored by Git. State written before 14 Nov 2026 uses older
reference names and is rejected as an unsupported version; delete that
directory and run `init` again.

Before committing, check that tracked files contain only synthetic email
addresses (reserved domains such as `example.invalid`). The check reports file
and line only, never the address, and also runs in the test suite and in CI:

```text
python scripts/check_synthetic_identifiers.py
```

## Development

Python 3.12 or later is required. Create an isolated environment and install
the approved development dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pytest ruff mypy
```

Run all checks (the same ones CI runs):

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
