from fastapi import HTTPException, status
from .config import RoleEnum

# Mock current user storage (in production, use JWT tokens)
current_user_context = {"user_id": None, "role": None}


def set_current_user(user_id: int, role: RoleEnum):
    """Set current user in context"""
    current_user_context["user_id"] = user_id
    current_user_context["role"] = role


def get_current_user():
    """Get current user from context"""
    return current_user_context


def check_admin(user_role: RoleEnum):
    """Check if user has admin role"""
    if user_role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


def check_analyst_or_admin(user_role: RoleEnum):
    """Check if user is analyst or admin"""
    if user_role not in [RoleEnum.ANALYST, RoleEnum.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst or Admin access required"
        )


def check_can_read(user_role: RoleEnum):
    """Check if user can read data (all roles can read)"""
    if user_role not in [RoleEnum.VIEWER, RoleEnum.ANALYST, RoleEnum.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


def check_can_modify(user_role: RoleEnum):
    """Check if user can modify records (analyst and admin)"""
    if user_role not in [RoleEnum.ANALYST, RoleEnum.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify records"
        )
