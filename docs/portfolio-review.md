# Portfolio review: OneKey SSO Lab

Prepared 2026-11-02. Original input: `onekey_https_google_project (3) (1).zip`. The owner approved separate copies and improvements, and confirmed contributor publication agreement. Originals remain unchanged. Phase 4 approval is recorded; Phase 5 changes are in this copy. Phase 6 is bounded by the checks and remaining gates below.

## 1. Actual purpose

A single-process Flask portal with synthetic learning/library/registration/faculty modules, local TOTP login, optional Google OIDC client support, and home-grown federation demonstrations.

## 2. Quality and public suitability

The original packaged broad UI functionality but mixed it with insecure authentication and protocol simulations. Debug mode was enabled, a default signing key was present, and the archive included real parseable RSA private keys, environment credentials, a database with seven users, and authentication/event records. The copy is explicitly a loopback teaching lab, not a standards-compliant IdP.

## 3. Security and evidence concerns

Severity is a qualitative project-context assessment, not a CVSS calculation. Confirmed source behavior is distinguished from unavailable evidence and potential privacy risks.

| Severity | Affected original file/area | Problem and impact | Remediation/status | Before publication? |
|---|---|---|---|---|
| Critical | app.py: login/mfa_verify | MFA seed was written to a signed, browser-readable session cookie. | Load seed server-side, add expiring pending login, conditional TOTP-step consumption. Applied and tested. | Yes; fixed in copy |
| Critical | app.py: render_template_string calls | User-derived values were interpolated into Jinja template source, enabling template-injection paths. | Return assembled HTML without Jinja evaluation; escape data insertion sites; block scripts via CSP. Targeted SSTI/XSS tests pass. | Yes; fixed targeted paths; further UI review useful |
| High | app.py: mfa_setup | Password-only retrieval of enrolled MFA seeds. | Only permit first enrollment before a verified TOTP is recorded. | Yes; fixed in copy |
| High | .env; *-key.pem; onekey_university.db | Credential-shaped environment values, three parseable private keys, user seeds and event data. | Exclude originals; rotate OAuth client secret and app signing key before reuse; regenerate TLS keys and re-enroll affected local MFA factors. Live credential validity was not tested. | Yes; originals excluded; owner rotation remains |
| High | app.py: saml_sso/moodle_acs | Unsigned XML accepted without proper signature, audience, or replay verification. | Preserve an explicitly labeled local simulation using signed expiring envelopes, session identity binding, and one-use tickets. This is not real SAML. | Yes; simulation bounded and tested |
| High | app.py: OAuth-style routes | Arbitrary redirect URI, fixed state, unsigned base64 token, weak redemption binding. | Exact redirect, random state, PKCE, authenticated token endpoint, transactional one-use codes, expiring signed local tokens. | Yes; local exercise fixed; not full OAuth server |
| High | app.py: audit/saml_viewer | Global records were visible to ordinary signed-in users. | Require administrator role. | Yes; fixed and tested |
| Medium | app.py: library_return/reg_drop/moodle_submit | Other-user book return could alter availability; repeated drops inflated seats; submission lacked enrollment validation. | Conditional ownership-bound changes, transactions, enrollment query. | Yes; applied with targeted tests |
| Medium | Launch/configuration/forms | Debug mode, known signing default, missing CSRF, predictable seeded accounts, broad interface guidance. | No default secrets or user seeds; explicit CLI users, CSRF, loopback enforcement, debug off. | Yes; applied |
| Medium | Architecture and displayed challenges | Large embedded-HTML module, plaintext seeds, broad logging exception catches, same-browser OTP/CAPTCHA. | Document as simulations; do not claim independent factors, production assurance, or complete logging. | Lab only; future refactoring recommended |

## 4. File-by-file disposition

See `docs/file-classification.csv` for every original archive entry/file and its KEEP/MODIFY/REMOVE/PRIVATE/OPTIONAL disposition. Originals containing sensitive material are not placed in the upload copy. New files are additions, not original coursework artifacts.

## 5. Complete resulting tree

The full tree is recorded in `docs/directory-tree.txt`. Runtime/cache files are excluded.

## 6. README assessment and complete replacement

Several conflicting TXT setup files referenced different ports, localhost/LAN behavior, certificate installation, and preconfigured provider values. They did not adequately distinguish SMS display, fake success buttons, unsigned XML, and real federation. A single README.md now documents verified behavior, local setup, disabled controls, and test limits.

The complete improved README is the repository's root `README.md`, rather than a second divergent copy pasted into this report.

## 7. Specific improvements and corrected code

The files in this prepared copy are the exact replacements/additions. `CHANGELOG.md` identifies behavior changes. Source PDFs, runtime data, and credential files were not rewritten in place. Do not interpret new tests or editorial additions as work performed during the original course.

## 8. Before-publication checklist

- [x] Separate copy created; original preserved.
- [x] Public README and clean directory structure provided.
- [x] Runtime data, keys, original identifiers, and unsafe original screenshots excluded.
- [x] MIT license and third-party notice supplied following contributor agreement.
- [ ] Rotate original OAuth and application signing secrets before reuse; regenerate the original TLS keypairs.
- [ ] Live Google OIDC is disabled by default and has not been tested against the provider.
- [ ] Manually review browser appearance and inspect hosted CI results.
- [ ] Keep simulation claims explicit; real federation requires vetted standards implementations.

Review `docs/verification.md` for exact executed checks and remaining limits. Hosted Actions results and manual review must not be reported as completed merely because a workflow exists.

## 9. Skills and CV wording

Python/Flask, authentication workflow analysis, role checks, PKCE/state concepts, signed local messages, database transactions, and vulnerability remediation. The supplied project does not establish standards-compliant SAML deployment, enterprise SSO integration, or real SMS delivery.

Suggested wording: “Built an academic university-portal authentication prototype and documented the limits of its OAuth/SAML-style simulations; hardened local MFA handling and added targeted security regression tests.”

## 10. Honest original score

| Dimension | Original score / 10 |
|---|---|
| Code quality | 4 |
| Security | 1 |
| Documentation | 3 |
| Organization | 3 |
| Professional presentation | 5 |
| Portfolio value | 5 |

**3.5/10 original**. Scores assess supplied evidence, not personal ability. Documentation-only artifacts are not assigned invented code/security scores. Improvements do not establish a certified security posture or guarantee a hiring outcome.

## Repository metadata

- Name: `onekey-sso-lab`
- Description: Local authentication teaching lab with TOTP, role-restricted portals, PKCE, and explicitly labeled federation simulations.
- Topics: python, flask, authentication, totp, oauth2, pkce, saml, educational-project
- Release: consider `v0.1.0` after the remaining verification and rights gates pass. Documentation/data corrections should have a changelog entry and updated version; do not retag a changed release.
- Screenshots: optional, synthetic and sanitized only. No original screenshots are cleared for public reuse.
- License: MIT for original code/documentation; third-party rights remain separate. Underlying data provenance may impose additional limits.
