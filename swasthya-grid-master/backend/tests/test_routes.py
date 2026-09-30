import pytest
from uuid import uuid4
from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db
from app.models.state import State
from app.models.district import District
from app.models.phc import PHC
from app.models.medicine import Medicine

client = TestClient(app)


@pytest.fixture
def mock_db():
    mock_session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: mock_session
    yield mock_session
    app.dependency_overrides.clear()


def test_get_states_with_db_mock(mock_db):
    state_id = uuid4()
    mock_state = State(
        id=state_id,
        name="Odisha",
        code="OD",
        created_at=datetime.utcnow()
    )
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_state]
    mock_db.execute.return_value = mock_result

    response = client.get("/api/states")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Odisha"
    assert data[0]["code"] == "OD"


def test_get_phc_by_id_with_db_mock(mock_db):
    phc_id = uuid4()
    dist_id = uuid4()
    state_id = uuid4()
    
    mock_state = State(id=state_id, name="Odisha", code="OD")
    mock_district = District(id=dist_id, state_id=state_id, name="Khordha", code="OD_KHO", state=mock_state)
    
    mock_phc = PHC(
        id=phc_id,
        district_id=dist_id,
        name="PHC Balipatna",
        code="OD-PHC-001",
        address="Balipatna Block",
        latitude=20.1834,
        longitude=85.9521,
        total_beds=12,
        active_doctors=2,
        active_nurses=4,
        status="critical",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        district=mock_district,
        beds=None
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_phc
    mock_db.execute.return_value = mock_result

    response = client.get(f"/api/phcs/{phc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "PHC Balipatna"
    assert data["status"] == "critical"
    assert data["district_name"] == "Khordha"
    assert data["state_name"] == "Odisha"
    assert data["total_beds"] == 12


def test_get_medicines_with_db_mock(mock_db):
    med_id = uuid4()
    mock_med = Medicine(
        id=med_id,
        name="Oral Rehydration Salts (ORS)",
        generic_name="ORS IP",
        category="Gastrointestinal & Electrolytes",
        unit="sachets",
        minimum_stock_level=200,
        reorder_level=500,
        created_at=datetime.utcnow()
    )

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_med]
    mock_db.execute.return_value = mock_result

    response = client.get("/api/medicines")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Oral Rehydration Salts (ORS)"
    assert data[0]["unit"] == "sachets"
