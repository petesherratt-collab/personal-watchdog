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
- Removing a profile (`profile delete`) removes its record from the local
  profile store only. It does not securely erase data from disk, filesystem
  journals, backups, or other copies, and it leaves historical scan records,
  which hold only the opaque reference, unchanged.
- The repository is public. `scripts/check_synthetic_identifiers.py` rejects
  tracked email addresses outside reserved domains; it does not detect other
  kinds of identifier, and passing it does not make the repository safe for
  real data.

## Live adapter: XposedOrNot check-email

This is the only live adapter. It is off unless a scan is run with
`--adapter xposedornot` and a typed `--confirm-live` matching the profile
reference.

- **What is sent:** the email address of the one selected profile, in the URL
  path of a single HTTPS `GET`. No password, credential, cookie, or other
  profile is sent. The request carries a generic `User-Agent`.
- **Where:** `api.xposedornot.com` (`/v1/check-email/{email}`,
  `include_details=false`). The operator of that service, and any proxy you
  route traffic through, can see the address.
- **Why:** to learn which named breaches that service associates with the
  address, so later scans can report changes.
- **Limits:** one request per invocation, no retry, no redirect, bounded time
  and response size.
- **What is kept:** the opaque profile reference, the outcome, and breach
  names. The address, URL, response headers, and response body are not written
  to history, reports, or console output.
- Approved profile values are stored locally in `profiles.json` in plain text
  with owner-only permissions. Encryption at rest is not implemented.

## Interpreting results

A transport error, timeout, rate limit, blocked page, parsing failure, empty or
unverifiable response is not a negative finding. “No findings” means only that
the configured sources returned no findings during successful scans. It does
not establish that an identity is safe or unexposed.

The version 0.1 identity profile will be a clearly labelled local file with
restrictive permissions. Encrypted-at-rest storage requires a separate reviewed
design and approval after the scan and diff model is correct.
