# Research Experiment R3 Phase 1 — XposedOrNot contract framing

**Status: current documentation-only specification.** No adapter, HTTP client,
credential flow, persistence, or live request is authorized by this document.
No functional XposedOrNot lookup endpoint was called and no identifier or
credential was submitted.

## 1. Experimental claim and non-claims

### Claim

The documented free XposedOrNot check-email family can be framed for one
later synthetic experiment without turning transport, authentication,
authorization, rate-limit, service, HTTP, content-type, schema, parsing,
timeout, partial-response, or ambiguity failures into `completed-empty` or
disappearance, provided the exact predicates and boundaries in this document
are used.

The first synthetic experiment is limited to keyless
`GET /v1/check-email/{email}` with `include_details=false`. The free
breach-analytics family is separately documented and deferred.

### Non-claims

This research does not claim that XposedOrNot responses are complete, current,
unique, ordered, stable, or exhaustive; that the service proves ownership of
the checked subject; that a no-match result proves safety; or that the public
examples are a closed live schema. It does not authorize a live adapter,
credential use, identifier submission, retry policy, or source-data archive.

## 2. Repository reconciliation

The repository remains authoritative and supplies the applicable boundary:

- R1 owns canonical source identity, comparison, comparability, exposure, and
  disappearance semantics.
- R2 owns bytes-first validation of its response envelope and construction of
  one R1 `SourceCheck`.
- The existing R2 maps `failed` to a failed source check and maps
  `unverifiable` or `incomplete` to a non-comparable source check with no
  accepted observations.
- R2 deterministically deduplicates equal observations with the same finding
  key and rejects conflicting observations with that key.

No material contradiction blocks this documentation experiment. This framing
does not change R1, R2, R2.5, the offline simulator, tests, fixtures, or
`DECISIONS.md`.

## 3. Official sources and provenance

All sources were accessed on **2026-09-08**. Only official XposedOrNot
documentation and official repositories were examined.

### Official web documentation

