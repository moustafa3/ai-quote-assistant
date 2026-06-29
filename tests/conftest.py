import pytest
from fastapi.testclient import TestClient

from app.infrastructure.repositories.quote_repository import InMemoryQuoteRepository
from app.main import app


@pytest.fixture(autouse=True)
def clear_quote_repository() -> None:
    """
    Clear in-memory quotes before each test.

    This keeps tests isolated and avoids one test depending on another.
    """
    InMemoryQuoteRepository().clear()


@pytest.fixture
def client() -> TestClient:
    """
    Return a FastAPI test client.
    """
    return TestClient(app)