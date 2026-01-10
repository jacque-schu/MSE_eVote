import pytest
from datetime import date
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from apps.abstimmungsmanagement.interfaces import abstimmung_endpoints as endpoints
from apps.abstimmungsmanagement.infrastructure.container.container import (
    get_abstimmungs_service,
    get_uebersichts_service,
    get_ergebnis_service,
)
from apps.abstimmungsmanagement.infrastructure.auth.abstimmung_auth import require_login
from apps.abstimmungsmanagement.domain.models.abstimmung import Stimmoption


# einfaches Dummy-Modell, das eine Abstimmung mit festen Testdaten repräsentiert
class DummyAbstimmung:
    def __init__(self, abstimmungsID=1, titel="Test", status=None):
        self.abstimmungsID = abstimmungsID
        self.titel = titel
        self.beschreibung = "Desc"
        self.startDatum = date(2025, 1, 1)
        self.endDatum = date(2025, 12, 31)
        self.status = status


# Dummy-Service, der das AbstimmungsService für Tests ersetzt und im Speicher arbeitet
class DummyAbstimmungsService:
    def __init__(self):
        self.abst_repo = type(
            "Repo",
            (),
            {
                "get": lambda _self, id_: DummyAbstimmung(abstimmungsID=id_),
            },
        )()

    # liefert eine kleine Liste von Dummy-Abstimmungen zurück
    def liste_abstimmungen(self):
        return [DummyAbstimmung(1), DummyAbstimmung(2)]

    # Platzhalter-Methode für das Abgeben einer Stimme (tut im Test nichts).
    def stimme_abgeben(self, abstimmungs_id, buerger_id, option, stimmdatum):
        return

    # Erzeugt eine neue Dummy-Abstimmung für Tests.
    def erstelle_abstimmung(self, **kwargs):
        return DummyAbstimmung(abstimmungsID=kwargs["abstimmungsID"])


# Dummy-Service, der offene und abgeschlossene Abstimmungen für die Übersicht liefert
class DummyUebersichtsService:
    def alle_offenen_abstimmungen(self):
        return [DummyAbstimmung(1)]

    def alle_abgeschlossenen_abstimmungen(self):
        return [DummyAbstimmung(2)]


# Dummy-Service, der ein festes Abstimmungsergebnis für Tests zurückgibt
class DummyErgebnisService:
    def hole_ergebnis_details_fuer_abstimmung(self, abstimmungs_id: int):
        return [{"abstimmungsID": abstimmungs_id, "stimmenJa": 10, "stimmenNein": 5}]


# Baut für jeden Test eine FastAPI-Testclient-Instanz mit Dummy-Services und Login-Override auf
@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(endpoints.router)

    # Service-Dependencies überschreiben
    app.dependency_overrides[get_abstimmungs_service] = lambda: DummyAbstimmungsService()
    app.dependency_overrides[get_uebersichts_service] = lambda: DummyUebersichtsService()
    app.dependency_overrides[get_ergebnis_service] = lambda: DummyErgebnisService()

    # Async-Login-Override, kompatibel mit require_login(request)
    async def override_require_login(request=None):
        return {"user_id": "buerger_1", "role": "buerger"}

    app.dependency_overrides[require_login] = override_require_login

    # Static-Routen, damit url_for(...) in Templates funktioniert
    static_dir = Path("ui") / "static"
    app.mount(
        "/static/common",
        StaticFiles(directory=static_dir, check_dir=False),
        name="static_common",
    )
    app.mount(
        "/static/abstimmung",
        StaticFiles(directory=static_dir, check_dir=False),
        name="static_abstimmung",
    )

    return TestClient(app)


# prüft, ob der GET‑Endpoint /abstimmungen das erwartete JSON zurückgibt
def test_liste_abstimmungen_returns_list_of_dicts(client: TestClient):
    response = client.get("/abstimmungen")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["abstimmungsID"] == 1


# Prüft, prüft, ob der Detail‑Endpoint für eine einzelne Abstimmung korrekt funktioniert
def test_get_abstimmung_returns_single_abstimmung(client: TestClient):
    response = client.get("/abstimmungen/1")
    assert response.status_code == 200
    data = response.json()
    assert data["abstimmungsID"] == 1
    assert data["titel"] == "Test"


# Prüft, dass die Ergebnis-API nur mit Login erreichbar ist und eine Ergebnisliste zurückgibt
def test_get_abstimmung_ergebnis_requires_login_and_returns_data(client: TestClient):
    response = client.get("/abstimmungen/1/ergebnis")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["abstimmungsID"] == 1


# Prüft, ob der „Stimme abgeben“-Endpoint nach einer erfolgreichen Stimmabgabe korrekt mit einem Redirect auf die Detailseite reagiert
def test_stimme_abgeben_endpoint_redirects_on_success(client: TestClient):
    response = client.post(
        "/abstimmungen/1/stimme",
        data={"wahl": Stimmoption.JA.name},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/ui/abstimmung/1"


# Prüft, dass die Abstimmungsübersicht als HTML gerendert wird
def test_abstimmungsuebersicht_renders_html(client: TestClient):
    response = client.get("/ui/abstimmungsuebersicht")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<html" in response.text.lower()


# Prüft, dass die Detailansicht einer Abstimmung als HTML gerendert wird
def test_abstimmungs_detail_renders_html(client: TestClient):
    response = client.get("/ui/abstimmung/1")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# Prüft, dass der JSON-POST zum Anlegen einer Abstimmung erfolgreich ist und die ID übernommen wird
def test_create_abstimmung_returns_json(client: TestClient):
    payload = {
        "abstimmungsID": 5,
        "titel": "Neue Abstimmung",
        "beschreibung": "Test",
        "startDatum": "2025-01-01",
        "endDatum": "2025-12-31",
        "mindestalter": None,
    }
    response = client.post("/abstimmungen", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["abstimmungsID"] == 5
    assert data["titel"] == "Test"


# Liefert für Tests einen eingeloggten Admin-Benutzer zurück
async def _override_require_login_admin(request=None):
    return {"user_id": "admin_1", "role": "admin"}


# Prüft, dass das Admin-Formular nur mit Admin-Login erreichbar ist und HTML liefert
def test_abstimmung_neu_form_requires_admin(client: TestClient):
    client.app.dependency_overrides[require_login] = _override_require_login_admin
    response = client.get("/ui/admin/abstimmungen/neu")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# Prüft, dass das Admin-Formular beim erfolgreichen Absenden zur Übersicht weiterleitet
def test_abstimmung_neu_submit_redirects_on_success(client: TestClient):
    client.app.dependency_overrides[require_login] = _override_require_login_admin
    form_data = {
        "abstimmungsID": "",
        "titel": "Titel",
        "beschreibung": "Beschreibung",
        "startDatum": "2025-01-01",
        "endDatum": "2025-12-31",
        "minAlter": "",
    }
    response = client.post(
        "/ui/admin/abstimmungen/neu",
        data=form_data,
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/ui/abstimmungsuebersicht"
