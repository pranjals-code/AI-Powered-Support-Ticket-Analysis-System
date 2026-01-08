import pytest
from app.tickets.schemas import TicketCreate, TicketResponse, TicketStatusUpdate
from app.core.enums import TicketStatus, TicketPriority, TicketCategory
from datetime import datetime


# Unit test for TicketCreate schema
def test_ticket_create_schema():
    ticket = TicketCreate(
        title="Issue with login", description="Cannot login to the system."
    )
    assert ticket.title == "Issue with login"
    assert ticket.description == "Cannot login to the system."


# Unit test for TicketResponse schema
def test_ticket_response_schema():
    now = datetime.utcnow()
    ticket = TicketResponse(
        id=1,
        title="Issue with login",
        description="Cannot login to the system.",
        status=TicketStatus.CREATED,
        priority=TicketPriority.LOW,
        category=TicketCategory.TECHNICAL,
        created_at=now,
    )
    assert ticket.id == 1
    assert ticket.status == TicketStatus.CREATED
    assert ticket.priority == TicketPriority.LOW
    assert ticket.category == TicketCategory.TECHNICAL
    assert ticket.created_at == now


# Unit test for TicketStatusUpdate schema
def test_ticket_status_update_schema():
    status_update = TicketStatusUpdate(status=TicketStatus.RESOLVED)
    assert status_update.status == TicketStatus.RESOLVED
