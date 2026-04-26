from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class Budget(Base, TimestampMixin):
    __tablename__ = "budgets"

    amount = Column(Numeric(10, 2), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    household_id = Column(
        UUID(as_uuid=True), ForeignKey("households.id"), nullable=False
    )
    category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )

    household = relationship("Household", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")
