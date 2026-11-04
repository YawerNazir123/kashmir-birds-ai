"""Sign-in / sign-up views for the site.

Three sign-in methods:

1. Email + password (Django's built-in User model). Works with no extra
   configuration.
2. Google sign-in, via a minimal hand-rolled OAuth2 flow (no extra
   dependency). Requires GOOGLE_OAUTH_CLIENT_ID and
   GOOGLE_OAUTH_CLIENT_SECRET to be set (see LOGIN_SETUP.md). If they are
   missing, the Google button shows "not configured yet".
3. Phone OTP, via Firebase. Requires the Firebase web config env vars
   (see LOGIN_SETUP.md) for the browser side, and the firebase_admin
   package plus a service-account credential for server-side token
   verification. If anything is missing, verification returns a polite
   JSON error instead of crashing.
"""

import json
import os
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'

REMEMBER_ME_AGE = 31536000  # one year, in seconds


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _safe_next(value):
    """Allow only local redirect targets, to avoid open redirects."""
    if value and value.startswith('/') and not value.startswith('//'):
        return value
    return ''


def _base_context(request, **extra):
    """Context shared by every render of the login page."""
    firebase_config = getattr(settings, 'FIREBASE_WEB_CONFIG', {}) or {}
    configured = getattr(settings, 'FIREBASE_WEB_CONFIGURED', False)
    context = {
        'google_available': bool(getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')),
        'firebase_configured': bool(configured),
        'firebase_config': {k: v for k, v in firebase_config.items() if v},
        'next': _safe_next(request.GET.get('next') or request.POST.get('next')),
        'tab': 'signin',
        'errors': [],
    }
    context.update(extra)
    return context


def _finish_login(request, user, next_url):
    """Apply remember-me, log the user in, and redirect onward."""
    remember = request.POST.get('remember_me') == 'on'
    request.session.set_expiry(REMEMBER_ME_AGE if remember else 0)
    login(request, user)
    return redirect(_safe_next(next_url) or '/birds/')


# ---------------------------------------------------------------------------
# Email / password
# ---------------------------------------------------------------------------

def login_page(request):
    """Render the login page, or handle a sign-in / create-account POST."""
    context = _base_context(request)

    if request.method != 'POST':
        return render(request, 'birds/login.html', context)

    action = request.POST.get('action', 'signin')
    email = (request.POST.get('email') or '').strip().lower()
    password = request.POST.get('password') or ''
    context['next'] = _safe_next(request.POST.get('next'))

    if not email or not password:
        context['errors'].append(
            'Please enter both your email address and your password.'
        )
        return render(request, 'birds/login.html', context)

    if action == 'signup':
        context['tab'] = 'signup'
        password2 = request.POST.get('password2') or ''
        if password != password2:
            context['errors'].append(
                'The two passwords do not match. Please try again.'
            )
        elif len(password) < 8:
            context['errors'].append(
                'Please choose a password with at least 8 characters.'
            )
        elif User.objects.filter(username=email).exists():
            context['errors'].append(
                'An account with this email already exists. '
                'Try signing in instead.'
            )
        else:
            user = User.objects.create_user(
                username=email, email=email, password=password
            )
            return _finish_login(request, user, context['next'])
        return render(request, 'birds/login.html', context)

    # Sign in.
    user = authenticate(request, username=email, password=password)
    if user is None:
        context['errors'].append(
            'We could not find an account with that email and password. '
            'Please check them and try again, or create a new account.'
        )
        return render(request, 'birds/login.html', context)
    return _finish_login(request, user, context['next'])


def logout_view(request):
    """Sign the user out and send them back to the public home page."""
    logout(request)
    return redirect('/')


# ---------------------------------------------------------------------------
# Google sign-in (minimal OAuth2, no extra dependency)
# ---------------------------------------------------------------------------

def google_login(request):
    """Start the Google OAuth2 flow, or show "not configured yet"."""
    if not getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', ''):
        return render(
            request,
            'birds/login.html',
            _base_context(
                request,
                errors=[
                    'Google sign-in is not configured yet. '
                    'You can still sign in with email and password.'
                ],
                google_available=False,
            ),
        )
    next_url = _safe_next(request.GET.get('next'))
    redirect_uri = request.build_absolute_uri(reverse('google_callback'))
    params = {
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': next_url,
        'access_type': 'online',
        'prompt': 'select_account',
    }
    return redirect(f'{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}')


def google_callback(request):
    """Handle Google's redirect back: exchange the code, sign the user in."""
    context = _base_context(request)
    code = request.GET.get('code')
    if not code:
        context['errors'].append(
            'Google sign-in did not complete. Please try again.'
        )
        return render(request, 'birds/login.html', context)

    try:
        redirect_uri = request.build_absolute_uri(reverse('google_callback'))
        token_data = urllib.parse.urlencode({
            'code': code,
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }).encode()
        token_request = urllib.request.Request(
            GOOGLE_TOKEN_URL, data=token_data
        )
        with urllib.request.urlopen(token_request, timeout=15) as response:
            tokens = json.loads(response.read().decode())
        access_token = tokens.get('access_token')
        if not access_token:
            raise ValueError('no access token')
        userinfo_request = urllib.request.Request(
            GOOGLE_USERINFO_URL,
            headers={'Authorization': f'Bearer {access_token}'},
        )
        with urllib.request.urlopen(userinfo_request, timeout=15) as response:
            profile = json.loads(response.read().decode())
        email = (profile.get('email') or '').strip().lower()
        if not email:
            raise ValueError('no email in profile')
    except Exception:
        context['errors'].append(
            'Something went wrong with Google sign-in. '
            'Please try again, or use email and password.'
        )
        return render(request, 'birds/login.html', context)

    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            'email': email,
            'first_name': profile.get('given_name', '') or '',
            'last_name': profile.get('family_name', '') or '',
        },
    )
    if created:
        user.set_unusable_password()
        user.save()
    else:
        updated = False
        if user.email != email:
            user.email = email
            updated = True
        if not user.first_name and profile.get('given_name'):
            user.first_name = profile['given_name'] or ''
            updated = True
        if updated:
            user.save()

    # Use GET values here because the redirect came from Google.
    next_url = _safe_next(request.GET.get('state'))
    remember = False  # Google sign-in keeps the default session length.
    request.session.set_expiry(REMEMBER_ME_AGE if remember else 0)
    login(request, user)
    return redirect(next_url or '/birds/')


