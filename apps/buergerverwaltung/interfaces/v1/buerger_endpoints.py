from pathlib import Path
import logging

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from apps.buergerverwaltung.domain.entities.buerger import Buerger, lade_buerger_db, speichere_buerger_db
from apps.buergerverwaltung.application.services import Registrierungsservice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/api/v1/buerger", tags=["Buerger"])

# Templates
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# Globale DB + Service
buerger_db = None
registrierungs_service = None


def init_buerger_db():
    global buerger_db, registrierungs_service
    if buerger_db is None:
        buerger_db = lade_buerger_db()
    if registrierungs_service is None:
        registrierungs_service = Registrierungsservice(buerger_db)


@router.get("/registrierung", response_class=HTMLResponse)
async def registrierung_seite(request: Request):
    return templates.TemplateResponse(
        "registrierung.html",
        {"request": request, "fehler": [], "form": {}},
    )


@router.post("/formular", response_class=HTMLResponse)
async def registriere_buerger_formular(
    request: Request,
    vorname: str = Form(...),
    nachname: str = Form(...),
    adresse: str = Form(...),
    geburtsdatum: str = Form(...),
    email: str = Form(...),
    authentifizierungsdaten: str = Form(...),
    buergerID: int = Form(1),
):
    init_buerger_db()

    name = f"{vorname} {nachname}"
    fehler: list[str] = []
    fehler.append("TEST aus Backend")

    try:
        # Pydantic prüft Name, Adresse, Geburtsdatum, Email wie in test_buerger.py
        neuer_buerger = Buerger(
            buergerID=buergerID,
            name=name,
          adresse=adresse,
            geburtsdatum=geburtsdatum,  # String → wird im Modell geparst/validiert
            email=email,
            authentifizierungsdaten=authentifizierungsdaten,
        )

        # Domain-/Anwendungslogik: Duplikat-E-Mail prüfen
        registrierungs_service.registriere_buerger(neuer_buerger)
        speichere_buerger_db(buerger_db)

    except ValidationError as ve:
        logger.error(f"Pydantic ValidationError: {ve}")
        for err in ve.errors():
            feld = err.get("loc", ["?"])[0]
            msg = err.get("msg", "Ungültige Eingabe")
            fehler.append(f"{feld}: {msg}")
    except ValueError as e:
        # z.B. "Ein Bürger mit der E-Mail ... existiert bereits!"
        logger.error(f"ValueError im Registrierungsservice: {e}")
        fehler.append(str(e))
    except Exception as e:
        logger.error(f"Unerwarteter Fehler bei der Registrierung: {e}")
        fehler.append("Es ist ein unerwarteter Fehler aufgetreten.")

    if fehler:
        return templates.TemplateResponse(
            "registrierung.html",
            {
                "request": request,
                "fehler": fehler,
                "form": {
                    "vorname": vorname,
                    "nachname": nachname,
                    "adresse": adresse,
                    "geburtsdatum": geburtsdatum,
                    "email": email,
                    "authentifizierungsdaten": authentifizierungsdaten,
                },
            },
        )

    return HTMLResponse(
        f"<html><body style='font-family: Arial; text-align:center;'>"
        f"<h2>Bürger {vorname} {nachname} erfolgreich registriert!</h2>"
        f"</body></html>"
    )
