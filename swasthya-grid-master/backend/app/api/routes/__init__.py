from app.api.routes.health import router as health_router
from app.api.routes.states import router as states_router
from app.api.routes.districts import router as districts_router
from app.api.routes.phcs import router as phcs_router
from app.api.routes.medicines import router as medicines_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.beds import router as beds_router
from app.api.routes.staff import router as staff_router
from app.api.routes.attendance import router as attendance_router
from app.api.routes.patients import router as patients_router
from app.api.routes.consumption import router as consumption_router
from app.api.routes.forecasts import router as forecasts_router
from app.api.routes.risks import router as risks_router
from app.api.routes.transfers import router as transfers_router
from app.api.routes.emergencies import router as emergencies_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.ai import router as ai_router
from app.api.routes.auth import router as auth_router

__all__ = [
    "health_router",
    "states_router",
    "districts_router",
    "phcs_router",
    "medicines_router",
    "inventory_router",
    "beds_router",
    "staff_router",
    "attendance_router",
    "patients_router",
    "consumption_router",
    "forecasts_router",
    "risks_router",
    "transfers_router",
    "emergencies_router",
    "metrics_router",
    "ai_router",
    "auth_router"
]
