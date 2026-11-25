from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr

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
