from app.core.config import GEMINI_API_KEY, GEMINI_MODEL
from app.core.prompts import SYSTEM_PROMPT
from app.models.profile import UserProfile
from app.models.eligibility import MatchResult


class GeminiService:
    def explain_match(self, match: MatchResult, language: str) -> str:
        if not GEMINI_API_KEY:
            return self._fallback(match, language)

        try:
            from google import genai

            client = genai.Client(api_key=GEMINI_API_KEY)
            facts = {
                "scheme": match.scheme.model_dump(mode="json"),
                "status": match.status,
                "reasons": [reason.model_dump(mode="json") for reason in match.reasons],
            }
            prompt = (
                f"{SYSTEM_PROMPT}\nLanguage: {'Telugu' if language == 'te' else 'English'}.\n"
                f"Verified facts and deterministic match: {facts}\n"
                "Write a concise explanation for the user."
            )
            response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            return response.text or self._fallback(match, language)
        except Exception:
            return self._fallback(match, language)

    def chat(self, message: str, language: str, scheme_context: dict | None) -> str:
        if not GEMINI_API_KEY:
            if language == "te":
                return "క్షమించండి, AI ప్రస్తుతం అందుబాటులో లేదు. మీరు ప్రొఫైల్ వివరాలు మరియు పథకం వివరాలను చూస్తూ పునఃపరిశీలించవచ్చు."
            return "AI is not configured right now. Please review the profile and scheme facts shown in the results."

        try:
            from google import genai

            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = (
                f"{SYSTEM_PROMPT}\nLanguage: {'Telugu' if language == 'te' else 'English'}.\n"
                f"Verified scheme context: {scheme_context or 'No scheme selected.'}\n"
                f"User question: {message}\n"
                "Answer only with supplied facts or say that the fact is not available."
            )
            response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            return response.text or "I could not generate a response from the available information."
        except Exception:
            return "AI is temporarily unavailable. Please use the verified scheme details shown below."

    def _fallback(self, match: MatchResult, language: str) -> str:
        name = match.scheme.name_te if language == "te" else match.scheme.name
        status_labels = {
            "te": {
                "potentially_eligible": "మీరు సంభావ్యంగా पात्रంగా ఉండవచ్చు",
                "not_eligible": "తెలిసిన సమాచారం ఆధారంగా మీరు पात्रులు కాకపోవచ్చు",
                "needs_verification": "మరిన్ని వివరాలు ధృవీకరించాలి",
            },
            "en": {
                "potentially_eligible": "You may be potentially eligible",
                "not_eligible": "You may not be eligible based on the known information",
                "needs_verification": "Additional information needs verification",
            },
        }
        explanation = status_labels[language][match.status]
        if language == "te":
            return f"{name}: {explanation}. ఇది అధికారిక నిర్ణయం కాదు; అధికారిక పథక నిబంధనలను ధృవీకరించండి."
        return f"{name}: {explanation}. This is informational guidance, not an official approval decision."
