# Roadmap

Nothing on this list is shipped. It is here so that the absence of a folder is
a stated plan rather than an oversight.

## Audit 003 — per-item model attribution

**Status: not run.**

MMLU Audit 002's corrigendum established that per-item correctness vectors for
published models are publicly available:
`open-llm-leaderboard-old/details_EleutherAI__pythia-1b-deduped` holds 57
per-subject parquet files at the standard 5-shot setting, with columns `acc`,
`gold`, `predictions` and per-option continuation log-likelihoods. The
astronomy file has 152 rows, matching MMLU astronomy exactly.

That makes the audit this programme has not yet done possible: not *"is the
instrument leaky"* but *"how much of a specific published model's score is
attributable to the instrument's non-semantic channel rather than to the
capability claimed."*

It must be pre-registered before the parquet files are loaded, under protocol
0.3.2, with the resampling unit, sidedness, multiplicity family, threshold
uncertainties and conditioning ceiling all fixed in advance.

## MMLU Audit 002 v1

See `audits/002-mmlu/STATUS.md` for the completion checklist.

## Protocol

- A conformance test suite that a third party can run against any package
  claiming EVALID compliance.
- Extension of the identifiability machinery beyond linear/Fisher settings.

## Explicitly not planned

**Repairing SRAG by deriving its distance scaling.** The audit's §9 explains
what such a derivation would need to show, and notes that in the current
functional form it makes the predicted effect larger and therefore more
excluded, not less. That work belongs to whoever wants to defend the theory.
This repository is the instrument, not the theory.
