#!/usr/bin/env python3
"""Build a SHA-256 manifest for an audit package. Thin wrapper over the library."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from evalid import manifest

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print("wrote", manifest.write(root))
