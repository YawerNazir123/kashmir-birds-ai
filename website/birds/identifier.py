"""Bird identification with the trained ConvNeXt-Tiny model (ONNX).

Model: single flat 689-way classifier, trained on Kaggle (v5 run,
test top-1 50.93% / top-5 74.04% with test-time augmentation).
Exported to ONNX (fp16) and verified against the PyTorch checkpoint:
99.5% top-1 agreement on 200 test images.

The model file itself (model.onnx, ~57 MB) is NOT committed to the repo
-- GitHub blocks files over 100 MB and the push tooling rejects binary
content. It is downloaded at Render build time by the `download_model`
management command (see render.yaml) from the public Kaggle dataset
yawarnazir/kashmir-birds-model-onnx, into this same directory.
`classes.json` (the 689 species, in model output order) IS committed.

Inference is lazy: the ONNX session is created on the first photo,
not at import time, so the landing page and gallery stay fast and a
missing model file never breaks the rest of the site.
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

MODEL_DIR = Path(__file__).resolve().parent / "model"
MODEL_PATH = MODEL_DIR / "model.onnx"
CLASSES_PATH = MODEL_DIR / "classes.json"

# Must match the eval transform used in training (train_baseline.py).
IMG_SIZE = 224
_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

_session = None
_classes = None


def model_available():
    """True when the downloaded model file and class list are present."""
    return MODEL_PATH.exists() and CLASSES_PATH.exists()


def _load():
    global _session, _classes
    if _session is None:
        import onnxruntime as ort

        _classes = json.loads(CLASSES_PATH.read_text())
        _session = ort.InferenceSession(
            str(MODEL_PATH), providers=["CPUExecutionProvider"]
        )
    return _session, _classes


def _preprocess(image):
    """Resize shortest side to 256, centre-crop 224, normalise.

    `image` is a PIL image (already RGB). Returns a float16 array of
    shape (1, 3, 224, 224) -- the fp16 model expects float16 input.
    """
    w, h = image.size
    scale = 256 / min(w, h)
    image = image.resize(
        (round(w * scale), round(h * scale)), Image.BILINEAR
    )
    w, h = image.size
    left, top = (w - IMG_SIZE) // 2, (h - IMG_SIZE) // 2
    image = image.crop((left, top, left + IMG_SIZE, top + IMG_SIZE))
    arr = np.asarray(image, dtype=np.float32) / 255.0
    arr = (arr - _MEAN) / _STD
    return arr.transpose(2, 0, 1)[None, :, :, :].astype(np.float16)


def predict(image, top_k=5):
    """Top-k predicted species for a PIL image.

    Returns a list of (scientific_name, confidence) with confidence
    in [0, 1], best first. Scientific names use underscores, exactly
    as in classes.json (e.g. "Passer_domesticus").
    """
    session, classes = _load()
    x = _preprocess(image.convert("RGB"))
    logits = session.run(None, {"image": x})[0][0].astype(np.float64)
    probs = np.exp(logits - logits.max())
    probs /= probs.sum()
    idx = probs.argsort()[::-1][:top_k]
    return [(classes[i], float(probs[i])) for i in idx]
