from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="MSE eVote")

BASE_DIR = Path(__file__).resolve().parent  # absoluter Pfad
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

static_dir = BASE_DIR / "static"
if static_dir.exists():  # nur mounten, wenn der Ordner vorhanden ist
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "MSE eVote", "subtitle": "Einfach abstimmen. Klar auswerten."}
    )

@app.get("/health")
def health():
    return {"status": "ok"}
