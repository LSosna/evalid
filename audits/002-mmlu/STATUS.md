# MMLU Audit 002 — status: PARTIALLY RETRACTED

**`EVALID_AUDIT_002.md` v0 is deliberately not in this repository.**

The corrigendum designates it PARTIALLY RETRACTED and instructs that it not be
published in its shipped form through any channel. Shipping it here with a
corrigendum stapled alongside would leave a document with a known-false
load-bearing claim reachable at a public URL, which is exactly the failure this
protocol exists to prevent.

What ships here:

| File | What it is |
|---|---|
| `PREREGISTRATION.md` | The registered predictions, unmodified. Safe to publish; it is the record. |
| `CORRIGENDUM.md` | The full self-correction: 16 findings adjudicated, 15 confirmed, 1 rejected. |
| `review_adjudication.csv` | Machine-readable adjudication of both reviews. |
| `audit002_per_subject.csv` | Per-subject results, unchanged. |

## What was retracted

1. **The availability claim.** The report said per-item model results are not
   publicly available. They are — `open-llm-leaderboard/details_*` repositories
   return HTTP 200 with 57 per-subject parquet files carrying per-item `acc`
   vectors. The target substitution (auditing the instrument instead of a
   model) rested on an author search failure, not a property of the world.
2. **The positional finding's BH survival.** P1 and P2 are one statistic, and
   the family used an item-level χ² p-value where the pre-registration declared
   the subject as the resampling unit. With the declared unit, survivors go
   from five to three.
3. **Every printed duplication number.** True item-level rate is 2.357 %, not
   1.253 %.

## What survives

The instrument-level verdict, `DETECTED-BUT-NOT-IDENTIFIED`, is untouched. A
rule with no access to the question text beats chance on MMLU: 28.22 % under
the shipped leave-one-subject-out estimator, 28.87 % under a within-subject
leave-one-out variant, against 25.00 % chance. The excess is **bidirectional** —
`public_relations` runs at 13.64 %, significantly *anti*-predicted — which the
one-sided screen was structurally incapable of reporting.

## Before v1 can ship

- [ ] Retract the availability claim in the body, not only the corrigendum
- [ ] Refit the BH family: five tests, subject-clustered p
- [ ] Disclose sidedness; report the two-sided result and `public_relations`
- [ ] Correct every duplication number
- [ ] Fix the `security_studies` mechanism attribution (len_ratio 0.925 — its
      correct options are *shorter*, contradicting the longest-option narrative)
- [ ] State anchor coverage honestly over all 38 entries
- [ ] Frame the 28.22 % headline as a lower bound
- [ ] Rename P8 to structural well-formedness and cite the label-error
      literature beside it
- [ ] Cite Balepur, Ravichander & Rudinger (2024), arXiv:2402.12483, by name,
      and state this audit's contribution as the framing, not the channel
- [ ] Re-run anchors under protocol 0.3.2 with source bindings

## References

- Balepur, N., Ravichander, A. & Rudinger, R. (2024). *Artifacts or Abduction:
  How Do LLMs Answer Multiple-Choice Questions Without the Question?*
  arXiv:2402.12483
- Gema, A. P. et al. (2025). *Are We Done with MMLU?* NAACL 2025.
  arXiv:2406.04127
- Wang, Y. et al. (2024). *MMLU-Pro.* arXiv:2406.01574
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language
  Understanding.* ICLR 2021. arXiv:2009.03300
