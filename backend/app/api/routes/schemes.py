from fastapi import APIRouter, HTTPException, Query

from app.models.scheme import Scheme
from app.services.scheme_service import load_schemes

router = APIRouter(prefix="/schemes", tags=["schemes"])


@router.get("", response_model=list[Scheme])
def list_schemes(
    state: str | None = Query(default=None, min_length=1, max_length=100),
    category: str | None = Query(default=None, min_length=1, max_length=100),
) -> list[Scheme]:
    schemes = load_schemes()
    if state:
        requested_state = state.strip().casefold()
        schemes = [
            scheme
            for scheme in schemes
            if (
                scheme.state.casefold() == requested_state
                or (
                    scheme.state.casefold() == "all india"
                    and requested_state
                    not in {excluded.casefold() for excluded in scheme.state_exclusions}
                )
            )
        ]
    if category:
        requested_category = category.strip().casefold()
        schemes = [
            scheme
            for scheme in schemes
            if scheme.category.casefold() == requested_category
        ]
    return schemes


@router.get("/{scheme_id}", response_model=Scheme)
def get_scheme(scheme_id: str) -> Scheme:
    scheme = next((item for item in load_schemes() if item.id == scheme_id), None)
    if scheme is None:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme
