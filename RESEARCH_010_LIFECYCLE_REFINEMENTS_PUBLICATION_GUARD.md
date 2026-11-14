# Research Experiment R10 — lifecycle refinements and publication guard

**Status: Phase 2 implemented and verified offline.** Phase 1 (§1–§11) was
drafted away from the authoritative local repository and is kept as written.
§12 records the reconciliation, §13 the approved decisions, and §14 the
Phase 2 result. R10 adds no dependency, CI configuration, or hook, and does
not authorize a real identifier, live request, credential, scheduler,
notification, or export.

## 1. Research question

Can the R9 approved-profile lifecycle be made more truthful and harder to
misuse, without weakening R1/R2 semantics? The specific goals are:

- a bounded profile store that cannot lock itself;
- a deliberate re-enable signal;
- honest wording about removal and erasure;
- historical reports that stay understandable after deletion.

A second question is whether a public repository can be protected against
accidental publication of non-synthetic identifiers.

R10 is about local lifecycle behavior, wording, and repository hygiene. It does
not test identity ownership, source coverage, source accuracy, secure erasure,
or remediation.

## 2. Repository reconciliation

The intended baseline is merge commit `67451e0` on `main` (PR #6, R9 lifecycle).
This framing was drafted on 13 Nov 2026 from a fresh clone of
`github.com/petesherratt-collab/personal-watchdog`. The local repository at
`/home/peters/personal-watchdog/` is authoritative and was not available.

Before any Phase 2 work:

```bash
cd /home/peters/personal-watchdog
git fetch && git status --short --branch
git log --oneline --decorate -12
.venv/bin/python -m pytest
```

Expect `main` at `67451e0` and 288 passing tests. If local state differs,
revise this framing before continuing. Phase 2 would use a new branch,
`experiment/r10-lifecycle-refinements`.

## 3. Existing state and observed issues

Code reading of `personal_watchdog/profiles.py` and `cli.py` at `67451e0`
shows:

- **Profile cap.** `MAX_PROFILES = 8` is checked against `len(profiles)`. That
  list holds enabled and disabled records; deleted records are removed. Deletion
  already frees a slot, so Peter's decision (cap counts stored profiles, not
  profiles ever created) is already the implemented behavior. It is not yet
  pinned by a dedicated test.
- **Reference counter exhaustion.** References use the pattern
  `r7-subject-NNN`, and `load_profiles` accepts `next_subject_number` only in
  `1..999`. A pre-framing check reproduced this with a synthetic value:
  `add_profile` issues `r7-subject-999`, then writes
  `next_subject_number = 1000`. The next `load_profiles` fails with
  `local profile sequence is invalid`, which makes the whole store, including
  `profile list`, unloadable. This fails closed and produces no false clean
  result, but it bricks the store. The add should be refused before the write.
- **Re-enable signal.** `profile enable --approve` accepts a bare flag. Add uses
  the same flag. A habitual flag is a weak signal of deliberate intent.
- **Deletion wording.** `profile delete` prints `PROFILE_DELETED`. The
  implementation makes no secure-erasure claim, but user-facing text does not
  say so explicitly.
- **History after deletion.** Historical scan records keep the opaque
  reference. Reports do not indicate that the referenced profile no longer
  exists.
- **Publication guard.** The repository is public. `.gitignore` excludes
  `data/*`, identity files, secrets, evidence, reports, and logs. A scan on
  13 Nov 2026 found only `example.invalid` addresses in tracked files. No
  pre-commit hook or CI check enforces this.
- **Stale records.** The status headers of `RESEARCH_002_5_…` and
  `RESEARCH_003_5_…` still read “framed, not implemented or run,” although both
  experiments were executed and merged.

## 4. Claim and non-claims

### Claim under test

The lifecycle refinements below can be implemented offline over synthetic
profiles. They can leave R1/R2 comparison, guarding, disappearance, and
failure semantics unchanged. They can avoid copying a profile value into
ordinary output, history, or reports. A repository check can reject
non-synthetic email addresses in tracked files.

### Non-claims

R10 would not establish that:

- typing a reference proves current consent, identity ownership, or control of
  the identifier;
- deletion securely erases data from disk, backups, or filesystem journals;
- the publication guard detects every kind of personal identifier (usernames,
  phone numbers, and free-text names are out of scope);
