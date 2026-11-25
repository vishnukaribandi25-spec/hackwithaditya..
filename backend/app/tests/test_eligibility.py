import pytest
from fastapi.testclient import TestClient

from app.api.routes import eligibility as eligibility_route
from app.main import app
from app.models.eligibility import EligibilityRule
from app.models.profile import UserProfile
from app.models.scheme import Scheme
from app.services.eligibility_engine import evaluate_all, evaluate_eligibility
from app.services.scheme_service import load_schemes

client = TestClient(app)


def demo_rules() -> list[EligibilityRule]:
    return [
        EligibilityRule(type="state", values=["Telangana"]),
        EligibilityRule(type="age", min=18, max=60),
        EligibilityRule(type="annual_family_income", min=100000, max=300000),
        EligibilityRule(type="occupation", values=["student"]),
        EligibilityRule(type="education_level", values=["undergraduate"]),
        EligibilityRule(type="gender", values=["female"]),
        EligibilityRule(
            type="attribute",
            attribute="first_generation_student",
            operator="equals",
            value=True,
        ),
    ]


def complete_profile(**overrides) -> UserProfile:
    values = {
        "state": "Telangana",
        "age": 24,
        "annual_family_income": 200000,
        "occupation": "Student",
        "education_level": "Undergraduate",
        "gender": "female",
        "additional_attributes": {"first_generation_student": True},
    }
    values.update(overrides)
    return UserProfile(**values)


def test_all_supported_conditions_satisfied():
    result = evaluate_eligibility(complete_profile(), "demo-education", demo_rules())

    assert result.scheme_id == "demo-education"
    assert result.status == "potentially_eligible"
    assert len(result.matched_conditions) == 7
    assert result.failed_conditions == []
    assert result.missing_information == []


def test_one_failed_condition_means_not_eligible():
    result = evaluate_eligibility(
        complete_profile(state="Andhra Pradesh"),
        "demo-education",
        [EligibilityRule(type="state", values=["Telangana"])],
    )

    assert result.status == "not_eligible"
    assert result.failed_conditions
    assert result.matched_conditions == []


def test_state_and_occupation_matching_normalize_case_and_internal_whitespace():
    profile = UserProfile(
        state="  aNdHrA   pRaDeSh ",
        occupation="  fArMeR ",
    )
    result = evaluate_eligibility(
        profile,
        "normalized-profile",
        [
            EligibilityRule(type="state", values=["Andhra Pradesh"]),
            EligibilityRule(type="occupation", values=["farmer"]),
        ],
    )

    assert result.status == "potentially_eligible"
    assert len(result.matched_conditions) == 2


def test_missing_age_needs_verification():
    result = evaluate_eligibility(
        complete_profile(age=None),
        "demo-age",
        [EligibilityRule(type="age", min=18, max=60)],
    )

    assert result.status == "needs_verification"
    assert result.missing_information
    assert result.matched_conditions == []


def test_missing_income_needs_verification():
    result = evaluate_eligibility(
        complete_profile(annual_family_income=None),
        "demo-income",
        [EligibilityRule(type="annual_family_income", max=300000)],
    )

    assert result.status == "needs_verification"
    assert result.missing_information


def test_unknown_additional_attribute_value_needs_verification():
    result = evaluate_eligibility(
        complete_profile(additional_attributes={"first_generation_student": None}),
        "demo-attribute",
        [
            EligibilityRule(
                type="attribute",
                attribute="first_generation_student",
                operator="equals",
                value=True,
            )
        ],
    )

    assert result.status == "needs_verification"
    assert result.missing_information


def test_age_and_income_boundaries_are_inclusive():
    rules = [
        EligibilityRule(type="age", min=18, max=60),
        EligibilityRule(type="annual_family_income", min=100000, max=300000),
    ]

    lower_bound = evaluate_eligibility(
        complete_profile(age=18, annual_family_income=100000),
        "demo-boundaries",
        rules,
    )
    upper_bound = evaluate_eligibility(
        complete_profile(age=60, annual_family_income=300000),
        "demo-boundaries",
        rules,
    )

    assert lower_bound.status == "potentially_eligible"
    assert upper_bound.status == "potentially_eligible"


