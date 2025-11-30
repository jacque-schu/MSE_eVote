from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from pathlib import Path
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository
from apps.buergerverwaltung.application.services.registrierungs_service import Registrierungsservice
from apps.buergerverwaltung.domain.models.buerger import Buerger
from fastapi import Header, HTTPException

router = APIRouter(prefix="/api/buergerverwaltung", tags=["Buergerverwaltung"])


DB_DATEIPFAD = Path(__file__).parent.parent.parent / "infrastructure" / "persistence" / "buerger_db.json"

# Globale Service-Variable
registrierungs_service = None

def init_buerger_db():
    global registrierungs_service
    if registrierungs_service is None:
        repository = BuergerRepository(str(DB_DATEIPFAD))
        registrierungs_service = Registrierungsservice(repository)

@router.post("/registrierung")
async def registriere_buerger_api(
    request: Request,
    name: str = Form(...),
    adresse: str = Form(...),
    geburtsdatum: str = Form(...),
    email: str = Form(...),
    authentifizierungsdaten: str = Form(...),
    authorization: str = Header(None)  # Liest den Authorization-Header aus
):
    init_buerger_db()

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization Header fehlt")

    # Erwartet Bearer-Token z.B. "Bearer eyJhbGciOiJIUzI1NiIsInR..."
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Ungültiger Authorization Header")

    buerger = Buerger(
        buergerID=0,  # ID ggf. automatisch generieren oder weglassen
        name=name,
        adresse=adresse,
        geburtsdatum=geburtsdatum,
        email=email,
        authentifizierungsdaten=authentifizierungsdaten
    )

    registrierter_buerger = registrierungs_service.registriere_buerger(
        buerger, auth_token=token
    )

    return {"message": "Bürger registriert", "buerger": registrierter_buerger}


@router.get("/registrierung", response_class=HTMLResponse)
async def registrierung_seite(request: Request):
    init_buerger_db()
    templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent.parent / "ui" / "buergerverwaltung" / "templates")
    return templates.TemplateResponse("registrierung.html", {"request": request})
