# Research Experiment R2 — Adapter boundary

**Status: framed, not run.** This document is a provisional research design,
not an adapter implementation, a source contract, a research result, or an
accepted product decision. It preserves the distinction between project
history, R1 comparison results, R2 normalization observations, and future
design choices.

R2 is an offline, synthetic, deterministic experiment. It deliberately uses a
made-up response format rather than XposedOrNot, Maigret, or another real
service.

## Research question

Can a bounded, untrusted adapter response be converted into an R1 source check
while preserving the distinctions among:

- explicitly completed with observations;
- explicitly completed with zero observations;
- failed;
- unverifiable;
- malformed;
- incomplete; and
- incompatible?

The adapter boundary must never turn an invalid, partial, incompatible, or
uncertain response into a clean zero-observation result. It must also never
produce an R1 comparison result or bark event.

## Hypotheses

1. A versioned, bounded synthetic envelope can be validated from bytes without
   accepting unknown fields, duplicate keys, non-standard JSON constants,
   unbounded values, or partial candidates.
2. A valid `completed` envelope with `results: []` can remain distinct from a
   failed, malformed, incomplete, or incompatible envelope after normalization.
3. Valid result records can be converted into the existing immutable R1
   observations while preserving R1-declared set-like and ordered-list
   semantics.
4. Every unusable response category can map to an R1 failed or unverifiable
   source check with no accepted observations, allowing R1—not the adapter—to
   derive comparisons and events.

R2 falsifies a hypothesis if normalization silently accepts an invalid
response, loses the reason for an unusable response, admits a partial
candidate, produces a clean zero-observation result for a non-completed
response, or emits comparison or bark output at the adapter boundary.

## Scope

R2 will frame and, after separate approval, test a pure normalizer whose
untrusted input is `bytes` and whose output is an R1 `SourceCheck` constructed
from trusted local context. The normalizer does not accept a decoded mapping
as its public input. A non-`bytes` call is a caller/programmer contract error,
not an adapter outcome.

The normalizer receives trusted local context for the scan, subject, and
configured `SourceIdentity`; the response bytes themselves are untrusted.

The experiment covers:

- one versioned synthetic response envelope;
- bounded result records containing only synthetic values;
- strict bytes-to-UTF-8-to-JSON parsing;
- explicit response outcome validation;
- response-to-R1 status and observation mapping;
- rejection or truthful classification of malformed, incomplete, and
  incompatible input; and
- passing normalized checks to the existing R1 `compare_scans` function in
  later tests to verify that R1 semantics remain unchanged.

## Exclusions

R2 does not authorize or include:

- XposedOrNot, Maigret, or any real service or real protocol;
- network access, credentials, real identifiers, external accounts, or
  subprocesses;
- a CLI, GUI, scheduler, background service, persistence, database, or report;
- notifications, evidence capture, raw-page retention, or an evidence archive;
- hashing, encryption, external dependencies, or a new runtime dependency;
- comparison logic, bark derivation, severity, risk scoring, or adapter-side
  notifications; or
- changing R1's comparator, accepted semantics, or provisional schema merely
  to accommodate an adapter response.

## Fixed provisional limits

These are concrete R2 limits, not future configuration points. They apply to
the untrusted response and to bounded trusted local diagnostics:

| Limit | Value | Rule |
|---|---:|---|
| Maximum input bytes | `65,536` | Enforced on the raw `bytes` value before UTF-8 decoding or JSON parsing |
| Maximum result count | `100` | `results` must contain no more than 100 items |
| Maximum array items | `100` | Every JSON array, including nested material arrays |
| Maximum object members | `16` | Every JSON object after duplicate-key checking |
| Maximum nesting depth | `8` | Root JSON value is depth 0; each object or array adds one |
| Maximum ordinary string length | `256` Unicode code points | Applies to required strings, keys, and material strings |
| Maximum diagnostic text | `512` Unicode code points | Raw bytes, decoded payloads, and exception text are never retained |
| Maximum reason-code count | `8` | Reason codes are fixed bounded codes, never arbitrary payload text |
| Maximum reason-code length | `64` Unicode code points | Reason codes are validated strings |
| Maximum diagnostic duration | `86,400,000` ms | Trusted local diagnostic metadata only |
| Maximum retry count | `100` | Trusted local diagnostic metadata only |

