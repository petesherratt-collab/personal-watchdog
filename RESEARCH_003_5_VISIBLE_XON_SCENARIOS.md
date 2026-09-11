# Research Experiment R3.5 — Visible synthetic XposedOrNot scenarios

**Status: framed, not implemented or run.** This document proposes a
documentation-only Phase 2 experiment. It does not add scenario files, change
the runner, change the R3 adapter, change R1/R2/R2.5, or authorize a live
request.

## Repository reconciliation

The authoritative starting point is clean merge commit 35ef380 on
experiment/r3-5-visible-xon-scenarios, containing the implemented synthetic
R1, R2, R2.5, and R3 Phase 2 experiments and 207 passing tests. The older R1,
R2, and R2.5 documents retain historical “framed, not run” status language;
the current source and append-only records are authoritative for what has
actually been implemented.

No material contradiction blocks this framing. The current code establishes
these facts:

- offline_simulator.py currently parses only the exact R2.5 scenario version,
  calls the existing R2 normalizer, constructs R1 records, and calls only
  compare_scans for comparison and events.
- xposedornot_check_email_adapter.py accepts a locally constructed
  TransportAttempt, classifies transport, validates the frozen check-email
  body, serializes the existing R2 envelope, calls normalize_response, and
  returns one R1 SourceCheck.
- The R3 adapter has no separate public XON-classification record. Therefore
  R3.5 must expose XON classification only as a presentation projection of
  the adapter’s public TransportClassification and returned SourceCheck; it
  must not reproduce _parse_xon_body, XON predicates, R2 validation, or R1
  comparison logic in the runner.
- R1 compares the immediately preceding in-memory ScanAttempt; it does not
  search backward for the last successful comparable state.

The existing editable-install setuptools package-discovery failure remains a
separate packaging task. R3.5 does not fix it.

## 1. Experimental claim and non-claims

### Claim

Within a new, bounded, synthetic scenario family, the existing deterministic
offline simulator can make this already implemented chain observable:

~~~text
synthetic TransportAttempt
  -> existing XON transport classification and normalizer
  -> existing R2 SourceCheck
  -> existing R1 compare_scans
  -> exposure event, guarding event, or derived silence
~~~

The experiment tests whether explicit dispatch and projection are sufficient
to expose the chain without a second transport parser, XON parser, R2
normalizer, comparator, baseline selector, or bark policy.

### Non-claims

This experiment does not establish live XposedOrNot compatibility, endpoint
availability, authentication or authorization behavior, rate-limit policy,
service completeness, freshness, ordering, duplicate behavior, pagination,
source coverage, identity ownership, absence of exposure, risk, severity,
notification usefulness, or safety. It does not submit an identifier, use a
credential, open a socket, or infer that a synthetic body is an official
closed schema.

The R1 exposure collections remain deterministic comparison outputs. They are
not notifications and this phase does not choose a product bark policy.

## 2. Why this is end-to-end visibility, not live integration

The experiment is end-to-end only through the local synthetic boundaries that
already exist. A scenario supplies bounded bytes and metadata to an in-memory
TransportAttempt; the existing adapter performs its transport/XON/R2 work;
the existing R1 records and comparator produce the final report. No request is
constructed, no DNS name is resolved, no HTTP library is imported, and no
identifier leaves the machine.

“End-to-end” therefore means that one scenario can be inspected from input
envelope to final R1 report. It does not mean that any step is connected to
XposedOrNot or that the synthetic envelope is wire-compatible with the
service. The XON source identity and body predicate remain the frozen R3
synthetic contract.

## 3. Explicit dispatch through existing boundaries

The Phase 2 runner extension should branch only on a trusted, allowlisted
source adapter identity:

| Trusted adapter_id | Input | Call | Output owner |
|---|---|---|---|
| xposedornot-check-email | transport_attempt | normalize_check_email(TransportAttempt) | Existing R3 adapter returns SourceCheck |
| synthetic-r2-adapter | Existing R2.5 bytes input, only in the mixed-source scenario | normalize_response(bytes, TrustedContext) | Existing R2 adapter returns SourceCheck |

The XON branch constructs only Header, TransportAttempt, and its trusted
context from validated scenario data, then calls the existing public
classify_transport for the transport projection and existing public
normalize_check_email for the source result. It does not call private XON
helpers or inspect response JSON to predict the result.

After dispatch, both branches use the existing common orchestration:

~~~text
validated scenario
  -> trusted SourceIdentity and scan plan
  -> adapter-specific SourceCheck
  -> ScanAttempt.create
  -> compare_scans(previous_scan, current_scan)
  -> projections and literal oracle comparison
~~~

The runner may infer the display-only XON classification as follows, using
only public results:

- not_entered if classify_transport is not READY;
- success_predicate_accepted if transport is READY and normalize_check_email
  returns a completed check; and
- success_predicate_rejected if transport is READY and the adapter returns an
  unverifiable check.

These are the only valid XON projection cases. This is not a new semantic
result; it is a bounded view of the existing adapter boundary. For zero-based
JSON-array positions i and j, if classify_transport returns READY but
normalize_check_email returns any status other than completed or unverifiable,
the R3.5 runner triggers xon_projection_invariant immediately. It discards
buffered normal output, does not construct an XON classification or R1 report,
does not run later scans, and exits 2. In human mode stdout is empty and
stderr is exactly this one LF-terminated line:

~~~text
INTERNAL_ERROR code=xon_projection_invariant path="/scans/i/checks/j" message="XON adapter result contradicts its READY transport projection"
~~~

In JSON mode stderr is empty and stdout is the exact internal-error object
specified in Section 17. This is an R3.5-only internal diagnostic, not an
invalid scenario and not a source result. It never invents a fourth XON
classification or converts the unexpected result into a source result. The
mixed synthetic R2 source reports not_applicable for XON classification. A
construction rejection has no classification because no valid attempt exists.

## 4. Scenario version and family

A separate scenario family and version are required:

~~~text
r3.5-visible-xon-scenarios/1
~~~

The R2.5 version cannot be widened: its exact input one-of, expected key
sets, human grammar, machine key sets, and golden outputs are already a
backward-compatibility contract. The runner may dispatch by exact
scenario_version, but the R2.5 parser and output branch must remain
behaviorally unchanged. The new family is not a new R1 or R2 semantic family;
it is a scenario/input and presentation family that exercises the existing
R3 adapter.

The proposed fixture directory is scenarios/r3_5_xon/. Each file contains
one scenario. The Phase 2 set has the exact names listed in Section 15.

## 5. R2.5 compatibility

All existing scenarios/r2_5_*.json files, their ten scenario IDs, their
human reports, their canonical JSON outputs, their mismatch behavior, and
their exit codes remain unchanged. The implementation must prove this with
the existing R2.5 tests plus byte-for-byte golden output assertions before and
after the dispatch extension.

The version dispatch is strict:

- exact r2.5-visible-offline-simulator/1 uses the current R2.5 schema,
  orchestration, projections, and output grammar;
- exact r3.5-visible-xon-scenarios/1 uses the new transport schema and new
  XON output fields; and
- any other version is invalid scenario input with the existing fixed
  invalid_value diagnostic.

