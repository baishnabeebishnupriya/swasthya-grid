from uuid import UUID
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ForecastBase(BaseModel):
    phc_id: UUID
    medicine_id: UUID
    forecast_date: date
    predicted_demand: float = Field(..., ge=0.0)
    lower_bound: float = Field(..., ge=0.0)
    upper_bound: float = Field(..., ge=0.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    model_version: str


class ForecastCreate(ForecastBase):
    pass


class ForecastResponse(ForecastBase):
    id: UUID
    medicine_name: Optional[str] = None
    phc_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
