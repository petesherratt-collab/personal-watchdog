# Research Experiment R2.5 — Visible offline simulator

**Status: framed, not implemented or run.** This document is a provisional
research design. It does not add a simulator, scenario fixtures, a CLI, a
policy decision, persistence, or a live adapter.

## Research question and repository reconciliation

Can the existing R1 comparison model and R2 bytes-first normalizer be exposed
through a small, deterministic, human-readable offline scenario runner without
adding comparison semantics, and can that runner make later bark-policy
questions observable rather than silently deciding them?

The repository is authoritative for the existing boundary:

- R1 owns `ScanPlan`, `SourceCheck`, `ScanAttempt`, `compare_scans`, comparison
  kinds, exposure events, and guarding events.
- R2 accepts untrusted `bytes`, validates the invented response envelope, and
  returns only an R1 `SourceCheck`.
- R2 does not compare scans or emit exposure or guarding events.
- Failed, unverifiable, malformed, incomplete, and incompatible responses do
  not become completed-empty checks.
- R1 compares only completed checks with the exact source identity and
  material policy required by its existing implementation.

The R1 and R2 design documents retain the words “framed, not run” because
they are provisional design artifacts. The append-only research and build
records separately document the approved synthetic implementations and the
101-test result at the R2 handoff. This framing treats those as two scopes of
status, not as permission to change R1 or R2 semantics.

The desktop packaging observation is retained as a separate gotcha: `pip
install -e '.[dev]'` failed because setuptools discovered both `data` and
`personal_watchdog` as top-level packages. Direct installation of pytest, Ruff,
and mypy succeeded. R2.5 does not fix packaging; a packaging change requires a
separate task.

## Claims and non-claims

### Experimental claim

Within synthetic scenario files, a thin orchestrator can make the existing R2
normalization status, R1 comparison result, exposure-event candidates, and
guarding events visible in chronological order while preserving deterministic
serialization and truthful failure semantics.

The experiment can also expose which sequences are currently determined by
R1/R2 and which user-facing bark choices are not determined by them.

### Non-claims

R2.5 does not establish source truth, source coverage, identity ownership,
useful alert frequency, risk, severity, notification usefulness, or live
protocol compatibility. It does not validate any real identifier, service,
adapter, scheduler, persistence model, or evidence-retention policy.

An R1 `ExposureEvent` is an existing deterministic comparison output. R2.5
does not promote it to a notification, a severity judgement, or a settled
product bark policy. No scenario result is evidence about a real person or
source.

## Exact ownership boundary

The proposed runner is orchestration and presentation only.

```text
scenario file
    -> validate trusted scenario structure
    -> construct R1 SourceIdentity and R2 TrustedContext
    -> provide simulated bytes, or construct an explicit local failure
    -> existing R2 normalize_response(bytes, trusted_context)
    -> existing R1 ScanAttempt.create(...)
    -> existing R1 compare_scans(previous_scan, current_scan)
    -> compare actual projections with trusted scenario expectations
    -> human or canonical JSON output
```

The runner must not copy or reimplement any of these R1 decisions:

- source identity comparability;
- completed, failed, or unverifiable source semantics;
- observation canonicalization or set-like field handling;
- baseline creation;
- new, unchanged, changed, disappeared, or not-comparable results;
- changed field paths;
- exposure-event derivation; or
- guarding-event derivation.

The runner may validate the scenario envelope, sequence numbers, references,
input representation, and expected-output shape. It may project immutable R1
records into output dictionaries. Those checks are scenario integrity checks,
not a second comparator.

## Deterministic scenario-file schema

Phase 2 should use one JSON file per scenario with a strict,
duplicate-key-aware parser. Each file describes exactly one scenario. The
top-level key set is exactly:

```json
{
  "scenario_version": "r2.5-visible-offline-simulator/1",
  "scenario_id": "r25-s01-baseline-silence",
  "subject_ref": "subject-r25-01",
  "sources": [],
  "scans": []
}
```

The scenario schema is deterministic and synthetic:

| Field | Rule |
|---|---|
| `scenario_version` | Exact string `r2.5-visible-offline-simulator/1`. |
| `scenario_id` | Exact ASCII syntax `^[a-z0-9][a-z0-9._-]{0,127}$`; the one-file runner validates this syntax but cannot enforce uniqueness across files. |
| `subject_ref` | Non-empty synthetic identifier; no email address or real identity. |
| `sources` | Non-empty list of trusted source identities. |
| `scans` | Non-empty chronological list with contiguous `scan_order` values starting at 1. |

Each `sources` entry has exactly `source_ref`, `source_id`,
`canonical_scope`, `adapter_id`, `adapter_version`, `schema_version`,
`normalization_version`, `material_fields`, and `set_like_fields`. These are
trusted scenario inputs and are used to construct the existing R1
`SourceIdentity`; they are not read from the response bytes. `source_ref` lets
one scenario explicitly exercise two trusted versions of the same synthetic
source ID. The `sources` array is sorted by unique `source_ref`.

