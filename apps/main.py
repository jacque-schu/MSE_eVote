from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.buergerverwaltung.api.v1.main import app as registrierung_app

# -----------------------------------------------------------------------------
# Basispfade
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Projektroot

# Templates:
#   - Hauptportal & Auth & Login: apps/templates/...
#   - Registrierung:              apps/buergerverwaltung/templates/...
haupt_templates = Jinja2Templates(directory=BASE_DIR / "apps" / "templates")
registrierung_templates = Jinja2Templates(
    directory=BASE_DIR / "apps" / "buergerverwaltung" / "templates"
)

# -----------------------------------------------------------------------------
# Haupt-App
# -----------------------------------------------------------------------------
app = FastAPI(title="eVote - Hauptportal")

# Statische Dateien (CSS etc.) -> ./static
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Optional: API-Unter-App unter einem eigenen Pfad (z.B. /registrierung/api)
app.mount("/registrierung/api", registrierung_app)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# --------------------------------------------------------------------------
# 1) Einstiegsseite: Auth-Auswahl (kommt als erstes)
#    -> erreichbar unter "/" und "/auth"
# --------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
@app.get("/auth", response_class=HTMLResponse)
async def auth_choice(request: Request):
    """
    Vorschalt-Seite:
    - Anmelden
    - Registrieren
    - Demo: Startseite ansehen (ohne Login)
    """
    return haupt_templates.TemplateResponse(
        "auth_choice.html",
        {"request": request},
    )


# --------------------------------------------------------------------------
# 2) Demo-Startseite: zeigt Umfragen, aber ohne Login-Pflicht
# --------------------------------------------------------------------------
@app.get("/startseite", response_class=HTMLResponse)
async def startseite(request: Request):
    """
    Demo-Startseite mit Übersicht über Umfragen.
    Kein Login notwendig.
    """
    return haupt_templates.TemplateResponse(
        "startseite.html",
        {"request": request},
    )


# --------------------------------------------------------------------------
# 3) Registrierung: Bürger registrieren
# --------------------------------------------------------------------------
@app.get("/registrierung", response_class=HTMLResponse)
async def registrierung_startseite(request: Request):
    """HTML-Seite für die Registrierung."""
    return registrierung_templates.TemplateResponse(
        "registrierung.html",
        {"request": request},
    )
