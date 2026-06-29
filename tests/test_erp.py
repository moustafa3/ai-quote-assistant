from fastapi.testclient import TestClient


def test_list_customers_returns_mock_customers(client: TestClient) -> None:
    response = client.get("/api/v1/erp/customers")

    assert response.status_code == 200

    customers = response.json()

    assert len(customers) == 3
    assert customers[0]["id"] == "cust_001"
    assert customers[0]["name"] == "Entreprise Martin"
    assert customers[0]["type"] == "ETI"
    assert customers[0]["discount_rate"] == 0.10


def test_list_products_returns_mock_products(client: TestClient) -> None:
    response = client.get("/api/v1/erp/products")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 3
    assert products[0]["id"] == "prod_001"
    assert products[0]["name"] == "Agent IA Devis"
    assert products[0]["unit_price"] == 2000
    assert products[0]["billing"] == "monthly"