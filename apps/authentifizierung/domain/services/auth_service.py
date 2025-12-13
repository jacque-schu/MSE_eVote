from ..models.admin import Admin
from ..models.buerger_auth import BuergerIdentity
from apps.shared.aspects.auth_aspect import create_token
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository
from apps.shared.aspects.auth_aspect import verify_password

class AuthService:
    """DDD Application Service: Zentrale Auth-Logik."""
    
    def __init__(self, buerger_repository: BuergerRepository):
        self.buerger_repo = buerger_repository

    def authenticate_admin(self, username: str, password: str):
        """Authentifiziert Admin."""
        admin = Admin(username=username)
        if admin.authenticate(password):
            return {"access_token": create_token(user_id=f"admin_{username}")}
        raise ValueError("Ungültige Admin-Daten")

    def authenticate_buerger(self, email: str, password: str):
        """Authentifiziert Bürger."""
        buerger = self._find_buerger_by_email(email)
        if buerger and verify_password(password, buerger.authentifizierungsdaten):
            identity = BuergerIdentity.from_buerger(buerger)
            return {
                "access_token": create_token(user_id=f"buerger_{identity.buerger_id}"),
                "role": "buerger",
                "name": identity.name
            }
        raise ValueError("Bürger oder Passwort falsch")
    
    def _find_buerger_by_email(self, email: str):
        """Repository-Zugriff (Infrastructure)."""
        alle = self.buerger_repo.lade_alle()
        return next((b for b in alle if b.email == email), None)
