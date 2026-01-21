from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from app.core.database import Base
from app.core.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    
    # Email verification fields
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_otp = Column(String, nullable=True)
    verification_otp_expires = Column(DateTime, nullable=True)
    
    # Password reset fields
    reset_otp = Column(String, nullable=True)
    reset_otp_expires = Column(DateTime, nullable=True)
