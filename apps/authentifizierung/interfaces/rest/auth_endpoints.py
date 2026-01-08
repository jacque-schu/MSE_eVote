from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

# ✅ KORREKTER IMPORT per DDD-Struktur (Application Layer von Bürgerverwaltung)
from apps.authentifizierung.application.services.auth_service import AuthApplicationService
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository

router = APIRouter(prefix="/api/auth", tags=["Authentifizierung"])

# ✅ Lokale Repo-Funktion (keine Imports-Probleme)
def get_local_repo() -> IBuergerRepository:
    from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent  # MSE_eVote root
    db_path = BASE_DIR / "apps" / "buergerverwaltung" / "infrastructure" / "persistence" / "buerger_db.json"
    return BuergerRepository(str(db_path))

def get_auth_service(repo: IBuergerRepository = Depends(get_local_repo)):
    return AuthApplicationService(repo)

# Templates-Pfad
TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "ui" / "authentifizierung" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/", response_class=HTMLResponse)
async def login_seite(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/buergerverwaltung/admin")
async def admin_login(username: str = Form(...), password: str = Form(...), service: AuthApplicationService = Depends(get_auth_service)):
    print(f"🔍 Admin-Login: {username}")
    try:
        result = service.login_admin(username, password)
        print(f"✅ Admin erfolgreich!")
        return result
    except ValueError:
        raise HTTPException(status_code=401, detail="Ungültige Admin-Daten")

@router.post("/buergerverwaltung/buerger")
async def buerger_login(
    email: str = Form(...), 
    password: str = Form(...), 
    service: AuthApplicationService = Depends(get_auth_service)
):
    try:
        result = service.login_buerger(email, password)
        print("🔍 Bürger-Login:", email)
        print("✅ Bürger erfolgreich!")
        return result
    except ValueError:
        raise HTTPException(status_code=401, detail="Ungültige Credentials")
