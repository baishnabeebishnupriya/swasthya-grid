from uuid import UUID
from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AttendanceBase(BaseModel):
    staff_id: UUID
    attendance_date: date
    status: str = Field(default="present", pattern="^(present|absent|leave|on_duty)$")
    check_in: Optional[time] = None
    check_out: Optional[time] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    id: UUID
    staff_name: Optional[str] = None
    staff_role: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
