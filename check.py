#!/usr/bin/env python3
"""Nordstern's checker: arithmetic over the register, plus the derived tables.

Run:  python3 check.py            # check + print the derived tables
      python3 check.py --markdown # emit the tables for index.md
      python3 check.py --json     # the whole register + derivations, for querying
      python3 check.py --build    # write web/ artifacts, and today's snapshot
      python3 check.py --diff     # what moved between the two latest snapshots

Two jobs, and the second is why this exists:

1. CHECK. Enum violations, missing units, absent sources, a `mechanism:
   established` with no chain stated in the witness. All arithmetic over a
   declaration — none of it requires knowing what a cell is.

2. DERIVE. Capability, delivery, quadrant and the no-champion list are computed
   from the records and never stored in them. index.md is generated from this,
   so the table cannot drift from the files it summarises.

3. SNAPSHOT. `--build` also freezes today's aggregates into
   web/snapshots/nordstern/. **That is what makes a second pass a comparison
   rather than a fresh opinion** — the same job `moved:` does per record, done
   for the register as a whole. Retrofitting history is impossible, which is why
   this exists before there is anything to compare against.

4. DIFF. `--diff` reads two snapshots and decomposes the change into arrivals,
   departures and **movements**, because only the third is a fact about
   medicine. A register still being written grows faster than medicine does, so
   a net bucket count would be dominated by new records and would read as
   progress. Requires `buckets.members`, stored from 2026-09-02; against an
   earlier snapshot it reports `skipped` rather than guessing.

Zero dependencies, like the rest of the family. PyYAML is used if importable;
otherwise the bounded loader below reads exactly the subset these records use
and raises on anything else rather than silently misreading it.
"""

from __future__ import annotations

import datetime
import glob
import json
import os
import sys

# --------------------------------------------------------------------------
# A bounded YAML-subset loader.
#
# Sperrwerk's yamlish deliberately does not cover multi-line scalars, and every
# `witness` in this register is a `>` block, so it cannot be borrowed. Covered
# here: nested block mappings, block sequences of mappings and of folded plain
# scalars, `>` folded block scalars, inline flow sequences, and scalars
# (int/float/bool/null/plain string). Anything else raises.
# --------------------------------------------------------------------------


class NordsternError(ValueError):
    """A record could not be read or does not satisfy the schema."""


def _scalar(text: str):
    t = text.strip()
    if t in ("null", "~", ""):
        return None
    if t in ("true", "false"):
        return t == "true"
    if t.startswith("[") and t.endswith("]"):
        inner = t[1:-1].strip()
        return [_scalar(p) for p in inner.split(",")] if inner else []
    if t.startswith("{"):
        # INLINE FLOW MAPPINGS ARE NOT SUPPORTED, AND MUST NOT BE GUESSED AT.
        #
        # Falling through returned `"{value: 0.65, units: ..., src: recall}"` —
        # a string, silently, where a dict was expected. The record passed every
        # schema check and then crashed six hundred lines later in a report
        # emitter, with a TypeError naming neither the file nor the field.
        #
        # SCHEMA.md documented this exact syntax for `burden` and `strata`, so
        # the loader and the documentation disagreed and the loader lost
        # quietly. Both are fixed; this raise is what stops it recurring.
        #
        # Same rule as a Sperrwerk check that cannot run: report that it cannot
        # run, never a value that looks like an answer.
        raise NordsternError(
            f"inline flow mapping is not supported: {t[:60]}"
            " — write it as an indented block (value/units/src on their own lines)")
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        pass
    return t.strip("'\"")


