# Research Experiment R4 Phase 1 — bounded live XON probe framing

**Status: Phase 1 framing complete; one separately approved Phase 2 probe was
implemented and run once.** This document defines the approval-gated probe of
the official XposedOrNot free check-email endpoint. It does not define a
collector, scheduler, persistence, notification, or credential flow.

## 1. Research question

Can one explicitly approved, one-shot live request for an obviously synthetic
subject be captured into the existing bounded `TransportAttempt` contract and
passed through the committed R3 XON adapter without turning network, HTTP,
metadata, schema, parsing, timeout, partial-body, or ambiguity failures into a
completed-empty result, disappearance, or clean claim?

The smallest useful R4 question is live transport and contract observation. It
does not ask whether XposedOrNot is complete, current, accurate, useful, or
safe for personal monitoring.

## 2. Repository reconciliation

The authoritative starting point is commit `573d44c` on the local branch
`experiment/r4-bounded-live-xon-probe`. The repository was clean at the start
of this framing step.

The current repository establishes these boundaries:

- R1 owns comparison, comparability, exposure, guarding, and disappearance.
- R2 owns strict response-envelope normalization into one `SourceCheck`.
- R3 owns the bounded synthetic XON check-email transport and body contract.
- R3.5 exposes that chain through deterministic in-memory scenarios only.
- `personal_watchdog/xposedornot_check_email_adapter.py` accepts an already
  captured `TransportAttempt`; it does not resolve a name, open a socket, or
  perform I/O.

R4 Phase 1 adds only this framing document and append-only research records.
It does not alter R1, R2, R3, R3.5, `DECISIONS.md`, or `REFERENCES.md`.

## 3. Claim and non-claims

### Claim

A single bounded live observation can be useful as a protocol-boundary
experiment if the live capture layer supplies only bounded, explicitly
classified transport data to the existing R3 adapter and preserves every
failure as failure, incompleteness, or unverifiability.

### Non-claims

R4 cannot establish that:

- the service response is complete, fresh, exhaustive, stable, or ordered;
- a response proves ownership of the checked subject;
- no finding means safety or absence of exposure;
- a returned breach name is independently verified truth;
- one successful response represents future service behavior; or
- a live result justifies persistence, alerts, scheduled monitoring, or a
  product decision.

The probe is not a breach scanner, dark-web search, OSINT suite, remediation
service, or autonomous agent.

## 4. Proposed probe scope

The later Phase 2 approval packet must freeze exactly one source family:

```text
HTTPS GET https://api.xposedornot.com/v1/check-email/{email}
query: include_details=false
source: xposedornot.free.check-email
schema: xon-check-email/1
```

The request must use one obviously synthetic identifier under a reserved
domain, such as `r4-probe-01@example.invalid`. The exact value must be shown
for approval immediately before any live execution. No real identifier,
password, credential, cookie, account, or user-supplied personal data is
permitted.

The probe must make at most one request per invocation. It must not retry,
follow redirects, call analytics or another endpoint, submit a credential,
schedule a later attempt, or use a proxy or alternate endpoint to broaden
coverage. A blocked DNS lookup, TLS failure, timeout, redirect, or service
error is an observed outcome, not permission to try a different path.

The request header policy must be explicit before execution: no
`Authorization`, `Cookie`, `Referer`, or identifying headers; only the minimum
fixed headers needed to request JSON and identify the experiment. TLS
certificate verification must remain enabled. The exact request bytes and
destination must be recorded in the approval packet without recording the
complete synthetic identifier in ordinary logs.

## 5. Bounded capture contract

The future capture layer must translate one completed or failed network
attempt into the existing R3 `TransportAttempt`. It must not create a second
transport or XON semantic model.

The following bounds carry forward from R3:

- at most 16 retained headers;
- raw header names at most 64 bytes and values at most 512 bytes;
- retained-header accounting at most 8,192 bytes;
- at most 16,384 retained body bytes;
- a body read that exceeds the bound is `over_limit`, never a truncated
  `complete` body; and
- a body prefix obtained after a read failure or timeout is `incomplete` and
  is never parsed.

Before Phase 2 starts, the approval packet must also state finite connection,
TLS, header, body, and total wall-clock timeouts. The probe must have no retry
budget. These values are deliberately not hidden in a later library default.

The capture must preserve the distinction between:

