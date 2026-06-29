from fastapi import FastAPI, Header, HTTPException, status

app = FastAPI(
    title="Mock External ERP API",
    description="Simulated third-party ERP API with dirty data formats.",
    version="0.1.0",
)

EXPECTED_API_KEY = "local-demo-key"


def _check_api_key(x_api_key: str | None) -> None:
    """
    Simulate API key authentication for the external ERP API.
    """
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid ERP API key.",
        )


@app.get("/external-api/v1/customers")
def list_customers(x_api_key: str | None = Header(default=None)) -> list[dict]:
    """
    Return intentionally messy customer data.

    This simulates a real ERP/CRM API where field names, casing,
    types and formats are not always clean.
    """
    _check_api_key(x_api_key)

    return [
        {
            "customerId": " CUST_001 ",
            "companyName": "Entreprise Martin",
            "customerCategory": " eti ",
            "industrySector": "Industrie",
            "discountPercent": "10%",
            "crmStatus": "HOT_LEAD",
        },
        {
            "customerId": "CUST_002",
            "companyName": "Cabinet Durand ",
            "customerCategory": "pme",
            "industrySector": "Services",
            "discountPercent": "5 %",
            "crmStatus": "EXISTING_CUSTOMER",
        },
        {
            "customerId": "cust_003",
            "companyName": "Logistique Bernard",
            "customerCategory": "PME",
            "industrySector": "Transport",
            "discountPercent": 5,
            "crmStatus": "prospect",
        },
    ]


@app.get("/external-api/v1/products")
def list_products(x_api_key: str | None = Header(default=None)) -> list[dict]:
    """
    Return intentionally messy product data.
    """
    _check_api_key(x_api_key)

    return [
        {
            "sku": " PROD_001 ",
            "label": "Agent IA Devis",
            "priceMonthly": "2000 EUR",
            "billingMode": "MONTHLY",
            "details": (
                "Agent permettant de générer des brouillons de devis "
                "à partir de demandes commerciales."
            ),
        },
        {
            "sku": "PROD_002",
            "label": "Agent IA Documentaire",
            "priceMonthly": "1500",
            "billingMode": "monthly",
            "details": (
                "Agent permettant de classifier, extraire et rechercher "
                "des informations dans des documents métier."
            ),
        },
        {
            "sku": "prod_003",
            "label": "Agent IA Email ",
            "priceMonthly": 1200,
            "billingMode": "Monthly",
            "details": (
                "Agent permettant d'analyser, classer et préparer des réponses "
                "aux emails clients."
            ),
        },
    ]