from uuid import UUID
from datetime import date
from typing import List, Optional, Dict
from pydantic import BaseModel, ConfigDict, Field


class ForecastItemResponse(BaseModel):
    forecast_date: date
    predicted_demand: float
    lower_bound: float
    upper_bound: float
    confidence_score: float
    model_version: str

    model_config = ConfigDict(from_attributes=True)


class PHCDemandForecastResponse(BaseModel):
    phc_id: UUID
    phc_name: str
    medicine_id: UUID
    medicine_name: str
    unit: str
    horizon_days: int
    forecasts: List[ForecastItemResponse]
    model_used: str

    model_config = ConfigDict(from_attributes=True)


class StockoutRiskItemResponse(BaseModel):
    medicine_id: UUID
    medicine_name: str
    medicine_category: str
    unit: str
    current_stock: int
    reserved_stock: int
    effective_available_stock: int
    predicted_daily_demand: float
    days_of_stock_remaining: float
    minimum_stock_level: int
    reorder_level: int
    estimated_stockout_date: Optional[date] = None
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    explanation: str

    model_config = ConfigDict(from_attributes=True)


class PHCStockoutRiskSummaryResponse(BaseModel):
    phc_id: UUID
    phc_name: str
    overall_stockout_risk: str
    critical_items_count: int
    high_risk_items_count: int
    items: List[StockoutRiskItemResponse]

    model_config = ConfigDict(from_attributes=True)


class ResilienceComponentScores(BaseModel):
    medicine_availability: float
    bed_availability: float
    staff_availability: float
    demand_stability: float
    emergency_readiness: float


class PHCResilienceResponse(BaseModel):
    phc_id: UUID
    phc_name: str
    resilience_score: float = Field(..., ge=0.0, le=100.0)
    status: str = Field(..., pattern="^(HEALTHY|AT_RISK|CRITICAL)$")
    components: ResilienceComponentScores
    weights: Dict[str, float]
    explanation: str

    model_config = ConfigDict(from_attributes=True)


class RedistributionRecommendationResponse(BaseModel):
    medicine_id: UUID
    medicine_name: str
    unit: str
    destination_phc_id: UUID
    destination_phc_name: str
    source_phc_id: UUID
    source_phc_name: str
    source_phc_code: str
    recommended_quantity: int
    distance_km: float
    estimated_arrival_minutes: int
    destination_urgency: str
    reason: str
    alternative_sources_count: int

    model_config = ConfigDict(from_attributes=True)


class PHCRedistributionPlanResponse(BaseModel):
    phc_id: UUID
    phc_name: str
    recommendations_count: int
    recommendations: List[RedistributionRecommendationResponse]

    model_config = ConfigDict(from_attributes=True)
