import os
import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'website.settings'
)

django.setup()

from birds.models import Bird

# ==========================================
# CATEGORY RULES
# ==========================================

CATEGORY_RULES = {

    "Duck": [
        "Mallard",
        "Teal",
        "Pintail",
        "Wigeon",
        "Shoveler",
        "Duck"
    ],

    "Raptor": [
        "Eagle",
        "Kite",
        "Harrier",
        "Falcon",
        "Kestrel"
    ],

    "Owl": [
        "Owl",
        "Owlet"
    ],

    "Pigeon/Dove": [
        "Pigeon",
        "Dove"
    ],

    "Kingfisher": [
        "Kingfisher"
    ],

    "Egret/Heron": [
        "Egret",
        "Heron"
    ],

    "Songbird": [
        "Sparrow",
        "Bulbul",
        "Robin",
        "Flycatcher",
        "Wagtail",
        "Thrush"
    ]
}

# ==========================================
# AUTO CATEGORY ASSIGNMENT
# ==========================================

birds = Bird.objects.all()

for bird in birds:

    assigned = False

    for category, keywords in (
        CATEGORY_RULES.items()
    ):

        for keyword in keywords:

            if keyword.lower() in (
                bird.common_name.lower()
            ):

                bird.category = category

                bird.save()

                print(
                    f"{bird.common_name}"
                    f" → {category}"
                )

                assigned = True

                break

        if assigned:
            break

    if not assigned:

        bird.category = "Other"

        bird.save()

        print(
            f"{bird.common_name}"
            f" → Other"
        )

print("\nALL BIRDS CATEGORIZED")