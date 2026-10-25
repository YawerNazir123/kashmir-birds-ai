# Label fixes — Kashmir Birds AI training list

Date: 2026-10-25. Authority: **IOC World Bird List v15.2** (master list, 11,227 species, downloaded from worldbirdnames.org).
Source list: 744 rows from `bird_database/*/info.json` in YawerNazir123/kashmir-birds-ai (`species-list.csv`).
Read-only on the GitHub repo — nothing was pushed. Outputs: `cleaned-species-list.csv` (one row per distinct scientific name kept, plus dropped/unresolved rows for the audit trail).

## Before / after

| | Count |
|---|---|
| Source rows (folders) | 744 |
| Duplicate folders merged (same taxon, two names) | 38 |
| Rows dropped (bird does not occur in J&K, or name is not a real taxon) | 13 |
| Rows unresolved (no recognised taxon — cannot be a class yet) | 2 |
| **Distinct species (classes) in the cleaned list** | **691** |
| Classes with ≥100 usable images (exact-taxon recount) | 654 |
| Classes below 100 | 37 |

The old collection claimed 701/744 at ≥100. The corrected figure is 654/691 — the difference is de-duplication (38 rows were the same bird twice), 13 drops, and exact-taxon recounts replacing inflated text-search counts (see §5).

## 1. Merges — 38 folders folded into another folder (same taxon)

Rule: the keeper is the folder whose common name is the IOC 15.2 English name. The merged folder's photos belong to the same species and must be downloaded once, under the keeper's scientific name.

