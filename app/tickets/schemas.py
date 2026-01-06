from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.enums import TicketStatus, TicketPriority, TicketCategory


# -------------------------
# Request schema (frontend → backend)
# -------------------------
class TicketCreate(BaseModel):
    title: str
    description: str


# -------------------------
# Response schema (backend → frontend)
# -------------------------
class TicketResponse(BaseModel):
    id: int
    title: str
    description: str

    status: TicketStatus
    priority: Optional[TicketPriority]
    category: Optional[TicketCategory]

    created_at: datetime

    class Config:
        from_attributes = True


class TicketStatusUpdate(BaseModel):
    status: TicketStatus