No existing scenario file, fixture helper, R2.5 expected record, or R2.5
output line is edited by this phase or proposed as part of the new fixtures.

## 6. Trusted fields and simulated untrusted data

### Trusted local fields

The scenario file supplies trusted test context, subject to strict validation:

- subject_ref;
- source_ref and the complete SourceIdentity;
- source_id, canonical_scope, adapter_id, adapter_version, schema_version,
  normalization_version, material_fields, and set_like_fields;
- derived scan_id and source_check_id;
- source and scan order; and
- expected transport, XON, R2, and R1 projections.

For the XON fixtures, the subject values are opaque synthetic strings such as
subject-r35-01; the echoed XON email field contains the same synthetic
string. This deliberately does not test email syntax and avoids placing a
complete email address in source, fixtures, output, or logs.

### Simulated untrusted transport and body

The scenario simulates, but does not perform, the following untrusted values:

- HTTP status;
- raw bounded header name and value bytes;
- complete body bytes or a bounded retained prefix;
- body state;
- transport failure and timeout flags; and
- failure phase.

normalized_content_type is never a scenario input. It is derived by the
existing adapter from the raw headers. The body is never decoded by the
runner before dispatch. Scenario expectations are not supplied to the adapter
and cannot repair or filter its result.

## 7. Exact JSON representation of the transport envelope

Every XON check has an input object with exactly one key:

~~~json
{
  "transport_attempt": {
    "http_status": 200,
    "bounded_headers": [
      {
        "name_bytes_hex": "436f6e74656e742d54797065",
        "value_bytes_hex": "6170706c69636174696f6e2f6a736f6e"
      }
    ],
    "body_bytes_hex": "...",
    "body_state": "complete",
    "transport_failure": null,
    "timed_out": false,
    "failure_phase": null
  }
}
~~~

The exact mapping is:

| TransportAttempt field | JSON field and representation |
|---|---|
| http_status | http_status: JSON null or exact JSON integer 100..599; booleans are invalid. |
| bounded_headers | bounded_headers: JSON array of header objects; order is retained and duplicate names are not deduplicated. |
| Header.name_bytes | name_bytes_hex: lowercase even-length hexadecimal string, including the empty string; decoded length at most 64 bytes. |
| Header.value_bytes | value_bytes_hex: even-length lowercase hexadecimal string; decoded length at most 512 bytes. |
| body_bytes | body_bytes_hex: lowercase even-length hexadecimal string, decoded before construction; no JSON string is treated as raw bytes. |
| body_state | Exact string complete, incomplete, over_limit, or absent. |
| transport_failure | JSON null or exact string transport. |
| timed_out | Exact JSON boolean. |
| failure_phase | JSON null, before_status, or after_status. |
| normalized_content_type | Not representable in input; derived only by the adapter. |
| trusted_context | Not representable in input; constructed from the validated subject/source and derived IDs. |

The body byte bound is 16,384 decoded bytes. An over_limit attempt stores
exactly the first 16,384 bytes in body_bytes_hex and is never parsed. An
incomplete post-status attempt stores a prefix of 0..16,384 bytes and is
never parsed. A pre-status failure has empty headers and empty body bytes.

The mixed-source scenario has one additional exact input form for its existing
synthetic R2 source:

~~~json
{"r2_bytes_hex":"..."}
~~~

It is permitted only when the trusted source adapter is exactly
synthetic-r2-adapter. It is not an XON transport and its transport and xon
projections are null.

For every source-check projection, input_kind and input_bytes have these
exact meanings. For an XON check, input_kind is the string
transport_attempt, and input_bytes is the decoded length of
body_bytes_hex: complete body bytes, an incomplete retained prefix, the
exact over-limit retained prefix, or zero for an absent body. It excludes
header bytes and scenario JSON bytes. For the synthetic-R2 check,
input_kind is the string r2_bytes_hex, and input_bytes is the decoded
length of the complete R2 envelope bytes passed to the existing
normalize_response; it is not a TransportAttempt body length.

## 8. Deterministic arbitrary-byte encoding

Hexadecimal is the only byte encoding. Every byte is represented by exactly
two lowercase ASCII hex digits, with no 0x prefix, whitespace, base64,
Unicode escape, or implicit text conversion. The empty byte string is "".
The decoder first validates the exact lowercase-hex grammar and even length,
then calls bytes.fromhex; it never calls .encode() on a JSON body string.

Readable body aliases in this document mean the following exact operation,
not a different scenario input type:

~~~text
BODY_HEX(ascii_text) = lowercase_hex(ascii_text encoded as UTF-8)
~~~

All curated XON body texts are ASCII, so the encoded bytes are exactly their
ASCII bytes. The actual Phase 2 JSON files must contain the expanded hex
strings. For a body requiring arbitrary bytes, such as ff, the file contains
"ff", not a JSON string intended to be decoded as text.

## 9. Bounds, types, key sets, uniqueness, ordering, and diagnostics

The R3.5 loader reuses the R2.5 outer bounds unchanged: 262,144 scenario
bytes before parsing; nesting depth 12; at most 8 sources, 32 scans, 8 checks
per scan; 256 code points for trusted strings; 16 canonical-scope items; 16
material-policy fields; 100 expected finding keys per check; and 256 expected
R1 records per scan. R2.5 exact integer, NFC, surrogate, duplicate-key, and
strict JSON rules remain in force.

R3.5 adds these bounds:

- at most 16 headers per attempt;
- raw header names at most 64 bytes and raw values at most 512 bytes;
- retained header accounting exactly
  sum(name_bytes + 1 + value_bytes + 1) <= 8,192;
- decoded body bytes at most 16,384;
- the adapter's retained-header allowlist remains the exact set of
  content-type, content-length, retry-after, date, etag, last-modified,
  location, and server, but the scenario validator does not pre-classify a
  bounded raw name as supported or unsupported; and
- at most one of transport_failure and timed_out is active.

The R3.5 top-level key set is exactly scenario_version, scenario_id,
subject_ref, sources, and scans. The exact nested key sets are:

```text
source:  source_ref, source_id, canonical_scope, adapter_id, adapter_version,
         schema_version, normalization_version, material_fields, set_like_fields
scan:    scan_order, source_order, checks, expected
check:   source_ref, input, expected
expected check: r3_transport, xon, r2
expected scan:  r1
transport_attempt: http_status, bounded_headers, body_bytes_hex, body_state,
                   transport_failure, timed_out, failure_phase
header:  name_bytes_hex, value_bytes_hex
transport oracle: disposition, reason, normalized_content_type
xon oracle: classification
r2 oracle: status, reason_codes, finding_keys
```

Unknown and missing keys are invalid. Source references are unique and sorted in sources; each
source_order is unique, known, and operational; checks match it position for
position; resolved source IDs are unique per scan; scan orders are contiguous
starting at 1; and expected arrays preserve the R1 order returned by the
comparator. The runner must not sort source checks before adapter invocation.

The XON source identity is accepted only when all of these trusted fields
match the existing XON_SOURCE exactly:

~~~text
source_id              = "xposedornot.free.check-email"
canonical_scope        = ["GET /v1/check-email/{email}", "include_details=false"]
adapter_id              = "xposedornot-check-email"
adapter_version        = "1"
schema_version          = 1
normalization_version  = 1
material_fields        = []
set_like_fields        = []
~~~

The corresponding literal JSON source object is:

~~~json
{
  "source_ref": "X1",
  "source_id": "xposedornot.free.check-email",
  "canonical_scope": ["GET /v1/check-email/{email}", "include_details=false"],
  "adapter_id": "xposedornot-check-email",
  "adapter_version": "1",
  "schema_version": 1,
  "normalization_version": 1,
  "material_fields": [],
  "set_like_fields": []
}
~~~

The synthetic R2 source has the same exact JSON type rule:

~~~json
{
  "source_ref": "B1",
  "source_id": "synthetic-source-b",
  "canonical_scope": ["synthetic-scope-b-v1"],
  "adapter_id": "synthetic-r2-adapter",
  "adapter_version": "1.0",
  "schema_version": 1,
  "normalization_version": 1,
  "material_fields": ["display_state", "labels", "ordered"],
  "set_like_fields": ["labels"]
}
~~~

The generic synthetic source in Scenario 17 uses the existing R2.5 trusted
identity and does not alter the XON identity. The trusted context passed to
the adapter is the exact local object represented by:

```json
{
  "scan_id": "<scenario_id>:scan-<scan_order as 3 digits>",
  "source_check_id": "<scan_id>:check-<source_ref>",
  "subject_ref": "<scenario subject_ref>",
  "source": "the fully validated source object above"
}
```

The angle-bracket values are construction notation only; expected records and
output contain the literal derived strings, never these placeholders.

Malformed, duplicate, and unsupported raw header names remain valid scenario
data when their byte bounds and hex syntax are valid. The scenario validator
does not apply the adapter's retained-header allowlist or duplicate policy;
the existing adapter owns those untrusted-metadata classifications. Only
structurally impossible local envelopes are invalid scenarios.

Invalid input uses the existing fixed diagnostic grammar. Human mode writes
only:

~~~text
INVALID_SCENARIO code=<code> path=<RFC-6901-pointer> message=<compact-JSON-string>
~~~

Machine mode writes the canonical invalid object with scenario_id: null,
result: invalid_scenario, empty scans and mismatches, and diagnostic:
{code,path,message}. The R2.5 scenario-input diagnostic set and exact messages
remain invalid_json, duplicate_json_key, unknown_field, missing_field,
invalid_type, invalid_value, bounds_exceeded, reference_error, and
construction_error. R3.5 additionally freezes the internal-only diagnostic
code xon_projection_invariant; it is not part of the R2.5 set, is not an
invalid-scenario diagnostic, and uses the separate internal-error object and
streams in Sections 3 and 17. A contradictory TransportAttempt uses
construction_error at the exact input path and is never converted to a source
result.

## 10. Local construction contradictions

TransportAttempt.__post_init__ remains the authority for local envelope
invariants. Examples that must reject the scenario before classification are:

- a pre-status failure with a non-null status, any body bytes, or any headers;
- an after-status failure without an integer status or with body_state other
  than incomplete;
- active failure flags with complete or over_limit;
- both transport failure and timeout active;
- failure_phase inconsistent with the failure flags;
- an over_limit body whose retained prefix is not exactly 16,384 bytes;
- a complete body above the 16,384-byte bound; or
- an absent body with non-empty bytes.

The scenario runner catches only the declared TransportConstructionError
family and raises the bounded construction_error scenario diagnostic. No
SourceCheck is fabricated, no guard is emitted, and no R1 comparison runs.
An invalid local envelope is therefore an invalid scenario, not an
unverifiable source result. Valid attempts with malformed untrusted metadata
remain source-level unverifiable results as the R3 adapter already defines.

## 11. Transport and XON ownership

Transport classification remains wholly owned by
xposedornot_check_email_adapter.py. The runner must call classify_transport
and project its returned TransportClassification fields:

~~~text
disposition, reason, normalized_content_type
~~~

The adapter’s current precedence remains frozen: local construction rejection;
pre-status failure; status >= 400 as failed; post-status body failure as
incomplete; over-limit body as incomplete; malformed/incompatible metadata as
unverifiable; unsupported below-400 status as unverifiable; then only eligible
HTTP 200 JSON proceeds to XON parsing.

XON normalization remains wholly owned by normalize_check_email. The runner
must not parse body_bytes, inspect email, count breaches, validate XON keys,
derive finding keys, deduplicate names, or map XON errors itself. XON
classification in output is the non-semantic projection defined in Section 3.

## 12. R2 and R1 ownership

The XON adapter remains the only layer that constructs the generated
fixture-response/1 envelope and calls R2. R2 remains the only layer that
constructs the final R1-compatible SourceCheck from that envelope. The
runner must not construct a completed, failed, or unverifiable XON
SourceCheck from expected values or transport fields.

R1 remains the only owner of:

- baseline creation;
- source comparability and identity/version mismatch reasons;
- comparison_id and guard_id construction;
- new, unchanged, changed, disappeared, and not_comparable results;
- exposure events;
- guarding events; and
- disappearance.

The runner constructs only scan_id and source_check_id. Expected comparison
and guard IDs are literal oracle strings. A wrong literal ID is an expectation
mismatch with exit code 1, never an invalid scenario with exit code 2.

## 13. Chronology and prior-state selection

Scans execute in ascending scan_order. Checks invoke adapters in the exact
source_order supplied by that scan. R1 then returns its own canonical
source/check, comparison, exposure, and guard ordering for output.

At scenario start previous_scan = None. After each valid scan, the complete
immutable ScanAttempt becomes previous_scan for the next scan. Nothing is
persisted between scenarios. The runner does not retain the last successful
scan separately and does not add a recovery or baseline-selection policy.

This is a material observation and limitation: a failed or unverifiable scan
can displace the prior successful comparable scan. A later completed check
then sees the immediately preceding failed/unverifiable SourceCheck and R1
creates a new baseline silently; it does not compare against the older
successful state. Scenario 8 intentionally makes this visible with
baseline -> 429 -> 503 -> valid.

## 14. Oracle model and exact ID rules

Every valid check has three separately compared oracle projections:

1. transport: exact disposition, reason, and derived normalized_content_type;
2. XON: a display-only projection derived from the public transport
   classification and returned SourceCheck under Section 3, separately
   compared as an oracle but not an independent semantic result; and
3. R2: exact status, sorted reason_codes, and sorted normalized finding_keys
   from the returned SourceCheck.

Every scan has one complete R1 oracle containing exactly
baseline_created_sources, comparisons, exposure_events, and guarding_events,
with every record field from the existing R2.5 projection. No expected silence
field is accepted. Actual
silence is derived only from the actual R1 exposure-event array.

The runner derives only:

~~~text
scan_id = {scenario_id}:scan-{scan_order:03d}
source_check_id = {scan_id}:check-{source_ref}
~~~

R1 derives comparison and guard IDs. Scenario authors write their literal
results using the existing formulas:

~~~text
comparison_id = {current_scan_id}:{source_id}:
                {finding_key or "source"}:{comparison_kind}
