import random
import string
from datetime import datetime, timedelta


def generate_otp(length: int = 6) -> str:
    """
    Generate a random numeric OTP.
    
    Args:
        length: Length of the OTP (default: 6)
    
    Returns:
        A string containing random digits
    """
    return ''.join(random.choices(string.digits, k=length))


def is_otp_expired(expires_at: datetime) -> bool:
    """
    Check if an OTP has expired.
    
    Args:
        expires_at: The expiration datetime
    
    Returns:
        True if expired, False otherwise
    """
    return datetime.utcnow() > expires_at


def get_otp_expiration(minutes: int = 15) -> datetime:
    """
    Get the expiration datetime for an OTP.
    
    Args:
        minutes: Number of minutes until expiration (default: 15)
    
    Returns:
        Datetime object representing the expiration time
    """
    return datetime.utcnow() + timedelta(minutes=minutes)
