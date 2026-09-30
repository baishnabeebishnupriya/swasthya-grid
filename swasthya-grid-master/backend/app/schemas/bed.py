from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator


class BedBase(BaseModel):
    phc_id: UUID
    total_beds: int = Field(default=0, ge=0)
    occupied_beds: int = Field(default=0, ge=0)
    reserved_beds: int = Field(default=0, ge=0)
    available_beds: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_bed_capacities(self):
        if self.occupied_beds + self.reserved_beds > self.total_beds:
            raise ValueError("The sum of occupied_beds and reserved_beds cannot exceed total_beds.")
        calculated_avail = self.total_beds - (self.occupied_beds + self.reserved_beds)
        if self.available_beds != calculated_avail:
            self.available_beds = calculated_avail
        return self


class BedUpdate(BaseModel):
    total_beds: int = Field(..., ge=0)
    occupied_beds: int = Field(..., ge=0)
    reserved_beds: int = Field(..., ge=0)

    @model_validator(mode="after")
    def validate_occupancy(self):
        if self.occupied_beds + self.reserved_beds > self.total_beds:
            raise ValueError(
                f"Occupied beds ({self.occupied_beds}) + Reserved beds ({self.reserved_beds}) "
                f"exceeds Total beds ({self.total_beds})."
            )
        return self


class BedResponse(BedBase):
    id: UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
