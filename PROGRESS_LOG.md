# Personal Watchdog progress log

This file is a chronological engineering journal. Its timestamps are copied
from the local system clock or Git metadata and are **unverified**: they are not
independently authenticated, cryptographically timestamped, or proof of when an
event occurred.

Entries should be appended rather than silently rewritten. If an earlier entry
is wrong, add a dated correction that links back to it. Keep confirmed facts,
assumptions, gotchas, wrong directions, verification results, and approval
boundaries visibly distinct. Never include real personal information, secrets,
or complete email addresses.

## 2026-08-17T21:26:47+01:00 (unverified local timestamp)

### Scope

Begin with Milestone 0 only. Inspect and preserve the existing repository; do
not use real personal information or proceed to live integrations.

### Observed facts

- The repository was already on `main` at commit
  `b07bed2c3872b083f541d7ae6c1b29e568c0079b` (`chore: establish milestone 0
  project foundation`). Git records that commit time as
  `2026-08-06T13:35:25+01:00`; that timestamp is also unverified metadata.
- Existing tracked project material comprised the policy and introductory
  documents, `pyproject.toml`, one policy smoke-test module, and the empty data
  directory placeholder. Local development tooling and caches were present.
- `PERSONAL_WATCHDOG_CODEX_ITINERARY.md` was not present in the repository or
  in the bounded search performed under `/home/peters`.
- The existing Milestone 0 checks passed: 3 tests, Ruff format check, Ruff lint,
  strict mypy, and `git diff --check`.
- A bounded scan of repository files, excluding Git metadata and the virtual
  environment, found no complete email-address or common credential-pattern
  matches.
- The worktree was clean before this progress log was added.

### Decision

Treat the current repository as an existing Milestone 0 checkpoint. Add only
this progress record; do not infer missing itinerary requirements, implement
Milestone 1, add dependencies, use live services, or introduce personal data.

### Gotchas and assumptions

- **Gotcha:** The request named an itinerary file, which made its presence seem
  likely. Inspection disproved that assumption. A missing file is not evidence
  of its intended contents.
- **Gotcha:** A prior commit and passing checks indicate a coherent checkpoint,
  but they do not independently prove that every requirement in the unavailable
  itinerary was satisfied.
- **Assumption:** The supplied repository-wide contributor rules and the
  visible Milestone 0 documentation are the operative constraints until the
  itinerary is supplied. This is a working assumption, not a recovered insight
  about the missing document.

### Wrong directions and avoided errors

- Reconstructing the missing itinerary from recollection or surrounding files
  would create false certainty, so that direction was rejected.
- Continuing into the described offline vertical slice would cross the stated
  Milestone 0 boundary, so no implementation work was started.

### Verification after this entry

Pending at the time the entry was created. Results should be appended below,
not backfilled into this statement.

## 2026-08-17T21:27:15+01:00 (unverified local timestamp)

### Verification result

- Pytest: 3 passed.
- Ruff format check: passed (6 files already formatted).
- Ruff lint: passed.
- Strict mypy: passed (1 source file checked).
- `git diff --check`: passed.
- Git status: `PROGRESS_LOG.md` is the only untracked file; no existing tracked
  file was modified.

## 2026-08-17T21:40:37+01:00 (unverified local timestamp)

### Scope

Confirm the Personal Watchdog project root, locate or place the missing
itinerary, and revise the Milestone 1 proposal using approved integrity
principles from the read-only Kibitzr evidence archive. Do not implement code.

### Observed facts

- The project root is `/home/peters/personal-watchdog` on branch `main`.
- Before this planning change, `PROGRESS_LOG.md` was the only untracked file.
- A bounded search under `/home/peters` found no file named
  `PERSONAL_WATCHDOG_CODEX_ITINERARY.md`.
- The evidence-collection repository was inspected only as architectural
  reference. Its existing untracked bytecode files were left untouched.

### Decision

Place a new `PERSONAL_WATCHDOG_CODEX_ITINERARY.md` in this repository. Keep
Milestone 0 as the policy and planning foundation, and present a revised,
fully offline Milestone 1 design for approval before implementation.

### Gotchas and assumptions

- **Gotcha:** A hash chain can expose many edits but does not authenticate its
  timestamps or detect a fully consistent rewrite by the keeper unless a head
  is committed outside the archive. External commitments remain out of scope.
- **Gotcha:** Retaining raw pages can improve re-derivation while violating this
  project's selective-evidence privacy boundary. The plan adopts bounded,
  normalized evidence objects instead.
