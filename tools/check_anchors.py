#!/usr/bin/env python3
"""Verify an anchors file. Exits non-zero unless coverage is complete and clean."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from evalid import anchors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: check_anchors.py <anchors.json> [root]")
    rep = anchors.verify(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(json.dumps(rep.to_dict(), indent=1, default=str))
    print(f"\ncoverage {rep.coverage} verified/defined, {rep.passed} passed")
    sys.exit(0 if rep.clean else 1)
