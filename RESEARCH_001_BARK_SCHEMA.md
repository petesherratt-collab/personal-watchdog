# Research Experiment R1 — Bark schema

**Status: framed, not run.** This document is a proposed research design, not
an implementation specification, a research result, or an accepted product
decision. It deliberately separates the project history in
`PROJECT_HISTORY.md`, recorded research in `RESEARCH_LOG.md`, accepted
constraints in `DECISIONS.md`, and the provisional choices below.

R1 is the next proposed experiment after Base Zero. It must remain offline,
synthetic, deterministic, and approval-gated.

## Research question

Can deterministic observations, compared only across exactly comparable source
checks, be converted into rare and truthful bark events without turning a
failed, incomplete, blocked, malformed, timed-out, or unverifiable check into
“not found” or disappearance?

## Hypotheses

1. A bounded normalized observation with an explicit stable identity can be
   compared deterministically across two valid results from the same source
   contract.
2. Exact set comparison plus an explicit material-field policy can distinguish
   `new`, `unchanged`, `changed`, and `disappeared` without relying on prose or
   model judgement.
3. A bark event can be limited to material transitions in comparable results;
   baseline establishment, unchanged results, and non-comparable results will
   not bark.
4. The failure and unverifiability boundary can prevent absence or
   disappearance claims even when a source returns an empty, partial, malformed,
   blocked, or otherwise unusable result.

R1 falsifies a hypothesis if the required distinction cannot be made
deterministically from the proposed fields, or if a scenario violates the
truthful-failure rule.

## Scope

R1 will frame and, after approval, test only an in-process comparison model
using synthetic opaque identifiers and predetermined source results. The
experiment may describe one or more named fixture sources, but those fixtures
are scenarios to be specified later, not files created by this framing step.

The proposed model covers:

- one scan attempt containing an ordered source-check plan;
- bounded normalized observations;
- source-check and scan-attempt terminal statuses;
- comparison of a current result with an explicitly selected baseline; and
- a deterministic bark-event candidate record.

## Exclusions

R1 does not authorize or include:

- application code, tests, fixtures, databases, SQLite schemas, or persistence;
- XposedOrNot, Maigret, or any other live or external adapter;
- network calls, credentials, real identifiers, external accounts, or
  notifications;
- a GUI, CLI, scheduler, background service, report, export, or deployment;
- raw-page retention, complete personal identifiers, or whole-site evidence;
- a trust claim about timestamps, source truth, identity ownership, or safety;
- an accepted schema decision. Every schema and rule in this document is
  provisional until an approved experiment and explicit decision.

## Proposed terminology

### Scan attempt

A **scan attempt** is one locally initiated run over a declared scope of source
checks for one synthetic subject. It records an opaque `scan_id`, the synthetic
`subject_ref`, a non-empty canonical scope, an operational execution order, a
local or fixture `recorded_at` value marked unverified, and one terminal
source-check result for each planned invocation.

A scan attempt exists even when every source check fails. Its aggregate status
describes whether its results are comparable, not whether observations were
found.

### Source check

A **source check** is one planned invocation of one named source through one
explicit adapter for one synthetic subject within a scan attempt. It has an
opaque `source_check_id`, `subject_ref`, `source_id`, relevant
`canonical_scope`, `adapter_id`, `adapter_version`, `schema_version`,
`normalization_version`, terminal status, bounded diagnostic metadata, and zero
or more normalized observations only when the result is complete and valid.

The proposed terminal statuses are:

- `completed`: the source returned a complete structurally and semantically
  valid result. Zero observations is valid.
- `failed`: no usable source result was produced, such as a transport or
  process failure, or a timeout before a result could be established.
- `unverifiable`: a result or partial result exists, but completeness or
  meaning cannot be established, such as blocked, malformed, truncated,
  contradictory, partial, or validation-failing output.

Neither `failed` nor `unverifiable` is an empty successful result.

### Observation

