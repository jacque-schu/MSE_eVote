import re #Für reguläre Ausdrücke (z.B. zur Namensprüfung)
from pydantic import BaseModel, EmailStr, field_validator #Für das Erstellen von Datenmodellen mit Validierung
from datetime import date, datetime #Für Datumsverarbeitung
from enum import Enum #Für die Definition von Aufzählungstypen (z.B. Status)

# Eine Enum-Klasse, die drei mögliche Zustände für einen Bürger definiert
# Wird als Typ für das Feld registrierungsstatus verwendet
class Registrierungsstatus(str, Enum):
    NEU = 'neu'
    REGISTRIERT = 'registriert'
    SUSPENDIERT = 'suspendiert'


class ValidationError:
    pass


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

    @field_validator("geburtsdatum", mode='before')
    @classmethod
    def parse_geburtsdatum(cls, value):
        if isinstance(value, date):
            return value
        try:
            dt = datetime.strptime(value, '%d.%m.%y')
            return dt.date()
        except ValueError:
            pass
        try:
            dt = datetime.strptime(value, '%d.%m.%Y')
            return dt.date()
        except ValueError:
            raise ValueError('Geburtsdatum muss im Format TT.MM.JJ oder TT.MM.JJJJ sein.')

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
