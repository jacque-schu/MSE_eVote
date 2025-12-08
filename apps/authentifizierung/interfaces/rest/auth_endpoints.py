from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from apps.shared.aspects.auth_aspect import create_token, verify_password
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository

# ✅ ROUTER DEFINIEREN!
router = APIRouter(prefix="/api/auth", tags=["Authentifizierung"])

DB_DATEIPFAD = Path(__file__).parent.parent.parent.parent.parent / "apps" / "buergerverwaltung" / "infrastructure" / "persistence" / "buerger_db.json"
repo = None

def init_repo():
    global repo
    if repo is None:
        repo = BuergerRepository(str(DB_DATEIPFAD))

# 1. LOGIN-SEITE
@router.get("/", response_class=HTMLResponse)
async def login_seite(request: Request):
    templates = Jinja2Templates(directory="ui/authentifizierung/templates")
    return templates.TemplateResponse(request, "login.html", {})

# 2. ADMIN-LOGIN
@router.post("/buergerverwaltung/admin")
async def admin_login(username: str = Form(...), password: str = Form(...)):
    print(f"🔍 Admin-Login: {username}")  # DEBUG
    VALID_ADMINS = {"admin": "admin123"}
    if username not in VALID_ADMINS or VALID_ADMINS[username] != password:
        print(f"❌ Login fehlgeschlagen: {username}")  # DEBUG
        raise HTTPException(status_code=401, detail="Ungültige Admin-Daten")
    
    token = create_token(user_id=username)
    print(f"✅ Admin-Token: {token[:20]}...")  # DEBUG
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "admin"
    }

# 3. BÜRGER-LOGIN
@router.post("/buergerverwaltung/buerger")
async def buerger_login(email: str = Form(...), password: str = Form(...)):
    print(f"🔍 Bürger-Login: {email}")  # DEBUG
    init_repo()
    buerger = next((b for b in repo.lade_alle() if b.email == email), None)
    if not buerger or not verify_password(password, buerger.authentifizierungsdaten):
        print(f"❌ Bürger-Login fehlgeschlagen: {email}")  # DEBUG
        raise HTTPException(status_code=401, detail="Bürger oder Passwort falsch")
    
    token = create_token(user_id=f"buerger_{buerger.buergerID}")
    print(f"✅ Bürger-Token: {token[:20]}...")  # DEBUG
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "buerger",
        "name": buerger.name
    }