- a passing guard makes the repository safe for real data;
- any source is complete, fresh, or accurate.

## 5. Proposed changes

**A. Profile cap (decided).** Keep the cap on stored profiles, with enabled and
disabled records both counting. Add a test that deleting a profile at the cap
permits a new add. The new add receives a fresh, never-reused reference.

**B. Reference exhaustion.** Refuse `add_profile` with a clear error before
writing when the counter cannot issue another valid reference. The existing
store must stay loadable. Widening the reference pattern is out of scope for
R10.

**C. Re-enable confirmation (decided).** Replace the bare `--approve` on
`profile enable` with a typed confirmation: `--confirm-ref <subject_ref>`,
which must exactly match `--subject-ref`. A mismatch or omission fails without
changing state. Whether `profile add` should change too is left open (§10).

**D. Removal wording (decided).** Change user-facing deletion output to say the
profile was removed from the local profile store, and that the command does not
securely erase data. Example: `PROFILE_REMOVED subject_ref=… (not securely
erased)`. Make matching wording changes in `README.md`/`PRIVACY.md` where
deletion is described. The machine-readable token change needs a decision
(§10).

**E. History annotation (decided).** When a report or history view shows a
scan record whose opaque reference has no current profile, add a plain
annotation such as `profile since removed`. The identifier must never be
restored. The stored historical record must stay unchanged; the annotation
exists only at display time.

**F. Publication guard (decided).** Add a dependency-free check script, for
example `scripts/check_synthetic_identifiers.py`. It scans tracked text files
and fails on any email address whose domain is not `example.invalid` (or
another explicitly allow-listed reserved domain). The script must report file
and line only, never the matched address. It can be run locally and,
separately approved, wired into a pre-commit hook or a GitHub Actions
workflow.

**G. Record housekeeping.** Correct the stale status headers in the R2.5 and
R3.5 research documents. Do not rewrite their history sections.

## 6. Consent and retention boundaries

- Typed confirmation is an intent signal, not proof of consent.
- Removal deletes only the current profile record. Historical scan records and
  the monotonic counter are untouched.
- Annotations are display-only and derived from current state.
- The guard script must not log or print the identifiers it detects.

## 7. Offline Phase 2 acceptance matrix

| Case | Expected result |
|---|---|
| 8 stored profiles, add | refused: limit reached; store unchanged |
| 8 stored, disable one, add | refused (disabled still counts) |
| 8 stored, disable + remove one, add | accepted with fresh reference |
| Counter at 999, add | `r7-subject-999` issued; store loadable afterwards |
| Counter exhausted, add | refused before write; store loadable; list works |
| Enable with matching `--confirm-ref` | re-enabled; history unchanged |
| Enable with mismatched/missing confirmation | fails; state unchanged |
| Remove disabled profile | output states removal and no secure erasure |
| Report with removed reference | shows opaque ref + `profile since removed`; no value |
| Report with live reference | no annotation |
| Guard: only `example.invalid` addresses | passes |
| Guard: non-reserved address in tracked file | fails; reports file:line only |
| Guard output | never contains the matched address |
| R1/R2/R2.5/R3.5/R5 suites | unchanged and passing |

## 8. Failure and stop criteria

Stop and record a negative result in any of these cases:

- a change requires altering R1/R2 semantics;
- a profile value appears in output, history, reports, or guard output;
- an annotation mutates stored history;
- the guard needs a new dependency;
- reference exhaustion cannot be prevented without a migration of existing
  stores.

## 9. Success and failure criteria

### Success

All acceptance cases pass. The full suite, Ruff format/lint, mypy, and
`git diff --check` pass. BUILD_HISTORY gains a Gotchas section, and the
history, research, decision, and progress records are updated.

### Failure

Any stop criterion is triggered, or any acceptance case cannot be met without
widening scope.

## 10. Open decisions

- Should `profile add` also move from `--approve` to a typed confirmation, for
  consistency?
- Should the output token change from `PROFILE_DELETED` to `PROFILE_REMOVED`,
  or keep the token and change only the human-readable text? Any scripts
  reading the output would care.
- Should the guard run in GitHub Actions, a local pre-commit hook, or both?
- Which reserved domains should the guard allow beyond `example.invalid`?
- Should reference exhaustion eventually be solved by a wider pattern, with a
  versioned migration (a later experiment)?
