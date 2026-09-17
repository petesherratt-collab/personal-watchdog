# Personal Watchdog build history

This is the chronological engineering history, distinct from
`PROJECT_HISTORY.md`. It records what was built or documented, how it was
verified, and what remained uncertain.

Where an entry says **directly verified**, the claim comes from the repository
or Git commands run for this record. Where it says **reconstructed**, the claim
comes from the existing project documents or supplied handoff history and is
not presented as a fresh Git observation.

## 2026-08-06 — Establish Milestone 0 project foundation

### Objective

Create a small, safe repository foundation for speculative Personal Watchdog
research without implementing watchdog behaviour.

### Changes

**Directly verified:** Git commit `b07bed2c3872b083f541d7ae6c1b29e568c0079b`
added `.gitignore`, `AGENTS.md`, `PRIVACY.md`, `README.md`, `SECURITY.md`,
`data/.gitkeep`, `pyproject.toml`, and `tests/test_project.py`. The project has
no runtime dependencies; development tools are configured as optional
dependencies.

**Reconstructed from the existing progress record:** policy and truthful-failure
boundaries were established and the Milestone 0 checks passed at the time.

### Verification

**Reconstructed from `PROGRESS_LOG.md`:**

- `.venv/bin/python -m pytest` — 3 passed.
- `.venv/bin/ruff format --check .` — 6 files already formatted.
- `.venv/bin/ruff check .` — passed.
- `.venv/bin/mypy .` — success, no issues found in 1 source file.
- `git diff --check` — passed.

### Decisions

Keep the first checkpoint policy-first and offline. Do not add a scanner,
identity store, adapter, ledger, evidence writer, verifier, report generator,
network request, real identifier, or later-milestone architecture.

### Gotchas

#### 1. Filesystem boundaries were easy to confuse

- **Observed:** ChatGPT Work and local Codex use different filesystems; a file
  created under `/workspace/scratch/...` does not automatically appear under
  `/home/peters/personal-watchdog/`. **Source:** reconstructed from supplied
  project history.
- **Why surprising or dangerous:** A successful write in one environment can
  look like a missing file in the repository, causing duplicate or incorrect
  reconstruction.
- **Diagnosis:** Compare the absolute path and filesystem visible to the
  command actually running in the repository.
- **Resolution or containment:** Use `/home/peters/personal-watchdog/` as the
  authoritative working path and inspect it before recreating material.
- **Open risk:** Future sessions can still use the wrong execution environment.

#### 2. An empty directory was reported in the evidence repository

- **Observed:** An accidental empty directory named `Personal Watchdog Base
  Zero` was found inside `/home/peters/evidence-collection/repo/`. **Source:**
  supplied project history; it was not inspected or modified for this step.
- **Why surprising or dangerous:** It resembles the project name but is not the
  Personal Watchdog root, so writing there would violate the repository
  boundary.
- **Diagnosis:** The reported absolute path distinguishes it from the actual
  project root.
- **Resolution or containment:** Leave the directory and the evidence
  repository untouched unless separately reviewed.
- **Open risk:** Root confusion remains possible if commands use relative paths.

#### 3. The correct project root was not self-evident

- **Observed:** The correct root is `/home/peters/personal-watchdog/`.
- **Why surprising or dangerous:** `/home/peters` contains multiple projects and
  reference material, so a command run one level too high can affect unrelated
  work.
- **Diagnosis:** Confirm `pwd`, Git branch, and repository status from the
  candidate directory.
- **Resolution or containment:** Run repository commands with the exact project
  root as the working directory.
- **Open risk:** A future shell command can still be launched from the wrong
  directory if the working directory is not checked.

#### 4. Whole-document amalgamation contaminated the research record

- **Observed:** The amalgamation became a large corpus with duplication,
  irrelevant GitHub material, at least one wrong XposedOrNot project, and
  missing Vanish material. **Source:** directly recorded in the Base Zero
  document.
- **Why surprising or dangerous:** Volume and apparent completeness can conceal
  provenance errors and missing or wrong references.
- **Diagnosis:** Compare the corpus contents against the intended retained
  projects and notice duplicated or unrelated material.
- **Resolution or containment:** Reject whole-document amalgamation and retain
  only capabilities needed for a concrete, source-labelled experiment.
- **Open risk:** A future broad import could recreate the same contamination.

#### 5. Failed checks cannot become clean negatives

- **Observed:** A failed or incomplete source check must never be converted into
  “not found” or disappearance.
- **Why surprising or dangerous:** An empty failure result looks superficially
  like a successful empty result and could create a false safety claim.
- **Diagnosis:** The rule is repeated in `AGENTS.md`, `PRIVACY.md`, and the
  itinerary's proposed outcome semantics.
- **Resolution or containment:** Make truthful failure a durable repository rule
  and require future experiments to test the distinction.
- **Open risk:** No runtime implementation exists yet, so enforcement is still
  documentary.

#### 6. A local hash chain has a residual trust limit

- **Observed:** A local hash chain can detect many edits and continuity failures
  but cannot detect a completely rewritten, internally consistent history
  without an independently retained checkpoint or external anchor.
- **Why surprising or dangerous:** Internal consistency can be mistaken for
  trustworthy time or source truth.
- **Diagnosis:** The itinerary separates recomputed continuity from external
  commitments and explicitly records the limitation.
- **Resolution or containment:** Keep external anchoring out of Base Zero and
  document the residual limitation before any future implementation.
- **Open risk:** Any future local-only integrity claim could still overstate
  what the chain proves.

#### 7. The initial commit omitted later research records

- **Observed:** The initial Milestone 0 commit did not include the later Base
  Zero, itinerary, and progress documents; they remained untracked, and the
  intended research-history files were absent. **Directly verified:** current
  Git status and the HEAD tree before this completion step.
- **Why surprising or dangerous:** A clean-looking committed foundation can be
  mistaken for the complete research record.
- **Diagnosis:** Compare `git ls-tree HEAD` with the worktree file list and
  `git status --short --branch`.
- **Resolution or containment:** Add the missing records in this one approved
  Base Zero documentation commit while preserving the original commit.
- **Open risk:** Future untracked handoff files can again be mistaken for
  committed history unless status is reviewed.

### Repository state

Directly verified before this entry: commit `b07bed2c3872b083f541d7ae6c1b29e568c0079b`,
branch `main`, with the Base Zero, itinerary, and progress documents
deliberately untracked. The final documentation commit is the requested next
state; its hash is reported in the handoff because a commit cannot contain its
own final hash as a non-circular literal.

### Next question

Whether deterministic observations can be converted into rare, truthful bark
events.

## 2026-08-17 — Record the planning and approval boundary

### Objective

Preserve the planning and handoff state while keeping the proposed offline
Milestone 1 implementation behind explicit approval.

### Changes

**Reconstructed from the existing documents:** `PROGRESS_LOG.md` recorded the
Milestone 0 handoff and `PERSONAL_WATCHDOG_CODEX_ITINERARY.md` recorded a
revised offline vertical-slice proposal. No application code or dependency was
added.

### Verification

**Reconstructed from `PROGRESS_LOG.md`:**

- `.venv/bin/python -m pytest` — 3 passed.
- `.venv/bin/ruff format --check .` — 7 files already formatted.
- `.venv/bin/ruff check .` — passed.
- `.venv/bin/mypy .` — success, no issues found in 1 source file.
- `git diff --check` — passed.

### Decisions

Treat the itinerary as a proposal, not permission to implement SQLite, a
comparator, fixtures, an adapter, evidence storage, or an independent
verifier. Preserve the read-only boundary around the evidence-collection
repository.

### Gotchas

None observed in this step beyond the historical gotchas recorded above.

### Repository state

Directly verified for this completion: branch `main` at `b07bed2`; the three
handoff documents were untracked and the research-history files were absent.

### Next question

Whether deterministic observations can be converted into rare, truthful bark
events.

## 2026-08-18 — Complete Base Zero records

### Objective

Complete the documentation and research-history scaffold without implementing
watchdog behaviour.

### Changes

Add the three existing untracked handoff documents, create
`PROJECT_HISTORY.md`, `RESEARCH_LOG.md`, `DECISIONS.md`, `REFERENCES.md`, and
`BUILD_HISTORY.md`, and add the durable build-history rule to `AGENTS.md`.
No application source, fixtures, adapters, databases, schemas, or network
integrations are added.

### Verification

- `.venv/bin/python -m pytest` — 3 passed.
- `.venv/bin/ruff format --check .` — 13 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 1 source file.
- `git diff --check` — passed.

### Decisions

Base Zero is complete as a documentation and history checkpoint. The next
question remains whether deterministic observations can be converted into
rare, truthful bark events. No comparator experiment begins here.

### Gotchas

The final commit hash is unknown until Git creates the commit, so this entry
records the pre-commit parent and reports the resulting hash in the handoff
rather than making a circular claim inside its own content. This is contained
by reporting the exact final hash after commit; it is not an open project risk.

### Repository state

Before commit: branch `main` at `b07bed2`; all requested documentation records
are staged together for the single commit named `docs: complete personal
watchdog base zero`. The final commit hash is reported in the handoff.

### Next question

Whether deterministic observations can be converted into rare, truthful bark
events.

## 2026-08-18 — Frame Research Experiment R1

### Objective

Frame the smallest proposed experiment for deciding whether deterministic
observations can become rare, truthful bark events, without implementing or
running it.

### Changes

Created `RESEARCH_001_BARK_SCHEMA.md` with the research question, hypotheses,
scope, exclusions, proposed terminology and schemas, exact comparability and
material-change rules, baseline behaviour, synthetic scenarios, falsification
and stopping conditions, unresolved decisions, and the approval boundary.

Appended to `RESEARCH_LOG.md` that R1 is framed but not run. Added only the
accepted meta-decision in `DECISIONS.md` that all R1 schema choices remain
provisional. No application code, tests, fixtures, databases, dependencies,
adapters, network calls, or notifications were added.

### Verification

- `.venv/bin/python -m pytest` — 3 passed.
- `.venv/bin/ruff format --check .` — 14 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 1 source file.
- `git diff --check` — passed.

### Decisions

The R1 framing is not a research result and does not authorize implementation.
All R1 schema choices remain provisional. Approval is required before running
or implementing the experiment.

### Gotchas

The word “schema” can make a proposed research model look like an accepted
database or product contract. It was therefore kept explicitly in Markdown,
with no code, fixtures, database, or persistence layer. This is contained by
marking every R1 design choice provisional and requiring approval before a
run; the risk remains that a future reader may still confuse framing with
validation.

#### Consistency review and provisional resolutions

- **Observed:** The first R1 framing lacked explicit adapter and schema-version
  comparability fields, did not fully separate diagnostic metadata, used a
  broad ordering statement, and left partial unverifiable candidates and
  aggregate outcomes under-specified.
- **Why surprising or dangerous:** Those gaps could allow two different source
  or schema contracts to compare, turn a status diagnostic into an exposure
  bark, silently reorder material lists, or let partial candidates support a
  false baseline or disappearance claim.