Each scan has exactly `scan_order`, `source_order`, `checks`, and `expected`.
`scan_id` is not authored: it is constructed as
`{scenario_id}:scan-{scan_order:03d}`. `source_order` is a permutation of the
source references used by that scan, and each `checks` list contains exactly
one check for each listed source in exactly that order. Each check has exactly
`source_ref`, `input`, and `expected`. The position in `source_order` is
operational and is not a comparison field.

The complete revised JSON shape is:

```json
{
  "scenario_version": "r2.5-visible-offline-simulator/1",
  "scenario_id": "r25-s01-baseline-silence",
  "subject_ref": "subject-r25-01",
  "sources": [
    {
      "source_ref": "A1",
      "source_id": "synthetic-source-a",
      "canonical_scope": ["synthetic-scope-a-v1"],
      "adapter_id": "synthetic-r2-adapter",
      "adapter_version": "1.0",
      "schema_version": 1,
      "normalization_version": 1,
      "material_fields": ["display_state", "labels", "ordered"],
      "set_like_fields": ["labels"]
    }
  ],
  "scans": [
    {
      "scan_order": 1,
      "source_order": ["A1"],
      "checks": [
        {
          "source_ref": "A1",
          "input": {"utf8_text": "..."},
          "expected": {
            "r2": {
              "status": "completed",
              "reason_codes": [],
              "finding_keys": ["finding-a"]
            }
          }
        }
      ],
      "expected": {
        "r1": {
          "baseline_created_sources": ["synthetic-source-a"],
          "comparisons": [],
          "exposure_events": [],
          "guarding_events": []
        }
      }
    }
  ]
}
```

The `expected.r2` object belongs to one check. The one `expected.r1` object
belongs to one scan and is the complete expected R1 `ComparisonReport`
projection for that scan. No expected R1 data is nested under a check.

The runner receives one scenario file at a time. It cannot enforce that
`scenario_id` is unique across files. The Phase 2 test suite must load all ten
curated fixture files and reject duplicate `scenario_id` values across that
set.

`input` has exactly one of these forms:

```json
{"utf8_text": "{\"contract_version\":\"fixture-response/1\", ...}"}
```

```json
{"raw_bytes_hex": "ff"}
```

```json
{"local_construction_error": "synthetic-local-construction-error"}
```

`utf8_text` is encoded as UTF-8 by the orchestrator and is still treated as
untrusted response bytes. It may contain duplicate JSON keys or malformed JSON
text. `raw_bytes_hex` is the representation for bytes that cannot be expressed
as UTF-8; it is decoded strictly with the standard library. The
`local_construction_error` value must be the exact synthetic marker
`synthetic-local-construction-error`. It never supplies a response object: the
orchestrator creates an existing R1 failed `SourceCheck` with the fixed reason
code `local_construction_error`. The input form is not allowed to provide a
decoded response mapping, trusted identity, observations, or a precomputed R1
result.

Check-level `expected` is trusted test data and is never passed to R1 or R2.
It has exactly `r2`. For a byte input, `r2` is an object with `status`,
`reason_codes`, and `finding_keys`; for a local construction error, `r2` is
`null` because R2 was not invoked. Scan-level `expected` has exactly `r1`,
whose four arrays are the complete expected `ComparisonReport` projection:

```json
{
  "r2": {
    "status": "completed",
    "reason_codes": [],
    "finding_keys": ["finding-a"]
  }
}
```

The expected R1 lists use the existing enum values and fields. A comparison
projection contains exactly `comparison_id`, `subject_ref`, `source_id`,
`baseline_scan_id`, `current_scan_id`, `finding_key`, `kind`,
`changed_field_paths`, and `reason_codes`. An exposure projection contains
exactly `comparison_id`, `subject_ref`, `source_id`, `finding_key`, `kind`,
and `changed_field_paths`. A guarding projection contains exactly `guard_id`,
`subject_ref`, `source_id`, `baseline_scan_id`, `current_scan_id`,
`guard_kind`, `prior_status`, `current_status`, and `reason_codes`.
`finding_key`, `baseline_scan_id`, and `prior_status` use JSON `null` where
the existing R1 record uses `None`. The expected representation must not add a
new result kind or interpretation. The scenario author must write the exact
IDs derived by the existing R1 implementation; the runner must not normalize
or replace them.

Scenario validation rejects unknown keys, duplicate keys, missing fields,
unknown source references, duplicate derived IDs, duplicate source positions,
non-contiguous scan order, invalid one-of inputs, and expectations that cannot
be represented by existing R1/R2 output. That is an invalid scenario, not an
expectation mismatch.

### Fixed outer bounds and exact validation

The loader applies these fixed outer limits before execution:

