"""Define models for voters app"""
from django.db import models

from apps.core.models.base_model import BaseModel
from apps.organizations.models import Organization
from apps.ballots.models import Ballot, Option


class Voter(BaseModel, models.Model):
    """Define model for a Voter"""
    organisation = models.ForeignKey(
            Organization,
            on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_accredited = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)


class Vote(BaseModel):
    """Defines model for a vote"""
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    organization = models.ForeignKey(
            'organizations.Organization',
            on_delete=models.CASCADE,
            null=True)

    class Meta:
        unique_together = ('voter', 'ballot')
