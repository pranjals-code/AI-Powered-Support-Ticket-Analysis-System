from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException

from app.core.database import get_db
from app.tickets.models import Ticket
from app.tickets.schemas import (
    TicketResponse,
)
from app.core.enums import TicketStatus, UserRole
from app.auth.dependencies import get_current_user
from app.users.models import User


# File size limits
MAX_PHOTO_SIZE = 6 * 1024 * 1024  # 6 MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

router = APIRouter(prefix="/tickets", tags=["Tickets"])


async def _handle_text_update(
    ticket: Ticket,
    title: Optional[str],
    description: Optional[str],
    is_creator: bool,
    is_admin_or_manager: bool,
) -> None:
    """Handle title and description updates with permission checks."""
    if title is None and description is None:
        return

    if not (is_creator or is_admin_or_manager):
        detail_msg = (
            "Only the ticket creator or administrators "
            "can edit title and description"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail_msg,
        )

    if title is not None:
        ticket.title = title
    if description is not None:
        ticket.description = description


async def _handle_file_operations(
    ticket: Ticket,
    photo: Optional[UploadFile],
    file: Optional[UploadFile],
    remove_photo: bool,
    remove_file: bool,
    is_creator: bool,
) -> None:
    """Handle photo and file upload/removal with permission checks."""
    if not (photo or remove_photo or file or remove_file):
        return

    if not is_creator:
        detail_msg = (
            "Only the ticket creator can add or "
            "remove attachments"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail_msg,
        )

    # Handle photo upload
    if photo:
        photo_content = await photo.read()
        if len(photo_content) > MAX_PHOTO_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Photo size must be less than 6 MB",
            )
        ticket.photo = photo_content
        ticket.photo_filename = photo.filename

    # Handle photo removal
    if remove_photo:
        ticket.photo = None
        ticket.photo_filename = None

    # Handle file upload
    if file:
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10 MB",
            )
        ticket.file = file_content
        ticket.file_filename = file.filename

    # Handle file removal
    if remove_file:
        ticket.file = None
        ticket.file_filename = None


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new ticket with optional photo and file attachments.
    Photo size limit: 6 MB
    File size limit: 10 MB
    """
    # Validate photo size
    photo_data = None
    photo_filename = None
    if photo:
        photo_content = await photo.read()
        if len(photo_content) > MAX_PHOTO_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Photo size must be less than 6 MB",
            )
        photo_data = photo_content
        photo_filename = photo.filename

    # Validate file size
    file_data = None
    file_filename = None
    if file:
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10 MB",
            )
        file_data = file_content
        file_filename = file.filename

    ticket = Ticket(
        title=title,
        description=description,
        status=TicketStatus.CREATED,
        created_by=current_user.id,
        photo=photo_data,
        photo_filename=photo_filename,
        file=file_data,
        file_filename=file_filename,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get(
    "",
    response_model=list[TicketResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all tickets ordered by creation date (newest first).
    """
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    return tickets


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
def update_ticket_status(
    ticket_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update ticket status.
    Only MANAGER and ADMIN roles can update ticket status.
    USER role cannot update status.
    """
    # Check if user is MANAGER or ADMIN
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can update ticket status",
        )

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    ticket.status = payload.get("status")

    db.commit()
    db.refresh(ticket)

    return ticket


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
async def update_ticket(
    ticket_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    remove_photo: Optional[bool] = Form(False),
    remove_file: Optional[bool] = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update ticket title, description, and/or attachments.
    Only the ticket creator can edit title and description.
    User can add/remove photos and files when updating.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    # Check if user is the creator or admin/manager
    is_creator = ticket.created_by == current_user.id
    is_admin_or_manager = current_user.role in [
        UserRole.ADMIN,
        UserRole.MANAGER,
    ]

    # Update text fields
    await _handle_text_update(
        ticket,
        title,
        description,
        is_creator,
        is_admin_or_manager,
    )

    # Update files
    await _handle_file_operations(
        ticket,
        photo,
        file,
        remove_photo,
        remove_file,
        is_creator,
    )

    db.commit()
    db.refresh(ticket)

    return ticket
