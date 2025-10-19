def prompt_age():
    return int(input("Bitte gib dein Alter ein: "))

def test_prompt_age(monkeypatch):
    # Simuliere, dass der Benutzer "25" eingibt
    monkeypatch.setattr('builtins.input', lambda prompt="": "25")
    assert prompt_age() == 25