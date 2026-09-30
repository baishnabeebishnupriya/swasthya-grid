from uuid import UUID
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.medicine_consumption import MedicineConsumption
from app.models.phc import PHC
from app.schemas.medicine_consumption import MedicineConsumptionResponse

router = APIRouter(prefix="/phcs", tags=["Medicine Consumption (Time Series)"])


def _format_consumption_response(mc: MedicineConsumption) -> MedicineConsumptionResponse:
    return MedicineConsumptionResponse(
        id=mc.id,
        phc_id=mc.phc_id,
        medicine_id=mc.medicine_id,
        consumption_date=mc.consumption_date,
        quantity_consumed=mc.quantity_consumed,
        created_at=mc.created_at,
        medicine_name=mc.medicine.name if mc.medicine else None,
        medicine_category=mc.medicine.category if mc.medicine else None,
        unit=mc.medicine.unit if mc.medicine else None,
        phc_name=mc.phc.name if mc.phc else None
    )


@router.get("/{phc_id}/consumption", response_model=List[MedicineConsumptionResponse], summary="Get historical medicine consumption for a PHC")
async def get_phc_medicine_consumption(
    phc_id: UUID,
    medicine_id: Optional[UUID] = Query(None, description="Filter by medicine ID"),
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: AsyncSession = Depends(get_db)
):
    # Verify PHC
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    if not phc_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    query = (
        select(MedicineConsumption)
        .where(MedicineConsumption.phc_id == phc_id)
        .options(selectinload(MedicineConsumption.medicine), selectinload(MedicineConsumption.phc))
    )

    if medicine_id:
        query = query.where(MedicineConsumption.medicine_id == medicine_id)
    if start_date:
        query = query.where(MedicineConsumption.consumption_date >= start_date)
    if end_date:
        query = query.where(MedicineConsumption.consumption_date <= end_date)

    query = query.order_by(MedicineConsumption.consumption_date.desc())
    result = await db.execute(query)
    records = result.scalars().all()
    return [_format_consumption_response(r) for r in records]
