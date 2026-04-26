from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


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
