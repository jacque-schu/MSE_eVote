from __future__ import annotations
from datetime import date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, field_validator, model_validator, ConfigDict

# Abstimmungsstatus (offen,geschlossen,archiviert)
class Abstimmungsstatus(str, Enum):
    OFFEN = "offen"
    GESCHLOSSEN = "geschlossen"
    ARCHIVIERT = "archiviert"

# Stimmoptionen als Wertobjekt-Enum (Ja, Nein, Enthaltung)
class Stimmoption(str, Enum):
    JA = "Ja"
    NEIN = "Nein"
    ENTHALTUNG = "Enthaltung"

class Stimme(BaseModel):
    # Einfaches Stimmenmodell gemäß Diagramm: buergerId, option, zeitpunkt
    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    buergerId: int
    option: Stimmoption
    zeitpunkt: date

    @field_validator("zeitpunkt")
    @classmethod
    def validate_zeitpunkt(cls, d: date) -> date:
        # Zeitpunkte in der Zukunft sind erlaubt; hier nur Minimalprüfung auf Typ/Kohärenz
        return d

class Abstimmung(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    abstimmungsID: int
    titel: str
    beschreibung: str
    startDatum: date
    endDatum: date
    # Teilnehmerliste: zur Entkopplung als Liste von Bürger-IDs abgebildet
    teilnehmerliste: List[int] = []
    stimmen: List[Stimme] = []
    status: Abstimmungsstatus = Abstimmungsstatus.OFFEN


    @field_validator("titel")
    @classmethod
    def validate_titel(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
        if not v or len(v) < 3:
            raise ValueError("Titel ist zu kurz oder leer.")
        return v

    @field_validator("beschreibung")
    @classmethod
    def validate_beschreibung(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
        if not v or len(v) < 5:
            raise ValueError("Beschreibung ist zu kurz oder leer.")
        return v

    # --- Modellweite Regel: endDatum >= startDatum ---
    @model_validator(mode="after")
    def _check_datumskohärenz(self) -> "Abstimmung":
        if self.endDatum < self.startDatum:
            raise ValueError("endDatum darf nicht vor startDatum liegen.")
        return self


    def erstellen(self) -> None:
        # Erstellung lässt Status auf OFFEN, Felder sind bereits validiert
        self.status = Abstimmungsstatus.OFFEN

    def starten(self) -> None:
        # Starten ist nur sinnvoll, wenn noch offen
        if self.status != Abstimmungsstatus.OFFEN:
            raise ValueError("Starten nur im Status 'offen' möglich.")
        # Keine weitere Logik nötig

    def beenden(self) -> None:
        if self.status != Abstimmungsstatus.OFFEN:
            raise ValueError("Beenden nur aus 'offen' möglich.")
        self.status = Abstimmungsstatus.GESCHLOSSEN

    def aktualisieren(self, **kwargs) -> None:
        # Erlaubt gezielte Updates auf validierte Felder; validate_assignment greift
        erlaubte = {"titel", "beschreibung", "startDatum", "endDatum", "teilnehmerliste"}
        for k, v in kwargs.items():
            if k in erlaubte:
                setattr(self, k, v)

    def ergebnisAuszaehlen(self) -> dict:
        # Zählt Stimmen je Option, ohne Nebenwirkungen
        result = {opt.value: 0 for opt in Stimmoption}
        for s in self.stimmen:
            result[s.option.value] += 1
        return result


# Beispiel-Test
if __name__ == "__main__":
    from datetime import date, timedelta

    # Gültige Abstimmung anlegen
    abstimmung = Abstimmung(
        abstimmungsID=100,
        titel="Kommunalwahl 2026",
        beschreibung="Wahl des Stadtrats",
        startDatum=date.today(),
        endDatum=date.today() + timedelta(days=7),
        teilnehmerliste=[1, 2, 3, 4],
        stimmen=[],
    )
    print(abstimmung)

    # Beispielstimmen hinzufügen
    abstimmung.stimmen = [
        Stimme(buergerId=1, option=Stimmoption.JA, zeitpunkt=date.today()),
        Stimme(buergerId=2, option=Stimmoption.NEIN, zeitpunkt=date.today()),
        Stimme(buergerId=3, option=Stimmoption.ENTHALTUNG, zeitpunkt=date.today()),
        Stimme(buergerId=4, option=Stimmoption.JA, zeitpunkt=date.today()),
    ]

    # Ergebnis zählen und ausgeben
    ergebnis = abstimmung.ergebnisAuszaehlen()
    print("Ergebnis:", ergebnis)