import os
import json

DATABASE_DIR = "bird_database"

# ======================================
# WINTER MIGRATORY
# ======================================
WINTER = [
"Mallard",
"Northern Pintail",
"Northern Shoveler",
"Gadwall",
"Eurasian Wigeon",
"Common Teal",
"Garganey",
"Tufted Duck",
"Ferruginous Duck",
"Common Pochard",
"Red-crested Pochard",
"Bar-headed Goose",
"Greylag Goose",
"Ruddy Shelduck",
"Mute Swan",
"Whooper Swan",
"Common Crane",
"Demoiselle Crane",
"Bluethroat",
"Siberian Rubythroat",
"White-tailed Rubythroat",
"Redwing",
"Fieldfare",
"Black-throated Thrush",
"Dusky Thrush",
"Eurasian Curlew",
"Whimbrel",
"Black-tailed Godwit",
"Bar-tailed Godwit",
"Ruff",
"Dunlin",
"Curlew Sandpiper",
"Temminck's Stint",
"Little Stint",
"Long-toed Stint",
"Wood Sandpiper",
"Green Sandpiper",
"Marsh Sandpiper",
"Common Greenshank",
"Spotted Redshank",
"Common Redshank",
"Terek Sandpiper",
"Ruddy Turnstone",
"Sanderling",
"Jack Snipe",
"Pin-tailed Snipe",
"Common Snipe",
"Eurasian Woodcock",
"Pacific Golden Plover",
"Grey Plover",
"Kentish Plover",
"Lesser Sand Plover",
"Greater Sand Plover",
"Pied Avocet",
"Black-winged Stilt",
"Northern Lapwing",
"River Lapwing",
"Pallas's Gull",
"Brown-headed Gull",
"Black-headed Gull",
"Whiskered Tern",
"White-winged Tern",
"Black Tern",
"Caspian Tern",
"Common Tern",
"Osprey",
"Pallid Harrier",
"Montagu's Harrier",
"Hen Harrier",
"Western Marsh Harrier",
"Steppe Eagle",
"Steppe Buzzard",
"Long-legged Buzzard",
"Upland Buzzard",
"Merlin",
"Eurasian Hobby",
"White-tailed Eagle",
"Black-necked Grebe",
"Great Crested Grebe",
"Red-necked Grebe",
"Dalmatian Pelican",
"Great White Pelican",
"Rosy Starling",
"Brambling",
"Twite",
"Common Linnet",
"European Goldfinch",
"Rustic Bunting",
"Little Bunting",
"Corn Bunting",
"Water Pipit",
"Olive-backed Pipit",
"Tree Pipit",
"Richard's Pipit",
"Rosy Pipit",
"Grey-headed Wagtail",
"Citrine Wagtail",
"Yellow Wagtail",
"Forest Wagtail",
"Dusky Warbler",
"Hume's Leaf Warbler",
"Yellow-browed Warbler",
"Greenish Warbler",
"Booted Warbler",
"Sykes's Warbler",
"Blyth's Reed Warbler",
"Paddyfield Warbler",
"Indian Reed Warbler",
"Clamorous Reed Warbler",
"Taiga Flycatcher",
"Red-breasted Flycatcher",
"Verditer Flycatcher",
"Ultramarine Flycatcher",
"Asian Brown Flycatcher",
"Blue-fronted Redstart",
"Black Redstart",
"White-capped Water Redstart",
"Plumbeous Water Redstart",
"Golden Bush Robin",
"Indian Blue Robin",
"Siberian Blue Robin",
"White-tailed Robin",
"Grey Bush Robin",
"Robin Accentor",
"Brown Accentor",
"Altai Accentor",
"Alpine Accentor",
"Wallcreeper",
"White-throated Dipper",
"Brown Dipper",
"Yellow-billed Chough",
"Red-billed Chough"
]

