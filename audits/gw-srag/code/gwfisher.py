"""TaylorF2 3.5PN aligned-spin waveform + Fisher / fitting-factor machinery
for auditing a logarithmic phase term  Psi -> Psi_GR - A_log * ln(f/f0).

Phase: Buonanno, Iyer, Ochsner, Pan & Sathyaprakash (2009) Eq. 3.18 form,
3.5PN, with Poisson-Will spin parameters (4*beta at 1.5PN, -10*sigma at 2PN).
PSD:  analytic Advanced LIGO fit (Ajith 2011).  Only the SHAPE of the PSD
matters here because every result is quoted at fixed network SNR.
"""
import numpy as np
from scipy.optimize import minimize

MSUN_S = 4.925491025543576e-6   # G M_sun / c^3, seconds
EULER_G = 0.5772156649015329


# ---------------------------------------------------------------- PSD
def psd_aligo(f):
    """Analytic aLIGO design-sensitivity fit (Ajith 2011). f in Hz."""
    x = np.asarray(f, float) / 215.0
    return 1e-49 * (x ** -4.14 - 5.0 * x ** -2
                    + 111.0 * (1.0 - x ** 2 + 0.5 * x ** 4) / (1.0 + 0.5 * x ** 2))


# ---------------------------------------------------------------- waveform
def _mc_eta_to_m(mc, eta):
    """Chirp mass (Msun) + eta -> total mass (Msun), m1, m2."""
    M = mc / eta ** 0.6
    disc = np.sqrt(np.maximum(1.0 - 4.0 * eta, 0.0))
    return M, 0.5 * M * (1.0 + disc), 0.5 * M * (1.0 - disc)


def taylorf2_phase(f, mc, eta, chi, A_log=0.0, f0=100.0, tc=0.0, phic=0.0):
    """Frequency-domain GW phase, radians. mc in Msun, eta, aligned spin chi
    (chi1 = chi2 = chi), A_log the coefficient of -ln(f/f0)."""
    M, m1, m2 = _mc_eta_to_m(mc, eta)
    Ms = M * MSUN_S
    v = (np.pi * Ms * f) ** (1.0 / 3.0)
    lv = np.log(v)

    # Poisson-Will spin parameters, aligned, chi1 = chi2 = chi
    q1, q2 = m1 / M, m2 / M
    beta = (chi / 12.0) * (113.0 * (q1 ** 2 + q2 ** 2) + 150.0 * eta)
    sigma = (eta / 48.0) * (721.0 - 247.0) * chi * chi

    a0 = 1.0
    a2 = 3715.0 / 756.0 + 55.0 * eta / 9.0
    a3 = -16.0 * np.pi + 4.0 * beta
    a4 = (15293365.0 / 508032.0 + 27145.0 * eta / 504.0
          + 3085.0 * eta ** 2 / 72.0 - 10.0 * sigma)
    a5c = np.pi * (38645.0 / 756.0 - 65.0 * eta / 9.0)
    a5 = a5c * (1.0 + 3.0 * lv)                      # <-- GR's own ln v term (2.5PN)
    a6 = (11583231236531.0 / 4694215680.0 - 640.0 * np.pi ** 2 / 3.0
          - 6848.0 * EULER_G / 21.0
          + eta * (-15737765635.0 / 3048192.0 + 2255.0 * np.pi ** 2 / 12.0)
          + 76055.0 * eta ** 2 / 1728.0 - 127825.0 * eta ** 3 / 1296.0
          - (6848.0 / 21.0) * np.log(4.0 * v))       # <-- GR's own ln v term (3PN)
    a7 = np.pi * (77096675.0 / 254016.0 + 378515.0 * eta / 1512.0
                  - 74045.0 * eta ** 2 / 756.0)

    series = (a0 + a2 * v ** 2 + a3 * v ** 3 + a4 * v ** 4
              + a5 * v ** 5 + a6 * v ** 6 + a7 * v ** 7)
    psi_gr = 2.0 * np.pi * f * tc - phic - np.pi / 4.0 \
        + (3.0 / (128.0 * eta * v ** 5)) * series
    return psi_gr - A_log * np.log(f / f0)


def f_isco(mc, eta):
    M, _, _ = _mc_eta_to_m(mc, eta)
    return 1.0 / (6.0 ** 1.5 * np.pi * M * MSUN_S)


def waveform(f, mc, eta, chi, A_log=0.0, f0=100.0, tc=0.0, phic=0.0, amp=1.0):
    """Restricted-PN amplitude h(f) = amp * f^(-7/6) exp(i Psi)."""
    return amp * f ** (-7.0 / 6.0) * np.exp(1j * taylorf2_phase(
        f, mc, eta, chi, A_log, f0, tc, phic))


