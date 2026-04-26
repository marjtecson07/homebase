from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    return service.create_task(task_data, current_user)


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.get_household_tasks(current_user)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    return service.get_task(task_id, current_user)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    return service.update_task(task_id, task_data, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    service.delete_task(task_id, current_user)
