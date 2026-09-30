from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.inventory import Inventory
from app.models.phc import PHC
from app.models.medicine import Medicine
from app.schemas.inventory import InventoryResponse

router = APIRouter(tags=["Inventory"])


def _format_inventory_response(inv: Inventory) -> InventoryResponse:
    return InventoryResponse(
        id=inv.id,
        phc_id=inv.phc_id,
        medicine_id=inv.medicine_id,
        quantity=inv.quantity,
        reserved_quantity=inv.reserved_quantity,
        daily_average_consumption=float(inv.daily_average_consumption),
        expiry_date=inv.expiry_date,
        batch_number=inv.batch_number,
        last_restocked_at=inv.last_restocked_at,
        updated_at=inv.updated_at,
        medicine_name=inv.medicine.name if inv.medicine else None,
        medicine_category=inv.medicine.category if inv.medicine else None,
        unit=inv.medicine.unit if inv.medicine else None,
        phc_name=inv.phc.name if inv.phc else None
    )


@router.get("/inventory", response_model=List[InventoryResponse], summary="List all inventory records")
async def list_inventory(
    phc_id: Optional[UUID] = Query(None, description="Filter by PHC ID"),
    medicine_id: Optional[UUID] = Query(None, description="Filter by Medicine ID"),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Inventory)
        .options(selectinload(Inventory.medicine), selectinload(Inventory.phc))
    )
    if phc_id:
        query = query.where(Inventory.phc_id == phc_id)
    if medicine_id:
        query = query.where(Inventory.medicine_id == medicine_id)

    query = query.order_by(Inventory.updated_at.desc())
    result = await db.execute(query)
    items = result.scalars().all()
    return [_format_inventory_response(i) for i in items]


@router.get("/inventory/{inventory_id}", response_model=InventoryResponse, summary="Get inventory item by ID")
async def get_inventory_item(inventory_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(Inventory)
        .where(Inventory.id == inventory_id)
        .options(selectinload(Inventory.medicine), selectinload(Inventory.phc))
    )
    result = await db.execute(query)
    inv = result.scalar_one_or_none()
    if not inv:
        raise HTTPException(status_code=404, detail=f"Inventory record with id '{inventory_id}' not found.")
    return _format_inventory_response(inv)


@router.get("/phcs/{phc_id}/inventory", response_model=List[InventoryResponse], summary="Get inventory for a specific PHC")
async def get_phc_inventory(
    phc_id: UUID,
    medicine_id: Optional[UUID] = Query(None, description="Filter by specific Medicine ID"),
    db: AsyncSession = Depends(get_db)
):
    # Verify PHC exists
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    if not phc_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    query = (
        select(Inventory)
        .where(Inventory.phc_id == phc_id)
        .options(selectinload(Inventory.medicine), selectinload(Inventory.phc))
    )
    if medicine_id:
        query = query.where(Inventory.medicine_id == medicine_id)

    query = query.order_by(Inventory.updated_at.desc())
    result = await db.execute(query)
    items = result.scalars().all()
    return [_format_inventory_response(i) for i in items]
