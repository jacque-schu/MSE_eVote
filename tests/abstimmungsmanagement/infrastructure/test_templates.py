from pathlib import Path

from apps.abstimmungsmanagement.infrastructure.templates.templates import (
    BASE_DIR,
    templates_abst,
)


# prüft, dass BASE_DIR ein existierender Ordner ist
def test_base_dir_points_to_existing_directory():
    assert isinstance(BASE_DIR, Path)
    assert BASE_DIR.exists()
    assert BASE_DIR.is_dir()


# prüft, dass templates_abst genau auf den Ordner ui/abstimmung/templates zeigt
def test_templates_abst_uses_correct_directory():
    expected_dir = BASE_DIR / "ui" / "abstimmung" / "templates"

    # Über den Jinja2-Environment/Loader den tatsächlichen Template-Pfad auslesen
    env = templates_abst.env
    loader = env.loader
    searchpath = loader.searchpath  # Liste der Template-Verzeichnisse

    paths = {Path(p) for p in searchpath}
    assert expected_dir in paths


# prüft, dass der Template-Ordner existiert und mindestens eine .html-Datei enthält
def test_templates_directory_exists_and_contains_html():
    template_dir = BASE_DIR / "ui" / "abstimmung" / "templates"
    assert template_dir.exists()
    assert template_dir.is_dir()

    html_files = list(template_dir.glob("*.html"))
    assert len(html_files) >= 1
