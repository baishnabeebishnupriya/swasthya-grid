from uuid import UUID
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.emergency_event import EmergencyEvent
from app.models.district import District
from app.schemas.emergency_event import EmergencyEventResponse, EmergencyEventCreate

router = APIRouter(prefix="/emergencies", tags=["Emergency Events"])


def _format_emergency_response(e: EmergencyEvent) -> EmergencyEventResponse:
    return EmergencyEventResponse(
        id=e.id,
        name=e.name,
        description=e.description,
        emergency_type=e.emergency_type,
        severity=e.severity,
        affected_district_id=e.affected_district_id,
        started_at=e.started_at,
        ended_at=e.ended_at,
        status=e.status,
        created_at=e.created_at,
        district_name=e.district.name if e.district else None
    )


@router.get("", response_model=List[EmergencyEventResponse], summary="List all emergency events")
async def list_emergency_events(
    status: Optional[str] = Query(None, pattern="^(active|contained|concluded)$"),
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    emergency_type: Optional[str] = Query(None, pattern="^(disease_outbreak|flood|cyclone|heatwave|mass_casualty|other)$"),
    district_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(EmergencyEvent).options(selectinload(EmergencyEvent.district))

    if status:
        query = query.where(EmergencyEvent.status == status)
    if severity:
        query = query.where(EmergencyEvent.severity == severity)
    if emergency_type:
        query = query.where(EmergencyEvent.emergency_type == emergency_type)
    if district_id:
        query = query.where(EmergencyEvent.affected_district_id == district_id)

    query = query.order_by(EmergencyEvent.started_at.desc())
    result = await db.execute(query)
    events = result.scalars().all()
    return [_format_emergency_response(e) for e in events]


@router.get("/{event_id}", response_model=EmergencyEventResponse, summary="Get emergency event by ID")
async def get_emergency_event(event_id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(EmergencyEvent).where(EmergencyEvent.id == event_id).options(selectinload(EmergencyEvent.district))
    result = await db.execute(query)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail=f"Emergency event with id '{event_id}' not found.")
    return _format_emergency_response(event)


@router.post("", response_model=EmergencyEventResponse, status_code=status.HTTP_201_CREATED, summary="Create an emergency event")
async def create_emergency_event(
    payload: EmergencyEventCreate,
    db: AsyncSession = Depends(get_db)
):
    if payload.affected_district_id:
        dist = await db.execute(select(District).where(District.id == payload.affected_district_id))
        if not dist.scalar_one_or_none():
            raise HTTPException(status_code=404, detail=f"District '{payload.affected_district_id}' not found.")

    event = EmergencyEvent(
        name=payload.name,
        description=payload.description,
        emergency_type=payload.emergency_type,
        severity=payload.severity,
        affected_district_id=payload.affected_district_id,
        started_at=payload.started_at or datetime.utcnow(),
        status="active"
    )

    db.add(event)
    await db.commit()
    await db.refresh(event)

    return await get_emergency_event(event.id, db)