An **observation** is one bounded, normalized, factual claim returned by a
`completed` source check. It has:

- a stable `finding_key` within the source and adapter contract;
- an observation `kind`;
- a canonical source locator or source-defined identity component;
- a `material` object containing declared fields whose changes may matter; and
- an optional `context` object containing bounded fields that are displayed or
  retained for comparison context but do not, by themselves, cause a bark.

R1 observations contain only synthetic or non-identifying values. They do not
contain complete email addresses, secrets, raw pages, executable content, or
unbounded source responses.

For R1, the proposed observation fingerprint is the canonical representation of
`finding_key`, `kind`, `locator`, and `material`. Timestamps, durations, retry
counts, diagnostic text, `reason_codes`, and other diagnostic metadata are not
fingerprint inputs.

### Diagnostic metadata and status guards

Diagnostic metadata explains how a source check reached its status. Proposed
diagnostic fields include unverified timestamps, duration, retry count, bounded
diagnostic text, and `reason_codes`. These fields never enter an observation
fingerprint or material comparison. `reason_codes` are source-status metadata,
not observations.

A status transition may produce a **status-guard event** when it prevents a
comparison. For a failed current source check, the comparison result is
`not_comparable` with an explicit reason code and a separate
`guarding_failed` event. For an unverifiable current source check, the result
is `not_comparable` with an explicit reason code and a separate
`guarding_unverifiable` event. These guard events are emitted even when no
previous successful baseline exists: they report inability to guard, not an
exposure change. A guard records the source and current scan references, the
current source-check status, any available prior baseline/status references,
and unique sorted reason codes. Missing prior references are represented as
absent or null rather than preventing the guard. Guards never become
`exposure-new`, `exposure-changed`, or `exposure-disappeared` events, do not
assert absence, and do not enter an observation fingerprint. Diagnostic-only
changes never produce exposure barks.

### Comparison result

A **comparison result** is the deterministic result for one finding key or
one source when an explicitly selected baseline and current source check are
compared. Proposed per-key result kinds are:

- `new`: the `finding_key` is absent from the comparable baseline and present
  currently;
- `unchanged`: the `finding_key` is present in both and all material fields are
  equal;
- `changed`: the `finding_key` is present in both and at least one material
  field differs;
- `disappeared`: the `finding_key` is present in the baseline and absent
  currently, but
  only when the current source check is comparable; and
- `not_comparable`: the source checks cannot support an absence or change
  claim.

`failed` and `unverifiable` are source-check statuses, not comparison results.
They must be retained as explicit reasons for `not_comparable`, never
collapsed into `disappeared` or an empty current set. A failed current status
also derives a separate `guarding_failed` event; an unverifiable current
status derives a separate `guarding_unverifiable` event. Neither guard event
is a comparison result or an exposure bark.

### Bark event

A **bark event** is a proposed local, deterministic record that a material
comparison transition deserves attention. R1 proposes one bark event for each
`new`, `changed`, or `disappeared` comparison result from a comparable source
check. It proposes no bark for `baseline`, `unchanged`, `not_comparable`,
`failed`, or `unverifiable`, and no guard event is itself barkable.

“Event” here means a comparison result in the experiment model. It does not
authorize a notification, network transmission, user interface, or durable
event ledger.

## Proposed schemas

These are illustrative canonical records for the experiment, not database
schemas and not accepted implementation interfaces. Objects use strings,
integers, booleans, null, arrays, and nested objects only. Floating-point
values, raw responses, complete identifiers, duplicate set members, and
unknown fields are rejected or make the result unverifiable rather than being
silently ignored.

### Scan attempt

```json
{
  "scan_id": "scan-r1-001",
  "subject_ref": "subject-r1-a",
  "scope_refs": ["fixture-source-a/public-profile-v1"],
  "execution_order": ["check-r1-001"],
  "source_statuses": ["fixture-source-a/public-profile-v1=completed"],
  "recorded_at": "2026-08-18T00:00:00Z",
  "outcome": "completed"
}
```

