import os
import json
from datetime import date
from typing import List
from ...domain.models.buerger import Buerger

# Pure Functions (keine I/O)

def parse_buerger_liste(daten) -> List[Buerger]:
    if not isinstance(daten, list):
        return []
    return [Buerger(**buerger) for buerger in daten]

def serialize_buerger_liste(buerger_liste: List[Buerger]) -> list[dict]:
    return [b.model_dump() for b in buerger_liste]

def date_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def hinzufuegen(buerger_liste: List[Buerger], neuer_buerger: Buerger) -> List[Buerger]:
    # keine Mutation der ursprünglichen Liste
    return [*buerger_liste, neuer_buerger]


class BuergerRepository:
    def __init__(self, dateipfad: str):
        self.dateipfad = dateipfad
        self._stelle_verzeichnis_sicher()

    def _stelle_verzeichnis_sicher(self):
        verzeichnis = os.path.dirname(self.dateipfad)
        if not os.path.exists(verzeichnis):
            os.makedirs(verzeichnis)

    def lade_alle(self) -> List[Buerger]:
        try:
            with open(self.dateipfad, "r", encoding="utf-8") as file:
                daten = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # Datei zurücksetzen bei Fehler
            self.speichere_alle([])
            return []

        # funktionale Transformation
        return parse_buerger_liste(daten)

    def speichere_alle(self, buerger_liste: List[Buerger]):
        daten = serialize_buerger_liste(buerger_liste)
        with open(self.dateipfad, "w", encoding="utf-8") as file:
            json.dump(
                daten,
                file,
                default=date_serializer,
                ensure_ascii=False,
                indent=4,
            )

    def naechste_buerger_id(self) -> int:
        alle = self.lade_alle()
        if not alle:
            return 0  # oder 1, wenn ihr bei 1 starten wollt
        return max(b.buergerID for b in alle) + 1

    def fuege_hinzu(self, neuer_buerger: Buerger):
        alte_liste = self.lade_alle()
        neue_liste = hinzufuegen(alte_liste, neuer_buerger)
        self.speichere_alle(neue_liste)