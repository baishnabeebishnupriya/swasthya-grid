import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db
from app.core.security import get_password_hash, create_access_token, verify_password
from app.models.user import User
from app.models.phc import PHC
from app.models.district import District
from app.models.state import State
from app.models.resource_transfer import ResourceTransfer
from app.api.deps import check_phc_access, check_district_access

client = TestClient(app)


def test_password_hashing_and_verification():
    """Verify bcrypt hashing generates secure salted hashes and verifies cleanly."""
    raw = "MySecretPass@2026"
    hashed = get_password_hash(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_generation_and_decoding():
    """Verify access and refresh token signing with subject claims."""
    user_id = str(uuid4())
    claims = {"user_id": user_id, "role": "STATE_ADMIN", "state_id": str(uuid4())}
    token = create_access_token(data=claims)

    from app.core.security import decode_token
    payload = decode_token(token)
    assert payload is not None
    assert payload["user_id"] == user_id
    assert payload["role"] == "STATE_ADMIN"
    assert payload["type"] == "access"


def test_unauthenticated_request_rejected():
    """Verify protected endpoints reject requests lacking Bearer token with 401."""
    res = client.get("/api/auth/me")
    assert res.status_code == 401
    assert "detail" in res.json()


def test_login_invalid_credentials():
    """Verify login with incorrect password returns 401 Unauthorized."""
    mock_session = AsyncMock()
    mock_user = User(
        id=uuid4(),
        name="Test User",
        email="test@health.gov.in",
        password_hash=get_password_hash("CorrectPass@123"),
        role="STATE_ADMIN",
        state_id=uuid4(),
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = mock_result

    async def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    res = client.post("/api/auth/login", json={
        "email": "test@health.gov.in",
        "password": "WrongPassword@123"
    })
    assert res.status_code == 401
    assert "Invalid email" in res.json()["detail"]

    app.dependency_overrides.clear()


def test_login_success_and_no_password_hash_exposed():
    """Verify successful login returns valid JWT and user object without password_hash."""
    mock_session = AsyncMock()
    user_id = uuid4()
    state_id = uuid4()
    mock_user = User(
        id=user_id,
        name="Dr. Rajeshwar Jena",
        email="state.admin@odisha.health.gov.in",
        password_hash=get_password_hash("Password@123"),
        role="STATE_ADMIN",
        state_id=state_id,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    call_count = 0
    def mock_exec(query):
        nonlocal call_count
        res = MagicMock()
        if call_count == 0:
            res.scalar_one_or_none.return_value = mock_user
        else:
            res.scalar_one_or_none.return_value = "Odisha"
        call_count += 1
        return res

    mock_session.execute.side_effect = mock_exec

    async def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    res = client.post("/api/auth/login", json={
        "email": "state.admin@odisha.health.gov.in",
        "password": "Password@123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "state.admin@odisha.health.gov.in"
    assert data["user"]["role"] == "STATE_ADMIN"
    assert "password_hash" not in data["user"]
    assert "password" not in data["user"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_phc_scope_isolation():
    """Verify that PHC_ADMIN cannot access another PHC facility's private operational scope."""
    from fastapi import HTTPException
    
    phc_a_id = uuid4()
    phc_b_id = uuid4()

    phc_admin_a = User(
        id=uuid4(),
        name="PHC Admin A",
        email="phc.a@odisha.health.gov.in",
        role="PHC_ADMIN",
        phc_id=phc_a_id,
        is_active=True
    )

    mock_db = AsyncMock()

    # Allowed access to own PHC
    await check_phc_access(phc_admin_a, phc_a_id, mock_db)

    # Denied access to another PHC
    with pytest.raises(HTTPException) as exc:
        await check_phc_access(phc_admin_a, phc_b_id, mock_db)
    assert exc.value.status_code == 403
    assert "Scope violation" in exc.value.detail


@pytest.mark.asyncio
async def test_district_scope_isolation():
    """Verify that DISTRICT_OFFICER cannot access another district's data."""
    from fastapi import HTTPException

    dist_a_id = uuid4()
    dist_b_id = uuid4()

    district_officer_a = User(
        id=uuid4(),
        name="Officer A",
        email="officer.a@odisha.health.gov.in",
        role="DISTRICT_OFFICER",
        district_id=dist_a_id,
        is_active=True
    )

    mock_db = AsyncMock()

    # Allowed access to own district
    await check_district_access(district_officer_a, dist_a_id, mock_db)

    # Denied access to another district
    with pytest.raises(HTTPException) as exc:
        await check_district_access(district_officer_a, dist_b_id, mock_db)
    assert exc.value.status_code == 403
    assert "Scope violation" in exc.value.detail


def test_transfer_approval_authorization_permission():
    """Verify that transfer approval requires STATE_ADMIN or DISTRICT_OFFICER, and rejects PHC_ADMIN."""
    transfer_id = uuid4()

    # Case 1: Unauthenticated -> 401
    res_unauth = client.put(f"/api/transfers/{transfer_id}/approve")
    assert res_unauth.status_code == 401

    # Case 2: PHC_ADMIN -> 403 Forbidden
    phc_admin_user = User(
        id=uuid4(),
        name="PHC Admin",
        email="phc.admin@odisha.health.gov.in",
        password_hash="hash",
        role="PHC_ADMIN",
        phc_id=uuid4(),
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    token_phc_admin = create_access_token({"user_id": str(phc_admin_user.id), "role": "PHC_ADMIN"})

    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = phc_admin_user
    mock_session.execute.return_value = mock_result

    async def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    res_phc = client.put(
        f"/api/transfers/{transfer_id}/approve",
        headers={"Authorization": f"Bearer {token_phc_admin}"}
    )
    assert res_phc.status_code == 403
    assert "Access denied" in res_phc.json()["detail"]

    app.dependency_overrides.clear()
