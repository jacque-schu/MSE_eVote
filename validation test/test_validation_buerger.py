import pytest
from modules.buergerverwaltung.domain.entities.buerger import Buerger
from pydantic import ValidationError
from datetime import date

# Name Tests
@pytest.mark.parametrize("name, valid", [
    ("Anna-Maria", True),               # Happy Path
    ("Élodie", True),
    ("Maximilian", True),
    ("É", True),                       # Edge Case: sehr kurzer Name
    ("A" * 50, True),                  # Edge Case: langer Name
    ("Anna--Maria", True),             # Edge Case: doppelte Bindestriche

    ("", False),                      # Negativ: leer
    ("Anna123", False),               # Negativ: Zahlen
    ("Anna@", False),                 # Negativ: Sonderzeichen
    ("-Anna", False),                 # Negativ: Bindestrich am Anfang
    ("Anna-", False),                 # Negativ: Bindestrich am Ende
])
def test_name_validation(name, valid):
    data = dict(
        buergerID=1,
        name=name,
        adresse="Musterstraße 1",
        geburtsdatum=date(1990, 1, 1),
        email="max@mustermann.de",
        authentifizierungsdaten="geheim"
    )
    if valid:
        b = Buerger(**data)
        assert b.name == name
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)

# Email Tests
@pytest.mark.parametrize("email, valid", [
    ("max.mustermann@example.com", True),
    ("user123@domain.de", True),
    ("a@b.co", True),

    ("user@domain", False),          # Negativ: kein TLD
    ("invalid-email", False),
    ("", False),
    ("user@ domain.com", False),     # Negativ: Leerzeichen
])
def test_email_validation(email, valid):
    data = dict(
        buergerID=2,
        name="Max Muster",
        adresse="Musterstraße 1",
        geburtsdatum=date(1990, 1, 1),
        email=email,
        authentifizierungsdaten="geheim"
    )
    if valid:
        b = Buerger(**data)
        assert b.email == email
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)

# Geburtsdatum Tests
@pytest.mark.parametrize("geburtsdatum, valid", [
    (date(1990, 1, 1), True),
    (date(2000, 2, 29), True),
    (date(1900, 1, 1), True),
    (date.today(), True),

    (date.today().replace(year=date.today().year + 1), False), # Zukunftsdatum
])
def test_geburtsdatum_validation(geburtsdatum, valid):
    data = dict(
        buergerID=3,
        name="Max Muster",
        adresse="Musterstraße 1",
        geburtsdatum=geburtsdatum,
        email="max@mustermann.de",
        authentifizierungsdaten="geheim"
    )
    if valid:
        b = Buerger(**data)
        assert b.geburtsdatum == geburtsdatum
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)

# Adresse Tests
@pytest.mark.parametrize("adresse, valid", [
    ("Musterstraße 12", True),
    ("Hauptstr. 1a", True),
    ("Am Stadtpark 5", True),
    ("A" * 100, True),

    ("", False),
    ("   ", False),
    (None, False),
])
def test_adresse_validation(adresse, valid):
    data = dict(
        buergerID=4,
        name="Max Muster",
        adresse=adresse,
        geburtsdatum=date(1990, 1, 1),
        email="max@mustermann.de",
        authentifizierungsdaten="geheim"
    )
    if valid:
        b = Buerger(**data)
        assert b.adresse == adresse
    else:
        with pytest.raises(ValidationError):
            Buerger(**data)
