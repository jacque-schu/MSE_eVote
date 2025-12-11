from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import urlencode
from apps.abstimmungsmanagement.application.services.abstimmungs_service import AbstimmungsService
from apps.abstimmungsmanagement.domain.models.abstimmung import Stimmoption
from pydantic import BaseModel
from apps.abstimmungsmanagement.infrastructure.templates.templates import templates_abst
from apps.abstimmungsmanagement.infrastructure.container import get_abstimmungs_service


router = APIRouter(tags=["abstimmungen"])

# --- JSON-API ---

@router.post("/abstimmungen/seed")
def seed(service: AbstimmungsService = Depends(get_abstimmungs_service)):
    abstimmung = service.erstelle_abstimmung(
        abstimmungsID=100,
        titel="Kommunalwahl 2026",
        beschreibung="Soll es eine Briefwahl geben?",
        startDatum=date.today(),
        endDatum=date.today() + timedelta(days=7),
        teilnehmerliste=[1, 2, 3],
        stimmen=[],
    )
    return abstimmung


@router.get("/abstimmungen", response_model=List[dict])
def liste_abstimmungen(service: AbstimmungsService = Depends(get_abstimmungs_service)):
    return [a.__dict__ for a in service.liste_abstimmungen()]


@router.get("/abstimmungen/{abstimmungs_id}")
def get_abstimmung(
    abstimmungs_id: int,
    service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmung = service.abst_repo.get(abstimmungs_id)
    return abstimmung.__dict__


@router.post("/abstimmungen/{abstimmungs_id}/stimme")
def stimme_abgeben_endpoint(
    abstimmungs_id: int,
    wahl: str = Form(...),
    service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    option = Stimmoption[wahl]
    try:
        service.stimme_abgeben(
            abstimmungs_id=abstimmungs_id,
            buerger_id=1,  # später durch Login-Bürger-ID ersetzen
            option=option,
            datum=date.today(),
        )
        # Redirect zurück auf die HTML-Detailansicht
        return RedirectResponse(
            url=f"/ui/abstimmung/{abstimmungs_id}",
            status_code=303,
        )
    except ValueError as e:
        params = urlencode({"error": str(e)})
        return RedirectResponse(
            url=f"/ui/abstimmung/{abstimmungs_id}?{params}",
            status_code=303,
        )


@router.get("/ui/abstimmungsuebersicht", response_class=HTMLResponse)
async def abstimmungsuebersicht(
    request: Request,
    service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmungen = service.liste_abstimmungen()
    return templates_abst.TemplateResponse(
        "abstimmungsuebersicht.html",
        {"request": request, "abstimmungen": abstimmungen},
    )


@router.get("/ui/abstimmung/{abstimmungs_id}", response_class=HTMLResponse)
async def abstimmungs_detail(
    request: Request,
    abstimmungs_id: int,
    service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmung = service.abst_repo.get(abstimmungs_id)
    fehlermeldung: Optional[str] = request.query_params.get("error")
    return templates_abst.TemplateResponse(
        "abstimmungsdetail.html",
        {
            "request": request,
            "abstimmung": abstimmung,
            "fehlermeldung": fehlermeldung,
        },
    )


class AbstimmungCreate(BaseModel):
    abstimmungsID: int
    titel: str
    beschreibung: str
    startDatum: date
    endDatum: date
    mindestalter: int | None = None

# JSON-API: Admin legt Abstimmung an
@router.post("/abstimmungen", response_model=dict)
def create_abstimmung(
    payload: AbstimmungCreate,
    service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmung = service.erstelle_abstimmung(**payload.dict(), stimmen=[])
    return abstimmung.__dict__

# HTML-Form anzeigen
@router.get("/ui/admin/abstimmungen/neu", response_class=HTMLResponse)
async def abstimmung_neu_form(request: Request):
    return templates_abst.TemplateResponse(
        "abstimmung_neu.html",
        {"request": request},
    )

# HTML-Form verarbeiten
@router.post("/ui/admin/abstimmungen/neu")
async def abstimmung_neu_submit(
    abstimmungsID: int | None = Form(None),
    titel: str = Form(...),
    beschreibung: str = Form(...),
    startDatum: date = Form(...),
    endDatum: date = Form(...),
    minAlter: int | None = Form(None),
    service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    # falls keine ID mitgekommen ist → automatisch vergeben
    if abstimmungsID is None:
        vorhandene = service.liste_abstimmungen()
        max_id = max((a.abstimmungsID for a in vorhandene), default=0)
        abstimmungsID = max_id + 1  # erste Abstimmung → 1

    abstimmung = service.erstelle_abstimmung(
        abstimmungsID=abstimmungsID,
        titel=titel,
        beschreibung=beschreibung,
        startDatum=startDatum,
        endDatum=endDatum,
        teilnehmerliste=[],
        stimmen=[],
        mindestalter=minAlter,
    )
    return RedirectResponse(
        url="/ui/abstimmungsuebersicht",
        status_code=303,
    )




