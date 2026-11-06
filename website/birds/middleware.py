"""Login gate for the Kashmir Birds AI site.

The home page (landing), the bird field guide (birds database,
gallery and every bird detail page) and the crawler files
(/sitemap.xml, /robots.txt) are public, so search engines can
index the 745 bird pages. The AI Identify tool and account
pages still require a signed-in user; unauthenticated visitors
are redirected to /login/?next=<path>.
"""

from urllib.parse import quote

from django.conf import settings
from django.shortcuts import redirect


EXEMPT_EXACT_PATHS = ('/', '/admin', '/sitemap.xml', '/robots.txt')
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
    '/bird-images/',
    '/favicon.ico',
    # Public field guide: the birds database listing, the gallery
    # and every bird detail page (/bird/<id>/). '/bird/' does not
    # match '/birds/' (different 6th character), so both are needed.
    '/birds/',
    '/gallery/',
    '/bird/',
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
