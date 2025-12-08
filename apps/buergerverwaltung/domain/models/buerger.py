from datetime import date, datetime
from enum import Enum
import re
from pydantic import BaseModel, EmailStr, field_validator


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
    authentifizierungsdaten: str  # z.B. Platzhalter für späteres Passwortfeld

    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        name = name.strip()
        if not name or len(name) < 2:
            raise ValueError("Name ist zu kurz")
        # 👇 Leerzeichen ERLAUBEN
        if not re.fullmatch(r"^[A-Za-zÄÖÜäöüß\s-]+$", name):
            raise ValueError("Name enthält ungültige Zeichen")
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
