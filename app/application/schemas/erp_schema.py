from pydantic import BaseModel, Field


class CustomerResponse(BaseModel):
    """
    API response model for a customer.
    """

    id: str = Field(..., examples=["cust_001"])
    name: str = Field(..., examples=["Entreprise Martin"])
    type: str = Field(..., examples=["ETI"])
    sector: str = Field(..., examples=["Industrie"])
    discount_rate: float = Field(..., examples=[0.10])
    crm_status: str = Field(..., examples=["prospect_chaud"])


class ProductResponse(BaseModel):
    """
    API response model for a product.
    """

    id: str = Field(..., examples=["prod_001"])
    name: str = Field(..., examples=["Agent IA Devis"])
    unit_price: float = Field(..., examples=[2000])
    billing: str = Field(..., examples=["monthly"])
    description: str = Field(
        ...,
        examples=[
            "Agent permettant de générer des brouillons de devis à partir de demandes commerciales."
        ],
    )