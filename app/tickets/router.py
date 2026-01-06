from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.core.database import get_db
from app.tickets.models import Ticket
from app.tickets.schemas import (
    TicketCreate,
    TicketResponse,
    TicketStatusUpdate,
)
from app.core.enums import TicketStatus
from app.auth.dependencies import get_current_user
from app.users.models import User


router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        status=TicketStatus.CREATED,
        created_by=current_user.id,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get(
    "",
    response_model=List[TicketResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    return tickets


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
def update_ticket_status(
    ticket_id: int,
    payload: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    ticket.status = payload.status

    db.commit()
    db.refresh(ticket)

    return ticket
