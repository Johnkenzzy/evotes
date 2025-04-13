import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings
from apps.organizations.models import OrganizationAdmin



class AdminJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])
            admin = OrganizationAdmin.objects.get(id=payload['admin_id'])
            request.admin = admin
        except (jwt.ExpiredSignatureError, jwt.DecodeError, OrganizationAdmin.DoesNotExist):
            raise AuthenticationFailed('Invalid or expired token')

        return (admin, None)  # admin will be set as request.user
