from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.api.routes import chat as chat_route
from app.main import app
from app.models.eligibility import EligibilityRule
from app.models.scheme import Scheme
from app.services import chat_service as chat_service_module
from app.services.chat_service import ChatGuidanceService, classify_intent

client = TestClient(app)


def verified_scheme(**updates) -> Scheme:
    values = {
        "id": "test-student-scholarship",
        "name": "Test Student Scholarship",
        "state": "Telangana",
        "department": "Test Department",
        "category": "education",
        "description": "Synthetic test record; not a government scheme.",
        "benefits": ["Synthetic tuition support."],
        "eligibility_rules": [
            EligibilityRule(type="state", values=["Telangana"]),
            EligibilityRule(type="age", min=18, max=30),
        ],
        "required_documents": ["Synthetic student certificate."],
        "application_url": None,
        "source_url": "https://example.com/test-student-scholarship",
        "last_verified": date(2026, 1, 15),
        "verification_status": "verified",
        "supported_languages": ["en", "te"],
    }
    values.update(updates)
    return Scheme(**values)


class FakeGeminiService:
    def __init__(self, reply: str | None = None):
        self.reply = reply
        self.calls = []

    def generate_guidance(self, **kwargs):
        self.calls.append(kwargs)
        return self.reply


def use_test_service(monkeypatch, schemes, gemini_service):
    monkeypatch.setattr(
        chat_service_module,
        "load_schemes",
        lambda: schemes,
    )
    monkeypatch.setattr(
        chat_route,
        "chat_service",
        ChatGuidanceService(gemini_service=gemini_service),
    )


@pytest.mark.parametrize(
    ("message", "intent"),
    [
        ("Find schemes for students", "finding_schemes"),
        ("Am I eligible for a scheme?", "eligibility"),
        ("What benefits does it provide?", "benefits"),
        ("Which documents are required?", "required_documents"),
        ("How do I apply?", "application_process"),
        ("What is a government scheme?", "general_government_schemes"),
        ("పథకాలు చూపించండి", "finding_schemes"),
        ("ఈ పథకానికి అర్హత ఉందా?", "eligibility"),
        ("ప్రయోజనాలు ఏమిటి?", "benefits"),
        ("ఏ పత్రాలు అవసరం?", "required_documents"),
        ("దరఖాస్తు ఎలా చేయాలి?", "application_process"),
    ],
)
def test_classifies_english_and_telugu_chat_intents(message, intent):
    assert classify_intent(message) == intent


