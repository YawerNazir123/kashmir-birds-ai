"""
Kashmir Birds AI — baseline training script (single flat model)
================================================================
Model: ConvNeXt-Tiny, pretrained on ImageNet, fine-tuned on 691 Kashmir
bird species. One flat 691-way classifier (NOT two-stage — the baseline
to beat; the two-stage family-first variant is tested against this later).

Run on Kaggle (free T4 GPU, 16 GB VRAM):
  1. Upload the dataset to Kaggle as a dataset (see train_baseline.ipynb
     for the steps): the folder `dataset/` with train/val/test/
     subfolders, one folder per species, named <Scientific_name>
     (spaces replaced by '_'), e.g. dataset/train/Psittacula_eupatria/.
  2. Attach the dataset to a Kaggle notebook, install requirements
     (timm, torch, torchvision — torch is preinstalled on Kaggle),
     and run this script, or run the notebook cells that call it.
  3. Outputs (best checkpoint, ONNX export, class list, metrics) are
     written to ./outputs/ — download them from the notebook when done.

Dataset: ~/workspace/kashmir-birds/model-data/dataset/ (local copy).
Cleaned species list: cleaned-species-list.csv (691 kept species).
Split is already done BY OBSERVATION (70/15/15) in the folder layout —
do NOT re-split randomly here.

Techniques (why each one is here):
  - Transfer learning, two phases: head-only first (backbone frozen),
    then unfreeze all at a low LR. Stops catastrophic forgetting.
  - RandAugment + MixUp/CutMix: the lookalike genera (leaf warblers,
    buntings, pipits) need boundary learning, not memorisation.
  - Label smoothing 0.1 + class-weighted loss: rare species (20-30
    photos) must not be drowned by common ones (capped at 200-300).
  - Mixed precision (AMP): fits batch 64 on a T4.
  - Top-1 / Top-5 + per-genus accuracy: top-1 alone hides the truth
    on 691 classes; per-genus scores show where the confusions live.
  - Test-time augmentation (flip) at final evaluation only.
"""

import argparse
import csv
import json
import math
import os
import random
import time
from collections import Counter, defaultdict
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, transforms

import timm
from timm.data import Mixup
from timm.loss import LabelSmoothingCrossEntropy, SoftTargetCrossEntropy
from timm.optim import create_optimizer_v2

IMG_SIZE = 224
BATCH = 64            # T4 16GB; drop to 32 on 6GB laptop GPUs
WORKERS = 4
EPOCHS_HEAD = 3       # phase 1: head only
EPOCHS_FULL = 17      # phase 2: whole model (total 20)
LR_HEAD = 3e-4
LR_FULL = 5e-5
LABEL_SMOOTHING = 0.1


