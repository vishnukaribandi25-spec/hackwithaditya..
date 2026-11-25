from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.eligibility import EligibilityRule


class Scheme(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    name: str = Field(min_length=1)
    state: str = Field(min_length=1)
    state_exclusions: list[str] = Field(default_factory=list)
    government_level: Literal["central", "state"] | None = None
    department: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    benefits: list[str]
    eligibility_summary: str | None = None
    eligibility_rules: list[EligibilityRule]
    required_documents: list[str]
    application_process: list[str] = Field(default_factory=list)
    unavailable_fields: list[str] = Field(default_factory=list)
    application_url: HttpUrl | None
    source_url: HttpUrl | None
    last_verified: date | None
    verification_status: Literal["verified", "unverified", "mock"]
    supported_languages: list[str] = Field(min_length=1)
