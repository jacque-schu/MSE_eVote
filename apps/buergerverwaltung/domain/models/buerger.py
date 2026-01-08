from datetime import date, datetime
from enum import Enum
import re
from pydantic import BaseModel, EmailStr, field_validator


class Registrierungsstatus(str, Enum):
    NEU = 'neu'
    REGISTRIERT = 'registriert'
    SUSPENDIERT = 'suspendiert'

# Kleine Prüffunktionen (Übung 7: funktionale Programmierkonzepte)
def ensure_not_empty(name: str) -> str:
    cleaned = name.strip()
    if len(cleaned) < 2:
        raise ValueError("Name ist zu kurz.")
    return cleaned

def ensure_valid_pattern(name: str) -> str:
    if not re.fullmatch(r"[A-Za-zÀ-ÿ\s-]+", name):
        raise ValueError("Name enthält ungültige Zeichen.")
    return name

def ensure_valid_hyphen(name: str) -> str:
    if name.startswith("-") or name.endswith("-"):
        raise ValueError("Name darf nicht mit Bindestrich beginnen oder enden.")
    return name

class Buerger(BaseModel):
    buergerID: int
    name: str
    adresse: str
    geburtsdatum: date
    email: EmailStr
    registrierungsstatus: Registrierungsstatus = Registrierungsstatus.NEU
    authentifizierungsdaten: str  # z.B. Platzhalter für späteres Passwortfeld

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        # Funktionale „Pipeline“ aus pure Functions
        checks = [ensure_not_empty, ensure_valid_pattern, ensure_valid_hyphen]

        for check in checks:
            name = check(name)
        return name

    @field_validator("adresse")
    @classmethod
    def validate_adresse(cls, adresse: str) -> str:
        if not adresse or len(adresse.strip()) < 5:
            raise ValueError("Adresse ist zu kurz oder leer.")
        if adresse.strip() == '':
            raise ValueError("Adresse darf nicht nur Leerzeichen enthalten.")
        return adresse

    @field_validator("geburtsdatum", mode="before")
    @classmethod
    def parse_geburtsdatum(cls, value) -> date:
        if isinstance(value, date):
            return value
        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d.%m.%y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        raise ValueError("Geburtsdatum muss im Format JJJJ-MM-TT oder TT.MM.JJJJ/JJ sein.")

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        if not email or email.strip() == '':
            raise ValueError("E-Mail-Adresse ist erforderlich.")
        return email
    
    @classmethod
    def erstelle_neu(cls, vorname: str, nachname: str, email: str, passwort: str):
    # Vollname = f"{vorname} {nachname}"
    # hashed_pw = hash_passwort(passwort)
    # id = repo.naechste_id()  # Repo via DI im Service
        return cls(id=0, vollname=..., email=email, hashed_passwort=hashed_pw)  # ID später

