import importlib.util
from pathlib import Path
import secrets
import pytest


@pytest.fixture
def lab(monkeypatch, tmp_path):
    monkeypatch.setenv("APP_SECRET_KEY", secrets.token_hex(32))
    monkeypatch.setenv("ONEKEY_LIBRARY_SECRET", secrets.token_hex(32))
    monkeypatch.setenv("ONEKEY_DATABASE", str(tmp_path / "onekey.db"))
    monkeypatch.delenv("ONEKEY_ENABLE_GOOGLE", raising=False)
    spec = importlib.util.spec_from_file_location(
        "onekey_under_test", Path(__file__).resolve().parents[1] / "app.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with module.app.app_context():
        module.init_db()
    conn = module.get_db()
    conn.execute(
        "INSERT INTO users (username,email,password_hash,mfa_secret,role,auth_provider,mfa_enrolled,created_at) VALUES (?,?,?,?,?,'local',1,?)",
        (
            "student1",
            "student1@example.test",
            module.bcrypt.generate_password_hash("synthetic-local-password").decode(),
            module.pyotp.random_base32(),
            "student",
                module.utc_now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()
    return module


@pytest.fixture
def client(lab):
    c = lab.app.test_client()
    with c.session_transaction() as session:
        session["user"] = "student1"
        session["email"] = "student1@example.test"
        session["role"] = "student"
    return c
