from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.category import CategoryType

class CategoryBase(BaseModel):
    name: str
    type: CategoryType

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID
    household_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True