| Constant | Limit and rule |
|---|---|
| `MAX_SCENARIO_BYTES` | `262144` bytes, measured before JSON parsing. |
| `MAX_SCENARIO_NESTING` | Depth `12`, with the root at depth `0`. |
| `MAX_SOURCES` | `8` source entries. |
| `MAX_SCANS` | `32` scans. |
| `MAX_CHECKS_PER_SCAN` | `8` checks, exactly equal to that scan's `source_order` length. |
| `MAX_STRING_CODEPOINTS` | `256` for trusted schema strings, IDs, keys, reason codes, and expected string values. |
| `MAX_CANONICAL_SCOPE_ITEMS` | `16` items per `canonical_scope`. |
| `MAX_MATERIAL_FIELDS` | `16` fields per material policy. |
| `MAX_EXPECTED_RECORDS_PER_CHECK` | `100` R2 `finding_keys`. |
| `MAX_EXPECTED_RECORDS_PER_SCAN` | `256` total records across baseline, comparison, exposure, and guarding arrays. |
| `MAX_RESPONSE_BYTES` | `65536` bytes after converting `utf8_text` or `raw_bytes_hex`; R2 applies the same input ceiling. |

Every integer is accepted only when `type(value) is int`; JSON booleans are
never accepted as integers. `schema_version` and `normalization_version` are
exact integers in `1..64`. `scan_order` is an exact integer in `1..32`, and
the scan orders must be exactly contiguous `1..len(scans)`. Array lengths are
checked as integers against the bounds above, never by truthiness.

Every trusted schema string is an exact string, non-empty, NFC-normalized,
surrogate-free, and at most 256 Unicode code points. JSON object keys must be
the exact declared key sets. `utf8_text` and `raw_bytes_hex` are the two
untrusted string exceptions to the ordinary string limit: `utf8_text` may be
empty and its UTF-8 encoding must be at most `MAX_RESPONSE_BYTES`;
`raw_bytes_hex` may be empty, must contain only lowercase or uppercase
hexadecimal digits, have even length, and represent at most
`MAX_RESPONSE_BYTES`. These empty forms deliberately allow R2's `blank_input`
path to remain simulatable. The fixed local error marker is the only accepted
`local_construction_error` value.

`canonical_scope` is a JSON array of `1..16` exact strings. The loader maps it
to `tuple[str, ...]` before constructing `SourceIdentity`; its items must be
non-empty, NFC-normalized, unique, and lexicographically sorted. The source
reference, `source_id`, adapter fields, material-field names, and set-like-field
names use the same string rule. `material_fields` and `set_like_fields` are
JSON arrays of `0..16` sorted, unique strings, and
`set_like_fields` must be a subset of `material_fields`. The response bytes
remain the only place where material values are supplied; the scenario file
supplies only this trusted policy.

`source_order` is a JSON array of `1..8` unique known `source_ref` strings.
Every scan's `checks` array must have the same length and the same references
in the same order as `source_order`; no check may be omitted, duplicated, or
silently reordered. After resolving those references, the resulting
`source_id` values must also be unique within that scan. If two references such
as `A1` and `A2` resolve to the same `source_id` in one scan, validation fails
with `reference_error` and exit code `2`; a single `ScanPlan` cannot contain
that source twice. Different scans may use different identities for the same
`source_id`, including `A1` in one scan and `A2` in a later scan. The `sources`
array is sorted by `source_ref`, while `source_order` remains the explicit
operational order. All expected arrays are validated against the existing
R1/R2 field types and the fixed record bounds.

## Trusted fields and simulated untrusted bytes

| Data | Owner | Use |
|---|---|---|
| `subject_ref`, source identity, scope, adapter/version, schema/version, material policy | Scenario file and local constructor | Trusted context for R1/R2. |
| derived `scan_id`, derived `source_check_id`, chronology, source order | Scenario orchestrator | Local execution identity and display order. |
| `utf8_text` or `raw_bytes_hex` | Scenario file | Untrusted bytes supplied only to R2. |
| `local_construction_error` | Scenario orchestrator | Existing R1 failed-check construction path. |
| `expected` | Scenario oracle | Compared only after actual R2/R1 execution. |

The response bytes may contain only the R2 envelope fields already defined by
`RESEARCH_002_ADAPTER_BOUNDARY.md`: `contract_version`, `source_id`,
`outcome`, and `results`. They cannot set subject, canonical scope, adapter
identity, schema version, normalization version, or the material policy.

The runner must not retain or echo raw response bytes in its output. It may
report the input form and byte length, plus bounded R2 reason codes. No evidence
hashing, archive, database, or raw-payload retention is part of R2.5.

### Deterministic execution IDs and R1 ID expectations

For every scan, the runner constructs these IDs exactly, without a UUID,
timestamp, hash, counter outside the scenario, or random value:

```text
scan_id = f"{scenario_id}:scan-{scan_order:03d}"
source_check_id = f"{scan_id}:check-{source_ref}"
```

The `source_check_id` is passed into `TrustedContext` or the direct R1 failed
check. It is included in machine output but is not comparison material.