# ---------------------------------------------------------------- inner products
def make_grid(mc, eta, f_low=20.0, f_high=None, n=20000):
    fh = f_isco(mc, eta) if f_high is None else f_high
    f = np.linspace(f_low, fh, n)
    return f, psd_aligo(f)


def inner(a, b, f, S):
    return 4.0 * np.real(np.trapezoid(a * np.conj(b) / S, f))


# ---------------------------------------------------------------- Fisher
PARAMS = ["ln_amp", "tc", "phic", "ln_mc", "ln_eta", "chi", "A_log"]


def fisher(mc, eta, chi, f, S, snr=25.0, f0=100.0, A_log=0.0,
           rel_step=1e-5):
    """Fisher matrix in PARAMS at the given point, normalised so that the
    waveform has the requested SNR. Returns (F, cov, sigmas, corr, snr_used)."""
    h = waveform(f, mc, eta, chi, A_log, f0)
    norm = np.sqrt(inner(h, h, f, S))
    amp = snr / norm                      # amplitude giving requested SNR
    h = amp * h

    d = {}
    d["ln_amp"] = h
    d["tc"] = 1j * 2.0 * np.pi * f * h
    d["phic"] = -1j * h
    d["A_log"] = -1j * np.log(f / f0) * h

    # numerical phase derivatives for mc, eta, chi (phase-only -> i*dPsi*h)
    def dpsi(par, val, step):
        kw = dict(mc=mc, eta=eta, chi=chi, A_log=A_log, f0=f0)
        kw[par] = val + step
        p_p = taylorf2_phase(f, **kw)
        kw[par] = val - step
        p_m = taylorf2_phase(f, **kw)
        return (p_p - p_m) / (2.0 * step)

    d["ln_mc"] = 1j * dpsi("mc", mc, mc * rel_step) * mc * h
    d["ln_eta"] = 1j * dpsi("eta", eta, eta * rel_step) * eta * h
    d["chi"] = 1j * dpsi("chi", chi, max(abs(chi), 1.0) * rel_step) * h

    n = len(PARAMS)
    F = np.empty((n, n))
    for i, pi in enumerate(PARAMS):
        for j, pj in enumerate(PARAMS):
            F[i, j] = inner(d[pi], d[pj], f, S)
    cov = np.linalg.inv(F)
    sig = np.sqrt(np.diag(cov))
    corr = cov / np.outer(sig, sig)
    return F, cov, sig, corr, snr


# ---------------------------------------------------------------- fitting factor
def fitting_factor(mc, eta, chi, A_log, f, S, f0=100.0):
    """Maximise the normalised overlap of a GR-only template against an
    injection containing the log-dispersion term. Maximisation over
    (mc, eta, chi) numerically and over (tc, phic) is folded in by
    maximising over tc analytically-free start values; phic maximised
    analytically via |<a|b>| with a complex overlap.

    Returns dict with FF and the recovered (biased) GR parameters.
    """
    hs = waveform(f, mc, eta, chi, A_log, f0)
    ns = np.sqrt(inner(hs, hs, f, S))

    def neg_overlap(x):
        lmc, leta_l, cl, tc = x
        m_, e_ = np.exp(lmc), 0.25 / (1.0 + np.exp(-leta_l))
        c = np.tanh(cl)                      # enforce |chi| <= 1 (physical)
        ht = waveform(f, m_, e_, c, 0.0, f0, tc=tc)
        nt = np.sqrt(inner(ht, ht, f, S))
        # maximise over phic analytically: use modulus of complex overlap
        z = 4.0 * np.trapezoid(hs * np.conj(ht) / S, f)
        return -np.abs(z) / (ns * nt)

    eta_l0 = np.log((eta / 0.25) / (1.0 - eta / 0.25 + 1e-12))
    cl0 = np.arctanh(np.clip(chi, -0.999, 0.999))
    best = None
    for dtc in (0.0, -0.005, 0.005, -0.02, 0.02):
        for dmc in (0.0, -1e-3, 1e-3):
            for dcl in (0.0, 0.5, -0.5):
                x0 = [np.log(mc) + dmc, eta_l0, cl0 + dcl, dtc]
                r = minimize(neg_overlap, x0, method="Nelder-Mead",
                             options=dict(maxiter=8000, xatol=1e-11, fatol=1e-13))
                if best is None or r.fun < best.fun:
                    best = r
    lmc, leta_l, cl, tc = best.x
    mc_r = float(np.exp(lmc))
    eta_r = float(0.25 / (1.0 + np.exp(-leta_l)))
    chi_r = float(np.tanh(cl))
    return dict(FF=float(-best.fun), mc_rec=mc_r, eta_rec=eta_r,
                chi_rec=chi_r, tc_rec=float(tc),
                mc_frac_bias=mc_r / mc - 1.0,
                eta_bias=eta_r - eta, chi_bias=chi_r - chi)
