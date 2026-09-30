from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.state import State
from app.models.district import District
from app.models.phc import PHC
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    TokenRefresh,
    UserResponse
)
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication & Access Control"])


async def format_user_response(user: User, db: AsyncSession) -> UserResponse:
    """Enriches user model with resolved territorial names for client context."""
    state_name = None
    district_name = None
    phc_name = None

    try:
        if getattr(user, "state", None) and getattr(user.state, "name", None):
            state_name = user.state.name
        elif user.state_id:
            s_res = await db.execute(select(State.name).where(State.id == user.state_id))
            val = s_res.scalar_one_or_none()
            if isinstance(val, str):
                state_name = val

        if getattr(user, "district", None) and getattr(user.district, "name", None):
            district_name = user.district.name
        elif user.district_id:
            d_res = await db.execute(select(District.name).where(District.id == user.district_id))
            val = d_res.scalar_one_or_none()
            if isinstance(val, str):
                district_name = val

        if getattr(user, "phc", None) and getattr(user.phc, "name", None):
            phc_name = user.phc.name
        elif user.phc_id:
            p_res = await db.execute(select(PHC.name).where(PHC.id == user.phc_id))
            val = p_res.scalar_one_or_none()
            if isinstance(val, str):
                phc_name = val
    except Exception:
        pass

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        state_id=user.state_id,
        district_id=user.district_id,
        phc_id=user.phc_id,
        state_name=state_name,
        district_name=district_name,
        phc_name=phc_name,
        is_active=user.is_active,
        created_at=user.created_at or datetime.now(timezone.utc),
        updated_at=user.updated_at or datetime.now(timezone.utc)
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register New User")
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Registers a new authorized administrative officer with role and scope validations.
    """
    existing_res = await db.execute(select(User).where(User.email == payload.email))
    if existing_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{payload.email}' is already registered."
        )

    if payload.state_id:
        s_check = await db.execute(select(State.id).where(State.id == payload.state_id))
        if not s_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"State '{payload.state_id}' does not exist.")

    if payload.district_id:
        d_check = await db.execute(select(District.id).where(District.id == payload.district_id))
        if not d_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"District '{payload.district_id}' does not exist.")

    if payload.phc_id:
        p_check = await db.execute(select(PHC.id).where(PHC.id == payload.phc_id))
        if not p_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"PHC '{payload.phc_id}' does not exist.")

    new_user = User(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role=payload.role.value,
        state_id=payload.state_id,
        district_id=payload.district_id,
        phc_id=payload.phc_id,
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    audit = AuditLog(
        actor_type=new_user.role,
        actor_id=str(new_user.id),
        action="USER_REGISTERED",
        entity_type="users",
        entity_id=str(new_user.id),
        meta_data={"email": new_user.email, "role": new_user.role}
    )
    db.add(audit)
    await db.commit()

    return await format_user_response(new_user, db)


@router.post("/login", response_model=TokenResponse, summary="Officer Authentication & Token Grant")
async def login_user(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticates administrative user credentials and issues signed JWT tokens.
    """
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email address or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is suspended or deactivated. Contact state health administrator."
        )

    token_claims = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role,
        "state_id": str(user.state_id) if user.state_id else None,
        "district_id": str(user.district_id) if user.district_id else None,
        "phc_id": str(user.phc_id) if user.phc_id else None
    }

    access_token = create_access_token(data=token_claims)
    refresh_token = create_refresh_token(data={"user_id": str(user.id)})

    audit = AuditLog(
        actor_type=user.role,
        actor_id=str(user.id),
        action="USER_LOGIN_SUCCESS",
        entity_type="auth",
        entity_id=str(user.id),
        meta_data={"email": user.email, "role": user.role}
    )
    db.add(audit)
    await db.commit()

    user_resp = await format_user_response(user, db)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_resp
    )


@router.get("/me", response_model=UserResponse, summary="Get Current Authenticated User")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns profile and territorial scope metadata for the currently authenticated officer.
    """
    return await format_user_response(current_user, db)


@router.post("/refresh", response_model=TokenResponse, summary="Refresh Access Token")
async def refresh_access_token(
    payload: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """
    Exchanges a valid refresh token for a newly minted access token.
    """
    token_data = decode_token(payload.refresh_token)
    if not token_data or token_data.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token."
        )

    user_id_str = token_data.get("user_id")
    try:
        user_id = UUID(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Malformed token subject.")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User account inactive or missing.")

    token_claims = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role,
        "state_id": str(user.state_id) if user.state_id else None,
        "district_id": str(user.district_id) if user.district_id else None,
        "phc_id": str(user.phc_id) if user.phc_id else None
    }

    new_access_token = create_access_token(data=token_claims)
    new_refresh_token = create_refresh_token(data={"user_id": str(user.id)})
    user_resp = await format_user_response(user, db)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_resp
    )


@router.post("/logout", summary="Logout User")
async def logout_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logs officer sign-out event in audit trail.
    """
    audit = AuditLog(
        actor_type=current_user.role,
        actor_id=str(current_user.id),
        action="USER_LOGOUT",
        entity_type="auth",
        entity_id=str(current_user.id),
        meta_data={"email": current_user.email}
    )
    db.add(audit)
    await db.commit()

    return {"status": "ok", "message": "Successfully logged out."}
