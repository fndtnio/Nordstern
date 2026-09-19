#!/usr/bin/env python3
"""Diff Nordstern against Mondo — what we hold, against what the ontology says.

    python3 mondo_sync.py            # fetch, diff, write the report and snapshot
    python3 mondo_sync.py --apply    # write the one unambiguous fix (see below)
    python3 mondo_sync.py --offline  # re-render from cache, no network

WHY THIS EXISTS
---------------
`mondo.md` promises: *"Re-run after a Mondo release to find terms that have been
merged or obsoleted."* Nothing did that. `resolve_mondo.py` finds an identifier
once and never looks at it again — so the join key the whole external-data plan
depends on could rot silently, and the register would keep reporting a confident
`MONDO:` id pointing at a term that no longer exists.

This is the other half. `resolve_mondo.py` answers *which term is this?*; this
answers *is that still true, and what does the ontology know that we do not?*

IT DIFFS IN TWO DIRECTIONS
--------------------------
**A. Nordstern against Mondo.** For every resolved id:

  obsolete        the term has been retired or merged. The join key is DEAD.
                  Mondo usually names its replacement, and that is the one thing
                  `--apply` will write, because it is Mondo's own explicit
                  statement rather than an inference.
  label           Mondo's label against our `name`. Divergence is often
                  deliberate (we say "lymphatic filariasis"; Mondo says "filarial
                  elephantiasis") so this reports and never acts.
  synonyms        exact synonyms Mondo carries that our `also` lacks. Proposed,
                  never written — see the scope rule below.
  scope audit     our `also` entries that Mondo classifies as BROAD or NARROW
                  rather than exact. This is the check that would have caught
                  the `duodenal ulcer` near-miss on `h-pylori-ulcer`: a term
                  sitting in `also` that names a different-sized thing.
  xrefs           what Mondo maps this to — ICD, Orphanet, OMIM, UMLS, MeSH,
                  SNOMED, DOID. This is the bridge to burden data and the reason
                  a batch import is now possible at all.
  sub-entities    the distinctions the register MAKES against the ones the
                  ontology can HOLD — a record pointing at its own parent, an
                  `also` entry that is somebody else's term, and a stratum the
                  ontology already has an identifier for. See `diff_subentities`.

**B. Mondo against itself.** The snapshot in `mondo-terms.json` is committed, so
a later run diffs today's ontology against the one we last looked at: labels
changed, terms obsoleted, definitions rewritten, cross-references added. That is
the part that turns a one-off resolution into something maintained.

THE RULES IT INHERITS
---------------------
  * **It proposes; a person decides.** `--apply` writes exactly one class of
    change — an obsoleted term's single named replacement. Synonyms and xrefs are
    reported and left alone.
  * **ONLY EXACT SYNONYMS ARE EVER PROPOSED.** Mondo scopes its synonyms
    (`hasExactSynonym`, `hasRelatedSynonym`, `hasBroadSynonym`,
    `hasNarrowSynonym`) and only the first is an equivalence. Importing the
    others would put terms of a different size into a field that is read as an
    alias list — which is precisely how `duodenal ulcer` nearly became the
    identifier for a record about peptic ulcer caused by *H. pylori*.
  * **A lookup that could not run is `unchecked`, never "no change".**
"""
import glob
import json
import os
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import resolve_mondo as rm                                   # noqa: E402
from check import load                                       # noqa: E402

SNAPSHOT = os.path.join(ROOT, "mondo-terms.json")
REPORT = os.path.join(ROOT, "mondo-sync.md")

# Which cross-reference sources are worth surfacing, and what each unlocks.
# Ordered by usefulness to the scalar-sourcing plan rather than alphabetically.
XREF_VALUE = {
    "ICD10CM": "burden — the route into GBD cause mappings",
    "ICD10WHO": "burden — the route into GBD cause mappings",
    "icd11.foundation": "burden — current WHO classification",
    "Orphanet": "RARE DISEASE PREVALENCE — publishes prevalence classes, not point estimates",
    "OMIM": "genetic — gene and variant level",
    "SCTID": "clinical coding (SNOMED CT)",
    "MESH": "literature search",
    "UMLS": "concept mapping across vocabularies",
    "DOID": "disease ontology",
    "MedDRA": "adverse event and regulatory coding",
    "GARD": "rare disease information",
    "NCIT": "cancer and biomedical terminology",
    "MEDGEN": "NCBI concept hub — links OMIM, Orphanet, GTR and literature",
    "ICD9": "burden — historical coding, still the key for older series",
    "EFO": "experimental factor ontology — the key into GWAS and biobank data",
    "NORD": "rare disease information",
    "NANDO": "Japanese intractable disease designations",
    "ICDO": "oncology morphology coding",
    "OMIMPS": "OMIM phenotypic series",
    "MFOMD": "mental functioning ontology",
    "birnlex": "neuroscience terminology",
}


