from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.elections.models import Election
from apps.organizations.models import Organization
from apps.core.utils.serializers import get_general_serializer
from apps.core.utils.validate_uuid import is_valid_uuid


class ElectionSerializer(get_general_serializer(Election)):
    """Serializer for the Election model."""
    pass


@api_view(['GET', 'POST'])
def elections(request, org_id=None):
    """Get all elections or create a new one for an organization."""
    if not is_valid_uuid(org_id):
        return Response(
            {"error": "Invalid organization ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if request.method == 'GET':
        elections = Election.objects.filter(organisation=org_id)
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Validate the request data
        if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        org_id = request.data.get('organisation', None)
        if org_id is None:
            return Response(
                {"error": "Organization is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(Organization, id=org_id)
        if request.data.get('name') is None:
            return Response(
                {"error": "Name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        start_time = request.data.get('start_time', None)
        end_time = request.data.get('end_time', None)
        if start_time is None or end_time is None:
            return Response(
                {"error": "Start time and end time are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create the election
        serializer = ElectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def election_detail(request, org_id=None, pk=None):
    """Get, update or delete a single election by ID."""
    if not is_valid_uuid(org_id) or not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid organization or election ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    election = get_object_or_404(
        Election, organisation=org_id, pk=pk)

    if request.method == 'GET':
        serializer = ElectionSerializer(election)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ElectionSerializer(
            election, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        election.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
