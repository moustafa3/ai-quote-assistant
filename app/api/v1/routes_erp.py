from fastapi import APIRouter

from app.application.schemas.erp_schema import CustomerResponse, ProductResponse
from app.application.use_cases.get_erp_data import GetERPDataUseCase

router = APIRouter()


@router.get("/erp/customers", response_model=list[CustomerResponse])
def list_customers() -> list[CustomerResponse]:
    """
    Return simulated CRM customers.
    """
    use_case = GetERPDataUseCase()
    customers = use_case.get_customers()

    return [
        CustomerResponse(
            id=customer.id,
            name=customer.name,
            type=customer.type,
            sector=customer.sector,
            discount_rate=customer.discount_rate,
            crm_status=customer.crm_status,
        )
        for customer in customers
    ]


@router.get("/erp/products", response_model=list[ProductResponse])
def list_products() -> list[ProductResponse]:
    """
    Return simulated ERP products.
    """
    use_case = GetERPDataUseCase()
    products = use_case.get_products()

    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            unit_price=product.unit_price,
            billing=product.billing,
            description=product.description,
        )
        for product in products
    ]