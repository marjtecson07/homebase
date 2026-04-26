

class TestTaskEndpoints:
    def test_create_task(self, client, auth_headers):
        response = client.post(
            "/tasks/",
            json={"title": "Buy groceries", "priority": "high"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["priority"] == "high"
        assert data["status"] == "todo"

    def test_create_task_without_auth(self, client):
        response = client.post("/tasks/", json={"title": "Buy groceries"})
        assert response.status_code == 401

    def test_create_task_missing_title(self, client, auth_headers):
        response = client.post(
            "/tasks/", json={"priority": "high"}, headers=auth_headers
        )
        assert response.status_code == 422

    def test_get_tasks(self, client, auth_headers):
        # Create two tasks
        client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers)
        client.post("/tasks/", json={"title": "Task 2"}, headers=auth_headers)

        response = client.get("/tasks/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_tasks_without_auth(self, client):
        response = client.get("/tasks/")
        assert response.status_code == 401

    def test_update_task(self, client, auth_headers):
        create_response = client.post(
            "/tasks/", json={"title": "Update me"}, headers=auth_headers
        )
        task_id = create_response.json()["id"]

        response = client.put(
            f"/tasks/{task_id}", json={"status": "done"}, headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "done"

    def test_delete_task(self, client, auth_headers):
        create_response = client.post(
            "/tasks/", json={"title": "Delete me"}, headers=auth_headers
        )
        task_id = create_response.json()["id"]

        delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert delete_response.status_code == 204

        get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_tasks_isolated_between_households(self, client, test_user_data):
        # Register two different users
        user2_data = {
            "email": "user2@test.com",
            "full_name": "User Two",
            "password": "password123",
        }
        client.post("/auth/register", json=test_user_data)
        client.post("/auth/register", json=user2_data)

        # Login as user 1
        login1 = client.post(
            "/auth/login",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"],
            },
        )
        headers1 = {"Authorization": f"Bearer {login1.json()['access_token']}"}

        # Login as user 2
        login2 = client.post(
            "/auth/login",
            data={"username": user2_data["email"], "password": user2_data["password"]},
        )
        headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

        # User 1 creates a task
        client.post("/tasks/", json={"title": "User 1 private task"}, headers=headers1)

        # User 2 should not see User 1's tasks
        response = client.get("/tasks/", headers=headers2)
        assert len(response.json()) == 0
