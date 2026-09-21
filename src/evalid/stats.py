"""Statistical machinery for EVALID 0.3.2.

The module that matters here is `threshold_verdict`: it is the implementation
of protocol §4, which requires every threshold comparison to carry a numerical
uncertainty and to return INDETERMINATE when the measured value falls inside
that band.

That rule exists because of a real defect. GW-SRAG prediction P6 compared
0.952 against a threshold of 0.95 with no uncertainty; the same quantity moved
by up to 0.096 under a change of projection implementation alone.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Iterable, Sequence

from ._deps import np
from .verdicts import check_prediction

UNCERTAINTY_METHODS = ("grid", "step", "resample", "implementation")

#: Recommended condition-number ceiling for double-precision work (protocol §4.3).
DEFAULT_COND_CEILING = 1e12


# --------------------------------------------------------------------------
# Threshold comparison -- protocol section 4
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class ThresholdResult:
    verdict: str
    value: float
    threshold: float
    uncertainty: float
    method: str
    direction: str
    margin: float
    margin_in_sigma: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def threshold_verdict(value: float, threshold: float, uncertainty: float,
                      method: str, direction: str = "above",
                      fail_side: str = "above") -> ThresholdResult:
    """Compare a measured value against a registered threshold, honestly.

    Parameters
    ----------
    value, threshold
        The measured quantity and the threshold registered before data were seen.
    uncertainty
        Half-width of the numerical uncertainty band on `value`, from one of
        the methods in `UNCERTAINTY_METHODS`. Must be finite and >= 0.
        There is deliberately no default: protocol 0.3.2 makes a threshold
        comparison without an uncertainty undefined.
    method
        Which method produced `uncertainty`. Recorded in the result so a reader
        can judge it.
    direction
        'above' if the registered criterion triggers when value >= threshold,
        'below' if it triggers when value <= threshold.
    fail_side
        Whether triggering the criterion means FAIL (default) or PASS.

    Returns
    -------
    ThresholdResult with verdict PASS, FAIL or INDETERMINATE.
    """
    if method not in UNCERTAINTY_METHODS:
        raise ValueError(
            f"uncertainty method {method!r} not one of {UNCERTAINTY_METHODS}")
    u = float(uncertainty)
    if not np.isfinite(u) or u < 0:
        raise ValueError("uncertainty must be finite and non-negative")
    if direction not in ("above", "below"):
        raise ValueError("direction must be 'above' or 'below'")

    margin = float(value) - float(threshold)
    if direction == "below":
        margin = -margin

    if abs(margin) <= u:
        verdict = "INDETERMINATE"
    else:
        triggered = margin > 0
        if fail_side == "above":
            verdict = "FAIL" if triggered else "PASS"
        else:
            verdict = "PASS" if triggered else "FAIL"

    return ThresholdResult(
        verdict=check_prediction(verdict),
        value=float(value), threshold=float(threshold), uncertainty=u,
        method=method, direction=direction, margin=margin,
        margin_in_sigma=(abs(margin) / u) if u > 0 else None,
    )


def uncertainty_from_spread(values: Iterable[float]) -> float:
    """Half-range of a set of independently computed values.

    The estimator behind methods 'grid', 'step' and 'implementation'. Pass the
    same quantity computed at several discretisations, several finite-difference
    steps, or by several independent implementations.
    """
    v = np.asarray(list(values), dtype=float)
    if v.size < 2:
        raise ValueError("need at least two independent computations")
    return float((v.max() - v.min()) / 2.0)


def implementation_spread(fns: Sequence[Callable[[], float]]) -> tuple[float, float]:
    """Run >=2 independent implementations of one quantity; return (mean, u).

    Required by protocol section 4.2 for any quantity involving a projection,
    an orthogonalisation, or a matrix inverse.
    """
    if len(fns) < 2:
        raise ValueError("protocol 4.2 requires at least two implementations")
    vals = [float(f()) for f in fns]
    return float(np.mean(vals)), uncertainty_from_spread(vals)


# --------------------------------------------------------------------------
# Numerical admissibility gate -- protocol section 4.3
# --------------------------------------------------------------------------
def condition_gate(matrix, ceiling: float = DEFAULT_COND_CEILING) -> tuple[str, float]:
    """Test a matrix against the registered condition-number ceiling.

    Returns ('OK'|'UNDERDETERMINED', cond). Quantities derived from an inverse
    that returns UNDERDETERMINED must not be reported.
    """
    cond = float(np.linalg.cond(np.asarray(matrix, dtype=float)))
    return ("UNDERDETERMINED" if cond > ceiling else "OK"), cond


def safe_inverse(matrix, ceiling: float = DEFAULT_COND_CEILING):
    """Invert with diagonal rescaling, refusing matrices past the ceiling.

    Rescaling by 1/sqrt(diag) before inversion recovers several digits on
    matrices whose parameters differ by many orders of magnitude, which is the
    normal situation for a Fisher matrix.
    """
    M = np.asarray(matrix, dtype=float)
    status, cond = condition_gate(M, ceiling)
    if status == "UNDERDETERMINED":
        raise ValueError(
            f"cond(M) = {cond:.3e} exceeds registered ceiling {ceiling:.3e}; "
            "verdict is UNDERDETERMINED and the quantity must not be reported")
    s = 1.0 / np.sqrt(np.abs(np.diag(M)))
    return np.linalg.inv(M * np.outer(s, s)) * np.outer(s, s)


# --------------------------------------------------------------------------
# Multiplicity -- protocol section 2.5
# --------------------------------------------------------------------------
def benjamini_hochberg(pvals: Sequence[float], q: float = 0.05):
    """Benjamini-Hochberg step-up. Returns (rejected mask, adjusted p-values).

    Each statistic must enter the family exactly once. Two predictions that
    resolve to one statistic -- as GW-SRAG P1 and P2 did, and as MMLU Audit 002
    P1/P2 did -- inflate the family size and must be collapsed before this is
    called.
    """
    p = np.asarray(pvals, dtype=float)
    if p.ndim != 1 or p.size == 0:
        raise ValueError("pvals must be a non-empty 1-D sequence")
    if np.any((p < 0) | (p > 1)):
        raise ValueError("p-values must lie in [0, 1]")
    n = p.size
    order = np.argsort(p)
    ranked = p[order]
    adj = np.minimum.accumulate((ranked * n / np.arange(n, 0, -1))[::-1])[::-1]
    adj = np.clip(adj, 0, 1)
    out = np.empty(n, dtype=float)
    out[order] = adj
    return out <= q, out


def cluster_bootstrap_ci(values, clusters, statistic=np.mean, n_boot: int = 2000,
                         alpha: float = 0.05, seed: int = 0):
    """Percentile CI resampling whole clusters, not individual observations.

    The resampling unit is the protocol's declared unit -- subject, galaxy,
    event. Resampling items inside a cluster when the declared unit is the
    cluster is the unit-consistency violation that cost GW-SRAG P1 its
    significance.
    """
    v = np.asarray(values, dtype=float)
    c = np.asarray(clusters)
    if v.shape[0] != c.shape[0]:
        raise ValueError("values and clusters must be the same length")
    uniq = np.unique(c)
    idx = {u: np.flatnonzero(c == u) for u in uniq}
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot, dtype=float)
    for b in range(n_boot):
        picked = rng.choice(uniq, size=uniq.size, replace=True)
        draws[b] = statistic(np.concatenate([v[idx[u]] for u in picked]))
    lo, hi = np.percentile(draws, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(statistic(v)), float(lo), float(hi)


def detection_limit(sigma: float, n_sigma: float = 3.0) -> float:
    """Smallest effect detectable at `n_sigma`. A null must be reported with it."""
    return float(n_sigma) * float(sigma)
