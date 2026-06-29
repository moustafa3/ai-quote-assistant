from pydantic import BaseModel, Field


class DashboardKpisResponse(BaseModel):
    """
    API response model for dashboard KPIs.
    """

    active_agents: int = Field(..., examples=[1])
    quotes_generated: int = Field(..., examples=[12])
    average_confidence_score: float = Field(..., ge=0, le=1, examples=[0.86])
    human_validation_rate: float = Field(..., ge=0, le=100, examples=[100])
    estimated_time_saved_minutes: int = Field(..., examples=[240])