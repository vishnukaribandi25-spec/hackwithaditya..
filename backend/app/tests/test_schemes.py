import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import scheme_service
from app.services.scheme_service import SchemeDataError


client = TestClient(app)


def test_list_schemes():
    response = client.get("/api/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) == 2
    assert all(scheme["verification_status"] == "mock" for scheme in schemes)
    assert all(scheme["application_url"] is None for scheme in schemes)
    assert all(scheme["source_url"] is None for scheme in schemes)


def test_filter_schemes_by_state_and_category():
    response = client.get("/api/schemes", params={"state": "telangana", "category": "EDUCATION"})
    assert response.status_code == 200
    schemes = response.json()
    assert [scheme["id"] for scheme in schemes] == ["mock-education-support"]


def test_filter_schemes_by_state():
    response = client.get("/api/schemes", params={"state": "Karnataka"})
    assert response.status_code == 200
    assert [scheme["id"] for scheme in response.json()] == ["mock-agriculture-support"]


def test_filter_schemes_by_category():
    response = client.get("/api/schemes", params={"category": "agriculture"})
    assert response.status_code == 200
    assert [scheme["id"] for scheme in response.json()] == ["mock-agriculture-support"]


def test_unknown_scheme_returns_404():
    response = client.get("/api/schemes/not-a-scheme")
    assert response.status_code == 404
    assert response.json()["detail"] == "Scheme not found"


def test_invalid_scheme_data_is_rejected(monkeypatch, tmp_path):
    invalid_data_path = tmp_path / "schemes.json"
    invalid_data_path.write_text(json.dumps([{"id": "incomplete"}]), encoding="utf-8")
    monkeypatch.setattr(scheme_service, "SCHEMES_DATA_PATH", invalid_data_path)

    with pytest.raises(SchemeDataError, match="invalid scheme data"):
        scheme_service.load_schemes()
