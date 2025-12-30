from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import urlencode
from pydantic import BaseModel

from apps.abstimmungsmanagement.application.services.abstimmungs_service import AbstimmungsService
from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import AbstimmungsUebersichtsService
from apps.abstimmungsmanagement.application.services.ergebnis_service import ErgebnisService
from apps.abstimmungsmanagement.domain.models.abstimmung import Stimmoption
from apps.abstimmungsmanagement.infrastructure.templates.templates import templates_abst
from apps.abstimmungsmanagement.infrastructure.container.container import (
    get_abstimmungs_service,
    get_uebersichts_service,
    get_ergebnis_service,
)
from apps.abstimmungsmanagement.infrastructure.auth.abstimmung_auth import require_login

# Die Datei bündelt alle HTTP‑Endpunkte („Routen“) rund um Abstimmungen.

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

# Liefert das Ergebnis einer Abstimmung als JSON (API).
@router.get("/abstimmungen/{abstimmungs_id}/ergebnis", response_model=List[dict])
async def get_abstimmung_ergebnis(
        request: Request,
        abstimmungs_id: int,
        ergebnis_service: ErgebnisService = Depends(get_ergebnis_service),
):
    await require_login(request)
    return ergebnis_service.hole_ergebnis_details_fuer_abstimmung(abstimmungs_id)

# Nimmt eine Stimme zu einer Abstimmung entgegen (Form‑POST) und leitet zurück zur HTML-Detailseite.
@router.post("/abstimmungen/{abstimmungs_id}/stimme")
async def stimme_abgeben_endpoint(
        abstimmungs_id: int,
        wahl: str = Form(...),
        current_user=Depends(require_login),  # ← FERTIG!
        service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    if current_user["role"] != "buerger":
        raise HTTPException(403, "Nur Bürger dürfen abstimmen! Bitte als Bürger einloggen.")
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
async def abstimmungsuebersicht(request: Request,
                                service: AbstimmungsUebersichtsService = Depends(get_uebersichts_service)):
    abstimmungen = service.alle_offenen_abstimmungen()

    try:
        user = await require_login(request)
        is_admin = user["role"] == "admin"
    except HTTPException:
        is_admin = False

    # ✅ NEU: Sortierung nach Ablaufdatum (endDatum) -> nächstes Ende zuerst
    # und Mapping auf startdatum/ablaufdatum für das Template.
    def end_key(a):
        end_dt = getattr(a, "endDatum", None)
        return end_dt if end_dt is not None else date.max

    abstimmungen_sorted = sorted(abstimmungen, key=end_key)  # [web:108]

    abstimmungen_view = []
    for a in abstimmungen_sorted:
        abstimmungen_view.append({
            "abstimmungsID": a.abstimmungsID,
            "titel": a.titel,

            # Template kann dann nutzen:
            # {{ a.startdatum.strftime('%d.%m.%Y') }}
            # {{ a.ablaufdatum.strftime('%d.%m.%Y') }}
            "startdatum": getattr(a, "startDatum", None),
            "ablaufdatum": getattr(a, "endDatum", None),
        })

    return templates_abst.TemplateResponse(
        "abstimmungsuebersicht.html",
        {"request": request, "abstimmungen": abstimmungen_view, "is_admin": is_admin},
    )

# Zeigt die HTML‑Detailansicht einer Abstimmung, optional mit Fehlermeldung.
@router.get("/ui/abstimmung/{abstimmungs_id}", response_class=HTMLResponse)
async def abstimmungs_detail(
        request: Request,
        abstimmungs_id: int,
        service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    abstimmung = service.abst_repo.get(abstimmungs_id)
    fehlermeldung = request.query_params.get("error")

    user = None
    try:
        user = await require_login(request)
    except HTTPException:
        pass

    return templates_abst.TemplateResponse(
        "abstimmungsdetail.html",
        {
            "request": request,
            "abstimmung": abstimmung,
            "fehlermeldung": fehlermeldung,
            "is_logged_in": user is not None,
            "current_user": user
        },
    )

# Zeigt die HTML‑Ergebnisansicht einer Abstimmung.
@router.get("/ui/abstimmung/{abstimmungs_id}/ergebnis", response_class=HTMLResponse)
async def abstimmungs_ergebnis_view(
        request: Request,
        abstimmungs_id: int,
        abstimmungs_service: AbstimmungsService = Depends(get_abstimmungs_service),
        ergebnis_service: ErgebnisService = Depends(get_ergebnis_service),

):
    # 1. Login erzwingen
    user = await require_login(request)

    # 2. Daten laden
    abstimmung = abstimmungs_service.abst_repo.get(abstimmungs_id)
    ergebnis_details = ergebnis_service.hole_ergebnis_details_fuer_abstimmung(abstimmungs_id)

    #3. Template laden
    return templates_abst.TemplateResponse(
        "abstimmung_ergebnis.html",
        {
            "request": request,
            "abstimmung": abstimmung,
            "ergebnis": ergebnis_details,
            "is_logged_in": True,
            "current_user": user,
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


# GET-Endpunkt (Admin-Check + Formular)
@router.get("/ui/admin/abstimmungen/neu", response_class=HTMLResponse)
async def abstimmung_neu_form(request: Request):
    user = await require_login(request)
    if user["role"] != "admin":
        raise HTTPException(403, "Admin-Zugriff erforderlich")
    return templates_abst.TemplateResponse(
        "abstimmung_neu.html",
        {"request": request}
    )


# POST-Endpunkt (Form-Verarbeitung + Date-Parsing)
@router.post("/ui/admin/abstimmungen/neu")
async def abstimmung_neu_submit(
        abstimmungsID: int | None = Form(None),
        titel: str = Form(...),
        beschreibung: str = Form(...),
        startDatum: str = Form(...),  # ← STRING aus HTML-Form
        endDatum: str = Form(...),  # ← STRING aus HTML-Form
        minAlter: int | None = Form(None),
        service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    # Auto-ID falls keine angegeben
    if abstimmungsID is None:
        vorhandene = service.liste_abstimmungen()
        max_id = max((a.abstimmungsID for a in vorhandene), default=0)
        abstimmungsID = max_id + 1

    service.erstelle_abstimmung(
        abstimmungsID=abstimmungsID,
        titel=titel,
        beschreibung=beschreibung,
        startDatum=date.fromisoformat(startDatum),
        endDatum=date.fromisoformat(endDatum),
        teilnehmerliste=[],
        stimmen=[],
        mindestalter=minAlter,
    )
    return RedirectResponse(url="/ui/abstimmungsuebersicht", status_code=303)