Lengths are measured after strict UTF-8 decoding. All accepted payload strings
must be non-empty and NFC-normalized. A string containing surrogate code
points, a disallowed float, or a value outside its declared type is invalid.
Limits are rejection limits; truncation never turns an invalid response into a
valid one.

Where an integer is required, validation must use exact integer typing
(`type(value) is int`), never `isinstance(value, int)`, so JSON `true` and
`false` cannot satisfy an integer field. Booleans are accepted only where the
field explicitly permits a boolean. Floating-point values, including values
created from non-standard JSON constants, are never accepted.

## Bytes and JSON parser boundary

The conceptual normalizer boundary is:

```text
normalize_response(raw: bytes, trusted_context: TrustedContext) -> SourceCheck
```

The checks occur in this order:

1. Require `raw` to be a `bytes` instance. A non-`bytes` call is a programmer
   or caller contract error and is not treated as a source result.
2. Check `len(raw) <= 65,536`. An oversized value becomes an R1
   `unverifiable` check with `input_too_large`; it is not decoded or parsed.
3. Decode with strict UTF-8. A decoding error becomes `unverifiable` with
   `invalid_utf8` and no retained exception text.
4. Reject empty or whitespace-only text as `unverifiable` with `blank_input`.
5. Parse one JSON value with duplicate-key detection and a rejecting
   `parse_constant` hook. `NaN`, `Infinity`, and `-Infinity` are parser
   failures, not accepted numbers.
6. Convert JSON decoder errors, duplicate-key errors, non-standard-constant
   errors, and recursion/depth errors into bounded R1 `unverifiable` outcomes
   with fixed reason codes. Do not retain raw input, decoded payloads, or
   exception messages.
7. Validate depth, collection limits, exact object keys, field types, NFC
   strings, outcome rules, result identities, and material values before
   constructing any R1 observation.

The parser must not use the default `json.loads` behavior for duplicate keys or
non-standard constants. A duplicate JSON object key is invalid even when its
repeated values are equal. This is distinct from two result records that carry
the same `finding_key`.

Known parser failures map as follows:

| Parser condition | R2 classification | R1 status | Reason code |
|---|---|---|---|
| input over 65,536 bytes | malformed | `unverifiable` | `input_too_large` |
| empty or whitespace-only input | malformed | `unverifiable` | `blank_input` |
| invalid UTF-8 | malformed | `unverifiable` | `invalid_utf8` |
| invalid JSON syntax | malformed | `unverifiable` | `invalid_json` |
| duplicate JSON object key | malformed | `unverifiable` | `duplicate_json_key` |
| `NaN`, `Infinity`, or `-Infinity` | malformed | `unverifiable` | `nonstandard_json_constant` |
| excessive nesting or parser recursion | malformed | `unverifiable` | `nesting_too_deep` |
| valid JSON with a non-object root | malformed | `unverifiable` | `wrong_top_level_type` |

## Synthetic response envelope

The response is a JSON object. Its required keys are exactly:

```json
{
  "contract_version": "fixture-response/1",
  "source_id": "site-a",
  "outcome": "completed",
  "results": []
}
```

There is no untrusted diagnostic field. The allowed top-level key set is
exactly:

```text
contract_version, source_id, outcome, results
```

Diagnostics consist only of fixed R2 reason codes and separately supplied
trusted local metadata. They never contain raw payload, decoded objects,
parser exceptions, or response bytes.

There is no untrusted `subject_ref`, `canonical_scope`, `adapter_id`,
`adapter_version`, `schema_version`, or `normalization_version` field in the
envelope. There is also no untrusted result `context` object in R2. Those
values cannot be supplied, replaced, or inferred from the response.

### Envelope fields

