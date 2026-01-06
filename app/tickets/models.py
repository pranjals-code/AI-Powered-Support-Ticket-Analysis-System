from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Enum as SqlEnum,
)
from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enums import TicketStatus, TicketPriority, TicketCategory


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    status = Column(
        SqlEnum(TicketStatus),
        default=TicketStatus.CREATED,
        nullable=False,
    )

    priority = Column(
        SqlEnum(TicketPriority),
        nullable=True,  # AI will set this later
    )

    category = Column(
        SqlEnum(TicketCategory),
        nullable=True,  # AI will set this later
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    assigned_agent_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
