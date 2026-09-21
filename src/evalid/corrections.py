"""The correction log, counted by code rather than by hand.

Protocol §5.2 makes the correction log a first-class deliverable, and the
paper proposes the external-finder ratio as a quality metric for audit
programmes. A metric quoted in four documents from a table maintained by hand
will drift -- it did, across three different numbers, which is the same shape
as the "29/29 passed from a file of 38" error this programme already retracted.

So the count is derived from CORRECTIONS.csv here, written into
corrections_summary.json, and anchored like every other number.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path

COUNTING_RULE = (
    "A correction is a confirmed finding that required a change to a shipped "
    "claim, number, verdict or stated limitation. Confirmations that something "
    "was already correct, and rejected findings, are excluded. Scope "
    "'audit-claim' covers audit content; 'release' covers packaging."
)

#: How a finding's discoverer is classified. See the note on `external-ai`.
FINDER_KINDS = {
    "author",                 # found by the author of the audited claim
    "external-human",         # found by a named or anonymous person
    "external-ai",            # found by an AI model run against the artefact
    "external-unspecified",   # provenance not yet resolved by the author
}

REQUIRED_COLUMNS = {"id", "date", "audit", "claim_as_shipped", "what_is_correct",
                    "verdict_change", "finder", "finder_kind", "scope"}


@dataclass(frozen=True)
class Summary:
    total_entries: int
    audit_claim_total: int
    audit_claim_external: int
    audit_claim_author: int
    release_total: int
    by_finder_kind: dict
    unresolved_provenance: int
    counting_rule: str

    def to_dict(self) -> dict:
        return asdict(self)


def load(path: str | Path) -> list[dict]:
    rows = list(csv.DictReader(open(Path(path), newline="")))
    if not rows:
        raise ValueError("correction log is empty")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise ValueError(f"correction log missing columns: {sorted(missing)}")
    for r in rows:
        if r["finder_kind"] not in FINDER_KINDS:
            raise ValueError(
                f"{r['id']}: finder_kind {r['finder_kind']!r} not in {sorted(FINDER_KINDS)}")
        if r["scope"] not in {"audit-claim", "release"}:
            raise ValueError(f"{r['id']}: scope {r['scope']!r} not recognised")
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        dupes = [i for i, n in Counter(ids).items() if n > 1]
        raise ValueError(f"duplicate correction ids: {dupes}")
    return rows


def summarise(path: str | Path) -> Summary:
    rows = load(path)
    audit = [r for r in rows if r["scope"] == "audit-claim"]
    ext = [r for r in audit if r["finder_kind"] != "author"]
    kinds = Counter(r["finder_kind"] for r in rows)
    return Summary(
        total_entries=len(rows),
        audit_claim_total=len(audit),
        audit_claim_external=len(ext),
        audit_claim_author=len(audit) - len(ext),
        release_total=sum(1 for r in rows if r["scope"] == "release"),
        by_finder_kind=dict(sorted(kinds.items())),
        unresolved_provenance=kinds.get("external-unspecified", 0),
        counting_rule=COUNTING_RULE,
    )


def write_summary(csv_path: str | Path, out: str | Path) -> Path:
    out = Path(out)
    out.write_text(json.dumps(summarise(csv_path).to_dict(), indent=1) + "\n")
    return out


def render_markdown(csv_path: str | Path) -> str:
    """Render CORRECTIONS.md from the CSV, so the prose cannot drift from it."""
    rows = load(csv_path)
    s = summarise(csv_path)
    head = [
        "# Correction log",
        "",
        "Generated from `CORRECTIONS.csv` by `evalid corrections`. Do not edit by",
        "hand -- edit the CSV and regenerate, so the counts quoted elsewhere cannot",
        "drift from the table they claim to summarise.",
        "",
        f"**Counting rule.** {COUNTING_RULE}",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Corrections to audit claims | {s.audit_claim_total} |",
        f"| — found by someone other than the author | {s.audit_claim_external} |",
        f"| — found by the author | {s.audit_claim_author} |",
        f"| Corrections to the release/packaging | {s.release_total} |",
        f"| Total entries | {s.total_entries} |",
        f"| Entries whose finder provenance is unresolved | {s.unresolved_provenance} |",
        "",
    ]
    if s.unresolved_provenance:
        head += [
            f"> **{s.unresolved_provenance} entries are marked `external-unspecified`.** "
            "Until the author records whether each",
            "> finder was a person or an AI model run against the artefact, the "
            "external-finder ratio",
            "> above is not a quotable claim about human peer review. See "
            "`finder_kind` in the CSV.",
            "",
        ]
    head += ["| ID | Audit | Claim as shipped | What is correct | Verdict change | Found by | Kind |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        head.append("| {id} | {audit} | {claim_as_shipped} | {what_is_correct} | "
                    "{verdict_change} | {finder} | `{finder_kind}` |".format(**r))
    return "\n".join(head) + "\n"
