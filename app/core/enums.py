from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"
    MANAGER = "MANAGER"


class TicketStatus(str, Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketCategory(str, Enum):
    BILLING = "BILLING"
    TECHNICAL = "TECHNICAL"
    ACCOUNT = "ACCOUNT"
    OTHER = "OTHER"
