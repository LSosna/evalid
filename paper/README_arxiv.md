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

**Navigating the category picker.** The submission form opens on whichever
archive group your account defaults to; if that is physics, the "Choose
archive" dropdown lists Astrophysics, Condensed Matter, General Relativity and
Quantum Cosmology and so on, and `stat.ME` is not among them. Change the
archive itself to **Statistics** first — the Subject Class dropdown then
repopulates and offers **Methodology (stat.ME)**. Cross-lists are entered on
the following page, not on this one.

**Endorsement.** stat.ME requires endorsement for first-time submitters, and
cross-lists are separately moderated. Secure an endorser who has published in
stat.ME before submitting — this is a hard gate, not a formality, and an
un-endorsed submission simply sits. Expect moderation to consider
`physics.data-an` or `cs.LG` as alternative primaries for a short
single-example methodology note; either is an acceptable outcome.

## Build the source archive

Run `./make_arxiv_zip.sh`. It rebuilds from the current sources, refuses to
build if any citation is undefined or a `\todo` marker survives, and prints the
DOI the paper cites so you can check it against the record you mean. The zip is
gitignored on purpose -- a committed one goes stale and there is no signal when
it does.

## Build by hand

```bash
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

`orcidlink` needs TeX Live 2021+. If the arXiv build errors on it, delete the
`\usepackage{orcidlink}` line and the `\,\orcidlink{...}` in the author block;
the ORCID remains in the affiliation line.

## Upload

Source archive: `main.tex`, `refs.bib`, `figures/`, and `main.bbl` — include
the `.bbl` so the bibliography does not depend on a remote BibTeX run. The
style is `plain`, which is in every TeX distribution; an earlier draft used
`plainurl`, which is not. Do
not upload a pre-built PDF. `\date` is fixed rather than `\today`, so rebuilds
do not silently re-date the paper.

## Pre-flight

- [ ] `grep -n 'todo{' main.tex` returns nothing
- [ ] DOI cited in the paper, README and CITATION.cff points at the **current**
      record, not a superseded one
- [ ] Zenodo records are linked as versions of one another (see below), or the
      paper says which single record it means
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


## Which DOI to cite

Cite the **concept DOI**, `10.5281/zenodo.22545296`. Zenodo mints it once per
record series; it always resolves to the newest version, so a reader who
follows it a year from now lands on whatever is current rather than on the
snapshot that happened to exist when the paper was written. It is shown on any
version's page under "Cite all versions?".

The per-version DOIs (`22545297` for v0.3.2, `22553660` for v0.3.3,
`22649089` for v0.3.4, and one per release after that) are the right thing to
cite only when you mean that exact snapshot — for example in a correction entry
that says which archive contained a defect.

*An earlier revision of this file asserted that the records were unlinked and
that no concept DOI existed. That was wrong: the Versions panel lists all
releases and shows the concept DOI. The claim came from a single automated read
of the record page that missed the panel, and was published without a second
check — logged as `C-29`.*