- **Diagnosis:** A read-only twelve-point review compared the R1 terminology,
  examples, rules, scenarios, and records against the required invariants.
- **Resolution or containment:** The provisional R1 framing now requires exact
  subject/source/scope/adapter/adapter-version/schema/normalization agreement,
  excludes diagnostic metadata from observation fingerprints, declares list
  semantics per field, retains only bounded diagnostics for failed or
  unverifiable checks, and defines aggregate `completed`, `incomplete`,
  `failed`, and invalid `empty_scope` outcomes. Status guards are explicitly
  non-exposure events.
- **Open risk:** R1 has not run; the proposed rules may still fail against
  synthetic scenarios and remain unaccepted design choices.

### Repository state

Before this entry: branch `main` at `0bd3f08`, clean after the Base Zero
documentation commit. This R1 framing is deliberately unstaged and uncommitted
pending review and explicit approval.

### Next question

Will the proposed deterministic schema survive the required synthetic
scenarios without false bark events or hidden non-comparability?

## 2026-08-18 — Clarify R1 guard-event semantics

### Objective

Resolve the material R1 output-semantics ambiguity found by the
pre-implementation consistency review before writing application code.

### Changes

Updated `RESEARCH_001_BARK_SCHEMA.md`, `DECISIONS.md`, and `RESEARCH_LOG.md` to
record that implementation correctly stopped, and to define the provisional
separation between comparison results, reasons, exposure events, and guard
events. A failed current source check now means `not_comparable` plus a
`guarding_failed` event; an unverifiable current source check means
`not_comparable` plus a `guarding_unverifiable` event. Guards can exist without
a prior successful baseline and never become exposure events. Empty scope is
rejected during plan construction or validation with no result or event.

No application source, tests, fixtures, persistence, dependency, adapter,
network call, notification, or R1 run was added in this clarification step.

### Verification

The documentation-only diff was reviewed for the clarified result/event
separation. `git diff --check` — passed. No R1 verification or experiment run
has occurred.

### Decisions

The guard semantics and empty-scope behaviour are provisional R1 resolutions,
not accepted product or schema decisions. The prior stop was correct because
choosing an output shape merely to satisfy a test would have violated the
experimental specification.

### Gotchas

#### Material guard-output ambiguity

- **Observed:** The R1 framing defined `failed` and `unverifiable` as source
  statuses and `not_comparable` as the comparison result, but did not define
  the required `guarding_failed` and `guarding_unverifiable` names or whether
  they were result kinds or separate events.
- **Why surprising or dangerous:** An implementation could collapse a guard
  into an exposure event, or make failure appear equivalent to disappearance,
  while still passing a superficially plausible transition test.
- **Diagnosis:** Compare the R1 terminology, proposed status-guard schema, and
  required failure scenarios before creating records or comparator code.
- **Resolution or containment:** Stop before implementation, record the stop,
  and clarify that guards are separate events alongside `not_comparable`, can
  exist without a baseline, and are never exposure events.
- **Open risk:** R1 remains unrun; the clarified provisional model may still
  expose further ambiguity during implementation.

### Repository state

Before this clarification commit: branch `main` at `610e17e`; the four
documentation files in this step are modified and unstaged. No implementation
files are present. The clarification is intended to be committed separately
as `docs: clarify R1 guard event semantics`.

### Next question

Can the clarified deterministic in-memory model pass the required synthetic
transitions without false exposure barks or hidden non-comparability?

## 2026-08-18 — Execute R1 truthful bark experiment

### Objective

Run the approved, clarified R1 experiment offline to test whether deterministic
synthetic observations can yield truthful comparison and bark outcomes without
turning failure, uncertainty, incompatible scope, or diagnostic variation into
exposure change.

### Changes

**Directly verified:** Added the `personal_watchdog` package containing frozen
in-memory records for source identities, non-empty scan plans, diagnostic
metadata, observations, terminal source checks, aggregate scan attempts,
comparison results, exposure events, guarding events, and reports. Added
contract-declared material fields and set-like fields, deterministic
canonicalization, construction-time rejection of invalid scope/status
combinations, and the pure `compare_scans` function.

**Directly verified:** Added synthetic-only fixtures and 26 R1 tests in
`tests/test_r1.py`; the existing three Milestone 0 policy tests remain
unchanged. No CLI, persistence, database, dependency, adapter, network call,
notification, evidence capture, hashing, encryption, background service, GUI,
report, risk score, or severity score was added.

### Verification

**Directly verified:**

- `.venv/bin/python -m pytest` — 29 passed.
- `.venv/bin/ruff format --check .` — 19 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 6 source files.
- `git diff --check` — passed.

### Decisions

Keep the result bounded to the synthetic in-memory model. Preserve the
comparison/result/reason, exposure-event, and guarding-event separation. Keep
the R1 schema and bark semantics provisional; the experiment does not justify
claims about live source truth, coverage, identity ownership, risk, danger, or
notification usefulness.

### Gotchas

#### 1. The provisional source contract needed explicit material fields

- **Observed:** The first implementation declared which fields were set-like
  but did not yet declare the complete synthetic material-field set, so an
  unknown material field could have been accepted.
- **Why surprising or dangerous:** An undeclared field could silently become
  material and make the experiment appear more deterministic than the source
  contract justified.
- **Diagnosis:** Review the R1 rule that the source contract declares material
  fields and add a test for an undeclared field.
- **Resolution or containment:** Added `material_fields` to the immutable
  source identity, rejected unknown fields during observation construction,
  and added a regression test. The fixture contract explicitly declares its
  three synthetic material fields.
- **Open risk:** Other source kinds would need their own separately declared
  contract; no such source is implemented here.

#### 2. Adjacent duplicate checks are not strict zip pairs

- **Observed:** A first lint cleanup changed adjacent-value checks to
  `zip(..., strict=True)`, which raised during fixture import because the
  compared sequences intentionally have lengths differing by one.
- **Why surprising or dangerous:** The error occurred before tests ran and
  could be mistaken for a source or fixture failure rather than a local
  validation bug.
- **Diagnosis:** The collection traceback pointed to duplicate detection in
  `_sorted_unique` during synthetic source construction.
- **Resolution or containment:** Use explicit `strict=False` for adjacent
  pair checks, rerun the full suite, and retain tests for set uniqueness.
- **Open risk:** None observed for the covered canonical value types; future
  canonical structures still require tests.

#### 3. R1 output names remain intentionally narrow

- **Observed:** The specification distinguishes `not_comparable` comparison
  results from `guarding_failed` and `guarding_unverifiable` events.
- **Why surprising or dangerous:** Treating the guard names as comparison
  kinds would collapse uncertainty into the wrong result model.
- **Diagnosis:** Compare the clarified R1 document with the separate immutable
  result/event records and their tests.
- **Resolution or containment:** Keep guards in their own collection and derive
  exposure events only from `new`, `changed`, or `disappeared` results.
- **Open risk:** The provisional names and event policy remain subject to a
  later accepted design decision.

### Repository state

Directly verified before this implementation commit: branch `main` at
`4b0ba31` (`docs: clarify R1 guard event semantics`). The implementation,
synthetic fixtures, tests, and these post-experiment history updates are
intended for the separate commit `test: execute R1 truthful bark experiment`.
Ignored Python cache files may exist from test execution; no generated cache
file is tracked.

### Next question

What, if anything, should be separately approved after reviewing this bounded
offline result?

## 2026-08-18 — Frame Research Experiment R2 adapter boundary

### Objective

Frame an offline adapter-boundary experiment that can test untrusted response
normalization without implementing a real adapter or changing R1 comparison and
event semantics.

### Changes

Created and then concretely corrected `RESEARCH_002_ADAPTER_BOUNDARY.md` with a
deliberately invented, versioned response envelope; a bytes-first parser
boundary; fixed 65,536-byte, 100-result, depth-8, string, collection, and
diagnostic limits; strict duplicate-key and non-standard-constant rejection;
trusted-context rules; exact allowed-key sets; result validation;
normalization mappings for completed, completed-empty, failed, unverifiable,
malformed, incomplete, and incompatible responses; exact-versus-conflicting
duplicate handling; boundary ownership; synthetic scenarios; falsification
conditions; and the approval boundary.

Updated `RESEARCH_LOG.md` to record the concrete R2 framing and that R2 is
framed but not run. No application source, parser, adapter, fixture, test,
dependency, network call, persistence, comparison, bark, notification,
evidence archive, or real identifier was added.

### Verification

The corrected documentation diff is reviewed for separation from R1, concrete
hostile-input rules, and the absence of implementation authorization.

- `.venv/bin/python -m pytest` — 29 passed.
- `.venv/bin/ruff format --check .` — 20 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 6 source files.
- `git diff --check` — passed.
- No R2 tests or adapter checks have run.

### Decisions

All R2 envelope and normalization choices remain provisional. Keep response
contract validation and source-check construction at the adapter boundary, and
keep comparison and derived-event ownership entirely in R1.

### Gotchas

#### 1. The response example does not contain all R1 identity fields

- **Observed:** The required envelope contains `contract_version`,
  `source_id`, `outcome`, and `results`, while R1 comparability also requires
  scope, adapter, schema, and normalization identity.
- **Why surprising or dangerous:** Letting untrusted response data fill or
  replace those fields could make an incompatible response appear comparable.
- **Diagnosis:** Compare the R2 envelope boundary with `SourceIdentity` and
  R1's exact comparability rules.
- **Resolution or containment:** Treat the R1 identity as trusted local
  context; use `contract_version` only for response-envelope validation and
  never as an identity substitute.
- **Open risk:** A later adapter implementation must define how that trusted
  context is constructed without introducing an unapproved configuration or
  live-service assumption.

#### 2. Malformed and incompatible are normalization classifications

- **Observed:** R1 has `completed`, `failed`, and `unverifiable` source
  statuses, but the R2 question also requires malformed, incomplete, and
  incompatible distinctions.
- **Why surprising or dangerous:** Adding those labels as new R1 statuses
  would silently change the existing comparator contract.
- **Diagnosis:** Map the additional categories to bounded reasons on an R1
  `unverifiable` source check while retaining the category for diagnostics.
- **Resolution or containment:** Keep the extra classifications at the R2
  boundary and require zero accepted observations for them.
- **Open risk:** The concrete error/result mapping is now provisionally framed;
  a separately approved implementation must still realize and test it without
  weakening the boundary.

#### 3. The initial correction attempt repeated review without changing files

- **Observed:** An initial correction attempt accidentally repeated the
  read-only consistency review and made no changes.
- **Why surprising or dangerous:** The known omissions—bytes input, concrete
  limits, strict JSON handling, and complete outcome mappings—would have
  remained in the framing while appearing to have been addressed.
- **Diagnosis:** Compare the first attempted handoff with the resulting
  worktree status and inspect the revised R2 document for the concrete rules.
