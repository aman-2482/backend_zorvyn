from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from ..database import Base


class RecordType(str, Enum):
    """Financial record types"""
    INCOME = "income"
    EXPENSE = "expense"


class Record(Base):
    """Financial record model"""
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(SQLEnum(RecordType), nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to user
    owner = relationship("User", back_populates="records")

    def __repr__(self):
        return f"<Record {self.type} {self.amount} - {self.category}>"