# --------------------------------------------------------------------------
# fetch
# --------------------------------------------------------------------------
def fetch_term(obo_id, cache):
    """One Mondo term, reduced to the fields worth diffing.

    The `obo_id` query form is used rather than the term-by-IRI endpoint: it
    avoids double-URL-encoding a purl and returns the same record.
    """
    qs = urllib.parse.urlencode({"obo_id": obo_id})
    data = rm._get(f"{rm.OLS}/ontologies/mondo/terms?{qs}", cache, f"term::{obo_id}")
    terms = (data.get("_embedded") or {}).get("terms") or []
    if not terms:
        return None
    t = terms[0]

    syn = {}
    for s in (t.get("obo_synonym") or []):
        name, scope = s.get("name"), s.get("scope")
        if name:
            syn[name] = scope
    xrefs = {}
    for x in (t.get("obo_xref") or []):
        db, xid = x.get("database"), x.get("id")
        if db and xid:
            xrefs.setdefault(db, []).append(xid)

    return {
        "id": t.get("obo_id"),
        "label": t.get("label") or "",
        "obsolete": bool(t.get("is_obsolete")),
        "replaced_by": t.get("term_replaced_by") or [],
        "definition": (t.get("description") or [""])[0],
        "synonyms": syn,                      # name -> scope
        "xrefs": {k: sorted(v) for k, v in sorted(xrefs.items())},
    }


def exact_synonyms(term):
    return sorted(n for n, scope in term["synonyms"].items() if scope == "hasExactSynonym")


# --------------------------------------------------------------------------
# diff A — the register against the ontology
# --------------------------------------------------------------------------
def diff_record(rec, term):
    """-> list of findings, each {level, kind, text, fix?}"""
    out = []
    ours_name = rec["name"]
    ours_also = list(rec.get("also") or [])
    ours_all = {rm.norm(x) for x in [ours_name] + ours_also}

    # 1. DEAD JOIN KEY. Everything else on this record is moot if this fires.
    if term["obsolete"]:
        repl = [r for r in term["replaced_by"] if isinstance(r, str)]
        out.append({
            "level": "error", "kind": "obsolete",
            "text": f"`{term['id']}` is OBSOLETE in Mondo — the join key is dead",
            "fix": repl[0].rsplit("/", 1)[-1].replace("_", ":") if len(repl) == 1 else None,
            "note": ("Mondo names one replacement" if len(repl) == 1 else
                     f"Mondo names {len(repl)} replacements — a person must choose"
                     if repl else "Mondo names no replacement"),
        })

    # 2. Label divergence. Reported, never acted on: we deliberately differ where
    #    Mondo names a disease after its sequela (lymphatic filariasis).
    if rm.norm(term["label"]) not in ours_all:
        out.append({
            "level": "note", "kind": "label",
            "text": f"we call it **{ours_name}**; Mondo's label is **{term['label']}**",
        })

    # 3. Exact synonyms we do not carry. THE BATCH-IMPORT CANDIDATE.
    missing = [s for s in exact_synonyms(term) if rm.norm(s) not in ours_all]
    if missing:
        out.append({
            "level": "propose", "kind": "synonyms",
            "text": "Mondo exact synonyms not in `also`: " + ", ".join(f"`{m}`" for m in missing),
        })

    # 4. SCOPE AUDIT — the check that would have caught `duodenal ulcer`.
    #    An `also` entry Mondo classifies as broad or narrow is not an alias; it
    #    names a different-sized thing, and this field is read as equivalences.
    byname = {rm.norm(n): (n, sc) for n, sc in term["synonyms"].items()}
    for a in ours_also:
        hit = byname.get(rm.norm(a))
        if hit and hit[1] in ("hasBroadSynonym", "hasNarrowSynonym"):
            out.append({
                "level": "warn", "kind": "scope",
                "text": f"`also: {a}` — Mondo scopes this **{hit[1]}**, not an exact "
                        f"synonym. It names a different-sized thing (see gaps.md #43)",
            })

    # 5. What this identifier unlocks.
    if term["xrefs"]:
        out.append({"level": "info", "kind": "xrefs", "text": "", "xrefs": term["xrefs"]})
    return out


