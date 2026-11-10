"""Download the bird ID model files (ONNX) for the Render build.

The v2 model is two files, neither committed (GitHub blocks files
over 100 MB and the API tooling caps arg size):
- model.onnx (1.2 MB graph)
- model.onnx.data (200 MB weights, external-data format)
This command fetches both from the public Hugging Face model repo
yawarnazir/kashmir-birds-v2-onnx into website/birds/model/.
Run by render.yaml on every deploy, skipped when files exist.

The Hugging Face resolve URLs work without authentication
for a public repo (verified 2026-11-02).

Best-effort on purpose: this command NEVER fails the build. If the
download fails here, the command warns and exits 0, the deploy goes
ahead, and the site fetches the files at runtime instead (see
birds/identifier.py -- background download thread with resume).
Missing model files must never block a deploy.
"""

import hashlib
import os
import tempfile
import urllib.request
from pathlib import Path

from django.core.management.base import BaseCommand

_HF_REPO = "yawarnazir/kashmir-birds-v2-onnx"
# Pinned Hugging Face revision (the main-branch commit of 2026-11-02)
# and the SHA-256 hashes of the two model files at that revision.
# The hashes were verified by downloading both files and hashing them
# (2026-11-10). Pinning stops the build silently fetching different
# weights if the "main" branch of the model repo ever changes, and
# the hash check stops a corrupted download from being installed.
_HF_REVISION = "aee59c1b33d9f1b9d5c0cf0134d38f33863048c7"
FILES = [
    # (filename, min_bytes, env_var, sha256)
    (
        "model.onnx",
        100_000,
        "MODEL_DOWNLOAD_URL",
        "962ee8c244df88b6b402de8c47100bb458adaf05e89ab9876d6283e419c6b663",
    ),
    (
        "model.onnx.data",
        100_000_000,
        "MODEL_DATA_DOWNLOAD_URL",
        "d3555db212cbb8c68efeb1132167c3ed7f45d61edd3841eb08daaaf325edc9a8",
    ),
]
MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "model"


def _sha256(path):
    """SHA-256 of a file, streamed so the 200 MB weights file is safe."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


class Command(BaseCommand):
    help = "Download v2 model files into website/birds/model/ if missing."

    def handle(self, *args, **options):
        try:
            self._download()
        except Exception as exc:  # noqa: BLE001 - never fail the build
            self.stdout.write(
                "WARNING: model download failed during build "
                f"({exc!r}). Deploy continues; the site will download "
                "the model at runtime on first request "
                "(see birds/identifier.py)."
            )

    def _download(self):
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        for filename, min_bytes, env_var, expected_sha256 in FILES:
            dest = MODEL_DIR / filename
            if dest.exists() and dest.stat().st_size > min_bytes:
                self.stdout.write(
                    f"{filename} already present "
                    f"({dest.stat().st_size / 1e6:.1f} MB)"
                )
                continue
            url = os.environ.get(
                env_var,
                f"https://huggingface.co/{_HF_REPO}/resolve/{_HF_REVISION}/{filename}",
            )
            self.stdout.write(f"downloading {filename} from {url}")
            with tempfile.TemporaryDirectory(dir=MODEL_DIR) as tmp:
                tmp_path = Path(tmp) / "download"
                req = urllib.request.Request(
                    url, headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=900) as resp, open(
                    tmp_path, "wb"
                ) as f:
                    while True:
                        chunk = resp.read(1024 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                if tmp_path.stat().st_size < min_bytes:
                    raise RuntimeError(
                        f"{filename} download too small "
                        f"({tmp_path.stat().st_size} bytes)"
                    )
                digest = _sha256(tmp_path)
                if digest != expected_sha256:
                    raise RuntimeError(
                        f"{filename} download failed its SHA-256 check "
                        f"(got {digest})"
                    )
                tmp_path.replace(dest)
            self.stdout.write(
                f"{filename} installed ({dest.stat().st_size / 1e6:.1f} MB)"
            )
