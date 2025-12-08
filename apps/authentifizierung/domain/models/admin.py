from dataclasses import dataclass

@dataclass(frozen=True)
class Admin:
    """DDD Entity: Admin-Benutzer (im Memory, später DB)."""
    username: str
    role: str = "admin"
    
    def authenticate(self, password: str) -> bool:
        """Domain Logik: Prüft Admin-Passwort."""
        VALID_ADMINS = {"admin": "admin123"}  # Später: AdminRepository
        return VALID_ADMINS.get(self.username) == password
