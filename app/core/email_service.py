"""
Email service for sending OTPs and notifications.

Uses SMTP to send real emails. Configure SMTP settings in .env file.
Falls back to console mode if SMTP is not configured.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending verification and reset OTPs."""

    def __init__(self):
        """Initialize the email service."""
        # Check if SMTP is configured
        self.smtp_configured = bool(
            settings.smtp_username
            and settings.smtp_password
            and settings.smtp_from_email
        )

        if not self.smtp_configured:
            logger.warning(
                "SMTP not configured. Emails will be printed to console. "
                "Please configure SMTP settings in .env file to "
                "send real emails."
            )

    def send_verification_otp(self, email: str, otp: str) -> bool:
        """
        Send email verification OTP to user.

        Args:
            email: Recipient email address
            otp: The OTP code to send

        Returns:
            True if sent successfully, False otherwise
        """
        subject = "Verify Your Email - AI Support Ticket System"
        body = f"""
Hello,

Thank you for signing up for the AI Support Ticket System!

Your email verification code is: {otp}

This code will expire in 15 minutes.

Please enter this code to verify your email address and complete your
registration.

If you didn't request this, please ignore this email.

Best regards,
AI Support Ticket System Team
        """

        return self._send_email(email, subject, body)

    def send_reset_otp(self, email: str, otp: str) -> bool:
        """
        Send password reset OTP to user.

        Args:
            email: Recipient email address
            otp: The OTP code to send

        Returns:
            True if sent successfully, False otherwise
        """
        subject = "Password Reset Request - AI Support Ticket System"
        body = f"""
Hello,

We received a request to reset your password for the AI Support Ticket System.

Your password reset code is: {otp}

This code will expire in 15 minutes.

Please use this code to reset your password. If you didn't request this,
please ignore this email and your password will remain unchanged.

Best regards,
AI Support Ticket System Team
        """

        return self._send_email(email, subject, body)

    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Internal method to send email via SMTP.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.smtp_configured:
            # Fallback to console mode
            print("\n" + "=" * 80)
            print("📧 EMAIL SENT (CONSOLE MODE - SMTP NOT CONFIGURED)")
            print("=" * 80)
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("-" * 80)
            print(body)
            print("=" * 80 + "\n")
            return True

        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            msg["To"] = to_email
            msg["Subject"] = subject

            # Add body
            msg.attach(MIMEText(body, "plain"))

            # Connect to SMTP server and send
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            # Fallback to console for debugging
            print("\n" + "=" * 80)
            print(f"⚠️  EMAIL FAILED TO SEND - Error: {str(e)}")
            print("=" * 80)
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("-" * 80)
            print(body)
            print("=" * 80 + "\n")
            return False


# Global email service instance
email_service = EmailService()