guard_id       = {current_scan_id}:{source_id}:{guard_kind}
~~~

The IDs are compared literally. Incorrect IDs, including otherwise plausible
IDs, produce mismatch records and exit code 1.

The complete expected R1 projection uses these exact record key sets and
values, with no omitted fields:

```text
comparison:
comparison_id, subject_ref, source_id, baseline_scan_id, current_scan_id,
finding_key, kind, changed_field_paths, reason_codes

exposure_event:
comparison_id, subject_ref, source_id, finding_key, kind, changed_field_paths

guarding_event:
guard_id, subject_ref, source_id, baseline_scan_id, current_scan_id,
guard_kind, prior_status, current_status, reason_codes
```

For example, the exact scan-2 R1 report for Scenario 3 is the following
object after literal substitution of its scenario ID and source IDs:

```json
{
  "baseline_created_sources": [],
  "comparisons": [{
    "comparison_id": "r35-s03-additional-breach:scan-002:xposedornot.free.check-email:breach:Another Breach:new",
    "subject_ref": "subject-r35-03",
    "source_id": "xposedornot.free.check-email",
    "baseline_scan_id": "r35-s03-additional-breach:scan-001",
    "current_scan_id": "r35-s03-additional-breach:scan-002",
    "finding_key": "breach:Another Breach",
    "kind": "new",
    "changed_field_paths": [],
    "reason_codes": []
  }],
  "exposure_events": [{
    "comparison_id": "r35-s03-additional-breach:scan-002:xposedornot.free.check-email:breach:Another Breach:new",
    "subject_ref": "subject-r35-03",
    "source_id": "xposedornot.free.check-email",
    "finding_key": "breach:Another Breach",
    "kind": "exposure-new",
    "changed_field_paths": []
  }],
  "guarding_events": []
}
```

The filename and scenario ID do not have literal string equality. The curated
suite instead enforces this explicit frozen correspondence:

| Filename | Scenario ID |
|---|---|
| 01_first_finding_baseline.json | r35-s01-first-finding-baseline |
| 02_identical_finding.json | r35-s02-identical-finding |
| 03_additional_breach.json | r35-s03-additional-breach |
| 04_one_disappears_one_remains.json | r35-s04-one-disappears-one-remains |
| 05_multiple_simultaneous_findings.json | r35-s05-multiple-simultaneous-findings |
| 06_zero_finding_unverifiable.json | r35-s06-zero-finding-unverifiable |
| 07_http_404_failed.json | r35-s07-http-404-failed |
| 08_http_429_503_failed.json | r35-s08-http-429-503-failed |
| 09_invalid_utf8_malformed_json.json | r35-s09-invalid-utf8-malformed-json |
| 10_content_type_metadata.json | r35-s10-content-type-metadata |
| 11_incomplete_body.json | r35-s11-incomplete-body |
| 12_over_limit_body.json | r35-s12-over-limit-body |
| 13_echo_mismatch.json | r35-s13-echo-mismatch |
| 14_hostile_unknown_field.json | r35-s14-hostile-unknown-field |
| 15_overlong_json_integer.json | r35-s15-overlong-json-integer |
| 16_contradictory_transport_invalid.json | r35-s16-contradictory-transport-invalid |
| 17_xon_failure_mixed_source_change.json | r35-s17-xon-failure-mixed-source-change |

The filename-to-ID table is a curated-test-suite invariant, not a generic
string transformation. Every actual expectation uses the full literal ID.
Baseline, unchanged,
new, disappearance, failed, unverifiable, rebaseline, and mixed-source rows
expand the same exact key sets, including null baseline/finding/prior fields
where R1 returns None. No expected report is a prose-only assertion.

### Frozen R1 report macros used by the ledger

The labels in the scenario tables are compact names for these complete report
expansions. They are documentation macros only; each proposed JSON fixture
must contain the resulting literal IDs, strings, arrays, nulls, and ordering.
Let `Q` be the literal scenario subject, `S` a literal source ID, `B` the
literal immediately prior scan ID, `C` the literal current scan ID, and `F` a
literal finding key.

`R1_BASELINE([S...])` is exactly

~~~json
{"baseline_created_sources":["<sorted literal S values>"],"comparisons":[],"exposure_events":[],"guarding_events":[]}
~~~

where the array contains every completed source newly establishing a baseline,
sorted by source ID. `R1_REBASE(S)` is the same object with exactly
`baseline_created_sources: [S]`; it is used when the immediately prior source
check was not completed.

For a completed comparable source, `R1_SILENT(S,B,C,F)` has exactly one
comparison object and no events:

~~~json
{"comparison_id":"C:S:F:unchanged","subject_ref":"Q","source_id":"S","baseline_scan_id":"B","current_scan_id":"C","finding_key":"F","kind":"unchanged","changed_field_paths":[],"reason_codes":[]}
~~~

`R1_NEW(S,B,C,F)` uses the same comparison shape with `kind: "new"` and
`comparison_id: "C:S:F:new"`, plus exactly one exposure object:

~~~json
{"comparison_id":"C:S:F:new","subject_ref":"Q","source_id":"S","finding_key":"F","kind":"exposure-new","changed_field_paths":[]}
~~~

`R1_DISAPPEAR(S,B,C,F)` uses the same comparison shape with
`kind: "disappeared"` and `comparison_id: "C:S:F:disappeared"`, plus exactly
one exposure object whose `kind` is `"exposure-disappeared"`. For multiple
findings, expand one such comparison and exposure per literal finding and
sort both collections by R1’s returned source/finding order. Thus Scenario 5
has `Another`, then `Third` in both collections.

`R1_CHANGED(S,B,C,F)` is the same exact shape with `kind: "changed"`,
`comparison_id: "C:S:F:changed"`, `changed_field_paths: ["display_state"]`,
and one exposure object with `kind: "exposure-changed"` and the same changed
path.

For a valid preceding scan and a current failed or unverifiable check,
`R1_GUARDED(S,B,C,P,status,guard_kind,reason)` is exactly one comparison,
one guarding event, and no exposure events:

~~~json
{
  "comparisons": [{
    "comparison_id": "C:S:source:not_comparable",
    "subject_ref": "Q", "source_id": "S", "baseline_scan_id": "B",
    "current_scan_id": "C", "finding_key": null,
    "kind": "not_comparable", "changed_field_paths": [],
    "reason_codes": ["reason"]
  }],
  "exposure_events": [],
  "guarding_events": [{
    "guard_id": "C:S:guard_kind", "subject_ref": "Q", "source_id": "S",
    "baseline_scan_id": "B", "current_scan_id": "C",
    "guard_kind": "guard_kind", "prior_status": "P",
    "current_status": "status", "reason_codes": ["reason"]
  }]
}
~~~

The full report also has `baseline_created_sources: []`. For failure rows,
`status`/`guard_kind`/`reason` are respectively
`failed`/`guarding_failed`/`response_failed`; for unverifiable rows they are
`unverifiable`/`guarding_unverifiable`/`response_unverifiable`. `P` is the
literal prior status shown in each row (`completed`, `failed`, or
`unverifiable`). With no preceding scan, `B` and `P` are null, but no curated
failure row relies on that case.

