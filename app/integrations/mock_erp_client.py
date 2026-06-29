from app.domain.entities import Customer, Product


class MockERPClient:
    """
    Simulated ERP/CRM client.

    In production, this class could be replaced by a real connector:
    SAP, Odoo, Cegid, Divalto, Salesforce, HubSpot, or another business API.
    """

    def list_customers(self) -> list[Customer]:
        """
        Return simulated CRM customers.
        """
        return [
            Customer(
                id="cust_001",
                name="Entreprise Martin",
                type="ETI",
                sector="Industrie",
                discount_rate=0.10,
                crm_status="prospect_chaud",
            ),
            Customer(
                id="cust_002",
                name="Cabinet Durand",
                type="PME",
                sector="Services",
                discount_rate=0.05,
                crm_status="client_existant",
            ),
            Customer(
                id="cust_003",
                name="Logistique Bernard",
                type="PME",
                sector="Transport",
                discount_rate=0.05,
                crm_status="prospect",
            ),
        ]

    def list_products(self) -> list[Product]:
        """
        Return simulated ERP products.
        """
        return [
            Product(
                id="prod_001",
                name="Agent IA Devis",
                unit_price=2000,
                billing="monthly",
                description=(
                    "Agent permettant de générer des brouillons de devis "
                    "à partir de demandes commerciales."
                ),
            ),
            Product(
                id="prod_002",
                name="Agent IA Documentaire",
                unit_price=1500,
                billing="monthly",
                description=(
                    "Agent permettant de classifier, extraire et rechercher "
                    "des informations dans des documents métier."
                ),
            ),
            Product(
                id="prod_003",
                name="Agent IA Email",
                unit_price=1200,
                billing="monthly",
                description=(
                    "Agent permettant d'analyser, classer et préparer des réponses "
                    "aux emails clients."
                ),
            ),
        ]