from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TimestampMixin
from app.database import Base

class User(Base, TimestampMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    household_id = Column(UUID(as_uuid=True), ForeignKey("households.id"), nullable=True)

    household = relationship("Household", back_populates="users")
    created_tasks = relationship("Task", foreign_keys="Task.created_by_id", 
                                  back_populates="created_by")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to_id", 
                                   back_populates="assigned_to")
    transactions = relationship("Transaction", back_populates="created_by")