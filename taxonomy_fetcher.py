import os
import json
import requests

from bs4 import BeautifulSoup

DATABASE_DIR = "bird_database"

HEADERS = {

    "User-Agent":
    "Mozilla/5.0"
}

# =====================================
# FETCH TAXONOMY
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

        family = ""
        genus = ""
        conservation = ""

        # =================================
        # INFOBOX
        # =================================

        infobox = soup.find(

            "table",

            class_="infobox biota"
        )

        if infobox:

            rows = infobox.find_all("tr")

            for row in rows:

                text = row.get_text(
                    " ",
                    strip=True
                )

                # FAMILY

                if text.startswith(
                    "Family:"
                ):

                    family = text.replace(
                        "Family:",
                        ""
                    ).strip()

                # GENUS

                if text.startswith(
                    "Genus:"
                ):

                    genus = text.replace(
                        "Genus:",
                        ""
                    ).strip()

                # CONSERVATION

                if (
                    "Conservation status"
                    in text
                ):

                    conservation = (
                        text.replace(
                            "Conservation status",
                            ""
                        )
                        .strip()
                    )

        # =================================
        # SAVE
        # =================================

        data["family"] = family
        data["genus"] = genus
        data[
            "conservation_status"
        ] = conservation

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
            f"{family}"
        )

    except Exception as e:

        print(
            f"ERROR: {folder}"
        )

print(
    "\nALL TAXONOMY UPDATED"
)