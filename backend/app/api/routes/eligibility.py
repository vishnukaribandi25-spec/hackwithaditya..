from typing import Literal

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.models.eligibility import (
    EligibilityCheckResponse,
    EligibilityCheckResult,
    EligibilityResult,
    SchemeSourceMetadata,
)
from app.models.profile import UserProfile
from app.models.scheme import Scheme
from app.services.eligibility_engine import evaluate_all
from app.services.gemini_service import GeminiService
from app.services.scheme_service import load_schemes

router = APIRouter(prefix="/eligibility", tags=["eligibility"])
gemini_service = GeminiService()


class SchemeMatch(EligibilityResult):
    scheme: Scheme
    explanation: str


class SchemeMatchResponse(BaseModel):
    matches: list[SchemeMatch]
    disclaimer: str


@router.post("/match", response_model=SchemeMatchResponse)
def match_schemes(profile: UserProfile) -> SchemeMatchResponse:
    schemes = load_schemes()
    results_by_id = {
        result.scheme_id: result
        for result in evaluate_all(profile, schemes)
    }
    matches = [
        SchemeMatch(
            **results_by_id[scheme.id].model_dump(),
            scheme=scheme,
            explanation=" ".join(results_by_id[scheme.id].explanation_reasons),
        )
        for scheme in schemes
    ]
    return SchemeMatchResponse(
        matches=matches,
        disclaimer=(
            "Eligibility results are informational, not official decisions. "
            "Mock development records are not government schemes."
        ),
    )


@router.post("/check", response_model=EligibilityCheckResponse)
def check_eligibility(
    profile: UserProfile,
    language: Literal["en", "te"] = Query(default="en"),
) -> EligibilityCheckResponse:
    schemes = load_schemes()
    results_by_id = {
        result.scheme_id: result
        for result in evaluate_all(profile, schemes)
    }
    grouped_results: dict[str, list[EligibilityCheckResult]] = {
        "potentially_eligible": [],
        "not_eligible": [],
        "needs_verification": [],
    }

    for scheme in schemes:
        result = results_by_id[scheme.id]
        grouped_results[result.status].append(
            EligibilityCheckResult(
                **result.model_dump(),
                scheme_name=scheme.name,
                source_metadata=SchemeSourceMetadata(
                    source_url=scheme.source_url,
                    application_url=scheme.application_url,
                    last_verified=scheme.last_verified,
                    verification_status=scheme.verification_status,
                ),
                ai_explanation=(
                    gemini_service.explain_eligibility(scheme, result, language)
                    if scheme.verification_status == "verified"
                    else None
                ),
            )
        )

    return EligibilityCheckResponse(
        **grouped_results,
        disclaimer=(
            "Eligibility results are informational, not official decisions or approval. "
            "Mock development records are not government schemes."
        ),
    )
