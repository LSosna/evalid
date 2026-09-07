# Corrigendum: GW-SRAG prediction P6

**Corrects:** `REPORT.md` v0, §5 and Figure 1 panel (d).
**Found by:** an independent re-run, not by the author.
**Verdict direction:** unchanged — P6 `FAIL`. The verdict is stronger than shipped.

## What v0 claimed

> max |ρ| = 0.952, above the registered 0.95 threshold. The logarithmic term is
> 95 % correlated with α = 0 — the massive graviton […]

with the row:

| α | 0 | 0.5 | 1.5 | 2.5 | 3 | 3.5 | 4 |
|---|---|---|---|---|---|---|---|
| \|ρ\| | 0.952 | 0.900 | 0.633 | 0.285 | 0.139 | 0.036 | 0.025 |

## What is true

Recomputed four independent ways — Gram–Schmidt with one pass, Gram–Schmidt
with re-orthogonalisation, a Gram-matrix pseudo-inverse at rcond 1e-12, and the
marginalised Fisher covariance (the definition with no projector-implementation
freedom in it). All four agree to four decimal places.

| α | Shipped | Recomputed | Δ | vs threshold 0.95 |
|---|---|---|---|---|
| 0 | 0.952 | **0.99895** | +0.047 | exceeds |
| 0.5 | 0.900 | 0.94825 | +0.048 | 0.0018 below |
| 1.5 | 0.633 | **0.98170** | +0.349 | exceeds |
| 2.5 | 0.285 | 0.91296 | +0.628 | below |
| 3 | 0.139 | 0.86794 | +0.729 | below |
| 3.5 | 0.036 | 0.81903 | +0.783 | below |
| 4 | 0.025 | 0.76907 | +0.744 | below |

Stable across grids from 10,000 to 80,000 points and finite-difference steps
from 1e-4 to 1e-7. Uncertainty u ≤ 1e-4 by methods `grid` and `step`.

## What was wrong, specifically

1. **The family is not cleanly separated above α = 2.5.** v0 reported ρ falling
   to 0.025; nothing in the family falls below 0.77.
2. **α = 0 is 99.9 % correlated, not 95 %.**
3. **α = 1.5 also exceeds the threshold.** v0 placed it at 0.633.
4. **Figure 1 panel (d) is materially misleading** and is replaced by
   `results/fig1_panel_d_corrected.png`. The v0 panel shows one α touching the
   threshold line and a clean monotone decay; the truth is two above the line
   and no clean decay.

The monotone-decreasing shape of the v0 profile is the signature of a
projection that did not remove the full nuisance basis.

## Consequence for the protocol

The v0 comparison was **0.952 against 0.95** — a margin of 0.002 — with no
stated numerical uncertainty. Varying only the projection implementation moved
the same quantity by up to 0.096: forty-eight times that margin. Under protocol
0.3.1 a defensible-looking program could have returned 0.948 and flipped the
verdict with no signal that anything was fragile.

Protocol 0.3.2 §4 now requires a numerical uncertainty on every threshold
comparison, adds the `INDETERMINATE` verdict for values inside that band, and
requires the `implementation` uncertainty method for any quantity involving a
projection, an orthogonalisation or a matrix inverse. See
`protocol/EVALID_v0.3.4.md` §9.1.

## Reproduce it

    python audits/gw-srag/code/reproduce.py --p6

Machine-readable record: `results/p6_corrected.json`.