These macros are complete R1 reports, not assertions about silence. Silence
is separately and exactly `exposure_events == []`; the runner must derive it
from actual R1 output.

## 15. Exact curated scenario ledger

The following names, subjects, source identities, body bytes, prior state, and
expected projections are frozen for the proposed fixture set. X1 means the
exact XON_SOURCE identity in Section 9. B1 means the existing R2.5
synthetic-source-b identity: scope synthetic-scope-b-v1, adapter
synthetic-r2-adapter version 1.0, schema 1, normalization 1, material fields
display_state, labels, ordered, and set-like field labels.

The exact scenario IDs, which are literal and unique across the proposed
fixture set, are:

~~~text
r35-s01-first-finding-baseline
r35-s02-identical-finding
r35-s03-additional-breach
r35-s04-one-disappears-one-remains
r35-s05-multiple-simultaneous-findings
r35-s06-zero-finding-unverifiable
r35-s07-http-404-failed
r35-s08-http-429-503-failed
r35-s09-invalid-utf8-malformed-json
r35-s10-content-type-metadata
r35-s11-incomplete-body
r35-s12-over-limit-body
r35-s13-echo-mismatch
r35-s14-hostile-unknown-field
r35-s15-overlong-json-integer
r35-s16-contradictory-transport-invalid
r35-s17-xon-failure-mixed-source-change
~~~

### Exact body catalog

Every name below is a compact ASCII JSON body. The fixture stores BODY_HEX(...),
not the text. subject is replaced by the row’s literal synthetic subject before
UTF-8 encoding and lowercase hex encoding.

~~~text
BODY(subject, names) = {"breaches":[[names]],"email":"subject","status":"success"}
BODY_ZERO(subject) = {"breaches":[],"email":"subject","status":"success"}
BODY_MALFORMED(subject) = {"breaches":[["Example Breach"]],"email":"subject","status":"success"
BODY_HOSTILE(subject) = {"breaches":[],"email":"subject","status":"success","extra":"attacker-clean"}
BODY_ECHO_MISMATCH(subject) = {"breaches":[["Example Breach"]],"email":"other-subject","status":"success"}
BODY_OVERLONG_INTEGER(subject) = {"breaches":[["Example Breach"]],"email":"subject","status":"success","hostile":<5000 ASCII digit 1 bytes>}
~~~

The exact valid body hex for subject-r35-01 with one finding is:

~~~text
7b226272656163686573223a5b5b224578616d706c6520427265616368225d5d2c22656d61696c223a227375626a6563742d7233352d3031222c22737461747573223a2273756363657373227d
~~~

The other valid bodies are the same exact compact JSON construction with the
literal row subject and names. For auditability, their byte lengths are 77
for one name, 94 for Example Breach plus Another Breach, and 109 for those two
plus Third Breach. BODY_OVERLONG_INTEGER is 5,088 bytes for subject-r35-15;
its body_bytes_hex is the exact lowercase hex expansion of the text with 5,000
1 bytes. The over-limit prefix is exactly "7b" repeated 16,384 times. No
fixture relies on an implicit JSON-to-bytes rule.

Header aliases are exact raw bytes:

~~~text
CT_JSON       = name 436f6e74656e742d54797065, value 6170706c69636174696f6e2f6a736f6e
CT_PARAM      = CT_JSON name, value 6170706c69636174696f6e2f6a736f6e3b20636861727365743d7574662d38
CT_WRONG      = CT_JSON name, value 746578742f706c61696e
CT_NONASCII   = CT_JSON name, value 6170706c69636174696f6e2f6a736f6e80
CT_DUPLICATE  = CT_JSON plus a second content-type name 636f6e74656e742d74797065 with JSON value
HEADER_BAD    = name 780a with value 79
~~~

Transport aliases are complete objects after substituting body bytes:

| Alias | Exact fields | Expected transport |
|---|---|---|
| T_READY(body, headers=CT_JSON) | status 200; complete; no failure; no timeout; no phase | READY, ready, application/json |
| T_HTTP(status) | status given; complete; CT_JSON; body empty; no failure | FAILED, http_failure, null for 404/429/503 |
| T_PRE_TIMEOUT | status null; headers []; body empty; absent; timeout true; phase before_status | FAILED, pre_status_failure, null |
| T_POST_TIMEOUT(prefix) | status 200; prefix; incomplete; timeout true; phase after_status | INCOMPLETE, post_status_body_failure, null |
| T_POST_TRUNCATED(prefix) | status 200; prefix; incomplete; transport failure; phase after_status | INCOMPLETE, post_status_body_failure, null |
| T_OVER_LIMIT | status 200; 16,384-byte prefix; over_limit; no failure | INCOMPLETE, body_over_limit, null |
| T_META(headers) | status 200; complete; valid body; headers given; no failure | adapter exact metadata reason, UNVERIFIABLE, null |

In every table below, the prior state is the immediately preceding scan’s
complete ScanAttempt, not the last successful scan.

### Scenario 1 — valid first finding creates a silent baseline

File: r3_5_xon/01_first_finding_baseline.json; subject subject-r35-01;
source order X1 on both scans; trusted identity X1 on both scans; input body is
the exact one-name valid body above.

| Scan/check | Simulated input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | T_READY(BODY(subject-r35-01,[Example Breach])); no prior scan | READY/ready/application-json | success_predicate_accepted | completed, [], [breach:Example Breach] | R1_BASELINE | TRUE |
| 2/X1 | same body; prior is scan 1 completed with that finding | same | accepted | completed, [], [breach:Example Breach] | R1_SILENT with unchanged | TRUE |

### Scenario 2 — identical valid finding remains unchanged and silent

File: r3_5_xon/02_identical_finding.json; subject subject-r35-02; X1 on
both scans; same trusted identity and exact one-name body on both scans.

| Scan/check | Prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | none | READY/ready/application-json | accepted | completed, [], [breach:Example Breach] | R1_BASELINE | TRUE |
| 2/X1 | scan 1 completed with same finding | same | accepted | same | R1_SILENT (unchanged) | TRUE |

### Scenario 3 — an additional breach name creates a new exposure

File: r3_5_xon/03_additional_breach.json; subject subject-r35-03; X1 on
both scans.

| Scan/check | Body and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | one Example Breach; none | ready | accepted | completed, [], [breach:Example Breach] | R1_BASELINE | TRUE |
| 2/X1 | Example Breach, Another Breach; prior scan 1 | ready | accepted | completed, [], [breach:Another Breach, breach:Example Breach] | R1_NEW for breach:Another Breach | FALSE |

### Scenario 4 — one breach disappears while another remains valid

File: r3_5_xon/04_one_disappears_one_remains.json; subject subject-r35-04;
X1 on both scans.

| Scan/check | Body and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | Example Breach, Another Breach; none | ready | accepted | completed, [], [breach:Another Breach, breach:Example Breach] | R1_BASELINE | TRUE |
| 2/X1 | only Another Breach; prior scan 1 | ready | accepted | completed, [], [breach:Another Breach] | R1_DISAPPEAR for breach:Example Breach | FALSE |

### Scenario 5 — multiple simultaneous breach findings

File: r3_5_xon/05_multiple_simultaneous_findings.json; subject subject-r35-05;
X1 on both scans.

| Scan/check | Body and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | only Example Breach; none | ready | accepted | completed, [], [breach:Example Breach] | R1_BASELINE | TRUE |
| 2/X1 | Example Breach, Another Breach, Third Breach; prior scan 1 | ready | accepted | completed, [], [breach:Another Breach, breach:Example Breach, breach:Third Breach] | R1_NEW with two new comparisons/events in R1 order: Another, then Third | FALSE |

### Scenario 6 — HTTP-200 zero-finding body is unverifiable

File: r3_5_xon/06_zero_finding_unverifiable.json; subject subject-r35-06;
X1 on both scans.

| Scan/check | Body and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | one valid Example Breach; none | ready | accepted | completed, [], [breach:Example Breach] | R1_BASELINE | TRUE |
| 2/X1 | exact BODY_ZERO(subject-r35-06); prior completed | READY/ready/application/json | success_predicate_rejected | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE with prior completed; no disappearance | TRUE |

### Scenario 7 — HTTP 404 fails without disappearance

File: r3_5_xon/07_http_404_failed.json; subject subject-r35-07; X1 on both
scans.

| Scan/check | Input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid one-finding body; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | T_HTTP(404); prior completed | FAILED/http_failure/null | not_entered | failed, [response_failed], [] | R1_FAILED with prior completed; no disappearance | TRUE |

### Scenario 8 — HTTP 429 and 503 fail, showing immediate prior selection

File: r3_5_xon/08_http_429_503_failed.json; subject subject-r35-08; X1 on
all scans.

| Scan/check | Input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid one-finding body; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | T_HTTP(429); prior scan 1 completed | failed/http_failure/null | not_entered | failed, [response_failed], [] | R1_FAILED, prior completed | TRUE |
| 3/X1 | T_HTTP(503); prior is scan 2 failed, not scan 1 | failed/http_failure/null | not_entered | failed, [response_failed], [] | R1_FAILED, baseline_scan_id=scan-002, prior_status=failed | TRUE |
| 4/X1 | valid one-finding body; prior is scan 3 failed | ready | accepted | completed, [], one key | R1_REBASE (new silent baseline, not comparison to scan 1) | TRUE |

### Scenario 9 — invalid UTF-8 and malformed JSON are unverifiable

File: r3_5_xon/09_invalid_utf8_malformed_json.json; subject subject-r35-09;
X1 on all scans.

| Scan/check | Input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid one-finding body; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | status 200, CT_JSON, body_bytes_hex=ff, complete; prior completed | ready | rejected | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, reason response_unverifiable | TRUE |
| 3/X1 | malformed body text ending before }; prior is scan 2 unverifiable | ready | rejected | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, prior status unverifiable | TRUE |