The following are repository observations for scenario authors: the
scenario-authored expected R1 records should use the IDs generated by the
existing `r1.py` implementation, exactly as follows:

```text
comparison_id = f"{current_scan_id}:{source_id}:"
                 f"{finding_key if finding_key is not None else 'source'}:"
                 f"{kind.value}"
guard_id = f"{current_scan_id}:{source_id}:{guard_kind.value}"
```

`kind.value` is the existing `ComparisonKind` value for a comparison and
`guard_kind.value` is the existing `GuardKind` value for a guard. These
formulas are documentation for scenario authors, not runner validation rules.
The runner constructs only `scan_id` and `source_check_id`; R1 alone constructs
`comparison_id` and `guard_id` inside `compare_scans`. Expected IDs are ordinary
well-typed oracle strings. The runner compares them literally with the IDs
returned by R1 and reports a mismatch if an author got one wrong; that is exit
code `1`, not an invalid scenario. It must not rewrite an expected ID to make
it match. In particular, an R1 `not_comparable` source-level comparison uses
the literal `source` key, while a finding comparison uses its exact finding
key. The ten scenario tables use shorthand labels for readability; their
future Phase 2 records must contain the fully expanded strings. R2.5 does not
claim that those future scenario files or the simulator have been executed.

## Chronology, source order, and in-memory prior state

Scans execute in ascending `scan_order`. Within a scan, checks are invoked in
`source_order`. This is the only operational ordering exposed by the runner.
The existing R1 constructors and comparator retain their own canonical ordering:
source checks and observations are sorted according to R1, and comparison,
exposure, and guarding collections are returned in R1's deterministic order.
The runner must not sort the input before invoking R2 or R1.

At the start of a scenario, `previous_scan` is `None`. After a scan is
constructed, its immutable `ScanAttempt` becomes `previous_scan` for the next
scan in that scenario. No scan, baseline, observation, raw response, or report
is persisted between scenarios. The runner passes the immediately preceding
`ScanAttempt` to the existing `compare_scans`; R1 decides whether each source
can actually compare with it. In particular, a failed prior check does not
become a successful baseline, and a later completed check may create a baseline
under the existing R1 rule.

The runner must retain the complete in-memory `ScanAttempt` for the duration of
one scenario so that source-level guarding and aggregate-incomplete behavior
remain visible. It must not invent a cross-scan baseline selector or recovery
state machine. A local construction error is the one exception to the R2 path:
it produces the fixed R1 failed check directly, and its expected `r2`
projection is `null`.

## Human-readable output

The default mode writes only the fixed-line report to stdout. A valid scenario
always writes an empty stderr. A valid expectation mismatch still writes the
complete report to stdout and exits `1`; it is not an error diagnostic.

The grammar is frozen as follows. Every `<string>` is rendered as one compact
JSON string (`ensure_ascii=false`), every `<array-or-object>` is rendered as
one compact canonical JSON value, and every `<count>` is an unsigned decimal
integer. There is exactly one LF after every line and no blank lines:

```text
SCENARIO <string> result=PASS|EXPECTATION_MISMATCH
SUBJECT <string>
SCAN order=<count> total=<count> scan_id=<string> outcome=<string> expectation=PASS|MISMATCH
SOURCE_CHECK source_ref=<string> source_id=<string> source_check_id=<string> input_kind=<string> input_bytes=<count> r2_invoked=TRUE|FALSE r2_status=<string-or-null> r2_reason_codes=<array> r2_finding_keys=<array> status=<string> reason_codes=<array> finding_keys=<array>
BASELINE_CREATED source_id=<string>
COMPARISON comparison_id=<string> subject_ref=<string> source_id=<string> baseline_scan_id=<string-or-null> current_scan_id=<string> finding_key=<string-or-null> kind=<string> changed_field_paths=<array> reason_codes=<array>
EXPOSURE_EVENT comparison_id=<string> subject_ref=<string> source_id=<string> finding_key=<string> kind=<string> changed_field_paths=<array>
GUARDING_EVENT guard_id=<string> subject_ref=<string> source_id=<string> baseline_scan_id=<string-or-null> current_scan_id=<string> guard_kind=<string> prior_status=<string-or-null> current_status=<string> reason_codes=<array>
EXPOSURE_SILENCE actual=TRUE|FALSE
MISMATCH path=<string> expected=<array-or-object-or-scalar> actual=<array-or-object-or-scalar>
SUMMARY scans=<count> source_checks=<count> comparisons=<count> exposure_events=<count> guarding_events=<count> mismatches=<count>
```

The first two lines occur once. For each scan, the `SCAN` line is followed by
source-check lines in `source_order`, then any `BASELINE_CREATED` lines, actual
R1 `COMPARISON`, `EXPOSURE_EVENT`, and `GUARDING_EVENT` lines in the exact order
returned by R1, one derived `EXPOSURE_SILENCE` line, and any `MISMATCH` lines
for that scan. The `SUMMARY` line occurs once. Zero-length collections produce
no record line and are represented by the counts and arrays.

