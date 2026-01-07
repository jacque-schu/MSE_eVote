from datetime import date, timedelta
from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import AbstimmungsUebersichtsService
from apps.abstimmungsmanagement.infrastructure.container.container import get_uebersichts_service
from apps.abstimmungsmanagement.infrastructure.auth.abstimmung_auth import require_login

router = APIRouter(tags=["ui"])

BASE_DIR = Path(__file__).resolve().parents[3]  # ggf. anpassen
templates = Jinja2Templates(directory=BASE_DIR / "ui" / "common" / "templates")

@router.get("/", response_class=HTMLResponse)
@router.get("/startseite", response_class=HTMLResponse)
async def startseite(
    request: Request,
    uebersicht: AbstimmungsUebersichtsService = Depends(get_uebersichts_service),
):
    current_user = None
    try:
        current_user = await require_login(request)
    except Exception:
        pass

    offene = uebersicht.alle_offenen_abstimmungen()

    heute = date.today()
    grenze = heute + timedelta(days=7)

    laufende_7tage = [
        {"abstimmungsID": a.abstimmungsID,"titel": a.titel, "endDatum": a.endDatum}
        for a in offene
        if getattr(a, "endDatum", None) is not None and heute <= a.endDatum <= grenze
    ]
    laufende_7tage.sort(key=lambda x: x["endDatum"])

    return templates.TemplateResponse(
        name="startseite.html",
        request=request,
        context={"request": request, "current_user": current_user, "laufende_7tage": laufende_7tage},
    )