# --------------------------------------------------------------------------
# diff A2 — SUB-ENTITIES: the distinctions the register makes, against the ones
#           the ontology can hold.
#
# WHY THIS EXISTS. Writing four fungal records in one day turned up the same
# hole three times: **chronic pulmonary aspergillosis**, **coccidioidal
# meningitis** and ***Candida auris*** have no Mondo term at all, and in each
# case the missing term is the one carrying the clinically decisive
# distinction — the larger burden, the only `suppressive` stratum, the only
# transmissible fungus. It looked like a mycology problem until `acute
# bronchitis` arrived the same day: Mondo has `bronchitis`, `chronic
# bronchitis`, and **`acute bronchitis, non-human animal`**, and no human acute
# term. gaps.md #227.
#
# All three were found by a person typing a name into a search box. This makes
# it a check.
#
# THREE QUESTIONS, AND THEY HAVE DIFFERENT NOISE PROFILES — which is why they
# are reported differently rather than lumped together.
#
#   precision   Our `name` is strictly more specific than the term's label
#               (`acute bronchitis` against `bronchitis`). That is the signature
#               of pointing at a PARENT. It is distinguished from deliberate
#               divergence — we say `lymphatic filariasis`, Mondo says `filarial
#               elephantiasis` — by a strict word-subset test, which those do
#               not satisfy. Six records match, with no false positives.
#
#   alias       An `also` entry that is the LABEL of a different Mondo term.
#               **This is NOT a defect and the first version said it was.**
#               `also` is defined by SCHEMA.md as "synonyms people actually
#               search for", `resolve_mondo` states that those "may be broader or
#               narrower than the entity", and the field's only consumer in this
#               codebase is free-text search in `web/query.js`. Somebody typing
#               `pernicious anaemia` SHOULD land on the `anaemia` record.
#               So the finding is informational: it names the `also` entries the
#               ontology holds as entities in their own right — **candidate
#               sub-records the register currently folds into a parent**, which
#               is the same question the `strata` check asks from the other side.
#               See gaps.md #229.
#
#   strata      A `strata[].name` that resolves. **Reported only when it does.**
#               A stratum name is often a descriptive phrase — "fluconazole-
#               susceptible, chiefly C. albicans" — and searching one of those
#               and finding nothing tells you nothing at all. Reporting the null
#               would be a check that cannot run reporting a result, which is
#               the one thing this codebase refuses to do.
#
# ALL THREE SEARCH, AND A SEARCH THAT COULD NOT RUN IS `unchecked`. Under
# `--offline` an uncached lookup raises, and that must never become the finding
# "Mondo does not have this" — the same rule `_get` already enforces, for the
# same reason.
# --------------------------------------------------------------------------
# Mondo namespaces its veterinary entities consistently, and **not one of them
# can ever be right for this register.** The first version of this check
# proposed `MONDO:1017104` *acute bronchitis, non-human animal* as the fix for
# the `acute-bronchitis` record — which is the `duodenal ulcer` failure again,
# and would have filed a human disease under a term about dogs.
ANIMAL = "non-human animal"


def _same(a, b):
    """`rm.norm`, plus the one thing it does not know: British spelling.

    The register writes `anaemia`, `haemorrhage`, `diarrhoeal`; Mondo writes the
    American forms. `rm.norm` is deliberately strict and is used by
    `resolve_mondo` to decide exact matches, so it is left alone and the
    ligature folding lives here.
    """
    def f(s):
        return rm.norm(s).replace("ae", "e").replace("oe", "e")
    return f(a) == f(b)


def _lookup(name, cache):
    """-> (list_of_hits, checked?). Never turns a failed lookup into a null."""
    try:
        hits = [h for h in rm.search(name, cache) if ANIMAL not in h["label"].lower()]
        return hits, True
    except Exception:
        return [], False


