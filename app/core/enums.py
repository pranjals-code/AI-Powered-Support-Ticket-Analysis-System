from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"
    MANAGER = "MANAGER"
