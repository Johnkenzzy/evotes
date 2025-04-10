from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.voters.models import Voter, Vote
from apps.organizations.models import Organization
from apps.ballots.models import Ballot, Option
from apps.core.utils.serializers import get_general_serializer


class VoterSerializer(get_general_serializer(Voter)):
    """Serializer for the Voter model."""
    pass


@api_view(['GET', 'POST'])
def voters(request, org_id=None):
    """Get all voters or create a new one for an organization."""
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
        org_id = request.data.get('organisation', None)
        if org_id is None:
            return Response(
                {"error": "Organization is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(Organization, id=org_id)
        if request.data.get('full_name') is None:
            return Response(
                {"error": "Full name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data.get('voter_id') is None:
            return Response(
                {"error": "Voter ID is required"},
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

        # Create the voter
        serializer = VoterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def voter_detail(request, org_id=None, pk=None):
    """Get, update or delete a single voter by ID."""
    voter = get_object_or_404(Voter, organisation=org_id, pk=pk)

    if request.method == 'GET':
        serializer = VoterSerializer(voter)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VoterSerializer(
            voter, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        voter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VoteSerializer(get_general_serializer(Vote)):
    """Serializer for the Vote model."""
    pass


@api_view(['GET', 'POST'])
def votes(request, ballot_id=None):
    """Get all votes for a ballot or create a new vote."""
    ballot = get_object_or_404(Ballot, id=ballot_id)

    if request.method == 'GET':
        votes = Vote.objects.filter(ballot=ballot)
        serializer = VoteSerializer(votes, many=True)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        voter_id = request.data.get('voter', None)
        if voter_id is None:
            return Response(
                {"error": "Voter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        voter = get_object_or_404(Voter, id=voter_id)
        if not voter.is_accredited or voter.has_voted:
            return Response(
                {"error": "Voter is not accredited or has already voted"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check if vote already exists
        if Vote.objects.filter(voter=voter_id, ballot=ballot).exists():
            return Response(
                {"error": "Vote already exists for this voter and ballot"},
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
            serializer.data.has_voted = True
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def vote_detail(request, ballot_id=None, pk=None):
    """Get, update or delete a vote by ID and ballot scope."""
    ballot = get_object_or_404(Ballot, id=ballot_id)
    vote = get_object_or_404(Vote, pk=pk, ballot=ballot)

    if request.method == 'GET':
        serializer = VoteSerializer(vote)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VoteSerializer(
            vote, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