- Should the repository stay public once real identifiers are in use locally?

## 11. Approval boundary

This is R10 Phase 1 only. Phase 2 requires Peter's explicit approval of
§5 A–G and of the §10 decisions. Approval of Phase 2 would not authorize a real
identifier, live request, credential, dependency, scheduler, notification,
export, staging, commit, push, pull request, or merge.

## 12. Reconciliation (13 Nov 2026)

Checked in a cloud session clone, not the local repository at
`/home/peters/personal-watchdog/`. Branch `ccr-058bcad3-37cjg1` was at
`67451e0`, identical to `main`; the worktree was clean; 288 tests passed;
Ruff format/lint and mypy (26 files) passed. Every §3 observation was
confirmed, including a reproduction of reference exhaustion with a synthetic
username. Four points not covered by §1–§11 were raised before approval:

1. The §7 case “counter at 999 → store loadable afterwards” needs the loader
   to accept `next_subject_number = 1000` as an exhausted marker. Stores
   already bricked at 1000 become loadable again; no migration is needed.
2. The default fixture subject `r6-subject-01` never has a profile, so the
   annotation must apply only to `r7-subject-NNN` references.
3. Human `history` output does not print `subject_ref`, so the annotation
   applies to `report`. `report --json` prints the stored record verbatim.
4. This session can push only to `ccr-058bcad3-37cjg1`, so Phase 2 is on that
   branch instead of `experiment/r10-lifecycle-refinements`.

## 13. Approved decisions (13 Nov 2026)

Peter approved §5 A–G and these resolutions:

- `profile add` keeps `--approve`; only `profile enable` moves to
  `--confirm-ref`.
- The removal token changes to `PROFILE_REMOVED … (not securely erased)`.
  No script in the repository consumed `PROFILE_DELETED`.
- The guard is a script run manually and by a pytest test, so CI running the
  suite enforces it. A pre-commit hook or GitHub Actions workflow would need
  separate approval.
- Allowed domains: `example.invalid`, `example.com`, `example.org`,
  `example.net` (and their subdomains) and the `.test` top-level domain.
- The loader accepts 1000 as an exhausted marker (§12 point 1).
- The annotation appears only in human-readable `report` output; JSON output
  stays the stored record (§12 point 3).

Deferred, not decided: a wider reference pattern with a versioned migration,
and whether the repository should stay public once real identifiers are used
locally.

## 14. Phase 2 result

All §7 acceptance cases pass offline over synthetic profiles.

- **A.** Tests pin that enabled and disabled profiles both count toward the
  cap and that removal frees a slot with a fresh, never-reused reference.
- **B.** `add_profile` refuses with `local profile references are exhausted`
  before writing once the counter passes 999. The loader accepts 1..1000;
  0 and 1001 still fail closed.
- **C.** `profile enable` requires `--confirm-ref` equal to `--subject-ref`.
  Missing, mismatched, or another profile's reference fails without changing
  the store. The bare `--approve` flag is rejected by the parser.
- **D.** Deletion prints `PROFILE_REMOVED subject_ref=… (not securely
  erased)`. `README.md` and `PRIVACY.md` state that removal does not securely
  erase data.
- **E.** Human `report` appends `PROFILE_NOTE subject_ref=… profile since
  removed` when an `r7-subject-NNN` reference has no current record. A disabled
  profile and the default subject get no note. If the profile store cannot be
  loaded, the note reads `profile status unavailable`, so the report never
  implies the profile is live. History bytes and JSON output are unchanged.
- **F.** `scripts/check_synthetic_identifiers.py` scans `git ls-files`
  output, skips binary files, prints `path:line` only, and fails closed (exit
  2) if tracked files cannot be listed. It uses only the standard library and
  the existing `git` executable.
- **G.** The R2.5 and R3.5 status headers were corrected with a dated note;
  their bodies were not rewritten.

R1/R2/R2.5/R3.5/R5 suites are unchanged and pass. No stop criterion was
triggered.

### Limitations

- `--confirm-ref` is an intent signal, not proof of consent or ownership.
- The guard detects email addresses only, and only in tracked files. Commit
  messages, branch names, and untracked files are not checked.
- The annotation reflects current state at display time; it cannot tell a
  removed profile from a store that was replaced or reset.
