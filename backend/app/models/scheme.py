from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class Scheme(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    name: str = Field(min_length=1)
    state: str = Field(min_length=1)
    department: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    benefits: list[str] = Field(min_length=1)
    eligibility_rules: list[str] = Field(min_length=1)
    required_documents: list[str] = Field(min_length=1)
    application_url: HttpUrl | None
    source_url: HttpUrl | None
    last_verified: date | None
    verification_status: Literal["verified", "unverified", "mock"]
    supported_languages: list[str] = Field(min_length=1)
