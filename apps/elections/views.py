from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.organizations.models import Organization
from apps.utils.serializers import get_general_serializer
from apps.utils.scoped_quries import get_org_queryset, perform_org_create
