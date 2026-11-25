from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.eligibility import EligibilityResult
from app.models.profile import UserProfile

ChatIntent = Literal[
    "finding_schemes",
    "eligibility",
    "benefits",
    "required_documents",
    "application_process",
    "general_government_schemes",
]


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=1000)
    language: Literal["en", "te"] = "en"
    profile: UserProfile | None = None


class ChatSchemeResult(BaseModel):
    scheme_id: str
    scheme_name: str
    state: str
    state_exclusions: list[str] = Field(default_factory=list)
    government_level: Literal["central", "state"] | None = None
    category: str
    description: str
    eligibility_summary: str | None = None
    benefits: list[str]
    required_documents: list[str]
    application_process: list[str] = Field(default_factory=list)
    unavailable_fields: list[str] = Field(default_factory=list)
    application_url: HttpUrl | None
    source_url: HttpUrl
    last_verified: date
    eligibility: EligibilityResult | None = None


class ChatResponse(BaseModel):
    intent: ChatIntent
    language: Literal["en", "te"]
    reply: str
    schemes: list[ChatSchemeResult]
    missing_information: list[str]
    disclaimer: str
