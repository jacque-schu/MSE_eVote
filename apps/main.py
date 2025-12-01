from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jinja2 import Environment, FileSystemLoader, select_autoescape

from apps.buergerverwaltung.interfaces.rest.buerger_endpoints import router as buerger_router
from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import (
    AbstimmungsUebersichtsService,
)
from apps.abstimmungsmanagement.infrastructure.repositories.abstimmung_repository import (
    InMemoryAbstimmungRepository,
)

# -------------------------------------------------------------------------
# Dependencies
# -------------------------------------------------------------------------
def get_abstimmungs_service() -> AbstimmungsUebersichtsService:
    return AbstimmungsUebersichtsService(InMemoryAbstimmungRepository())

# -------------------------------------------------------------------------
# Basispfade
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Projektroot

# -------------------------------------------------------------------------
# Templating
#   - Einzelne Loader bleiben für BC-spezifische Views.
#   - Zusätzlich: gemeinsamer Loader, damit Partials aus anderen Ordnern
#     (z. B. "abstimmungsmanagement/partials") überall importierbar sind.
# -------------------------------------------------------------------------
ui_templates = Jinja2Templates(directory=BASE_DIR / "apps" / "ui" / "common" / "templates")
ui_templates_buergerverwaltung = Jinja2Templates(directory=BASE_DIR / "apps" / "ui" / "buergerverwaltung" / "templates")
ui_templates_abstimmungen = Jinja2Templates(directory=BASE_DIR / "apps" / "ui" / "abstimmungsmanagement" / "templates")

templates_env = Environment(
    loader=FileSystemLoader([
        BASE_DIR / "apps" / "ui" / "common" / "templates",
        BASE_DIR / "apps" / "ui" / "abstimmungsmanagement" / "templates",
        BASE_DIR / "apps" / "ui" / "buergerverwaltung" / "templates",
    ]),
    autoescape=select_autoescape(["html", "xml"]),
)
ui_templates_all = Jinja2Templates(env=templates_env)

# -------------------------------------------------------------------------
# Haupt-App
# -------------------------------------------------------------------------
app = FastAPI(title="MSE evote")
app.include_router(buerger_router)

# Statische Dateien (CSS, JS, Bilder)
app.mount("/static/common",
          StaticFiles(directory=BASE_DIR / "apps" / "ui" / "common" / "styles"),
          name="static_common")
app.mount("/static/buergerverwaltung",
          StaticFiles(directory=BASE_DIR / "apps" / "ui" / "buergerverwaltung" / "styles"),
          name="static_buergerverwaltung")
app.mount("/static/abstimmungsmanagement",
          StaticFiles(directory=BASE_DIR / "apps" / "ui" / "abstimmungsmanagement" / "styles"),
          name="static_abstimmungsmanagement")

# -------------------------------------------------------------------------
# Health & Ping
# -------------------------------------------------------------------------
@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# -------------------------------------------------------------------------
# Pages
# -------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return ui_templates.TemplateResponse("auth_choice.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def auth_alias(request: Request):
    return ui_templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return ui_templates.TemplateResponse("login.html", {"request": request})

@app.get("/registrierung", response_class=HTMLResponse)
async def registrierung_startseite(request: Request):
    return ui_templates_buergerverwaltung.TemplateResponse("registrierung.html", {"request": request})

@app.get("/startseite", response_class=HTMLResponse)
async def startseite(
    request: Request,
    service: AbstimmungsUebersichtsService = Depends(get_abstimmungs_service),
):
    # Achtung: Startseite importiert Partials aus anderen Ordnern.
    abstimmungen = service.alle_offenen_abstimmungen()
    return ui_templates_all.TemplateResponse(
        "startseite.html",
        {"request": request, "abstimmungen": abstimmungen, "title": "Übersicht"},
    )

@app.get("/abstimmungen", response_class=HTMLResponse)
async def list_abstimmungen(
    request: Request,
    service: AbstimmungsUebersichtsService = Depends(get_abstimmungs_service),
):
    abstimmungen = service.alle_offenen_abstimmungen()
    return ui_templates_abstimmungen.TemplateResponse(
        "abstimmungen.html",
        {"request": request, "title": "Abstimmungen", "abstimmungen": abstimmungen},
    )
