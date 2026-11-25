import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_profile_is_returned_without_persistence():
    response = client.post(
        "/api/profile/validate",
        json={
            "age": 28,
            "state": "Telangana",
            "occupation": "Student",
            "education_level": "Undergraduate",
            "annual_family_income": 250000,
            "additional_attributes": {"course_type": "engineering"},
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "valid": True,
        "profile": {
            "age": 28,
            "state": "Telangana",
            "occupation": "Student",
            "education_level": "Undergraduate",
            "annual_family_income": 250000,
            "gender": None,
            "additional_attributes": {"course_type": "engineering"},
        },
    }


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("age", -1, "greater than or equal to 0"),
        ("age", 121, "less than or equal to 120"),
        ("annual_family_income", -1, "greater than or equal to 0"),
    ],
)
def test_invalid_age_or_income_returns_clear_validation_error(field, value, message):
    response = client.post("/api/profile/validate", json={field: value})

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == field and message in error["msg"] for error in errors)


def test_incomplete_profile_keeps_unknown_fields_unset():
    response = client.post("/api/profile/validate", json={})

    assert response.status_code == 200
    profile = response.json()["profile"]
    assert profile["age"] is None
    assert profile["state"] is None
    assert profile["occupation"] is None
    assert profile["education_level"] is None
    assert profile["annual_family_income"] is None
    assert profile["gender"] is None
    assert profile["additional_attributes"] == {}


@pytest.mark.parametrize(
    "payload",
    [
        {"aadhaar_number": "1234"},
        {"additional_attributes": {"bank_account_number": "1234"}},
        {"additional_attributes": {"otp": "000000"}},
    ],
)
def test_sensitive_or_unknown_profile_data_is_rejected(payload):
    response = client.post("/api/profile/validate", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"]
