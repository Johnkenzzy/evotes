from rest_framework.decorators import (api_view,
                                       parser_classes,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import (JSONParser,
                                    MultiPartParser,
                                    FormParser)
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.ballots.models import Ballot, Option
from apps.elections.models import Election
from apps.auth_and_auth.admin import (AdminJWTAuthentication,
                                      VoterJWTAuthentication)
from apps.core.utils.serializers import get_general_serializer
from apps.core.utils.validate_uuid import is_valid_uuid
from apps.core.utils.role_decorator import role_required


class BallotSerializer(get_general_serializer(Ballot)):
    """Serializer for the Ballot model."""
    pass


@api_view(['GET', 'POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
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
        serializer = BallotSerializer(
            ballots,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        title = request.data.get('title')
        if Ballot.objects.filter(election=election, title=title).exists():
            return Response(
                {"error": "Ballot title already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data.copy()
        data['election'] = str(election.id)
        serializer = BallotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@role_required(['voter'])
@authentication_classes([VoterJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ballots(request, election_id=None):
    """Get all ballots for an election(for voters only)."""
    if not is_valid_uuid(election_id):
        return Response(
            {"error": "Invalid election ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    election = get_object_or_404(Election, id=election_id)

    ballots = Ballot.objects.filter(election=election)
    serializer = BallotSerializer(
        ballots,
        context={'request': request},
        many=True
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
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
        serializer = BallotSerializer(
            ballot,
            context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['election'] = str(election_id)
        serializer = BallotSerializer(
            ballot, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not hasattr(request, 'admin') or request.admin.role != 'superadmin':
            return Response(
                {'error': 'forbidden access'},
                status=status.HTTP_403_FORBIDDEN)

        ballot.delete()
        return Response(
            [], status=status.HTTP_204_NO_CONTENT)


class OptionSerializer(get_general_serializer(Option)):
    """Serializer for the Option model."""
    pass


@api_view(['GET', 'POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
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
        serializer = OptionSerializer(
            options,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Check for duplicate option names
        name = request.data.get('name')
        if Option.objects.filter(ballot=ballot, name=name).exists():
            return Response(
                {"error": "Option name already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['ballot'] = str(ballot.id)
        serializer = OptionSerializer(data=data)
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
@parser_classes([JSONParser, MultiPartParser, FormParser])
def get_options(request, ballot_id=None):
    """Get all options for a ballot."""
    if not is_valid_uuid(ballot_id):
        return Response(
            {"error": "Invalid ballot ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    ballot = get_object_or_404(Ballot, id=ballot_id)

    if request.method == 'GET':
        options = Option.objects.filter(ballot=ballot)
        serializer = OptionSerializer(
            options,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
@role_required(['superadmin', 'admin'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
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
        serializer = OptionSerializer(
            option,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['ballot'] = str(ballot.id)
        serializer = OptionSerializer(
            option, data=data, partial=True)
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

        option.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)
