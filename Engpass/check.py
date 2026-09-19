#!/usr/bin/env python3
"""Engpass's checker: the obstacle register, and its link to Nordstern.

Run:  python3 check.py           # check + the derived tables
      python3 check.py --json    # obstacles + derived disease lists
      python3 check.py --build   # write today's snapshot into Nordstern's web/

WHAT THIS IS. Nordstern asks, per disease, do we understand it and can we do
anything about it. **Roughly a quarter of what it records as blocking a disease
is a `knowledge` blocker**, and none of those has a price — they are exactly the
ones money cannot triage. Read one record at a time they are forty-two separate
frustrations. Read together they collapse into a handful of questions asked over
and over in different tissues.

This register holds those obstacles. Nordstern says *this disease is blocked by
that obstacle*; Engpass derives *clearing this would unblock these diseases*,
which is the direction that can be acted on.

NAMED 2026-08-26, replacing **Engpass** ("uncharted territory"), which described
only the open-question half. **Engpass** is German for a bottleneck — literally a
narrow pass — and it names the function rather than the content: the register
exists to find the binding constraint. `FND-O-NNNN` IDs did NOT change — an id is
permanent through any rename. Moved under `Nordstern/` at the
same time, because the two are published together; the one-way dependency below
is unchanged and is now guarded by a test.

THE DEPENDENCY RUNS ONE WAY, DELIBERATELY, AND NESTING DOES NOT CHANGE IT.
Nordstern does not know Engpass exists. It records a list of obstacle slugs on a
blocker and nothing more; this tool reads Nordstern's built artifact and
reconciles. **Living inside `Nordstern/` is a publishing convenience and nothing
more** — `test_boundary.py` asserts that nothing in Nordstern imports or reads
anything in here. Same rule as Strangschrift
and Sperrwerk: **neither tool imports the other, a text file is the whole
interface.**

THE DISEASE LIST IS DERIVED, NEVER STORED. An obstacle does not declare what it
blocks. If it did, the two files could disagree, and an obstacle could claim to
block something the disease record does not cite. Nordstern is truth for the
link because the blocker is a claim about that disease, made by whoever rated it.

Zero dependencies. Borrows Nordstern's bounded YAML loader rather than carrying
a second copy — that is the one import, and it is a loader, not a model.
"""

from __future__ import annotations

import datetime
import glob
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NORDSTERN = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, NORDSTERN)

# THE ONE PERMITTED CROSSING: Nordstern's bounded YAML loader, by explicit file
# path. It is a loader, not a model — test_boundary.py pins that.
#
# LOADED BY PATH RATHER THAN BY `import check`, AND THE REASON IS A REAL BUG.
# Both files are named check.py. `import check` resolves through sys.modules, so
# it returns Nordstern's only when this file is `__main__` — the way the CLI runs
# it. The moment anything imports THIS module as `check`, the name is already
# taken and `import check` hands the module itself back, so `nordstern.load`
# raises AttributeError on a module that plainly has a `load`. That is what
# happened the first time `test_check.py` was written, on 2026-09-02.
# An explicit path cannot be shadowed and says which file it means.
_spec = importlib.util.spec_from_file_location(
    "nordstern_check", os.path.join(NORDSTERN, "check.py"))
nordstern = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("nordstern_check", nordstern)
_spec.loader.exec_module(nordstern)

# The kinds track Nordstern's blocker kinds deliberately, because an Engpass
# record IS a cluster of Nordstern blockers. Knowledge blockers were the obvious
# ones; the others cluster at least as hard — FIVE records independently record
# "the drug supply depends on a corporate donation that could stop".
KINDS = {
    "mechanism",     # nobody knows how it works
    "entity",        # nobody knows what this even is
    "capability",    # we cannot do the thing at all
    "measurement",   # we cannot tell, in a specific patient, in time
    "tooling",       # a missing instrument or model blocks the work
    "epidemiology",  # nobody has counted
    "economic",      # no market, donation-dependent, or priced out of reach
    "manufacturing", # cannot make enough, or fast enough
    "regulatory",    # the evidentiary standard cannot be met
}
# How far along the QUESTION is. Distinct from `status` below, which is whether
# the RECORD is live — an answered question is still an active record, and a
# deprecated record may hold a question nobody ever answered.
RESOLUTIONS = {"open", "partly-answered", "answered", "dissolved"}