- **Assumption:** One global event chain is preferable for Milestone 1 because
  it makes ordering between scan lifecycle events and corrections explicit.
  This remains a proposal until approved.

### Wrong directions and avoided errors

- No files were created under the evidence-collection repository.
- Kibitzr's live fetch, timestamp, report, service, backup, export, and
  deployment machinery were not copied into the Personal Watchdog plan.
- No application code, database, fixture, adapter, or verifier was implemented.

## 2026-08-17T21:42:20+01:00 (unverified local timestamp)

### Planning verification result

- Pytest: 3 passed.
- Ruff format check: passed (7 files already formatted).
- Ruff lint: passed.
- Strict mypy: passed (1 source file checked).
- `git diff --check`: passed.
- Bounded complete-email and common credential-pattern scan: no findings.
- Git status: `PERSONAL_WATCHDOG_CODEX_ITINERARY.md` and `PROGRESS_LOG.md`
  are untracked; no tracked file was modified.
- Implementation remains stopped at the approval gate.

## 2026-08-18 — Base Zero completion (unverified local date)

### Scope

Complete the Base Zero research records and preserve the Milestone 0 boundary.
Do not implement watchdog behaviour or begin the comparator experiment.

### Observed facts

- The existing Milestone 0 commit remains valid and is preserved unchanged.
- The three previously untracked handoff documents are being added.
- `PROJECT_HISTORY.md`, `RESEARCH_LOG.md`, `DECISIONS.md`, `REFERENCES.md`,
  and `BUILD_HISTORY.md` record the history that can be supported by the
  existing repository and documents.
- The eight retained MIT-licensed projects remain references, not dependencies.
- Kibitzr and `/home/peters/evidence-collection/repo/` remain read-only
  architectural reference material.
- No bark definition has been experimentally validated. No scanner,
  comparator, persistence layer, or live adapter exists.
- The next proposed research question is whether deterministic observations can
  be converted into rare, truthful bark events.

### Decision

Treat Base Zero as complete when the documentation records, requested checks,
diff review, and single documentation commit are complete. Stop before the
comparator experiment.

### Verification

- `.venv/bin/python -m pytest` — 3 passed.
- `.venv/bin/ruff format --check .` — 13 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 1 source file.
- `git diff --check` — passed.

### Gotchas and assumptions

- The final commit hash cannot be written literally into its own committed
  entry without creating a circular content dependency; it is reported in the
  handoff instead.
- The history records distinguish direct Git verification from reconstruction
  from existing documents and supplied history.

## 2026-09-06 — R2.5 framing handoff (unverified local date)

### Scope

Frame, but do not implement, a visible deterministic offline simulator around
the completed synthetic R1/R2 behavior. Preserve synthetic-only, standard-
library-only, no-network, no-persistence, no-notification, no-credentials,
no-archive, and no-R3 boundaries.

### Observed facts

- The repository is on `experiment/r2-5-visible-offline-simulator` at the
  supplied R2-complete commit `4f16048`.
- R1 remains the owner of comparison and derived exposure/guarding events.
- R2 remains the owner of bytes-first response normalization and returns only
  an R1 source check.
- The proposed document covers all ten curated scenarios and keeps every
  failure or uncertainty path visible.
- Repeated-failure suppression, recovery, trivial-change suppression,
  simultaneous grouping, baseline overload, minimum actionable bark
  information, and disappearance confirmation remain unresolved policy
  questions for later experiments.
- The editable-install setuptools discovery issue remains separate work.

### Decision boundary

Add only `RESEARCH_002_5_VISIBLE_OFFLINE_SIMULATOR.md` plus these append-only
history entries. Stop for adversarial review before creating the proposed
Phase 2 implementation, scenario fixture, or tests.

### Verification

- Baseline `.venv/bin/python -m pytest` — 101 passed.
- No simulator, scenario fixture, network call, real identifier, persistence,
  evidence archive change, or notification was created.

### Next question

Will the proposed Phase 2 implementation remain a thin deterministic
orchestrator rather than becoming a second R1/R2 or bark-policy owner?

## 2026-09-06 — R2.5 framing verification correction (unverified local date)

### Observed facts

- The final documentation-only framing was reconciled against the existing
  R1/R2 APIs; the repository's existing 101-test suite, Ruff format and lint,
  strict mypy, and `git diff --check` pass. These checks do not execute or
  behaviorally verify the proposed simulator.
- The proposed schema is one scenario per JSON file, with ten exact scenario
  files proposed for Phase 2.
