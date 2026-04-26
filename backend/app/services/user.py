from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models.household import Household
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> User:
        existing = self.user_repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        household = Household(name=f"{user_data.full_name}'s Household")
        self.db.add(household)
        self.db.flush()

        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
            household_id=household.id,
        )
        return self.user_repo.create(user)

    def get_household_members(self, household_id) -> list[User]:
        return self.user_repo.get_by_household(household_id)
