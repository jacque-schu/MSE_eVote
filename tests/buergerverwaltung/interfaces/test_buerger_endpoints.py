import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from apps.main import app
from apps.buergerverwaltung.domain.models.buerger import Buerger

client = TestClient(app)


@pytest.fixture
def mock_registrierungs_service():
    """Mock des Registrierungsservice"""
    with patch('apps.buergerverwaltung.interfaces.rest.buerger_endpoints.registrierungs_service') as mock:
        yield mock


def test_registriere_buerger_post_erfolgreich(mock_registrierungs_service):
    """Test: POST /registrierung mit gültigem Token"""
    # Mock Service-Antwort
    buerger_response = Buerger(
        buergerID=1,
        name="Max Mustermann",
        adresse="Musterstraße 1",
        geburtsdatum="1990-01-01",
        email="max@example.com",
        authentifizierungsdaten="geheim"
    )
    mock_registrierungs_service.registriere_buerger.return_value = buerger_response

    # POST-Request mit Authorization-Header
    response = client.post(
        "/api/buergerverwaltung/registrierung",
        data={
            "name": "Max Mustermann",
            "adresse": "Musterstraße 1",
            "geburtsdatum": "1990-01-01",
            "email": "max@example.com",
            "authentifizierungsdaten": "geheim"
        },
        headers={"Authorization": "Bearer geheimer_token"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Bürger registriert"
    mock_registrierungs_service.registriere_buerger.assert_called_once()


def test_registriere_buerger_post_ohne_token(mock_registrierungs_service):
    """Test: POST /registrierung ohne Authorization-Header"""
    response = client.post(
        "/api/buergerverwaltung/registrierung",
        data={
            "name": "Max Mustermann",
            "adresse": "Musterstraße 1",
            "geburtsdatum": "1990-01-01",
            "email": "max@example.com",
            "authentifizierungsdaten": "geheim"
        }
    )

    assert response.status_code == 401
    assert "Authorization Header fehlt" in response.json()["detail"]


def test_registriere_buerger_post_ungültiger_token(mock_registrierungs_service):
    """Test: POST /registrierung mit ungültigem Token-Format"""
    response = client.post(
        "/api/buergerverwaltung/registrierung",
        data={
            "name": "Max Mustermann",
            "adresse": "Musterstraße 1",
            "geburtsdatum": "1990-01-01",
            "email": "max@example.com",
            "authentifizierungsdaten": "geheim"
        },
        headers={"Authorization": "InvalidFormat"}  # Kein "Bearer " Prefix
    )

    assert response.status_code == 401
    assert "Ungültiger Authorization Header" in response.json()["detail"]


def test_registrierung_seite_get(mock_registrierungs_service):
    """Test: GET /registrierung liefert HTML-Formular"""
    response = client.get("/registrierung")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Bürger registrieren" in response.text
