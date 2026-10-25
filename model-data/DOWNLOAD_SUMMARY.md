# Kashmir Birds AI — training dataset download, final summary

Date: 2026-10-25. Phase 1 of the training pipeline. No GPU training run yet.

## Verified totals (checked on disk by the coordinator, after cleanup)

- **Images: 97,330** — files on disk = manifest rows exactly (97,330 = 97,330)
- **Species: 691 / 691** — every kept species from cleaned-species-list.csv
- **Size: 12 GB** (`~/workspace/kashmir-birds/model-data/dataset/`)
- **Splits (by observation, 0 leaks):** train 68,233 (70.1%) / val 14,871 (15.3%) / test 14,226 (14.6%)
- **Sources:** iNaturalist 95,576 / GBIF 1,432 / Wikimedia Commons 322
- **Licences:** mostly CC-BY-NC (84,437), CC-BY (8,576), CC0 (1,960), CC-BY-SA (770), plus GBIF URL-form licences. **0 CC-BY-NC-ND images remain** (180 were found in slices 07/08 and deleted, with their manifest rows removed).
- **At target:** 672 species at ≥100 images. **19 species below 100** (see below).
- **Integrity:** 0 missing files, 0 zero-byte files, 0 observations split across splits, 0 duplicate URLs within a species.
- **Combined manifest:** `download/manifest-combined.csv` (97,330 rows). Per-slice manifests: `manifest-download-slice-01.csv` … `-10.csv`. Per-slice summaries: `summary-slice-01.txt` … `-10.txt`.

## Per-slice totals (verified)

| Slice | Species | Images | Size |
|---|---|---|---|
| 01 | 70 | 8,927 | 1,096 MB |
| 02 | 69 | 9,994 | 1,196 MB |
| 03 | 69 | 9,166 | 1,101 MB |
| 04 | 69 | 10,039 | 1,400 MB |
| 05 | 69 | 8,724 | 1,077 MB |
| 06 | 69 | 10,165 | 1,158 MB |
| 07 | 69 | 8,704 | 1,015 MB |
| 08 | 69 | 8,964 | 1,018 MB |
| 09 | 69 | 12,560 | 1,383 MB |
| 10 | 69 | 10,267 | 1,183 MB |

Slice 09 is larger because 62 species there were downloaded to the 200 cap (151–200 images).

## Species below 100 images (19) — genuine scarcity, all sources exhausted

| Images | Species |
|---|---|
| 2 | Western Tragopan (*Tragopan melanocephalus*) — 1 train / 0 val / 1 test; only 2 wild CC photos exist (GBIF's 66 are preserved specimens, excluded) |
| 7 | Himalayan Quail (*Ophrysia superciliosa*) — all 7 are Wikimedia Commons illustrations / a stamp / museum-skin photos, NOT live-bird photos |
| 13 | White-throated Bushtit (*Aegithalos niveogularis*) |
| 25 | Brooks's Leaf Warbler (*Phylloscopus subviridis*) |
| 26 | Orange Bullfinch (*Pyrrhula aurantiaca*) |
| 29 | Desert Owl (*Strix hadorami*) |
| 45 | Tibetan Eared Pheasant (*Crossoptilon harmani*) |
| 48 | Long-billed Bush Warbler (*Locustella major*) |
| 52 | Finn's Weaver (*Ploceus megarhynchus*) |
| 57 | Tibetan Serin (*Spinus thibetanus*) |
| 74 | Yellow-legged Buttonquail (*Turnix tanki*) |
| 75 | Swamp Francolin (*Ortygornis gularis*) |
| 78 | Black-and-yellow Grosbeak (*Mycerobas icterioides*) |
| 78 | Kashmir Nuthatch (*Sitta cashmirensis*) |
| 80 | White-browed Bush Robin (*Tarsiger indicus*) |
| 84 | Grey-headed Parakeet (*Psittacula finschii*) |
| 87 | White-cheeked Nuthatch (*Sitta leucopsis*) |
| 94 | Kashmir Flycatcher (*Ficedula subrubra*) |
| 96 | Dark-sided Thrush (*Zoothera marginata*) |

Recommendation: drop Himalayan Quail and Western Tragopan from v1 (7 illustrations / 2 photos cannot train a class) → 689 classes. The other 17 stay, with class-balanced sampling + augmentation in the training script.

## Cleanup done by the coordinator after the workers finished

1. **180 CC-BY-NC-ND images deleted** (slices 07/08, all GBIF) — the exclusion rule was missed by those two workers' GBIF licence parsing. Manifest rows removed; 0 ND rows remain.
2. **164 zero-byte files deleted** — EPERM husks left by a system-wide VM write block (~15:53–16:20 UTC) that hit all workers.
3. **23 duplicate files deleted (Chukar Partridge)** — exact byte duplicates of manifest files placed in a *different* split folder (a real split leak in the files, though the manifests showed 0 leaks). After deletion, disk = manifest exactly.
4. **10 duplicate URLs across species** — the same photo appears under two different species (e.g. one photo in both Curlew Sandpiper and Whiskered Tern folders). Only 10 images affected; flagged, not deleted — they need a human look to decide which species is correct, or both copies should be dropped before training.

## Incidents during download (all recovered)

- System-wide VM write block ~15:53–16:20 UTC (EPERM on writes, 0-byte husks) and a VM reboot ~16:17–16:18; workers resumed from manifests/checkpoints, no data lost.
- Egress proxy outage ~1 h (slice 09) and intermittent iNaturalist proxy/ChunkedEncoding errors — retried, no 429 rate limits from iNaturalist/GBIF at any point.
- Several workers hit GBIF licence-parsing bugs (licences are CC URLs, not codes) and fixed them; slice 06's resume bug briefly over-downloaded 5 species to 249–298, caught and trimmed back to the 150 cap.

## Kaggle training notebook — ready, NOT run

- `train_baseline.py` and `train_baseline.ipynb` in `~/workspace/kashmir-birds/model-data/`
- Single flat fine-tuned ConvNeXt-Tiny baseline, 691-way (689 if the two species above are dropped), pretrained ImageNet, two-phase training (head-only 3 epochs, full fine-tune 17), RandAugment, MixUp/CutMix, label smoothing 0.1, class-balanced sampling, mixed precision, batch 64, top-1/top-5 + per-genus evaluation, ONNX export. Both files syntax-checked (py_compile / JSON validation). No torch installed on this VM, so training was not test-run here.
- **Still needed before training:** a Kaggle account (username `yawarnazir` is in MEMORY.md, created 2026-10-25 — account access was not verified here), upload the dataset as a Kaggle dataset (`dataset/` + `cleaned-species-list.csv`), attach it to a notebook, and run it. The notebook's step 1 has the exact upload steps. I cannot create the Kaggle account or upload anything — that needs the user.

## What is NOT done

- No GPU training run (no dataset existed until now; no Kaggle access confirmed).
- The 10 cross-species duplicate-URL images are flagged, not resolved.
- Himalayan Quail / Western Tragopan are still in the dataset (flagged for dropping from v1).