# CLAIMED UNBLOCKING IS NOT DEMONSTRATED UNBLOCKING, AND THE REGISTER MUST NOT
# CONFLATE THEM.
#
# A bottom-up record earns its disease list: a Nordstern blocker cites it, so
# somebody rating that disease said this is what they are waiting on. That link
# is derived and it is evidence.
#
# A top-down record — "if we understood how RNA folds, that would unblock X" —
# has no such link, and the claim may simply be wrong. Marburg is the standing
# warning: its reservoir WAS identified, everybody expected that to unblock
# something, and what followed was advice to miners (gaps.md #101).
#
# So claims are stored separately from derived links and carry Nordstern's
# `standing` vocabulary, which exists for exactly this purpose — to test a
# widely-repeated assertion rather than to echo it. When a question is answered,
# its `alleged` claims become `documented` or `refuted`, and THAT is the record
# of whether the field's intuitions about payoff were any good.
CLAIM_STANDINGS = {"alleged", "documented", "disputed", "refuted", "derived"}

# `derived` IS THE FIFTH AND IT IS NOT A GRADE — IT RECORDS A DIFFERENT EVENT.
#
# The other four say how well an assertion about payoff has stood up, and a claim
# moves between them when THE QUESTION IS ANSWERED. `derived` says something
# cheaper and more common: **somebody rating the disease agreed, so the link is
# now earned rather than asserted.** No question was answered; the register
# caught up with itself.
#
# ADDED 2026-09-02 AFTER IT HAPPENED TWICE IN ONE AFTERNOON — `growth-control` /
# `hearing-loss`, then `validation-throughput` / `mesothelioma` and
# `spinal-muscular-atrophy`. Both times the claim had to be DELETED, because a
# claim naming a disease that already cites the record is the same link stored
# twice. **Deleting it destroyed the only evidence that the assertion came
# first**, which is precisely what `claims` exists to keep: a record of whether
# the field's intuitions about payoff were any good. An assertion that was later
# earned is the most interesting kind there is, and it was being thrown away.
#
# SO THE GUARD IS INVERTED RATHER THAN LIFTED. A normal claim must NOT name a
# disease that cites the record. A `derived` claim MUST — it is a receipt for a
# link that lives in Nordstern, and if that link disappears the receipt is a
# fabrication and `check.py` errors. It is excluded from the top-down claim count
# and from `claims_by_obstacle`, so nothing downstream can draw it as an
# unconfirmed assertion.

# APPEND-ONLY, same contract as Nordstern. `id` is what an outside citation
# resolves against, so it is opaque, sequential, never reused and never
# renumbered. A record that stops being the right frame is deprecated in place
# and may point at whatever replaced it; it is never deleted.
ID_PATTERN = "FND-O-"


def status(q) -> str:
    """`active` or `deprecated`, derived from the presence of a `deprecated:`
    block rather than stored beside it, so the two cannot disagree."""
    return "deprecated" if q.get("deprecated") else "active"


def superseded_by(q):
    """The 302. `None` means simply no longer needed — a 410."""
    return (q.get("deprecated") or {}).get("see")

errors: list[str] = []
warnings: list[str] = []