`scope_refs` is a non-empty unique sorted set of canonical source/scope
references, with one scope reference per source in R1. `source_statuses` is a
unique sorted set of canonical `source_id/canonical_scope=status` entries.
`execution_order` preserves operational order and is non-material; it is not
sorted for comparison. The timestamp is unverified metadata and does not
control comparability.

The aggregate outcomes are exact:

- `completed`: every source in the non-empty declared scope completed;
- `incomplete`: at least one source completed and at least one failed or was
  unverifiable;
- `failed`: no source completed; and
- `empty_scope`: invalid request because the declared scope is empty.

An empty declared scope is rejected during scan-plan construction or
validation with a domain-specific invalid-input error such as
`InvalidScanPlanError`. It produces no scan result, baseline, comparison,
exposure event, or guard event because no source check was attempted.

Each declared source must have one terminal source-check status. A missing
terminal result is treated as a failed source check for aggregate guarding and
contributes no observations.

### Source check

```json
{
  "source_check_id": "check-r1-001",
  "scan_id": "scan-r1-001",
  "subject_ref": "subject-r1-a",
  "source_id": "fixture-source-a",
  "canonical_scope": ["public-profile-v1"],
  "adapter_id": "fixture-adapter",
  "adapter_version": "1.0",
  "schema_version": 1,
  "normalization_version": 1,
  "status": "completed",
  "reason_codes": [],
  "diagnostics": {
    "recorded_at": "2026-08-18T00:00:00Z",
    "duration_ms": 0,
    "retry_count": 0,
    "text": "synthetic completed result"
  },
  "observations": []
}
```

For `failed` or `unverifiable` checks, `observations` is absent or empty and
`reason_codes` must explain the non-comparable status. When selected as the
current check, `failed` derives a separate `guarding_failed` event and
`unverifiable` derives a separate `guarding_unverifiable` event, including when
no previous successful baseline exists. Bounded diagnostics may be retained,
but partial candidates are never accepted observations and cannot enter a
baseline or comparison. An empty observations array is a successful
zero-observation result only when `status` is `completed`.

### Observation

```json
{
  "finding_key": "fixture-source-a|profile|profile-r1-001",
  "kind": "profile",
  "locator": "profile-r1-001",
  "material": {
    "exposure_class": "public",
    "display_state": "active"
  },
  "context": {
    "label": "synthetic example",
    "observed_at": "2026-08-18T00:00:00Z"
  }
}
```

`finding_key`, `kind`, and `locator` identify the claim. A change to an
identity component is represented as one `disappeared` key and one `new` key,
not as an in-place `changed` result. The source contract must declare which
`material` fields exist; an undeclared field is a schema error.

### Comparison result

```json
{
  "comparison_id": "compare-r1-001",
  "subject_ref": "subject-r1-a",
  "source_id": "fixture-source-a",
  "canonical_scope": ["public-profile-v1"],
  "adapter_id": "fixture-adapter",
  "adapter_version": "1.0",
  "schema_version": 1,
  "normalization_version": 1,
  "baseline_scan_id": "scan-r1-001",
  "current_scan_id": "scan-r1-002",
  "finding_key": "fixture-source-a|profile|profile-r1-001",
  "result": "changed",
  "changed_field_paths": ["display_state"],
  "reason_codes": []
}
```

For `not_comparable`, `finding_key` and `changed_field_paths` may be absent,
and `reason_codes` must identify the failed comparability rule. A failed or
unverifiable current source status must also produce exactly one separate
status-guard event of the corresponding kind.

### Status-guard event

```json
{
  "guard_id": "guard-r1-001",
  "subject_ref": "subject-r1-a",
  "source_id": "fixture-source-a",
  "baseline_scan_id": "scan-r1-001",
  "current_scan_id": "scan-r1-002",
  "guard_kind": "guarding_unverifiable",
  "prior_status": "completed",
  "current_status": "unverifiable",
  "reason_codes": ["blocked"]
}
```

