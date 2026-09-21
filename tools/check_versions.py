#!/usr/bin/env python3
"""Fail if the version strings disagree, or disagree with the current git tag.

A release where pyproject says one version, the protocol constant says another
and the tag says a third has happened twice in this repository's short history.
This makes it a CI failure instead of a reader's discovery.
"""
import re, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
def grab(path, pat):
    m = re.search(pat, (R / path).read_text(), re.M)
    return m.group(1) if m else None

found = {
    "pyproject.toml":          grab("pyproject.toml", r'^version = "([^"]+)"'),
    "CITATION.cff":            grab("CITATION.cff", r"^version: (.+)$"),
    "src/evalid/__init__.py":  grab("src/evalid/__init__.py", r'^__version__ = "([^"]+)"'),
    ".zenodo.json":            grab(".zenodo.json", r'"version": "([^"]+)"'),
}
proto = grab("src/evalid/verdicts.py", r'^PROTOCOL_VERSION = "([^"]+)"')
spec = sorted(p.name for p in (R / "protocol").glob("EVALID_v*.md"))

bad = 0
vals = set(v for v in found.values() if v)
print("package version strings:")
for k, v in found.items():
    print(f"  {k:26s} {v}")
if len(vals) != 1:
    print(f"  MISMATCH: {sorted(vals)}"); bad += 1

print(f"\nprotocol constant           {proto}")
print(f"protocol spec file(s)       {spec}")
if not spec or f"EVALID_v{proto}.md" not in spec:
    print(f"  MISMATCH: constant {proto} has no matching spec file"); bad += 1

try:
    tag = subprocess.run(["git", "describe", "--tags", "--exact-match"],
                         cwd=R, capture_output=True, text=True).stdout.strip()
except Exception:
    tag = ""
if tag:
    print(f"\ngit tag at HEAD             {tag}")
    if tag.lstrip("v") not in vals:
        print(f"  MISMATCH: tag {tag} not among {sorted(vals)}"); bad += 1
else:
    print("\ngit tag at HEAD             (none - not a tagged commit)")

print("\n" + ("PASS" if not bad else f"{bad} MISMATCH(ES)"))
sys.exit(0 if not bad else 1)
