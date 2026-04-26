import enum

from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import TimestampMixin


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium, nullable=False)
    due_date = Column(Date, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String, nullable=True)
    household_id = Column(
        UUID(as_uuid=True), ForeignKey("households.id"), nullable=False
    )
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    household = relationship("Household", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    created_by = relationship(
        "User", foreign_keys=[created_by_id], back_populates="created_tasks"
    )
    assigned_to = relationship(
        "User", foreign_keys=[assigned_to_id], back_populates="assigned_tasks"
    )
