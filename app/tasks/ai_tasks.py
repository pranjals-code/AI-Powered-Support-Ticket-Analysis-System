from __future__ import annotations

from typing import Optional

from app.core.celery_app import celery_app
from app.core.ai_client import classify_ticket_sync
from app.core.database import SessionLocal
from app.core.enums import TicketCategory, TicketStatus, UserRole
from app.tickets.models import Ticket
from app.users.models import User

CATEGORY_EMAIL_HINTS = {
    TicketCategory.BILLING: ["billing", "finance", "invoice"],
    TicketCategory.TECHNICAL: ["tech", "support", "it", "dev"],
    TicketCategory.ACCOUNT: ["account", "acct", "customer"],
}


def _select_agent_for_category(
    db: SessionLocal,
    category: Optional[TicketCategory],
) -> Optional[User]:
    agents = (
        db.query(User).filter(User.role == UserRole.AGENT).order_by(User.id.asc()).all()
    )

    if not agents:
        return None

    if category:
        hints = CATEGORY_EMAIL_HINTS.get(category, [])
        if hints:
            for agent in agents:
                email = agent.email.lower()
                if any(hint in email for hint in hints):
                    return agent

    return agents[0]


@celery_app.task(name="tickets.classify_ticket")
def classify_ticket_task(ticket_id: int) -> None:
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return

        result = classify_ticket_sync(ticket.title, ticket.description)
        if not result:
            return

        ticket.priority = result.priority
        ticket.category = result.category
        ticket.status = TicketStatus.ASSIGNED

        agent = _select_agent_for_category(db, result.category)
        ticket.assigned_agent_id = agent.id if agent else None

        db.commit()
    finally:
        db.close()
