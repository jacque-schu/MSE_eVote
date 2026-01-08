from datetime import date
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from urllib.parse import urlencode
from typing import List

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
from apps.abstimmungsmanagement.infrastructure.auth.abstimmung_auth import require_login, require_login_optional

router = APIRouter(tags=["abstimmungen"])

# -------------------------
# UI: Abstimmungsübersicht
# -------------------------
@router.get("/abstimmungsuebersicht", response_class=HTMLResponse)
async def abstimmungsuebersicht(
    request: Request,
    service: AbstimmungsUebersichtsService = Depends(get_uebersichts_service),
    current_user=Depends(require_login_optional),
):
    offene = service.alle_offenen_abstimmungen()
    geschlossene = service.alle_abgeschlossenen_abstimmungen()

    is_admin = current_user is not None and current_user["role"] == "admin"

    def end_key(a):
        return getattr(a, "endDatum", None) or date.max

    def to_view(items):
        return [
            {
                "abstimmungsID": a.abstimmungsID,
                "titel": a.titel,
                "startdatum": getattr(a, "startDatum", None),
                "ablaufdatum": getattr(a, "endDatum", None),
                "status": a.status.value if getattr(a, "status", None) else "neu",
            }
            for a in sorted(items, key=end_key)
        ]

    return templates_abst.TemplateResponse(
        "abstimmungsuebersicht.html",
        {
            "request": request,
            "abstimmungen_offen": to_view(offene),
            "abstimmungen_geschlossen": to_view(geschlossene),
            "is_admin": is_admin,
            "current_user": current_user,
        },
    )

# -------------------------
# UI: Abstimmungsdetail
# -------------------------
# Abstimmungsübersicht
@router.get("/abstimmungsuebersicht", response_class=HTMLResponse)
async def abstimmungsuebersicht(
    request: Request,
    service: AbstimmungsUebersichtsService = Depends(get_uebersichts_service),
    current_user=Depends(require_login_optional),
):
    offene = service.alle_offenen_abstimmungen()
    geschlossene = service.alle_abgeschlossenen_abstimmungen()

    is_admin = current_user is not None and current_user["role"] == "admin"

    def end_key(a):
        return getattr(a, "endDatum", None) or date.max

    def to_view(items):
        return [
            {
                "abstimmungsID": a.abstimmungsID,
                "titel": a.titel,
                "startdatum": getattr(a, "startDatum", None),
                "ablaufdatum": getattr(a, "endDatum", None),
                "status": a.status.value if getattr(a, "status", None) else "neu",
            }
            for a in sorted(items, key=end_key)
        ]

    return templates_abst.TemplateResponse(
        "abstimmungsuebersicht.html",
        {
            "request": request,
            "abstimmungen_offen": to_view(offene),
            "abstimmungen_geschlossen": to_view(geschlossene),
            "is_admin": is_admin,
            "current_user": current_user,
        },
    )

# Abstimmungsdetail
@router.get("/abstimmung/{abstimmungs_id}", response_class=HTMLResponse)
async def abstimmungs_detail(
    request: Request,
    abstimmungs_id: int,
    service: AbstimmungsService = Depends(get_abstimmungs_service),
    current_user=Depends(require_login_optional),
):
    # 🔹 hier nutzen wir die vorhandene Methode im Service: liste_abstimmungen()
    abstimmung = next(
        (a for a in service.liste_abstimmungen() if a.abstimmungsID == abstimmungs_id),
        None
    )

    if abstimmung is None:
        raise HTTPException(404, "Abstimmung nicht gefunden")

    return templates_abst.TemplateResponse(
        "abstimmungsdetail.html",
        {
            "request": request,
            "abstimmung": abstimmung,
            "current_user": current_user,
        },
    )


# -------------------------
# Bürger: Stimme abgeben
# -------------------------
@router.post("/abstimmungen/{abstimmungs_id}/stimme")
async def stimme_abgeben_endpoint(
    abstimmungs_id: int,
    wahl: str = Form(...),
    current_user=Depends(require_login),
    service: AbstimmungsService = Depends(get_abstimmungs_service),
):
    if current_user is None:
        raise HTTPException(401, "Bitte erst einloggen")
    if current_user["role"] != "buerger":
        raise HTTPException(403, "Nur Bürger dürfen abstimmen")

    buerger_id = int(current_user["user_id"].replace("buerger_", ""))
    option = Stimmoption[wahl]

    try:
        service.stimme_abgeben(abstimmungs_id, buerger_id, option, date.today())
        return RedirectResponse(url=f"/ui/abstimmung/{abstimmungs_id}", status_code=303)
    except ValueError as e:
        params = urlencode({"error": str(e)})
        return RedirectResponse(url=f"/ui/abstimmung/{abstimmungs_id}?{params}", status_code=303)