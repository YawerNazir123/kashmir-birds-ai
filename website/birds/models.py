from django.db import models


class Bird(models.Model):

    region = models.CharField(

        max_length=200,

        blank=True,

        null=True
    )

    common_name = models.CharField(

        max_length=200
    )

    scientific_name = models.CharField(

        max_length=200,

        blank=True,

        null=True
    )

    local_name = models.CharField(

        max_length=200,

        blank=True,

        null=True
    )

    family = models.CharField(

        max_length=200,

        blank=True,

        null=True
    )

    genus = models.CharField(

        max_length=200,

        blank=True,

        null=True
    )

    category = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    migratory_status = models.CharField(

        max_length=100,

        default="Resident"
    )
    

    conservation_status = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    habitat = models.TextField(

        blank=True,

        null=True
    )
    length = models.CharField(
    max_length=100,
    blank=True
    )

    wingspan = models.CharField(
    max_length=100,
    blank=True
    )

    weight = models.CharField(
    max_length=100,
    blank=True
    )

    description = models.TextField(

        blank=True,

        null=True
    )

    wikipedia_url = models.URLField(

        blank=True,

        null=True
    )

    image = models.ImageField(

        upload_to="birds/",

        blank=True,

        null=True
    )
    extra_images = models.JSONField(

    blank=True,

    null=True
)

    @property
    def photo_url(self):
        """Public URL for the main bird photo.

        New format (stored by import_birds): repo-relative path like
        "ashy_drongo/1.jpg", served from bird_database/ via /bird-images/.
        Legacy format ("birds/<name>[_<suffix>].jpg", the old media pipeline):
        falls back to the old /media/ URL so nothing renders worse than today.
        """
        name = str(self.image) if self.image else ""
        if not name:
            return ""
        if name.startswith("birds/"):
            return f"/media/{name}"
        return f"/bird-images/{name}"

    @property
    def gallery_urls(self):
        """Public URLs for extra_images, same scheme as photo_url."""
        urls = []
        for p in (self.extra_images or []):
            p = str(p)
            if p.startswith("birds/"):
                urls.append(f"/media/{p}")
            else:
                urls.append(f"/bird-images/{p}")
        return urls

    local_name_kashmiri = models.CharField(max_length=200, blank=True, default="")
    local_name_dogri = models.CharField(max_length=200, blank=True, default="")
    local_name_ladakhi = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):

        return self.common_name


class ContactMessage(models.Model):

    name = models.CharField(

        max_length=200
    )

    email = models.EmailField()

    subject = models.CharField(

        max_length=200,

        blank=True
    )

    message = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return f"{self.name} <{self.email}>"