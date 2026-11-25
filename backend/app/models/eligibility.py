from typing import Literal

from pydantic import BaseModel

from app.models.scheme import Scheme


class EligibilityReason(BaseModel):
    code: str
    label: str
    detail: str
    status: Literal["satisfied", "not_satisfied", "needs_verification"]


class MatchResult(BaseModel):
    scheme: Scheme
    status: Literal["potentially_eligible", "not_eligible", "needs_verification"]
    reasons: list[EligibilityReason]
