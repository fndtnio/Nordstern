#!/usr/bin/env python3
"""Fallakte's checker: the case-file register, and its links outward.

Run:  python3 check.py           # check + the derived tables
      python3 check.py --json    # the cases, machine-readable
      python3 check.py --build   # render into Nordstern's web/ for publishing

WHAT THIS IS. Nordstern rates a disease. Engpass clusters what is in the way.
Fallakte holds the working file on a disease somebody has actually started on —
the mechanism chain with a status on every step, the open questions, the models
built so far and what each one refuses to claim, and a log.

THE DEPENDENCY RUNS OUTWARD ONLY, AND NESTING DOES NOT CHANGE IT. A case file
points at a Nordstern record and at Engpass obstacles. Neither register knows
this directory exists; `test_boundary.py` asserts that rather than trusting it.

AND THE CROSSINGS GO THROUGH BUILT ARTIFACTS, NOT SOURCE. This file reads
Nordstern's `web/nordstern.json` and Engpass's published snapshot. It does not
walk either register's source directory, for the same reason Engpass does not
walk Nordstern's: re-deriving somebody else's ratings is how two files start
disagreeing about what they both claim to say. The one permitted import is
Nordstern's bounded YAML loader, by explicit file path — it is a loader, not a
model, and the path form is used because both files are named check.py and
`import check` resolves through sys.modules (the bug Engpass documents).
"""

from __future__ import annotations

import datetime
import glob
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NORDSTERN = os.path.normpath(os.path.join(HERE, ".."))
HAMBURG = os.path.normpath(os.path.join(NORDSTERN, ".."))
CASES = os.path.join(HERE, "cases")
WEB = os.path.join(NORDSTERN, "web")

_spec = importlib.util.spec_from_file_location(
    "nordstern_check", os.path.join(NORDSTERN, "check.py"))
nordstern = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("nordstern_check", nordstern)
_spec.loader.exec_module(nordstern)

_rspec = importlib.util.spec_from_file_location(
    "fallakte_render", os.path.join(HERE, "render.py"))
render = importlib.util.module_from_spec(_rspec)
sys.modules.setdefault("fallakte_render", render)
_rspec.loader.exec_module(render)

