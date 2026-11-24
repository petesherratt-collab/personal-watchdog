# Personal Watchdog roadmap

Last updated: 14 Nov 2026. This replaces
`PERSONAL_WATCHDOG_CODEX_ITINERARY.md` as the plan. Update it only when the
plan changes; per-step history is in `BUILD_HISTORY.md`.

## Where the project stands

**Goal:** a local tool that tells one consenting person when the known
exposure of their own identifiers changes, and never reports a failed check as
a clean one.

**Working and tested offline**

- Comparison model: new, changed, and disappeared findings; failed and
  unverifiable checks produce guarding events, never exposure events.
- Strict response normalization with bounded input.
- Local profile store: opaque references, approval, disable, re-enable with
  typed confirmation, removal, bounded and fail-closed.
- Local history (32 scans), reports, per-profile and per-source baselines.
- XposedOrNot check-email adapter and a bounded single-request transport.
- Live scan command with typed confirmation on every run.
- Guard against non-synthetic email addresses in tracked files; CI workflow.

**Not yet verified**

- The live path has never returned a completed result from the real service.
  Its only real observation is the September probe of a synthetic address,
  which returned HTTP 200 with `{"Error":"Not found","email":null}`. Whether a
  real breached address returns the exact success shape the adapter expects is
  unknown.
- The CI workflow has not run yet.

**Known weaknesses**

- An address with no known breaches cannot produce a completed result, so for
  such an address the tool can only ever say `unverifiable`.
- Profile values are stored in plain text (owner-only file permissions).
- History is capped at 32 scans across all profiles, so heavy use of one
  profile can evict another profile's baseline.
- No rate-limit handling beyond "one request, no retry".
- Username profiles can be stored but no source checks them.
- No installed command; it runs as `python -m personal_watchdog.cli`.
- `cli.py` holds state, serialization, and commands in one 900-line file.

## Now — first real result

1. **Run the live check on your own machine against your own address.**
   Nobody else can do this step: it needs your address and network.

   ```bash
   cd /home/peters/personal-watchdog
   git fetch && git switch ccr-058bcad3-37cjg1 && .venv/bin/python -m pytest
   rm -rf .watchdog && .venv/bin/python -m personal_watchdog.cli init
   .venv/bin/python -m personal_watchdog.cli profile add --kind email --purpose monitoring --approve --value-stdin
   .venv/bin/python -m personal_watchdog.cli scan --adapter xposedornot --subject-ref profile-001 --confirm-live profile-001
   ```

   Record only the `TRANSPORT`, `SCAN`, and `SOURCE` lines. They contain no
   address. Do not paste the address or `profiles.json` anywhere.
2. **Act on what it shows.**
   - `status=completed`: the success contract holds. Run it again a day later
     and confirm `unchanged`.
   - `http_status=200 … status=unverifiable`: the response shape differs from
     the frozen contract (for example, address casing, extra fields, or the
     not-found body). Capture the shape with the address redacted and adjust
     the adapter in a reviewed change.
   - `http_status=404` or `429`: see items 3 and 6.
3. **Decide the no-match contract.** Options: (a) keep reporting
   `unverifiable`; (b) accept one exact not-found response as "completed, no
   findings"; (c) cross-check with a second endpoint before accepting. This is
   the one place a false clean could enter, so it needs evidence from step 1
   and an explicit decision.
4. **Confirm CI is green** on the first pull request.

## Next — a single-source monitor you can rely on

5. Per-profile history retention, so one profile cannot evict another's
   baseline, and a visible warning when a baseline has aged out.
6. Honour `Retry-After` and add a minimum interval between live checks of the
   same profile.
7. An installed `watchdog` command.
8. Split `cli.py` into state, serialization, and command modules.
9. A report that reads as plain sentences for the common cases, alongside the
   current line format.

## Later — unattended use and breadth

10. Scheduled checks and a local notification when, and only when, exposure
    changes or checks keep failing. Needs its own approval: it automates an
    external action.
11. Encryption at rest for the profile store. Needs a reviewed design and
    probably a dependency.
12. A second source for email (breach details, or another provider) and a
    first source for usernames. Each is a new adapter with its own contract
    work.
13. Move the research documents under `docs/research/`.

## Open decisions

- The no-match contract (item 3).
- Whether the repository stays public once real identifiers are used locally.
  Nothing real is committed, and the guard and CI enforce that for email
  addresses only.
- Whether the tamper-evident ledger from the old itinerary is still wanted.
  It is not on this roadmap.
- Whether profile references need to exceed 999.

## Not planned

Dark-web search, password or credential checking, scanning anyone other than
the consenting local user, active countermeasures, and anything that evades
access controls.
