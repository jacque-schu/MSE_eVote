import pytest
from datetime import datetime
from pydantic import ValidationError
from apps.abstimmungsmanagement.domain.models.ergebnis import Ergebnis, Stimmoption, Stimmenanzahl, Optionen

# Stimmenanzahl-Tests: Anzahl darf nicht negativ sein
@pytest.mark.parametrize("anzahl, valid", [
    (5, True),
    (0, True),
    (100000, True),
    (-1, False),
    (-50, False),
])
def test_stimmenanzahl_validation(anzahl, valid):
    option = Stimmoption(optionstext=Optionen.JA)
    if valid:
        stimme = Stimmenanzahl(stimmoption=option, anzahl=anzahl)
        assert stimme.anzahl == anzahl
    else:
        with pytest.raises(ValidationError):
            Stimmenanzahl(stimmoption=option, anzahl=anzahl)

# Stimmoption-Tests: Option muss gültig sein
@pytest.mark.parametrize("option, valid", [
    ("Ja", True),
    ("Nein", True),
    ("Enthaltung", True),
    ("Ungültig", False),
    ("ja", False),   # Case Sensitivity prüfen
    ("", False),
])
def test_stimmoption_validation(option, valid):
    if valid:
        s = Stimmoption(optionstext=Optionen(option))
        assert s.optionstext.value == option
    else:
        with pytest.raises(ValueError):
            Stimmoption(optionstext=Optionen(option))

# Ergebnis-Tests: Mindestens eine Stimmenanzahl erforderlich
@pytest.mark.parametrize("einzelwerte, valid", [
    ([Stimmenanzahl(stimmoption=Stimmoption(optionstext=Optionen.JA), anzahl=2)], True),
    ([], False),
    (None, False),
])
def test_ergebnis_einzelwerte_validation(einzelwerte, valid):
    if einzelwerte is None:
        einzelwerte_arg = None
    else:
        einzelwerte_arg = einzelwerte

    data = dict(
        ergebnisID=1,
        abstimmungsID=99,
        einzelwerte=einzelwerte_arg,
        timestamp=datetime.now()
    )
    if valid:
        e = Ergebnis(**data)
        assert isinstance(e, Ergebnis)
    else:
        with pytest.raises(ValidationError):
            Ergebnis(**data)

# Gesamtergebnis-Berechnungstest
def test_gesamtergebnis_berechnung():
    stimmen = [
        Stimmenanzahl(stimmoption=Stimmoption(optionstext=Optionen.JA), anzahl=3),
        Stimmenanzahl(stimmoption=Stimmoption(optionstext=Optionen.NEIN), anzahl=5),
        Stimmenanzahl(stimmoption=Stimmoption(optionstext=Optionen.ENTHALTUNG), anzahl=2)
    ]
    ergebnis = Ergebnis(ergebnisID=1, abstimmungsID=100, einzelwerte=stimmen)
    assert ergebnis.gesamtergebnis == 10

# Ergebnisdetails-Test
def test_ergebnisdetails():
    stimmen = [
        Stimmenanzahl(stimmoption=Stimmoption(optionstext=Optionen.JA), anzahl=2)
    ]
    ergebnis = Ergebnis(ergebnisID=7, abstimmungsID=23, einzelwerte=stimmen)
    details = ergebnis.getErgebnisDetails()
    assert details == [{'Option': 'Ja', 'Stimmen': 2}]

def test_stimmenanzahl_large_value():
    option = Stimmoption(optionstext=Optionen.JA)
    großer_wert = 10**12  # Beispiel: eine Billion Stimmen
    stimme = Stimmenanzahl(stimmoption=option, anzahl=großer_wert)
    assert stimme.anzahl == großer_wert
    stimmen = [Stimmenanzahl(stimmoption=option, anzahl=großer_wert)]
    ergebnis = Ergebnis(ergebnisID=1, abstimmungsID=99, einzelwerte=stimmen, timestamp=datetime.now())
    assert ergebnis.gesamtergebnis == großer_wert