# ---------------------------------------------------------------------------
# Phone OTP via Firebase
# ---------------------------------------------------------------------------

def _verify_firebase_id_token(id_token):
    """Verify a Firebase ID token and return the phone number, or None.

    Returns None (never raises) when firebase_admin is not installed,
    when no credentials are configured, or when the token is invalid.
    """
    try:
        import firebase_admin
        from firebase_admin import auth, credentials
    except ImportError:
        return None

    try:
        if not firebase_admin._apps:
            service_account_json = os.environ.get(
                'FIREBASE_SERVICE_ACCOUNT_JSON', ''
            )
            if service_account_json:
                cred = credentials.Certificate(
                    json.loads(service_account_json)
                )
            else:
                cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        decoded = auth.verify_id_token(id_token)
        return decoded.get('phone_number') or None
    except Exception:
        return None


@require_POST
def phone_verify(request):
    """Verify a Firebase phone-auth ID token and sign the user in."""
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse(
            {'ok': False, 'error': 'Invalid request.'}, status=400
        )

    id_token = payload.get('id_token')
    if not id_token:
        return JsonResponse(
            {'ok': False, 'error': 'Missing token.'}, status=400
        )

    phone = _verify_firebase_id_token(id_token)
    if not phone:
        return JsonResponse({
            'ok': False,
            'error': 'Phone login is not configured yet.',
        })

    user, _ = User.objects.get_or_create(username=phone)
    request.session.set_expiry(REMEMBER_ME_AGE)
    login(request, user)
    return JsonResponse({'ok': True})
