import unicodedata

from app.ai.llm_client import LLMClient
from app.domain.entities import Customer, Product, QuoteDraft, QuoteItem
from app.domain.quote_rules import (
    calculate_discount_amount,
    calculate_subtotal,
    calculate_total,
)


class QuoteAgent:
    """
    AI quote generation agent.

    It recommends a product, calculates a draft quote and adds mandatory
    human validation information.
    """

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()

    def generate(
        self,
        quote_id: str,
        customer: Customer,
        products: list[Product],
        request: str,
    ) -> QuoteDraft:
        """
        Generate a quote draft from customer data, product catalog and request.
        """
        product = self._recommend_product(request=request, products=products)

        item = QuoteItem(
            name=product.name,
            quantity=1,
            unit_price=product.unit_price,
            total=product.unit_price,
        )

        subtotal = calculate_subtotal([item])
        discount_amount = calculate_discount_amount(
            subtotal=subtotal,
            discount_rate=customer.discount_rate,
        )
        total = calculate_total(
            subtotal=subtotal,
            discount_amount=discount_amount,
        )

        llm_support = self.llm_client.generate_quote_support(
            customer_type=customer.type,
            product_name=product.name,
            request=request,
        )

        return QuoteDraft(
            quote_id=quote_id,
            customer_name=customer.name,
            recommended_solution=product.name,
            items=[item],
            subtotal=subtotal,
            discount_rate=customer.discount_rate,
            discount_amount=discount_amount,
            total=total,
            sources=[
                "sample_catalog.txt",
                "commercial_conditions.txt",
            ],
            assumptions=llm_support["assumptions"],
            validation_points=llm_support["validation_points"],
            human_validation_required=True,
            confidence_score=round(float(llm_support["confidence_score"]), 2),
        )

    def _recommend_product(
        self,
        request: str,
        products: list[Product],
    ) -> Product:
        """
        Recommend the best product based on the customer request.
        """
        normalized_request = self._normalize_text(request)

        if self._contains_any(
            normalized_request,
            ["devis", "commercial", "commerciales", "quote"],
        ):
            return self._find_product_by_name(products, "Agent IA Devis")

        if self._contains_any(
            normalized_request,
            ["document", "documents", "rag", "classification", "extraction"],
        ):
            return self._find_product_by_name(products, "Agent IA Documentaire")

        if self._contains_any(
            normalized_request,
            ["email", "emails", "mail", "inbox"],
        ):
            return self._find_product_by_name(products, "Agent IA Email")

        return self._find_product_by_name(products, "Agent IA Devis")

    def _find_product_by_name(
        self,
        products: list[Product],
        product_name: str,
    ) -> Product:
        """
        Find a product by name or fallback to the first product.
        """
        for product in products:
            if product.name == product_name:
                return product

        if not products:
            raise ValueError("No products available to generate a quote.")

        return products[0]

    def _contains_any(self, text: str, keywords: list[str]) -> bool:
        """
        Return True if the text contains at least one keyword.
        """
        return any(keyword in text for keyword in keywords)

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text by removing accents and lowering case.
        """
        normalized = unicodedata.normalize("NFKD", text)
        without_accents = "".join(
            char for char in normalized if not unicodedata.combining(char)
        )
        return without_accents.lower()