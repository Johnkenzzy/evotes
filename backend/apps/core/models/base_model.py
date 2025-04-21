"""Define the base model for all models"""
import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Abstract base model to provide common fields and methods."""
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        """Initialize the model instance."""
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-created_at']  # Default ordering by latest

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} ({self.id})')

    def soft_delete(self):
        """Mark the record as inactive (soft delete)."""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])

    def hard_delete(self, *args, **kwargs):
        """Permanently delete the record from the database."""
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Override save method to hash the password before saving."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
