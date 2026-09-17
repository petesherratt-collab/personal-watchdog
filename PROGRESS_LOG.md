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

## 2026-09-08 — R3 Phase 1 XposedOrNot contract research (unverified local date)

### Scope

Read the repository-authoritative R2.5 checkpoint and research only official
XposedOrNot documentation and official repositories. Create the R3 contract
framing document; do not implement an adapter or make a live request.

### Observed facts

- The requested branch is at the supplied R2.5 merge commit, with the stated
  147-test checkpoint and no material repository contradiction.
- Official XposedOrNot documentation describes a keyless free email lookup,
  analytics, password, catalogue, and key-authorized domain routes. Official
  SDKs separately describe Plus behavior.
- Official sources conflict or leave gaps around the free no-result HTTP
  status, the optional detail query name, rate spacing, error bodies, exact
  schema, content type/encoding, pagination, ordering, duplicates, response
  limits, and completeness/freshness.
- The conservative result keeps R1 as the owner of comparison and
  disappearance, R2 as the owner of bytes-to-`SourceCheck` normalization, and
  all ambiguous or failed paths outside completed-empty.

### Decision boundary

The synthetic adapter experiment is framed but not implemented or approved as
live work. `DECISIONS.md` was not changed. No endpoint, identifier,
credential, password, dependency, HTTP client, persistence, scheduler,
notification, evidence archive, or R4 work was added.

### Gotchas and assumptions

- **Gotcha:** The official documentation’s free email no-result example has no
  stated status, while the status table and Python SDK treat 404 as an error.
  The framing preserves both facts instead of choosing one.
- **Gotcha:** The official docs say `details`; the Python SDK sends
  `include_details`. This blocks silently assuming one request contract.
- **Assumption:** The documented analytics HTTP 200 all-null shape is a valid
  genuine-empty synthetic fixture only when analytics is explicitly selected;
  the free email no-result body is not treated as empty.

### Verification after this entry

Pending. Results will be appended below after the full repository checks and
complete diff/status inspection.

## 2026-09-08 — R3 Phase 1 verification (unverified local date)

### Verification observation

- Full pytest suite: 147 passed.
- Ruff format check: 28 files already formatted.
- Ruff lint: all checks passed.
- mypy: success, no issues found in 12 source files.
- `git diff --check`: passed.
- Complete diff inspection found only the permitted R3 research document and
  append-only history/log updates.

The checks validate repository hygiene and existing synthetic behavior only;
they do not call XposedOrNot or establish live-source truth.

### Decision boundary

Stop for adversarial review. Do not stage, commit, push, implement the adapter,
or make a live request.

## 2026-09-08 — R3 Phase 1 framing correction after Swagger/OpenAPI review

### Scope

Access only the official Swagger/OpenAPI documentation identified by the
official API repository, plus pinned official GitHub source revisions. No
functional lookup request or identifier was used.

### Corrections

- `/docs` is the official Swagger UI and `/openapi.json` reports OpenAPI
  `3.0.0`, API specification version `2.0.0`, and the production server.
- The specification resolves `include_details`, `application/json`, email
  parameter formats, and selected 200/404 statuses, but leaves schemas open
  and does not define no-match, encoding, size, pagination, duplicate,
  ordering, freshness, or completeness rules.
- The first synthetic experiment is now only free check-email with its own
  source identity, scope, and schema version. Analytics is a deferred,
  separate family and matrix.
- The exact analytics sentinel is
  `XON_ANALYTICS_HTTP_200_NO_MATCH_V1`, including non-null empty summary
  objects.
- The proposed transport envelope keeps HTTP metadata untrusted and keeps
  trusted source context local, with explicit transport/XON/R2/R1 boundaries.
- Exact duplicates use existing R2 deterministic deduplication; conflicting
  duplicates remain unverifiable.
- The permitted tracked record scope is four files:
  `BUILD_HISTORY.md`, `PROGRESS_LOG.md`, `REFERENCES.md`, and
  `RESEARCH_LOG.md`.

### Decision boundary

