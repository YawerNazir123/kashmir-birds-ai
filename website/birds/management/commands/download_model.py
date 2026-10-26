"""Download the bird ID model (ONNX) for the Render build.

The model file (model.onnx, ~57 MB, fp16) is too large to push through
the GitHub tooling, so it is NOT committed to the repo. This command
fetches it from the public Kaggle dataset yawarnazir/kashmir-birds-model-onnx
and places it in website/birds/model/model.onnx, next to the committed
classes.json. Run by render.yaml on every deploy, and skipped when the
file is already there.

The Kaggle single-file download endpoint works without authentication
for a public dataset (verified 2026-10-26). A zip URL also works: if
MODEL_DOWNLOAD_URL points at a zip, model.onnx is extracted from it.
"""

import os
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from django.core.management.base import BaseCommand

DEFAULT_URL = (
    "https://www.kaggle.com/api/v1/datasets/download/"
    "yawarnazir/kashmir-birds-model-onnx/model.onnx"
)
# The single-file endpoint works without authentication for this
# public dataset (verified 2026-10-26: byte-identical download).
# The whole-dataset zip endpoint does not work unauthenticated.
MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "model"
MODEL_PATH = MODEL_DIR / "model.onnx"
MIN_BYTES = 10_000_000  # sanity check: a real model is ~57 MB


class Command(BaseCommand):
    help = "Download model.onnx into website/birds/model/ if missing."

    def handle(self, *args, **options):
        if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > MIN_BYTES:
            self.stdout.write(
                f"model already present: {MODEL_PATH} "
                f"({MODEL_PATH.stat().st_size / 1e6:.1f} MB)"
            )
            return
        url = os.environ.get("MODEL_DOWNLOAD_URL", DEFAULT_URL)
        self.stdout.write(f"downloading model from {url}")
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp) / "model-download"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=600) as resp, open(
                tmp_path, "wb"
            ) as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
            if tmp_path.stat().st_size < MIN_BYTES:
                raise RuntimeError(
                    f"download too small ({tmp_path.stat().st_size} bytes) "
                    f"-- the model URL may have failed; refusing to install it"
                )
            if url.endswith(".onnx"):
                tmp_path.replace(MODEL_PATH)
            else:
                with zipfile.ZipFile(tmp_path) as zf:
                    names = [n for n in zf.namelist() if n.endswith("model.onnx")]
                    if not names:
                        raise RuntimeError(
                            f"no model.onnx inside downloaded zip; contents: "
                            f"{zf.namelist()}"
                        )
                    with zf.open(names[0]) as src, open(MODEL_PATH, "wb") as dst:
                        while True:
                            chunk = src.read(1024 * 1024)
                            if not chunk:
                                break
                            dst.write(chunk)
        size = MODEL_PATH.stat().st_size
        if size < MIN_BYTES:
            MODEL_PATH.unlink(missing_ok=True)
            raise RuntimeError(f"extracted model too small ({size} bytes)")
        self.stdout.write(
            f"model installed: {MODEL_PATH} ({size / 1e6:.1f} MB)"
        )
