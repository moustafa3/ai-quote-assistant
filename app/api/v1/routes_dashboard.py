from fastapi import APIRouter

from app.application.schemas.dashboard_schema import DashboardKpisResponse
from app.application.use_cases.get_dashboard_kpis import GetDashboardKpisUseCase

router = APIRouter()


@router.get(
    "/dashboard/kpis",
    response_model=DashboardKpisResponse,
)
def get_dashboard_kpis() -> DashboardKpisResponse:
    """
    Return simple business KPIs for the AI quote assistant.
    """
    use_case = GetDashboardKpisUseCase()
    kpis = use_case.execute()

    return DashboardKpisResponse(
        active_agents=kpis.active_agents,
        quotes_generated=kpis.quotes_generated,
        average_confidence_score=kpis.average_confidence_score,
        human_validation_rate=kpis.human_validation_rate,
        estimated_time_saved_minutes=kpis.estimated_time_saved_minutes,
    )