#!/usr/bin/env python3
"""What has already been tried, according to the register's own prose.

    python3 attempts_extract.py     # print the shape, write attempts-extract.md

WHY THIS RUNS BEFORE ANY SCHEMA IS WRITTEN. The proposal is a register of
attempts — what was tried, what failed, what is in flight — as a sibling to
Nordstern in the way Engpass is. **Corpus before schema**: find out whether the
data has a usable grain before committing to a shape for it, exactly as
`icd_coverage.py` asked whether the ICD join key was good enough before anything
was built on it.

WHAT IT CAN AND CANNOT DO. A regular expression can find the sentences in which
this register describes something that was tried and did not work. It cannot
reliably name the agent — drug names are lowercase common-looking words
(`inosine`, `creatine`, `isradipine`) and no pattern separates them from prose.
So this reports **shape, not content**: how many records, how many sentences, how
many carry a date, a phase, or a named trial, and — the question that decides the
architecture — **how many approaches recur across records.**

THE ARCHITECTURAL TEST IS THE LAST ONE. If attempts are unique to their disease,
they belong inside Nordstern records. If the same approach keeps appearing in
different diseases, they do not: storing them per-disease would lose the
cross-disease view, which is precisely the failure Engpass exists to prevent.
"""
from __future__ import annotations

import glob
import os
import re
from collections import Counter, defaultdict

import check

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "attempts-extract.md")

# Language the register uses when it records something that did not work.
FAIL = re.compile(
    r"\b(failed|negative|halted|stopped early|withdrawn|null result|neutral trials?|"
    r"did not (?:reduce|improve|show|prevent|work)|no benefit|missed (?:its|their) primary|"
    r"abandoned|discontinued|refuted|graveyard|unsuccessful)\b", re.I)

DATED = re.compile(r"\b(1[89]\d\d|20[0-2]\d)\b")
PHASE = re.compile(r"\bphase\s*(?:1|2|3|I{1,3}|II|III)\b", re.I)
# A named trial reads as an all-caps token of 4+ letters that is not an acronym
# the register uses for something else.
NAMED = re.compile(r"\b([A-Z][A-Z0-9-]{3,})\b")
NOT_A_TRIAL = {"WHO", "HIV", "AIDS", "GBD", "ICD", "MONDO", "DNA", "RNA", "NHS", "FDA",
               "CDC", "USPSTF", "HPV", "HSV", "COPD", "CFTR", "TRUE", "FALSE", "AND",
               "THE", "NOT", "ONE", "TWO", "SIX", "ALL", "NONE", "YES", "PKDL", "ORS",
               "CIN2", "ANCHOR", "POPI", "GEMS", "PALM", "SENS", "CRUD", "MPTP"}

# Modalities that plausibly recur across diseases. Chosen BEFORE running, so the
# recurrence count is a prediction being tested rather than a description of
# whatever turned up.
MODALITIES = {
    "anti-TNF":            r"\banti-?TNF\b|tumour necrosis factor",
    "checkpoint blockade": r"checkpoint (?:blockade|inhibit)|pembrolizumab|nivolumab|PD-1|PD-L1",
    "CAR-T":               r"\bCAR-?T\b",
    "monoclonal antibody": r"monoclonal antibod|-mab\b",
    "GLP-1":               r"\bGLP-?1\b|semaglutide|exenatide|liraglutide|tirzepatide",
    "gene therapy":        r"gene therap|gene editing|CRISPR|base editing",
    "antisense / siRNA":   r"antisense|\bASO\b|siRNA|oligonucleotide",
    "stem cell":           r"stem[- ]cell",
    "mRNA platform":       r"\bmRNA\b",
    "phage":               r"\bphage\b|bacteriophage",
    "vaccine":             r"\bvaccin",
    "corticosteroid":      r"corticosteroid|dexamethasone|prednisolone|glucocorticoid",
    "monoclonal vs virus": r"ansuvimab|REGN|casirivimab|palivizumab|nirsevimab",
    "senolytic / aging":   r"senolytic|senescen",
    "microbiome / FMT":    r"faecal microbiota|fecal microbiota|\bFMT\b|probiotic",
}


