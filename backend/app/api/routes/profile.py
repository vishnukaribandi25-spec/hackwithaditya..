from fastapi import APIRouter

from app.models.profile import ProfileValidationResponse, UserProfile

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/validate", response_model=ProfileValidationResponse)
def validate_profile(profile: UserProfile) -> ProfileValidationResponse:
    return ProfileValidationResponse(valid=True, profile=profile)
