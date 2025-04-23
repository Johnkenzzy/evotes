"""Defines and admin and voters authentication classes."""
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings
from apps.organizations.models import OrganizationAdmin
from apps.voters.models import Voter
from apps.auth_and_auth.models import BlacklistedToken



class AdminJWTAuthentication(BaseAuthentication):
    """Authenticates admin users using JWT tokens."""
    def authenticate(self, request):
        """Authenticates a request."""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])
            token_type = payload.get('type')
            if token_type not in ['access', 'refresh']:
                raise AuthenticationFailed('Invalid token type')

            # Check if token has been blacklisted
            jti = payload.get('jti')
            if jti and BlacklistedToken.objects.filter(jti=jti).exists():
                raise AuthenticationFailed('Token has been blacklisted')

            admin = OrganizationAdmin.objects.get(id=payload['admin_id'])
            request.admin = admin
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token')
        except OrganizationAdmin.DoesNotExist:
            raise AuthenticationFailed('Admin not found')

        return (admin, None)  # Sets request.user = admin


class VoterJWTAuthentication(BaseAuthentication):
    """Authenticates voter users using JWT tokens."""
    def authenticate(self, request):
        """Authenticates a request."""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])
            if payload.get('type') != 'voter_access':
                raise AuthenticationFailed('Invalid token type')
            voter = Voter.objects.get(id=payload['voter_id'])
            request.voter = voter
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            raise AuthenticationFailed('Invalid or expired token')
        except Voter.DoesNotExist:
            raise AuthenticationFailed('Voter not found')

        return (voter, None)