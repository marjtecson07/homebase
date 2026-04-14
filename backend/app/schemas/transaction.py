from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date as date_type
from typing import Optional
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    description: str
    amount: float
    type: TransactionType
    date: date_type
    is_shared: bool = False
    category_id: Optional[UUID] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    date: Optional[date_type] = None
    is_shared: Optional[bool] = None
    category_id: Optional[UUID] = None

class TransactionResponse(TransactionBase):
    id: UUID
    household_id: UUID
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True