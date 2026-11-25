from fastapi import APIRouter
from pydantic import BaseModel

from app.models.eligibility import EligibilityResult
from app.models.profile import UserProfile
from app.models.scheme import Scheme
from app.services.eligibility_engine import evaluate_all
from app.services.scheme_service import load_schemes

router = APIRouter(prefix="/eligibility", tags=["eligibility"])


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
