"""Defines admin and voter authentication views."""
import jwt
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from apps.organizations.models import Organization, OrganizationAdmin
from apps.organizations.views import OrganizationSerializer, OrganizationAdminSerializer
from apps.voters.models import Voter
from .models import BlacklistedToken
from apps.core.utils.generate_tokens import generate_jwt_token, generate_voter_token


@api_view(['POST'])
def admin_login(request):
    """Authenticate an admin and return a JWT token."""
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response(
            {'error': "Password and email are required"},
            status=status.HTTP_400_BAD_REQUEST)

    try:
        admin = OrganizationAdmin.objects.get(email=email)
        if not check_password(password, admin.password):
            raise Exception()
    except:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED)

    token = generate_jwt_token(admin)
    admin.last_login = timezone.now()
    admin.save()
    return Response(
        {'tokens': token,
         'admin_id': admin.id,
         'role': admin.role,
         'organization_id': admin.organization.id}
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
            org_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
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
            admin_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
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

        # Decode token to extract the jti
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=['HS256'])

        if payload.get("type") != "refresh":
            return Response(
                {"error": "Only refresh tokens can be blacklisted."},
                status=status.HTTP_400_BAD_REQUEST)

        jti = payload.get("jti")
        if not jti:
            return Response(
                {"error": "Token has no jti"},
                status=status.HTTP_400_BAD_REQUEST)

        # Blacklist it
        BlacklistedToken.objects.get_or_create(jti=jti)

        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_205_RESET_CONTENT)

    except jwt.ExpiredSignatureError:
        return Response(
            {"error": "Token has expired"},
            status=status.HTTP_400_BAD_REQUEST)
    except jwt.DecodeError:
        return Response(
            {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_voter(request):
    """Verify a voter's email address."""
    email = request.data.get("email")
    code = request.data.get("code")

    try:
        voter = Voter.objects.get(email=email, sign_in_code=code)

        if voter.expires_at > timezone.now():
            return Response(
                {"error": "Code expired"},
                status=400)

        if voter.is_verified:
            token = generate_voter_token(voter)
            return Response(
                {"tokens": {"access": token},
                "voter_id": voter.id,
                "organization_id": voter.organization.id},
                status=status.HTTP_200_OK)

        voter.is_verified = True
        voter.save()

        token = generate_voter_token(voter)
        return Response(
            {"tokens": token,
             "voter_id": voter.id,
             "organization_id": voter.organization.id},
             status=status.HTTP_200_OK)

    except Voter.DoesNotExist:
        return Response(
            {"error": "Invalid email or code"},
            status=status.HTTP_400_BAD_REQUEST)