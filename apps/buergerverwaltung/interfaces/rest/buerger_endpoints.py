from fastapi import APIRouter, Request, Form, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import date
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository
from apps.buergerverwaltung.domain.models.buerger import Buerger
from apps.shared.aspects.auth_aspect import fastapi_auth_check, hash_password




router = APIRouter(prefix="/api/buergerverwaltung", tags=["Buergerverwaltung"])



DB_DATEIPFAD = Path(__file__).parent.parent.parent / "infrastructure" / "persistence" / "buerger_db.json"
repo = None

def init_repo():
    global repo
    if repo is None:
        repo = BuergerRepository(str(DB_DATEIPFAD))

@router.post("/registrierung")
@fastapi_auth_check
async def registriere_buerger_api(
    request: Request,
    vorname: str = Form(...),
    nachname: str = Form(...),
    adresse: str = Form(...),
    geburtsdatum: str = Form(...),
    email: str = Form(...),
    authentifizierungsdaten: str = Form(...),
    authorization: str = Header(None),   # <-- hier
):
    print("ENDPOINT DEBUG header:", repr(authorization))
    
    init_repo()

    # Namen aus vorname + nachname zusammensetzen
    name = f"{vorname} {nachname}".strip()

    if any(b.email == email for b in repo.lade_alle()):
        raise HTTPException(409, detail="E-Mail bereits registriert")

    pw_hash = hash_password(authentifizierungsdaten)

    # ID aus Repository holen
    neue_id = repo.naechste_buerger_id()

    buerger = Buerger(
        buergerID=neue_id,
        name=name,
        adresse=adresse,
        geburtsdatum=geburtsdatum,
        email=email,
        authentifizierungsdaten=pw_hash,
    )

    repo.fuege_hinzu(buerger)
    return {"message": f"Bürger '{buerger.name}' erfolgreich registriert"}


@router.get("/registrierung", response_class=HTMLResponse)
async def registrierung_seite(request: Request):
    templates = Jinja2Templates(directory="ui/buergerverwaltung/templates")
    return templates.TemplateResponse("registrierung.html", {"request": request})

@router.get("/ui/registrierung", response_class=HTMLResponse)
async def registrierung_ui(request: Request):
    templates = Jinja2Templates(directory="ui/buergerverwaltung/templates")
    return templates.TemplateResponse("registrierung.html", {"request": request})