def _named(hits, name, our_id):
    """The hit whose LABEL *is* this name — not merely one that matched it.

    THE TIGHTENING THAT MADE THIS CHECK USABLE. Taking any non-ours hit produced
    **180 alias findings**, roughly half of them junk: `motor neurone disease`
    "resolved" to *frontotemporal dementia and/or ALS 1*, `Alzheimer's` to
    *Alzheimer disease 3*, `bronchial asthma` to *atopic IgE-mediated allergic
    disorder*. Mondo's exact search matches on synonyms as well as labels, so a
    term sharing one related synonym came back looking like an identification.
    Requiring the label itself to be the name is a much stronger claim — Mondo
    has an entity *called this* — and it is the claim the finding actually makes.
    """
    return next((h for h in hits
                 if h["id"] != our_id and _same(h["label"], name)), None)


def diff_subentities(rec, term, cache):
    out = []
    our_id = term["id"]
    label_w = set(rm.norm(term["label"]).split())
    name_w = set(rm.norm(rec["name"]).split())

    # 1. PRECISION — are we pointing at a parent?
    if label_w and label_w < name_w:
        hits, ok = _lookup(rec["name"], cache)
        better = [h for h in hits if h["id"] != our_id]
        if not ok:
            out.append({"level": "note", "kind": "unchecked",
                        "text": f"could not check whether Mondo has a term for "
                                f"**{rec['name']}** (not cached, offline)"})
        elif better:
            # NO `fix` KEY, DELIBERATELY. `--apply` writes only an obsoleted
            # term's single named replacement, because that is Mondo's own
            # explicit statement. This is an inference, and the tool cannot tell
            # a narrower term for OUR entity from a sibling that merely contains
            # our words — `pleomorphic adenoma of the salivary gland` returns
            # *carcinoma ex pleomorphic adenoma*, a malignant transformation and
            # a different disease. A person decides.
            out.append({
                "level": "propose", "kind": "precision",
                "text": f"we call it **{rec['name']}** and point at `{our_id}` "
                        f"**{term['label']}**, which is BROADER. Mondo also has "
                        + ", ".join(f"`{h['id']}` **{h['label']}**" for h in better[:3])
                        + " — **candidate(s) to review, not a fix**: these may be "
                          "narrower terms for this record, or siblings that merely "
                          "share its words",
            })
        else:
            out.append({
                "level": "note", "kind": "no-term",
                "text": f"**{rec['name']}** has no Mondo term; the record points at "
                        f"the parent `{our_id}` **{term['label']}**. The ontology "
                        f"cannot hold a distinction this register makes (gaps.md #227)",
            })

    # 2. ALIAS — an `also` entry that is somebody else's term.
    listed = {rm.norm(n) for n in term["synonyms"]}
    for a in (rec.get("also") or []):
        if rm.norm(a) in listed or rm.norm(a) == rm.norm(term["label"]):
            continue                      # already covered by the scope audit
        hits, ok = _lookup(a, cache)
        if not ok:
            continue                      # silence, not a null — see the note above
        other = _named(hits, a, our_id)
        if other:
            out.append({
                "level": "info", "kind": "alias",
                "text": f"`also: {a}` is the label of `{other['id']}` "
                        f"**{other['label']}** — the ontology holds it as its own "
                        f"entity, which the register currently folds into this "
                        f"record",
            })

    # 3. STRATA — positive findings only.
    for s in (rec.get("strata") or []):
        nm = s.get("name") or ""
        if not nm:
            continue
        hits, ok = _lookup(nm, cache)
        if not ok:
            continue
        hit = _named(hits, nm, our_id)
        if hit:
            out.append({
                "level": "info", "kind": "strata",
                "text": f"stratum **{nm}** → `{hit['id']}` **{hit['label']}** — "
                        f"the ontology holds this distinction and the register "
                        f"carries it only as prose",
            })
    return out


