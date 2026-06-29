from app.core.exceptions import ResourceNotFoundError
from app.domain.entities import QuoteDraft
from app.infrastructure.repositories.quote_repository import InMemoryQuoteRepository


class GetQuoteUseCase:
    """
    Application use case for retrieving a saved quote draft.
    """

    def __init__(
        self,
        quote_repository: InMemoryQuoteRepository | None = None,
    ) -> None:
        self.quote_repository = quote_repository or InMemoryQuoteRepository()

    def execute(self, quote_id: str) -> QuoteDraft:
        """
        Return a quote draft by ID.
        """
        quote = self.quote_repository.get_by_id(quote_id=quote_id)

        if quote is None:
            raise ResourceNotFoundError(
                f"Quote with id '{quote_id}' was not found."
            )

        return quote