from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import TimestampMixin
from app.database import Base

class Household(Base, TimestampMixin):
    __tablename__ = "households"

    name = Column(String, nullable=False)

    users = relationship("User", back_populates="household")
    categories = relationship("Category", back_populates="household")
    tasks = relationship("Task", back_populates="household")
    transactions = relationship("Transaction", back_populates="household")
    budgets = relationship("Budget", back_populates="household")
    savings_goals = relationship("SavingsGoal", back_populates="household")