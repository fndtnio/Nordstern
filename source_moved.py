#!/usr/bin/env python3
"""Source the `moved:` entries against PubMed — proposing, never inventing.

    python3 source_moved.py                    # look everything up, write the ledger
    python3 source_moved.py --apply            # write the ACCEPTED citations only
    python3 source_moved.py --offline          # re-render the ledger from cache
    python3 source_moved.py --only cml         # one record, while you work on it

WHY `moved:` FIRST
------------------
Of 1,582 scalars, 205 are `sourceable` — a public dataset settles them — and 462
are `supportable`, where a citation supports a number without determining it.
**One hundred of those 462 are `moved:` entries, and every one of them is a dated
historical claim with a canonical paper behind it.** They are simultaneously the
most citable thing in the register and, until now, entirely `src: recall`.

They also matter more than prevalence does. `moved:` is what makes a second pass
a comparison rather than a fresh opinion — it is the register's only time series.
If the dates and the claims are wrong, the one thing this project measures is
wrong.

THE RULES IT INHERITS
---------------------
From `resolve_mondo.py`, and they are why this is longer than it needs to be:

  * **It proposes; a person decides.** Nothing is written without `--apply`, and
    `--apply` writes only entries a human has ACCEPTED by pmid in
    moved-sources.json. A wrong citation is worse than a missing one, because a
    missing one announces itself.

  * **It carries the retrieved text.** The `quote` written into a record is
    copied verbatim out of the PubMed response and is never composed here. This
    tool cannot write a sentence; it can only move one. That is the entire
    defence against the failure mode this register is most exposed to — **a
    plausible citation is exactly what a language model produces when it does
    not know, and it looks like success.**

  * **It caches what the source said**, so a later run diffs against the last
    look rather than re-deriving. Same as `mondo-terms.json`.

WHAT IT CANNOT DO, AND WHY THAT IS THE HONEST DIVISION OF LABOUR
----------------------------------------------------------------
It cannot decide *which paper* a `moved:` entry is about. That judgement is in
`moved-sources.json` as a search query written by a human (or a model) who read
the entry — and it is a proposal about where to look, not an assertion about
what is true. The network supplies what the paper says. **Guessing the query is
cheap and recoverable; guessing the quote is fraud.**

Zero dependencies, stdlib only. NCBI asks for <=3 requests/second without a key.
"""

from __future__ import annotations

import datetime
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import check

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "moved-sources.json")
REPORT = os.path.join(HERE, "moved-sources.md")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = {"tool": "nordstern", "email": "nordstern@fndtn.io"}
PAUSE = 0.35

# Publication types that are ABOUT a paper rather than being one. `--apply`
# refuses these outright; the ledger still shows them so a human can see what the
# search returned and fix the query.
NOT_A_SOURCE = {"Comment", "Letter", "Editorial", "Published Erratum",
                "Retraction of Publication", "News", "Biography"}


# --------------------------------------------------------------------------
# the network, kept in one place so --offline is a real guarantee

def _get(path, params, offline):
    if offline:
        raise RuntimeError("offline")
    url = f"{EUTILS}/{path}?" + urllib.parse.urlencode({**params, **TOOL})
    time.sleep(PAUSE)
    with urllib.request.urlopen(url, timeout=30) as fh:
        return fh.read().decode("utf-8", "replace")


def esearch(term, offline, retmax=5):
    raw = _get("esearch.fcgi", {"db": "pubmed", "term": term,
                                "retmode": "json", "retmax": retmax}, offline)
    return json.loads(raw)["esearchresult"].get("idlist", [])


def efetch(pmids, offline):
    """Title, journal, year and the abstract, verbatim, for each pmid."""
    if not pmids:
        return {}
    raw = _get("efetch.fcgi", {"db": "pubmed", "id": ",".join(pmids),
                               "retmode": "xml"}, offline)
    return parse_articles(raw)


