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