`EXPOSURE_SILENCE actual=TRUE` is printed exactly when the actual R1
`exposure_events` collection is empty. It is never read from or compared with
a trusted scenario field. Guarding events remain independently printed and
counted. The report must explicitly print `not_comparable`, `failed`, and
`unverifiable`; it must never print “clean” or “not found”, and must print
`disappeared` only for an actual R1 disappearance result. Raw response content
and diagnostic exception text are omitted.

## Canonical machine-readable output

`--json` emits exactly one JSON object to stdout with these top-level keys and
no others, in canonical key-sorted serialization:

```text
runner_version, scenario_id, result, scans, mismatches, diagnostic
```

For a valid scenario, `scenario_id` is the scenario string, `result` is
`pass` or `expectation_mismatch`, and `diagnostic` is `null`. Each scan record
has exactly these keys:

```text
scan_id, scan_order, source_order, outcome, source_checks, r1,
exposure_silence
```

Each `source_checks` record has exactly these keys:

```text
source_ref, source_id, source_check_id, input_kind, input_bytes,
r2_invoked, r2, r1
```

`r2` is either `null` for a local construction error or an object with exactly
`status`, `reason_codes`, and `finding_keys`. The source-check `r1` object has
exactly `status`, `reason_codes`, and `finding_keys`. The scan-level `r1`
object has exactly `baseline_created_sources`, `comparisons`,
`exposure_events`, and `guarding_events`.

Comparison records, exposure records, guarding records, and mismatch records
have exactly these keys:

```text
comparison:
comparison_id, subject_ref, source_id, baseline_scan_id, current_scan_id,
finding_key, kind, changed_field_paths, reason_codes

exposure_event:
comparison_id, subject_ref, source_id, finding_key, kind, changed_field_paths

guarding_event:
guard_id, subject_ref, source_id, baseline_scan_id, current_scan_id,
guard_kind, prior_status, current_status, reason_codes

mismatch:
path, expected, actual
```

`exposure_silence` is an actual derived boolean equal to whether the actual
`exposure_events` array is empty. It is not an expected field. The output
contains no raw bytes and no new comparison semantics.

Canonical serialization is UTF-8 JSON with `ensure_ascii=false`, sorted object
keys, compact separators, and exactly one terminal LF. `runner_version` is
exactly `r2.5-visible-offline-simulator/1`. Arrays are ordered as follows:
scans by `scan_order`, source checks by `source_order`, and actual R1
result/event arrays in the order returned by R1. Mismatches are ordered by
scan order, then source order for check projections, then R1 collection order,
then JSON Pointer path. Object key order is serialization only; it never
changes comparison meaning.

The scenario file is an oracle-bearing test input. The runner must compare
each check's actual normalized R2 status, reason codes, and finding keys with
that check's `expected.r2`, and the complete actual scan-level R1 report with
that scan's `expected.r1`. Expected values are not used to repair, filter,
sort, derive exposure silence, or influence actual results.

Invalid scenarios never produce a fabricated scan. In human mode, stdout is
empty and stderr contains exactly one line:

```text
INVALID_SCENARIO code=<string> path=<string> message=<string>
```

In `--json` mode, stderr is empty and stdout contains the same canonical
top-level key set with `scenario_id: null`, `result: "invalid_scenario"`,
`scans: []`, `mismatches: []`, and a `diagnostic` object with exactly
`code`, `path`, and `message`. Diagnostic codes are fixed lower-case values:
`invalid_json`, `duplicate_json_key`, `unknown_field`, `missing_field`,
`invalid_type`, `invalid_value`, `bounds_exceeded`, `reference_error`, or
`construction_error`. The exact diagnostic messages are:

| Code | Exact `message` |
|---|---|
| `invalid_json` | `scenario JSON is invalid` |
| `duplicate_json_key` | `scenario JSON contains a duplicate object key` |
| `unknown_field` | `scenario contains an unknown field` |
| `missing_field` | `scenario is missing a required field` |
| `invalid_type` | `scenario field has an invalid type` |
| `invalid_value` | `scenario field has an invalid value` |
| `bounds_exceeded` | `scenario exceeds a fixed safety bound` |
| `reference_error` | `scenario contains an invalid reference` |
| `construction_error` | `scenario could not construct an R1 record` |

`path` is an RFC 6901 JSON Pointer with `~` escaped as `~0` and `/` escaped
as `~1`; the root path is `/`. Parser exception text and input bytes are
never emitted. Both invalid modes terminate with exit code `2`.

## Exit codes and pass semantics

The proposed command is:

```text
python -m personal_watchdog.offline_simulator SCENARIO.json
python -m personal_watchdog.offline_simulator --json SCENARIO.json
```

Exit codes are fixed:

| Code | Meaning |
|---:|---|
| `0` | Scenario is valid and every expected R2/R1 projection matches. |
| `1` | Scenario is valid, but at least one expected-versus-actual comparison mismatches. |
| `2` | Scenario is invalid, cannot be constructed safely, or violates the scenario contract. |

