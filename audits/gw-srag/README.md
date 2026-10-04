# EVALID-AUDIT-GW-SRAG

A pre-registered falsification audit of the SRAG/SRLG logarithmic
gravitational-wave dispersion proposal. **The audited framework is the
auditor's own prior work** — see `REPORT.md` §0.

Twelve of thirteen registered predictions fail.

## Contents

| Path | What it is |
|---|---|
| `PREREGISTRATION.md` | Registered before any test was run. Not edited since. |
| `REPORT.md` | The audit, v1, with P6 corrected. |
| `CORRIGENDUM_P6.md` | The P6 correction, found by an independent re-run. |
| `anchors.json` | 64 claimed/recomputed pairs, source-bound (protocol §5.1). |
| `manifest.json` | SHA-256 of every file here. |
| `code/reproduce.py` | Regenerates every results file. `--selftest` runs offline. |
| `code/gwfisher.py` | TaylorF2 3.5PN waveform, Fisher and fitting-factor machinery. |
| `code/srag_core.py` | The corpus's own formulas, implemented as stated. |
| `results/` | All computed outputs, plus `environment.json`. |

## Reproduce

```bash
python code/reproduce.py --selftest        # offline, synthetic, ~10 s
python code/reproduce.py --internal --p6 --fisher   # ~3 min
python code/reproduce.py --ff              # fitting factors, ~5 min
evalid conform .                           # protocol §8, mechanical subset
```

## A note on the pre-registration and protocol 0.3.2

The pre-registration was written under protocol 0.3.1, which did not yet
require the object's author to be named in it (§2.2) or a condition-number
ceiling to be registered in advance (§4.3). Both requirements were added in
0.3.2 *because of defects in this audit*.

The pre-registration is therefore **not** retrofitted — editing a
pre-registration after data are loaded is precisely what the document exists to
prevent. Instead:

- The self-audit disclosure appears in `REPORT.md` §0, and is stated as a
  disclosure made at report time rather than as something registered in advance.
- The conditioning ceiling (1e15) was set after the fact and is labelled as
  such in `REPORT.md`. The BBH exclusion it produces is honest but was not a
  registered rule at the time; the next audit registers it in advance.

Both are recorded here rather than quietly fixed, per protocol §5.2.

## Figures

`results/fig1_audit_ORIGINAL.png` is the v0 four-panel figure and is retained
as the record of what was published. **Its panel (d) is wrong** — see
`CORRIGENDUM_P6.md`. `results/fig1_panel_d_corrected.png` is the replacement.
