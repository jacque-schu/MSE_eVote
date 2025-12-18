from typing import Dict, List

from apps.abstimmungsmanagement.domain.models.abstimmung import Abstimmung
from apps.abstimmungsmanagement.domain.models.ergebnis import (
    Ergebnis,
    Stimmenanzahl,
    Stimmoption,
    Optionen,
)
from apps.abstimmungsmanagement.infrastructure.repositories.json_abstimmung_repository import (
    JsonAbstimmungRepository,
)


class ErgebnisService:
    def __init__(self, abstimmung_repository: JsonAbstimmungRepository):
        self._abstimmung_repository = abstimmung_repository

    def hole_ergebnis_fuer_abstimmung(self, abstimmungs_id: int) -> Ergebnis:
        # Abstimmung aus JSON-Repository laden
        abstimmung: Abstimmung = self._abstimmung_repository.get(abstimmungs_id)

        # Hier musst du an dein Abstimmungsmodell anpassen:
        # Annahme: abstimmung.stimmen ist eine Liste von Objekten mit einem Feld "option"
        # vom Typ Optionen.
        stimmen_nach_option: Dict[Optionen, int] = {
            Optionen.JA: 0,
            Optionen.NEIN: 0,
            Optionen.ENTHALTUNG: 0,
        }

        for stimme in getattr(abstimmung, "stimmen", []):
            # stimme.option ist vom Typ Stimmoption
            option_abstimmung: Stimmoption = stimme.option
            # in das Ergebnis-Enum konvertieren
            option = Optionen[option_abstimmung.name]  # Enum-Name -> Enum im Ergebnis-Model

            if option in stimmen_nach_option:
                stimmen_nach_option[option] += 1
            else:
                stimmen_nach_option[option] = 1

        einzelwerte: List[Stimmenanzahl] = [
            Stimmenanzahl(
                stimmoption=Stimmoption(optionstext=opt),
                anzahl=anz,
            )
            for opt, anz in stimmen_nach_option.items()
        ]

        return Ergebnis(
            ergebnisID=abstimmungs_id,   # oder separate ID-Strategie
            abstimmungsID=abstimmungs_id,
            einzelwerte=einzelwerte,
        )

    def hole_ergebnis_details_fuer_abstimmung(self, abstimmungs_id: int) -> List[dict]:
        ergebnis = self.hole_ergebnis_fuer_abstimmung(abstimmungs_id)
        return ergebnis.getErgebnisDetails()
