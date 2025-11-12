# apps/buergerverwaltung/domain/services/registrierungs_service.py
from pydantic import ValidationError
from .authentifizierungs_service import AuthentifizierungsService
from .models import Buerger
from sqlalchemy.orm import Session

class RegistrierungsService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthentifizierungsService()

    def register_buerger(self, buerger_data: dict):
        # Validierung könnte hier durchgeführt werden (Pydantic Model etc.)
        try:
            # Bürgerobjekt erstellen
            buerger = Buerger(**buerger_data)

            # Passwort verschlüsseln
            hashed_password = self.auth_service.hash_password(buerger_data["authentifizierungsdaten"])
            buerger.authentifizierungsdaten = hashed_password

            # Bürger in der DB speichern
            self.db.add(buerger)
            self.db.commit()
            self.db.refresh(buerger)
            return buerger
        except ValidationError as e:
            raise ValueError(f"Registrierung fehlgeschlagen: {str(e)}")

# Beispiel-Verwendung:
# registrierungs_service = RegistrierungsService(db_session)
# new_buerger = registrierungs_service.register_buerger(buerger_data)
