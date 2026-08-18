# Personal Watchdog research log

This is an append-oriented record of research questions, observations,
decisions, failures, and next questions. Timestamps copied from Git or local
notes are unverified. This log does not contain real personal information.

## 2026-08-06 — Milestone 0 foundation

### Research question

Can the repository establish a safe, policy-first foundation without pretending
that a scanner or product architecture has already been validated?

### Observation

The repository foundation was created in Git commit
`b07bed2c3872b083f541d7ae6c1b29e568c0079b`. The retained files establish
privacy, security, contributor, packaging, and policy-smoke-test boundaries.

### Result

The foundation checkpoint was accepted as Milestone 0. No watchdog behaviour
was implemented. The existing progress record reports passing Milestone 0
checks; the exact current verification is recorded in the Base Zero completion
entry below.

### Next question

What small offline experiment can define a bark without overstating what a
source check proves?

## 2026-08-17 — Planning and approval boundary

### Research question

Can the project record a bounded offline vertical-slice proposal while keeping
implementation, dependencies, live integrations, and real identifiers behind
explicit approval?

### Observations

- The project root is `/home/peters/personal-watchdog` on `main`.
- The existing policy requires synthetic identifiers, mocked or offline tests,
  bounded evidence, and truthful failure semantics.
- `PERSONAL_WATCHDOG_CODEX_ITINERARY.md` describes a revised Milestone 1
  proposal, including a possible SQLite ledger and independent verifier. It
  explicitly says that proposal is awaiting approval.
- No scanner, comparator, persistence layer, fixture adapter, database,
  verifier, or network integration was implemented.

### Result

The proposal remains a proposal. It is not an automatic marching order.

### Next question

Can deterministic observations be converted into rare, truthful bark events?

## 2026-08-18 — Base Zero completion

### Research question

Can the project preserve its exploratory history and approval boundaries in
durable records without implementing watchdog behaviour?

### Scope

Add the Base Zero, itinerary, progress, project-history, research, decision,
reference, and build-history records; add the durable build-history rule; do
not add source code, fixtures, adapters, databases, schemas, or network
integrations.

### Observations

- This is speculative research, not an urgent product build.
- SpiderFoot, XposedOrNot, Sherlock, Maigret, Vanish, auto-identity-remove,
  OnionScan, and ArchiveBox are retained as references, not dependencies.
- Kibitzr and `/home/peters/evidence-collection/repo/` are read-only
  architectural reference material.
- The documentation amalgamation approach was rejected as contaminated and
  incoherent.
- The earlier detailed itinerary is background and approval-gated.
- No bark definition has been experimentally validated.
- No scanner, comparator, persistence layer, or live adapter currently exists.
- The Milestone 0 policy and tooling checks pass.

### Result

Base Zero research records are complete. This entry records the documentation
checkpoint only; it does not answer the bark question or begin the comparator
experiment.

### Verification

- `.venv/bin/python -m pytest` — 3 passed.
- `.venv/bin/ruff format --check .` — 13 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 1 source file.
- `git diff --check` — passed.

### Next question

Whether deterministic observations can be converted into rare, truthful bark
events.

## 2026-08-18 — Frame Research Experiment R1

### Research question

Can deterministic observations, compared only across exactly comparable source
checks, be converted into rare and truthful bark events without turning a
failed, incomplete, blocked, malformed, timed-out, or unverifiable check into
“not found” or disappearance?

### Result

R1 has been framed in `RESEARCH_001_BARK_SCHEMA.md` but has not been run. The
document proposes terminology, schemas, comparability rules, material-change
rules, baseline behaviour, synthetic scenarios, falsification conditions,
stopping conditions, and unresolved decisions.

The schemas and rules are provisional. No application code, tests, fixtures,
databases, dependencies, adapters, network calls, notifications, or research
results were created by this framing step.

### Decision boundary

Stop for explicit approval before implementing or running R1. The recorded
Base Zero history and accepted decisions remain unchanged; this entry records
only that the experiment has been framed.

### Consistency review

A read-only review found four material framing gaps and resolved them
provisionally without running R1:

- comparability now requires exact agreement on `subject_ref`, `source_id`,
  `canonical_scope`, `adapter_id`, `adapter_version`, `schema_version`, and
  `normalization_version`; `contract_version` is not a substitute;
