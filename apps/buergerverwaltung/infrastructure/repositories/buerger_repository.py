import os
import json
from datetime import date
from typing import List
from ...domain.models.buerger import Buerger


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
                if isinstance(daten, list):
                    return [Buerger(**buerger) for buerger in daten]
                else:
                    return []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # Datei zurücksetzen bei Fehler
            self.speichere_alle([])
            return []

    def speichere_alle(self, buerger_liste: List[Buerger]):
        def date_serializer(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        with open(self.dateipfad, "w", encoding="utf-8") as file:
            json.dump([b.model_dump() for b in buerger_liste], file, default=date_serializer, ensure_ascii=False, indent=4)

    def fuege_hinzu(self, neuer_buerger: Buerger):
        buerger_liste = self.lade_alle()
        # Einfach anhängen, keine Duplikatprüfung hier (Optional in Application Service)
        buerger_liste.append(neuer_buerger)
        self.speichere_alle(buerger_liste)
