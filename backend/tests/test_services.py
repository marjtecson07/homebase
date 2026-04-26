import pytest
from fastapi import HTTPException

from app.models.task import TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.user import UserCreate
from app.services.task import TaskService
from app.services.user import UserService


class TestUserService:
    def test_create_user_successfully(self, db):
        service = UserService(db)
        user_data = UserCreate(
            email="new@test.com", full_name="New User", password="password123"
        )
        user = service.create_user(user_data)

        assert user.email == "new@test.com"
        assert user.full_name == "New User"
        assert user.hashed_password != "password123"
        assert user.household_id is not None

    def test_create_user_creates_household(self, db):
        service = UserService(db)
        user_data = UserCreate(
            email="new@test.com", full_name="New User", password="password123"
        )
        user = service.create_user(user_data)
        assert user.household_id is not None

    def test_create_duplicate_user_raises_error(self, db):
        service = UserService(db)
        user_data = UserCreate(
            email="duplicate@test.com", full_name="User One", password="password123"
        )
        service.create_user(user_data)

        with pytest.raises(HTTPException) as exc_info:
            service.create_user(user_data)

        assert exc_info.value.status_code == 400
        assert "already registered" in exc_info.value.detail


class TestTaskService:
    def test_create_task(self, db):
        # First create a user
        user_service = UserService(db)
        user = user_service.create_user(
            UserCreate(
                email="taskuser@test.com", full_name="Task User", password="password123"
            )
        )

        # Then create a task
        task_service = TaskService(db)
        task_data = TaskCreate(title="Buy groceries", priority=TaskPriority.high)
        task = task_service.create_task(task_data, user)

        assert task.title == "Buy groceries"
        assert task.priority == TaskPriority.high
        assert task.status == TaskStatus.todo
        assert task.created_by_id == user.id
        assert task.household_id == user.household_id

    def test_get_household_tasks(self, db):
        user_service = UserService(db)
        user = user_service.create_user(
            UserCreate(
                email="taskuser2@test.com",
                full_name="Task User 2",
                password="password123",
            )
        )

        task_service = TaskService(db)
        task_service.create_task(TaskCreate(title="Task 1"), user)
        task_service.create_task(TaskCreate(title="Task 2"), user)

        tasks = task_service.get_household_tasks(user)
        assert len(tasks) == 2

    def test_update_task_status(self, db):
        user_service = UserService(db)
        user = user_service.create_user(
            UserCreate(
                email="taskuser3@test.com",
                full_name="Task User 3",
                password="password123",
            )
        )

        task_service = TaskService(db)
        task = task_service.create_task(TaskCreate(title="Update me"), user)

        updated = task_service.update_task(
            task.id, TaskUpdate(status=TaskStatus.done), user
        )
        assert updated.status == TaskStatus.done

    def test_get_task_from_different_household_raises_error(self, db):
        user_service = UserService(db)
        user1 = user_service.create_user(
            UserCreate(
                email="user1@test.com", full_name="User 1", password="password123"
            )
        )
        user2 = user_service.create_user(
            UserCreate(
                email="user2@test.com", full_name="User 2", password="password123"
            )
        )

        task_service = TaskService(db)
        task = task_service.create_task(TaskCreate(title="Private task"), user1)

        # User 2 should not be able to access user 1's task
        with pytest.raises(HTTPException) as exc_info:
            task_service.get_task(task.id, user2)

        assert exc_info.value.status_code == 404
