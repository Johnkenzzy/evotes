
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from apps.organizations.models import (Organization,
                                       OrganizationAdmin)
from apps.elections.models import Election
from apps.voters.models import Voter, Vote
from apps.ballots.models import Ballot, Option


@api_view(['GET'])
def stats(request):
    """Return basic statistics about the system."""
    return Response({
        "organizations": Organization.objects.count(),
        "admins": OrganizationAdmin.objects.count(),
        "elections": Election.objects.count(),
        "voters": Voter.objects.count(),
        "votes": Vote.objects.count(),
        "ballots": Ballot.objects.count(),
        "options": Option.objects.count()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def index(request):
    """API root index view."""
    return Response({
        "message": "Welcome to the eVotes API Version 1.0",
        "endpoints": {
            "API Root": "/api/v1/",
            "Organizations": {
                "List": "/api/v1/organizations/",
                "Create": "/api/v1/organizations/",
                "Read": "/api/v1/organizations/{id}/",
                "Update": "/api/v1/organizations/{id}/",
                "Delete": "/api/v1/organizations/{id}/"
            },
            "Admins": {
                "List": "/api/v1/admins/",
                "Create": "/api/v1/admins/",
                "Read": "/api/v1/admins/{id}/",
                "Update": "/api/v1/admins/{id}/",
                "Delete": "/api/v1/admins/{id}/"
            },
            "Elections": {
                "List": "/api/v1/elections/",
                "Create": "/api/v1/elections/",
                "Read": "/api/v1/elections/{id}/",
                "Update": "/api/v1/elections/{id}/",
                "Delete": "/api/v1/elections/{id}/",
                "Get by Voter": "/api/v1/get_elections/"
            },
            "Ballots": {
                "List": "/api/v1/{election_id}/ballots/",
                "Create": "/api/v1/{election_id}/ballots/",
                "Read": "/api/v1/{election_id}/ballots/{id}/",
                "Update": "/api/v1/{election_id}/ballots/{id}/",
                "Delete": "/api/v1/{election_id}/ballots/{id}/",
                "Get by Election": "/api/v1/{election_id}/get_ballots/"
            },
            "Options": {
                "List": "/api/v1/{ballot_id}/options/",
                "Create": "/api/v1/{ballot_id}/options/",
                "Read": "/api/v1/{ballot_id}/options/{id}/",
                "Update": "/api/v1/{ballot_id}/options/{id}/",
                "Delete": "/api/v1/{ballot_id}/options/{id}/",
                "Get Options": "/api/v1/{ballot_id}/get_options/"
            },
            "Votes": {
                "List": "/api/v1/{ballot_id}/votes/",
                "Update": "/api/v1/{ballot_id}/votes/",
                "Delete": "/api/v1/{ballot_id}/votes/",
                "Get Votes": "/api/v1/{ballot_id}/get_votes/",
                "Cast Vote": "/api/v1/{ballot_id}/cast_votes/"
            },
            "Voters": {
                "List": "/api/v1/voters/",
                "Create": "/api/v1/voters/",
                "Read": "/api/v1/voters/{id}/",
                "Update": "/api/v1/voters/{id}/",
                "Delete": "/api/v1/voters/{id}/",
                "Send Codes": "/api/v1/voters/send_codes/"
            },
            "Stats": "/api/v1/stats/"
        },
        "auth": {
            "Login": "/auth/login/",
            "Logout": "/auth/logout/",
            "Register": "/auth/register/",
            "Verify Voter": "/auth/verify_voter/"
        }
    }, status=status.HTTP_200_OK)


def custom_404_view(request, exception=None):
    """Custom handler for 404 errors."""
    return JsonResponse({
        "error": "The resource you are looking for was not found."
    }, status=404)
