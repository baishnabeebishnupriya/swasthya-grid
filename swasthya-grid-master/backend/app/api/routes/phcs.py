from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.phc import PHC
from app.models.district import District
from app.models.state import State
from app.models.bed import Bed
from app.schemas.phc import PHCResponse

router = APIRouter(prefix="/phcs", tags=["Primary Health Centres (PHCs)"])


def _format_phc_response(phc: PHC) -> PHCResponse:
    district_name = phc.district.name if phc.district else None
    state_id = phc.district.state_id if phc.district else None
    state_name = phc.district.state.name if phc.district and phc.district.state else None
    available_beds = phc.beds.available_beds if phc.beds else max(0, phc.total_beds)

    return PHCResponse(
        id=phc.id,
        name=phc.name,
        code=phc.code,
        district_id=phc.district_id,
        address=phc.address,
        latitude=float(phc.latitude),
        longitude=float(phc.longitude),
        total_beds=phc.total_beds,
        active_doctors=phc.active_doctors,
        active_nurses=phc.active_nurses,
        status=phc.status,
        available_beds=available_beds,
        district_name=district_name,
        state_id=state_id,
        state_name=state_name,
        created_at=phc.created_at,
        updated_at=phc.updated_at
    )


@router.get("", response_model=List[PHCResponse], summary="List all PHCs with optional filtering")
async def list_phcs(
    state_id: Optional[UUID] = Query(None, description="Filter by State ID"),
    district_id: Optional[UUID] = Query(None, description="Filter by District ID"),
    status: Optional[str] = Query(None, pattern="^(healthy|at_risk|critical)$", description="Filter by PHC Status"),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(PHC)
        .join(District, PHC.district_id == District.id)
        .join(State, District.state_id == State.id)
        .options(
            selectinload(PHC.district).selectinload(District.state),
            selectinload(PHC.beds)
        )
    )

    if state_id:
        query = query.where(District.state_id == state_id)
    if district_id:
        query = query.where(PHC.district_id == district_id)
    if status:
        query = query.where(PHC.status == status)

    query = query.order_by(PHC.name)
    result = await db.execute(query)
    phcs = result.scalars().all()
    return [_format_phc_response(p) for p in phcs]


@router.get("/{phc_id}", response_model=PHCResponse, summary="Get PHC by ID")
async def get_phc(phc_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(PHC)
        .where(PHC.id == phc_id)
        .options(
            selectinload(PHC.district).selectinload(District.state),
            selectinload(PHC.beds)
        )
    )
    result = await db.execute(query)
    phc = result.scalar_one_or_none()
    if not phc:
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")
    return _format_phc_response(phc)
