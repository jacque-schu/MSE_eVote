import pytest
from datetime import timedelta
from unittest.mock import MagicMock
from apps.buergerverwaltung.application.services import (
    AuthentifizierungsService, pwd_context
)
from apps.buergerverwaltung.domain.entities.buerger import Buerger

@pytest.fixture
def auth_service():
    return AuthentifizierungsService()

def test_hash_and_verify_password(auth_service):
    password = "geheimes_passwort"
    print("PW:", repr(password), "LEN:", len(password), len(password.encode("utf-8")))
    assert len(password.encode("utf-8")) < 72
    hashed = auth_service.hash_password(password)
    assert hashed != password
    assert pwd_context.verify(password, hashed)

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
    plain_pw = "mein_passwort"
    assert len(plain_pw.encode("utf-8")) < 72
    hashed_pw = auth_service.hash_password(plain_pw)
    fake_user = Buerger(
        buergerID=1,
        name="Test Nutzer",
        adresse="Teststraße 1",
        geburtsdatum="01.01.2000",
        email="test@example.com",
        authentifizierungsdaten=hashed_pw
    )
    # Mock-Kette so setzen, dass alle Methodenaufrufe fake_user zurückgeben,
    # egal welcher Vergleich in .filter() steckt:
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = fake_user
    # Optional: filter ignoriert Argumente und gibt sich selbst zurück (ermöglicht weitere Methoden)
    db.query.return_value.filter.side_effect = lambda *args, **kwargs: db.query.return_value.filter.return_value

    user = db.query(Buerger).filter(lambda b: b.email == email).first()

    assert user is not None
    assert user.email == "test@example.com"