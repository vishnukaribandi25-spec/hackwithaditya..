from datetime import date
from types import SimpleNamespace

import httpx
import pytest
from google.genai import errors

from app.models.eligibility import EligibilityResult
from app.models.scheme import Scheme
from app.services.gemini_service import GeminiService


def verified_scheme() -> Scheme:
    return Scheme(
        id="verified-demo",
        name="Synthetic test scheme",
        state="Telangana",
        department="Test department",
        category="education",
        description="A synthetic fixture for service tests.",
        benefits=["Synthetic test benefit."],
        eligibility_rules=[],
        required_documents=["Synthetic test document."],
        application_url=None,
        source_url="https://example.gov.in/scheme",
        last_verified=date(2026, 1, 15),
        verification_status="verified",
        supported_languages=["en", "te"],
    )


def eligibility_result(
    scheme_id: str = "verified-demo",
    status: str = "potentially_eligible",
) -> EligibilityResult:
    return EligibilityResult(
        scheme_id=scheme_id,
        status=status,
        matched_conditions=["State matches an allowed value."],
        failed_conditions=[],
        missing_information=[],
        explanation_reasons=["State matches an allowed value."],
    )


class FakeModels:
    def __init__(self, response=None, error: Exception | None = None):
        self.response = response
        self.error = error
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.response


class FakeClient:
    def __init__(self, models: FakeModels):
        self.models = models


@pytest.mark.parametrize(
    ("language", "text"),
    [
        ("en", "This is an informational explanation."),
        ("te", "ఇది సమాచార వివరణ మాత్రమే."),
    ],
)
def test_explains_verified_result_in_requested_language(language, text):
    models = FakeModels(response=SimpleNamespace(text=text))
    service = GeminiService(client=FakeClient(models))

    explanation = service.explain_eligibility(
        verified_scheme(),
        eligibility_result(),
        language,
    )

    assert explanation == text
    assert len(models.calls) == 1
    call = models.calls[0]
    assert f"in {'English' if language == 'en' else 'Telugu'}" in call["contents"]
    assert call["config"].system_instruction
    assert "untrusted data" in call["config"].system_instruction.lower()


@pytest.mark.parametrize(
    "updates",
    [
        {
            "verification_status": "mock",
            "source_url": None,
            "last_verified": None,
        },
        {
            "verification_status": "verified",
            "source_url": None,
            "last_verified": None,
        },
    ],
)
def test_does_not_send_unverified_or_unsourced_scheme_to_gemini(updates):
    models = FakeModels(response=SimpleNamespace(text="Should not be returned"))
    service = GeminiService(client=FakeClient(models))
    scheme = verified_scheme().model_copy(update=updates)

    assert service.explain_eligibility(scheme, eligibility_result(), "en") is None
    assert models.calls == []


def test_missing_api_key_returns_no_explanation(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    service = GeminiService()

    assert service.explain_eligibility(
        verified_scheme(),
        eligibility_result(),
        "en",
    ) is None


@pytest.mark.parametrize(
    "error",
    [
        errors.APIError(429, {"error": "rate limited"}),
        httpx.ReadTimeout("synthetic timeout"),
        httpx.ConnectError("synthetic transport error"),
    ],
)
def test_api_rate_limit_timeout_and_transport_errors_return_no_explanation(error):
    service = GeminiService(
        client=FakeClient(FakeModels(error=error)),
    )

    assert service.explain_eligibility(
        verified_scheme(),
        eligibility_result(status="not_eligible"),
        "en",
    ) is None


def test_empty_provider_response_returns_no_explanation():
    service = GeminiService(
        client=FakeClient(FakeModels(response=SimpleNamespace(text=None))),
    )

    assert service.explain_eligibility(
        verified_scheme(),
        eligibility_result(),
        "en",
    ) is None
