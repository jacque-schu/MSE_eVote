# apps/buergerverwaltung/domain/services/authentifizierungs_service.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from apps.buergerverwaltung.domain.entities.buerger import Buerger  # Importiere das Buerger-Modell
from pydantic import EmailStr

# Beispiel: Sicherheitseinstellungen für Hashing und JWT
SECRET_KEY = "mein_geheimer_schluessel"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthentifizierungsService:
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        """Hashes a password using bcrypt."""
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Das Passwort darf für bcrypt maximal 72 Bytes lang sein.")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies that the given plain password matches the hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Creates a JWT access token."""
        now_utc = datetime.now(timezone.utc)

        if expires_delta:
            expire = now_utc + expires_delta
        else:
            expire = now_utc + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, db, email: EmailStr, password: str) -> Optional[Buerger]:
        """Authenticates the user by verifying email and password."""
        user = db.query(Buerger).filter(Buerger.email == email).first()  # Beispiel mit SQLAlchemy
        if not user or not self.verify_password(password, user.authentifizierungsdaten):
            return None
        return user