STATUSES = {"active", "dormant", "closed"}
Q_STATUSES = {"open", "partial", "answered", "abandoned"}
PARTNER_KINDS = {"nonprofit", "clinic", "academic", "patient-org", "company", "individual"}
ID_RE = re.compile(r"^FND-C-\d{4}$")
QID_RE = re.compile(r"^Q\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Every tool a `models[]` entry may name. A typo here is a dead link in a public
# file, which is the failure this list exists to catch.
TOOLS = {"Strangschrift", "Schaltwerk", "Strombild", "Sperrwerk", "Raumwerk",
         "Werdenfaltung", "Nordstern", "Engpass", "other"}

# How close a reader is to actually running the thing.
ACCESS = {
    "live":    "openable on the public site today, and `live:` says where",
    "repo":    "the source is public; the playground on the site is behind it",
    "private": "neither. It exists here and nowhere a reader can reach",
}

# THE SPLIT, ENFORCED. These keys held prose until 2026-10-10 and now live in
# README.md. Finding one here again means the two files have started to hold the
# same thing, which is the failure the split was made to prevent — a spine that
# slowly becomes a second, worse copy of the case file.
PROSE_KEYS = {
    "shows":      "a model's `shows` belongs in README section 5",
    "refuses":    "a model's `refuses` belongs in README section 5",
    "ask":        "a question's text belongs in README section 4",
    "would_move": "what an answer would change belongs in README section 4",
    "asks":       "the asks belong in README section 9",
    "log":        "the log belongs in README section 10",
    "routes":     "the routes belong in README section 8",
    "role":       "what a partner brings belongs in README section 1",
    "what":       "prose belongs in README",
    "why_open":   "use `one_line`, and the reasons in README",
}
ONE_LINE_MAX = 320


class DeadLinkError(ValueError):
    pass

# VOCABULARY RETIRED IN GLOSSARY.md, because each one hid the question it was
# standing in for. A case file that uses one of these has stopped being readable
# by the person the register is for, which is somebody new to the field.
RETIRED_TERMS = {
    "relevant cells": "name the cell type instead (GLOSSARY.md)",
    "disease at birth": "say which of defect-present / misbehaving / detectable / "
                        "harming you mean (GLOSSARY.md)",
}


def _text(v) -> str:
    return v if isinstance(v, str) else ""


def _walk_keys(node):
    """Every mapping key anywhere in the loaded case, for the prose guard."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from _walk_keys(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk_keys(v)


def nordstern_records() -> dict:
    """Nordstern's built artifact, keyed by slug. Absent is a skip, not a pass."""
    path = os.path.join(WEB, "nordstern.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return {r["slug"]: r for r in json.load(fh)["records"]}


def engpass_obstacles() -> set:
    """Engpass's published snapshot, newest first. Absent is a skip."""
    snaps = sorted(glob.glob(os.path.join(WEB, "snapshots/engpass", "2*.json")))
    if not snaps:
        return set()
    with open(snaps[-1], encoding="utf-8") as fh:
        return set((json.load(fh).get("blocks_members") or {}).keys())


def load_case(path: str) -> dict:
    case = nordstern.load(path)
    case["_path"] = path
    case["_dir"] = os.path.dirname(path)
    return case


def cases() -> list:
    return [load_case(p) for p in sorted(glob.glob(os.path.join(CASES, "*", "case.yaml")))]


def check(case: dict, records: dict, obstacles: set) -> tuple:
    """Return (errors, warnings, skips) for one case file."""
    errors, warnings, skips = [], [], []
    rel = os.path.relpath(case["_path"], HERE)
    e = lambda m: errors.append(f"{rel}: {m}")
    w = lambda m: warnings.append(f"{rel}: {m}")

    slug = case.get("slug")
    if not slug:
        e("no slug")
    elif slug != os.path.basename(case["_dir"]):
        e(f"slug {slug!r} does not match its directory {os.path.basename(case['_dir'])!r}")

    cid = case.get("id")
    if not ID_RE.match(_text(cid)):
        e(f"id {cid!r} is not FND-C-NNNN — an id is permanent and is what a citation resolves against")

    for field in ("disease", "disease_id", "opened", "updated", "status", "one_line"):
        if not _text(case.get(field)).strip():
            e(f"missing {field}")

    for field in ("opened", "updated"):
        if not DATE_RE.match(_text(case.get(field))):
            e(f"{field} {case.get(field)!r} is not YYYY-MM-DD")
    if (DATE_RE.match(_text(case.get("opened"))) and DATE_RE.match(_text(case.get("updated")))
            and case["updated"] < case["opened"]):
        e(f"updated ({case['updated']}) is before opened ({case['opened']})")

    if case.get("status") not in STATUSES:
        e(f"status {case.get('status')!r} not in {sorted(STATUSES)}")

    one = _text(case.get("one_line")).strip()
    if len(one) > ONE_LINE_MAX:
        e(f"one_line is {len(one)} characters — cap is {ONE_LINE_MAX}. It is a listing "
          f"line, not a summary; the summary is README section 1")

    # --- THE SPLIT: no prose in the spine -----------------------------------
    for key in set(_walk_keys(case)):
        if key in PROSE_KEYS:
            e(f"`{key}` is prose and must not be in case.yaml — {PROSE_KEYS[key]}")

    readme_path = os.path.join(case["_dir"], "README.md")
    if not os.path.exists(readme_path):
        e("no README.md beside case.yaml — the spine without the case file is not a case file")
        body = ""
    else:
        with open(readme_path, encoding="utf-8") as fh:
            body = fh.read()

    # --- the link to Nordstern: the disease has to be a real record ----------
    disease = _text(case.get("disease"))
    if not records:
        skips.append("Nordstern's web/nordstern.json is absent — disease links unchecked "
                     "(run the register's `check.py --build` first)")
    elif disease and disease not in records:
        e(f"disease {disease!r} is not a Nordstern record")
    elif disease:
        want = records[disease].get("id")
        if _text(case.get("disease_id")) != want:
            e(f"disease_id {case.get('disease_id')!r} is not {disease!r}'s id ({want})")

    # --- the link to Engpass: obstacle slugs have to resolve -----------------
    def check_obstacles(slugs, where):
        if not isinstance(slugs, list):
            if slugs is not None:
                e(f"{where}: obstacles must be a list")
            return
        if not obstacles:
            return
        for sl in slugs:
            if sl not in obstacles:
                e(f"{where}: obstacle {sl!r} is not in Engpass")

    if not obstacles:
        skips.append("Engpass's snapshot is absent — obstacle links unchecked")
    check_obstacles(case.get("obstacles"), "obstacles")

    for i, prt in enumerate(case.get("working_with") or [], 1):
        if not isinstance(prt, dict):
            e(f"working_with[{i}] is not a mapping")
            continue
        if prt.get("kind") not in PARTNER_KINDS:
            e(f"working_with[{i}]: kind {prt.get('kind')!r} not in {sorted(PARTNER_KINDS)}")
        if prt.get("named") not in (True, False):
            e(f"working_with[{i}]: `named` must be true or false — say whether this "
              f"partner has agreed to appear in a public repository")

    # --- models: the path resolves AND the README actually discusses it ------
    models = case.get("models") or []
    if not models:
        w("no models — allowed, and worth a sentence in the README saying why")
    for i, m in enumerate(models, 1):
        if not isinstance(m, dict):
            e(f"models[{i}] is not a mapping")
            continue
        if m.get("tool") not in TOOLS:
            e(f"models[{i}]: tool {m.get('tool')!r} not in {sorted(TOOLS)}")
        # ACCESS, NOT A BOOLEAN, because `published: true` turned out to mean
        # three different things. The repos are public; the playgrounds on the
        # site are a sync behind them; and Schaltwerk is neither. A reader needs
        # to know which, and "can I click it" is the only question they are
        # actually asking.
        acc = m.get("access")
        if acc not in ACCESS:
            e(f"models[{i}]: access {acc!r} not in {sorted(ACCESS)}")
        live = _text(m.get("live"))
        if acc == "live" and not live:
            e(f"models[{i}]: access is `live` and there is no `live:` URL — say "
              f"where, or say `repo`")
        if acc != "live" and live:
            e(f"models[{i}]: has a `live:` URL but access is {acc!r} — a link a "
              f"reader cannot follow is worse than no link")
        if live and not live.startswith("https://"):
            e(f"models[{i}]: live URL must be https: {live!r}")
        ref = _text(m.get("ref"))
        if not ref:
            e(f"models[{i}]: no ref")
            continue
        if not os.path.exists(os.path.normpath(os.path.join(case["_dir"], ref))):
            e(f"models[{i}]: ref does not resolve: {ref}")
        # A listed model nobody wrote about is a citation, not a case file. Match
        # the stem INSIDE A CODE SPAN, which is how the README names a model
        # (Strombild `iron`), not anywhere in the prose. A bare substring search
        # passed `iron.strombild` on a sentence about iron deficiency written
        # before the model existed — a short generic filename makes the loose
        # check useless exactly when it matters.
        stem = os.path.splitext(os.path.basename(ref))[0]
        if body and not re.search(r"`[^`\n]*\b" + re.escape(stem) + r"\b[^`\n]*`", body):
            e(f"models[{i}]: README never names `{stem}` in a code span — say what it "
              f"shows and what it refuses, or do not list it")

    # --- questions: the id is in the spine, the question is in the README ----
    qids = set()
    for i, q in enumerate(case.get("questions") or [], 1):
        if not isinstance(q, dict):
            e(f"questions[{i}] is not a mapping")
            continue
        qid = _text(q.get("id"))
        if not QID_RE.match(qid):
            e(f"questions[{i}]: id {qid!r} is not Q<n>")
        elif qid in qids:
            e(f"questions[{i}]: duplicate id {qid!r}")
        else:
            qids.add(qid)
        if q.get("status") not in Q_STATUSES:
            e(f"questions[{i}]: status {q.get('status')!r} not in {sorted(Q_STATUSES)}")
        check_obstacles(q.get("obstacles"), f"questions[{i}]")
        if qid and body and not re.search(r"\b" + re.escape(qid) + r"\b", body):
            e(f"questions[{i}]: README never mentions {qid} — a question with a status "
              f"and no text is a number, not a question")

    # --- the README has to carry the log, and the marked mechanism chain -----
    if body:
        if _text(case.get("updated")) and case["updated"] not in body:
            e(f"README has no entry dated {case['updated']}, which is `updated` in the "
              f"spine. The log lives in the README and the spine points at its newest date")
        if _text(case.get("opened")) and case["opened"] not in body:
            w(f"README never mentions the opening date {case['opened']}")
        for marker in ("established", "open"):
            if marker not in body:
                w(f"README never says {marker!r} — is every step of the mechanism marked?")
        if "Sources" not in body:
            w("README has no Sources section — an unread source has to be markable")
        if "GLOSSARY" not in body:
            w("README does not link GLOSSARY.md — a reader new to the field needs the "
              "terms, and the glossary exists so each case does not redefine them")
        # A GUARD THAT FIRES ON ITS OWN DOCUMENTATION GETS SUPPRESSED, and a
        # suppressed guard is worse than none — Engpass's boundary test learned
        # this first. This one fired on the sentence in the PV case file that
        # explains WHY these terms were retired. So emphasised and quoted spans
        # are stripped before the search: naming a term is always allowed,
        # USING it as though it meant something is not.
        # The character classes EXCLUDE newlines on purpose. With `[^*]+` a bold
        # pair matches across lines, swallows the italics between it, and can
        # end mid-span — which left `*relevant cells*` half-stripped and the
        # words still in the haystack. An emphasis span is a one-line thing.
        quoted = re.compile(r"`[^`\n]*`|\*\*[^*\n]+\*\*|\*[^*\n]+\*|_[^_\n]+_")
        prose = quoted.sub(" ", body).lower()
        for term, fix in RETIRED_TERMS.items():
            if term in prose:
                e(f"README uses the retired term {term!r} — {fix}")

    return errors, warnings, skips


# WHERE A REPO PATH GOES WHEN THE PAGE IS PUBLISHED.
#
# A case file is markdown in a repository and links to its neighbours the way a
# file does: `../../GLOSSARY.md`. Published, those are dead — they point at
# paths that do not exist on the site, and a dead link in a public page is the
# failure this register's checker exists to catch.
#
# So the links are rewritten at build time rather than being written twice. The
# two site pages are named here; everything else resolves to the public source
# on GitHub, which is where the file actually is.
GITHUB = {
    "Nordstern": "https://github.com/fndtnio/Nordstern/blob/main/",
    "Strangschrift": "https://github.com/fndtnio/Strangschrift/blob/main/",
    "strombild": "https://github.com/fndtnio/Strombild/blob/main/",
}
SITE_LINKS = {
    "GLOSSARY.md": "fallakte.html#terms",
    "TEMPLATE.md": "fallakte.html#template",
    "README.md": "fallakte.html",
}
_HREF = re.compile(r'href="([^"]+)"')


def _rewrite_link(href: str, case_dir: str) -> str:
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    base = os.path.basename(href.split("#")[0])
    if base in SITE_LINKS and "cases/" not in href:
        frag = href.split("#")[1] if "#" in href else ""
        out = SITE_LINKS[base]
        return out + ("#" + frag if frag and "#" not in out else "")
    target = os.path.normpath(os.path.join(case_dir, href.split("#")[0]))
    # a disease record is best read in the query tool, not as raw YAML
    m = re.search(r"entities/([a-z0-9-]+)\.yaml$", target)
    if m:
        return "query.html?q=slug:" + m.group(1)
    for root, url in GITHUB.items():
        marker = os.sep + root + os.sep
        if marker in target + os.sep:
            rel = target.split(marker, 1)[1]
            return url + rel
    return href


def _rewrite(html_text: str, case_dir: str) -> tuple:
    """Return (html, [links that could not be made public])."""
    bad = []

    def sub(m):
        out = _rewrite_link(m.group(1), case_dir)
        if not out.startswith(("http", "query.html", "fallakte.html", "case.html", "#")):
            bad.append(m.group(1))
        return 'href="' + out + '"'

    return _HREF.sub(sub, html_text), bad


def _doc(path: str) -> dict:
    """One markdown file, rendered, with its headings for a contents list."""
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    body, bad = _rewrite(render.render(src), os.path.dirname(os.path.abspath(path)))
    if bad:
        raise DeadLinkError(
            f"{os.path.relpath(path, HERE)}: link(s) that would be dead once "
            f"published: {bad}. Add a rule to SITE_LINKS or GITHUB in check.py.")
    return {"html": body,
            "headings": [{"level": l, "text": t, "anchor": a}
                         for l, t, a in render.headings(src)]}


class DeadLinkError(ValueError):
    pass


def build(all_cases: list, records: dict) -> str:
    """Write `web/fallakte-data.js`, and return a one-line report.

    IT IS A `<script>` TAG AND NOT A `fetch()`, which is Nordstern's own rule for
    `web/`: every page there also has to open over `file://`, so that a case file
    can be mailed to somebody as a folder and still work. The markdown is
    rendered HERE rather than in the browser for the same reason — a renderer
    from a CDN would break both the zero-dependency rule and `file://`.

    WRITING INTO NORDSTERN'S `web/` IS THE PERMITTED DIRECTION, and it is exactly
    what Engpass does with its snapshot. A published artifact in the shared
    output directory is a text file, which is the whole interface. The source
    directory of another register is not.
    """
    out = []
    for c in all_cases:
        rec = records.get(c.get("disease")) or {}
        derived = (rec.get("derived") or {})
        models = []
        for m in (c.get("models") or []):
            if not isinstance(m, dict):
                continue
            ref = _text(m.get("ref"))
            models.append({
                "tool": m.get("tool"),
                "ref": ref,
                "name": os.path.splitext(os.path.basename(ref))[0],
                "access": m.get("access"),
                "live": _text(m.get("live")) or None,
            })
        qs = [q for q in (c.get("questions") or []) if isinstance(q, dict)]
        doc = _doc(os.path.join(c["_dir"], "README.md"))
        out.append({
            "slug": c.get("slug"), "id": c.get("id"),
            "disease": c.get("disease"), "disease_id": c.get("disease_id"),
            "name": rec.get("name") or c.get("disease"),
            "common": rec.get("common"),
            "opened": c.get("opened"), "updated": c.get("updated"),
            "status": c.get("status"), "one_line": _text(c.get("one_line")).strip(),
            "working_with": c.get("working_with") or [],
            "obstacles": c.get("obstacles") or [],
            "models": models,
            "openable": sum(1 for m in models if m["access"] == "live"),
            "questions": [{"id": q.get("id"), "status": q.get("status"),
                           "obstacles": q.get("obstacles") or []} for q in qs],
            "open_questions": sum(1 for q in qs if q.get("status") in ("open", "partial")),
            # read off Nordstern's artifact, never re-rated here
            "record": {"capability": derived.get("capability"),
                       "delivery": derived.get("delivery"),
                       "mechanism": (rec.get("axes") or {}).get("mechanism"),
                       "intervention": (rec.get("axes") or {}).get("intervention"),
                       "blockers": sorted({b.get("kind") for b in (rec.get("blockers") or [])
                                           if isinstance(b, dict) and b.get("kind")}),
                       "reach": derived.get("reach")},
            "doc": doc,
        })

    payload = {
        "register": "fallakte",
        "generated": datetime.date.today().isoformat(),
        "cases": out,
        "about": {"readme": _doc(os.path.join(HERE, "README.md")),
                  "glossary": _doc(os.path.join(HERE, "GLOSSARY.md")),
                  "template": _doc(os.path.join(HERE, "TEMPLATE.md"))},
    }
    target = os.path.join(WEB, "fallakte-data.js")
    with open(target, "w", encoding="utf-8") as fh:
        fh.write("/* GENERATED by Fallakte/check.py --build — do not edit. */\n")
        fh.write("window.FALLAKTE = ")
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write(";\n")
    kb = os.path.getsize(target) // 1024
    return f"wrote web/fallakte-data.js ({kb} kB, {len(out)} case(s))"


def main(argv) -> int:
    records, obstacles = nordstern_records(), engpass_obstacles()
    all_cases = cases()

    if "--build" in argv:
        errs = []
        for c in all_cases:
            errs += check(c, records, obstacles)[0]
        if errs:
            for er in errs:
                print(f"  ERROR  {er}", file=sys.stderr)
            print("refusing to build from a register with errors", file=sys.stderr)
            return 1
        print(build(all_cases, records))
        return 0

    if "--json" in argv:
        out = []
        for c in all_cases:
            c = dict(c)
            for k in ("_path", "_dir"):
                c.pop(k, None)
            out.append(c)
        print(json.dumps({"register": "fallakte",
                          "generated": datetime.date.today().isoformat(),
                          "cases": out}, indent=1))
        return 0

    errors, warnings, skips, seen_ids = [], [], [], {}
    for c in all_cases:
        es, ws, sk = check(c, records, obstacles)
        errors += es
        warnings += ws
        for s in sk:
            if s not in skips:
                skips.append(s)
        cid = c.get("id")
        if cid in seen_ids:
            errors.append(f"id {cid} is used twice: {seen_ids[cid]} and {c.get('slug')}")
        elif cid:
            seen_ids[cid] = c.get("slug")

    print(f"\n## Fallakte — {len(all_cases)} case file(s)\n")
    if all_cases:
        print("| case | id | disease | opened | updated | status | models | questions open |")
        print("|---|---|---|---|---|---|---:|---:|")
        for c in all_cases:
            qs = c.get("questions") or []
            n_open = sum(1 for q in qs if isinstance(q, dict) and q.get("status") in ("open", "partial"))
            print("| {} | {} | {} | {} | {} | {} | {} | {} of {} |".format(
                c.get("slug"), c.get("id"), c.get("disease"), c.get("opened"),
                c.get("updated"), c.get("status"), len(c.get("models") or []),
                n_open, len(qs)))

    # The models table is the useful derived view: which tool covers which case,
    # and which artifacts a stranger can actually open.
    rows = [(c.get("slug"), m) for c in all_cases for m in (c.get("models") or [])
            if isinstance(m, dict)]
    if rows:
        by_tool = {}
        for slug, m in rows:
            by_tool.setdefault(m.get("tool"), []).append(slug)
        print("\n**models by tool** — " + " · ".join(
            f"{t} {len(v)}" for t, v in sorted(by_tool.items())))
        by_access = {}
        for _, m in rows:
            by_access.setdefault(m.get("access"), []).append(m.get("ref"))
        print("\n**reader access** — " + " · ".join(
            f"{k} {len(v)}" for k, v in sorted(by_access.items())))
        reachable = len(by_access.get("live") or [])
        print(f"\n**{reachable} of {len(rows)} referenced artifacts are openable on the "
              f"public site today.**")
        for k in ("repo", "private"):
            for r in sorted(set(by_access.get(k) or [])):
                print(f"  {k:7} {r}")

    for s in skips:
        print(f"\nSKIPPED: {s}")
    for wn in warnings:
        print(f"\nwarning: {wn}")
    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for er in errors:
            print(f"  - {er}")
        return 1
    print("\nok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
