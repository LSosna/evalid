# arXiv submission notes

## Status: NOT READY TO POST

`main.tex` compiles and every number in it is verified and anchored. Two
sections are deliberately unwritten, and posting before they exist would
reproduce the exact failure this protocol is about.

| Blocker | Why it blocks |
|---|---|
| §5 (MMLU worked example) | Audit 002 v0 is partially retracted. Citing a retracted report in a paper about audit integrity is not survivable. Checklist: `audits/002-mmlu/STATUS.md`. |
| §6.3 (cross-domain) | Audit 003 has not been run. Describing it as forthcoming is a promise, not a result. Either run it or cut the paragraph. |

**Do not describe unrun work as forthcoming.** MMLU Audit 002's worst error was
a claim published on the strength of a single unverified query. A paper that
advertises two audits it has not completed is the same error in a different
register.

### The minimum honest submission

If you want to post sooner, there is a version that is ready today: drop §5 and
§6.3, retitle around the single worked example, and submit as a methodology
note. It is shorter and it is completely defensible. The three-example version
is stronger — but only once the three examples exist.

## Categories

- **Primary:** `stat.ME` (methodology)
- **Cross-list:** `cs.LG`, `gr-qc`

`gr-qc` matters: the worked example makes a claim about a gravitational-wave
dispersion proposal and gr-qc referees are the ones equipped to check it. Do
not cross-list `astro-ph.IM` unless §5 lands and the paper genuinely spans
instrumentation.

## Build

```bash
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Needs `orcidlink` (TeX Live 2021+). If your arXiv build errors on it, delete
the `\usepackage{orcidlink}` line and the `\,\orcidlink{...}` in the author
block; the ORCID stays in the affiliation line.

## Upload

Submit as a source archive: `main.tex`, `refs.bib`, `figures/`. arXiv runs
BibTeX itself; include `main.bbl` as well if the build is fragile. Do **not**
upload a pre-built PDF.

## Pre-flight

- [ ] §5 written from Audit 002 v1, or cut
- [ ] §6.3 written from Audit 003, or cut
- [ ] Repository URL and Zenodo DOI filled in (both `\todo` markers)
- [ ] No `\todo` macros survive — `grep -n 'todo{' main.tex` returns nothing
- [ ] `evalid conform audits/gw-srag` passes
- [ ] `evalid anchors verify` reports N/N verified/defined
- [ ] Every number in the paper appears in an anchors file
- [ ] Competing-interests statement present and names the self-audit
- [ ] Balepur et al. cited by name wherever the question-blind method appears
- [ ] Zenodo DOI minted **before** posting, so the paper can cite it

## Order of operations

Mint the Zenodo DOI from a tagged GitHub release first, then post to arXiv
citing that DOI. Doing it the other way round leaves the paper pointing at a
moving repository.
