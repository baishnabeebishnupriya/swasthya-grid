from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class MedicineStockStatus(BaseModel):
    medicine_id: UUID
    medicine_name: str
    category: str
    current_stock: int
    minimum_stock_level: int
    reorder_level: int
    days_of_supply_remaining: Optional[float] = None
    status: str  # surplus, adequate, low, critical

    model_config = ConfigDict(from_attributes=True)


class PHCHealthMetricsResponse(BaseModel):
    phc_id: UUID
    phc_name: str
    phc_code: str
    status: str
    
    # Bed Metrics
    total_beds: int
    occupied_beds: int
    reserved_beds: int
    available_beds: int
    bed_occupancy_rate_pct: float
    
    # Staff Metrics
    total_staff: int
    active_staff: int
    present_today: int
    staff_availability_rate_pct: float
    doctor_count: int
    nurse_count: int
    
    # Patient Load Metrics
    recent_7day_total_visits: int
    recent_7day_daily_average_visits: float
    recent_7day_emergencies: int
    
    # Inventory Summary
    total_medicines_tracked: int
    critical_medicines_count: int
    low_stock_medicines_count: int
    adequate_medicines_count: int
    surplus_medicines_count: int
    medicine_availability_pct: float
    critical_medicines_list: List[MedicineStockStatus] = []

    model_config = ConfigDict(from_attributes=True)