def test_unknown_rule_type_needs_verification():
    result = evaluate_eligibility(
        complete_profile(),
        "demo-unknown",
        [EligibilityRule(type="household_size", min=4)],
    )

    assert result.status == "needs_verification"
    assert "unsupported" in result.missing_information[0].lower()


def test_unsupported_field_on_known_rule_needs_verification():
    result = evaluate_eligibility(
        complete_profile(),
        "demo-unsupported-field",
        [EligibilityRule(type="age", min=18, operator="approximately")],
    )

    assert result.status == "needs_verification"
    assert "unsupported fields" in result.missing_information[0].lower()


def test_malformed_rule_needs_verification():
    result = evaluate_eligibility(
        complete_profile(),
        "demo-malformed-rule",
        [{"type": "age", "min": "eighteen"}],
    )

    assert result.status == "needs_verification"
    assert "malformed" in result.missing_information[0].lower()


def test_multiple_failed_conditions_are_reported():
    result = evaluate_eligibility(
        complete_profile(state="Karnataka", occupation="Teacher"),
        "demo-multiple-failures",
        [
            EligibilityRule(type="state", values=["Telangana"]),
            EligibilityRule(type="occupation", values=["Student"]),
        ],
    )

    assert result.status == "not_eligible"
    assert len(result.failed_conditions) == 2


def test_known_failure_takes_precedence_over_missing_information():
    result = evaluate_eligibility(
        complete_profile(state="Karnataka", age=None),
        "demo-failure-and-missing",
        [
            EligibilityRule(type="state", values=["Telangana"]),
            EligibilityRule(type="age", min=18),
        ],
    )

    assert result.status == "not_eligible"
    assert result.failed_conditions
    assert result.missing_information


def test_no_rules_needs_verification():
    result = evaluate_eligibility(complete_profile(), "demo-no-rules", [])

    assert result.status == "needs_verification"
    assert result.missing_information


PROFILE_CASES = {
    "A": {
        "state": "Andhra Pradesh",
        "age": 19,
        "occupation": "Student",
        "education_level": "Undergraduate",
        "annual_family_income": 80000,
        "social_category": "SC",
    },
    "B": {
        "state": "Karnataka",
        "age": 30,
        "occupation": "Private employee",
        "education_level": "Postgraduate",
        "annual_family_income": 1500000,
        "social_category": "General",
    },
    "C": {
        "state": "Andhra Pradesh",
        "age": 48,
        "occupation": "Farmer",
        "education_level": "Primary",
        "annual_family_income": 150000,
        "social_category": "OBC",
    },
    "D": {
        "state": "Andhra Pradesh",
        "age": 70,
        "occupation": "Retired",
        "education_level": "Primary",
        "annual_family_income": 60000,
        "social_category": "SC",
    },
    "E": {
        "state": "Telangana",
        "age": 22,
        "occupation": "Student",
        "education_level": "Postgraduate",
        "annual_family_income": 1000000,
        "social_category": "General",
    },
    "F": {
        "state": "Andhra Pradesh",
        "age": 25,
        "occupation": "Student",
        "education_level": "Undergraduate",
        "annual_family_income": 100000,
    },
}


def _synthetic_profile_rule_scheme() -> Scheme:
    return Scheme(
        id="synthetic-profile-rules",
        name="Synthetic test fixture (not a government scheme)",
        state="All India",
        department="Test fixture",
        category="test",
        description="Synthetic rules used only to test profile personalization.",
        benefits=[],
        eligibility_rules=[
            EligibilityRule(type="state", label="State", values=["Andhra Pradesh"]),
            EligibilityRule(type="age", label="Age", min=18, max=60),
            EligibilityRule(
                type="annual_family_income",
                label="Annual income",
                max=200000,
            ),
            EligibilityRule(
                type="occupation",
                label="Occupation",
                values=["student", "farmer"],
            ),
            EligibilityRule(
                type="education_level",
                label="Education",
                values=["undergraduate", "primary"],
            ),
            EligibilityRule(
                type="social_category",
                label="Social category",
                values=["SC", "OBC"],
            ),
        ],
        required_documents=[],
        application_url=None,
        source_url=None,
        last_verified=None,
        verification_status="mock",
        supported_languages=["en"],
    )


