from uuid import UUID
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class PatientVisitBase(BaseModel):
    phc_id: UUID
    visit_date: date
    disease_category: str = Field(
        ...,
        pattern="^(general|fever|dengue|malaria|respiratory|diarrhea|dehydration|injury|other)$"
    )
    patient_count: int = Field(default=0, ge=0)
    emergency_count: int = Field(default=0, ge=0)


class PatientVisitCreate(PatientVisitBase):
    pass


class PatientVisitResponse(PatientVisitBase):
    id: UUID
    phc_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
