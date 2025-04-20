"""Define models for voters app"""
import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

from apps.core.models.base_model import BaseModel
from apps.organizations.models import Organization
from apps.ballots.models import Ballot, Option


class Voter(BaseModel, models.Model):
    """Define model for a Voter"""
    organisation = models.ForeignKey(
            Organization,
            on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    sign_in_code = models.CharField(max_length=100, unique=True, null=True)
    code_expires_at = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)

    def generate_sign_in_code(self, expiration_time=None):
        """Generates a sign-in code for the voter"""
        if expiration_time is None:
            expiration_time = timezone.now() + timedelta(hours=12)
        self.sign_in_code = str(uuid.uuid4()).split("-")[0].upper()
        self.code_expires_at = expiration_time


class Vote(BaseModel):
    """Defines model for a vote"""
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'ballot')
