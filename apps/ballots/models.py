"""Define models for ballots app."""
from django.db import models

from apps.core.models.base_model import BaseModel
from apps.elections.models import Election


class Ballot(BaseModel, models.Model):
    """Model for ballots."""
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    organization = models.ForeignKey(
            'organizations.Organization',
            on_delete=models.CASCADE,
            null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    votes = models.IntegerField(default=0)


class Option(BaseModel, models.Model):
    """Model for ballot options."""
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    organization = models.ForeignKey(
            'organizations.Organization',
            on_delete=models.CASCADE,
            null=True)
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=255, null=True)
    photo = models.ImageField(
            upload_to='candidate_images/',
            blank=True, null=True)
    votes = models.IntegerField(default=0)

    class Meta:
        """Enforce uniqueness per ballot"""
        unique_together = ('ballot', 'name')
