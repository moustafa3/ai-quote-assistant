from fastapi import APIRouter

from app.application.schemas.chat_schema import ChatAskRequest, ChatAskResponse
from app.application.use_cases.ask_documents import AskDocumentsUseCase

router = APIRouter()


@router.post("/chat/ask", response_model=ChatAskResponse)
def ask_documents(request: ChatAskRequest) -> ChatAskResponse:
    """
    Ask a question over local business documents.
    """
    use_case = AskDocumentsUseCase()
    answer = use_case.execute(question=request.question)

    return ChatAskResponse(
        answer=answer.answer,
        sources=answer.sources,
    )