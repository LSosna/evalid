# Correction log

Protocol §5.2: errors found after publication are logged, not silently
repaired. This file is a first-class deliverable. An audit programme with no
corrections is an audit programme that is not being checked.

Each entry records what was claimed, what is correct, the mechanism, whether a
verdict changed, and **who found it** — the last column being the one that
matters.

| Date | Audit | What was claimed | What is correct | Verdict change | Found by |
|---|---|---|---|---|---|
| 2026-09 | GW-SRAG | P6 max \|ρ\| = 0.952, family separated above α=2.5 (ρ→0.025) | max \|ρ\| = 0.99895; nothing below 0.77; two α above threshold | No — `FAIL` either way, stronger | Independent re-run |
| 2026-09 | GW-SRAG | *(self-caught)* P4 detectability threshold \|ΔΦ\| ≈ 1/SNR | Criterion invalid: only the component orthogonal to GR directions is observable | P4 → `REGISTERED_INVALID`, superseded by P5 | Author |
| 2026-09 | GW-SRAG | BBH case excluded on cond(F) = 1.9e16 | Correct exclusion, but the criterion was chosen after seeing the number | Now a registered `UNDERDETERMINED` gate | Independent re-run |
| 2026-08 | MMLU-002 | Per-item model results not publicly available | They are; `details_*` repos return HTTP 200 with 57 per-subject parquet files | Retracts the stated rationale for the target substitution | Reviewer 2 |
| 2026-08 | MMLU-002 | P1/P2 positional finding survives BH | It does not, once the declared subject-clustered p (0.0405) is used | Survivors 5 → 3 | Reviewer 2 |
| 2026-08 | MMLU-002 | Within-split duplication 1.253 % (176 items) | 2.357 % (331 items); 176 was rows beyond one per group | No — `FAIL` either way, stronger | Reviewer 2 |
| 2026-08 | MMLU-002 | "29/29 anchors passed" | 29 of **38** defined anchors were checked | Overstated verification | Reviewer 2 |
| 2026-08 | MMLU-002 | Question-blind method presented as novel | Prior art: Balepur, Ravichander & Rudinger (2024), arXiv:2402.12483 | Contribution restated as the audit framing | Reviewer 2 |
| 2026-08 | MMLU-002 | P8 "items well-formed" PASS | Structural well-formedness only; Gema et al. (2025) put label errors at 6.49 % | New stated limitation | Author |
| 2026-07 | 001 | A defect reported by the verifier was dismissed | The defect was real | Dismissal retracted | Verifier |

## Running total

Fourteen corrections across three audits. Eleven were found by someone other
than the author.

That ratio is the point. An author whose published error rate is zero is an
author who is not being checked; the number that matters is not how many
errors are found, but whether they are found by someone else and whether the
author prints them.
