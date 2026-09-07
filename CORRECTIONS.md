# Correction log

Generated from `CORRECTIONS.csv` by `evalid corrections`. Do not edit by
hand -- edit the CSV and regenerate, so the counts quoted elsewhere cannot
drift from the table they claim to summarise.

**Counting rule.** A correction is a confirmed finding that required a change to a shipped claim, number, verdict or stated limitation. Confirmations that something was already correct, and rejected findings, are excluded. Scope 'audit-claim' covers audit content; 'release' covers packaging.

| Metric | Value |
|---|---|
| Corrections to audit claims | 20 |
| — found by someone other than the author | 18 |
| — found by the author | 2 |
| Corrections to the release/packaging | 8 |
| Total entries | 28 |
| Entries whose finder provenance is unresolved | 0 |

| ID | Audit | Claim as shipped | What is correct | Verdict change | Found by | Kind |
|---|---|---|---|---|---|---|
| C-01 | 1 | A defect reported by the verifier was dismissed on inadequate evidence | The defect was real | dismissal retracted | Audit 001 verifier | `external-ai` |
| C-02 | 002-mmlu | Per-item model results are not publicly available for published models | They are; open-llm-leaderboard details_* repos return HTTP 200 with 57 per-subject parquet files | retracts the stated rationale for the target substitution | Review 2 | `external-ai` |
| C-03 | 002-mmlu | Per-subject screen reported without stating it is one-sided | Two-sided BH gives 17 subjects / 4613 items; public_relations at 13.64% is anti-predicted and invisible to the one-sided screen | headline undisclosed as one-sided | Review 2 | `external-ai` |
| C-04 | 002-mmlu | P1 and P2 enter the BH family as two tests | They are one statistic; LOSO selected the same index for all 57 subjects | inflates family size | Review 2 | `external-ai` |
| C-05 | 002-mmlu | BH family used the item-level chi2 p = 6e-10 for P1 | Declared resampling unit is the subject; clustered p = 0.0405 | positional finding loses BH; survivors 5 -> 3 | Review 2 | `external-ai` |
| C-06 | 002-mmlu | 176 items (1.253%) share a stem; 102 exact-repeat groups (204 rows) | 331 items (2.357%); 105 groups (210 rows) | none - P7 fails harder | Review 2 | `external-ai` |
| C-07 | 002-mmlu | security_studies flagged under a longest-option mechanism | len_ratio 0.925 - its correct options are shorter; mechanism mislabelled | mechanism column wrong | Review 2 | `external-ai` |
| C-08 | 002-mmlu | 29/29 anchors passed | 29 of 38 defined anchors were checked; 9 never verified | overstated verification | Review 2 | `external-ai` |
| C-09 | 002-mmlu | Question-blind method presented without prior art | Balepur Ravichander & Rudinger 2024 (arXiv:2402.12483) is the method; contribution is the audit framing | contribution restated | Review 2 | `external-ai` |
| C-10 | 002-mmlu | 28.22% headline presented without framing | LOSO estimator is a handicapped lower bound; within-subject LOO gives 28.87% | headline is a lower bound | Review 2 | `external-ai` |
| C-11 | 002-mmlu | EVALID_AUDIT_002.json ships unhashed beside audit002_results.json | A second source of truth with nothing binding it | divergence risk | Review 2 | `external-ai` |
| C-12 | 002-mmlu | Companion essay citations | MMLU-Pro is Wang et al. arXiv:2406.01574; one 2020 reference unlocatable | essay must be fixed | Review 2 | `external-ai` |
| C-13 | 002-mmlu | P8 'items well-formed' PASS reads as evidence the items are sound | Structural well-formedness only; Gema et al. 2025 put label errors at 6.49% | new stated limitation | Author | `author` |
| C-14 | 002-mmlu | evalid_harness.py runs a hardcoded demo under __main__ | Needs an argparse entry point | release hygiene | Review 1 | `external-ai` |
| C-15 | 002-mmlu | No requirements.txt and no import guards | Dependency manifest and guards required | release hygiene | Review 1 | `external-ai` |
| C-16 | 002-mmlu | Reproducer network-failure path exits with a generic message | Needs manual-download instructions and checksums | release hygiene | Review 1 | `external-ai` |
| C-17 | gw-srag | Registered detectability criterion |dPhi| ~ 1/SNR | Only the component orthogonal to the GR directions is observable; criterion invalid | P4 -> REGISTERED_INVALID superseded by P5 | Author | `author` |
| C-18 | gw-srag | P6 max |rho| = 0.952; family separated above alpha=2.5 down to 0.025 | max |rho| = 0.99895; nothing below 0.769; two alpha above threshold | none - FAIL either way and stronger | Independent re-run | `external-ai` |
| C-19 | gw-srag | BBH excluded on cond(F) = 1.9e16 | Correct exclusion but the criterion was chosen after seeing the number | now a registered UNDERDETERMINED gate | Independent re-run | `external-ai` |
| C-20 | gw-srag | BBH cond number reported as 1.95e16 | Regenerated value is 2.55e16; 1.95e16 came from an orphaned file no code produced | none - gate verdict unchanged | Hostile-referee review | `external-ai` |
| C-21 | gw-srag | SPARC-lambda residual 5.27 sigma; 'reproduces to 5 decimal places' | 5.30 sigma; the 5-decimal claim holds for FF not for the derived sigma | none | Hostile-referee review | `external-ai` |
| C-22 | gw-srag | t4_rest.json ships a separability block holding the retracted v0 P6 values | P6 lives only in p6_corrected.json; the duplicate is retracted | none - recurrence of C-11 | Independent re-run | `external-ai` |
| C-23 | release | reproduce.py --all 'regenerates every results file' | It wrote four of five and overwrote t3_ff.json with a different schema breaking manifest verify | none | Hostile-referee review | `external-ai` |
| C-24 | release | v0.3.2 tag archived to Zenodo as the citable record | Tag predated three fix commits; archive carries DOI/PENDING REPLACE-ME and a rendering typo | none | Independent re-run | `external-ai` |
| C-25 | release | .github/workflows/ci.yml .gitignore .zenodo.json present in the release | Dropped by a web-UI upload; no CI ran on v0.3.2 | none | Independent re-run | `external-ai` |
| C-26 | release | Corrigendum section 8 carried an assistant-authored paragraph published in the author's voice referring to private notes | Removed; present in the v0.3.2 and first-tagged v0.3.4 Zenodo archives and supersedable only by a new version | none | Hostile-referee review | `external-ai` |
| C-27 | release | Correction count stated as 14 with 11 by others | Did not reconcile with the table (10 rows) or the corrigendum (16 findings); count is now derived from CORRECTIONS.csv | none | Hostile-referee review | `external-ai` |
| C-28 | gw-srag | 3-sigma detection limits A_log >= 5.77 (SNR 25) and >= 1.44 (SNR 100) | 6.91 and 1.46; the shipped values extrapolated on a linearity assumption the ladder contradicts (local log-log slope 0.79) | none - the amplitude floor 0.705 still sits below both limits | Independent re-run | `external-ai` |