def read_questions() -> list[dict]:
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, "obstacles", "*.yaml"))):
        q = nordstern.load(path)
        here = os.path.basename(path)
        for field in ("slug", "id", "name", "kind", "resolution", "question"):
            if not q.get(field):
                errors.append(f"{here}: missing {field}")
        if q.get("kind") not in KINDS:
            errors.append(f"{here}: kind={q.get('kind')!r} not in {sorted(KINDS)}")
        if q.get("resolution") not in RESOLUTIONS:
            errors.append(f"{here}: resolution={q.get('resolution')!r} "
                          f"not in {sorted(RESOLUTIONS)}")
        if not str(q.get("id", "")).startswith(ID_PATTERN):
            errors.append(f"{here}: id={q.get('id')!r} missing or not {ID_PATTERN}NNNN")
        dep = q.get("deprecated")
        if dep and not (dep.get("date") and dep.get("why")):
            errors.append(f"{here}: deprecated block needs date and why")
        if q.get("slug") and q["slug"] != here[:-5]:
            errors.append(f"{here}: slug {q['slug']!r} does not match filename")

        # THE ONE RULE THAT MAKES THIS A REGISTER RATHER THAN A LIST OF THINGS
        # NOBODY KNOWS. Marburg's reservoir is established — Egyptian rousette
        # bats, virus isolated from wild colonies — and what followed was advice
        # to miners. No product, no surveillance, no capability. A knowledge
        # question can be answered and change nothing (Nordstern gaps.md #101),
        # so every question here must state what becomes possible if answered.
        # "Nothing much" is a legal and useful answer; silence is not.
        if not q.get("what_it_unblocks"):
            errors.append(f"{here}: no what_it_unblocks — see gaps.md #101")
        if not q.get("why_hard"):
            warnings.append(f"{here}: no why_hard")
        for c in q.get("claims") or []:
            if c.get("standing") not in CLAIM_STANDINGS:
                errors.append(f"{here}: claim standing={c.get('standing')!r} "
                              f"not in {sorted(CLAIM_STANDINGS)}")
            if not c.get("unblocks") or not c.get("why"):
                errors.append(f"{here}: claim needs `unblocks` and `why`")
        out.append(q)
    return out


def read_nordstern() -> list[dict]:
    art = os.path.join(NORDSTERN, "web", "nordstern.json")
    if not os.path.exists(art):
        raise SystemExit("Nordstern artifact missing — run `python3 check.py --build` there")
    with open(art, encoding="utf-8") as fh:
        return json.load(fh)["records"]


def link(questions, records):
    """Derive, per question, the diseases citing it. Nordstern is truth."""
    known = {q["slug"] for q in questions}
    cited: dict[str, list] = {s: [] for s in known}
    untagged = []
    for r in records:
        for b in r.get("blockers") or []:
            qs = b.get("obstacles") or []
            if not qs:
                # Only knowledge blockers are reported as untagged for now: the
                # first tagging pass covered them, and the others are the work
                # in front of us rather than an omission behind us.
                if b["kind"] == "knowledge":
                    untagged.append((r["slug"], b["blocks"]))
                continue
            for q in qs:
                if q not in known:
                    errors.append(
                        f"{r['slug']}: blocker cites obstacle {q!r}, which has no record")
                elif not any(x["slug"] == r["slug"] for x in cited[q]):
                    # ONE RECORD, ONE VOTE. A disease with two blockers citing
                    # the same obstacle was counted twice, which inflated the
                    # headline "records" column and printed prostate-cancer
                    # twice in the same row. The question is *which diseases
                    # does this block*, not *how many times was it mentioned*.
                    cited[q].append(r)
    # A claim that names a disease which already cites this record is not a
    # claim, it is the derived link written down twice — and the two could drift.
    for q in questions:
        have = {r["slug"] for r in cited[q["slug"]]}
        for c in q.get("claims") or []:
            if c.get("standing") == "derived":
                # The inverted guard: a receipt for a link that must still exist.
                if c.get("unblocks") not in have:
                    errors.append(
                        f"{q['slug']}: claim on {c['unblocks']!r} is marked `derived` "
                        f"and that record does not cite this obstacle — a receipt "
                        f"for a link that is not there")
            elif c.get("unblocks") in have:
                errors.append(f"{q['slug']}: claims to unblock {c['unblocks']!r}, "
                              f"which already cites it — that link is derived, not "
                              f"claimed. Mark the claim `standing: derived` to keep "
                              f"it as a record that the assertion came first.")

    for s, rs in cited.items():
        if not rs:
            # A question nothing cites is either premature or wrong. The rule
            # proposed in OPEN-QUESTIONS.md is that a question earns a record
            # when at least two disease records cite it.
            # Bottom-up records earn their list. A top-down record may have none
            # yet and still be worth holding — but it must be carrying claims,
            # or it is an assertion about nothing.
            q = next(x for x in questions if x["slug"] == s)
            # Only UNEARNED claims count here: a `derived` one is a receipt for
            # a link, and a record with nothing but receipts and no citations is
            # a contradiction the inverted guard above already catches.
            open_claims = [c for c in q["claims"]
                           if c.get("standing") != "derived"] if q.get("claims") else []
            if open_claims:
                warnings.append(f"{s}: no Nordstern record cites this — "
                                f"top-down, carrying {len(open_claims)} claim(s)")
            else:
                warnings.append(f"{s}: no disease record cites this, and no claims either")
        elif len(rs) == 1:
            warnings.append(f"{s}: only {rs[0]['slug']} cites this — "
                            f"the threshold for a record is two")
    return cited, untagged


