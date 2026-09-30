from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserRole(str, Enum):
    STATE_ADMIN = "STATE_ADMIN"
    DISTRICT_OFFICER = "DISTRICT_OFFICER"
    PHC_ADMIN = "PHC_ADMIN"


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole
    state_id: Optional[UUID] = None
    district_id: Optional[UUID] = None
    phc_id: Optional[UUID] = None

    @model_validator(mode="after")
    def validate_scope_hierarchy(self):
        if self.role == UserRole.STATE_ADMIN and not self.state_id:
            raise ValueError("state_id is mandatory for STATE_ADMIN role.")
        if self.role == UserRole.DISTRICT_OFFICER and not self.district_id:
            raise ValueError("district_id is mandatory for DISTRICT_OFFICER role.")
        if self.role == UserRole.PHC_ADMIN and not self.phc_id:
            raise ValueError("phc_id is mandatory for PHC_ADMIN role.")
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenRefresh(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: str
    state_id: Optional[UUID] = None
    district_id: Optional[UUID] = None
    phc_id: Optional[UUID] = None
    state_name: Optional[str] = None
    district_name: Optional[str] = None
    phc_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)
