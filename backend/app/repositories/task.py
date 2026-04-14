from typing import List, Any
from app.models.task import Task
from app.repositories.base import BaseRepository
from sqlalchemy.orm import Session

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_by_household(self, household_id: Any) -> List[Task]:
        return self.db.query(Task).filter(
            Task.household_id == household_id
        ).all()

    def get_by_assigned_user(self, user_id: Any) -> List[Task]:
        return self.db.query(Task).filter(
            Task.assigned_to_id == user_id
        ).all()

    def get_by_category(self, category_id: Any) -> List[Task]:
        return self.db.query(Task).filter(
            Task.category_id == category_id
        ).all()