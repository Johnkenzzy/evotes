"""Define models for the elections app."""
from django.db import models

from apps.core.models.base_model import BaseModel
from apps.organizations.models import Organization


class Election(BaseModel, models.Model):
    """Model for an election."""
    organisation = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=255, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
