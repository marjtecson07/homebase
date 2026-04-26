from datetime import timedelta

from jose import jwt

from app.auth import create_access_token, hash_password, verify_password
from app.config import settings


class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        hashed = hash_password("mypassword")
        assert isinstance(hashed, str)

    def test_hash_is_not_plain_text(self):
        hashed = hash_password("mypassword")
        assert hashed != "mypassword"

    def test_verify_correct_password(self):
        hashed = hash_password("mypassword")
        assert verify_password("mypassword", hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("mypassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_same_password_different_hashes(self):
        """bcrypt generates a new salt each time"""
        hash1 = hash_password("mypassword")
        hash2 = hash_password("mypassword")
        assert hash1 != hash2


class TestJWTTokens:
    def test_create_access_token(self):
        token = create_access_token(data={"sub": "test@test.com"})
        assert isinstance(token, str)

    def test_token_contains_correct_email(self):
        token = create_access_token(data={"sub": "test@test.com"})
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        assert payload["sub"] == "test@test.com"

    def test_token_expires(self):
        token = create_access_token(
            data={"sub": "test@test.com"}, expires_delta=timedelta(minutes=30)
        )
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        assert "exp" in payload
