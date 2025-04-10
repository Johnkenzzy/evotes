"""Defines scoped query sets helpers."""


def get_org_queryset(model_class, user):
    """Return organization-scoped queryset."""
    return model_class.objects.filter(organization=user.organization)


def perform_org_create(serializer, user):
    """Save model instance with user's organization."""
    serializer.save(organization=user.organization)
