from datetime import date


class TestTransactionEndpoints:
    def test_create_transaction(self, client, auth_headers):
        response = client.post(
            "/transactions/",
            json={
                "description": "Grocery run",
                "amount": 50.00,
                "type": "expense",
                "date": str(date.today()),
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Grocery run"
        assert data["amount"] == 50.00
        assert data["type"] == "expense"

    def test_create_transaction_without_auth(self, client):
        response = client.post(
            "/transactions/",
            json={
                "description": "Grocery run",
                "amount": 50.00,
                "type": "expense",
                "date": str(date.today()),
            },
        )
        assert response.status_code == 401

    def test_get_transactions(self, client, auth_headers):
        client.post(
            "/transactions/",
            json={
                "description": "Transaction 1",
                "amount": 100.00,
                "type": "income",
                "date": str(date.today()),
            },
            headers=auth_headers,
        )
        client.post(
            "/transactions/",
            json={
                "description": "Transaction 2",
                "amount": 50.00,
                "type": "expense",
                "date": str(date.today()),
            },
            headers=auth_headers,
        )

        response = client.get("/transactions/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_delete_transaction(self, client, auth_headers):
        create_response = client.post(
            "/transactions/",
            json={
                "description": "Delete me",
                "amount": 25.00,
                "type": "expense",
                "date": str(date.today()),
            },
            headers=auth_headers,
        )
        transaction_id = create_response.json()["id"]

        delete_response = client.delete(
            f"/transactions/{transaction_id}", headers=auth_headers
        )
        assert delete_response.status_code == 204

    def test_invalid_transaction_type(self, client, auth_headers):
        response = client.post(
            "/transactions/",
            json={
                "description": "Bad transaction",
                "amount": 50.00,
                "type": "invalid_type",
                "date": str(date.today()),
            },
            headers=auth_headers,
        )
        assert response.status_code == 422
