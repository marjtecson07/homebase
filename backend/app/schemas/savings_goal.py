from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SavingsGoalBase(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0
    target_date: Optional[date] = None


class SavingsGoalCreate(SavingsGoalBase):
    pass


class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    target_date: Optional[date] = None


class SavingsGoalResponse(SavingsGoalBase):
    id: UUID
    household_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
