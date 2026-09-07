# Corrigendum to EVALID Audit Report 002

**Status of the report it corrects: PARTIALLY RETRACTED. Do not publish
`EVALID_AUDIT_002.md` in its shipped form through any channel.**

| | |
|---|---|
| Corrects | `EVALID_AUDIT_002.md` (sha256 as listed in that report's §8) |
| Protocol version | 0.3.1 |
| Trigger | Two independent technical reviews, received unsolicited |
| Findings adjudicated | 16 |
| Confirmed against my own data | 15 |
| Rejected | 1 |
| Retracted claims | 1 (load-bearing) |
| Verdict changes | 1 (P1/P2 loses BH significance) |
| Headline verdict | unchanged: DETECTED-BUT-NOT-IDENTIFIED (instrument) |

---

## 0. The one-paragraph version

A reviewer told me the central factual premise of my report was false and
instructed me to check it before anything else. I checked it. It is false. The
report says item-level model results are unavailable; they are publicly
available, including at the exact address the report says returns 404. Every
other checkable claim the two reviews made — fifteen of sixteen findings — also
reproduced against my own saved data. One of my two headline statistical
failures does not survive multiplicity correction once I use the resampling unit
my own pre-registration declared. The instrument-level verdict survives all of
it, and is in one respect stronger than reported.

---

## 1. Retraction: the availability claim (Review 2, finding 1)

### What the report says

In the verdict block:

> requires per-item results, which are not publicly available for published
> models.

And in §"Deviations from the registered brief":

> Item-level result records for published models are not reachable from this
> environment: the `open-llm-leaderboard/details_*` datasets return 404 […]

### What is true

| Address queried | Status |
|---|---|
| `open-llm-leaderboard/details_gpt2` | **200** |
| `open-llm-leaderboard/gpt2-details` | **200** |
| `open-llm-leaderboard/meta-llama__Llama-2-7b-hf-details` | **200** |
| `open-llm-leaderboard-old/details_EleutherAI__pythia-1b-deduped` | **200** |

A hub-wide search returns a large number of further `details_*` repositories.
The dataset-serving API cannot process them (it returns *not-implemented* for
the config listing, which is very likely the error I misread as absence), but a
direct file listing resolves immediately: `details_EleutherAI__pythia-1b-deduped`
contains **57 per-subject parquet files** of original-MMLU records at the
standard 5-shot setting — one per subject, the full set.

I downloaded the astronomy file. It has **152 rows**, matching MMLU astronomy's
item count exactly, and carries the columns `acc`, `gold`, `predictions`, and
per-option continuation log-likelihoods.

**`acc` is a per-item correctness vector.** It is the object EVALID requires. It
was public the entire time.

### What this does to the report

The target substitution — auditing the instrument instead of a model — was
justified in the report on the grounds that the required data did not exist. It
does exist. The substitution therefore rests on **my search failure**, not on a
property of the world. The stated reason is withdrawn.

The report's closing recommendation, that evaluation hosts should publish
per-item correctness vectors, is withdrawn as a recommendation and reissued as
an **acknowledgement**: this host already does, and I did not find it.

### Why this is the worst possible error for this programme to make

EVALID exists to catch claims whose supporting evidence cannot bear their
weight. I published a claim — "the data is not available" — on the evidence of a
single failed query against one API surface, and did not try the direct file
listing that would have refuted it in one call. That is precisely the failure
mode the protocol is built to detect, committed in the document announcing the
protocol.

**A model-level Audit 003 is now possible and is the correct next step.** It is
not a patch to this report; it is the audit this report should have been.

---

## 2. Verdict change: the positional finding loses BH significance

Three findings compound here (Review 2, findings 2–4).

**P1 and P2 are one statistic, not two.** The results file records that the
subject-conditional (leave-one-subject-out) selection chose the same option
index for all 57 subjects. P1 and P2 therefore report an identical accuracy
(26.891%), an identical confidence interval, and an identical clustered
p-value. They entered the confirmatory family as two tests. They are one.

**The family used the wrong p-value.** The BH family was assembled with the
item-level χ² p-value for P1 (6×10⁻¹⁰). My pre-registration declares the
**subject** as the resampling unit, because items within a subject share
authorship and construction. The unit-consistent p-value is the
subject-clustered one: **0.0405**.

**Refitting the family** with those two corrections — five tests, clustered p:

| | Survivors under BH, q = 0.05 |
|---|---|
| As shipped (6 tests, item-level p for P1) | P7, P1, P3, P4, P2 — **five** |
| Corrected (5 tests, clustered p) | P7, P3, P4 — **three** |

**The positional finding does not survive multiplicity control at the
resampling unit I declared.** It was one of the two headline FAILs. The raw
threshold comparison still fails (26.89% against a ≤ 26% registered ceiling),
and the answer key is genuinely non-uniform — 3,222 / 3,462 / 3,582 / 3,776
against 3,510.5 expected — but "survives BH" cannot be claimed for it and the
report claims it.

This is a correction *I* should have caught. Choosing a clustered interval and
then a non-clustered p-value for the same quantity is not a subtle statistical
question; it is an inconsistency inside one row of my own results table.

---

## 3. The per-subject test was one-sided and the report never says so

The report's per-subject screen tests only whether question-blind accuracy runs
**above** chance. The words "one-sided" do not appear in the report.

| Procedure | Subjects flagged | Items |
|---|---|---|
| One-sided (as shipped) | 19 | 5,007 (35.66%) |
| Two-sided | 17 | 4,613 (32.85%) |

The two-sided procedure detects one subject the one-sided procedure cannot see:
**`public_relations`**, at **13.64%** question-blind accuracy on n = 110 —
significantly *anti*-predicted. A metadata-only rule does **worse than chance**
there, which means the channel exists but runs backwards. That is a finding, not
a clean subject, and my test was structurally incapable of reporting it.

**The channel's direction is subject-dependent, and the report presents it as
unidirectional.** On the simple "choose the longest option" rule, **16 subjects
(4,360 items, 31.0% of the split)** sit *below* chance.

Related mislabel: **`security_studies`** is reported as BH-significant with a
correct-to-incorrect option length ratio of **0.925** — its correct options are
*shorter*. It is flagged by a narrative, a table column, and a figure that all
assert a longest-option mechanism. The subject is real; the mechanism attributed
to it is wrong.

---

## 4. The duplication numbers are wrong, and the verdict is stronger than reported

The report states:

> **176 items (1.253%)** share a question stem with another item in the same
> split, against a 0.5% threshold — 155 duplicate groups covering 331 rows.
> Decomposed:
> - **102 groups (204 rows)** are exact repeats […]

Recomputed from the same file (sha256 `74a41822ce7d3def…`, confirmed identical
to the audit manifest; test split N = 14,042 items):

| Quantity | Reported | Correct |
|---|---|---|
| Stem-duplicate groups | 155 | 155 ✓ |
| Rows in those groups | 331 | 331 ✓ |
| **"Items" sharing a stem** | **176 (1.253%)** | **331 (2.357%)** |
| Exact-repeat groups | 102 | **105** |
| Exact-repeat rows | 204 | **210** |

The 176 is the count of rows *beyond one per duplicate group* — the redundancy
count, not the item count. The report labels it "items" and divides it by the
split size to state a rate. **The true item-level duplication rate is 2.357%,
close to double what I published**, against a 0.5% registered threshold.

Direction of the verdict: unchanged. P7 fails, and fails harder. Every printed
number in that finding is nonetheless wrong.

---

## 5. Smaller corrections, all confirmed

**5.1 Verification was overstated.** The report states 29 of 29 anchors passed.
The anchors file contains **38** entries. Twenty-nine passed; nine were never
checked. The claim "29/29" is true and the impression it creates — complete
coverage — is false. This is the second-worst error here, because the anchor
mechanism is the thing I offered as evidence the numbers could be trusted.

**5.2 The headline is a lower bound and does not say so.** The 28.22% figure
comes from a leave-one-subject-out estimator, which handicaps itself by design.
The reviewer's within-subject leave-one-out variant gives **28.87%**. Both are
defensible; presenting only the conservative one without naming it as a floor
understates the channel.

**5.3 A second, unhashed source of truth ships.** `EVALID_AUDIT_002.json`
duplicates values from `audit002_results.json` and appears in neither the
report's file table nor the anchors. Nothing binds them. Either hash it into the
manifest or delete it.

**5.4 Prior art is uncited and load-bearing.** Correcting this properly:

- **Balepur, Ravichander & Rudinger (2024)**, *Artifacts or Abduction: How Do
  LLMs Answer Multiple-Choice Questions Without the Question?*, arXiv:2402.12483.
  This is the question-blind method that produces my central finding. It must be
  cited by name, and my contribution stated as the audit framing — the
  pre-registration, the thresholds, the identifiability verdict — not the
  discovery of the channel.
- **Gema et al. (2025)**, *Are We Done with MMLU?*, NAACL 2025,
  arXiv:2406.04127 — MMLU-Redux, 5,700 manually re-annotated items across all 57
  subjects, estimating **6.49%** of MMLU questions contain errors.
- **Wang et al. (2024)**, *MMLU-Pro*, arXiv:2406.01574. The companion essay
  misattributes this. It also cites a 2020 reference I could not locate at all;
  until it is produced, treat it as fabricated and remove it.

**5.5 A new limitation the reviews did not raise.** My P8 test — "items
well-formed", 0.064%, PASS — checks *structural* well-formedness only: four
options present, none empty, no duplicated options. It says nothing about
whether the answer key is *correct*. Gema et al. put label errors at 6.49%,
roughly a hundred times my P8 rate. A reader can easily take my PASS as
evidence the items are sound. It is not. P8 must be renamed to what it measures
and the label-error literature cited beside it.

---

## 6. Release hygiene (Review 1)

Confirmed, all four:

1. `evalid_harness.py` runs a hardcoded `demo()` under `__main__`. It needs an
   `argparse` entry point (`--selftest`, `--test-parquet`, `--val-parquet`).
2. No `requirements.txt` and no import guards. The shipped archive contains the
   harness, the reproducer, and four ledgers — no dependency manifest.
3. The reproducer's network-failure path exits with a generic message. It needs
   explicit manual-download instructions with the file paths and expected
   checksums. I hit this exact failure twice while preparing this corrigendum.
4. The row-order determinism fix is correct, and closes the residual I disclosed
   in `AUDIT_001_verification_response.md`. Credited.

**Rejected: "95% ready for public release."** Review 1 assessed code hygiene,
competently and within its scope. Review 2 established that the report the code
accompanies contains a false load-bearing claim. Code readiness is not package
readiness. The package is not ready.

---

## 7. What survives

The instrument-level verdict stands, and the corrections do not touch it:

- A rule with **no access to the question text** beats chance on MMLU. Under the
  conservative estimator, 28.22%; under the reviewer's, 28.87%. Chance is 25.00%.
- The excess concentrates by subject rather than spreading uniformly, and it is
  **bidirectional** — a fact the report obscured.
- Within-split duplication is **2.357%**, worse than reported.
- **DETECTED-BUT-NOT-IDENTIFIED (instrument)** is the correct verdict, and the
  corrected multiplicity family still leaves three surviving findings.

What does *not* survive: the reason the audit targeted the instrument, the claim
that the positional finding survives BH, and every printed duplication number.

---

## 8. Attribution and process note

Both reviews were unsolicited and both were substantially correct. Review 2's
first finding is one I could not have been argued out of by assertion — it
required a query, and the reviewer told me to run it rather than telling me the
answer. That is the right way to file a finding against someone who has just
published a protocol about evidence.

Running total across this programme: Audit 001's verifier found a real defect I
dismissed on inadequate evidence, and I retracted that dismissal. Audit 002's
reviewers found fifteen more, including one that invalidates the report's stated
rationale. Every one of these is mine.

I will keep saying the same thing about this, because it is the only defensible
position: an author whose published error rate is zero is an author who is not
being checked. The number that matters is not how many errors are found; it is
whether they are found by someone other than the author, and whether the author
prints them.

**On sequencing.** A report containing a known-false central claim is not fit
to publish in any form. Fix it first. A corrigendum this size argues for
reissuing the corrected report as v1 rather than shipping v0 and correcting
in public.

---

## 9. Required actions before any publication

1. Run **Audit 003** against a real model using the per-item `acc` vectors now
   confirmed available. This is the report that should exist.
2. Reissue Audit 002 with: the availability retraction, the corrected BH family,
   the one-sided disclosure and `public_relations`, the corrected duplication
   numbers, the `security_studies` mechanism fix, honest anchor coverage, the
   P4 lower-bound framing, P8 renamed, and the prior art cited by name.
3. Fix the companion essay's citations. Remove the unlocatable reference.
4. Ship the four release-hygiene items.
5. Re-run the anchor check over all 38 entries and report the true denominator.
