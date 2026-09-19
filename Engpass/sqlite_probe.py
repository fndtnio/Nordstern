#!/usr/bin/env python3
"""Ask the register questions its own query language cannot express.

    python3 sqlite_probe.py            # build nordstern.sqlite, write sqlite-probe.md
    python3 sqlite_probe.py --keep     # ...and leave the database for ad-hoc SQL

**THIS IS AN ANALYSIS TOOL AND IS NEVER SHIPPED.** `web/` stays a static site
served from `slim.js` and `data.js`; putting SQLite in front of a visitor would
mean a megabyte of wasm against a 46 kB index, and would replace a query language
built so that *"a question you cannot type is a question only the author can
ask"* with one fewer people can type. YAML remains truth, `check.py --build`
remains the only thing that generates artifacts, and this reads those artifacts.

WHY SQLITE AND NOT A DICTIONARY. Two reasons, and the first is the interesting
one.

**A generated column is derive-never-store enforced by the storage layer.**

    capability TEXT GENERATED ALWAYS AS (json_extract(doc,'$.derived.capability')) VIRTUAL

That column cannot drift from the document, because it is not stored — it is
computed on read. The register's first rule, expressed as a schema constraint
rather than as a discipline. `index.md` drifted twice precisely because a derived
value was written down by hand (gaps.md #224); a virtual column cannot.
`CHECK (json_valid(doc))` gives the same guarantee at the storage layer that
`check.py` gives at the source layer.

**And the record shape is too variable to flatten.** `survival` is on 83 of 126
records, `strata` on some, `residue`, `window`, `moved` of varying length, and
the schema grows roughly weekly. Normalising that into tables would be lossy and
would need migrating every time a field is added. Storing the document whole and
indexing into it sidesteps all of it.

WHAT IT IS FOR — THE QUESTIONS `query.js` CANNOT ASK.
gaps.md #214 found the dashboard could not link several true figures because
**the query language counts RECORDS**, and blockers, `moved` entries and actor
mentions are not records. Those figures now carry no link and the footer says
why. SQL counts whatever it is told to count, so this answers exactly the
questions the dashboard had to leave unlinked — plus aggregates, self-joins, and
joins across the two registers, none of which the grammar has.

It also does one job that is not a query: it **checks the `attempts/` drafts
against the register**, because those files currently *assert* cross-disease
links (`against`, `succeeded_elsewhere`) that ought to be derived. An assertion
that names a record which does not exist is exactly the drift Engpass's derived
link was designed to prevent.
"""
from __future__ import annotations

import glob
import json
import os
import sqlite3
import sys

# IT LIVES IN `Engpass/` BECAUSE THE BOUNDARY TEST SAID SO, AND THE TEST WAS
# RIGHT. This tool joins both registers, and **only one side is permitted to
# know about both**: Engpass reads Nordstern's built artifact, and Nordstern does
# not know Engpass exists (`test_boundary.py`). Written first into Nordstern's
# root, it read `Engpass/obstacles/` directly — a path reference across the
# boundary, which sat undetected for several commits because the boundary suite
# was not run. **A tool that joins two registers belongs on the side allowed to
# see both.**
HERE = os.path.dirname(os.path.abspath(__file__))
NORDSTERN = os.path.normpath(os.path.join(HERE, ".."))
ARTIFACT = os.path.join(NORDSTERN, "web", "nordstern.json")
ENGPASS = os.path.join(HERE, "obstacles")
ATTEMPTS = os.path.join(NORDSTERN, "attempts")
DB = os.path.join(HERE, "nordstern.sqlite")
REPORT = os.path.join(HERE, "sqlite-probe.md")

