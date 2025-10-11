# 2.Grundlegende Git-Befehle

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

# 3.Branches und ihre Nutzung, Umgang mit Merge-Konflikten

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
