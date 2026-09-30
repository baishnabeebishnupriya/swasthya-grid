import pytest
from uuid import uuid4
from datetime import date, datetime, timedelta
import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.ai.preprocessing import Preprocessing
from app.ai.forecasting import DemandForecaster
from app.ai.stockout import StockoutEngine
from app.ai.risk_scoring import ResilienceScoringEngine
from app.ai.redistribution import RedistributionOptimizer
from app.ai.model_registry import ModelRegistry

client = TestClient(app)


def test_preprocessing_no_data_leakage():
    """Verify that lag features and rolling windows only use past observations."""
    records = []
    base_date = pd.Timestamp("2026-01-01")
    for i in range(40):
        records.append({
            "phc_id": "phc-1",
            "medicine_id": "med-1",
            "consumption_date": base_date + pd.Timedelta(days=i),
            "quantity_consumed": 10.0 + i
        })
    df = pd.DataFrame(records)
    featured = Preprocessing.build_features(df)

    assert "lag_1" in featured.columns
    assert "rolling_mean_7" in featured.columns
    # Check that lag_1 at index 10 is equal to quantity_consumed at index 9
    assert featured.loc[10, "lag_1"] == df.loc[9, "quantity_consumed"]
    # Check that rolling mean at index 10 does not include index 10 value
    expected_r7 = df.loc[3:9, "quantity_consumed"].mean()
    assert abs(featured.loc[10, "rolling_mean_7"] - expected_r7) < 1e-5


def test_forecasting_series_generation():
    """Verify recursive multi-day forecasting output structure and bounds."""
    forecaster = DemandForecaster()
    hist_df = pd.DataFrame({
        "consumption_date": pd.date_range("2026-01-01", periods=60),
        "quantity_consumed": [20.0 + (i % 5) for i in range(60)]
    })
    forecasts = forecaster.forecast_series(hist_df, horizon_days=7)

    assert len(forecasts) == 7
    for f in forecasts:
        assert f["predicted_demand"] > 0
        assert f["lower_bound"] <= f["predicted_demand"]
        assert f["upper_bound"] >= f["predicted_demand"]
        assert 0.0 <= f["confidence_score"] <= 1.0


def test_stockout_engine_critical_threshold():
    """Verify that a stockout within 2 days triggers CRITICAL risk tier."""
    result = StockoutEngine.evaluate_item_risk(
        medicine_id="med-ors",
        medicine_name="Oral Rehydration Salts (ORS)",
        medicine_category="Gastrointestinal",
        unit="sachets",
        current_stock=15,
        reserved_stock=0,
        daily_average_consumption=50.0,
        predicted_daily_demand=55.0,
        minimum_stock_level=200,
        reorder_level=500
    )
    assert result["risk_level"] == "CRITICAL"
    assert result["days_of_stock_remaining"] < 1.0
    assert result["risk_score"] >= 85.0
    assert "CRITICAL" in result["explanation"]


def test_resilience_scoring_weights_and_normalization():
    """Verify that resilience scoring strictly adheres to the 0-100 scale and weighted breakdown."""
    res = ResilienceScoringEngine.calculate_resilience(
        phc_id="phc-1",
        phc_name="PHC Test",
        inventory_items=[
            {"risk_level": "LOW"},
            {"risk_level": "LOW"},
            {"risk_level": "MEDIUM"}
        ],
        total_beds=20,
        available_beds=15,
        active_doctors=3,
        active_nurses=5,
        staff_present_count=7,
        total_staff_count=7,
        recent_daily_visits=30.0,
        baseline_daily_visits=30.0,
        active_district_emergencies=0
    )
    assert 0.0 <= res["resilience_score"] <= 100.0
    assert res["status"] in ["HEALTHY", "AT_RISK", "CRITICAL"]
    assert "medicine_availability" in res["components"]
    assert "bed_availability" in res["components"]
    assert "staff_availability" in res["components"]


def test_redistribution_demo_scenario():
    """
    Verify the Phase 1 AI Demo scenario:
    PHC Balipatna (Shortage) -> PHC Pipili (Surplus, ~14.2 km) recommended transfer.
    """
    dest_phc_id = "40000000-0000-0000-0000-000000000001"  # Balipatna
    source_phc_id = "40000000-0000-0000-0000-000000000004"  # Pipili
    ors_med_id = "30000000-0000-0000-0000-000000000002"

    dest_stock_items = [{
        "medicine_id": ors_med_id,
        "medicine_name": "Oral Rehydration Salts (ORS)",
        "unit": "sachets",
        "current_stock": 15,
        "reorder_level": 500,
        "predicted_daily_demand": 54.5,
        "risk_level": "CRITICAL"
    }]

    all_inventory = pd.DataFrame([
        {
            "phc_id": dest_phc_id,
            "phc_name": "PHC Balipatna",
            "phc_code": "OD-PHC-001",
            "medicine_id": ors_med_id,
            "quantity": 15,
            "reorder_level": 500,
            "daily_average_consumption": 54.5,
            "latitude": 20.1834,
            "longitude": 85.9521
        },
        {
            "phc_id": source_phc_id,
            "phc_name": "PHC Pipili",
            "phc_code": "OD-PHC-004",
            "medicine_id": ors_med_id,
            "quantity": 1450,
            "reorder_level": 500,
            "daily_average_consumption": 18.2,
            "latitude": 20.1167,
            "longitude": 85.8333
        }
    ])

    recs = RedistributionOptimizer.recommend_transfers(
        dest_phc_id=dest_phc_id,
        dest_phc_name="PHC Balipatna",
        dest_lat=20.1834,
        dest_lon=85.9521,
        dest_stock_items=dest_stock_items,
        all_phc_inventory=all_inventory
    )

    assert len(recs) == 1
    rec = recs[0]
    assert rec["source_phc_name"] == "PHC Pipili"
    assert rec["destination_phc_name"] == "PHC Balipatna"
    assert rec["recommended_quantity"] > 0
    assert 10.0 <= rec["distance_km"] <= 20.0
    assert "PHC Pipili" in rec["reason"]
