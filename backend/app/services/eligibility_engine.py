from collections.abc import Iterable
from numbers import Real

from pydantic import ValidationError

from app.models.eligibility import EligibilityResult, EligibilityRule
from app.models.profile import UserProfile
from app.models.scheme import Scheme


def _label(rule: EligibilityRule) -> str:
    return rule.label or rule.type.replace("_", " ").strip().capitalize()


def _same_value(actual: object, expected: object) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(actual, Real) and isinstance(expected, Real):
        return actual == expected
    if isinstance(actual, str) and isinstance(expected, str):
        return actual.casefold() == expected.casefold()
    return type(actual) is type(expected) and actual == expected


def _evaluate_rule(
    profile: UserProfile,
    rule: EligibilityRule,
) -> tuple[str, str]:
    rule_type = rule.type.strip().casefold()
    label = _label(rule)
    allowed_fields = {
        "age": {"min", "max"},
        "annual_family_income": {"min", "max"},
        "income": {"min", "max"},
        "state": {"values"},
        "occupation": {"values"},
        "education_level": {"values"},
        "gender": {"values"},
        "attribute": {"attribute", "operator", "value", "values"},
    }
    if rule_type in allowed_fields:
        unsupported_fields = rule.model_fields_set - allowed_fields[rule_type] - {"type", "label"}
        if unsupported_fields:
            names = ", ".join(sorted(unsupported_fields))
            return "missing", f"{label} rule contains unsupported fields ({names}) and needs manual verification."

    if rule_type in {"age", "annual_family_income", "income"}:
        profile_key = "age" if rule_type == "age" else "annual_family_income"
        unit = "years" if rule_type == "age" else "annual family income"
        minimum, maximum = rule.min, rule.max
        if (
            (minimum is not None and (isinstance(minimum, bool) or not isinstance(minimum, Real)))
            or (maximum is not None and (isinstance(maximum, bool) or not isinstance(maximum, Real)))
            or (minimum is None and maximum is None)
            or (minimum is not None and maximum is not None and minimum > maximum)
            or (
                rule_type == "age"
                and (
                    (minimum is not None and minimum < 0)
                    or (maximum is not None and maximum > 120)
                )
            )
            or (
                rule_type != "age"
                and (
                    (minimum is not None and minimum < 0)
                    or (maximum is not None and maximum < 0)
                )
            )
        ):
            return "missing", f"{label} rule is incomplete or invalid; it needs manual verification."

        actual = getattr(profile, profile_key)
        if actual is None:
            return "missing", f"{label} is not provided, so this rule could not be checked."
        if minimum is not None and actual < minimum:
            return "failed", f"{label} is below the required minimum of {minimum} {unit}."
        if maximum is not None and actual > maximum:
            return "failed", f"{label} is above the allowed maximum of {maximum} {unit}."
        return "matched", f"{label} satisfies the stated {unit} range."

    profile_fields = {
        "state": "state",
        "occupation": "occupation",
        "education_level": "education_level",
        "gender": "gender",
    }
    if rule_type in profile_fields:
        if not rule.values or not all(
            isinstance(value, str) and value.strip() for value in rule.values
        ):
            return "missing", f"{label} rule has no valid allowed values; it needs manual verification."
        actual = getattr(profile, profile_fields[rule_type])
        allowed_values = [value.casefold() for value in rule.values]
        if rule_type == "state" and any(value in {"all", "all india"} for value in allowed_values):
            return "matched", f"{label} is allowed for all states."
        if actual is None:
            return "missing", f"{label} is not provided, so this rule could not be checked."
        if actual.casefold() in allowed_values:
            return "matched", f"{label} matches an allowed value."
        return "failed", f"{label} does not match any allowed value."

    if rule_type == "attribute":
        if not rule.attribute or not rule.operator:
            return "missing", f"{label} rule is missing its attribute or operator."
        if rule.operator not in {"equals", "not_equals", "in", "not_in"}:
            return "missing", f"{label} uses unsupported operator '{rule.operator}'."
        if (
            rule.attribute not in profile.additional_attributes
            or profile.additional_attributes[rule.attribute] is None
        ):
            return "missing", f"{label} attribute '{rule.attribute}' is not provided."

        actual = profile.additional_attributes[rule.attribute]
        if rule.operator in {"equals", "not_equals"}:
            if rule.value is None:
                return "missing", f"{label} rule is missing its comparison value."
            matched = _same_value(actual, rule.value)
            if rule.operator == "not_equals":
                matched = not matched
        else:
            if not rule.values:
                return "missing", f"{label} rule is missing its allowed values."
            matched = any(_same_value(actual, value) for value in rule.values)
            if rule.operator == "not_in":
                matched = not matched

        if matched:
            return "matched", f"{label} matches the stated scheme-specific condition."
        return "failed", f"{label} does not match the stated scheme-specific condition."

    return "missing", f"Rule type '{rule.type}' is unsupported and needs manual verification."


def evaluate_eligibility(
    profile: UserProfile,
    scheme_id: str,
    eligibility_rules: Iterable[EligibilityRule | dict[str, object]],
) -> EligibilityResult:
    rules = list(eligibility_rules)
    matched_conditions: list[str] = []
    failed_conditions: list[str] = []
    missing_information: list[str] = []
    explanation_reasons: list[str] = []

    if not rules:
        missing_information.append("No eligibility rules are available to assess this scheme.")

    for index, raw_rule in enumerate(rules, start=1):
        try:
            rule = (
                raw_rule
                if isinstance(raw_rule, EligibilityRule)
                else EligibilityRule.model_validate(raw_rule)
            )
        except ValidationError:
            detail = f"Eligibility rule {index} is malformed and needs manual verification."
            missing_information.append(detail)
            explanation_reasons.append(detail)
            continue

        outcome, detail = _evaluate_rule(profile, rule)
        explanation_reasons.append(detail)
        if outcome == "matched":
            matched_conditions.append(detail)
        elif outcome == "failed":
            failed_conditions.append(detail)
        else:
            missing_information.append(detail)

    if failed_conditions:
        status = "not_eligible"
    elif missing_information:
        status = "needs_verification"
    else:
        status = "potentially_eligible"

    return EligibilityResult(
        scheme_id=scheme_id,
        status=status,
        matched_conditions=matched_conditions,
        failed_conditions=failed_conditions,
        missing_information=missing_information,
        explanation_reasons=explanation_reasons,
    )


def evaluate(profile: UserProfile, scheme: Scheme) -> EligibilityResult:
    return evaluate_eligibility(profile, scheme.id, scheme.eligibility_rules)


def evaluate_all(
    profile: UserProfile,
    schemes: Iterable[Scheme],
) -> list[EligibilityResult]:
    return [evaluate(profile, scheme) for scheme in schemes]
