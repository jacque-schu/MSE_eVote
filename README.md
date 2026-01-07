## JWT Setup
1. Kopiere `.env.example` zu `.env`
2. Generiere eigenen SECRET_KEY (mind. 32 Zeichen)
3. NIE in Git committen!



# Übung 2: Einrichtung einer CI/CD-Pipeline
## 1. Einrichtung und Fehlerbehebung eines GitHub Actions Workflows für Python
Die Dokumentation beschreibt die schrittweise Einrichtung und Optimierung eines GitHub-Actions-Workflows für ein Python-Projekt, der den Code bei jedem Commit automatisch prüft und testet und dabei typische Fehler sowie deren Lösungen behandelt.

### 1.1 Ziel des Workflows
Der Workflow sorgt dafür, dass bei Änderungen am main-Branch (Hauptzweig) der Python-Code automatisch mit GitHub Actions überprüft wird, wobei eine YAML-Datei Schritte wie Abhängigkeitsinstallation, Linting mit flake8 und Tests mit pytest definiert.

### 1.2 Aufbau der Datei python-app.yml
Die Datei 'python-app.yml' wurde im Verzeichnis '.github/workflows' angelegt. Sie enthält
Anweisungen für GitHub, wie der Code automatisch überprüft werden soll. Der Workflow
führt folgende Aufgaben aus:

- Den Code aus dem Repository auschecken
- Python 3.10 einrichten
- Abhängigkeiten installieren (z. B. flake8, pytest)
- Den Code mit flake8 auf Fehler prüfen
- Alle Tests mit pytest ausführen

### 1.3 Aufgetretene Fehler und Ursachen
Während der Entwicklung des Workflows traten mehrere Fehler auf, die typisch für YAML-
und CI/CD-Setups sind:

**Syntaxfehler in der YAML-Datei:**

YAML-Dateien sind sehr empfindlich bei Einrückungen. Ein Kommentar in der Zeile unter 'run: |' war nicht richtig eingerückt und führte dazu, dass der Workflow nicht ausgeführt werden konnte. Nach der Korrektur der
Einrückung funktionierte der Workflow wieder.

**Fehlende requirements.txt:**

GitHub Actions zeigte die Warnung 'No file matched to requirements.txt', da keine Abhängigkeitsdatei im Projekt gefunden wurde. Der Workflow wurde angepasst, um auch ohne diese Datei weiterlaufen zu können.

**Exit Code 5 (pytest):**  

Der Workflow schlug mit dem Code 5 fehl, weil pytest keine Testdateien im Projekt fand. Das wurde behoben, indem eine einfache Testdatei ('test_sanity.py') hinzugefügt wurde oder der Workflow so angepasst wurde, dass er auch
ohne Tests erfolgreich abgeschlossen wird.

### 1.4 Branches und Commits

Während der Fehlerbehebung wurden mehrere Commits auf einem eigenen Branch mit dem Namen 'fabtomsch' erstellt. Dieser Branch wurde verwendet, um Änderungen am Workflow zu testen, ohne den Hauptzweig zu beeinflussen. Nachdem die Datei korrekt funktionierte, konnte sie anschließend in den main-Branch übernommen werden. So bleibt der Hauptzweig stets stabil und funktionsfähig.

### 1.5 Ergebnis und Erkenntnisse

Am Ende lief der Workflow erfolgreich durch. Der Code wird nun automatisch geprüft, wenn Änderungen am main-Branch vorgenommen werden. Dabei werden sowohl die Codequalität (Linting) als auch die Tests überprüft. Durch die iterative Fehlerbehebung wurde deutlich, wie wichtig korrekte YAML-Syntax, Testdateien und klare Branch-Strukturen sind.

### 1.6 Fazit
Der Aufbau dieses Workflows zeigt, wie man mit GitHub Actions eine einfache, aber effektive Continuous-Integration-Pipeline für Python-Projekte einrichtet. Auch wenn anfangs kleinere Fehler auftraten, führten sie zu einem besseren Verständnis für YAML-Strukturen, Testkonventionen und Versionskontrolle mit Git.

# Übung 3: Systemarchitektur des Projektes modellieren

**Übersicht der:**
- Entitäten, Aggregate & Werte
- Bounded Contexts (BC)
- Domain Services und Repositories

<img width="756" height="1174" alt="image" src="https://github.com/user-attachments/assets/0ae0560e-4541-446c-8bc7-239230fcfc51" />

