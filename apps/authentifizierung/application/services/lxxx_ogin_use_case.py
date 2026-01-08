from __future__ import annotations
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.responses import JSONResponse
from datetime import timedelta
from apps.authentifizierung.application.services.auth_service import AuthApplicationService

# ✅ GENAUER IMPORT aus Application Layer (per Tree)
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository

router = APIRouter(prefix="/api/auth", tags=["Authentifizierung"])

def get_buerger_repo() -> IBuergerRepository:
    from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # MSE_eVote root
    db_path = BASE_DIR / "apps" / "buergerverwaltung" / "infrastructure" / "persistence" / "buerger_db.json"
    return BuergerRepository(str(db_path))

def get_auth_service(repo: IBuergerRepository = Depends(get_buerger_repo)):
    return AuthApplicationService(repo)

@router.get("/", response_class=HTMLResponse)
async def login_seite(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/buergerverwaltung/admin")
async def admin_login(username: str = Form(...), password: str = Form(...), service: AuthApplicationService = Depends(get_auth_service)):
    try:
        token_data = service.login_admin(username, password)
    except ValueError:
        raise HTTPException(401, "Ungültige Admin-Daten")

    response = JSONResponse(content={"msg": "Login erfolgreich"})
    response.set_cookie(
        key="access_token",
        value=token_data["access_token"],
        httponly=True,
        samesite="lax",
        max_age=24*3600
    )
    return response


@router.post("/buergerverwaltung/buerger")
async def buerger_login(email: str = Form(...), password: str = Form(...), service: AuthApplicationService = Depends(get_auth_service)):
    try:
        token_data = service.login_buerger(email, password)
    except ValueError:
        raise HTTPException(401, "Ungültige Credentials")

    response = JSONResponse(content={"msg": "Login erfolgreich"})
    response.set_cookie(
        key="access_token",
        value=token_data["access_token"],
        httponly=True,
        samesite="lax",
        max_age=24*3600
    )
    return response

