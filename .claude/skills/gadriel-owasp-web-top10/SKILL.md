---
name: gadriel-owasp-web-top10
description: OWASP Web Top 10 (A01-A10, 2021) detection patterns and language-specific remediations. Auto-invoke for findings tagged `owasp-web-*` or rule IDs `CODE-W1-L3-*` (injection/auth/access-control), and when the user asks about "SQL injection", "broken access control", "XSS", or general web vulnerabilities.
---

# OWASP Web Top 10 — Detection and Remediation

This skill maps each OWASP Top 10 (2021) web application risk to concrete detection patterns Gadriel scans for, and provides Claude with language-specific remediation snippets. It activates whenever a `security` pillar finding cites a classic web vulnerability category.

## When this skill activates

- Finding IDs in `CODE-W1-L3-*` range (Layer-3 semantic + AST rules cover most web issues)
- Tags: `owasp-web-top10`, `a01`..`a10`, `sql-injection`, `xss`, `ssrf`, `xxe`, `idor`
- User phrasings: "is this query parameterized", "can the user reach this endpoint", "auth bypass", "open redirect"
- File patterns: `*.py` web frameworks (Django/Flask/FastAPI), `*.go` net/http handlers, `*.ts` Express/Next API routes, `*.rb` Rails controllers

## Core concepts

- **A01 Broken Access Control** — missing or wrong authorization checks; IDOR; forced browsing; CORS misconfig.
- **A02 Cryptographic Failures** — weak ciphers (MD5/SHA1/DES), missing TLS, hardcoded keys, IV reuse.
- **A03 Injection** — SQL, NoSQL, OS command, LDAP, XPath, template injection.
- **A04 Insecure Design** — missing rate limit, missing CSRF, business-logic flaws (negative quantities, race conditions).
- **A05 Security Misconfiguration** — debug=true in prod, default credentials, verbose error pages, missing security headers.
- **A06 Vulnerable & Outdated Components** — outdated deps with known CVEs (cross-checked against OSV).
- **A07 Identification & Auth Failures** — weak password rules, session fixation, predictable tokens, no MFA.
- **A08 Software & Data Integrity Failures** — unsigned updates, untrusted deserialization, CI pipelines without provenance.
- **A09 Security Logging & Monitoring Failures** — no audit log, sensitive data in logs, no alert on auth failure.
- **A10 Server-Side Request Forgery (SSRF)** — user-controlled URL fetched server-side without allowlist.

## Detection patterns / cheatsheet

- **A01**: handler missing `@login_required`, route accessible without `current_user.is_admin`, `/api/users/{id}` returning data when `id != current_user.id`.
- **A02**: `hashlib.md5(password)`, `crypto.createCipher('des'...)`, `RSA.new(.., e=3)`, key material in source or env-checked-in.
- **A03 SQL**: `cursor.execute(f"SELECT * FROM u WHERE id={uid}")`, `db.raw(`SELECT ${col}`)`, Sequelize `query()` with template literals.
- **A03 cmd**: `subprocess.call(user_input, shell=True)`, `exec.Command("sh", "-c", input)`, `child_process.exec(`ping ${host}`)`.
- **A04**: POST endpoint without CSRF token, no `rate_limit` middleware, money transfer without idempotency key.
- **A05**: `DEBUG = True` in `settings.py`, `app.config['ENV'] = 'development'`, missing `X-Content-Type-Options`, `Strict-Transport-Security`.
- **A06**: dependency manifest entries flagged by OSV (Gadriel L2 lockfile scan emits `CODE-W1-L2-*`).
- **A07**: `bcrypt(rounds=4)`, JWT with `alg: none` accepted, session cookie missing `Secure; HttpOnly; SameSite`.
- **A08**: `pickle.loads(user_data)`, `yaml.load(...)` without `SafeLoader`, `JSON.parse` of signed payload without signature verification.
- **A09**: log statements containing `password=` / `Authorization:` headers; no log on `401`/`403`/`500`.
- **A10**: `requests.get(user_provided_url)` without URL allowlist or DNS-rebinding protection.

## Remediation playbook

1. Replace string-interpolated SQL with parameterized queries or ORM bindings (`?`, `$1`, `:param`).
2. Centralize authz in a decorator/middleware that resolves `resource.owner_id == current_user.id`; never rely on UI-layer hiding.
3. Use a vetted password hash: argon2id (cost-tuned) or bcrypt(rounds>=12). Never roll custom crypto.
4. Add security headers via a single middleware: HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy.
5. Whitelist outbound URLs for any user-driven fetch; block RFC1918 + link-local + metadata IPs (169.254.169.254).
6. Replace `pickle`/`yaml.load` with JSON + schema validation; sign artifacts with Sigstore/cosign.
7. Add structured logs with correlation IDs; redact tokens before logging; alert on `>5` auth failures/min/IP.
8. Bump or pin vulnerable deps; document residual risk if a CVE has no fix yet.

## Language-specific quick fixes

- **Python/Django**: `User.objects.raw(...)` → use ORM filters or `params=[...]`; turn on `SECURE_*` settings; use `django-axes` for brute-force protection.
- **Python/Flask**: replace `render_template_string(user_input)` with `render_template`; install `flask-talisman` for headers.
- **Node/Express**: use `helmet`, `express-rate-limit`, `csurf`; never `eval`/`Function`; switch to prepared statements (`db.query('... WHERE id = ?', [id])`).
- **Go**: use `database/sql` with `?`/`$1` placeholders; `html/template` (not `text/template`) for HTML output; `crypto/subtle.ConstantTimeCompare` for token comparison.
- **Java/Spring**: `@PreAuthorize` annotations + method security; use parameterized JPA queries; disable `XmlInputFactory` external entities.

## References

- OWASP Top 10:2021 — https://owasp.org/Top10/
- Gadriel L3 semantic rules `CODE-W1-L3-*`
- OSV — https://osv.dev/ (used by Gadriel L2 dep scanner)
