import io
import json
import os
import re
import sys
from datetime import datetime, date
from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator

# Erstelle den absoluten Pfad basierend auf dem aktuellen Arbeitsverzeichnis (Projektordner)
projektordner = os.path.dirname(os.path.abspath(__file__))  # Aktuellen Ordner bekommen
root_ordner = os.path.dirname(os.path.dirname(projektordner))  # Zwei Ebenen nach oben
json_dateipfad = os.path.join(root_ordner, "data", "buerger_db.json")  # Zum 'data' Ordner gehen
buerger_db = None

# Verzeichnis prüfen und ggf. erstellen
verzeichnis = os.path.dirname(json_dateipfad)
if not os.path.exists(verzeichnis):
    os.makedirs(verzeichnis)


# Setzt die Standard-Codierung für die Ausgabe in der Konsole auf UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Registrierungsstatus(str, Enum):
    NEU = 'neu'
    REGISTRIERT = 'registriert'
    SUSPENDIERT = 'suspendiert'

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
        if adresse.strip() == '':  # falls nur Leerzeichen
            raise ValueError("Adresse darf nicht nur Leerzeichen enthalten.")
        return adresse

    @field_validator("geburtsdatum", mode="before")
    @classmethod
    def parse_geburtsdatum(cls, value) -> date:
        """Validiert und parst das Geburtsdatum. Unterstützt verschiedene Formate."""
        if isinstance(value, date):
            return value  # Falls bereits ein 'date'-Objekt übergeben wird
        # Versuche, das Datum im Format TT.MM.JJ oder TT.MM.JJJJ zu parsen
        try:
            return datetime.strptime(value, "%d.%m.%y").date()  # Format TT.MM.JJ
        except ValueError:
            pass
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()  # Format TT.MM.JJJJ
        except ValueError:
            pass
        # Unterstütze auch das ISO-Format (YYYY-MM-DD)
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()  # Format JJJJ-MM-TT
        except ValueError:
            raise ValueError("Geburtsdatum muss im Format TT.MM.JJ, TT.MM.JJJJ oder JJJJ-MM-TT sein.")

# Funktion zum Laden der Bürger-Daten aus der JSON-Datei
def lade_buerger_db():
    print(f"Lade Bürger-Datenbank von: {json_dateipfad}")
    try:
        with open(json_dateipfad, "r", encoding="utf-8") as file:
            daten = json.load(file)
            if isinstance(daten, list):
                print(f"{len(daten)} Bürger-Daten wurden geladen.")
                return [Buerger(**buerger) for buerger in daten]
            else:
                print("Warnung: Die Datei enthält keine gültige Liste von Bürgern.")
                return []
    except FileNotFoundError:
        print("Die Datei wurde nicht gefunden. Erstelle eine neue Datei...")
        return []
    except json.JSONDecodeError as e:
        print(f"Fehler beim Decodieren der JSON-Daten: {e}. Die Datei wird zurückgesetzt.")
        # Setze die Datei zurück, falls ein Fehler auftritt
        with open(json_dateipfad, "w", encoding="utf-8") as file:
            json.dump([], file)  # Leere Liste schreiben, um die Datei zurückzusetzen
        return []

# Funktion zum Serialisieren von `date`-Objekten
def date_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()  # Wandelt das Datum in ISO-Format (yyyy-mm-dd) um
    raise TypeError(f"Type {type(obj)} not serializable")

# Funktion zum Speichern der Bürger-Daten in der JSON-Datei
def speichere_buerger_db(buerger_db):
    print(f"Speichere Bürger-Daten in: {json_dateipfad}")
    
    # Sicherstellen, dass der Ordner existiert
    verzeichnis = os.path.dirname(json_dateipfad)
    if not os.path.exists(verzeichnis):
        print(f"Ordner '{verzeichnis}' existiert noch nicht. Erstelle ihn...")
        os.makedirs(verzeichnis)

    try:
        # JSON mit dem date_serializer speichern, um die 'date'-Objekte zu serialisieren
        with open(json_dateipfad, "w", encoding="utf-8") as file:
            json.dump([buerger.model_dump() for buerger in buerger_db], file, default=date_serializer, ensure_ascii=False, indent=4)
        print(f"Die Bürger wurden erfolgreich in {json_dateipfad} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Bürger: {e}")


def init_buerger_db():
    global buerger_db
    if buerger_db is None:
        buerger_db = lade_buerger_db()

def add_buerger(neuer_buerger):
    init_buerger_db()
    buerger_db.append(neuer_buerger)
    speichere_buerger_db(buerger_db)

def get_all_buerger():
    init_buerger_db()
    return buerger_db

if __name__ == "__main__":
    init_buerger_db()
    print("Gespeicherte Bürger-Datenbank (nach Hinzufügen des neuen Bürgers):")
    for b in buerger_db:
        print(f"- {b.name}, {b.geburtsdatum}, {b.email}")
