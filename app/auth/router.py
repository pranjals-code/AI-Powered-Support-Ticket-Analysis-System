from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.users.models import User
from app.users.schemas import (
    UserCreate,
    UserLogin,
    SignupResponse,
    LoginResponse,
    LogoutResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)
from app.core.security.password import hash_password, verify_password
from app.core.security.jwt import create_access_token
from app.core.security.otp import (
    generate_otp,
    is_otp_expired,
    get_otp_expiration,
)
from app.core.email_service import email_service
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user and send email verification OTP.
    User must verify email before they can login.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    # Generate OTP for email verification
    otp = generate_otp()
    otp_expires = get_otp_expiration()

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
        is_verified=False,
        verification_otp=otp,
        verification_otp_expires=otp_expires,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send verification email
    email_service.send_verification_otp(new_user.email, otp)

    return {
        "message": (
            "Account created successfully. "
            "Please check your email for verification code."
        ),
        "user_id": new_user.id,
        "email": new_user.email,
        "role": new_user.role,
    }


@router.post("/verify-email", response_model=VerifyEmailResponse)
def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    """
    Verify user's email address using OTP sent during signup.
    """
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified",
        )

    if not user.verification_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verification OTP found. Please request a new one.",
        )

    if user.verification_otp != request.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP",
        )

    if is_otp_expired(user.verification_otp_expires):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new one.",
        )

    # Mark user as verified and clear OTP
    user.is_verified = True
    user.verification_otp = None
    user.verification_otp_expires = None
    db.commit()

    return {
        "message": "Email verified successfully. You can now login.",
        "email": user.email,
    }


@router.post("/resend-verification", response_model=SignupResponse)
def resend_verification(email: str, db: Session = Depends(get_db)):
    """
    Resend verification OTP to user's email.
    """
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified",
        )

    # Generate new OTP
    otp = generate_otp()
    otp_expires = get_otp_expiration()

    user.verification_otp = otp
    user.verification_otp_expires = otp_expires
    db.commit()

    # Send verification email
    email_service.send_verification_otp(user.email, otp)

    return {
        "message": "Verification code sent to your email.",
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
    }


@router.post("/login", response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login user with email and password.
    Email must be verified before login is allowed.
    """
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(
        user.password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Check if email is verified
    if not db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Email not verified. " "Please verify your email before logging in."
            ),
        )

    access_token = create_access_token(
        data={"sub": str(db_user.id), "role": db_user.role}
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request password reset OTP.
    Sends OTP to user's registered email address.
    """
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        # Don't reveal if user exists or not for security
        return {
            "message": ("If the email exists, a password reset code has been sent."),
        }

    # Generate OTP for password reset
    otp = generate_otp()
    otp_expires = get_otp_expiration()

    user.reset_otp = otp
    user.reset_otp_expires = otp_expires
    db.commit()

    # Send reset email
    email_service.send_reset_otp(user.email, otp)

    return {
        "message": "If the email exists, a password reset code has been sent.",
    }


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset user password using OTP.
    Validates OTP and updates password.
    """
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.reset_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No password reset request found. "
                "Please request a password reset first."
            ),
        )

    if user.reset_otp != request.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP",
        )

    if is_otp_expired(user.reset_otp_expires):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new password reset.",
        )

    # Update password and clear reset OTP
    user.hashed_password = hash_password(request.new_password)
    user.reset_otp = None
    user.reset_otp_expires = None
    db.commit()

    return {
        "message": (
            "Password reset successfully. " "You can now login with your new password."
        ),
    }


@router.post("/logout", response_model=LogoutResponse)
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint.
    Requires valid authentication token.
    Client should delete the token after receiving this response.
    """
    return {"message": "Logout successful"}
