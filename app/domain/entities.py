from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """
    Business customer coming from the simulated CRM/ERP.
    """

    id: str
    name: str
    type: str
    sector: str
    discount_rate: float
    crm_status: str


@dataclass(frozen=True)
class Product:
    """
    Business product coming from the simulated ERP catalog.
    """

    id: str
    name: str
    unit_price: float
    billing: str
    description: str