from fastapi.testclient import TestClient


def test_generate_quote_returns_draft_with_human_validation(
    client: TestClient,
) -> None:
    payload = {
        "customer_id": "cust_001",
        "request": (
            "Le client veut automatiser la génération de devis à partir "
            "des demandes commerciales et des documents internes."
        ),
    }

    response = client.post("/api/v1/quotes/generate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["quote_id"] == "quote_001"
    assert data["customer_name"] == "Entreprise Martin"
    assert data["recommended_solution"] == "Agent IA Devis"
    assert data["subtotal"] == 2000
    assert data["discount_rate"] == 0.10
    assert data["discount_amount"] == 200
    assert data["total"] == 1800
    assert data["human_validation_required"] is True
    assert data["confidence_score"] == 0.86
    assert "sample_catalog.txt" in data["sources"]
    assert "commercial_conditions.txt" in data["sources"]


def test_get_quote_returns_saved_quote(client: TestClient) -> None:
    payload = {
        "customer_id": "cust_001",
        "request": (
            "Le client veut automatiser la génération de devis à partir "
            "des demandes commerciales et des documents internes."
        ),
    }

    generate_response = client.post("/api/v1/quotes/generate", json=payload)

    assert generate_response.status_code == 200

    quote_id = generate_response.json()["quote_id"]

    get_response = client.get(f"/api/v1/quotes/{quote_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["quote_id"] == quote_id
    assert data["customer_name"] == "Entreprise Martin"
    assert data["human_validation_required"] is True


def test_generate_quote_returns_404_for_unknown_customer(
    client: TestClient,
) -> None:
    payload = {
        "customer_id": "cust_999",
        "request": "Le client veut automatiser la génération de devis.",
    }

    response = client.post("/api/v1/quotes/generate", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer with id 'cust_999' was not found."


def test_get_quote_returns_404_for_unknown_quote(client: TestClient) -> None:
    response = client.get("/api/v1/quotes/quote_999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Quote with id 'quote_999' was not found."