SCHEMA = """
CREATE TABLE records (
  doc        TEXT NOT NULL CHECK (json_valid(doc)),
  slug       TEXT GENERATED ALWAYS AS (json_extract(doc,'$.slug'))                    VIRTUAL,
  name       TEXT GENERATED ALWAYS AS (json_extract(doc,'$.name'))                    VIRTUAL,
  status     TEXT GENERATED ALWAYS AS (json_extract(doc,'$.derived.status'))          VIRTUAL,
  capability TEXT GENERATED ALWAYS AS (json_extract(doc,'$.derived.capability'))      VIRTUAL,
  quadrant   TEXT GENERATED ALWAYS AS (json_extract(doc,'$.derived.quadrant'))        VIRTUAL,
  terms      TEXT GENERATED ALWAYS AS (json_extract(doc,'$.derived.terms'))           VIRTUAL,
  reach      REAL GENERATED ALWAYS AS (json_extract(doc,'$.derived.reach'))           VIRTUAL,
  deaths     REAL GENERATED ALWAYS AS (json_extract(doc,'$.burden.deaths.value'))     VIRTUAL,
  mechanism  TEXT GENERATED ALWAYS AS (json_extract(doc,'$.axes.mechanism'))          VIRTUAL,
  interv     TEXT GENERATED ALWAYS AS (json_extract(doc,'$.axes.intervention'))       VIRTUAL,
  surv       REAL GENERATED ALWAYS AS (json_extract(doc,'$.survival.treated.value'))  VIRTUAL,
  gain       REAL GENERATED ALWAYS AS (json_extract(doc,'$.derived.survival_gain'))   VIRTUAL,
  outcome    TEXT GENERATED ALWAYS AS (json_extract(doc,'$.derived.survival_outcome'))VIRTUAL
);
CREATE INDEX i_cap    ON records(capability);
CREATE INDEX i_reach  ON records(reach);
CREATE INDEX i_deaths ON records(deaths);

-- ONE ROW PER BLOCKER. This is the table the query language cannot be:
-- `blocker.kind:knowledge` returns the RECORDS that have one, which is a
-- smaller and different number from how many there are (gaps.md #214).
CREATE TABLE blockers (
  slug     TEXT NOT NULL,
  doc      TEXT NOT NULL CHECK (json_valid(doc)),
  kind     TEXT GENERATED ALWAYS AS (json_extract(doc,'$.kind'))     VIRTUAL,
  standing TEXT GENERATED ALWAYS AS (json_extract(doc,'$.standing')) VIRTUAL,
  scale    REAL GENERATED ALWAYS AS (json_extract(doc,'$.scale'))    VIRTUAL,
  blocks   TEXT GENERATED ALWAYS AS (json_extract(doc,'$.blocks'))   VIRTUAL
);
CREATE INDEX i_bk ON blockers(kind);

-- The derived link, one row per (record, obstacle). Engpass computes this from
-- Nordstern; here it is a join key so the two registers can be queried together.
CREATE TABLE obstacle_links (slug TEXT NOT NULL, obstacle TEXT NOT NULL);
CREATE INDEX i_ol ON obstacle_links(obstacle);

CREATE TABLE obstacles (slug TEXT PRIMARY KEY, name TEXT, kind TEXT);

CREATE TABLE attempts (
  disease  TEXT NOT NULL,
  doc      TEXT NOT NULL CHECK (json_valid(doc)),
  approach TEXT GENERATED ALWAYS AS (json_extract(doc,'$.approach')) VIRTUAL,
  modality TEXT GENERATED ALWAYS AS (json_extract(doc,'$.modality')) VIRTUAL,
  phase    INT  GENERATED ALWAYS AS (json_extract(doc,'$.phase'))    VIRTUAL,
  read_out INT  GENERATED ALWAYS AS (json_extract(doc,'$.read_out')) VIRTUAL,
  outcome  TEXT GENERATED ALWAYS AS (json_extract(doc,'$.outcome'))  VIRTUAL,
  follows  TEXT GENERATED ALWAYS AS (json_extract(doc,'$.follows'))  VIRTUAL
);
CREATE TABLE attempt_links (disease TEXT, approach TEXT, other TEXT, relation TEXT);

-- ONE RECORD NAMING ANOTHER AS A CAUSE. gaps.md #242: `hearing-loss` listed the
-- infectious causes of childhood deafness and omitted congenital CMV, its
-- largest one, and nothing in the register found it — every existing guard
-- checks a record against itself or against a derivation, none checks a record
-- against another record.
CREATE TABLE claims (
  a TEXT NOT NULL,          -- the record making the claim
  b TEXT NOT NULL,          -- the record it names
  linked INT NOT NULL,      -- does a cite `b-slug` explicitly?
  reciprocated INT NOT NULL,-- does b name a at all?
  snippet TEXT
);
CREATE INDEX i_claims ON claims(b);
"""

