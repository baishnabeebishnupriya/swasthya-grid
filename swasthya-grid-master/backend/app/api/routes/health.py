from fastapi import APIRouter
from app.core.database import check_database_connection

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Application Health Check")
async def health_check():
    """
    Simple liveness probe.
    """
    return {"status": "ok"}


@router.get("/database", summary="Database Connectivity Probe")
async def database_health_check():
    """
    Verifies that the backend can actively query the PostgreSQL/PostGIS database.
    """
    result = await check_database_connection()
    if result.get("connected"):
        return {
            "status": "ok",
            "database": "connected",
            "details": result
        }
    else:
        return {
            "status": "degraded",
            "database": "disconnected",
            "error": result.get("error")
        }
