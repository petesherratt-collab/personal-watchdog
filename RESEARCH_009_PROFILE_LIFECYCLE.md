# Research Experiment R9 — approved-profile lifecycle

**Status: Phase 2 implemented and verified offline.** Phase 1 framed explicit
disable, re-enable, and deletion semantics for the R7 local profile store;
Phase 2 implements that bounded lifecycle protocol over synthetic local
profiles. It does not make a live request, accept a real identifier, add a
dependency, or authorize a backup, scheduler, notification, export, commit,
push, or pull request.

## 1. Research question

Can a consenting user explicitly disable, re-enable, or delete one local
approved profile while preserving consent boundaries, opaque historical scan
records, monotonic references, and truthful failure behavior?

R9 is about local lifecycle state. It does not test identity ownership, source
coverage, source accuracy, secure erasure, or whether a prior exposure was
remediated.

## 2. Repository reconciliation

The authoritative baseline is merge commit `c63c174` on local `main`, which
contains the merged R8 conservative retention and recovery subset. This
framing is on the new local branch `experiment/r9-profile-lifecycle`, created
from that clean baseline.

R7 provides `profile add`, redacted `profile list`, `profile disable`, and
offline fixture selection by opaque `subject_ref`. R8 made missing and
malformed profile state fail closed, while keeping the profile store bounded
to eight records and scan history bounded to 32 records. There is currently
no profile enable, delete, restore, or profile-state migration operation.

## 3. Existing state and lifecycle ambiguity

The current profile record has separate `approved` and `enabled` fields, but
the CLI only creates records with both true and can only change `enabled` to
false. This leaves several meanings that must not be conflated:

- disabling stops future selection but retains the sensitive value;
- approval is a local instruction, not proof of ownership;
- re-enabling a disabled profile could be a new explicit consent action or a
  mere administrative toggle;
- deletion could remove the profile record without rewriting historical scans;
- an old opaque `subject_ref` must never be reassigned to a different value;
  and
- removing the current profile record cannot prove secure erasure from every
  filesystem layer, backup, cache, or forensic copy.

R9 must resolve only the local state transitions needed for a small offline
experiment. It must not infer consent from a prior scan, a retained history
record, or the existence of a local file.

## 4. Claim and non-claims

### Claim under test

A narrowly defined lifecycle protocol can make disablement, any re-enable, and
any deletion explicit and auditable at the local state level, without changing
historical scan records or making unavailable profile state look empty.

### Non-claims

R9 would not establish that:

- re-enabling proves current consent, identity ownership, or control of the
  identifier;
- deleting a record securely erases the value from storage media, backups,
  memory, operating-system caches, or prior process artifacts;
- a historical scan remains valid for a newly created or reused identity;
- a stable opaque reference identifies the same person across installations;
- lifecycle state makes a source more complete, current, or accurate; or
- a failed, malformed, partial, uncertain, or unverifiable source check is a
  clean result or a disappearance.

## 5. Proposed lifecycle protocol

The approved and implemented protocol is:

| Transition | Required action | Profile value | History |
|---|---|---|---|
| enabled → disabled | explicit disable | retained locally | unchanged |
| disabled → enabled | explicit re-approval and enable action | retained locally | unchanged |
| disabled → deleted | explicit deletion confirmation | removed from current profile store, without secure-erasure claim | unchanged |
| enabled → deleted | require disable first, then explicit deletion | removed from current profile store, without secure-erasure claim | unchanged |
| missing/malformed → any state | no lifecycle action | unavailable/untrusted | unchanged and never reinterpreted |

The protocol should use separate commands or unambiguous action flags for
disable, enable, and delete. A generic toggle is unsafe because repeating it
can silently reverse a consent decision. Re-enable should require a fresh
explicit approval signal, even though the retained record still has
`approved=true`.

Deletion should be a two-step local action: disable first, then explicitly
confirm deletion by opaque reference. The tool should remove the targeted
profile record, preserve the monotonic reference counter, and never reuse the
deleted reference. If a deletion write is interrupted, the target must remain
either the old valid store or the new valid store.

Historical scan records should retain their opaque `subject_ref` and existing
comparison data. They must not be rewritten, relabelled as clean, or deleted
because the current profile was disabled or deleted. A future report may say
that current profile metadata is unavailable, but that is separate from the
historical scan result.

## 6. Consent and retention boundaries

R9 should distinguish these actions:

- **disable:** stop future scans while retaining the local value for possible
  explicit re-approval;
- **re-enable:** require an explicit new approval action and preserve the same
  opaque reference only while the profile record remains intact; and
