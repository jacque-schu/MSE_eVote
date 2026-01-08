from typing import Dict, Optional

from apps.shared.aspects.auth_aspect import create_token, verify_password
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository
from apps.buergerverwaltung.domain.models.buerger import Buerger


class AuthApplicationService:
    def __init__(self, buerger_repo: Optional[IBuergerRepository] = None):
        """
        buerger_repo:
          - für Bürger-Login erforderlich
          - für Admin-Login optional (da hardcoded Admin-Daten)
        """
        self.buerger_repo = buerger_repo

    def login_admin(self, username: str, password: str) -> Dict[str, str]:
        """
        Admin-Login mit hart codierten Credentials.
        Wirft ValueError bei ungültigen Daten.
        """
        VALID_ADMINS = {"admin": "admin123"}
        if username not in VALID_ADMINS or VALID_ADMINS[username] != password:
            raise ValueError("Ungültige Admin-Daten")

        return {
            "access_token": create_token(user_id=username),
            "token_type": "bearer",
            "role": "admin",
        }

    def login_buerger(self, email: str, password: str) -> Dict[str, str]:
        """
        Bürger-Login:
        - Hole Bürger über Repository
        - Prüfe Passwort via verify_password
        - Erzeuge JWT-Token
        Wirft ValueError bei ungültigen Credentials.
        """
        if self.buerger_repo is None:
            raise ValueError("Bürger-Repository nicht konfiguriert")

        buerger: Optional[Buerger] = self.buerger_repo.finde_nach_email(email)
        if not buerger or not verify_password(password, buerger.authentifizierungsdaten):
            raise ValueError("Ungültige Credentials")

        return {
            "access_token": create_token(user_id=f"buerger_{buerger.buergerID}"),
            "token_type": "bearer",
            "role": "buerger",
            "name": buerger.name,
        }
