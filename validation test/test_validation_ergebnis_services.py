import pytest
from modules.ergebnisdienst.domain.entities.ergebnis import Ergebnis, Stimmoption, Stimmenanzahl, Optionen
from modules.ergebnisdienst.domain.services.ergebnis_services import ErgebnisberechnungsService, ErgebnisvalidierungsService, ErgebnisanzeigeService
from datetime import datetime

@pytest.fixture
def sample_ergebnis():
    ja = Stimmoption(optionstext=Optionen.JA)
    nein = Stimmoption(optionstext=Optionen.NEIN)
    enth = Stimmoption(optionstext=Optionen.ENTHALTUNG)
    stimmen = [
        Stimmenanzahl(stimmoption=ja, anzahl=10),
        Stimmenanzahl(stimmoption=nein, anzahl=7),
        Stimmenanzahl(stimmoption=enth, anzahl=3)
    ]
    return Ergebnis(ergebnisID=1, abstimmungsID=99, einzelwerte=stimmen, timestamp=datetime.now())

# ErgebnisberechnungsService testen
def test_veroeffentlicheErgebnis(capsys, sample_ergebnis):
    service = ErgebnisberechnungsService()
    service.veroeffentlicheErgebnis(sample_ergebnis)
    output = capsys.readouterr().out
    assert f"Ergebnis veröffentlicht für Abstimmung {sample_ergebnis.abstimmungsID}" in output

# ErgebnisvalidierungsService testen
@pytest.mark.parametrize("anzahl, expected", [
    (10, True),     # gültig
    (0, True),      # gültig (keine Stimmen ist nicht negativ)
])
def test_stelleBerechnungSicher(sample_ergebnis, anzahl, expected):
    # Manipuliere das Ergebnis
    sample_ergebnis.einzelwerte[0].anzahl = anzahl
    service = ErgebnisvalidierungsService()
    result = service.stelleBerechnungSicher(sample_ergebnis)
    assert result == expected

# ErgebnisanzeigeService testen
def test_bereiteErgebnisseAuf(capsys, sample_ergebnis):
    service = ErgebnisanzeigeService()
    service.bereiteErgebnisseAuf(sample_ergebnis)
    output = capsys.readouterr().out
    assert "Ergebnisdetails:" in output
    assert "Option: Ja" in output
    assert "Option: Nein" in output
    assert "Option: Enthaltung" in output
