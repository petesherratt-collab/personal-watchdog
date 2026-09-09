# Personal Watchdog references

These references are retained from the existing Base Zero history. They are
not dependencies. The current project material does not record exact upstream
repository URLs, and no new repository lookup was performed for Base Zero
completion. Current licences, maintenance, terms, data flows, accuracy, and
security remain to be reviewed before any reuse.

## Retained MIT-licensed project references

The Base Zero document identifies the following eight projects as MIT-licensed
references. That attribution is preserved here as historical project material;
it is not independently re-verified by this record.

| Project | Capability remembered by the project history | Repository URL in existing material | Dependency status |
|---|---|---|---|
| SpiderFoot | OSINT orchestration and event-driven plugin architecture | Not recorded | Reference only |
| XposedOrNot API | Breach and paste exposure lookup | Not recorded | Reference only |
| Sherlock | Username discovery across many sites | Not recorded | Reference only |
| Maigret | Richer username discovery and candidate identity evidence | Not recorded | Reference only |
| Vanish | Data-broker scanning ideas | Not recorded | Reference only |
| auto-identity-remove | Recurring checks, removal, and verification workflows | Not recorded | Reference only |
| OnionScan | Onion-service analysis; probably not personal exposure discovery | Not recorded | Reference only |
| ArchiveBox | Evidence-preservation patterns | Not recorded | Reference only |

## Architectural references

### Kibitzr

Kibitzr's fetch, extract, compare, and notify shape was considered closer to a
possible watchdog than general-purpose archiving. Its relevant lessons are
architectural principles only: record attempted checks, preserve deterministic
history, distinguish failures from clean negatives, reconcile evidence, keep
corrections append-only, test hostile mutation, and use an independent verifier
when justified.

Repository URL: not recorded in existing project material.

### Evidence-collection repository

`/home/peters/evidence-collection/repo/` is read-only architectural reference
material. It is not a destination for Personal Watchdog files, is not a
dependency, and is not copied wholesale. Its local repository state is outside
the scope of this Base Zero completion record.

Repository URL: not recorded in existing project material.

## Reuse boundary

No source code, raw pages, complete personal identifiers, credentials, or
external service configuration have been adopted. Any future reuse requires a
separate question, licence and data-flow review, privacy review, and explicit
approval.

## R3 Phase 1 official XposedOrNot contract sources

Accessed 2026-09-08 for the bounded R3 documentation experiment. These are
source references only, not dependencies or permission to call the service.

| Official source | Provenance recorded for R3 |
|---|---|
| https://xposedornot.com/api_doc | “Free Data Breach API, No API Key Required”; API Quick Reference last updated 2026-06-03. |
| https://github.com/XposedOrNot/XposedOrNot-API/blob/master/README.md | Official API repository README; `master` history showed commit prefix `b394f21` when accessed. |
| https://github.com/XposedOrNot/XposedOrNot-Python | Official Python SDK README on `main`; fetched repository page showed no pinned commit hash or release tag. |
| https://github.com/XposedOrNot/XposedOrNot-Python/blob/main/xposedornot/client.py | Official Python SDK HTTP/status and JSON handling implementation on `main`; no pinned commit hash exposed by the fetched page. |
| https://github.com/XposedOrNot/XposedOrNot-Python/blob/main/xposedornot/endpoints/email.py | Official Python SDK email endpoint paths and query/auth behavior on `main`; no pinned commit hash exposed by the fetched page. |
| https://github.com/XposedOrNot/XposedOrNot-JS | Official JavaScript SDK README on `main`; fetched repository page showed no pinned commit hash or release tag. |

The exact facts extracted from these sources, including their conflicts and
unknowns, are recorded in `RESEARCH_003_XPOSEDORNOT_CONTRACT.md`. No source
code or documentation corpus was copied into this repository.

## R3 Phase 1 correction — pinned official sources and OpenAPI artifacts

Accessed 2026-09-08. The mutable branch URLs in the preceding R3 entry are
historical references only. Use these full-SHA file permalinks for
reproducibility:

| Official source | Full-SHA permalink and provenance |
|---|---|
| API repository README | [`cbf5423ed601bd74d896efebd0d28c637a6cddef` commit](https://github.com/XposedOrNot/XposedOrNot-API/commit/cbf5423ed601bd74d896efebd0d28c637a6cddef); [README](https://github.com/XposedOrNot/XposedOrNot-API/blob/cbf5423ed601bd74d896efebd0d28c637a6cddef/README.md); API repository `master` tip observed 2026-09-08. |
| Python SDK README | [`911f49aa08939827d4717f3d48fd192c0c072c29` commit](https://github.com/XposedOrNot/XposedOrNot-Python/commit/911f49aa08939827d4717f3d48fd192c0c072c29); [README](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/README.md); Python repository `main` tip observed 2026-09-08. |
| Python SDK client | [Pinned `client.py`](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/xposedornot/client.py) at the same full SHA. |
| Python SDK email endpoint | [Pinned `email.py`](https://github.com/XposedOrNot/XposedOrNot-Python/blob/911f49aa08939827d4717f3d48fd192c0c072c29/xposedornot/endpoints/email.py) at the same full SHA. |
| JavaScript SDK README | [`d4cf1af21a53c32c03d767a59d382b01b4a21908` commit](https://github.com/XposedOrNot/XposedOrNot-JS/commit/d4cf1af21a53c32c03d767a59d382b01b4a21908); [README](https://github.com/XposedOrNot/XposedOrNot-JS/blob/d4cf1af21a53c32c03d767a59d382b01b4a21908/README.md); JavaScript repository `main` tip observed 2026-09-08. |

The official API documentation artifacts examined separately were
`https://api.xposedornot.com/docs` (Swagger UI, title “XposedOrNot API
Documentation”) and `https://api.xposedornot.com/openapi.json` (OpenAPI
3.0.0, `info.version` 2.0.0). These are live documentation artifacts and do
not have Git commit SHAs. The exact resolved facts and unresolved conflicts
are recorded in the dated correction in
`RESEARCH_003_XPOSEDORNOT_CONTRACT.md`.

## R3 Phase 1 verification record

On 2026-09-08 the exact local checks were rerun: `.venv/bin/python -m
pytest` passed 147 tests; `.venv/bin/ruff format --check .` reported `28 files
already formatted`; `.venv/bin/ruff check .` reported `All checks passed!`;
`.venv/bin/mypy .` reported `Success: no issues found in 12 source files`; and
`git diff --check` exited 0 with no output. Ruff includes the new Markdown R3
document, explaining 28 versus the earlier R2.5 record’s 27; both revisions
contain the same 12 Python files.

## R3 Phase 1 final verification record

The complete diff and status inspection preceded the final run. On
2026-09-08, `.venv/bin/python -m pytest` reported `147 passed in 6.01s`;
`.venv/bin/ruff format --check .` reported `28 files already formatted`;
`.venv/bin/ruff check .` reported `All checks passed!`; `.venv/bin/mypy .`
reported `Success: no issues found in 12 source files`; and `git diff --check`
exited 0 with no output. The earlier 5.98-second pytest output was a separate
successful run; the timing difference is normal execution variance.

## R3 Phase 1 final contract-gap verification

The complete requested diff and status inspection preceded the final run. On
2026-09-09, `./.venv/bin/python -m pytest` reported `147 passed in 6.08s`;
`./.venv/bin/ruff format --check .` reported `28 files already formatted`;
`./.venv/bin/ruff check .` reported `All checks passed!`; `./.venv/bin/mypy .`
reported `Success: no issues found in 12 source files`; and `git diff --check`
exited 0 with no output.

## R3 Phase 1 final contract-gap correction

Accessed and recorded 2026-09-09 as a documentation-only correction. The
current research document removes the impossible selected-XON conflicting
duplicate row, keeps analytics positive-success normalization deferred, freezes
content-type/header derivation and retained-header accounting, freezes compact
normalized-R2 serialization, and distinguishes pre-status from post-status
transport failure. No new source was examined and no OpenAPI artifact was
downloaded again.