No adapter or HTTP client is implemented. No live request, credential,
identifier, persistence, evidence archive, scheduler, notification, R4 work,
staging, commit, push, or `DECISIONS.md` update is authorized by this
correction.

## 2026-09-08 — Verification of corrected R3 framing

### Results

- `.venv/bin/python -m pytest` — 147 passed in 6.01 seconds.
- `.venv/bin/ruff format --check .` — `28 files already formatted`.
- `.venv/bin/ruff check .` — `All checks passed!`.
- `.venv/bin/mypy .` — `Success: no issues found in 12 source files`.
- `git diff --check` — passed with no output.

The formatting count is 28 because Ruff includes the new Markdown R3 document;
the R2.5 commit and current worktree each contain 12 Python files. The prior
27 count was the earlier included-file count, not a Python source change.

### Boundary

The four tracked record files are `BUILD_HISTORY.md`, `PROGRESS_LOG.md`,
`REFERENCES.md`, and `RESEARCH_LOG.md`, alongside the R3 research document.
No code, adapter, HTTP client, identifier, credential, live request, staging,
commit, push, or external archive change was made.

## 2026-09-08 — Final verification after coherent R3 rewrite

### Verification

Complete diff and status inspection occurred before the final verification
sequence. The exact outputs were:

- `.venv/bin/python -m pytest` — 147 passed in 6.01 seconds.
- `.venv/bin/ruff format --check .` — `28 files already formatted`.
- `.venv/bin/ruff check .` — `All checks passed!`.
- `.venv/bin/mypy .` — `Success: no issues found in 12 source files`.
- `git diff --check` — passed with no output.

The prior 5.98-second pytest run and this final 6.01-second run are separate
successful runs; only execution timing differs.

### Boundary

The rewritten research document has one coherent Sections 1–22 specification
and no Section 23. No implementation or live request was made.

## 2026-09-09 — Final R3 contract-gap correction

### Corrections

- The selected check-email matrix no longer claims a conflicting duplicate
  fixture. Exact duplicate names use existing R2 deduplication; conflicting
  duplicates are generic R2-only protection.
- The analytics matrix is now sentinel-and-rejection research only. No
  analytics positive-success schema is frozen, and future positive-success
  framing is required before implementation.
- Content-Type derivation is now exact: trim only ASCII space/tab at both ends,
  reject non-ASCII and every parameter, compare the remaining media type ASCII
  case-insensitively to `application/json`, and reject duplicate names before
  derivation. The retained-header byte formula is explicit.
- Normalized R2 serialization is frozen as compact UTF-8 JSON with deterministic
  key order, `ensure_ascii=True` behavior, no non-standard numbers, final-byte
  measurement, and refusal to call R2 above 65,536 bytes.
- Transport states now distinguish before-status failure, after-status
  incomplete read/timeout with preserved status, complete response, and
  over-limit response. Contradictory local fixtures reject visibly.
- Every selected check-email matrix row now specifies transport, XON, and R2
  outcomes or construction rejection. R1 remains the sole owner of comparison,
  exposure, guarding, and disappearance.

### Boundary

No adapter, HTTP client, live request, identifier, credential, dependency,
R1/R2/R2.5 change, analytics implementation, staging, commit, push, or
unrelated file modification was made.

## 2026-09-09 — Verification of final R3 contract-gap correction

### Results

The complete requested diff inspection and status review preceded the final
sequence:

- `./.venv/bin/python -m pytest` — 147 passed in 6.08 seconds.
- `./.venv/bin/ruff format --check .` — `28 files already formatted`.
- `./.venv/bin/ruff check .` — `All checks passed!`.
- `./.venv/bin/mypy .` — `Success: no issues found in 12 source files`.
- `git diff --check` — passed with no output.

### Boundary

No implementation, functional request, identifier, credential, staging,
commit, push, or unrelated file change was made.

## 2026-09-09 — R3 Phase 2 synthetic experiment implementation

R3 Phase 2 now contains only the frozen free check-email synthetic adapter,
fixtures, and tests. The adapter keeps trusted source context outside
response bytes, distinguishes pre-status and post-status failures, rejects
ambiguous HTTP-200 bodies, preserves the selected no-completed-empty rule,
delegates candidate validation/deduplication to R2, and leaves all comparison,
exposure, guarding, and disappearance semantics to R1.

