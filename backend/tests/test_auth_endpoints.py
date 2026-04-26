

class TestRegisterEndpoint:
    def test_register_new_user(self, client, test_user_data):
        response = client.post("/auth/register", json=test_user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client, test_user_data):
        client.post("/auth/register", json=test_user_data)
        response = client.post("/auth/register", json=test_user_data)

        assert response.status_code == 400

    def test_register_invalid_email(self, client):
        response = client.post(
            "/auth/register",
            json={
                "email": "notanemail",
                "full_name": "Test User",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    def test_register_missing_fields(self, client):
        response = client.post("/auth/register", json={"email": "test@test.com"})
        assert response.status_code == 422


class TestLoginEndpoint:
    def test_login_valid_credentials(self, client, test_user_data, registered_user):
        response = client.post(
            "/auth/login",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user_data, registered_user):
        response = client.post(
            "/auth/login",
            data={"username": test_user_data["email"], "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "nobody@test.com", "password": "password123"},
        )
        assert response.status_code == 401


class TestProtectedEndpoints:
    def test_get_me_without_token(self, client):
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_get_me_with_token(self, client, test_user_data, auth_headers):
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == test_user_data["email"]