- `indian_reed_warbler` “Indian Reed Warbler” → **`clamorous_reed_warbler`** “Clamorous Reed Warbler” — same taxon *Acrocephalus stentoreus* (IOC English: Clamorous Reed Warbler); “Indian Reed Warbler” is an old synonym, not an IOC name.
- `black-throated_tit` “Black-throated Tit” → **`black-throated_bushtit`** “Black-throated Bushtit” — same taxon *Aegithalos concinnus* (IOC English: Black-throated Bushtit); “Black-throated Tit” is an old synonym, not an IOC name.
- `fork-tailed_swift` “Fork-tailed Swift” → **`pacific_swift`** “Pacific Swift” — same taxon *Apus pacificus* (IOC English: Pacific Swift); “Fork-tailed Swift” is an old synonym, not an IOC name.
- `imperial_eagle` “Imperial Eagle” → **`eastern_imperial_eagle`** “Eastern Imperial Eagle” — same taxon *Aquila heliaca* (IOC English: Eastern Imperial Eagle); “Imperial Eagle” is an old synonym, not an IOC name.
- `white-tailed_rubythroat` “White-tailed Rubythroat” → **`himalayan_rubythroat`** “Himalayan Rubythroat” — same taxon *Calliope pectoralis* (IOC English: Himalayan Rubythroat); “White-tailed Rubythroat” is an old synonym, not an IOC name.
- `beautiful_rosefinch` “Beautiful Rosefinch” → **`himalayan_beautiful_rosefinch`** “Himalayan Beautiful Rosefinch” — same taxon *Carpodacus pulcherrimus* (IOC English: Himalayan Beautiful Rosefinch); “Beautiful Rosefinch” is an old synonym, not an IOC name.
- `pied_cuckoo` “Pied Cuckoo” → **`jacobin_cuckoo`** “Jacobin Cuckoo” — same taxon *Clamator jacobinus* (IOC English: Jacobin Cuckoo); “Pied Cuckoo” is an old synonym, not an IOC name.
- `oriental_magpie_robin` “Oriental Magpie Robin” → **`oriental_magpie-robin`** “Oriental Magpie-Robin” — same taxon *Copsychus saularis* (IOC English: Oriental Magpie-Robin); “Oriental Magpie Robin” is an old synonym, not an IOC name.
- `jungle_crow` “Jungle Crow” → **`large-billed_crow`** “Large-billed Crow” — same taxon *Corvus macrorhynchos* (IOC English: Large-billed Crow); “Jungle Crow” is an old synonym, not an IOC name.
- `kestrel` “Kestrel” → **`common_kestrel`** “Common Kestrel” — same taxon *Falco tinnunculus* (IOC English: Common Kestrel); “Kestrel” is an old synonym, not an IOC name.
- `pied_wagtail` “Pied Wagtail” → **`white_wagtail`** “White Wagtail” — same taxon *Motacilla alba* (IOC English: White Wagtail); “Pied Wagtail” is an old synonym, not an IOC name.
- `white-tailed_blue_robin` “White-tailed Blue Robin” → **`white-tailed_robin`** “White-tailed Robin” — same taxon *Myiomela leucura* (IOC English: White-tailed Robin); “White-tailed Blue Robin” is an old synonym, not an IOC name.
- `brown_hawk_owl` “Brown Hawk Owl” → **`brown_boobook`** “Brown Boobook” — same taxon *Ninox scutulata* (IOC English: Brown Boobook); “Brown Hawk Owl” is an old synonym, not an IOC name.
- `mountain_hawk_eagle` “Mountain Hawk Eagle” → **`mountain_hawk-eagle`** “Mountain Hawk-Eagle” — same taxon *Nisaetus nipalensis* (IOC English: Mountain Hawk-Eagle); “Mountain Hawk Eagle” is an old synonym, not an IOC name.
- `tree_sparrow` “Tree Sparrow” → **`eurasian_tree_sparrow`** “Eurasian Tree Sparrow” — same taxon *Passer montanus* (IOC English: Eurasian Tree Sparrow); “Tree Sparrow” is an old synonym, not an IOC name.
- `white-winged_redstart` “White-winged Redstart” → **`güldenstädt's_redstart`** “Güldenstädt's Redstart” — same taxon *Phoenicurus erythrogastrus* (IOC English: Güldenstädt's Redstart); “White-winged Redstart” is an old synonym, not an IOC name.
- `plumbeous_redstart` “Plumbeous Redstart” → **`plumbeous_water_redstart`** “Plumbeous Water Redstart” — same taxon *Phoenicurus fuliginosus* (IOC English: Plumbeous Water Redstart); “Plumbeous Redstart” is an old synonym, not an IOC name.
- `white-capped_water_redstart` “White-capped Water Redstart” → **`white-capped_redstart`** “White-capped Redstart” — same taxon *Phoenicurus leucocephalus* (IOC English: White-capped Redstart); “White-capped Water Redstart” is an old synonym, not an IOC name.
- `hume's_warbler` “Hume's Warbler” → **`hume's_leaf_warbler`** “Hume's Leaf Warbler” — same taxon *Phylloscopus humei* (IOC English: Hume's Leaf Warbler); “Hume's Warbler” is an old synonym, not an IOC name.
- `white-cheeked_bulbul` “White-cheeked Bulbul” → **`himalayan_bulbul`** “Himalayan Bulbul” — same taxon *Pycnonotus leucogenys* (IOC English: Himalayan Bulbul); “White-cheeked Bulbul” is an old synonym, not an IOC name.
- `fire-fronted_serin` “Fire-fronted Serin” → **`red-fronted_serin`** “Red-fronted Serin” — same taxon *Serinus pusillus* (IOC English: Red-fronted Serin); “Fire-fronted Serin” is an old synonym, not an IOC name.
- `grey-headed_thrush` “Grey-headed Thrush” → **`chestnut_thrush`** “Chestnut Thrush” — same taxon *Turdus rubrocanus* (IOC English: Chestnut Thrush); “Grey-headed Thrush” is an old synonym, not an IOC name.
- `indian_pygmy_woodpecker` “Indian Pygmy Woodpecker” → **`brown-capped_pygmy_woodpecker`** “Brown-capped Pygmy Woodpecker” — same taxon *Yungipicus nanus* (IOC English: Brown-capped Pygmy Woodpecker); “Indian Pygmy Woodpecker” is an old synonym, not an IOC name.
- `bearded_vulture` “Bearded Vulture” (CSV sci: Gypaetinae) → **`lammergeier`** — CSV sci 'Gypaetinae' is a subfamily, not a species. The Bearded Vulture is Gypaetus barbatus, which already exists as lammergeier ('Lammergeier' is the old name for the Bearded Vulture; both folders claim the same bird). Merge into lammergeier.
- `black-eared_kite` “Black-eared Kite” (CSV sci: Milvus migrans lineatus) → **`black_kite`** — Milvus migrans lineatus (Black-eared Kite) is a subspecies of Black Kite; IOC 15.2 does not split it. black_kite row (Milvus migrans) already exists in species-list.csv.
- `black-shouldered_kite` “Black-shouldered Kite” (CSV sci: Elanus) → **`black-winged_kite`** — IOC 'Black-shouldered Kite' is Elanus axillaris, an Australian-only species (range AU) that does not occur in Asia. The Asian bird formerly called Black-shouldered Kite is Black-winged Kite Elanus caeruleus, which already exists as black-winged_kite row (Elanus caeruleus) in species-list.csv.
- `black-throated_weaver` “Black-throated Weaver” (CSV sci: Ploceus ocularis ocularis) → **`black-breasted_weaver`** — CSV sci Ploceus ocularis ocularis is the African Spectacled Weaver. 'Black-throated Weaver' is the former name of the Black-breasted Weaver Ploceus benghalensis, which already exists as black-breasted_weaver, so this row merges into it.
- `buff-bellied_pipit` “Buff-bellied Pipit” (CSV sci: Anthus rubescens) → **`water_pipit`** — CSV sci Anthus rubescens is the American Pipit (IOC range NA). The Kashmir bird behind this folder is the Water Pipit Anthus spinoletta - the Old World counterpart, a winter visitor to J&K - which already exists as water_pipit. Merge into water_pipit.
- `chestnut-headed_laughingthrush` “Chestnut-headed Laughingthrush” (CSV sci: blank) → **`chestnut-crowned_laughingthrush`** — 'Chestnut-headed Laughingthrush' is not an IOC/iNaturalist taxon; the folder's own info.json Wikipedia URL points to 'Chestnut-crowned_laughingthrush', i.e. the Chestnut-crowned Laughingthrush Trochalopteron erythrocephalum. That species already exists as chestnut-crowned_laughingthrush, so this row merges into it.
- `grey-headed_bushchat` “Grey-headed Bushchat” (CSV sci: blank) → **`grey_bushchat`** — 'Grey-headed Bushchat' is not a recognised taxon in IOC 15.2, iNaturalist or GBIF (all return no match); a web search for the exact name returns only the Grey Bushchat Saxicola ferreus, whose male is grey-headed (grey crown to rump). The folder has no images and no usable info.json clues (boilerplate description, junk Wikipedia URL). Saxicola ferreus already exists as grey_bushchat, so this row merges into it.
- `grey-headed_wagtail` “Grey-headed Wagtail” (CSV sci: Motacilla flava thunbergi) → **`yellow_wagtail`** — Motacilla flava thunbergi (Grey-headed Wagtail) is a subspecies of Western Yellow Wagtail; IOC 15.2 does not split it. yellow_wagtail row (Motacilla flava) already exists in species-list.csv.
- `heuglin's_gull` “Heuglin's Gull” (CSV sci: Larus heuglini) → **`lesser_black-backed_gull`** — IOC 15.2 does not recognise Larus heuglini as a species; Heuglin's Gull is the subspecies Larus fuscus heuglini of Lesser Black-backed Gull Larus fuscus. lesser_black-backed_gull row (Larus fuscus) already exists in species-list.csv.
- `hoopoe` “Hoopoe” (CSV sci: Bucerotiformes) → **`eurasian_hoopoe`** — CSV sci 'Bucerotiformes' is an order, not a species. The Hoopoe is Upupa epops (IOC 'Common Hoopoe'), which already exists as eurasian_hoopoe. Merge into eurasian_hoopoe.
- `hume's_whitethroat` “Hume's Whitethroat” (CSV sci: Curruca curruca althaea) → **`lesser_whitethroat`** — Curruca curruca althaea (Hume's Whitethroat) is a subspecies of Lesser Whitethroat; IOC 15.2 does not recognise Curruca althaea as a species. lesser_whitethroat row (Curruca curruca) already exists in species-list.csv.
- `lesser_goldenback` “Lesser Goldenback” (CSV sci: Dinopium benghalense tehminae) → **`black-rumped_flameback`** — 'Lesser Goldenback' is the old name for Black-rumped Flameback Dinopium benghalense; the CSV trinomial is a subspecies of it. black-rumped_flameback row (Dinopium benghalense) already exists in species-list.csv.
- `pied_stonechat` “Pied Stonechat” (CSV sci: blank) → **`pied_bushchat`** — 'Pied Stonechat' is not an IOC/iNaturalist taxon; it is the Pied Bushchat Saxicola caprata under its old 'stonechat' styling (the genus Saxicola was formerly placed with the stonechats). The folder's own info.json Wikipedia URL points to 'Pied_bush_chat' and its genus field is Saxicola. Saxicola caprata already exists as pied_bushchat, so this row merges into it.
- `steppe_buzzard` “Steppe Buzzard” (CSV sci: Buteo buteo vulpinus) → **`common_buzzard`** — Buteo buteo vulpinus (Steppe Buzzard) is a subspecies of Common Buzzard; IOC 15.2 does not split it. common_buzzard row (Buteo buteo) already exists in species-list.csv.
- `white-eye` “White-eye” (CSV sci: Zosteropidae) → **`oriental_white-eye`** — CSV value is a family name, not a species. The Kashmir white-eye is Indian White-eye Zosterops palpebrosus (IOC English Indian White-eye; formerly Oriental White-eye), and species-list.csv already has oriental_white-eye (blank sci, section C) for the same bird. Merge into that folder, which resolves to Zosterops palpebrosus.

