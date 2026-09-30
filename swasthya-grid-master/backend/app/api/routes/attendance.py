from uuid import UUID
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.attendance import Attendance
from app.models.staff import Staff
from app.models.phc import PHC
from app.schemas.attendance import AttendanceResponse

router = APIRouter(prefix="/phcs", tags=["Attendance"])


def _format_attendance_response(att: Attendance) -> AttendanceResponse:
    return AttendanceResponse(
        id=att.id,
        staff_id=att.staff_id,
        attendance_date=att.attendance_date,
        status=att.status,
        check_in=att.check_in,
        check_out=att.check_out,
        created_at=att.created_at,
        staff_name=att.staff_member.name if att.staff_member else None,
        staff_role=att.staff_member.role if att.staff_member else None
    )


@router.get("/{phc_id}/attendance", response_model=List[AttendanceResponse], summary="Get attendance records for a PHC")
async def get_phc_attendance(
    phc_id: UUID,
    attendance_date: Optional[date] = Query(None, description="Exact attendance date"),
    start_date: Optional[date] = Query(None, description="Start date range"),
    end_date: Optional[date] = Query(None, description="End date range"),
    status: Optional[str] = Query(None, pattern="^(present|absent|leave|on_duty)$", description="Filter by status"),
    db: AsyncSession = Depends(get_db)
):
    # Verify PHC
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    if not phc_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    query = (
        select(Attendance)
        .join(Staff, Attendance.staff_id == Staff.id)
        .where(Staff.phc_id == phc_id)
        .options(selectinload(Attendance.staff_member))
    )

    if attendance_date:
        query = query.where(Attendance.attendance_date == attendance_date)
    else:
        if start_date:
            query = query.where(Attendance.attendance_date >= start_date)
        if end_date:
            query = query.where(Attendance.attendance_date <= end_date)

    if status:
        query = query.where(Attendance.status == status)

    query = query.order_by(Attendance.attendance_date.desc(), Attendance.created_at.desc())
    result = await db.execute(query)
    records = result.scalars().all()
    return [_format_attendance_response(r) for r in records]
