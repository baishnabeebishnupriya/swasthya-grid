from uuid import UUID
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.resource_transfer import ResourceTransfer
from app.models.phc import PHC
from app.models.medicine import Medicine
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.resource_transfer import (
    ResourceTransferResponse,
    ResourceTransferCreate
)
from app.api.deps import get_current_user, require_roles

router = APIRouter(prefix="/transfers", tags=["Resource Transfers"])


def _format_transfer_response(t: ResourceTransfer) -> ResourceTransferResponse:
    return ResourceTransferResponse(
        id=t.id,
        source_phc_id=t.source_phc_id,
        destination_phc_id=t.destination_phc_id,
        resource_type=t.resource_type,
        medicine_id=t.medicine_id,
        quantity=t.quantity,
        status=t.status,
        distance_km=float(t.distance_km) if t.distance_km is not None else None,
        estimated_arrival_minutes=t.estimated_arrival_minutes,
        reason=t.reason,
        approved_by=t.approved_by,
        requested_at=t.requested_at,
        approved_at=t.approved_at,
        completed_at=t.completed_at,
        source_phc_name=t.source_phc.name if t.source_phc else None,
        destination_phc_name=t.destination_phc.name if t.destination_phc else None,
        medicine_name=t.medicine.name if t.medicine else None
    )


@router.get("", response_model=List[ResourceTransferResponse], summary="List all resource transfers")
async def list_transfers(
    status: Optional[str] = Query(None, pattern="^(recommended|pending_approval|approved|in_transit|completed|cancelled)$"),
    source_phc_id: Optional[UUID] = Query(None),
    destination_phc_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(ResourceTransfer)
        .options(
            selectinload(ResourceTransfer.source_phc),
            selectinload(ResourceTransfer.destination_phc),
            selectinload(ResourceTransfer.medicine)
        )
    )

    if status:
        query = query.where(ResourceTransfer.status == status)
    if source_phc_id:
        query = query.where(ResourceTransfer.source_phc_id == source_phc_id)
    if destination_phc_id:
        query = query.where(ResourceTransfer.destination_phc_id == destination_phc_id)

    query = query.order_by(ResourceTransfer.requested_at.desc())
    result = await db.execute(query)
    transfers = result.scalars().all()
    return [_format_transfer_response(t) for t in transfers]


@router.get("/{transfer_id}", response_model=ResourceTransferResponse, summary="Get transfer by ID")
async def get_transfer(transfer_id: UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(ResourceTransfer)
        .where(ResourceTransfer.id == transfer_id)
        .options(
            selectinload(ResourceTransfer.source_phc),
            selectinload(ResourceTransfer.destination_phc),
            selectinload(ResourceTransfer.medicine)
        )
    )
    result = await db.execute(query)
    transfer = result.scalar_one_or_none()
    if not transfer:
        raise HTTPException(status_code=404, detail=f"Transfer record with id '{transfer_id}' not found.")
    return _format_transfer_response(transfer)


@router.post("", response_model=ResourceTransferResponse, status_code=status.HTTP_201_CREATED, summary="Create a transfer recommendation record")
async def create_transfer_recommendation(
    payload: ResourceTransferCreate,
    db: AsyncSession = Depends(get_db)
):
    if payload.source_phc_id == payload.destination_phc_id:
        raise HTTPException(status_code=400, detail="Source PHC and Destination PHC must be distinct.")

    src = await db.execute(select(PHC).where(PHC.id == payload.source_phc_id))
    if not src.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"Source PHC '{payload.source_phc_id}' not found.")

    dst = await db.execute(select(PHC).where(PHC.id == payload.destination_phc_id))
    if not dst.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"Destination PHC '{payload.destination_phc_id}' not found.")

    if payload.medicine_id:
        med = await db.execute(select(Medicine).where(Medicine.id == payload.medicine_id))
        if not med.scalar_one_or_none():
            raise HTTPException(status_code=404, detail=f"Medicine '{payload.medicine_id}' not found.")

    transfer = ResourceTransfer(
        source_phc_id=payload.source_phc_id,
        destination_phc_id=payload.destination_phc_id,
        resource_type=payload.resource_type,
        medicine_id=payload.medicine_id,
        quantity=payload.quantity,
        distance_km=payload.distance_km,
        estimated_arrival_minutes=payload.estimated_arrival_minutes,
        reason=payload.reason,
        status="recommended",
        requested_at=datetime.now(timezone.utc)
    )

    db.add(transfer)
    await db.commit()
    await db.refresh(transfer)

    return await get_transfer(transfer.id, db)


