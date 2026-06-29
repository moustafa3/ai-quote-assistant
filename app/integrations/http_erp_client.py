import logging
import re
from typing import Any

import httpx

from app.core.config import get_settings
from app.domain.entities import Customer, Product

logger = logging.getLogger(__name__)


class HttpERPClient:
    """
    HTTP client for a simulated external ERP/CRM API.

    This client demonstrates realistic API integration concerns:
    authentication headers, timeouts, dirty data normalization and error handling.
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        settings = get_settings()

        self.base_url = (base_url or settings.erp_api_base_url).rstrip("/")
        self.api_key = api_key or settings.erp_api_key
        self.timeout_seconds = timeout_seconds or settings.erp_timeout_seconds

    def list_customers(self) -> list[Customer]:
        """
        Fetch and normalize customers from the external ERP API.
        """
        raw_customers = self._get("/external-api/v1/customers")
        return [self._normalize_customer(raw_customer) for raw_customer in raw_customers]

    def list_products(self) -> list[Product]:
        """
        Fetch and normalize products from the external ERP API.
        """
        raw_products = self._get("/external-api/v1/products")
        return [self._normalize_product(raw_product) for raw_product in raw_products]

    def _get(self, path: str) -> list[dict[str, Any]]:
        """
        Execute an authenticated GET request against the ERP API.
        """
        url = f"{self.base_url}{path}"

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.get(
                    url,
                    headers={"X-API-Key": self.api_key},
                )
                response.raise_for_status()
                payload = response.json()

                if not isinstance(payload, list):
                    raise ValueError("ERP API response must be a list.")

                return payload

        except httpx.HTTPError as error:
            logger.exception("ERP API request failed: %s", url)
            raise RuntimeError(f"ERP API request failed: {url}") from error

    def _normalize_customer(self, raw_customer: dict[str, Any]) -> Customer:
        """
        Convert dirty ERP customer data into a clean domain Customer.
        """
        return Customer(
            id=self._normalize_id(raw_customer.get("customerId", "")),
            name=str(raw_customer.get("companyName", "")).strip(),
            type=str(raw_customer.get("customerCategory", "unknown")).strip().upper(),
            sector=str(raw_customer.get("industrySector", "Unknown")).strip(),
            discount_rate=self._parse_discount_rate(
                raw_customer.get("discountPercent", 0)
            ),
            crm_status=self._normalize_crm_status(raw_customer.get("crmStatus", "")),
        )

    def _normalize_product(self, raw_product: dict[str, Any]) -> Product:
        """
        Convert dirty ERP product data into a clean domain Product.
        """
        return Product(
            id=self._normalize_id(raw_product.get("sku", "")),
            name=str(raw_product.get("label", "")).strip(),
            unit_price=self._parse_price(raw_product.get("priceMonthly", 0)),
            billing=str(raw_product.get("billingMode", "monthly")).strip().lower(),
            description=str(raw_product.get("details", "")).strip(),
        )

    def _normalize_id(self, value: Any) -> str:
        """
        Normalize external IDs to the internal lowercase format.
        """
        return str(value).strip().lower()

    def _parse_discount_rate(self, value: Any) -> float:
        """
        Parse discount values like '10%', '5 %' or 5 into decimal rates.
        """
        if isinstance(value, int | float):
            return round(float(value) / 100, 2)

        raw_value = str(value)
        match = re.search(r"\d+(\.\d+)?", raw_value)

        if not match:
            return 0.0

        return round(float(match.group()) / 100, 2)

    def _parse_price(self, value: Any) -> float:
        """
        Parse price values like '2000 EUR', '1500' or 1200.
        """
        if isinstance(value, int | float):
            return float(value)

        raw_value = str(value).replace(",", ".")
        match = re.search(r"\d+(\.\d+)?", raw_value)

        if not match:
            return 0.0

        return float(match.group())

    def _normalize_crm_status(self, value: Any) -> str:
        """
        Normalize external CRM statuses to internal values.
        """
        raw_status = str(value).strip().lower()

        mapping = {
            "hot_lead": "prospect_chaud",
            "existing_customer": "client_existant",
            "prospect": "prospect",
        }

        return mapping.get(raw_status, raw_status)