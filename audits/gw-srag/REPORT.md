# Falsification audit of the SRAG/SRLG logarithmic GW dispersion proposal

**Audit ID:** `EVALID-AUDIT-GW-SRAG` · **Protocol:** 0.3.2 · **Report version:** v1

| | |
|---|---|
| Object of audit | The proposal to test SRAG/SRLG logarithmic gravitational-wave dispersion, `δΦ(ω) = λ·ln(ω₀/ω)/C(λ)` |
| Author of the object of audit | Lukas A. Sosna |
| Author of this audit | Lukas A. Sosna |
| Relationship | **Self-audit. Disclosed under protocol §7.** |
| Pre-registration | [`PREREGISTRATION.md`](PREREGISTRATION.md), fixed before any test was run |
| Terminal verdict | Proposal not viable as written; 12 of 13 registered predictions FAIL |

---

## 0. Disclosure, stated first

**The framework audited in this report is my own.** SRAG/SRLG, the coherence
function `C(λ)`, the rotation-curve calibration and the gravitational-wave
dispersion proposal are all my prior work. I wrote the theory, then wrote
EVALID to test the limits of the evidence behind claims like it, then aimed
EVALID at the theory.

It failed. Twelve of thirteen registered predictions fail, three of them
fatally and independently of the others. This report is the record of that.

I state this in the opening paragraph rather than a footnote because a reader
who works it out later is entitled to ask why it was not said. There is no
answer to that question that helps me. There is a straightforward answer to
the version where I say it first: a protocol whose first published casualty is
its author's own theory has demonstrated something about itself that no
external validation can.

---

## 1. What was audited, and what the verdicts are

The proposal claims that a logarithmic phase deviation in the gravitational
waveform is (a) structurally novel relative to the LVK power-law dispersion
family, (b) numerically consistent with the SRAG corpus, (c) a propagation
effect, and (d) detectable. All four claims fail.

| ID | Registered prediction | Verdict | Basis |
|---|---|---|---|
| P1 | Log term is structurally novel | `FAIL` | α = 1 of the LVK family gives exactly a `ln f` phase at 2.5PN; LVK constrain α = 1 directly and separately vary `dχ₅ₗ` |
| P2a | `C(0.08) = 0.18` as stated | `FAIL` | recomputed 0.10509; stated value 71 % high |
| P2b | Headline 0.24 rad, 50→200 Hz | `FAIL` | recomputed 1.0553 rad, 4.4× larger; 0.24 rad needs C = 0.4621 |
| P2c | λ-vs-scale table (energy definition) | `FAIL` | the formula gives 0.341 at the Planck scale and 3.41e45 for a cluster; the table is inverted relative to its own formula |
| P2d | The two λ definitions agree | `FAIL` | compactness `GM/(Rc²)` gives 2.475e−8 for a spiral, reproducing the SPARC median 2.4e−8; the energy form reproduces nothing. They differ by ~3e6 |
| P2e | Rate 2.7e−22 rad/Mpc → 0.24 rad | `FAIL` | requires 8.889e20 Mpc, 2.1e17 × the Hubble radius |
| P3 | Distance scaling present | `FAIL` | the formula contains no distance; a propagation effect must accumulate with path length |
| P4 | Amplitude below detectability | `REGISTERED_INVALID` | the registered 1/SNR threshold is wrong because the deviation is absorbable; superseded by P5 |
| P5 | Log amplitude identifiable | `FAIL` (absorbed) | \|ρ\| to 0.9992; σ(A) inflates 411× on marginalisation; FF = 0.99987 at λ = 0.08 leaves 0.40 σ at SNR 25 |
| P6 | Separable from the power-law family | `FAIL` | max \|ρ\| = **0.99895** at α = 0; α = 1.5 also exceeds threshold; nothing in the family falls below 0.77 |
| P7 | \|r\| > 0.5 at n = 15 gives p < 0.01 | `FAIL` | exact p = 0.0577; needs r ≥ 0.641 at n = 15, or n ≥ 26 at r = 0.5 |
| P8 | Host path fraction > 1e−3 | `FAIL` | 7.50e−5 (3 kpc host) to 5.00e−4 (20 kpc) at 40 Mpc |
| P9 | ≥ 10 events with EM counterparts | `FAIL` | one confident multi-messenger event (GW170817) |

