from pathlib import Path
from apps.buergerverwaltung.domain.repositories.i_buerger_repository import IBuergerRepository
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository

BASE_DIR = Path(__file__).resolve().parent

def get_buerger_repo() -> IBuergerRepository:
    db_path = BASE_DIR / "apps" / "buergerverwaltung" / "infrastructure" / "persistence" / "buerger_db.json"
    return BuergerRepository(str(db_path))
