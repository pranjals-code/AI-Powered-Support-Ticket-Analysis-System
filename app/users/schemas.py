from pydantic import BaseModel, EmailStr, field_validator
from app.core.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


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


class LogoutResponse(BaseModel):
    message: str


# Email Verification Schemas
class VerifyEmailRequest(BaseModel):
    email: EmailStr
    otp: str


class VerifyEmailResponse(BaseModel):
    message: str
    email: str


# Forgot Password Schemas
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str


# Reset Password Schemas
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v


class ResetPasswordResponse(BaseModel):
    message: str