Note on merge chains: `white-eye` → `oriental_white-eye` → *Zosterops palpebrosus* (Indian White-eye); the chain resolves to one class.

## 2. Names resolved — scientific name corrected, class kept

These rows stay as classes, but with a corrected binomial and/or the IOC English name. (Rows whose CSV name was already the IOC binomial and English name are not listed — they needed no fix.)

- `asian_pied_starling` “Asian Pied Starling” (CSV sci: Gracupica) → **Indian Pied Myna**, *Gracupica contra* (Sturnidae). Genus-only CSV value; 'Asian Pied Starling' is the familiar name for Gracupica contra (IOC English Indian Pied Myna). No duplicate row in species-list.csv.
- `bay_woodpecker` “Bay Woodpecker” (CSV sci: Blythipicus) → **Bay Woodpecker**, *Blythipicus pyrrhotis* (Picidae). Genus-only CSV value; IOC English name matches exactly. No duplicate row in species-list.csv.
- `black-and-yellow_grosbeak` “Black-and-yellow Grosbeak” (CSV sci: Caryothraustes) → **Black-and-yellow Grosbeak**, *Mycerobas icterioides* (Fringillidae). Genus-only CSV value is wrong genus (Caryothraustes is Neotropical). IOC English name matches exactly: Mycerobas icterioides. Note CSV family Cardinalidae is wrong; IOC family is Fringillidae. No duplicate row.
- `black-headed_munia` “Black-headed Munia” (CSV sci: blank) → **Tricolored Munia**, *Lonchura malacca* (Estrildidae). 'Black-headed Munia' is the old name for the Tricolored Munia / Chestnut Munia pair (formerly conspecific); for a Kashmir list it is Lonchura malacca. iNaturalist maps the name to L. malacca, and the 2024 J&K checklist lists Tricoloured Munia L. malacca (#528) while Chestnut Munia L. atricapilla is absent from it (GBIF occurrences in the J&K+Ladakh box: malacca 24, atricapilla 0). No CSV row has this binomial.
- `black_eagle` “Black Eagle” (CSV sci: Geranoaetus melanoleucus) → **Black Eagle**, *Ictinaetus malaiensis* (Accipitridae). CSV sci Geranoaetus melanoleucus is the South American Black-chested Buzzard-Eagle. The Black Eagle is Ictinaetus malaiensis, which occurs in J&K. No CSV row has Ictinaetus malaiensis.
- `black_ibis` “Black Ibis” (CSV sci: Threskiornis) → **Red-naped Ibis**, *Pseudibis papillosa* (Threskiornithidae). 'Black Ibis' (Indian Black Ibis) is the old name for Red-naped Ibis Pseudibis papillosa; the CSV genus Threskiornis is wrong (that genus is the Black-headed Ibis, already listed as oriental_white_ibis). No red-naped_ibis row exists in species-list.csv, so keep under the IOC name. Caveat: a N Indian plains species, at the edge of its range in J&K (Jammu lowlands).
- `brambling` “Brambling” (CSV sci: Fringilla) → **Brambling**, *Fringilla montifringilla* (Fringillidae). Genus-only CSV value; IOC English name matches exactly. No duplicate row in species-list.csv.
- `crested_kingfisher` “Crested Kingfisher” (CSV sci: Megaceryle) → **Crested Kingfisher**, *Megaceryle lugubris* (Alcedinidae). Genus-only CSV value; IOC English name matches exactly, single species in genus for this name. No duplicate row in species-list.csv.
- `demoiselle_crane` “Demoiselle Crane” (CSV sci: Anthropoides virgo) → **Demoiselle Crane**, *Grus virgo* (Gruidae). CSV binomial Anthropoides virgo is a superseded combination; IOC 15.2 places Demoiselle Crane in Grus. No duplicate row in species-list.csv.
- `eurasian_bee-eater` “Eurasian Bee-eater” (CSV sci: blank) → **European Bee-eater**, *Merops apiaster* (Meropidae). 'Eurasian Bee-eater' is the older/alternative name for the European Bee-eater Merops apiaster; it is the only Kashmir bee-eater missing from the CSV (Blue-cheeked, Blue-tailed, Chestnut-headed, Green and Blue-bearded Bee-eaters are all present). The CSV family/genus fields (Passeridae/Passer) are junk copied from a wrong source. No CSV row has Merops apiaster.
- `eurasian_bittern` “Eurasian Bittern” (CSV sci: Botaurus minutus) → **Eurasian Bittern**, *Botaurus stellaris* (Ardeidae). CSV sci Botaurus minutus is the Little Bittern (IOC: Little Bittern), the wrong taxon for the name. The Eurasian Bittern is Botaurus stellaris, which occurs in J&K. No CSV row has Botaurus stellaris (the site's little_bittern row does not exist; the checklist lists Little Bittern as Ixobrychus minutus).
- `great_barbet` “Great Barbet” (CSV sci: Capito) → **Great Barbet**, *Psilopogon virens* (Megalaimidae). Genus-only CSV value is wrong genus (Capito is a Neotropical barbet genus). IOC English name matches exactly: Psilopogon virens. Note CSV family Capitonidae is also wrong; IOC family is Megalaimidae (Asian Barbets). No duplicate row.
- `greater_short-toed_lark` “Greater Short-toed Lark” (CSV sci: Calandrella) → **Greater Short-toed Lark**, *Calandrella brachydactyla* (Alaudidae). Genus-only CSV value; IOC English name matches exactly. No duplicate row in species-list.csv.
- `herring_gull` “Herring Gull” (CSV sci: Larus smithsonianus) → **Caspian Gull**, *Larus cachinnans* (Laridae). CSV sci Larus smithsonianus is the American Herring Gull. The large white-headed 'Herring Gull' of Kashmir is the Caspian Gull Larus cachinnans (formerly lumped in the Herring Gull complex); the European Herring Gull Larus argentatus is not in the J&K checklist either. No CSV row has Larus cachinnans.
- `hill_partridge` “Hill Partridge” (CSV sci: Arborophila) → **Hill Partridge**, *Arborophila torqueola* (Phasianidae). Genus-only CSV value; IOC English name matches exactly. No duplicate row in species-list.csv.
- `horned_lark` “Horned Lark” (CSV sci: Eremophila) → **Horned Lark**, *Eremophila alpestris* (Alaudidae). Genus-only CSV value; IOC English name matches exactly. Occurs in Ladakh/high Himalaya. No duplicate row in species-list.csv.
- `little_ringed_plover` “Little Ringed Plover” (CSV sci: Charadrius dubius) → **Little Ringed Plover**, *Thinornis dubius* (Charadriidae). CSV binomial Charadrius dubius is a superseded combination; IOC 15.2 places Little Ringed Plover in Thinornis. No duplicate row in species-list.csv.
- `mongolian_finch` “Mongolian Finch” (CSV sci: Bucanetes) → **Mongolian Finch**, *Bucanetes mongolicus* (Fringillidae). Genus-only CSV value shared with trumpeter_finch, but IOC English name matches exactly and it is a distinct species from Trumpeter Finch Bucanetes githagineus. No duplicate row.
- `oriental_white-eye` “Oriental White-eye” (CSV sci: blank) → **Indian White-eye**, *Zosterops palpebrosus* (Zosteropidae). 'Oriental White-eye' is the former IOC name of the Indian White-eye Zosterops palpebrosus (renamed in IOC). No CSV row has this binomial. The separate 'white-eye' folder is a family-level row (sci Zosteropidae), not a Zosterops palpebrosus row, so this is not a merge.
- `pale_martin` “Pale Martin” (CSV sci: Apus pallidus) → **Pale Martin**, *Riparia diluta* (Hirundinidae). CSV sci Apus pallidus is the Pallid Swift. The Pale Martin is Riparia diluta - IOC's English name for it is literally 'Pale Martin', so only the scientific name was wrong. It occurs in J&K. No CSV row has Riparia diluta.
- `plain-backed_thrush` “Plain-backed Thrush” (CSV sci: Zoothera mollissima) → **Alpine Thrush**, *Zoothera mollissima* (Turdidae). The CSV scientific name is correct for the pre-split taxon: 'Plain-backed Thrush' was the old name for the Zoothera mollissima complex, and IOC 15.2 now calls Z. mollissima the Alpine Thrush - the Himalayan form, which is the one in Kashmir (the split-off Himalayan Thrush Z. salimalii is a central/east Himalayan bird). Keep with the IOC name Alpine Thrush; no separate alpine_thrush row exists.
- `sand_martin` “Sand Martin” (CSV sci: Riparia) → **Sand Martin**, *Riparia riparia* (Hirundinidae). Genus-only CSV value; IOC English name matches exactly. No duplicate row in species-list.csv.
- `scaly-bellied_wren-babbler` “Scaly-bellied Wren-Babbler” (CSV sci: blank) → **Scaly-breasted Cupwing**, *Pnoepyga albiventer* (Pnoepygidae). 'Scaly-bellied Wren-Babbler' is a variant spelling of 'Scaly-breasted Wren-Babbler', the former name of the Scaly-breasted Cupwing Pnoepyga albiventer (the variant is used in field literature, e.g. a BirdQuest Nepal trip report); IOC's current name is Scaly-breasted Cupwing. No CSV row has this binomial. It does occur in J&K.
- `trumpeter_finch` “Trumpeter Finch” (CSV sci: Bucanetes) → **Trumpeter Finch**, *Bucanetes githagineus* (Fringillidae). Genus-only CSV value shared with mongolian_finch, but IOC English name matches exactly and it is a distinct species from Mongolian Finch Bucanetes mongolicus. No duplicate row.
- `twite` “Twite” (CSV sci: Linaria) → **Twite**, *Linaria flavirostris* (Fringillidae). Genus-only CSV value; IOC English name matches exactly. Note CSV family Plantaginaceae is a plant family and wrong; IOC family is Fringillidae. No duplicate row.
- `white-gorgeted_flycatcher` “White-gorgeted Flycatcher” (CSV sci: Anthipes) → **White-gorgeted Flycatcher**, *Anthipes monileger* (Muscicapidae). Genus-only CSV value; IOC English name matches exactly. No duplicate row in species-list.csv.
- `yellow-eyed_babbler` “Yellow-eyed Babbler” (CSV sci: Chrysomma) → **Yellow-eyed Babbler**, *Chrysomma sinense* (Paradoxornithidae). Genus-only CSV value; IOC English name matches exactly. No duplicate row in species-list.csv.

Also, for every kept class the chosen common name in `cleaned-species-list.csv` is the IOC 15.2 English name, even where the CSV used a different (older or regional) name for the same taxon — e.g. Common Teal → Eurasian Teal (*Anas crecca*), Cattle Egret → Eastern Cattle Egret (*Ardea coromanda*), Eurasian Cuckoo → Common Cuckoo (*Cuculus canorus*), Rock Pigeon → Rock Dove (*Columba livia*), Jungle Crow → Large-billed Crow (*Corvus macrorhynchos*). The CSV name is kept in the `csv_common_names` column. This is a naming standardisation, not a taxon change.

## 3. Dropped — 13 rows (do not train on these)

- `brown_hornbill` “Brown Hornbill” — 'Brown Hornbill' is the alternative name of Austen's Brown Hornbill Anorrhinus austeni (Tickell's Brown Hornbill A. tickelli is confined to S Myanmar/W Thailand). Austen's occurs only in NE India (Arunachal/Assam/Manipur/Nagaland/Mizoram) east to S China and mainland SE Asia; it does not occur in J&K. The info.json claim of Kashmir Valley residence is templated boilerplate, not evidence.
  Evidence: IOC 15.2: Anorrhinus austeni = Austen's Brown Hornbill, range OR; Anorrhinus tickelli = Tickell's Brown Hornbill, range OR. BirdForum/Bubo Birding: Austen's distribution 'from northeast India east to southern China, Burma, northern and central Thailand, Laos...' and 'distributed across many of the North-eastern states... Namdapha, Arunachal Pradesh'. No J&K occurrence.
- `redwing` “Redwing” — CSV sci Agelaius phoeniceus is the American Red-winged Blackbird. The real Redwing is Turdus iliacus, but it does not occur in Kashmir: its winter range runs only east to northern Iran, it is absent from the 2024 J&K checklist, and GBIF has 0 occurrences in the J&K+Ladakh box. The folder's claim of 'frequently observed' in Kashmir is boilerplate, not evidence. Drop.
  Evidence: IOC 15.2: Turdus iliacus = Redwing, Turdidae, range PAL; BirdForum Opus: winters 'east to northern Iran'; J&K checklist: no Turdus iliacus; GBIF occurrences in J&K+Ladakh box = 0.
- `white-eared_sibia` “White-eared Sibia” — The CSV scientific name is correct for the name - but the White-eared Sibia Heterophasia auricularis is endemic to Taiwan and does not occur in Kashmir (the J&K checklist lists only Rufous Sibia in this genus; GBIF has 0 occurrences in the J&K+Ladakh box). The folder's info.json is boilerplate with stats copied from the Taiwan species. Drop; no Kashmir sibia matches 'white-eared'.
  Evidence: IOC 15.2: Heterophasia auricularis = White-eared Sibia, Leiothrichidae, range OR (Taiwan endemic); J&K checklist #426 only 'Rufous Sibia Heterophasia capistrata'; GBIF occurrences in J&K+Ladakh box = 0.
- `mountain_quail` “Mountain Quail” — IOC Mountain Quail Oreortyx pictus is a New World quail of western North America (family Odontophoridae). It does not occur in India or Kashmir at all; there is no Kashmir equivalent called Mountain Quail. The info.json claim of Kashmir Valley residence is templated boilerplate, not evidence.
  Evidence: IOC 15.2: Oreortyx pictus = Mountain Quail, Odontophoridae (New World Quail), range NA, MA only. No J&K/India occurrence.
- `monal_partridge` “Monal Partridge” — Genus-only name covering two IOC species, Chestnut-throated Monal-Partridge Tetraophasis obscurus and Buff-throated Monal-Partridge Tetraophasis szechenyii, so it cannot be resolved to a single species; and both are endemic to the high mountains of western/central China and do not occur in India/J&K. The info.json claim of Ladakh occurrence is templated boilerplate, not evidence.
  Evidence: IOC 15.2: Tetraophasis obscurus = Chestnut-throated Monal-Partridge, range PAL; Tetraophasis szechenyii = Buff-throated Monal-Partridge, range PAL. Wikipedia: Buff-throated Monal-Partridge 'is endemic to western China' (SE Tibet, S Qinghai, W Sichuan, NW Yunnan); Chestnut-throated 'occurs only in mountainous areas of western and central China, particularly Gansu, Qinghai and Sichuan'.
- `snowcock` “Snowcock” — Generic genus-only name; cannot be resolved to a single species. The two Kashmir snowcocks are already listed as separate rows: Himalayan Snowcock Tetraogallus himalayensis (himalayan_snowcock) and Tibetan Snowcock Tetraogallus tibetanus (tibetan_snowcock). The generic folder duplicates both.
  Evidence: IOC 15.2: Tetraogallus himalayensis = Himalayan Snowcock; Tetraogallus tibetanus = Tibetan Snowcock; Tetraogallus caspius = Caspian Snowcock (W Asia, not J&K). Both Kashmir species already present in species-list.csv. info.json is templated boilerplate.
- `golden-fronted_woodpecker` “Golden-fronted Woodpecker” — The CSV scientific name is actually correct for the name - but the bird is a New World species (Texas, Mexico, Central America; IOC range NA, MA). No woodpecker called Golden-fronted occurs in Asia, and Melanerpes is absent from the 2024 J&K checklist. The folder's info.json is boilerplate with stats copied from the American species. Drop; there is no Kashmir bird this row could be re-pointed to.
  Evidence: IOC 15.2: Melanerpes aurifrons = Golden-fronted Woodpecker, Picidae, range NA, MA; J&K checklist: no Melanerpes; info.json wikipedia_url = Golden-fronted_woodpecker (the American species).
- `slaty-breasted_rail` “Slaty-breasted Rail” — CSV sci Aramides saracura is the South American Slaty-breasted Wood Rail. The real Slaty-breasted Rail is Lewinia striata (confirmed by IOC and iNaturalist), but it has no accepted J&K record: it is absent from the comprehensive 2024 J&K checklist (592 species), and the only GBIF occurrence in the J&K+Ladakh box is one undated museum specimen labelled 'NW Himalayas' at 35.85N 75.01E, outside the J&K UT. Drop on current evidence; revisit only if a documented J&K record appears.
  Evidence: IOC 15.2: Lewinia striata = Slaty-breasted Rail, Rallidae, range OR, AU; iNaturalist autocomplete 'Slaty-breasted Rail' -> Lewinia striata; J&K checklist: no Lewinia; GBIF: 1 occurrence in box, ROM preserved specimen, locality 'NW Himalayas', no date.
- `scops_owl` “Scops Owl” — Generic genus-only name; cannot be resolved to a single species. Four scops owls are already listed as separate rows: Indian Scops Owl Otus bakkamoena (indian_scops_owl), Oriental Scops Owl Otus sunia (oriental_scops_owl), Collared Scops Owl Otus lettia (collared_scops_owl) and Mountain Scops Owl Otus spilocephalus (mountain_scops_owl). The generic folder duplicates all four.
  Evidence: IOC 15.2: Otus bakkamoena = Indian Scops Owl; Otus sunia = Oriental Scops Owl; Otus lettia = Collared Scops Owl; Otus spilocephalus = Mountain Scops Owl. All four already present in species-list.csv. info.json is templated boilerplate.
- `mongolian_bunting` “Mongolian Bunting” — 'Mongolian Bunting' is not an IOC species: it is the informal name for the Mongolian subspecies Emberiza pallasi lydiae of Pallas's Reed Bunting, described in birding literature as a 'should-be-split race of Pallas's Bunting' / 'the lydiae form ... which may get split as Mongolian Bunting'. The species Emberiza pallasi does not occur in J&K or Ladakh: absent from the 2024 J&K checklist and 0 GBIF occurrences in the J&K+Ladakh box, so the row is dropped rather than kept as a species.
  Evidence: IOC 15.2: Emberiza pallasi = Pallas's Reed Bunting, Emberizidae, range PAL; iNaturalist autocomplete 'Mongolian Bunting' = no results; GBIF species match = NONE; J&K checklist: no Emberiza pallasi; GBIF occurrences in J&K+Ladakh box = 0.
- `white-cheeked_starling` “White-cheeked Starling” — IOC name and binomial are valid, but the species is East Asian and does not occur in India/J&K: it breeds in SE Siberia, Mongolia, N China, Korea and Japan, winters in S China/Taiwan, and is recorded as a vagrant only in Burma, Thailand and the Philippines. The info.json claim of Kashmir Valley residence is templated boilerplate, not evidence.
  Evidence: IOC 15.2: Spodiopsar cineraceus = White-cheeked Starling, Sturnidae, range PAL, nonbreeding 'se China'. BirdForum: 'Breeds in southeast Siberia, Mongolia, northern China, Korea, southern Sakhalin and Japan... Recorded as vagrant in Burma, Thailand and the Philippines.' No India record.
- `coral-billed_scimitar_babbler` “Coral-billed Scimitar Babbler” — The CSV scientific name is the correct pre-split taxon: 'Coral-billed Scimitar Babbler' was split, and the Himalayan form is now the Black-crowned Scimitar Babbler Pomatorhinus ferruginosus. But its range runs only from eastern Nepal eastwards, it is absent from the 2024 J&K checklist (whose only Pomatorhinus is the White-browed Scimitar-Babbler), and GBIF has 0 occurrences in the J&K+Ladakh box. It does not occur in Kashmir. Drop.
  Evidence: IOC 15.2: Pomatorhinus ferruginosus = Black-crowned Scimitar Babbler, Timaliidae, range OR; BirdForum Opus: 'Himalayas (eastern Nepal to eastern Assam)'; J&K checklist #419 only 'White-browed Scimitar-Babbler Pomatorhinus schisticeps'; GBIF occurrences in box = 0.
- `pale_thrush` “Pale Thrush” — CSV sci Turdus leucomelas is the South American Pale-breasted Thrush. The real Pale Thrush is Turdus pallidus, an East Asian species, but it does not occur in India at all: BirdLife's country list for it has no India entry, it is absent from the 2024 J&K checklist, and GBIF has 0 occurrences in the J&K+Ladakh box. Drop.
  Evidence: IOC 15.2: Turdus pallidus = Pale Thrush, Turdidae, range PAL; iNaturalist autocomplete 'Pale Thrush' -> Turdus pallidus; BirdLife DataZone country distribution for Turdus pallidus lists China, Japan, Koreas, Russia, Taiwan, Philippines, Hong Kong - no India; J&K checklist: no Turdus pallidus; GBIF occurrences in box = 0.

Closest calls (revisit if new evidence appears): Slaty-breasted Rail (one undated museum specimen labelled “NW Himalayas”, outside the J&K UT — no accepted J&K record); Mongolian Bunting (the taxon is Pallas's Reed Bunting *Emberiza pallasi*, subspecies *lydiae* is informally called “Mongolian Bunting” and may one day be split — if it is split and recorded in J&K, reinstate it); Coral-billed Scimitar Babbler (range runs from E Nepal eastward).

## 4. Unresolved — 2 rows (cannot be classes until resolved)

- `lesser_sand_plover` “Lesser Sand Plover” — IOC 15.2 has no 'Lesser Sand Plover': it was split in 2023 into Tibetan Sand Plover Anarhynchus atrifrons (breeds Pamir/Tian Shan/Tibetan Plateau/Himalayas; winters Indian subcontinent) and Siberian Sand Plover Anarhynchus mongolus (E Asia; winters to Australia). Both could occur in Kashmir and the folder name alone cannot assign the photos to one; do not guess. Needs photo-level identification before a new folder (tibetan_sand_plover or siberian_sand_plover) is created.
  Evidence: IOC 15.2: Anarhynchus atrifrons = Tibetan Sand Plover, range PAL, nonbreeding 'Indian subcontinent...'; Anarhynchus mongolus = Siberian Sand Plover, range PAL, nonbreeding 'coastal Taiwan and Vietnam to Australia...'. Wikipedia: IOU accepted the split in 2023. info.json is templated boilerplate.
- `grey_bush_robin` “Grey Bush Robin” — No recognised taxon called 'Grey Bush Robin' exists: not in IOC 15.2, iNaturalist taxon autocomplete returns 0 results, GBIF species match = NONE, and a web search finds no such bird. The bush-robin genus Tarsiger has only six species (White-browed, Rufous-breasted, Collared, Red-flanked Bluetail, Himalayan Bluetail, Golden), none of which is called Grey Bush Robin, and the folder's info.json is boilerplate with no images and no Wikipedia URL, so there is no evidence to pick one. Cannot guess which bush robin was meant.
  Evidence: IOC 15.2: no 'Grey Bush Robin'; iNaturalist /taxa/autocomplete?q='Grey Bush Robin' total_results 0; GBIF species match matchType NONE; info.json has no wikipedia_url and images [].
- **Lesser Sand Plover** — IOC 15.2 split it (2023) into Tibetan Sand Plover *Anarhynchus atrifrons* (breeds Pamir/Tian Shan/Tibetan Plateau/Himalayas; winters Indian subcontinent) and Siberian Sand Plover *A. mongolus* (E Asia). The folder name alone cannot assign the photos to one of them; needs photo-level identification before a `tibetan_sand_plover` or `siberian_sand_plover` class is created.
- **Grey Bush Robin** — no such taxon in IOC 15.2, iNaturalist (0 results), GBIF (no match) or web search. The bush-robin genus *Tarsiger* has only six species, none matching. The folder has no images and no Wikipedia URL, so there is nothing to identify it from. Needs the user (or a Kashmir field reference) to say what bird this folder was meant to be.

## 5. Counts re-checked by exact taxon ID

Method (script: `work/recount.py`): for each kept class, resolve the exact taxon with iNaturalist `/v1/taxa` (exact name match, rank species; one miss — Eurasian Eagle-Owl *Bubo bubo* — was resolved via `/v1/taxa/autocomplete`, taxon_id 20059) and GBIF `/v1/species/match` (exact/fuzzy species match). Then count iNaturalist CC-licensed photo observations (`taxon_id`, `photos=true`, `photo_license=cc-by,cc-by-nc,cc-by-sa,cc0`) and GBIF still-image occurrences (`taxonKey`, `mediaType=StillImage`). **Usable images = the larger of the two counts; best source = whichever is larger.** All 691 kept classes were re-checked this way (653 in the first pass, 45 resolved/duplicate-keeper classes in a second pass, 4 corrected-name classes re-run with their corrected binomials). No text-search counts remain in the cleaned list.

What the recount changed vs the old text-search counts:
- Eurasian Eagle-Owl: old text search ~370,000 (genus match) → **11,048** (GBIF exact taxon; iNaturalist CC photo observations 4,820).
- Black Francolin: old 24,529 → **808** (GBIF) / 462 (iNaturalist).
- Western Tragopan: iNaturalist CC photo observations only **3**; GBIF still-image occurrences **66** — usable count is 66 (GBIF), but see the caveat below.
- Finn's Weaver: 35 → **35** (unchanged); Fire-capped Tit: 79 → **69**; Snow Partridge: 92 → **90**; Swamp Francolin: 87 → **87**; Tibetan Eared Pheasant: 36 → **36**; Long-billed Bush Warbler: 5 → **12**; White-throated Bushtit: 9 → **18**; Brooks's Leaf Warbler: 31 (Wikimedia) → **13** by taxon ID (see Commons top-up note).
- Kashmir Flycatcher: old 55 (iNaturalist) → **≥100** via GBIF exact taxon (it left the problem list).

Caveats on the corrected counts:
- **iNaturalist counts are observations with photos, not photos** — one observation can hold several photos, so they are a conservative lower bound on downloadable images. GBIF counts are occurrences with a still image; they largely overlap iNaturalist and include other datasets.
- **GBIF counts are an upper bound, not a licence-checked count.** Licences vary per record and some records are museum specimens (e.g. Himalayan Quail's 7 are specimen photos only — the species is presumed extinct and has no live-bird photos). Per-image licence and specimen filtering must happen at download time.
- **GBIF's backbone taxonomy differs from IOC for some genera**, so GBIF keys could not be resolved for: bitterns (*Botaurus* → *Ixobrychus* in GBIF), *Accipiter*/*Tachyspiza* hawks (Besra, Shikra, Crested Goshawk, Northern Goshawk), Little Ringed Plover (*Thinornis dubius*), and Grey-capped Greenfinch (no match). iNaturalist counts exist for all of these, so their usable counts are unaffected.
- **Wikimedia Commons was not part of the taxon-ID recount** (no taxon IDs there). For the low species, Commons category file counts were checked separately as a top-up: White-cheeked Nuthatch 63 files, White-tailed Stonechat 58, Nilgiri Pipit 48, Rock Bush Quail 37, Brooks's Leaf Warbler 31, Long-billed Bush Warbler 28, Kashmir Nuthatch 28, Snow Partridge 27, Upland Pipit 28, Orange Bullfinch 22. These are file counts (may include maps/illustrations and duplicates of iNaturalist photos) — use them as a top-up at download time, not as additional verified counts. Brooks's Leaf Warbler's downloadable pool is roughly 13 (taxon-ID) + up to 31 (Commons).
- **No species was left without a count**: every kept class has an iNaturalist and/or GBIF exact-taxon count. One iNaturalist lookup needed the autocomplete endpoint (Eurasian Eagle-Owl); no species required a text-search fallback.

## 6. Corrected problem list — classes below 100 usable images (37)

| Usable | Species (IOC English) | Scientific name | Best source |
|---|---|---|---|
| 35 | Black-and-yellow Grosbeak | *Mycerobas icterioides* | GBIF |
| 85 | Black-tailed Crake | *Zapornia bicolor* | GBIF |
| 51 | Blanford's Snowfinch | *Pyrgilauda blanfordi* | GBIF |
| 67 | Blue-naped Pitta | *Hydrornis nipalensis* | GBIF |
| 13 | Brooks's Leaf Warbler | *Phylloscopus subviridis* | GBIF |
| 87 | Collared Grosbeak | *Mycerobas affinis* | GBIF |
| 90 | Dark-sided Thrush | *Zoothera marginata* | GBIF |
| 87 | Desert Owl | *Strix hadorami* | GBIF |
| 35 | Finn's Weaver | *Ploceus megarhynchus* | GBIF |
| 69 | Fire-capped Tit | *Cephalopyrus flammiceps* | GBIF |
| 67 | Great Parrotbill | *Paradoxornis aemodius* | GBIF |
| 48 | Green Avadavat | *Amandava formosa* | GBIF |
| 89 | Green-crowned Warbler | *Phylloscopus burkii* | GBIF |
| 7 | Himalayan Quail | *Ophrysia superciliosa* | GBIF |
| 33 | Kashmir Nuthatch | *Sitta cashmirensis* | GBIF |
| 12 | Long-billed Bush Warbler | *Locustella major* | GBIF |
| 79 | Long-tailed Thrush | *Zoothera dixoni* | GBIF |
| 93 | Nilgiri Pipit | *Anthus nilghiriensis* | GBIF |
| 38 | Orange Bullfinch | *Pyrrhula aurantiaca* | GBIF |
| 94 | Rock Bush Quail | *Perdicula argoondah* | GBIF |
| 64 | Rusty-flanked Treecreeper | *Certhia nipalensis* | GBIF |
| 96 | Slender-billed Vulture | *Gyps tenuirostris* | GBIF |
| 90 | Snow Partridge | *Lerwa lerwa* | GBIF |
| 80 | Spot-winged Starling | *Saroglossa spilopterus* | iNaturalist |
| 77 | Streaked Rosefinch | *Carpodacus rubicilloides* | GBIF |
| 87 | Swamp Francolin | *Ortygornis gularis* | GBIF |
| 36 | Tibetan Eared Pheasant | *Crossoptilon harmani* | GBIF |
| 78 | Tibetan Lark | *Melanocorypha maxima* | GBIF |
| 47 | Tibetan Sandgrouse | *Syrrhaptes tibetanus* | GBIF |
| 45 | Tibetan Serin | *Spinus thibetanus* | GBIF |
| 47 | Tibetan Snowfinch | *Montifringilla henrici* | GBIF |
| 78 | Upland Pipit | *Anthus sylvanus* | GBIF |
| 66 | Western Tragopan | *Tragopan melanocephalus* | GBIF |
| 47 | White-cheeked Nuthatch | *Sitta leucopsis* | GBIF |
| 66 | White-tailed Stonechat | *Saxicola leucurus* | GBIF |
| 18 | White-throated Bushtit | *Aegithalos niveogularis* | GBIF |
| 85 | Yellow-legged Buttonquail | *Turnix tanki* | GBIF |

Worst cases: Himalayan Quail 7 (specimen photos only, presumed extinct — no live-bird photos exist; consider excluding from v1), Long-billed Bush Warbler 12, Brooks's Leaf Warbler 13, White-throated Bushtit 18, Finn's Weaver 35, Black-and-yellow Grosbeak 35, Tibetan Eared Pheasant 36, Orange Bullfinch 38, Tibetan Serin 45, Tibetan Snowfinch 47, White-cheeked Nuthatch 47, Green Avadavat 48.

## 7. What still needs a decision (user)

1. **Lesser Sand Plover** — split into Tibetan vs Siberian Sand Plover; needs photo-level ID of the folder's photos (or new photos) before it becomes a class.
2. **Grey Bush Robin** — no recognised taxon; what bird was this folder meant to be?
3. **The 13 drops** — all have evidence in §3, but three are close calls (Slaty-breasted Rail, Mongolian Bunting/Pallas's Reed Bunting, Coral-billed Scimitar Babbler). If the user has a documented J&K record for any of them, reinstate it with the resolved scientific name in §3.
4. **Black-headed Munia** — the name was historically applied to both *Lonchura malacca* and *L. atricapilla*; resolved to *malacca* (Tricolored Munia) because iNaturalist maps the name to it, the 2024 J&K checklist lists only *malacca*, and GBIF has 24 vs 0 occurrences in the region. Flag if the intended bird was *atricapilla* (Chestnut Munia).
5. **Himalayan Quail** — 7 specimen photos only. Include as a 7-image class in v1, or exclude it and add it later if live photos ever exist?

## Files

- `cleaned-species-list.csv` — 691 kept classes (folders, IOC common name, scientific name, category, family, genus, corrected usable-image count, best source, count-verified flag, status) + 13 dropped + 2 unresolved rows.
- `work/resolve_sectionA.json`, `work/resolve_blanks_wrong.json` — per-row resolutions with evidence.
- `work/ioc_species.json` — IOC 15.2 species lookup used as authority.
- `work/recount.py`, `work/recount_all.jsonl`, `work/recount_p2_0.jsonl`, `work/recount_p2_1.jsonl`, `work/commons_low_counts.json` — recount method and raw results.
- `work/build_cleaned.py`, `work/build_state.json` — build script and intermediate state.
