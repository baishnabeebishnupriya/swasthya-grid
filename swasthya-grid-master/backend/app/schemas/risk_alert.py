from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class RiskAlertBase(BaseModel):
    phc_id: UUID
    medicine_id: Optional[UUID] = None
    alert_type: str = Field(..., pattern="^(stockout|bed_shortage|staff_shortage|demand_surge|emergency)$")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    title: str
    description: str
    risk_score: float = Field(..., ge=0.0, le=100.0)
    recommended_action: Optional[str] = None
    status: str = Field(default="open", pattern="^(open|acknowledged|resolved)$")


class RiskAlertCreate(RiskAlertBase):
    pass


class RiskAlertResponse(RiskAlertBase):
    id: UUID
    medicine_name: Optional[str] = None
    phc_name: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
