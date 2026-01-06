from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt

from app.core.database import get_db
from app.core.config import settings
from app.users.models import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        print("JWT PAYLOAD:", payload)  # 👈 ADD THIS

        user_id = int(payload.get("sub"))

    except Exception as e:  # 👈 CATCH EVERYTHING TEMPORARILY
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