def set_seed(seed=42):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def build_transforms():
    train_tf = transforms.Compose([
        transforms.RandomResizedCrop(IMG_SIZE, scale=(0.6, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandAugment(num_ops=2, magnitude=9),
        transforms.ColorJitter(0.2, 0.2, 0.2, 0.05),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
        transforms.RandomErasing(p=0.25),
    ])
    eval_tf = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    return train_tf, eval_tf


def class_weights(train_dir, classes):
    """Inverse-frequency weights, capped so the rarest species do not
    dominate the loss. Computed from actual on-disk train counts."""
    counts = Counter()
    for cls in classes:
        n = len(list((Path(train_dir) / cls).glob("*.[jJ][pP][gG]"))) \
            + len(list((Path(train_dir) / cls).glob("*.png")))
        counts[cls] = max(n, 1)
    total = sum(counts.values())
    n_cls = len(classes)
    w = torch.tensor([min(total / (n_cls * counts[c]), 5.0)
                      for c in classes], dtype=torch.float32)
    print(f"train images: {total}, classes: {n_cls}, "
          f"min/class {min(counts.values())}, max/class {max(counts.values())}")
    return w


@torch.no_grad()
def evaluate(model, loader, device, classes, genus_of, tta=False):
    model.eval()
    correct1 = correct5 = total = 0
    genus_correct = defaultdict(int)
    genus_total = defaultdict(int)
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        with torch.autocast("cuda", enabled=device.type == "cuda"):
            logits = model(x)
            if tta:  # horizontal-flip TTA
                logits = (logits + model(torch.flip(x, dims=[3]))) / 2
        top5 = logits.topk(5, dim=1).indices
        correct1 += (top5[:, 0] == y).sum().item()
        correct5 += sum(y[i].item() in top5[i].tolist()
                        for i in range(len(y)))
        total += len(y)
        for i, label in enumerate(y.tolist()):
            g = genus_of[classes[label]]
            genus_total[g] += 1
            if top5[i, 0].item() == label:
                genus_correct[g] += 1
    acc1, acc5 = correct1 / total, correct5 / total
    worst = sorted(((genus_correct[g] / genus_total[g], g, genus_total[g])
                    for g in genus_total), reverse=False)[:10]
    return acc1, acc5, worst


def train_one_phase(model, loader, val_loader, device, args, epochs,
                    lr, mixup_fn, criterion, optimizer, scheduler,
                    classes, genus_of, out_dir, phase_name, best):
    scaler = torch.amp.GradScaler("cuda", enabled=device.type == "cuda")
    for epoch in range(epochs):
        model.train()
        t0, running, seen = time.time(), 0.0, 0
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            if mixup_fn is not None:
                x, y = mixup_fn(x, y)
            with torch.autocast("cuda", enabled=device.type == "cuda"):
                logits = model(x)
                loss = criterion(logits, y)
            optimizer.zero_grad()
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            running += loss.item() * len(x)
            seen += len(x)
        scheduler.step()
        acc1, acc5, worst = evaluate(model, val_loader, device,
                                     classes, genus_of)
        print(f"[{phase_name}] epoch {epoch+1}/{epochs} "
              f"loss {running/seen:.4f} val top1 {acc1:.4f} "
              f"top5 {acc5:.4f} lr {optimizer.param_groups[0]['lr']:.2e} "
              f"({time.time()-t0:.0f}s)")
        print(f"  worst genera: {worst[:5]}")
        if acc1 > best["acc1"]:
            best.update(acc1=acc1, acc5=acc5)
            torch.save({"model": model.state_dict(),
                        "classes": classes, "acc1": acc1, "acc5": acc5},
                       out_dir / "best_checkpoint.pth")
            print(f"  -> saved best checkpoint ({acc1:.4f})")
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="/kaggle/input/kashmir-birds-dataset/dataset",
                    help="dataset root with train/val/test folders")
    ap.add_argument("--out", default="./outputs")
    ap.add_argument("--model", default="convnext_tiny",
                    help="timm model name; convnext_tiny fits 6GB too (batch 32)")
    ap.add_argument("--batch", type=int, default=BATCH)
    ap.add_argument("--epochs", type=int, default=EPOCHS_HEAD + EPOCHS_FULL)
    ap.add_argument("--species-csv",
                    default="/kaggle/input/kashmir-birds-dataset/cleaned-species-list.csv")
    args = ap.parse_args()
    set_seed()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Genus map (for per-genus evaluation) from the cleaned species list.
    genus_of = {}
    if os.path.exists(args.species_csv):
        with open(args.species_csv) as f:
            for row in csv.DictReader(f):
                if row["status"] in ("ok", "low"):
                    key = row["scientific_name"].replace(" ", "_")
                    genus_of[key] = row["genus"]
    train_tf, eval_tf = build_transforms()
    train_ds = datasets.ImageFolder(os.path.join(args.data, "train"), train_tf)
    val_ds = datasets.ImageFolder(os.path.join(args.data, "val"), eval_tf)
    test_ds = datasets.ImageFolder(os.path.join(args.data, "test"), eval_tf)
    classes = train_ds.classes
    print(f"classes: {len(classes)}  train {len(train_ds)}  "
          f"val {len(val_ds)}  test {len(test_ds)}")
    assert len(classes) <= 691, f"expected <=691 classes, got {len(classes)}"
    for c in classes:
        genus_of.setdefault(c, c.split("_")[0])
    (out_dir / "classes.json").write_text(json.dumps(classes, indent=1))

    # Class-balanced sampling (capped): rare species are oversampled so
    # they are not drowned by common ones. Works with MixUp/CutMix,
    # unlike a weighted loss on soft targets.
    _counts = Counter(t for _, t in train_ds.samples)
    _sample_w = [min(1.0 / _counts[t], 0.05) for _, t in train_ds.samples]
    train_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=False,
                              sampler=WeightedRandomSampler(
                                  _sample_w, num_samples=len(train_ds),
                                  replacement=True),
                              num_workers=WORKERS, pin_memory=True,
                              drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch, shuffle=False,
                            num_workers=WORKERS, pin_memory=True)
    test_loader = DataLoader(test_ds, batch_size=args.batch, shuffle=False,
                             num_workers=WORKERS, pin_memory=True)

    model = timm.create_model(args.model, pretrained=True,
                              num_classes=len(classes))
    model.to(device)
    mixup_fn = Mixup(mixup_alpha=0.2, cutmix_alpha=1.0, prob=1.0,
                     switch_prob=0.5, mode="batch",
                     label_smoothing=LABEL_SMOOTHING,
                     num_classes=len(classes))
    weights = class_weights(os.path.join(args.data, "train"), classes).to(device)
    # Class balance is handled by the WeightedRandomSampler above (it works
    # with MixUp soft targets, a weighted CE loss does not). The weights
    # are saved for analysis / the focal-loss variant.
    torch.save(weights.cpu(), out_dir / "class_weights.pt")
    criterion = SoftTargetCrossEntropy()

    best = {"acc1": 0.0, "acc5": 0.0}
    # Phase 1 — head only: freeze the backbone.
    for name, p in model.named_parameters():
        p.requires_grad = ("head" in name or "fc" in name)
    opt = create_optimizer_v2(model, opt="adamw", lr=LR_HEAD,
                              weight_decay=0.05)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
    best = train_one_phase(model, train_loader, val_loader, device, args,
                           EPOCHS_HEAD, LR_HEAD, mixup_fn, criterion,
                           opt, sched, classes, genus_of, out_dir,
                           "head-only", best)
    # Phase 2 — unfreeze everything at a low LR.
    for p in model.parameters():
        p.requires_grad = True
    opt = create_optimizer_v2(model, opt="adamw", lr=LR_FULL,
                              weight_decay=0.05)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
    best = train_one_phase(model, train_loader, val_loader, device, args,
                           args.epochs - EPOCHS_HEAD, LR_FULL, mixup_fn,
                           criterion, opt, sched, classes, genus_of,
                           out_dir, "full-finetune", best)

    # Final test evaluation (with flip TTA) on the best checkpoint.
    ckpt = torch.load(out_dir / "best_checkpoint.pth",
                      map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    acc1, acc5, worst = evaluate(model, test_loader, device,
                                 classes, genus_of, tta=True)
    print(f"TEST (TTA) top1 {acc1:.4f} top5 {acc5:.4f}")
    print(f"worst genera on test: {worst}")
    metrics = {"val_best_top1": best["acc1"], "val_best_top5": best["acc5"],
               "test_top1_tta": acc1, "test_top5_tta": acc5,
               "worst_genera_test": worst,
               "classes": len(classes)}
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))

    # Export to ONNX for the website (Render service).
    dummy = torch.randn(1, 3, IMG_SIZE, IMG_SIZE, device=device)
    torch.onnx.export(model.eval(), dummy, out_dir / "model.onnx",
                      input_names=["image"], output_names=["logits"],
                      dynamic_axes={"image": {0: "batch"},
                                    "logits": {0: "batch"}},
                      opset_version=13)
    print(f"done. best val top1 {best['acc1']:.4f}, "
          f"test top1 {acc1:.4f} / top5 {acc5:.4f}. "
          f"outputs in {out_dir}")


if __name__ == "__main__":
    main()
