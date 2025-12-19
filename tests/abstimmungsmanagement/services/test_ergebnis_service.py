import pytest
from unittest.mock import Mock
from apps.abstimmungsmanagement.domain.models.abstimmung import Abstimmung
from apps.abstimmungsmanagement.domain.models.ergebnis import Optionen, Ergebnis
from apps.abstimmungsmanagement.infrastructure.repositories.json_abstimmung_repository import JsonAbstimmungRepository
from apps.abstimmungsmanagement.application.services.ergebnis_service import ErgebnisService


@pytest.fixture
def mock_repository():
    return Mock(spec=JsonAbstimmungRepository)

@pytest.fixture
def abstimmung_mit_stimmen():
    # Erstelle eine Abstimmung mit Stimmen
    # WICHTIG: stimme.option ist hier direkt ein Enum (Optionen),
    # damit option_abstimmung.name im Service funktioniert.
    abstimmung = Mock(spec=Abstimmung)
    abstimmung.stimmen = [
        Mock(option=Optionen.JA),
        Mock(option=Optionen.JA),
        Mock(option=Optionen.NEIN),
        Mock(option=Optionen.ENTHALTUNG),
    ]
    return abstimmung

def test_hole_ergebnis_fuer_abstimmung_gueltig(mock_repository, abstimmung_mit_stimmen):
    mock_repository.get.return_value = abstimmung_mit_stimmen
    service = ErgebnisService(mock_repository)

    ergebnis = service.hole_ergebnis_fuer_abstimmung(1)

    assert isinstance(ergebnis, Ergebnis)
    assert ergebnis.ergebnisID == 1
    assert ergebnis.abstimmungsID == 1
    # 3 Optionen: JA, NEIN, ENTHALTUNG
    assert len(ergebnis.einzelwerte) == 3
    assert ergebnis.get_stimmen_fuer_option(Optionen.JA) == 2
    assert ergebnis.get_stimmen_fuer_option(Optionen.NEIN) == 1
    assert ergebnis.get_stimmen_fuer_option(Optionen.ENTHALTUNG) == 1

def test_hole_ergebnis_fuer_abstimmung_ohne_stimmen(mock_repository):
    abstimmung = Mock(spec=Abstimmung)
    abstimmung.stimmen = []
    mock_repository.get.return_value = abstimmung
    service = ErgebnisService(mock_repository)

    ergebnis = service.hole_ergebnis_fuer_abstimmung(1)

    assert isinstance(ergebnis, Ergebnis)
    assert ergebnis.get_stimmen_fuer_option(Optionen.JA) == 0
    assert ergebnis.get_stimmen_fuer_option(Optionen.NEIN) == 0
    assert ergebnis.get_stimmen_fuer_option(Optionen.ENTHALTUNG) == 0

def test_hole_ergebnis_fuer_abstimmung_repository_error(mock_repository):
    mock_repository.get.side_effect = Exception("Repository error")
    service = ErgebnisService(mock_repository)

    with pytest.raises(Exception, match="Repository error"):
        service.hole_ergebnis_fuer_abstimmung(1)

def test_hole_ergebnis_details_fuer_abstimmung(mock_repository, abstimmung_mit_stimmen):
    mock_repository.get.return_value = abstimmung_mit_stimmen
    service = ErgebnisService(mock_repository)

    details = service.hole_ergebnis_details_fuer_abstimmung(1)

    assert isinstance(details, list)
    assert len(details) == 3

    assert any(d["Option"] == "Ja" and d["Stimmen"] == 2 for d in details)
    assert any(d["Option"] == "Nein" and d["Stimmen"] == 1 for d in details)
    assert any(d["Option"] == "Enthaltung" and d["Stimmen"] == 1 for d in details)

def test_hole_ergebnis_fuer_abstimmung_aggregiert_stimmen_nach_optionen(mock_repository):
    # Arrange: Eine Abstimmung mit 4 Stimmen (2x JA, 1x NEIN, 1x ENTHALTUNG)
    abstimmung = Mock(spec=Abstimmung)
    abstimmung.id = 42
    abstimmung.stimmen = [
        Mock(option=Optionen.JA),
        Mock(option=Optionen.JA),
        Mock(option=Optionen.NEIN),
        Mock(option=Optionen.ENTHALTUNG),
    ]
    mock_repository.get.return_value = abstimmung

    service = ErgebnisService(mock_repository)

    # Act
    ergebnis = service.hole_ergebnis_fuer_abstimmung(42)

    # Assert: Aggregation und IDs stimmen
    assert isinstance(ergebnis, Ergebnis)
    assert ergebnis.ergebnisID == 42
    assert ergebnis.abstimmungsID == 42

    assert ergebnis.get_stimmen_fuer_option(Optionen.JA) == 2
    assert ergebnis.get_stimmen_fuer_option(Optionen.NEIN) == 1
    assert ergebnis.get_stimmen_fuer_option(Optionen.ENTHALTUNG) == 1
