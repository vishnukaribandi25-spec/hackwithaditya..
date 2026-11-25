from datetime import date
from typing import Literal

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, HttpUrl

from app.models.eligibility import (
    EligibilityCheckResponse,
    EligibilityCheckResult,
    EligibilityResult,
    SchemeSourceMetadata,
)
from app.models.profile import UserProfile
from app.models.scheme import Scheme
from app.services.eligibility_engine import evaluate_all, evaluate_eligibility
from app.services.gemini_service import GeminiService
from app.services.scheme_service import load_schemes

router = APIRouter(prefix="/eligibility", tags=["eligibility"])
gemini_service = GeminiService()


class SchemeMatch(EligibilityResult):
    scheme_name: str
    scheme: Scheme
    explanation: str
    match_group: Literal["recommendation", "not_applicable"]
    verification_required: bool
    verification_status: Literal["verified", "unverified", "mock"]
    source_url: HttpUrl | None
    last_verified_date: date | None
    is_mock: bool
    verification_steps: list[str]


class SchemeMatchResponse(BaseModel):
    matches: list[SchemeMatch]
    not_applicable: list[SchemeMatch] = Field(default_factory=list)
    disclaimer: str


def _has_profile_relevant_match(profile: UserProfile, scheme: Scheme) -> bool:
    for rule in scheme.eligibility_rules:
        if rule.type.strip().casefold() == "state":
            continue
        result = evaluate_eligibility(profile, scheme.id, [rule])
        if result.status == "potentially_eligible":
            return True
    return False


def _build_scheme_match(
    scheme: Scheme,
    result: EligibilityResult,
    match_group: Literal["recommendation", "not_applicable"],
) -> SchemeMatch:
    explanation = " ".join(result.explanation_reasons)
    if match_group == "not_applicable":
        if result.failed_conditions:
            explanation = (
                "Known profile condition(s) did not match: "
                + " ".join(result.failed_conditions)
            )
        else:
            explanation = (
                "No supported eligibility condition matched the supplied profile. "
                "This record is not recommended for this profile; this is not an "
                "official finding of ineligibility."
            )

    return SchemeMatch(
        **result.model_dump(),
        scheme_name=scheme.name,
        scheme=scheme,
        explanation=explanation,
        match_group=match_group,
        verification_required=bool(result.missing_information),
        verification_status=scheme.verification_status,
        source_url=scheme.source_url,
        last_verified_date=scheme.last_verified,
        is_mock=scheme.verification_status == "mock",
        verification_steps=list(scheme.application_process),
    )


@router.post("/match", response_model=SchemeMatchResponse)
def match_schemes(profile: UserProfile) -> SchemeMatchResponse:
    schemes = load_schemes()
    results_by_id = {
        result.scheme_id: result
        for result in evaluate_all(profile, schemes)
    }
    matches: list[SchemeMatch] = []
    not_applicable: list[SchemeMatch] = []
    for scheme in schemes:
        if scheme.verification_status != "verified":
            continue

        result = results_by_id[scheme.id]
        relevant = _has_profile_relevant_match(profile, scheme)
        if result.status == "not_eligible" or not relevant:
            not_applicable.append(
                _build_scheme_match(scheme, result, "not_applicable")
            )
        else:
            matches.append(_build_scheme_match(scheme, result, "recommendation"))

    return SchemeMatchResponse(
        matches=matches,
        not_applicable=not_applicable,
        disclaimer=(
            "Eligibility results are informational, not official decisions. "
            "Recommendations include only verified records with a relevant profile "
            "match. Not-applicable entries are not eligibility determinations. "
            "Mock and unverified records are excluded."
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
    mock_records: list[EligibilityCheckResult] = []
    unverified_records: list[EligibilityCheckResult] = []

    for scheme in schemes:
        result = results_by_id[scheme.id]
        item = EligibilityCheckResult(
            **result.model_dump(),
            scheme_name=scheme.name,
            source_metadata=SchemeSourceMetadata(
                source_url=scheme.source_url,
                application_url=scheme.application_url,
                last_verified=scheme.last_verified,
                verification_status=scheme.verification_status,
            ),
            verification_required=bool(result.missing_information)
            or scheme.verification_status != "verified",
            verification_status=scheme.verification_status,
            source_url=scheme.source_url,
            last_verified_date=scheme.last_verified,
            is_mock=scheme.verification_status == "mock",
            verification_steps=list(scheme.application_process),
            ai_explanation=(
                gemini_service.explain_eligibility(scheme, result, language)
                if scheme.verification_status == "verified"
                else None
            ),
        )
        if scheme.verification_status == "mock":
            mock_records.append(item)
        elif scheme.verification_status != "verified":
            unverified_records.append(item)
        else:
            grouped_results[result.status].append(item)

    return EligibilityCheckResponse(
        **grouped_results,
        mock_records=mock_records,
        unverified_records=unverified_records,
        disclaimer=(
            "Eligibility results are informational, not official decisions or approval. "
            "Mock development records are not government schemes."
        ),
    )
