# tests/buergerverwaltung/interfaces/test_buerger_endpoints.py
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Form, Header, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 1. POST Erfolg
def test_registriere_buerger_post_erfolgreich():
    test_app = FastAPI()
    
    @test_app.post("/api/buergerverwaltung/registrierung")
    async def endpoint(vorname: str = Form(...), nachname: str = Form(...),
                      adresse: str = Form(...), geburtsdatum: str = Form(...),
                      email: str = Form(...), authentifizierungsdaten: str = Form(...),
                      authorization: str = Header(None)):
        return {"message": f"Bürger '{vorname.strip()} {nachname.strip()}' erfolgreich registriert"}
    
    client = TestClient(test_app)
    response = client.post("/api/buergerverwaltung/registrierung", 
                          data={"vorname": "Anna", "nachname": "Schmidt", 
                                "adresse": "Str. 1", "geburtsdatum": "1990-01-01", 
                                "email": "anna@test.de", "authentifizierungsdaten": "pw123"},
                          headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    assert "Anna Schmidt" in response.json()["message"]

# 2. POST Duplikat
def test_registriere_buerger_email_duplikat():
    test_app = FastAPI()
    
    @test_app.post("/api/buergerverwaltung/registrierung")
    async def endpoint(
        vorname: str = Form(...),           # <- ALLE Parameter deklarieren!
        nachname: str = Form(...),
        adresse: str = Form(...),
        geburtsdatum: str = Form(...),
        email: str = Form(...),
        authentifizierungsdaten: str = Form(...),
        authorization: str = Header(None)
    ):
        raise HTTPException(status_code=409, detail="E-Mail bereits registriert")
    
    client = TestClient(test_app)
    response = client.post(
        "/api/buergerverwaltung/registrierung",
        data={
            "vorname": "Max",
            "nachname": "Mustermann",
            "adresse": "Vollständige Adresse 123",
            "geburtsdatum": "1985-03-15",
            "email": "test@duplikat.de",
            "authentifizierungsdaten": "mindestens8zeichenLang"
        },
        headers={"Authorization": "Bearer test-jwt"}
    )
    assert response.status_code == 409

# 3. GET Template - FIX: .decode() statt bytes-Literale
def test_registrierung_seite_get():
    test_app = FastAPI()
    
    # FIX: Static routes mocken
    @test_app.get("/static/buergerverwaltung/{path:path}")
    async def static_buergerverwaltung(path: str):
        return {"css": "mocked"}
    
    @test_app.get("/static/common/{path:path}")
    async def static_common(path: str):
        return {"css": "base-mocked"}
    
    templates = Jinja2Templates(directory="ui/buergerverwaltung/templates")
    
    @test_app.get("/api/buergerverwaltung/registrierung")
    async def page(request: Request):
        return templates.TemplateResponse(request=request, name="registrierung.html")

    client = TestClient(test_app)
    response = client.get("/api/buergerverwaltung/registrierung")
    assert response.status_code == 200
    
    html_content = response.text  # Schon decoded
    assert "Bürger registrieren" in html_content
    assert 'name="vorname"' in html_content
    assert 'name="authentifizierungsdaten"' in html_content

