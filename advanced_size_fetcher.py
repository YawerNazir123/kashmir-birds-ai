import os
import json
import re
import requests

from bs4 import BeautifulSoup

DATABASE_DIR = "bird_database"

HEADERS = {

    "User-Agent":
    "Mozilla/5.0"
}

# ======================================
# EXTRACT MEASUREMENTS
# ======================================

def extract_measurements(text):

    length = ""
    wingspan = ""
    weight = ""

    # LENGTH
    length_match = re.search(

        r'(\d+(?:–|-)?\d*\s?cm)',

        text
    )

    if length_match:

        length = length_match.group(1)

    # WINGSPAN
    wingspan_match = re.search(

        r'wingspan.*?(\d+(?:–|-)?\d*\s?cm)',

        text,

        re.IGNORECASE
    )

    if wingspan_match:

        wingspan = wingspan_match.group(1)

    # WEIGHT
    weight_match = re.search(

        r'(\d+(?:–|-)?\d*\s?g)',

        text
    )

    if weight_match:

        weight = weight_match.group(1)

    return length, wingspan, weight

# ======================================
# PROCESS BIRDS
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

    wiki_url = data.get(
        "wikipedia_url",
        ""
    )

    if not wiki_url:

        continue

    try:

        response = requests.get(

            wiki_url,

            headers=HEADERS,

            timeout=15
        )

        soup = BeautifulSoup(

            response.text,

            "html.parser"
        )

        text = soup.get_text()

        length, wingspan, weight = (
            extract_measurements(text)
        )

        data["length"] = length
        data["wingspan"] = wingspan
        data["weight"] = weight

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

            f"{data.get('common_name')}"

            f" → "

            f"L:{length} "

            f"W:{wingspan} "

            f"WT:{weight}"
        )

    except Exception as e:

        print(
            f"ERROR: {folder}"
        )

print(
    "\nALL SIZE METADATA UPDATED"
)