`baseline_scan_id` and `prior_status` may be absent or null when the current
failed or unverifiable check is the first check or otherwise has no previous
successful baseline. `guard_kind` is exactly `guarding_failed` when
`current_status` is `failed` and exactly `guarding_unverifiable` when
`current_status` is `unverifiable`. This is a diagnostic guard, not an
exposure comparison or bark. Its reason codes are a unique sorted set and
must contain an explicit status reason.

### Bark event

```json
{
  "bark_id": "bark-r1-001",
  "comparison_id": "compare-r1-001",
  "subject_ref": "subject-r1-a",
  "source_id": "fixture-source-a",
  "baseline_scan_id": "scan-r1-001",
  "current_scan_id": "scan-r1-002",
  "finding_key": "fixture-source-a|profile|profile-r1-001",
  "bark_kind": "exposure-changed",
  "changed_field_paths": ["display_state"]
}
```

The proposed `bark_id` is unique within the experiment output. Whether it is a
stable cross-run identifier, whether repeated transitions are deduplicated,
and whether any non-risk descriptive label exists are unresolved decisions
below. R1 defines no severity field and makes no claim about risk or danger.

## Exact comparability rules

Two source checks are comparable only if every rule below holds:

1. Both checks refer to the same synthetic `subject_ref`.
2. Both checks have the same `source_id`.
3. Both checks have exactly the same relevant `canonical_scope` unique sorted
   set.
4. Both checks have the same `adapter_id`.
5. Both checks have the same `adapter_version`.
6. Both checks have the same `schema_version`.
7. Both checks have the same `normalization_version`.
8. Both checks have `status: completed`.
9. Both checks passed structural and semantic validation, including allowed
   types, NFC strings, bounded sizes, declared fields, unique `finding_key`
   values, and the declared list semantics below.
10. Both checks describe the same declared scope and material-field policy
    through the matching scope and schema versions. A changed source scope,
    adapter, adapter version, schema, normalization rule, or material-field
    policy is not silently compared.
11. The baseline and current roles are explicit. Wall-clock timestamps are not
    used to infer order or truth.
12. Observation arrays are represented in their declared sorted-by-
    `finding_key` form, but operational execution order is not compared.
13. A completed zero-observation result is comparable. It can support
    disappearance claims against a valid baseline.
14. A `failed` or `unverifiable` check is never comparable, even if its payload
    happens to contain an empty list or partial candidates.
15. In a multi-source scan, comparability is decided per source. A non-
    comparable source makes the aggregate scan incomplete for absence claims;
    it does not invalidate a separate source whose two checks are comparable.

If any rule fails, the comparison result is `not_comparable` with a bounded
reason code. No absence or disappearance result may be emitted for that source.
R1 has no `contract_version` field; it must not be used as a substitute for any
member of the exact identity list above.

## Declared list semantics

R1 does not apply a blanket input-order normalization. Each collection has
declared semantics:

- `scope_refs`, `canonical_scope`, and `source_statuses` are unique sorted sets;
- observations are keyed and represented in sorted order by `finding_key`;
- `changed_field_paths` and `reason_codes` are unique sorted sets;
- scan execution order is operational and non-material; its recorded order is
  preserved and is not used for comparison; and
- list values inside observation fields remain ordered and material unless the
  field schema explicitly declares that particular field set-like.

Duplicate values in a declared set are invalid. A list whose field schema does
not declare set-like semantics cannot be silently sorted or deduplicated.

## Exact material-change rules

For two comparable observations with the same `finding_key`:

1. Canonicalize only according to the declared source contract, `schema_version`,
   `normalization_version`.
2. Compare the complete `material` objects as canonical objects. A material
   key added, removed, or changed is a material change.
