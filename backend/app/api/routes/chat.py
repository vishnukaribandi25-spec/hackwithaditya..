from typing import Literal, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    language: Literal["en", "te"] = "en"
    scheme_context: Optional[dict] = None


@router.post("")
def chat(request: ChatRequest):
    reply = GeminiService().chat(request.message, request.language, request.scheme_context)
    return {"reply": reply}
