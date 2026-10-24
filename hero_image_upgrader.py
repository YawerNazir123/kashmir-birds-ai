import os
import json
import requests

DATABASE_DIR = "bird_database"

HEADERS = {

    "User-Agent":
    "Mozilla/5.0"
}

# =====================================
# DOWNLOAD IMAGE
# =====================================

def download_image(url, save_path):

    try:

        response = requests.get(

            url,

            headers=HEADERS,

            timeout=20
        )

        if response.status_code == 200:

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(response.content)

            return True

    except Exception:

        return False

    return False


# =====================================
# GET INATURALIST IMAGE
# =====================================

def get_inat_image(bird_name):

    try:

        url = (

            "https://api.inaturalist.org/v1/search"
        )

        params = {

            "q": bird_name,

            "sources": "taxa"
        }

        response = requests.get(

            url,

            params=params,

            headers=HEADERS,

            timeout=20
        )

        data = response.json()

        results = data.get(
            "results",
            []
        )

        for item in results:

            record = item.get(
                "record",
                {}
            )

            photo = record.get(
                "default_photo"
            )

            if photo:

                image_url = photo.get(
                    "medium_url"
                )

                if image_url:

                    # HIGHER QUALITY

                    image_url = image_url.replace(

                        "medium",

                        "large"
                    )

                    return image_url

    except Exception:

        return None

    return None


# =====================================
# MAIN
# =====================================

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
        folder
    )

    print(
        f"Searching: {bird_name}"
    )

    image_url = get_inat_image(
        bird_name
    )

    if image_url:

        save_path = os.path.join(

            folder_path,

            "1.jpg"
        )

        success = download_image(

            image_url,

            save_path
        )

        if success:

            print(
                f"UPDATED: {bird_name}"
            )

        else:

            print(
                f"FAILED: {bird_name}"
            )

    else:

        print(
            f"NO IMAGE: {bird_name}"
        )

print(
    "\nALL HERO IMAGES UPDATED"
)