from app.domain.entities import DashboardKpis, QuoteDraft
from app.infrastructure.repositories.quote_repository import InMemoryQuoteRepository


class GetDashboardKpisUseCase:
    """
    Application use case for computing dashboard KPIs.
    """

    ESTIMATED_TIME_SAVED_PER_QUOTE_MINUTES = 20

    def __init__(
        self,
        quote_repository: InMemoryQuoteRepository | None = None,
    ) -> None:
        self.quote_repository = quote_repository or InMemoryQuoteRepository()

    def execute(self) -> DashboardKpis:
        """
        Compute KPIs from saved quote drafts.
        """
        quotes = self.quote_repository.list_all()

        return DashboardKpis(
            active_agents=1,
            quotes_generated=len(quotes),
            average_confidence_score=self._calculate_average_confidence(quotes),
            human_validation_rate=self._calculate_human_validation_rate(quotes),
            estimated_time_saved_minutes=(
                len(quotes) * self.ESTIMATED_TIME_SAVED_PER_QUOTE_MINUTES
            ),
        )

    def _calculate_average_confidence(self, quotes: list[QuoteDraft]) -> float:
        """
        Calculate average confidence score across generated quotes.
        """
        if not quotes:
            return 0.0

        total_confidence = sum(quote.confidence_score for quote in quotes)
        return round(total_confidence / len(quotes), 2)

    def _calculate_human_validation_rate(self, quotes: list[QuoteDraft]) -> float:
        """
        Calculate the percentage of quotes requiring human validation.
        """
        if not quotes:
            return 0.0

        quotes_requiring_validation = sum(
            1 for quote in quotes if quote.human_validation_required
        )

        return round((quotes_requiring_validation / len(quotes)) * 100, 2)