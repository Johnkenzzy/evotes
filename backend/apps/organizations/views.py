from rest_framework.decorators import (api_view,
                                       parser_classes,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from apps.organizations.models import Organization
from apps.organizations.models import OrganizationAdmin
from apps.core.utils.serializers import get_general_serializer
from apps.auth_and_auth.admin import AdminJWTAuthentication
from apps.core.utils.validate_uuid import is_valid_uuid
from apps.core.utils.role_decorator import role_required


class OrganizationSerializer(get_general_serializer(Organization)):
    """Serializer for the Organization model."""
    pass


@api_view(['GET', 'POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def organizations(request):
    """Get all organizations or create a new one."""
    if request.method == 'GET':
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Validate the request data
        if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data.get('name') is None:
            return Response(
                {"error": "Name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        email = request.data.get('email')
        if email is None:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Organization.objects.filter(email=email).exists():
            return Response(
                {"error": "Organization with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the organization
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def organization_detail(request, pk=None):
    """Get, update or delete a single organization by ID."""
    if not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid organization ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    organization = get_object_or_404(Organization, pk=pk)

    if request.method == 'GET':
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = OrganizationSerializer(
            organization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        organization.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)


class OrganizationAdminSerializer(get_general_serializer(OrganizationAdmin)):
    """Serializer for the OrganizationAdmin model."""
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


@api_view(['GET', 'POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin'])
def admins(request):
    """Get all organization admins or create a new one."""
    org_id = request.admin.organization.id

    if request.method == 'GET':
        admins = OrganizationAdmin.objects.filter(organization=org_id)
        serializer = OrganizationAdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Validate the request data
        if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.data.get('email')
        if email is None:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if OrganizationAdmin.objects.filter(
                organization=org_id, email=email).exists():
            return Response({
                "error": "Organization admin with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data.get('full_name') is None:
            return Response(
                {"error": "Full name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data.get('password') is None:
            return Response(
                {"error": "Password is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data.copy()
        data['organization'] = str(org_id)
        # Create the organization admin
        serializer = OrganizationAdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin'])
def admin_detail(request, pk=None):
    """Get, update or delete a single organization admin by ID."""
    if not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid admin ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    org_id = request.admin.organization.id
    admin = get_object_or_404(
            OrganizationAdmin, organization=org_id, pk=pk)

    if request.method == 'GET':
        serializer = OrganizationAdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = OrganizationAdminSerializer(
                admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    serializer.data, status=status.HTTP_200_OK)
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        admin.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)