**P6 is corrected in this version.** See §6 and [`CORRIGENDUM_P6.md`](CORRIGENDUM_P6.md).

---

## 2. The novelty claim is false (P1)

A phase term `f^(α−1)` sits at post-Newtonian order `n = (3α+2)/2` relative to
the leading `f^(−5/3)` GR phase. At α = 1 the power-law prefactor `1/(1−α)`
diverges and the limit is exactly `ln f`, at **2.5PN order**.

- **α = 1 is inside the tested set.** LVK constrain α ∈ {0, 0.5, 1, 1.5, 2.5,
  3, 3.5, 4} [4]. The value they exclude is α = 2, where all frequency
  components shift equally and the waveform is unchanged. The logarithmic case
  is not the gap in the audit; it is one of the audited points.
- **The 2.5PN log coefficient is separately constrained.** LVK's parameterized
  tests vary `dχ₅ₗ`, the 2.5PN logarithmic deformation parameter, directly,
  including in multiparameter analyses [4].

GR's own 2.5PN phase term already carries `ln v` with an η-dependent
coefficient. A `ln f` term is therefore not an orthogonal direction in waveform
space; it is a rescaling of a coefficient GR itself supplies. In the language
of the parameterized post-Einsteinian framework [3], this is a ppE deformation
at an exponent GR already occupies.

## 3. The stated numbers do not follow from the stated formulas (P2)

| Claim in the corpus | Recomputed | Status |
|---|---|---|
| `C(0.08) ≈ 0.18` | **0.10509** | 71 % high |
| ΔΦ = 0.24 rad, 50→200 Hz, λ = 0.08 | **1.0553 rad** | 4.4× low |
| 2.7e−22 rad/Mpc → 0.24 rad | needs **8.889e20 Mpc** | 2.1e17 × Hubble radius |
| λ table, Planck scale ~1e34 | **0.341** | inverted |
| λ table, cluster ~0.3 | **3.41e45** | inverted |

To get 0.24 rad from λ = 0.08 you need C = 0.4621, not 0.18 and not 0.10509.
Neither the stated `C` nor the stated ΔΦ is reproducible, and they are
inconsistent with each other.

The λ table is worse than numerically wrong — it is **ordered backwards
relative to its own formula**. `λ = GM²/(rE_Pl)` grows with mass.

**Two incompatible definitions of λ are in circulation.** The compactness form
`λ = GM/(Rc²)` gives 2.475e−8 for a spiral galaxy, reproducing the SPARC
median 2.4e−8 to 3 %. The energy form reproduces nothing. The proposal injects
λ = 0.08 (a rotation-curve fit parameter) while citing the SPARC result (a
compactness) as its empirical boundary condition. They differ by 3e6 and are
not the same quantity.

## 4. It is not a propagation effect (P3)

`δΦ(ω) = λ ln(ω₀/ω)/C(λ)` contains no distance. As written it predicts the
same dephasing for a source at 40 Mpc and at 4 Gpc.

Distance scaling is the entire handle that makes the LVK dispersion test work:
`A_α` is extracted by exploiting the fact that the effect grows with `D_α`
while source-physics parameters do not, which is what allows events to be
combined [1]. A distance-independent `ln f` term forfeits that handle and
collapses to a per-event 2.5PN coefficient shift — i.e. to `dχ₅ₗ`, §2 again.

## 5. The effect is unobservable, not merely unobserved (P5)

Fisher analysis [6] on a GW170817-like binary neutron star (M_c = 1.188 M☉,
η = 0.2497, χ = 0), TaylorF2 3.5PN aligned-spin [5], 20–1610 Hz, aLIGO-shape
PSD, SNR fixed to 25, parameters {ln A, t_c, φ_c, ln M_c, ln η, χ_eff, A_log}:

