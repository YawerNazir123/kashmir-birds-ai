import os

# ==========================================
# FILE PATH
# ==========================================

FILE_PATH = "kashmir_birds_list.txt"

# ==========================================
# READ BIRDS
# ==========================================

with open(
    FILE_PATH,
    "r",
    encoding="utf-8"
) as f:

    birds = [

        line.strip()

        for line in f.readlines()

        if line.strip()
    ]

# ==========================================
# REMOVE DUPLICATES
# ==========================================

unique_birds = sorted(
    list(set(birds))
)

# ==========================================
# SAVE CLEAN FILE
# ==========================================

with open(
    FILE_PATH,
    "w",
    encoding="utf-8"
) as f:

    for bird in unique_birds:

        f.write(
            bird + "\n"
        )

# ==========================================
# RESULT
# ==========================================

print(
    f"\nDuplicates removed."
)

print(
    f"Total unique birds:"
    f" {len(unique_birds)}"
)