from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineResponse

router = APIRouter(prefix="/medicines", tags=["Medicines"])


@router.get("", response_model=List[MedicineResponse], summary="List all medicines")
async def list_medicines(
    category: Optional[str] = Query(None, description="Filter by medicine category"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Medicine)
    if category:
        query = query.where(Medicine.category == category)
    query = query.order_by(Medicine.name)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{medicine_id}", response_model=MedicineResponse, summary="Get medicine by ID")
async def get_medicine(medicine_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medicine).where(Medicine.id == medicine_id))
    medicine = result.scalar_one_or_none()
    if not medicine:
        raise HTTPException(status_code=404, detail=f"Medicine with id '{medicine_id}' not found.")
    return medicine
