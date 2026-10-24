import os
import json

DATABASE_DIR = "bird_database"

# ======================================
# CATEGORY RULES
# ======================================

CATEGORY_RULES = {

    "Duck": "Duck",
    "Goose": "Duck",
    "Swan": "Duck",

    "Eagle": "Raptor",
    "Hawk": "Raptor",
    "Falcon": "Raptor",
    "Kite": "Raptor",
    "Harrier": "Raptor",
    "Buzzard": "Raptor",
    "Owl": "Owl",
    "Vulture": "Raptor",

    "Kingfisher": "Kingfisher",

    "Pigeon": "Pigeon/Dove",
    "Dove": "Pigeon/Dove",

    "Heron": "Egret/Heron",
    "Egret": "Egret/Heron",
    "Bittern": "Egret/Heron",

    "Warbler": "Songbird",
    "Flycatcher": "Songbird",
    "Robin": "Songbird",
    "Thrush": "Songbird",
    "Wagtail": "Songbird",
    "Bunting": "Songbird",
    "Finch": "Songbird",
    "Pipit": "Songbird",
    "Shrike": "Songbird",
    "Swallow": "Songbird",
    "Starling": "Songbird",
    "Minivet": "Songbird",
    "Bulbul": "Songbird",
    "Accentor": "Songbird",
}

# ======================================
# PROCESS
# ======================================

for folder in os.listdir(
    DATABASE_DIR
):

    json_path = os.path.join(

        DATABASE_DIR,

        folder,

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

    bird_name = data.get(
        "common_name",
        ""
    )

    category = "Other"

    for key, value in CATEGORY_RULES.items():

        if key.lower() in bird_name.lower():

            category = value

    data["category"] = category

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
        f"{bird_name}"
        f" → {category}"
    )

print(
    "\nALL CATEGORIES UPDATED"
)