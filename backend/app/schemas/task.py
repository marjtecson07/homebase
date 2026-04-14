from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from app.models.task import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[date] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    category_id: Optional[UUID] = None
    assigned_to_id: Optional[UUID] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = None
    category_id: Optional[UUID] = None
    assigned_to_id: Optional[UUID] = None

class TaskResponse(TaskBase):
    id: UUID
    household_id: UUID
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True