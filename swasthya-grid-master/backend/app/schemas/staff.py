from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class StaffBase(BaseModel):
    phc_id: UUID
    employee_code: str
    name: str
    role: str = Field(..., pattern="^(doctor|nurse|pharmacist|lab_technician|administrative|other)$")
    specialization: Optional[str] = None
    employment_type: str = Field(default="permanent", pattern="^(permanent|contract|visiting|temporary)$")
    is_active: bool = True
    joined_at: date


class StaffCreate(StaffBase):
    pass


class StaffResponse(StaffBase):
    id: UUID
    phc_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