3. Emit changed field paths as the unique sorted set `changed_field_paths`.
4. Any change to `context` or diagnostic metadata, including timestamps,
   durations, retry counts, diagnostic text, or `reason_codes`, is non-material
   and produces `unchanged` if `material` is equal and source status remains
   comparable.
5. A source-status transition may produce a separate status guard, but
   diagnostic-only changes and guards never produce `exposure-new`,
   `exposure-changed`, or `exposure-disappeared`.
6. Any change to `finding_key`, `kind`, or the identity-bearing `locator`
   is not an in-place material change; it becomes `disappeared` plus `new`.
7. Observation arrays are compared by `finding_key` after applying their
   declared sorted-list representation. Ordering inside a material observation
   field remains material unless that field explicitly declares set-like
   semantics.
8. Duplicate keys, undeclared material fields, invalid values, or
   non-canonical representations make the source result unverifiable rather
   than producing a best-effort comparison.

The proposed bark rule is therefore exact: emit only an
`exposure-new`, `exposure-changed`, or `exposure-disappeared` bark derived from
the corresponding `new`, `changed`, or `disappeared` comparison result after
rules 1–8 succeed. No bark is emitted for metadata-only changes or directly
from an adapter result.

## Baseline behaviour

- The first `completed` source check for a `subject_ref` and exact source,
  canonical-scope, adapter, schema, and normalization identity creates
  a baseline. Its observations are labelled `baseline`; it emits no bark.
- A first completed zero-observation check is a valid empty baseline and emits
  no bark.
- A failed or unverifiable first check creates no baseline.
- A later completed check after no baseline creates a new baseline and emits no
  bark, even if it contains observations.
- A comparable current check with a new finding emits `new` and an
  `exposure-new` bark.
- A comparable current check with the same finding key and equal material emits
  `unchanged` and no bark.
- A comparable current check with the same finding key and different material
  emits `changed` and an `exposure-changed` bark.
- A comparable current zero-observation check emits `disappeared` for each
  baseline finding key that is absent currently, with an
  `exposure-disappeared` bark for each.
- A failed current check emits `not_comparable` with an explicit reason and a
  separate `guarding_failed` event; it emits no disappearance or exposure
  bark. An unverifiable current check emits `not_comparable` with an explicit
  reason and a separate `guarding_unverifiable` event; it emits no
  disappearance or exposure bark. Either guard is emitted even without a
  previous successful baseline.
- With multiple sources, only source pairs that satisfy every comparability
  rule may produce comparison results. A failed or unverifiable source cannot
  erase another source's baseline or findings.

## Required synthetic scenarios

These are scenario descriptions for a later approved experiment. This framing
step creates no fixtures.

1. First completed check with zero observations: empty baseline, no bark.
2. First completed check with one observation: baseline, no bark.
3. Repeated completed check with identical observations in a different input
   order: `unchanged`, no bark.
4. A completed check adds one observation: one `new` bark.
5. A completed check changes one declared material field: one `changed` bark
   naming exactly that field.
6. A completed check changes only context: `unchanged`, no bark.
7. A completed check removes one baseline observation: one `disappeared` bark.
8. A current source check fails before producing a result: `not_comparable`
   with an explicit reason plus a separate `guarding_failed` event, no bark,
   and no disappearance, even without a baseline.
9. A current source check is blocked, malformed, partial, truncated, or
   contradictory: `not_comparable` with an explicit reason plus a separate
   `guarding_unverifiable` event, no bark, and no disappearance, even without a
   baseline.
10. A first check fails or is unverifiable, followed by a completed check:
    establish a baseline, no bark.
11. Each of subject ref, source ID, canonical scope, adapter ID, adapter
    version, schema version, and normalization version changes independently:
    `not_comparable`, no absence claim.
12. A diagnostic-only change in timestamp, duration, retry count, diagnostic
    text, or reason codes: no material change or exposure bark; a status change
    may produce only a status guard.
