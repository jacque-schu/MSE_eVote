from pathlib import Path
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parents[4]  # → .../MSE_eVote

templates_abst = Jinja2Templates(
    directory=BASE_DIR / "ui" / "abstimmung" / "templates"
)

if __name__ == "__main__":
    path = BASE_DIR / "ui" / "abstimmung" / "templates"
    print("Template dir:", path)
    print("Exists:", path.exists())
    print("Files:", list(path.glob("*.html")))
