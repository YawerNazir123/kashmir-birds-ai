from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

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
# the repo). Django only serves them automatically when DEBUG is on,
# so serve them explicitly in production too. This uses Django's
# static-file view, which is fine for a small free-tier field guide;
# if traffic grows, move media to object storage (S3/Cloudinary)
# and remove this block. Uploads made through the running site are
# still lost on restart/redeploy -- Render's filesystem is ephemeral.
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
