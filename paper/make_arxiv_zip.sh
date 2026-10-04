#!/usr/bin/env bash
# Build the arXiv source archive from the CURRENT sources.
#
# The archive is deliberately NOT committed. A build artifact in git goes stale
# silently: an earlier version of this repository shipped an arxiv_submission.zip
# whose main.tex still carried a superseded DOI and two provenance statements
# that the working copy had already corrected. Uploading it would have submitted
# the wrong paper. Build it at submission time instead.
set -euo pipefail
cd "$(dirname "$0")"

command -v pdflatex >/dev/null || { echo "pdflatex not found"; exit 1; }
rm -f main.aux main.bbl main.blg main.log main.out arxiv_submission.zip
pdflatex -interaction=nonstopmode main.tex >/dev/null
bibtex main >/dev/null
pdflatex -interaction=nonstopmode main.tex >/dev/null
pdflatex -interaction=nonstopmode main.tex >/dev/null

if grep -qE 'Warning.*[Uu]ndefined' main.log; then
  echo "refusing to build: undefined references or citations"; grep -E 'Warning.*[Uu]ndefined' main.log; exit 1
fi
if grep -q 'todo{' main.tex; then echo "refusing to build: \\todo markers remain"; exit 1; fi

zip -q arxiv_submission.zip main.tex refs.bib main.bbl figures/*
echo "built arxiv_submission.zip:"; unzip -l arxiv_submission.zip | tail -n +4 | head -n -2
echo
echo "DOI(s) referenced: $(grep -o 'zenodo\.[0-9]*' main.tex | sort -u | tr '\n' ' ')"
echo "Check that against the record you intend to cite before uploading."
