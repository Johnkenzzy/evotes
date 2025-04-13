import jwt
import uuid
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from apps.organizations.models import OrganizationAdmin
from datetime import datetime, timedelta

from apps.organizations.models import Organization, OrganizationAdmin
from apps.organizations.views import OrganizationSerializer, OrganizationAdminSerializer


SECRET_KEY = settings.SECRET_KEY

def generate_jwt_token(admin):
    access_payload = {
        'admin_id': str(admin.id),
        'email': admin.email,
        'role': admin.role,
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4()),
        'type': 'access'
    }

    refresh_payload = {
        'admin_id': str(admin.id),
        'email': admin.email,
        'role': admin.role,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4()),
        'type': 'refresh'
    }

    access_token = jwt.encode(
         access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(
         refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access': access_token,
        'refresh': refresh_token
    }


@api_view(['POST'])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        admin = OrganizationAdmin.objects.get(email=email)
        if not check_password(password, admin.password):
            raise Exception()
    except:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED)

    token = generate_jwt_token(admin)
    return Response(
        {'tokens': token,
         'admin_id': admin.id, 'role': admin.role}
        )


@api_view(['POST'])
def register(request):
    """Register a new organization and create a superadmin for it."""
    if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
    data = request.data
    org_name = data.get('organization_name', None)
    org_email = data.get('organization_email', None)
    admin_name = data.get('admin_name', None)
    admin_email = data.get('admin_email', None)
    password = data.get('password', None)

    if not org_name or not org_email:
        return Response(
            {"error": "Organization name and email are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not admin_name or not admin_email or not password:
        return Response(
            {"error": "Admin fullname, email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if Organization.objects.filter(email=org_email).exists():
            return Response(
                {"error": "Organization with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
    # Create the organization
    org_data = {
        "name": org_name,
        "email": org_email
        }
    org_serializer = OrganizationSerializer(data=org_data)
    if not org_serializer.is_valid():
        return Response(
            org_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    organization = org_serializer.save()
    # Create the superadmin
    admin_data = {
        "full_name": admin_name,
        "email": admin_email,
        "is_superuser": True,
        "role": "superadmin",
        "password": password,
        "organization": organization.id
        }
    admin_serializer = OrganizationAdminSerializer(data=admin_data)
    if not admin_serializer.is_valid():
        organization.delete()
        return Response(
            admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    admin_serializer.save()

    return Response({
        "organization": org_serializer.data,
        "superadmin": admin_serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logs out a user by blacklisting their refresh token."""
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                 {"error": "Refresh token required"},
                 status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
             {"message": "Successfully logged out"},
             status=status.HTTP_205_RESET_CONTENT)

    except Exception as e:
        return Response(
             {"error": str(e)},
             status=status.HTTP_400_BAD_REQUEST)