def snapshot(obstacles, cited, untagged, records, on_date=None) -> dict:
    """Freeze today's aggregates, the same job Nordstern's snapshot does.

    ENGPASS WRITES ITS OWN, RATHER THAN APPEARING IN NORDSTERN'S, because
    Nordstern does not know this register exists — see README rule 1 and
    test_boundary.py. The arrow runs this way and only this way, so writing
    *into* Nordstern's web/ is fine and being read *by* Nordstern's checker
    would not be.

    THE HEADLINE IS THE ASYMMETRY. A knowledge blocker carries `scale: null` by
    design, so the obstacles collected here are precisely the ones money cannot
    triage — and the count of records blocked by each is the number that answers
    "what should we work on next", which is the whole reason this register is a
    second file rather than more fields on the first.
    """
    def tally(vals):
        out = {}
        for v in vals:
            out[v] = out.get(v, 0) + 1
        return dict(sorted(out.items(), key=lambda kv: (-kv[1], str(kv[0]))))

    per = {q["slug"]: len(cited[q["slug"]]) for q in obstacles}
    claims = [c for q in obstacles for c in (q.get("claims") or [])]
    tagged = sum(len(v) for v in cited.values())

    return {
        "date": on_date or datetime.date.today().isoformat(),
        "register": "engpass",
        "obstacles": {
            "active": len(obstacles),
            "by_kind": tally(q["kind"] for q in obstacles),
            "by_resolution": tally(q.get("resolution", "open") for q in obstacles),
        },
        "against_nordstern_records": len(records),
        # The derived link, and the direction that can be acted on: not "this
        # disease is blocked by that", but "clearing this releases these N".
        "blocks": dict(sorted(per.items(), key=lambda kv: -kv[1])),
        # WHICH RECORDS, NOT ONLY HOW MANY — added 2026-09-02 alongside
        # Nordstern's `buckets.members`, for the same reason and with the same
        # rule. `who-progresses: 47` next to `who-progresses: 49` cannot say
        # whether two diseases were newly found to be waiting on it or two
        # records were simply written; the second happened three times that
        # afternoon. A derived link cannot be recovered from history, because the
        # deriving code and the ratings both move, so it is frozen here or it is
        # lost. NOT BACKFILLED into earlier snapshots — those are counts only and
        # a diff against them must report `skipped`, never a guess.
        "blocks_members": {
            q["slug"]: sorted(r["slug"] for r in cited[q["slug"]])
            for q in obstacles
        },
        # Per obstacle rather than tallied, because THIS is Engpass's own time
        # series: an obstacle's `resolution` moving open → partly-answered →
        # answered is the register of ignorance shrinking, and a tally cannot say
        # which one moved. Its equivalent of a bucket movement.
        "resolution_members": {
            q["slug"]: {"id": q["id"], "kind": q["kind"],
                        # The name IS the question — "Why this person and not
                        # that one?" — so a page needs nothing else to lead a
                        # section with. Carried here rather than typed into the
                        # dashboard, on the same rule as Nordstern's bucket defs:
                        # a definition written twice is a definition that drifts.
                        "name": q["name"],
                        "resolution": q.get("resolution", "open"),
                        "superseded_by": superseded_by(q),
                        "status": status(q)}
            for q in obstacles
        },
        # THE TOP-DOWN HALF, PER OBSTACLE AND CARRYING ITS STANDING.
        # A derived link is evidence — somebody rating that disease said this is
        # what they were waiting on. A claim is an assertion that may simply be
        # wrong, and the two must never be drawn as the same bar. When a question
        # is answered its claims become `documented` or `refuted`, and THAT is
        # the record of whether the field's intuitions about payoff were any good.
        # UNEARNED CLAIMS ONLY. A `derived` claim is a receipt for a link that is
        # already in `blocks_members`, and drawing it a second time as an
        # unconfirmed assertion is exactly the double-count the guard prevents.
        "claims_by_obstacle": {
            q["slug"]: [{"unblocks": c["unblocks"], "standing": c["standing"]}
                        for c in (q.get("claims") or [])
                        if c["standing"] != "derived"]
            for q in obstacles
            if any(c["standing"] != "derived" for c in (q.get("claims") or []))
        },
        # And separately, the ones the register caught up with — the count that
        # says how often an assertion made here was later agreed with by somebody
        # rating the disease. Its own time series.
        "claims_earned": {
            q["slug"]: sorted(c["unblocks"] for c in (q.get("claims") or [])
                              if c["standing"] == "derived")
            for q in obstacles
            if any(c["standing"] == "derived" for c in (q.get("claims") or []))
        },
        "records_blocked_at_least_once": len({
            r["slug"] for rs in cited.values() for r in rs}),
        "distinct_links": tagged,
        # THE PILE THAT IS A FINDING, NOT A BACKLOG. A knowledge blocker with no
        # obstacle assigned is often not a question at all — "nobody has made the
        # drug" is `no-sponsor` wearing a lab coat — and the count is the
        # standing argument for splitting Nordstern's `knowledge` kind.
        "untagged_knowledge_blockers": len(untagged),
        # The pile itself, not only its size. Seven of the first eight were not
        # questions at all — a TB vaccine, an antifungal for eumycetoma, in vivo
        # editing for sickle cell — which is the evidence for splitting
        # Nordstern's `knowledge` into `mechanism-unknown` / `no-candidate`. A
        # count cannot show that; the sentences can.
        "untagged_list": [{"record": s, "blocks": b} for s, b in sorted(untagged)],
        "claims": {
            "total": len(claims),
            "by_standing": tally(c["standing"] for c in claims),
        },
    }