- No material repository contradiction blocks the framing. README milestone
  wording is consistent with no product scanner, live adapter, or reporting
  CLI, while the later synthetic R1/R2 code and history remain authoritative
  for the completed experiments.

### Decision boundary

Remain stopped for adversarial review. Do not implement the simulator, add
scenario fixtures, modify R1/R2, fix packaging, or update `DECISIONS.md`.

### Verification

- `.venv/bin/python -m pytest` — 101 passed.
- `.venv/bin/ruff format --check .` — 24 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.

## 2026-09-08 — R2.5 framing contract revision (unverified local date)

### Scope

Revise the R2.5 framing only. Keep the runner unimplemented and do not begin
Phase 2.

### Observed reconciliation

- Check-level R2 expectations and scan-level R1 `ComparisonReport` expectations
  are now separated.
- Output grammar, machine key sets, mismatch records, invalid diagnostics,
  ordering, stdout/stderr behavior, deterministic IDs, and fixed outer bounds
  are specified.
- Exposure silence is derived from actual R1 exposure events only.
- Scenario 7 uses local construction error; Scenario 5 retains explicit R2
  failure; Scenario 8 names the R1 trusted identity/version boundary.
- The proposed behavior remains documented/reconciled only, not executed or
  behaviorally verified.

### Decision boundary

Remain stopped for adversarial review. Do not implement, stage, commit, push,
or modify R1/R2.

## 2026-09-08 — R2.5 framing revision verification (unverified local date)

### Verification observation

- Existing pytest suite: 101 passed.
- Ruff format check: 24 files already formatted.
- Ruff lint: all checks passed.
- mypy: success, no issues found in 9 source files.
- `git diff --check`: passed.
- Complete diff inspection found only the framing document and the three
  already changed logs modified or untracked.

These checks validate the existing repository and documentation hygiene only;
the proposed simulator remains unimplemented and unexecuted.

## 2026-09-08 — Final R2.5 framing verification (unverified local date)

### Verification observation

The final repository checks remain green: 101 tests passed; Ruff format and
lint passed; mypy found no issues in 9 source files; and `git diff --check`
passed. Complete diff inspection found only the framing document and the three
already changed logs. This does not execute or behaviorally verify the proposed
simulator.

### Decision boundary

Stop for adversarial review. No Phase 2 implementation or Git mutation was
performed.

## 2026-09-08 — Final R2.5 ownership-boundary correction (unverified local date)

### Observed reconciliation

- The runner constructs only `scan_id` and `source_check_id`; R1 alone
  constructs `comparison_id` and `guard_id`.
- Expected IDs are ordinary well-typed oracle strings compared literally.
  Wrong expected IDs produce expectation mismatch, exit code `1`.
- Per-scan duplicate resolved `source_id` values are `reference_error`, exit
  code `2`; identities may change between scans.
- The one-file runner validates `scenario_id` syntax, while the ten-fixture
  test suite must enforce cross-file uniqueness.

### Decision boundary

Stop for adversarial review. The proposed simulator remains unimplemented,
unstaged, uncommitted, unpushed, and behaviorally unverified.

## 2026-09-08 — Verify final R2.5 boundary correction (unverified local date)

### Verification observation

The established checks completed successfully: 101 tests passed; Ruff format
and lint passed; mypy found no issues in 9 source files; and `git diff --check`
passed. Complete diff inspection found only the framing document and the three
already changed logs. The proposed simulator remains unimplemented and
unexecuted.

## 2026-09-08 — R2.5 implementation execution record

The frozen framing was implemented as a visible deterministic offline runner
with ten synthetic scenario files and focused tests. Human and machine CLI
runs passed for all ten scenarios with exit code `0`; controlled expectation
mismatch and invalid-scenario CLI tests returned `1` and `2` respectively.
The full suite passed with 129 tests, and formatting, lint, mypy, and diff
checks passed. These results are local synthetic observations only and do not
establish live-source truth or product usefulness.

Stop for adversarial implementation review. No staging, commit, push, or R3
work was performed.

## 2026-09-08 — R2.5 adversarial implementation corrections

The Phase 2 runner now bounds file reads before parsing, emits array-accurate
and insertion-order-independent mismatch pointers, and reports exact local
construction validation paths. Tests cover the complete output contract,
declared bounds, focused validation, expectation isolation, and synthetic
fixture hygiene. All ten scenarios passed in both modes; the full suite passed
with 147 tests. No R1/R2 or valid scenario meaning changed.

Stop for adversarial review. No staging, commit, push, or R3 work was
performed.
