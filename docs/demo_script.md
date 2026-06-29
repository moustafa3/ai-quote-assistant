# Demo Script

This script can be used to present AI Quote Assistant during a technical interview.

## Demo goal

Show that the project can simulate a real business AI agent connected to documents, ERP/CRM data, quote generation logic, human validation, and operational KPIs.

## Before starting

Run the project locally:

```powershell
.\.venv\Scripts\Activate.ps1
fastapi dev app/main.py
```

Or run it with Docker:

```powershell
docker compose up --build
```

Open Swagger:

```text
http://localhost:8000/docs
```

## 1. Introduce the project

Suggested explanation:

AI Quote Assistant is a FastAPI backend that simulates an AI agent for a B2B company.

It can classify business documents, answer questions over local documents using a simple RAG approach, read customers and products from a simulated ERP/CRM, generate quote drafts, require human validation, and expose simple KPIs.

The goal is to show a realistic AI engineering workflow without over-engineering the MVP.

## 2. Show the health endpoint

Endpoint:

```http
GET /api/v1/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "ai-quote-assistant"
}
```

What to say:

This endpoint is useful for basic monitoring and deployment checks.

## 3. Show ERP/CRM customers

Endpoint:

```http
GET /api/v1/erp/customers
```

What to show:

A customer like:

```json
{
  "id": "cust_001",
  "name": "Entreprise Martin",
  "type": "ETI",
  "sector": "Industrie",
  "discount_rate": 0.1,
  "crm_status": "prospect_chaud"
}
```

What to say:

In the MVP, this is mocked. In production, this integration could call Odoo, SAP, Cegid, Divalto, Salesforce, HubSpot, or another business API.

## 4. Show ERP products

Endpoint:

```http
GET /api/v1/erp/products
```

What to show:

The product catalog includes:

* Agent IA Devis
* Agent IA Documentaire
* Agent IA Email

What to say:

The quote agent uses these products to recommend the best solution based on the customer request.

## 5. Show document classification

Endpoint:

```http
POST /api/v1/documents/classify
```

Request:

```json
{
  "filename": "commercial_conditions.txt",
  "content": "Les clients ETI bénéficient d'une remise de 10 %. Tout devis généré par IA doit être validé par un humain avant envoi."
}
```

Expected response:

```json
{
  "document_type": "commercial_conditions",
  "confidence_score": 0.84
}
```

What to say:

The classifier is deterministic in the MVP, which makes it easy to test and demo without an external LLM dependency.

Later, it could be replaced with an LLM classifier or an embeddings-based classifier.

## 6. Show simple RAG

Endpoint:

```http
POST /api/v1/chat/ask
```

Request:

```json
{
  "question": "Quelle remise appliquer pour une ETI ?"
}
```

Expected response:

```json
{
  "answer": "Les clients ETI bénéficient d’une remise de 10 %.",
  "sources": [
    "commercial_conditions.txt"
  ]
}
```

What to say:

The RAG implementation loads local text documents, searches for relevant passages, and returns an answer with sources.

The MVP uses keyword matching. A production version could use embeddings and pgvector.

## 7. Generate a quote draft

Endpoint:

```http
POST /api/v1/quotes/generate
```

Request:

```json
{
  "customer_id": "cust_001",
  "request": "Le client veut automatiser la génération de devis à partir des demandes commerciales et des documents internes."
}
```

Expected response highlights:

```json
{
  "quote_id": "quote_001",
  "customer_name": "Entreprise Martin",
  "recommended_solution": "Agent IA Devis",
  "subtotal": 2000,
  "discount_rate": 0.1,
  "discount_amount": 200,
  "total": 1800,
  "human_validation_required": true,
  "confidence_score": 0.86
}
```

What to say:

The quote agent selects the most relevant product, applies the customer discount, adds assumptions, adds validation points, and forces human validation.

The generated quote is a draft, not a final quote.

## 8. Retrieve the saved quote

Endpoint:

```http
GET /api/v1/quotes/quote_001
```

What to say:

The quote is saved in an in-memory repository for the MVP.

This keeps the project simple, but the repository pattern makes it easy to replace with PostgreSQL later.

## 9. Show dashboard KPIs

Endpoint:

```http
GET /api/v1/dashboard/kpis
```

Expected response after one generated quote:

```json
{
  "active_agents": 1,
  "quotes_generated": 1,
  "average_confidence_score": 0.86,
  "human_validation_rate": 100,
  "estimated_time_saved_minutes": 20
}
```

What to say:

This simulates a mini operational dashboard.

It tracks generated quotes, confidence, human validation rate, and estimated time saved.

## 10. Show tests

Run:

```powershell
pytest
```

What to say:

The project includes automated tests for the main API endpoints.

This helps prevent regressions when adding features.

## 11. Show Docker

Run:

```powershell
docker compose up --build
```

What to say:

The project can be run in Docker, which makes it easier to share and deploy.

## 12. Show GitHub Actions

Open the GitHub repository.

Go to:

```text
Actions > CI
```

What to say:

The CI workflow installs dependencies and runs the Pytest suite on every push and pull request to main.

## 13. Final interview summary

Suggested closing explanation:

This project is a realistic MVP of a business AI agent. It shows backend engineering, FastAPI, Clean Architecture, RAG basics, ERP/CRM integration patterns, quote generation logic, testing, Docker, CI/CD, and human validation. The current implementation is simple on purpose, but the architecture is ready for production improvements like PostgreSQL, pgvector, real ERP connectors, authentication, monitoring, and a full human approval workflow.