- `contract_version` is a non-empty NFC string and must equal exactly
  `fixture-response/1`. It identifies the response-envelope format only. It is
  not an R1 identity substitute.
- `source_id` is a non-empty NFC synthetic string and must exactly equal the
  locally requested `SourceIdentity.source_id`, byte-for-byte after decoding.
  A mismatch is incompatible and cannot alter the trusted source.
- `outcome` is exactly one of `completed`, `failed`, `unverifiable`, or
  `incomplete`.
- `results` is a JSON array with at most 100 items. It is required for every
  envelope, including non-completed outcomes.
Unknown fields, missing required fields, wrong field types, non-NFC or empty
strings, excessive collections, excessive nesting, unsupported contract
versions, and invalid result values make the response unusable. They never
produce a completed source check.

### Result records

Each item in `results` has exactly these keys:

```json
{
  "finding_key": "finding-site-a-001",
  "kind": "synthetic-profile",
  "locator": "record-site-a-001",
  "material": {
    "display_state": "active",
    "labels": ["alpha", "beta"],
    "ordered": ["first", "second"]
  }
}
```

No result-level unknown fields are accepted. `finding_key`, `kind`, and
`locator` are required non-empty NFC strings of at most 256 code points.
`material` is required and must be an object with at most 16 members. Its keys
must be non-empty NFC strings declared by the trusted R1 source contract; an
undeclared key is invalid. Declared material fields may be omitted, but an
omitted field is materially different from a present field when R1 compares
the complete material objects.

For this synthetic R2 contract, material values are JSON scalars (`string`,
exact integer, boolean, or null) or arrays containing recursively only those
scalars or arrays. Nested material objects are not part of the contract and
are rejected as unsupported values; a future contract requiring them needs a
new declared normalization version. Arrays preserve order unless the trusted
R1 contract declares that particular field set-like. Set-like fields must be
arrays and are passed through R1 canonicalization; duplicate set members are
invalid. R2 never globally sorts material lists.

The result list preserves operational input order until validation completes.
Accepted observations are constructed with the trusted R1 `SourceIdentity`,
then R1 represents them deterministically by `finding_key`. Input mapping order
cannot affect a normalized record because object keys are validated and R1
canonicalization orders object members.

## Trusted context and boundary ownership

The normalizer receives trusted local context containing the scan ID, source
check ID, `subject_ref`, and the requested immutable `SourceIdentity`. The
identity supplies the canonical scope, source ID, adapter ID and version,
schema version, normalization version, declared material fields, and declared
set-like fields. The response supplies none of these values.

Trusted context is constructed and validated locally before normalization. An
invalid trusted context, such as a wrong trusted field type or invalid R1
identity, is a caller/programmer construction error and may raise the declared
R1 domain error. It is not converted into a result about the untrusted source
bytes.

The ownership boundary is:

| Concern | R2 normalizer | R1 model |
|---|---|---|
| Bytes, UTF-8, JSON, duplicate keys, and constants | validates | not applicable |
| Envelope shape and response contract | validates | not applicable |
| Source outcome classification | maps to source-check status | stores terminal status |
| Result-field validation | validates and constructs observations | enforces observation contract |
| Set-like canonicalization | delegates to configured R1 contract | canonicalizes declared fields |
| Comparison classification | never produces | `compare_scans` only |
| Exposure events | never produces | derived from R1 comparisons only |
| Guarding events | never produces | derived from R1 failed/unverifiable checks |

R2 therefore cannot make a failed or uncertain response look like a comparison,
disappearance, or bark. A normalized `SourceCheck` is the entire adapter
output.

## Normalization outcomes

The following mapping is provisional but complete for the R2 envelope. Every
row produces an R1-compatible source check; only the two valid `completed` rows
can produce `SourceStatus.COMPLETED`.

