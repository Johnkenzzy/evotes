from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.ballots.models import Ballot, Option
from apps.elections.models import Election
from apps.core.utils.serializers import get_general_serializer
from apps.core.utils.validate_uuid import is_valid_uuid


class BallotSerializer(get_general_serializer(Ballot)):
    """Serializer for the Ballot model."""
    pass


@api_view(['GET', 'POST'])
def ballots(request, election_id=None):
    """Get all ballots for an election or create a new ballot."""
    if not is_valid_uuid(election_id):
        return Response(
            {"error": "Invalid election ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'GET':
        ballots = Ballot.objects.filter(election=election)
        serializer = BallotSerializer(ballots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        title = request.data.get('title')
        if not title:
            return Response(
                {"error": "Title is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Ballot.objects.filter(election=election, title=title).exists():
            return Response(
                {"error": "A ballot with this \
                        title already exists in this election"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.data['election'] = str(election.id)
        serializer = BallotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ballot_detail(request, election_id=None, pk=None):
    """Get, update or delete a ballot by ID and election scope."""
    if not is_valid_uuid(election_id) or not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid election ID or ballot ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    election = get_object_or_404(Election, id=election_id)
    ballot = get_object_or_404(Ballot, pk=pk, election=election)

    if request.method == 'GET':
        serializer = BallotSerializer(ballot)
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BallotSerializer(
            ballot, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ballot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OptionSerializer(get_general_serializer(Option)):
    """Serializer for the Option model."""
    pass


@api_view(['GET', 'POST'])
def options(request, ballot_id=None):
    """Get all options for a ballot or create a new option."""
    if not is_valid_uuid(ballot_id):
        return Response(
            {"error": "Invalid ballot ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)

    if request.method == 'GET':
        options = Option.objects.filter(ballot=ballot)
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.data:
            return Response(
                {"error": "Request body is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        name = request.data.get('name')
        if not name:
            return Response(
                {"error": "Name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Option.objects.filter(ballot=ballot, name=name).exists():
            return Response(
                {"error": "An option with this \
                        name already exists for this ballot"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.data['ballot'] = str(ballot.id)
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def option_detail(request, ballot_id=None, pk=None):
    """Get, update or delete a specific option by ID and ballot scope."""
    if not is_valid_uuid(ballot_id) or not is_valid_uuid(pk):
        return Response(
            {"error": "Invalid ballot ID or option ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)
    option = get_object_or_404(Option, pk=pk, ballot=ballot)

    if request.method == 'GET':
        serializer = OptionSerializer(option)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = OptionSerializer(
            option, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
