from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository
from apps.buergerverwaltung.application.services.buerger_registrierung_service import BuergerRegistrierungService
from pathlib import Path
from dependencies import get_buerger_repo

# ✅ ROUTER DEFINIEREN!
router = APIRouter(tags=["Bürgerverwaltung"])  

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent  # MSE_eVote
TEMPLATES_DIR = BASE_DIR / "ui" / "buergerverwaltung" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

def get_registrierung_service(repo: IBuergerRepository = Depends(get_buerger_repo)):
    return BuergerRegistrierungService(repo)

def get_templates():
    return request.app.state.templates  # Kein Import!

# 1. REGISTRIERUNGSEITE
@router.get("/registrierung", response_class=HTMLResponse)
async def registrierung_seite(request: Request):
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    return templates.TemplateResponse("registrierung.html", {"request": request})  # Korrekte Reihenfolge

# 2. REGISTRIEREN (passt zu deinen Tests!)
@router.post("/registrierung")
async def registriere_buerger(
    vorname: str = Form(...), nachname: str = Form(...), 
    adresse: str = Form(...), geburtsdatum: str = Form(...), 
    email: str = Form(...), authentifizierungsdaten: str = Form(...),
    service: BuergerRegistrierungService = Depends(get_registrierung_service)
):
    try:
        result = service.registriere(vorname, nachname, adresse, geburtsdatum, email, authentifizierungsdaten)
        return {"message": "Registrierung erfolgreich!", "buerger_id": result}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