13. Duplicate finding keys, undeclared material fields, or duplicate set values:
    reject as
    unverifiable, no comparison.
14. A list value changes order in a field declared ordered: material change. A
    list value changes order in a field explicitly declared set-like: no change.
15. A multi-source scan has one comparable source and one unverifiable source:
    compare only the valid source and suppress absence claims for the other.
16. An aggregate with every source completed is `completed`; one with at least
    one completed and one failed or unverifiable source is `incomplete`; one
    with no completed source is `failed`; and an empty scope is `empty_scope`
    and invalid.
17. A failed or unverifiable source with bounded partial candidates retains
    diagnostics only; no candidate enters a baseline or comparison, and the
    corresponding guard remains separate from exposure events.
18. A material change is repeated in a later scan: record the result for the
    experiment, while leaving deduplication and notification policy unresolved.

## Falsification conditions

R1 fails if any of the following occurs in a later approved experiment:

- identical canonical inputs represented with different input order for a
  declared sorted-set field or observation array produce different comparison
  results;
- an ordered list value is silently sorted or treated as set-like;
- a changed declared material field produces `unchanged` or no bark;
- a context-only change produces `changed` or a bark;
- a failed, blocked, malformed, partial, timed-out, or unverifiable check
  produces `disappeared`, `not found`, or a bark caused by absence;
- a completed zero-observation check cannot support a deterministic comparison
  with a valid baseline;
- a baseline establishment emits a bark;
- duplicate keys, unknown fields, invalid types, or changed source scope are
  silently accepted as comparable;
- a mismatch in subject ref, source, canonical scope, adapter, adapter version,
  schema version, or normalization version is treated as comparable;
- a multi-source failure causes a valid comparable source to lose its own
  result, or causes an invalid source to make an absence claim; or
- the proposed fields cannot express the source's uncertainty without hiding it
  in a generic empty result.

## Stopping conditions

Stop R1 before implementation or expansion if:

1. An explicit stable observation identity cannot be defined for a synthetic
   source without source-specific assumptions that the schema hides.
2. “Material” cannot be bounded to declared fields and deterministic equality.
3. The experiment requires live network access, real personal data, a new
   dependency, persistence, notifications, or an adapter to answer its first
   question.
4. The same input can reasonably yield both a bark and no bark under the
   proposed rules.
5. The design begins to claim source completeness, trustworthy time, identity
   ownership, safety, or comprehensive coverage.
6. A failed or unverifiable result cannot remain visibly distinct from a
   successful zero-observation result.
7. The experiment would need a broader product specification before its
   smallest falsifiable question can be tested.

## Unresolved decisions

All choices in this section and all schemas and rules above are **provisional**.
No R1 schema decision has been accepted.

- Should `finding_key` be supplied by each source contract, derived from a
  canonical identity tuple, or both with cross-checking?
- Which material fields are meaningful for each source kind, and who is allowed
  to change that field policy or its version?
- Should an identity change always be represented as `disappeared` plus `new`,
  or can a source-specific contract justify `changed`?
- How should repeated identical material transitions be deduplicated, grouped,
  acknowledged, or re-barked?
- Is any non-risk descriptive bark label useful, and can it be defined without
  implying confidence in identity or source truth?
- Should a bark event have a stable cross-run identifier, or only identify its
  comparison and finding key?
- Which bounded reason codes are sufficient for failed versus unverifiable
  checks without recording sensitive diagnostics?
- How should an explicitly corrected or superseded baseline be represented?
- Are unverified timestamps needed in the comparison output at all, given that
  they cannot prove order or truth?
- What evidence, if any, is necessary for a later experiment, and how can it
  remain selective, local, and independent of the comparison result?

## Approval boundary

This document frames R1 only. It does not authorize implementation, fixture
creation, tests, persistence, adapters, network calls, notifications, or a
commit. The next action requires explicit approval of the research question,
scope, proposed scenarios, and stopping conditions.
