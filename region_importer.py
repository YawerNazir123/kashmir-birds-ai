import os
import json

# ==========================================
# PATHS
# ==========================================

DATABASE_DIR = "bird_database"

REGION_DIR = "bird_regions"

JAMMU_FILE = os.path.join(
    REGION_DIR,
    "jammu.txt"
)

KASHMIR_FILE = os.path.join(
    REGION_DIR,
    "kashmir.txt"
)

LADAKH_FILE = os.path.join(
    REGION_DIR,
    "ladakh.txt"
)

# ==========================================
# LOAD REGION FILES
# ==========================================

def load_birds(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return set(

            line.strip()

            for line in f

            if line.strip()
        )

jammu_birds = load_birds(
    JAMMU_FILE
)

kashmir_birds = load_birds(
    KASHMIR_FILE
)

ladakh_birds = load_birds(
    LADAKH_FILE
)

# ==========================================
# PROCESS DATABASE
# ==========================================

updated = 0

for folder in os.listdir(
    DATABASE_DIR
):

    folder_path = os.path.join(

        DATABASE_DIR,
        folder
    )

    json_path = os.path.join(

        folder_path,
        "info.json"
    )

    # ======================================
    # CHECK FILE
    # ======================================

    if not os.path.exists(
        json_path
    ):

        continue

    # ======================================
    # LOAD JSON
    # ======================================

    with open(

        json_path,
        "r",
        encoding="utf-8"

    ) as f:

        data = json.load(f)

    bird_name = data.get(
        "common_name",
        ""
    ).strip()

    # ======================================
    # FIND REGIONS
    # ======================================

    regions = []

    if bird_name in jammu_birds:

        regions.append(
            "Jammu"
        )

    if bird_name in kashmir_birds:

        regions.append(
            "Kashmir Valley"
        )

    if bird_name in ladakh_birds:

        regions.append(
            "Ladakh"
        )

    # ======================================
    # DEFAULT
    # ======================================

    if not regions:

        regions.append(
            "Kashmir Valley"
        )

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    regions = list(
        dict.fromkeys(
            regions
        )
    )

    # ======================================
    # SAVE REGIONS
    # ======================================

    data["region"] = ", ".join(
        regions
    )

    # ======================================
    # WRITE JSON
    # ======================================

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

    updated += 1

    print(
        f"{bird_name}"
        f" → "
        f"{data['region']}"
    )

# ==========================================
# FINAL RESULT
# ==========================================

print("\n====================")

print(
    f"{updated} birds updated successfully."
)

print(
    "\nMulti-region support enabled."
)