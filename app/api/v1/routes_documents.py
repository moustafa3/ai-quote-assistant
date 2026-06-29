from fastapi import APIRouter

from app.application.schemas.document_schema import (
    DocumentClassificationRequest,
    DocumentClassificationResponse,
)
from app.application.use_cases.classify_document import ClassifyDocumentUseCase

router = APIRouter()


@router.post(
    "/documents/classify",
    response_model=DocumentClassificationResponse,
)
def classify_document(
    request: DocumentClassificationRequest,
) -> DocumentClassificationResponse:
    """
    Classify a business document.
    """
    use_case = ClassifyDocumentUseCase()
    classification = use_case.execute(
        filename=request.filename,
        content=request.content,
    )

    return DocumentClassificationResponse(
        document_type=classification.document_type,
        confidence_score=classification.confidence_score,
    )