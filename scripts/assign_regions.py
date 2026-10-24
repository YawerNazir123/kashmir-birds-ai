import os
import json

DATABASE_DIR = "bird_database"

# ==========================================
# REGION RULES
# ==========================================

LADAKH_KEYWORDS = [

    "Snowcock",
    "Accentor",
    "Chough",
    "Tibetan",
    "Snowfinch",
    "Lammergeier",
    "Monal"
]

JAMMU_KEYWORDS = [

    "Hornbill",
    "Parakeet",
    "Babbler",
    "Treepie",
    "Drongo"
]

# ==========================================
# PROCESS BIRDS
# ==========================================

for bird_folder in os.listdir(
    DATABASE_DIR
):

    folder_path = os.path.join(
        DATABASE_DIR,
        bird_folder
    )

    json_path = os.path.join(
        folder_path,
        "info.json"
    )

    if not os.path.exists(json_path):
        continue

    with open(
        json_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    bird_name = data.get(
        "common_name",
        ""
    )

    # DEFAULT
    region = "Kashmir Valley"

    # LADAKH
    for keyword in LADAKH_KEYWORDS:

        if keyword.lower() in (
            bird_name.lower()
        ):

            region = "Ladakh"

    # JAMMU
    for keyword in JAMMU_KEYWORDS:

        if keyword.lower() in (
            bird_name.lower()
        ):

            region = "Jammu"

    # SAVE
    data["region"] = region

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"{bird_name} → {region}"
    )

print(
    "\nALL REGIONS ASSIGNED"
)