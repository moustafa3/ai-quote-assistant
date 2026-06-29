from fastapi.testclient import TestClient


def test_chat_ask_returns_answer_with_source(client: TestClient) -> None:
    payload = {
        "question": "Quelle remise appliquer pour une ETI ?",
    }

    response = client.post("/api/v1/chat/ask", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "remise de 10" in data["answer"]
    assert "commercial_conditions.txt" in data["sources"]


def test_chat_ask_returns_catalog_source(client: TestClient) -> None:
    payload = {
        "question": "Quel est le prix de l'Agent IA Devis ?",
    }

    response = client.post("/api/v1/chat/ask", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "Agent IA Devis" in data["answer"]
    assert "sample_catalog.txt" in data["sources"]