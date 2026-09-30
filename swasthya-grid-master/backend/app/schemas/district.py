from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DistrictBase(BaseModel):
    name: str
    code: str
    state_id: UUID


class DistrictCreate(DistrictBase):
    pass


class DistrictResponse(DistrictBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
