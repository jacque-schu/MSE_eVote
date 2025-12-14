from pathlib import Path
from fastapi.templating import Jinja2Templates

#Die Datei richtet den Template‑Ordner für die Abstimmungsübersicht ein
#und stellt den Pfad zum HTML-Template bereit

BASE_DIR = Path(__file__).resolve().parents[4]

templates_abst = Jinja2Templates(
    directory=BASE_DIR / "ui" / "abstimmung" / "templates"
)


#Test, ob der Pfad zum HTML-Template stimmt/ kann später gelöscht werden
if __name__ == "__main__":
    path = BASE_DIR / "ui" / "abstimmung" / "templates"
    print("Template dir:", path)
    print("Exists:", path.exists())
    print("Files:", list(path.glob("*.html")))
