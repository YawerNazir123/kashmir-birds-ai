import json
import os

from django.core.management.base import BaseCommand

from birds.models import Bird

# Same source as import_birds: bird_database/ sits next to website/
# in the repo checkout.
BASE_DIR = "../bird_database"


class Command(BaseCommand):

    help = (
        "Sync Kashmiri/Dogri/Ladakhi local names from "
        "bird_database/*/info.json into the database. "
        "Only the three local-name fields are touched -- "
        "no images, no other metadata -- so this is safe "
        "to run on every deploy."
    )

    def handle(self, *args, **kwargs):

        updated = 0
        unchanged = 0
        missing = 0

        for folder in sorted(os.listdir(BASE_DIR)):

            folder_path = os.path.join(BASE_DIR, folder)
            json_path = os.path.join(folder_path, "info.json")

            if not os.path.exists(json_path):
                continue

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            common_name = data.get("common_name", folder)

            try:
                bird = Bird.objects.get(common_name=common_name)
            except Bird.DoesNotExist:
                missing += 1
                self.stdout.write(
                    f"No DB record for: {common_name}"
                )
                continue

            changed = False

            for field in (
                "local_name_kashmiri",
                "local_name_dogri",
                "local_name_ladakhi",
            ):
                value = (data.get(field) or "").strip()

                if value and getattr(bird, field) != value:
                    setattr(bird, field, value)
                    changed = True

            if changed:
                bird.save(
                    update_fields=[
                        "local_name_kashmiri",
                        "local_name_dogri",
                        "local_name_ladakhi",
                    ]
                )
                updated += 1
            else:
                unchanged += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Local names synced: "
                f"{updated} updated, "
                f"{unchanged} already correct, "
                f"{missing} info.json files with no DB record"
            )
        )
