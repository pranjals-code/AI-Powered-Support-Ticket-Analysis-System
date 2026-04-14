from fastapi import APIRouter, Depends, status, File, UploadFile, Form, Query
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException
import math

from app.core.s3 import upload_file_to_s3
from app.core.database import get_db
from app.tickets.models import Ticket
from app.tickets.schemas import (
    TicketResponse,
    PaginatedTicketResponse,
    DeleteResponseMessage,
)
from app.core.enums import TicketStatus, UserRole
from app.tasks.ai_tasks import classify_ticket_task
from app.auth.dependencies import get_current_user
from app.users.models import User

# File size limits
MAX_PHOTO_SIZE = 6 * 1024 * 1024  # 6 MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def _can_view_ticket(ticket: Ticket, user: User) -> bool:
    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        return True
    if user.role == UserRole.AGENT:
        return ticket.assigned_agent_id == user.id
    return ticket.created_by == user.id


def _apply_ticket_rbac_filter(query, user: User):
    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        return query
    if user.role == UserRole.AGENT:
        return query.filter(Ticket.assigned_agent_id == user.id)
    return query.filter(Ticket.created_by == user.id)


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

    if not (photo or remove_photo or file or remove_file):
        return

    if not is_creator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the ticket creator can add/remove attachments"
        )

    # ✅ PHOTO upload
    if photo:
        photo_content = await photo.read()
        if len(photo_content) > MAX_PHOTO_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Photo size must be less than 6 MB"
            )

        ticket.photo = upload_file_to_s3(photo.file, photo.filename)
        ticket.photo_filename = photo.filename

    # ❌ remove photo
    if remove_photo:
        ticket.photo = None
        ticket.photo_filename = None

    # ✅ FILE upload
    if file:
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size must be less than 10 MB"
            )

        ticket.file = upload_file_to_s3(file.file, file.filename)
        ticket.file_filename = file.filename

    # ❌ remove file
    if remove_file:
        ticket.file = None
        ticket.file_filename = None

@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    openapi_extra={
        "requestBody": {
            "content": {
                "multipart/form-data": {}
            }
        }
    }
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
    """

    photo_url = None
    file_url = None

    # ✅ PHOTO upload to S3
    if photo:
        photo_content = await photo.read()
        if len(photo_content) > MAX_PHOTO_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Photo size must be less than 6 MB",
            )

        photo_url = upload_file_to_s3(photo)

    # ✅ FILE upload to S3
    if file:
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10 MB",
            )

        file_url = upload_file_to_s3(file.file, file.filename)

    ticket = Ticket(
        title=title,
        description=description,
        status=TicketStatus.CREATED,
        created_by=current_user.id,
        photo=photo_url,          # ✅ URL stored
        photo_filename=photo.filename if photo else None,
        file=file_url,            # ✅ URL stored
        file_filename=file.filename if file else None,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    classify_ticket_task.delay(ticket.id)

    return ticket

@router.get(
    "",
    response_model=PaginatedTicketResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
):
    """
    Get all tickets with pagination and sorting.

    Query Parameters:
    - page: Page number (default: 1)
    - size: Items per page (default: 10, max: 100)
    - sort_by: Field to sort by (default: created_at)
    - order: Sort order - 'asc' or 'desc' (default: desc)
    - status: Filter by ticket status (optional)
    - search: Search in title and description (optional)
    """
    # Validate sort_by field
    valid_sort_fields = {
        "created_at": Ticket.created_at,
        "updated_at": Ticket.updated_at,
        "title": Ticket.title,
        "status": Ticket.status,
        "priority": Ticket.priority,
    }

    if sort_by not in valid_sort_fields:
        sort_by = "created_at"

    # Build base query
    query = db.query(Ticket)
    query = _apply_ticket_rbac_filter(query, current_user)

    # Apply status filter if provided
    if status:
        try:
            ticket_status = TicketStatus[status.upper()]
            query = query.filter(Ticket.status == ticket_status)
        except KeyError:
            pass  # Invalid status, ignore filter

    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Ticket.title.ilike(search_term)) | (Ticket.description.ilike(search_term))
        )

    # Get total count before pagination
    total = query.count()

    # Apply sorting
    sort_column = valid_sort_fields[sort_by]
    if order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Apply pagination
    offset = (page - 1) * size
    tickets = query.offset(offset).limit(size).all()

    # Calculate total pages
    total_pages = math.ceil(total / size) if total > 0 else 1

    return PaginatedTicketResponse(
        data=tickets,
        total=total,
        page=page,
        size=size,
        pages=total_pages,
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
def get_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if not _can_view_ticket(ticket, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this ticket",
        )

    return ticket


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
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if current_user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        pass
    elif current_user.role == UserRole.AGENT:
        if ticket.assigned_agent_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Agents can only update assigned tickets",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only agents, managers, and admins can update ticket status",
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

    if not _can_view_ticket(ticket, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this ticket",
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


@router.delete(
    "/{ticket_id}",
    response_model=DeleteResponseMessage,
    status_code=status.HTTP_200_OK,
)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a ticket by ID.
    Only MANAGER and ADMIN roles can delete tickets.
    Only CLOSED tickets can be deleted. Tickets in other statuses
    cannot be deleted.
    USER role cannot delete any ticket.

    Responses:
    - 200: Ticket deleted successfully
    - 400: Ticket must be in CLOSED status to delete
    - 403: Only managers and admins can delete tickets
    - 404: Ticket ID does not exist
    """
    # Check if user is MANAGER or ADMIN
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can delete tickets",
        )

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket ID {ticket_id} does not exist",
        )

    # Check if ticket status is CLOSED
    if ticket.status != TicketStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Ticket must be in CLOSED status to delete. "
                f"Current status: {ticket.status.value}"
            ),
        )

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully"}