- **delete:** remove the current profile record, preserve history, and make no
  secure-erasure claim.

No automatic deletion based on age, scan outcome, source disappearance, or
failure is in scope. No profile value may be copied to history, reports,
locators, comparison identifiers, logs, or command arguments. Deletion must
not trigger a source request or a history rewrite.

## 7. Offline Phase 2 acceptance matrix

The Phase 2 implementation and existing R7/R8 tests cover:

1. disable blocks scan selection and leaves the profile value and prior
   history unchanged;
2. re-enable requires an explicit approval signal, restores selection of the
   same valid record, and changes no historical scan;
3. delete requires a disabled profile and explicit confirmation, removes only
   the targeted current profile record, and leaves history bytes unchanged;
4. deleted subject references are never reused by later profile creation;
5. profile list, scan output, reports, and history remain redacted;
6. missing, malformed, wrong-version, duplicate, or unsupported profile state
   blocks lifecycle operations without recreation or empty-store semantics;
7. injected interruption during enable, disable, or delete leaves either the
   old or new valid profile store and no accepted partial target;
8. stale temporary files do not override a valid profile store;
9. the eight-profile and 32-scan bounds remain independent; and
10. lifecycle outcomes do not alter R1/R2 comparison, guarding, disappearance,
    or failure semantics.

Tests must use reserved synthetic values only. They must not test ownership,
secure erasure, real accounts, live requests, backups, or external services.

## 8. Failure and stop criteria

Stop if the design requires:

- a generic toggle or implicit re-approval;
- reusing an old opaque reference for a different profile value;
- treating a missing or malformed store as empty;
- rewriting history to hide a deleted or disabled profile;
- claiming secure erasure, identity ownership, or current consent without
  evidence;
- automatic deletion, backup, restore, identity expansion, or external sync;
- a real identifier, live request, credential, new dependency, or external
  account; or
- changes to R1/R2 failure, comparability, disappearance, or guarding rules.

## 9. Success and failure criteria

### Success

R9 succeeds if a bounded offline lifecycle experiment demonstrates explicit
disablement, explicit re-approval for re-enable, safe deletion semantics if
accepted, monotonic opaque references, preserved history, and fail-closed
profile state without changing R1/R2 behavior.

### Failure

R9 fails or stops if lifecycle actions cannot be distinguished in the stored
state, if history changes as a side effect of profile retention, if a missing
profile is treated as an empty one, or if the result depends on unsupported
secure-erasure or consent claims.

## 10. Open decisions

- Is re-enable needed, or should a disabled profile require creating a new
  profile and therefore a new opaque reference?
- Must deletion always require a prior disabled state and a second command?
- Should deletion be implemented at all before a platform-specific erasure
  design exists?
- What exact approval signal is sufficient for re-enable in an offline CLI?
- Should historical reports annotate missing current profile metadata, or
  continue showing only the opaque reference?
- What should happen when the eight-profile limit has been reached but old
  profiles were deleted?

The approved R9 default is explicit disable, fresh approval for re-enable,
two-step deletion with explicit confirmation, never-reused opaque references,
preserved history, no automatic retention action, and no secure-erasure claim.

## 11. Approval boundary

At framing time this was R9 Phase 1 only; Phase 2 required separate explicit
approval. Peter subsequently approved the lifecycle protocol, including fresh
approval for re-enable, disable-before-delete, explicit deletion confirmation,
and never-reused references. That approval did not authorize a real
identifier, live request, credential, dependency, staging, commit, push,
pull-request update, or merge.

## 12. R9 Phase 2 offline lifecycle execution

Added `profile enable --approve` and `profile delete --confirm` to the local
CLI. Re-enable requires an explicit approval signal and restores the existing
valid record. Deletion requires the profile to be disabled, removes only the
current profile record, preserves the monotonic subject-reference counter, and
leaves historical scan records unchanged. The implementation makes no secure
erasure claim.

The lifecycle writes continue to use the R8 bounded atomic replacement and
fail-closed profile loader. No profile value is copied into ordinary output,
scan history, reports, locators, or comparison identifiers, and R1/R2
semantics remain unchanged.

Focused R7/R8/R9 verification passed with 20 tests. Full-suite verification
passed with 288 tests. Ruff formatting and linting, mypy on 26 source files,
and `git diff --check` also passed.

### Phase 2 boundary

Only reserved synthetic values were used. This evidence does not prove
current consent, identity ownership, secure erasure, filesystem durability,
or recovery from a compromised host. No live request, network adapter,
credential, dependency, scheduler, notification, export, commit, push, or
pull request was added.
