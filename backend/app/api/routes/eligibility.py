from fastapi import APIRouter

from app.models.profile import UserProfile
from app.models.eligibility import MatchResult
from app.services.eligibility_engine import evaluate
from app.services.gemini_service import GeminiService
from app.services.scheme_service import load_schemes

router = APIRouter(prefix="/eligibility", tags=["eligibility"])


@router.post("/match")
def match(profile: UserProfile, language: str = "en") -> dict:
    gemini = GeminiService()
    matches: list[MatchResult] = []
    for scheme in load_schemes():
        match = evaluate(profile, scheme)
        matches.append(match)

    priority = {"potentially_eligible": 0, "needs_verification": 1, "not_eligible": 2}
    return {
        "matches": [
            {
                **match.model_dump(mode="json"),
                "explanation": gemini.explain_match(match, language),
            }
            for match in sorted(matches, key=lambda item: priority[item.status])
        ],
        "disclaimer": (
            "ఇది అధికారిక నిర్ణయం కాదు. దరఖాస్తుకు ముందు అధికారిక పథక నిబంధనలు ధృవీకరించండి."
            if language == "te"
            else "This is informational guidance, not an official eligibility or approval decision."
        ),
    }
