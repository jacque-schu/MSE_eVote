import aspectlib
import jwt
import os
from fastapi import Header
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import bcrypt
from functools import wraps
import inspect
from fastapi import Header, HTTPException, Request



load_dotenv()  # Lädt .env automatisch

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_for_dev")

# Aus Umgebungsvariable laden (Production-sicher!)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_for_dev_only_change_this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(user_id: str) -> str:
    """Erstellt einen JWT Access Token für einen Benutzer."""
    payload = {
        "sub": user_id,  # Subject = Benutzer-ID
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone.utc)  # Issued at
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def is_token_valid(token: str) -> bool:
    """Validiert einen JWT Token (Signatur + Ablaufzeit)."""
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token abgelaufen"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Ungültiger Token"
        )


def fastapi_auth_check(func):
    @wraps(func)
    async def wrapper(
        request: Request,
        *args,
        authorization: str = Header(None),
        **kwargs
    ):
        # Dauerhaftes Logging – bleibt im Terminal sichtbar
        print("AUTH DEBUG header:", repr(authorization))

        auth_value = str(authorization) if authorization is not None else None
        if not auth_value:
            raise HTTPException(status_code=401, detail="Authorization header fehlt")

        token = auth_value.replace("Bearer ", "").strip()
        print("AUTH DEBUG token startswith:", token[:20])  # nur Anfang

        if not is_token_valid(token):
            raise HTTPException(status_code=401, detail="Token ungültig oder abgelaufen")

        return await func(request, *args, **kwargs)
    return wrapper




def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
