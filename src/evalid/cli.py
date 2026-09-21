"""Command-line interface -- closes release-hygiene finding R1-2.

    evalid manifest build  <dir>
    evalid manifest verify <dir>
    evalid anchors  verify <anchors.json> [--root DIR]
    evalid conform         <dir>
    evalid corrections     <CORRECTIONS.csv> [--write DIR]
    evalid selftest
    evalid version
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import (__version__, anchors as anchors_mod, corrections as corr_mod,
               manifest as manifest_mod)
from .verdicts import PROTOCOL_VERSION


def _p(*a):
    try:
        print(*a, file=sys.stdout)
    except BrokenPipeError:          # piped into head/less; not an error
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)


# --------------------------------------------------------------------- conform
CONFORM_FILES = {
    "pre-registration": ("PREREGISTRATION.md", "PREREGISTRATION_*.md"),
    "report": ("REPORT.md", "AUDIT_REPORT.md"),
    "manifest": ("manifest.json",),
    "anchors": ("anchors.json",),
    "reproducer": ("reproduce.py", "code/reproduce.py"),
}


def cmd_conform(args) -> int:
    root = Path(args.dir).resolve()
    _p(f"EVALID protocol {PROTOCOL_VERSION} / package {__version__} -- {root}\n")
    fails = 0

    for label, names in CONFORM_FILES.items():
        hit = next((n for n in names
                    if list(root.glob(n))), None)
        ok = hit is not None
        fails += not ok
        _p(f"  [{'ok ' if ok else 'MISS'}] {label:<18} {hit or names[0]}")

    mf = root / "manifest.json"
    if mf.exists():
        res = manifest_mod.verify(root)
        ok = res["ok"]
        fails += not ok
        _p(f"\n  [{'ok ' if ok else 'FAIL'}] manifest covers {res['files_hashed']} files")
        for k in ("changed", "missing", "unhashed"):
            for f in res[k][:10]:
                _p(f"          {k}: {f}")

    af = root / "anchors.json"
    if af.exists():
        rep = anchors_mod.verify(af, root)
        fails += not rep.clean
        _p(f"\n  [{'ok ' if rep.clean else 'FAIL'}] anchors "
           f"{rep.passed} passed / {rep.coverage} verified/defined")
        for r in rep.results:
            if not r.ok:
                _p(f"          {r.id}: {r.detail} "
                   f"(claimed {r.claimed!r}, got {r.recomputed!r})")

    _p("\n  Mechanical checks only. The judgement items in protocol section 8 "
       "-- sidedness,\n  unit consistency, disclosure, prior art -- are not "
       "checkable by a program.")
    _p(f"\n{'PASS' if not fails else f'{fails} PROBLEM(S)'}")
    return 0 if not fails else 1


def cmd_manifest(args) -> int:
    root = Path(args.dir).resolve()
    if args.action == "build":
        out = manifest_mod.write(root)
        _p(f"wrote {out} ({len(json.loads(out.read_text()))} files)")
        return 0
    res = manifest_mod.verify(root)
    _p(json.dumps(res, indent=1))
    return 0 if res["ok"] else 1


def cmd_anchors(args) -> int:
    rep = anchors_mod.verify(args.anchors, args.root)
    _p(json.dumps(rep.to_dict(), indent=1, default=str))
    _p(f"\ncoverage {rep.coverage} verified/defined, {rep.passed} passed")
    if not rep.clean:
        _p("NOT CLEAN -- do not publish (protocol 5.1)")
    return 0 if rep.clean else 1


def cmd_corrections(args) -> int:
    """Derive the correction counts from the log, so prose cannot drift."""
    s = corr_mod.summarise(args.csv)
    _p(json.dumps(s.to_dict(), indent=1))
    if args.write:
        d = Path(args.write)
        d.mkdir(parents=True, exist_ok=True)
        (d / "CORRECTIONS.md").write_text(corr_mod.render_markdown(args.csv))
        corr_mod.write_summary(args.csv, d / "corrections_summary.json")
        _p(f"\nwrote {d/'CORRECTIONS.md'} and {d/'corrections_summary.json'}")
    if s.unresolved_provenance:
        _p(f"\nNOTE: {s.unresolved_provenance} entries have finder_kind "
           "'external-unspecified'.\nThe external-finder ratio is not a quotable "
           "claim about human review until\nthe author resolves them.")
    return 0


def cmd_selftest(args) -> int:
    """Offline self-test of the protocol machinery. No network, no data files."""
    from .stats import (threshold_verdict, benjamini_hochberg, condition_gate,
                        uncertainty_from_spread, cluster_bootstrap_ci)
    from ._deps import np
    from .verdicts import check_prediction, VerdictError
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok &= bool(cond)
        _p(f"  [{'ok ' if cond else 'FAIL'}] {name}")

    # The P6 case that motivated protocol 4: 0.952 vs 0.95 with u = 0.048.
    r = threshold_verdict(0.952, 0.95, uncertainty=0.048,
                          method="implementation", direction="above")
    chk("0.952 vs 0.95 with u=0.048 -> INDETERMINATE",
        r.verdict == "INDETERMINATE")
    r2 = threshold_verdict(0.99895, 0.95, uncertainty=0.0001,
                           method="implementation", direction="above")
    chk("0.99895 vs 0.95 with u=1e-4 -> FAIL", r2.verdict == "FAIL")
    chk("margin reported in sigma", r2.margin_in_sigma > 100)

    try:
        threshold_verdict(0.5, 0.4, uncertainty=-1, method="grid")
        chk("negative uncertainty rejected", False)
    except ValueError:
        chk("negative uncertainty rejected", True)

    try:
        threshold_verdict(0.5, 0.4, uncertainty=0.01, method="vibes")
        chk("unknown uncertainty method rejected", False)
    except ValueError:
        chk("unknown uncertainty method rejected", True)

    chk("half-range spread", abs(uncertainty_from_spread([0.9, 1.1]) - 0.1) < 1e-12)

    rej, adj = benjamini_hochberg([0.001, 0.02, 0.5, 0.9], q=0.05)
    chk("BH rejects the two smallest", rej.tolist() == [True, True, False, False])
    chk("BH adjusted p monotone", bool(np.all(np.diff(np.sort(adj)) >= -1e-12)))

    st, cond = condition_gate(np.diag([1.0, 1e15]), ceiling=1e12)
    chk("conditioning gate -> UNDERDETERMINED", st == "UNDERDETERMINED")
    st2, _ = condition_gate(np.eye(3), ceiling=1e12)
    chk("well-conditioned -> OK", st2 == "OK")

    rng = np.random.default_rng(0)
    vals = rng.normal(size=200)
    clus = np.repeat(np.arange(20), 10)
    m, lo, hi = cluster_bootstrap_ci(vals, clus, n_boot=200, seed=1)
    chk("cluster bootstrap brackets the mean", lo <= m <= hi)
    m2, lo2, hi2 = cluster_bootstrap_ci(vals, clus, n_boot=200, seed=1)
    chk("cluster bootstrap is seeded/deterministic", (lo, hi) == (lo2, hi2))

    try:
        check_prediction("CRITERION INVALID")
        chk("deprecated verdict rejected", False)
    except VerdictError as e:
        chk("deprecated verdict rejected, names replacement",
            "REGISTERED_INVALID" in str(e))

    from . import corrections as _c
    try:
        _c.load.__doc__
        chk("correction log schema is enforced", "finder_kind" in _c.REQUIRED_COLUMNS)
        chk("finder kinds include external-ai", "external-ai" in _c.FINDER_KINDS)
    except Exception:
        chk("corrections module importable", False)

    _p(f"\n{'SELFTEST PASS' if ok else 'SELFTEST FAIL'}")
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="evalid", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("manifest", help="build or verify a SHA-256 manifest")
    m.add_argument("action", choices=["build", "verify"])
    m.add_argument("dir")
    m.set_defaults(func=cmd_manifest)

    a = sub.add_parser("anchors", help="verify claimed vs recomputed anchors")
    a.add_argument("action", choices=["verify"])
    a.add_argument("anchors")
    a.add_argument("--root", default=None)
    a.set_defaults(func=cmd_anchors)

    c = sub.add_parser("conform", help="check an audit package against protocol 8")
    c.add_argument("dir")
    c.set_defaults(func=cmd_conform)

    x = sub.add_parser("corrections", help="derive counts from the correction log")
    x.add_argument("csv")
    x.add_argument("--write", default=None,
                   help="regenerate CORRECTIONS.md and corrections_summary.json here")
    x.set_defaults(func=cmd_corrections)

    s = sub.add_parser("selftest", help="offline self-test of the machinery")
    s.set_defaults(func=cmd_selftest)

    v = sub.add_parser("version")
    v.set_defaults(func=lambda _: (_p(f"evalid {__version__} "
                                      f"(protocol {PROTOCOL_VERSION})"), 0)[1])

    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
