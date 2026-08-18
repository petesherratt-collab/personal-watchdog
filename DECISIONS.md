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
