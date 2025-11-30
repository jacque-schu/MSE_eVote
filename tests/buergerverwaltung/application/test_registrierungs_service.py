import pytest
from unittest.mock import MagicMock
from apps.buergerverwaltung.domain.models.buerger import Buerger
from apps.buergerverwaltung.application.services.registrierungs_service import Registrierungsservice
from pydantic import ValidationError
from datetime import date


def test_registriere_buerger_erfolgreich():
    # Mock Repository
    mock_repo = MagicMock()
    mock_repo.lade_alle.return_value = []  # keine bestehenden Bürger
    mock_repo.fuege_hinzu.return_value = None

    service = Registrierungsservice(mock_repo)
    neuer_buerger = Buerger(
        buergerID=1,
        name="Max Mustermann",
        adresse="Musterstraße 1",
        geburtsdatum=date(1990, 1, 1),
        email="max@mustermann.de",
        authentifizierungsdaten="passwort"
    )

    result = service.registriere_buerger(neuer_buerger)

    mock_repo.lade_alle.assert_called_once()
    mock_repo.fuege_hinzu.assert_called_once_with(neuer_buerger)
    assert result == neuer_buerger


def test_registriere_buerger_bereits_vorhanden():
    # Mock Bürger mit gleicher Email
    bestehender_buerger = Buerger(
        buergerID=2,
        name="Anna Beispiel",
        adresse="Beispielstraße 2",
        geburtsdatum=date(1985, 5, 5),
        email="max@mustermann.de",
        authentifizierungsdaten="geheim"
    )
    mock_repo = MagicMock()
    mock_repo.lade_alle.return_value = [bestehender_buerger]

    service = Registrierungsservice(mock_repo)
    neuer_buerger = Buerger(
        buergerID=3,
        name="Anderer Nutzer",
        adresse="Andere Straße 3",
        geburtsdatum=date(1992, 2, 2),
        email="max@mustermann.de",  # gleiche Email wie vorhanden
        authentifizierungsdaten="passwort"
    )

    with pytest.raises(ValueError) as exc_info:
        service.registriere_buerger(neuer_buerger)

    assert "existiert bereits" in str(exc_info.value)
    mock_repo.lade_alle.assert_called_once()
    mock_repo.fuege_hinzu.assert_not_called()
