from apps.buergerverwaltung.domain.entities.buerger import Buerger

class Registrierungsservice:
    def __init__(self, buerger_db):
        """
        Initialisiert den Registrierungsservice mit der Bürger-Datenbank.

        :param buerger_db: Die Datenbank, in der die Bürger gespeichert sind.
        """
        self.buerger_db = buerger_db

    def registriere_buerger(self, buerger: Buerger) -> Buerger:
        """
        Registriert einen neuen Bürger in der Datenbank.

        :param buerger: Das Bürger-Objekt, das registriert werden soll.
        :return: Das registrierte Bürger-Objekt.
        """
        # Überprüfen, ob der Bürger bereits existiert (z.B. basierend auf der E-Mail)
        for existing_buerger in self.buerger_db:
            if existing_buerger.email == buerger.email:
                raise ValueError(f"Ein Bürger mit der E-Mail {buerger.email} existiert bereits!")

        # Füge den neuen Bürger zur Datenbank hinzu
        self.buerger_db.append(buerger)
        return buerger
