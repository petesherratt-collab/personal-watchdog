# Personal Watchdog Codex itinerary

Status: Milestone 0 complete; revised Milestone 1 proposal awaiting approval.

This itinerary is the approval boundary for Personal Watchdog work. It applies
only to `/home/peters/personal-watchdog`. The repository at
`/home/peters/evidence-collection/repo` is read-only architectural reference
material and is not a destination for Personal Watchdog files.

## Non-negotiable boundaries

- Work offline with obviously synthetic identifiers under reserved domains.
- Do not add live adapters, external timestamping, raw-page retention,
  background services, public exports, browser interfaces, backups, or
  deployment machinery.
- Do not add dependencies without separate approval. Milestone 1 uses the
  Python standard library plus the already approved development tools.
- Keep a failed, blocked, malformed, timed-out, or unverifiable adapter result
  distinct from a successful comparable result with no observations.
- Retain only selective, bounded evidence. Never store complete raw responses.
- Do not implement Milestone 1 until this revised proposal is approved.

## Approved architectural principles from Kibitzr

The reference architecture contributes principles, not code:

1. Record every attempted scan, not only changes or successful scans.
2. Use append-only records and represent corrections as later records.
3. Canonically serialize and hash versioned records into a continuity chain.
4. Recompute the chain from record fields; never trust stored hashes alone.
5. Reconcile every referenced evidence object and detect missing, corrupt,
   substituted, orphaned, or stray objects.
6. Keep the independent verifier separate from the writer implementation.
7. Test hostile mutations and internally consistent rewrites, not just ordinary
   read/write round trips.
8. State the limit honestly: without an external commitment, an offline hash
   chain detects accidental damage and unsophisticated edits but cannot prove
   trustworthy time or prevent a keeper from rewriting the entire archive.

Raw-response retention and external anchoring are deliberately not adopted.

## Milestone 0: repository and decision foundation

Milestone 0 contains policy, privacy and security documentation, packaging and
development-tool configuration, policy smoke tests, this itinerary, and the
progress journal. It contains no scanner, identity store, adapter, ledger,
evidence writer, report generator, or network integration.

Milestone 0 completion gate:

- repository contents and Git state inspected;
- privacy and truthful-failure rules documented;
- no runtime dependencies;
- tests, formatting, linting, type checks, and `git diff --check` pass;
- no real identifiers, credentials, or secrets appear in project material;
- Milestone 1 remains unimplemented pending explicit approval.

## Milestone 1: fully offline vertical slice — proposed

Milestone 1 will demonstrate one complete local path using only synthetic
fixture input:

1. Start a scan and append a `scan_started` event.
2. Run an in-process fixture adapter that performs no network access.
3. Validate its bounded structured output.
4. Write selective canonical evidence objects, if any.
5. Append one terminal `adapter_completed`, `adapter_incomplete`, or
   `adapter_failed` event per planned adapter invocation.
6. Derive and append exactly one terminal scan event: `scan_completed`,
   `scan_incomplete`, or `scan_failed`.
7. Compare only compatible completed scans for absence/change claims.
8. Verify the ledger chain and reconcile all selective evidence with a separate
   standard-library-only verifier.

No Milestone 1 implementation begins until the following design is approved.

## Proposed scan-ledger schema

The ledger is a local SQLite database. SQLite is a storage container, not the
trust root. Rows are append-only by application policy and are checked by the
independent verifier.

### `ledger_meta`

| column | type | rule |
|---|---|---|
| `key` | TEXT PRIMARY KEY | Known keys only |
| `value` | TEXT NOT NULL | Canonical textual value |

Initial keys are `schema_version=1`, `chain_version=1`, and a fixed
`archive_format=personal-watchdog-ledger` domain label. Metadata is configuration
for interpretation; the verifier does not use a mutable stored chain head as
evidence.

### `ledger_event`

| column | type | rule |
|---|---|---|
| `sequence` | INTEGER PRIMARY KEY | Positive and contiguous from 1 |
| `event_id` | TEXT UNIQUE NOT NULL | Lower-case UUID textual form |
| `event_type` | TEXT NOT NULL | Closed set for the record version |
| `recorded_at` | TEXT NOT NULL | UTC RFC 3339 seconds, ending in `Z`; unverified |
| `record_version` | INTEGER NOT NULL | Starts at 1 |
| `payload_json` | TEXT NOT NULL | Exact canonical JSON object |
| `prev_hash` | TEXT NOT NULL | Previous recomputed hash or genesis |
| `record_hash` | TEXT NOT NULL | Lower-case SHA-256 hex of the chain preimage |

Event payloads use synthetic opaque `scan_id`, `adapter_run_id`, and
`subject_id` values. They never contain a complete email address. The first
closed event set is:

