from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.config import RoleEnum
from ..services.user_service import UserService
from typing import Optional


class CurrentUser:
    """Dependency for getting current user"""
    def __init__(self, user_id: int, role: RoleEnum):
        self.user_id = user_id
        self.role = role


def get_current_user(
    x_user_id: Optional[int] = Header(None),
    x_user_role: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> CurrentUser:
    """Get current user from headers (mock authentication)"""
    if x_user_id is None or x_user_role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing user headers"
        )
    
    try:
        role = RoleEnum(x_user_role.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role: {x_user_role}"
        )
    
    # Try to verify user exists (for bootstrap, allow if user doesn't exist yet)
    try:
        user = UserService.get_user_by_id(db, x_user_id)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )
    except HTTPException:
        # Allow request if user doesn't exist (bootstrap scenario)
        pass
    
    return CurrentUser(user_id=x_user_id, role=role)


def get_admin_user_role_only(
    x_user_role: Optional[str] = Header(None)
) -> CurrentUser:
    """Get admin context from role header only (no user id required)."""
    if x_user_role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing user role header"
        )

    try:
        role = RoleEnum(x_user_role.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role: {x_user_role}"
        )

    if role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    # user_id is not needed for admin all-records access.
    return CurrentUser(user_id=0, role=role)
