from pathlib import Path
from typing import Annotated
from datetime import date, timedelta

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

# Router Imports
from apps.authentifizierung.interfaces.rest.auth_endpoints import router as auth_router
from apps.buergerverwaltung.interfaces.rest.buerger_endpoints import router as buerger_router
from apps.abstimmungsmanagement.interfaces.abstimmung_endpoints import router as abstimmung_router
from ui.common.interfaces.ui_endpoints import router as ui_router  # ✅ EINMAL!

# Dependencies
from dependencies import get_buerger_repo
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository


app = FastAPI(title="MSE eVote")
BASE_DIR = Path(__file__).resolve().parent

# Templates (unverändert)
templates = Jinja2Templates(directory=BASE_DIR / "ui")

def get_buerger_repo() -> IBuergerRepository:
    db_path = BASE_DIR / "apps" / "buergerverwaltung" / "infrastructure" / "persistence" / "buerger_db.json"
    return BuergerRepository(str(db_path))  # ← Vollständiger Pfad!
 

app.include_router(auth_router)
app.include_router(buerger_router, prefix="/api/buergerverwaltung")

# UI zuerst
app.include_router(ui_router, prefix="/ui")

# Fachliche UI-Endpunkte (Abstimmung)
app.include_router(abstimmung_router, prefix="/ui")


app.mount("/static_common", StaticFiles(directory=BASE_DIR / "ui" / "common" / "static"), name="static_common")
app.mount("/static_authentifizierung", StaticFiles(directory=BASE_DIR / "ui" / "authentifizierung" / "static"), name="static_authentifizierung")
app.mount("/static_abstimmung", 
          StaticFiles(directory=BASE_DIR / "ui" / "abstimmung" / "static"), 
          name="static_abstimmung")
app.mount("/static_buergerverwaltung", 
          StaticFiles(directory=BASE_DIR / "ui" / "buergerverwaltung" / "static"), 
          name="static_buergerverwaltung")


@app.get("/startseite", response_class=HTMLResponse)
async def startseite_redirect():
    return RedirectResponse(url="/ui/startseite")  # ← Automatischer Redirect


# Health (unverändert)
@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/health")
async def health():
    return {"status": "ok"}
