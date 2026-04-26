from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BudgetBase(BaseModel):
    amount: float
    month: int
    year: int
    category_id: UUID


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    amount: Optional[float] = None


class BudgetResponse(BudgetBase):
    id: UUID
    household_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