@pytest.mark.parametrize(
    ("case", "expected_status", "failed_labels"),
    [
        ("A", "potentially_eligible", set()),
        ("B", "not_eligible", {"State", "Annual income", "Occupation", "Education", "Social category"}),
        ("C", "potentially_eligible", set()),
        ("D", "not_eligible", {"Age", "Occupation"}),
        ("E", "not_eligible", {"State", "Annual income", "Education", "Social category"}),
        ("F", "needs_verification", set()),
    ],
)
def test_five_user_profiles_are_evaluated_from_rule_data(
    case, expected_status, failed_labels
):
    profile = UserProfile(**PROFILE_CASES[case])

    result = evaluate_eligibility(
        profile,
        "synthetic-profile-rules",
        _synthetic_profile_rule_scheme().eligibility_rules,
    )

    assert result.status == expected_status
    labels = {"State", "Age", "Annual income", "Occupation", "Education", "Social category"}
    actual_failed_labels = {
        label
        for label in labels
        if any(condition.startswith(f"{label} ") for condition in result.failed_conditions)
    }
    assert actual_failed_labels == failed_labels


def test_missing_social_category_needs_verification_when_rule_requires_it():
    profile = UserProfile(
        state="Andhra Pradesh",
        age=25,
        occupation="Student",
        education_level="Undergraduate",
        annual_family_income=100000,
    )
    result = evaluate_eligibility(
        profile,
        "synthetic-category-rule",
        [
            EligibilityRule(
                type="social_category",
                label="Social category",
                values=["SC", "OBC"],
            )
        ],
    )

    assert result.status == "needs_verification"
    assert result.missing_information
    assert not result.failed_conditions


@pytest.mark.parametrize("social_category", [None, "Prefer not to say"])
def test_unspecified_or_declined_category_is_not_treated_as_general(social_category):
    profile = UserProfile(social_category=social_category)
    result = evaluate_eligibility(
        profile,
        "synthetic-category-rule",
        [EligibilityRule(type="social_category", values=["SC"])],
    )

    assert result.status == "needs_verification"
    assert result.missing_information


def test_schemes_without_category_rules_are_not_blocked_by_missing_category():
    result = evaluate_eligibility(
        UserProfile(state="Andhra Pradesh"),
        "state-only-scheme",
        [EligibilityRule(type="state", values=["Andhra Pradesh"])],
    )

    assert result.status == "potentially_eligible"


def test_missing_profile_fields_do_not_pass_profile_rules():
    result = evaluate_eligibility(
        UserProfile(),
        "synthetic-profile-rules",
        _synthetic_profile_rule_scheme().eligibility_rules,
    )

    assert result.status == "needs_verification"
    assert not result.matched_conditions
    assert len(result.missing_information) == 6


