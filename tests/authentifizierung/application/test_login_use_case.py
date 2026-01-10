import pytest
from unittest.mock import Mock, patch

from apps.authentifizierung.application.services.login_use_case import AuthApplicationService

#Einfaches Dummy-Objekt, das einen Bürger aus dem Repository nachbildet
class DummyBuerger:
    def __init__(self, email, pwd_hash, buerger_id=1, name="Max Muster"):
        # E-Mail-Adresse des Bürgers
        self.email = email
        # Gespeicherter (gehashter) Passwortwert
        self.authentifizierungsdaten = pwd_hash
        # Interne Bürger-ID
        self.buergerID = buerger_id
        # Anzeigename des Bürgers
        self.name = name

#Dummy für die Identität, die der Domain-Service normalerweise erzeugt
class DummyIdentity:
    def __init__(self, buerger_id, name):
        # ID des Bürgers in der Identität
        self.buerger_id = buerger_id
        # Name des Bürgers in der Identität
        self.name = name

#Stellt ein Mock-Repository bereit, das einen festen Dummy-Bürger zurückgibt
@pytest.fixture
def buerger_repo():
    repo = Mock()
    # Wenn lade_alle aufgerufen wird, kommt eine Liste mit genau einem Bürger zurück
    repo.lade_alle.return_value = [
        DummyBuerger(email="user@example.org", pwd_hash="hashed-pass")
    ]
    return repo

@pytest.fixture
def auth_service(buerger_repo):
    """
    Baut einen AuthApplicationService mit Mock-Domain-Service.
    - AuthService wird durch ein Mock-Objekt ersetzt.
    - Admin-Validierung und Bürger-Identität liefern kontrollierte Testdaten.
    """
    with patch(
        "apps.authentifizierung.application.services.login_use_case.AuthService"
    ) as DomainServiceMock:
        domain_service = DomainServiceMock.return_value
        # Standardmäßig sind Admin-Zugangsdaten im Test gültig
        domain_service.validate_admin_credentials.return_value = True
        # create_buerger_identity gibt eine DummyIdentity zurück
        domain_service.create_buerger_identity.return_value = DummyIdentity(
            buerger_id=1, name="Max Muster"
        )

        service = AuthApplicationService(buerger_repo=buerger_repo)
        return service


def test_login_admin_success(auth_service):
    """
    Prüft den erfolgreichen Admin-Login.
    Erwartung:
    - Token wird mit create_token erzeugt.
    - Rückgabe enthält Token, Typ 'bearer' und Rolle 'admin'.
    """
    with patch(
        "apps.authentifizierung.application.services.login_use_case.create_token",
        return_value="token123",
    ):
        result = auth_service.login_admin("admin", "secret")

    assert result["access_token"] == "token123"
    assert result["token_type"] == "bearer"
    assert result["role"] == "admin"


def test_login_admin_invalid_credentials(buerger_repo):
    """
    Prüft das Fehlverhalten beim Admin-Login mit ungültigen Zugangsdaten.
    Erwartung:
    - Domain-Service meldet ungültige Daten.
    - AuthApplicationService wirft ValueError mit passender Meldung.
    """
    with patch(
        "apps.authentifizierung.application.services.login_use_case.AuthService"
    ) as DomainServiceMock:
        domain_service = DomainServiceMock.return_value
        # Für diesen Testfall sind die Admin-Daten absichtlich ungültig
        domain_service.validate_admin_credentials.return_value = False

        service = AuthApplicationService(buerger_repo=buerger_repo)

        with pytest.raises(ValueError, match="Ungültige Admin-Daten"):
            service.login_admin("admin", "wrong")


def test_login_buerger_success(auth_service, buerger_repo):
    """
    Prüft den erfolgreichen Bürger-Login.
    Erwartung:
    - Passwortprüfung ist erfolgreich.
    - Token wird erzeugt.
    - Rückgabe enthält Token, Typ 'bearer', Rolle 'buerger' und den Namen.
    - Das Repository wurde verwendet, um Bürgerdaten zu laden."""

    with patch(
        "apps.authentifizierung.application.services.login_use_case.verify_password",
        return_value=True,
    ), patch(
        "apps.authentifizierung.application.services.login_use_case.create_token",
        return_value="token456",
    ):
        result = auth_service.login_buerger("user@example.org", "geheim")

    assert result["access_token"] == "token456"
    assert result["token_type"] == "bearer"
    assert result["role"] == "buerger"
    assert result["name"] == "Max Muster"
    # Sicherstellen, dass das Repository wirklich abgefragt wurde
    buerger_repo.lade_alle.assert_called_once()


def test_login_buerger_wrong_password(auth_service):
    """
    Prüft das Verhalten beim Bürger-Login mit falschem Passwort.
    Erwartung:
    - verify_password liefert False.
    - AuthApplicationService wirft ValueError mit Meldung 'Falsches Passwort'."""

    with patch(
        "apps.authentifizierung.application.services.login_use_case.verify_password",
        return_value=False,
    ):
        with pytest.raises(ValueError, match="Falsches Passwort"):
            auth_service.login_buerger("user@example.org", "falsch")
