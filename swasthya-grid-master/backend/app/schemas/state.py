from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StateBase(BaseModel):
    name: str
    code: str


class StateCreate(StateBase):
    pass


class StateResponse(StateBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
