from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.users.models import User
from app.users.schemas import UserRoleUpdate, UserResponse
from app.core.enums import UserRole
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get the current logged-in user's profile information.
    Returns: id, email, and role
    """
    return current_user


@router.patch(
    "/role",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user_role(
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update user role by email.
    Only ADMIN users can perform this operation.
    """
    # Check if current user is ADMIN
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update user roles",
        )

    # Find user by email
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Update role
    user.role = payload.role

    db.commit()
    db.refresh(user)

    return user
