from typing import Optional, List, Callable
from uuid import UUID
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.phc import PHC
from app.models.district import District

security = HTTPBearer(auto_error=False)


async def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Validates JWT access token and returns authenticated User entity from database.
    """
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(auth.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str = payload.get("user_id")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing subject identifier.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed subject identifier in token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account associated with token no longer exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated.",
        )

    return user


def require_roles(allowed_roles: List[str]) -> Callable:
    """
    Dependency factory enforcing role-based permissions.
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}. Your role: {current_user.role}."
            )
        return current_user
    return role_checker


async def check_phc_access(user: User, phc_id: UUID, db: AsyncSession) -> None:
    """
    Enforces geographic scope isolation on PHC-level data:
    - PHC_ADMIN can only access their designated phc_id.
    - DISTRICT_OFFICER can only access PHCs within their designated district_id.
    - STATE_ADMIN can only access PHCs within their designated state_id.
    """
    if user.role == "PHC_ADMIN":
        if user.phc_id != phc_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Scope violation: PHC_ADMIN is restricted to assigned facility '{user.phc_id}'."
            )
        return

    # For District Officer or State Admin, resolve PHC's hierarchy
    phc_res = await db.execute(select(PHC).where(PHC.id == phc_id))
    phc = phc_res.scalar_one_or_none()
    if not phc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PHC '{phc_id}' not found.")

    if user.role == "DISTRICT_OFFICER":
        if user.district_id != phc.district_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Scope violation: DISTRICT_OFFICER is restricted to district '{user.district_id}'."
            )
        return

    if user.role == "STATE_ADMIN":
        dist_res = await db.execute(select(District).where(District.id == phc.district_id))
        dist = dist_res.scalar_one_or_none()
        if not dist or dist.state_id != user.state_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Scope violation: STATE_ADMIN is restricted to state '{user.state_id}'."
            )
        return


async def check_district_access(user: User, district_id: UUID, db: AsyncSession) -> None:
    """
    Enforces geographic scope isolation on District-level data.
    """
    if user.role == "DISTRICT_OFFICER":
        if user.district_id != district_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Scope violation: DISTRICT_OFFICER is restricted to district '{user.district_id}'."
            )
        return

    if user.role == "STATE_ADMIN":
        dist_res = await db.execute(select(District).where(District.id == district_id))
        dist = dist_res.scalar_one_or_none()
        if not dist or dist.state_id != user.state_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Scope violation: STATE_ADMIN is restricted to state '{user.state_id}'."
            )
        return
