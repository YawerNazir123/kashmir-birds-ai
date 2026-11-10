from django.contrib import admin
from django.urls import path, include, re_path

from pathlib import Path

from django.conf import settings
from django.views.static import serve


def _cached_serve(request, path, document_root):
    """Serve a file with a long browser cache lifetime.

    Bird photos are large and change rarely, so browsers and the CDN
    in front of the site may cache them for a year. NOT "immutable":
    a photo can be replaced in place in the repo, so a stale
    year-long cache would be wrong.
    """
    response = serve(request, path, document_root=document_root)
    response['Cache-Control'] = 'public, max-age=31536000'
    return response

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('birds.urls')
    ),
]

# /media/ is the legacy upload path (Bird.image files under "birds/").
# The previous code used django.conf.urls.static.static(), but static()
# returns an empty list when DEBUG is False, so in production it added
# no route at all and every /media/ URL 404'd even though the files
# exist in the checkout. Serve them explicitly with
# django.views.static.serve instead. This is the documented
# development-style file server; it is fine for a small free-tier
# field guide. If traffic grows, move media to object storage
# (S3/Cloudinary) and remove this block. Uploads made through the
# running site are still lost on restart/redeploy -- Render's
# filesystem is ephemeral.
urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        _cached_serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]

# Bird photos are committed to the repo under bird_database/<folder>/<n>.jpg.
# Serve them directly from the checkout so redeploys can never wipe them.
# (The old /media/ bird-photo pipeline copied files to an ephemeral disk
# and generated random-suffixed names; it is retired.)
BIRD_DATABASE_ROOT = Path(__file__).resolve().parent.parent.parent / "bird_database"
urlpatterns += [
    re_path(
        r'^bird-images/(?P<path>.*)$',
        _cached_serve,
        {'document_root': BIRD_DATABASE_ROOT},
    ),
]