1. failure before an HTTP status, with no response body or headers;
2. a terminal HTTP failure after a status exists;
3. a post-status read failure or timeout with a bounded prefix;
4. an over-limit response; and
5. a complete bounded response whose metadata or body is unacceptable.

The existing adapter remains responsible for status precedence, header
validation, content-type derivation, strict UTF-8/JSON parsing, exact XON
schema validation, echo matching, finding identity, and R2 invocation.

## 6. Expected mapping

| Live observation | Existing R3/R2 outcome | R4 interpretation |
|---|---|---|
| HTTP 200, exact `application/json`, complete body, exact success predicate, at least one valid finding | `completed` | Bounded source observation only; no completeness claim. |
| HTTP 200 with zero valid findings or an error-shaped body | `unverifiable` | Never completed-empty; never disappearance. |
| HTTP 404, 401/422, 429, terminal 5xx, or transport failure | `failed` | Failure remains visible; no clean result. |
| Post-status timeout/read failure or body over the bound | `incomplete` then R2/R1 non-comparable | No partial observations; no disappearance. |
| Wrong/missing/duplicate/malformed metadata, invalid UTF-8/JSON, schema drift, or echo mismatch | `unverifiable` | No source identity or subject identity is taken from the response. |
| Local capture envelope contradiction | construction rejection | Invalid probe input; not a source result. |

The check-email family has no R4 completed-empty path. R4 must not import the
deferred analytics sentinel from R3 or infer an empty result from any other
body.

## 7. Ownership and output boundary

The intended later chain is:

```text
one approved live attempt
  -> bounded capture
  -> existing TransportAttempt
  -> existing R3 transport/XON/R2 adapter
  -> bounded local observation report
```

The capture layer owns only I/O facts: status, bounded headers, body state,
bounded bytes, timeout/failure phase, and local timing diagnostics. It must
not compare findings, construct `comparison_id` or `guard_id`, choose a
baseline, suppress repeated failures, or emit a notification.

R1 comparison is outside this first live probe unless a separate experiment
freezes an approved prior state. A one-shot R4 result therefore cannot emit a
new, changed, disappeared, or guarding event merely because the live source
returned data. It may expose the existing `SourceCheck` status and bounded
finding keys as local experiment output.

## 8. Minimal local record and retention

The future probe may retain only a bounded local result containing:

- probe and adapter version;
- a local subject reference, not the complete identifier;
- endpoint family and canonical scope;
- local start/end timestamps, explicitly described as observation metadata;
- request outcome and failure phase;
- HTTP status, retained-header count, derived content type, body state, and
  retained-byte count;
- the existing adapter/R2 status and bounded reason codes; and
- bounded finding keys only when the existing adapter accepts them.

It must not retain the raw response body, complete request URL with the
identifier, cookies, credentials, unrelated headers, or unrelated response
data. A body digest, if later proposed, is evidence of retained bytes only;
it does not prove collection time, service provenance, completeness, or an
untampered history.

The record is local, purpose-specific, and disposable. R4 Phase 1 does not
authorize a database, archive, hash chain, export, background service, or
notification channel.

## 9. Success, failure, and stop criteria

The live probe mapping is supportable only if a later approved execution
demonstrates all of the following:

- one and only one request was attempted within the approved budget;
- the capture produced a valid `TransportAttempt` or a visible construction
  failure;
- the committed R3 adapter supplied the transport and XON/R2 outcomes;
- no failed, incomplete, malformed, ambiguous, or zero-finding response was
  represented as completed-empty, disappearance, or clean; and
- no raw payload, credential, real identifier, or unrelated personal data was
  retained.

Stop and classify the probe as inconclusive if the endpoint, proxy, TLS layer,
HTTP library, response framing, or service behavior requires an assumption not
covered by R3. Do not repair an unexpected response by loosening the schema,
retrying, accepting a partial body, or changing R1/R2 semantics.

## 10. Open questions intentionally left open

R4 Phase 1 does not decide:

- whether the endpoint accepts the reserved-domain synthetic identifier;
- whether the live service uses the documented path and query combination;
- whether redirects, compression, charset parameters, or error bodies occur;
- whether rate limits apply to the approved probe environment;
- whether live response data is complete, fresh, paginated, or stable;
- whether any finding is useful enough to retain or show to a person; or
- whether repeated probes, persistence, comparison, or notifications should
  ever be designed.

These questions require separate evidence and approval. They are not reasons
to broaden the first probe.

## 11. Phase 2 approval boundary