### Scenario 10 — bad Content-Type metadata is unverifiable

File: r3_5_xon/10_content_type_metadata.json; subject subject-r35-10; X1 on
all scans. Each bad attempt contains a valid one-name body so only metadata
controls the result.

| Scan/check | Headers and prior state | Transport classification | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | CT_JSON; none | ready/ready/application/json | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | missing headers; prior completed | UNVERIFIABLE, incompatible_content_type, null | not_entered | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE | TRUE |
| 3/X1 | CT_PARAM; prior scan 2 | UNVERIFIABLE, content type has parameters, null | not_entered | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, prior unverifiable | TRUE |
| 4/X1 | CT_DUPLICATE; prior scan 3 | UNVERIFIABLE, duplicate header name, null | not_entered | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, prior unverifiable | TRUE |
| 5/X1 | CT_NONASCII; prior scan 4 | UNVERIFIABLE, content type is not ASCII, null | not_entered | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, prior unverifiable | TRUE |
| 6/X1 | CT_WRONG; prior scan 5 | UNVERIFIABLE, content type is not application/json, null | not_entered | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, prior unverifiable | TRUE |
| 7/X1 | HEADER_BAD plus body; prior scan 6 | UNVERIFIABLE, header name is malformed, null | not_entered | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, prior unverifiable | TRUE |

### Scenario 11 — post-status timeout and truncated body are incomplete

File: r3_5_xon/11_incomplete_body.json; subject subject-r35-11; X1 on all
scans.

