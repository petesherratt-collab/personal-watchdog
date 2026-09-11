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

## 2026-08-18 — Frame Research Experiment R2

### Research question

Can a bounded, untrusted synthetic adapter response be normalized into an R1
source check while preserving completed, completed-empty, failed,
unverifiable, malformed, incomplete, and incompatible distinctions?

### Scope

Create the provisional `RESEARCH_002_ADAPTER_BOUNDARY.md` framing only. Define
a bytes-first parser boundary, a versioned invented response envelope, strict
JSON and object-key validation, concrete limits, result validation,
response-to-R1 status mapping, trusted-context ownership, synthetic scenarios,
falsification conditions, and the approval boundary. Do not implement or run
an adapter, parser, fixture, comparison, bark, network call, persistence
layer, dependency, or notification.

### Observations

- The response format is deliberately synthetic and does not model
  XposedOrNot, Maigret, or another real service.
- The normalizer accepts raw bytes, rejects inputs above 65,536 bytes before
  decoding, and applies a maximum of 100 results and nesting depth 8.
- Duplicate JSON keys, `NaN`, `Infinity`, `-Infinity`, malformed UTF-8, parser
  errors, unknown fields, unsupported types, and excessive values become
  bounded unverifiable outcomes with fixed reason codes.
- `contract_version` identifies only the response envelope. Trusted local R1
  context supplies subject, source, scope, adapter, schema, and normalization
  identity; the response cannot provide or overwrite those fields.
- Explicit completed, completed-empty, failed, unverifiable, incomplete,
  malformed, and incompatible conditions have separate provisional
  classifications. Every incomplete response maps to R1 `unverifiable`, and
  partial candidates are discarded.
- Exact duplicate result identities may be deduplicated; conflicting duplicate
  identities make the entire response unverifiable.
- Only a normalized R1 `SourceCheck` may cross the boundary. R2 must never
  produce a comparison result or a derived exposure or guarding event.

### Result

R2 has been framed but not run. The concrete parser boundary, limits, response
envelope, mappings, scenarios, falsification conditions, and approval boundary
remain provisional. No adapter code or research result was created.

### Decision boundary

Stop for explicit approval before implementing or running R2. R1 remains the
sole owner of comparison and derived-event semantics.

### Next question

Can the proposed synthetic response boundary normalize untrusted outcomes into
R1 source checks without accepting partial candidates or changing R1 meaning?

## 2026-08-18 — Execute Research Experiment R2 adapter boundary

### Research question

Can the committed bounded synthetic response boundary normalize untrusted bytes
into R1 source checks without accepting partial candidates or changing R1
comparison and event meaning?

### Scope

Implement and test only the standard-library-only R2 normalizer, synthetic
fixtures, hostile-input tests, and R1 integration tests described by
`RESEARCH_002_ADAPTER_BOUNDARY.md`. Do not add a real adapter, network access,
persistence, evidence storage, hashing, encryption, CLI, GUI, notification,
external dependency, or R3 work.

### Observations

- The normalizer accepts raw `bytes`, rejects values over 65,536 bytes before
  decoding, uses strict UTF-8, rejects duplicate JSON object keys and
  `NaN`/`Infinity` constants, and bounds arrays, objects, strings, nesting, and
  trusted diagnostics with the committed concrete values.
- The envelope contains only `contract_version`, `source_id`, `outcome`, and
  `results`. Trusted local context supplies the subject, source identity,
  scope, adapter identity/version, schema version, normalization version, and
  diagnostics; response data cannot replace them.
- Only a valid explicit `completed` response creates a completed R1 source
  check. Only `completed` with an empty result list represents observed
  absence. Failed, unverifiable, incomplete, malformed, incompatible, and
  invalid responses retain no accepted observations; every incomplete response
  maps to R1 `unverifiable`.
- Exact duplicate finding records are deterministically deduplicated after R1
  normalization. Conflicting duplicate finding identities invalidate the
  entire response. Ordered material lists remain order-sensitive while
  declared set-like lists use the existing R1 canonicalization.
- R1 baseline, new, disappearance, guarding, aggregate-incomplete, identity
  mismatch, diagnostic-exclusion, and subject-isolation transitions remained
  under the existing `compare_scans` implementation.

### Result

The bounded synthetic R2 adapter experiment passed its hostile-input and
integration scenarios. Within this synthetic contract, the adapter can produce
only R1-compatible source-check information while preserving successful empty
observation, failure, uncertainty, incompatibility, incompleteness, and
malformation distinctions. No partial candidate entered an observation,
baseline, comparison, or event.

### Verification

- `.venv/bin/python -m pytest` — 101 passed.
- `.venv/bin/ruff format --check .` — all files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.
- The implementation is standard-library-only; no R1 source file was modified,
  and no network, persistence, raw-response retention, real identifier, or
  external service behavior was added.

### What R2 establishes