def parse_articles(raw):
    """PubMed XML -> {pmid: record}. Split out so it can be tested offline.

    It is tested because it got this wrong once: see the ArticleIdList note
    below. A parser that silently attributes one paper's identifier to another
    produces citations that are wrong in the most convincing possible way.
    """
    out = {}
    for art in ET.fromstring(raw).iter("PubmedArticle"):
        pmid = art.findtext(".//PMID")
        title = "".join(art.find(".//ArticleTitle").itertext()) \
            if art.find(".//ArticleTitle") is not None else ""
        journal = art.findtext(".//Journal/ISOAbbreviation") or \
            art.findtext(".//Journal/Title") or ""
        year = art.findtext(".//JournalIssue/PubDate/Year") or \
            (art.findtext(".//JournalIssue/PubDate/MedlineDate") or "")[:4]
        # THE ARTICLE'S OWN DOI, NOT ONE FROM ITS BIBLIOGRAPHY.
        #
        # `art.iter("ArticleId")` walks the whole <PubmedArticle>, which contains
        # a <ReferenceList> — so the last DOI it finds is whatever the paper
        # happened to cite last. That wrote `10.1016/j.ccell.2022.02.007` into a
        # citation of a JAMA paper, and it looked entirely plausible.
        #
        # **A wrong identifier is worse than a missing one**, and it is exactly
        # the failure this whole tool exists to prevent — arrived at by a bug
        # rather than by a guess, which is the reminder that the discipline has
        # to be mechanical rather than intentional.
        doi = ""
        ids = art.find("PubmedData/ArticleIdList")
        for aid in (list(ids) if ids is not None else []):
            if aid.get("IdType") == "doi":
                doi = aid.text or ""
                break
        # Every abstract section, labelled where PubMed labels them. Kept whole
        # so the quote can be chosen from the retrieved text rather than
        # reconstructed from a summary of it.
        sections = []
        for ab in art.iter("AbstractText"):
            sections.append((ab.get("Label") or "", "".join(ab.itertext()).strip()))
        # PUBLICATION TYPE, BECAUSE CORRESPONDENCE KEEPS WINNING THE SEARCH.
        # Three times now — cetuximab in `head-neck-cancer`, riluzole in `als`,
        # PANTHER in this record — PubMed's top hits for a landmark trial were
        # LETTERS ABOUT IT, carrying the same title, in the same journal, in the
        # same year, with no abstract. A human caught all three. **A rule is
        # cheaper than vigilance**, so the types are carried through and
        # `--apply` refuses them.
        types = [t.text or "" for t in art.iter("PublicationType")]
        out[pmid] = {"pmid": pmid, "title": " ".join(title.split()),
                     "journal": journal, "year": year, "doi": doi,
                     "pubtypes": types, "sections": sections}
    return out


# --------------------------------------------------------------------------
# choosing a quote — mechanical, so the tool cannot editorialise

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def pick_quote(rec, limit=340):
    """A verbatim span from the retrieved abstract. Never composed.

    Prefers the CONCLUSIONS section, because a `moved:` entry is a claim about
    what changed and that is what a conclusion states. Falls back to the last
    labelled section, then to the abstract's opening. Truncates on a sentence
    boundary so the quote is never a fragment ending mid-clause.
    """
    secs = rec.get("sections") or []
    if not secs:
        # NO ABSTRACT — and this is most of the pre-1975 literature, which is
        # exactly where the oldest `moved:` entries point. Cotzias 1967, Banting
        # 1922, the 1989 Duchenne prednisone trial: PubMed has the title and
        # nothing else.
        #
        # The rule is that a quote must be VERBATIM RETRIEVED TEXT, not that it
        # must come from an abstract. A title is retrieved text, it is copied
        # rather than composed, and for a dated historical claim the paper's own
        # title is the appropriate evidence. The tool still cannot write a
        # sentence — it can only move one.
        return rec.get("title", "")
    body = ""
    for want in ("CONCLUSION", "INTERPRETATION", "RESULTS", "FINDINGS"):
        for label, text in secs:
            if label.upper().startswith(want) and text:
                body = text
                break
        if body:
            break
    if not body:
        body = next((t for _, t in reversed(secs) if t), "")
    body = " ".join(body.split())
    if len(body) <= limit:
        return body
    kept = ""
    for sentence in _SENT.split(body):
        if len(kept) + len(sentence) + 1 > limit:
            break
        kept = (kept + " " + sentence).strip()
    return kept or body[:limit].rsplit(" ", 1)[0]


