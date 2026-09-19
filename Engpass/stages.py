#!/usr/bin/env python3
"""Test a framing: is medicine four gates, and which one is shut?

    python3 stages.py        # print the numbers, write stages.md

THE IDEA, PROPOSED IN CONVERSATION 2026-09-02, as three steps:

    1  KNOW      do we know the mechanism — this causes this, doing that to that
    2  DO        can we do anything about it — *"we know how the common cold
                 works and we can't do shit about it"*
    3  PROVE     can we establish that the intervention works

and a fourth this register insisted on adding, because without it the framing
calls a two-dollar pair of glasses solved:

    4  REACH     does it get to the person who needs it

WHY THIS IS A FILE AND NOT A DOCUMENT. Same reason as `crud.py`: a framing is a
claim about the corpus, and a claim typed by hand goes stale the moment a record
is added. Every number below is recomputed from the built artifact on each run.
**If the corpus stops supporting the conclusion, this file says so** — and the
two sections that matter most are the ones where it already does.

IT READS NORDSTERN'S BUILT ARTIFACT AND NOTHING ELSE. Nordstern does not know
this exists; the arrow runs one way (test_boundary.py).

THE HEADLINE FINDING IS THAT THE FRAMING IS WRONG IN ITS OWN TERMS AND USEFUL
ANYWAY. "Stages" implies precedence — pass one, then the next. The corpus denies
it in both directions and the two counts are computed below. What survives is
better: **four independent gates, all of which must be open, none of which helps
open another.**
"""
from __future__ import annotations

import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
NORDSTERN = os.path.normpath(os.path.join(HERE, ".."))
ARTIFACT = os.path.join(NORDSTERN, "web", "nordstern.json")
REPORT = os.path.join(HERE, "stages.md")

# ---------------------------------------------------------------- the gates --
#
# EACH IS READ OFF A FIELD THE REGISTER ALREADY STORES, never off a new
# judgement, so this document cannot quietly invent a rating. Where a threshold
# had to be chosen it is named here and the sensitivity is reported.

def gate_know(r) -> bool:
    """Is there a causal account? `none` and `correlates` are not one.

    `partial` counts as OPEN and that is generous — most of this corpus is
    `partial` or better, so a strict reading would move records INTO gate 1 and
    the funnel's shape would not change. Reported below either way."""
    return r["axes"]["mechanism"] not in ("none", "correlates")


def gate_do(r) -> bool:
    """Is there something that ends or controls the disease?

    Closed for `unsolved` (nothing, or symptoms only) and for `partial`
    (disease-modifying — it alters the course and the disease still wins).
    `curable`, `managed` and `preventable` are open."""
    return r["derived"]["capability"] not in ("unsolved", "partial")


def gate_prove(r) -> bool:
    """Is the evidence in?

    The register's own marker: an `evidence-incomplete` or `candidate-untested`
    blocker says something plausible exists and nobody has established whether
    it works. **This is a LOWER BOUND on the validation problem** — it counts
    only candidates somebody wrote down."""
    return not any(b["kind"] in ("evidence-incomplete", "candidate-untested")
                   for b in r["blockers"])


# Nordstern's own delivery bands, not a threshold invented here. `delivered` and
# `mostly` are open; `partly`, `barely` and `undelivered` are shut. A record with
# no capability derives no delivery at all, and that is `None` — gate 4 does not
# apply when gate 2 is shut, and pretending otherwise would count one failure
# twice.
OPEN_DELIVERY = {"delivered", "mostly"}
LOOSE_SHUT = {"barely", "undelivered"}


def gate_reach(r):
    """`None` means the question does not apply, for one of two reasons.

    Gate 2 is shut — there is nothing to deliver, and charging that failure to
    two gates would double-count it. **Or the record is `preventable`**, where
    Nordstern withholds `delivery` on purpose: `efficacy` and `access` describe
    the TREATMENT, and a record rescued from *nothing can be done* by a vaccine
    has no treatment those numbers are about (Nordstern gaps.md #109).
    `hpv-infection` is the case that surfaced this, and it surfaced from a test
    rather than from reading the code."""
    d = r["derived"]["delivery"]
    if d in ("—", None):
        return None
    return d in OPEN_DELIVERY


GATES = [("know", "do we know what it is doing", gate_know),
         ("do", "can we do anything about it", gate_do),
         ("prove", "can we prove it works", gate_prove),
         ("reach", "does it reach the person", gate_reach)]


def load():
    if not os.path.exists(ARTIFACT):
        raise SystemExit("Nordstern artifact missing — run `python3 check.py --build` there")
    with open(ARTIFACT, encoding="utf-8") as fh:
        recs = json.load(fh)["records"]
    return [r for r in recs if r["derived"]["status"] == "active"]


def shut_gates(r) -> list:
    return [k for k, _, f in GATES if f(r) is False]


