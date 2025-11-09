from modules.ergebnisdienst.domain.entities.ergebnis import Ergebnis  # oder von der richtigen Stelle importieren

class ErgebnisberechnungsService:
    def veroeffentlicheErgebnis(self, ergebnis: Ergebnis):
        print(f"Ergebnis veröffentlicht für Abstimmung {ergebnis.abstimmungsID}: {ergebnis.getGesamtergebnis()} Stimmen.")

class ErgebnisvalidierungsService:
    def stelleBerechnungSicher(self, ergebnis: Ergebnis) -> bool:
        valid = ergebnis.getGesamtergebnis() >= 0
        print(f"Validierung: {'gültig' if valid else 'ungültig'}")
        return valid

class ErgebnisanzeigeService:
    def bereiteErgebnisseAuf(self, ergebnis: Ergebnis):
        print("Ergebnisdetails:")
        for detail in ergebnis.getErgebnisDetails():
            print(f"Option: {detail['Option'].value}, Stimmen: {detail['Stimmen']}")

