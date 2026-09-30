from fastapi import APIRouter
from app.api.routes import (
    health_router,
    states_router,
    districts_router,
    phcs_router,
    medicines_router,
    inventory_router,
    beds_router,
    staff_router,
    attendance_router,
    patients_router,
    consumption_router,
    forecasts_router,
    risks_router,
    transfers_router,
    emergencies_router,
    metrics_router,
    ai_router,
    auth_router
)

api_router = APIRouter()

# Authentication & Access Control
api_router.include_router(auth_router)

# Resource & Domain Routes
api_router.include_router(health_router)
api_router.include_router(states_router)
api_router.include_router(districts_router)
api_router.include_router(phcs_router)
api_router.include_router(medicines_router)
api_router.include_router(inventory_router)
api_router.include_router(beds_router)
api_router.include_router(staff_router)
api_router.include_router(attendance_router)
api_router.include_router(patients_router)
api_router.include_router(consumption_router)
api_router.include_router(forecasts_router)
api_router.include_router(risks_router)
api_router.include_router(transfers_router)
api_router.include_router(emergencies_router)
api_router.include_router(metrics_router)
api_router.include_router(ai_router)

__all__ = ["api_router"]
