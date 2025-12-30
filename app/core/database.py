from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# -------------------------------------------------
# Database Engine
# -------------------------------------------------
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# -------------------------------------------------
# Session Factory
# -------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# -------------------------------------------------
# Base class for all SQLAlchemy models
# -------------------------------------------------
Base = declarative_base()

# -------------------------------------------------
# FastAPI dependency to get DB session
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