An unexpected invariant or construction error fails closed with code `2` and a
bounded diagnostic. It must never be converted into an empty completed scan.

A scenario-level pass means all of these hold:

1. The scenario file passes strict schema and reference validation.
2. Every check yields an R2 result or an explicitly requested local R1 failed
   check.
3. Every scan is constructed through existing R1 constructors.
4. Every report is produced by existing `compare_scans`.
5. Every actual check-level R2 projection equals its check-level expected
   projection, and the actual scan-level `ComparisonReport` equals its
   scan-level expected projection.
6. Derived exposure silence is true exactly when actual
   `exposure_events` is empty; no trusted silence flag exists.
7. No unaccounted exposure or guarding event exists.
8. No failed, unverifiable, malformed, incomplete, incompatible, or adapter-
   rejected response is represented as completed-empty, disappearance, or
   clean silence without its visible guard/non-comparability output.

## Visibility and truthful failure

R2 adapter rejection, malformed bytes, failed checks, and unverifiable checks
remain visible as their R2 reason codes and R1 source status. The report shows
the resulting R1 `not_comparable` record and the appropriate
`guarding_failed` or `guarding_unverifiable` event. A completed source in a
multi-source incomplete scan remains independently comparable, exactly as R1
already defines.

Failure cannot become disappearance because R1 emits disappearance only after
the current source check is `completed`, has the exact comparable identity,
and contains zero observations. Failure cannot become completed-empty because
R2 maps explicit non-completed outcomes and invalid bytes to failed or
unverifiable `SourceCheck` values with no accepted observations. The runner
must preserve this distinction rather than applying a fallback empty list.

## Curated scenarios

All ten scenarios use synthetic subject refs and the trusted source identities
below. The payload catalog gives exact UTF-8 JSON text for readable responses;
the runner encodes each string exactly as UTF-8. `RAW_INVALID_UTF8` is the
explicit byte sequence `ff`. The source identity/version shown in each scan
row is trusted local context, not response content.

### Trusted source identities

| Ref | Source ID | Scope | Adapter | Adapter version | Schema | Normalization | Material policy |
|---|---|---|---|---:|---:|---:|---|
| `A1` | `synthetic-source-a` | `synthetic-scope-a-v1` | `synthetic-r2-adapter` | `1.0` | 1 | 1 | `display_state`, `labels`, `ordered`; `labels` set-like |
| `B1` | `synthetic-source-b` | `synthetic-scope-b-v1` | `synthetic-r2-adapter` | `1.0` | 1 | 1 | same fields; `labels` set-like |
| `A2` | `synthetic-source-a` | `synthetic-scope-a-v1` | `synthetic-r2-adapter` | `2.0` | 1 | 1 | same fields; `labels` set-like |
| `B2` | `synthetic-source-b` | `synthetic-scope-b-v1` | `synthetic-r2-adapter` | `1.0` | 2 | 1 | same fields; `labels` set-like |

The `A2` and `B2` rows exist only to test R1 identity/version
non-comparability; they do not change R2's response contract.

### Exact payload catalog

The following strings are scenario-file `utf8_text` values. Whitespace and
key order shown here are part of the simulated bytes, while R2's JSON parser
and R1's canonical records determine actual meaning.

```text
RAW_A_EMPTY = {"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[]}
RAW_A_ACTIVE = {"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[{"finding_key":"finding-a","kind":"synthetic-profile","locator":"locator-a","material":{"display_state":"active","labels":["alpha","beta"],"ordered":["first","second"]}}]}
RAW_A_CHANGED = {"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[{"finding_key":"finding-a","kind":"synthetic-profile","locator":"locator-a","material":{"display_state":"retired","labels":["alpha","beta"],"ordered":["first","second"]}}]}
RAW_A_BASE_TWO = {"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[{"finding_key":"finding-a","kind":"synthetic-profile","locator":"locator-a","material":{"display_state":"active","labels":["alpha","beta"],"ordered":["first","second"]}},{"finding_key":"finding-b","kind":"synthetic-profile","locator":"locator-b","material":{"display_state":"active","labels":["gamma"],"ordered":["first","second"]}}]}
RAW_A_SIMULTANEOUS = {"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[{"finding_key":"finding-a","kind":"synthetic-profile","locator":"locator-a","material":{"display_state":"retired","labels":["alpha","beta"],"ordered":["first","second"]}},{"finding_key":"finding-c","kind":"synthetic-profile","locator":"locator-c","material":{"display_state":"active","labels":["delta"],"ordered":["first","second"]}}]}
RAW_B_ACTIVE = {"contract_version":"fixture-response/1","source_id":"synthetic-source-b","outcome":"completed","results":[{"finding_key":"finding-b","kind":"synthetic-profile","locator":"locator-b","material":{"display_state":"active","labels":["gamma"],"ordered":["first","second"]}}]}
RAW_B_CHANGED = {"contract_version":"fixture-response/1","source_id":"synthetic-source-b","outcome":"completed","results":[{"finding_key":"finding-b","kind":"synthetic-profile","locator":"locator-b","material":{"display_state":"retired","labels":["gamma"],"ordered":["first","second"]}}]}
RAW_A_FAILED = {"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"failed","results":[]}
RAW_A_HOSTILE_CLEAN = {"contract_version":"fixture-response/1","source_id":"synthetic-source-a","outcome":"completed","results":[],"extra":"attacker-clean"}
RAW_INVALID_UTF8 = ff
LOCAL_CONSTRUCTION_ERROR = {"local_construction_error":"synthetic-local-construction-error"}
```

