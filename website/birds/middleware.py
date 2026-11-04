"""Login gate for the Kashmir Birds AI site.

The home page (landing) is public. Every other page requires a signed-in
user; unauthenticated visitors are redirected to /login/?next=<path>.
"""

from urllib.parse import quote

from django.conf import settings
from django.shortcuts import redirect


EXEMPT_EXACT_PATHS = ('/', '/admin')
EXEMPT_PREFIXES = (
    '/login/',
    '/logout/',
    # Google sign-in is part of the login process: the start endpoint
    # and Google's callback must be reachable before the user has a
    # session, otherwise the flow would redirect-loop on /login/.
    '/auth/google/',
    '/auth/phone/verify/',
    '/admin/',
    '/static/',
    '/media/',
    '/favicon.ico',
)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path in EXEMPT_EXACT_PATHS or path.startswith(EXEMPT_PREFIXES):
            return self.get_response(request)
        if not request.user.is_authenticated:
            login_url = getattr(settings, 'LOGIN_URL', '/login/')
            return redirect(f'{login_url}?next={quote(path, safe="/")}')
        return self.get_response(request)
