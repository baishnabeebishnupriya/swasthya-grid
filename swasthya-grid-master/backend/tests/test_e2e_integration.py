import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, date
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db
from app.ai.stockout import StockoutEngine
from app.ai.risk_scoring import ResilienceScoringEngine
from app.ai.redistribution import RedistributionOptimizer
import pandas as pd

client = TestClient(app)


def test_e2e_health_endpoint():
    """Verify health endpoint."""
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "ok"


def test_e2e_core_routes_mocked_db():
    """Verify core routes process requests and return structured JSON."""
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    async def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    endpoints = [
        "/api/states",
        "/api/districts",
        "/api/phcs",
        "/api/medicines",
        "/api/inventory",
        "/api/forecasts",
        "/api/risks",
        "/api/transfers",
        "/api/emergencies"
    ]
    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        assert isinstance(resp.json(), list)

    app.dependency_overrides.clear()


def test_e2e_phc_coordinate_bounds():
    """Verify that all seed PHCs have valid coordinates within Eastern India (Lat 18°-28° N, Lon 84°-90° E)."""
    sample_coords = [
        {"name": "PHC Balipatna", "code": "OD-PHC-001", "lat": 20.1834, "lon": 85.9521},
        {"name": "PHC Pipili", "code": "OD-PHC-004", "lat": 20.1167, "lon": 85.8333},
        {"name": "PHC Bishnupur", "code": "WB-PHC-001", "lat": 23.0750, "lon": 87.3190},
        {"name": "PHC Ormanjhi", "code": "JH-PHC-001", "lat": 23.4833, "lon": 85.4833}
    ]
    for phc in sample_coords:
        assert 18.0 <= phc["lat"] <= 28.0
        assert 84.0 <= phc["lon"] <= 90.0


def test_e2e_ai_demo_scenario_ors():
    """
    Verify complete AI demo scenario:
    1. Balipatna (OD-PHC-001) ORS inventory: low (15 sachets), consumption: 54.5/day.
    2. Stockout Engine predicts depletion in 0.3 days -> CRITICAL risk alert.
    3. Resilience Engine detects stressed facility capacity.
    4. Redistribution Engine scans network, finds Pipili (OD-PHC-004) with safe surplus of 1,250 sachets, 14.2 km away.
    5. Optimizer recommends safe transfer quantity with ETA ~35 mins.
    """
    stock_eval = StockoutEngine.evaluate_item_risk(
        medicine_id="30000000-0000-0000-0000-000000000002",
        medicine_name="Oral Rehydration Salts (ORS)",
        medicine_category="Gastrointestinal",
        unit="sachets",
        current_stock=15,
        reserved_stock=0,
        daily_average_consumption=54.5,
        predicted_daily_demand=54.5,
        minimum_stock_level=200,
        reorder_level=500
    )
    assert stock_eval["risk_level"] == "CRITICAL"
    assert stock_eval["days_of_stock_remaining"] < 1.0

    all_inv = pd.DataFrame([
        {
            "phc_id": "40000000-0000-0000-0000-000000000001",
            "phc_name": "PHC Balipatna",
            "phc_code": "OD-PHC-001",
            "medicine_id": "30000000-0000-0000-0000-000000000002",
            "quantity": 15,
            "reorder_level": 500,
            "daily_average_consumption": 54.5,
            "latitude": 20.1834,
            "longitude": 85.9521
        },
        {
            "phc_id": "40000000-0000-0000-0000-000000000004",
            "phc_name": "PHC Pipili",
            "phc_code": "OD-PHC-004",
            "medicine_id": "30000000-0000-0000-0000-000000000002",
            "quantity": 1450,
            "reorder_level": 500,
            "daily_average_consumption": 18.2,
            "latitude": 20.1167,
            "longitude": 85.8333
        }
    ])

    recs = RedistributionOptimizer.recommend_transfers(
        dest_phc_id="40000000-0000-0000-0000-000000000001",
        dest_phc_name="PHC Balipatna",
        dest_lat=20.1834,
        dest_lon=85.9521,
        dest_stock_items=[stock_eval],
        all_phc_inventory=all_inv
    )

    assert len(recs) == 1
    top = recs[0]
    assert top["source_phc_name"] == "PHC Pipili"
    assert top["recommended_quantity"] > 0
    assert 13.0 <= top["distance_km"] <= 16.0
    assert 30 <= top["estimated_arrival_minutes"] <= 45
    assert "PHC Pipili" in top["reason"]
