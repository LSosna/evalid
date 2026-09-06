# EVALID Audit 002 — Pre-registration

**Registered:** 2026-08-23, before any test statistic was computed on the target data.
**Protocol version:** EVALID v0.3.1 (`EVALID_VERSION = "0.3.1"`).
**Auditor:** Lukas A. Sosna (ORCID 0009-0004-1266-9729).

---

## 1. Target selection, and a declared deviation from the brief

The brief asks for a live third-party **model** capability claim. I cannot audit
one, and the reason is worth registering rather than working around.

EVALID operates on **per-item correctness vectors**. A leaderboard headline
number cannot support any of Steps 3–9: no floor distribution, no cluster
bootstrap, no per-slice interval, no provenance η². Item-level result records for
published models are not reachable from this environment — the
`open-llm-leaderboard/details_*` datasets return 404, HELM's result store is on
the network denylist, and no inference credential is configured, so I cannot
generate a correctness vector by running a model either.

Auditing a model on a number I cannot decompose would be exactly the failure
EVALID exists to name: treating an amplitude as evidence.

**So the target is the instrument, not a model.** This is a narrower claim but a
live, external, third-party one with wider consequence than any single model:

> **Claim under audit (C):** MMLU (`cais/mmlu`, `all/test`, N=14,042) measures
> *multitask language understanding*, such that an aggregate accuracy on it is a
> property of the model under test.
>
> **Rival explanation to be excluded:** some portion of any reported MMLU
> accuracy is attributable to **exploitable structure in the answer key and
> option surface** — properties of the instrument, not of model understanding.

This is EVALID Step 4 (saturated-nuisance ceiling) and Step 5b (provenance
baseline) applied to a benchmark rather than to a model. If the instrument
carries an exploitable nuisance channel, then **every** capability claim measured
on it inherits an open objection, which is a finding about thousands of published
claims rather than one.

What this audit cannot do, stated up front: it cannot issue a verdict on any
model, and it cannot say how much of a *specific* model's score came from the
nuisance channel — only how much is *available* to be absorbed by it.

## 2. Resampling unit — declared before testing

**Subject** (57 values) is the clustering unit, not the item. Items within an
MMLU subject share an author, a source, and a formatting convention, so they
share a coherent error. All intervals are subject-level cluster bootstraps
(n_boot = 2000). Where the item-level interval disagrees with the subject-level
one, both are reported and the disagreement is itself a result.

## 3. Registered predictions

Each carries a numeric pass/fail threshold fixed now. "PASS" means the
instrument is clean on that channel; "FAIL" means an exploitable nuisance channel
exists.

| # | Prediction | Statistic | PASS threshold | FAIL threshold |
|---|---|---|---|---|
| **P1** | The answer key is positionally uniform | accuracy of always choosing the modal correct index | ≤ 0.26 | > 0.26 |
| **P2** | Option position carries no per-subject signal | accuracy of a **subject-conditional** modal-index rule, leave-one-subject-out | ≤ 0.27 | > 0.27 |
| **P3** | Option length carries no signal | accuracy of "choose the longest option" | ≤ 0.28 | > 0.28 |
| **P4** | Combined surface nuisance is bounded | accuracy of the best LOO-fit metadata-only model (position + length rank + subject prior; **no question semantics**) | ≤ 0.30 | > 0.30 |
| **P5** | Step 4 CEILING is applicable to MMLU | harmonic mean cluster size, subject as cluster | ≥ 20 (applicable) | < 20 (INAPPLICABLE) |
| **P6** | No cross-split leakage | exact-duplicate question rate between `test` and `validation` | < 0.5% | ≥ 0.5% |
| **P7** | No within-split duplication | exact-duplicate question rate within `test` | < 0.5% | ≥ 0.5% |
| **P8** | Items are well-formed | share of items with ≠4 choices, an empty choice, or duplicate choices | < 1.0% | ≥ 1.0% |

**Confirmatory family (Step 2):** P1, P2, P3, P4, P6, P7 — six tests carrying
verdict weight, Benjamini–Hochberg at FDR = 0.05. P5 is an applicability
precondition and P8 is descriptive; neither enters the family.

**Chance baseline:** 0.25 (4 options). Every accuracy above is compared to it by
a subject-clustered permutation test, ≥2,000 replicates.

## 4. Bounding the nulls

For every prediction that returns PASS, I will report
`min_detectable_effect(n_subjects=57)` — the smallest excess-over-chance this
design could have detected at 80% power. A PASS without that number is
unfalsifiable and will not be reported as one.

## 5. Verdict mapping, declared in advance

| Outcome | Verdict on the instrument |
|---|---|
| All six confirmatory tests PASS after BH | **NONE** — no exploitable nuisance channel detected at this design's sensitivity |
| Any surface-nuisance test FAILs (P1–P4) | **DETECTED-BUT-NOT-IDENTIFIED** — MMLU accuracy has a non-capability co-owner of known size; every claim measured on it inherits an open objection |
| A duplication test FAILs (P6, P7) | Additionally **contamination channel OPEN** |
| P5 returns < 20 | Step 4 INAPPLICABLE; ceiling objection stays OPEN |

Because the target is an instrument rather than a model, **IDENTIFIED is not
reachable in this audit** and is not claimed. The reachable positive outcome is
NONE (instrument clean on the tested channels).

## 6. Pre-commitment

The result is published whichever way it comes out, including the outcome in
which MMLU is clean on every channel and this audit's headline is "we looked and
found nothing, down to an effect size of X." Analysis code is `audit002_*.py`;
every quoted number resolves to a JSON results file, verified by `check_anchors`
before the report is written.

**Not yet observed at registration time:** the answer-key distribution, any
accuracy statistic, any duplicate count. Observed: the row schema
(`question`, `subject`, `choices`, `answer`), the split sizes (14,042 test /
1,531 validation), and one example row.
