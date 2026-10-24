import os

os.environ.setdefault(

    "DJANGO_SETTINGS_MODULE",

    "website.settings"
)

import django

django.setup()

from birds.models import Bird

# ==========================================
# TRACK UNIQUE BIRDS
# ==========================================

seen = set()

duplicates = []

# ==========================================
# CHECK DATABASE
# ==========================================

birds = Bird.objects.all().order_by(
    'id'
)

for bird in birds:

    name = bird.common_name.strip().lower()

    if name in seen:

        duplicates.append(
            bird
        )

    else:

        seen.add(name)

# ==========================================
# DELETE DUPLICATES
# ==========================================

count = 0

for bird in duplicates:

    print(
        f"Deleting duplicate:"
        f" {bird.common_name}"
    )

    bird.delete()

    count += 1

print(
    f"\nTOTAL DUPLICATES "
    f"REMOVED: {count}"
)

print(
    f"TOTAL UNIQUE BIRDS:"
    f" {Bird.objects.count()}"
)