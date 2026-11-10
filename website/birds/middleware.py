"""Login gate and security headers for the Kashmir Birds AI site.

The home page (landing), the bird field guide (birds database,
gallery and every bird detail page), the About and Contact pages
and the crawler files (/sitemap.xml, /robots.txt) are public, so
search engines can index the 745 bird pages and a first-time
visitor can see what the site offers before signing up. The AI
Identify tool and account pages still require a signed-in user;
unauthenticated visitors are redirected to /login/?next=<path>.

Unknown paths are NOT login-gated: they fall through so Django
returns a real 404 instead of redirecting every typo to /login/.
"""

from urllib.parse import quote

from django.conf import settings
from django.shortcuts import redirect
from django.urls import Resolver404, resolve


EXEMPT_EXACT_PATHS = ('/', '/admin', '/sitemap.xml', '/robots.txt')
EXEMPT_PREFIXES = (
    '/login/',
    '/logout/',
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
    # Public pages: anyone can read what the site offers before
    # signing up. (The Identify tool itself stays behind login.)
    '/about/',
    '/contact/',
)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path in EXEMPT_EXACT_PATHS or path.startswith(EXEMPT_PREFIXES):
            return self.get_response(request)
        if not request.user.is_authenticated:
            # Only real pages get the login redirect. An unknown
            # path has no view at all, so let it through and let
            # Django return a 404 instead of hiding it behind
            # /login/ (which also hid it from search engines).
            try:
                resolve(path)
            except Resolver404:
                return self.get_response(request)
            login_url = getattr(settings, 'LOGIN_URL', '/login/')
            return redirect(f'{login_url}?next={quote(path, safe="/")}')
        return self.get_response(request)


class SecurityHeadersMiddleware:
    """Extra security headers on every response.

    Permissions-Policy disables camera, microphone and geolocation:
    the site uses none of them.

    Content-Security-Policy is Report-Only, not enforcing: the login
    page (tab switching) and the identify page (drag-and-drop photo
    preview) use inline <script> and <style>, and the identify
    results use an inline style attribute, so an enforcing policy
    without 'unsafe-inline' would break them. Report-Only records
    violations without breaking the site; revisit enforcing once
    those scripts move to static files.
    """

    # What an enforcing policy would look like. Font Awesome CSS
    # and fonts come from the cdnjs CDN; uploaded-photo previews
    # use data: URLs; everything else is same-origin.
    CSP_REPORT_ONLY = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' https://cdnjs.cloudflare.com; "
        "font-src 'self' https://cdnjs.cloudflare.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self'"
    )
    PERMISSIONS_POLICY = 'camera=(), microphone=(), geolocation=()'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Permissions-Policy'] = self.PERMISSIONS_POLICY
        response['Content-Security-Policy-Report-Only'] = (
            self.CSP_REPORT_ONLY
        )
        return response
