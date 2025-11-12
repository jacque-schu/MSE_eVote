# apps/buergerverwaltung/api/v1/buerger.py
from fastapi import APIRouter, HTTPException, Depends
from apps.buergerverwaltung.domain.services.authentifizierungs_service import AuthentifizierungsService
from apps.buergerverwaltung.domain.services.registrierungs_service import RegistrierungsService
from apps.buergerverwaltung.domain.models import Buerger
from sqlalchemy.orm import Session
from apps.database import SessionLocal

router = APIRouter()

# Dependency zur Datenbankverbindung
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registrieren")
def register_buerger(buerger_data: dict, db: Session = Depends(get_db)):
    try:
        registrierungs_service = RegistrierungsService(db)
        new_buerger = registrierungs_service.register_buerger(buerger_data)
        return {"message": "Bürger erfolgreich registriert", "buerger": new_buerger}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_buerger(email: str, password: str, db: Session = Depends(get_db)):
    auth_service = AuthentifizierungsService()
    user = auth_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Ungültige Anmeldedaten")
    # Token erstellen und zurückgeben
    token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
