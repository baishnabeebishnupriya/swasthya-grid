from app.schemas.state import StateBase, StateCreate, StateResponse
from app.schemas.district import DistrictBase, DistrictCreate, DistrictResponse
from app.schemas.phc import PHCBase, PHCCreate, PHCUpdate, PHCResponse
from app.schemas.medicine import MedicineBase, MedicineCreate, MedicineResponse
from app.schemas.inventory import InventoryBase, InventoryCreate, InventoryUpdate, InventoryResponse
from app.schemas.bed import BedBase, BedUpdate, BedResponse
from app.schemas.staff import StaffBase, StaffCreate, StaffResponse
from app.schemas.attendance import AttendanceBase, AttendanceCreate, AttendanceResponse
from app.schemas.patient_visit import PatientVisitBase, PatientVisitCreate, PatientVisitResponse
from app.schemas.medicine_consumption import MedicineConsumptionBase, MedicineConsumptionCreate, MedicineConsumptionResponse
from app.schemas.forecast import ForecastBase, ForecastCreate, ForecastResponse
from app.schemas.risk_alert import RiskAlertBase, RiskAlertCreate, RiskAlertResponse
from app.schemas.resource_transfer import ResourceTransferBase, ResourceTransferCreate, ResourceTransferResponse
from app.schemas.emergency_event import EmergencyEventBase, EmergencyEventCreate, EmergencyEventResponse
from app.schemas.health_metrics import PHCHealthMetricsResponse, MedicineStockStatus

__all__ = [
    "StateBase", "StateCreate", "StateResponse",
    "DistrictBase", "DistrictCreate", "DistrictResponse",
    "PHCBase", "PHCCreate", "PHCUpdate", "PHCResponse",
    "MedicineBase", "MedicineCreate", "MedicineResponse",
    "InventoryBase", "InventoryCreate", "InventoryUpdate", "InventoryResponse",
    "BedBase", "BedUpdate", "BedResponse",
    "StaffBase", "StaffCreate", "StaffResponse",
    "AttendanceBase", "AttendanceCreate", "AttendanceResponse",
    "PatientVisitBase", "PatientVisitCreate", "PatientVisitResponse",
    "MedicineConsumptionBase", "MedicineConsumptionCreate", "MedicineConsumptionResponse",
    "ForecastBase", "ForecastCreate", "ForecastResponse",
    "RiskAlertBase", "RiskAlertCreate", "RiskAlertResponse",
    "ResourceTransferBase", "ResourceTransferCreate", "ResourceTransferResponse",
    "EmergencyEventBase", "EmergencyEventCreate", "EmergencyEventResponse",
    "PHCHealthMetricsResponse", "MedicineStockStatus"
]
