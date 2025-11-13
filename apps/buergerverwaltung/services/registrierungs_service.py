# apps/buergerverwaltung/services/registrierungs_service.py

from apps.buergerverwaltung.domain.entities.buerger import (
    Buerger,
    Registrierungsstatus,
    lade_buerger_db,
    speichere_buerger_db
)
from datetime import date


class Registrierungsservice:
    def __init__(self, buerger_db):
        self.buerger_db = buerger_db
        # Lädt die aktuelle Bürgerdatenbank aus JSON
        

    def registriere_buerger(self, buerger_daten: dict) -> Buerger:
        """
        Registriert einen neuen Bürger, fügt ihn der JSON hinzu und gibt ihn zurück.
        """
        # Automatische ID-Vergabe (max + 1)
        neue_id = max([b.buergerID for b in self.buerger_db], default=0) + 1
        buerger_daten["buergerID"] = neue_id
        buerger_daten["registrierungsstatus"] = Registrierungsstatus.REGISTRIERT

        # Neues Bürger-Objekt anlegen
        neuer_buerger = Buerger(**buerger_daten)

        # Speichern in "Pseudo-DB"
        self.buerger_db.append(neuer_buerger)
        speichere_buerger_db(self.buerger_db)

        print(f"✅ Neuer Bürger registriert: {neuer_buerger.name} (ID {neue_id})")
        return neuer_buerger

    def alle_buerger(self) -> list[Buerger]:
        """
        Gibt alle registrierten Bürger zurück.
        """
        return self.buerger_db