It supports a bounded claim about this invented offline response format and
trusted-context boundary: strict bytes-first validation and explicit outcome
mapping can preserve R1's truthful-failure and comparison ownership under the
tested synthetic hostile inputs.

### What R2 does not establish

It does not establish source truth, source coverage, identity ownership, live
service behavior, protocol compatibility, useful alert frequency, risk,
notification policy, persistence semantics, or a production adapter contract.
The limits, fields, reason codes, and mappings remain provisional choices.

### Decision boundary

No new project-level decision was accepted. `DECISIONS.md` remains unchanged;
the R2 boundary and its result remain provisional, and R1 remains the sole
owner of comparison, exposure, and guarding semantics. Stop before R3.

### Next question

Whether this bounded synthetic boundary should be retained as provisional
research scaffolding after review, without treating it as a live integration or
product contract.

## 2026-09-06 — Frame Research Experiment R2.5 visible offline simulator

### Research question

Can the existing R1 comparison model and R2 bytes-first normalizer be exposed
through a small deterministic offline scenario runner without adding
comparison semantics, while making later bark-policy questions observable?

### Scope

Create only `RESEARCH_002_5_VISIBLE_OFFLINE_SIMULATOR.md`. Define a strict
synthetic scenario-file boundary, trusted local context versus simulated
untrusted bytes, chronological in-memory orchestration, human and canonical
machine-readable output, expectation comparison, exit codes, truthful failure
visibility, and ten curated scenarios. Do not implement or run a simulator,
add fixtures, alter R1/R2, add persistence, use a network, or begin R3.

### Repository reconciliation

The R1 and R2 design documents remain provisional framing artifacts and retain
their framing status language. The append-only research and build records
separately record the approved synthetic implementations and the 101-test R2
result. R2.5 treats this as a distinction between design-artifact status and
experiment execution history, not as permission to change either boundary.

The observed desktop packaging gotcha is retained: editable installation
failed because setuptools discovered both `data` and `personal_watchdog` as
top-level packages. Direct installation of pytest, Ruff, and mypy succeeded.
Packaging remains separate work.

### Result

The framing keeps R2 responsible for bytes-to-`SourceCheck` normalization and
R1 responsible for `compare_scans`, comparison results, exposure events, and
guarding events. It requires failed, unverifiable, malformed, incomplete,
incompatible, and adapter-rejected inputs to remain visible and never become
completed-empty or disappearance. It defines scenarios for baseline silence,
new exposure, material change, genuine disappearance, failure, unverifiable
input, mixed-source failure/change, adapter/schema incompatibility, hostile
false-clean input, and simultaneous findings.

Repeated-failure suppression, recovery events, trivial-change suppression,
simultaneous grouping, baseline overload, minimum actionable bark information,
and disappearance confirmation remain later experimental questions. No
project-level decision was established, so `DECISIONS.md` remains unchanged.

### Verification

- `.venv/bin/python -m pytest` — 101 passed.
- R2.5 framing remains documentation-only; no simulator or scenario fixture
  was implemented or run.
- No real identifiers, credentials, network calls, persistence, evidence
  hashing, archive changes, scheduler, notification, or R3 work was added.

### Decision boundary

Stop for adversarial review before implementing the proposed Phase 2 files.

### Next question

Does the proposed visible contract expose the existing R1/R2 behavior clearly
enough for a later implementation without silently choosing a bark policy?

## 2026-09-06 — Verify R2.5 framing handoff

### Observation

The framing was reconciled with the committed R1/R2 APIs. One JSON file now
represents one scenario; the ten curated scenarios are proposed as ten exact
Phase 2 files. Expected R1 projections include the complete existing record
fields, while local construction errors explicitly bypass R2 and use a fixed
R1 failed-check reason.

### Verification

- `.venv/bin/python -m pytest` — 101 passed.
- `.venv/bin/ruff format --check .` — 24 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.
- Complete diff inspection was performed; no source, test, fixture, dependency,
  archive, or `DECISIONS.md` change was made.

### Result

R2.5 remains a framing-only step. The repository shows no material
contradiction that blocks the framing: the README's Milestone 0 status remains
consistent with the absence of a product scanner, live network adapter, and
reporting CLI, while the later synthetic R1/R2 modules and append-only records
document the completed experiments. The stale milestone wording is historical
context, not a new behavior requirement.

### Decision boundary

Stop for adversarial review. Do not create the proposed Phase 2 files or alter
R1/R2 semantics in this turn.

## 2026-09-08 — Revise R2.5 framing contract

### Scope

Revise the framing without implementing or running the proposed simulator.

### Documented reconciliation

The revised document moves R2 expectations to checks and the complete expected
R1 `ComparisonReport` to scans; defines exact scenario/output/diagnostic key
sets and grammar; derives all execution IDs; removes the trusted
`exposure_silence` oracle; exercises local construction error in Scenario 7;
adds fixed outer bounds and exact validation rules; and renames Scenario 8 to
identify the R1 trusted-identity/version incompatibility boundary. Scenario 5
continues to cover an explicit R2 failed response.

