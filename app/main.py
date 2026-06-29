from fastapi import FastAPI

from app.api.v1.routes_erp import router as erp_router
from app.api.v1.routes_health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    configure_logging()
    settings = get_settings()

    app = FastAPI(
        title="AI Quote Assistant",
        description="A FastAPI prototype for an AI-powered quote generation assistant.",
        version="0.1.0",
    )

    app.include_router(
        health_router,
        prefix="/api/v1",
        tags=["health"],
    )

    app.include_router(
        erp_router,
        prefix="/api/v1",
        tags=["erp"],
    )

    return app


app = create_app()