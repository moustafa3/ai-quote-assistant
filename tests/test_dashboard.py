from fastapi.testclient import TestClient


def test_dashboard_kpis_without_quotes(client: TestClient) -> None:
    response = client.get("/api/v1/dashboard/kpis")

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "active_agents": 1,
        "quotes_generated": 0,
        "average_confidence_score": 0.0,
        "human_validation_rate": 0.0,
        "estimated_time_saved_minutes": 0,
    }


def test_dashboard_kpis_after_generating_quote(client: TestClient) -> None:
    payload = {
        "customer_id": "cust_001",
        "request": (
            "Le client veut automatiser la génération de devis à partir "
            "des demandes commerciales et des documents internes."
        ),
    }

    quote_response = client.post("/api/v1/quotes/generate", json=payload)

    assert quote_response.status_code == 200

    kpi_response = client.get("/api/v1/dashboard/kpis")

    assert kpi_response.status_code == 200

    data = kpi_response.json()

    assert data["active_agents"] == 1
    assert data["quotes_generated"] == 1
    assert data["average_confidence_score"] == 0.86
    assert data["human_validation_rate"] == 100
    assert data["estimated_time_saved_minutes"] == 20