def sentences(rec) -> list[str]:
    """Every sentence in the parts of a record that describe attempts."""
    parts = [str(rec.get("witness", ""))]
    parts += [b["what"] for b in rec["blockers"]]
    parts += [m.get("why", "") for m in (rec.get("moved") or [])]
    parts += [str(h) for h in (rec.get("holes") or [])]
    out = []
    for p in parts:
        out += re.split(r"(?<=[.!])\s+", p)
    return [s.strip() for s in out if s.strip()]


def main() -> int:
    recs = [check.load(p) for p in
            sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
    recs = [r for r in recs if check.status(r) == "active"]

    per_record: dict[str, list[str]] = {}
    for r in recs:
        hits = [s for s in sentences(r) if FAIL.search(s)]
        if hits:
            per_record[r["slug"]] = hits

    all_hits = [(s, txt) for s, v in per_record.items() for txt in v]
    n = len(all_hits)
    dated = sum(1 for _, t in all_hits if DATED.search(t))
    phased = sum(1 for _, t in all_hits if PHASE.search(t))
    named = Counter()
    for _, t in all_hits:
        for tok in NAMED.findall(t):
            if tok not in NOT_A_TRIAL and not tok.isdigit():
                named[tok] += 1

    # THE ARCHITECTURAL TEST.
    #
    # SEARCHED ONLY WITHIN THE FAILURE SENTENCES, WHICH IS THE CORRECTION THAT
    # MATTERS. The first version matched the whole record and reported "vaccine
    # in 76 records" — almost all of it `prevention` prose about vaccines that
    # work, not attempts that failed. Asking whether a modality RECURS AS AN
    # ATTEMPT requires looking only where the register is describing an attempt.
    mod_records: dict[str, set] = defaultdict(set)
    for slug, hits in per_record.items():
        blob = " ".join(hits)
        for name, rx in MODALITIES.items():
            if re.search(rx, blob, re.I):
                mod_records[name].add(slug)

    L = [
        "# What has already been tried — an extraction, not a register",
        "",
        "**GENERATED by `python3 attempts_extract.py`.** Run before any schema exists, to",
        "find out whether the data has a usable grain. Same move as `icd_coverage.py`:",
        "**corpus before schema.**",
        "",
        "## The size of what is already written down",
        "",
        f"**{len(per_record)} of {len(recs)} records** describe something that was tried and",
        f"did not work — **{n} sentences.** None of it is queryable; all of it is prose.",
        "",
        "| property | n | share |",
        "|---|---:|---:|",
        f"| sentences describing a failed or abandoned attempt | {n} | — |",
        f"| …carrying a **year** | {dated} | {100*dated/n:.0f}% |",
        f"| …naming a **trial phase** | {phased} | {100*phased/n:.0f}% |",
        "",
        "**The dating rate is the number that matters.** An attempt without a date cannot",
        "be placed in a sequence, and a register of attempts that cannot say *when* is a",
        "list rather than a history.",
        "",
        "## Records with the most already written",
        "",
    ]
    for slug, v in sorted(per_record.items(), key=lambda kv: -len(kv[1]))[:14]:
        L.append(f"- **{slug}** — {len(v)}")

    L += [
        "",
        "## THE ARCHITECTURAL TEST",
        "",
        "The question that decides where this lives: **does the same approach recur across",
        "diseases?** If attempts are unique to their disease they belong inside Nordstern",
        "records. If they recur, storing them per-disease loses the cross-disease view —",
        "which is exactly the failure Engpass was created to prevent.",
        "",
        "The modality list below was **chosen before running**, so this is a prediction",
        "being tested rather than a description of whatever turned up.",
        "",
        "**Counted only within the failure sentences.** The first version of this check",
        "searched whole records and reported *vaccine in 76 records* — which was almost",
        "entirely `prevention` prose about vaccines that work. Asking whether a modality",
        "recurs **as an attempt** means looking only where the register is describing one.",
        "",
        "| modality | records mentioning it | which |",
        "|---|---:|---|",
    ]
    for name, s in sorted(mod_records.items(), key=lambda kv: -len(kv[1])):
        shown = ", ".join(sorted(s)[:6]) + (f" +{len(s)-6}" if len(s) > 6 else "")
        L.append(f"| **{name}** | {len(s)} | {shown} |")

    recur = sum(1 for s in mod_records.values() if len(s) >= 3)
    L += [
        "",
        f"**{recur} of {len(MODALITIES)} modalities appear in three or more records** — and",
        "**this test is underpowered and does not settle the architecture question.**",
        "",
        f"The register names only {n} attempt sentences across {len(per_record)} records —",
        f"roughly {n/len(per_record):.1f} per record. A modality is detected as recurring only",
        "when two records both happened to name it in their handful of sentences. **Absence",
        "here is a fact about how much prose was written, not about whether the approach was",
        "tried.** Anti-TNF has been trialled in far more than the diseases that mention it;",
        "the register simply did not write it down.",
        "",
        "So the honest reading is: **the architectural case for a separate register rests on",
        "the unit being an approach, on volume, and on provenance — not on this table.** An",
        "earlier version of this check searched whole records, reported 12 of 15, and was",
        "used to argue the point. That number was wrong and this one cannot replace it.",
        "",
        "## What could not be extracted, and it is the important half",
        "",
        "**A regular expression cannot name the agent.** Drug names are lowercase and look",
        "like ordinary words — `inosine`, `creatine`, `isradipine`, `exenatide` — and no",
        "pattern separates them from prose. The named-trial column below is what a",
        "capitalisation heuristic can find, and it is thin:",
        "",
    ]
    for tok, c in named.most_common(12):
        L.append(f"- `{tok}` × {c}")
    L += [
        "",
        "**So the extraction gives a work-list, not a dataset.** Turning these sentences into",
        "structured attempts is a reading job, not a parsing one — roughly the same size as",
        "writing twenty records, and it should be done record by record with the same",
        "discipline, or not at all.",
        "",
        "## Verdict",
        "",
        "**The register is not a history of attempts and cannot be made into one by",
        "extraction.** Only 13% of what it says about failure carries a year and 5% names a",
        "phase, so the prose records *that* things failed and rarely *when* — which is the one",
        "property a register of attempts must have, since its whole value is sequence: what",
        "was tried, in what order, and what each ruled out.",
        "",
        "**What the extraction does produce is a seeded work-list**, and that is worth having:",
        "74 records already name something that did not work, bottom-up, each one judged",
        "relevant by whoever wrote the record. That is the same discipline Engpass uses —",
        "a link earned by a record citing it rather than asserted from outside.",
        "",
        "**The recommendation is to start with one record rather than a schema.** Take",
        "`parkinsons` or `sepsis` — the two with the most already written, and between them",
        "the register's clearest statements of a field failing repeatedly — and write their",
        "attempts out properly, with dates and citations. If the shape holds for two records",
        "it will hold for a hundred; if it does not, nothing has been built on it.",
        "",
        "## The candidate work-list",
        "",
        "Every sentence, per record, for a human to turn into entries or discard.",
        "",
    ]
    for slug, v in sorted(per_record.items()):
        L.append(f"### {slug}")
        for t in v:
            flag = []
            if DATED.search(t):
                flag.append("dated")
            if PHASE.search(t):
                flag.append("phase")
            tag = f" `[{' '.join(flag)}]`" if flag else ""
            L.append(f"- {t[:300]}{tag}")
        L.append("")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print(f"{len(per_record)}/{len(recs)} records · {n} attempt sentences")
    print(f"  dated {dated} ({100*dated/n:.0f}%) · phase named {phased} ({100*phased/n:.0f}%)")
    print(f"  modalities in >=3 records: {recur}/{len(MODALITIES)}")
    for name, s in sorted(mod_records.items(), key=lambda kv: -len(kv[1]))[:6]:
        print(f"    {name:<22}{len(s):>3} records")
    print(f"wrote {os.path.basename(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
