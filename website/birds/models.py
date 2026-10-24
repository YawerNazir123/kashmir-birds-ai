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
    local_name_kashmiri = models.CharField(max_length=200, blank=True, default="")
    local_name_dogri = models.CharField(max_length=200, blank=True, default="")
    local_name_ladakhi = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):

        return self.common_name