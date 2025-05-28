from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.elections.models import Election
from apps.auth_and_auth.admin import (AdminJWTAuthentication,
                                      VoterJWTAuthentication)
from apps.core.utils.serializers import get_general_serializer
from apps.core.utils.validate_uuid import is_valid_uuid
from apps.core.utils.role_decorator import role_required


class ElectionSerializer(get_general_serializer(Election)):
    """Serializer for the Election model."""
    pass


@api_view(['GET', 'POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
def elections(request):
    """Get all elections or create a new one for an organization."""
    org_id = request.admin.organization.id

    if request.method == 'GET':
        elections = Election.objects.filter(organization=org_id)
        serializer = ElectionSerializer(elections, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        data['organization'] = str(org_id)
        # Create the election
        serializer = ElectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([VoterJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['voter'])
def get_elections(request):
    """Get all elections."""
    org_id = request.voter.organization.id

    elections = Election.objects.filter(organization=org_id)
    serializer = ElectionSerializer(elections, many=True)
    return Response(
        serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
def election_detail(request, pk=None):
    """Get, update or delete a single election by ID."""
    if not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid election ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    org_id = request.admin.organization.id

    election = get_object_or_404(
        Election, organization=org_id, pk=pk)

    if request.method == 'GET':
        serializer = ElectionSerializer(election)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['organization'] = str(org_id)
        serializer = ElectionSerializer(
            election, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.admin.role != 'superadmin':
            return Response(
                {'error': 'Forbidden access'},
                status=status.HTTP_403_FORBIDDEN)

        election.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)
