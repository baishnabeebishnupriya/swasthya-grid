from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class MedicineBase(BaseModel):
    name: str
    generic_name: str
    category: str
    unit: str
    minimum_stock_level: int = Field(default=100, ge=0)
    reorder_level: int = Field(default=200, ge=0)


class MedicineCreate(MedicineBase):
    pass


class MedicineResponse(MedicineBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
