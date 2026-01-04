from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.buergerverwaltung.interfaces.rest.buerger_endpoints import router as buerger_router
from apps.authentifizierung.interfaces.rest.auth_endpoints import router as auth_router
from apps.abstimmungsmanagement.interfaces.abstimmung_endpoints import router as abstimmung_router

# ✅ NEU: UI-Router (Startseite) aus ui/common/interfaces/ui_endpoints.py
from ui.common.interfaces.ui_endpoints import router as ui_router


app = FastAPI(title="MSE eVote")
BASE_DIR = Path(__file__).resolve().parent

templates_abst = Jinja2Templates(
    directory=BASE_DIR / "ui" / "abstimmung" / "templates"
)

# Router
app.include_router(auth_router)
app.include_router(buerger_router)
app.include_router(abstimmung_router)
app.include_router(ui_router)  # ✅ jetzt kommen "/" und "/startseite" von ui_endpoints.py [web:158]

# Static Files → ROOT ui/!
app.mount("/static/common", StaticFiles(directory=BASE_DIR / "ui" / "common" / "static"), name="static_common")
app.mount("/static/buergerverwaltung", StaticFiles(directory=BASE_DIR / "ui" / "buergerverwaltung" / "static"), name="static_buergerverwaltung")
app.mount("/static/authentifizierung", StaticFiles(directory=BASE_DIR / "ui" / "authentifizierung" / "static"), name="static_authentifizierung")
app.mount("/static/abstimmung", StaticFiles(directory=BASE_DIR / "ui" / "abstimmung" / "static"), name="static_abstimmung")

# Health
@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/health")
async def health():
    return {"status": "ok"}
