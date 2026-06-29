from fastapi import APIRouter, HTTPException, status

from app.application.schemas.quote_schema import (
    QuoteGenerationRequest,
    QuoteGenerationResponse,
    QuoteItemResponse,
)
from app.application.use_cases.generate_quote import GenerateQuoteUseCase
from app.application.use_cases.get_quote import GetQuoteUseCase
from app.core.exceptions import ResourceNotFoundError
from app.domain.entities import QuoteDraft

router = APIRouter()


@router.post(
    "/quotes/generate",
    response_model=QuoteGenerationResponse,
)
def generate_quote(
    request: QuoteGenerationRequest,
) -> QuoteGenerationResponse:
    """
    Generate and save an AI quote draft.

    The generated quote is not final and requires human validation.
    """
    use_case = GenerateQuoteUseCase()

    try:
        quote = use_case.execute(
            customer_id=request.customer_id,
            request=request.request,
        )
    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return _to_quote_response(quote)


@router.get(
    "/quotes/{quote_id}",
    response_model=QuoteGenerationResponse,
)
def get_quote(quote_id: str) -> QuoteGenerationResponse:
    """
    Return a saved quote draft by ID.
    """
    use_case = GetQuoteUseCase()

    try:
        quote = use_case.execute(quote_id=quote_id)
    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return _to_quote_response(quote)


def _to_quote_response(quote: QuoteDraft) -> QuoteGenerationResponse:
    """
    Convert a domain QuoteDraft into an API response.
    """
    return QuoteGenerationResponse(
        quote_id=quote.quote_id,
        customer_name=quote.customer_name,
        recommended_solution=quote.recommended_solution,
        items=[
            QuoteItemResponse(
                name=item.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total=item.total,
            )
            for item in quote.items
        ],
        subtotal=quote.subtotal,
        discount_rate=quote.discount_rate,
        discount_amount=quote.discount_amount,
        total=quote.total,
        sources=quote.sources,
        assumptions=quote.assumptions,
        validation_points=quote.validation_points,
        human_validation_required=quote.human_validation_required,
        confidence_score=quote.confidence_score,
    )