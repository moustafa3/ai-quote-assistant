from app.ai.quote_agent import QuoteAgent
from app.application.use_cases.get_erp_data import GetERPDataUseCase
from app.core.exceptions import ResourceNotFoundError
from app.domain.entities import Customer, Product, QuoteDraft


class GenerateQuoteUseCase:
    """
    Application use case for generating AI quote drafts.
    """

    def __init__(
        self,
        erp_use_case: GetERPDataUseCase | None = None,
        quote_agent: QuoteAgent | None = None,
    ) -> None:
        self.erp_use_case = erp_use_case or GetERPDataUseCase()
        self.quote_agent = quote_agent or QuoteAgent()

    def execute(self, customer_id: str, request: str) -> QuoteDraft:
        """
        Generate a quote draft for a customer request.
        """
        customers = self.erp_use_case.get_customers()
        products = self.erp_use_case.get_products()

        customer = self._find_customer(
            customers=customers,
            customer_id=customer_id,
        )

        return self.quote_agent.generate(
            customer=customer,
            products=products,
            request=request,
        )

    def _find_customer(
        self,
        customers: list[Customer],
        customer_id: str,
    ) -> Customer:
        """
        Find a customer by ID.
        """
        for customer in customers:
            if customer.id == customer_id:
                return customer

        raise ResourceNotFoundError(
            f"Customer with id '{customer_id}' was not found."
        )