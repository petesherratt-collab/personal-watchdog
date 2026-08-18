# Personal Watchdog decisions

This file records decisions and their current status. A decision is not proof
that the underlying research question has been answered.

## 2026-08-18 — Keep the project speculative

- **Status:** accepted for the current checkpoint
- **Context:** The project began as an open-ended investigation into personal
  exposure monitoring.
- **Decision:** Treat Personal Watchdog as speculative research, not an urgent
  product build or settled product promise.
- **Reasoning:** The coverage, accuracy, identity interpretation, source terms,
  and useful technical direction remain uncertain.
- **Evidence that could change it:** A later experiment or explicit project
  decision could establish a narrower product scope.

## 2026-08-18 — Retain external projects as references, not dependencies

- **Status:** accepted
- **Context:** The Base Zero history names SpiderFoot, XposedOrNot, Sherlock,
  Maigret, Vanish, auto-identity-remove, OnionScan, and ArchiveBox.
- **Decision:** These eight projects are references only. No dependency is
  added merely because a project appeared in earlier research.
- **Reasoning:** Current licences, maintenance, data flows, terms, accuracy,
  and security require separate examination before reuse.
- **Evidence that could change it:** A specific approved experiment with a
  documented licence, data-flow, security, and maintenance review.

## 2026-08-18 — Keep Kibitzr and evidence-collection read-only

- **Status:** accepted
- **Context:** Kibitzr and `/home/peters/evidence-collection/repo/` supplied
  architectural ideas about fetch, extract, compare, notify, integrity, and
  failure recording.
- **Decision:** Use them as read-only architectural reference material, not as
  a destination, dependency, or source of wholesale copied code or documents.
- **Reasoning:** The projects provide principles, while Personal Watchdog's
  scope and privacy boundaries remain unsettled.
- **Evidence that could change it:** A separately approved, scoped review and
  reuse decision.

## 2026-08-18 — Reject whole-document amalgamation

- **Status:** rejected
- **Context:** An earlier documentation amalgamation became a large,
  contaminated corpus with duplication, irrelevant GitHub material, at least
  one wrong XposedOrNot project, and missing Vanish material.
- **Decision:** Do not combine whole documents or codebases. Extract only the
  capability or principle required by a concrete experiment.
- **Reasoning:** The amalgamation obscured provenance and introduced false
  confidence about what had actually been researched.
- **Evidence that could change it:** None for the rejected approach; a future
  narrowly scoped, source-labelled comparison could still be useful.

## 2026-08-18 — Treat the detailed itinerary as approval-gated background

- **Status:** accepted
- **Context:** The current itinerary describes a possible offline Milestone 1
  vertical slice with a ledger, selective evidence, and an independent
  verifier.
- **Decision:** The itinerary is background and a proposal, not automatic
  permission to implement the next milestone.
- **Reasoning:** Implementation would cross an explicit research and approval
  boundary.
- **Evidence that could change it:** Explicit approval of a defined milestone
  and its exact scope.

## 2026-08-18 — Preserve truthful failure semantics

- **Status:** accepted
- **Context:** A source can be blocked, unavailable, malformed, timed out,
  incomplete, or unverifiable.
- **Decision:** Never convert such a result into “not found,” a clean scan, or a
  disappearance claim. A successful comparable zero-observation result remains
  distinct.
- **Reasoning:** Absence claims are unsafe when the source did not produce a
  comparable result.
- **Evidence that could change it:** None without a new, explicitly justified
  semantics; implementation tests must enforce this decision.

## 2026-08-18 — Leave the bark definition open

- **Status:** provisional
- **Context:** The documents suggest that changes between comparable scans may
  matter, but no bark definition has been experimentally validated.
- **Decision:** Do not claim that any observation, change, or failure is a
  validated bark event yet.
- **Reasoning:** The project needs a deterministic, rare, truthful experiment
  before it chooses alert semantics.
- **Evidence that could change it:** A later offline comparator experiment with
  explicit success and failure signals.

## 2026-08-18 — Next research question

- **Status:** provisional
- **Context:** Base Zero is complete without watchdog behaviour.
- **Decision:** The next proposed question is whether deterministic
  observations can be converted into rare, truthful bark events.
- **Reasoning:** This is the smallest question that can test meaning before
  persistence or live integration.
- **Evidence that could change it:** A decision to narrow or replace the
  project's research objective.

## 2026-08-18 — Keep R1 schema choices provisional

- **Status:** accepted
- **Context:** `RESEARCH_001_BARK_SCHEMA.md` frames the next experiment but has
  not been run.
- **Decision:** Do not treat any R1 schema, comparability rule, material-change
  rule, baseline rule, bark rule, or unresolved choice as an accepted design
  decision. They remain provisional until an approved experiment produces
  evidence and a later decision explicitly accepts them.
- **Reasoning:** Framing a research experiment must not be mistaken for a
  research result or a settled product specification.
- **Evidence that could change it:** An approved R1 run and an explicit,
  evidence-backed decision record.

The following are provisional R1 framing resolutions, not accepted schema
decisions: comparability matches `subject_ref`, `source_id`,
`canonical_scope`, `adapter_id`, `adapter_version`, `schema_version`, and
`normalization_version`; diagnostic metadata is excluded from observation
fingerprints; list semantics are declared per field; failed or unverifiable
checks contribute no accepted observations; and aggregate outcomes are
`completed`, `incomplete`, `failed`, or invalid `empty_scope` as defined in R1.

## 2026-08-18 — Clarify R1 guard-event semantics

- **Status:** provisional R1 resolution; not an accepted product or schema
  decision
- **Context:** A pre-implementation consistency review correctly stopped on a
  material ambiguity: R1 described `not_comparable` and status guards, while
  the approved behavioural cases required the exact names
  `guarding_failed` and `guarding_unverifiable`.
- **Decision:** Keep `guarding_failed` and `guarding_unverifiable` as separate
  guard-event kinds. A failed or unverifiable current source check produces
  `not_comparable` with an explicit reason code and the corresponding guard.
  Guards are emitted even without a prior successful baseline and can never be
  exposure events. Reject an empty declared scope during plan construction or
  validation with a domain-specific `ValueError` subclass such as
  `InvalidScanPlanError`; it produces no result or event because no check was
  attempted.
- **Reasoning:** The comparison classification, comparison reason, derived
  exposure events, and derived guarding events must remain distinct so failure
  and uncertainty cannot imply exposure change.
- **Evidence that could change it:** Only an approved R1 result or a later
  explicitly accepted design decision. R1 remains framed and unrun.