- **Resolution or containment:** Apply the authorized documentation correction
  in this step, inspect the diff, and require the full 28-point review before
  staging or committing.
- **Open risk:** R2 remains framed and unrun; implementation must preserve the
  corrected boundary and R1 ownership.

### Repository state

Directly verified before this framing step: branch `main` at `62e2d94`
(`test: execute R1 truthful bark experiment`), clean. The new R2 framing and
research-history entry are deliberately uncommitted pending review and
approval.

### Next question

Can the proposed synthetic response boundary normalize untrusted outcomes into
R1 source checks without accepting partial candidates or changing R1 meaning?

## 2026-08-18 — Execute R2 adapter boundary experiment

### Objective

Execute the approved Phase 2 R2 experiment against the committed provisional
adapter-boundary specification without changing R1 or introducing a live
integration.

### Changes

**Directly verified:** Added `personal_watchdog/r2_adapter.py` with a pure,
standard-library-only bytes normalizer and immutable trusted-context wrapper.
It enforces the committed byte, collection, nesting, string, integer, and
diagnostic limits; performs duplicate-aware strict JSON parsing; rejects
non-standard constants; validates exact key sets and material types; preserves
trusted R1 identity; maps all response outcomes to R1 source checks; discards
partial candidates; and handles exact versus conflicting duplicate findings.

**Directly verified:** Added `tests/fixtures_r2.py` and
`tests/test_r2_adapter.py` with synthetic-only payloads covering parser attacks,
all concrete boundaries, outcome mappings, duplicate handling, deterministic
ordering, diagnostic exclusion, trusted identity ownership, subject isolation,
and R1 comparator transitions. The existing R1 implementation and tests were
not modified.

**Directly verified:** `RESEARCH_LOG.md` records observed R2 results. No new
project-level decision was supported, so `DECISIONS.md` was intentionally left
unchanged. No R3 work was started.

### Verification

**Directly verified:**

- `.venv/bin/python -m pytest` — 101 passed.
- `.venv/bin/ruff format --check .` — all files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.

### Decisions

Keep the R2 response envelope, limits, reason codes, trusted-context boundary,
and outcome mappings provisional. Preserve R1 as the sole owner of comparison,
exposure, and guarding semantics. The passing result is limited to the
invented offline format and does not authorize a live adapter or R3.

### Gotchas

#### 1. The initial correction attempt was a no-op

- **Observed:** An initial correction attempt accidentally repeated the
  read-only consistency review and made no changes. This was recorded during
  the R2 framing correction and remained relevant to this execution handoff.
- **Why surprising or dangerous:** The implementation could have been started
  from an apparently reviewed but still incomplete framing.
- **Diagnosis:** Compare the committed R2 specification with the implementation
  and test matrix, then inspect the resulting diff rather than relying on the
  earlier review report.
- **Resolution or containment:** Implemented the complete committed boundary,
  inspected the code and tests, and reran the full hostile-input and R1
  integration suite.
- **Open risk:** The synthetic choices remain provisional and have no live
  protocol evidence.

#### 2. R2 output must remain narrower than R1 comparison output

- **Observed:** The required integration scenarios could be satisfied by
  accidentally recreating comparison or event semantics inside the adapter.
- **Why surprising or dangerous:** That would create two owners for absence,
  exposure, and guarding meaning.
- **Diagnosis:** Review adapter return types and require end-to-end tests to
  call `compare_scans`.
- **Resolution or containment:** The adapter returns only `SourceCheck`; all
  transition assertions use the existing R1 comparator.
- **Open risk:** A future integration layer could still expand scope without a
  separate approval.

### Repository state

Directly verified before this implementation commit: branch `main` at
`5aa2f61` (`docs: frame R2 adapter boundary`). The R2 implementation, synthetic
fixtures, tests, and the two updated history files are intended for the
separate commit `test: execute R2 adapter boundary experiment`;
`DECISIONS.md` and the committed R2 specification remain unchanged.

### Next question

What, if anything, should be separately approved after reviewing this bounded
R2 result? Stop before R3.

## 2026-09-06 — Frame R2.5 visible offline simulator

### Objective

Frame a human-readable deterministic offline scenario runner around the
existing R1/R2 implementation without implementing the runner or introducing
new comparison semantics.

### Changes

**Directly verified:** Added `RESEARCH_002_5_VISIBLE_OFFLINE_SIMULATOR.md`.
The framing defines the scenario schema, trusted and untrusted boundaries,
chronological source execution, in-memory prior scans, human and canonical JSON
output, expected-versus-actual comparison, exit codes, failure visibility,
scenario-level pass criteria, and exact proposed Phase 2 files.

**Documented in the framing:** The ten curated scenarios cover baseline silence, new
exposure, material change, genuine completed-empty disappearance, explicit
failure, unverifiable bytes, one failed source beside a valid change, trusted
adapter/schema incompatibility, a hostile apparent clean response, and
simultaneous findings.

**Directly verified:** The framing leaves repeated-failure suppression,
recovery, trivial-change suppression, simultaneous grouping, baseline overload,
minimum actionable information, and disappearance confirmation for later
experiments. `DECISIONS.md` was not changed.

### Verification

- `.venv/bin/python -m pytest` — 101 passed.
- The R2.5 document is framing only; no implementation or scenario file was
  added.
- Ruff, mypy, `git diff --check`, and complete diff inspection are required
  before handoff.

### Decisions

No project-level decision was established. Preserve R1 as the sole owner of
comparison and derived-event semantics, and preserve R2 as the sole owner of
untrusted response normalization.

### Gotchas

#### 1. Framing-document status versus execution history

- **Observed:** R1/R2 design documents say they are provisional framing
  artifacts, while the append-only records document their later synthetic
  implementation and tests.
- **Why surprising or dangerous:** Treating the design documents as current
  execution claims, or treating the execution records as settled product
  policy, would create false certainty.
- **Diagnosis:** Compare the document headers and ownership boundaries with
  the research/build records and the committed implementation.
- **Resolution or containment:** R2.5 states that distinction explicitly and
  keeps its own scenario contract provisional.
- **Open risk:** A later implementation could still accidentally add policy
  semantics unless the proposed boundary is tested adversarially.

#### 2. Editable-install packaging discovery

- **Observed:** `pip install -e '.[dev]'` failed because setuptools found both
  `data` and `personal_watchdog` as top-level packages.
- **Why surprising or dangerous:** Fixing packaging during a framing-only
  experiment would expand scope and obscure whether the simulator itself was
  tested.
- **Diagnosis:** Direct installation of pytest, Ruff, and mypy succeeded, and
  the existing virtual environment ran the baseline suite.
- **Resolution or containment:** Record the gotcha and defer packaging to a
  separate approved task.
- **Open risk:** Future packaging changes need their own review and checks.

#### 3. Raw hostile bytes must remain visible without becoming evidence

- **Observed:** A visible simulator needs invalid bytes and malformed text to
  demonstrate failure handling, but raw response retention is outside scope.
- **Why surprising or dangerous:** Echoing raw bytes or parser exceptions could
  violate privacy and make a failure look like a clean result.
- **Diagnosis:** R2 already exposes bounded reason codes and returns an R1
  `SourceCheck` without raw payload retention.
- **Resolution or containment:** The framing reports input form, bounded
  reasons, status, comparison, and guards, but not raw bytes or exception text.
- **Open risk:** Phase 2 output tests must enforce this omission.

### Repository state

Before this framing update: branch `experiment/r2-5-visible-offline-simulator`
at the supplied R2-complete commit `4f16048`, with the framing document as the
only new R2.5 artifact. This step is deliberately unstaged and uncommitted
pending adversarial review.

### Next question

Can Phase 2 implement this visible contract while remaining a thin orchestrator
and preserving all existing R1/R2 semantics?

## 2026-09-06 — Verify R2.5 framing handoff

### Scope

Verify the documentation-only R2.5 framing after reconciling its scenario-file
contract with the existing R1/R2 APIs. No implementation, fixture, dependency,
network call, persistence, or external archive change was authorized.

### Verification

- `.venv/bin/python -m pytest` — 101 passed.
- `.venv/bin/ruff format --check .` — 24 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.
- Observation from complete diff inspection: only the four requested
  documentation files are changed or added, and `DECISIONS.md` is unchanged.

### Gotchas

- None observed beyond the editable-install packaging discovery failure and
  the provisional-design-versus-execution-history distinction already recorded
  in the preceding R2.5 framing entry.

### Repository state

The worktree remains deliberately unstaged and uncommitted for adversarial
review on `experiment/r2-5-visible-offline-simulator`.

### Next question

Can the proposed Phase 2 implementation preserve the exact R1/R2 ownership
boundary while making all ten scenarios and later bark-policy experiments
visible?

## 2026-09-08 — Revise R2.5 framing contract

### Scope

Revise the R2.5 framing only. Reconcile the scenario schema, output grammar,
deterministic IDs, validation bounds, derived exposure-silence rule, Scenario 7
local construction error, and Scenario 8 naming. Do not implement or execute a
simulator or begin Phase 2.

### Documented reconciliation

- R2 expectations now belong to individual checks; the one expected R1
  `ComparisonReport` projection belongs to each scan.
- `scan_id` and `source_check_id` construction is assigned to the runner;
  `comparison_id` and `guard_id` formulas are repository observations owned by
  R1 and are not runner validation logic.
- Exposure silence is derived only from actual R1 exposure events; guarding
  events remain separate.
- Scenario 7 uses the local construction-error path, while Scenario 5 retains
  the explicit R2 failed response. Scenario 8 is explicitly an R1 trusted
  identity/version incompatibility case.
- Fixed outer byte, depth, collection, string, and expected-record bounds and
  exact integer/type/NFC/order/material-policy validation are documented.
- Human and machine output key sets, ordering, stdout/stderr behavior, and
  invalid-scenario diagnostics are frozen provisionally.

### Status

These are documented and reconciled proposed behaviors only. No simulator
behavior was executed or behaviorally verified. The existing repository checks
remain separate from any future Phase 2 scenario execution.

### Gotchas

- None observed beyond the packaging discovery failure and the
  design-artifact-versus-execution-history distinction already recorded above.

### Decision boundary

Stop for adversarial review. Do not create Phase 2 files, stage, commit, push,
or modify R1/R2.

## 2026-09-08 — Verify R2.5 framing revision

### Verification

- `.venv/bin/python -m pytest` — 101 passed in the existing repository suite.
- `.venv/bin/ruff format --check .` — 24 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.
- Observation from complete diff inspection: only the R2.5 framing document
  and the three already changed logs are modified or untracked; no code,
  tests, fixtures, dependencies, `DECISIONS.md`, or external repository files
  changed.

### Status

The proposed simulator remains unimplemented and unexecuted. These checks do
not behaviorally verify the proposed scenario contract.

### Gotchas

- None observed beyond the previously recorded editable-install packaging
  discovery failure.

### Decision boundary

Stop for adversarial review without staging, committing, pushing, or beginning
Phase 2.

