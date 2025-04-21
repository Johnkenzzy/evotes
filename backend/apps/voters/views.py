from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.voters.models import Voter, Vote
from apps.organizations.models import Organization
from apps.ballots.models import Ballot, Option
from apps.auth_and_auth.admin import AdminJWTAuthentication
from apps.core.utils.serializers import get_general_serializer
from apps.core.utils.validate_uuid import is_valid_uuid
from apps.core.utils.role_decorator import role_required


class VoterSerializer(get_general_serializer(Voter)):
    """Serializer for the Voter model."""
    pass


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
def voters(request):
    """Get all voters or create a new one for an organization."""
    org_id = request.admin.organization.id

    if request.method == 'GET':
        voters = Voter.objects.filter(organisation=org_id)
        serializer = VoterSerializer(voters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get('full_name') is None:
            return Response(
                {"error": "Full name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        email = request.data.get('email')
        if email is None:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Voter.objects.filter(organisation=org_id, email=email).exists():
            return Response({
                "error": "Voter with this email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        request.data['organization'] = str(org_id)
        # Create the voter
        serializer = VoterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin', 'voter'])
def voter_detail(request, pk=None):
    """Get, update or delete a single voter by ID."""
    if not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid voter ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    org_id = request.admin.organization.id
    voter = get_object_or_404(Voter, organisation=org_id, pk=pk)

    if request.method == 'GET':
        serializer = VoterSerializer(voter)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if not request.admin:
            return Response(
                {'error': 'Unauthorized access'},
                status=status.HTTP_401_UNAUTHORIZED)

        serializer = VoterSerializer(
            voter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.admin or request.admin.role != 'superadmin':
            return Response(
                {'error': 'Unauthorized access'},
                status=status.HTTP_401_UNAUTHORIZED)

        voter.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)


class VoteSerializer(get_general_serializer(Vote)):
    """Serializer for the Vote model."""
    pass


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin', 'voter'])
def votes(request, ballot_id=None):
    """Get all votes for a ballot or create a new vote."""
    if not is_valid_uuid(ballot_id):
        return Response(
            {"error": "Invalid ballot ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)

    if request.method == 'GET':
        votes = Vote.objects.filter(ballot=ballot)
        serializer = VoteSerializer(votes, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.voter:
            return Response(
                {'error': 'Unauthorized access'},
                status=status.HTTP_401_UNAUTHORIZED)

        voter_id = request.voter.id
        voter = get_object_or_404(Voter, id=voter_id)
        if not voter.is_verified:
            return Response(
                {"error": "Voter not verified"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check if vote already exists
        if Vote.objects.filter(voter=voter, ballot=ballot).exists():
            return Response(
                {"error": "Voter has already voted"},
                status=status.HTTP_400_BAD_REQUEST
            )
        option_id = request.data.get('option', None)
        if option_id is None:
            return Response(
                {"error": "Option is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(Option, id=option_id, ballot=ballot)
        # Create the vote
        request.data['ballot'] = str(ballot.id)
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin', 'voter'])
def vote_detail(request, ballot_id=None, pk=None):
    """Get, update or delete a vote by ID and ballot scope."""
    if not is_valid_uuid(ballot_id) or not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid ballot ID or vote ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)
    vote = get_object_or_404(Vote, pk=pk, ballot=ballot)

    if request.method == 'GET':
        serializer = VoteSerializer(vote)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VoteSerializer(
            vote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vote.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)