### Entitäten und Aggregates

**Bürgerverwaltung (Aggregate Root)**
- Entität: Bürger
- Aggregate: Bürger (enthält alle Daten des Bürgers zur Registrierung, Aktivierung, E-Mail-Bestätigung, Statuswechsel)
- Attribute: Bürger-ID, Name, Adresse, Geburtsdatum, E-Mail, Status (aktiv/gesperrt), (Datum der Registrierung, E-Mail-Bestätigung (als Value Object), Passwort(-Hash))
- Methoden: registriere(), aktivieren(), sperren(), bestätigung_versenden(), bestätigung_validieren()

**Abstimmungsmanagement (Aggregate Root)**
- Entität: Abstimmung
- Aggregate: Abstimmung (enthält alle Daten zu einer Abstimmung, inkl. Frist und Status)
- Attribute: Abstimmungs-ID, Titel, Beschreibung, Frist (Value Object: Start-/Enddatum), Status (offen/geschlossen/archiviert)
- Methoden: abstimmung_erstellen(), abstimmung_schließen(), frist_prüfen(), beschreibung_aktualisieren()

**(Teilnahme) / Stimme (Aggregate Root)**
- Entität: Stimme
- Aggregate: Stimme (fasst die Stimmabgabe eines Bürgers für eine Abstimmung zusammen)
- Attribute: Stimmen-ID, Bürger-ID (Referenz), Abstimmungs-ID (Referenz), Auswahl/Option, Zeitstempel
- Methoden: abgeben(), ändern(), widerrufen()

**Abstimmungsübersicht / Abstimmungsübersicht / Ergebnis-Aggregat (Aggregate Root)**
- Entität: Abstimmungsübersicht
- Aggregate: Abstimmungsübersicht (bzw. Ergebnis)
- Attribute: Liste der aktuellen Abstimmungen (Titel, Beschreibung, Frist, Status), ggf. Ergebnisse pro Abstimmung (Anzahl Stimmen je Option)
- Methoden: abstimmungsuebersicht_anzeigen(), ergebnis_berechnen(), filtern(), sortieren()

### Implementierungsstrategie

**Entitäten und Aggregate implementieren**

- Bürgervewaltung (Aggregate Root: Bürger)<br>
Klasse Bürger<br>
Attribute: buergerID, name, adresse, geburtsdatum, e-mail, registrierungsstatus, authentifizierungsdaten<br>
Methoden: registriere(), authentifiziere(), datenAktualisieren()

- Abstimmungsübersicht (Aggregate Root: Abstimmung)<br>
Klasse Abstimmung<br>
Attribute: abstimmungsID, titel, Beschreibung, startDatum, endDatum, teilnehmerliste, stimmen, status<br>
Methoden: erstellen(), starten(), beenden(), aktualisieren(), ergebnisAuszählen()

- Stimme (Aggregate Root: Stimme)<br>
Klasse Stimme<br>
Attribute: buergerId, option, zeitpunkt<br>
Methoden: validiere(), saveStimme()

- Ergebnis (Aggregate Root: Ergebnis)<br>
Klasse Abstimmungsübersicht<br>
Attribute: ErgebnisID, AbstimmungsID, Gesamtergebnis, Ergebnisdetails, Zeitpunkt der Ergebniserstellung<br>
Methoden: getGesamtergebnis(), getErgebnisDetails()

**Domain Services implementieren**
- AuthentifizierungsService: z.B. Nutzer authentifizieren, Nutzungsstatus abfragen
- RegistrierungsService: Neue Nutzer registrieren, Bestätigungsprozesse steuern
- AbstimmungsService: Abstimmungen verwalten, Abstimmungen erstellen/abschließen
- AbstimmungsUebersichtsService: Verwaltung und Bereitstellung der Ansicht von Abstimmungen
- PolicyService: Prüfen von Berechtigungen und Regeln (z. B. wer darf abstimmen)
- ErgebnisberechnungsService: Stimmen zählen und Ergebnis berechnen
- ErgebnisvalidierungsService: Validierung und Regelauswertung der Ergebnisse
- ErgebnisanzeigeService: Formattierung und Aufbereitung der Ergebnisanzeige für Nutzer

**Repositories implementieren**
- BürgerverwaltungsRepository
- AbstimmungsRepository
- ErgebnisRepository




