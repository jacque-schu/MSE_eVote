from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.buergerverwaltung.interfaces.v1.buerger_endpoints import router as buerger_router

# -------------------------------------------------------------------------
# Basispfade
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Projektroot

# Alle HTML-Seiten (login, registrierung, startseite) liegen hier:
# apps/ui/templates/login.html
# apps/ui/templates/registrierung.html
# apps/ui/templates/startseite.html
ui_templates = Jinja2Templates(directory=BASE_DIR / "apps" / "ui" / "templates")

# -------------------------------------------------------------------------
# Haupt-App
# -------------------------------------------------------------------------
app = FastAPI(title="MSE evote")
app.include_router(buerger_router)

# Statische Dateien (CSS, JS, Bilder) -> ./static
app.mount("/static", StaticFiles(directory=BASE_DIR / "apps" / "static"), name="static")


@app.get("/ping")
async def ping():
    return {"msg": "pong"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# -------------------------------------------------------------------------
# 1) Root: Login-Seite
# -------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Beim Aufruf von http://127.0.0.1:8000 -> login.html
    return ui_templates.TemplateResponse("login.html", {"request": request})


# Optionaler Alias /auth -> ebenfalls login.html
@app.get("/auth", response_class=HTMLResponse)
async def auth_alias(request: Request):
    return ui_templates.TemplateResponse("login.html", {"request": request})


# -------------------------------------------------------------------------
# 2) Login (GET) – gleiche Seite wie Root
# -------------------------------------------------------------------------
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return ui_templates.TemplateResponse("login.html", {"request": request})


# -------------------------------------------------------------------------
# 3) Registrierung: Bürger registrieren
# -------------------------------------------------------------------------
@app.get("/registrierung", response_class=HTMLResponse)
async def registrierung_startseite(request: Request):
    return ui_templates.TemplateResponse("registrierung.html", {"request": request})


# -------------------------------------------------------------------------
# 4) Startseite (Demo/Übersicht)
# -------------------------------------------------------------------------
@app.get("/startseite", response_class=HTMLResponse)
async def startseite(request: Request):
    return ui_templates.TemplateResponse("startseite.html", {"request": request})
