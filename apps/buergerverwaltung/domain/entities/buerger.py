# apps/buergerverwaltung/domain/entities/buerger.py
import re
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, date
from enum import Enum
import json

# Funktion, um die Bürger in einer Datei zu speichern
def speichere_buerger_db(buerger_db):
    with open("buerger_db.json", "w") as file:
        # Alle Bürger als Liste von Dictionaries speichern
        json.dump([buerger.dict() for buerger in buerger_db], file)

# Funktion, um die Bürger aus einer Datei zu laden
def lade_buerger_db():
    try:
        with open("buerger_db.json", "r") as file:
            # Lade die Daten und konvertiere sie zurück in Buerger-Objekte
            daten = json.load(file)
            return [Buerger(**buerger) for buerger in daten]
    except FileNotFoundError:
        # Falls die Datei nicht gefunden wird, gibt es keine gespeicherten Daten
        return []

# Enum für den Registrierungsstatus
class Registrierungsstatus(str, Enum):
    NEU = 'neu'
    REGISTRIERT = 'registriert'
    SUSPENDIERT = 'suspendiert'

# In-Memory-Datenbank (Liste für Bürger)
buerger_db = []

# Bürger Modell
class Buerger(BaseModel):
    buergerID: int
    name: str
    adresse: str
    geburtsdatum: date
    email: EmailStr
    registrierungsstatus: Registrierungsstatus = Registrierungsstatus.NEU
    authentifizierungsdaten: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        """Validiert den Namen des Bürgers."""
        if not name or len(name) < 1:
            raise ValueError("Name ist zu kurz.")
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s-]+", name):
            raise ValueError("Name enthält ungültige Zeichen.")
        if name.startswith('-') or name.endswith('-'):
            raise ValueError("Name darf nicht mit Bindestrich beginnen oder enden.")
        return name

    @field_validator("adresse")
    @classmethod
    def validate_adresse(cls, adresse: str) -> str:
        """Validiert die Adresse des Bürgers."""
        if not adresse or len(adresse.strip()) < 5:
            raise ValueError("Adresse ist zu kurz oder leer.")
        if adresse.strip() == '':
            raise ValueError("Adresse darf nicht nur Leerzeichen enthalten.")
        return adresse

    @field_validator("geburtsdatum", mode="before")
    @classmethod
    def parse_geburtsdatum(cls, value) -> date:
        """Validiert und parst das Geburtsdatum. Unterstützt verschiedene Formate."""
        if isinstance(value, date):
            return value  # Falls bereits ein 'date'-Objekt übergeben wird
        try:
            return datetime.strptime(value, "%d.%m.%y").date()  # Format TT.MM.JJ
        except ValueError:
            pass
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()  # Format TT.MM.JJJJ
        except ValueError:
            raise ValueError("Geburtsdatum muss im Format TT.MM.JJ oder TT.MM.JJJJ sein.")

# Funktion zum Registrieren eines Bürgers
def registriere_buerger(buerger: Buerger):
    # Überprüfen, ob der Bürger bereits existiert
    if any(existing_buerger.buergerID == buerger.buergerID for existing_buerger in buerger_db):
        raise ValueError("Bürger mit dieser ID existiert bereits.")
    
    # Bürger zur Liste (Datenbank) hinzufügen
    buerger_db.append(buerger)
    return buerger

# Funktion, um alle registrierten Bürger zu bekommen
def get_all_buerger():
    return buerger_db

# Beispiel-Test
if __name__ == "__main__":
    # Erstelle ein Beispiel-Bürger-Objekt
    try:
        buerger = Buerger(
            buergerID=1,
            name="Max Mustermann",
            adresse="Beispielweg 11",
            geburtsdatum=date(1990, 1, 1),
            email="max@example.com",
            authentifizierungsdaten="geheim",
        )
        registriere_buerger(buerger)
        print(f"Bürger registriert: {buerger}")
    except ValueError as e:
        print(f"Fehler: {e}")
    
    # Alle Bürger anzeigen
    print("Alle Bürger:")
    for b in get_all_buerger():
        print(b)
