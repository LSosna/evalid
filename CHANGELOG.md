# Changelog

## 0.3.3 — 2026-09-06

Release hygiene only. No protocol or result changes; every number is unchanged.
Cut because the v0.3.2 tag archived a pre-fix snapshot.

### Fixed
- `.github/workflows/ci.yml`, `.gitignore` and `.zenodo.json` were absent from
  the v0.3.2 tag (dropped by a web-UI upload), so no CI ran on the release.
- `CITATION.cff` pointed at `github.com/REPLACE-ME/evalid`; now the real
  repository, with the Zenodo DOI recorded.
- A line-wrap in `paper/main.tex` rendered "0.0405 a nd cost the finding" in
  the compiled PDF.
- Restored the explicit statement that question-blind results use Balepur et
  al.'s method rather than ours. Deleting it weakened the attribution this
  programme was corrected on (finding R2-8).
- The paper pointed readers to "Audit 002 in the accompanying repository"; the
  v0 report is deliberately not shipped, so the pointer now names the
  corrigendum and correction log.

## 0.3.2 — 2026-09

Every change originates in a defect found in EVALID's own output. See
`protocol/EVALID_v0.3.2.md` §9 and `CORRECTIONS.md`.

### Added
- `INDETERMINATE` verdict for values inside the uncertainty band of a threshold.
- Mandatory numerical uncertainty on every threshold comparison, with four
  named estimation methods (`grid`, `step`, `resample`, `implementation`).
  Method `implementation` is required for projections, orthogonalisations and
  matrix inverses.
- `UNDERDETERMINED` verdict and a registered condition-number ceiling.
- Mandatory disclosure where the auditor is also the author of the audited
  object.
- Anchors now require `source` bindings; coverage is reported as
  verified/defined.
- A working library and CLI: `evalid selftest | manifest | anchors | conform`.
- `requirements.txt`, import guards, packaging, CI.

### Changed
- The verdict lattice is frozen and enforced at write time.

### Deprecated
- `CRITERION INVALID` → `REGISTERED_INVALID`. Emitting the old spelling raises.

### Fixed
- GW-SRAG P6 correlation table. Shipped max 0.952; correct value 0.99895 by
  four independent methods. Verdict direction unchanged (`FAIL`). Figure 1
  panel (d) redrawn.

## 0.3.1
- Protocol as used for MMLU Audit 002. Superseded.