## 2026-09-08 — Final R2.5 framing verification observation

### Verification

- `.venv/bin/python -m pytest` — 101 passed in the existing repository suite.
- `.venv/bin/ruff format --check .` — 24 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.
- Observation from complete diff inspection: the worktree contains only the
  requested R2.5 framing document and the three already changed logs.

### Status and Gotchas

The simulator and proposed scenarios remain unimplemented, unexecuted, and
behaviorally unverified. No new gotcha was observed; the packaging discovery
failure remains separate work.

### Decision boundary

Stop for adversarial review. Do not stage, commit, push, or begin Phase 2.

## 2026-09-08 — Final R2.5 ownership-boundary correction

### Documented reconciliation

- The runner constructs only `scan_id` and `source_check_id`.
- R1 alone constructs `comparison_id` and `guard_id`; their formulas remain
  author guidance only.
- Expected IDs are ordinary well-typed oracle strings compared literally with
  R1 output. A wrong expected ID is an expectation mismatch with exit code `1`,
  not an invalid scenario.
- Each scan must resolve its `source_ref` values to unique `source_id` values;
  duplicate resolution is `reference_error` with exit code `2`. The same
  `source_id` may use different identities in different scans.
- The one-file runner validates `scenario_id` syntax only; the Phase 2 test
  suite must enforce uniqueness across the ten curated fixtures.

### Status and Gotchas

This is a framing correction only. Proposed simulator behavior remains
unexecuted and behaviorally unverified. No new gotcha was observed.

### Decision boundary

Stop for adversarial review without implementing, staging, committing, pushing,
or beginning Phase 2.

## 2026-09-08 — Verify final R2.5 boundary correction

### Verification observation

- The established repository checks completed successfully: 101 pytest tests
  passed; Ruff format reported 24 files already formatted; Ruff lint passed;
  mypy found no issues in 9 source files; and `git diff --check` passed.
- Complete diff inspection observed only the framing document and the three
  already changed logs.

### Status and Gotchas

The proposed simulator remains unimplemented, unexecuted, and behaviorally
unverified. No new gotcha was observed.

### Decision boundary

Stop for adversarial review without staging, committing, pushing, or beginning
Phase 2.

## 2026-09-08 — Implement R2.5 visible offline simulator

### Implementation and verification

- Added the bounded standard-library-only `offline_simulator` CLI, its ten
  frozen synthetic scenarios, and focused contract tests.
- Executed every curated scenario in human and JSON modes; all twenty runs
  returned exit code `0`.
- Exercised a controlled expected-ID mismatch through the CLI with exit code
  `1`, and invalid scenario cases through the CLI with exit code `2`.
- Full pytest suite: 129 passed.
- Ruff format check: 27 files already formatted.
- Ruff lint: all checks passed.
- mypy: success, no issues found in 12 source files.
- `git diff --check`: passed.

### Gotchas

- The previously observed editable-install packaging failure remains separate
  work: setuptools discovers both `data` and `personal_watchdog` as top-level
  packages. Verification used the already working direct tool installation.
- R1 emits only the source check’s reason code on a non-comparable failed or
  unverifiable comparison; the scenario oracles were aligned to that existing
  behavior rather than adding a runner reason.

### Status

These are deterministic synthetic offline executions and tests. They do not
verify live-source truth, archive behavior, notifications, or product
usefulness. Stop for adversarial implementation review without staging,
committing, pushing, or beginning R3.

## 2026-09-08 — R2.5 adversarial implementation corrections

### Implementation and verification

- Replaced whole-file scenario reads with a binary read capped at
  `MAX_SCENARIO_BYTES + 1`.
- Corrected mismatch JSON Pointer array positions and made differing object
  fields sort by pointer component after preserving scan/source/R1 ordering.
- Corrected local construction marker diagnostics and expanded contract tests
  for output goldens, canonical JSON, all bounds, validation, and fixture
  hygiene.
- All ten scenarios passed in human and JSON modes with exit code `0`.
- Controlled expectation mismatch: exit `1`; controlled invalid/reference
  cases: exit `2`.
- Full pytest suite: 147 passed.
- Ruff format check: 27 files already formatted; Ruff lint passed.
- mypy: success, no issues found in 12 source files.
- `git diff --check`: passed.

### Gotchas

- The editable-install packaging discovery failure remains separate work.
- No valid scenario meaning or R1/R2 behavior was changed; this pass tightened
  runner safety, diagnostics, deterministic reporting, and test coverage.

### Status

Verification is limited to deterministic synthetic offline scenarios and local
tests. It does not establish live-source truth or product usefulness. Stop for
adversarial review without staging, committing, pushing, modifying R1/R2, or
beginning R3.

## 2026-09-08 — Frame R3 Phase 1 XposedOrNot contract research

### Objective

Research the documented official XposedOrNot contract and frame a conservative
synthetic adapter experiment without implementing an adapter or making a live
request.

### Changes

**Directly verified:** Added `RESEARCH_003_XPOSEDORNOT_CONTRACT.md`. It records
official endpoint and request facts, authentication and quota behavior, HTTP
status classes, documented response shapes, empty-result distinctions,
official-source conflicts, missing protocol guarantees, threat/ambiguity
handling, R2 mapping, trusted-context ownership, a provisional finding model,
later file boundaries, a frozen synthetic test matrix, and conclusion
criteria.

**Directly verified:** Appended this research result to `RESEARCH_LOG.md` and
preserved `DECISIONS.md` unchanged because the work does not establish a
project-level decision.

**Boundary:** No XposedOrNot endpoint was called. No identifier, credential,
password, HTTP client, dependency, adapter, persistence, evidence archive,
scheduler, notification, R1/R2/R2.5 change, or external archive change was
made.

### Gotchas

- The official sources do not form one unambiguous wire contract: the free
  email no-result status is unspecified while 404 is documented as no data or
  input error; the website and Python SDK name different detail parameters;
  and the website and SDKs publish different request-spacing numbers.
- No official maximum response size, pagination, duplicate policy, ordering
  guarantee, exact content type/charset, or freshness/completeness marker was
  found. These omissions are unknowns, not permission to accept a clean empty
  result.
- The existing R2 `completed-empty` meaning is narrower than a parseable HTTP
  200 body. Only the explicitly documented analytics all-null 200 shape is
  proposed as a genuine empty fixture; free email `Error: Not found` remains
  conservative failure or unverifiable.

### Status

R3 Phase 1 is documentation research and experimental framing only. The later
synthetic adapter experiment remains approval-gated. Stop for adversarial
review without staging, committing, pushing, or implementing the adapter.

## 2026-09-08 — Verify R3 Phase 1 XposedOrNot contract research

### Verification

- Full pytest suite: 147 passed.
- Ruff format check: 28 files already formatted.
- Ruff lint: all checks passed.
- mypy: success, no issues found in 12 source files.
- `git diff --check`: passed.
- Complete diff inspection found only the R3 research document and the three
  permitted append-only history/log files changed or added.

The checks validate the repository and existing synthetic behavior only. No
XposedOrNot endpoint was called, and no live protocol or source truth was
verified.

### Gotchas

- None observed beyond the official documentation conflicts and missing
  protocol guarantees already recorded in the preceding R3 entry.

### Status

R3 Phase 1 remains documentation-only and stopped for adversarial review.
Nothing was staged, committed, pushed, or implemented.

## 2026-09-08 — Correct R3 Phase 1 XposedOrNot framing

### Objective

Revise only the R3 documentation framing after examining the official Swagger
UI and OpenAPI JSON artifacts. Preserve the no-adapter, no-live-request
boundary.

### Changes

- Recorded `/docs` and `/openapi.json` provenance, OpenAPI/API versions, the
  facts they resolve, and the gaps or conflicts they leave unresolved.
- Pinned every official GitHub source used by R3 to a full commit SHA and
  immutable file permalink.
- Separated free check-email and breach-analytics into distinct source
  identities, scopes, schema versions, and matrices; selected free check-email
  as the sole first synthetic experiment.
- Named and structurally defined `XON_ANALYTICS_HTTP_200_NO_MATCH_V1`,
  preserving its non-null empty summary objects.
- Defined the synthetic transport-attempt envelope and its transport → XON →
  R2 → R1 ownership boundary without adding an HTTP client.
- Corrected exact-duplicate handling to use existing R2 deterministic
  deduplication and conflict rejection.
- Corrected the record-file count to four tracked files:
  `BUILD_HISTORY.md`, `PROGRESS_LOG.md`, `REFERENCES.md`, and
  `RESEARCH_LOG.md`.

### Boundary

No functional lookup endpoint, identifier, credential, password, adapter,
HTTP client, dependency, persistence, evidence archive, scheduler,
notification, R1/R2/R2.5 code, staging, commit, push, or external archive
change was made.

### Gotchas

- OpenAPI version `2.0.0` is specification metadata, not proof of data
  freshness or a closed response contract.
- OpenAPI does not define the analytics no-match predicate and conflicts with
  website examples on several nullable/type details.
- The selected check-email family has no documented genuine empty-success
  response; the analytics sentinel is deliberately a separate deferred test.

### Status

Documentation correction appended. Stop for verification and adversarial
review; the synthetic implementation remains approval-gated.

## 2026-09-08 — Verify corrected R3 Phase 1 framing

### Verification

Exact commands and outputs:

- `.venv/bin/python -m pytest` — `147 passed in 6.01s`.
- `.venv/bin/ruff format --check .` — `28 files already formatted`.
- `.venv/bin/ruff check .` — `All checks passed!`.
- `.venv/bin/mypy .` — `Success: no issues found in 12 source files`.
- `git diff --check` — no output; exit 0.

The Ruff count increased from the R2.5 record’s 27 to 28 because Ruff’s
configured include set includes Markdown and the R3 research document is now
included. The R2.5 commit and current worktree both have 12 Python files, so
there was no Python source change; mypy remains 12.

### Gotchas

- OpenAPI remains an open, partially conflicting specification; it does not
  establish a live response guarantee.
- The first synthetic experiment remains check-email only. Analytics remains a
  separate deferred family.

### Status

All requested local verification passed. Stop for adversarial review without
staging, committing, pushing, implementing, or making a live request.

## 2026-09-08 — Final R3 Phase 1 framing verification

### Verification

The complete diff and status inspection preceded this final sequence. Exact
commands and outputs were:

- `.venv/bin/python -m pytest` — `147 passed in 6.01s`.
- `.venv/bin/ruff format --check .` — `28 files already formatted`.
- `.venv/bin/ruff check .` — `All checks passed!`.
- `.venv/bin/mypy .` — `Success: no issues found in 12 source files`.
- `git diff --check` — no output; exit 0.

The earlier 5.98-second pytest report and this 6.01-second run are separate
successful executions of the same 147-test suite. The timing difference is
runtime variance; no Python source or behavior changed.

### Gotchas

- None beyond the documented official-source conflicts and unspecified live
  protocol guarantees.

### Status

