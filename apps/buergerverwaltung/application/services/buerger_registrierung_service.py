from fastapi import HTTPException
from typing import Dict
from apps.shared.aspects.auth_aspect import hash_password
from ...domain.repositories.i_buerger_repository import IBuergerRepository
from ...domain.models.buerger import Buerger

class BuergerRegistrierungService:
    def __init__(self, buerger_repo: IBuergerRepository):
        self.repo = buerger_repo
    
    def registriere(self, vorname: str, nachname: str, adresse: str, 
                    geburtsdatum: str, email: str, pw: str) -> Dict[str, str]:
        # 1. Duplicate-Check (Repository)
        if self.repo.finde_nach_email(email):
            raise HTTPException(409, detail="E-Mail bereits registriert")
        
        # 2. Hash PW
        pw_hash = hash_password(pw)
        
        # 3. Domain Entity erstellen (validiert selbst!)
        name = f"{vorname.strip()} {nachname.strip()}"
        neue_id = self.repo.naechste_buerger_id()
        buerger = Buerger(
            buergerID=neue_id, name=name, adresse=adresse,
            geburtsdatum=geburtsdatum, email=email,
            authentifizierungsdaten=pw_hash
        )
        
        # 4. Persistieren
        self.repo.fuege_hinzu(buerger)
        return {"message": f"Bürger '{name}' erfolgreich registriert"}
