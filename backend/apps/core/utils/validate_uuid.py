"""Defines a function to validate a UUID."""
import uuid


def is_valid_uuid(val):
    """Validate a UUID."""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
