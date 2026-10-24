import os
import json

DATABASE_DIR = "bird_database"

updated = 0

for folder in os.listdir(DATABASE_DIR):

    folder_path = os.path.join(DATABASE_DIR, folder)

    if not os.path.isdir(folder_path):
        continue

    json_path = os.path.join(folder_path, "info.json")

    if not os.path.exists(json_path):
        continue

    try:

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "local_name_kashmiri" not in data:
            data["local_name_kashmiri"] = ""

        if "local_name_dogri" not in data:
            data["local_name_dogri"] = ""

        if "local_name_ladakhi" not in data:
            data["local_name_ladakhi"] = ""

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        updated += 1

    except Exception as e:

        print(f"ERROR: {folder}")
        print(e)

print(f"\nUpdated {updated} birds successfully.")