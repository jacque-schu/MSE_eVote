from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.buergerverwaltung.api.v1.main import app as registrierung_app

# -----------------------------------------------------------------------------
# Basispfade
# -----------------------------------------------------------------------------
# Diese Datei liegt in apps/main.py
BASE_DIR = Path(__file__).resolve().parent.parent  # Projektroot

# Templates:
#   - Hauptportal:   apps/templates/startseite.html
#   - Registrierung: apps/buergerverwaltung/templates/registrierung.html
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


@app.get("/", response_class=HTMLResponse)
async def startseite(request: Request):
    """Hauptseite mit Links auf Registrierung / Abstimmung."""
    return haupt_templates.TemplateResponse(
        "startseite.html",
        {"request": request},
    )


@app.get("/registrierung", response_class=HTMLResponse)
async def registrierung_startseite(request: Request):
    """HTML-Seite für die Registrierung."""
    return registrierung_templates.TemplateResponse(
        "registrierung.html",
        {"request": request},
    )
