# Contributing

The most valuable contribution to this repository is a finding against it.

## Filing a finding

Open an issue with:

1. **The claim you are challenging** — file, section, and the printed number.
2. **What you computed instead**, and the code that computed it.
3. **Whether a verdict changes.**

The best findings are the ones that tell the author to run a query rather than
telling him the answer. The single most damaging error in this programme's
history — the MMLU availability claim — was one the author could not have been
argued out of by assertion. It took one HTTP request.

Confirmed findings are recorded in `CORRECTIONS.md` with the finder credited.
Findings are not resolved by editing the claim quietly.

## Code

- `evalid selftest` and `python audits/gw-srag/code/reproduce.py --selftest`
  must pass.
- Any new threshold comparison must go through `stats.threshold_verdict` with a
  real uncertainty. There is no default, deliberately.
- Any new verdict string must be added to `evalid/verdicts.py` and to the
  protocol spec in the same change, or it will raise.
- Seed every stochastic step.

## Audits

A new audit needs a pre-registration hashed into a manifest *before* data are
loaded, an anchors file with source bindings, and a reproducer with an offline
`--selftest`. Run `evalid conform <dir>` before opening the PR; it checks the
mechanical subset of protocol §8. The judgement items — sidedness, unit
consistency, disclosure, prior art — are yours.
