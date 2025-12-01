from datetime import date, timedelta
from typing import List, Optional
from apps.abstimmungsmanagement.domain.models.abstimmung import (
    Abstimmung, Abstimmungsstatus, Stimme, Stimmoption
)

class InMemoryAbstimmungRepository:
    def __init__(self):
        self._data: List[Abstimmung] = [
            Abstimmung(
                abstimmungsID=1,
                titel="Neugestaltung Marktplatz",
                beschreibung="Sollen mehr Bäume und Sitzgelegenheiten errichtet werden?",
                startDatum=date.today(),
                endDatum=date.today() + timedelta(days=3),
                teilnehmerliste=[1,2,3],
                stimmen=[
                    Stimme(buergerId=1, option=Stimmoption.JA, zeitpunkt=date.today()),
                    Stimme(buergerId=2, option=Stimmoption.NEIN, zeitpunkt=date.today()),
                ],
                status=Abstimmungsstatus.OFFEN,
            ),
            Abstimmung(
                abstimmungsID=2,
                titel="Tempo-30-Zone in der Ortsmitte",
                beschreibung="Einführung einer dauerhaften Tempo-30-Zone auf der Hauptstraße.",
                startDatum=date.today(),
                endDatum=date.today() + timedelta(days=7),
                teilnehmerliste=[4,5],
                stimmen=[],
                status=Abstimmungsstatus.OFFEN,
            ),
            Abstimmung(
                abstimmungsID=3,
                titel="Sanierung Sporthalle",
                beschreibung="Sanierung jetzt oder in zwei Jahren?",
                startDatum=date.today() - timedelta(days=14),
                endDatum=date.today() - timedelta(days=7),
                teilnehmerliste=[6,7],
                stimmen=[],
                status=Abstimmungsstatus.GESCHLOSSEN,
            ),
        ]

    def find_by_status(self, status: Abstimmungsstatus) -> List[Abstimmung]:
        return [a for a in self._data if a.status == status]

    def get(self, abstimmungs_id: int) -> Optional[Abstimmung]:
        return next((a for a in self._data if a.abstimmungsID == abstimmungs_id), None)
