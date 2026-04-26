from sqlalchemy import Column, Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class SavingsGoal(Base, TimestampMixin):
    __tablename__ = "savings_goals"

    name = Column(String, nullable=False)
    target_amount = Column(Numeric(10, 2), nullable=False)
    current_amount = Column(Numeric(10, 2), default=0, nullable=False)
    target_date = Column(Date, nullable=True)
    household_id = Column(
        UUID(as_uuid=True), ForeignKey("households.id"), nullable=False
    )

    household = relationship("Household", back_populates="savings_goals")
