# Architecture

## Overview

AI Quote Assistant follows a Clean Architecture inspired structure.

The goal is to keep the codebase easy to understand, test, and extend.

The project separates:

* API routes
* application use cases
* domain entities and rules
* AI services
* infrastructure repositories
* external integrations

This makes the project easier to evolve toward production.

## Main request flow

Example: quote generation.

```text
POST /api/v1/quotes/generate
        │
        ▼
routes_quotes.py
        │
        ▼
GenerateQuoteUseCase
        │
        ├── GetERPDataUseCase
        │       └── MockERPClient
        │
        ├── QuoteAgent
        │       ├── LLMClient
        │       └── quote_rules.py
        │
        └── InMemoryQuoteRepository
```

## Layer responsibilities

### API layer

Location:

```text
app/api/v1/
```

Responsibility:

* expose HTTP endpoints
* validate request and response schemas
* call application use cases
* translate application errors into HTTP errors

Routes must stay thin. They should not contain business logic.

### Application layer

Location:

```text
app/application/use_cases/
```

Responsibility:

* orchestrate business workflows
* call domain services
* call repositories
* call integrations through clear abstractions

Examples:

* classify a document
* ask a question over documents
* generate a quote draft
* retrieve a quote
* compute dashboard KPIs

### Schema layer

Location:

```text
app/application/schemas/
```

Responsibility:

* define Pydantic request models
* define Pydantic response models
* make Swagger documentation clear

Schemas are API contracts. They should not contain business logic.

### Domain layer

Location:

```text
app/domain/
```

Responsibility:

* define business entities
* define pure business rules
* stay independent from FastAPI, databases, and external APIs

Examples:

* `Customer`
* `Product`
* `QuoteDraft`
* `QuoteItem`
* `DashboardKpis`
* quote calculation rules

### AI layer

Location:

```text
app/ai/
```

Responsibility:

* document classification
* local RAG logic
* quote agent logic
* LLM abstraction

The AI layer is isolated so the rest of the application does not depend directly on a specific LLM provider.

Current AI services:

* `DocumentClassifier`
* `RagService`
* `QuoteAgent`
* `LLMClient`

### Integration layer

Location:

```text
app/integrations/
```

Responsibility:

* simulate or connect to external business systems

Current integration:

```text
MockERPClient
```

In production, this could be replaced by connectors to:

* Odoo
* SAP
* Cegid
* Divalto
* Salesforce
* HubSpot
* custom REST APIs
* OData APIs
* SOAP APIs

### Infrastructure layer

Location:

```text
app/infrastructure/
```

Responsibility:

* persistence
* repositories
* database adapters

Current repository:

```text
InMemoryQuoteRepository
```

This is simple and useful for the MVP.

Production target:

```text
PostgreSQLQuoteRepository
```

with:

* SQLAlchemy
* Alembic migrations
* persistent quote storage
* audit logs

## Why this architecture

This architecture helps keep the project maintainable.

For example, replacing the in-memory repository with PostgreSQL should not require changing the API route.

Replacing the mock ERP client with a real ERP connector should not require changing the quote agent.

Replacing the keyword RAG with embeddings should not require changing the chat endpoint.

## Current architecture trade-offs

The project is intentionally simple.

Accepted MVP trade-offs:

* in-memory quote storage
* mocked ERP/CRM data
* deterministic mock LLM mode
* keyword-based RAG
* no authentication yet

These choices make the project fast to run, easy to test, and demo-ready.

## Future production architecture

Recommended production improvements:

```text
FastAPI
  ├── Auth / RBAC
  ├── Application use cases
  ├── PostgreSQL + SQLAlchemy
  ├── pgvector semantic search
  ├── real ERP/CRM connectors
  ├── OpenAI or private LLM provider
  ├── audit logging
  ├── monitoring
  └── human approval workflow
```

## Human validation rule

The quote generation feature must always require human validation.

The AI can prepare a quote draft, but it must not send or validate the quote automatically.

This is an important safety and business control rule.
