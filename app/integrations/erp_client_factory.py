from typing import Protocol

from app.core.config import get_settings
from app.domain.entities import Customer, Product
from app.integrations.http_erp_client import HttpERPClient
from app.integrations.mock_erp_client import MockERPClient


class ERPClient(Protocol):
    """
    Protocol for ERP/CRM clients.
    """

    def list_customers(self) -> list[Customer]:
        """
        Return customers from an ERP/CRM system.
        """

    def list_products(self) -> list[Product]:
        """
        Return products from an ERP/CRM system.
        """


def create_erp_client() -> ERPClient:
    """
    Create the ERP client based on application settings.
    """
    settings = get_settings()

    if settings.erp_provider == "mock":
        return MockERPClient()

    if settings.erp_provider == "http":
        return HttpERPClient()

    raise ValueError(f"Unsupported ERP provider: {settings.erp_provider}")