### Result status

This is a documentation and reconciliation update only. The proposed simulator
behavior was not executed or behaviorally verified. Existing test and tooling
checks do not constitute execution of the proposed ten scenarios.

### Decision boundary

Stop for adversarial review before Phase 2 implementation. `DECISIONS.md`, R1,
R2, tests, fixtures, dependencies, and external repositories remain unchanged.

## 2026-09-08 — Verify R2.5 framing revision

### Verification observation

The existing repository suite and tooling checks completed successfully:

- `.venv/bin/python -m pytest` — 101 passed.
- `.venv/bin/ruff format --check .` — 24 files already formatted.
- `.venv/bin/ruff check .` — all checks passed.
- `.venv/bin/mypy .` — success, no issues found in 9 source files.
- `git diff --check` — passed.

Complete diff inspection observed changes only in the R2.5 framing document and
the three already changed logs. The proposed simulator and its ten scenarios
were not executed; the checks do not behaviorally verify proposed Phase 2
behavior.

### Decision boundary

Stop for adversarial review. No implementation, staging, commit, push, or R1/R2
change was made.

## 2026-09-08 — Final R2.5 ownership-boundary correction

### Documented reconciliation

The framing now assigns construction of only `scan_id` and `source_check_id` to
the runner. R1 alone constructs `comparison_id` and `guard_id`; their formulas
remain repository observations for authors. Expected IDs are ordinary
well-typed oracle strings compared literally with `compare_scans` output, so a
wrong ID is exit-code-1 expectation mismatch rather than exit-code-2 invalid
scenario.

Each scan must resolve its source references to unique source IDs, with
duplicate resolution reported as `reference_error`; different scans may use
different identities for the same source ID. One-file syntax validation cannot
enforce cross-file `scenario_id` uniqueness, so the ten-fixture test suite must
enforce it.

### Result status

Documentation and reconciliation only. The proposed simulator behavior was
not executed or behaviorally verified.

### Decision boundary

Stop for adversarial review. Do not begin Phase 2 or modify R1/R2.

## 2026-09-08 — Verify final R2.5 boundary correction

### Verification observation

The established repository checks completed successfully: 101 pytest tests
passed; Ruff format and lint passed; mypy found no issues in 9 source files;
and `git diff --check` passed. Complete diff inspection observed only the
framing document and the three already changed logs. The proposed simulator
was not executed or behaviorally verified.

### Decision boundary

Stop for adversarial review. No Phase 2 implementation or Git mutation was
made.

## 2026-09-08 — Final R2.5 framing verification observation

### Verification observation

The existing repository checks completed successfully: 101 pytest tests passed;
Ruff format reported 24 files already formatted; Ruff lint passed; mypy found
no issues in 9 source files; and `git diff --check` passed. Complete diff
inspection observed only the requested framing document and three logs. The
proposed simulator behavior was not executed or behaviorally verified.

### Decision boundary

Stop for adversarial review with no implementation, staging, commit, push, or
R1/R2 change.

## 2026-09-08 — Execute R2.5 visible offline simulator

### Synthetic execution observation

Phase 2 was implemented against the frozen R2.5 framing. All ten curated
scenario files passed in both human and `--json` modes with exit code `0`:

1. baseline followed by silence;
2. new exposure;
3. material change;
4. genuine disappearance;
5. source failure without disappearance;
6. unverifiable source;
7. mixed local construction failure and valid change;
8. R1 trusted identity/version incompatibility;
9. hostile false-clean response;
10. simultaneous findings.

The test suite also exercised a controlled CLI expectation mismatch (exit `1`)
and invalid scenarios (exit `2`). These are synthetic offline observations of
the existing R1/R2 behavior and runner contract only; they say nothing about
live-source truth or product usefulness.

### Boundary observation

The runner constructs only scan and source-check IDs. R2 interpreted the
simulated bytes, while R1 constructed source aggregates, comparisons, IDs,
exposure events, and guarding events. Exposure silence was derived only from
the actual R1 exposure collection. No live source, persistence, archive,
network, credential, or later milestone behavior was added.

### Decision boundary

Stop for adversarial implementation review. Do not stage, commit, push, or
begin R3.

## 2026-09-08 — R2.5 adversarial implementation corrections

### Synthetic execution observation

The runner was revised without changing the ten valid scenario meanings.
Scenario-file reads are bounded before parsing; mismatch pointers use actual
array positions and deterministic sorted object-field traversal; and local
construction validation reports the exact marker path. Tests now exercise the
complete frozen output grammar, canonical serialization, all declared bounds,
validation rules, fixture hygiene, and expectation isolation.

All ten scenarios again passed in both human and JSON modes with exit code `0`.
Controlled expectation mismatch and invalid/reference-error cases returned
exit codes `1` and `2`. The full suite passed with 147 tests. These remain
synthetic offline observations only and establish neither live-source truth
nor product usefulness.

### Decision boundary

