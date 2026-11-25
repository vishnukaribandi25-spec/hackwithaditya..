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
            "social_category": "SC",
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
            "social_category": "SC",
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
    assert profile["social_category"] is None
    assert profile["gender"] is None
    assert profile["additional_attributes"] == {}


def test_social_category_is_optional_and_allowlisted():
    response = client.post(
        "/api/profile/validate",
        json={"social_category": "Prefer not to say"},
    )

    assert response.status_code == 200
    assert response.json()["profile"]["social_category"] == "Prefer not to say"


def test_profile_normalizes_known_case_and_education_aliases():
    response = client.post(
        "/api/profile/validate",
        json={
            "state": "  telangana ",
            "occupation": " farmer ",
            "education_level": "High School",
            "social_category": "general",
            "additional_attributes": {
                "residence_type": " RURAL ",
                "owns_pucca_house": True,
                "landholding_farmer_family": True,
            },
        },
    )

    assert response.status_code == 200
    profile = response.json()["profile"]
    assert profile["state"] == "Telangana"
    assert profile["occupation"] == "Farmer"
    assert profile["education_level"] == "secondary"
    assert profile["social_category"] == "General"
    assert profile["additional_attributes"] == {
        "resides_in_rural_area": True,
        "household_owns_pucca_house": True,
        "pm_kisan_landholding_farmer_family": True,
    }


@pytest.mark.parametrize(
    ("education_level", "normalized"),
    [
        ("highschool", "secondary"),
        ("high_school", "secondary"),
        ("High School", "secondary"),
        ("secondary", "secondary"),
        ("Some Unlisted Study", "Some Unlisted Study"),
    ],
)
def test_education_aliases_are_normalized_without_reclassifying_unknown_values(
    education_level, normalized
):
    response = client.post(
        "/api/profile/validate",
        json={"education_level": education_level},
    )

    assert response.status_code == 200
    assert response.json()["profile"]["education_level"] == normalized


@pytest.mark.parametrize(
    ("attributes", "message"),
    [
        (
            {"owns_pucca_house": "true"},
            "household_owns_pucca_house must be a JSON boolean",
        ),
        (
            {"resides_in_rural_area": "true"},
            "resides_in_rural_area must be a JSON boolean",
        ),
        (
            {
                "residence_type": "rural",
                "resides_in_rural_area": False,
            },
            "conflicts with resides_in_rural_area",
        ),
        (
            {"residence_type": "suburban"},
            "residence_type must be 'rural' or 'urban'",
        ),
    ],
)
def test_additional_attribute_alias_errors_identify_the_invalid_field(
    attributes, message
):
    response = client.post(
        "/api/profile/validate",
        json={"additional_attributes": attributes},
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"][-1] == "additional_attributes"
    assert message in error["msg"]


def test_invalid_social_category_is_not_echoed_in_validation_error():
    response = client.post(
        "/api/profile/validate",
        json={"social_category": "sensitive user-entered value"},
    )

    assert response.status_code == 422
    assert "sensitive user-entered value" not in response.text


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