| correlation with A_log | value |
|---|---|
| φ_c | 0.9992 |
| ln η | −0.9975 |
| χ_eff | +0.9939 |
| ln M_c | +0.9833 |

σ(A_log) = 0.06339 with GR parameters held fixed; **26.048** once they are
marginalised — a **410.9× degeneracy degradation**. Stable to one decimal
under diagonal parameter rescaling, grid refinement from 10k to 40k points,
and finite-difference steps from 1e−4 to 1e−7.

The nonlinear check does not rely on linearization — which matters, because
Fisher forecasts are known to mislead exactly where correlations are this high
[2]. Injecting the log term and maximising a GR-only template over
(M_c, η, χ_eff, t_c, φ_c), with η bounded below 0.25 and |χ| ≤ 1:

| λ | A_log | raw ΔΦ (50→200 Hz) | fitting factor | residual significance, SNR 25 |
|---|---|---|---|---|
| 0.08 (rotation curve) | 0.7613 | 1.055 rad | 0.999875 | **0.40 σ** |
| 1e−4 (GW paper) | 2.7433 | 3.803 rad | 0.998431 | 1.40 σ |
| 2.4e−8 (SPARC) | 14.5288 | 20.141 rad | 0.977504 | **5.27 σ** |

A 1-radian coherent dephasing is nonetheless invisible: the template absorbs
it by moving χ_eff by +0.0094 and M_c by 6.1e−5 fractionally — a chirp-mass
shift of 0.04 σ, well inside the posterior.

### The framework cannot predict a small effect anywhere

Because `C(λ) → κλ^β` as λ → 0, the amplitude `A = λ/C(λ) → λ^(−0.2)/κ`
**diverges** at small λ:

> **min over all λ of A = 0.70523, at λ\* = 0.21035 — a minimum possible
> dephasing of 0.97766 rad between 50 and 200 Hz.**

There is no value of λ that makes this effect small, and the SPARC-calibrated
λ = 2.4e−8 implies a *larger* dephasing (20.1 rad) than λ = 0.08 does
(1.06 rad). The proposal treats the SPARC result as a tightening constraint;
in this framework it is the opposite.

### Detection limits (bounding the null)

3σ thresholds for this configuration: A_log ≥ 5.77 at SNR 25, ≥ 1.44 at
SNR 100. The framework's floor, A = 0.705, is below both.

- **λ = 0.08 branch:** requires network SNR ≈ 190 for 3σ in one event, or
  ≈ 58 SNR-25 BNS events stacked. The loudest event in GWTC-3 (GW170817) had
  network SNR 32.4. Untestable with existing or O5 data.
- **λ = 2.4e−8 branch:** predicts 5.27 σ in a single SNR-25 event. Already
  excluded by existing observations.

Neither branch supports the proposal, and which branch you are on is decided
by which of the two mutually inconsistent λ definitions you use (§3).

## 6. The model-comparison ladder cannot separate its own models (P6)

**This section is corrected in v1.** The v0 values were not reproducible; see
[`CORRIGENDUM_P6.md`](CORRIGENDUM_P6.md) for the full record.

Correlation between the `ln f` phase basis and `f^(α−1)`, marginalised over
{ln A, t_c, φ_c, ln M_c, ln η, χ_eff}. Computed by four independent
implementations — Gram–Schmidt with one pass and with re-orthogonalisation, a
Gram-matrix pseudo-inverse, and the marginalised Fisher covariance — which
agree to four decimal places. Protocol §4.2 requires the `implementation`
uncertainty method for exactly this class of quantity.

| α | 0 | 0.5 | 1.5 | 2.5 | 3 | 3.5 | 4 |
|---|---|---|---|---|---|---|---|
| \|ρ\| | **0.99895** | 0.94825 | **0.98170** | 0.91296 | 0.86794 | 0.81903 | 0.76907 |

max \|ρ\| = **0.99895**, far above the registered 0.95 threshold, with
uncertainty u ≤ 1e−4 across grids from 10k to 80k points and steps from 1e−4
to 1e−7. Two α values exceed the threshold and a third (α = 0.5) sits 0.0018
below it. **Nothing in the family falls below 0.77.**