The implementation remains offline and standard-library-only. Analytics and
live integration remain deferred.

## 2026-09-09 — R3 Phase 2 verification

The final requested sequence passed: 199 tests, 31 Ruff-formatted files,
clean Ruff lint, mypy with 15 checked source files, and clean Git whitespace.
The 199-test total is 147 existing tests plus 52 new synthetic XON tests; the
R2.5 implementation files were not changed. The experiment remains offline,
synthetic, and stopped before live integration.

## 2026-09-09 — Final transport invariant correction

Pre-status transport failures now reject retained response headers as a visible
construction error. The final rerun remained green: 199 tests passed, Ruff
format/lint passed, mypy passed, and `git diff --check` passed. This is the
final Phase 2 verification state.

## 2026-09-09 — R3 Phase 2 adversarial correction pass

Added the bounded hostile-integer regression, explicit simultaneous-fault
precedence, exact non-BMP size evidence, all requested adjacent-bound tests,
and chronologically distinct R1 integration IDs. The selected experiment
remains synthetic, standard-library-only, and offline.

## 2026-09-09 — Verify R3 Phase 2 adversarial correction pass

Final verification passed: 207 tests, Ruff format and lint, mypy, and
`git diff --check`. The branch remains uncommitted and no live-source work was
started.

## 2026-09-09 — R3 Phase 2 final consistency corrections

Aligned the oversized-envelope documentation with the implemented visible
construction rejection and added the missing incomplete first-check R1 guard
coverage. Corrected the recorded test arithmetic to 147 pre-R3 plus 60 focused
XON tests = 207 total.

## 2026-09-09 — Verify R3 Phase 2 final consistency corrections

Final consistency verification passed with 207 tests and clean formatting,
lint, mypy, and whitespace checks. No commit, push, or live-source work was
performed.

## 2026-09-09 — R3.5 visible synthetic XON scenario framing

### Scope

Frame, but do not implement, a new visible scenario family around the
committed synthetic XON check-email adapter. Preserve the existing R2.5
scenario contracts and outputs, the standard-library-only boundary, and the
no-network/no-real-identifier/no-credential rules.

### Observed reconciliation

- The requested starting checkpoint is clean merge commit `35ef380` on the
  requested branch with 207 passing tests.
- The existing offline simulator does not yet dispatch to the XON adapter.
- The existing XON adapter owns transport classification and body
  normalization, delegates generated-envelope validation to R2, and returns
  only an R1 SourceCheck.
- The adapter has no separate public XON-classification record, so the framing
  limits XON classification to a display projection of public adapter output.
- R1 receives the immediately preceding ScanAttempt, so a failed or
  unverifiable scan can displace the last successful comparable state.

### Framing result

Created `RESEARCH_003_5_VISIBLE_XON_SCENARIOS.md` with the proposed
`r3.5-visible-xon-scenarios/1` family, exact transport/body/header-byte
representation, strict bounds and diagnostics, 17 curated scenarios,
complete transport/R2/R1 oracle requirements, frozen output/exit behavior,
delegation tests, backward-compatibility checks, and the exact proposed Phase
2 file list.

### Boundary and assumptions

Scenario 17 is framed using the existing multi-source R1/R2.5 model with
explicit XON versus existing synthetic-R2 adapter dispatch; it adds no new
comparison semantics. Scenario 16 is intentionally invalid input and must
produce exit code 2 without a SourceCheck or R1 report. No policy question
about suppression, recovery, disappearance confirmation, grouping, baseline
retention, or notification was settled.

No source, test, fixture, existing research specification, reference,
decision, dependency, network endpoint, credential, persistence layer,
evidence archive, staging, commit, push, merge, or Phase 2 implementation was
performed. The editable-install packaging gotcha remains separate work.

### Verification after this entry

Pending. Results will be appended below after the required checks and complete
diff/status inspection.

## 2026-09-09 — Verify R3.5 visible synthetic XON scenario framing