- timestamps, durations, retry counts, diagnostic text, and `reason_codes` are
  diagnostic metadata, not observation materiality; status transitions may
  produce non-exposure status guards;
- list semantics now distinguish unique sorted sets, observations sorted by
  `finding_key`, operational execution order, and ordered material list values;
  and
- failed or unverifiable checks contribute no accepted observations, while
  aggregate `completed`, `incomplete`, `failed`, and invalid `empty_scope`
  outcomes are defined explicitly.

The review also confirmed that the R1 document remains framed, not run, and
all schema choices remain provisional.

### Next question

Will the proposed deterministic schema survive the required synthetic
scenarios without false bark events or hidden non-comparability?

## 2026-08-18 — Clarify R1 guard-event semantics

### Research question

How should R1 represent a failed or unverifiable current source check without
allowing a guard to be mistaken for an exposure change?

### Observation

Implementation correctly stopped before code was written when a consistency
review found that the R1 framing named `not_comparable` and a possible status
guard but did not define whether the required `guarding_failed` and
`guarding_unverifiable` names were comparison results or separate events. This
was a material ambiguity, not a test convenience issue.

### Clarification

The provisional R1 model now separates comparison classification, comparison
reason, derived exposure events, and derived guarding events. Failed and
unverifiable current checks produce `not_comparable` plus respectively
`guarding_failed` or `guarding_unverifiable`, even without a successful
baseline. Guards never become exposure events. Empty declared scope is invalid
input rejected before any source check, with no scan result, baseline,
comparison, exposure event, or guard event.

### Result

The ambiguity is resolved for the approved R1 implementation, but no R1 run
has occurred and no schema choice has become accepted research evidence.

### Next question

Can the clarified deterministic in-memory model pass the required synthetic
transitions without false exposure barks or hidden non-comparability?

## 2026-08-18 — Execute Research Experiment R1

### Research question

Can deterministic synthetic observations be classified into truthful bark or
silence events without treating failure, uncertainty, incompatible scope, or
diagnostic variation as exposure change?

### Scope

Implement only immutable in-memory R1 records, source-contract canonicalization
for declared set-like fields, a pure comparator, synthetic fixtures, and tests.
Do not add a CLI, persistence, network access, live adapter, notification,
hashing, evidence capture, risk scoring, or product reporting.

### Observations

- A first completed source check creates a per-source baseline and remains
  silent, including when it has zero or more synthetic observations.
- Equal material observations remain `unchanged`; new, changed, and
  disappeared findings produce the corresponding derived exposure events.
- Timestamp, duration, retry count, diagnostic text, reason-code, and context
  changes do not enter observation fingerprints or produce exposure events.
- Failed and unverifiable current checks produce `not_comparable` with
  explicit reasons and separate `guarding_failed` or
  `guarding_unverifiable` events, including without a prior baseline. They
  produce no disappearance or exposure event.
- Completed sources in an aggregate `incomplete` scan remain independently
  comparable. Failed or unverifiable candidates cannot enter observations,
  baselines, or comparisons.
- Exact subject, source, scope, adapter, adapter-version, schema-version, and
  normalization-version mismatches remain non-comparable.
- Declared set-like fields canonicalize deterministically; ordered observation
  lists remain material. Empty declared scope is rejected before a scan exists.
- Source output order is deterministic and does not depend on input collection
  order.

### Result

The synthetic R1 implementation passed all specified transitions. The result
supports a bounded claim about this in-memory model: within the declared
synthetic source contract, comparison classification, comparison reasons,
derived exposure events, and derived guarding events can remain separate and
deterministic without converting failure or uncertainty into disappearance.

### Verification

- `.venv/bin/python -m pytest` — 29 passed.
- `.venv/bin/ruff format --check .` — 19 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 6 source files.
- `git diff --check` — passed.
- A scope review found no runtime network, persistence, hashing, live adapter,
  notification, evidence, risk, or severity implementation.

### What R1 does not establish

R1 does not establish source coverage, source truth, identity ownership,
comprehensive exposure detection, useful alert frequency, risk or danger,
live integration behaviour, persistence semantics, or notification policy. It
uses synthetic identifiers and a synthetic source contract only.

### Decision boundary

The observed result does not promote the provisional R1 schemas or bark rules
to an accepted product design. No further experiment begins in this entry.

### Next question

What, if anything, should be separately approved after reviewing this bounded
offline result?
