"""SHA-256 release manifest -- protocol section 6.1.

No result file may exist outside the manifest. A second, unhashed source of
truth sitting beside a hashed one is finding R2-10 against MMLU Audit 002, and
this module exists to make that state detectable.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", ".pytest_cache",
             ".venv", "venv", "node_modules", ".mypy_cache"}
SKIP_NAMES = {"manifest.json", ".DS_Store"}


def sha256(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while block := fh.read(chunk):
            h.update(block)
    return h.hexdigest()


def _walk(root: Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if p.name in SKIP_NAMES or p.name.startswith("._"):
            continue
        if SKIP_DIRS & set(p.relative_to(root).parts):
            continue
        yield p


def build(root: str | Path) -> dict:
    """Hash every shippable file under `root`, keyed by relative POSIX path."""
    root = Path(root).resolve()
    return {str(p.relative_to(root).as_posix()): sha256(p) for p in _walk(root)}


def write(root: str | Path, out: str | Path | None = None) -> Path:
    root = Path(root).resolve()
    out = Path(out) if out else root / "manifest.json"
    out.write_text(json.dumps(build(root), indent=1, sort_keys=True) + "\n")
    return out


def verify(root: str | Path, manifest_file: str | Path | None = None) -> dict:
    """Compare the tree against the manifest.

    Returns {ok, changed, missing, unhashed}. `unhashed` is the important one:
    a shipped file that no hash covers.
    """
    root = Path(root).resolve()
    mf = Path(manifest_file) if manifest_file else root / "manifest.json"
    recorded = json.loads(mf.read_text())
    actual = build(root)
    changed = sorted(k for k in recorded if k in actual and recorded[k] != actual[k])
    missing = sorted(k for k in recorded if k not in actual)
    unhashed = sorted(k for k in actual if k not in recorded)
    return {"ok": not (changed or missing or unhashed), "changed": changed,
            "missing": missing, "unhashed": unhashed,
            "files_hashed": len(recorded)}
