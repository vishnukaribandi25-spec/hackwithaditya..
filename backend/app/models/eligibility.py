from datetime import date
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
)

RuleNumber = StrictInt | StrictFloat
RuleValue = StrictStr | StrictInt | StrictFloat | StrictBool


class EligibilityRule(BaseModel):
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    type: str = Field(min_length=1)
    label: str | None = None
    min: RuleNumber | None = None
    max: RuleNumber | None = None
    values: list[RuleValue] | None = None
    attribute: str | None = None
    operator: str | None = None
    value: RuleValue | None = None


class EligibilityResult(BaseModel):
    scheme_id: str
    status: Literal[
        "potentially_eligible",
        "not_eligible",
        "needs_verification",
    ]
    matched_conditions: list[str]
    failed_conditions: list[str]
    missing_information: list[str]
    explanation_reasons: list[str]


class SchemeSourceMetadata(BaseModel):
    source_url: HttpUrl | None
    application_url: HttpUrl | None
    last_verified: date | None
    verification_status: Literal["verified", "unverified", "mock"]


class EligibilityCheckResult(EligibilityResult):
    scheme_name: str
    source_metadata: SchemeSourceMetadata
    ai_explanation: str | None = None


class EligibilityCheckResponse(BaseModel):
    potentially_eligible: list[EligibilityCheckResult]
    not_eligible: list[EligibilityCheckResult]
    needs_verification: list[EligibilityCheckResult]
    disclaimer: str
