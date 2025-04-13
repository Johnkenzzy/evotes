from rest_framework.response import Response
from rest_framework import status
from functools import wraps


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user or not hasattr(user, 'role'):
                return Response(
                    {'error': 'Unauthorized'},
                    status=status.HTTP_401_UNAUTHORIZED)
            if user.role not in allowed_roles:
                return Response(
                    {'error': 'Forbidden'},
                    status=status.HTTP_403_FORBIDDEN)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