The payload catalog is a framing shorthand, not a second parser or fixture
file. Phase 2 should put the exact strings and expected records in the
corresponding checked scenario files.

### Scenario 1 — baseline followed by silence

Subject: `subject-r25-01`. Source: `A1` on both scans.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | none | baseline created for A | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | scan 1 completed A | `finding-a=unchanged` | none | none |

Scenario pass requires one visible baseline record, one unchanged comparison,
no exposure event, and no guard.

### Scenario 2 — new exposure

Subject: `subject-r25-02`. Source: `A1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_EMPTY` | none | baseline created with zero observations | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | scan 1 completed-empty A | `finding-a=new` | `finding-a=exposure-new` | none |

The event is an existing R1 exposure-event candidate, not a notification
decision.

### Scenario 3 — material change

Subject: `subject-r25-03`. Source: `A1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | none | baseline created | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_CHANGED` | scan 1 completed A | `finding-a=changed`, path `display_state` | `finding-a=exposure-changed` | none |

R1 already determines that this material field change is an exposure event;
R2.5 does not add a threshold or trivial-change rule.

### Scenario 4 — genuine disappearance after a completed comparable check

Subject: `subject-r25-04`. Source: `A1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | none | baseline created | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_EMPTY` | scan 1 completed A | `finding-a=disappeared` | `finding-a=exposure-disappeared` | none |

This is the only curated disappearance path. Both R2 checks are valid
`completed` checks, and the current one is valid completed-empty.

### Scenario 5 — source failure without disappearance

Subject: `subject-r25-05`. Source: `A1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | none | baseline created | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_FAILED` | scan 1 completed A | `not_comparable`, reason `response_failed` | none | `guarding_failed`, prior completed/current failed |

The failed response retains visible failure and cannot produce disappearance.

### Scenario 6 — unverifiable source

Subject: `subject-r25-06`. Source: `A1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | none | baseline created | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_INVALID_UTF8` (`ff`) | scan 1 completed A | `not_comparable`, reason `invalid_utf8` | none | `guarding_unverifiable`, prior completed/current unverifiable |

The raw byte is rejected before a decoded payload can be used.

### Scenario 7 — one source failing while another changes validly

Subject: `subject-r25-07`. Sources: `A1` and `B1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1, B1 | adapter 1.0/schema 1/norm 1 | A=`RAW_A_ACTIVE`; B=`RAW_B_ACTIVE` | none | baselines for A and B | none | none |
| 2 | A1, B1 | adapter 1.0/schema 1/norm 1 | A=`local_construction_error`; B=`RAW_B_CHANGED` | scan 1 completed A/B | A `not_comparable`/`local_construction_error`; B `changed` | B `exposure-changed` only | A `guarding_failed` only |

The aggregate scan is incomplete, but the valid B source remains comparable.
No event is derived from A's local construction failure. Scenario 5 separately
covers an R2 response whose explicit `outcome` is `failed`; Scenario 7 covers
the orchestrator's local R1 failed-check construction path without adding an
eleventh scenario.

### Scenario 8 — R1 trusted identity/version incompatibility

Subject: `subject-r25-08`. Sources: A and B, with current trusted identities
`A2` and `B2`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1, B1 | adapter 1.0/schema 1/norm 1 | A=`RAW_A_ACTIVE`; B=`RAW_B_ACTIVE` | none | baselines for A and B | none | none |
| 2 | A2, B2 | A adapter 2.0/schema 1; B adapter 1.0/schema 2 | A=`RAW_A_ACTIVE`; B=`RAW_B_ACTIVE` | scan 1 completed A/B | A `not_comparable`/`adapter_version_mismatch`; B `not_comparable`/`schema_version_mismatch` | none | none; both current checks are completed |

Both R2 response envelopes are accepted under the supported response contract;
only R1's trusted subject/source/scope/adapter/schema/normalization identity
comparison rejects comparability. This scenario does not claim an R2 adapter
rejection; the R2 rejection path is covered by Scenario 9.

### Scenario 9 — hostile response attempting a false clean result

Subject: `subject-r25-09`. Source: `A1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_ACTIVE` | none | baseline created | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_HOSTILE_CLEAN` | scan 1 completed A | `not_comparable`, reason `unknown_field` | none | `guarding_unverifiable`, prior completed/current unverifiable |

