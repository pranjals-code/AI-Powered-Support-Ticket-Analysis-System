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
    # Files uploaded via multipart/form-data


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

    photo_filename: Optional[str]
    file_filename: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Paginated Response
# -------------------------
class PaginatedTicketResponse(BaseModel):
    data: list[TicketResponse]
    total: int
    page: int
    size: int
    pages: int


class DeleteResponseMessage(BaseModel):
    message: str


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TicketFullUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    # For file uploads, we'll use binary data in multipart/form-data
    # These are not in the JSON body but in form data