The logarithmic term is 99.9 % correlated with α = 0 — the massive graviton,
the most-constrained case in the family [4]. The registered success criterion
for the proposal's model ladder, ΔBIC < −10 for Model 2 over Model 1, is
therefore unreachable. *(That last sentence is inference, not a registered
result: P6 as registered tests ρ, not BIC.)*

## 7. Phase 3 fails on arithmetic and on sample (P7–P9)

- **Statistical power.** "|r| > 0.5, p < 0.01" at n = 15 is internally
  unsatisfiable. Exact two-tailed p for r = 0.5, n = 15 is **0.05770**.
  Reaching p < 0.01 needs r ≥ **0.6411** at n = 15, or n ≥ **26** at r = 0.5.
- **Host-path suppression.** λ is defined as a host-galaxy property, but a
  propagation effect samples the host over only R_host/D of the path:
  **7.50e−5** (3 kpc host) to **5.00e−4** (20 kpc) at 40 Mpc. A host-λ
  correlation therefore requires the effect to be generated at the source — in
  which case it is not dispersion, and §4 applies.
- **Sample.** Test 3.1 needs ≥ 10 events with confident EM counterparts. There
  is one.

## 8. Errors in my own pre-registration and in v0 of this report

**P4 — the registered detectability criterion is wrong.** I registered
|ΔΦ| ≈ 1/SNR ≈ 0.04–0.10 rad and predicted that a ≥ 0.98 rad effect would be
"already excluded." The raw band-wide phase deviation is not the observable;
only its component orthogonal to the GR parameter directions is. Once
(M_c, η, χ_eff) are marginalised, a 1.055 rad deviation leaves 0.40 σ (§5). P4
is `REGISTERED_INVALID` and superseded by P5. The correct statement is
"unobservable by absorption", not "excluded by amplitude".

**P6 — the shipped correlation table was not reproducible.** Found by an
independent re-run, not by me. The verdict direction was unchanged and in fact
strengthened, but every value in the row was wrong and the published figure
panel was materially misleading. Recorded in `CORRIGENDUM_P6.md` and in the
repository correction log.

**What the P6 defect changed in the protocol.** It exposed that a threshold
comparison with no stated numerical uncertainty is undefined — I compared
0.952 against 0.95 with a margin of 0.002, while the quantity moved by up to
0.096 under a change of implementation alone. Protocol 0.3.2 §4 now requires an
uncertainty on every threshold comparison and adds an `INDETERMINATE` verdict.
The defect improved the instrument, which is the only defence I would offer
for having made it.

## 9. What would make a test of this worth running

1. **Put the distance in.** The only non-degenerate signature available is
   distance scaling: (η, χ_eff) are distance-independent, so a phase deviation
   growing as `D` cannot be absorbed by them event-to-event. This is how the
   existing LVK test achieves its sensitivity [1]. Deriving `δΦ ∝ D` would make
   the proposal testable — and would also make it the α = 1 MDR, whose
   coefficient is already bounded [4]. That bound then becomes a real,
   quotable constraint on λ rather than an un-run experiment.
2. **Pick one λ and derive it.** The compactness definition is the one that
   reproduces SPARC. Note that fixing it makes the predicted effect *larger*,
   and thus more excluded, not less.
3. **Test the coherence function where it was fitted.** `C(λ)`'s κ and β were
   fitted to rotation curves. Its small-λ divergence in `A = λ/C(λ)` drives
   every quantitative result here, and it is an extrapolation of eight orders
   of magnitude beyond the calibration range. That is testable on rotation
   curves alone, with no GW data and no new detectors.

The defensible version of this programme is not a six-week injection campaign.
It is a short paper deriving the distance dependence and comparing the
resulting λ bound to the published α = 1 constraint.

---

## Methods, assumptions and limitations

