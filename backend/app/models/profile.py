import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ProfileAttributeValue = str | int | float | bool | None
SENSITIVE_ATTRIBUTE_TOKENS = {
    "aadhaar",
    "account",
    "bank",
    "ifsc",
    "mobile",
    "otp",
    "password",
    "phone",
    "pan",
}


class UserProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    age: Annotated[int, Field(strict=True, ge=0, le=120)] | None = None
    state: str | None = Field(default=None, min_length=2, max_length=100)
    occupation: str | None = Field(default=None, min_length=1, max_length=100)
    education_level: str | None = Field(default=None, min_length=1, max_length=100)
    annual_family_income: Annotated[int, Field(strict=True, ge=0)] | None = None
    gender: Literal["male", "female", "other", "prefer_not_to_say"] | None = Field(
        default=None,
        description="Provide only when a verified scheme rule requires it.",
    )
    additional_attributes: dict[str, ProfileAttributeValue] = Field(
        default_factory=dict,
        max_length=20,
        description="Non-sensitive, scheme-specific attributes only.",
    )

    @field_validator("additional_attributes")
    @classmethod
    def _validate_attribute_names(cls, attributes: dict[str, ProfileAttributeValue]):
        for key in attributes:
            tokens = set(re.findall(r"[a-z0-9]+", key.casefold()))
            if not tokens:
                raise ValueError("Additional attribute names must contain letters or numbers.")
            if tokens & SENSITIVE_ATTRIBUTE_TOKENS:
                raise ValueError(
                    "Additional attributes must not contain Aadhaar, OTP, bank, account, "
                    "phone, mobile, PAN, or other sensitive information."
                )
        return attributes


class ProfileValidationResponse(BaseModel):
    valid: Literal[True] = True
    profile: UserProfile
