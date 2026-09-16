# Research Experiment R8 — profile retention and recovery

**Status: Phase 2 conservative subset implemented and verified offline.** Phase
1 framed the retention and recovery boundary; Phase 2 tightens missing-state
handling and verifies conservative local recovery behavior. It does not add
deletion, backup, recovery commands, encryption, a live source, a real
identifier, a dependency, a scheduler, a notification, or an external
request.

## 1. Research question

Can Personal Watchdog retain, disable, remove, and recover local approved
identifier profiles without silently changing consent state, rewriting
historical scan evidence, or turning damaged state into a clean or empty
result?

The experiment is about local state behavior, not about identity ownership or
source truth. The smallest useful test must distinguish active, disabled,
deleted, missing, malformed, interrupted, and successfully recovered state.

## 2. Repository reconciliation

The authoritative baseline is merge commit `81e979c` on local `main`, which
contains the merged R7 offline approved-identifier configuration. This framing
is on the new local branch `experiment/r8-profile-retention-recovery`, created
from that clean baseline.

R7 currently stores sensitive profile values in a separate versioned
`profiles.json` sidecar. It supports add, redacted list, disable, and offline
fixture selection by opaque `subject_ref`; it has no delete, backup, restore,
corruption-repair, or re-enable command. R6 scan history remains a separate
bounded record set with a maximum of 32 retained scans.

## 3. Observed R7 facts and limits

The R7 implementation provides the starting evidence for this framing:

- profile storage is limited to eight profiles;
- values are kind-validated and stored only in the local profile file;
- the profile file is written using a temporary-file replacement and set to
  mode `0600`;
- disablement changes `enabled` to false and prevents future selection;
- disablement does not remove the value or rewrite scan history;
- ordinary profile, scan, report, and history output is redacted; and
- no encryption, filesystem sync guarantee, backup, secure erasure, or
  compromised-host resistance is claimed.

The current atomic replacement is an implementation mechanism, not proof that
data survives power loss or that a complete write is durable on every
filesystem. R8 must keep that distinction explicit.

## 4. Claim and non-claims

### Claim under test

A small, explicit local retention policy can preserve the distinction between
an enabled profile, a disabled profile, a deleted profile, and damaged or
unavailable profile state, while leaving prior scan records truthful and
bounded.

### Non-claims

R8 would not establish that:

- a profile value is encrypted, unrecoverable after deletion, or safe from a
  compromised host;
- a local backup is authentic, current, complete, or free of sensitive data;
- a restored profile remains authorized by the user who originally created it;
- filesystem replacement is durable across power loss, disk failure, or
  concurrent writers;
- historical scan records prove current profile ownership or source coverage;
- a missing profile means that the identifier was absent from a source; or
- any failed, malformed, partial, uncertain, or unverifiable scan is clean.

## 5. Retention model to evaluate

R8 should evaluate these explicit states independently rather than infer one
from another:

| State | Can a new scan select it? | What happens to the value? | Historical records |
|---|---:|---|---|
| enabled and approved | yes | retained locally | retained by existing history policy |
| disabled | no | retained unless separately deleted | retained and not rewritten |
| deleted | no | removed by an explicit local action, subject to best-effort limits | retained as opaque historical references |
| missing or malformed store | no | unavailable or untrusted | history remains distinct and must not be reinterpreted |

The conservative policy for a later implementation is:

- disablement is a reversible selection state only if a separately approved
  re-enable operation is defined;
- deletion is explicit, separately confirmed, and never implied by
  disablement, scan failure, or an age threshold;
- no automatic time-based deletion is introduced without an explicit user
  retention policy;
- the eight-profile bound remains independent from the 32-scan history bound;
- historical records are not deleted or rewritten merely because a profile is
  disabled or deleted; and
- secure erasure is not claimed unless a reviewed platform-specific design
  supports that claim.

Whether deletion should be available in the first R8 implementation remains
an approval choice. A framing experiment must not silently turn the existing
disable-only R7 behavior into deletion.

## 6. Recovery and corruption model

The experiment should test recovery as a truth-preservation problem:

1. A normal profile write produces either the previous complete target or the
   new complete target. A partially written temporary file must not be
   accepted as the profile store.
2. An interrupted write may leave a temporary artifact, but the target must
   remain readable or fail visibly. Cleanup must not remove the only valid
   target.
3. A truncated, invalid-UTF-8, invalid-JSON, unsupported-version, duplicate,
   or unsupported-field profile file must fail closed. It must not be treated
   as an empty profile set, and it must not cause scan disappearance.
4. A missing profile sidecar beside valid legacy R6 config/history needs an
   explicit compatibility rule. Creating an empty sidecar must never be
   presented as recovering or deleting prior profile state.