The extra field makes the apparent clean result invalid. The runner must not
turn it into completed-empty or disappearance.

### Scenario 10 — simultaneous findings

Subject: `subject-r25-10`. Source: `A1`.

| Scan | Source order | Trusted version | Input | Previous comparable state | Expected R1 comparison | Exposure | Guard |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_BASE_TWO` | none | baseline created for A | none | none |
| 2 | A1 | adapter 1.0/schema 1/norm 1 | `RAW_A_SIMULTANEOUS` | scan 1 completed A | `finding-a=changed` path `display_state`; `finding-b=disappeared`; `finding-c=new` | three corresponding R1 exposure events in R1 order | none |

R1 exposes one underlying event per logical finding. Whether a later product
surface groups, suppresses, or prioritizes these simultaneous events remains an
open policy question; R2.5 must show all three.

## Policy questions deliberately left open

The simulator must make existing behavior observable without pretending that
the behavior answers the following policy questions:

| Question | What R1/R2 currently determine | Later experiment observation that would distinguish choices |
|---|---|---|
| Repeated-failure suppression | Every failed/unverifiable current check remains visible as a guard; no suppression exists. | Run controlled sequences with 1, 2, 3, and many consecutive failures; measure operator comprehension, repeated-warning burden, and time to notice a later valid result. |
| Recovery events | A completed check after a failed prior source can create a baseline; R1 does not emit a recovery event. | Compare candidate “recovered”, “baseline re-established”, and silent policies on failure→valid sequences, including prior exposure state. |
| Trivial-change suppression | Any material change produces `changed` and an exposure event; context/diagnostic changes do not. | Vary individual material fields and ask whether each change is actionable; record false-positive and missed-change judgements. |
| Grouping simultaneous barks | R1 emits one exposure event per finding and sorts deterministically. | Present multi-finding reports with grouped versus per-finding display; measure whether grouping hides distinct findings or reduces actionable overload. |
| Baseline overload | R1 keeps only the in-memory previous scan in this proposed runner; it does not define retention, pruning, or cross-run baseline selection. | Vary source count, finding count, failed-source proportion, and scan history; observe memory, review burden, and which baseline users expect. |
| Minimum actionable bark information | Existing events contain subject/source/finding/kind and changed paths; there is no severity or narrative. | Test compact reports with those fields versus additional synthetic context; identify the smallest reliably actionable representation without adding risk claims. |
| Confirmation of disappearance | A valid completed-empty current check immediately yields disappearance. | Compare immediate versus repeated-confirmation policies after controlled completed-empty sequences, including source volatility and false disappearance cost. |

R2.5 must not add suppression, recovery, grouping, severity, confirmation,
baseline retention, or narrative rules to make any scenario look better.

## Phase 2 implementation boundary and proposed files

Implementation after review should add exactly these files unless a later
approved scope change says otherwise:

1. `personal_watchdog/offline_simulator.py` — strict scenario loading,
   orchestration, existing R1/R2 calls, projections, comparison, output, and
   exit codes. Standard library only.
2. `tests/fixtures_r2_5.py` — synthetic scenario and exact payload builders;
   no real identifiers or live calls.
3. `tests/test_r2_5_simulator.py` — schema, chronology, trusted/untrusted
   boundary, all ten scenario expectations, deterministic output, exit codes,
   and failure-visibility tests.
4. The following ten scenario files, each containing one scenario and its
   trusted expectations:
   `scenarios/r2_5_baseline_silence.json`,
   `scenarios/r2_5_new_exposure.json`,
   `scenarios/r2_5_material_change.json`,
   `scenarios/r2_5_genuine_disappearance.json`,
   `scenarios/r2_5_source_failure.json`,
   `scenarios/r2_5_unverifiable_source.json`,
   `scenarios/r2_5_mixed_source_failure_and_change.json`,
   `scenarios/r2_5_r1_trusted_identity_incompatibility.json`,
   `scenarios/r2_5_hostile_false_clean.json`, and
   `scenarios/r2_5_simultaneous_findings.json`.

No R1/R2 source changes, dependency changes, database, archive, evidence
hashing, scheduler, background service, notification, credential, network,
configuration-secret, R3, or XposedOrNot file is proposed. The CLI should be
invoked as a module so `pyproject.toml` need not change merely to frame or run
this offline experiment.

## Falsification and stopping conditions

The framing is falsified if the proposed orchestration must duplicate R1/R2
comparison or normalization logic, if any scenario requires treating failure or
unverifiability as completed-empty, if source order changes R1 output, if
expected values leak into actual computation, or if deterministic canonical
output cannot be produced from the same scenario file.

Stop implementation and return for review if a scenario requires a new R1
status, comparison kind, event kind, material rule, recovery policy, grouping
rule, persistence rule, or live-source assumption. R2.5 is a framing step only;
it does not authorize the Phase 2 files above.
