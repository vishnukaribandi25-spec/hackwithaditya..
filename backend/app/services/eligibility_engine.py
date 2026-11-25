from app.models.profile import UserProfile
from app.models.scheme import Scheme
from app.models.eligibility import EligibilityReason, MatchResult


def _profile_value(profile: UserProfile, key: str):
    return getattr(profile, key, None)


def _reason(code: str, label: str, detail: str, status: str) -> EligibilityReason:
    return EligibilityReason(code=code, label=label, detail=detail, status=status)


def evaluate(profile: UserProfile, scheme: Scheme) -> MatchResult:
    conditions = scheme.conditions
    reasons: list[EligibilityReason] = []

    state = conditions.get("states")
    if state:
        if profile.state.lower() in [item.lower() for item in state]:
            reasons.append(_reason("state", "Residence", f"Your state matches the scheme requirement.", "satisfied"))
        elif "all" in [item.lower() for item in state]:
            reasons.append(_reason("state", "Residence", "The scheme is available across India.", "satisfied"))
        else:
            reasons.append(_reason("state", "Residence", f"The scheme is not listed for {profile.state}.", "not_satisfied"))

    age = conditions.get("age")
    if age:
        minimum = age.get("min")
        maximum = age.get("max")
        if profile.age is None:
            reasons.append(_reason("age", "Age", "Your age is needed to verify this condition.", "needs_verification"))
        elif (minimum is None or profile.age >= minimum) and (maximum is None or profile.age <= maximum):
            reasons.append(_reason("age", "Age", f"Age {profile.age} is within the stated range.", "satisfied"))
        else:
            reasons.append(_reason("age", "Age", f"Age {profile.age} is outside the stated range.", "not_satisfied"))

    income = conditions.get("annual_family_income_max")
    if income is not None:
        if profile.annual_family_income is None:
            reasons.append(_reason("income", "Annual family income", "Income is needed to verify this condition.", "needs_verification"))
        elif profile.annual_family_income <= income:
            reasons.append(_reason("income", "Annual family income", "Income is within the stated limit.", "satisfied"))
        else:
            reasons.append(_reason("income", "Annual family income", "Income is above the stated limit.", "not_satisfied"))

    occupation = conditions.get("occupations")
    if occupation:
        if not profile.occupation:
            reasons.append(_reason("occupation", "Occupation", "Your occupation is needed to verify this condition.", "needs_verification"))
        elif profile.occupation.lower() in [item.lower() for item in occupation]:
            reasons.append(_reason("occupation", "Occupation", "Your occupation matches the scheme.", "satisfied"))
        else:
            reasons.append(_reason("occupation", "Occupation", "Your occupation does not match the listed criteria.", "not_satisfied"))

    gender = conditions.get("genders")
    if gender:
        if not profile.gender:
            reasons.append(_reason("gender", "Gender", "Gender is needed to verify this condition.", "needs_verification"))
        elif profile.gender.lower() in [item.lower() for item in gender]:
            reasons.append(_reason("gender", "Gender", "Gender condition is satisfied.", "satisfied"))
        else:
            reasons.append(_reason("gender", "Gender", "Gender condition is not satisfied.", "not_satisfied"))

    education = conditions.get("education")
    if education:
        if not profile.education:
            reasons.append(_reason("education", "Education", "Education information is needed.", "needs_verification"))
        elif any(value.lower() in profile.education.lower() for value in education):
            reasons.append(_reason("education", "Education", "Education level appears to match.", "satisfied"))
        else:
            reasons.append(_reason("education", "Education", "Education level does not match.", "not_satisfied"))

    for key, label in (
        ("is_farmer", "Farmer status"),
        ("is_student", "Student status"),
        ("is_unemployed", "Employment status"),
    ):
        if key in conditions:
            required = bool(conditions[key])
            actual = _profile_value(profile, key)
            if actual is None:
                reasons.append(_reason(key, label, f"{label} is needed to verify this condition.", "needs_verification"))
            elif actual == required:
                reasons.append(_reason(key, label, f"{label} matches.", "satisfied"))
            else:
                reasons.append(_reason(key, label, f"{label} does not match.", "not_satisfied"))

    category = conditions.get("categories")
    if category:
        if not profile.category:
            reasons.append(_reason("category", "Category", "Category is needed to verify this condition.", "needs_verification"))
        elif profile.category.lower() in [item.lower() for item in category]:
            reasons.append(_reason("category", "Category", "Category matches.", "satisfied"))
        else:
            reasons.append(_reason("category", "Category", "Category does not match.", "not_satisfied"))

    if any(reason.status == "not_satisfied" for reason in reasons):
        status = "not_eligible"
    elif any(reason.status == "needs_verification" for reason in reasons):
        status = "needs_verification"
    else:
        status = "potentially_eligible"

    return MatchResult(scheme=scheme, status=status, reasons=reasons)