# Causal language. A bare mention is not a finding — `stroke` and `tuberculosis`
# appear in dozens of records as comparisons and comorbidities, and matching on
# names alone produced 254 unlinked pairs, which is a list rather than a
# work-list. Requiring a causal verb near the name cuts it to roughly 50.
CAUSAL = (r"(?:leading cause|commonest cause|major cause|principal cause|causes?|causing|"
          r"caused by|results? in|leads? to|complication of|drives?|responsible for|precursor)")


def build(conn):
    conn.executescript(SCHEMA)
    with open(ARTIFACT, encoding="utf-8") as fh:
        recs = json.load(fh)["records"]
    recs = [r for r in recs if r["derived"]["status"] == "active"]
    conn.executemany("INSERT INTO records(doc) VALUES (?)",
                     [(json.dumps(r),) for r in recs])
    for r in recs:
        for b in r["blockers"]:
            conn.execute("INSERT INTO blockers(slug,doc) VALUES (?,?)",
                         (r["slug"], json.dumps(b)))
            for o in (b.get("obstacles") or []):
                conn.execute("INSERT INTO obstacle_links VALUES (?,?)", (r["slug"], o))

    # ---- cross-record causal claims -------------------------------------
    import re
    prose = {r["slug"]: " ".join([
        json.dumps(r.get("witness", "")),
        " ".join(b["what"] for b in r["blockers"]),
        json.dumps(r.get("holes", "")),
        " ".join(m.get("why", "") for m in (r.get("moved") or [])),
    ]) for r in recs}
    for a in recs:
        for b in recs:
            if a["slug"] == b["slug"] or len(b["name"]) < 5:
                continue
            nm = re.escape(b["name"])
            pat = re.compile(rf"(?:{CAUSAL}[^.]{{0,90}}?\b{nm}\b|\b{nm}\b[^.]{{0,60}}?{CAUSAL})",
                             re.I)
            m = pat.search(prose[a["slug"]])
            if not m:
                continue
            conn.execute(
                "INSERT INTO claims VALUES (?,?,?,?,?)",
                (a["slug"], b["slug"],
                 int(f"`{b['slug']}`" in prose[a["slug"]]),
                 # RECIPROCITY COUNTS THE SLUG CITATION TOO, WHICH IS HOW THIS
                 # REGISTER ACTUALLY LINKS. Fixing `obesity` to name its
                 # downstream cancers as `uterine-cancer` did not clear the
                 # flag, because the test looked for the NAME *uterine cancer*
                 # and the prose contains the hyphenated slug. **The check did
                 # not recognise the register's own linking convention.**
                 #
                 # RECIPROCITY MATCHES `name` AND `also`, NOT `name` ALONE.
                 # Records refer to each other in clinical rather than canonical
                 # form: `epilepsy` names *neurocysticercosis*, and the record it
                 # means is called *taeniasis and cysticercosis*. Matching only
                 # the name reported that as unreciprocated, which was wrong.
                 int(f"`{a['slug']}`" in prose[b["slug"]]
                     or any(re.search(rf"\b{re.escape(t)}\b", prose[b["slug"]], re.I)
                            for t in [a["name"]] + list(a.get("also") or [])
                            if len(t) >= 5)),
                 re.sub(r"\s+", " ", m.group(0))[:150]))

    sys.path.insert(0, NORDSTERN)
    import check                                                   # noqa: E402
    for p in sorted(glob.glob(os.path.join(ENGPASS, "*.yaml"))):
        o = check.load(p)
        conn.execute("INSERT INTO obstacles VALUES (?,?,?)",
                     (o["slug"], o.get("name"), o.get("kind")))
    for p in sorted(glob.glob(os.path.join(ATTEMPTS, "*.yaml"))):
        d = check.load(p)
        for a in d.get("attempts") or []:
            conn.execute("INSERT INTO attempts(disease,doc) VALUES (?,?)",
                         (d["disease"], json.dumps(a)))
            for other in (a.get("against") or []):
                if other != d["disease"]:
                    conn.execute("INSERT INTO attempt_links VALUES (?,?,?,?)",
                                 (d["disease"], a["approach"], other, "also-tried-in"))
            for other in (a.get("succeeded_elsewhere") or []):
                conn.execute("INSERT INTO attempt_links VALUES (?,?,?,?)",
                             (d["disease"], a["approach"], other, "succeeded-in"))
    conn.commit()
    return len(recs)


