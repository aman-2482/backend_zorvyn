from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from ..database import get_db
from ..schemas.record import RecordCreate, RecordUpdate, RecordResponse
from ..services.record_service import RecordService
from ..utils.dependencies import get_current_user, CurrentUser
from ..core.security import check_can_modify, check_admin

router = APIRouter(prefix="/api/records", tags=["records"])


@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    record_create: RecordCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new financial record (Analyst and Admin only)"""
    check_can_modify(current_user.role)
    return RecordService.create_record(db, current_user.user_id, record_create)


@router.get("/all", response_model=list[RecordResponse])
def list_all_records(
    skip: int = 0,
    limit: int = 100,
    record_type: str = Query(None, description="Filter by type (income/expense)"),
    category: str = Query(None, description="Filter by category"),
    start_date: date = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all records across all users (Admin only)."""
    check_admin(current_user.role)
    return RecordService.get_all_records(
        db,
        skip,
        limit,
        record_type,
        category,
        start_date,
        end_date
    )


@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get record by ID (must be owner or admin)"""
    record = RecordService.get_record_by_id(db, record_id)
    
    if current_user.user_id != record.user_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's records"
        )
    
    return record


@router.get("/", response_model=list[RecordResponse])
def list_records(
    skip: int = 0,
    limit: int = 100,
    record_type: str = Query(None, description="Filter by type (income/expense)"),
    category: str = Query(None, description="Filter by category"),
    start_date: date = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's financial records with optional filtering"""
    return RecordService.get_user_records(
        db,
        current_user.user_id,
        skip,
        limit,
        record_type,
        category,
        start_date,
        end_date
    )


@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    record_update: RecordUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a record (must be owner or admin)"""
    check_can_modify(current_user.role)
    
    record = RecordService.get_record_by_id(db, record_id)
    if current_user.user_id != record.user_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other user's records"
        )
    
    return RecordService.update_record(db, record_id, record_update)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a record (must be owner or admin)"""
    check_can_modify(current_user.role)
    
    record = RecordService.get_record_by_id(db, record_id)
    if current_user.user_id != record.user_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other user's records"
        )
    
    RecordService.delete_record(db, record_id)
