from fastapi.testclient import TestClient

from app.api.routes import eligibility as eligibility_route
from app.main import app
from app.models.eligibility import EligibilityRule
from app.models.profile import UserProfile
from app.models.scheme import Scheme
from app.services.eligibility_engine import evaluate_eligibility

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


def test_match_endpoint_returns_deterministic_results_without_gemini():
    response = client.post(
        "/api/eligibility/match",
        json={"state": "Telangana", "education_level": "graduate"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert {match["scheme_id"] for match in payload["matches"]} == {
        "mock-education-support",
        "mock-agriculture-support",
    }
    assert all(match["scheme"]["verification_status"] == "mock" for match in payload["matches"])
    assert all("explanation_reasons" in match for match in payload["matches"])


def test_check_endpoint_groups_results_and_includes_source_metadata():
    response = client.post(
        "/api/eligibility/check",
        json={"state": "Telangana", "education_level": "graduate"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert [item["scheme_id"] for item in payload["potentially_eligible"]] == [
        "mock-education-support"
    ]
    assert [item["scheme_id"] for item in payload["not_eligible"]] == [
        "mock-agriculture-support"
    ]
    assert payload["needs_verification"] == []

    failed_match = payload["not_eligible"][0]
    assert failed_match["failed_conditions"]
    assert failed_match["source_metadata"] == {
        "source_url": None,
        "application_url": None,
        "last_verified": None,
        "verification_status": "mock",
    }
    assert "not official" in payload["disclaimer"].lower()


def test_check_endpoint_groups_incomplete_profile_as_needs_verification():
    response = client.post("/api/eligibility/check", json={})

    assert response.status_code == 200
    payload = response.json()
    assert payload["potentially_eligible"] == []
    assert payload["not_eligible"] == []
    assert len(payload["needs_verification"]) == 2
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
