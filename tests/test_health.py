from fastapi.testclient import TestClient
from apps.main import app


def test_health_ok():
    client = TestClient(app)
    r = client.get("/health")
    print("Response status code:", r.status_code)
    print("Response JSON:", r.json())
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}