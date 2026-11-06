"""Sitemaps for the public field guide.

Lists the homepage, the birds database, the gallery and every
bird detail page, so search engines can find all 745 species.
Built from the Bird model, not a hardcoded list.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Bird


class StaticSitemap(Sitemap):
    """Homepage, birds database and gallery (all public pages)."""

    def items(self):
        return ['landing_page', 'birds', 'gallery']

    def location(self, item):
        return reverse(item)


class BirdSitemap(Sitemap):
    """One entry per bird detail page, from the Bird model."""

    def items(self):
        return Bird.objects.all().order_by('id')

    def location(self, obj):
        return reverse('bird_detail', args=[obj.pk])
