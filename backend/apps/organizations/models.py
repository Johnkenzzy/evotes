"""Define models for organization app."""
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager,
                                        Group, Permission)

from apps.core.models.base_model import BaseModel


class Organization(BaseModel, models.Model):
    """Model for organizations."""
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    logo = models.ImageField(
        upload_to='organization_logos/',
        blank=True,
        null=True,
        default='organization_logo/default.jpg'
        )
    website = models.URLField(null=True)


class AdminManager(BaseUserManager):
    """Manager for organization admins."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class OrganizationAdmin(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Model for organization admins."""
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
    ]
    groups = models.ManyToManyField(
        Group,
        related_name='organization_admins',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='organization_admins_permissions',  # changed from default
        blank=True,                                      # 'user_set'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='admin')

    objects = AdminManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