def _lines(src: str):
    """(indent, text) for every content line, comments and blanks dropped."""
    out = []
    for n, raw in enumerate(src.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        out.append((len(raw) - len(raw.lstrip()), raw.strip(), n))
    return out


def _parse_block(rows, i, indent):
    """Parse a mapping or sequence at `indent`. Returns (value, next_index)."""
    if rows[i][1].startswith("- "):
        seq = []
        while i < len(rows) and rows[i][0] == indent and rows[i][1].startswith("- "):
            head = rows[i][1][2:].strip()
            # A sequence item that is itself a mapping: "- kind: cost"
            if ":" in head and not head.endswith(":") and _looks_like_key(head):
                item, i = _parse_inline_mapping_item(rows, i, indent, head)
                seq.append(item)
                continue
            # Otherwise a plain scalar, possibly folded over continuation lines.
            parts = [head]
            i += 1
            while i < len(rows) and rows[i][0] > indent and not rows[i][1].startswith("- "):
                parts.append(rows[i][1])
                i += 1
            seq.append(" ".join(parts))
        return seq, i

    mapping = {}
    while i < len(rows) and rows[i][0] == indent:
        indent_, text, lineno = rows[i]
        if ":" not in text:
            raise NordsternError(f"line {lineno}: expected 'key: value', got {text!r}")
        key, _, rest = text.partition(":")
        key, rest = key.strip(), rest.strip()
        if rest in (">", "|", ">-", "|-"):
            i += 1
            parts = []
            while i < len(rows) and rows[i][0] > indent_:
                parts.append(rows[i][1])
                i += 1
            mapping[key] = " ".join(parts)
        elif rest:
            mapping[key] = _scalar(rest)
            i += 1
        else:
            i += 1
            if i < len(rows) and rows[i][0] > indent_:
                mapping[key], i = _parse_block(rows, i, rows[i][0])
            else:
                mapping[key] = None
    return mapping, i


def _looks_like_key(head: str) -> bool:
    key = head.split(":", 1)[0]
    return bool(key) and all(c.isalnum() or c in "_-" for c in key)


def _parse_inline_mapping_item(rows, i, indent, head):
    """A '- key: value' sequence item and the deeper-indented keys under it."""
    inner_indent = rows[i][0] + 2
    synthetic = [(inner_indent, head, rows[i][2])]
    i += 1
    while i < len(rows) and rows[i][0] >= inner_indent:
        synthetic.append(rows[i])
        i += 1
    item, _ = _parse_block(synthetic, 0, inner_indent)
    return item, i


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        rows = _lines(src)
        value, end = _parse_block(rows, 0, 0)
        if end != len(rows):
            raise NordsternError(f"{path}: stopped at line {rows[end][2]}")
        return value
    return yaml.safe_load(src)


# --------------------------------------------------------------------------
# The schema, as closed sets. Kept here rather than in prose so a violation is
# a failure and not a matter of noticing.
# --------------------------------------------------------------------------

AXIS_ENUMS = {
    "mechanism": ["established", "partial", "correlates", "none"],
    "intervention": ["curative", "suppressive", "disease-modifying", "symptomatic", "none"],
    "prevention": ["eradicated", "prophylaxis", "risk-reduction", "none"],
    "ongoing": ["none", "low", "moderate", "high"],
}
KINDS = {"disease", "syndrome", "complaint"}
BLOCKER_KINDS = {
    "knowledge", "candidate-untested", "evidence-incomplete", "no-sponsor",
    "regulatory", "manufacturing", "cost", "logistics", "diagnosis",
    "adherence", "tooling", "policy",
}
ACTORS = {
    "academic", "nonprofit", "philanthropy", "sponsor", "regulator", "payer",
    "government", "legislator", "health-system", "software", "patient-org",
    "manufacturer",
}
STANDINGS = {"documented", "alleged", "disputed", "refuted"}

# --------------------------------------------------------------------------
# PROVENANCE. `src` is either one of three words meaning "not a citation", or a
# mapping that IS one.
#
#     src: recall                      the model's memory
#     src: reasoning                   the model's arithmetic over other numbers
#     src: unknown                     nobody has the number (msmds, noma, hat)
#
#     src:
#       id: 10.1016/S0140-6736(20)30925-9
#       retrieved: 2026-08-26
#       quote: >
#         Global prevalence of osteoarthritis was 595 million cases in 2020.
#
# **A CITATION MUST CARRY WHAT IT READ.** `id` and `retrieved` alone are
# unenforceable — a plausible DOI is exactly what a language model produces when
# it does not know, and it looks like success. Requiring a verbatim `quote`
# makes the claim checkable by a human in ten seconds and makes fabrication a
# deliberate act rather than a slip. Inherited from resolve_mondo.py, which
# prints Mondo's own definition beside every proposal so that review is
# verification rather than trust.
#
# **`src: recall` is honest. A fabricated citation is not.** That asymmetry is
# the whole reason this validation exists before any sourcing tool does.
UNSOURCED = ("recall", "reasoning", "unknown")
CITATION_FIELDS = ("id", "retrieved", "quote")


def src_kind(src) -> str:
    """One of UNSOURCED, or "cited", or "invalid". Never guesses."""
    if isinstance(src, str):
        return src if src in UNSOURCED else "invalid"
    if isinstance(src, dict) and all(str(src.get(f) or "").strip()
                                     for f in CITATION_FIELDS):
        return "cited"
    return "invalid"


def check_src(src, where, out_errors):
    """Validate one `src` in place. Called from wherever a scalar is checked."""
    kind = src_kind(src)
    if kind != "invalid":
        return kind
    if isinstance(src, dict):
        missing = [f for f in CITATION_FIELDS if not str(src.get(f) or "").strip()]
        out_errors.append(
            f"{where}: src is a citation missing {', '.join(missing)} — "
            f"a citation must carry what it read, or it cannot be checked")
    else:
        out_errors.append(
            f"{where}: src={src!r} is not one of {list(UNSOURCED)} and is not a "
            f"citation ({{{', '.join(CITATION_FIELDS)}}})")
    return "invalid"


# WHAT A CITATION COULD EVEN SETTLE. Three tiers, keyed by where the scalar
# lives, because they are three different problems and a verification pass that
# treats them alike will invent citations for the third.
#
#   sourceable  a named public dataset publishes this number. GBD and WHO
#               publish burden against an identifier this register now carries.
#               A citation SETTLES it.
#   supportable a citation supports the number without determining it — a dated
#               historical event, an incidence quoted from one cohort.
#   judged      no citation could settle it, because the quantity is one this
#               register defines. Nothing published anywhere holds "the fraction
#               of patients in whom the best available treatment works".
#
# THIS EXISTS TO FIX A DENOMINATOR THAT WAS ON THE PUBLIC PAGE. "0 of 1,582
# sourced" implies 1,582 could be, and more than half never can. The banner was
# honest about direction and wrong about magnitude.
# --------------------------------------------------------------------------
# SURVIVAL. "You get it, and then what?"
#
# THE FIELD EXISTS BECAUSE `efficacy` IS NOT COMPARABLE ACROSS RECORDS AND
# NOBODY HAD WRITTEN THAT DOWN. `head-neck-cancer` at 0.55 means alive and
# disease-free at five years. `asthma` at 0.85 means good symptom control.
# `hearing-loss` at 0.75 means meaningful benefit from a hearing aid. The
# register's central axis measures a different thing in each record, and
# `reach = efficacy x access` multiplies across them as though they commuted.
#
# `survival` measures one thing everywhere: **the fraction of people alive at a
# stated horizon.** It is the question a patient actually asks, it is the only
# axis here that is comparable between diseases, and it is the one with real
# historical series behind it.
#
# TWO VALUES, AND THE UNTREATED ONE IS THE INTERESTING HALF. `treated` says
# where medicine is; `untreated` says what the disease does when left alone, and
# the gap between them is what medicine has actually bought. **A record whose
# untreated survival is zero and whose treated survival is not describes a
# disease that used to kill everybody and no longer does** — insulin, HAART,
# imatinib, childhood leukaemia — and counting those is the most concrete
# statement of progress this register can make.
#
# THE HORIZON IS DECLARED PER RECORD BECAUSE IT HAS TO BE. Rabies kills within a
# month of symptoms; Huntington's takes twenty years and is equally certain.
# Five-year survival would call one terminal and the other excellent. The horizon
# is part of the claim, not a global constant.
SURVIVAL_BANDS = (
    (0.10, "terminal"),      # nothing meaningful can be done
    (0.50, "a chance"),      # a real but minority chance
    (1.01, "good chance"),
)


def survival_band(rec) -> str:
    """Three bands over `survival.treated`, or `n/a`.

    `n/a` is NOT `terminal`. Thirty-five records in this corpus have no deaths
    at all — hearing loss, cataract, osteoarthritis, low back pain — and a
    mortality ladder is silent about them by construction. Same rule as
    `predictive: n/a`: a question that does not apply is not a question answered
    badly, and the largest disability burdens here are invisible to this axis.
    """
    s = rec.get("survival")
    if not s or not isinstance(s.get("treated"), dict):
        return "n/a"
    v = s["treated"].get("value")
    if not isinstance(v, (int, float)):
        return "n/a"
    for ceiling, name in SURVIVAL_BANDS:
        if v < ceiling:
            return name
    return "good chance"


def was_uniformly_fatal(rec) -> bool:
    """Untreated, essentially nobody survived to the horizon."""
    s = rec.get("survival") or {}
    u = (s.get("untreated") or {}).get("value")
    return isinstance(u, (int, float)) and u < 0.10


def no_longer_terminal(rec) -> bool:
    """THE PROGRESS CLAIM, DERIVED RATHER THAN ASSERTED.

    Uniformly fatal untreated, and not terminal treated. This is the countable
    version of *"X, Y and Z all used to kill everybody, and that list is
    shrinking"* — and because `moved:` entries can be written on a `survival`
    axis, the date each one crossed is recordable too.

    **Read this with `survival_outcome`, never alone.** Its own gap (#216) is
    that a rise from 0.05 to 0.15 in a disease nobody survives counts here
    exactly as insulin does.
    """
    return was_uniformly_fatal(rec) and survival_band(rec) != "terminal"


# --------------------------------------------------------------------------
# THE SECOND QUESTION SURVIVAL CANNOT ANSWER: does the disease end?
#
# gaps.md #216, forced by `als` on the day the axis was added. Two records sit
# in the same band and mean opposite things:
#
#   pancreatic-cancer  0.13 at 5 years — thirteen percent are CURED
#   als                0.20 at 5 years — twenty percent are STILL DYING OF IT
#
# A view built on `survival` alone ranks ALS above pancreatic cancer and is
# exactly wrong about which one anybody survives.
#
# **NO NEW FIELD.** The information was already in the register, one column
# over: the intervention ladder distinguishes `curative` (a finite intervention
# ends it) from `suppressive` (near-normal life, treated indefinitely) from
# everything below. `survival` simply was not reading it. #216 proposed this
# derivation as "cheap and probably right, and worth resisting the urge to add a
# field before trying it" — this is trying it.
#
# THE TWO READINGS ARE INDEPENDENT AND THAT IS THE WHOLE DESIGN.
#   survival_band     HOW MANY reach the horizon      (a measured fraction)
#   survival_outcome  WHAT REACHING IT MEANS          (which rung ends the story)
# Gating the outcome on the band would fold them back together and lose exactly
# the distinction this exists to draw. A curative disease with 2% survival still
# cures 2% of people; that is a scale statement, not a kind statement.
OUTCOMES = {
    "cured":     "some are cured — the disease is gone",
    "recovered": "alive and recovered — the disease passed",
    "held":      "alive and held — treated indefinitely",
    "delayed":   "alive and still dying of it",
}

# `course: acute` — THE FOURTH OUTCOME, AND THE RECORD THAT FORCED IT.
#
# The first version of this derivation read the ladder alone and printed, for
# measles: **"99% at 30 days from rash onset — alive and still dying of it."**
# That is not a rounding error, it is false. Measles is `symptomatic` because
# there is no antiviral, and the survivors are not dying of anything — they
# recovered, because the immune system ended it.
#
# Six records produced the same false sentence: `measles`, `dengue`,
# `influenza`, `cholera`, `h5n1` and `marburg`. All acute, all self-limiting in
# survivors, none of them curable by anything medicine currently has.
#
# THE LADDER DESCRIBES WHAT TREATMENT ACHIEVES, NOT WHAT HAPPENS TO THE PATIENT,
# and for chronic disease those coincide closely enough that the shortcut held.
# For an acute infection they come apart completely. gaps.md #216 noted that
# "nothing in the schema holds duration"; this is that gap arriving with a bill.
#
# It is a declaration rather than a derivation because nothing in the register
# implies it — not the ladder, not `kind`, not the horizon, which is prose. It
# is consulted ONLY for records below `suppressive`: an acute disease that
# antibiotics cure (`typhoid`, `cholera` treated, `malaria`) is `cured`, because
# there the treatment genuinely ended it.
COURSES = ("acute", "chronic")


def survival_outcome(rec) -> str:
    """`cured` / `recovered` / `held` / `delayed`, or `n/a` if not rated.

    Read off `axes.intervention` plus the optional `survival.course`, so it
    costs almost nothing and cannot disagree with the ladder. Requires
    `survival` because the phrase it produces is *"X% at five years, and they
    are ..."* — without a fraction there is no sentence.
    """
    if survival_band(rec) == "n/a":
        return "n/a"
    rung = (rec.get("axes") or {}).get("intervention")
    if rung == "curative":
        return "cured"
    if rung == "suppressive":
        return "held"
    if (rec.get("survival") or {}).get("course") == "acute":
        return "recovered"
    return "delayed"


def survival_gain(rec):
    """`treated - untreated` — what medicine has actually bought, or None.

    THE MOST DIRECT STATEMENT OF PROGRESS IN THE REGISTER, and the only one
    computed by subtracting two measured numbers rather than by judging an axis.
    It is also the column that produces the register's least comfortable rows:
    `alzheimers` is **+0.00** and `copd` is +0.05.

    It is a difference of two fractions and not a ratio, deliberately. Lung
    cancer's 0.02 -> 0.25 is a twelve-fold *relative* improvement and a +0.23
    absolute one; the relative figure is the one that gets published and the
    absolute figure is the one a patient experiences.
    """
    s = rec.get("survival")
    if not s:
        return None
    u = (s.get("untreated") or {}).get("value")
    t = (s.get("treated") or {}).get("value")
    if not isinstance(u, (int, float)) or not isinstance(t, (int, float)):
        return None
    return round(t - u, 6)


def survival_sentence(rec) -> str:
    """The record as the sentence a patient would ask for: *you get X, then Y*.

    THE QUALIFIER IS NOT DECORATION. "20% survive five years" and "20% survive
    five years, and they are still dying of it" are different claims, and the
    register is only entitled to publish the second. #216 logged the first as
    unsafe to display on its own; this is the display that is safe.
    """
    if survival_band(rec) == "n/a":
        return ""
    s = rec["survival"]
    pct = round(s["treated"]["value"] * 100)
    # THE DEGENERATE CASE, WHICH THE FIRST VERSION GOT WRONG. It printed
    # "0% at 20 years — alive and still dying of it" for rabies and
    # Huntington's. Nobody is alive; there is no cohort for the qualifier to
    # describe. `delayed` is still the right *kind* — the disease does not end
    # except by killing you — but the sentence has to say so.
    if pct == 0:
        return f"nobody survives {s['horizon']}"
    tail = OUTCOMES[survival_outcome(rec)].split("—")[-1].strip()
    # NEVER PRINT 100% FOR A FRACTION BELOW 1. `asthma` is 0.997 and `cholera`
    # 0.995, and both round up — but "100% survive" is a different claim from
    # "99.7% survive", and the missing 0.3% of asthmatics is 455,000 people a
    # year. These are precisely the records where the axis compresses worst
    # (gaps.md #221), so they are the last place to let rounding speak.
    shown = ">99" if pct == 100 and s["treated"]["value"] < 1 else str(pct)
    return f"{shown}% at {s['horizon']} — {tail}"


def survival_course(rec):
    """`acute` / `chronic` / None. Declared, never inferred — see COURSES."""
    return (rec.get("survival") or {}).get("course")


SOURCEABLE = {
    # Registries, cohorts and national audits publish these. Unlike `efficacy`,
    # which is a judgement, survival is a number somebody measured.
    "survival.treated", "survival.untreated",
    "burden.deaths", "burden.prevalence", "burden.incidence", "burden.ylds",
    "burden.dalys", "burden.cases", "burden.births", "burden.disability",
    "burden.deaths_attributable", "burden.deaths_associated",
}
SUPPORTABLE = {
    "moved[]",                 # a dated event with a canonical reference
    "toll.incidence", "residue.incidence",
    "strata[].fraction",
}


def scalar_tier(path: str) -> str:
    if path in SOURCEABLE:
        return "sourceable"
    if path in SUPPORTABLE:
        return "supportable"
    return "judged"
SEVERITIES = ["none", "minor", "major", "catastrophic"]

# Measurement is three questions, not one. `diagnostic` keeps its own vocabulary
# because the KIND of evidence is more informative there than a quality grade;
# the other two are graded, and carry `n/a` for "there is no question to ask".
MEASUREMENT_ENUMS = {
    "diagnostic": ["objective", "clinical", "complaint"],
    "prognostic": ["good", "partial", "none"],
    "predictive": ["good", "partial", "none", "n/a"],
}
TERMS = {"none": "clean", "minor": "clean", "major": "costly", "catastrophic": "harsh"}

CAPABILITY = {
    "curative": "curable", "suppressive": "managed",
    "disease-modifying": "partial", "symptomatic": "unsolved", "none": "unsolved",
}
DELIVERY_BANDS = [(0.8, "delivered"), (0.6, "mostly"), (0.3, "partly"), (0.05, "barely")]


ID_PATTERN = "FND-D-"


def status(rec) -> str:
    """`active` or `deprecated`, DERIVED from the presence of a `deprecated:`
    block rather than stored beside it.

    Storing both invites them to disagree, which is the same rule that makes
    `capability` derived rather than written down. A record is deprecated
    because somebody wrote down why and when; there is no second place to say so.
    """
    return "deprecated" if rec.get("deprecated") else "active"


def superseded_by(rec) -> str | None:
    """The 302. `None` means the record is simply no longer needed — a 410.

    THE REGISTER IS APPEND-ONLY. Records are never deleted and `id` is never
    reused, because the point of a public dataset is that a citation keeps
    resolving. A record that turns out to be the wrong frame, or whose MONDO
    term is merged away, is deprecated and left in place, pointing at whatever
    replaced it. Deprecated records stay in the JSON and the CSV so they can be
    read; they are excluded from the derived tables and hidden from search by
    default.
    """
    return (rec.get("deprecated") or {}).get("see")


def active(records) -> list:
    return [r for r in records if status(r) == "active"]


def is_eradicated(rec) -> bool:
    """The top rung of the prevention axis, and after 48 records it has exactly
    one occupant.

    THIS EXISTS BECAUSE THE SPECIAL CASE WAS HANDLED IN ONE PLACE AND NEEDED
    THREE. `capability()` returned `curable` for an eradicated disease and
    `quadrant()` read `intervention` directly, so smallpox came out
    **`capability: curable` and `quadrant: engineering problem` simultaneously**
    — two derivations contradicting each other about the only disease humanity
    has ever eliminated. `orphaned` fired on it as well: *science done, nobody
    carrying it*, about a disease that does not exist.

    None of that is gaps.md #66 (capability ignores the prevention axis), which
    is a real design question still open. This is just the one special case that
    was already decided, applied consistently.
    """
    return rec["axes"]["prevention"] == "eradicated"


PREVENTS = ("prophylaxis", "eradicated")


def capability(rec) -> str:
    """Can anything be done about this — by TREATMENT or by PREVENTION.

    IT USED TO READ ONLY `intervention`, WHICH WAS gaps.md #66 AND AN INTERNAL
    CONTRADICTION: `has_capability()` below has always counted prevention at
    `prophylaxis` and above, so the two functions disagreed about the same
    record.

    Measles ended the argument. A two-dose vaccine, ~97% effective, in use since
    1963, off patent, which eliminated the disease from the entire American
    continent and took deaths from ~2.6 million a year to ~100,000 — and because
    there is no antiviral and never has been, `intervention: symptomatic`, so the
    register said **`unsolved`**. Dengue and rabies said it before, and rabies is
    the sharpest: essentially 100% fatal once symptomatic, and essentially 100%
    preventable by post-exposure prophylaxis.

    `preventable` is a new value rather than a promotion to an existing one,
    because none of the others is true. Nobody is cured of measles. Nobody is
    managed. **"Don't get it, because if you do we can't help you much" is a
    distinct answer** and it is the honest one for four records.

    SCHEMA.md has always said prevention is independent of intervention rather
    than a continuation of it — PKU is the proof. This makes the derivation agree
    with the schema it derives from.
    """
    if is_eradicated(rec):
        return "curable"
    treat = CAPABILITY[rec["axes"]["intervention"]]
    if treat == "unsolved" and rec["axes"]["prevention"] in PREVENTS:
        return "preventable"
    return treat


def reach(rec) -> float:
    ax = rec["axes"]
    return ax["efficacy"]["value"] * ax["access"]["value"]


def delivery(rec) -> str:
    if capability(rec) in ("unsolved", "preventable"):
        # `reach` is efficacy x access and BOTH describe the treatment. For a
        # record whose capability is prevention, that number describes the wrong
        # thing, so no band is reported rather than a misleading one. Prevention
        # has no efficacy or access scalars at all — see gaps.md #109.
        return "—"
    r = reach(rec)
    for floor, label in DELIVERY_BANDS:
        if r >= floor:
            return label
    return "undelivered"


# --------------------------------------------------------------------------
# BUCKETS — the register read as a small set of named states. See buckets.yaml
# for the definitions and for why the two axes are different kinds of thing.
# --------------------------------------------------------------------------

# Axis A. ORDER IS LOAD-BEARING: first match wins, and without a stated order
# `type-1-diabetes` is both `held-off` and `defines-your-life` and the partition
# is not one. Ending your life outranks changing it; being held off indefinitely
# outranks the residue that the holding costs.
BUCKETS_A = ("ends-it", "ends-it-unless-caught", "ends-it-later", "held-off",
             "defines-your-life", "changes-you", "back-to-normal")
BUCKETS_B = ("nobody-makes-it", "found-too-late", "cannot-aim-it",
             "no-starting-point", "cannot-reach-people", "needs-more-evidence")


def bucket(rec) -> str:
    """Which of the seven states of axis A this record is in — always exactly one.

    **THE SPINE IS WHAT HAPPENS TO YOUR LIFE, NOT WHETHER YOU DIE.** A mortality
    ladder is silent about hearing loss, cataract, osteoarthritis and low back
    pain, and about `me-cfs`, `heds` and `msmds` — 37 records that `survival`
    cannot rate at all. Death is the most severe answer on this axis rather than
    the axis itself, which is why there is no residual "unrated" bucket: every
    record lands, and a test asserts it.
    """
    ax = rec["axes"]
    out = survival_outcome(rec)
    treated = ((rec.get("survival") or {}).get("treated") or {}).get("value")

    # MOST PEOPLE WITH THIS DISEASE DIE OF IT — READ BEFORE THE LADDER.
    # buckets.yaml v4, and it corrected the worst output this axis had produced.
    #
    # `survival_outcome()` reads `axes.intervention`, so ANY record on the
    # `curative` rung returned `cured` however few survived — and `cured` never
    # reached the branch below. **`pancreatic-cancer` was therefore filed in
    # `changes-you`, "you survive, and it changes you", on 13% five-year
    # survival**, alongside cataract. So were lung, gastric and liver cancer.
    # The rung was right about what the treatment does when it works; the bucket
    # was answering a different question and taking the rung's word for it.
    #
    # The line is drawn where it can be said in a sentence — **more than half
    # die** — which also leaves `vaginal-cancer` and `h5n1` at exactly 0.50
    # outside it, where a coin flip belongs.
    #
    # ACUTE ILLNESS IS EXCLUDED, AND NOT TO PROTECT A RECORD. `marburg` kills
    # three quarters of the people it infects in about two weeks; the quarter who
    # live *recover*. "It ends your life, but later" is false for both of them.
    # That is the ⧉ `spans_ladder` shape the register already names — **a
    # malformed question, not a hard one** — and the honest move is to decline to
    # average it rather than to file it wrongly with a straight face. Logged as a
    # hole in buckets.yaml: acute high-lethality infection has no bucket that
    # fits, and it has two records.
    mostly_fatal = (out != "recovered" and isinstance(treated, (int, float))
                    and treated < 0.5)
    if out == "delayed" or mostly_fatal:
        if (treated or 0) < 0.05:
            return "ends-it-unless-caught" if rec.get("window") else "ends-it"
        return "ends-it-later"
    # `held` covers the rated ones; the rung covers those `survival` cannot rate.
    if out == "held" or ax["intervention"] == "suppressive":
        return "held-off"
    if ax["ongoing"] == "high" or residue_terms(rec) == "harsh" or terms(rec) == "harsh":
        return "defines-your-life"
    # SEVERITY, NOT PRESENCE — buckets.yaml v3, and it fixed a contradiction
    # between two of this file's own derivations. The v1/v2 rule tested
    # `rec.get("residue")`, so ANY residue block sent a record to `changes-you`;
    # `restored()` has always tested residue SEVERITY, treating none/minor as
    # clean. Eight records therefore derived `restored: restored` — *back to the
    # state before it all* — and `bucket: changes-you` simultaneously. `clubfoot`
    # made it obvious: its residue is a shoe size and a slightly thinner calf in
    # somebody who runs normally, which is not a life changed.
    #
    # `harsh` is already taken by `defines-your-life` above, so `costly` is what
    # remains here. Note this also removes the `restored()` call: severity is now
    # read directly, so the two derivations cannot drift apart again.
    if (residue_terms(rec) == "costly" or terms(rec) == "costly"
            or ax["ongoing"] == "moderate"):
        return "changes-you"
    return "back-to-normal"


def bucket_tags(rec) -> list:
    """Axis B — why it is not better than that. Several, or none.

    **NEVER SUM THESE.** They are tags on a record, not a partition of the
    register; a chart that totals them is counting some diseases repeatedly and
    presenting the result as a share.
    """
    kinds = {b["kind"] for b in rec["blockers"]}
    out = []
    # THE `capability` GUARD IS THE WHOLE DEFINITION. `no-sponsor` on a record
    # where nothing works is nobody funding the *research*; on a record with a
    # real capability it is nobody producing the *cure*. Only the second is a
    # thing a factory or a buyer could fix, and conflating them would put
    # `me-cfs` in a bucket about manufacturing.
    if "manufacturing" in kinds or (
            "no-sponsor" in kinds and capability(rec) != "unsolved"):
        out.append("nobody-makes-it")
    # THE FOREST FIRE. Caught early it is curable, caught late it is not — and
    # a window alone does not say that, because 86 records have one. Three
    # conditions: the late stratum is hopeless, the early one is mostly cured,
    # and MORE THAN HALF ARE MISSED. The third is what makes this a finding
    # rather than a description; it is the size of the screening prize.
    effs = [s["efficacy"]["value"] for s in (rec.get("strata") or [])
            if isinstance((s.get("efficacy") or {}).get("value"), (int, float))]
    caught = ((rec.get("window") or {}).get("caught_in_time") or {}).get("value")
    if (len(effs) >= 2 and min(effs) <= 0.2 and max(effs) >= 0.7
            and isinstance(caught, (int, float)) and caught < 0.5):
        out.append("found-too-late")
    if futile_treatment_risk(rec):
        out.append("cannot-aim-it")
    if rec["axes"]["mechanism"] in ("none", "correlates"):
        out.append("no-starting-point")
    # THE NAME SAYS "IT WORKS", SO THE RULE HAS TO ASK. `delivery` alone put
    # Alzheimer's here — a `disease-modifying` record whose own efficacy field
    # says the number is the wrong shape and whose survival gain is zero. A
    # treatment that does not hold or end the disease has nothing to arrive.
    # Same call Engpass's stages report makes: `partial` does not open the
    # "can we do anything about it" gate, so reach is not asked of it.
    if (delivery(rec) in ("barely", "undelivered")
            and capability(rec) in ("curable", "managed", "preventable")):
        out.append("cannot-reach-people")
    if kinds & {"evidence-incomplete", "candidate-untested"}:
        out.append("needs-more-evidence")
    return out


def bucket_version() -> int:
    """buckets.yaml's `version`, read from beside this file.

    Read rather than hardcoded so the definitions and the number that stamps
    them cannot drift — the definitions are the artefact a future comparison
    needs, and a version that lived in the code would be edited separately from
    the rules it versions.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "buckets.yaml")
    return int(load(path)["version"])


def bucket_names() -> dict:
    """slug -> display name, straight from buckets.yaml. One copy, not two."""
    return _bucket_field("name")


def bucket_defs() -> dict:
    """slug -> {rule, not}, straight from buckets.yaml.

    THE PAGE MUST NOT CARRY ITS OWN COPY OF A DEFINITION. `web/banner.js` exists
    because three hand-written provenance paragraphs drifted and one of them was
    a year out of date. A bucket's rule is exactly that shape of text — written
    once, read on a public page, and never re-checked — so it travels in the
    snapshot with the counts it produced, and a section renders whatever the
    version it is displaying actually said.
    """
    return {slug: {"rule": (b.get("rule") or "").strip(),
                   "not": (b.get("not") or "").strip(),
                   # THE EXEMPLARS, WHICH ARE A CHOICE AND ARE MEANT TO BE.
                   # A section lists its members alphabetically, which is the
                   # only neutral order — and a neutral order buries things: the
                   # register's single largest unmet need is called *Uncorrected
                   # refractive error* and lands 66th of 68 under U. `examples`
                   # is where buckets.yaml has always said which records make the
                   # case, and it is now rendered rather than only read by
                   # whoever opens the file.
                   "examples": list(b.get("examples") or [])}
            for slug, b in _bucket_raw().items()}


def _bucket_raw() -> dict:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "buckets.yaml")
    return {b["slug"]: b for axis in load(path)["axes"] for b in axis["buckets"]}


def _bucket_field(field) -> dict:
    return {slug: b[field] for slug, b in _bucket_raw().items()}


def bucket_digest() -> str:
    """A fingerprint of the bucket RULES, so a silent redefinition cannot hide.

    A record moving between buckets is progress and is what `moved:` records. A
    bucket's *definition* moving is a corruption of the time series — next year's
    count answers a different question while looking like the same one. The
    digest goes into every snapshot beside `buckets.yaml`'s `version`, and
    `TestBuckets` fails if the digest moved and the version did not.
    """
    import hashlib
    import inspect
    src = inspect.getsource(bucket) + inspect.getsource(bucket_tags)
    return hashlib.sha256(src.encode()).hexdigest()[:12]


def _burden_inputs(rec, key):
    """`(burden, efficacy, access)` for `burden.<key>`, or None.

    Shared by the deaths-based and YLD-based gaps so the two can never drift
    apart. `key` is `deaths` or `ylds` and **the results must never be mixed or
    summed**: one is people who died, the other is years lived with disability,
    and adding them produces a number about nothing.
    """
    if capability(rec) == "preventable":
        return None
    scalar = (rec.get("burden") or {}).get(key) or {}
    v = scalar.get("value")
    if not isinstance(v, (int, float)):
        return None
    return v, rec["axes"]["efficacy"]["value"], rec["axes"]["access"]["value"]


def knowledge_yld(rec):
    """Years lived with disability a year that remain **with perfect delivery**.

    `ylds x (1 - efficacy)`. The exact analogue of `knowledge_gap`, computed on
    the burden metric that does not require anybody to have died.

    **THIS IS THE FIELD THE REGISTER HAS BEEN MISSING WITHOUT KNOWING IT.**
    `burden.ylds` has existed in the schema since early on, carried by four
    records, referenced once in a path list, and used by nothing. Meanwhile four
    consecutive records — `glaucoma`, `retinopathy-of-prematurity`,
    `refractive-error`, `migraine` — were written with an explicit comment
    explaining that the mortality axes could not see them. Around two billion
    people between them and no attributed deaths at all.

    **NEVER ADD THIS TO `knowledge_gap`.** Deaths and YLDs are different units.
    A record may carry both, one or neither, and the two rankings are separate
    readings of the register in exactly the sense the standfirst describes.
    """
    got = _burden_inputs(rec, "ylds")
    return None if got is None else round(got[0] * (1 - got[1]), 3)


def delivery_yld(rec):
    """Years lived with disability a year claimable **by what already exists**.

    `ylds x efficacy x (1 - access)`. Same caveats as `delivery_gap`, and the
    same prohibition on mixing units.
    """
    got = _burden_inputs(rec, "ylds")
    return None if got is None else round(got[0] * got[1] * (1 - got[2]), 3)


def _gap_inputs(rec):
    """`(deaths, efficacy, access)` if this record can carry a gap, else None.

    THE GUARD IS THE WHOLE DESIGN. Two independent reasons a gap cannot be
    computed, and both must return nothing rather than a plausible zero:

    - **No `burden.deaths`.** 43 of 129 records have none, and four of the five
      diseases where medicine is most completely helpless — `huntington`,
      `me-cfs`, `msmds`, `heds` — are among them. A gap of `None` keeps them out
      of the ranking; a gap of `0` would rank them last, which is the opposite
      of true. Same rule as a Sperrwerk check reporting `skipped`, never `ok`.
    - **`capability` is `preventable`.** `efficacy` and `access` describe only
      the *treatment*, and for these five the capability is prevention — so the
      arithmetic would read rabies as a 59,000-death knowledge gap when the
      vaccine is ~100% effective and the deaths are access. That is gaps.md #109
      appearing as arithmetic, and it is why `delivery()` above returns "—" for
      the same set.
    """
    return _burden_inputs(rec, "deaths")


def knowledge_gap(rec):
    """Deaths a year that remain **with delivery already perfect** — or None.

    `deaths x (1 - efficacy)`. The half of the burden that no amount of money,
    logistics or policy can claim, because the thing that would be delivered
    does not work well enough or does not exist.

    **THIS IS THE NUMBER THAT ANSWERS "SHOULD WE WORK ON THE RARE HORRIFIC ONES
    OR THE COMMON ONES".** It answers *neither*, and that is the finding: the
    largest knowledge gaps in the register are inside the common diseases.
    `stroke` alone is ~3.3M, against ~91,000 attributed deaths across all eight
    records where `efficacy` is zero. A disease can be both extremely common and
    largely beyond current medicine, and a graph of capability without burden
    hides exactly that.

    **IT IS A PROXY AND MUST BE READ AS ONE.** `efficacy` is *the fraction of
    patients whose course is altered*, not a mortality reduction, so multiplying
    it by deaths is a shape rather than a body count. `stroke`'s own efficacy
    field says **"A CONSTRUCT, not a measurement"**. And every input is in the
    915 `judged` scalars, of which **0 are sourced** — see the provenance banner.
    Do not publish these as figures.
    """
    got = _gap_inputs(rec)
    return None if got is None else round(got[0] * (1 - got[1]), 3)


def delivery_gap(rec):
    """Deaths a year preventable **by what already exists** — or None.

    `deaths x efficacy x (1 - access)`. The burden that would fall away if the
    treatment already on the shelf reached everyone it works for.

    Read beside `knowledge_gap`, this is the register's headline asymmetry
    restated in lives rather than in blocker counts: **knowledge cannot be
    triaged with money and delivery can.** The same caveats apply in full — a
    proxy over unsourced judgement, not a figure to quote.
    """
    got = _gap_inputs(rec)
    return None if got is None else round(got[0] * got[1] * (1 - got[2]), 3)


def overtreatment_risk(rec) -> bool:
    """Real capability, a permanent price, and no way to say who needs it.

    The register's sharpest argument for funding measurement over therapeutics:
    these are entities where people are harmed because nobody can tell in
    advance which of them was going to be harmed by the disease.
    """
    return (has_capability(rec) and terms(rec) in ("costly", "harsh")
            and rec["measurement"]["prognostic"] == "none")


def futile_treatment_risk(rec) -> bool:
    """Real capability, a permanent price, and no way to say who will respond.

    Jeremy's sentence, made checkable: "chemo doesn't work on certain
    variations, but we prescribe it because that is all we got."
    """
    return (has_capability(rec) and terms(rec) in ("costly", "harsh")
            and rec["measurement"]["predictive"] == "none")


def residue_terms(rec) -> str:
    """What the disease leaves behind, one word. Same map as `terms`, because
    permanent damage is permanent damage whichever side it came from."""
    return TERMS[(rec.get("residue") or {}).get("severity", "none")]


def restored(rec) -> str:
    """ARE THEY BACK TO THE STATE THEY WERE IN BEFORE ANY OF THIS?

    Jeremy's question, and it is the one a patient actually asks. It has been
    unanswerable here until now because the register recorded only half of it:
    `toll` is what the CURE takes, and there was no field for what the DISEASE
    leaves in someone the cure worked on.

    Both are permanent, both stop a person returning to baseline, and the
    difference between them is causal rather than experiential — which is why
    this reads both and names which one is in the way.

      restored         nothing permanent from either side
      cure-costs       the treatment took something (parotid surgery, the nerve)
      disease-residue  the treatment worked and the damage was already done
                       (tuberculosis: the bacterium is gone, the lungs are scarred)
      both             the cure took something AND the disease left something
      n/a              nothing to be restored from — no capability, so nobody
                       reaches the end of successful treatment in the first place

    `n/a` is not `restored`, and the distinction is the usual one: a question
    that cannot be asked is not a question answered well.
    """
    if not has_capability(rec):
        return "n/a"
    took = terms(rec) != "clean"
    left = residue_terms(rec) != "clean"
    return {(False, False): "restored", (True, False): "cure-costs",
            (False, True): "disease-residue", (True, True): "both"}[(took, left)]


def terms(rec) -> str:
    """What the cure costs, one word. `capability` alone hid the question a
    patient actually asks: not "can this be fixed" but "what will it take"."""
    return TERMS[(rec.get("toll") or {}).get("severity", "none")]


def cured_at_a_price(rec) -> bool:
    """Something demonstrated helps, and it takes something permanent."""
    return has_capability(rec) and terms(rec) in ("costly", "harsh")


def window_toll_link(rec) -> bool:
    """A window AND a permanent price: the price is largely what missing the
    window cost, so `diagnosis` is the cheap lever. The register's most
    actionable shape — no new therapy required, only earlier arrival.

    READS BOTH COSTS. Written before `residue` existed, when the only permanent
    price the schema knew was the one the treatment charged. Schistosomiasis is
    the record that forced the fix: praziquantel is a cheap, safe tablet, so the
    toll is `clean` — and treating a child before the eggs have scarred the
    bladder or the liver is the whole game. The window's price there is
    entirely `residue`, and the old rule would have reported no link on the
    most window-dependent record in the register.
    """
    permanent = terms(rec) in ("costly", "harsh") or \
        residue_terms(rec) in ("costly", "harsh")
    return bool(rec.get("window")) and permanent


def spans_ladder(rec) -> bool:
    """Do the strata disagree about capability?

    When they do, "is this solved" is a MALFORMED question rather than a hard
    one, and the register should say so instead of picking a side. Breast
    cancer: stage I is cured, stage IV is not, and both are breast cancer.
    """
    # NOTE: a copy of the measurement-validation block from `check()` was pasted
    # into this function at some point and sat here as dead code, referring to
    # `errors` and `here`, neither of which exists in this scope. It could only
    # ever raise NameError, and it never ran, because reaching an `append` needs
    # `predictive: n/a` together with efficacy below 0.85 — and `hepatitis-c`,
    # the register's only other `n/a`, sits at 0.95. `cryptococcal-meningitis`
    # was the first record to reach it, on the day it was written.
    # A DERIVATION MUST NOT VALIDATE. `check()` owns errors; this returns a bool.
    strata = rec.get("strata") or []
    return len({CAPABILITY[s["intervention"]] for s in strata}) > 1


def capability_tier(rec) -> str:
    """Where the intervention sits on the ladder, in three bands.

    THE LADDER HAS FIVE RUNGS AND THIS USED TO FLATTEN IT TO A BOOLEAN —
    `fixable = intervention in ("suppressive", "curative")` — which put
    `disease-modifying` in the same bucket as `none`.

    That is how ischaemic heart disease and stroke, the first and third largest
    causes of death on Earth, came to be filed as "understood, and nothing can
    be done": 15.6 million deaths a year, against a coronary death rate that has
    more than halved since about 1980 and thrombectomy effect sizes among the
    largest in medicine. gaps.md #89.

    COPD CHOSE THE REPAIR, which is why it was added before this was fixed.
    It is `symptomatic` — nothing alters the decline in lung function — so it
    belongs in the bottom band and the harsh verdict is deserved. Moving
    `disease-modifying` up a rung would have dragged nothing useful up with it
    and would have left `symptomatic` and `none` conflated. Deleting the grid
    would have lost a true statement about COPD. **A third band separates all
    three records correctly**, and forty-three records had not supplied a case
    where the harsh verdict was earned.
    """
    if is_eradicated(rec):
        # Smallpox rates `intervention: symptomatic` and correctly so — nothing
        # has ever been shown to alter the course of the disease in a human.
        # Filing it under "understood, and nothing can be done" on the strength
        # of that would be the #89 error again, in its purest form.
        return "treatable"
    iv = rec["axes"]["intervention"]
    if iv in ("none", "symptomatic") and rec["axes"]["prevention"] in PREVENTS:
        # PREVENTION RESCUES ONLY WHAT WOULD OTHERWISE READ "NOTHING CAN BE
        # DONE". Leaving measles in `engineering problem` was #89's error
        # arriving from the prevention side: a two-dose vaccine that eliminated
        # the disease from a continent, filed as untreatable.
        #
        # It deliberately does NOT promote past `modifiable`. Rheumatic heart
        # disease has both — penicillin prophylaxis and disease-modifying
        # treatment — and an unconditional override hid the treatment behind the
        # prophylaxis. Where the map already says something works, there is
        # nothing to rescue.
        return "treatable"
    if iv in ("suppressive", "curative"):
        return "treatable"       # the course is held or ended
    if iv == "disease-modifying":
        return "modifiable"      # the course is slowed, and not arrested
    return "neither"             # the course is unchanged


# Six cells, and the field is still called `quadrant`.
#
# The name is now literally wrong and is kept anyway: `quadrant:frontier` is a
# canned question on the public page, `quadrant:"known & treatable"` is the
# documented example of quoting in the query language, and the term is the
# register's API. Accuracy in a field name is worth less than not breaking a
# query somebody bookmarked. The user-facing labels — which are the part that
# can state a verdict about a disease — say "map" and "cell" instead.
QUADRANTS = {
    # NOT "solved". The cell means the mechanism is known and a treatment
    # exists — it says nothing about reach, toll, or cure. Labelling it "solved"
    # put the word next to breast cancer's 670,000 annual deaths and Crohn's
    # bowel resections, where it reads as a verdict on the disease rather than a
    # description of a cell. A name that overclaims on a public page is a
    # defect, not a wording preference. Same rule applied to the new cells.
    (True,  "treatable"):  "known & treatable",
    (True,  "modifiable"): "known & modifiable",
    (True,  "neither"):    "engineering problem",
    (False, "treatable"):  "empirical luck",
    # Unoccupied at 44 records, and named anyway because the derivation must be
    # total. Something that slows a disease nobody understands — weaker than
    # lithium in bipolar disorder, which is the `empirical luck` case. If this
    # cell is still empty at a hundred records that is worth reporting, not
    # worth deleting.
    (False, "modifiable"): "empirical foothold",
    (False, "neither"):    "frontier",
}


def quadrant(rec) -> str:
    known = rec["axes"]["mechanism"] in ("established", "partial")
    return QUADRANTS[(known, capability_tier(rec))]


ORPHAN_REACH_CEILING = 0.6


def has_capability(rec) -> bool:
    """Is there anything demonstrated that helps — by treatment OR prevention?

    Prevention counts. Rheumatic heart disease's valves cannot be repaired, and
    a monthly penicillin injection prevents the damage; excluding it because
    `intervention` is only `disease-modifying` would drop the register's
    clearest manufacturing failure.
    """
    return (capability(rec) in ("curable", "managed", "partial", "preventable")
            or rec["axes"]["prevention"] in PREVENTS)


def orphaned(rec) -> bool:
    """Science done, nobody carrying it — the register's actionable output.

    Two corrections came out of running this rule against the records, and both
    are worth stating because the first version looked reasonable and was wrong:

    1. The presence of a `knowledge` blocker must NOT disqualify. Sickle cell has
       one (in vivo editing, to remove the transplant requirement) alongside a
       documented logistics failure for off-patent hydroxyurea. Wanting a better
       cure does not stop the existing treatment from being undelivered.
    2. A reach ceiling is required, or HIV qualifies — it has documented
       logistics and policy blockers and is nonetheless one of the best-funded
       delivery efforts in history. "No champion" has to mean under-delivered,
       not merely imperfect.

    The ceiling is a tunable, not a truth. PKU sits just outside it at 0.665 and
    has a strong documented screening blocker; a stricter reading would include
    it.
    """
    if not has_capability(rec):
        return False
    if is_eradicated(rec):
        # "Science done, nobody carrying it" cannot be said about a disease
        # nobody has. Smallpox's blockers are about keeping it gone — the only
        # record in the register where that is what a blocker means.
        return False
    if reach(rec) >= ORPHAN_REACH_CEILING:
        return False
    return any(b["standing"] == "documented" and b["kind"] != "knowledge"
               for b in rec.get("blockers") or [])


# --------------------------------------------------------------------------
# Checks. Each returns a list of witness strings — never a bare boolean.
# --------------------------------------------------------------------------


def check(rec, path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    here = os.path.basename(path)

    if rec.get("kind") not in KINDS:
        errors.append(f"{here}: kind={rec.get('kind')!r} is not one of {sorted(KINDS)}")

    ax = rec.get("axes") or {}
    for key, allowed in AXIS_ENUMS.items():
        if ax.get(key) not in allowed:
            errors.append(f"{here}: axes.{key}={ax.get(key)!r} not in {allowed}")

    for key in ("efficacy", "access"):
        scalar = ax.get(key)
        if not isinstance(scalar, dict):
            errors.append(f"{here}: axes.{key} must be a {{value, units, src}} record")
            continue
        for field in ("value", "units", "src"):
            if scalar.get(field) in (None, ""):
                errors.append(f"{here}: axes.{key} is missing {field}")
        if isinstance(scalar.get("value"), (int, float)) and not 0 <= scalar["value"] <= 1:
            errors.append(f"{here}: axes.{key}.value={scalar['value']} is not a fraction")
        if src_kind(scalar.get("src")) == "recall":
            warnings.append(f"{here}: axes.{key} is src=recall — unverified, do not publish")

    # SURVIVAL, if present. Optional while the rating pass runs; once a record
    # carries it, it must be complete — a half-populated survival block would
    # derive a band from nothing.
    sv = rec.get("survival")
    if sv is not None:
        if not sv.get("horizon"):
            errors.append(f"{here}: survival has no horizon — five-year survival "
                          f"and twenty-year survival are different claims")
        # `course` is optional and defaults to chronic. A MISSPELLING MUST NOT
        # SILENTLY DEFAULT: writing `course: accute` would put the record back
        # to "alive and still dying of it", which is the exact false sentence
        # this field was added to stop.
        if sv.get("course") is not None and sv["course"] not in COURSES:
            errors.append(f"{here}: survival.course={sv['course']!r} — "
                          f"expected one of {' · '.join(COURSES)}")
        for key in ("untreated", "treated"):
            sc = sv.get(key)
            if not isinstance(sc, dict):
                errors.append(f"{here}: survival.{key} must be a {{value, units, src}} record")
                continue
            for field in ("value", "units", "src"):
                if sc.get(field) in (None, ""):
                    errors.append(f"{here}: survival.{key} is missing {field}")
            v = sc.get("value")
            if isinstance(v, (int, float)) and not 0 <= v <= 1:
                errors.append(f"{here}: survival.{key}.value={v} is not a fraction")
        u = (sv.get("untreated") or {}).get("value")
        t = (sv.get("treated") or {}).get("value")
        if isinstance(u, (int, float)) and isinstance(t, (int, float)) and t < u:
            # Not an error: a treatment CAN make survival worse, and a record
            # that says so is making a real claim. But it must be argued.
            if not sv.get("witness"):
                errors.append(f"{here}: survival.treated ({t}) is below untreated "
                              f"({u}) with no witness — that is a claim, not a typo")

    # A `moved:` ENTRY MUST STATE ITS BASIS. 47 of 147 were written without a
    # `src` at all, because nothing required one — and `moved:` is the register's
    # only time series, so a dated claim with no stated basis is the worst place
    # in the schema to leave a hole. Warned rather than errored while the
    # sourcing pass fills them in; see source_moved.py.
    for i, m in enumerate(rec.get("moved") or []):
        if "src" not in m:
            warnings.append(f"{here}: moved[{i}] ({m.get('date')}, "
                            f"{m.get('axis')}) has no src — a dated claim with "
                            f"no stated basis")

    # EVERY `src` IN THE RECORD, wherever it lives — axes, burden, toll, strata,
    # window, moved, blockers. Walking is deliberate: the schema grows fields and
    # a hand-written list of paths is the thing that goes stale (gaps.md #69).
    def walk_src(node, path):
        if isinstance(node, dict):
            if "src" in node:
                check_src(node["src"], f"{here}: {path or 'record'}", errors)
            for k, v in node.items():
                walk_src(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for v in node:
                walk_src(v, path + "[]")
    walk_src(rec, "")

    # A mechanism claim must be argued in the witness, not merely asserted.
    witness = rec.get("witness") or {}
    if ax.get("mechanism") == "established" and not witness.get("mechanism"):
        errors.append(f"{here}: mechanism=established with no chain stated in the witness")
    if rec.get("contested") and not witness.get("contested"):
        errors.append(f"{here}: contested=true but the witness does not name the parties")

    # toll is required: a half-populated field poisons the derived lists, and
    # "not rated" must never be silently readable as "costs nothing".
    toll = rec.get("toll")
    if not isinstance(toll, dict):
        errors.append(f"{here}: no toll — every intervention has a price, including none")
    else:
        if toll.get("severity") not in SEVERITIES:
            errors.append(f"{here}: toll.severity={toll.get('severity')!r} not in {SEVERITIES}")
        if not toll.get("what"):
            errors.append(f"{here}: toll has no witness — say what it takes, or that it takes nothing")
        inc = (toll.get("incidence") or {})
        if not isinstance(inc, dict) or inc.get("value") is None or not inc.get("units"):
            errors.append(f"{here}: toll.incidence must be a {{value, units, src}} record")
        elif toll.get("severity") == "none" and inc["value"] > 0:
            errors.append(f"{here}: toll severity is none but incidence is {inc['value']}")

    meas = rec.get("measurement")
    if not isinstance(meas, dict):
        errors.append(f"{here}: no measurement block")
    else:
        # BURDEN SCALARS WERE NEVER SHAPE-CHECKED. `burden.ylds` sat in the
        # schema on four records, unvalidated and unused, while four records
        # were written complaining that the mortality axes could not see them.
        # A field nothing reads is a field nothing checks.
        for key in ("deaths", "prevalence", "incidence", "ylds"):
            scalar = (rec.get("burden") or {}).get(key)
            if scalar is None:
                continue
            if not isinstance(scalar, dict):
                errors.append(f"{here}: burden.{key} must be a {{value, units, src}} record")
                continue
            for field in ("value", "units", "src"):
                if scalar.get(field) in (None, ""):
                    errors.append(f"{here}: burden.{key} is missing {field}")
            if isinstance(scalar.get("value"), (int, float)) and scalar["value"] < 0:
                errors.append(f"{here}: burden.{key}.value={scalar['value']} is negative")

        for key, allowed in MEASUREMENT_ENUMS.items():
            if meas.get(key) not in allowed:
                errors.append(f"{here}: measurement.{key}={meas.get(key)!r} not in {allowed}")
        if not meas.get("witness"):
            errors.append(f"{here}: measurement has no witness")
        # `n/a` means there is no predictive question — either nothing
        # course-altering to predict a response to, or a treatment that works in
        # essentially everyone (hepatitis C: pan-genotypic DAAs abolished the
        # question). Anything else claiming n/a is dodging a real gap.
        if meas.get("predictive") == "n/a":
            eff = (rec["axes"].get("efficacy") or {}).get("value", 0)
            if rec["axes"]["intervention"] not in ("none", "symptomatic") and eff < 0.85:
                errors.append(f"{here}: predictive=n/a but there IS a selection "
                              f"question (intervention={rec['axes']['intervention']}, "
                              f"efficacy={eff})")

    strata = rec.get("strata")
    if strata is not None:
        total = 0.0
        for s in strata:
            label = f"{here}: stratum {s.get('name')!r}"
            if s.get("intervention") not in AXIS_ENUMS["intervention"]:
                errors.append(f"{label} has intervention={s.get('intervention')!r}")
            if s.get("toll") not in SEVERITIES:
                errors.append(f"{label} has toll={s.get('toll')!r} not in {SEVERITIES}")
            if not s.get("what"):
                errors.append(f"{label} has no witness")
            for field in ("fraction", "efficacy"):
                scalar = s.get(field)
                if not isinstance(scalar, dict) or scalar.get("value") is None or not scalar.get("units"):
                    errors.append(f"{label} {field} must be a {{value, units, src}} record")
            if isinstance(s.get("fraction"), dict):
                total += s["fraction"]["value"]
        # Arithmetic, not judgement: strata partition the patients or they are
        # not strata. A set that sums to 0.8 is silently missing a fifth of them.
        if abs(total - 1.0) > 0.05:
            errors.append(f"{here}: stratum fractions sum to {total:.3g}, not 1")

    # residue: what the DISEASE leaves behind in someone the treatment cured.
    # Optional, and shaped like `toll` on purpose — the two are the two ways a
    # person fails to return to the state they were in before any of it.
    res = rec.get("residue")
    if res is not None:
        if res.get("severity") not in SEVERITIES:
            errors.append(f"{here}: residue.severity={res.get('severity')!r} not in {SEVERITIES}")
        if not res.get("what"):
            errors.append(f"{here}: residue has no witness — say what the disease leaves")
        inc = (res.get("incidence") or {})
        if not isinstance(inc, dict) or inc.get("value") is None or not inc.get("units"):
            errors.append(f"{here}: residue.incidence must be a {{value, units, src}} record")
        elif res.get("severity") == "none" and inc["value"] > 0:
            errors.append(f"{here}: residue severity is none but incidence is {inc['value']}")
        # A residue is damage that outlasts the EPISODE. The original rule
        # required capability, on the reasoning that with nothing that works
        # nobody survives to be left with anything — and dracunculiasis broke it
        # on arrival: there is no drug and no vaccine, the worm emerges over
        # weeks and the disease is over, and a minority are permanently disabled
        # by the secondary infection. Self-limiting disease leaves a residue
        # without anyone curing anything.
        #
        # So the real precondition is that the episode ENDS — by cure, or by
        # resolving on its own — and the schema cannot tell those apart. What a
        # residue genuinely cannot mean is damage from a disease that is still
        # doing it (Huntington's, ME/CFS): there the damage IS the disease and
        # the axes already say so.
        #
        # Warn rather than reject: the distinction needs a person, and a check
        # that cannot decide should report rather than block.
        if not has_capability(rec):
            warnings.append(
                f"{here}: residue on a record with no capability — check that the "
                f"episode ENDS (self-limiting, like dracunculiasis) rather than the "
                f"disease still causing the damage (progressive, like Huntington's)")

    win = rec.get("window")
    if win is not None:
        for field in ("what", "closes_on", "caught_in_time"):
            if not win.get(field):
                errors.append(f"{here}: window is missing {field}")

    for b in rec.get("blockers") or []:
        tag = f"{here}: blocker[{b.get('kind')}]"
        if b.get("kind") not in BLOCKER_KINDS:
            errors.append(f"{tag} kind is not in the taxonomy")
        if b.get("standing") not in STANDINGS:
            errors.append(f"{tag} standing={b.get('standing')!r} not in {sorted(STANDINGS)}")
        for field in ("blocks", "what", "who_could"):
            if not b.get(field):
                errors.append(f"{tag} is missing {field}")
        for actor in b.get("who_could") or []:
            if actor not in ACTORS:
                errors.append(f"{tag} who_could has unknown actor {actor!r}")
        if b.get("kind") == "knowledge" and b.get("scale") is not None:
            warnings.append(f"{tag} is a knowledge blocker with a price — is it really?")
        if b.get("standing") == "alleged":
            warnings.append(f"{tag} is ALLEGED — convert to documented or refuted")
    if not rec.get("blockers"):
        errors.append(f"{here}: no blockers — every unsolved gap has a reason")

    if not (rec.get("assertion") or {}).get("id"):
        errors.append(f"{here}: no assertion id")
    return errors, warnings


# --------------------------------------------------------------------------


def flatten(rec, d) -> dict:
    """One flat row per record — the shape a spreadsheet or dataframe wants.

    Prose is dropped deliberately: CSV is for counting, not reading. Anything
    that needs the witness should use the JSON.
    """
    ax, m, toll = rec["axes"], rec["measurement"], rec["toll"]
    return {
        "slug": rec["slug"], "name": rec["name"], "kind": rec["kind"],
        "mondo": rec["mondo"], "residual": rec["residual"], "contested": rec["contested"],
        "mechanism": ax["mechanism"], "intervention": ax["intervention"],
        "prevention": ax["prevention"], "ongoing": ax["ongoing"],
        "efficacy": ax["efficacy"]["value"], "access": ax["access"]["value"],
        "diagnostic": m["diagnostic"], "prognostic": m["prognostic"],
        "predictive": m["predictive"],
        "toll_severity": toll["severity"], "toll_incidence": toll["incidence"]["value"],
        "capability": d["capability"], "terms": d["terms"],
        "residue_severity": (rec.get("residue") or {}).get("severity", ""),
        "residue_terms": d["residue_terms"], "restored": d["restored"],
        "reach": d["reach"],
        "delivery": d["delivery"], "quadrant": d["quadrant"],
        "orphaned": d["orphaned"], "has_window": d["has_window"],
        "spans_ladder": d["spans_ladder"],
        "overtreatment_risk": d["overtreatment_risk"],
        "futile_treatment_risk": d["futile_treatment_risk"],
        "cured_at_a_price": d["cured_at_a_price"],
        "only_knowledge_blockers": d["only_knowledge_blockers"],
        "measurement_gap": d["measurement_gap"],
        "cheapest_priced_blocker": d["cheapest_priced_blocker"],
        "blocker_kinds": "|".join(d["blocker_kinds"]),
        "actors": "|".join(d["actors"]),
        "assertion": rec["assertion"]["id"],
    }


def _srcs(node, out, path=""):
    """Walk anything and record every `src:` it finds, wherever it is.

    Deliberately generic rather than a list of known field paths. Every
    empirical scalar in this schema is `{value, units, src}`, so a walker
    cannot go stale when a field is added — and the one number this register
    most needs to publish about itself is how many of those are sourced.

    Records the PATH as well as the kind, because the path decides what a
    citation could even settle. See `scalar_tier`.
    """
    if isinstance(node, dict):
        if "src" in node:
            out.append((path, src_kind(node["src"])))
        for k, v in node.items():
            _srcs(v, out, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for v in node:
            _srcs(v, out, path + "[]")
    return out


def _tally(values) -> dict:
    """Counter, but ordered by count then key so the JSON diffs cleanly."""
    out = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], str(kv[0]))))


def snapshot(payload, on_date=None) -> dict:
    """Freeze today's aggregates — the register's own state of the world.

    COMPUTED ONLY FROM THE BUILT PAYLOAD, never from the YAML directly, so a
    snapshot cannot disagree with the artifacts published beside it. Same rule
    as index.md: derive once, in one place.

    WHAT IT DELIBERATELY DOES NOT CONTAIN. Anything from Engpass — that register
    writes its own snapshots, because Nordstern does not know it exists
    (Engpass/test_boundary.py). And no copy of what the records DECLARE: a
    snapshot is what the register SAID on a date, not a duplicate of it. The
    YAML is already in nordstern.json and in whatever holds this repository.

    THAT RULE WAS AMENDED ON 2026-09-02 AND THE AMENDMENT IS NARROW.
    It used to read "no per-record data" full stop, and `buckets` stored counts
    alone. That made the bucket time series unusable for the only question it
    exists to answer. `changes-you: 63` next to `changes-you: 71` cannot say
    whether eight diseases got worse or eight records were written, and those are
    opposite findings — the register grew by three the afternoon this was fixed.

    A DECLARED value can be recovered from history; a DERIVED one cannot, because
    the deriving code moves. Recovering "which bucket was `hepatitis-c` in on
    this date" would mean checking out that day's YAML *and* that day's
    `bucket()`, and reconciling them against a `buckets.yaml` version that may
    since have changed — which is precisely the drift `version` and `digest` were
    added to make visible. Freezing the count while not freezing the assignment
    that produced it was inconsistent: they are the same derived object at
    different granularity.

    So `buckets.members` is stored, and nothing else per-record is. The test is
    whether the value can be reconstructed later from data plus code; if it can,
    it stays out.

    MEMBERSHIP IS NOT BACKFILLED AND MUST NOT BE. Snapshots before this date
    carry counts only, and `bucket_diff` reports `skipped` against them rather
    than guessing — the same rule as a Sperrwerk check that cannot run. Deriving
    August's membership from September's records would fabricate exactly the
    history this field exists to record.

    THE `provenance` BLOCK IS THE POINT AND IT IS NOT FLATTERING. Every
    empirical scalar carries a `src`, and at the time of writing not one of them
    is a citation. A register that publishes a state of the world without
    publishing the state of its own sourcing is doing the thing Sperrwerk's
    ledger exists to prevent.
    """
    active = [r for r in payload if r["derived"]["status"] == "active"]
    blockers = [b for r in active for b in r["blockers"]]
    deaths = [(r["burden"].get("deaths") or {}).get("value") for r in active]
    deaths = [d for d in deaths if d]
    moved = [m for r in active for m in (r.get("moved") or [])]

    priced = [b for b in blockers if b.get("scale")]
    by_kind_priced = {}
    for b in blockers:
        k = b["kind"]
        slot = by_kind_priced.setdefault(k, {"total": 0, "priced": 0})
        slot["total"] += 1
        if b.get("scale"):
            slot["priced"] += 1

    # `unknown` is NOT sourced. It means nobody has the number — `msmds` and
    # `noma` use it deliberately — and counting it as a citation would be the
    # same error as a Sperrwerk check reporting `ok` when it could not run.
    found = []
    for r in payload:               # per record, so a path reads `burden.deaths`
        _srcs(r, found)
    prov = _tally(kind for _, kind in found)
    cited = prov.get("cited", 0)

    # THE DENOMINATOR, AND IT IS THE POINT OF THIS BLOCK. A citation settles a
    # burden figure, supports a dated event, and cannot touch a synthesis this
    # register defines. Reporting one total made "0 of 1,582" read as a backlog
    # when most of it is not work anybody could do.
    tiers = {t: {"total": 0, "cited": 0} for t in
             ("sourceable", "supportable", "judged")}
    for path, kind in found:
        slot = tiers[scalar_tier(path)]
        slot["total"] += 1
        if kind == "cited":
            slot["cited"] += 1

    return {
        "date": on_date or datetime.date.today().isoformat(),
        "register": "nordstern",
        "records": {
            "active": len(active),
            "deprecated": len(payload) - len(active),
        },
        # What the register concluded. These are RATINGS — the register's own
        # judgements — which is what it is for, and they do not pretend to be
        # measurements the way the burden block does.
        "capability": _tally(r["derived"]["capability"] for r in active),
        # "You get it, and then what?" — the only axis in this register that
        # means the same thing in every record.
        "survival": {
            "bands": _tally(r["derived"]["survival_band"] for r in active),
            "rated": sum(1 for r in active if r["derived"]["survival_band"] != "n/a"),
            # HOW MANY reach the horizon vs WHAT REACHING IT MEANS. Bands alone
            # put `head-neck-cancer` (cured) and `heart-failure` (still dying) in
            # one bucket at 0.55, which is the failure gaps.md #216 logged.
            "outcomes": _tally(r["derived"]["survival_outcome"] for r in active),
            "was_uniformly_fatal": sum(1 for r in active
                                       if r["derived"]["was_uniformly_fatal"]),
            "no_longer_terminal": sum(1 for r in active
                                      if r["derived"]["no_longer_terminal"]),
            # What medicine bought, summed over the rated records. The mean is
            # not a claim about medicine — it is a claim about *this corpus*,
            # which is chosen for structural diversity and is not a sample.
            #
            # THE UNTREATED GUARD IS LOAD-BEARING AND WAS ADDED WITH
            # `genital-herpes`. A gain of zero means two completely different
            # things depending on what was at stake. For `alzheimers`,
            # `huntington`, `rabies` and `prion-disease` — untreated survival
            # 0.45, 0.0, 0.0, 0.02 — it means **medicine buys no life against a
            # course that kills you.** For a disease nobody dies of it means
            # only that **there was no death to prevent**, which is not a
            # finding about medicine at all.
            # Without this guard, genital herpes would have been listed on the
            # dashboard beside rabies under *"where treatment bought no extra
            # life at all"*. The threshold is deliberately loose: 0.95 untreated
            # survival is "essentially nobody was going to die of this".
            "zero_gain": sorted(
                r["slug"] for r in active
                if r["derived"]["survival_gain"] == 0
                and ((r.get("survival") or {}).get("untreated") or {}).get("value", 0) < 0.95),
        },
        # THE BUCKETS, WITH THE VERSION AND DIGEST THAT MAKE THEM COMPARABLE.
        # Counts alone are not a time series: if a rule changed between two
        # snapshots, the same label answers a different question. `version` is
        # buckets.yaml's; `digest` fingerprints the rules themselves.
        "buckets": {
            "version": bucket_version(),
            "digest": bucket_digest(),
            # The display names come from buckets.yaml, not from the page. The
            # definitions are the artefact; a second copy of the labels in the
            # HTML is exactly the drift the banner rewrite already fixed once.
            "names": bucket_names(),
            # The rule and the disclaimer, carried with the counts they produced,
            # so a section can render the definition that was in force on the day
            # rather than today's copy of it. See bucket_defs().
            "defs": bucket_defs(),
            "a": _tally(r["derived"]["bucket"] for r in active),
            "b": _tally(t for r in active for t in r["derived"]["bucket_tags"]),
            "b_untagged": sum(1 for r in active if not r["derived"]["bucket_tags"]),
            # WHO WAS IN EACH BUCKET, WHICH IS THE ONLY WAY THE COUNTS ABOVE
            # BECOME A TIME SERIES. See the docstring: a count that moved cannot
            # say whether a disease moved or a record was written, and only the
            # first is a fact about medicine. Keyed by slug because `slug` is the
            # human handle and `id` is the permanent one — both are carried, so a
            # renamed record can still be followed across a year.
            "members": {
                r["slug"]: {
                    "id": r["id"],
                    "a": r["derived"]["bucket"],
                    "b": r["derived"]["bucket_tags"],
                }
                for r in active
            },
        },
        "quadrant": _tally(r["derived"]["quadrant"] for r in active),
        "delivery": _tally(r["derived"]["delivery"] for r in active),
        # THE ASYMMETRY IN LIVES RATHER THAN IN BLOCKER COUNTS. The register's
        # headline finding is that most of what blocks medicine is delivery
        # rather than knowledge; this says the same thing in deaths per year, so
        # a later pass can watch it move. `rated` is carried because the totals
        # are sums over a subset — 43 records have no `deaths` and five are
        # `preventable` — and a total whose denominator is invisible is the kind
        # of number that gets quoted wrongly.
        "gaps": {
            # TWO PARALLEL READINGS, DELIBERATELY NOT SUMMED. `knowledge`/
            # `delivery` are deaths a year; `knowledge_yld`/`delivery_yld` are
            # years lived with disability a year. A record may carry both, one
            # or neither, and adding them across units would be meaningless.
            "yld_rated": sum(1 for r in active if r["derived"]["knowledge_yld"] is not None),
            "knowledge_yld": round(sum(r["derived"]["knowledge_yld"] or 0 for r in active), 1),
            "delivery_yld": round(sum(r["derived"]["delivery_yld"] or 0 for r in active), 1),
            "top_knowledge_yld": [
                r["slug"] for r in sorted(
                    (r for r in active if r["derived"]["knowledge_yld"]),
                    key=lambda r: -r["derived"]["knowledge_yld"])[:10]],
            "rated": sum(1 for r in active if r["derived"]["knowledge_gap"] is not None),
            "knowledge": round(sum(r["derived"]["knowledge_gap"] or 0 for r in active), 1),
            "delivery": round(sum(r["derived"]["delivery_gap"] or 0 for r in active), 1),
            "top_knowledge": [
                r["slug"] for r in sorted(
                    (r for r in active if r["derived"]["knowledge_gap"]),
                    key=lambda r: -r["derived"]["knowledge_gap"])[:10]],
            "top_delivery": [
                r["slug"] for r in sorted(
                    (r for r in active if r["derived"]["delivery_gap"]),
                    key=lambda r: -r["derived"]["delivery_gap"])[:10]],
        },
        "terms": _tally(r["derived"]["terms"] for r in active),
        "axes": {ax: _tally(r["axes"][ax] for r in active)
                 for ax in ("mechanism", "intervention", "prevention", "ongoing")},
        "measurement": {m: _tally(r["measurement"][m] for r in active)
                        for m in ("diagnostic", "prognostic", "predictive")},
        "flags": {
            f: sum(1 for r in active if r["derived"].get(f))
            for f in ("measurement_gap", "overtreatment_risk", "futile_treatment_risk",
                      "cured_at_a_price", "harm_without_benefit", "orphaned",
                      "spans_ladder", "has_window", "has_residue",
                      "only_knowledge_blockers")
        },
        "contested": sum(1 for r in active if r.get("contested")),
        "reach": {
            "mean": round(sum(r["derived"]["reach"] for r in active) / len(active), 4),
            "median": round(sorted(r["derived"]["reach"] for r in active)[len(active) // 2], 4),
        },
        "blockers": {
            "total": len(blockers),
            "by_kind": _tally(b["kind"] for b in blockers),
            "by_standing": _tally(b["standing"] for b in blockers),
            # THE ASYMMETRY THE REGISTER EXISTS TO SHOW: a knowledge blocker
            # cannot be triaged with money and a delivery blocker can. Stored as
            # priced-vs-total per kind so the claim can be checked rather than
            # asserted.
            "priced": len(priced),
            "by_kind_priced": dict(sorted(by_kind_priced.items())),
            "actors": _tally(a for b in blockers for a in (b.get("who_could") or [])),
        },
        # A HISTORY THE REGISTER HAS ALWAYS HELD AND NEVER PLOTTED. Every `moved`
        # entry is a dated, attributed change on a named axis, the earliest here
        # from 1926. Aggregated by decade so the shape of a century of medicine
        # is one array — and so the register's own finding stays visible: it
        # records changes in CAPABILITY and almost none in mechanism or
        # measurement.
        "moved": {
            "total": len(moved),
            "by_axis": _tally(m["axis"] for m in moved),
            "by_decade": dict(sorted(_tally(
                f"{int(str(m['date'])[:4]) // 10 * 10}s" for m in moved
                if str(m.get("date", ""))[:4].isdigit()).items())),
        },
        # PUBLISHED BECAUSE IT IS BAD. See the docstring.
        "provenance": {
            "scalars": len(found),
            "by_src": prov,
            "cited": cited,
            "by_tier": tiers,
            # Kept under the old name so a stored snapshot stays readable; it is
            # the same number as `cited`.
            "verified": cited,
            "unknown": prov.get("unknown", 0),
            # The join key to every external source, and the second half of what
            # this register has to say about its own trustworthiness. It went
            # from "unresolved everywhere" to mostly resolved without the public
            # page noticing, which is why it is a computed field now.
            "mondo_resolved": sum(
                1 for r in active if r.get("mondo", "unresolved") != "unresolved"),
            "mondo_unresolved": sum(
                1 for r in active if r.get("mondo", "unresolved") == "unresolved"),
            "note": ("Every empirical scalar carries a src. `recall` is the model's "
                     "memory, `reasoning` is its arithmetic, and `unknown` means "
                     "nobody has the number — none of the three is a citation. "
                     "`by_tier` is the honest denominator: a citation SETTLES a "
                     "sourceable scalar, SUPPORTS a supportable one, and cannot "
                     "touch a judged one, because no dataset holds a quantity this "
                     "register defines. Blockers are judged and carry their "
                     "evidential status in `standing` instead."),
        },
        # Kept last and deliberately hedged: this column is the least trustworthy
        # thing here. It exceeds all human mortality because the records overlap
        # (gaps.md #147), and six of its zeros mean six different things (#182,
        # #211).
        "burden": {
            "records_with_deaths": len(deaths),
            "records_without_deaths": len(active) - len(deaths),
            "attributed_deaths_sum": sum(deaths),
            "note": ("An UPPER BOUND, not a total. Records overlap — TB deaths in "
                     "people with HIV are in both, sepsis is the mode of death for "
                     "several others — and the sum exceeds annual global mortality. "
                     "Do not chart this as a total."),
        },
    }


def bucket_diff(old, new) -> dict:
    """What moved between two snapshots, decomposed so the signal is separable.

    THREE NUMBERS AND ONLY ONE OF THEM IS ABOUT MEDICINE.
      arrivals   — records that did not exist in `old`. THE CORPUS GREW.
      departures — records deprecated or removed since. Also not medicine.
      movements  — a record rated into a different bucket. **THE ONLY SIGNAL.**

    A bucket's net count change is arrivals minus departures plus movements in
    and out, and while the register is still being written the first term
    dominates everything. Reporting the net alone would let corpus growth read
    as progress, which is the failure this whole file is built to avoid.

    RECORDS ARE FOLLOWED BY `id`, NEVER BY `slug`. Slugs are the rename-tempting
    handle — `befund` became `nordstern`, `questions/` became `obstacles/` — and
    a renamed record followed by slug reads as a departure plus an arrival, which
    is two fabricated events in place of nothing happening at all.

    IT REFUSES RATHER THAN GUESSES, TWICE OVER.
    No `members` in either snapshot and it reports `skipped` — snapshots written
    before 2026-09-02 stored counts alone and their membership is not
    recoverable. And if `digest` moved between the two, the rules themselves
    changed: every "movement" may be a record sitting still while the definition
    walked past it, so the diff is returned with `rules_changed` set and the
    caller must say so. Neither case is allowed to look like a clean answer.
    """
    ob, nb = old.get("buckets") or {}, new.get("buckets") or {}
    out = {
        "from": old.get("date"), "to": new.get("date"),
        "skipped": None, "rules_changed": False,
        "from_version": ob.get("version"), "to_version": nb.get("version"),
        "arrivals": [], "departures": [], "movements": [],
        "tags_gained": [], "tags_lost": [], "by_bucket": {},
    }
    om, nm = ob.get("members"), nb.get("members")
    # `is None`, NOT falsiness. An empty membership map is a register with no
    # active records, which is a fact; an absent one is a snapshot that never
    # recorded it, which is the refusal. Written with `not` first, and the
    # departure test caught it — the last record leaving a register would have
    # been reported as "membership was not recorded" rather than as a departure.
    if om is None or nm is None:
        missing = [d for d, m in ((out["from"], om), (out["to"], nm)) if m is None]
        out["skipped"] = (
            f"bucket membership was not recorded in {', '.join(str(d) for d in missing)}"
            " — snapshots before 2026-09-02 stored counts only, and membership"
            " cannot be reconstructed after the fact")
        return out

    if ob.get("digest") != nb.get("digest"):
        out["rules_changed"] = True

    # Index by the permanent id; keep the slug for display.
    o_by = {v.get("id") or k: (k, v) for k, v in om.items()}
    n_by = {v.get("id") or k: (k, v) for k, v in nm.items()}

    for i in sorted(set(n_by) - set(o_by)):
        slug, v = n_by[i]
        out["arrivals"].append({"id": i, "slug": slug, "bucket": v["a"]})
    for i in sorted(set(o_by) - set(n_by)):
        slug, v = o_by[i]
        out["departures"].append({"id": i, "slug": slug, "bucket": v["a"]})

    for i in sorted(set(o_by) & set(n_by)):
        (o_slug, ov), (n_slug, nv) = o_by[i], n_by[i]
        if ov["a"] != nv["a"]:
            out["movements"].append({"id": i, "slug": n_slug, "was": o_slug,
                                     "from": ov["a"], "to": nv["a"]})
        gained = sorted(set(nv.get("b") or []) - set(ov.get("b") or []))
        lost = sorted(set(ov.get("b") or []) - set(nv.get("b") or []))
        for t in gained:
            out["tags_gained"].append({"id": i, "slug": n_slug, "tag": t})
        for t in lost:
            out["tags_lost"].append({"id": i, "slug": n_slug, "tag": t})

    # Per bucket, the four components that sum to the net change, so a reader can
    # see which of them produced it instead of being handed the total.
    for b in BUCKETS_A:
        slot = {"arrived": 0, "left": 0, "moved_in": 0, "moved_out": 0}
        slot["arrived"] = sum(1 for a in out["arrivals"] if a["bucket"] == b)
        slot["left"] = sum(1 for d in out["departures"] if d["bucket"] == b)
        slot["moved_in"] = sum(1 for m in out["movements"] if m["to"] == b)
        slot["moved_out"] = sum(1 for m in out["movements"] if m["from"] == b)
        slot["net"] = (slot["arrived"] - slot["left"]
                       + slot["moved_in"] - slot["moved_out"])
        slot["was"] = (ob.get("a") or {}).get(b, 0)
        slot["now"] = (nb.get("a") or {}).get(b, 0)
        out["by_bucket"][b] = slot
    return out


def load_snapshots(root) -> list:
    """Every snapshot on disk, oldest first. The series the dashboard reads."""
    d = os.path.join(root, "web", "snapshots", "nordstern")
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*.json"))):
        if os.path.basename(p) == "index.json":
            continue
        with open(p, encoding="utf-8") as fh:
            out.append(json.load(fh))
    return out


def print_diff(root) -> int:
    """`--diff` — the two most recent snapshots, decomposed. The tracking loop
    in its smallest form: measure, change something, measure again."""
    snaps = load_snapshots(root)
    if len(snaps) < 2:
        print("need two snapshots to compare", file=sys.stderr)
        return 1
    d = bucket_diff(snaps[-2], snaps[-1])
    print(f"\n# {d['from']} → {d['to']}\n")
    if d["skipped"]:
        print(f"  skipped — {d['skipped']}")
        return 0
    if d["rules_changed"]:
        print(f"  ** RULES CHANGED (buckets.yaml v{d['from_version']} → "
              f"v{d['to_version']}). A record can appear to move because the\n"
              f"     definition moved past it. Read every movement below with that.**\n")
    print(f"  {len(d['arrivals'])} arrived · {len(d['departures'])} departed · "
          f"**{len(d['movements'])} moved**   (only the last is about medicine)\n")
    for m in d["movements"]:
        print(f"    {m['slug']:<34} {m['from']}  →  {m['to']}")
    if not d["movements"]:
        print("    nothing moved bucket. On a register whose `moved:` entries span"
              "\n    the 1790s to the 2020s, that is the expected reading of one year.")
    print()
    for b, s in d["by_bucket"].items():
        if s["was"] == s["now"] and not s["moved_in"] and not s["moved_out"]:
            continue
        print(f"    {b:<24} {s['was']:>4} → {s['now']:<4} "
              f"(+{s['arrived']} new, -{s['left']} gone, "
              f"+{s['moved_in']}/-{s['moved_out']} rated)")
    print()
    return 0


def write_snapshot(snap, root) -> str:
    """One file per register per day, plus an index a static page can fetch.

    Same-day rebuilds overwrite. That makes the series densest on the days the
    register actually changed, which is the honest sampling: a snapshot is not
    an annual ceremony, it is a record of what was true whenever anyone built.

    The index exists because a static host will not list a directory, and the
    dashboard has to discover the series without a server.
    """
    d = os.path.join(root, "web", "snapshots", "nordstern")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, snap["date"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(snap, indent=1, ensure_ascii=False) + "\n")

    dates = sorted(os.path.splitext(f)[0] for f in os.listdir(d)
                   if f.endswith(".json") and f != "index.json")
    with open(os.path.join(d, "index.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"register": "nordstern", "snapshots": dates},
                            indent=1) + "\n")

    # And the whole series as a script tag. `fetch()` of a local file is blocked
    # by CORS in most browsers, so a dashboard that fetched its snapshots would
    # work on a server and be blank over file:// — the same reason data.js is a
    # script tag rather than JSON. Snapshots are a few kB each; this stays small
    # for decades.
    series = []
    for dt in dates:
        with open(os.path.join(d, dt + ".json"), encoding="utf-8") as fh:
            series.append(json.load(fh))
    # THE DIFF IS COMPUTED HERE, AT BUILD TIME, AND NEVER IN THE PAGE.
    # `web/`'s standing rule is that a derivation lives in one place or the two
    # copies drift, and "what moved between two snapshots" is a derivation with
    # three separate refusals in it — missing membership, a changed rule digest,
    # and following records by permanent id rather than by slug. Re-implementing
    # that in JavaScript is exactly how the page ends up telling a visitor that
    # eight diseases improved when eight records were written.
    diffs = [bucket_diff(a, b) for a, b in zip(series, series[1:])]
    with open(os.path.join(root, "web", "snapshots.js"), "w", encoding="utf-8") as fh:
        fh.write("/* GENERATED by check.py --build — do not edit. */\n")
        fh.write("window.NORDSTERN_SNAPSHOTS = "
                 + json.dumps(series, indent=1, ensure_ascii=False) + ";\n")
        fh.write("window.NORDSTERN_BUCKET_DIFFS = "
                 + json.dumps(diffs, indent=1, ensure_ascii=False) + ";\n")
    return path


def build(records, root) -> None:
    """YAML is the source of truth; this is the build stage.

    Emits three artifacts, all with the derived fields already computed —
    **never recompute a derivation in the front end**, or the rules live in two
    places and drift, which is the failure check.py exists to prevent.

      web/data.js    window.NORDSTERN — a script tag, so the page works over file://
      web/nordstern.json  the same payload, for machines and downloads
      web/nordstern.csv   one flat row per record, for a spreadsheet or dataframe
      web/slim.js    window.NORDSTERN_SLIM — one small row per record, for charts
      web/snapshots/nordstern/YYYY-MM-DD.json   today's aggregates, frozen
      web/snapshots.js    the whole snapshot series, as a script tag

    The snapshot is computed from `payload` rather than from `records`, so it
    can never disagree with the three artifacts published beside it.
    """
    import csv

    payload = [{**r, "derived": derive(r)} for r in records]
    web = os.path.join(root, "web")
    os.makedirs(web, exist_ok=True)

    blob = json.dumps({"records": payload, "generated_from": "entities/*.yaml"},
                      indent=1, ensure_ascii=False)
    with open(os.path.join(web, "nordstern.json"), "w", encoding="utf-8") as fh:
        fh.write(blob + "\n")
    # A script tag rather than fetch(): no CORS, so the page opens over file://
    # as well as over http. Swap to fetch when the payload outgrows a few MB.
    with open(os.path.join(web, "data.js"), "w", encoding="utf-8") as fh:
        fh.write("/* GENERATED by check.py --build — do not edit. */\n")
        fh.write("window.NORDSTERN = " + blob + ";\n")

    # A SLIM PER-RECORD ARTIFACT, for the dashboard.
    #
    # data.js is past 2 MB and the landing page is the CASUAL page — pulling the
    # full register to draw a scatter plot is the wrong trade. This carries only
    # what a chart needs, at roughly 1% of the size, and every value in it is
    # copied from the derived payload rather than recomputed: the front end must
    # never own a derivation.
    #
    # It is also the first half of the split the README has been predicting
    # since the payload-size note was written — slim index now, per-record fetch
    # when a page needs the prose.
    slim = [{
        "slug": r["slug"], "name": r["name"],
        "capability": r["derived"]["capability"], "quadrant": r["derived"]["quadrant"],
        "delivery": r["derived"]["delivery"], "terms": r["derived"]["terms"],
        "reach": r["derived"]["reach"],
        "efficacy": r["axes"]["efficacy"]["value"], "access": r["axes"]["access"]["value"],
        "mechanism": r["axes"]["mechanism"], "intervention": r["axes"]["intervention"],
        "deaths": (r["burden"].get("deaths") or {}).get("value"),
        "prevalence": (r["burden"].get("prevalence") or {}).get("value"),
        "knowledge_gap": r["derived"]["knowledge_gap"],
        "delivery_gap": r["derived"]["delivery_gap"],
        "bucket": r["derived"]["bucket"], "bucket_tags": r["derived"]["bucket_tags"],
        "ylds": (r["burden"].get("ylds") or {}).get("value"),
        "knowledge_yld": r["derived"]["knowledge_yld"],
        "delivery_yld": r["derived"]["delivery_yld"],
        # THE NAMES PEOPLE ACTUALLY USE, CARRIED SO A PAGE CAN BE SEARCHED.
        # The dashboard listed `refractive-error` in the section about treatments
        # that do not arrive, and the word "glasses" appeared nowhere on the
        # page. A register whose chips are its own slugs is legible only to
        # somebody who already knows them — `hat` is sleeping sickness, `cre` is
        # a carbapenem-resistant infection, `msmds` is nobody's idea of a word.
        "also": r.get("also") or [],
        # ONE PLAIN-ENGLISH NAME, RENDERED VISIBLY — the field that actually
        # solved this. `also` was tried first, clipped into the DOM so browser
        # find would reach it, and that was worse than nothing: ctrl-F jumped to
        # a match with no visible highlight, which reads as a broken page.
        # A name a reader can SEE is the only kind that helps, so there is one
        # per record, chosen, optional, and absent wherever `name` is already
        # what people say.
        "common": r.get("common"),
        "blocker_kinds": r["derived"]["blocker_kinds"],
        "orphaned": r["derived"]["orphaned"],
        "spans_ladder": r["derived"]["spans_ladder"],
        "has_window": r["derived"]["has_window"],
        "contested": bool(r.get("contested")),
        # "You get it, and then what?" — the band, the qualifier that stops the
        # band being misread, and the gap that says what medicine bought.
        "survival_band": r["derived"]["survival_band"],
        "survival_outcome": r["derived"]["survival_outcome"],
        "survival_sentence": r["derived"]["survival_sentence"],
        "survival_gain": r["derived"]["survival_gain"],
        "survival_treated": ((r.get("survival") or {}).get("treated") or {}).get("value"),
        "survival_untreated": ((r.get("survival") or {}).get("untreated") or {}).get("value"),
        "survival_horizon": (r.get("survival") or {}).get("horizon"),
        "survival_course": survival_course(r),
    } for r in payload if r["derived"]["status"] == "active"]
    with open(os.path.join(web, "slim.js"), "w", encoding="utf-8") as fh:
        fh.write("/* GENERATED by check.py --build — do not edit. */\n")
        fh.write("window.NORDSTERN_SLIM = "
                 + json.dumps(slim, ensure_ascii=False) + ";\n")

    rows = [flatten(r, r["derived"]) for r in payload]
    with open(os.path.join(web, "nordstern.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    snap = snapshot(payload)
    snap_path = write_snapshot(snap, root)

    size = len(blob) / 1024
    print(f"wrote web/data.js, web/nordstern.json ({size:.0f} kB), web/nordstern.csv "
          f"({len(rows)} rows)")
    print(f"wrote {os.path.relpath(snap_path, root)} "
          f"({snap['records']['active']} records, {snap['blockers']['total']} blockers, "
          f"{snap['provenance']['verified']}/{snap['provenance']['scalars']} scalars verified)")
    if size > 2048:
        print("  NOTE: payload past ~2 MB — time to split into a slim index "
              "plus per-record fetches (see README).")


def derive(r) -> dict:
    return {
        "status": status(r), "superseded_by": superseded_by(r),
        "capability": capability(r), "terms": terms(r),
        "residue_terms": residue_terms(r), "restored": restored(r),
        "has_residue": bool(r.get("residue")),
        "reach": round(reach(r), 6), "delivery": delivery(r),
        "knowledge_gap": knowledge_gap(r), "delivery_gap": delivery_gap(r),
        "bucket": bucket(r), "bucket_tags": bucket_tags(r),
        "knowledge_yld": knowledge_yld(r), "delivery_yld": delivery_yld(r),
        "quadrant": quadrant(r), "orphaned": orphaned(r),
        "survival_band": survival_band(r),
        "survival_outcome": survival_outcome(r),
        "survival_sentence": survival_sentence(r),
        "survival_gain": survival_gain(r),
        "was_uniformly_fatal": was_uniformly_fatal(r),
        "no_longer_terminal": no_longer_terminal(r),
        "spans_ladder": spans_ladder(r), "has_window": bool(r.get("window")),
        "overtreatment_risk": overtreatment_risk(r),
        "futile_treatment_risk": futile_treatment_risk(r),
        "cured_at_a_price": cured_at_a_price(r),
        "harm_without_benefit": (CAPABILITY[r["axes"]["intervention"]] == "unsolved"
                                 and terms(r) != "clean"),
        "cheapest_priced_blocker": min(
            (b["scale"] for b in r["blockers"] if b.get("scale")), default=None),
        # Two named concepts the register already talks about, derived here so the
        # query language does not need a quantifier or a cross-term OR to say them.
        # The rule: derive a flag when it names a concept the register HAS (these
        # were both canned questions long before they were fields) — never merely
        # to dodge a gap in the grammar.
        #
        # only_knowledge_blockers: EVERY blocker is knowledge. `blocker.kind:knowledge`
        # asks whether SOME blocker is, which is a different and much weaker claim.
        # This is the "money cannot move it at any price" set.
        "only_knowledge_blockers": bool(r["blockers"]) and all(
            b["kind"] == "knowledge" for b in r["blockers"]),
        # measurement_gap: either measurement failure. Overtreatment (we cannot say
        # who needed it) and futile treatment (we cannot say who will respond) are
        # two faces of one question — can we aim what we already have?
        "measurement_gap": overtreatment_risk(r) or futile_treatment_risk(r),
        "blocker_kinds": sorted({b["kind"] for b in r["blockers"]}),
        "actors": sorted({a for b in r["blockers"] for a in (b.get("who_could") or [])}),
        "unsourced_scalars": sum(1 for k in ("efficacy", "access")
                                 if r["axes"][k].get("src") == "recall"),
    }


def main() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    paths = sorted(glob.glob(os.path.join(root, "entities", "*.yaml")))
    if not paths:
        print("no records found", file=sys.stderr)
        return 2

    records, errors, warnings = [], [], []
    for p in paths:
        rec = load(p)
        e, w = check(rec, p)
        errors += e
        warnings += w
        records.append(rec)

    ids = [r["assertion"]["id"] for r in records if r.get("assertion")]
    if len(set(ids)) != len(ids):
        errors.append("assertion ids are not unique")

    # ---- append-only identity ------------------------------------------
    # `slug` is the human handle and is therefore tempting to rename. `id` is
    # the thing an outside citation resolves against and must never move, which
    # is why it is opaque and sequential rather than descriptive.
    # A residual record with no strata is the worst case: a bucket whose
    # record-level numbers are the only numbers, with nothing to fall back to.
    for r in records:
        if r.get("residual") and not r.get("strata"):
            warnings.append(f"{r['slug']}: residual bucket with no strata — "
                            f"every scalar is an average over an unnamed set")

    seen: dict[str, str] = {}
    by_slug = {r["slug"]: r for r in records}
    for r in records:
        rid = r.get("id")
        if not rid or not str(rid).startswith(ID_PATTERN):
            errors.append(f"{r['slug']}: id={rid!r} missing or not {ID_PATTERN}NNNN")
            continue
        if rid in seen:
            errors.append(f"id {rid} used by both {seen[rid]} and {r['slug']} "
                          f"— ids are never reused")
        seen[rid] = r["slug"]

    for r in records:
        dep = r.get("deprecated")
        if not dep:
            continue
        for field in ("date", "why"):
            if not dep.get(field):
                errors.append(f"{r['slug']}: deprecated block needs {field}")
        see = dep.get("see")
        if see is None:
            continue
        if see not in by_slug:
            errors.append(f"{r['slug']}: deprecated.see={see!r} is not a record")
            continue
        # A redirect must land somewhere a reader can use. Chains are allowed
        # and cycles are not; an unresolvable 302 is worse than a 410.
        hops, cur = 0, see
        while cur in by_slug and superseded_by(by_slug[cur]):
            cur = superseded_by(by_slug[cur])
            hops += 1
            if hops > 8 or cur == r["slug"]:
                errors.append(f"{r['slug']}: deprecated.see chain does not terminate")
                break

    markdown = "--markdown" in sys.argv
    records.sort(key=lambda r: (capability(r) != "curable", -reach(r)))
    # Deprecated records stay in --json and the built artifacts so a citation
    # still resolves; every derived table below counts only the live register.
    retired = [r for r in records if status(r) == "deprecated"]
    records = active(records)

    # --json makes the register a database rather than a document: every stored
    # field plus every derived one, so a question can be asked with jq, pandas
    # or a model, without re-implementing the derivation rules.
    if "--json" in sys.argv:
        print(json.dumps({"records": [{**r, "derived": derive(r)}
                                      for r in records + retired],
                          "errors": errors, "warnings": warnings},
                         indent=2, ensure_ascii=False))
        return 1 if errors else 0

    if "--diff" in sys.argv:
        return print_diff(root)

    if "--build" in sys.argv:
        if errors:
            for e in errors:
                print(f"  ERROR  {e}", file=sys.stderr)
            print("refusing to build from a register with errors", file=sys.stderr)
            return 1
        build(records, root)
        return 0

    print("\n## Register\n")
    print("| entity | mechanism | measurement dx·pg·pd | intervention | capability | terms | reach | delivery |")
    print("|---|---|---|---|---|---|---|---|")
    for r in records:
        ax = r["axes"]
        star = " ⚑" if orphaned(r) else ""
        clock = " ⧗" if r.get("window") else ""
        clock += " ⧉" if spans_ladder(r) else ""
        t = terms(r)
        t = f"**{t}**" if t != "clean" else t
        m = r["measurement"]
        mm = f"{m['diagnostic'][:4]}·{m['prognostic'][:4]}·{m['predictive'][:4]}"
        print(f"| {r['slug']}{star}{clock} | {ax['mechanism']} | {mm} | {ax['intervention']} "
              f"| **{capability(r)}** | {t} | {reach(r):.4g} | {delivery(r)} |")

    print("\n## Measurement — where treatment is aimed badly\n")
    over = [r for r in records if overtreatment_risk(r)]
    futile = [r for r in records if futile_treatment_risk(r)]
    print("**Overtreatment risk** — real capability, permanent price, no way to say who needs it:")
    for r in over:
        print(f"  - {r['slug']} (toll {r['toll']['severity']}, prognostic none)")
    print("\n**Futile treatment risk** — real capability, permanent price, no way to say who responds:")
    for r in futile:
        print(f"  - {r['slug']} (toll {r['toll']['severity']}, predictive none)")
    gaps = [r for r in records
            if r["measurement"]["prognostic"] in ("none", "partial")
            or r["measurement"]["predictive"] in ("none", "partial")]
    print(f"\n{len(gaps)}/{len(records)} records carry a prognostic or predictive gap.")
    abolished = [r["slug"] for r in records
                 if r["measurement"]["predictive"] == "n/a"
                 and r["axes"]["intervention"] not in ("none", "symptomatic")]
    # `n/a` has THREE meanings and they are not interchangeable:
    #   - abolished by success  : a treatment that works in essentially everyone
    #                             (hepatitis C, once pan-genotypic antivirals landed)
    #   - nothing to predict    : no course-altering therapy exists at all
    #                             (Huntington's, MSMDS)
    #   - abolished by monopoly : exactly one drug, so nothing to choose between
    #                             (schistosomiasis — praziquantel, alone, since the 1970s)
    # The first two are good news and the third is the opposite. Nothing in the
    # schema distinguishes them, so this prints the list and says so rather than
    # inventing a field to guess with. See gaps.md #55.
    print(f"predictive question with no answer needed: {', '.join(abolished) or 'none'}")
    print("  three different reasons, indistinguishable in the schema: abolished by a")
    print("  good-enough treatment, nothing course-altering to predict, or only one")
    print("  drug in existence. schistosomiasis is the third and reads like the first.")

    print("\n## Cured at a price — the cure itself takes something permanent\n")
    for r in sorted(records, key=lambda r: -SEVERITIES.index(r["toll"]["severity"])):
        if not cured_at_a_price(r):
            continue
        toll = r["toll"]
        inc = toll["incidence"]
        print(f"- **{r['slug']}** — {capability(r)}, **{terms(r)}** · "
              f"{toll['severity']}, {inc['value']:.3g} of treated · {inc['units']}")

    # The other half of "are they back to how they were before". `toll` is what
    # the cure takes; this is what the disease already took and no cure reaches.
    print("\n## Residue — what the disease leaves in someone it was cured in\n")
    print("| entity | restored? | toll | residue | incidence |")
    print("|---|---|---|---|---|")
    # NB: `records` here are the raw records — the `derived` block only exists
    # in the build payload, so the derivations are called rather than read.
    for r in sorted(records, key=lambda r: (restored(r) == "restored", r["slug"])):
        if restored(r) in ("n/a", "restored") and not r.get("residue"):
            continue
        res = r.get("residue") or {}
        inc = res.get("incidence") or {}
        v = f"{inc['value']:.3g}" if inc.get("value") is not None else "—"
        print(f"| **{r['slug']}** | `{restored(r)}` | {terms(r)} | "
              f"{res.get('severity', '—')} | {v} |")

    # Not designed for — this category fell out of the data once `toll` existed,
    # and it is the sharpest thing the field produces: treatment that takes
    # something permanent while the course of the disease is unchanged.
    #
    # IT USED TO BE HEADED "Harm without benefit — a major toll and nothing to
    # show for it", AND THAT WAS A VERDICT THE DATA DOES NOT SUPPORT. COPD is
    # the record that made it visible: `capability: unsolved` is correct, since
    # nothing alters the decline in lung function — and long-acting
    # bronchodilators substantially relieve breathlessness, which for a disease
    # whose entire burden IS breathlessness is a large benefit delivered to
    # hundreds of millions of people.
    #
    # The register has exactly one notion of benefit and it is course
    # alteration (gaps.md #98). Until it has another, this section must describe
    # what was computed — a permanent toll alongside an unchanged course — and
    # must not editorialise past it. Same defect as the `solved` →
    # `known & treatable` rename: a name that overclaims is a defect, not a
    # wording preference.
    print("\n## A permanent toll while the course is unchanged\n")
    print("Capability is `unsolved` — nothing alters the course — and the")
    print("treatment still takes something permanent. **This is not the same as")
    print("saying the treatment does nothing**: symptom relief is real and this")
    print("register has no axis that records it (gaps.md #98).\n")
    for r in records:
        if CAPABILITY[r["axes"]["intervention"]] != "unsolved" or terms(r) == "clean":
            continue
        print(f"- **{r['slug']}** — {r['toll']['severity']} toll, course "
              f"**unchanged** · {r['toll']['incidence']['units']}")

    # RESIDUAL BUCKETS. The flag existed from the beginning, was set by three
    # records, and until non-Hodgkin lymphoma forced the question NOTHING READ
    # IT — the schema marked a category error and then permitted every rating
    # anyway (gaps.md #125). This section is the minimum: make the flag visible
    # in the output, and say what it costs, so nobody quotes a record-level
    # scalar without seeing that it averages over a bucket.
    buckets = [r for r in records if r.get("residual")]
    if buckets:
        print("\n## Residual buckets — entities defined by exclusion\n")
        print("`residual: true` means the entity is a leftover rather than a disease.")
        print("**Every record-level scalar below is an average over a bucket** and")
        print("describes no patient. Read the strata, not the row.\n")
        for r in buckets:
            n = len(r.get("strata") or [])
            caps = sorted({CAPABILITY[s["intervention"]] for s in (r.get("strata") or [])})
            print(f"- **{r['slug']}** — efficacy {r['axes']['efficacy']['value']:.2g}, "
                  f"capability **{capability(r)}** · "
                  + (f"{n} strata spanning {', '.join(caps)}" if n
                     else "**and no strata at all**, so nothing carries the real numbers"))

    print("\n## Spans the ladder ⧉ — one entity, more than one answer\n")
    for r in records:
        if not spans_ladder(r):
            continue
        print(f"- **{r['slug']}** — \"is it solved\" is malformed, not hard:")
        for s in r["strata"]:
            cap = CAPABILITY[s["intervention"]]
            print(f"    - {s['fraction']['value']:.0%} {s['name']} → **{cap}**, "
                  f"toll {s['toll']}, efficacy {s['efficacy']['value']:.2g}")

    print("\n## Window ⧗ — capability depends on catching it in time\n")
    for r in records:
        w = r.get("window")
        if not w:
            continue
        caught = w["caught_in_time"]
        # Name which cost the window is charging. Schistosomiasis pays entirely
        # in `residue` — praziquantel is a safe cheap tablet — so calling it a
        # toll would misdescribe the most window-dependent record here.
        which = ("toll" if terms(r) in ("costly", "harsh") else "residue") \
            if window_toll_link(r) else None
        link = (f" · **the {which} is the price of missing it → `diagnosis` is "
                f"the cheap lever**") if which else ""
        print(f"- **{r['slug']}** — closes on {w['closes_on']}; "
              f"{caught['value']:.3g} caught in time{link}")

    print("\n## No champion (⚑) — science done, nobody carrying it\n")
    for r in records:
        if not orphaned(r):
            continue
        priced = [b for b in r["blockers"] if b.get("scale")]
        cheapest = min((b["scale"] for b in priced), default=None)
        cost = f"~${cheapest:.0g}" if cheapest else "unpriced"
        kinds = ",".join(sorted({b["kind"] for b in r["blockers"]}))
        actors = sorted({a for b in r["blockers"] for a in (b.get("who_could") or [])})
        print(f"- **{r['slug']}** — {capability(r)}, {delivery(r)} "
              f"(reach {reach(r):.3g}) · blockers: {kinds} · from {cost} · {', '.join(actors)}")

    # ---- THE MAP, GENERATED (it used to be maintained by hand) -----------
    #
    # This 2x3 was hand-edited into index.md for a hundred records and drifted
    # twice that anyone caught: two blocker counts were patched in wrong by
    # record 46, and four consecutive records — typhoid, mrsa, cre, malaria —
    # were appended to the wrong cell by a first-occurrence string replacement.
    # `test_index_md_quadrant_cells_match_the_derived_map` was written to catch
    # the second and does not prevent it.
    #
    # DERIVE, NEVER STORE — the rule index.md is written in, finally applied to
    # index.md. A footnoted slug (`sickle-cell\*`) is cross-listed on purpose;
    # cross-listing is now the only thing left to do by hand, and the test
    # treats an unannotated slug in the wrong cell as an error.
    print("\n## The map\n")
    cells: dict[str, list[str]] = {}
    for r in records:
        cells.setdefault(quadrant(r), []).append(r["slug"])
    # ROW LABELS ARE LOAD-BEARING: `test_index_md_quadrant_cells_match_the_derived_map`
    # finds the rows by their leading cell, reading `| **known** |` strictly and
    # `| **not known** |` for total membership. The second row is labelled by
    # what is NOT known rather than by "empirical", which is the wording the web
    # map uses — the two should probably converge, but the label here is what
    # the guard keys on and changing it silently disables half the check.
    MAP_ROWS = [("known", ["known & treatable", "known & modifiable",
                           "engineering problem"]),
                ("not known", ["empirical foothold", "empirical luck", "frontier"])]
    print("| mechanism | a treatment that works | alters the course | nothing yet |")
    print("|---|---|---|---|")
    for label, names in MAP_ROWS:
        row = [f"**{n}**<br>" + (" · ".join(sorted(cells.get(n, []))) or "—")
               for n in names]
        print(f"| **{label}** | " + " | ".join(row) + " |")
    unplaced = sorted({r["slug"] for r in records}
                      - {s for v in cells.values() for s in v})
    if unplaced:
        print(f"\n**Unplaced — derived no quadrant:** {', '.join(unplaced)}")

    print("\n## Blocker census\n")
    census: dict[str, int] = {}
    standing: dict[str, int] = {}
    for r in records:
        for b in r["blockers"]:
            census[b["kind"]] = census.get(b["kind"], 0) + 1
            standing[b["standing"]] = standing.get(b["standing"], 0) + 1
    print("| kind | n |")
    print("|---|---|")
    for k, n in sorted(census.items(), key=lambda kv: -kv[1]):
        print(f"| {k} | {n} |")
    total = sum(census.values())
    print(f"\n**{total} across {len(records)} records.**")
    print("\nstanding: " + " · ".join(f"{k}={v}" for k, v in sorted(standing.items())))

    knowledge_only = [r["slug"] for r in records
                      if all(b["kind"] == "knowledge" for b in r["blockers"])]
    print(f"\nknowledge-blocked only (no delivery lever): {', '.join(knowledge_only) or 'none'}")

    if not markdown:
        print("\n## Checks\n")
        for e in errors:
            print(f"  ERROR  {e}")
        seen = set()
        for w in warnings:
            label = w.split(" — ")[-1] if " — " in w else w
            if "recall" in w:
                seen.add("recall")
                continue
            print(f"  warn   {w}")
        if "recall" in seen:
            n = sum(1 for w in warnings if "recall" in w)
            print(f"  warn   {n} efficacy/access values are src=recall — unverified")
        # `mondo:` is the join key to every external source, so an unresolved one
        # is not cosmetic — it is a record no other dataset can be attached to.
        # Reported as a count rather than a warning per record: three of these
        # will never resolve (see mondo.md) and repeating that is noise.
        un = sum(1 for r in records if r.get("mondo", "unresolved") == "unresolved")
        if un:
            print(f"  note   {un}/{len(records)} records have no mondo: id — "
                  f"run resolve_mondo.py; see mondo.md for why some cannot")
        print(f"\n{len(records)} records · {len(errors)} errors · {len(warnings)} warnings")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
