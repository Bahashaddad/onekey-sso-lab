# Verification — 2026-11-02

**Status: prepared loopback teaching candidate; protocol simulations are explicitly bounded.**

- Fresh isolated Python 3.12 environment installed the exact supplied `requirements-dev.txt` successfully.
- `pip check`: no broken requirements.
- 11 targeted regression tests passed: no default admin, enrollment seed denial, no seed in cookie, TOTP reuse denial, MFA failure lockout, SSTI non-evaluation, escaped search text, global-log authorization, forged/replayed message denial, OAuth redirect/state/PKCE flow, and selected business authorization/CSRF/header behavior.
- Real-CSRF registration, password login, TOTP login, and representative portal routes passed through Flask's test client. Initialization and prompted user commands passed via the CLI test runner.
- Critical-error Ruff checks passed.
- `pip-audit 2.10.1` reported no known vulnerabilities for the 25 pinned runtime packages. JSON is `dependency-audit.json`; no absence-of-future-vulnerabilities guarantee is implied.

Remaining: rotate original provider/application secrets and regenerate old TLS keypairs before reuse; manual browser review; hosted CI; optional live Google sign-in. Live Google was disabled and not exercised. SAML XML interoperability, external OAuth clients, real SMS, full security testing, and production operation were not verified and are not claimed.

## Common publication checks and limits

- Original inputs were accessed read-only and all seven original SHA-256 hashes were rechecked unchanged.
- Prepared files were compared against 69 sensitive values from original environment/database material and nine identifier-shaped values from original reports, without printing those values. No matches remained in the public candidates.
- No original private keys, `.env`, runtime databases/logs, executable tools, raw PDFs, or original XLSX files are included.
- The publication guard passed against Git-tracked snapshots of all seven candidates. It is a limited guard, not a complete commercial secret scanner or proof of absence.
- No Git history was supplied or imported. Existing repositories/history must be reviewed separately if these files are added to them.
- No GitHub repository, hosted Actions run, release, CV change, or LinkedIn update was published.
- Contributor publication agreement was confirmed by the owner. Third-party data/service/source rights remain separate.
- Inspection used source/static review, report text extraction, report previews where available, workbook cell/object inventory, and targeted execution of the prepared copies. Original compiled Python was not decompiled, `mkcert.exe` was not executed or reverse engineered, and screenshots/embedded objects were not all individually cleared. Exclusion of originals is deliberate; no claim of exhaustive visual clearance is made.
