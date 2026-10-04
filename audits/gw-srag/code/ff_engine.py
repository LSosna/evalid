"""Fitting-factor engine for the GW-SRAG audit.

Split out of reproduce.py so that t3_ff.json, t4_rest.json and t5_derived.json
are produced by shipped code rather than existing as archival orphans
(release-hygiene finding, v0.3.4).

Determinism: the ladder is solved in increasing A with warm starts, and each
point additionally runs a fixed, seeded set of perturbed restarts. The achieved
spread across restarts is recorded per point, so "a global optimum is not
proven" is a statement with a number behind it.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from gwfisher import waveform, inner

SEED = 20260906
N_RESTARTS = 5
MC, ETA, CHI, F0 = 1.188, 0.2497, 0.0, 100.0


def _eta_logit(eta: float) -> float:
    x = eta / 0.25
    return float(np.log(x / (1.0 - x + 1e-12)))


def fitting_factor(A_log: float, f, S, x0=None, mc=MC, eta=ETA, chi=CHI,
                   f0=F0, n_restarts: int = N_RESTARTS, seed: int = SEED):
    """Maximise a GR-only template against a log-dispersed injection.

    eta is bounded below 0.25 and |chi| <= 1 by construction, so the template
    cannot absorb the deviation by leaving the physical region. phi_c is
    maximised analytically via the modulus of the complex overlap.

    Returns dict with FF, the recovered (biased) GR parameters, the restart
    count, and the spread of achieved optima across restarts.
    """
    hs = waveform(f, mc, eta, chi, A_log, f0)
    ns = np.sqrt(inner(hs, hs, f, S))

    def neg_overlap(x):
        lmc, el, cl, tc = x
        m_ = np.exp(lmc)
        e_ = 0.25 / (1.0 + np.exp(-el))
        c_ = np.tanh(cl)
        ht = waveform(f, m_, e_, c_, 0.0, f0, tc=tc)
        nt = np.sqrt(inner(ht, ht, f, S))
        z = 4.0 * np.trapezoid(hs * np.conj(ht) / S, f)
        return -abs(z) / (ns * nt)

    base = np.array(x0 if x0 is not None
                    else [np.log(mc), _eta_logit(eta),
                          np.arctanh(np.clip(chi, -0.999, 0.999)), 0.0],
                    dtype=float)

    rng = np.random.default_rng(seed + int(round(A_log * 1e6)))
    starts = [base]
    # tight, physically-scaled perturbations: wide jumps in the chi logit
    # send Nelder-Mead wandering without improving the optimum.
    scales = np.array([2e-4, 5e-2, 5e-2, 1e-3])
    for _ in range(n_restarts - 1):
        starts.append(base + scales * rng.normal(size=4))

    best, achieved = None, []
    for s in starts:
        r = minimize(neg_overlap, s, method="Nelder-Mead",
                     options=dict(maxiter=8000, xatol=1e-11, fatol=1e-13))
        achieved.append(-r.fun)
        if best is None or r.fun < best.fun:
            best = r

    lmc, el, cl, tc = best.x
    mc_r = float(np.exp(lmc))
    eta_r = float(0.25 / (1.0 + np.exp(-el)))
    chi_r = float(np.tanh(cl))
    ach = np.asarray(achieved, dtype=float)
    return {
        "FF": float(-best.fun),
        "mc_rec": mc_r, "eta_rec": eta_r, "chi_rec": chi_r, "tc_rec": float(tc),
        "mc_frac_bias": mc_r / mc - 1.0,
        "eta_bias": eta_r - eta, "chi_bias": chi_r - chi,
        "n_restarts": int(n_restarts), "seed": int(seed),
        "restart_spread_FF": float(ach.max() - ach.min()),
        "_x": best.x.tolist(),
    }


def significance(ff: float, snr: float) -> float:
    """Residual significance of an unmodelled deviation at fixed SNR."""
    return float(snr * np.sqrt(max(2.0 * (1.0 - ff), 0.0)))


def A_for_significance(scan, target_sigma: float = 3.0, snr: float = 25.0):
    """Smallest A_log detectable at `target_sigma` -- the detection limit that
    protocol section 3.2 requires a null to be reported with.

    Read off the computed ladder by log-log interpolation between the two
    bracketing points, rather than by assuming a functional form. An earlier
    version fitted a straight line through the small-A branch; the fit's own
    residual diagnostic showed the linear model was wrong by more than an order
    of magnitude in relative terms, so it was replaced. The bracketing points
    are returned so the interpolation is checkable.

    Returns (A_at_target, diagnostics dict).
    """
    pts = sorted(((r["A_log"], significance(r["FF"], snr)) for r in scan
                  if r["A_log"] > 0), key=lambda t: t[0])
    A = np.array([a for a, _ in pts], dtype=float)
    sg = np.array([s for _, s in pts], dtype=float)
    if not np.all(np.diff(sg) > 0):
        raise ValueError("significance is not monotone in A; cannot interpolate")
    if target_sigma <= sg[0] or target_sigma >= sg[-1]:
        raise ValueError(
            f"target {target_sigma} sigma is outside the computed ladder "
            f"[{sg[0]:.3g}, {sg[-1]:.3g}] at SNR {snr}; extend the ladder rather "
            "than extrapolating")
    j = int(np.searchsorted(sg, target_sigma))
    lo_A, hi_A, lo_s, hi_s = A[j - 1], A[j], sg[j - 1], sg[j]
    t = (np.log(target_sigma) - np.log(lo_s)) / (np.log(hi_s) - np.log(lo_s))
    val = float(np.exp(np.log(lo_A) + t * (np.log(hi_A) - np.log(lo_A))))
    return val, {"method": "log-log interpolation on the computed ladder",
                 "bracket_A": [float(lo_A), float(hi_A)],
                 "bracket_sigma": [float(lo_s), float(hi_s)],
                 "local_log_slope": float((np.log(hi_s) - np.log(lo_s))
                                          / (np.log(hi_A) - np.log(lo_A)))}


def ladder(A_values, f, S, n_restarts: int = N_RESTARTS):
    """Solve an increasing ladder of A with warm starts. Returns list of dicts."""
    out, x0 = [], None
    for A in sorted(float(a) for a in A_values):
        r = fitting_factor(A, f, S, x0=x0, n_restarts=n_restarts)
        x0 = r.pop("_x")
        r["A_log"] = A
        r["dPhi_50_200_rad"] = A * float(np.log(4.0))
        r["sig_snr25"] = significance(r["FF"], 25.0)
        r["sig_snr100"] = significance(r["FF"], 100.0)
        out.append(r)
    return out