Final R3 Phase 1 framing is complete and stopped for adversarial review.

## 2026-09-09 — Final R3 Phase 1 contract-gap correction

### Objective

Correct the remaining R3 framing gaps without implementing Phase 2 or changing
R1, R2, R2.5, or the offline simulator.

### Changes

- Removed the impossible conflicting-duplicate fixture from the selected
  check-email matrix. Exact duplicate breach names still exercise existing R2
  deterministic deduplication; conflicting duplicates remain generic R2 test
  protection only.
- Reframed analytics as deferred sentinel-and-rejection research. Its positive
  success schema is not frozen and requires future framing before any
  implementation.
- Defined exact content-type derivation, optional whitespace handling,
  ASCII-case comparison, parameter rejection, malformed/non-ASCII handling,
  duplicate-header rejection, and the retained-header byte formula.
- Froze compact UTF-8 normalized-R2 serialization and the pre-R2 byte-limit
  guard while preserving the 13,918-byte XON and 25,910-byte normalized-R2
  calculations.
- Added before-status and after-status transport failure phases so a post-
  status read failure or timeout preserves the known HTTP status and remains
  incomplete and non-comparable.
- Expanded every selected check-email matrix row with transport, XON, and R2
  outcomes or visible construction rejection.

### Boundary

No functional endpoint, identifier, credential, adapter, HTTP client,
dependency, persistence, scheduler, notification, evidence archive, staging,
commit, push, or unrelated file change was made.

### Gotchas

- A conflicting duplicate cannot be generated by the selected XON mapping
  because the exact breach name determines all R2 identity/material fields.
- Analytics positive-success normalization remains intentionally undefined and
  implementation-blocked.
- Harness construction errors remain visible construction failures; only valid
  transport attempts with untrusted malformed metadata receive conservative
  source classifications.

### Status

Documentation-only correction appended. Stop after verification for final
adversarial review.

## 2026-09-09 — Verify final R3 Phase 1 contract-gap correction

### Verification

The complete requested diff inspection and status review preceded this final
verification sequence. Exact commands and outputs were:

- `./.venv/bin/python -m pytest` — `147 passed in 6.08s`.
- `./.venv/bin/ruff format --check .` — `28 files already formatted`.
- `./.venv/bin/ruff check .` — `All checks passed!`.
- `./.venv/bin/mypy .` — `Success: no issues found in 12 source files`.
- `git diff --check` — no output; exit 0.

### Gotchas

- No new contradiction was found. The selected XON matrix excludes
  conflicting duplicates because that state is not constructible under its
  deterministic mapping; generic R2 protection remains separate.
- Analytics positive-success normalization remains future framing work.

### Status

Documentation-only correction verified. Stop for final adversarial review
without implementation, staging, commit, or push.

## 2026-09-09 — Implement R3 Phase 2 synthetic XON check-email experiment

### Objective

Implement only the frozen deterministic check-email experiment from R3 Phase 1
after confirming the exact Phase 1 HEAD, upstream branch, and clean starting
tree.

### Changes

- Added the standard-library-only in-memory `TransportAttempt` and bounded raw
  `Header` contract, including trusted-context validation, exact header
  accounting, content-type derivation, and distinct transport failure/body
  states.
- Added check-email-only XON normalization with strict UTF-8/JSON validation,
  exact schema and echo checks, bounded NFC strings, no completed-empty path,
  deterministic breach candidates, and existing R2 deduplication.
- Added deterministic compact ASCII-escaped R2 serialization with the final
  byte guard before calling the existing R2 adapter.
- Added synthetic fixtures and tests for every constructible selected matrix
  row, R1 guarding/disappearance protection, size bounds, and absence of
  network-capable imports.

### Boundary

No functional request, identifier submission, credential, HTTP client,
analytics implementation, persistence, scheduler, notification, archive,
dependency, R1/R2/R2.5 modification, staging, commit, or push was made.
Verification proves only deterministic synthetic behavior, not live
XposedOrNot compatibility, completeness, freshness, coverage, usefulness, or
safety.

### Gotchas

- The selected check-email contract has no completed-empty result; zero valid
  findings remain unverifiable.
- Post-status read failures preserve the received HTTP status but become
  incomplete and never parse a retained prefix.
- Exact duplicate breach names are intentionally delegated to generic R2
  deterministic deduplication; conflicting XON duplicates are not constructible.

### Status

Implementation is complete pending the final full verification sequence and
adversarial implementation review.

## 2026-09-09 — Verify R3 Phase 2 synthetic experiment

### Verification

The complete implementation diff and status inspection preceded this final
verification sequence. Exact commands and outputs were:

- `./.venv/bin/python -m pytest` — `199 passed in 6.87s`.
- `./.venv/bin/ruff format --check .` — `31 files already formatted`.
- `./.venv/bin/ruff check .` — `All checks passed!`.
- `./.venv/bin/mypy .` — `Success: no issues found in 15 source files`.
- `git diff --check` — no output; exit 0.

The R2.5 checkpoint contained 147 tests. The final count is 199 because this
phase adds 52 synthetic XON adapter tests; no existing R1, R2, R2.5, or offline
simulator Python file was changed.

### Gotchas

- Verification covers only deterministic synthetic behavior. It does not prove
  live XposedOrNot compatibility, completeness, freshness, coverage,
  usefulness, or safety.
- No network-capable import or call was added; no functional endpoint was used.

### Status

R3 Phase 2 synthetic implementation is verified and stopped for adversarial
implementation review without staging, commit, push, merge, or live work.

## 2026-09-09 — Final transport invariant correction and verification

### Correction

Pre-status failures now reject retained headers as contradictory local
envelopes: without an HTTP status, no response headers can be present. The
selected outcome mappings and all other transport states are unchanged.

### Verification

After the correction, the exact final sequence passed:

- `./.venv/bin/python -m pytest` — `199 passed in 6.44s`.
- `./.venv/bin/ruff format --check .` — `31 files already formatted`.
- `./.venv/bin/ruff check .` — `All checks passed!`.
- `./.venv/bin/mypy .` — `Success: no issues found in 15 source files`.
- `git diff --check` — no output; exit 0.

### Gotchas

- This correction supersedes the earlier 6.87-second implementation
  verification as the final code verification; both were separate successful
  runs.

### Status

Final synthetic implementation verification is complete; stop for adversarial
review without staging, commit, push, merge, or live work.

## 2026-09-09 — R3 Phase 2 adversarial correction pass

### Corrections

- JSON decoding now catches ordinary `ValueError`, including Python’s bounded
  integer-conversion limit, and maps it to the existing R2-compatible
  `response_unverifiable` result without broad exception handling elsewhere.
- Transport precedence is frozen and implemented: construction rejection,
  pre-status failure, HTTP 400-or-greater failure, known-status incomplete
  body, complete-body metadata unverifiability, unsupported below-400 status,
  then eligible HTTP-200 XON normalization.
- Exact boundary tests now use a non-BMP code point and assert 13,918-byte XON
  and 25,910-byte normalized-R2 outputs, plus every requested adjacent bound.
- R1 integration fixtures now use distinct deterministic baseline/current scan
  and source-check IDs and assert visible guarding without disappearance or
  exposure.

### Gotchas

- A status at or above 400 wins over simultaneous malformed headers,
  over-limit body state, or post-status read failure.
- The exact size evidence is serializer-specific and remains synthetic; it is
  not evidence of live service response size or compatibility.

### Status

Correction implementation is complete pending the final full verification
sequence and adversarial review.

## 2026-09-09 — Verify R3 Phase 2 adversarial correction pass

### Verification

The complete corrected diff and status inspection preceded this final required
sequence. Exact commands and outputs were:

- `./.venv/bin/python -m pytest -q` — `207 passed in 6.09s`.
- `./.venv/bin/ruff format --check .` — `31 files already formatted`.
- `./.venv/bin/ruff check .` — `All checks passed!`.
- `./.venv/bin/mypy .` — `Success: no issues found in 15 source files`.
- `git diff --check` — no output; exit 0.
- `git --no-pager diff --stat` — 4 tracked files changed; 287 insertions and
  2 deletions. Untracked implementation/test files are listed by status.

The test count is 147 pre-R3 tests plus 60 focused XON tests = 207 total.

### Gotchas

- The exact 6.09-second runtime is one final run; earlier successful timings
  remain historical execution variance.
- Verification remains synthetic and offline and does not establish live
  compatibility, completeness, freshness, coverage, usefulness, or safety.

### Status

Correction pass is verified and stopped for adversarial review without
staging, commit, push, merge, or live-source work.

## 2026-09-09 — R3 Phase 2 final consistency corrections

### Corrections

- The research document now matches the implementation: an oversized
  generated R2 envelope raises `R2EnvelopeTooLargeError` as a visible local
  construction rejection before R2, unreachable through the bounded selected
  XON path.
- The first-check R1 integration test now includes an after-status incomplete
  attempt and asserts no baseline, `NOT_COMPARABLE`,
  `guarding_unverifiable`, `response_incomplete`, and no exposure events.
- Corrected the recorded arithmetic to state: 147 pre-R3 tests plus 60
  focused XON tests = 207 total.

### Gotchas

- The oversized-envelope rejection is a local guard, not an R2 or R1 source
  outcome.

### Status

Final consistency corrections are complete pending verification and adversarial
review.

## 2026-09-09 — Verify R3 Phase 2 final consistency corrections

### Verification

The complete corrected diff and status inspection preceded this final sequence:

- `./.venv/bin/python -m pytest -q` — `207 passed in 6.19s`.
- `./.venv/bin/ruff format --check .` — `31 files already formatted`.
- `./.venv/bin/ruff check .` — `All checks passed!`.
- `./.venv/bin/mypy .` — `Success: no issues found in 15 source files`.
- `git diff --check` — no output; exit 0.

### Gotchas

- The oversized generated-envelope guard raises visibly before R2 and is not
  a source outcome.

### Status

Final consistency corrections are verified and stopped for adversarial review
without staging, commit, push, merge, or live-source work.

## 2026-09-09 — Frame R3.5 visible synthetic XON scenarios

### Objective

Frame, without implementation, a visible end-to-end synthetic scenario
experiment that dispatches the existing offline simulator to the committed R3
check-email adapter and preserves R2.5, R2, and R1 ownership.

### Changes

**Directly verified:** Created `RESEARCH_003_5_VISIBLE_XON_SCENARIOS.md`.
It reconciles the requested phase with merge commit `35ef380`, freezes a new
`r3.5-visible-xon-scenarios/1` family, defines the transport envelope and
lowercase-hex byte encoding, records exact bounds and diagnostics, specifies
the 17 curated scenarios, and states the proposed Phase 2 files and
delegation tests.

The framing keeps transport classification and XON normalization in the
existing R3 adapter, R2 as the only SourceCheck constructor, and R1 as the
only owner of baseline, comparison, exposure, guarding, and disappearance.
It records the observed immediate-prior ScanAttempt selection and the fact
that a failed or unverifiable scan can displace an older successful state.

