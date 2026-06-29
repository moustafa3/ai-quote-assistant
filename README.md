# AI Quote Assistant

AI Quote Assistant is a professional FastAPI project that simulates a business AI agent for small and mid-sized companies.

The API demonstrates how an AI assistant can classify business documents, answer questions over local documents with a simple RAG approach, retrieve customer and product data from a simulated ERP/CRM, generate quote drafts, require human validation, and expose operational KPIs through a mini dashboard.

## 1. Project overview

AI Quote Assistant is a backend API designed to simulate a real-world AI agent connected to business systems.

It focuses on a concrete business use case: helping a sales team generate quote drafts from customer requests, internal documents, and ERP/CRM data.

The generated quote is never considered final. It always requires human validation before being sent to a customer.

## 2. Business context

Many small and mid-sized companies manage sales requests across multiple tools:

* ERP systems
* CRM platforms
* internal documents
* product catalogs
* commercial conditions
* customer emails

This creates manual work for sales teams. They need to search for information, check pricing, apply discounts, prepare quote drafts, and validate commercial rules.

AI Quote Assistant shows how an AI agent can assist this workflow while keeping a human in control.

## 3. Why this project

This project was built to demonstrate practical backend and AI engineering skills:

* Clean FastAPI architecture
* business-oriented AI agent design
* simple but useful RAG over local documents
* simulated ERP/CRM integration
* quote generation logic
* mandatory human validation
* API testing with Pytest
* Docker setup
* GitHub Actions CI
* clear documentation and demo scenario

The project is intentionally realistic but not over-engineered. It is designed as a strong MVP that can be extended toward production.

## 4. Features

### Health check

```text
GET /api/v1/health
```

Returns the API status.

### Mock ERP/CRM integration

```text
GET /api/v1/erp/customers
GET /api/v1/erp/products
```

Returns simulated customers and products.

### Document classification

```text
POST /api/v1/documents/classify
```

Classifies business documents into:

* `product_catalog`
* `commercial_conditions`
* `customer_request`
* `unknown`

### Simple local RAG

```text
POST /api/v1/chat/ask
```

Answers questions using local text documents from the `docs/` folder.

The current implementation uses keyword matching to keep the MVP simple and fully testable.

### Quote draft generation

```text
POST /api/v1/quotes/generate
```

Generates an AI-assisted quote draft using:

* customer data
* product catalog data
* commercial discount rules
* assumptions
* validation points
* confidence score
* mandatory human validation

### Quote retrieval

```text
GET /api/v1/quotes/{quote_id}
```

Returns a previously generated quote draft from the in-memory repository.

### Dashboard KPIs

```text
GET /api/v1/dashboard/kpis
```

Returns simple KPIs:

* active agents
* generated quotes
* average confidence score
* human validation rate
* estimated time saved

## 5. Architecture

The project follows a Clean Architecture inspired structure.

```text
ai-quote-assistant/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   ├── core/
│   ├── domain/
│   ├── application/
│   │   ├── schemas/
│   │   └── use_cases/
│   ├── infrastructure/
│   │   └── repositories/
│   ├── integrations/
│   └── ai/
│
├── docs/
├── tests/
├── .github/
│   └── workflows/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Layer responsibilities

| Layer                   | Responsibility                                             |
| ----------------------- | ---------------------------------------------------------- |
| `api/v1`                | FastAPI routes                                             |
| `application/use_cases` | Application orchestration                                  |
| `application/schemas`   | Pydantic request and response models                       |
| `domain`                | Business entities and pure business rules                  |
| `ai`                    | AI services, RAG, classifier, quote agent, LLM abstraction |
| `integrations`          | Simulated ERP/CRM client                                   |
| `infrastructure`        | Repositories and persistence adapters                      |
| `core`                  | Configuration, logging, exceptions                         |

The goal is to keep routes thin and business logic isolated.

## 6. Tech stack

* Python
* FastAPI
* Pydantic
* Pydantic Settings
* OpenAI SDK-ready architecture
* Pytest
* HTTPX / FastAPI TestClient
* Docker
* Docker Compose
* GitHub Actions
* PowerShell-friendly setup for Windows

## 7. API endpoints

### Health

```http
GET /api/v1/health
```

Example response:

```json
{
  "status": "ok",
  "service": "ai-quote-assistant"
}
```

### ERP customers

```http
GET /api/v1/erp/customers
```

Example response:

```json
[
  {
    "id": "cust_001",
    "name": "Entreprise Martin",
    "type": "ETI",
    "sector": "Industrie",
    "discount_rate": 0.1,
    "crm_status": "prospect_chaud"
  }
]
```

### ERP products

```http
GET /api/v1/erp/products
```

Example response:

```json
[
  {
    "id": "prod_001",
    "name": "Agent IA Devis",
    "unit_price": 2000,
    "billing": "monthly",
    "description": "Agent permettant de générer des brouillons de devis à partir de demandes commerciales."
  }
]
```

### Document classification

```http
POST /api/v1/documents/classify
```

Example request:

```json
{
  "filename": "commercial_conditions.txt",
  "content": "Les clients ETI bénéficient d'une remise de 10 %."
}
```

Example response:

```json
{
  "document_type": "commercial_conditions",
  "confidence_score": 0.84
}
```

### Chat / RAG

```http
POST /api/v1/chat/ask
```

Example request:

```json
{
  "question": "Quelle remise appliquer pour une ETI ?"
}
```

Example response:

```json
{
  "answer": "Les clients ETI bénéficient d’une remise de 10 %.",
  "sources": [
    "commercial_conditions.txt"
  ]
}
```

### Quote generation

```http
POST /api/v1/quotes/generate
```

Example request:

```json
{
  "customer_id": "cust_001",
  "request": "Le client veut automatiser la génération de devis à partir des demandes commerciales et des documents internes."
}
```

Example response:

```json
{
  "quote_id": "quote_001",
  "customer_name": "Entreprise Martin",
  "recommended_solution": "Agent IA Devis",
  "items": [
    {
      "name": "Agent IA Devis",
      "quantity": 1,
      "unit_price": 2000,
      "total": 2000
    }
  ],
  "subtotal": 2000,
  "discount_rate": 0.1,
  "discount_amount": 200,
  "total": 1800,
  "sources": [
    "sample_catalog.txt",
    "commercial_conditions.txt"
  ],
  "assumptions": [
    "Le devis est basé sur un abonnement mensuel.",
    "Le volume exact de demandes commerciales doit être confirmé."
  ],
  "validation_points": [
    "Valider la remise commerciale.",
    "Confirmer le périmètre fonctionnel.",
    "Vérifier les conditions contractuelles."
  ],
  "human_validation_required": true,
  "confidence_score": 0.86
}
```

### Quote retrieval

```http
GET /api/v1/quotes/quote_001
```

### Dashboard KPIs

```http
GET /api/v1/dashboard/kpis
```

Example response after generating one quote:

```json
{
  "active_agents": 1,
  "quotes_generated": 1,
  "average_confidence_score": 0.86,
  "human_validation_rate": 100,
  "estimated_time_saved_minutes": 20
}
```

## 8. How to run locally on Windows

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the API:

```powershell
fastapi dev app/main.py
```

Open Swagger:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/api/v1/health
```

