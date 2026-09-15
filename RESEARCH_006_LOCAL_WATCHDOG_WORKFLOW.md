# Research Experiment R6 — minimal local watchdog workflow

**Status: Phase 2 implemented and verified offline on 2026-09-15.** The
experiment adds a minimal local module, bounded JSON state, one synthetic
fixture source, and tests for `init → scan → compare → report → history`. It
does not add a scheduler, notification delivery, live adapter, credential
flow, dependency, or network request.

## 1. Research question

Can Personal Watchdog define a small local workflow that a consenting user can
operate and understand, while preserving R1/R2 truthfulness across setup,
source checks, comparison, reports, and retained history?

The first implementation target, if approved, should be an offline fixture
workflow. It should demonstrate the user-visible lifecycle before any live
source or background execution is considered.

## 2. Repository reconciliation

The authoritative code baseline is commit `6e6fc3d` on
`experiment/r4-bounded-live-xon-probe`. The current worktree also contains the
uncommitted R5 Phase 2 offline fixture, test, and records. R4 is merged and
pushed; R5 remains local. This R6 document adds framing only and does not
alter those changes.

The current repository already provides:

- R1 deterministic source-check comparison, baseline, exposure, disappearance,
  and guarding semantics;
- R2 strict bytes-first response interpretation;
- R2.5 and R3.5 offline scenario runners; and
- R4/R5 bounded evidence about one XON response shape, without a usable live
  source integration.

The README’s planned workflow is now available through
`python -m personal_watchdog.cli`. The installed `watchdog` executable remains
deferred.

## 3. User model and scope

The user explicitly approves each identifier and source scope. The watchdog is
local-first: approved subject values, configuration, scan results, and
reports stay on the local machine unless a future, separately approved export
exists.

The initial workflow should support one synthetic subject and one offline
fixture source. It should establish the interaction and data contracts before
supporting multiple subjects, live sources, schedules, notifications, or
public exports.

This is not a comprehensive personal-data, breach, OSINT, or dark-web scanner.
“No findings” means only that the configured source returned no findings during
a successful comparable check. It never means that an identity is safe.

## 4. Proposed command contract

These are the implemented offline command meanings. They remain limited to
the synthetic fixture source described in this document.

### `watchdog init`

Create the smallest local configuration for an explicitly approved subject
and selected source scope. It should:

- reject an empty scope;
- assign a stable opaque `subject_ref` and source references;
- make the selected adapter, schema, normalization, and material policies
  visible;
- avoid printing or logging complete identifiers by default; and
- state where local configuration and history are retained.

The command must not silently discover identifiers, import a contact book,
enable a broad source set, or transmit configuration.

### `watchdog scan --adapter fixture`

Run one explicitly selected source check and retain a bounded scan attempt. The
first Phase 2 implementation should use only a local fixture adapter or the
existing offline scenario boundary. It should expose the terminal source
status and bounded diagnostics without retaining raw payloads by default.

Each scan attempt exists even when a source fails. A failed or unverifiable
source must remain visible as such.

### Comparison within `scan`

The workflow should pass source checks to existing R1 comparison only when the
baseline and current checks are completed and exactly comparable. It should
not implement a second comparator, search arbitrarily backward for a baseline,
or compare a failed or unverifiable result as an empty set.

The user-visible outcomes should preserve the existing meanings:

| Situation | User-visible result |
|---|---|
| First completed check | Baseline created; no exposure alert |
| Equal completed check | Unchanged; silent |
| Material difference | New or changed exposure event |
| Completed absence after comparable baseline | Disappeared event |
| Failed current check | Not comparable; guarding failed; no disappearance |
| Unverifiable current check | Not comparable; guarding unverifiable; no disappearance |

### `watchdog report --latest`

Render the latest retained scan and its derived comparisons in plain language
and a deterministic machine-readable form. The report should distinguish:

- completed source findings;
- baseline, unchanged, new, changed, and disappeared results;
- failed, incomplete, and unverifiable sources; and
- whether the scan had enough successful comparable data to support an absence
  claim for each source.

It must not describe a failed or unverifiable source as clean, not found, or
disappeared. It must not send a notification; a report is a local output.

### `watchdog history`

Show bounded retained scan attempts, source statuses, comparison events, and
guarding events in chronological order. History should make it possible to
answer what was checked, when the local run occurred, which source result was
usable, and why a comparison was or was not made.

History should not retain full response bodies, credentials, unnecessary
headers, full request URLs, or unbounded diagnostics. Retention limits,
deletion, correction, and export are separate design questions.

## 5. Minimal local data contract

The proposed persisted records are:

1. **Configuration:** opaque subject reference, approved source references,
   source identities, adapter/schema/normalization versions, material policy,
   and local retention settings.
