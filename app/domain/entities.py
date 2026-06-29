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