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
