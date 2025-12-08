import pytest
from datetime import date
from pydantic import ValidationError

from apps.buergerverwaltung.domain.models.buerger import Buerger


# Name-Validierung (mind. 2 Zeichen, Buchstaben/Leerzeichen/Bindestrich)
@pytest.mark.parametrize("name, valid", [
    ("Anna Maria", True),
    ("Max-Moritz", True),
    ("ÄÖÜ äöüß", True),
    ("A B", True),                 # minimal 2 Zeichen + Leerzeichen erlaubt

    ("A", False),                  # zu kurz
    ("", False),
    ("  ", False),
    ("Anna123", False),
    ("Anna@", False),
])
def test_name_validation(name, valid):
    data = dict(
        buergerID=1,
        name=name,
        adresse="Musterstraße 1",
        geburtsdatum=date(1990, 1, 1),
        email="max@mustermann.de",
        authentifizierungsdaten="geheim",
    )
    if valid:
        b = Buerger(**data)
        assert b.name == name.strip()
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)


# Email-Validierung (nur „nicht leer“ plus EmailStr)
@pytest.mark.parametrize("email, valid", [
    ("max.mustermann@example.com", True),
    ("user123@domain.de", True),
    ("a@b.co", True),

    ("", False),
    ("   ", False),
])
def test_email_validation(email, valid):
    data = dict(
        buergerID=2,
        name="Max Muster",
        adresse="Musterstraße 1",
        geburtsdatum=date(1990, 1, 1),
        email=email,
        authentifizierungsdaten="geheim",
    )
    if valid:
        b = Buerger(**data)
        assert b.email == email
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)


# Geburtsdatum-Parsing (mehrere Formate)
@pytest.mark.parametrize("geburtsdatum, valid", [
    ("05.11.1990", True),
    ("05.11.25", True),
    ("1990-11-05", True),
    (date(1990, 11, 5), True),

    ("31.02.1990", False),
    ("", False),
    ("2025/01/01", False),
    ("01-01-2025", False),
])
def test_geburtsdatum_validation(geburtsdatum, valid):
    data = dict(
        buergerID=3,
        name="Max Muster",
        adresse="Musterstraße 1",
        geburtsdatum=geburtsdatum,
        email="max@mustermann.de",
        authentifizierungsdaten="geheim",
    )
    if valid:
        b = Buerger(**data)
        assert isinstance(b.geburtsdatum, date)
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)


# Adress-Validierung (min. 5 Zeichen, nicht nur Leerzeichen)
@pytest.mark.parametrize("adresse, valid", [
    ("Musterstraße 12", True),
    ("Hauptstr. 1a", True),
    ("Am Park 5", True),
    ("A" * 100, True),

    ("", False),
    ("   ", False),
    ("abc", False),   # zu kurz
])
def test_adresse_validation(adresse, valid):
    data = dict(
        buergerID=4,
        name="Max Muster",
        adresse=adresse,
        geburtsdatum=date(1990, 1, 1),
        email="max@mustermann.de",
        authentifizierungsdaten="geheim",
    )
    if valid:
        b = Buerger(**data)
        assert b.adresse == adresse
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)
