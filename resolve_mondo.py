#!/usr/bin/env python3
"""Resolve `mondo:` against the Mondo Disease Ontology — proposing, never guessing.

    python3 resolve_mondo.py                      # look everything up, write the ledger
    python3 resolve_mondo.py --apply              # write the unambiguous matches only
    python3 resolve_mondo.py --accept heds=MONDO:0007523 --apply    # confirm one by hand
    python3 resolve_mondo.py --offline            # re-render the ledger, no network

WHY THIS IS A TOOL AND NOT A CHORE
----------------------------------
`mondo:` is the join key. Without it nothing else can be automated — GBD,
Orphanet, trial registries and every future source are keyed on an identifier
this register does not yet carry. It is unresolved on every record, it is a
mechanical lookup against an open ontology, and it is therefore the cheapest
thing on the board and the one that unblocks the rest.

THE RULES IT INHERITS
---------------------
From Sperrwerk, and they are the reason this is fifty lines longer than it
needs to be:

  * **It proposes; a person decides.** Nothing is written without `--apply`,
    and `--apply` writes ONLY exact label matches. Everything else waits for a
    human to look at it. A wrong identifier is worse than a missing one,
    because a missing one announces itself and a wrong one joins cleanly to
    somebody else's data.
  * **It carries the retrieved text.** Every proposal prints the matched label
    and Mondo's own definition, so review is verification rather than trust.
  * **No match reports `none`, never a plausible identifier.** A check that
    cannot run reports skipped, never ok.
  * **The lookup happens once and is written down.** No runtime resolution and
    no bundled ontology: the identifier goes into the record with its
    provenance in `mondo.md`, exactly as external data is supposed to arrive.

THE FOUR TIERS
--------------
  auto       the record's `name` EQUALS a Mondo label, case-insensitively, and
             every query agrees on one identifier. Safe to write.
  review     Mondo knows something, but by synonym or with more than one
             candidate. `hepatitis C` -> `hepatitis C virus infection` lands
             here and is obviously right; it still waits for a person, because
             the rule that would wave that through is the same rule that would
             wave through a near-miss.
  none       Mondo has nothing RELEVANT. Stays `unresolved`, and the report says
             so rather than reaching for the closest thing.
  unchecked  the lookup could not run — no network, or `--offline` with a cold
             cache. Its own tier on purpose: a question nobody asked Mondo must
             never be reported as a question Mondo answered no to.

`none` and `review` are not failures of the tool. A register that has been
deliberately admitting entities at the contested edge of medicine should expect
some of them to have no clean identifier, and finding that out is a result —
three of the twenty-one, for three different reasons, all recorded in
`gaps.md` #44.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import load                                    # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
OLS = "https://www.ebi.ac.uk/ols4/api"
CACHE = os.path.join(ROOT, ".mondo-cache.json")
LEDGER = os.path.join(ROOT, "mondo.md")
UA = "nordstern-resolve-mondo/1.0 (https://github.com/; static register tooling)"


# --------------------------------------------------------------------------
# network — cached on disk, so a re-run costs nothing and `--offline` works
# --------------------------------------------------------------------------
OFFLINE = False


def _get(url, cache, key):
    if key in cache:
        return cache[key]
    if OFFLINE:
        # `--offline` re-renders from what was already fetched. It must NOT
        # silently answer "nothing found" for a term it never looked up —
        # that would turn a missing cache entry into the finding "Mondo does
        # not have this", which is a lie the ledger would then publish.
        raise LookupError(f"not cached: {key}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    cache[key] = data
    time.sleep(0.2)                                       # be a good citizen
    return data


def search(term, cache):
    """Exact search on labels AND synonyms. Fuzzy search is not usable here —
    it answers `hepatitis C` with `hepatocellular carcinoma`."""
    qs = urllib.parse.urlencode({
        "q": term, "ontology": "mondo", "exact": "true", "rows": 8,
        "fieldList": "obo_id,label,description,short_form",
    })
    docs = _get(f"{OLS}/search?{qs}", cache, f"search::{term}")["response"]["docs"]
    return [{"id": d.get("obo_id"), "label": d.get("label", ""),
             "definition": (d.get("description") or [""])[0]}
            for d in docs if d.get("obo_id", "").startswith("MONDO:")]


def release(cache):
    try:
        o = _get(f"{OLS}/ontologies/mondo", cache, "release")
        return o.get("config", {}).get("version") or "unknown"
    except Exception:
        return "unknown"


# --------------------------------------------------------------------------
# resolution
# --------------------------------------------------------------------------
def norm(s):
    """Compare on words, ignoring the possessive.

    `Huntington's disease` and `Huntington disease` are the same disease, and
    the difference is a naming convention rather than a distinction — the
    standard nomenclatures dropped the possessive and the clinical world did
    not. Dropping it here is the ONLY liberty this function takes; everything
    else is punctuation and case. Anything looser and a near-miss would be
    waved through as an exact match, which is the failure this whole tool is
    arranged to avoid."""
    s = s.lower().replace("’", "'")
    s = re.sub(r"'s\b", "", s)                            # Huntington's -> Huntington
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def words(s):
    # Three, not four. Four drops `HIV`, and dropping it filtered out
    # `HIV infectious disease` — the correct term — before anyone could review
    # it. A relevance filter that hides a right answer is worse than one that
    # lets noise through, because noise is visible in the report and a missing
    # candidate is not. Two- and one-letter tokens stay out; they carry no
    # signal and match everything.
    return {w for w in norm(s).split() if len(w) >= 3}


def resolve(rec, cache):
    """-> {tier, id, label, definition, candidates, queries, matched_on}"""
    names = [rec["name"]] + list(rec.get("also") or [])
    seen, cands, hits = {}, [], []
    # Exact search still matches on tokens, so a short synonym drags in
    # nonsense: `AMR` returned `alopecia - intellectual disability syndrome`.
    # A candidate sharing no substantial word with anything we asked for is not
    # a weak match, it is noise — and letting it through would report "needs a
    # person" for a term Mondo simply does not have. `none` has to mean
    # "nothing relevant", not "literally zero rows".
    ours = set().union(*(words(n) for n in names)) if names else set()

    for term in names:
        for c in search(term, cache):
            if not (words(c["label"]) & ours):
                continue
            if c["id"] not in seen:
                seen[c["id"]] = c
                cands.append(c)
            # THE STRONG SIGNAL IS `name` ONLY, NEVER `also`.
            #
            # Learned the hard way on the first run. `also` is defined by the
            # schema as "synonyms people actually search for" — search aliases,
            # which may be broader or narrower than the entity. h-pylori-ulcer
            # lists `duodenal ulcer`, which exactly matches a Mondo label and is
            # the WRONG identifier: it excludes gastric ulcers and says nothing
            # about Helicobacter. Auto-accepting that would have written a clean,
            # confident, wrong join key.
            #
            # So `also` still widens the SEARCH, because it finds candidates the
            # formal name misses, and it never decides anything.
            if term == rec["name"] and norm(term) == norm(c["label"]):
                hits.append((term, c))

    ids = {c["id"] for _, c in hits}
    if len(ids) == 1:
        term, c = hits[0]
        return dict(tier="auto", matched_on=term, candidates=cands, queries=names, **c)
    if cands:
        tier = "review"
        note = ("more than one exact-label match — a person must choose"
                if len(ids) > 1 else
                "matched by synonym, not by label" if not hits else "")
        return dict(tier=tier, id=None, label=None, definition=None, matched_on=note,
                    candidates=cands, queries=names)
    return dict(tier="none", id=None, label=None, definition=None, matched_on="",
                candidates=[], queries=names)


# --------------------------------------------------------------------------
# writing — a surgical line edit, never a YAML round-trip
# --------------------------------------------------------------------------
def write_id(path, mondo_id):
    """Replace the `mondo:` line in place. Round-tripping the YAML would
    reformat every record and discard the header comments, which in these files
    carry the reasoning."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    new, n = re.subn(r"(?m)^mondo:.*$", f"mondo: {mondo_id}", text, count=1)
    if n != 1:
        raise SystemExit(f"{path}: expected exactly one `mondo:` line, found {n}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new)


# --------------------------------------------------------------------------
# the ledger — provenance, because `mondo:` is a bare string with no room for it
# --------------------------------------------------------------------------
def ledger(rows, rel, stamp):
    n = {t: sum(1 for r in rows if r["res"]["tier"] == t)
         for t in ("auto", "review", "none", "unchecked")}
    done = sum(1 for r in rows if r["current"] != "unresolved")
    out = [
        "# Mondo resolution ledger",
        "",
        "**Generated by `python3 resolve_mondo.py`.** `mondo:` is a bare string with",
        "nowhere to record where it came from, so provenance lives here: which of the",
        "record's names matched, what Mondo calls it, and against which release. Re-run",
        "after a Mondo release to find terms that have been merged or obsoleted.",
        "",
        f"- Mondo release: **{rel}** · resolved {stamp}",
        f"- {done} of {len(rows)} records carry an identifier",
        f"- this pass: {n['auto']} unambiguous · {n['review']} need a person · "
        f"{n['none']} not in Mondo"
        + (f" · **{n['unchecked']} not checked** (lookup unavailable)" if n["unchecked"] else ""),
        "",
        "## Resolved",
        "",
        "| slug | mondo | Mondo's label | matched on |",
        "|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: r["slug"]):
        if r["current"] != "unresolved":
            res = r["res"]
            # A hand-confirmed row is the one where a person exercised judgement,
            # so it is the row that most needs Mondo's own label recorded next to
            # it — otherwise the ledger documents the easy decisions and leaves
            # the debatable ones as a bare identifier. Recover it from the
            # candidate list.
            lab = res["label"] or next(
                (c["label"] for c in res["candidates"] if c["id"] == r["current"]), "—")
            mo = res["matched_on"] if res["tier"] == "auto" else "confirmed by hand"
            out.append(f"| {r['slug']} | `{r['current']}` | {lab} | {mo} |")
    if done == 0:
        out.append("| *(none yet)* | | | |")

    out += ["", "## Needs a person", "",
            "Mondo knows something, but not by an exact label match. Confirm with",
            "`--accept <slug>=<MONDO:id> --apply`, or leave it unresolved.", ""]
    any_review = False
    for r in sorted(rows, key=lambda r: r["slug"]):
        if r["res"]["tier"] != "review" or r["current"] != "unresolved":
            continue
        any_review = True
        out.append(f"**{r['slug']}** — searched: {', '.join(r['res']['queries'])}"
                   + (f"  \n*{r['res']['matched_on']}*" if r["res"]["matched_on"] else ""))
        out.append("")
        for c in r["res"]["candidates"][:6]:
            d = (c["definition"] or "").strip().replace("\n", " ")
            out.append(f"- `{c['id']}` **{c['label']}**" + (f" — {d[:240]}" if d else ""))
        out.append("")
    if not any_review:
        out.append("*(nothing outstanding)*\n")

    out += ["## Not in Mondo", "",
            "Left `unresolved`. The register does not reach for the closest thing —",
            "a wrong identifier joins cleanly to somebody else's data, which is worse",
            "than no identifier at all.", ""]
    none = [r for r in rows if r["res"]["tier"] == "none" and r["current"] == "unresolved"]
    for r in sorted(none, key=lambda r: r["slug"]):
        out.append(f"- **{r['slug']}** — searched: {', '.join(r['res']['queries'])}")
    if not none:
        out.append("*(nothing)*")
    out.append("")
    return "\n".join(out)


def main():
    global OFFLINE
    argv = sys.argv[1:]
    apply_ = "--apply" in argv
    offline = OFFLINE = "--offline" in argv
    accepts = {}
    for a in argv:
        if a.startswith("--accept"):
            for pair in a.split("=", 1)[1].split(",") if "=" in a else []:
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    accepts[k.strip()] = v.strip()
    for i, a in enumerate(argv):                          # `--accept slug=ID` form
        if a == "--accept" and i + 1 < len(argv) and "=" in argv[i + 1]:
            k, v = argv[i + 1].split("=", 1)
            accepts[k.strip()] = v.strip()

    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as fh:
            cache = json.load(fh)

    import glob
    paths = sorted(glob.glob(os.path.join(ROOT, "entities", "*.yaml")))
    rows = []
    for p in paths:
        rec = load(p)
        try:
            res = resolve(rec, cache)                     # offline: served from cache
        except Exception as e:
            # A dead network, or an uncached term under --offline, is NOT a
            # verdict. It gets its own tier so the ledger cannot print
            # "not in Mondo" for something nobody asked Mondo about.
            print(f"  !! {rec['slug']}: lookup unavailable ({type(e).__name__}) — "
                  f"reported as UNCHECKED, not as absent", file=sys.stderr)
            res = {"tier": "unchecked", "id": None, "label": None, "definition": None,
                   "matched_on": str(e), "candidates": [], "queries": []}
        rows.append({"slug": rec["slug"], "path": p, "current": rec.get("mondo", "unresolved"),
                     "res": res})

    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(cache, fh)

    # ---- report ----------------------------------------------------------
    written = 0
    for r in sorted(rows, key=lambda r: r["slug"]):
        res, slug = r["res"], r["slug"]
        if r["current"] != "unresolved":
            print(f"  have  {slug:24} {r['current']}")
            continue
        target = accepts.get(slug) or (res["id"] if res["tier"] == "auto" else None)
        if target and apply_:
            write_id(r["path"], target)
            r["current"] = target
            written += 1
            src = "accepted" if slug in accepts else f"= {res['matched_on']!r}"
            print(f"  WROTE {slug:24} {target}  ({src})")
        elif target:
            print(f"  auto  {slug:24} {target}  {res['label']!r}  — run --apply to write")
        elif res["tier"] == "review":
            print(f"  ?     {slug:24} {len(res['candidates'])} candidate(s), needs a person"
                  + (f" — {res['matched_on']}" if res["matched_on"] else ""))
        elif res["tier"] == "unchecked":
            print(f"  ....  {slug:24} not checked — lookup unavailable")
        else:
            print(f"  none  {slug:24} not in Mondo — stays unresolved")

    rel = "offline" if offline else release(cache)
    stamp = time.strftime("%Y-%m-%d")
    with open(LEDGER, "w", encoding="utf-8") as fh:
        fh.write(ledger(rows, rel, stamp))

    done = sum(1 for r in rows if r["current"] != "unresolved")
    print(f"\n{done}/{len(rows)} resolved · Mondo {rel} · wrote {os.path.basename(LEDGER)}"
          + (f" · {written} written into records" if written else ""))
    if not apply_ and any(r["res"]["tier"] == "auto" and r["current"] == "unresolved" for r in rows):
        print("nothing written — re-run with --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
