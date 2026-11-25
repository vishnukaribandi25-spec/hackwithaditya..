from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def test_eligibility_route_is_not_enabled_yet():
    response = client.post("/api/eligibility/match", json={})
    assert response.status_code == 404
