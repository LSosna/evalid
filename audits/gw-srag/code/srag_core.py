"""SRAG/SRLG coherence formulas, exactly as stated in the corpus.

Sources (page refs in docs/PREREGISTRATION_GW_EVALID.md):
  C(lam)   = 1 - exp(-kappa*|lam|**beta),  kappa=2.3, beta=1.2
  dPhi(w)  = lam * ln(w0/w) / C(lam)
  lam_A    = -G M^2 / (r * E_Planck)        "energy transformation"
  lam_B    =  G M_bar / (R_eff c^2)         "baryonic compactness"
"""
import numpy as np

# CODATA-consistent constants
G     = 6.674e-11          # m^3 kg^-1 s^-2   (value quoted in SPARC_compactness p3)
C_L   = 2.998e8            # m/s              (value quoted in SPARC_compactness p3)
HBAR  = 1.054571817e-34    # J s
E_PL  = np.sqrt(HBAR * C_L**5 / G)   # Planck energy, J
MSUN  = 1.98892e30         # kg
MPC   = 3.0856775814913673e22  # m

KAPPA, BETA = 2.3, 1.2


def C_of_lambda(lam, kappa=KAPPA, beta=BETA):
    """Coherence function C(lam) = 1 - exp(-kappa |lam|^beta)."""
    lam = np.asarray(lam, dtype=float)
    return 1.0 - np.exp(-kappa * np.abs(lam) ** beta)


def A_of_lambda(lam, kappa=KAPPA, beta=BETA):
    """Amplitude of the log-phase term: A = lam / C(lam).

    Observable phase is Psi(f) = Psi_GR(f) - A * ln(f/f0).
    Small-lam limit: C -> kappa*lam^beta, so A -> lam^(1-beta)/kappa = lam^-0.2/kappa,
    which DIVERGES as lam -> 0.  This is the key structural property.
    """
    return np.asarray(lam, dtype=float) / C_of_lambda(lam, kappa, beta)


def dPhi_between(lam, f_lo, f_hi, kappa=KAPPA, beta=BETA):
    """Phase-shift difference between two frequency components, per the corpus formula
    dPhi(w) = lam ln(w0/w)/C(lam):
        DPhi = dPhi(w_lo) - dPhi(w_hi) = lam ln(w_hi/w_lo)/C(lam) = A * ln(f_hi/f_lo)
    w0 cancels exactly -- it is unobservable.
    """
    return A_of_lambda(lam, kappa, beta) * np.log(f_hi / f_lo)


def lam_energy(M_kg, r_m):
    """lam = G M^2 / (r E_Planck)  (magnitude; corpus writes it with a leading minus)."""
    return G * np.asarray(M_kg, float) ** 2 / (np.asarray(r_m, float) * E_PL)


def lam_compactness(M_kg, r_m):
    """lam = G M / (R c^2)."""
    return G * np.asarray(M_kg, float) / (np.asarray(r_m, float) * C_L**2)


def pn_order_of_mdr(alpha):
    """PN order at which an MDR phase term f^(alpha-1) enters, relative to the
    leading GR phase f^(-5/3).

    ratio  = f^(alpha-1) / f^(-5/3) = f^(alpha + 2/3)
    v ~ f^(1/3)  =>  f^(alpha+2/3) = v^(3*alpha+2)
    v^(2n) => n = (3*alpha + 2)/2
    """
    return (3.0 * np.asarray(alpha, float) + 2.0) / 2.0