| Response condition | R2 classification | R1 source status | Accepted observations | R1 consequence |
|---|---|---|---|---|
| supported envelope, `completed`, valid results | completed | `completed` | all validated, deduplicated results | R1 may establish or compare a baseline |
| supported envelope, `completed`, `results: []` | completed-empty | `completed` | none | valid zero-observation baseline/comparison |
| explicit `failed`, `results: []` | failed | `failed` | none | R1 `not_comparable` plus `guarding_failed` |
| explicit `unverifiable`, `results: []` | unverifiable | `unverifiable` | none | R1 `not_comparable` plus `guarding_unverifiable` |
| explicit `incomplete`, regardless of candidate-looking results | incomplete | `unverifiable` | none | R1 `not_comparable` plus `guarding_unverifiable`; no absence claim |
| malformed envelope, parser error, or invalid result | malformed | `unverifiable` | none | R1 `not_comparable` plus `guarding_unverifiable` |
| unsupported contract or source mismatch | incompatible | `unverifiable` | none | R1 `not_comparable` plus `guarding_unverifiable`; no comparison |
| `failed` or `unverifiable` with non-empty results | malformed | `unverifiable` | none | candidates discarded; no clean failure or empty result |

An explicit `incomplete` response always maps to R1 `unverifiable`, even when
its `results` array is empty. Any candidate-looking values attached to an
incomplete, failed, unverifiable, malformed, or incompatible response are
discarded and never become observations. A non-empty `results` array on a
non-completed response produces `response_outcome_mismatch` and
`partial_candidates_discarded` as applicable.

Only a structurally and semantically valid explicit `completed` envelope can
produce an R1 completed source check. Only that envelope with `results: []`
means successfully observed absence. Blank input, malformed JSON, structural
errors, unsupported versions, excessive results, invalid values, and all other
non-completed outcomes become `unverifiable` or `failed` as shown above, never
completed-empty.

### Reason and diagnostic rules

R2 reason codes are fixed bounded strings. They explain normalization and
source-check status, are not observations, and do not enter R1 material
fingerprints. The response itself never supplies reason codes. Proposed fixed
codes include:

- `input_too_large`;
- `blank_input`;
- `invalid_utf8`;
- `invalid_json`;
- `duplicate_json_key`;
- `nonstandard_json_constant`;
- `nesting_too_deep`;
- `wrong_top_level_type`;
- `missing_field`;
- `unknown_field`;
- `invalid_field_type`;
- `invalid_string`;
- `collection_too_large`;
- `too_many_results`;
- `unsupported_response_contract`;
- `response_source_mismatch`;
- `response_outcome_mismatch`;
- `malformed_envelope`;
- `malformed_result`;
- `unsupported_value_type`;
- `duplicate_finding_key_deduplicated`;
- `conflicting_duplicate_finding_key`;
- `partial_candidates_discarded`;
- `response_failed`;
- `response_unverifiable`; and
- `response_incomplete`.

Parser failures retain only the fixed reason code. Separately supplied trusted
local diagnostic text is limited to 512 code points, and trusted local
duration, retry, and reason-code limits are those in the fixed-limits table.
Trusted diagnostics never contain raw bytes, the complete payload, or exception
text, and never alter observation fingerprints, material comparisons, or R1
outcome selection.

## Duplicate result identities

Duplicate JSON object keys are always malformed and are rejected before result
validation. Duplicate result identities are a separate semantic case:

- Two results with the same `finding_key` and the same complete normalized
  record are exact duplicates. They may be deterministically deduplicated to
  one observation and may add the bounded diagnostic code
  `duplicate_finding_key_deduplicated`.
- Two results with the same `finding_key` but any differing identity, ordered
  material value, or normalized material value are conflicting duplicates. The
  entire source response becomes R1 `unverifiable` with
  `conflicting_duplicate_finding_key`; no result from that response is
  accepted.

The first rule is not applied to duplicate JSON object keys. Object-key
duplicates are never deduplicated.

## Identity and version incompatibility

`contract_version` is checked only against the supported response contract.
The payload cannot provide or override R1 identity/version fields. A source ID
mismatch is separately diagnosed as `response_source_mismatch`; an unsupported
response contract is separately diagnosed as
`unsupported_response_contract`. Both are R1 `unverifiable` and cannot enter
comparison.

