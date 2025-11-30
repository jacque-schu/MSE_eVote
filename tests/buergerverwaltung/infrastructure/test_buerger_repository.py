import pytest
from unittest.mock import mock_open, patch, MagicMock
from datetime import date
import json
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository
from apps.buergerverwaltung.domain.models.buerger import Buerger


@pytest.fixture
def example_buerger_data():
    return [
        {
            "buergerID": 1,
            "name": "Max Mustermann",
            "adresse": "Musterstraße 1",
            "geburtsdatum": "1990-01-01",
            "email": "max@mustermann.de",
            "authentifizierungsdaten": "secret"
        }
    ]


def test_lade_alle_erfolgreich(example_buerger_data):
    mock_file_data = json.dumps(example_buerger_data)

    with patch("builtins.open", mock_open(read_data=mock_file_data)):
        with patch.object(BuergerRepository, "_stelle_verzeichnis_sicher", return_value=None):
            repo = BuergerRepository("fake_path.json")
            alle_buerger = repo.lade_alle()

            assert len(alle_buerger) == 1
            assert alle_buerger[0].name == "Max Mustermann"
            assert isinstance(alle_buerger[0].geburtsdatum, date)


def test_lade_alle_datei_nicht_gefunden():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch.object(BuergerRepository, "_stelle_verzeichnis_sicher", return_value=None):
            repo = BuergerRepository("fake_path.json")
            alle_buerger = repo.lade_alle()
            assert alle_buerger == []


def test_lade_alle_json_decode_error_resettet_datei():
    mock_open_obj = mock_open()
    mock_open_obj.side_effect = [json.JSONDecodeError("msg", "doc", 0), mock_open().return_value]

    with patch("builtins.open", mock_open_obj):
        with patch.object(BuergerRepository, "_stelle_verzeichnis_sicher", return_value=None):
            repo = BuergerRepository("fake_path.json")
            # patch speichere_alle, um tatsächlich kein IO zu machen
            with patch.object(repo, "speichere_alle") as mock_speichere:
                alle_buerger = repo.lade_alle()
                mock_speichere.assert_called_once_with([])
                assert alle_buerger == []


def test_speichere_alle_schreibt_datei(example_buerger_data):
    buerger_objekte = [Buerger(**b) for b in example_buerger_data]
    m = mock_open()
    with patch("builtins.open", m):
        with patch.object(BuergerRepository, "_stelle_verzeichnis_sicher", return_value=None):
            repo = BuergerRepository("fake_path.json")
            repo.speichere_alle(buerger_objekte)
            m.assert_called_once_with("fake_path.json", "w", encoding="utf-8")
            handle = m()
            # Prüfe, dass JSON geschrieben wurde
            written = "".join(call.args[0] for call in handle.write.mock_calls)
            assert "Max Mustermann" in written


def test_fuege_hinzu_ruft_alle_folgt_von_speichern_auf(example_buerger_data):
    neuer_buerger = Buerger(
        buergerID=2,
        name="Anna Beispiel",
        adresse="Beispielstraße 2",
        geburtsdatum="1985-05-05",
        email="anna@beispiel.de",
        authentifizierungsdaten="geheim"
    )
    m = mock_open(read_data=json.dumps(example_buerger_data))
    with patch("builtins.open", m):
        with patch.object(BuergerRepository, "_stelle_verzeichnis_sicher", return_value=None):
            repo = BuergerRepository("fake_path.json")
            with patch.object(repo, "speichere_alle") as mock_speichere:
                repo.fuege_hinzu(neuer_buerger)
                mock_speichere.assert_called_once()
