from ..domain.services.auth_service import AuthDomainService
from apps.shared.aspects.auth_aspect import create_token, verify_password
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository

class AuthApplicationService:
    """Application Layer: Koordiniert Login-Use-Cases."""
    
    def __init__(self, buerger_repo: BuergerRepository):
        self.domain_service = AuthDomainService()
        self.buerger_repo = buerger_repo
    
    def login_admin(self, username: str, password: str) -> dict:
        """Use Case: Admin Login."""
        if not self.domain_service.validate_admin_credentials(username, password):
            raise ValueError("Ungültige Admin-Daten")
        return {
            "access_token": create_token(user_id=username),
            "token_type": "bearer",
            "role": "admin"
        }
    
    def login_buerger(self, email: str, password: str) -> dict:
        """Use Case: Bürger Login."""
        buerger = self._find_buerger(email)
        if not verify_password(password, buerger.authentifizierungsdaten):
            raise ValueError("Falsches Passwort")
        
        identity = self.domain_service.create_buerger_identity(buerger)
        return {
            "access_token": create_token(user_id=f"buerger_{identity.buerger_id}"),
            "token_type": "bearer",
            "role": "buerger",
            "name": identity.name
        }
    
    def _find_buerger(self, email: str):
        return next((b for b in self.buerger_repo.lade_alle() if b.email == email), None)
