from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/household", response_model=list[UserResponse])
def get_household_members(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.get_household_members(current_user.household_id)
