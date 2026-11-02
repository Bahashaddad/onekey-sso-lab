# OneKey SSO Lab

A local Flask teaching application combining password/TOTP authentication, role-restricted portal views, an OAuth-style authorization-code exercise, and a SAML-style message viewer.

**This is a simulation lab, not a production identity provider.** The SAML-style flow uses a signed local envelope and one-use ticket, not standards-compliant SAML XML signatures or an independent service provider. The displayed OTP exercise sends no SMS and is not an independent factor.

## Verified functionality

- Local registration and CLI user creation with bcrypt password hashing.
- First-time TOTP enrollment; enrolled seeds cannot be retrieved using only a password.
- TOTP seeds loaded server-side for verification, with atomic step consumption.
- Synthetic course, assignment, registration, library, and faculty views.
- Role checks for faculty access and administrator-only global event/message views.
- Local authorization codes with exact redirect matching, random state, PKCE, and one-use redemption.
- Expiring signed local library tokens and authenticated local SAML-style envelopes.
- CSRF-protected browser forms, no-store responses, disabled debug mode, and loopback request enforcement.

## Technologies and architecture

Python 3.12, Flask, Flask-WTF, Flask-Bcrypt, SQLite, PyOTP, qrcode/Pillow, ItsDangerous, Authlib, requests, and cryptography. Google OIDC support is optional and disabled by default.

```text
app.py                 Application, embedded views, database helpers, and CLI
tests/                 Targeted security regression tests
docs/                  Trust boundaries and limitations
requirements.txt       Pinned runtime dependency closure
requirements-dev.txt   Tests, critical-error linting, and dependency auditing
.env.example           Configuration names only; no usable credentials
```

All portal modules share one process and session. They demonstrate workflows rather than real university integrations. Grade-editing and cross-session-revocation controls are explicitly disabled because their original buttons did not implement those operations.

## Install and initialize

Use Python 3.12 from the repository directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
$env:APP_SECRET_KEY = (.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))")
$env:ONEKEY_LIBRARY_SECRET = (.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))")
.\.venv\Scripts\python.exe -m flask --app app init-db
.\.venv\Scripts\python.exe -m flask --app app create-user --username learner --role student
.\.venv\Scripts\python.exe app.py
```

The user command prompts for a password. No administrator or default-password accounts are seeded. Create a separate `--role admin` or `--role faculty` account only when needed for local demonstrations. Synthetic catalog fixtures include illustrative learner records; they do not create login accounts.

Open `https://127.0.0.1:5050`. The launcher generates a temporary self-signed certificate. For this explicitly local address only, the browser will show a trust warning; no certificate authority installation is required. Do not deploy this server or extend these instructions to remote services.

Visit `/mfa/setup` once to enroll a newly created account. Then sign in and submit an authenticator code to finish enrollment. The next visit to the enrollment page cannot reveal an enrolled seed.

## Configuration

| Variable | Purpose |
|---|---|
| `APP_SECRET_KEY` | Required stable, locally generated session-signing key, 32+ characters |
| `ONEKEY_LIBRARY_SECRET` | Required 32+ character secret for the demonstration token endpoint |
| `ONEKEY_DATABASE` | Optional path; defaults to `instance/onekey.db` |
| `ONEKEY_ENABLE_GOOGLE` | Set to `1` only to enable optional Google OIDC |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Optional credentials from your own development integration |

Use process environment variables. `.env.example` is a reference, not an automatically loaded configuration promise. If an optional dotenv installation is present, `.env` remains private.

For optional Google OIDC, register the exact local callback URI for the hostname you use, for example `https://127.0.0.1:5050/google/callback`. The application requires a verified provider email and will not automatically link a local account to a provider identity. Live provider configuration and authentication were not tested in this preparation; do not claim verified Google integration from the local tests.

## Demonstration

After sign-in, browse synthetic courses and the library. Start the library exercise from its authorization link. The same-process callback redeems the code through a local helper. The token endpoint also requires HTTP Basic client authentication with client ID `library-app`, the locally configured secret, `grant_type=authorization_code`, the code, the PKCE verifier, and the exact redirect URI.

The learning view's SAML-style message requires a manual Continue button. A signed, expiring local envelope and one-use ticket protect this demonstration; they are not SAML interoperability. Global packet inspection requires an administrator account.

Faculty displayed-code verification is visibly labeled a simulation. It is not evidence of SMS delivery or phishing-resistant MFA.

## Checks

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\python.exe -m pip_audit --disable-pip --no-deps -r requirements.txt
```

## Security considerations and limitations

- Use synthetic data and loopback access only. Remote requests are rejected.
- TOTP seeds remain plaintext at rest; protect or discard the local database.
- The displayed challenge is readable by the user and is not a meaningful bot defense.
- Inline styles remain for the original UI; script execution is blocked by CSP.
- The app remains a large module with embedded HTML and broad legacy exception handling. Logging is not guaranteed to record every failure.
- The protocol exercises are not independently deployed clients, full OAuth/OIDC server implementations, or SAML-compliant federation.
- No recovery-code mechanism, full session revocation, production key management, or production deployment is implemented.
- Local regression tests do not verify live Google sign-in, browser appearance, real university interoperability, or independent penetration-test coverage.

Do not publish original databases, `.env`, private keys, certificates, authentication screenshots, or packet logs. If original credentials were exposed outside trusted custody, rotate provider secrets and session keys, regenerate affected local TLS keys, and re-enroll affected MFA accounts.

## Future improvements

Extract views into templates, expand transaction and browser tests, and replace protocol simulations with vetted standards libraries and separately deployed clients if real federation becomes a goal.

## Authorship and license

Original academic contributors: Baha'a Aldeen Shaddad, Tamer Alomari, Ibrahim Al-Shishani, and Yahia Abdallah. See [NOTICE.md](NOTICE.md) for later changes and third-party scope. Original code and portfolio documentation use the [MIT license](LICENSE).
