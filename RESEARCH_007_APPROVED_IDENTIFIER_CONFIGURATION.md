# Research Experiment R7 — approved-identifier configuration

**Status: Phase 2 implemented and verified offline.** Phase 1 framed the
configuration boundary; Phase 2 implements only synthetic local profiles and
their offline fixture selection. It does not accept a real identifier, make a
live request, add credentials, or authorize a scheduler, notification, export,
or new source.

## 1. Research question

Can Personal Watchdog represent one consenting user’s explicitly approved
identifier with the minimum local information needed for a later scan, while
keeping the sensitive value out of ordinary reports, history, logs, test
fixtures, and comparison records?

The Phase 2 implementation target is configuration only. It must prove that
a profile can be created, validated, referenced by an opaque
`subject_ref`, redacted for display, and rejected when approval or identity
constraints are not satisfied. It does not prove identity ownership or source
coverage.

## 2. Repository reconciliation

The authoritative baseline is merge commit `2ab2510` on local `main`, which
contains the merged R4, R5, and R6 work. The local R6 workflow currently uses
one synthetic subject reference and a fixture source; its JSON state contains
structured scan data but no approved real-identifier profile.

This R7 framing is on the new local branch
`experiment/r7-approved-identifier-config`. The branch was created from the
merged baseline and is clean before this document is added. R1/R2/R3/R4/R5/R6
semantics remain authoritative and are not reopened by this experiment.

## 3. Claim and non-claims

### Claim under test

A narrowly scoped local profile can record explicit approval for one synthetic
identifier, assign a stable opaque subject reference, validate the profile,
and supply the identifier only to a separately selected local adapter when
that later adapter is approved.

### Non-claims

R7 would not establish that:

- the configured person owns or controls the identifier;
- an identifier is safe, private, unique, or absent from any source;
- a source is complete, current, stable, or comprehensive;
- storing an identifier locally is secure against a compromised host;
- encryption, a system keyring, or any external secret store is available;
- a username and email have interchangeable identity or normalization rules;
- a profile authorizes a live request, credential use, scheduling, notification,
  or export; or
- a failed or unverifiable scan can be reported as clean.

## 4. Proposed profile boundary

The profile is a local sensitive record, separate from scan history. The
versioned profile contains exactly the information needed to select and
authorize one subject:

| Field | Purpose and boundary |
|---|---|
| `profiles_version` | Exact configuration contract version |
| `subject_ref` | Stable opaque local reference used by scans and reports |
| `kind` | Explicit identity kind, initially `email` or `username` |
| `value` | Sensitive identifier value, local-only and never echoed by default |
| `approved` | Explicit local approval gate; must be true before selection |
| `purpose` | Short local purpose label, bounded and non-sensitive |
| `created_at` | Local profile metadata, not proof of identity or collection time |
| `enabled` | Local selection gate; disabled profiles cannot be scanned |

The exact storage shape remains provisional. `value` may be stored in a
clearly labelled local profile with restrictive permissions, as described by
the existing privacy policy. Encrypted-at-rest storage and key management are
separate decisions and must not be implied by a plain JSON implementation.

The profile must not contain credentials, source response bodies, full request
URLs, unrelated contact-book data, inferred aliases, or automatically
discovered identifiers.

## 5. Approval and input rules

Approval must be explicit and local. The profile operation must not silently
import, discover, normalize, or expand identifiers. The exact input interface
must avoid placing a complete identifier in shell history or ordinary process
list output; an interactive non-echo prompt or protected local input channel
is preferred for a later implementation.

For the first offline implementation:

- tests use only reserved synthetic values such as
  `r7-subject-01@example.invalid` and `r7-user-01`;
- a complete identifier never appears in source, fixtures, logs, reports, or
  committed expected output;
- `subject_ref` is generated or accepted only under a strict opaque reference
  rule and is the only identity value exposed to scan/history records;
- `approved=false` or `enabled=false` prevents adapter selection; and
- response data can never create, approve, enable, or replace a profile.

The profile does not prove that the consenting user controls the value. It
records the user’s local instruction and nothing more.

## 6. Proposed local operations

The following bounded local operations are implemented for synthetic values.

### Add one approved profile

Accept one explicit identity kind and value through a protected local input
path, validate bounded syntax without claiming ownership, assign an opaque
`subject_ref`, and write the profile with restrictive local permissions.
Duplicate values, duplicate references, empty values, unsupported kinds,
overlong values, and missing approval must fail visibly.

### Inspect profiles

List only `subject_ref`, `kind`, approval/enablement state, and bounded purpose
metadata. Never print the complete value by default. A deliberate local reveal,
if ever added, is a separate security decision and is outside R7 Phase 1.

### Select a profile for a scan

A future separately approved local adapter may receive only the selected
profile’s trusted value in memory. In this offline phase, the fixture receives
no profile value. Scan records, comparison records, reports, and history use
`subject_ref`; they do not copy the sensitive value.

### Disable or remove a profile

Disablement must prevent future selection without rewriting historical scan
records. Deletion, secure erasure, correction, and recovery from interrupted
profile writes require separate retention and recovery decisions.

## 7. Interaction with R6

