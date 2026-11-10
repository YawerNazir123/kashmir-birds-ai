"""Sign-in / sign-up views for the site.

Email + password only (Django's built-in User model). No external
providers, no extra configuration needed: anyone can create an account
on the login page and sign in immediately.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

REMEMBER_ME_AGE = 2592000  # 30 days, in seconds (was one year)


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
    context = {
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
            # Enforce Django's password validators (common-password,
            # numeric, similarity). The 8+ check above runs first;
            # validate_password adds the rest. A transient unsaved
            # User lets the similarity validator compare the
            # password against the email/username.
            try:
                validate_password(
                    password,
                    user=User(username=email, email=email),
                )
            except ValidationError as exc:
                context['errors'].extend(exc.messages)
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