Stop for adversarial review. Do not stage, commit, push, modify R1/R2, or
begin R3.

## 2026-09-08 — Frame R3 Phase 1 XposedOrNot contract research

### Research question

Can the currently documented official XposedOrNot API contract be mapped
through the existing R2 adapter boundary and R1 comparison semantics without
turning transport, authentication, authorization, rate-limit, service, HTTP,
content-type, schema, parsing, timeout, partial-response, or ambiguity
failures into completed-empty or disappearance?

### Scope and provenance

Read the repository-authoritative R1/R2/R2.5 documents, implementation, tests,
fixtures, and policy records before research. Examined only official
XposedOrNot documentation and official repositories, on 2026-09-08:

- the official API documentation at `https://xposedornot.com/api_doc`, whose
  page identifies the API Quick Reference as last updated 2026-06-03;
- the official API repository README at
  `https://github.com/XposedOrNot/XposedOrNot-API`, whose `master` history
  showed current commit prefix `b394f21`;
- the official Python SDK README and the `client.py` and email-endpoint files
  at `https://github.com/XposedOrNot/XposedOrNot-Python`; and
- the official JavaScript SDK README at
  `https://github.com/XposedOrNot/XposedOrNot-JS`.

No XposedOrNot API endpoint was called, and no identifier, credential, or
password was submitted.

### Observations

- The official documentation identifies keyless free email, analytics,
  password, catalogue, and key-authorized domain routes, with a separate
  Plus API described by the official SDKs.
- The free email found example contains breach arrays, an email echo, and a
  success status. The documented free no-result body contains an `Error`
  string and null email but does not state its HTTP status.
- The same official documentation assigns HTTP 404 to input/no-data errors,
  while the official Python client maps 404 to `NotFoundError`.
- The official documentation names the optional free lookup query `details`,
  while the official Python client sends `include_details`.
- The website publishes 2 requests/second plus hourly/daily caps; the official
  SDKs describe 1-request/second client spacing and retries. This is preserved
  as a documentation/client-behavior conflict.
- Analytics documents an explicit HTTP 200 all-null no-result shape. No
  equivalent unambiguous empty contract was documented for the free email
  body, password body, catalogue, or domain report.
- No official source examined specifies a closed schema, content type/charset,
  maximum response size, pagination, truncation marker, ordering, duplicate
  behavior, or freshness/completeness signal for the selected free lookup.

### Result

`RESEARCH_003_XPOSEDORNOT_CONTRACT.md` records a conservative mapping. A
later synthetic adapter experiment is justified as a boundary test only if it
freezes a narrower schema and maps ambiguity, malformed output, partial data,
auth, rate limits, server failures, and timeouts to failed, unverifiable, or
incomplete. The documentation is not sufficient to authorize a live adapter or
to treat the free email no-result body as completed-empty.

### Decision boundary

No project-level decision was established, so `DECISIONS.md` remains
unchanged. Stop for adversarial review. Do not implement an adapter, add an
HTTP client, make a live request, add a dependency, use credentials, or begin
R4.

## 2026-09-08 — Verify R3 Phase 1 XposedOrNot contract research

### Verification observation

- Full pytest suite: 147 passed.
- Ruff format check: 28 files already formatted.
- Ruff lint: all checks passed.
- mypy: success, no issues found in 12 source files.
- `git diff --check`: passed.
- Complete diff inspection found only `RESEARCH_003_XPOSEDORNOT_CONTRACT.md`
  and the three permitted append-only history/log files changed or added.

These checks validate repository hygiene and preserve the existing synthetic
R1/R2/R2.5 behavior. They do not execute a live XposedOrNot request or prove
the official service contract.

### Decision boundary

Stop for adversarial review without staging, committing, pushing, implementing
the adapter, or making a live request.

## 2026-09-08 — Correct R3 Phase 1 contract framing after OpenAPI review

### Correction scope

The official API repository README identifies `https://api.xposedornot.com/docs`
and `https://api.xposedornot.com/openapi.json` as the current Swagger/OpenAPI
artifacts. They were accessed for documentation only. No Swagger action or
functional XposedOrNot lookup endpoint was called.

The specification reports OpenAPI `3.0.0`, API specification version `2.0.0`,
and production server `https://api.xposedornot.com`. It resolves the free
check-email query name as `include_details`, documents `application/json` for
the two email-family 200 responses, and specifies email-format parameters and
selected 200/404 statuses. It does not close the schemas, require their
properties, define the analytics no-match body, or resolve charset, size,
pagination, truncation, ordering, duplicate, freshness, or completeness
behavior. Its free 404 schema also conflicts with the website’s null email
example; these facts remain separate.

### Reproducible source pins

The mutable GitHub URLs in the earlier entry are historical only. The current
source register is pinned to full SHAs and immutable file permalinks:

