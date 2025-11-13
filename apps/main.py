from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from apps.buergerverwaltung.api.v1.main import app as registrierung_app

app = FastAPI(title="eVote - Hauptportal")

# Unter-App "Registrierung" einbinden
app.mount("/registrierung", registrierung_app)

@app.get("/", response_class=HTMLResponse)
def startseite():
    """Einfache Startseite mit Links zu Modulen"""
    html_content = """
    <html>
        <head>
            <title>eVote Hauptseite</title>
        </head>
        <body style='font-family: Arial; text-align: center;'>
            <h1>Willkommen beim eVote System</h1>
            <p>Wählen Sie eine Aktion:</p>
            <a href="/registrierung" style="
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                margin: 10px;
                text-decoration: none;
                border-radius: 5px;">Zur Registrierung</a>
            <a href="/abstimmung" style="
                display: inline-block;
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                margin: 10px;
                text-decoration: none;
                border-radius: 5px;">Zur Abstimmung</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
