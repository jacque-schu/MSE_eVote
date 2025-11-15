from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from apps.buergerverwaltung.domain.entities.buerger import Buerger, lade_buerger_db, speichere_buerger_db
from apps.buergerverwaltung.services.registrierungs_service import Registrierungsservice
from fastapi import APIRouter
from pathlib import Path
import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")





# Erstelle FastAPI-Anwendung und Templates
app = FastAPI(title="Registrierungs-Service")
templates = Jinja2Templates(directory="apps/buergerverwaltung/templates")

# Erstelle eine Instanz des Routers für diese API-Version
router = APIRouter()



# Bürgerdaten laden
buerger_db = lade_buerger_db()
registrierungs_service = Registrierungsservice(buerger_db)

# GET-Route für die Registrierungsseite (zeigt das Formular an)
@router.get("/registrierung", response_class=HTMLResponse)
async def registrierung_seite():
    try:
        file_path = Path(__file__).parent / "templates" / "registrierung.html"
        html_content = file_path.read_text()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"Ein Fehler ist aufgetreten: {str(e)}", status_code=500)


# POST-Route für das Formular (empfängt die Formulardaten)
@router.post("/formular", response_class=HTMLResponse)
async def registriere_buerger_formular(
    request: Request,
    vorname: str = Form(...),
    nachname: str = Form(...),
    adresse: str = Form(...),
    geburtsdatum: str = Form(...),
    email: str = Form(...),
    authentifizierungsdaten: str = Form(...),
    buergerID: int = Form(1)  # Der Wert für die Bürger-ID wird hier gesetzt
):
    # Umwandlung des Geburtsdatums von String in Date-Objekt
    from datetime import date
    geburtsdatum = date.fromisoformat(geburtsdatum)

    # Kombiniere Vorname und Nachname zu einem vollständigen Namen
    name = f"{vorname} {nachname}"

    # Erstelle den neuen Bürger
    neuer_buerger = Buerger(
        buergerID=buergerID,
        name=name,
        adresse=adresse,
        geburtsdatum=geburtsdatum,
        email=email,
        authentifizierungsdaten=authentifizierungsdaten
    )

    # Speichere den neuen Bürger in der DB
    registrierungs_service.registriere_buerger(neuer_buerger)
    speichere_buerger_db(buerger_db)

    # Erfolgsnachricht
    return HTMLResponse(f"""
    <html>
        <body style='font-family: Arial; text-align:center;'>
            <h2>Bürger {vorname} {nachname} erfolgreich registriert!</h2>
        </body>
    </html>
    """)

# Registriere die Routen im FastAPI-Handler
app.include_router(router)