- `scan_started`: scan ID, ordered adapter plan, plan digest, and subject IDs;
- `adapter_completed`: comparable successful result and evidence digests;
- `adapter_incomplete`: bounded partial result plus explicit limitation codes;
- `adapter_failed`: no comparable result plus explicit failure codes;
- `scan_completed`, `scan_incomplete`, or `scan_failed`: aggregate counts,
  ordered terminal adapter-event IDs, and plan digest;
- `correction_recorded`: target event IDs or sequence interval, reason code,
  corrected assertion, effective time if known, and recording time.

Error codes and limitation codes are hashed facts. Human-readable diagnostic
text is local display context and must be redacted and bounded; Milestone 1
should either hash it explicitly or omit it rather than imply it is attested.

### Selective evidence objects

Evidence is stored outside SQLite as canonical JSON bytes at:

`data/evidence/sha256/<first-two-hex>/<digest>.json`

Each object has `evidence_version`, synthetic subject ID, adapter name and
version, normalized observation kind, bounded factual fields, source category,
and an unverified observation time when supplied by the fixture. It contains no
raw page, complete email address, secret, unrelated personal data, HTML, or
executable content. The SHA-256 filename is computed over the exact canonical
bytes. Terminal adapter events commit to an ordered, duplicate-free list of
these digests.

## Scan outcome semantics

Outcomes describe comparability, not whether observations were found.

### `completed`

Every adapter invocation in the committed plan produced a terminal comparable
result, its output passed structural and semantic validation, every referenced
evidence object was durably written and re-readable, and the plan/result set is
internally consistent. Zero observations is allowed and means only “no
observation in these successful fixture results.”

### `incomplete`

At least one planned adapter produced a comparable completed result and at least
one planned adapter did not. The latter may be partial, blocked, malformed,
timed out, cancelled, or otherwise unverifiable. Successful subsets remain
facts, but the scan cannot support whole-plan absence or disappearance claims.
Milestone 1 does not promote an incomplete scan to the comparable baseline.

### `failed`

No planned adapter produced a comparable completed result, or the scan could
not safely finalize because its plan/result relationship or selective evidence
failed validation. A recordable orchestration or fixture-adapter failure is a
failed scan. A storage failure that prevents appending the terminal event is not
misreported as a finalized failed scan; verification will instead expose an
unterminated `scan_started` sequence.

An adapter failure never becomes an empty successful result. Finding presence
is independent of scan outcome: completed scans may contain zero or many
observations.

## Canonical JSON serialization

Canonical bytes are produced and independently reproduced with these exact
rules:

- JSON value must be an object at the top level.
- Allowed values are objects, arrays, strings, integers, booleans, and null.
- Floating-point numbers are forbidden; `NaN` and infinities are forbidden.
- Object keys are strings and sorted lexicographically by Unicode code point.
- All strings and keys must already be Unicode NFC; non-NFC input is rejected,
  not silently rewritten.
- Arrays retain their defined order. Set-like collections must be sorted by
  their specification before serialization and contain no duplicates.
- Serialize with UTF-8 encoded Python
  `json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
  allow_nan=False)`.
- Emit no trailing newline, byte-order mark, or insignificant whitespace.
- Timestamps use UTC RFC 3339 at whole-second precision (`YYYY-MM-DDTHH:MM:SSZ`)
  and are explicitly unverified local or fixture-supplied values.

The verifier implements these rules itself and rejects stored JSON whose bytes
are not already canonical.

## Chain genesis and linking

- There is one global ledger chain so ordering across scans and corrections is
  explicit.
- Genesis is exactly 64 lower-case zero characters.
- For sequence 1, `prev_hash` must equal genesis.
- For every later sequence, `prev_hash` must equal the independently recomputed
  hash of the immediately preceding sequence.
- Sequences must be contiguous, unique, and strictly increasing from 1.
- The record preimage is canonical JSON with this shape:

```json
{"chain":"personal-watchdog-ledger","chain_version":1,"event":{"event_id":"...","event_type":"...","payload":{},"record_version":1,"recorded_at":"...","sequence":1},"prev":"0000000000000000000000000000000000000000000000000000000000000000"}
```

- `record_hash` is lower-case hexadecimal SHA-256 of those exact UTF-8 bytes.
- Verification recomputes every preimage from stored fields and never accepts
  `record_hash`, `prev_hash`, metadata, or a cached head without reconstruction.
- This chain does not authenticate timestamps and does not resist a complete
  rewrite by an actor controlling the database and all local files.

## Record and schema versioning

- `schema_version` describes the SQLite layout. Milestone 1 starts at 1.
- `record_version` describes event field meaning. Every event commits to it.
- `chain_version` describes the hash preimage and linking algorithm. Every
  preimage commits to it.
- Additive database changes may increment `schema_version` without changing old
  record bytes or their hashes.
- A semantic change to an event requires a new `record_version`; old versions
  remain verifiable under their original rules.
