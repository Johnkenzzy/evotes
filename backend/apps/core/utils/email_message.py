"""Defines the voter email message and code assigning functions."""
from django.core.mail import send_mail
from django.conf import settings


def send_voter_email(voter, title=None, expires_at=None):
    """Send an email to the voter with their sign-in code."""
    if not expires_at:
        expires_at = "12 hours"
    if not title:
        title = "Election"

    uri = f"{settings.FRONTEND_URL}/auth/verify_voter"
    sign_in_link = f"{uri}?email={voter.email}&code={voter.sign_in_code}"
    subject = f"{title} Voting Access Link"
    message = f"""Hello {voter.full_name},\n
        Your sign-in code is: {voter.sign_in_code}
        Or click the link below to verify:
        {sign_in_link}\n
        This code will expire in {expires_at}.
        """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [voter.email])


def assign_voter_code(voter, title=None, expires_at=None):
    """Assigns a sign-in code and send email to a voter."""
    voter.generate_sign_in_code(expires_at=expires_at)
    voter.is_verified = False
    voter.save()
    send_voter_email(
        voter,
        title,
        expires_at=expires_at)
