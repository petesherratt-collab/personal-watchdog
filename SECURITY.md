# Security policy

## Scope

Personal Watchdog is a local diagnostic prototype. It does not provide complete
exposure coverage, credential protection, identity verification, or a guarantee
of safety. Version 0.1 must fail visibly when a source is blocked, unavailable,
malformed, rate-limited, or otherwise unverifiable.

## Safe development

- Use synthetic fixtures only; never commit real identifiers or secrets.
- Do not submit passwords or perform credential testing.
- Mock network access in automated tests.
- Bound network time, redirects, response size, and subprocess output before
  live adapters are enabled.
- Treat public username matches as candidates, not confirmed identities.
- Escape untrusted report content and retain only minimal evidence.
- Do not add active countermeasures, automated submissions, CAPTCHA bypass, or
  anti-bot evasion.

## Reporting a vulnerability

Do not include real personal data, credentials, or exploit data in an issue or
commit. Report the smallest synthetic reproduction privately to the repository
owner. There is no production deployment or security-bounty programme in this
prototype milestone.
