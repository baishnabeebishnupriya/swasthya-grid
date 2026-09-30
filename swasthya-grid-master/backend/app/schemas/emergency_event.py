from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class EmergencyEventBase(BaseModel):
    name: str
    description: Optional[str] = None
    emergency_type: str = Field(..., pattern="^(disease_outbreak|flood|cyclone|heatwave|mass_casualty|other)$")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    affected_district_id: Optional[UUID] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: str = Field(default="active", pattern="^(active|contained|concluded)$")


class EmergencyEventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    emergency_type: str = Field(..., pattern="^(disease_outbreak|flood|cyclone|heatwave|mass_casualty|other)$")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    affected_district_id: Optional[UUID] = None
    started_at: Optional[datetime] = None


class EmergencyEventResponse(EmergencyEventBase):
    id: UUID
    district_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