2. **Scan attempt:** scan identity, local run metadata, one terminal result per
   declared source, bounded diagnostic metadata, and no raw payload by default.
3. **Comparison record:** the existing R1 result, including explicit
   `not_comparable` reasons where applicable.
4. **Report projection:** a deterministic view derived from retained records;
   it is not an additional semantic result.

Trusted subject and source context must come from local configuration. Response
data must not overwrite subject identity, source identity, scope, or policy.

The storage format, encryption-at-rest expectations, retention duration,
correction model, and crash-recovery behavior remain open. The Phase 1 framing
does not choose a database, file format, key-management scheme, or service.

## 6. Offline Phase 2 acceptance matrix

If separately approved, the smallest implementation should cover:

1. empty or malformed configuration is rejected;
2. one completed fixture check creates a silent baseline;
3. a repeated equal completed check is unchanged and silent;
4. a material fixture change produces the existing exposure event;
5. a completed absence after a comparable baseline produces disappearance;
6. a failed current check produces guarding failure, not disappearance;
7. an unverifiable current check produces guarding unverifiable, not
   disappearance;
8. a restart or reload preserves the bounded records needed for the latest
   report and history;
9. one source failure does not erase another source’s valid comparison; and
10. reports and history contain no raw payload, credential, full URL, or
    complete identifier by default.

The implementation must reuse R1 comparison and existing adapter boundaries.
It must not duplicate semantic logic in a CLI or storage layer.

## 7. Stop criteria and deferred scope

Stop the experiment if implementation requires any of the following before the
offline workflow is understood:

- a live request, real identifier, credential, or new source adapter;
- a scheduler, background service, notification channel, or public export;
- a second comparison or baseline policy;
- broad identity discovery or comprehensive source coverage;
- raw-payload archiving, indefinite retention, or an unbounded database; or
- changing R1/R2/R3 semantics to make the workflow appear cleaner.

Notifications, scheduling, live XON integration, multi-user support,
encryption design, exports, and recovery from corrupted history are deferred.

## 8. Success and failure criteria

### Success

R6 succeeds if a user can configure the narrow offline scope, run two or more
fixture scans, inspect a truthful latest report, and inspect bounded history,
while the existing R1/R2 semantics and all prior tests remain unchanged.

### Failure

R6 fails or stops if the workflow cannot distinguish a clean comparable result
from a failed or unverifiable source, if history loses the reason comparison
was suppressed, or if local retention requires unbounded or unnecessary
personal data.

## 9. Phase 1 approval boundary

At framing time, this was R6 Phase 1 only. The framing itself did not
authorize a CLI, persistence, fixture extension, scheduler, notification, live
request, credential, dependency, commit, push, pull-request update, or merge.
Peter subsequently approved the exact offline Phase 2 scope on 2026-09-15;
that execution is recorded in Section 11. Any future live work still requires
separate explicit approval.

## 10. Open decisions

- Should the first offline workflow be a dedicated CLI or a thin wrapper over
  the existing scenario runner?
- What is the smallest acceptable local storage format and retention limit?
- Should configuration store approved subject values directly, or use a local
  indirection that keeps values out of ordinary reports and history?
- Which report fields are useful enough to retain while remaining minimal?
- What recovery behavior is acceptable when a retained record is malformed or
  incomplete?

The conservative default is one synthetic subject, one offline fixture source,
manual invocation, bounded local records, deterministic reports, and no
notifications.

## 11. Phase 2 offline execution — 2026-09-15

Peter approved the offline command, storage, retention, and test scope. The
implementation added `personal_watchdog/cli.py`, which provides:

- `init`, creating `.watchdog/config.json` and `.watchdog/history.json`;
- `scan --adapter fixture --fixture NAME`, passing synthetic fixture envelopes
  through existing R2 and comparing the resulting scan through existing R1;
- `report --latest`, rendering the latest bounded result; and
- `history`, rendering retained scan summaries.

The state retains at most 32 scans and stores structured source checks,
observations, comparison results, exposure events, and guarding events. It
does not retain raw response envelopes, credentials, request URLs, or a
complete identifier by default. State writes use a temporary file replacement
to avoid leaving a partially written target file during normal writes.

The implemented fixture names are `baseline`, `unchanged`, `changed`,
`disappeared`, `failed`, and `unverifiable`. Failed and unverifiable current
checks remain `not_comparable` with their guarding events; they never produce
disappearance.

Five focused R6 tests pass. The workflow has been manually exercised through
baseline, changed, and failed scans. Full repository verification passed:
268 tests, Ruff format, Ruff lint, mypy, and `git diff --check`.

R6 remains offline-only. The installed `watchdog` executable, live adapters,
scheduling, notifications, encryption design, export, and broader source
coverage remain deferred.
