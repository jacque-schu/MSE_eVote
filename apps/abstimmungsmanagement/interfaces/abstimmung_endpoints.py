from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import urlencode
from apps.abstimmungsmanagement.application.services.abstimmungs_service import AbstimmungsService
from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import AbstimmungsUebersichtsService
from apps.abstimmungsmanagement.domain.models.abstimmung import Stimmoption
from pydantic import BaseModel
from apps.abstimmungsmanagement.infrastructure.templates.templates import templates_abst
from apps.abstimmungsmanagement.infrastructure.container.container import get_abstimmungs_service, get_uebersichts_service
from apps.shared.aspects.auth_aspect import is_token_valid
import jwt
from apps.shared.aspects.auth_aspect import SECRET_KEY, ALGORITHM


# Die Datei bündelt alle HTTP‑Endpunkte („Routen“) rund um Abstimmungen.


async def require_login(request: Request):  # ← Request statt token!
    """Login prüfen (Bürger/Admin) mit deiner is_token_valid()"""
    token = request.cookies.get('auth_token')  # ← AUS COOKIE!
    if not token or not is_token_valid(token):
        raise HTTPException(
            status_code=401,
            detail="Bitte loggen Sie sich ein, um Ihre Stimme abzugeben"
        )

    # Payload extrahieren
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return {
        "user_id": payload["sub"],
        "role": payload.get("role", "buerger")
    }

router = APIRouter(tags=["abstimmungen"])


# Listet alle Abstimmungen als JSON auf (für API‑Nutzung).
@router.get("/abstimmungen", response_model=List[dict])
def liste_abstimmungen(service: AbstimmungsService = Depends(get_abstimmungs_service)):
    return [a.__dict__ for a in service.liste_abstimmungen()]


# Liefert die Details einer einzelnen Abstimmung als JSON.
@router.get("/abstimmungen/{abstimmungs_id}")
def get_abstimmung(
        abstimmungs_id: int,
        service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmung = service.abst_repo.get(abstimmungs_id)
    return abstimmung.__dict__




# Nimmt eine Stimme zu einer Abstimmung entgegen (Form‑POST) und leitet zurück zur HTML-Detailseite.
@router.post("/abstimmungen/{abstimmungs_id}/stimme")
async def stimme_abgeben_endpoint(
        abstimmungs_id: int,
        wahl: str = Form(...),
        current_user=Depends(require_login),  # ← FERTIG!
        service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    # Bürger ID extrahieren
    buerger_id = int(current_user["user_id"].replace("buerger_", ""))

    option = Stimmoption[wahl]
    try:
        service.stimme_abgeben(abstimmungs_id, buerger_id, option, date.today())
        return RedirectResponse(url=f"/ui/abstimmung/{abstimmungs_id}", status_code=303)
    except ValueError as e:
        params = urlencode({"error": str(e)})
        return RedirectResponse(url=f"/ui/abstimmung/{abstimmungs_id}?{params}", status_code=303)


# Zeigt eine HTML‑Übersicht aller offenen Abstimmungen.
@router.get("/ui/abstimmungsuebersicht", response_class=HTMLResponse)
async def abstimmungsuebersicht(
    request: Request,
    service: AbstimmungsUebersichtsService = Depends(get_uebersichts_service),  # ← NEU
):
    abstimmungen = service.alle_offenen_abstimmungen()  # ← Nur OFFEN!
    return templates_abst.TemplateResponse(
        "abstimmungsuebersicht.html",
        {"request": request, "abstimmungen": abstimmungen},
    )

# Zeigt die HTML‑Detailansicht einer Abstimmung, optional mit Fehlermeldung.
# Zeigt die HTML‑Detailansicht einer Abstimmung, optional mit Fehlermeldung.
@router.get("/ui/abstimmung/{abstimmungs_id}", response_class=HTMLResponse)
async def abstimmungs_detail(
        request: Request,
        abstimmungs_id: int,
        service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmung = service.abst_repo.get(abstimmungs_id)
    fehlermeldung = request.query_params.get("error")

    # ← ECHTE PRÜFUNG (HARDCODE LÖSCHEN):
    token = request.cookies.get('auth_token')
    is_logged_in = token is not None  # ← Nur wenn Cookie da!

    return templates_abst.TemplateResponse(
        "abstimmungsdetail.html",
        {
            "request": request,
            "abstimmung": abstimmung,
            "fehlermeldung": fehlermeldung,
            "is_logged_in": is_logged_in
        },
    )


class AbstimmungCreate(BaseModel):
    abstimmungsID: int
    titel: str
    beschreibung: str
    startDatum: date
    endDatum: date
    mindestalter: int | None = None


# JSON‑API: Admin legt eine neue Abstimmung an und bekommt sie als JSON zurück.
@router.post("/abstimmungen", response_model=dict)
def create_abstimmung(
        payload: AbstimmungCreate,
        service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmung = service.erstelle_abstimmung(**payload.dict(), stimmen=[])
    return abstimmung.__dict__


# Zeigt das HTML‑Formular, mit dem der Admin eine neue Abstimmung anlegen kann.
@router.get("/ui/admin/abstimmungen/neu", response_class=HTMLResponse)
async def abstimmung_neu_form(request: Request):
    return templates_abst.TemplateResponse(
        "abstimmung_neu.html",
        {"request": request},
    )


# Verarbeitet das HTML‑Formular zur Erstellung einer neuen Abstimmung und leitet zur Übersicht um.
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
    # da es im HTML-Template kein Feld für eine ID gibt, wird die ID automatisch vergeben
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
