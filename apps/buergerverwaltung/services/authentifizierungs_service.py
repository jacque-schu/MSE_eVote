# apps/buergerverwaltung/domain/services/authentifizierungs_service.py
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .models import Buerger  # Importiere das Buerger-Modell

# Beispiel: Sicherheitseinstellungen für Hashing und JWT
SECRET_KEY = "mein_geheimer_schluessel"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthentifizierungsService:
    def __init__(self):
        pass
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, db, email: str, password: str) -> Optional[Buerger]:
        # Diese Methode könnte mit einer Datenbank oder einer anderen Quelle arbeiten
        user = db.query(Buerger).filter(Buerger.email == email).first()  # Einfaches Beispiel
        if not user or not self.verify_password(password, user.authentifizierungsdaten):
            return None
        return user

# Beispiel-Verwendung:
# auth_service = AuthentifizierungsService()
# user = auth_service.authenticate_user(db_session, email="max@example.com", password="mein_passwort")
# token = auth_service.create_access_token({"sub": user.email})