def obstacle_diff(old, new) -> dict:
    """What changed between two Engpass snapshots.

    NORDSTERN'S DIFF ASKS WHETHER A DISEASE CHANGED STATE. THIS ONE ASKS
    WHETHER A QUESTION GOT ANSWERED, and they are not the same event — a
    question can be answered and change nothing, which is the rule forced by
    `marburg` and enforced on every record by `what_it_unblocks`.

    Four things move, and only two of them are about ignorance shrinking:
      resolutions — `open` → `partly-answered` → `answered`. **THE SIGNAL.**
      graded      — a claim going `alleged` → `documented` or `refuted`, which
                    is the register scoring its own guesses. **ALSO SIGNAL.**
      added/gone  — obstacles written or deprecated. The register growing.
      blocks      — records citing each obstacle, which moves mostly because
                    Nordstern grew. Reported, never headlined.

    Followed by `id`, and it refuses rather than guesses when membership is
    absent — both for the same reasons as `bucket_diff`, which this mirrors.
    """
    out = {"from": old.get("date"), "to": new.get("date"), "skipped": None,
           "added": [], "gone": [], "resolutions": [], "graded": [],
           "blocks_delta": {}}
    om = old.get("resolution_members")
    nm = new.get("resolution_members")
    if om is None or nm is None:
        missing = [d for d, m in ((out["from"], om), (out["to"], nm)) if m is None]
        out["skipped"] = (
            f"per-obstacle resolution was not recorded in "
            f"{', '.join(str(d) for d in missing)} — snapshots before 2026-09-02"
            f" stored tallies only, and it cannot be reconstructed after the fact")
        return out

    o_by = {v.get("id") or k: (k, v) for k, v in om.items()}
    n_by = {v.get("id") or k: (k, v) for k, v in nm.items()}
    for i in sorted(set(n_by) - set(o_by)):
        slug, v = n_by[i]
        out["added"].append({"id": i, "slug": slug, "resolution": v["resolution"]})
    for i in sorted(set(o_by) - set(n_by)):
        slug, v = o_by[i]
        out["gone"].append({"id": i, "slug": slug})
    for i in sorted(set(o_by) & set(n_by)):
        (_, ov), (slug, nv) = o_by[i], n_by[i]
        if ov["resolution"] != nv["resolution"]:
            out["resolutions"].append({"id": i, "slug": slug,
                                       "from": ov["resolution"],
                                       "to": nv["resolution"]})

    # A claim changing standing, keyed by obstacle + the disease it names.
    oc, nc = old.get("claims_by_obstacle") or {}, new.get("claims_by_obstacle") or {}
    flat = lambda d: {(q, c["unblocks"]): c["standing"]
                      for q, cs in d.items() for c in cs}
    o_cl, n_cl = flat(oc), flat(nc)
    for key in sorted(set(o_cl) & set(n_cl)):
        if o_cl[key] != n_cl[key]:
            out["graded"].append({"obstacle": key[0], "unblocks": key[1],
                                  "from": o_cl[key], "to": n_cl[key]})
    # A claim that stopped being a claim because the link became derived is not a
    # grading and must not be counted as one — `growth-control`/`hearing-loss`,
    # 2026-09-02. It shows as a disappearance here and as a new derived link.
    for key in sorted(set(o_cl) - set(n_cl)):
        out["graded"].append({"obstacle": key[0], "unblocks": key[1],
                              "from": o_cl[key], "to": "withdrawn"})

    ob, nb = old.get("blocks") or {}, new.get("blocks") or {}
    for slug in sorted(set(ob) | set(nb)):
        was, now = ob.get(slug, 0), nb.get(slug, 0)
        if was != now:
            out["blocks_delta"][slug] = {"was": was, "now": now}
    return out


