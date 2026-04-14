import enum
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TimestampMixin
from app.database import Base

class CategoryType(str, enum.Enum):
    task = "task"
    finance = "finance"
    both = "both"

class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    type = Column(Enum(CategoryType), nullable=False, default=CategoryType.both)
    household_id = Column(UUID(as_uuid=True), ForeignKey("households.id"), nullable=False)

    household = relationship("Household", back_populates="categories")
    tasks = relationship("Task", back_populates="category")
    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")