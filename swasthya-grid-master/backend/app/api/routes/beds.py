from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.bed import Bed
from app.models.phc import PHC
from app.schemas.bed import BedResponse, BedUpdate

router = APIRouter(prefix="/phcs", tags=["Beds"])


@router.get("/{phc_id}/beds", response_model=BedResponse, summary="Get bed availability for a PHC")
async def get_phc_beds(phc_id: UUID, db: AsyncSession = Depends(get_db)):
    # Check PHC
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    phc = phc_check.scalar_one_or_none()
    if not phc:
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    result = await db.execute(select(Bed).where(Bed.phc_id == phc_id))
    bed = result.scalar_one_or_none()
    
    if not bed:
        # Create initial bed record if missing
        bed = Bed(
            phc_id=phc_id,
            total_beds=phc.total_beds,
            occupied_beds=0,
            reserved_beds=0,
            available_beds=phc.total_beds
        )
        db.add(bed)
        await db.commit()
        await db.refresh(bed)

    return bed


@router.put("/{phc_id}/beds", response_model=BedResponse, summary="Update bed capacity and occupancy")
async def update_phc_beds(
    phc_id: UUID,
    payload: BedUpdate,
    db: AsyncSession = Depends(get_db)
):
    # Verify bed record exists
    result = await db.execute(select(Bed).where(Bed.phc_id == phc_id))
    bed = result.scalar_one_or_none()
    if not bed:
        # Check if PHC exists
        phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
        phc = phc_check.scalar_one_or_none()
        if not phc:
            raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")
        bed = Bed(phc_id=phc_id)
        db.add(bed)

    # Validation: occupied + reserved <= total
    if payload.occupied_beds + payload.reserved_beds > payload.total_beds:
        raise HTTPException(
            status_code=400,
            detail=f"Occupied beds ({payload.occupied_beds}) + Reserved beds ({payload.reserved_beds}) exceeds Total beds ({payload.total_beds})."
        )

    bed.total_beds = payload.total_beds
    bed.occupied_beds = payload.occupied_beds
    bed.reserved_beds = payload.reserved_beds
    bed.available_beds = payload.total_beds - (payload.occupied_beds + payload.reserved_beds)
    bed.updated_at = datetime.utcnow()

    # Also update total_beds in PHC table
    phc_result = await db.execute(select(PHC).where(PHC.id == phc_id))
    phc = phc_result.scalar_one_or_none()
    if phc:
        phc.total_beds = payload.total_beds
        phc.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(bed)
    return bed
