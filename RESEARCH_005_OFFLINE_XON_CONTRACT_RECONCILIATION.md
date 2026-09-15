# Research Experiment R5 — offline XON contract reconciliation

**Status: Phase 2 implemented and verified offline on 2026-09-15.** The
experiment adds one bounded research fixture and one test module. It does not
change the R3 adapter, change R1/R2/R2.5, make a live request, add a
dependency, or authorize a collector, persistence, comparison, notification,
or monitoring.

## 1. Research question

Can the one observed R4 HTTP-200 response body
`{"Error":"Not found","email":null}` be represented as a bounded,
provenance-limited offline fixture and passed through the existing R3/R2
boundary without weakening the selected check-email contract or producing a
completed-empty or clean result?

This asks about reproducible local interpretation of one observed response
shape. It does not ask whether the response is the service’s general no-match
contract.

## 2. Repository reconciliation

The authoritative starting point is commit `6e6fc3d` on
`experiment/r4-bounded-live-xon-probe`, the commit containing the completed
R4 bounded probe and its records. The worktree was clean before this framing.
R4 was merged through pull request #2, but this R5 framing is local only and
is not being committed or pushed in this step.

The relevant existing facts are:

- R1 owns comparison, comparability, exposure, disappearance, and clean-state
  meaning.
- R2 owns strict bytes-first interpretation and construction of one R1
  `SourceCheck`.
- R3 freezes the selected check-email success predicate and has no
  completed-empty path for this family.
- R4 observed one complete HTTP-200 `application/json` response whose body
  decoded to `{"Error":"Not found","email":null}`.
- R4 classified that response as `unverifiable` with
  `response_unverifiable`.

No contradiction is resolved by this framing. The observed body is evidence
for a local fixture candidate, not a new source contract.

## 3. Claim and non-claims

### Claim under test

Given the exact bounded R4 observation as an offline input, the existing
R3/R2 path can produce the same deterministic `unverifiable` result without
accepting findings, inferring no exposure, or changing the check-email
contract.

### Non-claims

R5 would not establish that:

- every XON no-match response has HTTP status 200;
- every no-match response has this JSON shape;
- the service is complete, current, stable, available, or safe;
- the response proves ownership of the checked identifier;
- the body is a closed or officially versioned schema;
- the selected check-email family should gain completed-empty semantics; or
- a live adapter, scheduler, persistence layer, notification, or monitor is
  justified.

R5 would not use a real identifier or credentials and would not make a network
request.

## 4. Proposed offline input

If Phase 2 is approved, it may add one explicitly named research fixture
derived from the R4 diagnostic observation. The fixture must be local,
bounded, and sufficient to reproduce the transport and body classification.
It must carry provenance as test metadata rather than presenting the body as a
general service rule.

The proposed observation metadata is:

| Field | Frozen value or rule |
|---|---|
| Provenance | R4 Stage 3 diagnostic follow-up, observed 2026-09-13 |
| Subject | Reserved-domain synthetic identifier only; not included in the fixture body or output |
| HTTP status | `200` |
| Content type | `application/json` |
| Body state | `complete` |
| Body size | 34 bytes |
| Body | Exact observed bytes decoding to `{"Error":"Not found","email":null}` |
| Expected R3/R2 result | `unverifiable`, reason `response_unverifiable`, no findings |

The fixture must not contain a complete email address, credentials, request
headers outside the bounded test metadata, a full request URL, or unrelated
response data. The existing R4 document and append-only records remain the
provenance source for the observation.

## 5. Required boundary behavior

The existing R3/R2 implementation remains the only interpreter. A Phase 2
offline test may construct the already supported in-memory transport attempt,
call the existing adapter, and assert the public result. It must not duplicate
the parser, inspect the body to manufacture an expected result, or add a new
XON classification.

The expected result is:

```text
transport: ready
source status: unverifiable
reason: response_unverifiable
accepted findings: none
comparison: not run
```

The fixture must not be routed through R1 comparison because an unverifiable
source check is not comparable. It must not be treated as a completed-empty
check and must not produce disappearance.

## 6. Adversarial cases for a later Phase 2

A later offline implementation should test only the smallest cases needed to
protect the boundary:

1. the exact R4 body remains `unverifiable`;
2. changing the body to the frozen success shape is the only path to accepted
   findings under the existing adapter;
3. an empty or error-shaped body cannot become completed-empty;
4. provenance metadata cannot change the adapter result;
5. the fixture and output contain no complete identifier or full URL; and
6. the existing R1, R2, R2.5, R3, and R3.5 tests remain unchanged and pass.

These are offline tests. They do not justify trying another response,
re-querying XON, or sampling additional identifiers.

## 7. Success, failure, and stop criteria

### Success

R5 succeeds only if the existing adapter reproduces the R4 public result from
the bounded offline input and all existing suites remain green without a
semantic change.

### Failure

R5 fails or stops if the fixture requires schema loosening, a completed-empty
path, response-derived trusted context, a new parser, a new dependency, raw
payload persistence, or any live request.

Any malformed, partial, ambiguous, incompatible, failed, or unverifiable
offline input remains non-comparable. It is never converted to no exposure,
completed-empty, disappearance, or silence that could be mistaken for a clean
check.

## 8. Phase 1 approval boundary

At framing time, this was Phase 1 only. The framing itself did not authorize a
fixture, test, implementation, live request, commit, push, pull-request
update, or merge. Peter subsequently approved the exact offline Phase 2 scope
on 2026-09-15; that execution is recorded in Section 10. Any future live work
still requires a separate experiment and separate explicit approval.

## 9. Open questions

- Is retaining this one observed error-shaped body as a local fixture useful,
  or is the existing adapter test coverage sufficient?
- Should provenance live only in research records, or also in fixture metadata
  that cannot reach trusted adapter context?
- Does R5 provide enough value without accepting any new source result?

At framing time, the default conservative choice was to keep R5
documentation-only until these questions were answered. Phase 2 now answers
the narrow reproducibility question, but the open questions remain relevant
to any future extension.

## 10. Phase 2 offline execution — 2026-09-15

Peter approved the exact offline scope: one provenance-limited fixture derived
from the R4 diagnostic observation and tests that call the existing public
R3/R2 adapter boundary. The implementation added:

- `scenarios/r5_xon/01_observed_http_200_not_found.json`, containing the
  bounded 34-byte body as hex, one `application/json` header, HTTP 200,
  complete body state, and redacted local trusted references; and
- `tests/test_r5_offline_xon_contract_reconciliation.py`, which loads the
  fixture, constructs the existing in-memory `TransportAttempt`, and calls
  `classify_transport` and `normalize_check_email` without calling R1.

The exact fixture reproduced:

```text
transport: ready
source status: unverifiable
reason: response_unverifiable
accepted findings: none
```

The fixture contains no complete identifier, request URL, credential, or
response data beyond the already observed bounded body. Provenance metadata is
validated separately and cannot establish trusted adapter context.

Focused R5 tests passed: 2. The full repository suite passed: 263 tests.
Ruff format, Ruff lint, mypy, and `git diff --check` passed. No live request,
new dependency, semantic adapter change, comparison, persistence,
notification, collector, commit, or push was made during Phase 2.

R5 confirms only reproducible local interpretation of this one observed body.
It does not turn the body into a general XON no-match contract or authorize
completed-empty, clean, disappearance, or monitoring behavior.