The required verification sequence passed: 207 tests, Ruff format check,
Ruff lint, mypy, and `git diff --check`. The complete review confirmed that
only `RESEARCH_003_5_VISIBLE_XON_SCENARIOS.md`, `RESEARCH_LOG.md`,
`BUILD_HISTORY.md`, and this log changed. The branch remains unstaged and
uncommitted; no implementation or scenario execution was performed.

## 2026-09-09 — Amend R3.5 framing after adversarial self-review

Added complete normative R1 report macros, covered the previously omitted
wrong Content-Type case, and corrected the mixed-source R1 ordering. This
remains documentation-only and unstaged.

## 2026-09-09 — Verify amended R3.5 framing

The final required checks passed again after the adversarial framing
corrections: 207 tests, Ruff format, Ruff lint, mypy, and `git diff --check`.
No source, test, fixture, or existing specification changed.

## 2026-09-09 — Correct remaining R3.5 framing details

Corrected the hostile-body byte count to 5,088, permitted empty raw header
names as adapter-owned untrusted metadata, froze exact trusted source JSON
types and literal identities, completed mixed-source input/output semantics,
froze Scenario 16's exact invalid result, replaced filename/ID equality with
an explicit table, made the XON presentation projection exhaustive, corrected
the oracle wording, and added the three append-only Phase 2 record files to
the proposed list. No implementation or unrelated file change was made.

## 2026-09-09 — Verify corrected R3.5 framing

The final verification passed: pytest reported 207 passed in 7.12 seconds;
Ruff format reported 32 files already formatted; Ruff lint passed; mypy
reported no issues in 15 source files; and git diff --check passed. The
corrected framing remains unimplemented and no source, test, fixture, or
unrelated file changed.

## 2026-09-09 — Freeze R3.5 XON projection internal error

Fully froze xon_projection_invariant as an R3.5-only internal-error fallback:
READY transport plus an unexpected adapter status stops immediately with exit
2, discards normal output, emits the exact human or JSON diagnostic, produces
no XON or R1 result, and skips later scans. R2.5 diagnostics remain unchanged;
both output forms are required in the Phase 2 test double.

## 2026-09-09 — Verify frozen R3.5 XON projection internal error

The established verification sequence passed: 207 tests in 6.57 seconds,
32 files already formatted, Ruff lint passed, mypy found no issues in 15
source files, and git diff --check passed. The fallback remains documentation
only and was not executed.

## 2026-09-09 — R3.5 Phase 2 implementation complete

The visible synthetic XON scenario experiment is implemented within the
frozen Phase 2 boundary. The simulator dispatches only the exact R3.5
scenario version and allowlisted adapter identities, preserves R2.5 behavior,
and exposes transport, XON, R2, and R1 projections without duplicating their
semantics. The 17 required scenarios and focused delegation/diagnostic tests
are present. No live request, identifier, credential, or network operation was
used.

## 2026-09-09 — R3.5 Phase 2 verification

242 tests passed; Ruff format and lint passed; mypy passed; and
`git diff --check` passed. The valid curated scenario set passed in both
output modes, Scenario 16 remained an invalid construction result, and the
branch is left unstaged and uncommitted for adversarial implementation review.

## 2026-09-09 — Final R3.5 Phase 2 verification correction

The final verification run passed with 243 tests, 34 formatted files, clean
Ruff lint, clean mypy across 17 source files, and clean `git diff --check`.
The previous 242-test record remains unchanged as historical output from the
earlier focused-test set.

## 2026-09-09 — Final verification after invalid-family correction

The final verification passed: 243 tests, 34 files already formatted, clean
Ruff lint, clean mypy across 17 source files, and clean `git diff --check`.
The implementation remains uncommitted and ready for adversarial review.

## 2026-09-10 — R3.5 Phase 2 adversarial test-strengthening correction

Added independent fixture digest and raw-byte proofs, exact Scenario 17 output
goldens, complete nested output-schema checks, strict-oracle assertions,
delegation-call and immediate-prior object checks, and source-structure guards
against runner semantic duplication. No runner semantics or scenario bytes
changed.

