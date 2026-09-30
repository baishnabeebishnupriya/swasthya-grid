import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.bed import BedUpdate

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SwasthyaGrid API"
    assert data["status"] == "operational"
    assert "/docs" in data["docs_url"]


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_bed_validation_exceeds_capacity():
    """Verify that occupied + reserved > total raises ValueError in BedUpdate schema."""
    with pytest.raises(ValueError):
        BedUpdate(
            total_beds=10,
            occupied_beds=8,
            reserved_beds=4  # 8 + 4 = 12 > 10
        )


def test_bed_validation_valid():
    """Verify that occupied + reserved <= total passes validation."""
    bed = BedUpdate(
        total_beds=10,
        occupied_beds=6,
        reserved_beds=2  # 6 + 2 = 8 <= 10
    )
    assert bed.occupied_beds == 6
    assert bed.reserved_beds == 2
    assert bed.total_beds == 10


def test_openapi_documentation_accessible():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/api/health" in schema["paths"]
    assert "/api/phcs" in schema["paths"]
    assert "/api/inventory" in schema["paths"]
    assert "/api/transfers" in schema["paths"]
