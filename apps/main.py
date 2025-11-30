from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.buergerverwaltung.interfaces.rest.buerger_endpoints import router as buerger_router

# -------------------------------------------------------------------------
# Basispfade
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Projektroot

# UI Templates liegen bspw. hier:
# src/ui/common/templates/auth_choice.html
# src/ui/common/templates/login.html
# src/ui/common/templates/startseite.html
# BC-spezifische Templates z.B. in src/ui/buergerverwaltung/templates/
ui_templates = Jinja2Templates(directory=BASE_DIR / "apps" / "ui" / "common" / "templates")
ui_templates_buergerverwaltung = Jinja2Templates(directory=BASE_DIR / "apps" / "ui" / "buergerverwaltung" / "templates")


# -------------------------------------------------------------------------
# Haupt-App
# -------------------------------------------------------------------------
app = FastAPI(title="MSE evote")
app.include_router(buerger_router)

# Statische Dateien (CSS, JS, Bilder) -> src/ui/common/styles und src/ui/<bc>/styles
app.mount("/static/common", StaticFiles(directory=BASE_DIR / "apps" / "ui" / "common" / "styles"), name="static_common")
app.mount("/static/buergerverwaltung", StaticFiles(directory=BASE_DIR / "apps" / "ui" /"buergerverwaltung" / "styles"), name="static_buergerverwaltung")



@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# -------------------------------------------------------------------------
# Einstiegsseite: Auth-Auswahl (kommt als erstes)
# -------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return ui_templates.TemplateResponse("auth_choice.html", {"request": request})

# Optionaler Alias /auth -> login.html
@app.get("/auth", response_class=HTMLResponse)
async def auth_alias(request: Request):
    return ui_templates.TemplateResponse("login.html", {"request": request})

# Login (GET) – gleiche Seite wie Root
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return ui_templates.TemplateResponse("login.html", {"request": request})

# Registrierung: Bürger registrieren (BC Bürgerverwaltung)
@app.get("/registrierung", response_class=HTMLResponse)
async def registrierung_startseite(request: Request):
    return ui_templates_buergerverwaltung.TemplateResponse("registrierung.html", {"request": request})

# Startseite (Demo/Übersicht)
@app.get("/startseite", response_class=HTMLResponse)
async def startseite(request: Request):
    return ui_templates.TemplateResponse("startseite.html", {"request": request})
