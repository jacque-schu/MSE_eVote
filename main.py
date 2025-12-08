from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apps.buergerverwaltung.interfaces.rest.buerger_endpoints import router as buerger_router
from apps.authentifizierung.interfaces.rest.auth_endpoints import router as auth_router

app = FastAPI(title="MSE eVote")
#BASE_DIR = Path(__file__).resolve().parent.parent  # MSE_eVote/
BASE_DIR = Path(__file__).resolve().parent

# Router
app.include_router(auth_router)
app.include_router(buerger_router)

# Static Files → ROOT ui/!
app.mount("/static/common", StaticFiles(directory=BASE_DIR / "ui" / "common"), name="static_common")
app.mount("/static/buergerverwaltung", StaticFiles(directory=BASE_DIR / "ui" / "buergerverwaltung"), name="static_buergerverwaltung")


# Health
@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Startseite → ROOT ui/!
@app.get("/", response_class=HTMLResponse)
@app.get("/startseite", response_class=HTMLResponse)
async def startseite(request: Request):
    templates = Jinja2Templates(directory=BASE_DIR / "ui" / "common" / "templates")
    return templates.TemplateResponse(request, "startseite.html", {"request": request})
