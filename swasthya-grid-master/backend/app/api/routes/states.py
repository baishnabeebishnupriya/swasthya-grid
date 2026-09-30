from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.state import State
from app.models.district import District
from app.schemas.state import StateResponse
from app.schemas.district import DistrictResponse

router = APIRouter(prefix="/states", tags=["States"])


@router.get("", response_model=List[StateResponse], summary="List all states")
async def list_states(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(State).order_by(State.name))
    return result.scalars().all()


@router.get("/{state_id}", response_model=StateResponse, summary="Get state by ID")
async def get_state(state_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(State).where(State.id == state_id))
    state = result.scalar_one_or_none()
    if not state:
        raise HTTPException(status_code=404, detail=f"State with id '{state_id}' not found.")
    return state


@router.get("/{state_id}/districts", response_model=List[DistrictResponse], summary="List districts in a state")
async def list_districts_by_state(state_id: UUID, db: AsyncSession = Depends(get_db)):
    # Check if state exists
    state_result = await db.execute(select(State).where(State.id == state_id))
    if not state_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"State with id '{state_id}' not found.")
        
    result = await db.execute(
        select(District).where(District.state_id == state_id).order_by(District.name)
    )
    return result.scalars().all()
