#!/usr/bin/env python3
import collections, csv, re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 8: "eight", 9: "nine",
         18: "eighteen", 20: "twenty", 26: "twenty-six", 27: "twenty-seven",
         28: "twenty-eight", 29: "twenty-nine", 30: "thirty"}

rows = list(csv.DictReader(open(R / "CORRECTIONS.csv", newline="")))
audit = [r for r in rows if r["scope"] == "audit-claim"]
ext = [r for r in audit if r["finder_kind"] != "author"]
kinds = collections.Counter(r["finder_kind"] for r in rows)

# Paper checks
tex = (R / "paper" / "main.tex").read_text()
CHECKS = [
    ("corrections to audit claims", len(audit), r"{w} corrections to audit"),
    ("of those, external",          len(ext),   r"{w} of them found by someone other"),
    ("corrections to the release",  sum(1 for r in rows if r["scope"] == "release"),
                                                r"{w} corrections to the release"),
    ("entries in the log",          len(rows),  r"the {w} corrections in the"),
    ("found by AI",                 kinds["external-ai"], r"{w} were found by AI models"),
    ("found by the author",         kinds["author"],      r"and {w} by the author"),
]

# README checks
readme = (R / "README.md").read_text()
README_CHECKS = [
    ("README audit claims", len(audit), r"records {n} corrections to audit claims"),
    ("README external finders", len(ext), r"— {n} found by someone other than the"),
    ("README release claims", sum(1 for r in rows if r["scope"] == "release"), r"and {n} to the release itself"),
]

bad = 0
print("paper counts vs CORRECTIONS.csv\n")
for name, n, tmpl in CHECKS:
    word = WORDS.get(n)
    if word is None: continue
    phrase = tmpl.format(w=word)
    hit = re.search(phrase.replace(" ", r"\s+"), tex) is not None
    bad += not hit
    print(f"  [{'ok ' if hit else 'FAIL'}] {name:30s} = {n:2d}  expects \"{phrase}\"")

print("\nREADME counts vs CORRECTIONS.csv\n")
for name, n, tmpl in README_CHECKS:
    phrase = tmpl.format(n=n)
    hit = re.search(phrase.replace(" ", r"\s+"), readme) is not None
    bad += not hit
    print(f"  [{'ok ' if hit else 'FAIL'}] {name:30s} = {n:2d}  expects \"{phrase}\"")

print("\n" + ("PASS" if not bad else f"{bad} MISMATCH(ES)"))
sys.exit(0 if not bad else 1)
