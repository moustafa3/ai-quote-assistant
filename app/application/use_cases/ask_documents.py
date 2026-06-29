from app.ai.rag_service import RagService
from app.domain.entities import RagAnswer


class AskDocumentsUseCase:
    """
    Application use case for asking questions over local business documents.
    """

    def __init__(self, rag_service: RagService | None = None) -> None:
        self.rag_service = rag_service or RagService()

    def execute(self, question: str) -> RagAnswer:
        """
        Answer a question using the local document RAG service.
        """
        return self.rag_service.answer_question(question=question)