from apps.buergerverwaltung.domain.models.buerger import Buerger
from apps.buergerverwaltung.infrastructure.repositories.buerger_repository import BuergerRepository


class Registrierungsservice:
    def __init__(self, buerger_repository: BuergerRepository):
        """
        Initialisiert den Registrierungsservice mit einem Bürger-Repository.

        :param buerger_repository: Repository zur Verwaltung der Bürgerdaten.
        """
        self.buerger_repository = buerger_repository

    def registriere_buerger(self, buerger: Buerger) -> Buerger:
        """
        Registriert einen neuen Bürger in der Datenbank.

        :param buerger: Das Bürger-Objekt, das registriert werden soll.
        :return: Das registrierte Bürger-Objekt.
        """
        alle_buerger = self.buerger_repository.lade_alle()

        # Überprüfen, ob der Bürger bereits existiert (z.B. basierend auf der E-Mail)
        for existing_buerger in alle_buerger:
            if existing_buerger.email == buerger.email:
                raise ValueError(f"Ein Bürger mit der E-Mail {buerger.email} existiert bereits!")

        # Neuen Bürger speichern
        self.buerger_repository.fuege_hinzu(buerger)
        return buerger