### Verification

Pending the final repository verification sequence and complete diff/status
review. No implementation or scenario execution is claimed by this entry.

### Decisions

No project-level decision was added. The document stops at adversarial framing
review and does not authorize Phase 2 implementation or live integration.

### Gotchas

- The committed R3 adapter exposes transport classification and SourceCheck,
  but not an independent XON-classification record. The proposed output must
  use a non-semantic projection rather than duplicate the XON parser.
- Raw malformed or duplicate headers are valid untrusted transport metadata;
  only contradictory locally constructed envelopes are invalid scenarios.
- The editable-install setuptools package-discovery failure remains separate
  work and was not fixed.

### Status

Documentation framing is complete pending verification. No files were staged,
committed, pushed, merged, or implemented.

## 2026-09-09 — Verify R3.5 visible synthetic XON scenario framing

### Verification

- `./.venv/bin/python -m pytest -q` — 207 passed.
- `./.venv/bin/ruff format --check .` — 32 files already formatted.
- `./.venv/bin/ruff check .` — all checks passed.
- `./.venv/bin/mypy .` — no issues found in 15 source files.
- `git diff --check` — passed.
- Complete diff and status review found only the new framing document and the
  three permitted append-only logs changed; no source, test, fixture, or
  existing specification changed.

### Gotchas

- The verification run confirms the existing 207-test checkpoint; it does not
  execute the proposed R3.5 scenarios because this phase is framing only.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

R3.5 framing verification is complete. No files were staged, committed,
pushed, merged, or implemented. Stop for adversarial framing review.

## 2026-09-09 — Amend R3.5 framing after adversarial self-review

### Changes

- Added normative complete R1 report macros so every curated ledger row
  expands to literal comparison, exposure, guarding, and silence assertions.
- Added the missing wrong-Content-Type row to the metadata scenario.
- Corrected Scenario 17’s stated comparison ordering to R1’s lexical source
  ordering.

### Gotchas

- The framing document uses readable body and report aliases only as explicit
  documentation macros; Phase 2 fixtures must expand them to literal bytes and
  IDs.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

The framing was tightened for adversarial review. No source, test, fixture,
dependency, network, or Phase 2 implementation was added.

## 2026-09-09 — Verify amended R3.5 framing

### Verification

- `./.venv/bin/python -m pytest -q` — 207 passed.
- `./.venv/bin/ruff format --check .` — 32 files already formatted.
- `./.venv/bin/ruff check .` — all checks passed.
- `./.venv/bin/mypy .` — no issues found in 15 source files.
- `git diff --check` — passed.
- The final diff/status review still contains only the framing document and
  the three permitted append-only logs; no source, test, fixture, or existing
  specification changed.

### Gotchas

- The amended framing was not executed; verification remains against the
  existing 207-test implementation checkpoint.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

Amended R3.5 framing verification is complete. No files were staged,
committed, pushed, merged, or implemented. Stop for adversarial framing
review.

## 2026-09-09 — Correct R3.5 framing contract details

### Corrections

- Corrected the bounded overlong-integer body to 5,088 bytes.
- Permitted an empty raw header-name byte string while retaining the 64-byte
  bound and adapter-owned malformed-header classification.
- Froze exact JSON types and literal identities for XON and synthetic R2
  sources.
- Completed mixed-source input-size and human-output rules, Scenario 16's
  exact invalid diagnostic, the filename-to-ID table, the exhaustive XON
  presentation fallback, the derived-oracle wording, and the append-only
  Phase 2 record-file list.

### Gotchas

- The framing remains unimplemented; verification can only exercise the
  existing 207-test repository checkpoint.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

Documentation-only correction pass. No source, test, fixture, dependency,
network, staging, commit, push, merge, or Phase 2 implementation was added.

## 2026-09-09 — Verify corrected R3.5 framing

### Verification

- ./.venv/bin/python -m pytest -q — 207 passed in 7.12s.
- ./.venv/bin/ruff format --check . — 32 files already formatted.
- ./.venv/bin/ruff check . — All checks passed!
- ./.venv/bin/mypy . — Success: no issues found in 15 source files.
- git diff --check — passed with no output.
- Complete diff and status inspection confirmed only the R3.5 document and
  three permitted append-only logs are changed.

### Gotchas

- Verification covers the existing implementation checkpoint only; the R3.5
  scenario runner remains unimplemented and unexecuted.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

The corrected framing is verified and stopped for final adversarial review.

## 2026-09-09 — Freeze R3.5 XON projection internal error

### Corrections

Frozen the R3.5-only xon_projection_invariant fallback: READY transport plus
an adapter status other than completed or unverifiable produces the exact
human or JSON internal-error output, exit 2, discarded buffered normal
output, no XON/R1 result, and no later scans. R2.5 diagnostic behavior is
unchanged, and a Phase 2 test double is required to exercise both output
forms.

### Gotchas

- This is an internal runner invariant, not an invalid scenario or source
  result.
- The R3.5 runner remains unimplemented and unexecuted.

### Status

Documentation-only correction. No source, test, fixture, dependency, network,
staging, commit, push, merge, or Phase 2 implementation was added.

## 2026-09-09 — Verify frozen R3.5 XON projection internal error

### Verification

- ./.venv/bin/python -m pytest -q — 207 passed in 6.57s.
- ./.venv/bin/ruff format --check . — 32 files already formatted.
- ./.venv/bin/ruff check . — All checks passed!
- ./.venv/bin/mypy . — Success: no issues found in 15 source files.
- git diff --check — passed with no output.

### Gotchas

- The internal-error fallback was documented only; no test double or runner
  execution was added in this framing phase.

### Status

Verification passed. Nothing was staged, committed, pushed, merged, or
implemented.
Nothing was staged, committed, pushed, merged, or implemented.

## 2026-09-09 — Implement R3.5 visible synthetic XON scenarios

### Implementation

- Added exact-version R3.5 dispatch to the offline simulator while preserving
  the R2.5 branch and its output contract.
- Added the 17 literal curated scenario files, scenario helpers, and focused
  tests. The runner delegates transport/XON normalization to the committed
  XON adapter, synthetic-R2 checks to R2, and comparison, baselines, guards,
  exposures, disappearance, and ordering to R1.
- Implemented the frozen human and canonical JSON projections, exit codes,
  expectation mismatches, invalid construction diagnostics, and the
  R3.5-only `xon_projection_invariant` internal error path.

### Gotchas

- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.
- Scenario 16 is deliberately invalid input and exits 2; it is not a source
  result. The other 16 curated scenarios pass in both output modes.
- This proves deterministic synthetic delegation only; it does not establish
  live XposedOrNot compatibility, freshness, completeness, or coverage.

### Status

Phase 2 implementation is complete and remains unstaged, uncommitted, and
unpushed for adversarial implementation review.

## 2026-09-09 — Verify R3.5 visible synthetic XON scenarios

### Verification

- `./.venv/bin/python -m pytest -q` — 242 passed in 13.41s.
- `./.venv/bin/ruff format --check .` — 34 files already formatted.
- `./.venv/bin/ruff check .` — All checks passed!
- `./.venv/bin/mypy .` — Success: no issues found in 17 source files.
- `git diff --check` — passed with no output.
- All 16 valid curated scenarios passed in human and JSON modes with exit 0;
  Scenario 16 returned its exact human and JSON exit-2 contracts.

### Gotchas

- No network-capable imports or calls, credentials, real identifiers, or live
  endpoints were used.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

Verification passed. No files were staged, committed, pushed, or merged.

## 2026-09-10 — R3.5 Phase 2 adversarial test-strengthening correction

### Correction

- Added independently frozen raw SHA-256 digests and literal filename-to-ID
  aliases for all 17 scenario files, including exact hostile and over-limit
  body-byte assertions.
- Added byte-exact Scenario 17 human and canonical JSON golden output checks,
  complete nested machine-schema assertions, strict-oracle checks, delegation
  argument checks, and structural protection against semantic reimplementation
  in the runner.
- The existing runner, scenario bytes, and R1/R2/R3 semantics were preserved.

### Gotchas

- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.
- The new raw digest and golden-output assertions are synthetic evidence only;
  they do not establish live XposedOrNot compatibility.

### Status

This correction remains unstaged, uncommitted, and unpushed for adversarial
review.

## 2026-09-10 — Verify R3.5 Phase 2 adversarial test strengthening

### Verification

- All 17 curated scenarios passed in both modes: 34 runs, with 32 exit 0 and
  2 Scenario 16 exit 2.
- `./.venv/bin/python -m pytest -q` — 252 passed in 22.18s.
- `./.venv/bin/ruff format --check .` — 34 files already formatted.
- `./.venv/bin/ruff check .` — All checks passed!
- `./.venv/bin/mypy .` — Success: no issues found in 17 source files.
- `git diff --check` — passed with no output.

### Gotchas

- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

Verification passed. No files were staged, committed, pushed, or merged.

## 2026-09-09 — Final R3.5 Phase 2 verification correction

### Verification

- `./.venv/bin/python -m pytest -q` — 243 passed in 13.88s.
- `./.venv/bin/ruff format --check .` — 34 files already formatted.
- `./.venv/bin/ruff check .` — All checks passed!
- `./.venv/bin/mypy .` — Success: no issues found in 17 source files.
- `git diff --check` — passed with no output.

### Gotchas

- This final count includes the completed R3.5 implementation and focused
  tests; the earlier 242-test entry predates the final focused assertions.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

Final verification passed. The work remains unstaged, uncommitted, and
unpushed for adversarial implementation review.

## 2026-09-09 — Final verification after R3.5 invalid-family correction

### Verification

- `./.venv/bin/python -m pytest -q` — 243 passed in 13.45s.
- `./.venv/bin/ruff format --check .` — 34 files already formatted.
- `./.venv/bin/ruff check .` — All checks passed!
- `./.venv/bin/mypy .` — Success: no issues found in 17 source files.
- `git diff --check` — passed with no output.

### Gotchas

- R3.5 parser diagnostics now retain the R3.5 runner version even when
  validation fails before a scenario object can be constructed.
- The editable-install setuptools package-discovery issue remains separate
  work and was not fixed.

### Status

Verification passed. No files were staged, committed, pushed, or merged.

## 2026-09-11 — Frame R4 Phase 1 bounded live XON probe

### Objective

Frame the smallest approval-gated live experiment after the verified synthetic
R3 and R3.5 checkpoints, without implementing the collector or opening a
network connection.

### Changes

- Added `RESEARCH_004_BOUNDED_LIVE_XON_PROBE.md`.
- Defined a one-request, reserved-domain synthetic check-email probe that
  would translate only bounded I/O facts into the existing R3
  `TransportAttempt`.
- Preserved R3/R2/R1 ownership, failure visibility, the no-completed-empty
  check-email rule, and the no-raw-payload/no-credential boundary.
- Recorded explicit approval requirements for the future endpoint, synthetic
  identifier, headers, finite timeouts, request budget, retention, and stop
  conditions.

