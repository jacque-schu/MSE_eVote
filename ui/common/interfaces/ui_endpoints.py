from __future__ import annotations
from datetime import date, timedelta
from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import AbstimmungsUebersichtsService
from apps.abstimmungsmanagement.infrastructure.container.container import get_uebersichts_service
from apps.abstimmungsmanagement.infrastructure.auth.abstimmung_auth import require_login

# Domain/Infra für Services
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository
# ✅ KRITISCH: Für AbstimmungsUebersichtsService & Dependencies
from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import AbstimmungsUebersichtsService
# ✅ Domain Interfaces (für Type-Hints/Services)
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository  # Falls Auth benötigt
from apps.abstimmungsmanagement.infrastructure.auth.abstimmung_auth import require_login_optional


router = APIRouter(tags=["ui"])

BASE_DIR = Path(__file__).resolve().parents[3]  # MSE_eVote Root
templates = Jinja2Templates(directory=BASE_DIR / "ui" / "common" / "templates")  # ui/common/templates/


@router.get("/", response_class=HTMLResponse)
@router.get("/startseite", response_class=HTMLResponse)
async def startseite(
    request: Request,
    uebersicht: AbstimmungsUebersichtsService = Depends(get_uebersichts_service),
    current_user=Depends(require_login_optional),
):
    offene = uebersicht.alle_offenen_abstimmungen()

    heute = date.today()
    grenze = heute + timedelta(days=7)

    laufende_7tage = [
        {"titel": a.titel, "endDatum": a.endDatum}
        for a in offene
        if getattr(a, "endDatum", None) is not None and heute <= a.endDatum <= grenze
    ]
    laufende_7tage.sort(key=lambda x: x["endDatum"])

    return templates.TemplateResponse(
        "startseite.html",
        {
            "request": request,
            "current_user": current_user,
            "laufende_7tage": laufende_7tage,
        },
    )
