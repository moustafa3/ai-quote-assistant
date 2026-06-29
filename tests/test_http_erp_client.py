import httpx
from pytest import MonkeyPatch

from app.integrations.http_erp_client import HttpERPClient


def test_http_erp_client_normalizes_dirty_customer_data(
    monkeypatch: MonkeyPatch,
) -> None:
    def fake_get(*args, **kwargs) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json=[
                {
                    "customerId": " CUST_001 ",
                    "companyName": "Entreprise Martin ",
                    "customerCategory": " eti ",
                    "industrySector": " Industrie ",
                    "discountPercent": "10 %",
                    "crmStatus": "HOT_LEAD",
                }
            ],
        )

    monkeypatch.setattr(httpx.Client, "get", fake_get)

    client = HttpERPClient(
        base_url="http://fake-erp.test",
        api_key="test-key",
        timeout_seconds=1,
    )

    customers = client.list_customers()

    assert len(customers) == 1
    assert customers[0].id == "cust_001"
    assert customers[0].name == "Entreprise Martin"
    assert customers[0].type == "ETI"
    assert customers[0].sector == "Industrie"
    assert customers[0].discount_rate == 0.10
    assert customers[0].crm_status == "prospect_chaud"


def test_http_erp_client_normalizes_dirty_product_data(
    monkeypatch: MonkeyPatch,
) -> None:
    def fake_get(*args, **kwargs) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json=[
                {
                    "sku": " PROD_001 ",
                    "label": "Agent IA Devis ",
                    "priceMonthly": "2000 EUR",
                    "billingMode": "MONTHLY",
                    "details": " Génération de brouillons de devis. ",
                }
            ],
        )

    monkeypatch.setattr(httpx.Client, "get", fake_get)

    client = HttpERPClient(
        base_url="http://fake-erp.test",
        api_key="test-key",
        timeout_seconds=1,
    )

    products = client.list_products()

    assert len(products) == 1
    assert products[0].id == "prod_001"
    assert products[0].name == "Agent IA Devis"
    assert products[0].unit_price == 2000
    assert products[0].billing == "monthly"
    assert products[0].description == "Génération de brouillons de devis."