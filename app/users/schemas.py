from pydantic import BaseModel, EmailStr
from app.core.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRoleUpdate(BaseModel):
    email: EmailStr
    role: UserRole


class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    message: str = "Login successful"


class SignupResponse(BaseModel):
    message: str
    user_id: int
    email: str
    role: UserRole


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
