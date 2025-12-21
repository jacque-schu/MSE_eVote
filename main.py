from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.buergerverwaltung.interfaces.rest.buerger_endpoints import router as buerger_router
from apps.authentifizierung.interfaces.rest.auth_endpoints import router as auth_router
from apps.abstimmungsmanagement.interfaces.abstimmung_endpoints import router as abstimmung_router

app = FastAPI(title="MSE eVote")
BASE_DIR = Path(__file__).resolve().parent

templates_common = Jinja2Templates(directory=BASE_DIR / "ui" / "common" / "templates")
templates_abst = Jinja2Templates(directory=BASE_DIR / "ui" / "abstimmung" / "templates")

def is_partial(request: Request) -> bool:
    return request.query_params.get("partial") == "1" or request.headers.get("X-Partial") == "1"



# Static
app.mount("/static/common", StaticFiles(directory=BASE_DIR / "ui" / "common" / "static"), name="static_common")
app.mount("/static/buergerverwaltung", StaticFiles(directory=BASE_DIR / "ui" / "buergerverwaltung" / "static"), name="static_buergerverwaltung")
app.mount("/static/authentifizierung", StaticFiles(directory=BASE_DIR / "ui" / "authentifizierung" / "static"), name="static_authentifizierung")
app.mount("/static/abstimmung", StaticFiles(directory=BASE_DIR / "ui" / "abstimmung" / "static"), name="static_abstimmung")

# Startseite
@app.get("/", response_class=HTMLResponse)
@app.get("/startseite", response_class=HTMLResponse)
async def startseite(request: Request):
    if is_partial(request):
        return templates_common.TemplateResponse("startseite.partial.html", {"request": request})
    return templates_common.TemplateResponse("startseite.html", {"request": request})

# Erstellen (Abstimmung neu)
@app.get("/ui/abstimmung/neu", response_class=HTMLResponse)
async def abstimmung_neu(request: Request):
    if is_partial(request):
        return templates_abst.TemplateResponse("abstimmung_neu.partial.html", {"request": request})
    return templates_abst.TemplateResponse("abstimmung_neu.html", {"request": request})
# Router
app.include_router(auth_router)
app.include_router(buerger_router)
app.include_router(abstimmung_router)