def q(conn, sql, args=()):
    return conn.execute(sql, args).fetchall()


def main() -> int:
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    n = build(conn)

    L = ["# SQLite probe — the questions the query language cannot ask", "",
         "**GENERATED by `python3 sqlite_probe.py`** from `web/nordstern.json`, "
         "`Engpass/obstacles/` and `attempts/`. **Never shipped to `web/`** — the site "
         "stays static and served from `slim.js`.", "",
         "Records are stored as whole JSON documents with **virtual generated columns** "
         "indexing into them, so no derived value is ever written down: "
         "`json_extract` computes on read and cannot drift from the document. That is "
         "derive-never-store enforced by the storage layer rather than by discipline.", ""]

    # 1 — the thing gaps.md #214 could not link
    L += ["## 1. Blockers counted as blockers", "",
          "`blocker.kind:knowledge` returns the **records** that have at least one. This "
          "counts the blockers themselves — the figure the dashboard carries with no link "
          "because the grammar cannot express it (gaps.md #214).", "",
          "| kind | blockers | records | blockers per record |", "|---|---:|---:|---:|"]
    for kind, nb, nr in q(conn, """
        SELECT kind, count(*), count(DISTINCT slug) FROM blockers
        GROUP BY kind ORDER BY 2 DESC"""):
        L.append(f"| `{kind}` | {nb} | {nr} | {nb/nr:.2f} |")

    # 2 — aggregate, which the grammar has no verb for
    L += ["", "## 2. Aggregates", "",
          "The query language filters and lists. It has no `avg`, no `sum`, no "
          "`group by` — so every figure on the dashboard that is a mean or a total was "
          "computed in `check.py` and hard-coded into the snapshot.", "",
          "| capability | records | mean reach | total deaths/yr | mean treated survival |",
          "|---|---:|---:|---:|---:|"]
    for cap, c, r, d, s in q(conn, """
        SELECT capability, count(*), round(avg(reach),3),
               sum(coalesce(deaths,0)), round(avg(surv),3)
        FROM records GROUP BY capability ORDER BY 2 DESC"""):
        L.append(f"| {cap} | {c} | {r} | {d/1e6:.1f}M | {s if s is not None else '—'} |")

    # 3 — cross-register join
    L += ["", "## 3. Nordstern joined to Engpass", "",
          "Two registers, one query. Engpass computes this link in its own build; here "
          "it is a join, so the mortality sitting behind each obstacle can be asked for "
          "directly — which neither register's own tooling does.", "",
          "| obstacle | records | deaths/yr behind it | mean reach |", "|---|---:|---:|---:|"]
    for ob, c, d, r in q(conn, """
        SELECT ol.obstacle, count(DISTINCT r.slug), sum(coalesce(r.deaths,0)),
               round(avg(r.reach),3)
        FROM obstacle_links ol JOIN records r ON r.slug = ol.slug
        GROUP BY ol.obstacle ORDER BY 2 DESC"""):
        L.append(f"| `{ob}` | {c} | {d/1e6:.1f}M | {r} |")

    # 4 — a self-join nobody has run
    L += ["", "## 4. Which obstacles co-occur on the same record", "",
          "A self-join. **Nothing in either register has asked this**, and it is the "
          "question that would say whether the obstacles are independent or are facets "
          "of the same thing.", "",
          "| obstacle A | obstacle B | records citing both |", "|---|---|---:|"]
    for a, b, c in q(conn, """
        SELECT x.obstacle, y.obstacle, count(DISTINCT x.slug)
        FROM obstacle_links x JOIN obstacle_links y
          ON x.slug = y.slug AND x.obstacle < y.obstacle
        GROUP BY 1,2 HAVING count(DISTINCT x.slug) >= 2 ORDER BY 3 DESC"""):
        L.append(f"| `{a}` | `{b}` | {c} |")

    # 5 — the attempts drafts
    rows = q(conn, "SELECT count(*), count(DISTINCT disease) FROM attempts")
    if rows and rows[0][0]:
        L += ["", "## 5. The attempts drafts", "",
              f"{rows[0][0]} attempts across {rows[0][1]} diseases, from `attempts/*.yaml`. "
              "These are drafts and nothing validates them.", "",
              "| outcome | n | earliest | latest |", "|---|---:|---:|---:|"]
        for o, c, lo, hi in q(conn, """
            SELECT outcome, count(*), min(read_out), max(read_out)
            FROM attempts GROUP BY outcome ORDER BY 2 DESC"""):
            L.append(f"| `{o}` | {c} | {lo} | {hi} |")

        L += ["", "### The chains", "",
              "`follows` links a confirmatory readout to the result that motivated it. "
              "**The gap between them measures how long a field held a belief that did "
              "not survive** — the one figure in these files a funder would want.", ""]
        # A YEAR REGEX, NOT "THE FIRST FOUR DIGITS". The first version concatenated
        # every digit in the string, so `exenatide phase 2 (2017)` yielded 2201 and
        # a span of MINUS 177 YEARS. **That is a schema finding, not just a bug**:
        # `follows` is free text naming another attempt, so anything reading it has
        # to parse prose. It should be a reference to an attempt id, and the fact
        # that a trivial consumer got it wrong immediately is the argument.
        import re as _re
        for dis, app, ro, fol in q(conn, """
            SELECT disease, approach, read_out, follows FROM attempts
            WHERE follows IS NOT NULL ORDER BY read_out"""):
            m = _re.findall(r"\b(1[89]\d\d|20[0-2]\d)\b", fol or "")
            span = f"{int(ro)-int(m[-1])} years" if m else "**unparseable**"
            L.append(f"- **{dis}** · {app} — {fol} → {ro} · **{span}**")

        # 6 — the check that is not a query
        L += ["", "### Cross-references, checked against the register", "",
              "The drafts **assert** `against` and `succeeded_elsewhere`. Engpass's rule "
              "is that such a link must be *derived*, because a stored one can drift. "
              "Until it is, this at least checks that every named record exists.", ""]
        bad = q(conn, """
            SELECT DISTINCT al.other, al.relation, al.approach FROM attempt_links al
            LEFT JOIN records r ON r.slug = al.other WHERE r.slug IS NULL""")
        if bad:
            for other, rel, app in bad:
                L.append(f"- **`{other}` does not exist** — named as *{rel}* by `{app}`")
        else:
            L.append("*(every cross-referenced record exists)*")
            for other, rel, app, cap in q(conn, """
                SELECT al.other, al.relation, al.approach, r.capability
                FROM attempt_links al JOIN records r ON r.slug = al.other
                ORDER BY al.relation, al.other"""):
                L.append(f"- `{app}` — *{rel}* → **{other}** (`{cap}`)")

    # 6 — the check that found gaps.md #242 after the fact
    tot, lk, rec_ = q(conn, """SELECT count(*), sum(linked), sum(reciprocated)
                               FROM claims""")[0]
    work = q(conn, """SELECT a,b,snippet FROM claims
                      WHERE linked=0 AND reciprocated=0 ORDER BY b,a""")
    L += ["", "## 6. One record naming another as a cause", "",
          "**The guard the register did not have.** `hearing-loss` listed the infectious "
          "causes of childhood deafness and omitted congenital CMV, its largest — and "
          "nothing found it, because every existing check tests a record against itself "
          "or against a derivation (gaps.md #242).", "",
          "A bare mention is not a finding: `stroke` and `tuberculosis` appear in dozens "
          "of records as comparisons. **Requiring causal language near the name** cuts "
          f"254 raw mentions to {tot}.", "",
          f"- **{tot}** causal cross-record claims",
          f"- {lk} already cite the other record's slug",
          f"- {rec_} are mentioned back by the other record, under some name",
          f"- **{len(work)} are neither linked nor reciprocated** — the work-list below", "",
          "### Records named as a cause by others, ranked", "",
          "| named record | claims against it | by |", "|---|---:|---|"]
    for b, c, who in q(conn, """SELECT b, count(*), group_concat(a, ', ')
                                FROM claims WHERE linked=0 AND reciprocated=0
                                GROUP BY b HAVING count(*) >= 2 ORDER BY 2 DESC"""):
        L.append(f"| **`{b}`** | {c} | {who} |")
    # NOT A HAND-WRITTEN EXAMPLE. The first version of this report said in prose
    # that `obesity` was the clearest hit — then `obesity` was fixed, and the
    # sentence stayed true-looking and false, in a GENERATED file. Exactly the
    # drift that broke `index.md` (gaps.md #224), reproduced inside the tool
    # written to catch drift. The headline example is now computed.
    top = q(conn, """SELECT b, count(*) FROM claims WHERE linked=0 AND reciprocated=0
                     GROUP BY b ORDER BY 2 DESC, b LIMIT 1""")
    if top:
        L += ["", f"**The current head of the list is `{top[0][0]}`**, named as a cause by "
              f"{top[0][1]} records that it does not name back — the shape the CMV and "
              "obesity omissions both had.", ""]
    L += ["**Two have already been fixed this way**: `hearing-loss`, which listed the "
          "infectious causes of childhood deafness and omitted congenital CMV; and "
          "`obesity`, which said *roughly thirteen cancers* where every other downstream "
          "record was named by slug. **A number is not a link, and a count is the form an "
          "omission takes when it looks like precision.**", "",
          "### The full work-list", "",
          "**Roughly half are false positives and the classes are predictable**: "
          "comparison prose (*\"unlike X\"*, *\"the same arithmetic as X\"*), shared "
          "risk-factor lists, and sub-entity collisions — *portal hypertension* matching "
          "the `hypertension` record. Read, do not apply.", ""]
    for a, b, s in work:
        L.append(f"- `{a}` → **`{b}`** — …{s}…")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    keep = "--keep" in sys.argv
    print(f"{n} records · {q(conn,'SELECT count(*) FROM blockers')[0][0]} blockers · "
          f"{q(conn,'SELECT count(*) FROM obstacle_links')[0][0]} obstacle links · "
          f"{q(conn,'SELECT count(*) FROM attempts')[0][0]} attempts")
    print(f"wrote {os.path.basename(REPORT)}")
    conn.close()
    if keep:
        print(f"kept {os.path.basename(DB)} — regenerable, do not commit")
    else:
        os.remove(DB)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
