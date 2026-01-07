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

# Übung 4: Advanced Java, Test-Driven Design (TDD) und LLM-gestütztes Entwickeln

### 2. Testfälle mit LLM generieren und validieren (TDD Schritt 1)

Der erste zentrale Teil unserer Domänenlogik ist die Registrierung eines neuen Bürgers (BC: Bürgerverwaltung).
Die Tests wurden mittels LLM-gesteuerter Generierung von Testfällen erstellt, mit Fokus auf Validierungsmethoden,
insbesondere zur:
Eingabevalidierung von Name, Adresse, Geburtsdatum und Email.

Die Tests decken folgende Kategorien ab:<br>
- Happy Path: Typische zulässige Eingaben <br>
- Edge Cases: Grenzfälle, z.B. sehr kurze oder lange Namen, Sonderfälle bei Datum, etc.<br>
- Negative Tests: Ungültige Eingaben wie Zahlen im Namen, spezielle Sonderzeichen, falsche Formate

Für die Namensvalidierung wurde ergänzend eine Regex eingeführt, die nur Buchstaben (auch Unicode),
Leerzeichen und Bindestriche erlaubt – dabei wird auch geprüft, dass Namen nicht mit Bindestrich beginnen oder enden.

Die Geburtsdatumseingabe wurde an das Format „TT.MM.JJ“ angepasst und per Eigen-Parser im Validator behandelt,
sodass Strings korrekt in Python date konvertiert und validiert werden.

Auch für den zweiten (Abstimmungsübersicht) und dritten (Ergebnisdienst) Teil unserer Domänenlogik wurden Testfälle generiert, die die oben genannten Kategorien abdecken.
Was genau wird zum Beispiel in Teil 3 (Ergebnisdienst) getestet?

**Happy Path:**
-	Gültige Stimmenanzahlen (z.B. anzahl=5, anzahl=0, anzahl=100000) werden akzeptiert und korrekt zugewiesen
-	Gültige Stimmoptionen ("Ja", "Nein", "Enthaltung") funktionieren ohne Fehler
-	Das "Ergebnis" entsteht bei vorhandenen Einzelwerten und die Methoden liefern die korrekten Resultate

**Edge Cases:**
-	Grenzwerte wie null Stimmen (anzahl=0) oder extrem hohe Werte (anzahl=100000), sowie Minimalbelegung für Einzelwerte (Liste mit genau einer Stimme) werden explizit getestet
-	Case Sensitivity (z.B. "ja" statt "Ja") wird als Grenzfall für Enums geprüft

**Negative Tests:**
-	Ungültige Werte wie negative Zahlen bei Stimmen, unzulässige oder falsch geschriebene Stimmoptionen, leere oder None-Einzelwerte führen zu ValidationError/Fehlern und werden bewusst erwartet
Es gibt zahlreiche weitere Testfälle, die das LLM empfiehlt und je nach Bedarf im Laufe des Projektes ergänzt werden können. Auf ein Beispiel wird in 4. Eingegangen.


### 3. Implementierung der Domänenlogik (TDD Schritt 2) mit LLM-Pair-Programming
Zu allen drei Teilen der Dämonenlogik wurde Code mit Hilfe eines LLMs (perplexity pro) generiert, der die unter 2. erstellten Tests besteht. Das LLM schlägt einige Verbesserungen vor.
Zum Bespiel gilt es Redundanzen zu vermeiden.

**Beispiel aus ergebnis.py:**

def gesamtergebnis(self) -> int:
    return sum(e.anzahl for e in self.einzelwerte)

def getGesamtergebnis(self) -> int:
    return self.gesamtergebnis

Hier empfiehlt das LLM die Methode getGesamtergebnis() zu entfernen und konsistent das gesamtergebnis (Property) zu nutzen. Demzufolge wurde sowohl ergebnis.py als auch test_validation_ergebnis.py entsprechend angepasst.
Auf Nachfrage an das LLM ob dann die Methode getErgebnisDetails() ebenfalls als property verwendet werden sollte, bestätigte dies das LLM, falls keine Parameter nötig wären.
Da noch nicht genau feststeht, welche Ausgaben letztendlich benötigt werden, wird getErgebnisDetails() vorerst so gelassen.

Eine weitere bespielhafte Empfehlung des LLMs ist die Nutzung von Enum-Strings bei Ausgaben anstelle von Enum-Objekten. Dies ist sinnvoll für die Ausgabe und Serialisierung z.B. beim Erstellen von Dicts, bei der Anzeige für Nutzer oder beim Export/Import.
Deshalb wurde folgender Code angepasst.

**Vorher:**

def getErgebnisDetails(self) -> List[dict]:
    return [
        {"Option": e.stimmoption.optionstext, "Stimmen": e.anzahl}
        for e in self.einzelwerte
    ]

**Nachher:**

def getErgebnisDetails(self) -> List[dict]:
    return [
        {"Option": e.stimmoption.optionstext.value, "Stimmen": e.anzahl}
        for e in self.einzelwerte
    ]

Das LLM macht durchaus sinnvolle Vorschläge zum Verbessern des Codes. Allerdings muss immer geprüft werden, ob diese entsprechend benötigt werden, da das LLM nicht das gesamte Projekt im Auge hat und ggf. nicht über alle Informationen verfügt.

