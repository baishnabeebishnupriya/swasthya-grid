from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.staff import Staff
from app.models.phc import PHC
from app.schemas.staff import StaffResponse

router = APIRouter(tags=["Staff"])


def _format_staff_response(s: Staff) -> StaffResponse:
    return StaffResponse(
        id=s.id,
        phc_id=s.phc_id,
        employee_code=s.employee_code,
        name=s.name,
        role=s.role,
        specialization=s.specialization,
        employment_type=s.employment_type,
        is_active=s.is_active,
        joined_at=s.joined_at,
        phc_name=s.phc.name if s.phc else None
    )


@router.get("/phcs/{phc_id}/staff", response_model=List[StaffResponse], summary="Get staff for a specific PHC")
async def get_phc_staff(
    phc_id: UUID,
    role: Optional[str] = Query(None, description="Filter by staff role"),
    is_active: Optional[bool] = Query(None, description="Filter active/inactive staff"),
    db: AsyncSession = Depends(get_db)
):
    # Verify PHC
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    if not phc_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    query = select(Staff).where(Staff.phc_id == phc_id).options(selectinload(Staff.phc))
    if role:
        query = query.where(Staff.role == role)
    if is_active is not None:
        query = query.where(Staff.is_active == is_active)

    query = query.order_by(Staff.role, Staff.name)
    result = await db.execute(query)
    staff_members = result.scalars().all()
    return [_format_staff_response(s) for s in staff_members]


@router.get("/staff/{staff_id}", response_model=StaffResponse, summary="Get staff member by ID")
async def get_staff_member(staff_id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(Staff).where(Staff.id == staff_id).options(selectinload(Staff.phc))
    result = await db.execute(query)
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail=f"Staff member with id '{staff_id}' not found.")
    return _format_staff_response(s)