def load_snapshots() -> list:
    d = os.path.join(NORDSTERN, "web", "snapshots", "engpass")
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*.json"))):
        if os.path.basename(p) == "index.json":
            continue
        with open(p, encoding="utf-8") as fh:
            out.append(json.load(fh))
    return out


def write_snapshot(snap) -> str:
    """Into Nordstern's web/ — the permitted direction, and where the dashboard
    will look. One file per day; same-day rebuilds overwrite."""
    d = os.path.join(NORDSTERN, "web", "snapshots", "engpass")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, snap["date"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(snap, indent=1, ensure_ascii=False) + "\n")
    dates = sorted(os.path.splitext(f)[0] for f in os.listdir(d)
                   if f.endswith(".json") and f != "index.json")
    with open(os.path.join(d, "index.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"register": "engpass", "snapshots": dates}, indent=1) + "\n")

    # A separate script tag from Nordstern's, for the same file:// reason and to
    # keep the two registers' artifacts separable. The dashboard loads both.
    series = []
    for dt in dates:
        with open(os.path.join(d, dt + ".json"), encoding="utf-8") as fh:
            series.append(json.load(fh))
    # Computed here, at build time, never in the page — the same rule Nordstern's
    # `bucket_diff` follows. This comparison carries a refusal and a distinction
    # (a withdrawn claim is not a graded one) that a second implementation in
    # JavaScript would quietly lose.
    diffs = [obstacle_diff(a, b) for a, b in zip(series, series[1:])]
    with open(os.path.join(NORDSTERN, "web", "engpass-snapshots.js"), "w",
              encoding="utf-8") as fh:
        fh.write("/* GENERATED by Engpass/check.py --build — do not edit. */\n")
        fh.write("window.ENGPASS_SNAPSHOTS = "
                 + json.dumps(series, indent=1, ensure_ascii=False) + ";\n")
        fh.write("window.ENGPASS_DIFFS = "
                 + json.dumps(diffs, indent=1, ensure_ascii=False) + ";\n")
    return path


def deaths(r) -> float:
    v = (r.get("burden") or {}).get("deaths") or {}
    return v.get("value") or 0.0


def main() -> int:
    questions = read_questions()
    ids = [q.get("id") for q in questions]
    for i in sorted({x for x in ids if ids.count(x) > 1}):
        errors.append(f"id {i} is used more than once — ids are never reused")
    by_slug = {q["slug"]: q for q in questions}
    for q in questions:
        see = superseded_by(q)
        if see is not None and see not in by_slug:
            errors.append(f"{q['slug']}: deprecated.see={see!r} is not a record")
    # Deprecated records stay readable in --json and out of the derived tables.
    retired = [q for q in questions if status(q) == "deprecated"]
    questions = [q for q in questions if status(q) == "active"]

    records = read_nordstern()
    cited, untagged = link(questions, records)

    if "--build" in sys.argv:
        snap = snapshot(questions, cited, untagged, records)
        path = write_snapshot(snap)
        print(f"wrote {os.path.relpath(path, NORDSTERN)} "
              f"({snap['obstacles']['active']} obstacles, "
              f"{snap['distinct_links']} links, "
              f"{snap['untagged_knowledge_blockers']} untagged)")
        return 1 if errors else 0

    if "--json" in sys.argv:
        print(json.dumps({"questions": [
            {**q, "status": status(q), "superseded_by": superseded_by(q), "blocks": sorted(r["slug"] for r in cited[q["slug"]])}
            for q in questions]}, indent=2))
        return 1 if errors else 0

    print(f"\n# Engpass — {len(questions)} obstacles, "
          f"against {len(records)} Nordstern records\n")

    print("## What each question blocks\n")
    print("| question | kind | records | deaths/yr cited | blocked ONLY by this |")
    print("|---|---|---|---|---|")
    for q in sorted(questions, key=lambda q: -len(cited[q["slug"]])):
        rs = cited[q["slug"]]
        # "Only by this" means every knowledge blocker on the record cites this
        # question and no other. It is the strongest claim available: answer it
        # and nothing scientific is left in the way.
        only = [r["slug"] for r in rs
                if {x for b in r["blockers"] if b["kind"] == "knowledge"
                    for x in (b.get("obstacles") or [])} == {q["slug"]}]
        d = sum(deaths(r) for r in rs)
        print(f"| **{q['slug']}** | {q['kind']} | {len(rs)} | {d:,.0f} | "
              f"{', '.join(only) or '—'} |")

    print("\n## Diseases citing more than one question\n")
    for r in records:
        qs = sorted({x for b in (r.get("blockers") or [])
                     for x in (b.get("obstacles") or [])})
        if len(qs) > 1:
            print(f"- **{r['slug']}** — {' · '.join(qs)}")

    claimed = [(q, c) for q in questions for c in (q.get("claims") or [])]
    if claimed:
        print("\n## Claimed, not demonstrated\n")
        print("A top-down record asserts what answering it would unblock. Nothing")
        print("in Nordstern cites these links, so they are claims and carry a")
        print("standing. **When the question is answered they become `documented`")
        print("or `refuted`** — which is the record of whether the field's")
        print("intuitions about payoff were worth anything (gaps.md #101).\n")
        print("| question | claims to unblock | standing |")
        print("|---|---|---|")
        for q, c in claimed:
            print(f"| {q['slug']} | {c['unblocks']} | **{c['standing']}** |")

    print("\n## Knowledge blockers with no question assigned\n")
    print("Every one of these is either a question nobody has named yet, or —")
    print("more often — **not an open question at all**. \"Nobody has made the")
    print("drug\" is a different object from \"nobody knows how this works\", and")
    print("several below are `no-sponsor` wearing a lab coat. See")
    print("Nordstern/OPEN-QUESTIONS.md §3.\n")
    for slug, blocks in untagged:
        print(f"- {slug} — {blocks}")

    for w in warnings:
        print(f"\n  warn   {w}", end="")
    for e in errors:
        print(f"\n  ERROR  {e}", end="")
    print(f"\n\n{len(questions)} obstacles"
          f"{f' (+{len(retired)} deprecated)' if retired else ''}"
          f" · {len(errors)} errors · "
          f"{len(warnings)} warnings · {len(untagged)} untagged knowledge blockers")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
