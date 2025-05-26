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
    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    sign_in_code = models.CharField(max_length=100,
                                    unique=True, null=True)
    expires_at = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=30,
                            default='voter')

    @property
    def is_authenticated(self):
        return True

    def generate_sign_in_code(self, expires_at=None):
        """Generates a sign-in code for the voter"""
        if expires_at is None:
            expires_at = timezone.now() + timedelta(hours=12)
        self.sign_in_code = str(uuid.uuid4()).split("-")[0].upper()
        self.expires_at = expires_at


class Vote(BaseModel):
    """Defines model for a vote"""
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'ballot')
