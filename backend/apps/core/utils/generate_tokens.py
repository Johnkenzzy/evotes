"""Defines a function to generate JWT tokens for admins and voters."""
import jwt
import uuid
from django.conf import settings
from datetime import datetime, timedelta


def generate_jwt_token(admin):
    """Generates a JWT token for an admin."""
    access_payload = {
        'admin_id': str(admin.id),
        'email': admin.email,
        'role': admin.role,
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'type': 'access',
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4())
    }

    refresh_payload = {
        'admin_id': str(admin.id),
        'email': admin.email,
        'role': admin.role,
        'exp': datetime.utcnow() + timedelta(days=7),
        'type': 'refresh',
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4())
    }

    access_token = jwt.encode(
         access_payload,
         settings.SECRET_KEY,
         algorithm='HS256')
    refresh_token = jwt.encode(
         refresh_payload,
         settings.SECRET_KEY,
         algorithm='HS256')

    return {
        'access': access_token,
        'refresh': refresh_token
    }

def generate_voter_token(voter):
    """Generates a JWT token for a voter."""
    payload = {
        'voter_id': str(voter.id),
        'email': voter.email,
        'exp': datetime.utcnow() + timedelta(hours=2),
        'iat': datetime.utcnow(),
        'type': 'voter_access'
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256')