import pytest
from pydantic import ValidationError
from abstimmung import Abstimmung, Stimme, Stimmoption, Abstimmungsstatus
from datetime import date, timedelta

def _valid_abstimmung(**overrides):
    base = dict(
        abstimmungsID=1,
        titel="Kommunalwahl 2026",
        beschreibung="Wahl des Stadtrats",
        startDatum=date.today(),
        endDatum=date.today() + timedelta(days=7),
        teilnehmerliste=[1, 2, 3],
        stimmen=[],
    )
    base.update(overrides)
    return base

# Titel-Tests
@pytest.mark.parametrize("titel, valid", [
    ("Kommunalwahl", True),          # Happy Path
    ("  Wahl  ", True),              # Edge Case: Trim
    ("AB", False),                   # Negativ: zu kurz
    ("   ", False),                  # Negativ: leer nach Trim
])
def test_titel_validation(titel, valid):
    data = _valid_abstimmung(titel=titel)
    if valid:
        a = Abstimmung(**data)
        assert a.titel == titel.strip()
    else:
        with pytest.raises(ValidationError):
            Abstimmung(**data)

# Beschreibung-Tests
@pytest.mark.parametrize("beschreibung, valid", [
    ("Kurzbeschreibung", True),
    ("   ausreichend lang   ", True),
    ("abcd", False),                 # Negativ: < 5
    ("  ", False),
])
def test_beschreibung_validation(beschreibung, valid):
    data = _valid_abstimmung(beschreibung=beschreibung)
    if valid:
        a = Abstimmung(**data)
        assert a.beschreibung == beschreibung.strip()
    else:
        with pytest.raises(ValidationError):
            Abstimmung(**data)

# Datums-Validierung: endDatum >= startDatum
def test_date_consistency_valid():
    a = Abstimmung(**_valid_abstimmung(
        startDatum=date.today(),
        endDatum=date.today() + timedelta(days=1)
    ))
    assert a.endDatum >= a.startDatum

def test_date_consistency_invalid():
    with pytest.raises(ValidationError):
        Abstimmung(**_valid_abstimmung(
            startDatum=date.today(),
            endDatum=date.today() - timedelta(days=1)
        ))

# Extra-Felder verboten
def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        Abstimmung(**_valid_abstimmung(unbekannt="x"))

# Stimmen/Optionen
@pytest.mark.parametrize("opt, valid", [
    (Stimmoption.JA, True),
    (Stimmoption.NEIN, True),
    (Stimmoption.ENTHALTUNG, True),
    ("MAYBE", False),                # Negativ: ungültige Option
])
def test_stimme_option_validation(opt, valid):
    if valid:
        s = Stimme(buergerId=1, option=opt, zeitpunkt=date.today())
        assert s.option == opt
    else:
        with pytest.raises(ValidationError):
            Stimme(buergerId=1, option=opt, zeitpunkt=date.today())

# Statuswechsel: offen -> geschlossen
def test_status_transitions_offen_to_geschlossen():
    a = Abstimmung(**_valid_abstimmung())
    assert a.status == Abstimmungsstatus.OFFEN
    a.starten()
    a.beenden()
    assert a.status == Abstimmungsstatus.GESCHLOSSEN

# Ungültiger Statuswechsel: beenden aus geschlossen
def test_invalid_status_transition_beenden_twice():
    a = Abstimmung(**_valid_abstimmung())
    a.beenden()
    with pytest.raises(ValueError):
        a.beenden()

# validate_assignment: nachträgliche Updates validiert
def test_validate_assignment_on_update_dates():
    a = Abstimmung(**_valid_abstimmung())
    with pytest.raises(ValidationError):
        # endDatum vor startDatum -> verletzt Model-Validator
        a.endDatum = a.startDatum - timedelta(days=1)

def test_aktualisieren_valid_and_invalid():
    a = Abstimmung(**_valid_abstimmung())
    a.aktualisieren(titel="Neue Wahl")
    assert a.titel == "Neue Wahl"
    with pytest.raises(ValidationError):
        a.aktualisieren(endDatum=a.startDatum - timedelta(days=1))

# Ergebniszählung
def test_ergebnis_auszaehlen_counts_correctly():
    a = Abstimmung(**_valid_abstimmung())
    a.stimmen = [
        Stimme(buergerId=1, option=Stimmoption.JA, zeitpunkt=date.today()),
        Stimme(buergerId=2, option=Stimmoption.NEIN, zeitpunkt=date.today()),
        Stimme(buergerId=3, option=Stimmoption.JA, zeitpunkt=date.today()),
        Stimme(buergerId=4, option=Stimmoption.ENTHALTUNG, zeitpunkt=date.today()),
    ]
    res = a.ergebnisAuszaehlen()
    assert res == {"Ja": 2, "Nein": 1, "Enthaltung": 1}
