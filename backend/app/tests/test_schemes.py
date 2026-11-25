import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import scheme_service
from app.models.profile import UserProfile
from app.services.eligibility_engine import evaluate
from app.services.scheme_service import SchemeDataError


client = TestClient(app)


def test_list_schemes():
    response = client.get("/api/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) == 8
    assert sum(scheme["verification_status"] == "mock" for scheme in schemes) == 2
    assert sum(scheme["verification_status"] == "verified" for scheme in schemes) == 6
    mock_schemes = [scheme for scheme in schemes if scheme["verification_status"] == "mock"]
    assert all(scheme["application_url"] is None for scheme in mock_schemes)
    assert all(scheme["source_url"] is None for scheme in mock_schemes)


def test_filter_schemes_by_state_and_category():
    response = client.get("/api/schemes", params={"state": "telangana", "category": "EDUCATION"})
    assert response.status_code == 200
    schemes = response.json()
    assert {scheme["id"] for scheme in schemes} == {
        "mock-education-support",
        "pm-usp-csss",
    }


def test_filter_schemes_by_state():
    response = client.get("/api/schemes", params={"state": "Karnataka"})
    assert response.status_code == 200
    assert {scheme["id"] for scheme in response.json()} == {
        "mock-agriculture-support",
        "pm-kisan-samman-nidhi",
        "pmay-gramin",
        "pradhan-mantri-matru-vandana-yojana",
        "pm-usp-csss",
    }


def test_filter_schemes_by_category():
    response = client.get("/api/schemes", params={"category": "agriculture"})
    assert response.status_code == 200
    assert {scheme["id"] for scheme in response.json()} == {
        "mock-agriculture-support",
        "pm-kisan-samman-nidhi",
        "telangana-rythu-bharosa",
    }


def test_state_filter_excludes_states_where_scheme_is_not_implemented():
    response = client.get(
        "/api/schemes",
        params={"state": "telangana", "category": "women"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_verified_dataset_has_six_official_records_with_complete_metadata():
    response = client.get("/api/schemes")
    verified = [
        scheme
        for scheme in response.json()
        if scheme["verification_status"] == "verified"
    ]

    assert {scheme["id"] for scheme in verified} == {
        "pm-kisan-samman-nidhi",
        "pmay-gramin",
        "pradhan-mantri-matru-vandana-yojana",
        "pm-usp-csss",
        "ntr-bharosa-pension",
        "telangana-rythu-bharosa",
    }
    for scheme in verified:
        assert scheme["government_level"] in {"central", "state"}
        assert scheme["department"]
        assert scheme["source_url"].endswith(".gov.in/") or ".gov.in/" in scheme["source_url"]
        assert scheme["application_url"]
        assert scheme["last_verified"] == "2026-11-25"
        assert "application_process" in scheme
        assert "eligibility_summary" in scheme
        assert "unavailable_fields" in scheme


@pytest.mark.parametrize(
    ("scheme_id", "profile_data", "expected_status"),
    [
        ("pm-kisan-samman-nidhi", {"occupation": "farmer"}, "needs_verification"),
        ("pm-kisan-samman-nidhi", {"occupation": "student"}, "not_eligible"),
        (
            "pmay-gramin",
            {
                "additional_attributes": {
                    "resides_in_rural_area": True,
                    "household_owns_pucca_house": False,
                }
            },
            "needs_verification",
        ),
        (
            "pmay-gramin",
            {
                "additional_attributes": {
                    "resides_in_rural_area": False,
                    "household_owns_pucca_house": False,
                }
            },
            "not_eligible",
        ),
        (
            "pradhan-mantri-matru-vandana-yojana",
            {"state": "Andhra Pradesh"},
            "needs_verification",
        ),
        (
            "pradhan-mantri-matru-vandana-yojana",
            {"state": "Telangana"},
            "not_eligible",
        ),
        ("pm-usp-csss", {"occupation": "student"}, "needs_verification"),
        ("pm-usp-csss", {"occupation": "teacher"}, "not_eligible"),
        ("ntr-bharosa-pension", {"state": "Andhra Pradesh"}, "needs_verification"),
        ("ntr-bharosa-pension", {"state": "Telangana"}, "not_eligible"),
        (
            "telangana-rythu-bharosa",
            {"state": "Telangana", "occupation": "farmer"},
            "needs_verification",
        ),
        (
            "telangana-rythu-bharosa",
            {"state": "Telangana", "occupation": "teacher"},
            "not_eligible",
        ),
        (
            "telangana-rythu-bharosa",
            {"state": "Andhra Pradesh", "occupation": "farmer"},
            "not_eligible",
        ),
    ],
)
def test_verified_scheme_eligibility_is_conservative(
    scheme_id, profile_data, expected_status
):
    scheme = next(
        scheme for scheme in scheme_service.load_schemes() if scheme.id == scheme_id
    )

    result = evaluate(UserProfile(**profile_data), scheme)

    assert result.status == expected_status
    if expected_status == "needs_verification":
        assert result.missing_information


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
