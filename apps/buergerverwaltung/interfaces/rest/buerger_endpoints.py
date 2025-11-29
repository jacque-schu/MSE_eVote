from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from pathlib import Path

from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository
from apps.buergerverwaltung.application.services.registrierungs_service import Registrierungsservice
from apps.buergerverwaltung.domain.models.buerger import Buerger

router = APIRouter(prefix="/api/v1/buerger", tags=["Buerger"])

DB_DATEIPFAD = Path(__file__).parent.parent.parent / "infrastructure" / "persistence" / "buerger_db.json"

# Globale Service-Variable
registrierungs_service = None

def init_buerger_db():
    global registrierungs_service
    if registrierungs_service is None:
        repository = BuergerRepository(str(DB_DATEIPFAD))
        registrierungs_service = Registrierungsservice(repository)

# Beispiel-Endpunkt (weiter Endpunkte folgen entsprechend)
@router.get("/registrierung", response_class=HTMLResponse)
async def registrierung_seite(request: Request):
    init_buerger_db()
    templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent.parent / "ui" / "common" / "templates")
    return templates.TemplateResponse("registrierung.html", {"request": request})
