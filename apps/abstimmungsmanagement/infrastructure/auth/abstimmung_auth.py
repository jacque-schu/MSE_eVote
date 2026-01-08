from fastapi import Request, HTTPException, status
import jwt

# -----------------------------
# Zentrale Auth-Logik für Abstimmungen
# -----------------------------

SECRET_KEY = "your-super-secret-key-must-change"
ALGORITHM = "HS256"

# ---------------------------------
# Hilfsfunktion: Token dekodieren
# ---------------------------------
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") not in ["buerger", "admin"]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Falsche Rolle")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Ungültiges Token")


# ---------------------------------
# Für zwingend eingeloggte Endpunkte
# ---------------------------------
async def require_login(request: Request):
    """
    Prüft, ob ein gültiges Token vorhanden ist.
    Wirft HTTPException 401, wenn nicht.
    """
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nicht eingeloggt")
    return decode_token(token)


# ---------------------------------
# Optionaler Login für Templates
# ---------------------------------
async def require_login_optional(request: Request):
    """
    Prüft optional Cookie. Rückgabe payload dict oder None.
    """
    token = request.cookies.get("auth_token")
    if not token:
        return None
    try:
        return decode_token(token)
    except HTTPException:
        return None
