"""Defines the voter email message and code assigning functions."""
from django.core.mail import send_mail
from django.conf import settings


def send_voter_email(voter, election_title=None, expiration_time=None):
    """Send an email to the voter with their sign-in code."""
    if not expiration_time:
        expiration_time = "12 hours"
    if not election_title:
        election_title = "Election"

    sign_in_link = f"{settings.FRONTEND_URL}/vote/verify?email={
        voter.email}&code={
            voter.sign_in_code}"
    subject = f"{election_title} Voting Access Link"
    message = f"""Hello {voter.full_name},\n
                Your sign-in code is: {voter.sign_in_code}
                Or click the link below to verify:\n
                {sign_in_link}\n
                This code will expire in {expiration_time}."""
    send_mail(
        subject, 
        message,
        settings.DEFAULT_FROM_EMAIL,
        [voter.email])


def assign_voter_code(voter, election_title, expiration_time=None):
    """Assigns a sign-in code and send email to a voter."""
    voter.generate_sign_in_code(expiration_time=expiration_time)
    voter.save()
    send_voter_email(
        voter,
        election_title,
        expiration_time=expiration_time)