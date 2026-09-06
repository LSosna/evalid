# EVALID Protocol, version 0.3.2

**A pre-registered identifiability protocol for bounding nuisance capacity in
empirical claims.**

| | |
|---|---|
| Version | 0.3.2 |
| Supersedes | 0.3.1 |
| Status | Normative |
| Changes | Three, all listed in §9. All arose from defects found in EVALID's own audits. |

---

## 0. What this protocol is for

An empirical claim of the form *"system S has capability C, evidenced by score
X on instrument I"* can fail in four distinct places:

1. **The instrument** carries a channel that produces X without C.
2. **The estimator** is degenerate with nuisance parameters, so X is not
   attributable to C even if C exists.
3. **The analysis** contains multiplicity, unit, or arithmetic errors.
4. **The claim** was selected after seeing the data.

EVALID addresses all four by requiring that predictions, thresholds and the
resampling unit are fixed in writing before any data are touched, and that the
resulting verdict is whatever the numbers give.

EVALID is not a significance test and does not certify that a capability is
real. It bounds how much of a reported quantity can be produced without the
capability, and reports whether the remainder is identifiable.

---

## 1. Normative language

MUST, MUST NOT, SHOULD and MAY are used in the RFC 2119 sense. A package that
violates a MUST is not an EVALID audit and MUST NOT be described as one.

---

## 2. The pre-registration

Before any data are loaded, a pre-registration document MUST fix:

1. **The object of audit** — the specific claim, instrument, model or corpus,
   named unambiguously, with a content hash where the object is a file.
2. **The author of the object of audit**, and whether that person is also the
   author of the audit. *(New in 0.3.2 — see §9.3.)*
3. **Numbered predictions**, each with a pass condition and a fail condition
   stated as a numeric threshold or an explicit structural criterion.
4. **The resampling unit.** Every interval and every p-value for a given
   quantity MUST use the same unit. Choosing a clustered interval and an
   unclustered p-value for one quantity is a protocol violation, not a
   judgement call.
5. **The multiplicity family** — which tests enter it, and the procedure and
   level (default: Benjamini–Hochberg at q = 0.05).
6. **Test sidedness.** One-sided tests MUST be declared as one-sided. A
   one-sided screen cannot observe effects that run backwards, and the
   pre-registration MUST state whether that blindness is intended.
7. **Deviations policy** — how a deviation discovered during execution will be
   recorded.

The pre-registration MUST be hashed into the release manifest (§6) and MUST NOT
be edited after data are loaded. Registered predictions that turn out to be
invalid are retained and marked, never deleted (§5.2).

---

## 3. Verdict lattice

The lattice is closed. An audit MUST NOT emit a verdict string outside it.
Implementations SHOULD reject unknown verdict strings at write time.

### 3.1 Per-prediction verdicts

| Verdict | Meaning |
|---|---|
| `PASS` | The registered pass condition is met, outside the uncertainty band (§4). |
| `FAIL` | The registered fail condition is met, outside the uncertainty band. |
| `INDETERMINATE` | The measured value lies within the uncertainty band of its threshold. **New in 0.3.2.** |
| `UNDERDETERMINED` | The computation did not meet the numerical admissibility gate (§4.3). **New in 0.3.2.** |
| `REGISTERED_INVALID` | The prediction was registered but its criterion is unsound; the criterion is superseded and the reason recorded. |
| `NOT_RUN` | Registered but not executed; a reason MUST be given. |

`CRITERION INVALID`, used in earlier packages, is a deprecated spelling of
`REGISTERED_INVALID` and MUST NOT be emitted by conforming implementations.

### 3.2 Terminal audit verdicts

| Verdict | Meaning |
|---|---|
| `IDENTIFIED` | The excess is present and attributable to the named mechanism. |
| `DETECTED-BUT-NOT-IDENTIFIED` | The excess is present; the mechanism is not separable from nuisance directions. |
| `LOCALIZED` | The excess is confined to an identified subset of the object. |
| `NONE` | No excess above the registered detection floor; reported with the floor. |
| `ARTIFACT` | The excess is attributable to the measurement apparatus rather than the object. |

A null result MUST be reported with its detection limit: the smallest effect
the registered configuration would have detected at the registered
significance. A bounded null MUST NOT be reported as a proof of zero.

---

## 4. Threshold comparison (new in 0.3.2)

### 4.1 The rule

> **Every quantity compared against a registered threshold MUST ship with a
> numerical uncertainty, and a verdict inside that uncertainty MUST be reported
> as `INDETERMINATE`.**

A threshold comparison without a stated uncertainty is undefined. This is the
central change in 0.3.2.

### 4.2 Estimating the uncertainty

The uncertainty `u` on a computed quantity MUST be estimated by at least one
of the following, and the method MUST be named in the results file:

| Method | Applies to | Procedure |
|---|---|---|
| `grid` | quadratures, integrals | Recompute at ≥3 discretisations spanning a factor of 4; `u` = half-range. |
| `step` | finite-difference derivatives | Recompute across ≥3 step sizes spanning two decades; `u` = half-range. |
| `resample` | statistics over sampled units | Cluster bootstrap at the registered unit; `u` = the interval half-width. |
| `implementation` | quantities with more than one defensible algorithm | Compute by ≥2 independent implementations; `u` = half-range. |

Where more than one applies, `u` is the largest.

Method `implementation` is REQUIRED for any quantity involving a projection,
an orthogonalisation, or a matrix inverse. These are the quantities where two
correct-looking programs disagree, and they are where EVALID's own worst
published defect occurred.

### 4.3 Numerical admissibility gate

Before any quantity derived from a matrix inverse is read, the condition
number MUST be tested against a registered ceiling:

```
cond(M) > ceiling        ->  UNDERDETERMINED, quantity not reported
```

