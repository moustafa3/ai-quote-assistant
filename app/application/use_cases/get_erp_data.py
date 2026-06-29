from app.domain.entities import Customer, Product
from app.integrations.erp_client_factory import ERPClient, create_erp_client


class GetERPDataUseCase:
    """
    Application use case for reading ERP/CRM data.
    """

    def __init__(self, erp_client: ERPClient | None = None) -> None:
        self.erp_client = erp_client or create_erp_client()

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