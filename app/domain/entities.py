from dataclasses import dataclass
from typing import Literal


DocumentType = Literal[
    "product_catalog",
    "commercial_conditions",
    "customer_request",
    "unknown",
]


@dataclass(frozen=True)
class Customer:
    """
    Business customer coming from the simulated CRM/ERP.
    """

    id: str
    name: str
    type: str
    sector: str
    discount_rate: float
    crm_status: str


@dataclass(frozen=True)
class Product:
    """
    Business product coming from the simulated ERP catalog.
    """

    id: str
    name: str
    unit_price: float
    billing: str
    description: str


@dataclass(frozen=True)
class DocumentClassification:
    """
    Result of a business document classification.
    """

    document_type: DocumentType
    confidence_score: float


@dataclass(frozen=True)
class SourcePassage:
    """
    Text passage retrieved from a local business document.
    """

    filename: str
    content: str
    score: int


@dataclass(frozen=True)
class RagAnswer:
    """
    Answer generated from retrieved local document passages.
    """

    answer: str
    sources: list[str]


@dataclass(frozen=True)
class QuoteItem:
    """
    Single line item in a quote draft.
    """

    name: str
    quantity: int
    unit_price: float
    total: float


@dataclass(frozen=True)
class QuoteDraft:
    """
    AI-generated quote draft.

    This is never a final quote. It always requires human validation.
    """

    quote_id: str
    customer_name: str
    recommended_solution: str
    items: list[QuoteItem]
    subtotal: float
    discount_rate: float
    discount_amount: float
    total: float
    sources: list[str]
    assumptions: list[str]
    validation_points: list[str]
    human_validation_required: bool
    confidence_score: float


@dataclass(frozen=True)
class DashboardKpis:
    """
    Business KPIs exposed by the mini dashboard.
    """

    active_agents: int
    quotes_generated: int
    average_confidence_score: float
    human_validation_rate: float
    estimated_time_saved_minutes: int