### Verification

Pending the post-edit repository checks recorded in the next handoff section.

### Decisions

No project-level decision was added to `DECISIONS.md`. R4 remains framing only;
the live experiment is not authorized by this entry.

### Gotchas

- The R3 adapter accepts only an in-memory transport attempt; a future capture
  layer must not duplicate its classification or XON/R2 semantics.
- A successful live response would be one bounded source observation, not
  evidence of completeness, ownership, safety, or notification usefulness.
- The editable-install setuptools discovery issue remains a separate work
  item and was not changed.

### Repository state

The new branch remains uncommitted and unpushed. Full verification and final
diff/status inspection are required before handoff.

## 2026-09-11 — Verify R4 Phase 1 framing

### Verification

- `./.venv/bin/python -m pytest -q` — 252 passed in 15.55 seconds.
- `./.venv/bin/ruff format --check .` — 35 files already formatted.
- `./.venv/bin/ruff check .` — all checks passed.
- `./.venv/bin/mypy .` — success, no issues found in 17 source files.
- `git diff --check` — passed.
- Final diff and status inspection found only
  `RESEARCH_004_BOUNDED_LIVE_XON_PROBE.md`, `BUILD_HISTORY.md`,
  `RESEARCH_LOG.md`, and `PROGRESS_LOG.md` changed.

### Decisions

No project-level decision was added. The R4 probe remains approval-gated and
unimplemented.

### Gotchas

- The checks validate the existing synthetic behavior and documentation only;
  they do not establish live XposedOrNot compatibility, completeness,
  freshness, coverage, ownership, or safety.
- The editable-install setuptools discovery issue remains a separate work
  item and was not changed.

### Status

Verification passed. No files were staged, committed, pushed, or merged. No
live request or external action was performed.

## 2026-09-11 — Execute approved R4 Phase 2 bounded live XON probe

### Objective

Execute exactly one approved bounded live probe against the documented free
XposedOrNot check-email endpoint using only the reserved synthetic subject,
then pass the captured attempt through the committed R3 adapter.

### Changes

- Added `personal_watchdog/r4_bounded_live_xon_probe.py`, a standard-library
  one-shot probe with no retry, redirect following, persistence, or comparison.
- Added `tests/test_r4_bounded_live_xon_probe.py` with five offline tests for
  request shape, failure visibility, malformed success, size bounds, and
  bounded output retention.
- Executed one approved live request; the response was not retained raw.

### Verification

- Focused R4 tests: 5 passed.
- Full suite: 257 passed.
- Ruff format and lint passed.
- mypy passed across 19 source files.
- `git diff --check` passed.

### Decisions

No project-level decision was added. The result is a single bounded
observation, not authorization for retries, monitoring, persistence,
notifications, or broader live coverage.

### Gotchas

- The transport was ready, but the complete 34-byte HTTP-200 JSON body was
  conservatively `unverifiable`; its exact shape was intentionally not
  retained, so no more specific cause can be claimed.
- This does not establish live service completeness, freshness, schema
  stability, ownership, coverage, or safety.
- The editable-install setuptools discovery issue remains a separate work
  item and was not changed.

### Status

The probe run completed without a second request. No files were staged,
committed, pushed, or merged.

## 2026-09-12 — R4 Stage 1 adversarial offline review

### Objective

Review the R4 one-shot probe against its approved bounds and R3 ownership
without making another network request or expanding it into a collector.

### Corrections

- Corrected timeout detection when `URLError` wraps a timeout cause.
- Rejected non-text response-header metadata before constructing a bounded
  attempt.
- Redacted the complete synthetic identifier from the local report.
- Added offline coverage for pre-status and post-status timeouts, duplicate
  content types, redirect rejection, over-limit capture, and output redaction.

### Verification

- Full suite: 261 passed.
- Ruff format and lint passed.
- mypy passed across 19 source files.
- `git diff --check` passed.

### Decisions

No project-level decision was added. The prior live result remains a single
unverifiable observation and was not repeated.

### Gotchas

- The response body remains intentionally unavailable for diagnosing the
  original 34-byte HTTP-200 unverifiable result.
- The checks establish bounded local behavior only; they do not establish
  live-service completeness, freshness, coverage, ownership, or safety.

### Status

Stage 1 review is complete. No files were staged, committed, pushed, or
merged, and no additional live request was made.

## 2026-09-12 — R4 Stage 2 conclusion

### Result

The bounded live experiment is inconclusive at the source-contract boundary:
transport reached HTTP 200 with complete JSON bytes, while the existing R3/R2
path returned `unverifiable`. The body was not retained, so no more specific
service-response explanation is supported.

### Decisions

Stop R4 here. Do not retry, loosen the schema, infer completed-empty, compare
the result, or begin monitoring. Any diagnostic follow-up requires a new
bounded approval.

### Gotchas

- A ready transport response is not an accepted source response.
- This result does not establish live completeness, freshness, coverage,
  ownership, safety, or notification usefulness.

### Status

Stage 2 conclusion recorded. No additional live request, staging, commit, or
push was performed.

## 2026-09-13 — Execute approved R4 Stage 3 diagnostic follow-up

### Objective

Diagnose the observed 34-byte HTTP-200 `unverifiable` response with one
additional bounded request and temporary diagnostic output, without retaining
the body in a file or broadening the probe.

### Changes

- Added explicit `--diagnostic` output that exposes only the bounded response
  bytes as lowercase hex; normal output remains redacted.
- Added offline coverage for diagnostic output.
- Made exactly one approved follow-up request using the same synthetic
  identifier and no credentials, retry, or redirect.

### Verification

- Focused R4 tests: 9 passed.
- Full suite: 261 passed.
- Ruff format and lint passed.
- mypy passed across 19 source files.
- `git diff --check` passed.

### Result

The body decoded to `{"Error":"Not found","email":null}` over HTTP 200 with
complete JSON transport. R3/R2 correctly preserved `unverifiable`; no
completed-empty result or clean claim was produced.

### Decisions

No project-level decision was added. This is one observed no-match shape, not
a general service contract or completeness finding.

### Gotchas

- Diagnostic output was bounded and not written to disk, but it is still
  response data and must not become a default output mode.
- The observed HTTP-200 no-match shape does not authorize changing the R3
  check-email semantics or importing analytics empty semantics.

### Status

Stage 3 is complete. No third request, staging, commit, or push was performed.

## 2026-09-13 — R4 Stage 4 final review and handoff

### Objective

Complete final review and leave the R4 branch ready for separately authorized
commit, without making another network request or changing repository history.

### Review

- Reviewed the complete intended R4 change set and boundary-sensitive source
  references.
- Confirmed branch, HEAD, worktree, staging state, and absence of a remote
  tracking branch for the experiment branch.
- Confirmed the probe remains synthetic-only, one-shot, bounded, and without
  credentials, retries, redirects, persistence, comparison, notification, or
  collector behavior.

### Verification

- Full suite: 261 passed.
- Ruff format: passed.
- Ruff lint: passed.
- mypy: passed using the configured `tests` target; 6 source files checked.
- `git diff --check`: passed.

### Result

R4 is complete as a bounded live observation. The observed no-match body does
not change R3/R2 semantics: the result remains `unverifiable`, not
completed-empty or clean. The branch is ready for a separately authorized
commit.

### Gotchas

- The diagnostic observation is evidence about one request, not a general
  source contract or completeness guarantee.
- The final review did not make a network request or alter the two-request
  experiment count.
- No files were staged; no commit or push was performed.

## 2026-09-15 — R5 Phase 1 offline XON contract reconciliation framing

### Objective

Frame a local-only R5 experiment using the already observed R4 response shape,
without implementing a fixture or making another live request.

### Changes

- Added `RESEARCH_005_OFFLINE_XON_CONTRACT_RECONCILIATION.md`.
- Defined a narrow question about reproducing the existing R3/R2
  `unverifiable` result from one bounded, provenance-limited offline input.
- Preserved the prohibition on completed-empty inference, clean claims,
  schema loosening, live requests, persistence, comparison, notification, and
  monitoring.

### Verification

- Confirmed the worktree was clean at R4 commit `6e6fc3d` before framing.
- Confirmed no implementation file, fixture, or test was added.
- Confirmed no network request was made.

### Result

R5 remains framed only. Any Phase 2 fixture or test requires explicit approval
of the exact offline scope.

### Gotchas

- The observed body is evidence from one R4 request, not a general XON
  no-match contract.
- Adding a fixture later must not turn `unverifiable` into completed-empty,
  disappearance, or a clean claim.
- This framing is local and remains uncommitted and unpushed.

## 2026-09-15 — R5 Phase 2 offline execution

### Objective

Execute the explicitly approved offline R5 scope: add one bounded,
provenance-limited fixture for the R4 body and verify it through the existing
R3/R2 adapter without making a live request.

### Changes

- Added `scenarios/r5_xon/01_observed_http_200_not_found.json` with HTTP 200,
  complete `application/json` transport metadata, the exact bounded body as
  hex, and redacted local references.
- Added `tests/test_r5_offline_xon_contract_reconciliation.py` with coverage
  for adapter reproduction and fixture redaction/bounds.
- Updated the R5 document and append-only records with the execution result.

### Verification

- Focused R5 tests: 2 passed.
- Full suite: 263 passed.
- Ruff format: passed.
- Ruff lint: passed.
- mypy: passed using the configured `tests` target; 14 source files checked.
- `git diff --check`: passed.

### Result

The existing adapter reproduced `ready` transport and
`unverifiable`/`response_unverifiable` source output with no accepted
findings. R5 did not alter R3/R2 semantics or invoke R1 comparison.

### Gotchas

- The fixture proves only local reproducibility of one observed body shape; it
  does not establish a general no-match contract or service completeness.
- The fixture’s provenance metadata is test data and must not become trusted
  adapter context.
- No live request, dependency, persistence, notification, collector, commit,
  or push was made during Phase 2.

## 2026-09-15 — R6 Phase 1 minimal local watchdog workflow framing

### Objective

Define the smallest truthful user workflow for Personal Watchdog without
implementing a CLI or local persistence.

### Changes

- Added `RESEARCH_006_LOCAL_WATCHDOG_WORKFLOW.md`.
- Framed proposed meanings for `init`, `scan`, comparison, `report`, and
  `history`.
- Defined a one-synthetic-subject, one-offline-fixture Phase 2 target,
  bounded local records, and stop criteria for live or broader product scope.

### Verification

- Confirmed the R5-local worktree state before framing.
- Confirmed no production code, fixture, test, dependency, or network request
  was added by R6.
- `git diff --check`: passed.

### Result

R6 remains framed only. The proposed workflow preserves existing R1/R2
semantics: only completed comparable checks support absence or change claims;
failed and unverifiable results remain visible and non-comparable.

### Gotchas

- The planned `watchdog` commands in the README remain unimplemented.
- Storage format, retention, correction, recovery, and configuration secrecy
  require decisions before Phase 2 implementation.
