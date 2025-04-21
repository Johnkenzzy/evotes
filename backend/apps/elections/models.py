"""Define models for the elections app."""
from django.db import models

from apps.core.models.base_model import BaseModel
from apps.organizations.models import Organization


class Election(BaseModel, models.Model):
    """Model for an election."""
    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             default='New Election')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
