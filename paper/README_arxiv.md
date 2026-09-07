# arXiv submission notes

## What this submission is

A methodology note with one worked example: the protocol, and a pre-registered
audit in which it falsified its author's own gravitational-wave dispersion
proposal, then caught a defect in that audit's own output.

The two additional worked examples that an earlier draft reserved space for —
the MMLU instrument audit and a per-item model attribution audit — are **not**
in this paper. The first is partially retracted and its reissue is outstanding;
the second has not been run. Describing either as forthcoming would be the same
error the paper is about, so they are absent rather than promised.

## Categories

- **Primary:** `stat.ME`
- **Cross-list:** `cs.LG`, `gr-qc`

`gr-qc` matters: the worked example makes a claim about a gravitational-wave
dispersion proposal, and gr-qc referees are the ones equipped to check it.

**Endorsement.** stat.ME requires endorsement for first-time submitters, and
cross-lists are separately moderated. Secure an endorser who has published in
stat.ME before submitting — this is a hard gate, not a formality, and an
un-endorsed submission simply sits. Expect moderation to consider
`physics.data-an` or `cs.LG` as alternative primaries for a short
single-example methodology note; either is an acceptable outcome.

## Build

```bash
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

`orcidlink` needs TeX Live 2021+. If the arXiv build errors on it, delete the
`\usepackage{orcidlink}` line and the `\,\orcidlink{...}` in the author block;
the ORCID remains in the affiliation line.

## Upload

Source archive: `main.tex`, `refs.bib`, `figures/`, and `main.bbl` — include
the `.bbl` so the build does not depend on arXiv resolving `plainurl.bst`. Do
not upload a pre-built PDF. `\date` is fixed rather than `\today`, so rebuilds
do not silently re-date the paper.

## Pre-flight

- [ ] `grep -n 'todo{' main.tex` returns nothing
- [ ] Concept DOI (not the version DOI) cited in the paper, README and CITATION.cff
- [ ] A GitHub *release* exists for the tag, so Zenodo actually minted the version
- [ ] `evalid conform audits/gw-srag` passes
- [ ] `evalid corrections ../CORRECTIONS.csv` totals match every prose mention
- [ ] Every number in the paper is anchored, or is explicitly flagged as not anchored
- [ ] Competing-interests statement names the self-audit
- [ ] Use-of-AI-tools statement present, and the finder-provenance claim in it is true
- [ ] Balepur et al. cited wherever a question-blind result appears
- [ ] Endorser secured
- [ ] **One paragraph of your own history added to §3.1 or the disclosure**, in
      the first person and specific: where the theory came from, when you
      decided to point the protocol at it, what the twelve failures looked like
      from the inside. Deliberately not drafted for you — a paragraph written
      by a model about your experience is the one thing in this paper that
      would actually be dishonest. It is also the paragraph no reader will
      mistake for a model.
- [ ] Finder provenance resolved in `CORRECTIONS.csv` — every
      `external-unspecified` changed to `external-human` or `external-ai`
      (see the note at the end of this file)

## Order of operations

Tag → **create a GitHub release** (this is the step that fires the Zenodo
webhook; a bare tag does not) → let Zenodo mint the version → put the *concept*
DOI in the paper → then post. The concept DOI always resolves to the latest
version; a version DOI freezes a reader on whatever snapshot you happened to
cite.


## The one thing only you can resolve

`CORRECTIONS.csv` marks most entries `finder_kind: external-unspecified`. The
paper's quality metric — corrections found by someone other than the author —
is only a claim about scrutiny if that column is filled in.

What is already known: entry **C-18** (the P6 correlation table), **C-19** (the
post-hoc conditioning criterion), **C-22** (the retracted P6 values still
shipping inside `t4_rest.json`), **C-24**, **C-25** and **C-28** were found by
an AI model run against the artefact, and are marked `external-ai`. The
"Reviewer 1", "Reviewer 2", "Audit 001 verifier" and "hostile-referee review"
entries are marked `external-unspecified` because only you know what they were.

If those were also model runs, the honest wording is "found by an independent
process other than the author" or "found by automated adversarial review", not
"found by someone other than the author" — and the paper should say plainly
that the programme has not yet been through human peer review. That is still a
real and unusual claim. It is just a different one, and a referee who works it
out first will treat the original wording as the finding.
