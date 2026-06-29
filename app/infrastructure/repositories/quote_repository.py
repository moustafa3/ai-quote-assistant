from typing import ClassVar

from app.domain.entities import QuoteDraft


class InMemoryQuoteRepository:
    """
    Simple in-memory quote repository.

    This repository is useful for the MVP because it requires no database.
    In production, it can be replaced by a PostgreSQL repository using SQLAlchemy.
    """

    _quotes: ClassVar[dict[str, QuoteDraft]] = {}
    _counter: ClassVar[int] = 0

    def next_quote_id(self) -> str:
        """
        Generate the next quote identifier.
        """
        type(self)._counter += 1
        return f"quote_{type(self)._counter:03d}"

    def save(self, quote: QuoteDraft) -> QuoteDraft:
        """
        Save a quote draft in memory.
        """
        type(self)._quotes[quote.quote_id] = quote
        return quote

    def get_by_id(self, quote_id: str) -> QuoteDraft | None:
        """
        Return a quote draft by ID.
        """
        return type(self)._quotes.get(quote_id)

    def list_all(self) -> list[QuoteDraft]:
        """
        Return all saved quote drafts.
        """
        return list(type(self)._quotes.values())

    def clear(self) -> None:
        """
        Clear all saved quotes.

        This is mainly useful for future tests.
        """
        type(self)._quotes.clear()
        type(self)._counter = 0