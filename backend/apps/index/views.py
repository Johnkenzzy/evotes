
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from apps.organizations.models import Organization, OrganizationAdmin
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
            "Organizations": "/api/v1/organizations/",
            "Admins": "/api/v1/<org_id>/admins/",
            "Elections": "/api/v1/<org_id>/elections/",
            "Voters": "/api/v1/<org_id>/voters/",
            "Votes": "/api/v1/<ballot_id>/votes/",
            "Ballots": "/api/v1/<election_id>/elections/",
            "Options": "/api/v1/<ballot_id>/ballots/"
        }
    }, status=status.HTTP_200_OK)


def custom_404_view(request, exception=None):
    """Custom handler for 404 errors."""
    return JsonResponse({
        "error": "The resource you are looking for was not found."
    }, status=404)