## 2026-09-10 — Verify R3.5 Phase 2 adversarial test strengthening

All 17 scenarios passed in both modes (34 runs: 32 exit 0 and 2 exit 2), the
full suite passed with 252 tests, Ruff format/lint and mypy passed, and
`git diff --check` passed. The editable-install setuptools discovery issue
remains an unchanged separate Gotcha.

## 2026-09-11 — R4 Phase 1 bounded live XON probe framing

### Scope

Frame, but do not execute, the smallest live follow-on to the synthetic R3
and R3.5 XON experiments: one approval-gated HTTPS check-email request using
one reserved-domain synthetic identifier and the existing bounded
`TransportAttempt` contract.

### Observed reconciliation

- The authoritative branch starts at `573d44c` and was clean before editing.
- The R3 adapter is deliberately I/O-free and already owns transport, XON,
  and R2 classification after a captured attempt is supplied.
- R3.5 proves only deterministic offline delegation; it provides no live
  compatibility, completeness, freshness, or safety evidence.

### Framing result

`RESEARCH_004_BOUNDED_LIVE_XON_PROBE.md` freezes the proposed one-request
scope, reserved-domain subject rule, no-credential/no-retry/no-redirect
boundary, inherited byte and header bounds, explicit future timeout approval,
minimal local retention, and conservative outcome mapping. It does not add a
collector, HTTP client, live request, comparison policy, persistence,
notification, or archive.

### Decision boundary

No live request or identifier submission was made. Phase 2 is blocked on
explicit approval of the exact synthetic identifier, endpoint, headers,
timeouts, one-request budget, retention fields, and stop conditions. Any need
to loosen R3/R2/R1 semantics or add a retry, baseline, or raw-payload policy
requires a new framing decision.

## 2026-09-11 — Verify R4 Phase 1 framing

### Verification

The final repository checks passed: 252 tests; 35 files already formatted;
Ruff lint passed; mypy passed across 17 source files; and `git diff --check`
passed. The final status review found only the R4 framing document and the
three permitted append-only records changed.

### Boundary

This verifies the documentation and existing synthetic checkpoint only. No
live request, network operation, identifier submission, collector, or Phase 2
implementation was performed. The branch remains unstaged, uncommitted, and
unpushed.

## 2026-09-11 — Execute approved R4 Phase 2 bounded live XON probe

### Scope and execution

After explicit approval, implemented and ran the one-shot bounded probe with
`r4-probe-01@example.invalid` against the documented free check-email
endpoint. The probe made exactly one request, used no credentials, did not
retry or follow redirects, and retained no raw response body.

### Observed result

The transport was `ready`: HTTP 200, five retained headers, complete 34-byte
body, and `application/json`. The existing R3/R2 path returned
`unverifiable` with `response_unverifiable` and no finding keys. The body was
not retained, so its exact shape is unknown and no more specific explanation
is claimed.

### Verification and boundary

Five focused R4 tests and the full 257-test suite passed; Ruff format/lint,
mypy across 19 source files, and `git diff --check` passed. No collector,
persistence, comparison, notification, retry, second request, staging,
commit, or push was performed. Further live work requires new approval.

## 2026-09-12 — R4 Stage 1 adversarial offline review

### Corrections

Corrected `URLError`-wrapped timeout classification, rejected non-text
response-header metadata, and redacted the complete synthetic identifier from
the report. Added offline tests for pre-status and post-status timeouts,
duplicate content type, redirect rejection, over-limit capture, and output
redaction.

### Verification and boundary

The full suite passed with 261 tests; Ruff format/lint and mypy across 19
source files passed; and `git diff --check` passed. The prior live observation
was not repeated. No network request, collector, persistence, comparison,
notification, staging, commit, or push was performed.

## 2026-09-12 — R4 Stage 2 conclusion

### Result

R4 is inconclusive at the live source-contract boundary. The single request
reached ready HTTP-200 JSON transport, but the frozen R3/R2 path returned
`unverifiable`; the body was not retained, so its exact shape is unknown.

### Boundary

