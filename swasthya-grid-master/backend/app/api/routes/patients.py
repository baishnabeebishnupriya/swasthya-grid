from uuid import UUID
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.patient_visit import PatientVisit
from app.models.phc import PHC
from app.schemas.patient_visit import PatientVisitResponse

router = APIRouter(prefix="/phcs", tags=["Patient Visits (Aggregated)"])


def _format_patient_visit_response(pv: PatientVisit) -> PatientVisitResponse:
    return PatientVisitResponse(
        id=pv.id,
        phc_id=pv.phc_id,
        visit_date=pv.visit_date,
        disease_category=pv.disease_category,
        patient_count=pv.patient_count,
        emergency_count=pv.emergency_count,
        created_at=pv.created_at,
        phc_name=pv.phc.name if pv.phc else None
    )


@router.get("/{phc_id}/patients", response_model=List[PatientVisitResponse], summary="Get aggregated patient visits for a PHC")
async def get_phc_patient_visits(
    phc_id: UUID,
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    disease_category: Optional[str] = Query(None, description="Filter by disease category"),
    db: AsyncSession = Depends(get_db)
):
    # Verify PHC
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    if not phc_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    query = select(PatientVisit).where(PatientVisit.phc_id == phc_id).options(selectinload(PatientVisit.phc))

    if start_date:
        query = query.where(PatientVisit.visit_date >= start_date)
    if end_date:
        query = query.where(PatientVisit.visit_date <= end_date)
    if disease_category:
        query = query.where(PatientVisit.disease_category == disease_category)

    query = query.order_by(PatientVisit.visit_date.desc(), PatientVisit.disease_category)
    result = await db.execute(query)
    records = result.scalars().all()
    return [_format_patient_visit_response(r) for r in records]