| Source | Provenance and use |
|---|---|
| [API documentation](https://xposedornot.com/api_doc) | “Free Data Breach API, No API Key Required”; API Quick Reference last updated 2026-06-03. Primary endpoint, response, quota, and status documentation. |
| [Swagger UI](https://api.xposedornot.com/docs) | Official page titled “XposedOrNot API Documentation”. Documentation artifact only; no interactive request was made. |
| [OpenAPI JSON](https://api.xposedornot.com/openapi.json) | Exact bytes examined on 2026-09-08. SHA-256: `d9fae920f9986e0fd0bf0e181f67f9bdc3413c653f83e33f1e5cbe753bf64d20`. Reports OpenAPI `3.0.0`, `info.version` `2.0.0`, and server `https://api.xposedornot.com`. The downloaded bytes were not committed. |

### Immutable official GitHub sources

Mutable branch URLs are not reproducible source versions. The following full
SHAs and commit/file permalinks are the sources used:

| Source | Full SHA and immutable permalink | Use |
|---|---|---|
| API repository README | `cbf5423ed601bd74d896efebd0d28c637a6cddef`; [commit](https://github.com/XposedOrNot/XposedOrNot-API/commit/cbf5423ed601bd74d896efebd0d28c637a6cddef), [README](https://github.com/XposedOrNot/XposedOrNot-API/blob/cbf5423ed601bd74d896efebd0d28c637a6cddef/README.md) | Identifies `/docs` and `/openapi.json`, endpoints, limits, and API-key behavior. |
| Python SDK README | `911f49aa08939827d4717f3d48fd192c0c072c29`; [commit](https://github.com/XposedOrNot/XposedOrNot-Python/commit/911f49aa08939827d4717f3d48fd192c0c072c29), [README](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/README.md) | Official client models and documented client behavior. |
| Python SDK client | Same SHA; [client.py](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/xposedornot/client.py) | Client status/error handling and timeout behavior. |
| Python SDK email endpoints | Same SHA; [email.py](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/xposedornot/endpoints/email.py) | Client paths and query parameters. |
| JavaScript SDK README | `d4cf1af21a53c32c03d767a59d382b01b4a21908`; [commit](https://github.com/XposedOrNot/XposedOrNot-JS/commit/d4cf1af21a53c32c03d767a59d382b01b4a21908), [README](https://github.com/XposedOrNot/XposedOrNot-JS/blob/d4cf1af21a53c32c03d767a59d382b01b4a21908/README.md) | Independent official SDK evidence for client behavior. |

The live Swagger/OpenAPI artifacts have no Git commit SHA. Their access date,
reported versions, and exact JSON-byte hash are recorded above; the JSON file
itself is not added to the repository.

## 4. OpenAPI findings: resolved and unresolved facts

The OpenAPI specification resolves these facts:

- Free check-email is `GET /v1/check-email/{email}` with required path
  `email: string` formatted as an email and optional query
  `include_details: boolean`, default `false`.
- Free check-email documents HTTP 200 and 404. Its 200 media type is
  `application/json`; the shown properties are `breaches` as an array of
  arrays of strings and `email` as a string.
- Free analytics is `GET /v1/breach-analytics` with required query
  `email: string` formatted as an email and optional string `token`. Its 200
  media type is `application/json`, and its named top-level components are
  `BreachMetrics`, `BreachesSummary`, `ExposedBreaches`, `ExposedPastes`,
  `PasteMetrics`, and `PastesSummary`.
- The catalogue specification adds an `if-modified-since` header and 304
  response, but catalogue behavior is outside the selected experiment.

The specification does not resolve these apparent unknowns:

- No response property is required and `additionalProperties: false` is not
  declared, so the schemas are not closed.
- The website’s found check-email example includes `status: "success"`, but
  the OpenAPI 200 schema omits it. The selected synthetic contract freezes the
  website example’s status field and treats this as a documented source-schema
  discrepancy.
- The website check-email no-match example has `email: null`, while the
  OpenAPI 404 schema describes `email` as a string.
- The website analytics no-match sample contains null components and two
  non-null empty summary objects, while OpenAPI describes two components as
  arrays and does not define the no-match predicate.
- Charset, compression, maximum response size, pagination, truncation,
  ordering, duplicate semantics, freshness, completeness, and a closed
  analytics error schema remain unspecified.

OpenAPI version `2.0.0` is specification metadata, not a freshness guarantee
or a claim that response data is versioned by that value.

## 5. Separate endpoint families and selected experiment

Free check-email and free breach-analytics are separate contracts. They have
different source identities, canonical scopes, schema versions, normalization
policies, finding interpretations, and synthetic matrices.

| Family | Source identity | Canonical scope | Schema version | Phase status |
|---|---|---|---|---|
| Free check-email | `xposedornot.free.check-email` | `GET /v1/check-email/{email}`, keyless, `include_details=false` | `xon-check-email/1` | **Selected first synthetic experiment** |
| Free breach-analytics | `xposedornot.free.breach-analytics` | `GET /v1/breach-analytics?email={email}`, keyless, no token | `xon-breach-analytics/1` | Deferred; separate matrix only |

The check-email experiment must not accept analytics bodies. The analytics
experiment is not selected for implementation and does not supply empty-result
semantics to check-email.

## 6. Selected check-email success predicate

The selected synthetic contract accepts a check-email success only when every
condition below holds:

1. The transport attempt has HTTP status exactly `200`.
2. The body state is `complete` and the body bytes are the complete response,
   not a prefix or locally bounded fragment.
3. The derived normalized media type is exactly `application/json`.
4. The complete body decodes as strict UTF-8 JSON, rejects duplicate object
   keys and non-standard JSON constants, and has a top-level object with
   exactly these keys and no others:

   ```text
   {"breaches": ..., "email": ..., "status": "success"}
   ```

5. `status` is required and exactly the string `"success"`.
6. `email` is a JSON string of 1–128 Unicode code points, contains no surrogate
   code points, is NFC-normalized, and is exactly equal to the locally
   supplied synthetic request identifier by code-point equality. No trimming,
   case-folding, or response-derived normalization is applied.
7. `breaches` is an array containing exactly one inner array. The inner array
   contains 1–16 JSON strings. Each string is a breach name of 1–64 Unicode
   code points, contains no surrogate code points, is NFC-normalized, and is
   not empty. The original name is retained; no trimming, case-folding, or
   sorting is applied before R2 normalization.
8. Every breach name maps to one valid finding candidate. Duplicate names are
   passed to existing R2 duplicate handling; they do not create a new XON
   duplicate policy.

The response email is untrusted response data. It cannot populate
`subject_ref`, source identity, canonical scope, or any other trusted context.
An echo mismatch is `unverifiable` with no accepted observations.

The selected contract has no completed-empty path. An HTTP-200 body with
`breaches: []`, `breaches: [[]]`, an empty breach-name string, an invalid name,
or otherwise zero valid finding candidates is always `unverifiable`, never
`completed-empty` and never disappearance.

## 7. Analytics contract and exact deferred no-match sentinel

Analytics remains deferred under source identity
`xposedornot.free.breach-analytics` and schema `xon-breach-analytics/1`.

The documented analytics no-match fixture is named
**`XON_ANALYTICS_HTTP_200_NO_MATCH_V1`**. It is accepted only when:

- HTTP status is exactly `200`;
- derived normalized media type is exactly `application/json`;
- body state is `complete` and strict UTF-8/JSON validation succeeds; and
- the top-level object has exactly these six keys and exact values:

  ```text
  {
    "BreachMetrics": null,
    "BreachesSummary": {"site": ""},
    "ExposedBreaches": null,
    "ExposedPastes": null,
    "PasteMetrics": null,
    "PastesSummary": {"cnt": 0, "domain": "", "tmpstmp": ""}
  }
  ```

The two non-null empty summary objects are part of the predicate. Only this
exact predicate under the analytics source identity is `completed-empty`.
Missing, extra, or differently typed values are not the sentinel.

The website documents this body as an HTTP-200 no-match response. OpenAPI
does not define this variant, so the exact predicate is a deliberately frozen
deferred synthetic contract, not a claim that the OpenAPI schema is closed.

## 8. Request encoding, authentication, and authorization

The selected check-email request is an HTTPS GET with one path value and no
credential. The OpenAPI specification resolves the optional query name as
`include_details`; the website page uses `details`, and the official Python
client uses `include_details`. The selected synthetic request contract uses
`include_details=false` and records the website/specification discrepancy.

The locally supplied synthetic request identifier is the only subject value
that a later approved adapter could submit. The response echo is never a
source of identity. No identifier is supplied in this phase.

The basic check-email and analytics endpoints are documented as keyless. The
domain route and Plus route are separate authorized families and are excluded.
Missing, invalid, or unauthorized credentials in any future authorized family
are failures, not empty results.

## 9. Rate limits and quota behavior

The website documents free-tier per-IP, per-endpoint limits:

| Endpoint | Per second | Per hour | Per day |
|---|---:|---:|---:|
| `/v1/check-email/{email}` | 2 | 25 | 100 |
| `/v1/breach-analytics` | 2 | 25 | 100 |
| `/v1/breaches` | 2 | 50 | 100 |
| `/v1/domain-breaches` | 2 | 25 | 50 |
| `/v1/metrics` | 5/min | 50 | 100 |

The API repository documents HTTP 429 with `Retry-After`, `retry_after`, and
`reset_time`; the website documents waiting for the quota window. Official
SDKs describe client-side spacing and retries, which are not server guarantees.
Any terminal 429 or exhausted retry policy is `failed`, not empty.

## 10. HTTP statuses and response classification

For the selected check-email family, the frozen synthetic classification is:

| Condition | Classification | R1 consequence |
|---|---|---|
| HTTP 200 and exact success predicate | `completed` | Findings may be compared. |
| HTTP 200 with zero valid findings | `unverifiable` | No observations; no disappearance. |
| HTTP 200 malformed, incompatible, error-shaped, or ambiguous body | `unverifiable` | No observations; no disappearance. |
| HTTP 404 | `failed` | No observations; no disappearance. |
| HTTP 401, 422, or other authorization failure | `failed` | No observations; no disappearance. |
| HTTP 429 | `failed` | No observations; no disappearance. |
| HTTP 502, 503, or other terminal 5xx | `failed` | No observations; no disappearance. |
| Other 2xx | `unverifiable` unless separately frozen; no empty inference. | No observations; no disappearance. |
| Timeout or transport failure | `failed` | No observations; no disappearance. |
| Incomplete or over-limit body | `incomplete` at the transport boundary, then R2/R1 `unverifiable` | No partial observations or disappearance. |

The analytics family uses its own equivalent status classification, with only
`XON_ANALYTICS_HTTP_200_NO_MATCH_V1` eligible for `completed-empty`.

## 11. Response encoding, errors, and empty semantics

The official website says responses are JSON. OpenAPI declares
`application/json` for the two email-family 200 responses. Neither source
specifies a charset, compression, or maximum body size. The selected synthetic
contract requires normalized media type exactly `application/json` and strict
UTF-8 JSON decoding; content-type parameters do not supply a second encoding
truth.

The website check-email no-match body contains an `Error` string and
`email: null`, while OpenAPI documents a 404 error schema with `Error: string`
and `email: string`. The status of the website example is not separately
stated. This is an HTTP/error ambiguity and is never a completed-empty path.

An HTTP-200 error object, undocumented object, missing field, wrong type,
invalid JSON, invalid UTF-8, or echo mismatch is `unverifiable`. Raw error
bytes are not observations and may only be retained as bounded diagnostics in
a separately approved implementation.

## 12. Exact `TransportAttempt` envelope

The later synthetic experiment uses one local in-memory envelope. It is not an
HTTP client and does not authorize a request.

```text
TransportAttempt {
  http_status: integer | null,
  bounded_headers: array of Header,
  normalized_content_type: string | null,  # derived, never independent truth
  body_bytes: bytes,
  body_state: "complete" | "incomplete" | "over_limit" | "absent",
  transport_failure: null | "transport",
  timed_out: boolean,
  failure_phase: null | "before_status" | "after_status",
  trusted_context: TrustedContext
}

Header {
  name_bytes: bytes,
  value_bytes: bytes
}

TrustedContext {
  scan_id: string,
  source_check_id: string,
  subject_ref: string,
  source_id: string,
  canonical_scope: array of strings,
  adapter_id: string,
  adapter_version: string,
  schema_version: integer,
  normalization_version: integer,
  material_field_policy: object
}
```

### 12.1 Exact bounds and header rules

The envelope freezes these limits:

- `MAX_XON_BODY_BYTES = 16_384` bytes.
- `MAX_XON_HEADER_COUNT = 16` entries.
- Each raw header name is at most 64 bytes and each raw header value is at
  most 512 bytes. Header bytes are retained as received; they are not decoded
  before bounds checking.
- The exact retained-header byte total is
  `sum(len(name_bytes) + 1 + len(value_bytes) + 1)` for every retained entry,
  where the first `1` is the ASCII colon separator `:` and the second `1` is
  the ASCII line-feed byte `0x0A` terminating that entry. The total must
  be at most 8,192 bytes. No other separator, whitespace, or framing byte is
  counted.
- Only `content-type`, `content-length`, `retry-after`, `date`, `etag`,
  `last-modified`, `location`, and `server` may be retained.
- `bounded_headers` is raw untrusted metadata. Header names are compared by
  ASCII lower-casing only after bounds checking. A valid received response
  containing duplicate names is rejected before content-type derivation and is
  classified `unverifiable`; values are not merged and there is no
  first-value-wins rule. A locally contradictory fixture is instead a
  construction rejection as specified below.
- A raw header name containing non-ASCII bytes, an invalid retained header
  shape, or an unsupported retained name is malformed untrusted metadata in a
  valid transport attempt and is classified `unverifiable` before XON parsing.

### 12.2 Exact content-type derivation

The derivation is deterministic and occurs only after duplicate-name checking:

1. Select the sole retained header whose name, after ASCII lower-casing, is
   `content-type`. No header means the derived value is null.
2. Remove only leading and trailing ASCII optional whitespace bytes `0x20`
   (space) and `0x09` (horizontal tab) from the raw value. No other Unicode or
   whitespace character is removed.
3. If any byte remaining after that trim is non-ASCII, the content-type is
   malformed untrusted metadata and the valid transport attempt is
   `unverifiable`.
4. If the trimmed value contains `;` or any parameter, including
   `charset=utf-8`, it is rejected as an incompatible content type and the
   valid transport attempt is `unverifiable`.
5. Compare the remaining bytes ASCII case-insensitively with exactly
   `application/json`. An exact match derives
   `normalized_content_type="application/json"`; any other value derives no
   accepted media type and is `unverifiable`.

The normalized value is computed from bounded raw metadata, never supplied as
an independent truth. If a fixture serializes a derived value, it must equal
the recomputed value or the fixture is a malformed local envelope and is
rejected before the synthetic experiment runs.

### 12.3 Exact status, failure, and body-state invariants

- `http_status` is null or an exact integer in the inclusive range 100–599.
- `failure_phase` is null exactly when both `transport_failure` is null and
  `timed_out` is false. `transport_failure` and `timed_out` cannot both be
  active.
- A failure before an HTTP status is received has
  `failure_phase="before_status"`, `http_status=null`, `body_state="absent"`,
  empty body bytes, and no retained response headers. Exactly one of
  `transport_failure="transport"` or `timed_out=true` is active.
- A body read failure or timeout after a valid HTTP status is received has
  `failure_phase="after_status"`, an integer `http_status`,
  `body_state="incomplete"`, and exactly one active failure flag. It may
  retain a received prefix of 0–16,384 bytes. The prefix is never parsed.
- `body_state="complete"` requires an integer HTTP status,
  `failure_phase=null`, both failure flags clear, `len(body_bytes) <= 16,384`,
  and body bytes equal to the complete received body, including an empty body.
- `body_state="over_limit"` requires an integer HTTP status,
  `failure_phase=null`, both failure flags clear, and
  `len(body_bytes) == 16,384`. The bytes are only the retained prefix and are
  never parsed.
- `body_state="absent"` requires empty body bytes. With an integer status and
  no failure it represents a response with no body; an HTTP-200 check-email
  attempt is then XON `unverifiable`. With null status it is valid only for
  the before-status failure state.
- A body longer than 16,384 bytes is retained only as its first 16,384 bytes
  with `body_state="over_limit"`; it is never truncated into `complete`.
- Any state with null status but no before-status failure, any after-status
  failure without an integer status, any active failure with `complete` or
  `over_limit`, or any other contradictory combination is a malformed local
  envelope and is a construction rejection. It does not become a source
  `unverifiable` result.

Malformed test fixtures and contradictory locally constructed trusted fields
are invalid experiment input and must fail visibly before transport/XON/R2
classification. In contrast, a valid transport attempt whose untrusted HTTP
metadata is missing, duplicate, non-ASCII, malformed, or incompatible is
classified conservatively as `failed`, `incomplete`, or `unverifiable` by the
matrix; harness construction errors are never collapsed into source
unverifiability.

### 12.4 Simultaneous-fault precedence

When a valid transport attempt contains more than one defect, classification
uses this order and does not add comparison, bark, disappearance, retry, or
live-transport policy:

1. Contradictory or structurally impossible local `TransportAttempt`
   construction is rejected visibly with `TransportConstructionError`.
2. A failure before an HTTP status exists is `failed`.
3. Once a status exists, HTTP status 400 or greater is `failed`, even when
   headers are malformed, the body is over-limit, or a post-status read failure
   is also present.
4. For a known status below 400, a post-status read failure or over-limit body
   is `incomplete`.
5. For a known status below 400 with a complete bounded body, malformed or
   unacceptable header metadata is `unverifiable`.
6. Redirects, informational statuses, and other unsupported statuses below
   400 are `unverifiable`.
7. Only an exact eligible HTTP 200 attempt with acceptable metadata and a
   complete bounded body proceeds to XON body normalization.

This is transport failure-classification precedence only. It does not alter
R1 comparison, exposure, guarding, disappearance, or retry ownership.

## 13. Boundary ownership

1. **Transport classification** validates the local envelope, derives content
   type from bounded raw headers, and classifies timeout, transport failure,
   body completeness, size, status, and media type. It does not create
   observations.
2. **XON normalization** selects exactly one family, applies that family’s
   status/media/body predicate, strictly decodes complete bytes, validates the
   selected schema, and creates an existing R2 response envelope using only
   trusted local context for source identity and scope.
3. **Existing R2 validation** receives its own envelope bytes and retains its
   existing strict UTF-8/JSON, duplicate-key, bounds, exact-key, source-match,
   outcome, and deterministic duplicate behavior. No R2 code changes are
   proposed.
4. **R1 comparison** receives only the resulting `SourceCheck`. R1 owns
   comparability, finding changes, exposures, and disappearance. No failed,
   unverifiable, or incomplete current check can establish an empty baseline
   or disappearance.

## 14. Body and normalized-R2 size proof

The selected check-email limits are deliberately narrower than the existing
R2 limit:

- at most 16 breach names;
- at most 64 Unicode code points per name;
- at most 128 Unicode code points in the response email; and
- at most 16,384 raw XON body bytes.

For a conservative JSON-escape calculation, one Unicode code point occupies
at most 12 ASCII bytes when escaped, plus two quote bytes per JSON string. The
largest selected XON success body is therefore bounded by:

```text
breaches value: 2 outer/inner brackets
              + 16 * (12*64 + 2) name bytes
              + 15 commas
              = 12,337 bytes
email value:    12*128 + 2 = 1,538 bytes
fixed keys/status/punctuation: 43 bytes
total:          13,918 bytes < MAX_XON_BODY_BYTES (16,384)
```

The normalized R2 success envelope uses the existing `fixture-response/1`
contract, fixed source ID `xposedornot.free.check-email`, `completed`, and at
most 16 results. Each finding maps to `finding_key="breach:" + name`,
`kind="breach"`, `locator="breach:" + name`, and empty material. With the
same worst-case escaped name bound, the exact worst-case compact JSON envelope
calculation is 25,910 bytes, which is below the existing R2
`MAX_INPUT_BYTES = 65,536` bytes. Failure and empty envelopes are smaller.

No R2 constant is changed. The XON body bound and selected field bounds are
the reason the normalized envelope remains within the existing R2 byte bound.

### 14.1 Frozen normalized-R2 serialization

Before calling existing R2, the XON normalizer constructs the envelope with
this exact serialization:

- UTF-8 encoding of the final JSON text;
- compact separators `(",", ":")` and no insignificant whitespace;
- deterministic object construction in this key order:
  `contract_version`, `source_id`, `outcome`, `results`; each result is
  constructed in this order: `finding_key`, `kind`, `locator`, `material`;
- ASCII escaping equivalent to Python `json.dumps(..., ensure_ascii=True)`;
- no floating-point values and rejection of non-standard numeric values,
  equivalent to `allow_nan=False`;
- no serializer-generated indentation, trailing bytes, or alternate key
  ordering; and
- measurement of the final UTF-8 encoded byte string before R2 is called.

If the final encoded envelope exceeds the existing R2
`MAX_INPUT_BYTES = 65,536` bytes, the normalizer raises
`R2EnvelopeTooLargeError`, a visible local `TransportConstructionError`,
before calling R2. It does not return a `SourceCheck` or convert the condition
to a source `unverifiable` result. No R2 constant or implementation is
changed. Under the frozen selected bounds, the maximum is 25,910 bytes, so
this rejection is unreachable through the selected bounded XON path and is a
defensive construction guard only.

## 15. Success structures, finding identity, and material policy

The selected check-email response has only the exact top-level keys described
in Section 6. The response email is an untrusted echo. The inner breach-name
strings are the only selected finding values; detailed mode is excluded.

The proposed source-local finding key is `breach:<exact NFC name>`. The XON
normalizer supplies this key to existing R2; it does not sort or case-fold
names. Equal keys with equal observations use R2 deduplication. A future
detailed contract would require a different source/schema identity.

Because an exact check-email breach name deterministically produces the same
finding key, kind, locator, and empty material, the selected XON check-email
mapping cannot construct a conflicting duplicate observation. Conflicting
duplicates remain protected by existing generic R2 tests, but they are not a
constructible XON check-email fixture and are not part of the selected XON
experiment. Exact duplicate breach names continue to exercise R2’s
deterministic deduplication.

For this simple contract, material fields are empty because the selected
finding fact is presence of the source-defined breach name. The source name is
the finding identity, not trusted subject identity. HTTP status, headers,
response email, response `status`, transport timing, retry metadata, and
parser diagnostics are context or diagnostics, not material fields.

## 16. Empty, partial, ordering, and completeness semantics

The selected check-email family has no completed-empty result. Zero valid
findings under HTTP 200 is unverifiable, including empty or invalid arrays and
names. HTTP errors, malformed bodies, partial bodies, and missing guarantees
never become empty.

The deferred analytics family has exactly one documented completed-empty
predicate: `XON_ANALYTICS_HTTP_200_NO_MATCH_V1` under its own source identity.

No endpoint documentation specifies pagination, cursoring, total counts,
truncation markers, response-size maxima, freshness timestamps, snapshot IDs,
ordering, or source completeness. A complete valid response is comparable
under its frozen contract but does not prove that the upstream database is
exhaustive or current. A partial, truncated, over-limit, or unfulfilled result
is incomplete/unverifiable with no partial observations.

## 17. Threat and ambiguity inventory

| Threat or ambiguity | Conservative treatment |
|---|---|
| Response echo differs from local request identifier | `unverifiable`; never replace trusted context. |
| HTTP 200 contains zero valid findings | `unverifiable`; no empty path for check-email. |
| HTTP 200 body is an error or another family’s body | `unverifiable`. |
| Wrong/missing/malformed content type | `unverifiable`. |
| Invalid UTF-8, duplicate JSON keys, malformed JSON, non-standard constants | `unverifiable`. |
| Unknown/missing fields or changed types | `unverifiable`; exact selected keys are required. |
| Duplicate or incompatible untrusted header metadata | Valid attempt → transport `unverifiable`; contradictory envelope/trusted fields are construction rejection. |
| Timeout, transport failure, 429, authorization, 5xx | `failed`. |
| Incomplete or over-limit body | `incomplete`/`unverifiable`; discard partial data. |
| Duplicate breach names | Use existing R2 deterministic deduplication; conflicting duplicates are generic R2-only protection, not a selected XON fixture. |
| Undocumented ordering or completeness | Do not sort, infer set semantics, or claim upstream completeness. |
| OpenAPI/example schema conflict | Preserve the conflict; use only the frozen synthetic family contract. |

## 18. Mapping table to existing R2 outcomes

| Documented or synthetic class | R2 outcome | Observations |
|---|---|---:|
| Exact selected check-email HTTP-200 success with at least one valid finding | `completed` | Accepted after R2 validation. |
| Check-email HTTP-200 body with zero valid findings | `unverifiable` | 0 |
| Check-email HTTP-200 malformed, wrong type, unknown/missing field, echo mismatch, or ambiguous body | `unverifiable` | 0 |
| Check-email HTTP 404, 401/422, 429, 5xx, timeout, or transport failure | `failed` | 0 |
| Incomplete or over-limit response | `incomplete` at transport boundary, then R2/R1 `unverifiable` | 0 |
| Exact analytics `XON_ANALYTICS_HTTP_200_NO_MATCH_V1` under analytics identity | `completed-empty` | 0 |
| Analytics body outside its exact sentinel | `unverifiable` | 0 |
| Equal duplicate finding key and equal observation | `completed`; existing R2 diagnostic `duplicate_finding_key_deduplicated` | One canonical observation |
| Conflicting duplicate finding key in generic R2 input | Generic R2 protection only; not constructible in selected XON check-email | 0 |

No undocumented or merely parseable HTTP-200 body maps to completed-empty.

## 19. Trusted values outside response bytes

The following values must be constructed locally and remain outside response
bytes and untrusted HTTP metadata:

- subject reference;
- source identity;
- canonical scope;
- adapter ID and version;
- schema version;
- normalization version; and
- material-field policy.

The existing R2 `scan_id`, `source_check_id`, and diagnostics are likewise
local context. The response email echo, breach names, HTTP status, headers,
status string, and body bytes cannot overwrite any trusted value.

## 20. Frozen synthetic matrices

### `XON_CHECK_EMAIL_MATRIX_V1` — selected first experiment

Every fixture uses the check-email source identity, scope, schema version, and
transport envelope. Each row freezes the transport classification, XON result,
and resulting R2 outcome or visible construction rejection:

| Fixture | Transport classification | XON classification | R2 outcome or construction result |
|---|---|---|---|
| Exact success with one or more valid breach names | Complete, HTTP 200, derived `application/json` | Exact success predicate accepted | `completed`; R2/R1 comparison applies. |
| `breaches=[]` | Complete, HTTP 200, derived `application/json` | `unverifiable`, zero valid findings | `unverifiable`; no observations. |
| `breaches=[[]]` | Complete, HTTP 200, derived `application/json` | `unverifiable`, zero valid findings | `unverifiable`; no observations. |
| Empty or invalid breach name | Complete, HTTP 200, derived `application/json` | `unverifiable`, invalid finding | `unverifiable`; no observations. |
| Response email mismatch | Complete, HTTP 200, derived `application/json` | `unverifiable`, untrusted echo mismatch | `unverifiable`; no observations. |
| Malformed JSON | Complete, HTTP 200, derived `application/json` | `unverifiable`, parse failure | `unverifiable`; no observations. |
| Invalid UTF-8 | Complete, HTTP 200, derived `application/json` | `unverifiable`, decoding failure | `unverifiable`; no observations. |
| Wrong content type, including a parameter or non-ASCII value | Complete, HTTP 200, metadata incompatible before derivation | Not entered | `unverifiable`; no observations. |
| Missing content type | Complete, HTTP 200, no derived media type | Not entered | `unverifiable`; no observations. |
| Duplicate retained header name | Valid attempt, duplicate metadata rejected before derivation | Not entered | `unverifiable`; no observations. |
| Undocumented top-level field | Complete, HTTP 200, derived `application/json` | `unverifiable`, exact-key failure | `unverifiable`; no observations. |
| Missing required top-level field | Complete, HTTP 200, derived `application/json` | `unverifiable`, exact-key failure | `unverifiable`; no observations. |
| Exact duplicate breach name | Complete, HTTP 200, derived `application/json` | Success candidates passed to R2 | `completed`; existing R2 deterministic deduplication. |
| Partial body after status receipt | HTTP status retained; `after_status`, `incomplete`, bounded prefix | Not entered; prefix never parsed | R2 `unverifiable` via incomplete boundary; no partial observations. |
| Body read timeout after status receipt | HTTP status retained; `after_status`, `incomplete`, bounded prefix | Not entered; prefix never parsed | R2 `unverifiable` via incomplete boundary; no disappearance. |
| Body over limit | HTTP status retained; `over_limit`, 16,384-byte prefix | Not entered; prefix never parsed | R2 `unverifiable`; no observations. |
| Failure or timeout before status | `before_status`, null status, absent body | Not entered | R2 `failed`; no observations. |
| Authentication/authorization response | Terminal HTTP failure, such as 401/422 | Error classification | R2 `failed`; no observations. |
| Rate limiting response | HTTP 429 | Error classification | R2 `failed`; no observations. |
| Server failure response | HTTP 502/503 or terminal 5xx | Error classification | R2 `failed`; no observations. |
| Other 2xx status | Complete or absent body with non-selected status | Unsupported status | R2 `unverifiable`; no observations. |
| Schema drift or response-family mismatch | Complete, HTTP 200, derived `application/json` | `unverifiable`, incompatible schema | R2 `unverifiable`; no observations. |
| HTTP-200 error-shaped body | Complete, HTTP 200, derived `application/json` | `unverifiable`, not selected success | R2 `unverifiable`; no observations. |
| Contradictory local envelope fields or trusted context | Not a valid transport attempt | Not entered | Construction rejection; synthetic run fails visibly. |

There is deliberately no genuine empty-success row in this matrix.

### `XON_ANALYTICS_SENTINEL_REJECTION_MATRIX_V1` — deferred separate research

This deferred matrix uses only analytics identity, scope, schema version, and
analytics body shapes. It is sentinel-and-rejection research, not an
implementation-ready positive-success matrix:

| Fixture | Expected transport/XON/R2 result |
|---|---|
| Exact `XON_ANALYTICS_HTTP_200_NO_MATCH_V1` predicate | Complete HTTP 200 with derived `application/json`; exact sentinel accepted; R2 `completed-empty`. |
| Any missing/extra/wrongly typed sentinel field | Complete HTTP 200 with derived `application/json`; XON `unverifiable`; R2 `unverifiable`. |
| Malformed JSON or invalid UTF-8 | Complete HTTP 200 with derived `application/json`; XON `unverifiable`; R2 `unverifiable`. |
| Wrong/missing/duplicate/incompatible media metadata | Valid attempt classified `unverifiable` before XON; R2 `unverifiable`. |
| Partial/over-limit body or timeout/read failure | `incomplete` with status preserved when received; R2 `unverifiable`. |
| Authentication, rate-limit, or server failure | Terminal transport/HTTP failure; R2 `failed`. |
| HTTP-200 body outside the exact sentinel | Complete HTTP 200; XON `unverifiable`; R2 `unverifiable`. |

The matrices are not shared and no fixture is reclassified by changing only a
source ID. Analytics positive-success normalization requires separate future
framing before any implementation. No analytics adapter or analytics files are
part of the selected Phase 2 file set.

## 21. Facts sufficient for later synthetic implementation

The first synthetic experiment is justified because the repository already
provides the R1/R2 boundary, the official sources provide an endpoint and
basic response facts, and this document freezes bounded success, error,
transport, body, identity, duplicate, and empty behavior.

The exact later files for the selected family are:

1. `personal_watchdog/xposedornot_check_email_adapter.py`
2. `tests/fixtures_xposedornot_check_email.py`
3. `tests/test_xposedornot_check_email_adapter.py`

No analytics adapter file is proposed in that phase. No change to
`personal_watchdog/r1.py`, `personal_watchdog/r2_adapter.py`, or
`personal_watchdog/offline_simulator.py` is proposed.

## 22. Blocking uncertainties and conclusion criteria

The following remain unknown in official documentation and require
deliberately conservative handling: live body charset/parameters, compression,
upstream completeness/freshness, ordering, duplicate semantics, maximum
service response size, and closed error schemas. They do not block the bounded
synthetic experiment because the experiment rejects ambiguous cases.

### Mapping is supportable

Conclude this only if the selected synthetic matrix passes and no failure,
ambiguity, partial body, malformed envelope, or zero-finding HTTP-200 body is
mapped to completed-empty or disappearance.

### Mapping is supportable only with conservative assumptions

This is the current R3 Phase 1 conclusion. It applies to a synthetic
check-email experiment that uses the exact predicate and bounds here, keeps
analytics separate, and treats all unspecified or conflicting cases as
failed, unverifiable, or incomplete.

### Documentation is insufficient for an adapter experiment

Conclude this if implementation would need to guess the check-email empty
path, accept an open schema, merge endpoint families, invent duplicate or
completeness semantics, trust response identity, or parse an incomplete body.
Under that condition, stop and request clarification; do not implement a live
adapter.

## Final research boundary

R3 Phase 1 remains documentation-only. No adapter, HTTP client, dependency,
credential, identifier, functional lookup request, persistence, scheduler,
notification, evidence archive, R4 work, or archive-repository change was
made. Stop for final adversarial review without staging, committing, or
pushing.