The ceiling MUST be registered in advance. A default of `1e12` is RECOMMENDED
for double-precision work, leaving roughly four significant digits. An audit
MAY register a looser ceiling with a stated justification, and MUST then
report the achieved condition number alongside the quantity.

Exclusions made on this gate MUST be reported. Exclusion decided after seeing
the result, without a registered ceiling, is a deviation and MUST be recorded
as one.

---

## 5. Reporting

### 5.1 Anchors

Every numeric quantity printed in a report MUST appear in an anchors file as a
claimed/recomputed pair, bound to the file and location it was read from:

```json
{
  "id": "P6 max correlation",
  "claimed": 0.99895,
  "source": {"file": "results/p6_corrected.json",
             "json_path": "$.recomputed_max"},
  "tolerance": 1e-5
}
```

The report MUST state anchor coverage as `verified / defined`, where `defined`
is the number of entries in the anchors file, not the number of checks that
were run. `29/29 passed` where the file holds 38 entries is a true sentence
that creates a false impression and MUST NOT be published.

The `source` binding is REQUIRED in 0.3.2. An anchor whose recomputed value is
produced by the same code path that produced the claim verifies nothing.

### 5.2 Corrections

Errors found after publication MUST be logged, not silently repaired. A
correction entry MUST record: what was claimed, what is correct, the mechanism
of the error, whether any verdict changed, and who found it.

The correction log is a first-class deliverable of the protocol. An audit
programme with no corrections is an audit programme that is not being checked.

### 5.3 Prior art

Any method load-bearing for a headline finding MUST be cited by name and
identifier. Where the method is prior art, the audit's contribution MUST be
stated as the audit framing — the pre-registration, the thresholds, the
identifiability verdict — and not as the discovery of the effect.

---

## 6. Release requirements

A conforming release MUST contain:

1. `manifest.json` — SHA-256 of every shipped file, including the
   pre-registration, every results file, every figure and the report itself.
   No result file may exist outside the manifest.
2. `anchors.json` — per §5.1, with source bindings.
3. A reproducer that regenerates every results file from the raw inputs, with
   a `--selftest` mode that runs on synthetic data and requires no network.
4. A dependency manifest with version floors, and import guards that name the
   missing package and the install command.
5. A recorded environment: interpreter and library versions.
6. A determinism statement: every stochastic step seeded, every optimiser
   restart count and achieved-optimum spread recorded.
7. Resolvable links. Authoring-environment placeholders MUST NOT survive into
   a release.

---

## 7. Disclosure

The report MUST name the author of the object under audit. Where the auditor
and that author are the same person, the report MUST say so in its opening
section, not in a footnote.

Self-audit is permitted and is not a weakness of the result. Undisclosed
self-audit is a integrity failure regardless of the quality of the analysis.

---

## 8. Conformance

A package conforms to EVALID 0.3.2 if:

- [ ] Pre-registration exists, is hashed into the manifest, and predates data loading
- [ ] Object of audit and its author are named; self-audit disclosed if applicable
- [ ] Resampling unit declared, and used consistently for every interval and p-value
- [ ] Sidedness declared for every test
- [ ] Multiplicity family declared; each statistic enters exactly once
- [ ] Every threshold comparison carries an uncertainty and a named estimation method
- [ ] Conditioning ceiling registered; exclusions on it reported
- [ ] Every verdict string is in the §3 lattice
- [ ] Nulls reported with detection limits
- [ ] Anchors file complete, source-bound, coverage stated as verified/defined
- [ ] Manifest covers every shipped file
- [ ] Reproducer runs offline in `--selftest`
- [ ] Environment and determinism recorded
- [ ] Load-bearing prior art cited by identifier
- [ ] Corrections logged, not repaired silently

`evalid conform <package>` checks the mechanical subset of this list.

---

## 9. Changes from 0.3.1

### 9.1 `INDETERMINATE` and mandatory threshold uncertainty (§4)

**Origin.** In the GW-SRAG audit, prediction P6 compared a projected
correlation of 0.952 against a registered threshold of 0.95 — a margin of
0.002 — with no stated uncertainty. Independent recomputation returned 0.99895
by three separate methods, and varying only the projection implementation
moved the same quantity by up to 0.096: forty-eight times the margin the
verdict rested on.

The verdict direction survived, which is luck rather than method. Under 0.3.1
a defensible-looking program could have returned 0.948 and flipped the verdict
with no signal that anything was fragile.

**Consequence.** §4 is now normative, and method `implementation` is required
for projections, orthogonalisations and matrix inverses.

### 9.2 Conditioning gate and `UNDERDETERMINED` (§4.3)

**Origin.** The same audit correctly excluded a binary-black-hole case whose
Fisher matrix had condition number 1.9e16, at the double-precision limit — but
the exclusion criterion was chosen after seeing the number, and the primary
case at 4.0e13 was retained without a stated rule.

**Consequence.** The ceiling is now registered in advance and exclusions are a
reported verdict rather than a judgement.

### 9.3 Mandatory disclosure of self-audit (§2.2, §7)

**Origin.** The GW-SRAG audit report referred to the audited framework in the
third person throughout, without stating that the framework was the auditor's
own prior work.

**Consequence.** Authorship of the audited object is now part of the
pre-registration and the report's opening section.

### 9.4 Deprecations

`CRITERION INVALID` → `REGISTERED_INVALID`. Anchors without `source` bindings
are non-conforming in 0.3.2.

---

## 10. Provenance of this version

Every change in §9 originates in a defect found in EVALID's own output, three
of them by reviewers other than the author and one by an independent re-run.
The protocol is revised by being used against its author's work and failing.

That is the intended failure mode, and the correction log is the evidence that
it is working.
