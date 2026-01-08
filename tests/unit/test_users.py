import pytest
from app.users.schemas import UserCreate, UserLogin, TokenResponse
from app.core.enums import UserRole


# Unit test for UserCreate schema
@pytest.mark.parametrize(
    "email,password,role",
    [
        ("test@example.com", "password123", UserRole.ADMIN),
        ("admin@example.com", "adminpass", UserRole.AGENT),
        ("manager@example.com", "managerpass", UserRole.MANAGER),
    ],
)
def test_user_create_schema(email, password, role):
    user = UserCreate(email=email, password=password, role=role)
    assert user.email == email
    assert user.password == password
    assert user.role == role


# Unit test for UserLogin schema
def test_user_login_schema():
    login = UserLogin(email="test@example.com", password="password123")
    assert login.email == "test@example.com"
    assert login.password == "password123"


# Unit test for TokenResponse schema
def test_token_response_schema():
    token = TokenResponse(access_token="abc123")
    assert token.access_token == "abc123"
    assert token.token_type == "bearer"
