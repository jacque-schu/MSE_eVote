import pytest
from fastapi import HTTPException
from starlette.requests import Request
from starlette.datastructures import Headers
import jwt

from apps.abstimmungsmanagement.infrastructure.auth.abstimmung_auth import require_login
from apps.shared.aspects import auth_aspect

# diese Testdatei prüft das Verhalten der Auth‑Funktion require_login entlang aller wichtiger Pfade

# erzeugt künstliche HTTP‑Anfrage und prüft Verhalten mit oder ohne Cookie
def make_request_with_cookie(token: str | None):
    headers = {}
    if token is not None:
        headers["cookie"] = f"auth_token={token}"

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/dummy",
        "headers": Headers(headers).raw,
    }

    request = Request(scope)
    return request

def test_require_login_no_token(monkeypatch):
    monkeypatch.setattr(auth_aspect, "is_token_valid", lambda token: False)

    request = make_request_with_cookie(None)

    with pytest.raises(HTTPException) as exc:
        require_login(request)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Login fehlt"

#prüft, was require_login macht, wenn gar kein Token im Cookie steckt
def test_require_login_invalid_token(monkeypatch):
    # Token vorhanden, aber ungültig -> ebenfalls 401
    monkeypatch.setattr(auth_aspect, "is_token_valid", lambda token: False)

    request = make_request_with_cookie("invalid-token")

    with pytest.raises(HTTPException) as exc:
        require_login(request)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Ungültiger Token"


def test_require_login_valid_buerger(monkeypatch):
    # 1) Gültiger Token
    monkeypatch.setattr(auth_aspect, "is_token_valid", lambda token: True)

    # 2) jwt.decode stubben, damit kein echter Schlüssel nötig ist
    def fake_decode(token, key, algorithms):
        return {"sub": "buerger_123"}

    monkeypatch.setattr(jwt, "decode", fake_decode)

    request = make_request_with_cookie("dummy-token")

    result = require_login(request)

    assert result["user_id"] == "buerger_123"
    assert result["role"] == "buerger"

#prüft den happy path für einen eingeloggten Bürger
def test_require_login_valid_admin_exact(monkeypatch):
    monkeypatch.setattr(auth_aspect, "is_token_valid", lambda token: True)

    def fake_decode(token, key, algorithms):
        return {"sub": "admin"}

    monkeypatch.setattr(jwt, "decode", fake_decode)

    request = make_request_with_cookie("dummy-token")

    result = require_login(request)

    assert result["user_id"] == "admin"
    assert result["role"] == "admin"

# prüft, ob require_login einen Benutzer mit einer Admin‑ID mit Präfix korrekt als Admin erkennt
def test_require_login_valid_admin_prefix(monkeypatch):
    monkeypatch.setattr(auth_aspect, "is_token_valid", lambda token: True)

    def fake_decode(token, key, algorithms):
        return {"sub": "admin_mareike"}

    monkeypatch.setattr(jwt, "decode", fake_decode)

    request = make_request_with_cookie("dummy-token")

    result = require_login(request)

    assert result["user_id"] == "admin_mareike"
    assert result["role"] == "admin"
