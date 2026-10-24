import os
import json

DATABASE_DIR = "bird_database"

# =====================================
# REGION TEXT
# =====================================

REGION_INFO = {

    "Kashmir Valley":
    "across the wetlands, forests and river systems of Kashmir Valley",

    "Jammu":
    "through the plains, forests and agricultural landscapes of Jammu",

    "Ladakh":
    "within the cold deserts, alpine regions and high-altitude wetlands of Ladakh"
}

# =====================================
# STATUS TEXT
# =====================================

STATUS_INFO = {

    "Resident":
    "is a resident bird species commonly found",

    "Winter Migratory":
    "is a winter migratory bird frequently observed",

    "Summer Migratory":
    "is a summer migratory species recorded",

    "Rare Visitor":
    "is considered a rare visitor occasionally sighted"
}

# =====================================
# CATEGORY TEXT
# =====================================

CATEGORY_INFO = {

    "Duck":
    "near lakes, marshes and wetlands.",

    "Raptor":
    "across mountains, cliffs and open valleys.",

    "Songbird":
    "within forests, gardens and woodland habitats.",

    "Wader":
    "along riverbanks and shallow wetland areas.",

    "Owl":
    "inside forests and rocky landscapes.",

    "Waterbird":
    "around wetlands and freshwater ecosystems.",

    "Other":
    "across diverse ecological habitats."
}

# =====================================
# GENERATE
# =====================================

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

    common_name = data.get(
        "common_name",
        "This bird"
    )

    status = data.get(
        "migratory_status",
        "Resident"
    )

    region = data.get(
        "region",
        "Kashmir Valley"
    )

    category = data.get(
        "category",
        "Other"
    )

    # ================================
    # BUILD DESCRIPTION
    # ================================

    desc = (

        f"The {common_name} "

        f"{STATUS_INFO.get(status, 'is a bird species found')} "

        f"{REGION_INFO.get(region, 'across Himalayan regions')} "

        f"{CATEGORY_INFO.get(category, 'across diverse habitats.')} "

        f"This species contributes to the rich avian biodiversity "

        f"of Jammu, Kashmir and Ladakh."
    )

    data["description"] = desc

    # ================================
    # SAVE
    # ================================

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
        f"UPDATED: {common_name}"
    )

print(
    "\nALL DESCRIPTIONS GENERATED"
)