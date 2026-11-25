import re
import unicodedata

from app.models.chat import ChatIntent, ChatRequest, ChatResponse, ChatSchemeResult
from app.models.eligibility import EligibilityResult
from app.models.profile import UserProfile
from app.models.scheme import Scheme
from app.services.eligibility_engine import evaluate_all
from app.services.gemini_service import GeminiService
from app.services.scheme_service import load_schemes

_ELIGIBILITY_TERMS = (
    "eligible",
    "eligibility",
    "qualify",
    "qualifies",
    "do i qualify",
    "can i get",
    "అర్హత",
    "అర్హుడ",
    "అర్హురా",
)
_DOCUMENT_TERMS = (
    "document",
    "documents",
    "paperwork",
    "what papers",
    "పత్రాలు",
    "డాక్యుమెంట్",
    "సర్టిఫికెట్",
)
_BENEFIT_TERMS = (
    "benefit",
    "benefits",
    "amount",
    "how much",
    "what do i get",
    "ప్రయోజన",
    "లాభ",
    "ఎంత",
)
_APPLICATION_TERMS = (
    "apply",
    "application",
    "application process",
    "how to apply",
    "దరఖాస్తు",
    "అప్లై",
)
_FIND_TERMS = (
    "find",
    "search",
    "show me",
    "list",
    "available schemes",
    "what schemes",
    "schemes for",
    "find schemes",
    "పథకాలు",
    "పథకాల",
    "పథకాలను",
)
_GENERAL_DEFINITION_TERMS = (
    "what is a government scheme",
    "what is government scheme",
    "ప్రభుత్వ పథకం అంటే ఏమిటి",
)


def classify_intent(message: str) -> ChatIntent:
    normalized = unicodedata.normalize("NFKC", message).casefold()
    if any(term in normalized for term in _ELIGIBILITY_TERMS):
        return "eligibility"
    if any(term in normalized for term in _DOCUMENT_TERMS):
        return "required_documents"
    if any(term in normalized for term in _BENEFIT_TERMS):
        return "benefits"
    if any(term in normalized for term in _APPLICATION_TERMS):
        return "application_process"
    if any(term in normalized for term in _FIND_TERMS):
        return "finding_schemes"
    if any(term in normalized for term in _GENERAL_DEFINITION_TERMS):
        return "general_government_schemes"
    return "general_government_schemes"


def _normalized_text(value: str) -> str:
    return re.sub(
        r"[^\w\s-]",
        " ",
        unicodedata.normalize("NFKC", value).casefold(),
    ).strip()


def _nonempty_items(items: list[str]) -> list[str]:
    return [item.strip() for item in items if item.strip()]


def _mentioned_schemes(message: str, schemes: list[Scheme]) -> list[Scheme]:
    normalized_message = _normalized_text(message)
    return [
        scheme
        for scheme in schemes
        if any(
            candidate and candidate in normalized_message
            for candidate in (
                _normalized_text(scheme.name),
                _normalized_text(scheme.id),
                _normalized_text(scheme.id.replace("-", " ")),
            )
        )
    ]


def _verified_schemes(schemes: list[Scheme]) -> list[Scheme]:
    return [
        scheme
        for scheme in schemes
        if scheme.verification_status == "verified"
        and scheme.source_url is not None
        and scheme.last_verified is not None
    ]


def _scheme_facts(scheme: Scheme) -> dict[str, object]:
    facts = scheme.model_dump(
        mode="json",
        include={
            "id",
            "name",
            "state",
            "state_exclusions",
            "government_level",
            "department",
            "category",
            "description",
            "eligibility_summary",
            "benefits",
            "eligibility_rules",
            "required_documents",
            "application_process",
            "unavailable_fields",
            "application_url",
            "source_url",
            "last_verified",
            "verification_status",
        },
    )
    facts["benefits"] = _nonempty_items(scheme.benefits)
    facts["required_documents"] = _nonempty_items(scheme.required_documents)
    return facts


def _missing_notice(language: str) -> str:
    if language == "te":
        return "గమనిక: ధృవీకరించిన రికార్డుల్లో కొన్ని అడిగిన వివరాలు అందుబాటులో లేవు."
    return "Note: Some requested details are not available in the verified records."


