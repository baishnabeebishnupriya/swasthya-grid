from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.forecast import Forecast
from app.models.phc import PHC
from app.schemas.forecast import ForecastResponse

router = APIRouter(tags=["Forecasts (AI Demands)"])


def _format_forecast_response(f: Forecast) -> ForecastResponse:
    return ForecastResponse(
        id=f.id,
        phc_id=f.phc_id,
        medicine_id=f.medicine_id,
        forecast_date=f.forecast_date,
        predicted_demand=float(f.predicted_demand),
        lower_bound=float(f.lower_bound),
        upper_bound=float(f.upper_bound),
        confidence_score=float(f.confidence_score),
        model_version=f.model_version,
        created_at=f.created_at,
        medicine_name=f.medicine.name if f.medicine else None,
        phc_name=f.phc.name if f.phc else None
    )


@router.get("/forecasts", response_model=List[ForecastResponse], summary="List all stored forecast records")
async def list_forecasts(
    phc_id: Optional[UUID] = Query(None, description="Filter by PHC ID"),
    medicine_id: Optional[UUID] = Query(None, description="Filter by Medicine ID"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Forecast).options(selectinload(Forecast.medicine), selectinload(Forecast.phc))
    if phc_id:
        query = query.where(Forecast.phc_id == phc_id)
    if medicine_id:
        query = query.where(Forecast.medicine_id == medicine_id)

    query = query.order_by(Forecast.forecast_date.asc())
    result = await db.execute(query)
    records = result.scalars().all()
    return [_format_forecast_response(r) for r in records]


@router.get("/phcs/{phc_id}/forecasts", response_model=List[ForecastResponse], summary="Get forecast records for a specific PHC")
async def get_phc_forecasts(
    phc_id: UUID,
    medicine_id: Optional[UUID] = Query(None, description="Filter by Medicine ID"),
    db: AsyncSession = Depends(get_db)
):
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    if not phc_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    query = (
        select(Forecast)
        .where(Forecast.phc_id == phc_id)
        .options(selectinload(Forecast.medicine), selectinload(Forecast.phc))
    )
    if medicine_id:
        query = query.where(Forecast.medicine_id == medicine_id)

    query = query.order_by(Forecast.forecast_date.asc())
    result = await db.execute(query)
    records = result.scalars().all()
    return [_format_forecast_response(r) for r in records]
