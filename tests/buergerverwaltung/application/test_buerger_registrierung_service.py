# test_buerger_registrierung_service.py
import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException
from apps.buergerverwaltung.application.services.buerger_registrierung_service import BuergerRegistrierungService
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository
from apps.buergerverwaltung.domain.models.buerger import Buerger

@pytest.fixture
def mock_repo():
    repo = Mock(spec=IBuergerRepository)
    repo.naechste_buerger_id.return_value = 42
    repo.finde_nach_email.return_value = None  # Kein Duplikat
    return repo

@pytest.fixture
def service(mock_repo):
    return BuergerRegistrierungService(mock_repo)

def test_registriere_erfolgreich(service, mock_repo):
    """Erfolgreiche Registrierung"""
    result = service.registriere(
        "Anna", "Schmidt", "Musterstraße 1", 
        "1990-01-01", "anna@test.de", "passwort123"
    )
    
    assert result == {"message": "Bürger 'Anna Schmidt' erfolgreich registriert"}
    mock_repo.finde_nach_email.assert_called_once_with("anna@test.de")
    mock_repo.naechste_buerger_id.assert_called_once()
    mock_repo.fuege_hinzu.assert_called_once()
    
    # Buerger-Objekt prüfen
    buerger_arg = mock_repo.fuege_hinzu.call_args.args[0]
    assert buerger_arg.buergerID == 42
    assert buerger_arg.name == "Anna Schmidt"
    assert buerger_arg.email == "anna@test.de"

def test_registriere_email_duplikat(service, mock_repo):
    """E-Mail bereits registriert"""
    mock_repo.finde_nach_email.return_value = MagicMock(buergerID=99)
    
    with pytest.raises(HTTPException) as exc_info:
        service.registriere("Max", "Mustermann", "Adresse", 
                           "1985-05-15", "max@test.de", "pw456")
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "E-Mail bereits registriert"
    mock_repo.naechste_buerger_id.assert_not_called()
    mock_repo.fuege_hinzu.assert_not_called()

def test_registriere_namen_strip(service, mock_repo):
    """Leerzeichen werden gestrippt"""
    result = service.registriere("  Anna  ", "  Schmidt  ", "Adresse", 
                                "1990-01-01", "anna@test.de", "pw")
    assert result["message"] == "Bürger 'Anna Schmidt' erfolgreich registriert"
