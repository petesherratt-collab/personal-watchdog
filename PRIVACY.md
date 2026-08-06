# Privacy policy and data boundaries

Personal Watchdog is designed for a consenting local user monitoring only their
explicitly approved identifiers. Local identity data is sensitive even when the
application does not collect passwords.

## Version 0.1 rules

- Development, tests, examples, logs, screenshots, commits, and reports use no
  real personal information.
- Complete email addresses are never written to console or structured logs.
- Identity profiles, databases, evidence, reports, and secrets remain local and
  are excluded from Git.
- An identifier may leave the machine only through a specifically enabled
  adapter endpoint required for the selected scan.
- Before a live adapter is enabled, its documentation must say exactly which
  identifier is sent, where it is sent, and why.
- Evidence is selective and bounded. Whole-site capture and unrelated personal
  information are outside scope.
- Raw adapter payload retention is off by default and, if later approved, must
  be bounded, local, and documented.
- No telemetry or remote analytics are planned for version 0.1.

## Interpreting results

A transport error, timeout, rate limit, blocked page, parsing failure, empty or
unverifiable response is not a negative finding. “No findings” means only that
the configured sources returned no findings during successful scans. It does
not establish that an identity is safe or unexposed.

The version 0.1 identity profile will be a clearly labelled local file with
restrictive permissions. Encrypted-at-rest storage requires a separate reviewed
design and approval after the scan and diff model is correct.
