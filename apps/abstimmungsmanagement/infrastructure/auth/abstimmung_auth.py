from fastapi import HTTPException, Request
import jwt
from apps.shared.aspects.auth_aspect import is_token_valid, SECRET_KEY, ALGORITHM

def require_login(request: Request):
    token = request.cookies.get("auth_token")
    if not token or not is_token_valid(token):
        raise HTTPException(status_code=401, detail="Login fehlt")

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload["sub"]
    role = "admin" if user_id == "admin" or user_id.startswith("admin_") else "buerger"

    return {"user_id": user_id, "role": role}