- No scheduling, notification, live source, or comprehensive coverage is
  implied by this framing.

## 2026-09-15 — R6 Phase 2 offline workflow execution

### Objective

Implement the explicitly approved minimal local workflow over one synthetic
subject and one offline fixture source, preserving existing R1/R2 semantics.

### Changes

- Added `personal_watchdog/cli.py` with `init`, fixture `scan`,
  `report --latest`, and `history` commands.
- Added bounded JSON configuration and history state under a caller-selected
  directory, defaulting to `.watchdog/`.
- Added six fixture outcomes: `baseline`, `unchanged`, `changed`,
  `disappeared`, `failed`, and `unverifiable`.
- Added `tests/test_r6_local_workflow.py` covering baseline, change,
  disappearance, guarding, reloadable reports/history, and uninitialized
  state.
- Updated `README.md` and the R6 document with the current offline usage.
- Added `.watchdog/` to `.gitignore` so default local state is not staged.

### Verification

- Focused R6 tests: 5 passed.
- Full suite: 268 passed.
- Ruff format: passed.
- Ruff lint: passed.
- mypy: passed using the configured `tests` target; 16 source files checked.
- `git diff --check`: passed.
- Manually exercised init, baseline scan, changed scan, failed scan, report,
  and history in a temporary local state directory.

### Result

The workflow produces a baseline, material-change exposure, disappearance
only after a comparable completed baseline, and guarding events for failed or
unverifiable current checks. State contains structured records only and is
bounded to 32 scans.

### Gotchas

- This is an offline fixture workflow, not a live watchdog or installed CLI
  executable.
- The local JSON state is bounded and atomically replaced, but encryption,
  retention deletion, correction, corruption recovery, and export remain open.
- No real identifier, credential, scheduler, notification, live adapter,
  dependency, commit, or push was added.

## 2026-09-16 — R7 Phase 1 approved-identifier configuration framing

### Objective

Frame the first ordered R7 focus: local configuration for an explicitly
approved identifier, without implementing profile storage or handling real
identity data.

### Changes

- Added `RESEARCH_007_APPROVED_IDENTIFIER_CONFIGURATION.md`.
- Defined a provisional profile boundary separating sensitive values from
  opaque scan/history references.
- Framed explicit approval, enablement, protected input, redacted output,
  R6 migration, retention, and synthetic acceptance requirements.

### Verification

- Confirmed local `main` was synchronized to merge commit `2ab2510`.
- Created clean local branch `experiment/r7-approved-identifier-config`.
- Confirmed no production code, fixture, test, dependency, or network request
  was added by R7.
- `git diff --check`: passed.

### Result

R7 remains framed only. The next phase must choose the profile schema, input
channel, permission model, and compatibility behavior before implementation.

### Gotchas

- A local approval record does not prove identity ownership or source truth.
- Complete identifiers must remain out of normal reports, history, logs,
  fixtures, and committed expected output.
- Encryption, secure deletion, key management, and compromised-host resistance
  remain separate design questions.
- No real identifier, live request, commit, or push was made.

## 2026-09-16 — R7 Phase 2 approved-identifier configuration execution

### Objective

Implement the explicitly approved offline R7 profile boundary over the merged
R6 workflow, using synthetic values only and preserving R1/R2 semantics.

### Changes

- Added `personal_watchdog/profiles.py` with versioned, bounded local profile
  storage for `email` and `username` kinds.
- Added explicit approval and protected input requirements, strict validation,
  opaque generated subject references, redacted listing, disablement, atomic
  writes, and restrictive `0600` profile-file permissions.
- Extended `personal_watchdog/cli.py` with profile add/list/disable commands
  and optional `scan --subject-ref` selection for enabled approved profiles.
- Added `tests/test_r7_profiles.py` for redaction, reload, approval and input
  validation, scan selection, R6 state compatibility, disablement, and
  history preservation.
- Updated the README and R7 research record with the implemented offline
  usage and boundary.

### Verification

- Focused R7 plus R6 compatibility tests: 11 passed.
- Ruff format and lint passed for the changed Python files.
- mypy passed for the changed Python files.
- `git diff --check` and full repository verification remain in progress.

### Result

The local profile is kept separate from R6 scan history. Ordinary profile,
scan, report, and history output exposes only opaque references and bounded
metadata. A disabled profile cannot be selected for a new scan.

### Gotchas

- The profile JSON contains the sensitive value by design and is local-only;
  `0600` permissions are not encryption or protection from a compromised
  host.
- The offline fixture does not use the profile value, so this phase proves
  selection and redaction, not live adapter behavior or source accuracy.
- No real identifier, live request, credential, dependency, scheduler,
  notification, export, commit, or push was added.

### Verification correction

The focused R7/R6 set was expanded to 13 passing tests to cover successful
username configuration and duplicate-value rejection. The full repository
suite passed with 276 tests. Ruff format/lint, mypy, `git diff --check`, and
the manual offline CLI smoke test passed.

## 2026-09-16 — R8 Phase 1 profile retention and recovery framing

### Objective

Frame the next ordered research question after R7: how local profile
retention, disablement, deletion, corruption, interruption, and recovery can
remain bounded and truthful.

### Changes

- Added `RESEARCH_008_PROFILE_RETENTION_RECOVERY.md`.
- Reconciled the current R7 profile sidecar, eight-profile limit, `0600`
  permissions, atomic replacement, disable-only behavior, and independent R6
  32-scan bound.
- Defined proposed state distinctions, fail-closed malformed-state handling,
  history preservation, interruption tests, and explicit Phase 2 choices.

### Verification

- Confirmed clean local `main` at merged R7 commit `81e979c`.
- Created clean local branch `experiment/r8-profile-retention-recovery`.
- Confirmed no production code, fixture, test, dependency, or network request
  was added by R8 framing.
- Documentation/worktree checks remain to be completed after this record.

### Result

R8 remains documentation-only and proposes no automatic deletion, backup,
restore, secure-erasure claim, or universal durability claim.

### Gotchas

- Current atomic replacement does not prove power-loss durability or protect
  against a compromised host.
- Disablement currently retains the profile value; deletion and re-enable are
  separate policy decisions, not implied behavior.
- A missing or malformed profile store must never become an empty store or a
  source-level clean result.
- No real identifier, live request, staging, commit, push, or pull request
  was made.

### Verification update

- Full repository suite: 284 passed.
- Ruff format and lint: passed.
- mypy: passed on 25 source files.
- `git diff --check`: passed.
- No production code changed; R9 remains uncommitted and unpushed.

## 2026-09-16 — R8 Phase 2 conservative retention and recovery execution

### Objective

Implement the approved conservative R8 subset over the R7 profile store:
fail-closed missing state, preserve valid state across interrupted writes,
ignore stale temporary files, and keep profile/history bounds independent.

### Changes

- Changed `load_profiles` so it no longer creates a missing profile sidecar;
  missing state is reported visibly.
- Added `tests/test_r8_profile_recovery.py` covering missing, malformed,
  wrong-version, unsupported-field, interrupted-write, stale-temporary-file,
  and independent-bound behavior.
- Kept R7 disable-only retention, opaque history, R1/R2 semantics, and the
  existing bounded atomic replacement mechanism unchanged.
- Did not add deletion, backup, restore, re-enable, or automatic age-based
  retention.
- Updated the R8 research record with the executed conservative boundary.

### Verification

- Focused R7/R8 tests: 16 passed.
- Ruff format and lint passed for the changed Python files.
- mypy passed on 25 source files.
- Full repository suite: 284 passed.
- `git diff --check`: passed.

### Result

Unavailable or malformed profile state cannot be silently converted into an
empty store. An injected failure before replacement leaves the prior valid
profile target intact, and a stale temporary file cannot override it.

### Gotchas

- The existing replacement mechanism does not prove power-loss durability,
  filesystem-wide atomicity, or secure deletion.
- Disablement retains the profile value; deletion, backup, restore, and
  re-enable remain separate policy decisions.
- No real identifier, live request, credential, dependency, scheduler,
  notification, export, commit, push, or pull request was added.

## 2026-09-16 — R9 Phase 1 approved-profile lifecycle framing

### Objective

Frame the next ordered research question after R8: how explicit disablement,
re-enable, and deletion can preserve local consent boundaries and opaque scan
history.

### Changes

- Added `RESEARCH_009_PROFILE_LIFECYCLE.md`.
- Defined proposed lifecycle transitions, fresh approval for re-enable,
  optional two-step deletion, non-reuse of opaque references, and history
  preservation.
- Defined failure, interruption, redaction, bound, and R1/R2 invariants for a
  possible later offline implementation.

### Verification

- Confirmed clean local `main` at merged R8 commit `c63c174`.
- Created clean local branch `experiment/r9-profile-lifecycle`.
- Confirmed no production code, fixture, test, dependency, or network request
  was added by R9 framing.
- Documentation/worktree checks remain to be completed after this record.

### Result

R9 remains documentation-only. The conservative default is disable-only until
re-enable and deletion are separately chosen and approved.

### Gotchas

- Re-enabling a retained record does not prove current consent or identity
  ownership.
- Removing a profile record does not prove secure erasure from every storage
  layer or backup.
- Historical records must remain opaque and unchanged after lifecycle actions.
- No real identifier, live request, staging, commit, push, or pull request
  was made.

### Verification update

- Full repository suite: 276 passed.
- Ruff format and lint: passed.
- mypy: passed on 24 source files.
- `git diff --check`: passed.
- No production code changed; R8 remains uncommitted and unpushed.

## 2026-09-16 — R9 Phase 2 approved-profile lifecycle execution

### Objective

Implement the explicitly approved offline lifecycle protocol over R7/R8:
fresh approval for re-enable, disable-before-delete, explicit deletion
confirmation, monotonic opaque references, and preserved history.

### Changes

- Added `enable_profile` and `delete_profile` with explicit approval and
  disable-before-delete guards.
- Added CLI commands `profile enable --approve` and
  `profile delete --confirm`.
- Preserved the existing monotonic subject-reference counter so deleted
  references cannot be reused.
- Added lifecycle tests for re-enable, deletion guards, history preservation,
  reference non-reuse, and interrupted deletion writes.
- Updated the README and R9 research record with the implemented boundary.

### Verification

- Focused R7/R8/R9 tests: 20 passed.
- Ruff format and lint passed for the changed Python files.
- mypy passed on 26 source files.
- Full repository suite: 288 passed.
- `git diff --check`: passed.

### Result

Re-enable now requires a fresh explicit approval signal. Deletion is a
separate confirmed action available only for disabled profiles, and it does
not rewrite scan history or claim secure erasure.

### Gotchas

- Profile deletion removes the current record but cannot prove secure erasure
  from filesystem layers, backups, memory, or forensic copies.
- Re-enable preserves the opaque reference but does not prove current consent
  or identity ownership.
- No real identifier, live request, credential, dependency, scheduler,
  notification, export, commit, push, or pull request was added.