5. A user-supplied restore or backup, if later allowed, must be validated as a
   complete versioned profile file before replacement. Automatic imports,
   merging, alias discovery, and conflict resolution are outside this scope.
6. Recovery output must identify unavailable or invalid local profile state
   without exposing the sensitive value or claiming a source result.

R8 should not add a second history authority, silently replay old profile
values, or use scan history to reconstruct a deleted profile.

## 7. Offline Phase 2 acceptance matrix

If separately approved, the smallest implementation should test:

1. disabled profiles remain unavailable for selection and prior history bytes
   remain unchanged;
2. an explicit deletion path, if accepted, removes only the targeted local
   profile record and leaves prior history as opaque records;
3. reload preserves valid enabled and disabled states without adding fields or
   leaking values into ordinary output;
4. malformed, truncated, wrong-version, duplicate-reference, and unsupported
   field inputs fail visibly and are not converted into an empty store;
5. an injected write interruption leaves either the old valid target or the
   new valid target, never a partially accepted target;
6. a stale temporary file cannot replace or override a valid profile store;
7. profile and scan-history bounds remain independent and enforced;
8. no recovery or deletion result changes R1/R2 comparison, guarding, or
   exposure semantics; and
9. all tests use reserved synthetic values, with no complete value in normal
   output, reports, history, fixtures, or committed expected output.

The conservative Phase 2 implementation covers missing and malformed-state
failure, interrupted-write preservation, stale temporary-file isolation, and
independent bounds. Deletion, backup, restore, and secure-erasure behavior
remain outside the implemented subset.

## 8. Failure and stop criteria

Stop if the design requires:

- treating a missing or malformed profile store as an empty store;
- treating deletion as proof that an identifier was never scanned or never
  exposed;
- rewriting or deleting history to hide a profile’s prior use;
- claiming secure erasure, encryption, durability, or backup authenticity
  without a reviewed platform-specific basis;
- automatic restore, profile merging, identity expansion, or external backup;
- a real identifier, live request, credential, new dependency, or external
  account; or
- changes to R1/R2 failure, comparability, disappearance, or guarding rules.

## 9. Success and failure criteria

### Success

R8 succeeds if an approved offline experiment demonstrates a bounded and
truthful policy for profile disablement, any explicitly approved deletion,
normal writes, interrupted writes, malformed state, and recovery boundaries,
while leaving R6 history and R1/R2 outcomes intact.

### Failure

R8 fails or stops if the implementation cannot distinguish unavailable local
profile state from an empty profile set, if retention actions rewrite history,
or if the experiment requires claims about secure deletion or durable recovery
that the local evidence cannot support.

## 10. Open decisions

- Is deletion needed now, or is disablement plus manual local file removal
  sufficient for the next experiment?
- Should a disabled profile retain its value indefinitely until explicit
  deletion, or should a user-selected retention period be supported?
- Should the tool refuse to initialize a missing sidecar beside an existing
  R6 state, or create it only through an explicit profile setup command?
- Is a backup/restore feature in scope at all, given that it creates another
  sensitive copy?
- What crash and filesystem guarantees can be tested on the supported local
  platform without claiming universal durability?
- Should historical reports show a stable opaque subject reference when its
  profile is deleted, or mark the profile metadata unavailable without
  changing the scan record?

The conservative default is disable-only, no automatic deletion, no backup,
fail-closed malformed-state handling, bounded atomic replacement, preserved
opaque history, and no claim of secure erasure or durable recovery.

## 11. Approval boundary

At framing time this was R8 Phase 1 only; Phase 2 required separate explicit
approval. Peter subsequently approved the conservative offline subset. That
approval did not authorize deletion, backup, restore, secure-erasure claims,
real identifiers, live requests, credentials, dependencies, staging, commit,
push, pull-request update, or merge.

## 12. R8 Phase 2 conservative offline execution

The profile loader now fails visibly when the R7 sidecar is missing rather
than recreating an empty store. Existing malformed, wrong-version,
unsupported-field, and invalid-JSON handling remains fail closed. The existing
temporary-file replacement remains the only write mechanism; tests inject a
failure before replacement and verify that the previous valid target remains
unchanged. A stale temporary file is ignored and cannot override a valid
target.

The implementation does not add deletion, backup, restore, re-enable, or
automatic age-based retention. Disabled profiles retain their local value and
cannot be selected; historical scan records remain independent and bounded.

Focused R7/R8 verification passed with 16 tests. Full-suite verification
passed with 284 tests. Ruff formatting and linting, mypy on 25 source files,
and `git diff --check` also passed.

### Phase 2 boundary

Only reserved synthetic values were used. This evidence does not prove
power-loss durability, secure erasure, encryption, backup authenticity, or
recovery from a compromised host. R1/R2 comparison, guarding, disappearance,
and failure semantics were not changed.
