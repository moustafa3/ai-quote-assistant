from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """
    Check if the API is running correctly.
    """
    settings = get_settings()

    return {
        "status": "ok",
        "service": settings.app_name,
    }