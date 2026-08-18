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