- API README: `cbf5423ed601bd74d896efebd0d28c637a6cddef`, [commit-pinned file](https://github.com/XposedOrNot/XposedOrNot-API/blob/cbf5423ed601bd74d896efebd0d28c637a6cddef/README.md).
- Python SDK README, client, and email endpoint: `911f49aa08939827d4717f3d48fd192c0c072c29`, [README](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/README.md), [client](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/xposedornot/client.py), [email endpoint](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/xposedornot/endpoints/email.py).
- JavaScript SDK README: `d4cf1af21a53c32c03d767a59d382b01b4a21908`, [commit-pinned file](https://github.com/XposedOrNot/XposedOrNot-JS/blob/d4cf1af21a53c32c03d767a59d382b01b4a21908/README.md).

### Endpoint-family and boundary correction

Free check-email and breach-analytics are now explicitly distinct source
contracts. The proposed first synthetic experiment selects only keyless
`GET /v1/check-email/{email}` with `include_details=false`, source identity
`xposedornot.free.check-email`, and schema `xon-check-email/1`. Analytics has
source identity `xposedornot.free.breach-analytics`, scope
`GET /v1/breach-analytics?email={email}`, and schema
`xon-breach-analytics/1`; it is deferred and has a separate matrix.

The documented analytics no-match fixture is now named
`XON_ANALYTICS_HTTP_200_NO_MATCH_V1`. Its exact synthetic predicate is HTTP
200, normalized `application/json`, complete strict JSON, exactly six
top-level keys, and values:

```text
BreachMetrics: null
BreachesSummary: {"site": ""}
ExposedBreaches: null
ExposedPastes: null
PasteMetrics: null
PastesSummary: {"cnt": 0, "domain": "", "tmpstmp": ""}
```

The two non-null empty summary objects are part of the predicate. Only this
predicate under the analytics source identity may become `completed-empty`.

The later synthetic transport envelope now explicitly separates HTTP status,
normalized content type, bounded allowlisted headers, complete or bounded
body bytes, body state, transport/timeout failure, and locally trusted source
context. HTTP metadata is untrusted transport metadata. Transport
classification precedes XON normalization; XON normalization precedes the
existing R2 bytes-first validator; R1 receives only the resulting
`SourceCheck` and retains comparison/disappearance ownership.

Exact duplicate handling follows existing R2: equal duplicate observations are
deterministically deduplicated with `duplicate_finding_key_deduplicated`,
while conflicting duplicates are `unverifiable` with no observations. No
contradictory XON duplicate rule is added.

The record-file scope is four tracked files: `BUILD_HISTORY.md`,
`PROGRESS_LOG.md`, `REFERENCES.md`, and `RESEARCH_LOG.md`. The earlier “three”
wording is superseded by this correction without rewriting earlier history.

## 2026-09-08 — Verify corrected R3 Phase 1 framing

### Exact verification commands and outputs

```text
$ .venv/bin/python -m pytest
============================= 147 passed in 6.01s =============================

$ .venv/bin/ruff format --check .
28 files already formatted

$ .venv/bin/ruff check .
All checks passed!

$ .venv/bin/mypy .
Success: no issues found in 12 source files

$ git diff --check
(no output; exit 0)
```

The Ruff count is 28 rather than the R2.5 record’s 27 because Ruff’s
configured include set formats Markdown as well as Python, and the new R3
research document is now one additional included file. The R2.5 commit and
the current worktree both contain the same 12 Python files; no Python source
file was added or changed. The mypy count is therefore unchanged at 12.

### Final boundary

Complete diff inspection and status review remain required before handoff.
No endpoint, identifier, credential, adapter, HTTP client, dependency,
staging, commit, push, or external archive change was performed.

## 2026-09-08 — Final R3 Phase 1 framing verification

### Verification ordering

The complete diff and status inspection was performed before this verification
sequence. The research document contained only Sections 1–22, and no
implementation paths were changed.

### Exact final commands and outputs

```text
$ .venv/bin/python -m pytest
============================= 147 passed in 6.01s =============================

$ .venv/bin/ruff format --check .
28 files already formatted

$ .venv/bin/ruff check .
All checks passed!

$ .venv/bin/mypy .
Success: no issues found in 12 source files

$ git diff --check
(no output; exit 0)
```

The earlier 5.98-second pytest report and this 6.01-second report are
separate successful runs of the unchanged 147-test suite; the runtime
difference is execution variance, not a behavioral change. This entry records
the exact final run.

### Boundary

No adapter, identifier, credential, functional endpoint, staging, commit, or
push was used. Stop for final adversarial review.

## 2026-09-09 — Final R3 Phase 1 contract-gap correction

### Scope

Perform documentation/framing correction only. The repository-authoritative
branch and complete pre-correction diff were inspected first. Only the R3
research document and the four append-only record files are in scope.

### Corrections recorded

- The selected check-email mapping cannot generate a conflicting duplicate:
  exact breach names deterministically produce the same finding key, kind,
  locator, and empty material. That fixture was removed from
  `XON_CHECK_EMAIL_MATRIX_V1`. Generic R2 conflicting-duplicate tests remain
  the boundary protection; exact duplicate names still exercise R2
  deterministic deduplication.
- The analytics matrix is now
  `XON_ANALYTICS_SENTINEL_REJECTION_MATRIX_V1`. It freezes only
  `XON_ANALYTICS_HTTP_200_NO_MATCH_V1` and rejection cases. Analytics
  positive-success normalization requires separate future framing and is not
  part of the selected implementation files.
- Content-Type derivation now trims only ASCII space/tab at both ends, rejects
  non-ASCII values and all parameters, compares ASCII case-insensitively to
  exactly `application/json`, rejects duplicate header names before derivation,
  and defines the retained-header byte sum as name bytes + one colon byte +
  value bytes + one line-feed byte per entry, capped at 8,192 bytes.
- Normalized R2 serialization is fixed to UTF-8, compact separators,
  deterministic object construction/key ordering, `ensure_ascii=True`
  escaping, no non-standard numbers, final-byte measurement, and no R2 call
  above 65,536 bytes. The verified bounds remain 13,918 XON bytes and 25,910
  normalized-R2 bytes.
- `TransportAttempt` now distinguishes before-status failure, after-status
  body read failure/timeout with preserved HTTP status and bounded prefix,
  complete response, and over-limit response. Contradictory local fixtures or
  trusted fields reject as construction errors; valid attempts with malformed
  untrusted metadata classify conservatively.
- Every selected check-email matrix row now records transport, XON, and R2
  outcomes or visible construction rejection. R1 remains the sole owner of
  comparison, exposure, guarding, and disappearance.

### Boundary

No functional XposedOrNot request, identifier, credential, adapter, HTTP
client, dependency, persistence, scheduler, notification, evidence archive,
R1/R2/R2.5 modification, staging, commit, or push was performed.

## 2026-09-09 — Verify final R3 Phase 1 contract-gap correction

### Verification ordering

The complete requested diff inspection and status review preceded this final
verification sequence.

### Exact final commands and outputs

```text
$ ./.venv/bin/python -m pytest
============================= 147 passed in 6.08s =============================

$ ./.venv/bin/ruff format --check .
28 files already formatted

$ ./.venv/bin/ruff check .
All checks passed!

$ ./.venv/bin/mypy .
Success: no issues found in 12 source files

$ git diff --check
(no output; exit 0)
```

Earlier 5.98s, 6.01s, and this 6.08s pytest outputs are separate successful
runs of the same 147-test suite; their timing differences are execution
variance, not behavior changes.

### Boundary

No adapter, functional endpoint, identifier, credential, dependency, staging,
commit, push, or unrelated file change was made.

## 2026-09-09 — R3 Phase 2 synthetic check-email implementation

### Experiment result

The frozen check-email-only experiment is implemented as an in-memory
normalizer. It accepts only locally constructed trusted context plus bounded
raw transport metadata/body bytes, derives transport classification, strictly
validates the frozen XON success predicate, and passes a deterministic
`fixture-response/1` envelope to the existing R2 adapter. It does not create
requests or perform network I/O.

The synthetic matrix covers successful findings, zero-finding rejection,
echo/schema/parser/media/failure/body-state cases, exact duplicate names,
transport construction rejection, the final-byte guard, and R1 guarding. No
analytics behavior was implemented. No result establishes live API
compatibility, upstream completeness, freshness, coverage, usefulness, or
safety.

### Boundary

Only the selected Phase 2 adapter and synthetic fixture/test files were added;
R1, R2, R2.5, the offline simulator, official-source records, and project
decisions were not changed. No functional endpoint, identifier, credential,
or archive repository was used.

## 2026-09-09 — Verify R3 Phase 2 synthetic experiment

### Exact final verification

The complete implementation diff and status inspection preceded the final
sequence:

```text
$ ./.venv/bin/python -m pytest
============================= 199 passed in 6.87s ==============================

$ ./.venv/bin/ruff format --check .
31 files already formatted

$ ./.venv/bin/ruff check .
All checks passed!

$ ./.venv/bin/mypy .
Success: no issues found in 15 source files

$ git diff --check
(no output; exit 0)
```

The count increased from 147 to 199 through 52 new synthetic adapter tests;
existing Python implementation files remained unchanged. This verifies only
offline deterministic behavior and not live service compatibility or any
upstream completeness/freshness claim.

## 2026-09-09 — Final transport invariant correction and verification

The frozen envelope now rejects retained headers on a pre-status failure,
because no HTTP response headers can exist before a response status. The final
verification sequence after this correction was:

```text
$ ./.venv/bin/python -m pytest
============================= 199 passed in 6.44s ==============================

$ ./.venv/bin/ruff format --check .
31 files already formatted

$ ./.venv/bin/ruff check .
All checks passed!

$ ./.venv/bin/mypy .
Success: no issues found in 15 source files

$ git diff --check
(no output; exit 0)
```

The correction did not change the matrix outcomes or the 147-plus-52 test
count. No live endpoint or identifier was used.

## 2026-09-09 — R3 Phase 2 adversarial correction pass

The selected implementation now catches bounded hostile JSON integer-conversion
`ValueError` at the JSON boundary and returns R2 `unverifiable`. Simultaneous
transport defects follow the newly frozen precedence in Section 12.4, with
HTTP 400-or-greater taking failure precedence once a status exists. Exact
non-BMP serialization evidence and adjacent body, field, collection, header
count, and retained-header-byte boundaries are covered by synthetic tests.

R1 tests now use distinct chronological IDs and assert `guarding_failed` or
`guarding_unverifiable` as appropriate, with no baseline creation,
disappearance, or exposure. No R1/R2 semantics or live-source behavior was
changed.

## 2026-09-09 — Verify R3 Phase 2 adversarial correction pass

The complete corrected diff and status inspection preceded the final sequence:

```text
$ ./.venv/bin/python -m pytest -q
207 passed in 6.09s

$ ./.venv/bin/ruff format --check .
31 files already formatted

$ ./.venv/bin/ruff check .
All checks passed!

$ ./.venv/bin/mypy .
Success: no issues found in 15 source files

$ git diff --check
(no output; exit 0)
```

The final suite includes 60 focused XON tests. No network-capable imports or
calls, credentials, real identifiers, or functional endpoints were used.

## 2026-09-09 — R3 Phase 2 final consistency corrections

Section 14.1 now explicitly freezes oversized generated R2 envelopes as
visible `R2EnvelopeTooLargeError` local construction rejection before R2,
unreachable through the bounded selected XON path. The first-check R1 test
also covers an after-status incomplete attempt and verifies
`response_incomplete`, `guarding_unverifiable`, no baseline, and no exposure.
The build record’s test arithmetic now states 147 pre-R3 tests plus 60 focused
XON tests = 207 total.

## 2026-09-09 — Verify R3 Phase 2 final consistency corrections

Final verification passed: 207 tests in 6.19 seconds, 31 files formatted,
Ruff lint passed, mypy passed for 15 source files, and `git diff --check`
passed. The corrected research and tests remain offline and synthetic.

## 2026-09-09 — Frame R3.5 visible synthetic XON scenarios

### Research question

Can the frozen synthetic XposedOrNot check-email transport and normalization
boundary be exposed through the existing deterministic offline simulator so a
human can observe transport attempt, XON classification, R2 SourceCheck, R1
comparison, and exposure/guard/silence without duplicating logic or implying
live-service compatibility?

### Repository reconciliation

The authoritative checkpoint is clean merge commit `35ef380` on the requested
branch, with the implemented R1, R2, R2.5, and R3 synthetic experiments and
207 passing tests. The older research specifications retain historical
framing-status language; current source and append-only records determine what
has actually run. No material contradiction was found.

### Framing result

Added `RESEARCH_003_5_VISIBLE_XON_SCENARIOS.md` only. It proposes a separate
`r3.5-visible-xon-scenarios/1` scenario family so every existing R2.5 scenario
file and output remains unchanged. The proposed runner dispatches by the
trusted allowlisted adapter identity, calls the existing XON adapter and R2.5
R2 path, constructs only local scan/check IDs, and passes every valid scan to
the existing R1 comparator.

The XON adapter has no separate public XON-classification record. The framing
therefore defines only a non-semantic presentation projection from public
transport classification plus the returned SourceCheck; it does not authorize
a second XON parser. Raw transport metadata and body bytes are represented as
bounded lowercase hex in the proposed scenarios, and malformed untrusted
metadata remains adapter-classified rather than becoming invalid scenario
input. Contradictory local TransportAttempt construction remains exit-code-2
invalid input.

The 17 proposed scenarios cover baseline silence, unchanged findings, new
findings, valid omission-based disappearance, simultaneous findings,
zero-finding rejection, HTTP 404/429/503 failures, malformed bodies and
metadata, incomplete/over-limit bodies, echo mismatch, hostile unknown fields,
overlong integers, local construction rejection, and mixed-source failure with
an independently changing source.

### Boundary

No Phase 2 runner extension, scenario file, source change, test change,
dependency, network request, credential, real identifier, persistence,
notification, scheduler, analytics path, evidence archive change, staging,
commit, push, merge, or live XposedOrNot work was performed. The editable
install setuptools discovery issue remains separate work.

### Decision boundary

Stop for adversarial framing review. Do not implement the proposed Phase 2
files or settle repeated-failure suppression, recovery events, disappearance
confirmation, trivial-change suppression, bark grouping, baseline overload,
minimum actionable bark information, or older-baseline selection.

## 2026-09-09 — Verify R3.5 visible synthetic XON scenario framing

### Verification observation

The required repository checks passed: 207 tests; Ruff format check; Ruff
lint; mypy with no issues in 15 source files; and `git diff --check`. The
complete diff and status review found only the new R3.5 framing document and
the permitted append-only research, build, and progress logs changed.

### Boundary

This verification confirms repository health at the existing checkpoint only.
It does not claim that the proposed runner, scenario files, or XON scenarios
have been implemented or executed. The branch remains unstaged and
uncommitted, and work stops for adversarial framing review.

## 2026-09-09 — Amend R3.5 framing after adversarial self-review

The framing was tightened before handoff: all ledger shorthand now expands
through complete R1 report macros; Scenario 10 explicitly covers a wrong
Content-Type value; and Scenario 17 states the actual lexical source ordering.
No implementation or semantic change was made.

## 2026-09-09 — Verify amended R3.5 framing

The final required verification passed after the framing corrections: 207
tests, Ruff format check, Ruff lint, mypy, and `git diff --check`. The complete
status review still shows only the new framing document and the three
permitted append-only logs. The branch remains unstaged and uncommitted.

## 2026-09-09 — Correct remaining R3.5 framing details

The framing correction preserves the existing scenario family and ownership
boundaries. It fixes the exact 5,088-byte hostile body, permits empty raw
header names without loader pre-classification, freezes trusted source JSON
types and literal examples, completes mixed-source human and machine
projection semantics, freezes Scenario 16's diagnostic object and streams,
defines the explicit filename-to-ID table, makes unexpected public XON
statuses a visible internal projection failure, and records the required
append-only Phase 2 files. No source, test, fixture, dependency, network, or
live-service work was performed.

## 2026-09-09 — Freeze R3.5 XON projection internal error

The xon_projection_invariant contract is now fully frozen for R3.5 only. It
applies when READY transport is followed by an adapter status other than
completed or unverifiable; it discards buffered output, stops before R1 and
later scans, returns exit 2, and emits the exact human or JSON internal-error
form. It is not an invalid scenario and does not alter R2.5 diagnostics.
Phase 2 must test both output modes with a public-adapter test double.

## 2026-09-09 — Verify frozen R3.5 XON projection internal error

The established verification sequence passed: pytest 207 passed in 6.57
seconds, Ruff format reported 32 files already formatted, Ruff lint passed,
mypy found no issues in 15 source files, and git diff --check passed. No
implementation or internal-error test execution was performed.

## 2026-09-09 — Verify corrected R3.5 framing

The exact verification sequence passed: pytest 207 passed in 7.12 seconds,
Ruff format 32 files already formatted, Ruff lint passed, mypy found no issues
in 15 source files, and git diff --check passed. Complete diff inspection
confirmed only the R3.5 framing document and the three permitted append-only
logs changed. No scenario runner or scenario was implemented or executed.

## 2026-09-09 — Execute R3.5 synthetic scenario experiment

Implemented the frozen visible scenario runner and 17 literal synthetic XON
scenario records. The XON transport attempt is constructed locally and passed
unchanged to the committed adapter; synthetic-R2 inputs use the existing R2
normalizer; R1 remains the sole owner of comparison and event semantics. The
experiment covers valid baselines, unchanged/new/disappeared findings,
failure and incomplete precedence, malformed and hostile bodies, metadata
rejection, immediate-prior displacement, mixed-source change, and visible
construction rejection. It makes no claim about live service behavior.

## 2026-09-09 — Verify R3.5 synthetic scenario experiment

The full suite passed with 242 tests. All 16 valid curated scenarios passed in
both human and JSON modes; Scenario 16 produced the frozen exit-2 result; and
controlled mismatch, invalid-input, delegation, byte-count, canonical-output,
and internal-invariant tests passed. No network or live-source operation was
performed.

## 2026-09-09 — Final R3.5 Phase 2 verification correction

After the final focused delegation and identity-type assertions were added,
the exact verification sequence passed with 243 tests; Ruff format and lint,
mypy, and `git diff --check` all passed. The earlier 242-test verification
entry is retained as history and is superseded by this final run.

## 2026-09-09 — Final verification after R3.5 invalid-family correction

The final exact sequence passed with 243 tests in 13.45 seconds; Ruff format
and lint passed, mypy passed across 17 source files, and `git diff --check`
passed. The invalid R3.5 diagnostic path now reports the R3.5 runner version
even when parsing fails before dispatch.

## 2026-09-10 — R3.5 Phase 2 adversarial test-strengthening correction

The Phase 2 review additions freeze independent raw digests and filename-to-ID
aliases for all 17 literal scenarios, exact Scenario 17 human and JSON output,
nested machine-schema shapes, strict oracle nullability, exact immediate-prior
comparison arguments, and structural protection against duplicating XON or R2
semantics in the runner. Existing implementation and scenario bytes were not
changed.

## 2026-09-10 — Verify R3.5 Phase 2 adversarial test strengthening

All 34 curated scenario executions passed in their frozen modes, and the full
suite passed with 252 tests. Ruff format and lint, mypy, and `git diff --check`
also passed. These checks prove synthetic deterministic behavior and fixture
integrity only; they do not prove live-service compatibility, completeness, or
freshness.
