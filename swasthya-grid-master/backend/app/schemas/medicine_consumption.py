from uuid import UUID
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MedicineConsumptionBase(BaseModel):
    phc_id: UUID
    medicine_id: UUID
    consumption_date: date
    quantity_consumed: int = Field(default=0, ge=0)


class MedicineConsumptionCreate(MedicineConsumptionBase):
    pass


class MedicineConsumptionResponse(MedicineConsumptionBase):
    id: UUID
    medicine_name: Optional[str] = None
    medicine_category: Optional[str] = None
    unit: Optional[str] = None
    phc_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
