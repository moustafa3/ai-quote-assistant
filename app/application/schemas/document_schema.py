from typing import Literal

from pydantic import BaseModel, Field


DocumentTypeResponse = Literal[
    "product_catalog",
    "commercial_conditions",
    "customer_request",
    "unknown",
]


class DocumentClassificationRequest(BaseModel):
    """
    API request model used to classify a business document.
    """

    filename: str = Field(..., examples=["commercial_conditions.txt"])
    content: str = Field(
        ...,
        examples=["Les clients ETI bénéficient d'une remise de 10 %."],
    )


class DocumentClassificationResponse(BaseModel):
    """
    API response model for document classification.
    """

    document_type: DocumentTypeResponse = Field(
        ...,
        examples=["commercial_conditions"],
    )
    confidence_score: float = Field(..., ge=0, le=1, examples=[0.91])