from django.http import HttpResponsePermanentRedirect
from django.urls import resolve, Resolver404
from urllib.parse import urlsplit, urlunsplit


class ForceSlashMiddleware:
    """
    Redirects any URL without trailing slash to its slash version
    for all HTTP methods (GET, POST, PUT, DELETE, etc.)
    only if the slash version resolves.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if not path.endswith('/'):
            try:
                # Try to resolve the slash-appended path
                resolve(path + '/')
            except Resolver404:
                # No match with slash, don't redirect
                return self.get_response(request)

            # Rebuild full URL with trailing slash
            split = urlsplit(request.get_full_path())
            new_path = urlunsplit(
                (split.scheme,
                 split.netloc,
                 split.path + '/',
                 split.query,
                 split.fragment)
                )

            # Use 307 to preserve method (POST, PUT, etc.)
            return HttpResponsePermanentRedirect(new_path, status=307)

        return self.get_response(request)
