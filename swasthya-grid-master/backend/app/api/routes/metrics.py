from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.health_metrics import HealthMetricsService
from app.schemas.health_metrics import PHCHealthMetricsResponse

router = APIRouter(prefix="/phcs", tags=["Operational Health Metrics"])


@router.get("/{phc_id}/metrics", response_model=PHCHealthMetricsResponse, summary="Get calculated operational health metrics for a PHC")
async def get_phc_health_metrics(
    phc_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Computes key baseline non-AI facility metrics including:
    - Bed occupancy rate (%)
    - Staff availability rate (%)
    - Recent 7-day patient demand & emergency volume
    - Inventory stock health & critical stockout alerts
    """
    return await HealthMetricsService.compute_phc_metrics(db, phc_id)
