# EVALID

**A pre-registered identifiability protocol for bounding nuisance capacity in
empirical claims.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22545297.svg)](https://doi.org/10.5281/zenodo.22545297)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

A claim of the form *"system S has capability C, evidenced by score X on
instrument I"* can fail in four places: the instrument carries a channel that
produces X without C; the estimator is degenerate with nuisance parameters; the
analysis has multiplicity, unit or arithmetic errors; or the claim was chosen
after seeing the data.

EVALID fixes predictions, numeric thresholds and the resampling unit **before**
data are loaded, publishes passes and failures alike, and logs every correction
rather than repairing it silently.

It does not certify that a capability is real. It bounds how much of a reported
quantity can be produced *without* the capability, and reports whether the
remainder is identifiable.

**Protocol spec:** [`protocol/EVALID_v0.3.4.md`](protocol/EVALID_v0.3.4.md)

---

## The worked example is a self-falsification

The audit shipped in this repository is aimed at **the author's own prior
work**. I proposed a logarithmic gravitational-wave dispersion effect derived
from the SRAG/SRLG framework. I then wrote EVALID and pointed it at that
proposal.

Twelve of thirteen registered predictions fail. Three fail fatally and
independently. The full record is in
[`audits/gw-srag/REPORT.md`](audits/gw-srag/REPORT.md), disclosed in its
opening paragraph.

This is the intended use. A protocol for bounding evidence should be able to
demolish its author's own theory, and if it cannot, there is no reason to
believe it will demolish anyone else's.

---

## Install

```bash
pip install -r requirements.txt
pip install -e .
```

Requires Python ≥ 3.10 and **NumPy ≥ 2.0** (`np.trapezoid`). Missing
dependencies raise an error that names the package and the install command.

## Use

```bash
evalid selftest                                    # offline check of the machinery
evalid manifest build  audits/gw-srag              # SHA-256 every shipped file
evalid manifest verify audits/gw-srag              # detect drift and unhashed files
evalid anchors verify  audits/gw-srag/anchors.json --root audits/gw-srag
evalid conform         audits/gw-srag              # protocol section 8, mechanical subset
```

Reproduce the shipped audit:

```bash
python audits/gw-srag/code/reproduce.py --selftest   # offline, synthetic
python audits/gw-srag/code/reproduce.py --all        # regenerates every results file
```

## The library

```python
from evalid import threshold_verdict, benjamini_hochberg, condition_gate

# Protocol section 4: a threshold comparison without an uncertainty is undefined.
r = threshold_verdict(value=0.952, threshold=0.95,
                      uncertainty=0.048, method="implementation")
r.verdict          # 'INDETERMINATE' -- the margin is inside the band
r.margin_in_sigma  # 0.042
```

That example is not hypothetical. It is the exact comparison that produced this
protocol's worst published defect, and the reason version 0.3.2 exists.

| Module | Purpose |
|---|---|
| `evalid.verdicts` | The frozen verdict lattice. Unknown or deprecated strings raise. |
| `evalid.stats` | Threshold comparison with mandatory uncertainty, BH multiplicity, cluster bootstrap, conditioning gate. |
| `evalid.anchors` | Claimed-vs-recomputed verification with source bindings. Reports coverage as verified/defined. |
| `evalid.manifest` | SHA-256 release manifest; detects files shipped outside it. |
| `evalid.cli` | `evalid` command. |

---

## What is new in protocol 0.3.2

Every change originates in a defect found in EVALID's own output.

| Change | Origin |
|---|---|
| **`INDETERMINATE` verdict; mandatory uncertainty on every threshold comparison** | GW-SRAG P6 compared 0.952 against 0.95 — a margin of 0.002 — while the quantity moved by up to 0.096 under a change of implementation alone. |
| **Registered condition-number ceiling; `UNDERDETERMINED` verdict** | The same audit correctly excluded a case at cond(F) = 1.9e16, but chose the criterion after seeing the number. |
| **Mandatory disclosure of self-audit** | The GW-SRAG report referred to the audited framework in the third person without stating it was the auditor's own. |
| **Anchors require source bindings** | MMLU Audit 002 reported "29/29 anchors passed" from a file holding 38 entries. |

---

## Repository layout

```
protocol/EVALID_v0.3.4.md     the normative spec
src/evalid/                   the library and CLI
audits/gw-srag/               worked example: self-falsification (complete)
audits/002-mmlu/              MMLU instrument audit -- RETRACTED, v1 pending
CORRECTIONS.md                the correction log
paper/                        arXiv methodology paper source
```

## Audit status

| Audit | Object | Status |
|---|---|---|
| `gw-srag` | The author's own GW dispersion proposal | **Complete.** 12/13 predictions FAIL. Reproducible end to end. |
| `002-mmlu` | MMLU as an instrument | **Partially retracted.** Corrigendum shipped; v1 not yet written. The v0 report is deliberately **not** in this repository — see [`audits/002-mmlu/STATUS.md`](audits/002-mmlu/STATUS.md). |
| `003` | Per-item model attribution | **Not run.** Listed in [`ROADMAP.md`](ROADMAP.md), not shipped. |

`001` is not in this repository. It was an early determinism audit of the
harness itself, predating the protocol's release requirements; its one
substantive outcome — a real defect the author dismissed and then retracted the
dismissal of — is entry `C-01` in the correction log. There is no conforming
package for it and there will not be one.

A folder for an audit that has not been run would be the same class of
overstatement this protocol exists to catch.

---

## The correction log

[`CORRECTIONS.md`](CORRECTIONS.md) is generated from
[`CORRECTIONS.csv`](CORRECTIONS.csv) by `evalid corrections`, so the totals
quoted anywhere are derived rather than maintained by hand. It currently
records 20 corrections to audit claims — 18 found by someone other than the
author — and 8 to the release itself.

Read the `finder_kind` column before you read the ratio. **Every external
finder in this log was an AI model run adversarially against the artefact; none
was a human reviewer.** This project has had no human peer review. The ratio
measures automated adversarial scrutiny, which we think is worth counting, and
which is not the same thing.

The counting rule and the per-entry finder provenance are in
[`CORRECTIONS.csv`](CORRECTIONS.csv); `evalid corrections` derives the totals so
they cannot drift from the table.

---

## Citing

See [`CITATION.cff`](CITATION.cff). The methodology paper is in `paper/`;
this README will carry its arXiv identifier once posted.

## Licence

MIT. See [`LICENSE`](LICENSE).

Lukas A. Sosna · Independent Researcher ·
[ORCID 0009-0004-1266-9729](https://orcid.org/0009-0004-1266-9729)