# --------------------------------------------------------------------------
# diff B — the ontology against the last time we looked
# --------------------------------------------------------------------------
def diff_snapshot(old, new):
    out = []
    for oid, now in sorted(new.items()):
        was = old.get(oid)
        if was is None:
            out.append((oid, "new", "first time this identifier has been snapshotted"))
            continue
        if was.get("label") != now["label"]:
            out.append((oid, "label", f"`{was.get('label')}` → `{now['label']}`"))
        if bool(was.get("obsolete")) != now["obsolete"]:
            out.append((oid, "obsolete", f"is_obsolete {was.get('obsolete')} → {now['obsolete']}"))
        if (was.get("definition") or "") != now["definition"]:
            out.append((oid, "definition", "the definition text changed"))
        oldx, newx = was.get("xrefs") or {}, now["xrefs"]
        added = sorted(set(newx) - set(oldx))
        gone = sorted(set(oldx) - set(newx))
        if added:
            out.append((oid, "xref+", "new cross-reference sources: " + ", ".join(added)))
        if gone:
            out.append((oid, "xref-", "cross-reference sources removed: " + ", ".join(gone)))
        olds, news = set(was.get("synonyms") or {}), set(now["synonyms"])
        if news - olds:
            out.append((oid, "synonyms", f"{len(news - olds)} synonym(s) added"))
    for oid in sorted(set(old) - set(new)):
        out.append((oid, "dropped", "was snapshotted before and was not fetched this run"))
    return out


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
def write_report(rows, changes, rel, stamp, unchecked):
    n = {k: 0 for k in ("error", "warn", "propose", "note")}
    for r in rows:
        for f in r["findings"]:
            if f["level"] in n:
                n[f["level"]] += 1

    o = [
        "# Mondo sync — the register against the ontology",
        "",
        "**Generated by `python3 mondo_sync.py`.** `resolve_mondo.py` finds an",
        "identifier once; this checks that it is still true and reports what Mondo",
        "knows that the register does not. Re-run after a Mondo release.",
        "",
        f"- Mondo release: **{rel}** · checked {stamp}",
        f"- {len(rows)} identifiers checked"
        + (f" · **{unchecked} could not be checked**" if unchecked else ""),
        f"- {n['error']} dead · {n['warn']} scope warnings · {n['propose']} import proposals",
        "",
    ]

    dead = [(r, f) for r in rows for f in r["findings"] if f["level"] == "error"]
    o += ["## Dead join keys", ""]
    if dead:
        o.append("A retired or merged term means every future lookup on this identifier")
        o.append("returns nothing, or worse, the wrong thing. This is the one class of")
        o.append("finding `--apply` will act on, and only where Mondo names exactly one")
        o.append("replacement.")
        o.append("")
        for r, f in dead:
            o.append(f"- **{r['slug']}** — {f['text']}. {f.get('note','')}"
                     + (f" → `{f['fix']}`" if f.get("fix") else ""))
    else:
        o.append("*(none — every identifier in the register is live in this release)*")
    o.append("")

    o += ["## Scope warnings — an `also` entry that is not an equivalence", ""]
    scope = [(r, f) for r in rows for f in r["findings"] if f["kind"] == "scope"]
    if scope:
        o.append("`also` is read as a list of aliases, and `resolve_mondo.py` searches on")
        o.append("it. A term Mondo scopes as broad or narrow names a different-sized")
        o.append("thing. This is the automated form of the near-miss recorded in")
        o.append("gaps.md #43.")
        o.append("")
        for r, f in scope:
            o.append(f"- **{r['slug']}** — {f['text']}")
    else:
        o.append("*(none)*")
    o.append("")

    o += ["## Batch import — what Mondo has that the register does not", "",
          "**Exact synonyms only.** Mondo scopes its synonyms and only",
          "`hasExactSynonym` is an equivalence; importing the rest would put",
          "differently-sized terms into an alias field. Nothing here is written",
          "automatically — adding a synonym also changes what `resolve_mondo.py`",
          "searches on, which is how five identifiers in this register became",
          "reproducible in the first place.", ""]
    props = [(r, f) for r in rows for f in r["findings"] if f["kind"] == "synonyms"]
    for r, f in props:
        o.append(f"- **{r['slug']}** — {f['text']}")
    if not props:
        o.append("*(nothing outstanding)*")
    o.append("")

    o += ["## Label divergence", "",
          "Reported, never acted on. Some of these are deliberate: Mondo names",
          "several diseases after their sequela rather than their cause.", ""]
    labs = [(r, f) for r in rows for f in r["findings"] if f["kind"] == "label"]
    for r, f in labs:
        o.append(f"- **{r['slug']}** — {f['text']}")
    if not labs:
        o.append("*(none)*")
    o.append("")

    # ---- the bridge -------------------------------------------------------
    o += ["## Cross-references — the bridge to everything else", "",
          "This is what resolving `mondo:` actually bought. Each identifier below",
          "is a join key into a dataset the register cannot currently reach.", ""]
    src_count, src_records = {}, {}
    for r in rows:
        for f in r["findings"]:
            if f["kind"] == "xrefs":
                for db in f["xrefs"]:
                    src_count[db] = src_count.get(db, 0) + 1
                    src_records.setdefault(db, []).append(r["slug"])
    o += ["| source | records | what it unlocks |", "|---|---|---|"]
    for db in sorted(src_count, key=lambda d: -src_count[d]):
        o.append(f"| `{db}` | {src_count[db]}/{len(rows)} | {XREF_VALUE.get(db, '—')} |")
    o.append("")
    o.append("Per record:")
    o.append("")
    for r in sorted(rows, key=lambda r: r["slug"]):
        xr = next((f["xrefs"] for f in r["findings"] if f["kind"] == "xrefs"), {})
        if not xr:
            o.append(f"- **{r['slug']}** — *no cross-references*")
            continue
        bits = [f"{db}:{','.join(ids)}" for db, ids in xr.items()]
        o.append(f"- **{r['slug']}** — " + " · ".join(f"`{b}`" for b in bits))
    o.append("")

    # ---- SUB-ENTITIES: what the register distinguishes and the ontology may not
    o += ["## Sub-entities — the distinctions we make against the ones Mondo holds", ""]
    prec = [(r, f) for r in rows for f in r["findings"] if f["kind"] == "precision"]
    noterm = [(r, f) for r in rows for f in r["findings"] if f["kind"] == "no-term"]
    alias = [(r, f) for r in rows for f in r["findings"] if f["kind"] == "alias"]
    strata = [(r, f) for r in rows for f in r["findings"] if f["kind"] == "strata"]

    o += ["### Pointing at a parent — candidates to review", ""]
    if prec:
        o.append("**The record names something narrower than the term it cites.** Every")
        o.append("join made on this identifier silently widens to the parent, which is")
        o.append("how a burden figure for the whole disease ends up attached to a record")
        o.append("about one form of it.")
        o.append("")
        o.append("**These are candidates and never fixes, and `--apply` will not touch")
        o.append("them.** The tool cannot tell a narrower term for this entity from a")
        o.append("sibling that merely shares its words — `pleomorphic adenoma of the")
        o.append("salivary gland` returns *carcinoma ex pleomorphic adenoma*, which is a")
        o.append("malignant transformation and a different disease. Pointing at a broader")
        o.append("term is also sometimes deliberate.")
        o.append("")
        for r, f in prec:
            o.append(f"- **{r['slug']}** — {f['text']}"
                     + (f" → `{f['fix']}`" if f.get("fix") else ""))
    else:
        o.append("*(none)*")
    o.append("")

    o += ["### No term exists — the ontology cannot hold this distinction", ""]
    if noterm:
        o.append("**This is gaps.md #227.** The record points at its parent because")
        o.append("nothing narrower exists. Filing the term upstream is the fix; until")
        o.append("then the register carries a distinction nobody outside can cite.")
        o.append("")
        for r, f in noterm:
            o.append(f"- **{r['slug']}** — {f['text']}")
    else:
        o.append("*(none)*")
    o.append("")

    o += ["### Aliases the ontology holds as entities — candidate sub-records", ""]
    if alias:
        o.append("**NOT a defect list.** `also` is *\"synonyms people actually search")
        o.append("for\"* (SCHEMA.md), explicitly allowed to be broader or narrower than")
        o.append("the entity, and its only consumer is free-text search. Somebody typing")
        o.append("`pernicious anaemia` should land on the `anaemia` record, and that is")
        o.append("this field working.")
        o.append("")
        o.append("What the list is for: these are the aliases Mondo holds as **entities in")
        o.append("their own right**, so each is a candidate for its own record — or for a")
        o.append("stratum — if the register ever decides the parent is doing too much")
        o.append("work. Same question as the strata section, asked from the other side.")
        o.append("")
        for r, f in alias:
            o.append(f"- **{r['slug']}** — {f['text']}")
    else:
        o.append("*(none)*")
    o.append("")

    o += ["### Strata the ontology could address", ""]
    o.append("**Positive findings only, and the silence is not evidence.** A stratum name")
    o.append("is often a descriptive phrase rather than a disease name, so searching one")
    o.append("and finding nothing tells you nothing — reporting that null would be a")
    o.append("check that could not run reporting a result. Absence of a record below")
    o.append("does NOT mean Mondo lacks a term for that stratum.")
    o.append("")
    o.append("**And a one-word stratum name can match a qualifier rather than a")
    o.append("disease.** `prion-disease`'s stratum `acquired` matches a Mondo term")
    o.append("literally labelled *acquired*, which is not an entity anyone would cite.")
    o.append("No filter removes it without also removing `dysentery` and `hydrocele`,")
    o.append("which are one word and genuine — so it is left visible and named here.")
    o.append("")
    if strata:
        for r, f in strata:
            o.append(f"- **{r['slug']}** — {f['text']}")
    else:
        o.append("*(none resolved)*")
    o.append("")

    o += ["## Changes since the last snapshot", ""]
    if changes:
        for oid, kind, text in changes:
            o.append(f"- `{oid}` **{kind}** — {text}")
    else:
        o.append("*(no change, or this is the first run)*")
    o.append("")
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o))


