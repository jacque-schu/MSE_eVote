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
        if not name or len(name) < 1:
            raise ValueError("Name ist zu kurz.")
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s-]+", name):
            raise ValueError("Name enthält ungültige Zeichen.")
        if name.startswith('-') or name.endswith('-'):
            raise ValueError("Name darf nicht mit Bindestrich beginnen oder enden.")
        return name

    @field_validator("adresse")
    @classmethod
    def validate_adresse(cls, adresse):
        if not adresse or len(adresse.strip()) < 5:
            raise ValueError("Adresse ist zu kurz oder leer.")
        return adresse

    @field_validator("geburtsdatum", mode="before")
    @classmethod
    def parse_geburtsdatum(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%d.%m.%y").date()
        except ValueError:
            pass
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Geburtsdatum muss im Format TT.MM.JJ oder TT.MM.JJJJ sein.")

# Beispiel-Test
if __name__ == "__main__":
    # Das wird bei gültiger Eingabe funktionieren:
    buerger = Buerger(
        buergerID=1,
        name="Max Mustermann",
        adresse="Beispielweg 11",
        geburtsdatum=date(1990, 1, 1),
        email="max@example.com",
        authentifizierungsdaten="geheim",
    )
    print(buerger)
