import unicodedata

from app.domain.entities import DocumentClassification


class DocumentClassifier:
    """
    Simple deterministic document classifier.

    This mock classifier is intentionally simple for the MVP.
    Later, it can be replaced by an LLM-based classifier or an embedding model.
    """

    def classify(self, filename: str, content: str) -> DocumentClassification:
        """
        Classify a business document using filename and content keywords.
        """
        text = self._normalize_text(f"{filename} {content}")

        scores = {
            "product_catalog": self._score_product_catalog(text),
            "commercial_conditions": self._score_commercial_conditions(text),
            "customer_request": self._score_customer_request(text),
        }

        best_type = max(scores, key=scores.get)
        best_score = scores[best_type]

        if best_score == 0:
            return DocumentClassification(
                document_type="unknown",
                confidence_score=0.35,
            )

        confidence_score = min(0.60 + (best_score * 0.08), 0.95)

        return DocumentClassification(
            document_type=best_type,  # type: ignore[arg-type]
            confidence_score=round(confidence_score, 2),
        )

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text to make keyword matching more reliable.
        """
        normalized = unicodedata.normalize("NFKD", text)
        without_accents = "".join(
            char for char in normalized if not unicodedata.combining(char)
        )
        return without_accents.lower()

    def _score_product_catalog(self, text: str) -> int:
        keywords = [
            "catalog",
            "catalogue",
            "produit",
            "produits",
            "prix",
            "tarif",
            "unit_price",
            "agent ia documentaire",
            "agent ia devis",
            "agent ia email",
            "abonnement",
            "mensuel",
        ]

        return self._count_keywords(text, keywords)

    def _score_commercial_conditions(self, text: str) -> int:
        keywords = [
            "conditions commerciales",
            "commercial_conditions",
            "remise",
            "discount",
            "pme",
            "eti",
            "validation humaine",
            "valide par un humain",
            "devis genere par ia",
            "avant envoi",
        ]

        return self._count_keywords(text, keywords)

    def _score_customer_request(self, text: str) -> int:
        keywords = [
            "demande client",
            "customer_request",
            "le client veut",
            "besoin",
            "souhaite",
            "automatiser",
            "generation de devis",
            "documents internes",
            "demandes commerciales",
        ]

        return self._count_keywords(text, keywords)

    def _count_keywords(self, text: str, keywords: list[str]) -> int:
        """
        Count matching keywords in the normalized text.
        """
        return sum(1 for keyword in keywords if keyword in text)