No live request is authorized by this document. Before any Phase 2 work, Peter
must approve the exact synthetic identifier, endpoint, request headers,
timeouts, one-request budget, retention fields, and stop conditions. Phase 2
must remain local, standard-library-only unless separately approved, and
must not add a collector, scheduler, persistence, notification, credential,
real identifier, or external archive.

If Phase 2 requires changing the committed R3 adapter, R1/R2 semantics,
adding a retry or baseline policy, accepting an undocumented empty path, or
retaining raw payloads, stop for a new framing decision instead.

Do not stage, commit, push, merge, or make a live request as part of this
Phase 1 framing step.

## 12. Phase 2 execution note — 2026-09-11

Peter separately approved one bounded Phase 2 execution using the proposed
reserved-domain subject `r4-probe-01@example.invalid`, the documented
check-email endpoint, no credentials, one request, no retry, no redirect, and
the R3 byte/header bounds. The implementation is a one-shot probe, not a
collector, and retains the response body only in memory while the existing R3
adapter runs.

The single observed result was:

```text
request_count=1
http_status=200
header_count=5
body_bytes=34
body_state=complete
normalized_content_type=application/json
transport_disposition=ready
transport_reason=ready
source_status=unverifiable
reason_codes=["response_unverifiable"]
finding_keys=[]
```

The response body was not retained or printed. Because the body is not
available for post-hoc inspection, this result does not establish whether the
service returned a no-match body, an undocumented shape, or another
unverifiable response. It establishes only that this one request reached a
complete JSON transport response that the frozen R3 contract did not accept
as a comparable finding result.

The execution does not authorize retries, a live adapter beyond this probe,
real identifiers, persistence, comparison, notification, or broader source
coverage. Any follow-up requires a new bounded approval and must preserve the
same conservative failure semantics.

## 13. Stage 1 adversarial review — 2026-09-12

The offline review corrected timeout classification when a timeout is wrapped
inside `URLError`, rejected non-text response-header metadata before using it,
and changed the report to expose only the local subject reference
`r4-probe-01` rather than the complete synthetic identifier. The review added
coverage for pre-status timeout, post-status read timeout, duplicate
content-type metadata, redirect rejection, over-limit capture, and output
redaction.

The prior single live observation was not repeated or changed. No additional
network request, persistence, comparison, notification, or collector work was
performed during this review.

## 14. Stage 2 conclusion — 2026-09-12

R4 established a bounded live transport observation, not a usable live source
mapping. The request reached the documented host and returned a complete JSON
transport response, but the frozen R3 check-email contract returned
`unverifiable`. Since the body was not retained, the experiment cannot
distinguish a service no-match shape from another undocumented response.

The correct conclusion is **inconclusive at the live source-contract boundary**.
The probe must not retry, loosen the schema, invent a completed-empty path, or
continue into comparison or monitoring. A future diagnostic experiment would
need separate approval for a more specific bounded retention rule before any
additional request.

## 15. Stage 3 diagnostic follow-up — 2026-09-13

Peter approved one diagnostic follow-up using the same synthetic identifier
and request boundary. The second request overall made exactly one request for
this invocation. Diagnostic mode emitted the bounded response bytes as
lowercase hex and did not write a file.

The body decoded to:

```json
{"Error":"Not found","email":null}
```

The response was HTTP 200, complete, and `application/json`. It therefore
confirms the observed no-match body shape for this request, while also
confirming that the frozen R3 check-email contract must keep it
`unverifiable`: the selected check-email family has no completed-empty path,
and the response does not satisfy the exact success predicate.

This is one observed service response, not a general status or completeness
guarantee. No raw body was written to disk, no retry was made, and no R1
comparison or monitoring behavior was added.

## 16. Stage 4 final review and handoff — 2026-09-13

The final review found only the intended R4 framing, bounded probe, focused
tests, and append-only project records changed. The branch remains at the
requested starting commit, with no staged files, commit, push, or remote
tracking branch. The probe remains one-shot and synthetic-only; it has no
credentials, retry, redirect following, persistence, comparison,
notification, or collector behavior.

The two approved live invocations made one request each. The second diagnostic
observation identified one HTTP-200 no-match body shape, but the frozen R3
contract correctly remains `unverifiable`. R4 therefore does not justify a
live adapter, completed-empty mapping, clean claim, or monitoring behavior.

Stage 4 is complete and the branch is ready for a separately authorized
commit. No further live request is warranted by this experiment.
