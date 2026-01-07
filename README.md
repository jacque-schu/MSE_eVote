# eVote – Digitale Bürgerabstimmungsplattform

eVote ist eine **digitale Bürgerabstimmungsplattform** für Online‑Bürgerbefragungen zu städtischen Entscheidungen und Projekten. Ziel ist ein sicheres und nachvollziehbares Abstimmungssystem, mit dem Bürger unkompliziert online ihre Stimme abgeben können.

## Features

- Nutzerregistrierung und Authentifizierung  
- Übersicht über laufende und vergangene Abstimmungen  
- Sicherer Abstimmungsmechanismus („eine Person, eine Stimme“)  
- Ergebnisübersicht mit detaillierten Resultaten  
- Hoher Fokus auf Datenintegrität und Abstimmungssicherheit[1]

## Tech Stack

- Sprache / Backend: **Python** mit FastAPI  
- Tests: pytest inkl. parametrisierten Tests und Coverage  
- CI/CD: GitHub Actions für Build, Tests und Linting  
- Codequalität: SonarCloud (Code Smells, Coverage, Complexity usw.)  
- Validierung: Pydantic für Domain‑Modelle und Eingabedaten

## Architektur (kurz)

- Domain‑Driven Design mit zwei Bounded Contexts:  
  - Bürgerverwaltung (Registrierung, Validierung von Bürgerdaten)  
  - Abstimmungsmanagement (Abstimmung, Ergebnis, Stimmenzählung)[1]
- Fachlogik über Aggregate (Bürger, Abstimmung, Ergebnis) und Policies wie „Nur wahlberechtigte Bürger“.

## Qualitätssicherung

- Test‑Driven Development (Red‑Green‑Refactor) für zentrale Fachlogik (Validierungen, Statusübergänge, Stimmenzählung).
- GitHub Actions‑Pipeline: Installieren der Abhängigkeiten, Linting (ruff), Unit‑ und Integrationstests, Coverage‑Report.
- SonarCloud‑Analyse für Coverage, Duplications, Security, Reliability und Maintainability.

## Installation

```bash
# Repository klonen
git clone <REPO_URL>
cd <REPO_ORDNER>

# Virtuelle Umgebung anlegen (optional, Beispiel für venv)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

*(Passe die Befehle an eure tatsächliche Struktur an, z.B. Ordnername oder Tooling.)*

## Entwicklung & Tests

```bash
# Tests ausführen
pytest

# Optional: Coverage
pytest --cov=evote
```

Die CI‑Pipeline führt bei jedem Push oder Pull Request auf `main` automatisch Linting, Tests und SonarCloud‑Scan aus.

## Ausblick





