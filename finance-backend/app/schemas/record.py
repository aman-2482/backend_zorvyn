from pydantic import BaseModel, Field
from ..models.record import RecordType
from datetime import datetime
from typing import Optional


class RecordBase(BaseModel):
    """Base record schema"""
    amount: float = Field(..., gt=0, description="Transaction amount")
    type: RecordType = Field(..., description="Record type (income/expense)")
    category: str = Field(..., min_length=1, max_length=50, description="Category")
    date: datetime = Field(..., description="Transaction date")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")


class RecordCreate(RecordBase):
    """Schema for creating record"""
    pass


class RecordUpdate(BaseModel):
    """Schema for updating record"""
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)


class RecordResponse(RecordBase):
    """Schema for record response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    """Schema for dashboard summary"""
    total_income: float
    total_expenses: float
    net_balance: float
    category_totals: dict[str, float]
    recent_records: list[RecordResponse]
    transaction_count: int