## 9. How to run with Docker

Make sure Docker Desktop is running.

Build the image:

```powershell
docker compose build
```

Start the API:

```powershell
docker compose up
```

Or build and start in one command:

```powershell
docker compose up --build
```

Open Swagger:

```text
http://localhost:8000/docs
```

Stop the container:

```powershell
docker compose down
```

## 10. How to run tests

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run all tests:

```powershell
pytest
```

Run tests with verbose output:

```powershell
pytest -v
```

The test suite covers:

* health endpoint
* ERP/CRM mock endpoints
* document classification
* local RAG endpoint
* quote generation
* quote retrieval
* dashboard KPIs

## 11. Demo scenario

A complete demo scenario is available here:

```text
docs/demo_script.md
```

Recommended demo flow:

1. Open Swagger.
2. Check the health endpoint.
3. List ERP customers and products.
4. Classify a commercial document.
5. Ask a RAG question about ETI discounts.
6. Generate a quote draft.
7. Retrieve the generated quote.
8. Display dashboard KPIs.
9. Explain why human validation is mandatory.

## 12. Production notes

This MVP is intentionally simple, but the architecture prepares production improvements.

Recommended production evolutions:

* Replace in-memory storage with PostgreSQL and SQLAlchemy.
* Add database migrations with Alembic.
* Replace simple keyword RAG with embeddings and pgvector.
* Add authentication and role-based access control.
* Add request tracing and structured logs.
* Add monitoring and alerting.
* Add rate limiting.
* Add input sanitization and stricter validation.
* Store audit logs for quote generation and validation.
* Add a real human approval workflow before quote sending.

## 13. Limitations

Current limitations:

* Quote storage is in memory.
* Data is lost when the API server restarts.
* ERP/CRM integration is mocked.
* RAG uses simple keyword matching.
* The LLM mode defaults to deterministic mock responses.
* No authentication is implemented yet.
* No real email sending or quote sending is implemented.
* No production database is connected yet.
* No frontend dashboard is included.

These limitations are acceptable for an MVP and are documented clearly.

## 14. Next improvements

Planned improvements:

* Add PostgreSQL persistence.
* Add SQLAlchemy models and repositories.
* Add Alembic migrations.
* Add pgvector for semantic search.
* Add LangChain-based RAG pipeline.
* Add document upload support.
* Add real OpenAI mode for classification and quote support.
* Add human approval status for quote drafts.
* Add quote export to PDF.
* Add a small frontend dashboard.
* Add observability with structured logs and metrics.

## LLM mode

Default mode:

```env
LLM_PROVIDER=mock
```

This mode works without an API key.

Optional mode:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.5
```

Never commit the `.env` file.

## Security note

Secrets must be stored in a local `.env` file or a secure secret manager.

The `.env` file must never be committed to GitHub.

Use `.env.example` only to document expected environment variables.

## Final quote safety rule

Every AI-generated quote is a draft.

It must be reviewed and validated by a human before being sent to a customer.
