"""Anchor verification -- protocol section 5.1.

An anchor binds a number printed in a report to the file and location it was
read from, and re-reads it independently. Coverage is reported as
verified/defined, where `defined` is the number of entries in the anchors
file. "29/29 passed" against a file holding 38 entries is a true sentence that
creates a false impression; this module makes that impossible to write.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_TOLERANCE = 1e-9

_TOKEN = re.compile(
    r"""\[(-?\d+)\]                 # [0]  list index
      | \['([^']*)'\]               # ['key with . in it']
      | \["([^"]*)"\]               # ["key with . in it"]
      | \.?([^.\[\]]+)              # .key
    """,
    re.VERBOSE,
)


def read_json_path(doc, path: str):
    """Minimal JSONPath: `$.a.b[0].c`, plus `$['key.with.dots']`.

    Keys that themselves contain a dot -- alpha values like "0.5", version
    strings -- must use the bracket form, or the dotted form will split them.
    """
    if not path.startswith("$"):
        raise ValueError(f"json_path must start with '$': {path!r}")
    cur = doc
    pos, tail = 0, path[1:]
    for m in _TOKEN.finditer(tail):
        if m.start() != pos:
            raise ValueError(f"unparsable json_path near {tail[pos:]!r} in {path!r}")
        pos = m.end()
        idx, q1, q2, key = m.groups()
        if idx is not None:
            cur = cur[int(idx)]
        else:
            k = q1 if q1 is not None else (q2 if q2 is not None else key)
            if isinstance(cur, list):
                cur = cur[int(k)]
            else:
                cur = cur[k]
    if pos != len(tail):
        raise ValueError(f"unparsable json_path tail {tail[pos:]!r} in {path!r}")
    return cur


@dataclass
class AnchorResult:
    id: str
    claimed: object
    recomputed: object
    ok: bool
    detail: str = ""


@dataclass
class AnchorReport:
    defined: int
    verified: int
    passed: int
    results: list = field(default_factory=list)

    @property
    def coverage(self) -> str:
        return f"{self.verified}/{self.defined}"

    @property
    def clean(self) -> bool:
        return self.defined == self.verified == self.passed

    def to_dict(self) -> dict:
        return {
            "anchors_defined": self.defined,
            "anchors_verified": self.verified,
            "anchors_passed": self.passed,
            "coverage": self.coverage,
            "clean": self.clean,
            "mismatches": [r.id for r in self.results if not r.ok],
            "results": [vars(r) for r in self.results],
        }


def _close(a, b, tol) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) == bool(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y, tol) for x, y in zip(a, b))
    return a == b


def verify(anchors_file: str | Path, root: str | Path | None = None) -> AnchorReport:
    """Verify every anchor in `anchors_file` against its bound source.

    Each anchor needs `id`, `claimed`, and a `source` of
    {"file": <path relative to root>, "json_path": "$..."}.
    An anchor with no source is counted as defined but NOT verified -- which is
    exactly the distinction the coverage string exists to expose.
    """
    anchors_file = Path(anchors_file)
    root = Path(root) if root else anchors_file.parent
    spec = json.loads(anchors_file.read_text())
    entries = spec["anchors"] if isinstance(spec, dict) and "anchors" in spec else spec
    if isinstance(entries, dict):
        entries = [{"id": k, **v} for k, v in entries.items()]

    cache: dict[Path, object] = {}
    results, verified, passed = [], 0, 0

    for e in entries:
        aid = str(e.get("id", "<unnamed>"))
        claimed = e.get("claimed")
        src = e.get("source")
        if not src:
            results.append(AnchorResult(aid, claimed, None, False,
                                        "no source binding (protocol 5.1)"))
            continue
        fp = (root / src["file"]).resolve()
        if not fp.exists():
            results.append(AnchorResult(aid, claimed, None, False,
                                        f"source file missing: {src['file']}"))
            continue
        if fp not in cache:
            cache[fp] = json.loads(fp.read_text())
        try:
            got = read_json_path(cache[fp], src["json_path"])
        except (KeyError, IndexError, TypeError) as exc:
            results.append(AnchorResult(aid, claimed, None, False,
                                        f"json_path failed: {exc}"))
            continue
        verified += 1
        tol = float(e.get("tolerance", DEFAULT_TOLERANCE))
        ok = _close(claimed, got, tol)
        passed += ok
        results.append(AnchorResult(aid, claimed, got, ok,
                                    "" if ok else "claimed != recomputed"))

    return AnchorReport(defined=len(entries), verified=verified,
                        passed=passed, results=results)
