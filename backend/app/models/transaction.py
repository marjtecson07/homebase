import enum

from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    date = Column(Date, nullable=False)
    is_shared = Column(Boolean, default=False)
    household_id = Column(
        UUID(as_uuid=True), ForeignKey("households.id"), nullable=False
    )
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    household = relationship("Household", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    created_by = relationship("User", back_populates="transactions")
