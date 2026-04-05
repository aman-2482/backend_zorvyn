from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.record import DashboardSummary
from ..services.record_service import RecordService
from ..utils.dependencies import get_current_user, CurrentUser

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard summary (all authenticated users can access)"""
    return RecordService.get_dashboard_summary(db, current_user.user_id)


@router.get("/categories", response_model=dict)
def get_category_distribution(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get category-wise income and expense breakdown"""
    return RecordService.get_category_distribution(db, current_user.user_id)


@router.get("/trends", response_model=dict)
def get_monthly_trends(
    months: int = 6,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly income/expense trends"""
    return RecordService.get_monthly_trends(db, current_user.user_id, months)