def _localized_status(status: str, language: str, scheme_name: str) -> str:
    if language == "te":
        labels = {
            "potentially_eligible": (
                f"మీరు అందించిన వివరాల ప్రకారం, {scheme_name} పథకానికి "
                "మీరు సంభావ్యంగా అర్హులు కావచ్చు."
            ),
            "not_eligible": (
                f"తెలిసిన వివరాల ప్రకారం, {scheme_name} పథకంలోని కనీసం ఒక "
                "నిబంధన సరిపోలలేదు."
            ),
            "needs_verification": (
                f"{scheme_name} పథకానికి అర్హతను నిర్ధారించడానికి మరిన్ని "
                "వివరాలు అవసరం."
            ),
        }
    else:
        labels = {
            "potentially_eligible": (
                f"Based on the details provided, you may potentially qualify "
                f"for {scheme_name}."
            ),
            "not_eligible": (
                f"Based on known information, at least one stated condition "
                f"for {scheme_name} was not met."
            ),
            "needs_verification": (
                f"More information is needed to assess potential eligibility "
                f"for {scheme_name}."
            ),
        }
    return labels[status]


def _fallback_reply(
    intent: ChatIntent,
    language: str,
    schemes: list[ChatSchemeResult],
    missing_information: list[str],
) -> str:
    if not schemes:
        if missing_information and not any(
            item.startswith("No verified scheme records")
            for item in missing_information
        ):
            if language == "te":
                return (
                    "మీరు పేర్కొన్న పథకాన్ని ధృవీకరించిన రికార్డుల్లో కనుగొనలేకపోయాను. "
                    "దయచేసి పథకం పేరును తనిఖీ చేయండి లేదా ధృవీకరించిన పథకాలను చూపమని అడగండి."
                )
            return (
                "I couldn't find that scheme in the verified records. Check the scheme "
                "name or ask me to list verified schemes."
            )
        if language == "te":
            return (
                "ఈ ప్రశ్నకు సమాధానం ఇవ్వడానికి ప్రస్తుతం ధృవీకరించిన పథక "
                "వివరాలు అందుబాటులో లేవు."
            )
        return "I don't have verified scheme information to answer this yet."

    if intent == "eligibility":
        parts: list[str] = []
        for scheme in schemes:
            result = scheme.eligibility
            if result is None:
                continue
            text = _localized_status(result.status, language, scheme.scheme_name)
            if result.failed_conditions:
                if language == "te":
                    text += " తెలిసిన నిబంధనల్లో కనీసం ఒకటి సరిపోలలేదు."
                else:
                    text += " Failed conditions: " + " ".join(result.failed_conditions)
            if result.missing_information:
                if language == "te":
                    text += " మరింత సమాచారం ధృవీకరించాలి."
                else:
                    text += " Information still to verify: " + " ".join(
                        result.missing_information
                    )
            parts.append(text)
        if language == "te":
            return " ".join(parts) + " ఇది సమాచార మార్గదర్శకం మాత్రమే; అధికారిక నిర్ణయం కాదు."
        return " ".join(parts) + " This is informational guidance, not an official decision."

    if intent == "finding_schemes":
        names = "; ".join(scheme.scheme_name for scheme in schemes)
        if language == "te":
            return f"ధృవీకరించిన పథకాల జాబితా: {names}."
        return f"Verified schemes in the available records: {names}."

    if intent == "benefits":
        facts = []
        for scheme in schemes:
            benefits = _nonempty_items(scheme.benefits)
            if benefits:
                facts.append(f"{scheme.scheme_name}: {'; '.join(benefits)}")
        if not facts:
            return (
                "ధృవీకరించిన ప్రయోజన వివరాలు అందుబాటులో లేవు."
                if language == "te"
                else "No verified benefit details are available."
            )
        if language == "te":
            return "ధృవీకరించిన ప్రయోజనాలు: " + " ".join(facts)
        return "Verified benefits: " + " ".join(facts)

    if intent == "required_documents":
        facts = []
        for scheme in schemes:
            documents = _nonempty_items(scheme.required_documents)
            if documents:
                facts.append(f"{scheme.scheme_name}: {'; '.join(documents)}")
        if not facts:
            return (
                "ధృవీకరించిన అవసరమైన పత్రాల వివరాలు అందుబాటులో లేవు."
                if language == "te"
                else "No verified required-document details are available."
            )
        if language == "te":
            return "ధృవీకరించిన అవసరమైన పత్రాలు: " + " ".join(facts)
        return "Verified required documents: " + " ".join(facts)

    if intent == "application_process":
        parts = []
        for scheme in schemes:
            if scheme.application_process:
                parts.append(
                    f"{scheme.scheme_name}: {'; '.join(scheme.application_process)}"
                )
            elif language == "te":
                parts.append(
                    f"{scheme.scheme_name}: ధృవీకరించిన దరఖాస్తు సూచనలు అందుబాటులో లేవు."
                )
            else:
                parts.append(
                    f"{scheme.scheme_name}: verified application steps are unavailable."
                )
            if scheme.application_url:
                parts.append(f"Official information/application portal: {scheme.application_url}")
            elif language == "te":
                parts.append(
                    f"{scheme.scheme_name}: ధృవీకరించిన దరఖాస్తు లింక్ అందుబాటులో లేదు."
                )
            else:
                parts.append(
                    f"{scheme.scheme_name}: no verified application link is available."
                )
        if language == "te":
            return "అధికారిక రికార్డులోని దరఖాస్తు సమాచారం: " + " ".join(parts)
        return (
            "Application guidance from the verified records: " + " ".join(parts)
        )

    if language == "te":
        return "ధృవీకరించిన పథక వివరాలు: " + " ".join(
            f"{scheme.scheme_name}: {scheme.description}" for scheme in schemes
        )
    return "Verified scheme information: " + " ".join(
        f"{scheme.scheme_name}: {scheme.description}" for scheme in schemes
    )


