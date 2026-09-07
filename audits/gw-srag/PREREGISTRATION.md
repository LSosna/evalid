# Pre-registration: Falsification audit of the GW-EVALID Gen-3 proposal

**Object of audit:** the proposal to test SRAG/SRLG logarithmic gravitational-wave
dispersion, `δΦ(ω) = λ·ln(ω₀/ω)/C(λ)`, with `C(λ) = 1 − exp(−κ|λ|^β)`, κ ≈ 2.3, β ≈ 1.2.

**Registered before any test was run.** Thresholds below are fixed; verdicts are
whatever the numbers give.

## Source of the hypothesis (as stated in the corpus)

| Quantity | Value / form | Source |
|---|---|---|
| Phase shift | `δΦ(ω) = λ·ln(ω₀/ω)/C(λ)` | SRAG_spinoff p7, SRAG_vixra p5 |
| Coherence fn | `C(λ) = 1 − exp(−κ|λ|^β)`, κ=2.3, β=1.2 | SRAG_spinoff p3 |
| λ definition A | `λ = −GM²/(r·E_Planck)` (energy transformation) | SRAG_main_rev22 p3, SRAG_vixra p5 |
| λ definition B | `λ = GM_bar/(R_eff c²)` (baryonic compactness) | SPARC_compactness p3 |
| λ (spiral, empirical) | 0.08, with stated `C(0.08) ≈ 0.18` | SRAG_vixra p4, SRAG_spinoff p8 |
| λ (SPARC median) | 2.4 × 10⁻⁸ | SPARC_compactness p4 |
| Headline prediction | 0.24 rad between 50 Hz and 200 Hz | GW_wave_based p6, SRAG_spinoff p8 |
| Alt. prediction | (2.7 ± 0.5)×10⁻²² rad/Mpc for λ ≈ 10⁻⁴ | GW_wave_based p7 |

Observable form used throughout: `Ψ(f) = Ψ_GR(f) − A·ln(f/f₀)`, with
**`A ≡ λ/C(λ)`** and f₀ arbitrary (a change of f₀ shifts Ψ by a constant, which is
absorbed exactly by the coalescence phase φ_c — so f₀ is unobservable and is *not*
a testable part of the hypothesis).

## Registered predictions and pass/fail thresholds

**P1 — Structural novelty.** The claim is that logarithmic dispersion is
"structurally un-audited" and orthogonal to the LVK power-law MDR family
`E² = p²c² + A_α(pc)^α`.
- PASS if the `ln f` phase term is *not* obtainable as a member/limit of that family.
- FAIL if it is. Decide by explicit derivation of the PN order of `f^{α−1}` relative
  to the leading GR phase.

**P2 — Internal arithmetic consistency.** Each stated number must follow from the
corpus's own formulas.
- PASS per item if recomputed value is within 10% of the stated value.
- Items: `C(0.08)`; ΔΦ(50→200 Hz) at λ=0.08; every row of the λ-vs-scale table under
  definition A; the 2.7×10⁻²² rad/Mpc rate; consistency of definitions A and B.

**P3 — Physical admissibility (distance scaling).** A propagation effect must
accumulate with path length.
- PASS if a distance factor is present in, or derivable from, the stated formula.
- FAIL if the formula is distance-independent while the text claims growth with distance.

**P4 — Amplitude vs. the framework's own empirical λ.** For the proposal to be
"un-audited" the predicted dephasing must be small enough to have hidden in existing data.
- Detectability scale for a coherent band-wide phase deviation: |δΨ| ≈ 1/SNR.
  For GWTC events (SNR 10–25) this is 0.04–0.10 rad.
- PASS (viable) if predicted |ΔΦ(50→200 Hz)| < 0.10 rad.
- FAIL (already excluded) if > 1 rad.
- Evaluate at λ = 0.08 and at λ = 2.4×10⁻⁸ separately.

**P5 — Identifiability / the collider test (proposal Phase 1, done by Fisher analysis).**
TaylorF2 3.5PN aligned-spin waveform, aLIGO-shape PSD, f_low = 20 Hz, SNR fixed to 25.
Parameters {ln A_amp, t_c, φ_c, ln M_c, ln η, χ_eff, A}.
- Report ρ(A, ln M_c), ρ(A, ln η), ρ(A, χ_eff) and marginalized σ(A).
- "IDENTIFIABLE" if A_pred/σ(A) > 3 for the framework's λ.
- "ABSORBED" if max|ρ| > 0.99 **and** a GR-only template recovers a dispersed
  injection with fitting factor > 0.99 while biasing a parameter beyond its 90% CI.
- Both can hold; report both.

**P6 — Log vs. power-law separability (proposal Phase 2, Model 1 vs Model 2).**
Noise-weighted correlation between the `ln f` phase basis function and `f^{α−1}` for
α ∈ {0, 0.5, 1.5, 2.5, 3, 3.5, 4} over the observing band, after projecting out
{t_c, φ_c, ln M_c, ln η, χ_eff}.
- α = 1 is excluded from the grid because it *is* the log term (|ρ| = 1 by
  construction), and α = 2 because there the phase deviation is degenerate with
  t_c and carries no waveform signature at all. Both omissions are structural,
  not selective.
- PASS (ΔBIC ladder is meaningful) if max_α |ρ| < 0.95.
- FAIL if ≥ 0.95 — Model 1 and Model 2 are then not separable and the registered
  ΔBIC < −10 against Model 1 is unreachable.

**P7 — Phase 3 statistical power arithmetic.** The proposal registers "|r| > 0.5,
p < 0.01" on n = 15 events.
- PASS if the exact two-tailed p-value for r = 0.5, n = 15 is < 0.01.
- Also report: r required for p < 0.01 at n = 15; n required for r = 0.5 at p < 0.01.

**P8 — Phase 3 host-path suppression.** λ is stated to be a property of the *host
galaxy*. A propagation effect samples the host over only a fraction f_path = R_host/D
of the path.
- PASS if f_path > 10⁻³ for a GW170817-like event (D = 40 Mpc).
- FAIL otherwise — the host-λ correlation premise then requires the effect to be
  generated at the source, which is not dispersion.

**P9 — Phase 3 sample availability.** Number of GW events with confident EM
counterparts usable for Test 3.1.
- PASS if ≥ 10.

## Null-result bounding

Any null is reported with its detection limit: the minimum |A| (and hence minimum λ)
that the registered configuration would have detected at 3σ. A bounded null is not a
proof of zero and will not be reported as one.

## Deviations from the proposal's own method, and why

- Phase 1's 1,000 × 2 Bilby runs are replaced by a Fisher-matrix + overlap-maximisation
  calculation. Justification: the quantity Phase 1 asks for is the correlation structure
  and the parameter bias, both of which the Fisher matrix and a fitting-factor
  maximisation give directly and exactly in the linear-signal regime. This is a forecast,
  not an analysis of real strain, and is labelled as such everywhere.
- No GWOSC strain data are used. Real-data anchoring is via the published LVK GWTC-3
  constraint on the α = 1 MDR coefficient.
- Waveform is TaylorF2 3.5PN (aligned spin), inspiral only. Validated by reproducing the
  known σ(M_c)/M_c ≈ 10⁻³ scale for a BNS at SNR 25. For the BBH case the inspiral band
  is narrow and TaylorF2 understates information from merger–ringdown; this is recorded
  as a caveat, and the BNS case is primary.
