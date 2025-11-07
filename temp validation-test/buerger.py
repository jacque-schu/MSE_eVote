import re
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from enum import Enum

from pydantic_core.core_schema import is_instance_schema


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
        if isinstance(name, str):       # Trim vor der Prüfung, überprüft ob "name" wirklich ein Text ist,
            name = name.strip()         # wenn ja, werden vorne und hinten überflüssige Leerzeichen abgeschnitten.
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
        if isinstance(adresse, str):    # nochmal Trim vor der Prüfung, überprüft ob "adresse" wirklich ein Text ist,
            adresse = adresse.strip()   # wenn ja, werden wieder vorne und hinten überflüssige Leerzeichen abgeschnitten.
        if not adresse or len(adresse.strip()) < 5:
            raise ValueError("Adresse ist zu kurz oder leer.")
        return adresse

    @field_validator("geburtsdatum")
    @classmethod
    def validate_geburtsdatum(cls, geburtsdatum):
        if geburtsdatum > date.today():
            raise ValueError("Geburtsdatum darf nicht in der Zukunft liegen.")
        return geburtsdatum

    def registriere(self):
        self.registrierungsstatus = Registrierungsstatus.REGISTRIERT

    def authentifiziere(self, daten):
        return self.authentifizierungsdaten == daten

    def datenAktualisieren(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

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
