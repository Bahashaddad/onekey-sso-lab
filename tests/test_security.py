import re
from urllib.parse import urlparse, parse_qs

BASE = "https://localhost:5050"


def test_no_automatic_privileged_users(lab):
    conn = lab.get_db()
    assert (
        conn.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0] == 0
    )
    conn.close()


def test_enrolled_seed_cannot_be_retrieved(lab):
    c = lab.app.test_client()
    assert (
        c.post(
            "/mfa/setup",
            base_url=BASE,
            data={"username": "student1", "password": "synthetic-local-password"},
        ).status_code
        == 403
    )


def test_seed_not_in_browser_session(lab):
    c = lab.app.test_client()
    c.get("/login", base_url=BASE)
    with c.session_transaction() as session:
        captcha = session["captcha_answer"]
    response = c.post(
        "/login",
        base_url=BASE,
        data={
            "username": "student1",
            "password": "synthetic-local-password",
            "captcha": captcha,
        },
    )
    assert response.status_code == 302
    with c.session_transaction() as session:
        assert "temp_secret" not in session
        assert session["temp_user"] == "student1"


def test_totp_single_use(lab):
    assert lab.consume_step("student1", 1234)
    assert not lab.consume_step("student1", 1234)


def test_mfa_failures_lock_account(lab):
    import time

    c = lab.app.test_client()
    with c.session_transaction() as session:
        session["temp_user"] = "student1"
        session["temp_email"] = "student1@example.test"
        session["temp_role"] = "student"
        session["temp_expires"] = time.time() + 300
    for _ in range(5):
        assert (
            c.post(
                "/mfa_verify", base_url=BASE, data={"mfa_code": "invalid"}
            ).status_code
            == 200
        )
    assert lab.check_lock("student1")


def test_ssti_not_evaluated_and_search_escaped(lab, client):
    with lab.app.test_request_context():
        assert b"{{7*7}}" in lab.render_html("<body>{{7*7}}</body>").data
    with client.session_transaction() as session:
        session["library_token"] = lab.signer.dumps(
            {"sub": "student1", "aud": "library-app"}, salt="library-access"
        )
    response = client.get(
        "/library/home",
        base_url=BASE,
        query_string={"q": '"><script>alert(1)</script>{{7*7}}'},
    )
    assert response.status_code == 200
    assert b"<script>alert(1)</script>" not in response.data
    assert b"&lt;script&gt;" in response.data


def test_global_logs_admin_only(client):
    for path in ["/audit", "/saml/viewer"]:
        assert client.get(path, base_url=BASE).status_code == 403


def test_saml_simulation_rejects_forgery_and_replay(lab, client):
    assert (
        client.post(
            "/moodle/acs", base_url=BASE, data={"SAMLResponse": "forged"}
        ).status_code
        == 400
    )
    response = client.get("/saml/sso", base_url=BASE)
    token = (
        re.search(rb'name="SAMLResponse" value="([^"]+)"', response.data)
        .group(1)
        .decode()
    )
    assert (
        client.post(
            "/moodle/acs", base_url=BASE, data={"SAMLResponse": token}
        ).status_code
        == 302
    )
    assert (
        client.post(
            "/moodle/acs", base_url=BASE, data={"SAMLResponse": token}
        ).status_code
        == 403
    )


def test_oauth_redirect_pkce_state_and_code_reuse(lab, client):
    assert (
        client.get(
            "/oauth/authorize",
            base_url=BASE,
            query_string={
                "client_id": "library-app",
                "response_type": "code",
                "redirect_uri": "https://example.invalid/steal",
            },
        ).status_code
        == 400
    )
    start = client.get("/library/start", base_url=BASE)
    authorized = client.get(start.location, base_url=BASE)
    assert authorized.status_code == 302
    callback = client.get(authorized.location, base_url=BASE)
    assert callback.status_code == 302 and callback.location.endswith("/library/home")
    assert client.get(authorized.location, base_url=BASE).status_code == 400
    assert (
        client.post(
            "/oauth/token", base_url=BASE, data={"code": "anything"}
        ).status_code
        == 401
    )


def test_other_users_book_return_and_repeated_drop_do_not_change_counts(lab, client):
    with client.session_transaction() as session:
        session["library_token"] = lab.signer.dumps(
            {"sub": "student1", "aud": "library-app"}, salt="library-access"
        )
    conn = lab.get_db()
    conn.execute("UPDATE library_books SET available=0 WHERE id=1")
    conn.commit()
    conn.close()
    client.post("/library/return/1", base_url=BASE)
    conn = lab.get_db()
    assert (
        conn.execute("SELECT available FROM library_books WHERE id=1").fetchone()[0]
        == 0
    )
    before = conn.execute(
        "SELECT seats_available FROM registration_courses WHERE id=1"
    ).fetchone()[0]
    conn.close()
    client.post("/registration/drop/1", base_url=BASE)
    client.post("/registration/drop/1", base_url=BASE)
    conn = lab.get_db()
    assert (
        conn.execute(
            "SELECT seats_available FROM registration_courses WHERE id=1"
        ).fetchone()[0]
        == before
    )
    conn.close()


def test_csrf_loopback_and_session_headers(lab, client):
    lab.app.config["WTF_CSRF_ENABLED"] = True
    assert client.post("/register", base_url=BASE, data={}).status_code == 400
    assert (
        client.get(
            "/dashboard",
            base_url=BASE,
            environ_overrides={"REMOTE_ADDR": "203.0.113.5"},
        ).status_code
        == 403
    )
    response = client.get("/dashboard", base_url=BASE)
    assert response.headers["Cache-Control"] == "no-store"
    assert "script-src 'none'" in response.headers["Content-Security-Policy"]
    assert client.get("/logout", base_url=BASE).status_code == 405
