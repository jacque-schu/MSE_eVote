import re
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, date
from enum import Enum

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

# Beispiel-Test
if __name__ == "__main__":
    # Das wird bei gültiger Eingabe funktionieren:
    try:
        buerger = Buerger(
            buergerID=1,
            name="Max Mustermann",
            adresse="Beispielweg 11",
            geburtsdatum=date(1990, 1, 1),
            email="max@example.com",
            authentifizierungsdaten="geheim",
        )
        print(buerger)
    except ValueError as e:
        print(f"Fehler: {e}")
