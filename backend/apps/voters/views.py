from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.voters.models import Voter, Vote
from apps.ballots.models import Ballot, Option
from apps.auth_and_auth.admin import (AdminJWTAuthentication,
                                      VoterJWTAuthentication)
from apps.core.utils.serializers import get_general_serializer
from apps.core.utils.validate_uuid import is_valid_uuid
from apps.core.utils.role_decorator import role_required
from apps.core.utils.email_message import assign_voter_code


class VoterSerializer(get_general_serializer(Voter)):
    """Serializer for the Voter model."""
    pass


@api_view(['GET', 'POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
def voters(request):
    """Get all voters or create a new one for an organization."""
    org_id = request.admin.organization.id

    if request.method == 'GET':
        voters = Voter.objects.filter(organization=org_id)
        serializer = VoterSerializer(
            voters,
            context={'request': request},
            many=True
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Check email uniqueness
        email = request.data.get('email')
        if Voter.objects.filter(organization=org_id, email=email).exists():
            return Response({
                "error": "Voter with this email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['organization'] = str(org_id)
        # Create the voter
        serializer = VoterSerializer(data=data)
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
def get_voter(request, pk=None):
    """Gets a voter."""
    if pk == 'me':
        serializer = VoterSerializer(
            request.voter,
            context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK)
    else:
        if not is_valid_uuid(pk):
            return Response(
                {"error": "Invalid voter ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
    org_id = request.admin.organization.id
    voter = get_object_or_404(Voter, organization=org_id, pk=pk)

    serializer = VoterSerializer(
        voter,
        context={'request': request}
    )
    return Response(
        serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
def voter_detail(request, pk=None):
    """Get, update or delete a single voter by ID."""
    if not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid voter ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    org_id = request.admin.organization.id
    voter = get_object_or_404(Voter, organization=org_id, pk=pk)

    if request.method == 'GET':
        serializer = VoterSerializer(
            voter,
            context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['organization'] = str(org_id)
        # Validate the request data
        serializer = VoterSerializer(
            voter, data=data, partial=True)
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

        voter.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
def send_codes(request):
    """Send codes to voters."""
    org_id = request.admin.organization.id
    expires_at = request.data.get('expires_at')
    title = request.data.get('title')
    voters = Voter.objects.filter(organization=org_id)
    for voter in voters:
        assign_voter_code(voter, title=title, expires_at=expires_at)
    serializer = VoterSerializer(voters, many=True)
    return Response(
      {"detail": f"Sent codes to {len(serializer.data)} voters"},
      status=status.HTTP_200_OK)


class VoteSerializer(get_general_serializer(Vote)):
    """Serializer for the Vote model."""
    pass


@api_view(['POST'])
@authentication_classes([VoterJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['voter'])
def cast_votes(request, ballot_id=None):
    """Cast vote within a ballot choosing a particular option."""
    if not is_valid_uuid(ballot_id):
        return Response(
            {"error": "Invalid ballot ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)

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
    option = get_object_or_404(Option, id=option_id, ballot=ballot)
    data = request.data.copy()
    data['voter'] = voter_id
    data['ballot'] = ballot_id
    # Create the vote
    request.data['ballot'] = str(ballot.id)
    serializer = VoteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        option.votes = option.votes + 1
        option.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
def get_votes(request, ballot_id=None):
    """Get all votes for a ballot"""
    if not is_valid_uuid(ballot_id):
        return Response(
            {"error": "Invalid ballot ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)

    if request.method == 'GET':
        votes = Vote.objects.filter(ballot=ballot)
        serializer = VoteSerializer(
            votes,
            context={'request': request},
            many=True
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([VoterJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['voter'])
def vote_detail(request, ballot_id=None):
    """Get, update or delete a vote by ID and ballot scope."""
    if not is_valid_uuid(ballot_id):
        return Response(
            {"error": "Invalid ballot ID or vote ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)
    voter = get_object_or_404(Voter, id=request.voter.id)
    vote = get_object_or_404(Vote, ballot=ballot.id, voter=voter.id)

    if request.method == 'GET':
        serializer = VoteSerializer(
            vote,
            context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        prev_option = get_object_or_404(Option, ballot=ballot, vote=vote)
        new_option = get_object_or_404(Option, id=request.data["option"])

        serializer = VoteSerializer(
            vote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if prev_option != new_option:
                prev_option.votes = prev_option.votes - 1
                prev_option.save()
                new_option.votes = new_option.votes + 1
                new_option.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        option = get_object_or_404(Option, ballot=ballot, vote=vote)
        vote.delete()
        option.votes = option.votes - 1
        option.save()
        return Response(
            [], status=status.HTTP_204_NO_CONTENT)
