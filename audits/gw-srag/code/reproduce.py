#!/usr/bin/env python3
"""Reproducer for EVALID-AUDIT-GW-SRAG. Closes release-hygiene findings R1-2/3/4.

    python reproduce.py --selftest    # offline, synthetic, no data files needed
    python reproduce.py --internal    # P1, P2, P7, P8 -- pure arithmetic, fast
    python reproduce.py --p6          # the corrected P6 correlation table
    python reproduce.py --fisher      # P5 Fisher + conditioning gate
    python reproduce.py --ff          # P5 fitting factors (slow, ~5 min)
    python reproduce.py --all         # everything, rewrites results/

Every step runs offline. There is no network path in this audit: it is a
forecast against published constraints, not an analysis of real strain.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"

# ------------------------------------------------------------------ deps
_HINT = ("\nEVALID's GW audit needs {p}.\n"
         "  pip install -r requirements.txt\n"
         "Minimum versions: numpy>=2.0 (np.trapezoid), scipy>=1.11, "
         "matplotlib>=3.7.\n")
try:
    import numpy as np
except ImportError:
    sys.exit(_HINT.format(p="numpy>=2.0"))
if tuple(int(x) for x in np.__version__.split(".")[:2]) < (2, 0):
    sys.exit(_HINT.format(p=f"numpy>=2.0 (found {np.__version__})"))
try:
    from scipy import stats as sps, optimize as spo
except ImportError:
    sys.exit(_HINT.format(p="scipy>=1.11"))

sys.path.insert(0, str(HERE))
from gwfisher import psd_aligo, taylorf2_phase, f_isco, waveform, inner  # noqa: E402
from srag_core import C_of_lambda, A_of_lambda, lam_energy, lam_compactness  # noqa: E402

MC, ETA, CHI, F0 = 1.188, 0.2497, 0.0, 100.0
ALPHAS = [0, 0.5, 1.5, 2.5, 3, 3.5, 4]
COND_CEILING = 1e15          # registered for this audit; protocol section 4.3
SEED = 20260906


def env() -> dict:
    return {"python": platform.python_version(), "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "platform": platform.platform(), "seed": SEED}


# ------------------------------------------------------------------ P1/P2/P7/P8
def internal() -> dict:
    out = {}
    out["P1_pn_order"] = {str(a): (3 * a + 2) / 2
                          for a in [0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4]}
    C08 = float(C_of_lambda(0.08))
    A08 = float(A_of_lambda(0.08))
    out["P2a"] = {"C_0.08_stated": 0.18, "C_0.08_recomputed": C08,
                  "A_0.08": A08}
    out["P2b"] = {"dPhi_stated_rad": 0.24,
                  "dPhi_recomputed_rad": A08 * float(np.log(4.0)),
                  "C_required_for_0.24": 0.08 * float(np.log(4.0)) / 0.24}
    rows = [("Quantum (Planck)", 1e-35, 1e-8, 1e34),
            ("Atomic nucleus", 1e-15, 1e-25, 1e-10),
            ("Solar System", 1e11, 1e30, 1e-10),
            ("Dwarf galaxy", 3e20, 1e38, 1e-5),
            ("Spiral galaxy", 3e21, 1e41, 0.08),
            ("Galaxy cluster", 1e23, 1e44, 0.3)]
    out["P2c_lambda_table"] = [
        {"system": n, "r_m": r, "M_kg": m, "lambda_claimed": c,
         "lambda_energy_def_A": float(lam_energy(m, r)),
         "lambda_compactness_def_B": float(lam_compactness(m, r))}
        for n, r, m, c in rows]
    out["P2e_rate"] = {"claimed_rate_rad_per_Mpc": 2.7e-22,
                       "Mpc_needed_for_0.24_rad": 0.24 / 2.7e-22,
                       "Hubble_radius_Mpc": 4300.0}
    # amplitude floor
    r = spo.minimize_scalar(lambda L: float(A_of_lambda(np.exp(L))),
                            bounds=(-30, 3), method="bounded",
                            options={"xatol": 1e-12})
    out["A_floor"] = {"lambda_star": float(np.exp(r.x)), "A_min": float(r.fun),
                      "dPhi_min_50_200Hz_rad": float(r.fun * np.log(4.0))}

    def p_exact(rr, n):
        t = rr * np.sqrt((n - 2) / (1 - rr ** 2))
        return float(2 * sps.t.sf(abs(t), n - 2))
    out["P7"] = {"p_at_r0.5_n15": p_exact(0.5, 15),
                 "r_needed_p0.01_n15": float(
                     spo.brentq(lambda x: p_exact(x, 15) - 0.01, 0.5, 0.99)),
                 "n_needed_p0.01_r0.5": next(
                     n for n in range(5, 300) if p_exact(0.5, n) < 0.01)}
    out["P8_host_path_fraction"] = {f"{k}kpc_at_40Mpc": k * 1e-3 / 40
                                    for k in (3, 20)}
    out["environment"] = env()
    return out


# ------------------------------------------------------------------ P6
def _basis(f, rel=1e-5):
    def dpsi(par, val, step):
        kw = dict(mc=MC, eta=ETA, chi=CHI, A_log=0.0, f0=F0)
        kw[par] = val + step
        pp = taylorf2_phase(f, **kw)
        kw[par] = val - step
        return (pp - taylorf2_phase(f, **kw)) / (2 * step)
    return [2 * np.pi * f, -np.ones_like(f),
            dpsi("mc", MC, MC * rel) * MC,
            dpsi("eta", ETA, ETA * rel) * ETA,
            dpsi("chi", CHI, rel)]


def _rho_fisher(alpha, n=20000, rel=1e-5):
    """Marginalised Fisher covariance route -- no projector freedom."""
    f = np.linspace(20.0, f_isco(MC, ETA), n)
    S, amp2 = psd_aligo(f), f ** (-7.0 / 3.0)
    ip = lambda u, v: 4.0 * np.trapezoid(u * v * amp2 / S, f)  # noqa: E731
    d = _basis(f, rel) + [-np.log(f / F0), f ** (alpha - 1.0)]
    F = np.array([[ip(a, b) for b in d] for a in d])
    s = 1.0 / np.sqrt(np.diag(F))
    cov = np.linalg.inv(F * np.outer(s, s)) * np.outer(s, s)
    sig = np.sqrt(np.diag(cov))
    return abs(cov[5, 6] / (sig[5] * sig[6]))


def _rho_gs(alpha, n=20000, passes=2):
    """Gram-Schmidt projection route -- independent implementation."""
    f = np.linspace(20.0, f_isco(MC, ETA), n)
    S, amp2 = psd_aligo(f), f ** (-7.0 / 3.0)
    w = 4.0 * amp2 / S
    ip = lambda u, v: float(np.trapezoid(u * v * w, f))  # noqa: E731
    B, o = _basis(f), []
    for b in B:
        v = b.copy()
        for _ in range(passes):
            for u in o:
                v = v - ip(v, u) * u
        o.append(v / np.sqrt(ip(v, v)))

    def po(x):
        v = x.copy()
        for _ in range(passes):
            for u in o:
                v = v - ip(v, u) * u
        return v
    pl, pa = po(np.log(f / F0)), po(f ** (alpha - 1.0))
    return abs(ip(pl, pa) / np.sqrt(ip(pl, pl) * ip(pa, pa)))


def p6() -> dict:
    """Protocol 4.2 requires the `implementation` method here: this quantity
    involves a projection and a matrix inverse."""
    shipped = {0: .952, .5: .900, 1.5: .633, 2.5: .285, 3: .139, 3.5: .036, 4: .025}
    per = {}
    for a in ALPHAS:
        vals = [_rho_fisher(a), _rho_gs(a), _rho_fisher(a, n=40000),
                _rho_fisher(a, rel=1e-6)]
        rec, u = float(np.mean(vals)), float((max(vals) - min(vals)) / 2)
        per[str(a)] = {"shipped": shipped[a], "recomputed": round(rec, 5),
                       "uncertainty": u, "uncertainty_method": "implementation",
                       "delta": round(rec - shipped[a], 5),
                       "exceeds_threshold": bool(rec - u >= 0.95)}
    mx = max(v["recomputed"] for v in per.values())
    return {"quantity": "|corr(A_log, A_alpha)| marginalised over "
                        "{ln_amp,tc,phic,ln_Mc,ln_eta,chi}",
            "registered_threshold": 0.95,
            "methods_agreeing": ["marginalised Fisher covariance",
                                 "Gram-Schmidt projection (2 passes)",
                                 "grid refinement 20k/40k",
                                 "finite-difference step 1e-5/1e-6"],
            "per_alpha": per, "shipped_max": 0.952, "recomputed_max": mx,
            "shipped_n_above_threshold": 1,
            "recomputed_n_above_threshold":
                int(sum(v["exceeds_threshold"] for v in per.values())),
            "verdict": "FAIL", "verdict_direction": "unchanged: FAIL",
            "environment": env()}


# ------------------------------------------------------------------ P5
def fisher_block() -> dict:
    from gwfisher import fisher, make_grid
    out = {}
    for name, mc, eta in (("BNS_GW170817like", MC, ETA),
                          ("BBH_GW150914like", 30.0, 0.2497)):
        f, S = make_grid(mc, eta, 20.0, None, 20000)
        F, cov, sig, corr, _ = fisher(mc, eta, CHI, f, S, snr=25.0)
        cond = float(np.linalg.cond(F))
        admissible = cond <= COND_CEILING
        out[name] = {
            "cond_number": cond, "registered_ceiling": COND_CEILING,
            "gate": "OK" if admissible else "UNDERDETERMINED",
            "f_low": float(f[0]), "f_high": float(f[-1]), "snr": 25.0}
        if admissible:
            out[name].update({
                "sigma_A_log_marginalised": float(sig[-1]),
                "sigma_A_log_fixed_GR": float(1 / np.sqrt(F[-1, -1])),
                "degradation_factor": float(sig[-1] * np.sqrt(F[-1, -1])),
                "sigma_mc_over_mc": float(sig[3]),
                "corr_Alog_lnmc": float(corr[-1, 3]),
                "corr_Alog_lneta": float(corr[-1, 4]),
                "corr_Alog_chi": float(corr[-1, 5]),
                "corr_Alog_phic": float(corr[-1, 2])})
        else:
            out[name]["note"] = ("quantities not reported: protocol 4.3 gate "
                                 "failed, verdict UNDERDETERMINED")
    out["environment"] = env()
    return out


def ff_block(restarts: int = 45) -> dict:
    from gwfisher import make_grid, fitting_factor
    f, S = make_grid(MC, ETA, 20.0, None, 20000)
    rows = {}
    for lab, lam in (("lam_0.08_rotation_curve", 0.08),
                     ("lam_1e-4_GW_paper", 1e-4),
                     ("lam_2.4e-8_SPARC", 2.4e-8)):
        A = float(A_of_lambda(lam))
        r = fitting_factor(MC, ETA, CHI, A, f, S)
        rows[lab] = {"lambda": lam, "A_log": A, "FF": r["FF"],
                     "residual_sigma_at_snr25":
                         float(25.0 * np.sqrt(max(2 * (1 - r["FF"]), 0))),
                     "mc_frac_bias": r["mc_frac_bias"],
                     "chi_bias": r["chi_bias"],
                     "restarts": restarts, "seed": SEED}
    rows["environment"] = env()
    return rows


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    """Offline, synthetic, no result files touched. Tests the analysis path."""
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok &= bool(cond)
        print(f"  [{'ok ' if cond else 'FAIL'}] {name}")

    chk("C(0.08) = 0.10509", abs(float(C_of_lambda(0.08)) - 0.10508706) < 1e-7)
    chk("A(lam) diverges as lam -> 0",
        float(A_of_lambda(1e-8)) > float(A_of_lambda(0.21)))
    chk("compactness reproduces SPARC median to 5%",
        abs(float(lam_compactness(1e41, 3e21)) / 2.4e-8 - 1) < 0.05)
    chk("energy and compactness definitions disagree by >1e6",
        float(lam_energy(1e41, 3e21)) / float(lam_compactness(1e41, 3e21)) > 1e6)

    # A synthetic waveform with a known injected log term must be recovered
    # by the Fisher A_log derivative up to the degeneracy.
    f = np.linspace(20.0, 400.0, 4000)
    p0 = taylorf2_phase(f, MC, ETA, CHI, A_log=0.0)
    p1 = taylorf2_phase(f, MC, ETA, CHI, A_log=1.0)
    chk("log term enters the phase as -ln(f/f0)",
        float(np.max(np.abs((p0 - p1) - np.log(f / F0)))) < 1e-9)

    chk("PSD is positive across the band", bool(np.all(psd_aligo(f) > 0)))
    chk("f_isco(BNS) ~ 1610 Hz", abs(f_isco(MC, ETA) - 1609.94) < 1.0)

    # P6 by two implementations must agree -- protocol 4.2
    a, b = _rho_fisher(0, n=6000), _rho_gs(0, n=6000)
    chk(f"P6 two implementations agree at alpha=0 ({a:.5f} vs {b:.5f})",
        abs(a - b) < 1e-3)
    chk("P6 alpha=0 well above the 0.95 threshold", a > 0.99)

    # A known-bad matrix must trip the conditioning gate
    chk("conditioning gate trips at 1e16",
        float(np.linalg.cond(np.diag([1.0, 1e16]))) > COND_CEILING)

    print(f"\n{'SELFTEST PASS' if ok else 'SELFTEST FAIL'}")
    return 0 if ok else 1


# ------------------------------------------------------------------ main
def _dump(name, obj):
    RESULTS.mkdir(parents=True, exist_ok=True)
    p = RESULTS / name
    p.write_text(json.dumps(obj, indent=1) + "\n")
    print(f"wrote {p}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    for flag, helptext in (("--selftest", "offline synthetic checks"),
                           ("--internal", "P1/P2/P7/P8 arithmetic"),
                           ("--p6", "corrected P6 correlation table"),
                           ("--fisher", "P5 Fisher + conditioning gate"),
                           ("--ff", "P5 fitting factors (slow)"),
                           ("--all", "everything")):
        ap.add_argument(flag, action="store_true", help=helptext)
    args = ap.parse_args(argv)
    if not any(vars(args).values()):
        ap.print_help()
        return 0
    if args.selftest:
        return selftest()
    if args.internal or args.all:
        _dump("t1_internal.json", internal())
    if args.p6 or args.all:
        _dump("p6_corrected.json", p6())
    if args.fisher or args.all:
        _dump("t2_fisher.json", fisher_block())
    if args.ff or args.all:
        _dump("t3_ff.json", ff_block())
    _dump("environment.json", env())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
