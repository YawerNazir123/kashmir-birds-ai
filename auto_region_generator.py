import os
import requests
import time

# ==========================================
# FILE PATHS
# ==========================================

BASE_DIR = "bird_regions"

ALL_BIRDS_FILE = os.path.join(
    BASE_DIR,
    "all_birds.txt"
)

JAMMU_FILE = os.path.join(
    BASE_DIR,
    "jammu.txt"
)

KASHMIR_FILE = os.path.join(
    BASE_DIR,
    "kashmir.txt"
)

LADAKH_FILE = os.path.join(
    BASE_DIR,
    "ladakh.txt"
)

# ==========================================
# USER AGENT
# ==========================================

HEADERS = {

    "User-Agent":
    "BirdsOfParadise/1.0"
}

# ==========================================
# ECOLOGICAL REGION BOXES
# ==========================================

REGIONS = {

    "Jammu": {

        "swlat": 31.0,
        "swlng": 73.0,

        "nelat": 33.9,
        "nelng": 76.0
    },

    "Kashmir Valley": {

        "swlat": 33.0,
        "swlng": 73.0,

        "nelat": 35.7,
        "nelng": 76.5
    },

    "Ladakh": {

        "swlat": 34.0,
        "swlng": 75.0,

        "nelat": 37.8,
        "nelng": 80.5
    }
}

# ==========================================
# READ ALL BIRDS
# ==========================================

with open(
    ALL_BIRDS_FILE,
    "r",
    encoding="utf-8"
) as f:

    all_birds = [

        line.strip()

        for line in f

        if line.strip()
    ]

# ==========================================
# REGION SETS
# ==========================================

jammu_birds = set()

kashmir_birds = set()

ladakh_birds = set()

# ==========================================
# GET TAXON ID
# ==========================================

def get_taxon_id(bird_name):

    try:

        url = (

            "https://api.inaturalist.org/v1/taxa"
        )

        params = {

            "q": bird_name,

            "rank": "species",

            "per_page": 1
        }

        response = requests.get(

            url,

            params=params,

            headers=HEADERS,

            timeout=20
        )

        if response.status_code != 200:

            return None

        data = response.json()

        results = data.get(
            "results",
            []
        )

        if not results:

            return None

        return results[0]["id"]

    except Exception:

        return None

# ==========================================
# CHECK REGION OBSERVATIONS
# ==========================================

def exists_in_region(

    taxon_id,
    region_box
):

    try:

        url = (

            "https://api.inaturalist.org/v1/observations"
        )

        params = {

            "taxon_id": taxon_id,

            "quality_grade": "research",

            "geo": "true",

            "per_page": 1,

            "swlat": region_box["swlat"],
            "swlng": region_box["swlng"],

            "nelat": region_box["nelat"],
            "nelng": region_box["nelng"]
        }

        response = requests.get(

            url,

            params=params,

            headers=HEADERS,

            timeout=30
        )

        if response.status_code != 200:

            return False

        data = response.json()

        total = data.get(
            "total_results",
            0
        )

        return total > 0

    except Exception:

        return False

# ==========================================
# PROCESS BIRDS
# ==========================================

for bird in all_birds:

    print(
        f"\nChecking: {bird}"
    )

    taxon_id = get_taxon_id(
        bird
    )

    if not taxon_id:

        print(
            "→ NO TAXON FOUND"
        )

        continue

    found_regions = []

    # ======================================
    # CHECK EACH REGION
    # ======================================

    for region_name, region_box in REGIONS.items():

        exists = exists_in_region(

            taxon_id,
            region_box
        )

        if exists:

            found_regions.append(
                region_name
            )

    # ======================================
    # FALLBACK LOGIC
    # ======================================

    if not found_regions:

        # Himalayan fallback

        if any(

            word in bird.lower()

            for word in [

                "snow",
                "tibetan",
                "mountain",
                "alpine",
                "accentor",
                "rosefinch",
                "redstart",
                "monal",
                "tragopan",
                "snowfinch",
                "vulture",
                "griffon",
                "eagle"
            ]
        ):

            found_regions = [

                "Kashmir Valley",
                "Ladakh"
            ]

        # Plains/subtropical fallback

        elif any(

            word in bird.lower()

            for word in [

                "myna",
                "weaver",
                "bee-eater",
                "parakeet",
                "bulbul",
                "prinia",
                "jacana",
                "sunbird",
                "hornbill",
                "kingfisher",
                "munia",
                "francolin"
            ]
        ):

            found_regions = [

                "Jammu"
            ]

        # General fallback

        else:

            found_regions = [

                "Jammu",
                "Kashmir Valley"
            ]

    # ======================================
    # SAVE
    # ======================================

    if "Jammu" in found_regions:

        jammu_birds.add(
            bird
        )

    if "Kashmir Valley" in found_regions:

        kashmir_birds.add(
            bird
        )

    if "Ladakh" in found_regions:

        ladakh_birds.add(
            bird
        )

    print(
        "→ "
        + ", ".join(found_regions)
    )

    time.sleep(0.3)

# ==========================================
# SAVE FILES
# ==========================================

def save_txt(path, birds):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        for bird in sorted(
            birds
        ):

            f.write(
                bird + "\n"
            )

save_txt(
    JAMMU_FILE,
    jammu_birds
)

save_txt(
    KASHMIR_FILE,
    kashmir_birds
)

save_txt(
    LADAKH_FILE,
    ladakh_birds
)

# ==========================================
# FINAL COUNTS
# ==========================================

print("\n====================")

print(
    f"Jammu Birds: "
    f"{len(jammu_birds)}"
)

print(
    f"Kashmir Birds: "
    f"{len(kashmir_birds)}"
)

print(
    f"Ladakh Birds: "
    f"{len(ladakh_birds)}"
)

print(
    "\nALL REGION FILES CREATED SUCCESSFULLY"
)