# --------------------------------------------------------------------------
# the register side

def moved_entries():
    """(key, slug, path, entry) for every moved entry, in file order."""
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml"))):
        rec = check.load(path)
        for i, m in enumerate(rec.get("moved") or []):
            key = f"{rec['slug']}|{m['date']}|{m['axis']}"
            out.append((key, rec["slug"], path, i, m))
    return out


def load_ledger():
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as fh:
            return json.load(fh)
    return {"entries": {}}


def save_ledger(led):
    with open(LEDGER, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(led, indent=1, ensure_ascii=False, sort_keys=True) + "\n")


# --------------------------------------------------------------------------
# writing a citation into a record, textually and conservatively

def apply_one(path, entry_index, cite) -> bool:
    """Replace `    src: recall` inside the Nth moved entry with a citation.

    Textual rather than a YAML round-trip on purpose: the corpus is hand-written
    prose with deliberate formatting, and re-emitting it from a parse would
    reflow every block scalar in the file. Refuses unless it finds exactly the
    line it expects, in the entry it expects.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    start = next((i for i, l in enumerate(lines) if l.rstrip() == "moved:"), None)
    if start is None:
        return False
    # entry boundaries: `  - date:` at two-space indent inside moved:
    bounds = [i for i in range(start + 1, len(lines))
              if lines[i].startswith("  - date:")]
    if entry_index >= len(bounds):
        return False
    lo = bounds[entry_index]
    hi = bounds[entry_index + 1] if entry_index + 1 < len(bounds) else len(lines)
    # the next top-level key ends the block
    for i in range(lo, hi):
        if lines[i] and not lines[i].startswith(" "):
            hi = i
            break

    target = [i for i in range(lo, hi) if lines[i].rstrip() == "    src: recall"]
    if len(target) > 1:
        return False
    if not target:
        # NO `src` AT ALL — 47 of 147 moved entries were written without one,
        # because check.py never required it. A dated claim with no stated basis
        # is the thing this pass exists to remove, so insert rather than skip.
        # (check.py now errors on a moved entry with no src, so this branch
        # closes as the corpus is filled in.)
        end = hi
        while end > lo and not lines[end - 1].strip():
            end -= 1
        lines.insert(end, "    src: recall")
        target = [end]

    q = " ".join(str(cite["quote"]).split())
    block = ["    src:",
             f"      id: {cite['id']}",
             f"      retrieved: {cite['retrieved']}",
             "      quote: >"]
    # wrap at a readable width; a folded scalar rejoins the lines
    line = "        "
    for word in q.split():
        if len(line) + len(word) + 1 > 84:
            block.append(line.rstrip())
            line = "        "
        line += word + " "
    block.append(line.rstrip())

    lines[target[0]:target[0] + 1] = block
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return True


# --------------------------------------------------------------------------

def main() -> int:
    offline = "--offline" in sys.argv
    apply = "--apply" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]

    led = load_ledger()
    entries = moved_entries()
    today = datetime.date.today().isoformat()

    todo = [e for e in entries if only is None or e[1] == only]
    proposals, applied, skipped = [], 0, 0

    for key, slug, path, idx, m in todo:
        rowset = led["entries"].setdefault(key, {})
        query = rowset.get("query")
        if not query:
            skipped += 1
            continue

        pmids = [rowset["accept"]] if rowset.get("accept") else None
        if pmids is None:
            try:
                pmids = esearch(query, offline)
            except Exception as exc:                       # noqa: BLE001
                rowset["error"] = str(exc)
                continue
        try:
            fetched = efetch(pmids[:3], offline)
        except Exception as exc:                           # noqa: BLE001
            rowset["error"] = str(exc)
            continue

        rowset.pop("error", None)
        rowset["looked_at"] = today
        rowset["candidates"] = [
            {k: v for k, v in fetched[p].items() if k != "sections"}
            | {"quote": pick_quote(fetched[p])}
            for p in pmids[:3] if p in fetched
        ]
        proposals.append((key, slug, m, rowset))

        if apply and rowset.get("accept"):
            cand = next((c for c in rowset["candidates"]
                         if c["pmid"] == rowset["accept"]), None)
            # Write when there is a quote and the entry is not already cited.
            # A missing `src` is written too — 47 moved entries had none, because
            # check.py never required one. Never overwrites an existing citation.
            bad_type = sorted(set(cand["pubtypes"]) & NOT_A_SOURCE) if cand else []
            if bad_type:
                rowset["refused"] = (f"PMID {cand['pmid']} is {', '.join(bad_type)} "
                                     f"— correspondence about a paper is not the paper")
            elif cand and cand["quote"] and not isinstance(m.get("src"), dict):
                cite = {"id": f"PMID:{cand['pmid']}"
                                + (f" doi:{cand['doi']}" if cand["doi"] else ""),
                        "retrieved": today, "quote": cand["quote"]}
                if apply_one(path, idx, cite):
                    applied += 1

    save_ledger(led)
    write_report(entries, led)

    have = sum(1 for e in entries if led["entries"].get(e[0], {}).get("query"))
    acc = sum(1 for e in entries if led["entries"].get(e[0], {}).get("accept"))
    print(f"{len(entries)} moved entries · {have} with a query · {acc} accepted "
          f"· {len(proposals)} looked up{' · ' + str(applied) + ' written' if apply else ''}")
    if not apply and acc:
        print("  run with --apply to write the accepted citations")
    return 0


def write_report(entries, led):
    out = ["# `moved:` sourcing ledger",
           "",
           "GENERATED by `python3 source_moved.py`. **Proposals, not decisions.**",
           "A row is written into a record only after a pmid is recorded as",
           "`accept` in `moved-sources.json` and `--apply` is passed.",
           "",
           "The `quote` is copied verbatim out of the PubMed response. This tool",
           "cannot compose a sentence — only move one.",
           ""]
    n_q = n_a = 0
    for key, slug, path, idx, m in entries:
        row = led["entries"].get(key, {})
        if row.get("query"):
            n_q += 1
        if row.get("accept"):
            n_a += 1
    out += [f"**{len(entries)} entries · {n_q} with a query · {n_a} accepted.**", ""]
    for key, slug, path, idx, m in entries:
        row = led["entries"].get(key, {})
        if not row.get("query"):
            continue
        out.append(f"## {slug} — {m['date']} · `{m['axis']}`")
        out.append(f"*query:* `{row['query']}`")
        if row.get("error"):
            out.append(f"**error:** {row['error']}")
        for c in row.get("candidates", []):
            mark = "**ACCEPTED**" if c["pmid"] == row.get("accept") else ""
            bad = sorted(set(c.get("pubtypes") or []) & NOT_A_SOURCE)
            flag = f" — **{', '.join(bad)}, NOT A SOURCE**" if bad else ""
            out.append(f"- {mark} PMID {c['pmid']} — *{c['title']}* "
                       f"({c['journal']} {c['year']}){flag}")
            if c.get("quote"):
                out.append(f"  > {c['quote']}")
        out.append("")
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))


if __name__ == "__main__":
    raise SystemExit(main())
