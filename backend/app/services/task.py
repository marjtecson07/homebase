from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.repositories.task import TaskRepository
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)

    def create_task(self, task_data: TaskCreate, 
                    current_user: User) -> Task:
        task = Task(
            **task_data.model_dump(),
            household_id=current_user.household_id,
            created_by_id=current_user.id
        )
        return self.task_repo.create(task)

    def get_household_tasks(self, current_user: User) -> list[Task]:
        return self.task_repo.get_by_household(current_user.household_id)

    def get_task(self, task_id: UUID, current_user: User) -> Task:
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        if str(task.household_id) != str(current_user.household_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task

    def update_task(self, task_id: UUID, 
                    task_data: TaskUpdate, current_user: User) -> Task:
        task = self.get_task(task_id, current_user)
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        return self.task_repo.update(task)

    def delete_task(self, task_id: UUID, current_user: User) -> None:
        task = self.get_task(task_id, current_user)
        self.task_repo.delete(task)