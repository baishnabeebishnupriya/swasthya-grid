from uuid import UUID
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class InventoryBase(BaseModel):
    phc_id: UUID
    medicine_id: UUID
    quantity: int = Field(default=0, ge=0)
    reserved_quantity: int = Field(default=0, ge=0)
    daily_average_consumption: float = Field(default=0.0, ge=0.0)
    expiry_date: date
    batch_number: str
    last_restocked_at: Optional[datetime] = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, ge=0)
    reserved_quantity: Optional[int] = Field(default=None, ge=0)
    daily_average_consumption: Optional[float] = Field(default=None, ge=0.0)
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = None


class InventoryResponse(InventoryBase):
    id: UUID
    medicine_name: Optional[str] = None
    medicine_category: Optional[str] = None
    unit: Optional[str] = None
    phc_name: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
