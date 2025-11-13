from fastapi import FastAPI, HTTPException
from typing import List
from apps.buergerverwaltung.domain.entities.buerger import (
    Buerger, lade_buerger_db, speichere_buerger_db
)
from apps.buergerverwaltung.services.registrierungs_service import Registrierungsservice

app = FastAPI(title="Registrierungs-Service")

# Bürgerdaten laden
buerger_db = lade_buerger_db()
registrierungs_service = Registrierungsservice(buerger_db)

@app.get("/", response_model=List[Buerger])
def alle_buerger():
    """Liste aller gespeicherten Bürger"""
    return buerger_db

@app.post("/registriere_buerger/", response_model=Buerger)
def registriere_buerger(buerger: Buerger):
    """Neuen Bürger registrieren"""
    neuer_buerger = registrierungs_service.registriere_buerger(buerger)
    speichere_buerger_db(buerger_db)
    return neuer_buerger
