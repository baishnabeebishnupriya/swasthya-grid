from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ResourceTransferBase(BaseModel):
    source_phc_id: UUID
    destination_phc_id: UUID
    resource_type: str = Field(..., pattern="^(medicine|equipment|staff|other)$")
    medicine_id: Optional[UUID] = None
    quantity: int = Field(..., gt=0)
    status: str = Field(default="recommended", pattern="^(recommended|pending_approval|approved|in_transit|completed|cancelled)$")
    distance_km: Optional[float] = Field(default=None, ge=0.0)
    estimated_arrival_minutes: Optional[int] = Field(default=None, ge=0)
    reason: str
    approved_by: Optional[str] = None


class ResourceTransferCreate(BaseModel):
    source_phc_id: UUID
    destination_phc_id: UUID
    resource_type: str = Field(..., pattern="^(medicine|equipment|staff|other)$")
    medicine_id: Optional[UUID] = None
    quantity: int = Field(..., gt=0)
    distance_km: Optional[float] = Field(default=None, ge=0.0)
    estimated_arrival_minutes: Optional[int] = Field(default=None, ge=0)
    reason: str


class ResourceTransferResponse(ResourceTransferBase):
    id: UUID
    source_phc_name: Optional[str] = None
    destination_phc_name: Optional[str] = None
    medicine_name: Optional[str] = None
    requested_at: datetime
    approved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