### 4. Tests-Erweiterung und Refaktorisierung (TDD Schritt 3):
Zu allen drei Teilen der Dämonenlogik wurde das LLM nach Testerweiterungen gefragt.
Das LLM schlägt zum Beispiel vor, extrem hohe Wertebereiche zu testen.

Beispiel aus ergebnis.py: Großer Wertebereich für "anzahl"
-	Extrem hohe Zahlen könnten zu Performance- oder Logikfehlern führen (z.B. bei Integer Overflow oder Datenbankgrenzen)
-	Test: Erzeuge "Stimmenanzahl" mit sehr großem "anzahl" (z.B. 10**12)

def test_stimmenanzahl_large_value():

    option = Stimmoption(optionstext=Optionen.JA)

    großer_wert = 10**12  # Beispiel: eine Billion Stimmen

    stimme = Stimmenanzahl(stimmoption=option, anzahl=großer_wert)

    assert stimme.anzahl == großer_wert

    stimmen = [Stimmenanzahl(stimmoption=option, anzahl=großer_wert)]

    ergebnis = Ergebnis(ergebnisID=1, abstimmungsID=99, einzelwerte=stimmen, timestamp=datetime.now())

    assert ergebnis.gesamtergebnis == großer_wert

Weitere Testfälle werden sich im Laufe des Projektes ergeben. Einige Vorschläge des LLMs wurden nicht umgesetzt, da noch nicht ganz klar ist, welche Ausgaben letztendlich benötigt werden. Diese Vorschläge werden dann erneut beurteilt.



### 6. Kritische Reflektion zu TDD, DDD und LLM-gestützte Entwicklung
- **Testgetriebene Entwicklung** (TDD) führt zu einem strukturierteren und fehlerärmeren Entwicklungsprozess,
da Anforderungen frühzeitig überprüft werden. Sie verbessert die Codequalität und erleichtert Refactoring,
erfordert jedoch anfangs mehr Aufwand und stößt bei komplexen Systemen an Grenzen, wenn geeignete Tests
schwer vorab zu definieren sind. <br>

- **Domain-Driven Design (DDD)** unterstützt das Team dabei, eine gemeinsame Sprache und klare Struktur im Projekt
zu etablieren. Durch die Aufteilung in klar abgegrenzte Domänen wissen alle Beteiligten jederzeit, in welchem
Bereich sie arbeiten und welche Logik betroffen ist. Dies erleichtert Abstimmung, Testabdeckung und Wartbarkeit.
Gleichzeitig erfordert DDD eine konsequente Einhaltung der definierten Domänengrenzen, um die Übersicht zu bewahren. <br>

- **Large Language Models (LLMs)** beschleunigen die Entwicklung, etwa durch Codegenerierung oder Ideenvorschläge, bergen
jedoch das Risiko unkritischer Übernahme. Eine reflektierte Nutzung ist daher essenziell, um die generierten
Vorschläge sinnvoll in den eigenen Kontext zu integrieren. LLMs eignen sich besonders für standardisierte Aufgaben,
weniger für komplexe, domänenspezifische Logik. <br>

Fazit:
TDD, DDD und LLMs ergänzen sich, wenn ihre jeweiligen Stärken gezielt genutzt und ihre Grenzen beachtet werden.
Ein bewusster Umgang mit LLMs trägt dazu bei, Codequalität, Verständlichkeit und Teamkonsistenz nachhaltig zu sichern.

# Übung 5: Software- und Architekturmetriken für Codequalität und Architekturoptimierung

### Allgemein: GitHub-Projekt in SonarCloud integrieren
**Schritte zur erfolgreichen Integration**
- Projekt auf SonarCloud anlegen und mit dem GitHub Repo verbinden
- Dies ermöglicht, dass alle Commits und Pull Requests automatisch analysiert werden.
- Erstellung der Datei sonar-project.properties im Repository-Root: Hier werden Projektschlüssel,
Organisation, Source-/Test-Pfade und weitere Einstellungen zentral hinterlegt

**Konfiguration der GitHub Actions Pipeline**
- Coverage-Bericht (coverage.xml) wird nach Testausführung erzeugt (z.B. mit pytest-cov)
- SonarCloud-Scan wird anschließend als eigener Schritt gestartet

**SonarCloud-Token generieren und als Secret in GitHub speichern**
- Ein persönlicher Token von SonarCloud wird als Secret SONAR_TOKEN im GitHub-Repository hinterlegt,
damit die Analyse authentisiert abläuft.

**Vorteile dieser Maßnahme**
- Transparenz: Codequalität, Testabdeckung und Schwachstellen werden kontinuierlich sichtbar und nachvollziehbar.
- Schnelles Feedback: Fehler und Verbesserungen werden früh erkannt und können gezielt angegangen werden.
- Automatisierung: Die Pipeline prüft automatisch bei jedem Push, so dass manuelle CodeReviews effizienter werden.
- Teamorientierung: Alle Teammitglieder profitieren von konsistenten Qualitätsstandards und automatischem PR-Feedback.