R7 must not silently reinterpret existing R6 `.watchdog/config.json` or
`history.json` files. A later implementation must choose an explicit versioned
migration, a separate profile file, or a clean initialization path and must
fail visibly on an unsupported mixed state.

R6’s fixture source remains the only scan source in the first offline
implementation. R7 profile configuration supplies trusted local subject
context; it does not alter the fixture result, add a live adapter, or change
R1 comparability. A profile value must never be copied into a source response,
observation locator, comparison identifier, or report field.

The existing R6 `r6-subject-01` synthetic workflow may remain a compatibility
fixture. It must not be treated as an approved real-identifier profile.

## 8. Offline Phase 2 acceptance matrix

The Phase 2 implementation covers the following smallest acceptance set:

1. one synthetic email profile can be added with explicit approval;
2. one synthetic username profile can be added with explicit approval;
3. missing approval, disabled state, empty value, unsupported kind, overlong
   value, malformed profile, and duplicate profile are rejected;
4. profile listing and scan/history output expose only opaque references and
   bounded non-sensitive metadata;
5. a selected profile supplies trusted subject context without response data
   changing that context;
6. existing R6 fixture scans and R1/R2 outcomes remain unchanged;
7. disabling a profile blocks a new scan but does not rewrite prior history;
8. a restart or reload preserves valid profiles without retaining extra
   payload data; and
9. profile and history writes do not leave a partial target file during normal
   atomic replacement.

The tests must use reserved synthetic values only. They must not test live
ownership, send an identifier, inspect a real account, or introduce a secret
management dependency.

## 9. Failure and stop criteria

Stop if the implementation requires:

- a real identifier, live request, credential, or external account;
- an implicit consent or ownership assumption;
- printing complete identifiers in normal output, logs, or process arguments;
- copying profile values into history, reports, source responses, or findings;
- changing R1/R2/R6 semantics to accommodate configuration;
- contact-book import, alias discovery, broad identity expansion, or public
  export; or
- claiming encryption, deletion, secure erasure, or host compromise
  resistance without a reviewed design.

Malformed, failed, incomplete, ambiguous, or unverifiable source results remain
distinct from clean results regardless of profile state.

## 10. Success and failure criteria

### Success

R7 succeeds if one synthetic approved profile can be created, validated,
redacted for display, selected for the offline fixture workflow, disabled
without history rewriting, and reloaded without leaking the value into
ordinary outputs, while all prior R1/R2/R6 behavior remains unchanged.

### Failure

R7 fails or stops if the profile cannot be kept separate from history, if
approval is implicit or unverifiable, if a redacted output can be reversed
from ordinary metadata, or if the storage design requires unbounded or
unnecessary personal data.

## 11. Approval boundary

At framing time this was R7 Phase 1 only; Phase 2 required separate explicit
approval. Peter subsequently approved the offline implementation scope. That
approval did not authorize a real identifier, live request, credential,
dependency, commit, push, pull-request update, or merge.

## 12. Open decisions

- Should the sensitive value live in a separate profile file from R6 state?
- Should the first profile operation use a non-echo prompt, protected stdin,
  or a pre-created local file with restrictive permissions?
- What exact bounded validation rules differ between email and username values?
- Is a stable opaque `subject_ref` generated by the tool or selected by the
  user?
- What should disablement and deletion mean for future scans and historical
  reports?
- What permission and recovery guarantees can be made without encryption?

The conservative default is one synthetic profile, local-only storage,
redacted ordinary output, explicit approval and enablement, no migration by
surprise, and no live or external operation.

### Phase 2 decisions

- The value lives in a separate `profiles.json` sidecar from R6 config and
  history.
- Interactive input uses a non-echo prompt; piped stdin is retained only for
  controlled local automation and tests.
- Email and username syntax is bounded and kind-specific without claiming
  ownership or performing normalization-based discovery.
- The tool generates opaque `r7-subject-###` references.
- Disablement blocks future selection and leaves historical scans untouched.

## 13. R7 Phase 2 offline execution

The approved implementation uses a separate versioned `profiles.json` file in
the selected state directory. It supports `profile add`, `profile list`, and
`profile disable`, plus `scan --subject-ref` for an approved and enabled
profile. Interactive input is non-echoed; piped input is available for
controlled local tests. Profile values are validated but are not echoed in
normal output, scan records, comparison records, reports, or history.

The profile file is bounded to eight profiles, written through a temporary file
replacement, and set to mode `0600`. R6 config and history remain in their
existing shape; no migration or replacement of the R6 subject is performed.
The offline fixture receives no profile value and R1/R2 continue to own source
interpretation, comparability, and event semantics.

Focused verification passed: 13 tests covering R6 compatibility and R7
profile behavior. Full-suite verification passed with 276 tests. Ruff
formatting and linting, mypy, `git diff --check`, and the manual CLI smoke
test also passed.

### Phase 2 boundary

Only reserved synthetic values were used. No live request, network adapter,
credential, scheduler, notification, export, dependency, commit, push, or pull
request was added. The local approval record does not prove identity
ownership, source coverage, or safety. Encryption, secure deletion, recovery,
and future live-adapter handling remain separate decisions.