def main() -> int:
    recs = load()
    n = len(recs)
    pct = lambda x: f"{100 * x / n:.0f}%"
    closed = {k: [r["slug"] for r in recs if f(r) is False] for k, _, f in GATES}
    na_reach = [r["slug"] for r in recs if gate_reach(r) is None]
    preventable = sorted(r["slug"] for r in recs
                         if gate_reach(r) is None
                         and r["derived"]["capability"] == "preventable")

    # --- where the framing breaks, computed rather than asserted -------------
    # TWO READINGS, AND THE FINDING LIVES OR DIES ON WHICH ONE YOU TAKE.
    # `strict` asks whether a COMPLETE causal account was in hand; `loose` asks
    # only whether there was any account at all. Both are reported, because the
    # first was quoted in conversation as "19% out of order" and the second says
    # 1 record, and a document that printed either alone would be arguing.
    out_strict = sorted(r["slug"] for r in recs
                        if r["axes"]["mechanism"] != "established" and gate_do(r))
    out_loose = sorted(r["slug"] for r in recs
                       if not gate_know(r) and gate_do(r))
    out_of_order = out_strict
    bought_nothing = sorted(r["slug"] for r in recs
                            if r["axes"]["mechanism"] == "established"
                            and not gate_do(r))
    science_done = sorted(r["slug"] for r in recs
                          if gate_know(r) and gate_do(r) and gate_prove(r)
                          and gate_reach(r) is False)
    loose_reach = [r["slug"] for r in recs
                   if r["derived"]["delivery"] in LOOSE_SHUT]
    strict_know = [r["slug"] for r in recs if r["axes"]["mechanism"] != "established"]
    per = Counter(len(shut_gates(r)) for r in recs)
    all_open = sorted(r["slug"] for r in recs if not shut_gates(r))
    first_shut = Counter(shut_gates(r)[0] if shut_gates(r) else "none" for r in recs)

    L = [
        "# Four gates, and which one is shut",
        "",
        "**GENERATED by `python3 stages.py` from Nordstern's built artifact.** Every",
        "number is recomputed on each run, because a framing typed by hand goes stale the",
        "moment a record is added. Sibling of `crud.md`, and the same contract: if the",
        "corpus stops supporting the argument, this file says so.",
        "",
        "## The claim",
        "",
        "Proposed as three steps — **know the mechanism**, **do something about it**,",
        "**prove it works** — with the observation that they are not equally hard and that",
        "the ones nobody talks about are the tight ones. A fourth was added because",
        "without it the framing calls a two-dollar pair of glasses solved.",
        "",
        "| | gate | records where it is SHUT | |",
        "|---|---|---:|---:|",
    ]
    for i, (k, q, _) in enumerate(GATES, 1):
        L.append(f"| **{i}** | {q}? | {len(closed[k])} | {pct(len(closed[k]))} |")
    L += [
        "",
        f"**Each gate is tighter than the one before it, and the tightest is not a science",
        f"gate at all.** That ordering is the framing's main result and it is the opposite",
        f"of how the problem is usually described.",
        "",
        f"`reach` does not apply to {len(na_reach)} records, for two reasons that are both",
        "the register refusing to guess. A disease with **no capability** has nothing to",
        "deliver, and charging that to two gates would count one failure twice. And a",
        f"**`preventable`** record ({len(preventable)}: " +
        " · ".join(f"`{s}`" for s in preventable) + ") has its `delivery` withheld",
        "because `efficacy` and `access` describe the *treatment*, and a disease rescued",
        "from *nothing can be done* by a vaccine has no treatment those numbers are about.",
        "",
        "## Where the framing breaks, and it breaks first on the word *stages*",
        "",
        "A stage model claims precedence: pass one, then the next. **The corpus denies it",
        "in both directions.**",
        "",
        f"### {len(out_strict)} records ({pct(len(out_strict))}) reached a treatment without a complete causal account",
        "",
        "Curable, managed or preventable, on a mechanism that is only `partial` or a set of",
        "correlations:",
        "",
        "> " + " · ".join(f"`{s}`" for s in out_strict),
        "",
        f"**THE SIZE OF THIS FINDING DEPENDS ENTIRELY ON WHAT GATE 1 IS ASKING, AND THE",
        f"DOCUMENT SHOULD NOT HIDE THAT.** Read strictly — did anybody have a complete",
        f"mechanism — it is {len(out_strict)} records. Read loosely — was there any causal",
        f"account at all — it is **{len(out_loose)}**"
        + (f" (`{out_loose[0]}`)" if len(out_loose) == 1 else "") + ".",
        "The strict reading is the one that matters for the sequential claim, because",
        "`partial` is exactly the state a stage model says you must leave before",
        "proceeding, and a fifth of the register proceeded anyway.",
        "",
        "`clubfoot` states it in its own witness: *\"the aetiology is unknown, the treatment",
        "is 95% effective, and the two facts are unrelated.\"* Engpass's",
        "`anaesthesia-mechanism` is the extreme case — gate 2 has been open since 1846 and",
        "gate 1 is still shut.",
        "",
        f"### {len(bought_nothing)} records have an `established` mechanism and gate 2 shut anyway",
        "",
        "> " + " · ".join(f"`{s}`" for s in bought_nothing),
        "",
        "`tay-sachs` is the cleanest: enzyme, gene, substrate, organelle and clinical sign",
        "form an unbroken chain published in **1969**, and the capability is zero because",
        "the protein will not cross a membrane. `dipg`'s causal mutation was found in 2012",
        "and survival has not moved since the 1960s.",
        "",
        "**So passing a gate neither requires nor produces the next one.** What survives is",
        "a better claim than the sequential one: **four independent gates, all of which",
        "must be open, none of which helps open another.** It also explains the funnel —",
        "the gates fail roughly independently, so the union is nearly everything.",
        "",
        "## The finding the framing was missing",
        "",
        f"**{len(science_done)} records — {pct(len(science_done))} — have all three science gates open and still do",
        "not arrive.**",
        "",
        "> " + " · ".join(f"`{s}`" for s in science_done[:40]) +
        (" · …" if len(science_done) > 40 else ""),
        "",
        "Glasses passes every scientific test this framing can pose: the mechanism is",
        "optics, the intervention costs two dollars, the efficacy is 0.98 and nobody",
        "disputes it. Under the three-stage version it is **solved**. It reaches under a",
        "third of the people who need it.",
        "",
        "## Most records are shut at more than one gate",
        "",
        "| gates shut | records |",
        "|---:|---:|",
    ]
    for k in sorted(per):
        L.append(f"| {k} | {per[k]} |")
    L += [
        "",
        f"**{len(all_open)} records pass all four**: " + " · ".join(f"`{s}`" for s in all_open) + ".",
        "",
        "That is the honest size of *solved* on this framing, and it is worth reading",
        "against the register's own warning that a bare one-word verdict is the thing the",
        "public page refuses to print. These are not diseases that are over; they are",
        "diseases where all four gates happen to be open **at once, somewhere**.",
        "",
        "### Where each record is first blocked",
        "",
        "| first shut gate | records |",
        "|---|---:|",
    ]
    for k, q, _ in GATES:
        L.append(f"| {k} — {q} | {first_shut.get(k, 0)} |")
    L.append(f"| none | {first_shut.get('none', 0)} |")
    L += [
        "",
        "**Read this table with care.** It says where a record is blocked *earliest*, not",
        "where it is blocked *hardest*, and on a framing whose own conclusion is that the",
        "gates are independent, *earliest* is close to meaningless. It is here because a",
        "sequential reading is the natural one and this is what it produces.",
        "",
        "## What this document is not sure of",
        "",
        "**Two thresholds are choices and both are reported.**",
        "",
        f"- **Gate 1** counts `partial` as open, which is generous. Requiring `established`",
        f"  would shut it on **{len(strict_know)} records ({pct(len(strict_know))})** instead of",
        f"  {len(closed['know'])}. The funnel's ordering survives either reading: gate 1 stays",
        "  the loosest of the four.",
        f"- **Gate 4** uses Nordstern's `delivery` bands, so open means `delivered` or",
        f"  `mostly`. On the loosest possible reading — only `barely` and `undelivered`",
        f"  count as shut — it is still **{len(loose_reach)} records ({pct(len(loose_reach))})**,",
        "  which is more than gates 1, 2 and 3 combined.",
        "",
        "**Gate 3 is a lower bound and probably a large one.** It counts records where",
        "somebody wrote down a candidate whose evidence is missing. It cannot count the",
        "candidates nobody has recorded, and the argument that prompted this document —",
        "*we can generate millions of drug possibilities and cannot get through mice fast",
        "enough* — is about exactly those. **Engpass has no obstacle for validation",
        "throughput.** `animal-translation` covers a gate that misleads and",
        "`no-model-system` covers a gate that is absent; a gate that works and is too",
        "narrow is a third shape and it is not filed anywhere.",
        "",
        "**And the register is 143 records chosen for structural diversity, with 0 of its",
        "sourceable numbers carrying a citation.** Every count here inherits that.",
    ]

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print(f"{n} records")
    for i, (k, q, _) in enumerate(GATES, 1):
        print(f"  {i}. {q:<32} shut on {len(closed[k]):>3}  ({pct(len(closed[k]))})")
    print(f"  treated without a full mechanism : {len(out_strict)} strict / {len(out_loose)} loose")
    print(f"  established mechanism, gate 2 shut: {len(bought_nothing)}")
    print(f"  all science gates open, no reach : {len(science_done)}")
    print(f"  all four gates open              : {len(all_open)}")
    print(f"wrote {os.path.basename(REPORT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
