from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.risk_alert import RiskAlert
from app.models.phc import PHC
from app.schemas.risk_alert import RiskAlertResponse

router = APIRouter(tags=["Risk Alerts"])


def _format_risk_response(r: RiskAlert) -> RiskAlertResponse:
    return RiskAlertResponse(
        id=r.id,
        phc_id=r.phc_id,
        medicine_id=r.medicine_id,
        alert_type=r.alert_type,
        severity=r.severity,
        title=r.title,
        description=r.description,
        risk_score=float(r.risk_score),
        recommended_action=r.recommended_action,
        status=r.status,
        created_at=r.created_at,
        resolved_at=r.resolved_at,
        medicine_name=r.medicine.name if r.medicine else None,
        phc_name=r.phc.name if r.phc else None
    )


@router.get("/risks", response_model=List[RiskAlertResponse], summary="List all risk alerts with filters")
async def list_risk_alerts(
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$", description="Filter by severity"),
    status: Optional[str] = Query(None, pattern="^(open|acknowledged|resolved)$", description="Filter by status"),
    alert_type: Optional[str] = Query(None, pattern="^(stockout|bed_shortage|staff_shortage|demand_surge|emergency)$", description="Filter by alert type"),
    phc_id: Optional[UUID] = Query(None, description="Filter by PHC ID"),
    db: AsyncSession = Depends(get_db)
):
    query = select(RiskAlert).options(selectinload(RiskAlert.medicine), selectinload(RiskAlert.phc))

    if severity:
        query = query.where(RiskAlert.severity == severity)
    if status:
        query = query.where(RiskAlert.status == status)
    if alert_type:
        query = query.where(RiskAlert.alert_type == alert_type)
    if phc_id:
        query = query.where(RiskAlert.phc_id == phc_id)

    query = query.order_by(RiskAlert.risk_score.desc(), RiskAlert.created_at.desc())
    result = await db.execute(query)
    alerts = result.scalars().all()
    return [_format_risk_response(a) for a in alerts]


@router.get("/phcs/{phc_id}/risks", response_model=List[RiskAlertResponse], summary="Get risk alerts for a specific PHC")
async def get_phc_risk_alerts(
    phc_id: UUID,
    severity: Optional[str] = Query(None, pattern="^(low|medium|high|critical)$"),
    status: Optional[str] = Query(None, pattern="^(open|acknowledged|resolved)$"),
    alert_type: Optional[str] = Query(None, pattern="^(stockout|bed_shortage|staff_shortage|demand_surge|emergency)$"),
    db: AsyncSession = Depends(get_db)
):
    phc_check = await db.execute(select(PHC).where(PHC.id == phc_id))
    if not phc_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"PHC with id '{phc_id}' not found.")

    query = (
        select(RiskAlert)
        .where(RiskAlert.phc_id == phc_id)
        .options(selectinload(RiskAlert.medicine), selectinload(RiskAlert.phc))
    )

    if severity:
        query = query.where(RiskAlert.severity == severity)
    if status:
        query = query.where(RiskAlert.status == status)
    if alert_type:
        query = query.where(RiskAlert.alert_type == alert_type)

    query = query.order_by(RiskAlert.risk_score.desc(), RiskAlert.created_at.desc())
    result = await db.execute(query)
    alerts = result.scalars().all()
    return [_format_risk_response(a) for a in alerts]
