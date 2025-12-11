from apps.abstimmungsmanagement.domain.models.abstimmung import Abstimmung

class InMemoryAbstimmungRepository:
    def __init__(self):
        self._store: dict[int, Abstimmung] = {}

    def get(self, abstimmungs_id: int) -> Abstimmung:
        return self._store[abstimmungs_id]

    def save(self, abstimmung: Abstimmung) -> None:
        self._store[abstimmung.abstimmungsID] = abstimmung

    def list_all(self) -> list[Abstimmung]:
        return list(self._store.values())
