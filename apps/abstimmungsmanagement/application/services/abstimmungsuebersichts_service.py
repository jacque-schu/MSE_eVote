from typing import List
from apps.abstimmungsmanagement.domain.models.abstimmung import Abstimmung, Abstimmungsstatus

class AbstimmungsUebersichtsService:
    def __init__(self, abst_repo):
        self.abst_repo = abst_repo

    def alle_offenen_abstimmungen(self) -> List[Abstimmung]:
        return self.abst_repo.find_by_status(Abstimmungsstatus.OFFEN)

    def alle_abgeschlossenen_abstimmungen(self) -> List[Abstimmung]:
        return self.abst_repo.find_by_status(Abstimmungsstatus.GESCHLOSSEN)

    def details_zu_abstimmung(self, abstimmungs_id: int) -> Abstimmung:
        return self.abst_repo.get(abstimmungs_id)


