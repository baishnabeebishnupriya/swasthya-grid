from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.district import District
from app.schemas.district import DistrictResponse

router = APIRouter(prefix="/districts", tags=["Districts"])


@router.get("", response_model=List[DistrictResponse], summary="List all districts")
async def list_districts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(District).order_by(District.name))
    return result.scalars().all()


@router.get("/{district_id}", response_model=DistrictResponse, summary="Get district by ID")
async def get_district(district_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(District).where(District.id == district_id))
    district = result.scalar_one_or_none()
    if not district:
        raise HTTPException(status_code=404, detail=f"District with id '{district_id}' not found.")
    return district
