# apps/abstimmungsmanagement/infrastructure/auth/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from apps.shared.aspects.auth_aspect import is_token_valid

security = HTTPBearer()


async def require_login(token: str = Depends(security)):
    """Prüft Login (Bürger ODER Admin) mit is_token_valid()"""
    try:
        is_token_valid(token.credentials)  # ← DEINE Funktion!

        # Payload extrahieren (aus create_token)
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])

        return {
            "user_id": payload["sub"],  # Dein "sub" = user_id
            "role": payload.get("role", "buerger")  # Optional role
        }
    except HTTPException:
        raise HTTPException(
            status_code=401,
            detail="Bitte loggen Sie sich ein, um Ihre Stimme abzugeben"
        )