class ChatGuidanceService:
    def __init__(self, gemini_service: GeminiService | None = None):
        self._gemini_service = gemini_service or GeminiService()

    def respond(self, request: ChatRequest) -> ChatResponse:
        intent = classify_intent(request.message)
        verified_schemes = _verified_schemes(load_schemes())
        mentioned = _mentioned_schemes(request.message, verified_schemes)

        if intent == "finding_schemes":
            selected = verified_schemes
        elif intent == "eligibility":
            selected = mentioned or verified_schemes
        else:
            selected = mentioned

        missing_information: list[str] = []
        if not verified_schemes:
            missing_information.append(
                "No verified scheme records are available in the current dataset."
            )
        elif not selected and intent != "finding_schemes":
            missing_information.append(
                "Name a scheme exactly as listed in the verified data, or ask to find schemes."
            )

        eligibility_by_id: dict[str, EligibilityResult] = {}
        if intent == "eligibility":
            profile = request.profile or UserProfile()
            eligibility_by_id = {
                result.scheme_id: result
                for result in evaluate_all(profile, selected)
            }
            for result in eligibility_by_id.values():
                missing_information.extend(result.missing_information)

        results: list[ChatSchemeResult] = []
        for scheme in selected:
            assert scheme.source_url is not None
            assert scheme.last_verified is not None
            results.append(
                ChatSchemeResult(
                    scheme_id=scheme.id,
                    scheme_name=scheme.name,
                    state=scheme.state,
                    state_exclusions=scheme.state_exclusions,
                    government_level=scheme.government_level,
                    category=scheme.category,
                    description=scheme.description,
                    eligibility_summary=scheme.eligibility_summary,
                    benefits=_nonempty_items(scheme.benefits),
                    required_documents=_nonempty_items(scheme.required_documents),
                    application_process=_nonempty_items(scheme.application_process),
                    unavailable_fields=scheme.unavailable_fields,
                    application_url=scheme.application_url,
                    source_url=scheme.source_url,
                    last_verified=scheme.last_verified,
                    eligibility=eligibility_by_id.get(scheme.id),
                )
            )

        if intent == "application_process" and selected:
            for scheme in selected:
                if not _nonempty_items(scheme.application_process):
                    missing_information.append(
                        f"Verified application steps are not available for {scheme.name}."
                    )
                if scheme.application_url is None:
                    missing_information.append(
                        f"No verified application URL is available for {scheme.name}."
                    )
        if intent == "benefits" and selected:
            for scheme in selected:
                if not _nonempty_items(scheme.benefits):
                    missing_information.append(
                        f"No verified benefit details are listed for {scheme.name}."
                    )
        if intent == "required_documents" and selected:
            for scheme in selected:
                if not _nonempty_items(scheme.required_documents):
                    missing_information.append(
                        f"No verified required-document details are listed for {scheme.name}."
                    )

        reply = _fallback_reply(
            intent,
            request.language,
            results,
            missing_information,
        )
        can_use_gemini = bool(selected) and intent not in {
            "eligibility",
            "application_process",
        }
        if intent == "benefits":
            can_use_gemini = can_use_gemini and any(
                _nonempty_items(scheme.benefits) for scheme in selected
            )
        elif intent == "required_documents":
            can_use_gemini = can_use_gemini and any(
                _nonempty_items(scheme.required_documents) for scheme in selected
            )

        if can_use_gemini:
            generated_reply = self._gemini_service.generate_guidance(
                intent=intent,
                language=request.language,
                scheme_facts=[_scheme_facts(scheme) for scheme in selected],
                missing_information=missing_information,
            )
            if generated_reply:
                reply = generated_reply
                if missing_information:
                    reply = f"{reply} {_missing_notice(request.language)}"

        return ChatResponse(
            intent=intent,
            language=request.language,
            reply=reply,
            schemes=results,
            missing_information=missing_information,
            disclaimer=(
                "Guidance is informational, based only on verified scheme records, "
                "and is not an official eligibility decision or approval."
            ),
        )
