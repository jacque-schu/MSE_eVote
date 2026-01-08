from __future__ import annotations
from datetime import datetime, timedelta, timezone
import jwt  # pip install pyjwt
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository
import bcrypt

SECRET_KEY = "your-super-secret-key-change-in-prod"  # .env später!
ALGORITHM = "HS256"

class AuthApplicationService:
    def __init__(self, repo: IBuergerRepository):
        self.repo = repo
    
    def login_admin(self, username: str, password: str):
        if username != "admin" or password != "admin123":  # Placeholder
            raise ValueError("Ungültige Admin-Daten")
        payload = {"sub": "admin", "role": "admin", "exp": datetime.now(timezone.utc) + timedelta(hours=24)}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer", "role": "admin"}
    
    def login_buerger(self, email: str, password: str):
        buerger = self.repo.finde_nach_email(email)
        print(f"DEBUG Email: {email}")
        
        if not buerger or not bcrypt.checkpw(password.encode('utf-8'), buerger.authentifizierungsdaten.encode('utf-8')):
            print("❌ Password mismatch")
            raise ValueError("Ungültige Credentials")
        
        print("✅ bcrypt OK")
        
        payload = {
            "sub": str(buerger.buergerID),
            "email": buerger.email, 
            "role": "buerger",
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        print("🔍 TOKEN generiert")
        return {
            "access_token": token,
            "token_type": "bearer", 
            "user_id": buerger.buergerID,
            "email": buerger.email
        }