| Scan/check | Input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid one-finding body; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | T_POST_TIMEOUT(prefix={"breaches":); prior completed | incomplete/post_status_body_failure/null | not_entered | unverifiable, [response_incomplete], [] | R1_UNVERIFIABLE, no disappearance | TRUE |
| 3/X1 | T_POST_TRUNCATED(prefix={"breaches":); prior scan 2 incomplete | incomplete/post_status_body_failure/null | not_entered | unverifiable, [response_incomplete], [] | R1_UNVERIFIABLE, prior unverifiable | TRUE |

### Scenario 12 — over-limit body is incomplete and never parsed

File: r3_5_xon/12_over_limit_body.json; subject subject-r35-12; X1 on both
scans.

| Scan/check | Input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid one-finding body; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | T_OVER_LIMIT, prefix "7b" repeated 16,384; prior completed | incomplete/body_over_limit/null | not_entered | unverifiable, [response_incomplete], [] | R1_UNVERIFIABLE, no disappearance | TRUE |

### Scenario 13 — echo mismatch cannot replace trusted subject

File: r3_5_xon/13_echo_mismatch.json; subject subject-r35-13; X1 on both
scans. The body’s email value is exactly other-subject and the trusted subject
remains subject-r35-13.

| Scan/check | Input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid body echoing subject; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | BODY_ECHO_MISMATCH(subject-r35-13); prior completed | ready | rejected | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, subject remains trusted | TRUE |

### Scenario 14 — hostile unknown-field false-clean body

File: r3_5_xon/14_hostile_unknown_field.json; subject subject-r35-14; X1 on
both scans.

| Scan/check | Body and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid one-finding body; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | BODY_HOSTILE(subject-r35-14); prior completed | ready | rejected | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, no disappearance despite apparent empty list | TRUE |

### Scenario 15 — bounded overlong JSON integer is unverifiable

File: r3_5_xon/15_overlong_json_integer.json; subject subject-r35-15; X1 on
both scans. The hostile body is under 16,384 bytes but contains a JSON integer
with 5,000 ASCII 1 digits, causing the existing strict parser’s bounded
integer conversion ValueError path.

| Scan/check | Input and prior state | Transport | XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|---|
| 1/X1 | valid one-finding body; none | ready | accepted | completed, [], one key | R1_BASELINE | TRUE |
| 2/X1 | exact BODY_OVERLONG_INTEGER; prior completed | ready | rejected | unverifiable, [response_unverifiable], [] | R1_UNVERIFIABLE, no crash and no disappearance | TRUE |

### Scenario 16 — contradictory local transport envelope is invalid

File: r3_5_xon/16_contradictory_transport_invalid.json; subject
subject-r35-16; source order X1. The only check has
/scans/0/checks/0/input/transport_attempt with http_status null, one CT_JSON
header, body_state "complete", empty body, no failure, and failure_phase null.
This is not a pre-status failure: TransportAttempt rejects it because a
complete response lacks an HTTP status. The exact fixed diagnostic is:

~~~text
code=construction_error
path=/scans/0/checks/0/input/transport_attempt
message=scenario could not construct an R1 record
~~~

Human mode has empty stdout, exactly this one stderr line, and exit code 2:

~~~text
INVALID_SCENARIO code=construction_error path="/scans/0/checks/0/input/transport_attempt" message="scenario could not construct an R1 record"
~~~

--json mode has empty stderr, exit code 2, and exactly this UTF-8 JSON line
with a terminal LF (shown in canonical sorted-key serialization):

~~~json
{"diagnostic":{"code":"construction_error","message":"scenario could not construct an R1 record","path":"/scans/0/checks/0/input/transport_attempt"},"mismatches":[],"result":"invalid_scenario","runner_version":"r3.5-visible-xon-scenarios/1","scans":[],"scenario_id":null}
~~~

There is no transport classification, XON classification, R2 SourceCheck, R1
report, exposure event, guard, or derived silence.

### Scenario 17 — XON failure with an independently changing source

File: r3_5_xon/17_xon_failure_mixed_source_change.json; subject
subject-r35-17; source order X1, B1 on both scans. This is expressible without
new comparison semantics because R2.5 already constructs multi-source
ScanAttempt values and the dispatch table merely selects the existing XON
adapter for X1 and existing R2 normalizer for B1.

| Scan/check | Input and prior state | Transport/XON | R2 | Complete R1 report | Silence |
|---|---|---|---|---|---|
| 1/X1 | valid XON body; none | ready/accepted | completed, [], [breach:Example Breach] | baseline for X1 and B1 | TRUE |
| 1/B1 | exact existing R2 synthetic-source-b active envelope; none | null/not_applicable | completed, [], [finding-b] | same scan baseline for both | TRUE |
| 2/X1 | T_HTTP(503); prior X1 completed | failed/not entered | failed, [response_failed], [] | X1 R1_FAILED, prior completed | FALSE overall because B1 changes |
| 2/B1 | exact existing R2 B1 retired envelope; prior B1 completed | null/not_applicable | completed, [], [finding-b] | B1 changed comparison with display_state and one exposure-changed event | FALSE |

The complete scan-1 report is exactly R1_BASELINE expanded for both source IDs,
with baseline_created_sources ["synthetic-source-b", "xposedornot.free.check-email"]
in R1's sorted order and all other arrays empty. The complete scan-2 report has
exactly two comparisons, ordered by source ID: the B1 changed/display_state
record first (`synthetic-source-b` sorts before
`xposedornot.free.check-email`), then the X1 source-level
not_comparable/response_failed record; one guarding_failed event for X1; one
exposure-changed event for B1; and no other records. The aggregate outcome is
incomplete. X1’s
failed response never suppresses B1’s valid comparison and never creates
disappearance.

## 16. Frozen human-readable output grammar

Valid R3.5 runs write only stdout and end every line with exactly one LF.
Stderr is empty for both pass and expectation mismatch. The R2.5 lines remain
in their established order; R3.5 inserts the following two lines immediately
before each XON SOURCE_CHECK line:

~~~text
TRANSPORT source_ref=<string> source_id=<string> source_check_id=<string> http_status=<integer-or-null> header_count=<count> body_bytes=<count> body_state=<string> transport_failure=<string-or-null> timed_out=TRUE|FALSE failure_phase=<string-or-null> normalized_content_type=<string-or-null> disposition=<string> reason=<string>
XON source_ref=<string> source_id=<string> source_check_id=<string> classification=<string>
~~~

For an XON check, the TRANSPORT line reports the actual public transport
projection and the XON line reports the two-case display projection from
Section 3. For the mixed synthetic R2 check, the exact lines use the same
source/check identifiers and these fixed values:

~~~text
TRANSPORT source_ref=<string> source_id=<string> source_check_id=<string> http_status=null header_count=0 body_bytes=<input_bytes> body_state="not_applicable" transport_failure=null timed_out=FALSE failure_phase=null normalized_content_type=null disposition="not_applicable" reason="not_applicable"
XON source_ref=<string> source_id=<string> source_check_id=<string> classification="not_applicable"
~~~

Here <input_bytes> is the decoded r2_bytes_hex length, as defined in Section
7. No TransportAttempt or XON classification is constructed for this source.
The existing R2 source-check line follows. The complete grammar is therefore
the R2.5 grammar plus these lines and the existing SOURCE_CHECK, R1 record,
derived EXPOSURE_SILENCE, mismatch, and summary lines. No raw header, body, or
R2 bytes are echoed; only bounded byte counts and classifications are printed.

Every field marked <string> is one compact JSON string with ensure_ascii=false;
arrays and objects are compact canonical JSON values; null is the JSON token
null; counts are unsigned decimal integers. The output must never print clean
or not found, and must print only actual disappeared R1 results.

## 17. Frozen canonical JSON output

--json writes exactly one UTF-8 JSON object plus one terminal LF. Top-level
keys are exactly, in canonical sorted serialization:

~~~text
runner_version, scenario_id, result, scans, mismatches, diagnostic
~~~

runner_version is exactly r3.5-visible-xon-scenarios/1. Valid result is pass
or expectation_mismatch; diagnostic is null. Scan key sets and R1 projection
key sets remain exactly the R2.5 sets. The new source-check object extends the
R2.5 projection with adapter_id, transport, and xon, and has exactly these
keys:

~~~text
source_ref, source_id, adapter_id, source_check_id, input_kind, input_bytes,
transport, xon, r2_invoked, r2, r1
~~~

transport is null for the mixed synthetic R2 check; otherwise it has exactly
http_status, header_count, body_bytes, body_state, transport_failure,
timed_out, failure_phase, normalized_content_type, disposition, and reason.
xon is null only for the mixed synthetic R2 check; otherwise it has exactly
classification. r2 is null only when an explicitly supported non-R2
construction path is used; normal XON transport construction errors invalidate
the scenario.

The R3.5-only internal projection failure is not a valid result or an invalid
scenario. When the READY/SourceCheck invariant in Section 3 triggers at
zero-based check position i and j, JSON mode discards all buffered normal
output and writes exactly one canonical UTF-8 object plus a terminal LF:

~~~json
{"diagnostic":{"code":"xon_projection_invariant","message":"XON adapter result contradicts its READY transport projection","path":"/scans/i/checks/j"},"mismatches":[],"result":"internal_error","runner_version":"r3.5-visible-xon-scenarios/1","scans":[],"scenario_id":"<validated literal scenario ID>"}
~~~

The scenario ID is the validated literal value, not a placeholder in the
actual output. stderr is empty, no XON classification or R1 report is
constructed, later scans are not run, and the exit code is 2. The diagnostic
code is accepted only by the R3.5 internal-error branch.

Serialization is UTF-8 JSON, ensure_ascii=false, sort_keys=true, compact
separators (',', ':'), and one terminal LF. Arrays are ordered by scan order,
operational source order for source checks, and the exact order returned by R1
for comparisons, exposure events, and guards. Mismatches are ordered by scan,
source/check projection order, R1 collection order, and RFC 6901 path. Object
key order is serialization only and never changes meaning.

## 18. Exit codes and scenario-level pass

The invocation remains module-based:

~~~text
python -m personal_watchdog.offline_simulator scenarios/r3_5_xon/01_first_finding_baseline.json
python -m personal_watchdog.offline_simulator --json scenarios/r3_5_xon/01_first_finding_baseline.json
~~~

Exit codes are exact:

| Code | Meaning |
|---:|---|
| 0 | Valid scenario and every transport, XON, R2, and complete R1 oracle matches. |
| 1 | Valid scenario, but at least one literal expected-versus-actual mismatch. |
| 2 | An R3.5 internal projection invariant failure, or an invalid scenario, construction contradiction, unsupported version, or unsafe input. The internal-error branch is not an invalid scenario. |

A scenario-level pass requires strict schema/reference validation; successful
construction of every requested transport attempt; explicit adapter dispatch;
an actual R2 SourceCheck for every XON check; actual ScanAttempt.create and
compare_scans for every valid scan; exact transport/XON/R2/R1 oracle matches;
no unaccounted event; and actual silence equal to
len(actual_r1.exposure_events) == 0. Scenario 16 is intentionally not a valid
pass scenario: its expected outcome is invalid-scenario exit 2.

## 19. Failure visibility and disappearance

HTTP 404, 429, 503, transport failure, timeout, incomplete body, over-limit
body, malformed or incompatible metadata, invalid UTF-8, malformed JSON,
unknown fields, echo mismatch, hostile values, and unsupported XON bodies
remain visible through transport/XON/R2 status and reason projections, then
through R1 not_comparable and its appropriate guard where a valid scan is
constructed. They never become completed-empty, a clean result, or
disappearance.

The check-email adapter has no completed-empty path. In particular, an
HTTP-200 breaches: [], breaches: [[]], empty name, invalid name, malformed
body, hostile body, failed check, timeout, incomplete body, incompatible body,
or unverifiable check cannot prove disappearance. A valid completed success
with at least one valid finding can prove disappearance only when a later
completed, comparable success still contains at least one valid finding but
omits the previous finding. Scenario 4 is the curated disappearance case.

The experiment must also test that a transport construction error is not
misclassified as a source result; Scenario 16 does so with exit code 2.

## 20. Exact Phase 2 implementation files

After adversarial review and separate approval, the proposed implementation
scope is exactly:

1. Modify personal_watchdog/offline_simulator.py to add strict R3.5 version
   dispatch, transport-input validation, calls to the existing R3 adapter,
   non-semantic transport/XON projections, the R3.5 output branch, and shared
   literal oracle comparison. Preserve the R2.5 branch byte-for-byte in
   behavior.
2. Add tests/fixtures_r3_5_xon_scenarios.py for synthetic body/header
   constants, path helpers, CLI helpers, and literal oracle assertions. It
   must contain no real identifier and no network helper.
3. Add tests/test_r3_5_visible_xon_scenarios.py covering every file in the
   curated set, delegation spies, exact output, mismatches, invalid transport
   construction, bounds, byte encoding, failure visibility, prior-state
   selection, and R2.5 regression output.
4. Add exactly these scenario files under scenarios/r3_5_xon/:

   ~~~text
   01_first_finding_baseline.json
   02_identical_finding.json
   03_additional_breach.json
   04_one_disappears_one_remains.json
   05_multiple_simultaneous_findings.json
   06_zero_finding_unverifiable.json
   07_http_404_failed.json
   08_http_429_503_failed.json
   09_invalid_utf8_malformed_json.json
   10_content_type_metadata.json
   11_incomplete_body.json
   12_over_limit_body.json
   13_echo_mismatch.json
   14_hostile_unknown_field.json
   15_overlong_json_integer.json
   16_contradictory_transport_invalid.json
   17_xon_failure_mixed_source_change.json
   ~~~

5. Append the required implementation record updates to
   BUILD_HISTORY.md, RESEARCH_LOG.md, and PROGRESS_LOG.md. Keep
   DECISIONS.md and REFERENCES.md unchanged unless a genuinely new
   project-level decision or source is introduced and reported before that
   change.

The existing xposedornot_check_email_adapter.py, r1.py, r2_adapter.py, R2.5
scenario files, existing fixtures, pyproject.toml, REFERENCES.md, and
DECISIONS.md are not proposed for modification. The R3 adapter is used as
committed.

## 21. Exact delegation tests

The Phase 2 tests must prove delegation rather than reproduce semantics:

- patch offline_simulator.normalize_check_email with a wrapping spy and
  assert one call per valid XON check, with a constructed TransportAttempt
  and no call for Scenario 16;
- patch offline_simulator.classify_transport with a wrapping spy and assert
  transport projections come from its returned object, including the exact
  404/429/503, metadata, incomplete, and over-limit precedence;
- patch offline_simulator.normalize_response and assert the XON runner does
  not call R2 directly for XON checks; the call occurs inside the existing XON
  adapter, while the mixed B1 check calls the existing R2 path exactly once;
- patch offline_simulator.compare_scans with a wrapping spy and assert one
  call per valid scan after all source checks are built, with the immediately
  preceding ScanAttempt object;
- mutate an adapter-produced result through a test double and prove expected
  values cannot alter actual R2 or R1 output;
- use a test double that returns an unexpected status after READY transport and
  assert both the exact human INTERNAL_ERROR line and the exact JSON
  internal_error object, exit 2, discarded normal output, no R1 report, and no
  later scans;
- assert the runner source contains no duplicate implementation of XON body
  keys, breach bounds, finding-key construction, transport precedence, R2
  envelope construction, comparison_id, or guard_id formulas; and
- keep the existing R2.5 golden-output tests unchanged and passing.

These tests are structural delegation tests, not permission to add a second
semantic implementation hidden behind projections.

## 22. Unresolved policy questions and limitations

R3.5 deliberately does not settle repeated-failure suppression, recovery
events, disappearance confirmation, trivial-change suppression, bark grouping,
baseline overload, minimum actionable bark information, or persistence or
selection of an older successful baseline. It exposes the current immediate
prior-state mechanics and leaves policy experiments for later review.

The XON experiment still cannot establish:

- whether the live endpoint accepts the documented path/query combination;
- whether live response schemas are closed or stable;
- whether breaches is exhaustive, current, paginated, ordered, or complete;
- whether a live no-result body is HTTP 404, HTTP 200, or another shape;
- whether live content-type parameters, compression, or charset differ from
  the synthetic predicate;
- whether rate-limit or server failures have the documented status/body
  combinations;
- whether the synthetic response echo corresponds to ownership of the
  subject; or
- whether any R1 exposure event is useful, safe, or worth notifying.

## 23. Approval boundary

This document frames R3.5 only. It creates no scenario file and makes no
source or test change. Phase 2 must stop if it would require changing R1,
R2, R2.5, or R3 semantics; adding a second XON/R2/R1 implementation; adding
a dependency; using a real identifier; enabling a network request; changing
the immediate prior-state rule; or settling an open bark policy question.

Do not stage, commit, push, merge, implement, enable live scanning, add
credentials, add persistence, add analytics, or modify the evidence archive.
Stop here for adversarial framing review.
