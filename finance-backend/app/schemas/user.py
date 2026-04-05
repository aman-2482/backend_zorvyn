from pydantic import BaseModel, EmailStr, Field
from ..core.config import RoleEnum
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email")
    full_name: str = Field(..., min_length=1, max_length=100, description="Full name")
    role: RoleEnum = Field(default=RoleEnum.VIEWER, description="User role")


class UserCreate(UserBase):
    """Schema for creating user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
