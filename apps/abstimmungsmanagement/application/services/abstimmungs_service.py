from datetime import date
from typing import Protocol

from apps.abstimmungsmanagement.domain.models.abstimmung import (
    Abstimmung, Stimme, Stimmoption
)
from apps.abstimmungsmanagement.domain.models.ergebnis import Ergebnis


class AbstimmungRepository(Protocol):
    def get(self, abstimmungs_id: int) -> Abstimmung: ...
    def save(self, abstimmung: Abstimmung) -> None: ...
    def list_all(self) -> list[Abstimmung]: ...  # NEU

class ErgebnisRepository(Protocol):
    def save(self, ergebnis: Ergebnis) -> None: ...


class AbstimmungsService:
    def __init__(self, abst_repo: AbstimmungRepository, erg_repo: ErgebnisRepository):
        self.abst_repo = abst_repo
        self.erg_repo = erg_repo

    def erstelle_abstimmung(self, **daten) -> Abstimmung:
        abstimmung = Abstimmung(**daten)
        self.abst_repo.save(abstimmung)
        return abstimmung

    def stimme_abgeben(self, abstimmungs_id: int, buerger_id: int,
                       option: Stimmoption, datum: date) -> Abstimmung:
        abstimmung = self.abst_repo.get(abstimmungs_id)
        stimme = Stimme(buergerId=buerger_id, option=option, zeitpunkt=datum)
        abstimmung.stimme_abgeben(stimme)
        self.abst_repo.save(abstimmung)
        return abstimmung

    def ergebnis_berechnen(self, abstimmungs_id: int, ergebnis_id: int) -> Ergebnis:
        abstimmung = self.abst_repo.get(abstimmungs_id)
        ergebnis = Ergebnis.berechneErgebnis(
            ergebnisID=ergebnis_id,
            abstimmungsID=abstimmungs_id,
            stimmen=abstimmung.stimmen,
        )
        self.erg_repo.save(ergebnis)
        return ergebnis

    def liste_abstimmungen(self) -> list[Abstimmung]:
        return self.abst_repo.list_all()