- A change to canonicalization or the preimage requires a new `chain_version`
  and an explicit continuation/migration design. Existing rows are never
  silently rehashed.
- Unknown versions fail closed as unsupported, not verified.

## Selective evidence reconciliation

The writer uses write-to-temporary-file, flush, and atomic replace within the
target directory before appending an event that references an object. The
verifier then:

1. derives the expected digest set only from completed and incomplete adapter
   events, never from an untrusted index;
2. rejects malformed, duplicate, or non-canonical digest references;
3. requires each referenced object at its digest-derived path;
4. reads bounded bytes, rejects symlinks and paths escaping the evidence root,
   recomputes SHA-256, and requires canonical JSON;
5. validates the object version and privacy-safe evidence shape independently;
6. reports referenced missing, unreadable, misnamed, non-canonical, or malformed
   objects as `broken`;
7. reports well-formed unreferenced objects and interrupted `.tmp` files as
   `suspect`, not as verified evidence; and
8. never treats an evidence problem as “no observation” or a clean scan.

Milestone 1 defines fixed byte, item-count, string-length, and nesting limits in
both writer and verifier. Exact numeric limits will be fixtures-backed constants
in their respective implementations and listed in user documentation before
code approval is considered complete.

## Append-only correction records

Ledger events and evidence objects are never edited to tidy history. A
`correction_recorded` event identifies the affected event IDs or contiguous
sequence interval and records:

- a closed reason code;
- the corrected bounded assertion;
- `effective_at`, when the corrected fact became true, if known;
- `recorded_at`, when the correction was appended; and
- optional replacement evidence digests that pass normal reconciliation.

A correction does not erase or make the original event unverifiable. Readers
must display both and apply corrections in ledger order. Milestone 1 will not
provide a command that updates or deletes existing ledger events.

## Independent verifier boundary

The verifier is a separate executable Python module using only the standard
library. It must not import Personal Watchdog's writer, models, serialization,
storage, hashing, adapter, or evidence implementation. It may use only the
published format specification in this itinerary and its own code for:

- opening SQLite read-only;
- validating schema and closed values;
- parsing and reproducing canonical JSON;
- recomputing event hashes and chain links;
- checking scan state-machine and aggregation invariants;
- reconciling selective evidence objects; and
- emitting a deterministic finding list and nonzero exit status for broken or
  unsupported archives.

The writer and verifier may share fixture files containing inert example
archives, but not executable implementation code. Agreement is a cross-check,
not proof of correctness; mutation tests must assert the written specification.

## Proposed mutation tests

Milestone 1 must cover at least:

1. edit a hashed event field without changing hashes;
2. edit a field and recompute only that row's hash;
3. delete the first, middle, or final event;
4. insert, duplicate, or reorder events;
5. create a sequence gap or duplicate event ID;
6. change `prev_hash`, `record_hash`, record version, or chain version;
7. rewrite the entire local chain consistently and demonstrate the documented
   residual limitation: without an external commitment this is not detectable;
8. replace evidence bytes while retaining the filename;
9. rename evidence to its new digest while leaving the committed reference;
10. delete referenced evidence;
11. add orphan or temporary evidence files;
12. use a symlink or traversal-shaped evidence reference;
13. supply non-canonical JSON, duplicate set-like entries, non-NFC strings,
    floats, excessive nesting, oversized strings, or oversized files;
14. omit, duplicate, or contradict a planned adapter terminal event;
15. label a scan completed when any adapter is incomplete or failed;
16. label a scan incomplete with no comparable adapter result;
17. label a scan failed despite a comparable completed adapter result;
18. convert adapter failure into zero-observation success;
19. infer disappearance from an incomplete or failed scan;
20. leave a started scan unterminated and require it to remain visibly open;
21. mutate correction targets, effective time, or replacement evidence;
22. use an unknown schema, record, evidence, or chain version; and
23. verify deterministic finding order and stable exit status.

Both normal tests and mutated archives use synthetic identifiers only and make
no network requests.

## Milestone 1 implementation sequence after approval

1. Freeze this format specification and exact bounds in tests.
2. Add small immutable domain types and outcome aggregation tests.
3. Add canonical serialization and ledger hashing with adversarial tests.
4. Add SQLite append-only writer and interruption/state-machine tests.
5. Add bounded selective evidence writer and reconciliation tests.
6. Add the fixture adapter and one zero-observation, one finding, one partial,
   and one failed synthetic scenario.
7. Add the independent standard-library verifier without importing writer code.
8. Run cross-implementation fixtures and the full mutation suite.
9. Run pytest, Ruff format/lint, strict mypy, `git diff --check`, privacy/secret
   scans, and review the complete diff and uncommitted-file list.
10. Stop for approval before any later milestone.

## Approval gate

Approval of this document authorizes only the offline Milestone 1 vertical
slice above. It does not authorize any excluded feature, dependency, real
identifier, network access, publication, or deployment.