def test_match_endpoint_returns_verified_recommendations_only():
    response = client.post(
        "/api/eligibility/match",
        json={"state": "Telangana", "education_level": "graduate"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert {match["scheme_id"] for match in payload["matches"]} == {
        match["scheme_id"]
        for match in payload["matches"]
        if match["status"] in {"potentially_eligible", "needs_verification"}
    }
    assert all(
        match["status"] != "not_eligible" for match in payload["matches"]
    )
    assert all("explanation_reasons" in match for match in payload["matches"])
    assert all(
        match["scheme"]["verification_status"] == "verified"
        for match in payload["matches"]
    )
    assert all(match["is_mock"] is False for match in payload["matches"])
    assert "mock" in payload["disclaimer"].lower()


@pytest.mark.parametrize("profile_data", PROFILE_CASES.values())
def test_profile_recommendations_match_deterministic_results(profile_data):
    match_response = client.post("/api/eligibility/match", json=profile_data)
    assert match_response.status_code == 200
    expected_ids = {
        result.scheme_id
        for result in evaluate_all(UserProfile(**profile_data), load_schemes())
        if result.status in {"potentially_eligible", "needs_verification"}
        and next(s for s in load_schemes() if s.id == result.scheme_id).verification_status == "verified"
        and eligibility_route._has_profile_relevant_match(
            UserProfile(**profile_data),
            next(s for s in load_schemes() if s.id == result.scheme_id),
        )
    }
    assert {
        item["scheme_id"] for item in match_response.json()["matches"]
    } == expected_ids


def test_recommendations_change_when_supported_profile_rules_change():
    recommendation_ids = {
        case: {
            item["scheme_id"]
            for item in client.post(
                "/api/eligibility/match",
                json=profile_data,
            ).json()["matches"]
        }
        for case, profile_data in PROFILE_CASES.items()
    }

    assert len({tuple(sorted(ids)) for ids in recommendation_ids.values()}) > 1
    assert recommendation_ids["A"] != recommendation_ids["B"]
    assert recommendation_ids["A"] != recommendation_ids["C"]


def test_repeated_and_irrelevant_profile_changes_are_deterministic():
    profile = PROFILE_CASES["A"]
    baseline = client.post("/api/eligibility/match", json=profile).json()
    repeated = client.post("/api/eligibility/match", json=profile).json()
    with_irrelevant_gender = client.post(
        "/api/eligibility/match",
        json={**profile, "gender": "prefer_not_to_say"},
    ).json()

    assert baseline == repeated
    assert baseline["matches"] == with_irrelevant_gender["matches"]


def test_check_endpoint_groups_results_and_includes_source_metadata():
    response = client.post(
        "/api/eligibility/check",
        json={"state": "Telangana", "education_level": "graduate"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["potentially_eligible"] == []
    assert {item["scheme_id"] for item in payload["mock_records"]} == {
        "mock-education-support"
    } | {"mock-agriculture-support"}
    assert {item["scheme_id"] for item in payload["not_eligible"]} == {
        "pradhan-mantri-matru-vandana-yojana",
        "ntr-bharosa-pension",
    }
    assert {item["scheme_id"] for item in payload["needs_verification"]} == {
        "pm-kisan-samman-nidhi",
        "pmay-gramin",
        "pm-usp-csss",
        "telangana-rythu-bharosa",
    }

    mock_failed_match = next(
        item for item in payload["mock_records"] if item["status"] == "not_eligible"
    )
    assert mock_failed_match["failed_conditions"]
    assert mock_failed_match["source_metadata"] == {
        "source_url": None,
        "application_url": None,
        "last_verified": None,
        "verification_status": "mock",
    }
    assert all(
        item["source_metadata"]["verification_status"] != "mock"
        for group in ("potentially_eligible", "not_eligible", "needs_verification")
        for item in payload[group]
    )
    assert "not official" in payload["disclaimer"].lower()


def test_check_endpoint_groups_incomplete_profile_as_needs_verification():
    response = client.post("/api/eligibility/check", json={})

    assert response.status_code == 200
    payload = response.json()
    assert payload["potentially_eligible"] == []
    assert payload["not_eligible"] == []
    assert len(payload["needs_verification"]) == 6
    assert len(payload["mock_records"]) == 2
    assert all(item["missing_information"] for item in payload["needs_verification"])


def test_check_endpoint_rejects_invalid_profile():
    response = client.post("/api/eligibility/check", json={"age": -1})

    assert response.status_code == 422
    assert any(
        error["loc"][-1] == "age"
        for error in response.json()["detail"]
    )


def test_check_endpoint_handles_empty_scheme_catalog(monkeypatch):
    monkeypatch.setattr(eligibility_route, "load_schemes", lambda: [])

    response = client.post("/api/eligibility/check", json={"state": "Telangana"})

    assert response.status_code == 200
    assert response.json()["potentially_eligible"] == []
    assert response.json()["not_eligible"] == []
    assert response.json()["needs_verification"] == []
    assert response.json()["mock_records"] == []


def test_check_endpoint_adds_ai_text_without_changing_engine_result(monkeypatch):
    scheme = Scheme(
        id="verified-demo",
        name="Synthetic verified scheme",
        state="Telangana",
        department="Synthetic test department",
        category="education",
        description="A synthetic fixture, not an official scheme.",
        benefits=["Synthetic test benefit."],
        eligibility_rules=[EligibilityRule(type="state", values=["Karnataka"])],
        required_documents=["Synthetic test document."],
        application_url=None,
        source_url="https://example.gov.in/scheme",
        last_verified="2026-01-15",
        verification_status="verified",
        supported_languages=["en", "te"],
    )

    class ExplanationService:
        def explain_eligibility(self, scheme, result, language):
            assert scheme.id == result.scheme_id
            assert language == "te"
            return "AI explanation only."

    monkeypatch.setattr(eligibility_route, "load_schemes", lambda: [scheme])
    monkeypatch.setattr(
        eligibility_route,
        "gemini_service",
        ExplanationService(),
    )

    response = client.post(
        "/api/eligibility/check?language=te",
        json={"state": "Telangana"},
    )

    assert response.status_code == 200
    result = response.json()["not_eligible"][0]
    assert result["status"] == "not_eligible"
    assert result["failed_conditions"]
    assert result["ai_explanation"] == "AI explanation only."


def test_match_endpoint_uses_profile_values_and_excludes_mock(monkeypatch):
    scheme = _synthetic_profile_rule_scheme().model_copy(
        update={"verification_status": "verified"}
    )
    monkeypatch.setattr(eligibility_route, "load_schemes", lambda: [scheme])

    response = client.post(
        "/api/eligibility/match",
        json={
            "state": "Andhra Pradesh",
            "age": 19,
            "occupation": "Student",
            "education_level": "Undergraduate",
            "annual_family_income": 80000,
            "social_category": "SC",
        },
    )

    assert response.status_code == 200
    assert len(response.json()["matches"]) == 1
    assert response.json()["matches"][0]["status"] == "potentially_eligible"
    assert response.json()["matches"][0]["scheme"]["verification_status"] == "verified"


def test_farmer_profile_returns_pm_kisan_for_verification_not_confirmed_eligibility():
    response = client.post(
        "/api/eligibility/match",
        json={
            "state": "Andhra Pradesh",
            "age": 48,
            "occupation": "Farmer",
            "education_level": "Primary",
            "annual_family_income": 150000,
            "social_category": "General",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    matches = payload["matches"]
    assert all(item["is_mock"] is False for item in matches)
    assert {item["verification_status"] for item in matches} == {"verified"}
    assert {item["scheme_id"] for item in matches} == {"pm-kisan-samman-nidhi"}

    pm_kisan = matches[0]
    assert pm_kisan["status"] == "needs_verification"
    assert pm_kisan["verification_required"] is True
    assert pm_kisan["scheme_name"].startswith("Pradhan Mantri Kisan")
    assert pm_kisan["source_url"] == "https://pmkisan.gov.in/homenew.aspx"
    assert pm_kisan["last_verified_date"] == "2026-11-25"
    assert any("landholding farmer family is not provided" in text for text in pm_kisan["missing_information"])
    assert any("land records" in text.lower() and "e-kyc" in text.lower() for text in pm_kisan["missing_information"])
    assert any("e-KYC" in step for step in pm_kisan["verification_steps"])
    assert "pmay-gramin" in {item["scheme_id"] for item in payload["not_applicable"]}
    assert all("mock" not in item["scheme_name"].lower() for item in matches)


def test_farmer_landholding_self_report_does_not_replace_official_verification():
    response = client.post(
        "/api/eligibility/match",
        json={
            "state": "Andhra Pradesh",
            "age": 48,
            "occupation": "Farmer",
            "additional_attributes": {
                "pm_kisan_landholding_farmer_family": True,
            },
        },
    )

    assert response.status_code == 200
    pm_kisan = next(
        item for item in response.json()["matches"]
        if item["scheme_id"] == "pm-kisan-samman-nidhi"
    )
    assert pm_kisan["status"] == "needs_verification"
    assert any("landholding farmer family matches" in text.lower() for text in pm_kisan["matched_conditions"])
    assert any("land records" in text.lower() and "e-kyc" in text.lower() for text in pm_kisan["missing_information"])


@pytest.mark.parametrize(
    ("state", "occupation", "education_level"),
    [
        ("telangana", "farmer", "highschool"),
        ("Telangana", "Farmer", "high_school"),
        (" TELANGANA ", " FARMER ", "High School"),
        ("Telangana", "Farmer", "secondary"),
    ],
)
def test_telangana_farmer_aliases_reach_supported_rules_without_false_eligibility(
    state, occupation, education_level
):
    response = client.post(
        "/api/eligibility/match",
        json={
            "state": state,
            "age": 50,
            "occupation": occupation,
            "education_level": education_level,
            "annual_family_income": 50000,
            "social_category": "General",
            "additional_attributes": {
                "residence_type": "rural",
                "owns_pucca_house": True,
                "landholding_farmer_family": True,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert {item["scheme_id"] for item in payload["matches"]} == {
        "pm-kisan-samman-nidhi",
        "telangana-rythu-bharosa",
    }
    assert all(item["is_mock"] is False for item in payload["matches"])

    pm_kisan = payload["matches"][0]
    assert pm_kisan["status"] == "needs_verification"
    assert any("landholding farmer family matches" in text.lower() for text in pm_kisan["matched_conditions"])
    assert any("land records" in text.lower() and "e-kyc" in text.lower() for text in pm_kisan["missing_information"])
    assert any("self-reported" in text.lower() and "beneficiary records" in text.lower() for text in pm_kisan["missing_information"])
    assert any("e-KYC" in step for step in pm_kisan["verification_steps"])

    not_applicable = {
        item["scheme_id"]: item for item in payload["not_applicable"]
    }
    pmay = not_applicable["pmay-gramin"]
    assert pmay["status"] == "not_eligible"
    assert any("pucca house" in text.lower() for text in pmay["failed_conditions"])
    assert not_applicable[
        "pradhan-mantri-matru-vandana-yojana"
    ]["failed_conditions"] == ["State availability is excluded from this scheme."]
    assert "pm-usp-csss" in not_applicable
    assert "ntr-bharosa-pension" in not_applicable
    assert all(item["is_mock"] is False for item in payload["not_applicable"])


def test_farmer_self_report_outside_landholding_rule_is_not_recommended():
    response = client.post(
        "/api/eligibility/match",
        json={
            "state": "Andhra Pradesh",
            "occupation": "Farmer",
            "additional_attributes": {
                "pm_kisan_landholding_farmer_family": False,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "pm-kisan-samman-nidhi" not in {
        item["scheme_id"] for item in payload["matches"]
    }
    pm_kisan = next(
        item for item in payload["not_applicable"]
        if item["scheme_id"] == "pm-kisan-samman-nidhi"
    )
    assert pm_kisan["status"] == "not_eligible"
    assert pm_kisan["failed_conditions"]


def test_non_farmer_and_urban_profiles_do_not_get_farmer_or_rural_housing_matches():
    response = client.post(
        "/api/eligibility/match",
        json={
            "state": "Karnataka",
            "age": 30,
            "occupation": "Private employee",
            "additional_attributes": {
                "resides_in_rural_area": False,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert not {
        item["scheme_id"] for item in payload["matches"]
    } & {"pm-kisan-samman-nidhi", "pmay-gramin", "ntr-bharosa-pension"}
    ntr = next(
        item for item in payload["not_applicable"]
        if item["scheme_id"] == "ntr-bharosa-pension"
    )
    assert ntr["status"] == "not_eligible"


def test_rural_household_is_not_confirmed_for_pmay_without_housing_information():
    response = client.post(
        "/api/eligibility/match",
        json={
            "state": "Andhra Pradesh",
            "occupation": "Farmer",
            "additional_attributes": {
                "resides_in_rural_area": True,
            },
        },
    )

    assert response.status_code == 200
    pmay = next(
        item for item in response.json()["matches"]
        if item["scheme_id"] == "pmay-gramin"
    )
    assert pmay["status"] == "needs_verification"
    assert any("pucca house is not provided" in text.lower() for text in pmay["missing_information"])


def test_student_profile_does_not_receive_farmer_scheme_as_recommendation():
    response = client.post(
        "/api/eligibility/match",
        json={
            "state": "Andhra Pradesh",
            "age": 19,
            "occupation": "Student",
            "education_level": "Undergraduate",
            "annual_family_income": 80000,
        },
    )

    assert response.status_code == 200
    ids = {item["scheme_id"] for item in response.json()["matches"]}
    assert "pm-usp-csss" in ids
    assert "pm-kisan-samman-nidhi" not in ids
    assert "telangana-rythu-bharosa" not in ids


def test_telangana_farmer_receives_rythu_bharosa_for_verification_only():
    response = client.post(
        "/api/eligibility/match",
        json={"state": "telangana", "occupation": "farmer"},
    )

    assert response.status_code == 200
    match = next(
        item
        for item in response.json()["matches"]
        if item["scheme_id"] == "telangana-rythu-bharosa"
    )
    assert match["status"] == "needs_verification"
    assert match["verification_required"] is True
    assert match["missing_information"]
    assert "detailed beneficiary eligibility" in match["missing_information"][0]
    assert match["is_mock"] is False


def test_empty_profile_does_not_fall_back_to_mock_catalogue_records():
    response = client.post("/api/eligibility/match", json={})

    assert response.status_code == 200
    payload = response.json()
    assert payload["matches"] == []
    assert len(payload["not_applicable"]) == 6
    assert all(item["is_mock"] is False for item in payload["not_applicable"])
    assert all(item["verification_status"] == "verified" for item in payload["not_applicable"])


def test_profile_with_no_relevant_verified_scheme_returns_empty_recommendations():
    response = client.post(
        "/api/eligibility/match",
        json={"state": "Sikkim", "occupation": "Teacher"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["matches"] == []
    assert {item["scheme_id"] for item in payload["not_applicable"]} == {
        "pm-kisan-samman-nidhi",
        "pmay-gramin",
        "pradhan-mantri-matru-vandana-yojana",
        "pm-usp-csss",
        "ntr-bharosa-pension",
        "telangana-rythu-bharosa",
    }
    assert all(item["is_mock"] is False for item in payload["not_applicable"])


def test_check_endpoint_keeps_mock_records_out_of_verified_status_groups(monkeypatch):
    mock_scheme = _synthetic_profile_rule_scheme()
    monkeypatch.setattr(eligibility_route, "load_schemes", lambda: [mock_scheme])

    response = client.post(
        "/api/eligibility/check",
        json={"state": "Andhra Pradesh", "social_category": "SC"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["potentially_eligible"] == []
    assert payload["not_eligible"] == []
    assert payload["needs_verification"] == []
    assert [item["scheme_id"] for item in payload["mock_records"]] == [
        "synthetic-profile-rules"
    ]


def test_gemini_unavailable_does_not_change_eligibility_status(monkeypatch):
    scheme = Scheme(
        id="verified-demo",
        name="Synthetic verified scheme",
        state="Andhra Pradesh",
        department="Synthetic test department",
        category="education",
        description="A synthetic fixture, not an official scheme.",
        benefits=[],
        eligibility_rules=[EligibilityRule(type="state", values=["Andhra Pradesh"])],
        required_documents=[],
        application_url=None,
        source_url="https://example.gov.in/scheme",
        last_verified="2026-01-15",
        verification_status="verified",
        supported_languages=["en", "te"],
    )

    class UnavailableExplanationService:
        def explain_eligibility(self, scheme, result, language):
            return None

    monkeypatch.setattr(eligibility_route, "load_schemes", lambda: [scheme])
    monkeypatch.setattr(
        eligibility_route,
        "gemini_service",
        UnavailableExplanationService(),
    )
    expected = evaluate_eligibility(
        UserProfile(state="Andhra Pradesh"),
        scheme.id,
        scheme.eligibility_rules,
    )

    response = client.post(
        "/api/eligibility/check",
        json={"state": "Andhra Pradesh"},
    )

    assert response.status_code == 200
    result = response.json()["potentially_eligible"][0]
    assert result["status"] == expected.status
    assert result["matched_conditions"] == expected.matched_conditions
    assert result["ai_explanation"] is None
