import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.storage import default_storage

from birds.models import Bird

# bird_database/ sits next to website/ in the repo checkout.
# Resolve it from this file's location, not the working
# directory, so the command works wherever manage.py is run
# from (Render's build runs it from website/, a local run
# may differ -- a relative "../bird_database" would break).
BASE_DIR = str(
    Path(__file__).resolve().parents[3].parent / "bird_database"
)


class Command(BaseCommand):

    help = "Import birds into database"

    def handle(self, *args, **kwargs):

        imported_names = set()
        created_count = 0
        updated_count = 0

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

            common_name = data.get(
                "common_name",
                folder
            )
            imported_names.add(common_name)

            # ==================================
            # CREATE OR UPDATE BIRD
            # ==================================

            bird, created = Bird.objects.update_or_create(

                common_name=common_name,

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

            if created:
                created_count += 1
            else:
                updated_count += 1

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
        # PRUNE STALE RECORDS
        # ==================================
        # The committed db.sqlite3 predates the metadata
        # fixes, so it still holds birds that were deleted
        # from bird_database/ (non-occurrences in J&K,
        # duplicate merges) and rows under old names of
        # birds that were renamed in info.json. import
        # alone would leave those stale rows in the
        # gallery alongside the corrected ones, so remove
        # every DB record whose common_name has no
        # info.json file. Records created in the DB with
        # no folder are not affected -- every legitimate
        # bird has an info.json file.
        stale = Bird.objects.exclude(
            common_name__in=imported_names
        )
        pruned_count = stale.count()
        stale_names = list(
            stale.values_list("common_name", flat=True)
        )
        stale.delete()
        for name in stale_names:
            self.stdout.write(
                f"Pruned stale record: {name}"
            )

        # ==================================
        # FINISHED
        # ==================================

        self.stdout.write(

            self.style.SUCCESS(

                "\nALL BIRDS IMPORTED"
            )
        )
        self.stdout.write(
            f"Created: {created_count}, "
            f"updated: {updated_count}, "
            f"pruned stale: {pruned_count}"
        )
