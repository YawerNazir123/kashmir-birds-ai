# Kashmir Birds AI — Model Profile (two-stage identification idea)

**Date:** 2026-10-25
**Repo HEAD analysed:** `8bf1715d` (main)
**Sources used:** all 744 `bird_database/*/info.json` files (downloaded from `main`), the committed `website/db.sqlite3`, the full GitHub repo tree (21,165+ entries), a random 40-image sample checked for dimensions, and live iNaturalist API counts (2026-10-25).
**Rule for this document:** read-only analysis. Nothing in the repo was changed.

> **Pivot (user correction, 2026-10-25):** we do NOT have training data right now and will NOT train on the existing 5-images-per-bird database. The existing database is used here only for the **target species list**. Training data will be downloaded fresh. Sections 1–3 profile the existing data (so we know what it is and is not); Sections 4–6 are the download plan, sources, and the verdict on the two-stage idea based on that plan.

---

## 1. Target species list — the 744 species the model must identify

- **744 species** with an `info.json` in `bird_database/` (760 folders total; see §3 for the 16 extra folders).
- Full list saved as [`species-list.csv`](sandbox://workspace/kashmir-birds/species-list.csv) — 744 rows with: folder, common name, scientific name, category, family, genus, migratory status, region, Kashmiri name, existing images in repo, and whether it is in the committed DB.
- **9 species have a blank scientific name** in `info.json` (Scaly-bellied Wren-Babbler, Pied Stonechat, Oriental White-eye, Mongolian Bunting, Grey Bush Robin, Grey-headed Bushchat, Eurasian Bee-eater, Chestnut-headed Laughingthrush, Black-headed Munia) — these must be resolved to a correct binomial before downloading, or the download query will miss/mismatch them.
- **97 / 744 species have a Kashmiri name** (`local_name_kashmiri` non-blank). The name is display metadata, not a training feature.
- **46 species in `info.json` are NOT in the committed `db.sqlite3`** (e.g. Coal Tit, Grandala, Egyptian Vulture, Northern Wheatear, Dark-sided Flycatcher, Rusty-tailed Flycatcher, Rosy Minivet, Greater Coucal, Plum-headed Parakeet, Speckled Wood Pigeon, Wedge-tailed Green Pigeon, Yellow-eyed Pigeon). The committed DB has 724 rows and **0 Kashmiri names** — it is a stale snapshot from before the names/metadata work. The live Render DB was refreshed to 744 rows, but the file in the repo is still stale. **Use `info.json` (or the live DB), never the committed `db.sqlite3`, as the species list.**
- **26 rows in the committed DB have no `info.json`** — the deleted/renamed birds (European Starling, Great Tit, Marsh Harrier, Purple Moorhen, Whimbrel, Spot-billed Duck, etc.). These are ghosts in the old snapshot, not target species.

## 2. Categories, families, genera — the groupings a stage-1 model could use

### 2.1 Categories (the site's `category` field)

`info.json` has **12 distinct category values** (the site says "8 categories" — that matches the stale DB, which has only 8):

| Category | Species | Share |
|---|---|---|
| Other | 375 | 50.4% |
| Songbird | 228 | 30.6% |
| Raptor | 62 | 8.3% |
| Owl | 27 | 3.6% |
| Pigeon/Dove | 15 | 2.0% |
| Egret/Heron | 14 | 1.9% |
| Duck | 11 | 1.5% |
| Kingfisher | 6 | 0.8% |
| Swan | 2 | 0.3% |
| Goose | 2 | 0.3% |
| Parakeet | 1 | 0.1% |
| Pheasant | 1 | 0.1% |

**The category field is complete (744/744 non-blank) but it is not a visual grouping:**
- `Other` (half of all species) spans **69 families** — waders, gamebirds, woodpeckers, gulls, cuckoos, rails, swifts, crows, sparrows… there is no visual concept of "Other" for a model to learn.
- `Songbird` spans **32 families** (flycatchers, finches, wagtails, thrushes, warblers, buntings…).
- Four categories have ≤2 species (Swan 2, Goose 2, Parakeet 1, Pheasant 1) — unlearnable as classes; a stage-1 model would never see enough examples.
- Category labels also disagree between `info.json` and the committed DB for many species (DB: Other 417 vs info.json 375; Songbird 186 vs 228) — the DB snapshot predates the category corrections.

### 2.2 Families — 89 distinct

| Family | Species |
|---|---|
| Muscicapidae (chats, flycatchers, robins) | 67 |
| Accipitridae (hawks, eagles, harriers) | 52 |
| Fringillidae (finches, rosefinches) | 30 |
| Phasianidae (pheasants, partridges) | 28 |
| Strigidae (owls) | 27 |
| Scolopacidae (sandpipers, snipes) | 26 |
| Picidae (woodpeckers) | 22 |
| Laridae (gulls, terns) | 22 |
| Motacillidae (wagtails, pipits) | 20 |
| Turdidae (thrushes) | 20 |
| Phylloscopidae (leaf warblers) | 17 |
| Anatidae (ducks, geese, swans) | 16 |
| Cuculidae (cuckoos) | 16 |
| Columbidae (pigeons, doves) | 15 |
| Emberizidae (buntings) | 15 |
| Ardeidae (herons, egrets) | 14 |
| Corvidae (crows, jays) | 14 |
| Leiothrichidae (laughingthrushes, babblers) | 14 |
| Passeridae (sparrows) | 13 |
| Rallidae (rails, coots, moorhens) | 12 |

24 families have ≥10 species; 19 families have exactly 1 species. Families are taxonomically and (mostly) visually coherent — unlike `category`.

### 2.3 Genera — where the real confusion lives

- **344 distinct genera.** **148 genera have ≥2 species, covering 537 of 744 species (72%).** The model will mostly be confused *within* a genus, not across genera.
- Largest multi-species genera (species that look very alike):

| Genus | Species | Notes |
|---|---|---|
| *Phylloscopus* (leaf warblers) | 17 | Famously near-identical; separated by call, wing bars, leg colour |
| *Emberiza* (buntings) | 15 | |
| *Turdus* (thrushes) | 13 | |
| *Anthus* (pipits) | 12 | Ground birds, subtle streaking differences |
| *Falco* (falcons) | 11 | |
| *Phoenicurus* (redstarts) | 10 | |
| *Ficedula* (flycatchers) | 9 | |
| *Oenanthe* (wheatears) | 9 | |
| *Calidris* (sandpipers/stints) | 9 | Waders — size and bill shape matter |
| *Prunella* (accentors) | 8 | |
| *Motacilla*, *Passer*, *Carpodacus*, *Acrocephalus* | 7 each | |
| *Columba*, *Tringa*, *Pericrocotus*, *Circus*, *Lanius*, *Aquila*, *Psittacula*, *Caprimulgus*, *Apus* | 6 each | |
| *Saxicola*, *Enicurus*, *Dicrurus*, *Strix*, *Otus*, *Ardea*, *Pitta* | 5 each | |

30 genera have ≥5 species. Any evaluation must report accuracy *within* these genera separately — overall accuracy will hide the failures.

## 3. What the existing database is (and is not) — for the record

This data will **not** be trained on, but its profile explains why the previous model struggled, and it can later be added as a small supplement after cleaning.

- **Images:** 3,529 image files in `bird_database/`. Distribution: **705 species have 5 images, 1 has 3 (Western Tragopan), 1 has 1 (Himalayan Quail), 53 have 0 images** (the newly created records, `images: []`). The `images` field in `info.json` agrees except for Himalayan Quail (has 1 file, field is empty).
- **16 orphan folders** have images but no `info.json` (the 18 deleted birds minus 2, e.g. `great_tit`, `marsh_harrier`, `himalayan_golden_eagle`, `purple_cochoa`) — 80 images of birds that are not target species.
- **Duplicate images across species — serious:** 103 identical files (same blob SHA) appear in more than one species folder; **36 species pairs share at least one identical image; 19 pairs share ≥3; 11 pairs share all 5 images** (the two folders are exact copies of the same bird under two names — duplicate folders not yet merged). Worst cases: Black-throated Bushtit ↔ Black-throated Tit (5/5), Brown Boobook ↔ Brown Hawk Owl (5/5), Clamorous Reed Warbler ↔ Indian Reed Warbler (5/5), Fire-fronted Serin ↔ Red-fronted Serin (5/5), Fork-tailed Swift ↔ Pacific Swift (5/5), Güldenstädt's Redstart ↔ White-winged Redstart (5/5), Himalayan Bulbul ↔ White-cheeked Bulbul (5/5), Hume's Leaf Warbler ↔ Hume's Warbler (5/5), Mountain Hawk-eagle ↔ Mountain Hawk Eagle (5/5), Plumbeous Redstart ↔ Plumbeous Water Redstart (5/5), White-capped Redstart ↔ White-capped Water Redstart (5/5), Bearded Vulture ↔ Lammergeier (4/5). Identical images with different labels are poison for training: the model cannot learn a distinction that does not exist in the pixels.
- **Corrupt/tiny files:** 24 images are <20 KB, 11 are <10 KB. `eurasian_collared_dove/3.jpg` is **282 bytes and is an XML document, not an image** (verified by reading it).
- **Resolution is generally fine:** a random sample of 40 images was all readable — median width 1024 px, min 463 px, 6/40 under 640 px wide. Resolution is not the problem; label duplication and scarcity are.
- **Field completeness in `info.json`** (non-blank / 744): common_name 744, category 744, migratory_status 741, region 740, description 739, wikipedia_url 737, scientific_name 735, family 735, genus 733, length 634, weight 569, wingspan 511, local_name_kashmiri 97, iucn_status 82, size 78, habitat 35, conservation_status 27, local_name (generic) 0. Habitat/conservation/size are mostly empty — irrelevant for image classification, but don't plan to use them as features.
- `website/media/` holds 17,045 files — imported copies of the same photos, not a separate source.

## 4. Dataset plan — downloading fresh training data

### 4.1 How many images per species

| Level | Train images / species | Total train (744 spp.) | What to expect |
|---|---|---|---|
| Minimum viable | 50 | ~37,000 | Works for fine-tuning a pretrained model on distinctive species; confusable genera (leaf warblers, pipits, buntings) will be poor |
| **Good (recommended target)** | **100–150** | **~74,000–112,000** | The standard working point for fine-grained transfer learning; comparable to the Kaggle 525-species set (~160/species) |
| Ideal | 200–300 | ~149,000–223,000 | Diminishing returns beyond this for most species; worth it only for the hardest genera |

- **Cap common species** at ~200–300 images: do not let House Sparrow contribute 5,000 photos while Western Tragopan has 20 — cap and balance, or the model just learns the common classes.
- **Validation/test:** hold out 15% / 15% per species on top of train (so ~100 train ⇒ ~15 val + ~15 test). At the minimum level (50 train), use 40 train / 5 val / 5 test and accept noisy per-species test numbers.
- **Storage:** at ~100–200 KB per photo, 100 images/species ≈ **11–15 GB** total; 200/species ≈ 22–30 GB. Download size is not the bottleneck; cleaning is.
- **Split by observation, not by photo.** One iNaturalist observation often has several photos of the same individual bird. All photos from one observation must go into the same split, or near-duplicates leak from train into test and the test score lies.
- **Image requirements:** JPEG, shortest side ≥224 px (model input is 224 or 384 px), prefer ≥640 px on the long side; dedupe by exact hash *and* perceptual hash (near-duplicates from the same photo burst); drop illustrations, captive birds, nests/eggs-only shots, and photos where the bird is tiny in the frame; keep diversity — male/female/juvenile, breeding/non-breeding plumage, perched/flying, different backgrounds and seasons. Prefer photos taken in J&K / the Himalaya where available (domain match with what users will photograph), but global photos of the same species are fine.
- **Metadata to keep per image:** common name, scientific name, category, family, genus, source (e.g. iNaturalist), source URL, observation/photo ID, licence, photographer (attribution), date, country/region, sex/age if known. Store it in a CSV/JSONL next to the images — this is what makes the dataset auditable and lets you filter or re-split later.
- **Rare / hard species — the long tail is real.** Live iNaturalist research-grade observation counts (2026-10-25) for a sample of our species: House Sparrow 512,745; White-cheeked Bulbul 2,056; Hume's Leaf Warbler 1,465; Güldenstädt's Redstart 1,135; Himalayan Monal 563; White-winged… Stewart's Bunting 201; Grandala 172; Yellow-eyed Pigeon 109; Kashmir Flycatcher 83; **Western Tragopan 2**. For the rarest endemics there may be only 10–30 usable photos on the whole internet. Plan for them explicitly: accept 20–30 images with heavy augmentation and class weighting; consider a "rare species" tier in v1 (model may answer with lower confidence, or the app says "likely X — rare, please confirm"); never pad a rare class with photos of a different species. If a species ends up with <15 usable photos, consider leaving it out of v1 and adding it later rather than shipping a class the model has never really seen.

### 4.2 Sources — pros, cons, licensing, method

| Source | What it is | Pros | Cons / limits | Licence | Method |
|---|---|---|---|---|---|
| **iNaturalist via GBIF + AWS Open Data — primary source** | Research-grade observations, photos included | Huge volume; covers most of our 744; photos have per-photo licences; includes date/location; GBIF export is a single structured download; iNaturalist AWS bucket holds open-licensed photos in bulk | GBIF export gives only the *first* photo per observation; API rate limits (~1 req/s, ~10k/day; >5 GB media/hr can get blocked); quality varies; even research-grade IDs can be wrong; rare Himalayan species are thin (see §4.1) | GBIF only carries open licences (CC0, CC-BY, CC-BY-NC). Filter to those. Attribution required (CC-BY). **CC-BY-NC is fine for this non-commercial project; do not use it in a commercial product later without re-checking.** | GBIF occurrence download (species list + `mediaType=StillImage` + licence filter), then download photo URLs; or iNaturalist API per species for all photos |
| **GBIF (general)** | Aggregator of occurrence datasets (iNaturalist, museums, other surveys) | One download API; licence and media filters; standard Darwin Core format | Media coverage varies by dataset; eBird occurrences come without photos; museum specimen photos are often dead/preserved specimens, not field photos — filter them out | Per-dataset licence; filter to CC0/CC-BY/CC-BY-NC | GBIF download API with taxon + media filters |
| **Macaulay Library / eBird — NOT a bulk download source** | The world's largest bird-photo archive | Best coverage and quality of any source; the photos exist for nearly every species | **Copyright stays with each photographer; there is no bulk download of other people's media and downloading it for third-party use without permission is not allowed.** Some contributors now optionally apply a CC licence, but that is per-photo and must be requested/checked individually. | Per-photo, mostly all-rights-reserved | Do not scrape or bulk-download. Use for reference/verification, and for the user's own photos. eBird *occurrence data* (not photos) can be requested for research under its terms |
| **Wikimedia Commons** | Community photo repository | Clear per-file licences; API access; good for common/well-known species | Thin for rare Himalayan species (often 1–5 photos/species); variable quality and labelling; must check the licence on every file | Mostly CC-BY / CC-BY-SA / public domain — check per file | Commons API (`generator=search` / category) per scientific name |
| **Kaggle "525 Bird Species" dataset — supplement only** | ~85,000–90,000 images, 525 species, ~160/species, ready-made train/val/test folders | Ready to use; proven in many published projects (fine-tuned models report ~93–97% test accuracy on it) | **The dataset page has been removed from Kaggle** (availability uncertain); licence/provenance unclear (web-scraped images); unknown overlap with our 744 — many species are New World or cage birds; labels not verified | Unclear — do not rely on it commercially | Only after checking the species overlap with our list; use as extra images for the overlapping species, not as the base dataset |
| **CUB-200-2011 / NABirds — benchmarks, not sources** | Academic fine-grained datasets (CUB: 11,788 images, 200 spp., with bounding boxes; NABirds: ~50,000 images, 400 spp.) | Clean labels; CUB has bounding boxes (useful for cropping/attention) | North American species only — small overlap with Kashmir; research-only licences | Research use | Reference/benchmarking only |
| **Xeno-canto** | Bird sounds | — | Audio only; not needed for a photo-ID model (note for a possible future audio feature) | CC licences per recording | Not used for this model |

**Recommended pipeline:** GBIF/iNaturalist as the base for all 744 species → Wikimedia Commons to top up species that are thin on iNaturalist → Kaggle 525 only for overlapping species after an overlap check → manual review of a sample per species (and all images for the rarest 50 species) → dedupe → split by observation → train.

## 5. Verdict — is the two-stage idea right?

**Short answer: the instinct is right, but the grouping is wrong. Don't build two models on the site's `category`. Build one flat model on a pretrained backbone first, and use taxonomy (family/genus) — not `category` — if you add hierarchy later.**

### 5.1 Where the user is right
- 744-way flat classification *is* hard, and the errors are not random — they concentrate inside lookalike groups (leaf warblers, pipits, buntings, wheatears). Dividing the problem is a sound instinct.
- A coarse step that is easy and reliable does help: if you can confidently narrow 744 candidates to ~10–20, the fine step has a much easier job, and its errors become interpretable ("it confused two *Phylloscopus* warblers" is a meaningful failure mode).
- Shared features within a real taxonomic group (same family/genus) genuinely transfer — a model that has learned "warbler" features can separate warbler species with less data per species.

### 5.2 Where the two-stage idea, as proposed, hurts
- **Error cascade, unrecoverable.** If stage 1 says the wrong category, stage 2 *cannot* recover — the right species is not even in its candidate set. Overall accuracy becomes (stage-1 accuracy) × (stage-2 accuracy given correct stage 1). With a stage-1 accuracy of, say, 90%, you have already capped the system at 90% before stage 2 starts.
- **The site's `category` is not learnable as a visual class.** Stage 1 would have to learn "Other" — a class containing 69 families and half the dataset (waders, gamebirds, woodpeckers, gulls, cuckoos, rails, swifts…). There is no visual pattern there; the model would just learn "everything that isn't a raptor/owl/duck/songbird". Four categories have ≤2 species and cannot be learned at all. Stage-1 accuracy on this labelling would be poor, and every stage-1 error would be fatal.
- **Category does not touch the actual hard problem.** All 17 *Phylloscopus* leaf warblers are "Songbird". All 15 *Emberiza* buntings are "Songbird". All 12 *Anthus* pipits are "Songbird". After stage 1, stage 2 still faces the exact same 17-way near-identical warbler problem, undiminished — the hierarchy removed the easy distinctions (eagle vs sparrow) and kept the hard ones.
- **Two models, twice the cost.** Two training runs, two serving paths, two failure modes to monitor, and each stage-2 model (if one per category) is trained on *less* data than a single model that shares features across all 744 species.
- **No architecture fixes data scarcity.** The previous model's weak results were most likely a data problem (5 images/species, duplicated images labelled as different species, wrong labels) more than an architecture problem. Two stages on 5 images/species would still fail. The fresh dataset (§4) is what fixes that, not the number of stages.

### 5.3 What would actually matter more (in order)
1. **Transfer learning from a pretrained backbone** — the single biggest factor. Fine-tune an ImageNet-pretrained ConvNeXt/EfficientNet (or a bird-specific pretrained model) instead of training from scratch. This is the proven recipe: the Kaggle 525-species models reach ~93–97% test accuracy this way on ~160 images/species.
2. **Enough images per species (§4.1)** — 100–150/species is the target; 50 is the floor.
3. **Clean labels** — dedupe (the 103 cross-species duplicates in the old data are a warning), remove wrong-species photos, split by observation.
4. **Hierarchy at the right level, if at all — family, not category.** If a second stage is added later, make stage 1 predict *family* (89 families, visually/taxonomically coherent) or use a hierarchical loss / coarse-to-fine head on one model, rather than two separate models. Even better: train the flat model first, look at its confusion matrix, and only add hierarchy for the genera it actually confuses.
5. **Evaluation that matches the real task** — report top-1 *and* top-5 accuracy, and per-genus accuracy for the 30 genera with ≥5 species. A model that is 90% overall but 40% on leaf warblers is not a 90% model for this app.
6. **Test on real user photos** — photos taken on a phone in Kashmir (backlit, distant, partially hidden birds), not just clean downloaded photos. The gap between the two is usually the biggest surprise.

### 5.4 Recommended sequence (understanding step only — no training run recommended yet)
1. Download the dataset per §4 (iNaturalist/GBIF first), with the per-image metadata in §4.1.
2. Clean + split by observation; audit the rarest 50 species by hand.
3. Baseline: **one flat fine-tuned model** on the pretrained backbone; measure top-1/top-5 and per-genus accuracy.
4. Only then decide about hierarchy: if within-genus confusion dominates, add a family-level coarse step or hierarchical loss and measure whether it *actually* beats the flat baseline on the same test set. Do not assume two-stage is better — test it.
