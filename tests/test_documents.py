from fastapi.testclient import TestClient


def test_classify_commercial_conditions_document(client: TestClient) -> None:
    payload = {
        "filename": "commercial_conditions.txt",
        "content": (
            "Les clients ETI bénéficient d'une remise de 10 %. "
            "Tout devis généré par IA doit être validé par un humain avant envoi."
        ),
    }

    response = client.post("/api/v1/documents/classify", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["document_type"] == "commercial_conditions"
    assert 0 <= data["confidence_score"] <= 1


def test_classify_product_catalog_document(client: TestClient) -> None:
    payload = {
        "filename": "sample_catalog.txt",
        "content": (
            "Agent IA Devis : 2000 euros par mois. "
            "Agent IA Documentaire : 1500 euros par mois."
        ),
    }

    response = client.post("/api/v1/documents/classify", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["document_type"] == "product_catalog"
    assert 0 <= data["confidence_score"] <= 1


def test_classify_unknown_document(client: TestClient) -> None:
    payload = {
        "filename": "random_note.txt",
        "content": "Bonjour, ceci est une note sans contexte métier clair.",
    }

    response = client.post("/api/v1/documents/classify", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["document_type"] == "unknown"
    assert data["confidence_score"] == 0.35