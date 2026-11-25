from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatGuidanceService

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatGuidanceService()


@router.post("")
def chat(request: ChatRequest) -> ChatResponse:
    return chat_service.respond(request)