@router.put("/{transfer_id}/approve", response_model=ResourceTransferResponse, summary="Authorize/Approve Resource Transfer")
async def approve_transfer(
    transfer_id: UUID,
    current_user: User = Depends(require_roles(["STATE_ADMIN", "DISTRICT_OFFICER"])),
    db: AsyncSession = Depends(get_db)
):
    """
    Authorizes an AI-recommended or requested resource transfer.
    Restricted to STATE_ADMIN or DISTRICT_OFFICER with jurisdictional authority.
    """
    query = (
        select(ResourceTransfer)
        .where(ResourceTransfer.id == transfer_id)
        .options(
            selectinload(ResourceTransfer.source_phc),
            selectinload(ResourceTransfer.destination_phc),
            selectinload(ResourceTransfer.medicine)
        )
    )
    result = await db.execute(query)
    transfer = result.scalar_one_or_none()
    if not transfer:
        raise HTTPException(status_code=404, detail=f"Transfer '{transfer_id}' not found.")

    # Validate jurisdictional authority
    if current_user.role == "DISTRICT_OFFICER":
        src_dist = transfer.source_phc.district_id if transfer.source_phc else None
        dst_dist = transfer.destination_phc.district_id if transfer.destination_phc else None
        if current_user.district_id not in [src_dist, dst_dist]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authority violation: District Officer can only authorize transfers involving facilities within their district."
            )

    transfer.status = "approved"
    transfer.approved_at = datetime.now(timezone.utc)
    transfer.approved_by = f"{current_user.name} ({current_user.role})"

    # Log to audit trail
    audit = AuditLog(
        actor_type=current_user.role,
        actor_id=str(current_user.id),
        action="TRANSFER_APPROVED",
        entity_type="resource_transfers",
        entity_id=str(transfer.id),
        meta_data={
            "source_phc": str(transfer.source_phc_id),
            "dest_phc": str(transfer.destination_phc_id),
            "quantity": transfer.quantity,
            "approved_by": transfer.approved_by
        }
    )
    db.add(audit)
    await db.commit()
    await db.refresh(transfer)

    return _format_transfer_response(transfer)


@router.put("/{transfer_id}/reject", response_model=ResourceTransferResponse, summary="Reject Resource Transfer")
async def reject_transfer(
    transfer_id: UUID,
    current_user: User = Depends(require_roles(["STATE_ADMIN", "DISTRICT_OFFICER"])),
    db: AsyncSession = Depends(get_db)
):
    """
    Rejects or cancels a recommended transfer.
    """
    query = (
        select(ResourceTransfer)
        .where(ResourceTransfer.id == transfer_id)
        .options(
            selectinload(ResourceTransfer.source_phc),
            selectinload(ResourceTransfer.destination_phc),
            selectinload(ResourceTransfer.medicine)
        )
    )
    result = await db.execute(query)
    transfer = result.scalar_one_or_none()
    if not transfer:
        raise HTTPException(status_code=404, detail=f"Transfer '{transfer_id}' not found.")

    transfer.status = "cancelled"

    audit = AuditLog(
        actor_type=current_user.role,
        actor_id=str(current_user.id),
        action="TRANSFER_REJECTED",
        entity_type="resource_transfers",
        entity_id=str(transfer.id),
        meta_data={"cancelled_by": current_user.name}
    )
    db.add(audit)
    await db.commit()
    await db.refresh(transfer)

    return _format_transfer_response(transfer)
