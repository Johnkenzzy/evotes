"""Define models for organization app."""
from django.db import models

from apps.core.models.base_model import BaseModel


class Organization(BaseModel, models.Model):
    """Model for organizations."""
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    logo = models.ImageField(upload_to='organization_logos/', null=True)
    website = models.URLField(null=True)
    password = models.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrganizationAdmin(BaseModel, models.Model):
    """Model for organization admins."""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_super_admin = models.BooleanField(default=False, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
