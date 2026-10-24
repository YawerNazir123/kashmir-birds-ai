import os
import json
import requests
import wikipedia
from tqdm import tqdm
from urllib.parse import quote

# ==========================================
# BIRDS LIST
# ==========================================
# ==========================================
# LOAD BIRD LIST FROM FILE
# ==========================================

with open(
    "kashmir_birds_list.txt",
    "r",
    encoding="utf-8"
) as f:

    birds = [
        line.strip()
        for line in f.readlines()
        if line.strip()
    ]

# ==========================================
# SETTINGS
# ==========================================

BASE_DIR = "bird_database"
IMAGES_PER_BIRD = 5

os.makedirs(BASE_DIR, exist_ok=True)

# ==========================================
# DOWNLOAD IMAGES
# ==========================================

def download_images(bird_name, bird_folder):

    print(f"\nDownloading images for {bird_name}")

    query = quote(bird_name)

    url = (
        f"https://api.inaturalist.org/v1/observations"
        f"?taxon_name={query}"
        f"&photos=true"
        f"&per_page={IMAGES_PER_BIRD}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch images")
        return []

    data = response.json()

    image_files = []

    count = 1

    for item in tqdm(data["results"]):

        photos = item.get("photos", [])

        for photo in photos:

            try:

                image_url = photo["url"].replace("square", "large")

                image_data = requests.get(image_url).content

                image_name = f"{count}.jpg"

                image_path = os.path.join(
                    bird_folder,
                    image_name
                )

                with open(image_path, "wb") as f:
                    f.write(image_data)

                image_files.append(image_name)

                count += 1

                if count > IMAGES_PER_BIRD:
                    return image_files

            except Exception as e:
                print("Error:", e)

    return image_files

# ==========================================
# GET WIKIPEDIA INFO
# ==========================================

def get_bird_info(bird_name):

    try:

        page = wikipedia.page(bird_name)

        summary = wikipedia.summary(
            bird_name,
            sentences=3
        )

        return {
            "title": page.title,
            "summary": summary,
            "url": page.url
        }

    except Exception as e:

        print("Wikipedia Error:", e)

        return {
            "title": bird_name,
            "summary": "No information available.",
            "url": ""
        }

# ==========================================
# MAIN LOOP
# ==========================================

for bird in birds:

    print(f"\nProcessing {bird}")

    folder_name = bird.lower().replace(" ", "_")

    bird_folder = os.path.join(
        BASE_DIR,
        folder_name
    )

    os.makedirs(bird_folder, exist_ok=True)

    # Download Images
    images = download_images(
        bird,
        bird_folder
    )

    # Fetch Bird Information
    info = get_bird_info(bird)

    # Create JSON Data
    bird_data = {
        "common_name": bird,
        "scientific_name": "",
        "local_name": "",
        "migratory_status": "Resident",
        "size": "",
        "wingspan": "",
        "habitat": "",
        "iucn_status": "",
        "description": info["summary"],
        "wikipedia_url": info["url"],
        "images": images
    }

    # Save JSON File
    json_path = os.path.join(
        bird_folder,
        "info.json"
    )

    with open(json_path, "w", encoding="utf-8") as f:

        json.dump(
            bird_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"{bird} completed.")

print("\nALL BIRDS DOWNLOADED SUCCESSFULLY")