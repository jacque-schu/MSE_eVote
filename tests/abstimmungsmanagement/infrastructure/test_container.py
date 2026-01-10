import pathlib

from apps.abstimmungsmanagement.infrastructure.repositories.json_abstimmung_repository import JsonAbstimmungRepository
from apps.abstimmungsmanagement.application.services.abstimmungs_service import AbstimmungsService
from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import AbstimmungsUebersichtsService
from apps.abstimmungsmanagement.application.services.ergebnis_service import ErgebnisService

from apps.abstimmungsmanagement.infrastructure.container.container import (
    _repo,
    _abst_service,
    _uebersicht_service,
    _erg_service,
    get_abstimmungs_service,
    get_uebersichts_service,
    get_ergebnis_service,
)

#Die Testdatei überprüft in einfachen Schritten, ob das „Container“-Modul die richtigen Objekte baut und wieder zurückgibt.

#prüft, ob das Repository‑Objekt stimmt und auf die richtige Datei zeigt
def test_repo_is_json_repository_with_correct_path():
    # Typ prüfen
    assert isinstance(_repo, JsonAbstimmungRepository)

    # Pfad prüfen → findet Tippfehler in der Container-Datei
    expected = pathlib.Path(
        "apps/abstimmungsmanagement/infrastructure/persistence/abstimmungen.json"
    )
    assert str(_repo._file_path).endswith(str(expected))

#prüft, ob alle drei Services im Container wirklich mit dem gleichen Repository‑Objekt verbunden sind
def test_services_are_instantiated_with_repo():
    # AbstimmungsService nutzt das Repository über .abst_repo
    assert isinstance(_abst_service, AbstimmungsService)
    assert _abst_service.abst_repo is _repo

    # ErgebnisService nutzt das Repository über ._abstimmung_repository
    assert isinstance(_erg_service, ErgebnisService)
    assert _erg_service._abstimmung_repository is _repo

    # Übersichtsservice nutzt das Repository über .abst_repo
    assert isinstance(_uebersicht_service, AbstimmungsUebersichtsService)
    assert _uebersicht_service.abst_repo is _repo

#prüft, ob die drei Getter Singltons zurückgeben, also immer dieselben Service‑Objekte
def test_getter_return_singletons():
    # AbstimmungsService
    s1 = get_abstimmungs_service()
    s2 = get_abstimmungs_service()
    assert s1 is _abst_service
    assert s1 is s2

    # Übersichtsservice
    u1 = get_uebersichts_service()
    u2 = get_uebersichts_service()
    assert u1 is _uebersicht_service
    assert u1 is u2

    # ErgebnisService
    e1 = get_ergebnis_service()
    e2 = get_ergebnis_service()
    assert e1 is _erg_service
    assert e1 is e2
