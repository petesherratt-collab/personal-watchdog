# Personal Watchdog contributor rules

These rules apply to the entire repository.

## Safety and privacy

- Never add real personally identifiable information (PII) to source, tests,
  fixtures, examples, logs, commands, screenshots, commits, or reports.
- Use obviously synthetic identifiers under reserved domains such as
  `example.invalid` when a later milestone requires fixtures.
- Never log a complete email address. Console and structured logs must redact it.
- Never translate adapter failure, blocking, timeout, malformed output, or an
  unverifiable result into "not found" or a clean scan.
- Send identifiers only to the explicitly configured endpoint required by an
  approved adapter. Document what leaves the machine, its destination, and why
  before enabling a live adapter.
- Do not collect passwords, test credentials, evade access controls, or scan
  anyone except the consenting local user.
- Keep evidence selective, bounded, and local. Do not archive whole sites or
  unrelated personal information.

## Engineering workflow

- Add or update tests for every behavioural change.
- Mock network access by default; tests must not require external services.
- Ask before adding a dependency, enabling a live scan, using real personal
  data, automating an external action, or expanding scope.
- Do not implement a later milestone automatically when it crosses one of those
  approval boundaries.
- After every approved research or implementation step, append one entry to
  `BUILD_HISTORY.md`. Always include a Gotchas section, writing `None observed`
  when there were none. Never rewrite earlier entries merely to make the
  development path appear cleaner; correct them with a later dated note.
- `BUILD_HISTORY.md` is the only per-step record. Do not repeat the entry
  elsewhere. `PROGRESS_LOG.md` and `RESEARCH_LOG.md` are closed archives.
  Add to `DECISIONS.md` only when a decision changes direction, and update
  `ROADMAP.md` only when the plan changes. Write a `RESEARCH_0NN_*.md` framing
  document only for work that crosses an approval boundary listed above.
- Stored formats, references, and module names must not carry experiment
  numbers. Test files may keep them as provenance.
- A live request needs a typed confirmation on every invocation and must be
  limited to one request with no retry and no redirect. Real identifiers are
  entered only on the user's own machine, never in this repository, a cloud
  session, a command line, or a log.
- Run formatting, linting, type checks, and tests before declaring a milestone
  complete.
- Review `git diff` and report uncommitted files at every handoff.
- Preserve the distinction between a successful comparable scan with no
  observation and a failed or incomplete scan.

## Supported commands

Create the development environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pytest ruff mypy
```

Run verification:

```bash
.venv/bin/python scripts/check_synthetic_identifiers.py
.venv/bin/python -m pytest
.venv/bin/ruff format --check .
.venv/bin/ruff check .
.venv/bin/mypy .
git diff --check
git status --short --branch
```