Adapter ID, adapter version, schema version, normalization version, subject,
and canonical scope are trusted local values. If two normalized completed
checks later differ in any of those values, the existing R1 `compare_scans`
function must produce `not_comparable` with its identity/version reason and no
absence claim. R2 does not recreate or pre-empt those comparison semantics.

## Required synthetic scenarios for a later R2 run

1. Bytes exactly at 65,536 bytes are eligible for parsing; 65,537 bytes become
   `unverifiable` before decoding.
2. Blank bytes, whitespace-only bytes, invalid UTF-8, invalid JSON, duplicate
   JSON keys, and non-standard constants become unverifiable with fixed parser
   reasons.
3. A valid completed response with one result becomes one completed R1 source
   check with one observation.
4. A valid completed response with `results: []` becomes a completed empty R1
   source check and remains distinct from failure.
5. Explicit failed and explicit unverifiable responses with empty results map
   to their stated R1 statuses, with no observations and their corresponding
   guard behavior.
6. Every explicit incomplete response maps to R1 `unverifiable`, including
   incomplete responses with candidate-looking results; no candidate is kept.
7. Missing fields, wrong types, unknown keys at every allowed object level,
   invalid outcome, excessive results, excessive nesting, overlong strings,
   malformed result objects, and invalid material values become unverifiable,
   never completed-empty.
8. An unsupported `contract_version` becomes incompatible/unverifiable and
   cannot use `contract_version` as an R1 identity substitute.
9. A response `source_id` differing from the configured source becomes
   incompatible/unverifiable without changing the configured R1 source.
10. A valid completed response whose result contains an undeclared material
    field becomes unverifiable with no partial observation.
11. Reordering a set-like material list is normalized only because the R1
    fixture contract declares it set-like; reordering an ordered list remains
    material.
12. Exact duplicate result identities may be deduplicated deterministically;
    conflicting duplicate identities make the entire response unverifiable.
13. A normalized completed source check is passed to the existing R1
    `compare_scans` function to establish a baseline or produce R1 comparison
    results; R2 itself produces none.
14. A normalized failed or unverifiable source check reaches R1 as
    `not_comparable` with the corresponding guard and cannot produce
    disappearance, exposure, or a clean zero-observation comparison.
15. One completed normalized source and one unverifiable normalized source in
    the same aggregate scan leave the completed source independently comparable
    while the aggregate remains incomplete.
16. Input mapping order, result-list order, and set-like list order produce
    deterministic normalized records without globally sorting ordered fields.
17. R1 identity/version mismatches are exercised through `compare_scans`, remain
    diagnostically distinct, and never enter comparison.

## Falsification conditions

R2 fails if any of the following occurs:

- the parser decodes an input larger than 65,536 bytes;
- duplicate JSON keys or non-standard constants are accepted;
- a malformed, incomplete, incompatible, failed, or unverifiable response
  becomes a completed zero-observation source check;
- any candidate from a non-completed or invalid response enters an R1
  observation, baseline, or comparison;
- an unsupported response contract or response source ID silently overwrites
  configured R1 identity metadata;
- response `contract_version` is used as a substitute for R1's exact source,
  scope, adapter, adapter-version, schema-version, or normalization-version
  identity;
- R2 emits a comparison result, exposure event, guarding event, or bark;
- R1 receives a different failure, uncertainty, ordering, or materiality
  meaning after normalization;
- ordered material lists are silently sorted or set-like lists are left
  order-sensitive; or
- unbounded, real, identifying, raw, or unsupported data is retained by the
  synthetic boundary.

## Provisional status and approval boundary

All limits, field sets, parser rules, normalization mappings, reason codes, and
scenarios in this document are provisional R2 choices. They are concrete for
the proposed experiment but are not accepted product or schema decisions.

This document frames R2 Phase 1 only. It does not authorize adapter code,
parsers, fixtures, tests, dependencies, network calls, real service research,
or a commit. A later step requires explicit approval of this complete boundary
before implementation or execution. R1 remains the sole owner of comparison,
exposure, and guarding semantics.
