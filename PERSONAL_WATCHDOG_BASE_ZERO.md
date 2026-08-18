# Personal Watchdog — Base Zero

## Instruction to Codex

Work only in:

```text
/home/peters/personal-watchdog/
```

This is a speculative research project. We do not yet know what it should become, whether it will become a product, or which technical direction will prove useful. Do not treat the notes below as a settled specification. The purpose of this first step is to establish a clean, durable base of operations from which experiments and decisions can be recorded.

The separate repository at `/home/peters/evidence-collection/repo/` is read-only reference material. Do not create, edit, delete, stage, or commit anything there. Leave its tracked and untracked files untouched.

## Project history to preserve

The project began with a question: could a standalone application act as a personal watchdog, checking whether a consenting user's name or approved personal identifiers appear on ordinary websites, data-broker sites, breach sources, or parts of the dark web?

Early research found no single mature open-source application that honestly covers the whole problem. Instead, useful capabilities are scattered across several MIT-licensed projects:

- **SpiderFoot** — OSINT orchestration and event-driven plugin architecture.
- **XposedOrNot API** — breach and paste exposure lookup.
- **Sherlock** — username discovery across many sites.
- **Maigret** — richer username discovery and candidate identity evidence.
- **Vanish** — data-broker scanning ideas.
- **auto-identity-remove** — recurring checks, removal, and verification workflows.
- **OnionScan** — onion-service analysis; probably not personal exposure discovery.
- **ArchiveBox** — evidence-preservation patterns.

These are references, not approved dependencies. Their dependencies, current licences, maintenance, data flows, terms, accuracy, and security would require separate examination before reuse.

An attempted amalgamation of their documentation produced a large, incoherent corpus. That established an important lesson: do not combine whole codebases or documentation. Extract capabilities and patterns only when a concrete experiment needs them.

ArchiveBox prompted comparison with **Kibitzr** and the existing evidence-collection project. Kibitzr's monitoring shape—fetch, extract, compare, notify—is closer to the possible watchdog than general-purpose archiving. The evidence archive also offers useful integrity principles:

- record attempted checks, including failures;
- never turn failed or incomplete checks into clean negative results;
- preserve deterministic history and verify stored claims from underlying fields;
- reconcile referenced evidence rather than trusting database integrity alone;
- keep corrections append-only;
- test hostile mutation;
- use an independent verifier where the research question requires one.

These are principles to remember, not requirements to implement immediately. A local hash chain cannot prove trustworthy time or detect a completely rewritten, internally consistent history without an independently retained checkpoint or external anchor.

A previous build itinerary proposed a local-first Python CLI using XposedOrNot and Maigret, SQLite history, deterministic comparison, and JSON/HTML reports. That itinerary is background material, not the current marching order. It became too close to a product specification for the present exploratory stage.

The enduring conceptual distinctions are:

1. **Publicly exposed:** an identifier appears on an observable page or service.
2. **Known to be held privately:** an organisation stores the data, which usually cannot be discovered by external scanning.
3. **Leaked or traded:** data appears in breach corpora, pastes, forums, marketplaces, or specialist feeds.

No future prototype should claim comprehensive dark-web coverage or interpret “no finding” as “safe.” Username matches are candidates, not proof of identity.

## First step: establish the research base

Do not write application code in this step.

1. Run `pwd` and confirm the exact project root.
2. Inspect all existing files and report them before changing anything.
3. If Git already exists, report its status and recent history. If it does not exist, initialise a repository.
4. Preserve any existing material. Do not overwrite or reorganise it silently.
5. Create only the minimal research scaffold described below, adapting names if equivalent files already exist:

```text
README.md
PROJECT_HISTORY.md
RESEARCH_LOG.md
DECISIONS.md
REFERENCES.md
AGENTS.md
.gitignore
```

### File purposes

- `README.md`: a short statement that this is an exploratory personal-exposure research project, with no settled product promise.
- `PROJECT_HISTORY.md`: preserve the history in this document, including abandoned or deferred directions. Do not rewrite the past to make the project appear more settled than it was.
- `RESEARCH_LOG.md`: chronological, append-oriented entries for questions, experiments, observations, failures, and next questions. Start it with today's date and a Base Zero entry.
- `DECISIONS.md`: decisions with date, context, current status (`provisional`, `accepted`, `rejected`, or `superseded`), reasoning, and what evidence might change them.
- `REFERENCES.md`: the eight retained MIT-licensed projects, Kibitzr/evidence-collection references, exact repository URLs when already known, and a clear distinction between “reference” and “dependency.” Do not perform a broad new repository audit in this step.
- `AGENTS.md`: durable working rules for future Codex sessions.
- `.gitignore`: exclude local data, secrets, databases, generated reports, caches, virtual environments, and files likely to contain personal identifiers.

### `AGENTS.md` rules

Include these rules:

- This is speculative research; do not assume a product, architecture, or destination.
- Prefer the smallest experiment that answers the current question.
- Separate observations, inferences, and decisions.
- Record failures and negative results rather than hiding them.
- Do not use real personal information in source, tests, fixtures, logs, reports, prompts, or commits unless the user explicitly approves a later controlled experiment.
- Do not scan another person or automate intrusive, evasive, destructive, or deceptive activity.
- Do not add a dependency merely because it appeared in an earlier plan. State what question it helps answer, inspect its licence and data flow, and obtain approval first.
- Treat `/home/peters/evidence-collection/repo/` as read-only.
- Before implementation, state the research question, success signal, failure signal, scope, and stopping point.
- After an experiment, update the research log and decisions affected by the result.
- Never describe a failed, blocked, incomplete, or unverifiable check as “not found.”
- Review `git diff` and report `git status` at each handoff.

## Boundaries for Base Zero

Do not yet create:

- application source code;
- a database or schema;
- adapters, crawlers, scanners, or network requests;
- hash chains or an independent verifier;
- encryption or key management;
- a GUI, background service, report generator, packaging, or deployment configuration;
- external accounts, API keys, scheduled jobs, or live integrations;
- synthetic technical architecture merely to fill the repository.

Do not copy source or documentation wholesale from the reference projects or the evidence repository.

## Completion and handoff

After creating the minimal scaffold:

1. show the resulting file tree;
2. summarise what was placed in each file;
3. run any lightweight documentation checks that are already available, but add no tool solely for this purpose;
4. show `git diff --check` and `git status`;
5. create a Base Zero Git commit only if Git author identity is already configured; otherwise stop and report the exact blocker without changing global Git configuration;
6. propose **one small research question** as the next step, but do not begin answering or implementing it.

Stop after the handoff and wait for approval.

## Base Zero success condition

Success is not runnable software. Success is a clean repository that accurately remembers why the project exists, what has already been considered, what remains uncertain, and how future experiments should be conducted without prematurely deciding what the project must become.
