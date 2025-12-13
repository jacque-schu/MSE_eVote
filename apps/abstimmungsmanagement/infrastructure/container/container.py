
from apps.abstimmungsmanagement.infrastructure.repositories.json_abstimmung_repository import JsonAbstimmungRepository
from apps.abstimmungsmanagement.application.services.abstimmungs_service import AbstimmungsService
from apps.abstimmungsmanagement.application.services.abstimmungsuebersichts_service import AbstimmungsUebersichtsService

#Hier wird das JSON erzeugt und eine zentrale Instanz des Abstimmungs-services und Abstimmungsübersichts-Services gebaut.

_repo = JsonAbstimmungRepository("apps/abstimmungsmanagement/infrastructure/persistence/abstimmungen.json")
_abst_service = AbstimmungsService(abst_repo=_repo, erg_repo=None)
_uebersicht_service = AbstimmungsUebersichtsService(_repo)

def get_abstimmungs_service() -> AbstimmungsService:
    return _abst_service

def get_uebersichts_service() -> AbstimmungsUebersichtsService:
    return _uebersicht_service
