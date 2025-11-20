import pytest
from datetime import timedelta
from unittest.mock import MagicMock

from apps.buergerverwaltung.services.authentifizierungs_service import (
    AuthentifizierungsService,
    pwd_context,
)
from apps.buergerverwaltung.domain.entities.buerger import Buerger  # Importiere das Buerger-Modell

@pytest.fixture
def auth_service():
    return AuthentifizierungsService()

def test_hash_and_verify_password(auth_service):
    password = "geheimes_passwort"
    # Debug-Ausgabe vor dem Hashen
    print("PW:", repr(password), "LEN:", len(password), len(password.encode("utf-8")))
    assert len(password.encode("utf-8")) < 72
    hashed = auth_service.hash_password(password)

    assert hashed != password
    assert pwd_context.verify(password, hashed)

def hash_password(self, password: str) -> str:
    bs = password.encode("utf-8")
    if len(bs) > 72:
        print("ZU LANG:", repr(password), len(bs))  # <-- niemals im Produktivcode, aber perfekt zum Debuggen!
        raise ValueError(f"Password too long for bcrypt: {len(bs)} bytes\n{repr(password)}")
    return pwd_context.hash(password)


def test_create_access_token_default_expiry(auth_service):
    data = {"sub": "testuser"}
    token = auth_service.create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 0

def test_create_access_token_custom_expiry(auth_service):
    data = {"sub": "testuser"}
    token = auth_service.create_access_token(
        data, expires_delta=timedelta(minutes=5)
    )
    assert isinstance(token, str)
    assert len(token) > 0

def test_authenticate_user_success(auth_service):
    # Passwort < 72 Zeichen!
    plain_pw = "mein_passwort"
    assert len(plain_pw.encode("utf-8")) < 72
    hashed_pw = pwd_context.hash(plain_pw)

    fake_user = Buerger()
    fake_user.email = "test@example.com"
    fake_user.authentifizierungsdaten = hashed_pw

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = fake_user

    user = auth_service.authenticate_user()
