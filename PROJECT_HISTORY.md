# Personal Watchdog project history

This record preserves the project story without turning exploratory notes into
a product specification. Dates and claims are marked by their evidence where
that distinction matters.

## Origin and research direction

The project began with an open question: could a standalone application help a
consenting user notice whether their name or explicitly approved identifiers
appear on ordinary websites, data-broker sites, breach sources, or parts of the
dark web?

The existing Base Zero material records an early conclusion: no single mature
open-source application was found that honestly covers the whole problem.
Useful capabilities appeared to be distributed across several projects. That
is a research observation, not a claim of comprehensive market or repository
coverage.

The enduring distinctions recorded for future work are:

1. **Publicly exposed:** an identifier appears on an observable page or service.
2. **Known to be held privately:** an organisation stores the data, which is
   usually not discoverable through external scanning.
3. **Leaked or traded:** data appears in breach corpora, pastes, forums,
   marketplaces, or specialist feeds.

No definition of a Personal Watchdog “bark” has been experimentally validated.
No future prototype should treat no findings as proof of safety, claim
comprehensive dark-web coverage, or treat a username match as confirmed
identity evidence.

## Rejected or deferred directions

- A documentation amalgamation produced a large, incoherent corpus. Whole
  documents and whole codebases were not retained as an implementation method.
  Capabilities and patterns may be examined only when a concrete experiment
  requires them.
- A more detailed local-first Python CLI itinerary involving XposedOrNot,
  Maigret, SQLite history, deterministic comparison, and JSON/HTML reports is
  background material. It is not automatic permission or the current marching
  order.
- Live adapters, real identifiers, external accounts, scheduled jobs,
  persistence, evidence retention, publication, and deployment remain outside
  Base Zero.

## Milestone 0 foundation

The directly verified Git history contains the Milestone 0 foundation commit:

`b07bed2c3872b083f541d7ae6c1b29e568c0079b` — `chore: establish milestone 0 project foundation`

It contains policy and privacy documentation, packaging and development-tool
configuration, a policy smoke-test module, and an empty `data/` placeholder.
It contains no scanner, comparator, persistence layer, adapter, or network
integration. The Milestone 0 policy and tooling checks pass.

The later Base Zero, itinerary, progress, research, decision, reference, and
build-history records preserve the project history around that commit. The
three handoff documents were untracked before Base Zero completion and are now
being added without changing the earlier commit.

## Current status after Base Zero

Base Zero is a documentation and research-history checkpoint. The project is
speculative research, not an urgent product build. The next proposed research
question is whether deterministic observations can be converted into rare,
truthful bark events. That question is not answered by this record and no
comparator experiment is begun here.
