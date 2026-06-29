import json
from typing import Any

from app.core.config import get_settings


class LLMClient:
    """
    LLM client abstraction.

    The default mock mode is deterministic and works without any API key.
    The OpenAI mode is isolated here so the rest of the application does not
    depend directly on the OpenAI SDK.
    """

    def generate_quote_support(
        self,
        customer_type: str,
        product_name: str,
        request: str,
    ) -> dict[str, Any]:
        """
        Generate quote assumptions, validation points and confidence score.
        """
        settings = get_settings()

        if settings.llm_provider == "mock":
            return self._mock_quote_support()

        if settings.llm_provider == "openai":
            return self._openai_quote_support(
                customer_type=customer_type,
                product_name=product_name,
                request=request,
            )

        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")

    def _mock_quote_support(self) -> dict[str, Any]:
        """
        Return deterministic quote support for demos and tests.
        """
        return {
            "assumptions": [
                "Le devis est basé sur un abonnement mensuel.",
                "Le volume exact de demandes commerciales doit être confirmé.",
            ],
            "validation_points": [
                "Valider la remise commerciale.",
                "Confirmer le périmètre fonctionnel.",
                "Vérifier les conditions contractuelles.",
            ],
            "confidence_score": 0.86,
        }

    def _openai_quote_support(
        self,
        customer_type: str,
        product_name: str,
        request: str,
    ) -> dict[str, Any]:
        """
        Generate quote support using OpenAI.

        This path is optional. The project works without it in mock mode.
        """
        settings = get_settings()

        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
            )

        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)

        prompt = f"""
You are a business AI quote assistant.

Return only valid JSON with this exact structure:
{{
  "assumptions": ["..."],
  "validation_points": ["..."],
  "confidence_score": 0.86
}}

Context:
- Customer type: {customer_type}
- Recommended product: {product_name}
- Customer request: {request}

Rules:
- The quote is only a draft.
- Human validation is mandatory before sending.
- Keep assumptions and validation points short.
"""

        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
        )

        raw_text = getattr(response, "output_text", "")
        return self._parse_openai_response(raw_text)

    def _parse_openai_response(self, raw_text: str) -> dict[str, Any]:
        """
        Parse OpenAI JSON output and fallback to mock values if parsing fails.
        """
        try:
            parsed = json.loads(raw_text)

            return {
                "assumptions": parsed.get("assumptions", []),
                "validation_points": parsed.get("validation_points", []),
                "confidence_score": float(parsed.get("confidence_score", 0.75)),
            }
        except json.JSONDecodeError:
            return self._mock_quote_support()