# --------------------------------------------------------------------------
def main():
    argv = sys.argv[1:]
    apply_ = "--apply" in argv
    rm.OFFLINE = offline = "--offline" in argv

    cache = {}
    if os.path.exists(rm.CACHE):
        with open(rm.CACHE, encoding="utf-8") as fh:
            cache = json.load(fh)
    old = {}
    if os.path.exists(SNAPSHOT):
        with open(SNAPSHOT, encoding="utf-8") as fh:
            old = json.load(fh).get("terms", {})

    rows, snapshot, unchecked, written = [], {}, 0, 0
    for path in sorted(glob.glob(os.path.join(ROOT, "entities", "*.yaml"))):
        rec = load(path)
        oid = rec.get("mondo", "unresolved")
        if oid == "unresolved":
            continue
        try:
            term = fetch_term(oid, cache)
        except Exception as e:
            print(f"  ....  {rec['slug']:26} not checked — {type(e).__name__}", file=sys.stderr)
            unchecked += 1
            continue
        if term is None:
            # Not an error we can interpret: the id returned no term at all.
            print(f"  !!    {rec['slug']:26} {oid} returned NO TERM — check by hand")
            unchecked += 1
            continue

        snapshot[oid] = term
        findings = diff_record(rec, term) + diff_subentities(rec, term, cache)
        rows.append({"slug": rec["slug"], "path": path, "id": oid, "findings": findings})

        worst = next((f for f in findings if f["level"] == "error"), None)
        if worst and apply_ and worst.get("fix"):
            text = open(path, encoding="utf-8").read()
            import re as _re
            text, n = _re.subn(r"(?m)^mondo:.*$", f"mondo: {worst['fix']}", text, count=1)
            if n == 1:
                open(path, "w", encoding="utf-8").write(text)
                written += 1
                print(f"  WROTE {rec['slug']:26} {oid} → {worst['fix']} (obsolete, replaced)")
        elif worst:
            print(f"  DEAD  {rec['slug']:26} {oid} is obsolete — {worst.get('note','')}")
        else:
            flags = "".join(sorted({f['level'][0] for f in findings if f['level'] in
                                    ('warn', 'propose')})) or "·"
            print(f"  ok    {rec['slug']:26} {oid}  {flags}")

    with open(rm.CACHE, "w", encoding="utf-8") as fh:
        json.dump(cache, fh)

    changes = diff_snapshot(old, snapshot)
    rel = "offline" if offline else rm.release(cache)
    import time
    stamp = time.strftime("%Y-%m-%d")
    with open(SNAPSHOT, "w", encoding="utf-8") as fh:
        json.dump({"release": rel, "checked": stamp, "terms": snapshot}, fh,
                  indent=1, sort_keys=True)
    write_report(rows, changes, rel, stamp, unchecked)

    dead = sum(1 for r in rows for f in r["findings"] if f["level"] == "error")
    print(f"\n{len(rows)} checked · Mondo {rel} · {dead} dead · {len(changes)} change(s) "
          f"since last snapshot · wrote {os.path.basename(REPORT)}"
          + (f" · {written} written" if written else ""))
    return 1 if dead and not apply_ else 0


if __name__ == "__main__":
    sys.exit(main())
