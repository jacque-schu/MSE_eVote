from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class BuergerIdentity:
    """DDD Value Object: Bürger-Identität für Auth (kein volles Bürger-Modell!)."""
    buerger_id: int
    email: str
    name: str
    
    @classmethod
    def from_buerger(cls, buerger):
        return cls(buerger.buergerID, buerger.email, buerger.name)