def test_chat_returns_english_guidance_from_verified_scheme(monkeypatch):
    scheme = verified_scheme()
    gemini = FakeGeminiService("The verified benefit is synthetic tuition support.")
    use_test_service(monkeypatch, [scheme], gemini)

    response = client.post(
        "/api/chat",
        json={
            "message": "What benefits does Test Student Scholarship provide?",
            "language": "en",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "benefits"
    assert payload["language"] == "en"
    assert payload["reply"] == gemini.reply
    assert payload["schemes"][0]["scheme_id"] == scheme.id
    assert payload["schemes"][0]["source_url"] == str(scheme.source_url)
    assert gemini.calls[0]["language"] == "en"
    assert gemini.calls[0]["scheme_facts"][0]["verification_status"] == "verified"


def test_chat_returns_telugu_guidance(monkeypatch):
    scheme = verified_scheme()
    gemini = FakeGeminiService("ధృవీకరించిన ప్రయోజనం: సింథటిక్ విద్యా సహాయం.")
    use_test_service(monkeypatch, [scheme], gemini)

    response = client.post(
        "/api/chat",
        json={
            "message": "Test Student Scholarship పథకం ప్రయోజనాలు ఏమిటి?",
            "language": "te",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "benefits"
    assert payload["language"] == "te"
    assert payload["reply"] == gemini.reply
    assert gemini.calls[0]["language"] == "te"


def test_finding_schemes_returns_only_verified_records(monkeypatch):
    verified = verified_scheme()
    mock = verified_scheme(
        id="mock-scholarship",
        name="Mock Scholarship",
        verification_status="mock",
        source_url=None,
        last_verified=None,
    )
    gemini = FakeGeminiService(reply=None)
    use_test_service(monkeypatch, [verified, mock], gemini)

    response = client.post(
        "/api/chat",
        json={"message": "Find schemes for students"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert [scheme["scheme_id"] for scheme in payload["schemes"]] == [verified.id]
    assert verified.name in payload["reply"]


def test_eligibility_without_profile_reports_missing_information(monkeypatch):
    scheme = verified_scheme()
    gemini = FakeGeminiService()
    use_test_service(monkeypatch, [scheme], gemini)

    response = client.post(
        "/api/chat",
        json={
            "message": "Am I eligible for Test Student Scholarship?",
            "language": "en",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    eligibility = payload["schemes"][0]["eligibility"]
    assert eligibility["status"] == "needs_verification"
    assert any("age" in item.lower() for item in eligibility["missing_information"])
    assert payload["missing_information"]
    assert "more information" in payload["reply"].lower()
    assert gemini.calls == []


def test_unknown_scheme_is_not_matched_to_another_verified_record(monkeypatch):
    gemini = FakeGeminiService("This should not be used.")
    use_test_service(monkeypatch, [verified_scheme()], gemini)

    response = client.post(
        "/api/chat",
        json={"message": "What are the benefits of Unknown Grant?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["schemes"] == []
    assert payload["missing_information"]
    assert "couldn't find" in payload["reply"].lower()
    assert gemini.calls == []


def test_application_guidance_reports_missing_steps_without_gemini(monkeypatch):
    scheme = verified_scheme()
    gemini = FakeGeminiService("Submit an online form.")
    use_test_service(monkeypatch, [scheme], gemini)

    response = client.post(
        "/api/chat",
        json={
            "message": "How do I apply for Test Student Scholarship?",
            "language": "en",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "application_process"
    assert any("application steps" in item.lower() for item in payload["missing_information"])
    assert any("application URL" in item for item in payload["missing_information"])
    assert "verified application steps are unavailable" in payload["reply"]
    assert "no verified application link" in payload["reply"]
    assert gemini.calls == []


def test_application_guidance_uses_verified_application_steps(monkeypatch):
    scheme = verified_scheme(
        application_process=["Submit the official application after checking eligibility."],
        application_url="https://example.gov.in/apply",
    )
    gemini = FakeGeminiService("This should not be used.")
    use_test_service(monkeypatch, [scheme], gemini)

    response = client.post(
        "/api/chat",
        json={
            "message": "How do I apply for Test Student Scholarship?",
            "language": "en",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "Submit the official application" in payload["reply"]
    assert "https://example.gov.in/apply" in payload["reply"]
    assert payload["schemes"][0]["application_process"] == scheme.application_process
    assert not payload["missing_information"]
    assert gemini.calls == []


def test_gemini_failure_returns_deterministic_verified_facts(monkeypatch):
    scheme = verified_scheme()
    gemini = FakeGeminiService(reply=None)
    use_test_service(monkeypatch, [scheme], gemini)

    response = client.post(
        "/api/chat",
        json={"message": "What benefits does Test Student Scholarship provide?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "Synthetic tuition support." in payload["reply"]
    assert payload["schemes"][0]["benefits"] == ["Synthetic tuition support."]
    assert payload["schemes"][0]["source_url"] == str(scheme.source_url)


def test_eligibility_status_is_determined_only_by_python(monkeypatch):
    scheme = verified_scheme(
        eligibility_rules=[EligibilityRule(type="state", values=["Karnataka"])]
    )
    gemini = FakeGeminiService("You are eligible.")
    use_test_service(monkeypatch, [scheme], gemini)

    response = client.post(
        "/api/chat",
        json={
            "message": "Am I eligible for Test Student Scholarship?",
            "language": "en",
            "profile": {"state": "Telangana"},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["schemes"][0]["eligibility"]["status"] == "not_eligible"
    assert payload["schemes"][0]["eligibility"]["failed_conditions"]
    assert "not met" in payload["reply"]
    assert "You are eligible." not in payload["reply"]
    assert gemini.calls == []


def test_mock_records_are_not_returned_as_scheme_guidance(monkeypatch):
    mock_scheme = verified_scheme(
        verification_status="mock",
        source_url=None,
        last_verified=None,
    )
    gemini = FakeGeminiService("Should not be called.")
    use_test_service(monkeypatch, [mock_scheme], gemini)

    response = client.post(
        "/api/chat",
        json={"message": "Find schemes for students"},
    )

    assert response.status_code == 200
    assert response.json()["schemes"] == []
    assert "No verified scheme records" in response.json()["missing_information"][0]
    assert gemini.calls == []
