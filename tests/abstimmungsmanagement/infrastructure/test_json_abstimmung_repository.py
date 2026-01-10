import json
from datetime import date, timedelta

import pytest

from apps.abstimmungsmanagement.infrastructure.repositories.json_abstimmung_repository import JsonAbstimmungRepository
from apps.abstimmungsmanagement.domain.models.abstimmung import Abstimmung, Abstimmungsstatus

#Die Testdatei prüft, ob das JsonAbstimmungRepository korrekt mit der JSON‑Datei arbeitet: richtig lädt, speichert, nach IDs sucht und nach Status filtert.

#prüft Format einer gültigen Abstimmung - so werden Format‑/Validierungsfehler vermieden
def make_abstimmung_dict(
    abstimmungs_id: int,
    status: Abstimmungsstatus,
    start_datum: date,
    end_datum: date,
) -> dict:
    """Erzeugt ein gültiges Abstimmungs-Dict passend zu deinem Pydantic-Modell."""
    abstimmung = Abstimmung(
        abstimmungsID=abstimmungs_id,
        titel=f"Abstimmung {abstimmungs_id}",
        beschreibung="Gültige Testbeschreibung",
        startDatum=start_datum,
        endDatum=end_datum,
        teilnehmerliste=[],
        stimmen=[],
        status=status,
    )
    return abstimmung.model_dump(mode="json")

#prüft Status geschlossen und offen
def test_load_closes_expired_open_polls_and_keeps_others(tmp_path):
    file_path = tmp_path / "abstimmungen.json"

    heute = date.today()
    # Abgelaufen: beide Daten in der Vergangenheit, endDatum >= startDatum
    start_alt = heute - timedelta(days=10)
    end_alt = heute - timedelta(days=1)
    # Noch laufend: beide Daten in der Zukunft
    start_zukunft = heute + timedelta(days=1)
    end_zukunft = heute + timedelta(days=10)

    data = [
        # Offen, aber in der Vergangenheit -> soll auf GESCHLOSSEN gesetzt werden
        make_abstimmung_dict(
            abstimmungs_id=1,
            status=Abstimmungsstatus.OFFEN,
            start_datum=start_alt,
            end_datum=end_alt,
        ),
        # Offen und in der Zukunft -> bleibt OFFEN
        make_abstimmung_dict(
            abstimmungs_id=2,
            status=Abstimmungsstatus.OFFEN,
            start_datum=start_zukunft,
            end_datum=end_zukunft,
        ),
    ]
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    repo = JsonAbstimmungRepository(str(file_path))

    a1 = repo.get(1)
    a2 = repo.get(2)

    assert a1.status == Abstimmungsstatus.GESCHLOSSEN
    assert a2.status == Abstimmungsstatus.OFFEN

#prüft Speicherung Abstimmung in der JSON‑Datei auf der Festplatte
def test_save_persists_changes(tmp_path):
    file_path = tmp_path / "abstimmungen.json"
    file_path.write_text("[]", encoding="utf-8")

    repo = JsonAbstimmungRepository(str(file_path))

    heute = date.today()
    abstimmung = Abstimmung(
        abstimmungsID=1,
        titel="Test",
        beschreibung="Gültige Testbeschreibung",
        startDatum=heute,
        endDatum=heute,
        status=Abstimmungsstatus.OFFEN,
        teilnehmerliste=[],
        stimmen=[],
    )

    repo.save(abstimmung)

    raw = json.loads(file_path.read_text(encoding="utf-8"))
    assert len(raw) == 1
    assert raw[0]["abstimmungsID"] == 1

#prüft, ob bei fehlender Abstimmungs-ID ein KeyError geworfen wird
def test_get_raises_keyerror_for_unknown_id(tmp_path):
    file_path = tmp_path / "abstimmungen.json"
    file_path.write_text("[]", encoding="utf-8")

    repo = JsonAbstimmungRepository(str(file_path))

    with pytest.raises(KeyError):
        repo.get(999)

#prüft, ob list_all() alle vorhandenen Abstimmungen lädt und find_by_status() jeweils nur die Abstimmungen mit dem gewünschten Status liefert
def test_list_all_and_find_by_status(tmp_path):
    file_path = tmp_path / "abstimmungen.json"

    heute = date.today()
    start1 = heute
    end1 = heute + timedelta(days=5)

    start2 = heute - timedelta(days=10)
    end2 = heute - timedelta(days=1)

    data = [
        make_abstimmung_dict(
            abstimmungs_id=1,
            status=Abstimmungsstatus.OFFEN,
            start_datum=start1,
            end_datum=end1,
        ),
        make_abstimmung_dict(
            abstimmungs_id=2,
            status=Abstimmungsstatus.GESCHLOSSEN,
            start_datum=start2,
            end_datum=end2,
        ),
    ]
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    repo = JsonAbstimmungRepository(str(file_path))

    alle = repo.list_all()
    assert {a.abstimmungsID for a in alle} == {1, 2}

    offen = repo.find_by_status(Abstimmungsstatus.OFFEN)
    geschlossen = repo.find_by_status(Abstimmungsstatus.GESCHLOSSEN)

    assert {a.abstimmungsID for a in offen} == {1}
    assert {a.abstimmungsID for a in geschlossen} == {2}
