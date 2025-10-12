# Übung 1: Erstellen eines Git-Handouts für Anfänger

## 2.Grundlegende Git-Befehle

- **git init**  
  Initialisiert ein neues Git-Repository im aktuellen Verzeichnis.

- **git clone <URL>**  
  Kopiert ein bestehendes Repository von einem Remote-Server.

- **git add <Datei>**  
  Fügt Änderungen einer Datei dem kommenden Commit hinzu.

- **git commit -m "<Nachricht>"**  
  Speichert die Änderungen im Repository mit einer Nachricht.

- **git status**  
  Zeigt den aktuellen Zustand der Arbeitskopie und der Staging-Area an.

- **git push**  
  Überträgt Commits vom lokalen Repository ins entfernte Repository.

- **git pull**  
  Holt und integriert Änderungen vom entfernten Repository in das lokale.

- **git branch**  
  Listet lokale Branches auf, erstellt oder löscht Branches.

- **git checkout <Branch>**  
  Wechselt zu einem anderen Branch oder stellt Dateien wieder her.

- **git merge <Branch>**  
  Führt Änderungen eines anderen Branches mit dem aktuellen zusammen.
​

## 3. Branches und ihre Nutzung, Umgang mit Merge-Konflikten

### 3.1 Branches
Branches sind Entwicklungszweige, die parallel in einem Versionskontrollsystem wie Git entwickelt werden.
Ein Branch ermöglicht es, unabhängig vom Haupt-(main/master)Branch neue Features, Bugfixes oder experimentelle Funktionen zu entwickeln, ohne dabei den stabilen Code (main branch) zu beeinflussen.

Eine typische Nutzung sieht oft wie folgt aus:

Main Branch: Dies ist die stabile Produktionsversion.
Feature Branches: Dient zur Entwicklung neuer Features.
Bugfix Branches: Dient zur Behebung von Fehlern, ohne dabei die Hauptentwicklung zu stören.
Release Branches: Dient zur Vorbereitung neuer Releases (Veröffentlichungen).

Branches können nach Fertigstellung wieder in den Hauptbranch gemerged werden.
Mergen bedeutet, dass zwei Branches im Versionskontrollsystem Git miteinander zusammengeführt werden. 
Dabei werden die Änderungen, die in einem Branch gemacht werden, in den anderen Branch integriert.

### 3.2 Merge-Konflikte
Merge-Konflikte entstehen, wenn in unterschiedlichen Branches dieselben Codebereiche geändert wurden.
In diesem Fall kann Git nicht automatisch entscheiden, welche Änderungen bleiben.
Ein Merge-Konflikt muss manuell gelöst werden.

Ein typisches Vorgehen bei Merge-Konflikten sieht wie folgt aus:

Git zeigt die Konflikte beim merge an.
Die Konfliktstellen sind dabei im Code markiert.
Die Entwickler müssen entscheiden, welche Änderungen übernommen oder kombiniert werden.
Erst nach der Auflösung des Konflikts wird der Code committet.
Anschließend können Tests dabei helfen, eine korrekte Lösung sicherzustellen. 
## 5. Nützliche Git-Tools und Plattformen


### 5.1 GitHub

**GitHub** ist eine bekannte Plattform zur Verwaltung von Git-Repositories in der Cloud. 
Sie bietet nicht nur Speicherplatz für Code, sondern auch viele Funktionen zur Teamarbeit und Projektorganisation.

#### Hauptfunktionen
- **Remote-Repositories:** Speicherung des Codes in der Cloud, um von überall darauf zugreifen zu können.  
- **Pull Requests:** Entwickler können Änderungen vorschlagen, die dann von anderen überprüft („reviewed“) und freigegeben werden.  
- **Code Review:** Kommentare und Diskussionen direkt an Codezeilen möglich – ideal zur Qualitätssicherung.  
- **Issues & Projektverwaltung:** Aufgaben, Bugs und Ideen können als „Issues“ erfasst, kommentiert und priorisiert werden.  
- **GitHub Actions:** Automatisierung von Prozessen wie Tests, Builds oder Deployments (CI/CD).  
- **Wikis & Pages:** Möglichkeit, Dokumentationen oder Websites direkt im Repository zu pflegen.

#### Vorteile
- Weltweit verbreitet 
- Gute Integration in IDEs wie PyCharm, IntelliJ und VS Code  
- Kostenlos für öffentliche und private Projekte  
- Ideal für Open-Source- und Teamprojekte

### 5.2 GitLab

**GitLab** ist eine leistungsfähige Alternative zu GitHub und besonders beliebt in Unternehmen, 
die eigene Server betreiben möchten.

#### Hauptfunktionen
- Git-Repository-Verwaltung mit Rechten und Rollen
- **Self-Hosting** möglich → Daten bleiben im eigenen Netzwerk  
- **Wiki, Issue Tracker und Boards** ähnlich wie GitHub  
- **Merge Requests** statt Pull Requests (gleiche Idee)

#### Vorteile
- Datenschutzfreundlich, da lokal installierbar  
- Umfassende Automatisierungs- und Sicherheitsfunktionen
- Ideal für Unternehmen mit strengen Compliance-Richtlinien


###  5.3 Grafische Git-Tools

Neben den Online-Plattformen gibt es Desktop-Anwendungen, die Git-Befehle visuell darstellen und besonders für Einsteiger hilfreich sind.

#### Sourcetree
- Kostenloses Git-Tool von Atlassian  
- Zeigt Commits, Branches und Merges als übersichtlichen Verlauf (Commit-Graph)  
- Ideal, um ohne Terminal zu arbeiten  
- Unterstützt GitHub, GitLab und Bitbucket  

#### GitKraken
- Moderne, optisch ansprechende Benutzeroberfläche  
- Visualisierung von Branches, Commits und Merges  
- Integrierter Code-Editor und GitHub-/GitLab-/Bitbucket-Anbindung  
- Besonders beliebt bei Teams, die visuell arbeiten möchten

#### GitHub Desktop
- Offizielles GUI-Tool von GitHub.  
- Einfaches Klonen, Committen, Branch-Wechseln und Pushen ohne Terminal.  
- Integration mit GitHub.com für Pull Requests und Issues.
