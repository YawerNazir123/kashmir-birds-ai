import os
import requests
from urllib.parse import quote

# ==========================================
# SETTINGS
# ==========================================

BASE_DIR = "bird_database"

IMAGES_PER_BIRD = 5

# ==========================================
# GET WIKIMEDIA IMAGES
# ==========================================

def get_wikimedia_images(bird_name):

    search_query = quote(bird_name)

    url = (
        "https://commons.wikimedia.org/w/api.php"
        "?action=query"
        "&generator=search"
        "&gsrnamespace=6"
        f"&gsrsearch={search_query}"
        "&gsrlimit=10"
        "&prop=imageinfo"
        "&iiprop=url"
        "&format=json"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    pages = data.get("query", {}).get("pages", {})

    image_urls = []

    for page_id in pages:

        try:

            image_url = pages[page_id][
                "imageinfo"
            ][0]["url"]

            # FILTER BAD FILE TYPES
            if image_url.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png"
                )
            ):

                image_urls.append(
                    image_url
                )

        except:
            continue

    return image_urls

# ==========================================
# DOWNLOAD IMAGES
# ==========================================

def download_images(
    bird_name,
    folder_path
):

    print(f"\nDownloading {bird_name}")

    image_urls = get_wikimedia_images(
        bird_name
    )

    count = 1

    for url in image_urls:

        try:

            response = requests.get(url)

            if response.status_code != 200:
                continue

            image_path = os.path.join(
                folder_path,
                f"{count}.jpg"
            )

            with open(
                image_path,
                "wb"
            ) as f:

                f.write(response.content)

            print(
                f"Downloaded image {count}"
            )

            count += 1

            if count > IMAGES_PER_BIRD:
                break

        except Exception as e:

            print("Error:", e)

# ==========================================
# MAIN LOOP
# ==========================================

for folder in os.listdir(BASE_DIR):

    folder_path = os.path.join(
        BASE_DIR,
        folder
    )

    bird_name = folder.replace(
        "_",
        " "
    ).title()

    download_images(
        bird_name,
        folder_path
    )

print(
    "\nALL WIKIMEDIA IMAGES DOWNLOADED"
)