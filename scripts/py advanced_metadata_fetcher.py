import os
import json
import requests
import wikipedia

# ==========================================
# SETTINGS
# ==========================================

BASE_DIR = "bird_database"

# ==========================================
# FETCH INATURALIST DATA
# ==========================================

def fetch_inaturalist_data(bird_name):

    url = (
        "https://api.inaturalist.org/v1/taxa"
        f"?q={bird_name}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data["results"]:
        return None

    bird = data["results"][0]

    info = {
        "scientific_name": bird.get("name", ""),
        "common_name": bird.get("preferred_common_name", bird_name),
        "family": "",
        "genus": "",
        "conservation_status": "",
        "wikipedia_url": bird.get("wikipedia_url", "")
    }

    # TAXONOMY
    ancestors = bird.get("ancestors", [])

    for a in ancestors:

        rank = a.get("rank", "")

        if rank == "family":
            info["family"] = a.get("name", "")

        elif rank == "genus":
            info["genus"] = a.get("name", "")

    # CONSERVATION STATUS
    status = bird.get("conservation_status")

    if status:
        info["conservation_status"] = status.get(
            "status_name",
            ""
        )

    return info

# ==========================================
# FETCH WIKIPEDIA SUMMARY
# ==========================================

def fetch_wikipedia_summary(bird_name):

    try:

        summary = wikipedia.summary(
            bird_name,
            sentences=3
        )

        return summary

    except:
        return "No description available."

# ==========================================
# UPDATE JSON FILES
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

    with open(json_path, "r", encoding="utf-8") as f:

        bird_data = json.load(f)

    bird_name = bird_data["common_name"]

    print(f"\nUpdating {bird_name}")

    # FETCH DATA
    inat_data = fetch_inaturalist_data(
        bird_name
    )

    wiki_summary = fetch_wikipedia_summary(
        bird_name
    )

    if inat_data:

        bird_data["scientific_name"] = (
            inat_data["scientific_name"]
        )

        bird_data["family"] = (
            inat_data["family"]
        )

        bird_data["genus"] = (
            inat_data["genus"]
        )

        bird_data["conservation_status"] = (
            inat_data["conservation_status"]
        )

        bird_data["wikipedia_url"] = (
            inat_data["wikipedia_url"]
        )

    bird_data["description"] = wiki_summary

    # SAVE UPDATED JSON
    with open(json_path, "w", encoding="utf-8") as f:

        json.dump(
            bird_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"{bird_name} updated successfully.")

print("\nALL BIRD METADATA UPDATED.")