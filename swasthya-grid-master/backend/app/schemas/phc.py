from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class PHCBase(BaseModel):
    name: str
    code: str
    district_id: UUID
    address: Optional[str] = None
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    total_beds: int = Field(default=0, ge=0)
    active_doctors: int = Field(default=0, ge=0)
    active_nurses: int = Field(default=0, ge=0)
    status: str = Field(default="healthy", pattern="^(healthy|at_risk|critical)$")


class PHCCreate(PHCBase):
    pass


class PHCUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    total_beds: Optional[int] = Field(default=None, ge=0)
    active_doctors: Optional[int] = Field(default=None, ge=0)
    active_nurses: Optional[int] = Field(default=None, ge=0)
    status: Optional[str] = Field(default=None, pattern="^(healthy|at_risk|critical)$")


class PHCResponse(PHCBase):
    id: UUID
    available_beds: Optional[int] = None
    district_name: Optional[str] = None
    state_id: Optional[UUID] = None
    state_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
