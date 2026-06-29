from pydantic import BaseModel, Field


class QuoteGenerationRequest(BaseModel):
    """
    API request model for quote generation.
    """

    customer_id: str = Field(..., examples=["cust_001"])
    request: str = Field(
        ...,
        min_length=10,
        examples=[
            "Le client veut automatiser la génération de devis à partir des demandes commerciales et des documents internes."
        ],
    )


class QuoteItemResponse(BaseModel):
    """
    API response model for a quote item.
    """

    name: str = Field(..., examples=["Agent IA Devis"])
    quantity: int = Field(..., examples=[1])
    unit_price: float = Field(..., examples=[2000])
    total: float = Field(..., examples=[2000])


class QuoteGenerationResponse(BaseModel):
    """
    API response model for an AI-generated quote draft.
    """

    quote_id: str = Field(..., examples=["quote_001"])
    customer_name: str = Field(..., examples=["Entreprise Martin"])
    recommended_solution: str = Field(..., examples=["Agent IA Devis"])
    items: list[QuoteItemResponse]
    subtotal: float = Field(..., examples=[2000])
    discount_rate: float = Field(..., examples=[0.10])
    discount_amount: float = Field(..., examples=[200])
    total: float = Field(..., examples=[1800])
    sources: list[str] = Field(
        ...,
        examples=[["sample_catalog.txt", "commercial_conditions.txt"]],
    )
    assumptions: list[str] = Field(
        ...,
        examples=[
            [
                "Le devis est basé sur un abonnement mensuel.",
                "Le volume exact de demandes commerciales doit être confirmé.",
            ]
        ],
    )
    validation_points: list[str] = Field(
        ...,
        examples=[
            [
                "Valider la remise commerciale.",
                "Confirmer le périmètre fonctionnel.",
                "Vérifier les conditions contractuelles.",
            ]
        ],
    )
    human_validation_required: bool = Field(..., examples=[True])
    confidence_score: float = Field(..., ge=0, le=1, examples=[0.86])