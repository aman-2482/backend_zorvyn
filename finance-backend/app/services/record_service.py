from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from fastapi import HTTPException, status
from datetime import datetime, timedelta, date
from ..models.record import Record, RecordType
from ..schemas.record import RecordCreate, RecordUpdate, DashboardSummary, RecordResponse


class RecordService:
    """Service for record operations"""

    @staticmethod
    def create_record(db: Session, user_id: int, record_create: RecordCreate) -> Record:
        """Create a new financial record"""
        db_record = Record(
            user_id=user_id,
            amount=record_create.amount,
            type=record_create.type,
            category=record_create.category,
            date=record_create.date,
            notes=record_create.notes
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    @staticmethod
    def get_record_by_id(db: Session, record_id: int) -> Record:
        """Get record by ID"""
        record = db.query(Record).filter(Record.id == record_id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found"
            )
        return record

    @staticmethod
    def get_user_records(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        record_type: str = None,
        category: str = None,
        start_date: date = None,
        end_date: date = None
    ) -> list[Record]:
        """Get records for a user with optional filtering"""
        query = db.query(Record).filter(Record.user_id == user_id)
        
        if record_type:
            try:
                query = query.filter(Record.type == RecordType(record_type))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid record type: {record_type}"
                )
        
        if category:
            query = query.filter(Record.category.ilike(f"%{category}%"))
        
        if start_date:
            # Convert date to datetime at midnight
            start_datetime = datetime.combine(start_date, datetime.min.time())
            query = query.filter(Record.date >= start_datetime)
        
        if end_date:
            # Convert date to datetime at end of day
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.filter(Record.date <= end_datetime)
        
        return query.order_by(desc(Record.date)).offset(skip).limit(limit).all()

    @staticmethod
    def get_all_records(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        record_type: str = None,
        category: str = None,
        start_date: date = None,
        end_date: date = None
    ) -> list[Record]:
        """Get all records across users with optional filtering (admin use)."""
        query = db.query(Record)

        if record_type:
            try:
                query = query.filter(Record.type == RecordType(record_type))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid record type: {record_type}"
                )

        if category:
            query = query.filter(Record.category.ilike(f"%{category}%"))

        if start_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            query = query.filter(Record.date >= start_datetime)

        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.filter(Record.date <= end_datetime)

        return query.order_by(desc(Record.date)).offset(skip).limit(limit).all()

    @staticmethod
    def update_record(db: Session, record_id: int, record_update: RecordUpdate) -> Record:
        """Update a record"""
        record = RecordService.get_record_by_id(db, record_id)
        
        update_data = record_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)
        
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def delete_record(db: Session, record_id: int) -> None:
        """Delete a record"""
        record = RecordService.get_record_by_id(db, record_id)
        db.delete(record)
        db.commit()

    @staticmethod
    def get_dashboard_summary(db: Session, user_id: int) -> DashboardSummary:
        """Get dashboard summary for user"""
        records = db.query(Record).filter(Record.user_id == user_id).all()
        
        total_income = sum(r.amount for r in records if r.type == RecordType.INCOME)
        total_expenses = sum(r.amount for r in records if r.type == RecordType.EXPENSE)
        net_balance = total_income - total_expenses
        
        # Calculate category totals
        category_totals = {}
        for record in records:
            if record.category not in category_totals:
                category_totals[record.category] = 0
            category_totals[record.category] += record.amount if record.type == RecordType.INCOME else -record.amount
        
        # Get recent records (last 5)
        recent_records = sorted(records, key=lambda r: r.date, reverse=True)[:5]
        
        return DashboardSummary(
            total_income=total_income,
            total_expenses=total_expenses,
            net_balance=net_balance,
            category_totals=category_totals,
            recent_records=[RecordResponse.model_validate(r) for r in recent_records],
            transaction_count=len(records)
        )

    @staticmethod
    def get_category_distribution(db: Session, user_id: int) -> dict:
        """Get category-wise income and expense breakdown"""
        records = db.query(Record).filter(Record.user_id == user_id).all()
        
        distribution = {}
        for record in records:
            if record.category not in distribution:
                distribution[record.category] = {"income": 0, "expense": 0}
            
            if record.type == RecordType.INCOME:
                distribution[record.category]["income"] += record.amount
            else:
                distribution[record.category]["expense"] += record.amount
        
        return distribution

    @staticmethod
    def get_monthly_trends(db: Session, user_id: int, months: int = 6) -> dict:
        """Get monthly income/expense trends"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30 * months)
        
        records = db.query(Record).filter(
            and_(Record.user_id == user_id, Record.date >= start_date)
        ).all()
        
        trends = {}
        for record in records:
            month_key = record.date.strftime("%Y-%m")
            if month_key not in trends:
                trends[month_key] = {"income": 0, "expense": 0}
            
            if record.type == RecordType.INCOME:
                trends[month_key]["income"] += record.amount
            else:
                trends[month_key]["expense"] += record.amount
        
        return dict(sorted(trends.items()))
