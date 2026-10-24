import os
import json

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.storage import default_storage

from birds.models import Bird

BASE_DIR = "../bird_database"


class Command(BaseCommand):

    help = "Import birds into database"

    def handle(self, *args, **kwargs):

        for folder in os.listdir(BASE_DIR):

            folder_path = os.path.join(

                BASE_DIR,

                folder
            )

            json_path = os.path.join(

                folder_path,

                "info.json"
            )

            if not os.path.exists(
                json_path
            ):

                continue

            with open(

                json_path,

                "r",

                encoding="utf-8"

            ) as f:

                data = json.load(f)

            # ==================================
            # CREATE OR UPDATE BIRD
            # ==================================

            bird, created = Bird.objects.update_or_create(

                common_name=data.get(

                    "common_name",

                    folder
                ),

                defaults={

                    "scientific_name":

                    data.get(
                        "scientific_name",
                        ""
                    ),

                    "region":

                    data.get(
                        "region",
                        ""
                    ),

                    "local_name":

                    data.get(
                        "local_name",
                        ""
                    ),
                    "local_name_kashmiri":

                    data.get(
                        "local_name_kashmiri",
                        ""
                    ),

                    "local_name_dogri":

                    data.get(
                        "local_name_dogri",
                        ""
                    ),

                    "local_name_ladakhi":

                    data.get(
                        "local_name_ladakhi",
                        ""
                    ),

                    "family":

                    data.get(
                        "family",
                        ""
                    ),

                    "genus":

                    data.get(
                        "genus",
                        ""
                    ),

                    "length":

                    data.get(
                        "length",
                        ""
                    ),

                    "wingspan":

                    data.get(
                        "wingspan",
                        ""
                    ),

                    "weight":

                    data.get(
                        "weight",
                        ""
                    ),

                    "category":

                    data.get(
                        "category",
                        "Other"
                    ),

                    "migratory_status":

                    data.get(
                        "migratory_status",
                        "Resident"
                    ),

                    "conservation_status":

                    data.get(
                        "conservation_status",
                        ""
                    ),

                    "habitat":

                    data.get(
                        "habitat",
                        ""
                    ),

                    "description":

                    data.get(
                        "description",
                        ""
                    ),

                    "wikipedia_url":

                    data.get(
                        "wikipedia_url",
                        ""
                    )
                }
            )

            # ==================================
            # IMPORT IMAGES
            # ==================================

            images = data.get(
                "images",
                []
            )

            gallery_paths = []

            if images:

                for index, img in enumerate(images):

                    image_path = os.path.join(
                        folder_path,
                        img
                    )

                    if os.path.exists(image_path):

                        with open(
                            image_path,
                            "rb"
                        ) as img_file:

                            image_name = (
                                f"{folder}_{img}"
                            )

                            # MAIN IMAGE

                            if index == 0:

                                bird.image.save(

                                    image_name,

                                    File(img_file),

                                    save=True
                                )

                                gallery_paths.append(

                                    bird.image.name
                                )

                            # EXTRA IMAGES

                            else:

                                extra_path = default_storage.save(

                                    f"birds/gallery/{image_name}",

                                    File(img_file)
                                )

                                gallery_paths.append(
                                    extra_path
                                )

            # SAVE GALLERY

            bird.extra_images = gallery_paths

            bird.save()

            # ==================================
            # SUCCESS MESSAGE
            # ==================================

            self.stdout.write(

                self.style.SUCCESS(

                    f"Imported: "
                    f"{bird.common_name}"
                )
            )

        # ==================================
        # FINISHED
        # ==================================

        self.stdout.write(

            self.style.SUCCESS(

                "\nALL BIRDS IMPORTED"
            )
        )