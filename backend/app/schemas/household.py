from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class HouseholdBase(BaseModel):
    name: str

class HouseholdCreate(HouseholdBase):
    pass

class HouseholdResponse(HouseholdBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True