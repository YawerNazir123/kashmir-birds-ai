from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.urls import path
from . import views, auth_views
from .sitemaps import BirdSitemap, StaticSitemap

sitemaps = {
    'static': StaticSitemap,
    'birds': BirdSitemap,
}

urlpatterns = [

    # HOME PAGE
    path(
        '',
        views.landing_page,
        name='landing_page'
    ),

    # SITEMAP + ROBOTS (public, for search engines)
    path(
        'sitemap.xml',
        sitemap_view,
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    path(
        'robots.txt',
        views.robots_txt,
        name='robots_txt'
    ),

    # BIRDS DATABASE
    path(
        'birds/',
        views.home,
        name='birds'
    ),

    # AI IDENTIFICATION
    path(
        'identify/',
        views.identify_bird,
        name='identify_bird'
    ),

    # DETAIL PAGE
    path(
        'bird/<int:id>/',
        views.bird_detail,
        name='bird_detail'
    ),
    path(
    'gallery/',
    views.gallery,
    name='gallery'
),
path(
    'about/',
    views.about,
    name='about'
),
path(
    'contact/',
    views.contact,
    name='contact'
),

# SIGN-IN
path(
    'login/',
    auth_views.login_page,
    name='login'
),
path(
    'logout/',
    auth_views.logout_view,
    name='logout'
),
]
