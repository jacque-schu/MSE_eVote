
from apps.abstimmungsmanagement.infrastructure.repositories.abstimmungs_repository import InMemoryAbstimmungRepository
from apps.abstimmungsmanagement.application.services.abstimmungs_service import AbstimmungsService

_repo = InMemoryAbstimmungRepository()
_service = AbstimmungsService(abst_repo=_repo, erg_repo=None)

def get_abstimmungs_service() -> AbstimmungsService:
    return _service
