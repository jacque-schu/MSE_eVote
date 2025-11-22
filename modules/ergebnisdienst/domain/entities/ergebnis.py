from typing import List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class Optionen(str, Enum):
    JA = "Ja"
    NEIN = "Nein"
    ENTHALTUNG = "Enthaltung"

class Stimmoption(BaseModel):
    optionstext: Optionen

class Stimmenanzahl(BaseModel):
    stimmoption: Stimmoption
    anzahl: int = Field(ge=0)

class Ergebnis(BaseModel):
    ergebnisID: int
    abstimmungsID: int
    einzelwerte: List[Stimmenanzahl]
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def gesamtergebnis(self) -> int:
        return sum(e.anzahl for e in self.einzelwerte)

    def getErgebnisDetails(self) -> List[dict]:
        return [
            {"Option": e.stimmoption.optionstext.value, "Stimmen": e.anzahl}
            for e in self.einzelwerte
        ]

    @field_validator("einzelwerte")
    @classmethod
    def validate_einzelwerte(cls, einzelwerte):
        if not einzelwerte or len(einzelwerte) == 0:
            raise ValueError("Es müssen Stimmen für mindestens eine Option vorhanden sein.")
        return einzelwerte

# Beispiel-Test
if __name__ == "__main__":
    ja = Stimmoption(optionstext=Optionen.JA)
    nein = Stimmoption(optionstext=Optionen.NEIN)
    enth = Stimmoption(optionstext=Optionen.ENTHALTUNG)
    stimmen = [
        Stimmenanzahl(stimmoption=ja, anzahl=10),
        Stimmenanzahl(stimmoption=nein, anzahl=7),
        Stimmenanzahl(stimmoption=enth, anzahl=3)
    ]
    ergebnis = Ergebnis(ergebnisID=1, abstimmungsID=99, einzelwerte=stimmen)
    print("Gesamtergebnis:", ergebnis.gesamtergebnis)
    print("Details:", ergebnis.getErgebnisDetails())
