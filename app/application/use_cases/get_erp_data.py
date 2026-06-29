from app.domain.entities import Customer, Product
from app.integrations.mock_erp_client import MockERPClient


class GetERPDataUseCase:
    """
    Application use case for reading ERP/CRM data.
    """

    def __init__(self, erp_client: MockERPClient | None = None) -> None:
        self.erp_client = erp_client or MockERPClient()

    def get_customers(self) -> list[Customer]:
        """
        Get customers from the ERP/CRM integration.
        """
        return self.erp_client.list_customers()

    def get_products(self) -> list[Product]:
        """
        Get products from the ERP catalog integration.
        """
        return self.erp_client.list_products()