**Waveform.** TaylorF2 3.5PN frequency-domain phase [5], aligned spin via the
Poisson–Will parameters (4β at 1.5PN, −10σ at 2PN), restricted PN amplitude
`f^(−7/6)`, inspiral only. `lalsuite` was not available; the phase is
implemented directly from the standard PN expansion — see
[`code/gwfisher.py`](code/gwfisher.py).

**Validation.** σ(M_c)/M_c = 1.492e−3 for the BNS at SNR 25, matching the known
~1e−3 scale for this configuration.

**PSD.** Analytic Advanced LIGO design-sensitivity fit (Ajith 2011),
f_low = 20 Hz. Every result is quoted at fixed SNR, so only the *shape* of the
PSD enters — deliberate, and it makes the conclusions insensitive to the
O3-versus-design difference.

**Numerical admissibility (protocol §4.3).** Registered ceiling: cond(F) ≤ 1e15
for this audit, with the achieved value reported. The BNS case achieves
3.97e13 and is admissible. **The BBH case achieves 1.95e16 and is reported
`UNDERDETERMINED`** — its σ(A_log) = 1.7e4 is a numerical artifact, not a
physical bound. All quoted results are the BNS case.

**Environment.** Python 3.11.15, NumPy 2.4.4, SciPy 1.17.1. Recorded in
`results/environment.json`.

**Determinism.** Fitting-factor maximisation uses Nelder–Mead with warm starts
along the A ladder, seeded, 45 restarts per point. The FF surface is smooth in
this region and η saturates at its physical bound 0.25 throughout; a global
optimum is not proven. The reported values reproduce to 5 decimal places at
8,000 grid points with 9 restarts.

**Not assessed.** Precession, higher harmonics, tidal terms, merger–ringdown,
calibration error, detector-network geometry. None of these can rescue a
0.99895 basis-function correlation or a distance-independent phase term.

**Fisher caveat.** The 2.5PN log coefficient is precisely where Fisher-based
bounds are known to diverge most from full Bayesian bounds for high-mass
binaries [2]. Mitigated, not eliminated, by using an inspiral-dominated BNS and
by the fact that the decisive result (§5) comes from the nonlinear
fitting-factor maximisation, which makes no linearization assumption.

**This is a forecast, not an analysis of real strain.** No GWOSC data were
used. Real-data anchoring is by comparison to published LVK constraints.

---

## References

1. Mirshekari, S., Yunes, N. & Will, C. M. (2012). *Constraining
   Lorentz-violating, modified dispersion relations with gravitational waves.*
   Phys. Rev. D 85, 024041. [arXiv:1110.2720](https://arxiv.org/abs/1110.2720)
2. Vallisneri, M. (2008). *Use and Abuse of the Fisher Information Matrix in
   the Assessment of Gravitational-Wave Parameter-Estimation Prospects.*
   Phys. Rev. D 77, 042001.
   [arXiv:gr-qc/0703086](https://arxiv.org/abs/gr-qc/0703086)
3. Yunes, N. & Pretorius, F. (2009). *Fundamental Theoretical Bias in
   Gravitational Wave Astrophysics and the Parameterized Post-Einsteinian
   Framework.* Phys. Rev. D 80, 122003.
   [arXiv:0909.3328](https://arxiv.org/abs/0909.3328)
4. LIGO Scientific, Virgo & KAGRA Collaborations (2021). *Tests of General
   Relativity with GWTC-3.*
   [arXiv:2112.06861](https://arxiv.org/abs/2112.06861)
5. Buonanno, A., Iyer, B. R., Ochsner, E., Pan, Y. & Sathyaprakash, B. S.
   (2009). *Comparison of post-Newtonian templates for compact binary inspiral
   signals in gravitational-wave detectors.* Phys. Rev. D 80, 084043.
   [arXiv:0907.0700](https://arxiv.org/abs/0907.0700)
6. Cutler, C. & Flanagan, É. E. (1994). *Gravitational waves from merging
   compact binaries: How accurately can one extract the binary's parameters
   from the inspiral waveform?* Phys. Rev. D 49, 2658.
   [arXiv:gr-qc/9402014](https://arxiv.org/abs/gr-qc/9402014)
