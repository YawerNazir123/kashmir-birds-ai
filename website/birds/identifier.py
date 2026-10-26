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

How the model gets onto the server (learned the hard way, 2026-10-26):
the build-time download is best-effort -- if it fails, the deploy
still goes ahead and the model is fetched at runtime instead. The
runtime download runs in a BACKGROUND thread with resume: the first
version downloaded synchronously inside the request, which meant the
first visitor's request hung while 57 MB came down, gunicorn killed
the worker at its 120 s request timeout, the partial file was
discarded, and the next request started again from zero -- forever.
Now the request returns immediately (the page says the model is
downloading), the thread keeps downloading, a partial file survives
worker restarts, and the next attempt resumes from where it stopped
via HTTP Range. The model becomes available as soon as the file is
complete -- no redeploy needed.
"""

import json
import os
import threading
import time
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

MODEL_DIR = Path(__file__).resolve().parent / "model"
MODEL_PATH = MODEL_DIR / "model.onnx"
MODEL_TMP_PATH = MODEL_DIR / "model.onnx.download"
CLASSES_PATH = MODEL_DIR / "classes.json"

# Same public model file the build-time download_model command uses.
MODEL_URL = os.environ.get(
    "MODEL_DOWNLOAD_URL",
    "https://www.kaggle.com/api/v1/datasets/download/"
    "yawarnazir/kashmir-birds-model-onnx/model.onnx",
)
_MIN_MODEL_BYTES = 10_000_000
# Wait this long after a failed download before starting a new attempt.
_RETRY_SECONDS = 60

# Must match the eval transform used in training (train_baseline.py).
IMG_SIZE = 224
_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

_session = None
_classes = None

# One lock guards the download thread handle and the status dict.
_lock = threading.Lock()
_download_thread = None
_download_state = {
    "status": "idle",  # idle | downloading | done | failed
    "downloaded": 0,  # bytes in the partial file
    "total": None,  # total bytes, once known
    "error": None,  # last error message
    "finished_at": 0.0,  # time the last attempt ended
}


def _model_file_ok():
    return MODEL_PATH.exists() and MODEL_PATH.stat().st_size > _MIN_MODEL_BYTES


def _download_model():
    """Background thread: fetch model.onnx, resuming a partial file.

    Never raises: failures are recorded in _download_state so the
    next request can retry (after _RETRY_SECONDS). The partial file
    is kept, so a retry resumes instead of starting over.
    """
    try:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        # Up to two tries in this thread: once resuming the partial
        # file, and once from scratch if the server refuses the range
        # (HTTP 416) or ignores it in a way we cannot use.
        for attempt in range(2):
            existing = (
                MODEL_TMP_PATH.stat().st_size if MODEL_TMP_PATH.exists() else 0
            )
            headers = {"User-Agent": "Mozilla/5.0"}
            if existing > 0:
                headers["Range"] = f"bytes={existing}-"
            req = urllib.request.Request(MODEL_URL, headers=headers)
            try:
                resp = urllib.request.urlopen(req, timeout=300)
            except Exception as exc:
                raise RuntimeError(f"could not reach model URL: {exc}") from exc
            with resp:
                status = resp.status
                if status == 416:
                    # Range beyond the end of the file: stale partial.
                    MODEL_TMP_PATH.unlink(missing_ok=True)
                    continue
                if status == 206:
                    mode, downloaded = "ab", existing
                elif status == 200:
                    # Server ignored Range: start over.
                    mode, downloaded = "wb", 0
                else:
                    raise RuntimeError(f"unexpected HTTP status {status}")
                content_len = resp.headers.get("Content-Length")
                total = (
                    (downloaded + int(content_len))
                    if content_len
                    else None
                )
                with _lock:
                    _download_state["total"] = total
                    _download_state["downloaded"] = downloaded
                with open(MODEL_TMP_PATH, mode) as f:
                    while True:
                        chunk = resp.read(1024 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        with _lock:
                            _download_state["downloaded"] = downloaded
            size = MODEL_TMP_PATH.stat().st_size
            if size < _MIN_MODEL_BYTES:
                MODEL_TMP_PATH.unlink(missing_ok=True)
                raise RuntimeError(
                    f"downloaded file too small ({size} bytes) -- "
                    "the model URL may have failed; refusing to install it"
                )
            MODEL_TMP_PATH.replace(MODEL_PATH)
            with _lock:
                _download_state.update(
                    status="done",
                    downloaded=size,
                    total=size,
                    error=None,
                    finished_at=time.time(),
                )
            print(
                f"identifier: model downloaded "
                f"({size / 1e6:.1f} MB)"
            )
            return
        raise RuntimeError("range requests refused twice, giving up")
    except Exception as exc:  # noqa: BLE001 - stay available
        with _lock:
            _download_state.update(
                status="failed", error=str(exc), finished_at=time.time()
            )
        print(f"identifier: model download failed: {exc!r}")


def _ensure_model():
    """Start the background download if the model file is missing.

    Returns True only when a usable model file is already present.
    When it is missing this starts (or keeps) the download thread and
    returns False immediately -- the caller shows the download state
    instead of hanging. Concurrent requests never start a second
    download; a failed download is retried at most once a minute.
    """
    global _download_thread
    if _model_file_ok():
        with _lock:
            _download_state["status"] = "done"
        return True
    with _lock:
        thread = _download_thread
        if thread is not None and thread.is_alive():
            return False
        state = _download_state["status"]
        finished_at = _download_state["finished_at"]
        if state == "failed" and time.time() - finished_at < _RETRY_SECONDS:
            return False
        partial = (
            MODEL_TMP_PATH.stat().st_size if MODEL_TMP_PATH.exists() else 0
        )
        _download_state.update(
            status="downloading", error=None, downloaded=partial
        )
        thread = threading.Thread(
            target=_download_model, name="model-download", daemon=True
        )
        # Start while still holding the lock: otherwise a concurrent
        # request could see the thread assigned but not yet alive and
        # start a second download.
        thread.start()
        _download_thread = thread
    return False


def model_available():
    """True when the downloaded model file and class list are present."""
    if _model_file_ok() and CLASSES_PATH.exists():
        return True
    if not CLASSES_PATH.exists():
        return False
    return _ensure_model()


def download_status():
    """Snapshot of the background download, for the template.

    Keys: status (idle/downloading/done/failed), downloaded (bytes),
    total (bytes or None), error, downloaded_mb / total_mb (rounded,
    for display), model_available.
    """
    with _lock:
        state = dict(_download_state)
    state["model_available"] = _model_file_ok()
    state["downloaded_mb"] = round(state["downloaded"] / 1e6, 1)
    state["total_mb"] = (
        round(state["total"] / 1e6, 1) if state["total"] else None
    )
    return state


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
