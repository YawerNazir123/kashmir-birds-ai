import os
import json
import pandas as pd

# ==========================================
# SETTINGS
# ==========================================

BASE_DIR = "bird_database"

all_birds = []

# ==========================================
# READ ALL BIRD FOLDERS
# ==========================================

for folder in os.listdir(BASE_DIR):

    folder_path = os.path.join(
        BASE_DIR,
        folder
    )

    json_path = os.path.join(
        folder_path,
        "info.json"
    )

    if not os.path.exists(json_path):
        continue

    try:

        with open(
            json_path,
            "r",
            encoding="utf-8"
        ) as f:

            bird_data = json.load(f)

        # IMAGE PATHS
        image_paths = []

        for image in bird_data.get(
            "images",
            []
        ):

            image_paths.append(
                os.path.join(
                    folder,
                    image
                )
            )

        # CREATE MASTER RECORD
        bird_record = {
            "common_name": bird_data.get(
                "common_name",
                ""
            ),

            "scientific_name": bird_data.get(
                "scientific_name",
                ""
            ),

            "local_name": bird_data.get(
                "local_name",
                ""
            ),

            "family": bird_data.get(
                "family",
                ""
            ),

            "genus": bird_data.get(
                "genus",
                ""
            ),

            "migratory_status": bird_data.get(
                "migratory_status",
                ""
            ),

            "size": bird_data.get(
                "size",
                ""
            ),

            "wingspan": bird_data.get(
                "wingspan",
                ""
            ),

            "habitat": bird_data.get(
                "habitat",
                ""
            ),

            "conservation_status": bird_data.get(
                "conservation_status",
                ""
            ),

            "description": bird_data.get(
                "description",
                ""
            ),

            "wikipedia_url": bird_data.get(
                "wikipedia_url",
                ""
            ),

            "images": ", ".join(image_paths)
        }

        all_birds.append(
            bird_record
        )

        print(
            f"Added: "
            f"{bird_record['common_name']}"
        )

    except Exception as e:

        print(
            f"Error processing {folder}: {e}"
        )

# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(all_birds)

# ==========================================
# SAVE CSV
# ==========================================

csv_path = "birds_master_database.csv"

df.to_csv(
    csv_path,
    index=False,
    encoding="utf-8"
)

print(
    f"\nMASTER DATABASE CREATED:"
    f" {csv_path}"
)