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
    ergebnisID: int = Field(ge=0)
    abstimmungsID: int = Field(ge=0)
    einzelwerte: List[Stimmenanzahl]
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def gesamtergebnis(self) -> int:
        return sum(e.anzahl for e in self.einzelwerte)

    def getErgebnisDetails(self) -> List[dict]:
        gesamt = self.gesamtergebnis or 1  # Division durch 0 verhindern
        return [
            {
                "Option": e.stimmoption.optionstext.value,
                "Stimmen": e.anzahl,
                "Prozent": round(e.anzahl / gesamt * 100, 2),
            }
            for e in self.einzelwerte
        ]

    def get_stimmen_fuer_option(self, option: Optionen) -> int:
        for e in self.einzelwerte:
            if e.stimmoption.optionstext == option:
                return e.anzahl
        return 0

    @field_validator("einzelwerte")
    @classmethod
    def validate_einzelwerte(cls, einzelwerte: List[Stimmenanzahl]) -> List[Stimmenanzahl]:
        if not einzelwerte:
            raise ValueError("Es müssen Stimmen für mindestens eine Option vorhanden sein.")
        optionen = [e.stimmoption.optionstext for e in einzelwerte]
        if len(set(optionen)) != len(optionen):
            raise ValueError("Jede Stimmoption darf nur einmal vorkommen.")

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
    print("Ja-Stimmen:", ergebnis.get_stimmen_fuer_option(Optionen.JA))