Stop without retrying, loosening the schema, inferring completed-empty,
comparing the result, or beginning monitoring. Any diagnostic follow-up needs
new approval for a more specific bounded retention rule and another explicit
request.

## 2026-09-13 — R4 Stage 3 diagnostic follow-up

### Result

The approved second request made exactly one request with diagnostic output.
The complete HTTP-200 JSON body decoded to `{"Error":"Not found","email":null}`.
The existing R3/R2 path correctly returned `unverifiable` with
`response_unverifiable`; no completed-empty or clean result was produced.

### Boundary

The response bytes were bounded, emitted as hex, and not written to disk. This
confirms one observed no-match shape only; it does not establish a general
HTTP status, completeness, freshness, stability, ownership, or safety claim.
No retry, third request, persistence, comparison, notification, collector,
staging, commit, or push was performed.

## 2026-09-13 — R4 Stage 4 complete

Final review and handoff preparation are complete. The intended six-file R4
change set is present, the branch remains at `573d44c` on
`experiment/r4-bounded-live-xon-probe`, and the worktree is uncommitted and
unstaged. Verification remains green: 261 tests passed, Ruff format/lint
passed, mypy passed using the configured `tests` target with 6 source files
checked, and `git diff --check` passed.

The experiment remains bounded and inconclusive for live source mapping:
R3/R2 preserves `unverifiable`, with no completed-empty or clean claim. No
additional live request is warranted. Commit authorization remains separate.

## 2026-09-15 — R5 Phase 1 framed locally

Added the documentation-only R5 framing for offline XON contract
reconciliation. The proposed experiment would test whether the exact observed
R4 HTTP-200 `{"Error":"Not found","email":null}` shape can reproduce the
existing R3/R2 `unverifiable` result without weakening semantics or making a
new live request.

No fixture, implementation, test, dependency, network request, commit, push,
or pull-request update was made. Stop for review and explicit Phase 2 scope
approval.

## 2026-09-15 — R5 Phase 2 executed offline

The approved R5 fixture and test were added locally. The existing R3/R2
adapter reproduced `transport=ready` with source status `unverifiable`, reason
`response_unverifiable`, and no findings. Focused R5 tests: 2 passed; full
suite: 263 passed. Ruff format/lint, mypy, and `git diff --check` passed.

No live request, dependency, semantic adapter change, R1 comparison,
persistence, notification, collector, commit, or push was made. R5 remains a
one-observation offline reconciliation, not a general XON no-match contract.

## 2026-09-15 — R6 Phase 1 framed locally

Added documentation-only framing for the minimal user workflow:
`init → scan → compare → report → history`. The proposed first implementation
uses one synthetic subject and one offline fixture source, with bounded local
records and truthful handling of completed, failed, and unverifiable checks.

No CLI, persistence, scheduler, notification, live request, dependency,
commit, push, or pull-request update was made. R6 Phase 2 requires explicit
approval of storage, retention, command, and test details.

## 2026-09-15 — R6 Phase 2 executed offline

Implemented the approved local workflow in `personal_watchdog/cli.py` with
bounded JSON state and one synthetic fixture source. The commands now support
initialization, fixture scans, latest reports, and retained history. Existing
R1 comparison and R2 normalization remain the semantic owners.

Focused R6 tests: 5 passed; full suite: 268 passed. Ruff format/lint, mypy,
and `git diff --check` passed. No live request, real identifier, scheduler,
notification, dependency, commit, or push was added. Changes remain local and
uncommitted for review.

## 2026-09-16 — R7 Phase 1 framed locally

Added documentation-only framing for approved-identifier configuration, the
first ordered R7 focus. It defines explicit approval and enablement, opaque
subject references, redacted ordinary output, local-sensitive profile values,
and separation from R6 scan history.

No profile storage, CLI change, real identifier, live request, dependency,
commit, push, scheduler, notification, or export was added. Phase 2 requires
explicit approval of the schema, input channel, permissions, migration,
retention, and synthetic test scope.

## 2026-09-16 — R7 Phase 2 execution in progress

