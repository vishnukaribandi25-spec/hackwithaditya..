import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ProfileAttributeValue = str | int | float | bool | None
STATE_NAMES = {
    "andhra pradesh": "Andhra Pradesh",
    "telangana": "Telangana",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "karnataka": "Karnataka",
    "all india": "All India",
}
SOCIAL_CATEGORIES = {
    "general": "General",
    "sc": "SC",
    "st": "ST",
    "obc": "OBC",
    "other": "Other",
    "prefer not to say": "Prefer not to say",
}
EDUCATION_ALIASES = {
    "highschool": "secondary",
    "high school": "secondary",
    "high_school": "secondary",
    "secondary": "secondary",
}
ATTRIBUTE_ALIASES = {
    "owns_pucca_house": "household_owns_pucca_house",
    "landholding_farmer_family": "pm_kisan_landholding_farmer_family",
}
BOOLEAN_ATTRIBUTE_KEYS = {
    "resides_in_rural_area",
    "household_owns_pucca_house",
    "pm_kisan_landholding_farmer_family",
}
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
    social_category: Literal[
        "General",
        "SC",
        "ST",
        "OBC",
        "Other",
        "Prefer not to say",
    ] | None = Field(
        default=None,
        description=(
            "Optional self-reported category. Used only when a verified scheme rule "
            "requires it; 'Prefer not to say' remains unknown for matching."
        ),
    )
    gender: Literal["male", "female", "other", "prefer_not_to_say"] | None = Field(
        default=None,
        description="Provide only when a verified scheme rule requires it.",
    )
    additional_attributes: dict[str, ProfileAttributeValue] = Field(
        default_factory=dict,
        max_length=20,
        description="Non-sensitive, scheme-specific attributes only.",
    )

    @field_validator("state", mode="before")
    @classmethod
    def _normalize_state(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        normalized = " ".join(value.split())
        return STATE_NAMES.get(normalized.casefold(), normalized)

    @field_validator("occupation", mode="before")
    @classmethod
    def _normalize_occupation(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        normalized = " ".join(value.split())
        known_values = {"farmer": "Farmer", "student": "Student"}
        return known_values.get(normalized.casefold(), normalized)

    @field_validator("education_level", mode="before")
    @classmethod
    def _normalize_education_level(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        normalized = " ".join(value.split())
        return EDUCATION_ALIASES.get(normalized.casefold(), normalized)

    @field_validator("social_category", mode="before")
    @classmethod
    def _normalize_social_category(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        normalized = " ".join(value.split())
        return SOCIAL_CATEGORIES.get(normalized.casefold(), normalized)

    @field_validator("gender", mode="before")
    @classmethod
    def _normalize_gender(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        normalized = " ".join(value.casefold().replace("_", " ").split())
        known_values = {
            "male": "male",
            "female": "female",
            "other": "other",
            "prefer not to say": "prefer_not_to_say",
        }
        return known_values.get(normalized, value)

    @field_validator("additional_attributes", mode="before")
    @classmethod
    def _normalize_additional_attributes(cls, value: object) -> object:
        if not isinstance(value, dict):
            return value

        attributes = dict(value)
        if "residence_type" in attributes:
            residence = attributes.pop("residence_type")
            if residence is None:
                normalized_residence = None
            elif isinstance(residence, str):
                normalized_residence = {
                    "rural": True,
                    "urban": False,
                }.get(" ".join(residence.split()).casefold())
                if normalized_residence is None:
                    raise ValueError(
                        "additional_attributes.residence_type must be 'rural' or 'urban'."
                    )
            else:
                raise ValueError(
                    "additional_attributes.residence_type must be 'rural' or 'urban'."
                )
            if (
                "resides_in_rural_area" in attributes
                and attributes["resides_in_rural_area"] != normalized_residence
            ):
                raise ValueError(
                    "additional_attributes.residence_type conflicts with "
                    "resides_in_rural_area."
                )
            attributes["resides_in_rural_area"] = normalized_residence

        for alias, canonical in ATTRIBUTE_ALIASES.items():
            if alias not in attributes:
                continue
            alias_value = attributes.pop(alias)
            if canonical in attributes and attributes[canonical] != alias_value:
                raise ValueError(
                    f"additional_attributes.{alias} conflicts with {canonical}."
                )
            attributes[canonical] = alias_value

        for key in BOOLEAN_ATTRIBUTE_KEYS:
            if key in attributes and attributes[key] is not None and type(attributes[key]) is not bool:
                raise ValueError(f"additional_attributes.{key} must be a JSON boolean.")
        return attributes

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