SUMMER = [
"Asian Paradise Flycatcher",
"Pied Cuckoo",
"Common Cuckoo",
"Indian Cuckoo",
"Plaintive Cuckoo",
"Grey-bellied Cuckoo",
"Drongo Cuckoo",
"Banded Bay Cuckoo",
"Jacobin Cuckoo",
"Asian Koel",
"Eurasian Golden Oriole",
"Black-hooded Oriole",
"Maroon Oriole",
"Blue-cheeked Bee-eater",
"Chestnut-headed Bee-eater",
"Eurasian Bee-eater",
"Green Bee-eater",
"Indian Pitta",
"Blue-naped Pitta",
"Fairy Pitta",
"Hooded Pitta",
"Blue Pitta",
"Mangrove Pitta",
"Black-naped Monarch",
"White-throated Fantail",
"White-browed Fantail",
"Grey-headed Canary Flycatcher",
"Tickell's Blue Flycatcher",
"Ferruginous Flycatcher",
"Rufous-gorgeted Flycatcher",
"Kashmir Flycatcher",
"Slaty-blue Flycatcher",
"Pale-chinned Flycatcher",
"Brown-breasted Flycatcher",
"Chestnut-bellied Rock Thrush",
"Blue Rock Thrush",
"Blue-capped Rock Thrush",
"Rufous-tailed Rock Thrush",
"Orange-flanked Bush Robin",
"White-browed Bush Robin",
"Barn Swallow",
"Red-rumped Swallow",
"Wire-tailed Swallow",
"Hill Swallow",
"Asian House Martin",
"Common House Martin",
"Sand Martin",
"Pale Martin",
"White-throated Needletail",
"Fork-tailed Swift",
"Pacific Swift",
"Common Swift",
"Little Swift",
"House Swift",
"Asian Palm Swift",
"Alpine Swift",
"Himalayan Swiftlet",
"Western Crowned Warbler",
"Sulphur-bellied Warbler",
"Tickell's Leaf Warbler",
"Grey-sided Bush Warbler",
"Mountain Tailorbird",
"Plain Prinia",
"Ashy Prinia",
"Common Tailorbird",
"Zitting Cisticola",
"Common Rosefinch",
"Beautiful Rosefinch",
"Pink-browed Rosefinch",
"Dark-breasted Rosefinch",
"Red-fronted Rosefinch",
"Orange Bullfinch",
"White-winged Grosbeak",
"Black-and-yellow Grosbeak",
"Spot-winged Grosbeak",
"Collared Grosbeak"
]

RARE = [

    "Black-necked Crane",
"Relict Gull",
"Pallas's Fish Eagle",
"Grey-headed Fish Eagle",
"Amur Falcon",
"Red-necked Falcon",
"Saker Falcon",
"Eastern Imperial Eagle",
"Greater Spotted Eagle",
"Lesser Spotted Eagle",
"Bearded Vulture",
"Lammergeier",
"Cinereous Vulture",
"Himalayan Griffon",
"White-rumped Vulture",
"Red-headed Vulture",
"Long-billed Vulture",
"Western Tragopan",
"Satyr Tragopan",
"Blood Pheasant",
"Cheer Pheasant",
"Himalayan Monal",
"Tibetan Eared Pheasant",
"Snow Partridge",
"Tibetan Snowcock",
"Himalayan Snowcock",
"Tibetan Sandgrouse",
"Pallas's Sandgrouse",
"Mongolian Ground Jay",
"Ground Tit",
"Blanford's Snowfinch",
"White-rumped Snowfinch",
"Black-winged Snowfinch",
"Tibetan Snowfinch",
"Black-throated Accentor",
"Rufous-breasted Accentor",
"Güldenstädt's Redstart",
"White-winged Redstart",
"Horned Lark",
"Tibetan Lark",
"Hume's Short-toed Lark",
"Greater Short-toed Lark",
"Oriental Skylark",
"Bimaculated Lark",
"Greater Hoopoe-Lark",
"Desert Wheatear",
"Variable Wheatear",
"Mourning Wheatear",
"Pied Wheatear",
"Eastern Black-eared Wheatear",
"Isabelline Wheatear",
"Red-tailed Wheatear",
"Plain-backed Thrush",
"Siberian Thrush",
"Japanese Thrush",
"Dark-sided Thrush",
"Chestnut-headed Tesia",
"Fire-capped Tit",
"Black-lored Tit",
"White-throated Tit",
"Kashmir Nuthatch",
"Brown Creeper",
"Rusty-flanked Treecreeper",
"Bar-tailed Treecreeper",
"Pallas's Leaf Warbler",
"Trumpeter Finch",
"Brandt's Mountain Finch",
"Mongolian Finch",
"Plain Mountain Finch",
"Pine Bunting",
"Godlewski's Bunting",
"Mongolian Bunting"
]

# ======================================
# PROCESS
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

    bird_name = (

    data.get(
        "common_name",
        ""
    )

    + " "

    + folder.replace(
        "_",
        " "
    )
)

    status = "Resident"

    # ==================================
    # WINTER MIGRATORY
    # ==================================

    for item in WINTER:

        if item.lower() in bird_name.lower():

            status = (
                "Winter Migratory"
            )

    # ==================================
    # SUMMER MIGRATORY
    # ==================================

    for item in SUMMER:

        if item.lower() in bird_name.lower():

            status = (
                "Summer Migratory"
            )

    # ==================================
    # RARE VISITOR
    # ==================================

    for item in RARE:

        if item.lower() in bird_name.lower():

            status = (
                "Rare Visitor"
            )

    # ==================================
    # SAVE
    # ==================================

    data[
        "migratory_status"
    ] = status

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
        f"{bird_name}"
        f" → {status}"
    )

print(
    "\nALL STATUS UPDATED"
)