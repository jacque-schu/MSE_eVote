import json
from pathlib import Path
from typing import List
from apps.abstimmungsmanagement.domain.models.abstimmung import Abstimmung
from datetime import date
from apps.abstimmungsmanagement.domain.models.abstimmung import Abstimmungsstatus

class JsonAbstimmungRepository:
    def __init__(self, file_path: str = "apps/abstimmungsmanagement/infrastructure/persistence/abstimmungen.json"):
        self._file_path = Path(file_path)
        self._store: dict[int, Abstimmung] = {}
        self._load()

    def _load(self):
        if self._file_path.exists():
            try:
                with open(self._file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._store = {}
                    for item_data in data:  # ← Liste iterieren!
                        abstimmung = Abstimmung.model_validate(item_data)

                        # Status prüfen & OBJEKT ändern
                        if (abstimmung.status == Abstimmungsstatus.OFFEN and
                                abstimmung.endDatum < date.today()):
                            # Pydantic erlaubt .model_copy_update()
                            abstimmung = abstimmung.model_copy(update={'status': Abstimmungsstatus.GESCHLOSSEN})

                        self._store[abstimmung.abstimmungsID] = abstimmung
            except (json.JSONDecodeError, KeyError, ValueError):
                self._store = {}

        if self._store:
            self._save()  # ← Neue Objekte speichern!

    def _save(self):
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [abstimmung.model_dump(mode='json') for abstimmung in self._store.values()]
        self._file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

    def get(self, abstimmungs_id: int) -> Abstimmung:
        if abstimmungs_id not in self._store:
            raise KeyError(f"Abstimmung {abstimmungs_id} nicht gefunden")
        return self._store[abstimmungs_id]

    def save(self, abstimmung: Abstimmung) -> None:
        self._store[abstimmung.abstimmungsID] = abstimmung
        self._save()

    def list_all(self) -> List[Abstimmung]:
        return list(self._store.values())

    def find_by_status(self, status: Abstimmungsstatus) -> List[Abstimmung]:
        return [a for a in self._store.values() if a.status == status]

