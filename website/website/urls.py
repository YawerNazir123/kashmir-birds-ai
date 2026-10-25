from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.views.static import serve

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

# Media files are the bird photos in website/media/birds/ (committed to
# the repo). The previous code used django.conf.urls.static.static(),
# but static() returns an empty list when DEBUG is False, so in
# production it added no route at all and every /media/ URL 404'd
# even though the files exist in the checkout. Serve them explicitly
# with django.views.static.serve instead. This is the documented
# development-style file server; it is fine for a small free-tier
# field guide. If traffic grows, move media to object storage
# (S3/Cloudinary) and remove this block. Uploads made through the
# running site are still lost on restart/redeploy -- Render's
# filesystem is ephemeral.
urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