Peter approved the offline implementation scope. The local branch now has the
bounded profile store, CLI profile operations, optional approved-profile
fixture selection, and focused R7 tests. The focused R7/R6 set passes 11 tests;
full-suite verification and final diff/worktree review are still pending.

No real identifier or live request has been used. No commit, push, pull
request, scheduler, notification, export, or dependency change has been made.

## 2026-09-16 — R7 Phase 2 verified locally

The focused R7/R6 set passed 13 tests and the full repository suite passed 276
tests. Ruff format/lint, mypy, `git diff --check`, and the manual offline CLI
smoke test passed. The branch remains uncommitted and unpushed for review.

The implementation remains limited to synthetic local profiles and offline
fixture selection; it does not authorize or perform live collection.

## 2026-09-16 — R8 Phase 1 framed locally

Added documentation-only framing for profile retention and recovery on branch
`experiment/r8-profile-retention-recovery`, based on merged R7 commit
`81e979c`. The framing covers disablement, possible deletion, bounded local
retention, malformed state, interrupted writes, recovery, and preservation of
opaque scan history.

No implementation, fixture, test, dependency, real identifier, live request,
staging, commit, push, pull request, scheduler, notification, or export was
made. Phase 2 requires explicit approval of the retention policy, deletion
choice, corruption behavior, interruption tests, and recovery boundary.

The framing branch passed the full 276-test suite, Ruff format/lint, mypy,
and `git diff --check`. No production behavior changed, and the framing
remains uncommitted and unpushed pending review.

## 2026-09-16 — R8 Phase 2 conservative subset in progress

Peter approved the conservative offline retention/recovery subset. The profile
loader now fails closed on a missing sidecar, and focused tests cover malformed
state, interrupted writes, stale temporary files, and independent bounds.
Focused R7/R8 verification passes 16 tests; full verification is pending.

No deletion, backup, restore, re-enable, real identifier, live request,
dependency, commit, push, pull request, scheduler, notification, or export was
added.

## 2026-09-16 — R8 Phase 2 conservative subset verified locally

Focused R7/R8 tests passed 16 tests and the full repository suite passed 284
tests. Ruff format/lint, mypy on 25 source files, and `git diff --check` also
passed. The branch remains uncommitted and unpushed for review.

The implemented boundary remains fail-closed missing/malformed profile state,
preserved opaque history, interrupted-write protection, and independent
bounds. Deletion, backup, restore, re-enable, and secure-erasure claims remain
out of scope.

## 2026-09-16 — R9 Phase 1 framed locally

Added documentation-only framing for explicit approved-profile lifecycle on
branch `experiment/r9-profile-lifecycle`, based on merged R8 commit `c63c174`.
The framing covers disablement, fresh approval for re-enable, optional
two-step deletion, non-reuse of opaque references, preserved history, and
fail-closed local state.

No implementation, fixture, test, dependency, real identifier, live request,
staging, commit, push, pull request, scheduler, notification, or export was
made. Phase 2 requires explicit approval of the lifecycle protocol and the
re-enable/deletion choices.

The framing branch passed the full 284-test suite, Ruff format/lint, mypy on
25 source files, and `git diff --check`. No production behavior changed, and
the framing remains uncommitted and unpushed pending review.

## 2026-09-16 — R9 Phase 2 lifecycle execution in progress

Peter approved the R9 lifecycle protocol. The local branch now has explicit
fresh-approval re-enable, disable-before-delete, confirmed deletion,
never-reused references, and preserved-history tests. Focused R7/R8/R9 tests
pass 20 tests; full verification is pending.

No real identifier, live request, dependency, backup, scheduler, notification,
export, commit, push, or pull request was added.

## 2026-09-16 — R9 Phase 2 lifecycle verified locally

Focused R7/R8/R9 tests passed 20 tests and the full repository suite passed 288
tests. Ruff format/lint, mypy on 26 source files, and `git diff --check` also
passed. The branch remains uncommitted and unpushed for review.

The implemented lifecycle remains explicit fresh-approval re-enable,
disable-before-delete, confirmed deletion, never-reused opaque references,
and preserved history. No secure-erasure claim is made.
