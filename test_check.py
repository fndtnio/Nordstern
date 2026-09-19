"""Tests for check.py — the loader contract and the derivations that were wrong once.

    python3 -m unittest test_check -v

Zero dependencies, stdlib `unittest`, same as Sperrwerk.

WHY THIS FILE EXISTS, AND WHY IT IS SMALL. Until stroke (record 43) the Python
side of Nordstern had no tests at all; `node --test web/` covers the front end and
the built artifacts, which means it exercises the derivations only through
whatever the corpus happens to contain. A loader defect survived forty-three
records that way — SCHEMA.md documented an inline flow mapping the loader could
not read, and the loader returned it as a *string* rather than refusing, so the
record passed every schema check and crashed six hundred lines later in a report
emitter. See gaps.md #93-95.

So this covers two things and does not pretend to be a suite:

  1. The loader's contract, including what it must REFUSE. A parser that guesses
     is worse than one that fails.
  2. The three derivations that have been demonstrably wrong at least once —
     `restored`, `window_toll_link`, and the `residue`-without-capability rule.
     Each is pinned with the record that forced the correction.
"""

import unittest
import glob
import re
import os
import tempfile

import check

HERE = os.path.dirname(os.path.abspath(__file__))

try:                       # noqa: SIM105
    import yaml            # noqa: F401
    HAVE_PYYAML = True
except ImportError:
    HAVE_PYYAML = False


def rec(**over):
    """A minimal record that satisfies the derivations under test."""
    base = {
        "slug": "t", "name": "t", "kind": "disease",
        "axes": {"mechanism": "established", "intervention": "curative",
                 "prevention": "none", "ongoing": "none",
                 "efficacy": {"value": 0.9, "units": "u", "src": "recall"},
                 "access": {"value": 0.9, "units": "u", "src": "recall"}},
        "measurement": {"diagnostic": "objective", "prognostic": "good",
                        "predictive": "good", "witness": "w"},
    }
    base.update(over)
    return base


class TestLoaderRefuses(unittest.TestCase):
    """A value the loader cannot read must never come back looking like a value."""

    def load(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False)
        f.write(text)
        f.close()
        try:
            return check.load(f.name)
        finally:
            os.unlink(f.name)

    @unittest.skipIf(HAVE_PYYAML, "PyYAML accepts inline mappings — see the note below")
    def test_inline_flow_mapping_raises(self):
        # THE BUG. SCHEMA.md documented exactly this syntax in six places.
        #
        # NOTE THE SKIP, WHICH IS ITSELF A FINDING. `load()` uses PyYAML when it
        # is importable and the bounded loader otherwise, and the two now
        # DISAGREE about this syntax: PyYAML reads it, the bounded loader
        # refuses it. Sperrwerk tests that its two loaders produce identical
        # reports for exactly this reason; Nordstern does not, and a record
        # written with inline mappings would work on a machine with PyYAML and
        # fail on one without. Logged in gaps.md.
        with self.assertRaises(check.NordsternError) as cm:
            self.load("burden:\n  deaths: {value: 1, units: x, src: recall}\n")
        self.assertIn("inline flow mapping", str(cm.exception))

    @unittest.skipIf(HAVE_PYYAML, "PyYAML accepts inline mappings")
    def test_the_error_names_the_fix(self):
        # A diagnostic that does not say what to do instead is half a diagnostic.
        with self.assertRaises(check.NordsternError) as cm:
            self.load("a:\n  b: {value: 1}\n")
        self.assertIn("block", str(cm.exception))

    def test_block_form_of_the_same_value_works(self):
        got = self.load("burden:\n  deaths:\n    value: 1.5e6\n"
                        "    units: deaths/year\n    src: recall\n")
        self.assertEqual(got["burden"]["deaths"]["value"], 1.5e6)
        self.assertEqual(got["burden"]["deaths"]["src"], "recall")

    def test_inline_flow_SEQUENCE_still_works(self):
        # Lists are supported and are used by `also:` and `who_could:`;
        # the refusal above must not have caught them too.
        got = self.load("also: [a, b, c]\nempty: []\n")
        self.assertEqual(got["also"], ["a", "b", "c"])
        self.assertEqual(got["empty"], [])

    def test_folded_block_scalar(self):
        got = self.load("witness: >\n  one\n  two\nnext: 1\n")
        self.assertEqual(got["witness"].strip(), "one two")
        self.assertEqual(got["next"], 1)


class TestRestored(unittest.TestCase):
    """`restored` answers: are they back to the state before any of this?"""

    def test_clean_both_sides_is_restored(self):
        self.assertEqual(check.restored(rec()), "restored")

    def test_toll_only_is_cure_costs(self):
        r = rec(toll={"severity": "major", "permanent": True, "what": "w"})
        self.assertEqual(check.restored(r), "cure-costs")

    def test_residue_only_is_disease_residue(self):
        # Tuberculosis: the bacterium is gone, the lungs are scarred.
        r = rec(residue={"severity": "major", "permanent": True, "what": "w"})
        self.assertEqual(check.restored(r), "disease-residue")

    def test_both_sides_is_both(self):
        r = rec(toll={"severity": "major", "permanent": True, "what": "w"},
                residue={"severity": "catastrophic", "permanent": True, "what": "w"})
        self.assertEqual(check.restored(r), "both")

    def test_no_capability_is_na_not_restored(self):
        # `n/a` is not `restored`: a question that cannot be asked is not a
        # question answered well.
        r = rec(axes={**rec()["axes"], "intervention": "none"})
        self.assertEqual(check.restored(r), "n/a")


class TestWindowTollLink(unittest.TestCase):
    """Written reading only `toll`, which was wrong. It must read both costs."""

    def test_window_plus_residue_alone_still_links(self):
        # SCHISTOSOMIASIS IS THE RECORD THAT FORCED THIS. Praziquantel is a
        # cheap safe tablet, so the toll is clean; the entire price of missing
        # the window is scarring. The old rule reported no link on the most
        # window-dependent record in the register.
        r = rec(window={"what": "w", "closes_on": "c",
                        "caught_in_time": {"value": 0.1, "units": "u", "src": "recall"}},
                residue={"severity": "major", "permanent": True, "what": "w"})
        self.assertTrue(check.window_toll_link(r))

    def test_window_plus_toll_alone_links(self):
        r = rec(window={"what": "w", "closes_on": "c",
                        "caught_in_time": {"value": 0.1, "units": "u", "src": "recall"}},
                toll={"severity": "major", "permanent": True, "what": "w"})
        self.assertTrue(check.window_toll_link(r))

    def test_window_with_no_permanent_price_does_not_link(self):
        r = rec(window={"what": "w", "closes_on": "c",
                        "caught_in_time": {"value": 0.1, "units": "u", "src": "recall"}})
        self.assertFalse(check.window_toll_link(r))

    def test_permanent_price_with_no_window_does_not_link(self):
        r = rec(residue={"severity": "major", "permanent": True, "what": "w"})
        self.assertFalse(check.window_toll_link(r))


class TestQuadrant(unittest.TestCase):
    """The 2x3 map. gaps.md #89 — the boolean it replaced filed the first and
    third largest causes of death on Earth as 'nothing can be done'."""

    def test_the_ladder_is_three_bands_not_a_boolean(self):
        band = lambda iv: check.capability_tier(rec(axes={**rec()["axes"], "intervention": iv}))
        self.assertEqual(band("curative"), "treatable")
        self.assertEqual(band("suppressive"), "treatable")
        self.assertEqual(band("disease-modifying"), "modifiable")   # THE FIX
        self.assertEqual(band("symptomatic"), "neither")
        self.assertEqual(band("none"), "neither")

    def test_disease_modifying_is_not_binned_with_none(self):
        # The whole of #89 in one assertion.
        mod = rec(axes={**rec()["axes"], "intervention": "disease-modifying"})
        non = rec(axes={**rec()["axes"], "intervention": "none"})
        self.assertNotEqual(check.quadrant(mod), check.quadrant(non))

    def test_every_cell_is_named(self):
        # The derivation must be total, including cells no record occupies.
        for known in (True, False):
            for tier in ("treatable", "modifiable", "neither"):
                self.assertIn((known, tier), check.QUADRANTS)
        self.assertEqual(len(check.QUADRANTS), 6)

    def test_no_cell_is_called_solved(self):
        # The oldest naming rule here: a derived cell must not read as a verdict
        # on the disease. It applies to the new cells too.
        for name in check.QUADRANTS.values():
            self.assertNotIn("solved", name.lower(), name)


class TestEradicated(unittest.TestCase):
    """`prevention: eradicated` was special-cased in one derivation and needed three.

    Smallpox came out `capability: curable` and `quadrant: engineering problem`
    simultaneously — two derivations contradicting each other about the only
    disease humanity has ever eliminated — and `orphaned` fired on it as well:
    *science done, nobody carrying it*, about a disease nobody has.
    """

    def eradicated(self, efficacy=0.9, access=0.9, **over):
        ax = {**rec()["axes"], "prevention": "eradicated", "intervention": "symptomatic",
              "efficacy": {"value": efficacy, "units": "u", "src": "recall"},
              "access": {"value": access, "units": "u", "src": "recall"}}
        return rec(axes=ax, **over)

    def test_capability_is_curable(self):
        self.assertEqual(check.capability(self.eradicated()), "curable")

    def test_quadrant_agrees_with_capability(self):
        # THE CONTRADICTION. `symptomatic` would otherwise put the one
        # eradicated disease in "understood, and nothing can be done".
        r = self.eradicated()
        self.assertEqual(check.capability_tier(r), "treatable")
        self.assertEqual(check.quadrant(r), "known & treatable")

    def test_orphaned_never_fires(self):
        # Low reach + a documented non-knowledge blocker is exactly the shape
        # that fires everywhere else in the register.
        r = self.eradicated(efficacy=0.3, access=0.3,
                            blockers=[{"kind": "policy", "blocks": "b", "what": "w",
                                       "who_could": ["government"],
                                       "standing": "documented", "src": "recall"}])
        self.assertLess(check.reach(r), check.ORPHAN_REACH_CEILING)
        self.assertFalse(check.orphaned(r))

    def test_smallpox_is_the_only_occupant(self):
        # If a second one appears, these rules should be re-read rather than
        # assumed. After 48 records the top rung of `prevention` has one.
        recs = [check.load(p) for p in
                sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
        got = sorted(r["slug"] for r in recs if check.is_eradicated(r))
        self.assertEqual(got, ["smallpox"])


class TestAppendOnly(unittest.TestCase):
    """Permanent ids, deprecation, and the 302.

    `slug` is the human handle and is therefore tempting to rename. `id` is what
    an outside citation resolves against, so it is opaque, sequential, never
    reused, and never renumbered. A record that turns out to be the wrong frame
    — or whose MONDO term gets merged away — is deprecated in place and points
    at whatever replaced it.
    """

    def test_status_is_derived_not_stored(self):
        self.assertEqual(check.status(rec()), "active")
        self.assertEqual(check.status(rec(deprecated={"date": "2026-01-01", "why": "w"})),
                         "deprecated")

    def test_no_see_is_a_410_not_a_302(self):
        # "This record is simply no longer needed" is a different answer from
        # "it moved", and the register must be able to say both.
        r = rec(deprecated={"date": "2026-01-01", "why": "w"})
        self.assertIsNone(check.superseded_by(r))

    def test_see_is_the_302(self):
        r = rec(deprecated={"date": "2026-01-01", "why": "w", "see": "other"})
        self.assertEqual(check.superseded_by(r), "other")

    def test_active_filters(self):
        live, dead = rec(slug="a"), rec(slug="b", deprecated={"date": "x", "why": "y"})
        self.assertEqual([r["slug"] for r in check.active([live, dead])], ["a"])


class TestCorpusIdentity(unittest.TestCase):
    """The identity invariants, over the real records."""

    @classmethod
    def setUpClass(cls):
        cls.records = [check.load(p) for p in
                       sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]

    def test_every_record_has_a_permanent_id(self):
        for r in self.records:
            self.assertRegex(str(r.get("id")), r"^FND-D-\d{4}$", r["slug"])

    def test_ids_are_unique(self):
        ids = [r["id"] for r in self.records]
        dupes = {i for i in ids if ids.count(i) > 1}
        self.assertFalse(dupes, f"reused ids: {dupes}")

    def test_ids_and_slugs_are_both_unique(self):
        slugs = [r["slug"] for r in self.records]
        self.assertEqual(len(set(slugs)), len(slugs))

    def test_every_redirect_resolves(self):
        by_slug = {r["slug"]: r for r in self.records}
        for r in self.records:
            see = check.superseded_by(r)
            if see is None:
                continue
            self.assertIn(see, by_slug, f"{r['slug']} points at a missing record")
            # and the chain terminates
            hops, cur = 0, see
            while cur in by_slug and check.superseded_by(by_slug[cur]):
                cur = check.superseded_by(by_slug[cur]); hops += 1
                self.assertLess(hops, 8, f"{r['slug']}: redirect chain does not terminate")
                self.assertNotEqual(cur, r["slug"], f"{r['slug']}: redirect cycle")


class TestPreventable(unittest.TestCase):
    """gaps.md #66 — capability ignored the prevention axis and contradicted
    `has_capability`, which has always counted it."""

    def make(self, intervention, prevention):
        return rec(axes={**rec()["axes"], "intervention": intervention,
                         "prevention": prevention})

    def test_prophylaxis_rescues_a_record_with_no_treatment(self):
        # MEASLES AND RABIES. Both read `unsolved` before this.
        for iv in ("symptomatic", "none"):
            r = self.make(iv, "prophylaxis")
            self.assertEqual(check.capability(r), "preventable", iv)
            self.assertEqual(check.quadrant(r), "known & treatable", iv)

    def test_it_does_not_promote_past_modifiable(self):
        # RHEUMATIC HEART DISEASE has both penicillin prophylaxis AND
        # disease-modifying treatment. An unconditional override hid the
        # treatment behind the prophylaxis; where the map already says something
        # works, there is nothing to rescue.
        r = self.make("disease-modifying", "prophylaxis")
        self.assertEqual(check.capability(r), "partial")
        self.assertEqual(check.quadrant(r), "known & modifiable")

    def test_risk_reduction_is_not_enough(self):
        # Smoking cessation and diet do not make a disease preventable.
        r = self.make("symptomatic", "risk-reduction")
        self.assertEqual(check.capability(r), "unsolved")

    def test_capability_and_has_capability_no_longer_disagree(self):
        # THE CONTRADICTION #66 NAMED, asserted directly.
        for iv in ("none", "symptomatic", "disease-modifying", "suppressive", "curative"):
            for pv in ("none", "risk-reduction", "prophylaxis", "eradicated"):
                r = self.make(iv, pv)
                self.assertEqual(check.has_capability(r),
                                 check.capability(r) != "unsolved",
                                 f"{iv} x {pv}")

    def test_delivery_is_withheld_not_guessed(self):
        # `reach` is efficacy x access and both describe the TREATMENT, so for a
        # record whose capability is prevention the number means nothing.
        self.assertEqual(check.delivery(self.make("symptomatic", "prophylaxis")), "—")

    def test_the_three_records_that_forced_it(self):
        recs = {r["slug"]: r for r in
                (check.load(p) for p in
                 sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml"))))}
        for slug in ("measles", "rabies", "dengue"):
            self.assertEqual(check.capability(recs[slug]), "preventable", slug)
        # and the two that must NOT move
        for slug in ("rheumatic-heart-disease", "h5n1"):
            self.assertEqual(check.quadrant(recs[slug]), "known & modifiable", slug)


class TestResidual(unittest.TestCase):
    """`residual: true` marks an entity defined by exclusion. gaps.md #125.

    The flag existed from the beginning and NOTHING READ IT until non-Hodgkin
    lymphoma — three records had set it and the schema went on permitting every
    record-level rating as though the bucket were one disease.
    """

    @classmethod
    def setUpClass(cls):
        cls.records = [check.load(p) for p in
                       sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]

    def test_the_flag_is_used(self):
        buckets = [r["slug"] for r in self.records if r.get("residual")]
        self.assertIn("non-hodgkin-lymphoma", buckets)
        self.assertGreaterEqual(len(buckets), 3)

    def test_a_residual_record_with_strata_carries_the_real_numbers(self):
        # NHL's record-level efficacy averages diseases running from ~0.30 to
        # ~0.85. The strata are the only honest numbers in the file.
        nhl = next(r for r in self.records if r["slug"] == "non-hodgkin-lymphoma")
        caps = {check.CAPABILITY[s["intervention"]] for s in nhl["strata"]}
        self.assertGreater(len(caps), 1, "a bucket whose strata agree is not a bucket")
        self.assertTrue(check.spans_ladder(nhl))

    def test_residual_without_strata_is_flagged(self):
        # Two records set the flag and carry no strata, so the record-level
        # scalar is the ONLY number and it describes an unnamed set. The check
        # warns; this pins that they are known about rather than overlooked.
        bare = sorted(r["slug"] for r in self.records
                      if r.get("residual") and not r.get("strata"))
        self.assertEqual(bare, ["low-back-pain", "mcas"],
                         "a new residual record without strata needs a decision, "
                         "not a silent addition")


class TestCorpus(unittest.TestCase):
    """Cheap invariants over the real records, so the corpus itself is a fixture."""

    @classmethod
    def setUpClass(cls):
        cls.records = [check.load(p) for p in
                       sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]

    def test_every_record_loads_and_derives(self):
        self.assertGreaterEqual(len(self.records), 43)
        for r in self.records:
            self.assertIn(check.capability(r),
                          set(check.CAPABILITY.values()) | {"preventable"})
            self.assertIn(check.restored(r),
                          {"restored", "cure-costs", "disease-residue", "both", "n/a"})

    def test_scalars_are_mappings_not_strings(self):
        # The exact shape the loader bug produced. If a `{...}` ever slips back
        # into a record, this fails HERE rather than inside a report emitter.
        for r in self.records:
            for blk in ("efficacy", "access"):
                v = r["axes"][blk]
                self.assertIsInstance(v, dict, f"{r['slug']}.axes.{blk} is {type(v)}")
                self.assertIn("value", v)
            for s in r.get("strata") or []:
                self.assertIsInstance(s["fraction"], dict,
                                      f"{r['slug']} stratum {s['name']}: fraction is a string")
                self.assertIsInstance(s["efficacy"], dict,
                                      f"{r['slug']} stratum {s['name']}: efficacy is a string")

    def test_the_cardiovascular_records_moved_out_of_engineering_problem(self):
        # THE RECORDS THAT FORCED #89, pinned by name so a future change to the
        # bands cannot silently refile them as untreatable again.
        q = {r["slug"]: check.quadrant(r) for r in self.records}
        for slug in ("ischaemic-heart-disease", "stroke", "rheumatic-heart-disease"):
            self.assertEqual(q[slug], "known & modifiable", slug)
        # And COPD stays put — it is `symptomatic`, and the harsh verdict on the
        # COURSE is deserved. It is the record that chose this repair over the
        # other two.
        self.assertEqual(q["copd"], "engineering problem")

    def test_index_md_blocker_census_matches_the_records(self):
        """index.md is generated, and its census kept being hand-edited anyway.

        Two counts had drifted by record 46 — `no-sponsor` was two low and
        `regulatory` one low — because each new record's numbers were patched in
        by hand and two were missed. That is exactly the failure the
        derive-never-store rule exists to prevent, arriving in the file that
        rule is written in.
        """
        from collections import Counter
        counts = Counter(b["kind"] for r in self.records
                         for b in (r.get("blockers") or []))
        md = open(os.path.join(HERE, "index.md"), encoding="utf-8").read()
        stated = {m.group(1): int(m.group(2)) for m in
                  re.finditer(r"\|\s*([a-z-]+)\s*\|\s*(\d+)\s*\|", md)}
        for kind, n in counts.items():
            if kind in stated:
                self.assertEqual(stated[kind], n,
                                 f"index.md says {kind}={stated[kind]}, records say {n}")
        total = sum(counts.values())
        self.assertIn(f"{total} across {len(self.records)} records", md,
                      f"index.md census header should read {total} across "
                      f"{len(self.records)} records")

    def test_index_md_quadrant_cells_match_the_derived_map(self):
        """The census guard caught the counts; the map drifted underneath it.

        Four consecutive records — typhoid, mrsa, cre, malaria — were appended to
        `index.md`'s map by a first-occurrence string replacement, and every one
        of them landed in `known & modifiable`. All four derive `curable`. The
        census test passed the whole time, because a blocker count knows nothing
        about which cell a slug sits in.

        A slug carrying a footnote marker (`sickle-cell\\*`) may appear in a
        second cell deliberately — sickle cell is cross-listed because its cure
        exists and reaches nearly nobody. So the rule is asymmetric: every record
        MUST appear in its true cell, and an unannotated slug must NOT appear in
        any other.
        """
        import check, collections
        md = open(os.path.join(HERE, "index.md"), encoding="utf-8").read()
        row = next(l for l in md.splitlines() if l.startswith("| **known** |"))
        truth = collections.defaultdict(set)
        for r in self.records:
            if check.status(r) == "active":
                truth[check.quadrant(r)].add(r["slug"])

        seen = set()
        for cell in row.split("|")[2:5]:
            m = re.match(r"\s*\*\*(.+?)\*\*<br>(.*)", cell.strip())
            self.assertIsNotNone(m, f"unparseable map cell: {cell[:60]}")
            name = m.group(1)
            self.assertIn(name, truth, f"index.md map has unknown cell {name!r}")
            plain, annotated = set(), set()
            for tok in m.group(2).split("·"):
                tok = tok.strip().strip("*").strip()
                if not tok:
                    continue
                if tok.endswith("\\"):            # trailing \* / \*\* footnote
                    annotated.add(tok.rstrip("\\*").strip())
                else:
                    plain.add(tok)
            here = plain | annotated
            seen |= here
            self.assertEqual(truth[name] - here, set(),
                             f"index.md map cell {name!r} is missing "
                             f"{sorted(truth[name] - here)}")
            self.assertEqual(plain - truth[name], set(),
                             f"index.md map cell {name!r} lists "
                             f"{sorted(plain - truth[name])}, which derive "
                             f"a different quadrant and carry no footnote")

        # the bottom row's cells are checked for membership too, via the total
        every = {s for v in truth.values() for s in v}
        bottom = next(l for l in md.splitlines() if l.startswith("| **not known** |"))
        for tok in re.findall(r"[a-z][a-z0-9-]+", bottom.split("<br>", 1)[-1]):
            if tok in every:
                seen.add(tok)
        self.assertEqual(every - seen, set(),
                         f"records missing from the index.md map entirely: "
                         f"{sorted(every - seen)}")

    def test_strata_fractions_sum_to_one(self):
        for r in self.records:
            strata = r.get("strata") or []
            if not strata:
                continue
            total = sum(s["fraction"]["value"] for s in strata)
            self.assertAlmostEqual(total, 1.0, places=2, msg=r["slug"])


if __name__ == "__main__":
    unittest.main()


class TestSnapshot(unittest.TestCase):
    """The snapshot is what the register SAID on a date. Two ways it can lie.

    It can disagree with the artifacts published beside it, which would make the
    dashboard and the query tool tell a visitor two different things. And it can
    go stale — a snapshot file left behind after the records changed is exactly
    `index.md`'s drift failure, in a file nobody reads by eye.

    Both are checked by recomputing rather than by trusting, which is the same
    move as the two index.md guards above.
    """

    @classmethod
    def setUpClass(cls):
        cls.payload = [{**check.load(p), } for p in
                       sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
        cls.payload = [{**r, "derived": check.derive(r)} for r in cls.payload]
        cls.snap = check.snapshot(cls.payload, on_date="TEST")

    def test_snapshot_totals_agree_with_the_records(self):
        active = [r for r in self.payload if r["derived"]["status"] == "active"]
        self.assertEqual(self.snap["records"]["active"], len(active))
        self.assertEqual(self.snap["blockers"]["total"],
                         sum(len(r["blockers"]) for r in active))
        for tally in ("capability", "quadrant", "delivery", "terms"):
            self.assertEqual(sum(self.snap[tally].values()), len(active),
                             f"{tally} tally does not cover every active record")
        self.assertEqual(sum(self.snap["blockers"]["by_kind"].values()),
                         self.snap["blockers"]["total"])
        self.assertEqual(sum(self.snap["blockers"]["by_standing"].values()),
                         self.snap["blockers"]["total"])

    def test_unknown_is_not_counted_as_verified(self):
        """`unknown` means nobody has the number, and it is used deliberately.

        The first version of `snapshot()` counted everything that was not
        `recall` or `reasoning` as verified, and reported "8/1582 scalars
        verified" on its first run — all eight of them `src: unknown` in
        `msmds`, `noma` and `hat`, which is the opposite of a citation. Same
        error as a Sperrwerk check reporting `ok` when it could not run.
        """
        prov = self.snap["provenance"]
        self.assertEqual(prov["scalars"], sum(prov["by_src"].values()))
        self.assertEqual(
            prov["verified"],
            prov["scalars"] - sum(prov["by_src"].get(k, 0)
                                  for k in ("recall", "reasoning", "unknown")),
            "verified must exclude recall, reasoning AND unknown")
        self.assertEqual(prov["unknown"], prov["by_src"].get("unknown", 0))

    def test_moved_history_covers_every_moved_entry(self):
        """The century-long series the register has always held and never plotted."""
        active = [r for r in self.payload if r["derived"]["status"] == "active"]
        total = sum(len(r.get("moved") or []) for r in active)
        self.assertEqual(self.snap["moved"]["total"], total)
        self.assertEqual(sum(self.snap["moved"]["by_axis"].values()), total)
        self.assertLessEqual(sum(self.snap["moved"]["by_decade"].values()), total,
                             "a decade bucket cannot hold more than the entries")

    def test_the_snapshot_on_disk_is_not_stale(self):
        """Rebuild-vs-disk, ignoring only the date. This is the drift guard.

        If it fails, `python3 check.py --build` was not run after the records
        changed — and the dashboard is showing yesterday's state of the world
        beside today's query results.
        """
        import json
        d = os.path.join(HERE, "web", "snapshots", "nordstern")
        files = sorted(f for f in os.listdir(d)
                       if f.endswith(".json") and f != "index.json")
        self.assertTrue(files, "no snapshot written — run `python3 check.py --build`")
        with open(os.path.join(d, files[-1]), encoding="utf-8") as fh:
            on_disk = json.load(fh)
        fresh = dict(self.snap)
        fresh["date"] = on_disk["date"]
        self.assertEqual(on_disk, fresh,
                         "the latest snapshot disagrees with the current records — "
                         "run `python3 check.py --build`")

    def test_snapshot_index_lists_what_is_on_disk(self):
        """A static host will not list a directory, so the index IS the series."""
        import json
        for register in ("nordstern", "engpass"):
            d = os.path.join(HERE, "web", "snapshots", register)
            if not os.path.isdir(d):
                continue
            on_disk = sorted(os.path.splitext(f)[0] for f in os.listdir(d)
                             if f.endswith(".json") and f != "index.json")
            with open(os.path.join(d, "index.json"), encoding="utf-8") as fh:
                listed = json.load(fh)
            self.assertEqual(listed["snapshots"], on_disk,
                             f"{register}/index.json does not match the directory")
            self.assertEqual(listed["register"], register)

    def test_snapshot_carries_no_engpass_data(self):
        """Nordstern does not know Engpass exists — including in its snapshot.

        The dashboard wants both registers, and the shortcut is to total up the
        obstacles here. Engpass writes its own snapshot instead; the page reads
        two files. Mirrors Engpass/test_boundary.py from this side.
        """
        blob = repr(self.snap).lower()
        for word in ("engpass", "neuland", "obstacle"):
            self.assertNotIn(word, blob,
                             f"Nordstern's snapshot mentions {word!r}")


class TestProvenance(unittest.TestCase):
    """`src` became structured so a sourcing tool could not fabricate its way in.

    The rule is one line and it is the whole defence: **a citation must carry
    what it read.** An `id` and a date are unenforceable — a plausible DOI is
    exactly what a language model emits when it does not know, and it looks
    like success. A verbatim `quote` makes the claim checkable by a human in
    ten seconds and makes fabrication deliberate rather than accidental.

    `src: recall` is honest. A fabricated citation is not. That asymmetry is
    why this validation exists before any sourcing tool does.
    """

    def test_the_three_unsourced_words_are_accepted(self):
        for word in ("recall", "reasoning", "unknown"):
            self.assertEqual(check.src_kind(word), word)

    def test_anything_else_as_a_bare_string_is_refused(self):
        for bad in ("verified", "cited", "GBD", "", "https://doi.org/10.1/x"):
            self.assertEqual(check.src_kind(bad), "invalid",
                             f"{bad!r} was accepted as a src")

    def test_a_citation_needs_an_id_a_date_and_a_quote(self):
        full = {"id": "10.1016/x", "retrieved": "2026-08-26",
                "quote": "Global prevalence was 595 million cases in 2020."}
        self.assertEqual(check.src_kind(full), "cited")
        for drop in check.CITATION_FIELDS:
            partial = {k: v for k, v in full.items() if k != drop}
            self.assertEqual(check.src_kind(partial), "invalid",
                             f"a citation without {drop} was accepted")
        blank = dict(full, quote="   ")
        self.assertEqual(check.src_kind(blank), "invalid",
                         "an empty quote is not a quote")

    def test_the_error_message_names_what_is_missing(self):
        errs = []
        check.check_src({"id": "10.1/x", "retrieved": "2026-08-26"}, "here", errs)
        self.assertEqual(len(errs), 1)
        self.assertIn("quote", errs[0])
        self.assertIn("carry what it read", errs[0])

    def test_every_src_in_the_corpus_is_valid(self):
        """The walker covers the whole record, not a list of known paths.

        A hand-written list of field paths is the thing that goes stale — see
        the seven deferral notes in gaps.md #69 that nothing was checking.
        """
        bad = []
        for path in sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml"))):
            rec = check.load(path)

            def walk(node, where):
                if isinstance(node, dict):
                    if "src" in node and check.src_kind(node["src"]) == "invalid":
                        bad.append(f"{rec['slug']}: {where} src={node['src']!r}")
                    for k, v in node.items():
                        walk(v, f"{where}.{k}" if where else k)
                elif isinstance(node, list):
                    for v in node:
                        walk(v, where + "[]")
            walk(rec, "")
        self.assertEqual(bad, [])


class TestTiers(unittest.TestCase):
    """The denominator, and it was wrong on the public page.

    "0 of 1,582 sourced" reads as a backlog of 1,582 lookups. More than half of
    those are quantities no dataset holds — a citation cannot settle "the
    fraction of patients in whom the best available treatment works", because
    this register is where that number is defined. Reporting one total
    overstated the problem while hiding the specific one.
    """

    @classmethod
    def setUpClass(cls):
        cls.payload = [{**check.load(p)} for p in
                       sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
        cls.payload = [{**r, "derived": check.derive(r)} for r in cls.payload]
        cls.snap = check.snapshot(cls.payload, on_date="TEST")

    def test_burden_is_sourceable_and_the_syntheses_are_not(self):
        self.assertEqual(check.scalar_tier("burden.deaths"), "sourceable")
        self.assertEqual(check.scalar_tier("burden.prevalence"), "sourceable")
        # A dated historical event has a canonical reference that supports the
        # claim without being the claim.
        self.assertEqual(check.scalar_tier("moved[]"), "supportable")
        self.assertEqual(check.scalar_tier("toll.incidence"), "supportable")
        # The two axes the register exists to supply.
        self.assertEqual(check.scalar_tier("axes.efficacy"), "judged")
        self.assertEqual(check.scalar_tier("axes.access"), "judged")
        # A blocker's evidential status lives in `standing`, not in `src`.
        self.assertEqual(check.scalar_tier("blockers[]"), "judged")

    def test_the_tiers_partition_every_scalar(self):
        p = self.snap["provenance"]
        self.assertEqual(sum(t["total"] for t in p["by_tier"].values()),
                         p["scalars"],
                         "a scalar fell outside all three tiers")
        self.assertEqual(sum(t["cited"] for t in p["by_tier"].values()),
                         p["cited"])

    def test_nothing_lands_in_judged_by_accident(self):
        """`judged` is the default, so a typo'd path silently becomes a
        judgement. Pin the counts of the two named tiers instead."""
        p = self.snap["provenance"]["by_tier"]
        self.assertGreater(p["sourceable"]["total"], 150,
                           "burden scalars stopped being counted as sourceable — "
                           "check SOURCEABLE against the real field paths")
        self.assertGreater(p["supportable"]["total"], 300)

    def test_cited_and_verified_agree(self):
        p = self.snap["provenance"]
        self.assertEqual(p["cited"], p["verified"],
                         "`verified` is kept as an alias so stored snapshots "
                         "stay readable; it must not drift from `cited`")


class TestMovedSourcing(unittest.TestCase):
    """`moved:` is the register's only time series, so its citations get a test.

    The sourcing tool writes into hand-formatted YAML textually rather than by
    round-tripping a parse, because re-emitting these files would reflow every
    block scalar in them. That is the right trade and it is also the one that
    can corrupt a record, so the result is checked here rather than trusted.
    """

    @classmethod
    def setUpClass(cls):
        cls.recs = [check.load(p) for p in
                    sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]

    def moved(self):
        for r in self.recs:
            for i, m in enumerate(r.get("moved") or []):
                yield r["slug"], i, m

    def test_every_written_citation_is_valid_and_quotes_something(self):
        cited = [(s, i, m) for s, i, m in self.moved()
                 if isinstance(m.get("src"), dict)]
        self.assertGreater(len(cited), 30,
                           "the sourcing pass appears to have been reverted")
        for slug, i, m in cited:
            self.assertEqual(check.src_kind(m["src"]), "cited",
                             f"{slug} moved[{i}] has a malformed citation")
            self.assertGreater(len(m["src"]["quote"].strip()), 20,
                               f"{slug} moved[{i}] quotes almost nothing")

    def test_a_citation_carries_a_resolvable_identifier(self):
        """The rule is RESOLVABLE, not PubMed.

        This test read `(PMID|doi|10.xxxx)` because the first sourcing pass went
        entirely through PubMed, and it promptly failed on the first citation
        that did not — an FDA approval page for `pancreatic-cancer`, which is
        the primary source for a regulatory action and has no DOI. **A source
        of record is not always a journal article**, and the register will
        accumulate more of them: WHO position papers, eradication declarations,
        national screening programmes, GBD releases.

        What still must hold is that an identifier resolves somewhere a reader
        can check. `recall` is honest; an unresolvable id is not.
        """
        for slug, i, m in self.moved():
            src = m.get("src")
            if not isinstance(src, dict):
                continue
            self.assertRegex(
                src["id"], r"(PMID:\d+|doi:\S+|10\.\d{4,}|https?://\S+)",
                f"{slug} moved[{i}] id does not resolve anywhere: {src['id']!r}")

    def test_writing_a_citation_did_not_disturb_the_entry(self):
        """The textual insert must not have eaten a neighbouring field.

        Every moved entry still needs its date, axis and why — if the writer
        mis-counted entry boundaries it would clobber one of them, and the
        record would still parse.
        """
        for slug, i, m in self.moved():
            for field in ("date", "axis", "why"):
                self.assertIn(field, m,
                              f"{slug} moved[{i}] lost its {field}")
            self.assertGreater(len(str(m["why"]).strip()), 40,
                               f"{slug} moved[{i}] why is suspiciously short")

    def test_the_ledger_and_the_records_agree(self):
        """A pmid recorded as accepted should be the pmid in the record.

        The ledger is the review artifact; the record is the published claim.
        If they drift, the review was of something other than what shipped.
        """
        import json
        path = os.path.join(HERE, "moved-sources.json")
        if not os.path.exists(path):
            self.skipTest("no ledger")
        led = json.load(open(path, encoding="utf-8"))["entries"]
        drift = []
        for r in self.recs:
            for m in (r.get("moved") or []):
                key = f"{r['slug']}|{m['date']}|{m['axis']}"
                acc = (led.get(key) or {}).get("accept")
                src = m.get("src")
                if acc and isinstance(src, dict) and f"PMID:{acc}" not in src["id"]:
                    drift.append(f"{key}: ledger {acc}, record {src['id']}")
        self.assertEqual(drift, [])


class TestSourcingParser(unittest.TestCase):
    """The PubMed parser, pinned offline, because it was wrong once.

    `source_moved.py` iterated `ArticleId` across the whole `<PubmedArticle>`,
    which contains the paper's own `<ReferenceList>`. The last DOI it found was
    therefore whatever the paper happened to cite last, and it wrote that into
    a record as the article's identifier.

    **THE RESULT WAS A CITATION WRONG IN THE MOST CONVINCING POSSIBLE WAY.** The
    `covid-19` vaccine entry ended up carrying `PMID:33301246` — the BNT162b2
    (Pfizer) trial — beside `doi:10.1056/NEJMoa2027906`, which resolves to the
    mRNA-1273 (Moderna) trial. Two real NEJM papers, same journal, same year,
    same subject, different vaccine. Nothing about it looked wrong.

    It is worth being precise about what failed. The rule "a citation must carry
    what it read" held — the quote was genuine. What slipped was the identifier
    beside it, and no amount of care would have caught that by reading. **The
    discipline has to be mechanical, and this test is the mechanism.**
    """

    FIXTURE = """<?xml version="1.0"?>
    <PubmedArticleSet><PubmedArticle>
      <MedlineCitation>
        <PMID>33301246</PMID>
        <Article>
          <Journal><ISOAbbreviation>N Engl J Med</ISOAbbreviation>
            <JournalIssue><PubDate><Year>2020</Year></PubDate></JournalIssue></Journal>
          <ArticleTitle>Safety and Efficacy of the BNT162b2 mRNA Covid-19 Vaccine.</ArticleTitle>
          <Abstract><AbstractText Label="CONCLUSIONS">A two-dose regimen conferred
            95% protection against Covid-19.</AbstractText></Abstract>
        </Article>
      </MedlineCitation>
      <PubmedData>
        <ArticleIdList>
          <ArticleId IdType="pubmed">33301246</ArticleId>
          <ArticleId IdType="doi">10.1056/NEJMoa2034577</ArticleId>
        </ArticleIdList>
        <ReferenceList>
          <Reference><ArticleIdList>
            <ArticleId IdType="doi">10.1056/NEJMoa2027906</ArticleId>
          </ArticleIdList></Reference>
        </ReferenceList>
      </PubmedData>
    </PubmedArticle></PubmedArticleSet>"""

    def parsed(self):
        import source_moved
        return source_moved.parse_articles(self.FIXTURE)["33301246"]

    def test_the_doi_is_the_articles_own_not_one_it_cites(self):
        rec = self.parsed()
        self.assertEqual(rec["doi"], "10.1056/NEJMoa2034577")
        self.assertNotEqual(rec["doi"], "10.1056/NEJMoa2027906",
                            "the parser took a DOI out of the reference list again")

    def test_title_journal_and_year_come_from_the_article(self):
        rec = self.parsed()
        self.assertIn("BNT162b2", rec["title"])
        self.assertEqual(rec["journal"], "N Engl J Med")
        self.assertEqual(rec["year"], "2020")

    def test_the_quote_prefers_the_conclusion_and_is_verbatim(self):
        import source_moved
        q = source_moved.pick_quote(self.parsed())
        self.assertIn("95% protection", q)
        # verbatim means verbatim: the quote must appear in the source text with
        # whitespace normalised, and nowhere else does the tool get to write one
        flat = " ".join(self.FIXTURE.split())
        self.assertIn(" ".join(q.split()), flat,
                      "the quote is not a span of the retrieved text")

    def test_no_abstract_falls_back_to_the_title(self):
        """Most pre-1975 papers have no abstract, and that is where the oldest
        `moved:` entries point. A title is retrieved text; it is copied, not
        composed."""
        import source_moved
        self.assertEqual(source_moved.pick_quote({"sections": [], "title": "T."}), "T.")


class TestSurvival(unittest.TestCase):
    """"You get it, and then what?" — the only axis that means one thing everywhere.

    It exists because `efficacy` does not. That field reads 0.55 for
    head-and-neck cancer (alive and disease-free at five years) and 0.85 for
    asthma (good symptom control), and `reach = efficacy x access` multiplies
    across them as though they were the same kind of number. **Survival is
    comparable between records and `efficacy` is not.**
    """

    @classmethod
    def setUpClass(cls):
        cls.recs = [check.load(p) for p in
                    sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
        cls.rated = [r for r in cls.recs if check.survival_band(r) != "n/a"]

    def test_the_bands_are_read_off_treated_survival(self):
        for r in self.rated:
            v = r["survival"]["treated"]["value"]
            band = check.survival_band(r)
            if v < 0.10:
                self.assertEqual(band, "terminal", r["slug"])
            elif v < 0.50:
                self.assertEqual(band, "a chance", r["slug"])
            else:
                self.assertEqual(band, "good chance", r["slug"])

    def test_unrated_is_n_a_and_n_a_is_not_terminal(self):
        """Thirty-five records have no deaths at all. A mortality ladder is
        silent about them by construction, and silence must not read as death —
        same rule as `predictive: n/a` and as `unrated is never unsolved`."""
        for r in self.recs:
            if "survival" not in r:
                self.assertEqual(check.survival_band(r), "n/a", r["slug"])
                self.assertFalse(check.was_uniformly_fatal(r), r["slug"])
                self.assertFalse(check.no_longer_terminal(r), r["slug"])
        hl = next(r for r in self.recs if r["slug"] == "hearing-loss")
        self.assertEqual(check.survival_band(hl), "n/a",
                         "a record with no deaths must not acquire a survival band")

    def test_the_progress_claim_is_derived_not_asserted(self):
        """`no_longer_terminal` is the countable form of "X, Y and Z all used to
        kill everybody, and that list is shrinking"."""
        for r in self.rated:
            u = r["survival"]["untreated"]["value"]
            t = r["survival"]["treated"]["value"]
            self.assertEqual(check.no_longer_terminal(r), u < 0.10 and t >= 0.10,
                             r["slug"])
        # the two controls: terminal then, terminal now
        for slug in ("rabies", "huntington"):
            r = next(x for x in self.recs if x["slug"] == slug)
            self.assertTrue(check.was_uniformly_fatal(r), slug)
            self.assertFalse(check.no_longer_terminal(r), slug)

    def test_a_horizon_is_required_because_it_is_part_of_the_claim(self):
        """Rabies kills within a month; Huntington's takes twenty years and is
        equally certain. Five-year survival would call one terminal and the
        other excellent."""
        for r in self.rated:
            self.assertTrue(str(r["survival"].get("horizon") or "").strip(),
                            f"{r['slug']} has survival with no horizon")
        hu = next(r for r in self.recs if r["slug"] == "huntington")
        self.assertIn("20", str(hu["survival"]["horizon"]))
        self.assertEqual(check.survival_band(hu), "terminal",
                         "a disease that kills everybody slowly is still terminal")

    def test_survival_is_sourceable_not_judged(self):
        """Registries publish these. Unlike `efficacy`, which is a judgement,
        survival is a number somebody measured — so it belongs in the tier the
        sourcing tool can actually work on."""
        self.assertEqual(check.scalar_tier("survival.treated"), "sourceable")
        self.assertEqual(check.scalar_tier("survival.untreated"), "sourceable")

    def test_survival_says_nothing_about_what_survival_costs(self):
        """The axis answers "do I live" and not "as what". `head-neck-cancer` is
        a `good chance` record with a `catastrophic` toll, and a view that showed
        survival alone would report it as an unqualified success."""
        hn = next(r for r in self.recs if r["slug"] == "head-neck-cancer")
        self.assertEqual(check.survival_band(hn), "good chance")
        self.assertEqual(hn["toll"]["severity"], "catastrophic")


class TestMondoIdentifiers(unittest.TestCase):
    """Every `mondo:` id must exist in the committed ontology snapshot.

    WHY THIS EXISTS. On 2026-08-28 the `idiopathic-pulmonary-fibrosis` record was
    written with `MONDO:0008345`, which **does not exist**. It was not a typo of a
    real id and not a merged term — it was recalled rather than looked up, in a
    record written minutes after a search that had returned the correct
    `MONDO:0800504` on screen.

    Nothing caught it. `check.py` validated the format; `mondo-terms.json` held
    three terms because nobody had run `mondo_sync.py` across the corpus. **The
    guard existed and was empty.**

    An identifier that resolves to nothing is recoverable. An identifier that
    resolves to the WRONG term is not, and the register has already had one of
    those — `MONDO:0007403` is *inherited* Creutzfeldt-Jakob disease and was the
    exact-label match for "Creutzfeldt-Jakob disease". Same class of error, same
    afternoon, caught only because that one was checked.

    The snapshot is refreshed by `python3 mondo_sync.py`. A new record's id will
    fail here until it is, which is the correct direction to fail in.
    """

    @classmethod
    def setUpClass(cls):
        import json
        path = os.path.join(HERE, "mondo-terms.json")
        # the file is {checked, release, terms:{id:{...}}} — read the terms, not
        # the wrapper. The first version of this test read the wrapper, found
        # three keys, and would have "passed" the coverage check at 3 records.
        blob = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
        cls.snapshot = blob.get("terms", {}) if isinstance(blob, dict) else {}
        cls.recs = [check.load(p) for p in
                    sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]

    def test_the_snapshot_actually_covers_the_corpus(self):
        """The guard was empty for a hundred records. Fail if it is again."""
        resolved = [r for r in self.recs if r.get("mondo", "unresolved") != "unresolved"]
        self.assertGreater(len(self.snapshot), 0.9 * len(resolved),
                           "mondo-terms.json does not cover the corpus — "
                           "run `python3 mondo_sync.py`")

    def test_every_mondo_id_exists_in_the_ontology(self):
        unknown = []
        for r in self.recs:
            mid = r.get("mondo", "unresolved")
            if mid != "unresolved" and mid not in self.snapshot:
                unknown.append(f"{r['slug']}: {mid}")
        self.assertEqual(unknown, [], (
            "these ids are not in the Mondo snapshot — either fabricated, or the "
            "snapshot is stale (run `python3 mondo_sync.py`):\n  "
            + "\n  ".join(unknown)))

    def test_the_id_matches_the_record_it_is_used_for(self):
        """A plausible id for the wrong population is worse than none.

        `prion-disease` is the worked example: the exact-label match for
        "Creutzfeldt-Jakob disease" was `MONDO:0007403`, which means the
        *inherited* form — roughly a tenth of that record.
        """
        for slug, must in [("prion-disease", "prion"),
                           ("idiopathic-pulmonary-fibrosis", "idiopathic pulmonary fibrosis"),
                           ("mesothelioma", "mesothelioma")]:
            r = next((x for x in self.recs if x["slug"] == slug), None)
            if r is None:
                continue
            label = (self.snapshot.get(r["mondo"]) or {})
            label = label.get("label", "") if isinstance(label, dict) else str(label)
            self.assertIn(must, label.lower(),
                          f"{slug} points at {r['mondo']} — {label!r}")


class TestIcdCoverage(unittest.TestCase):
    """`icd_coverage.py` must stay honest about which ICD flavour it counts.

    WHY THIS EXISTS. The report was written to answer *should the register adopt
    WHO ICD*, and the tempting answer was yes — 89 of 100 records already carry
    an ICD cross-reference. That number is true and nearly useless: it counts
    `ICD9` (retired from mortality coding around 1999), `ICD10CM` (one country's
    billing modification) and `icd11.foundation` (an entity id, not a code)
    alongside the single flavour that joins to the WHO Mortality Database.

    The honest number is **ICD10WHO on records that carry a deaths figure**, and
    it was 15 of 73. This pins the distinction so a later refactor cannot quietly
    collapse the flavours back into one count — which is the same failure as a
    Sperrwerk check reporting `ok` when it could not run.

    See gaps.md #217.
    """

    @classmethod
    def setUpClass(cls):
        import icd_coverage
        cls.mod = icd_coverage
        cls.terms, cls.recs = icd_coverage.load()
        cls.rows = [icd_coverage.row(r, cls.terms) for r in cls.recs]

    def test_the_mortality_flavour_is_counted_separately(self):
        """ICD10WHO must never be totalled with the others."""
        self.assertEqual(self.mod.FLAVOURS[0], "ICD10WHO",
                         "the mortality standard leads the list on purpose")
        for f in ("ICD9", "ICD10CM", "icd11.foundation"):
            self.assertIn(f, self.mod.FLAVOURS,
                          "the other flavours must stay visible and separate — "
                          "collapsing them hides that coverage is the wrong kind")

    def test_any_icd_xref_overstates_the_mortality_key(self):
        """The headline that must not be quoted, against the one that may be."""
        any_icd = [r for r in self.rows if any(r["codes"].values())]
        who = [r for r in self.rows if r["codes"]["ICD10WHO"]]
        self.assertGreater(len(any_icd), 2 * len(who), (
            "if these ever converge the report's framing needs revisiting; "
            f"any-ICD={len(any_icd)} ICD10WHO={len(who)}"))

    def test_a_code_being_present_does_not_make_the_number_sourceable(self):
        """heart-failure is the demonstration: it HAS I50 and carries deaths: 0.

        ICD's mutually-exclusive underlying-cause rule reassigns those deaths, so
        the join key resolves and the figure still is not there. If this record
        ever gains a deaths figure the worked example in gaps.md #217 is stale.
        """
        hf = next((r for r in self.rows if r["slug"] == "heart-failure"), None)
        if hf is None:
            self.skipTest("heart-failure record not present")
        self.assertTrue(hf["codes"]["ICD10WHO"],
                        "heart-failure lost its ICD10WHO xref — #217 needs a new example")
        self.assertFalse(hf["has_deaths"],
                         "heart-failure now carries deaths — revisit gaps.md #217")

    def test_the_predicted_mismatches_are_real_records(self):
        """A prediction list that names nothing checks nothing."""
        slugs = {r["slug"] for r in self.rows}
        missing = sorted(s for s in self.mod.PREDICTED_MISMATCH if s not in slugs)
        self.assertEqual(missing, [], f"PREDICTED_MISMATCH names non-records: {missing}")


class TestSurvivalOutcome(unittest.TestCase):
    """`survival` and `outcome` must stay two questions.

    WHY THIS EXISTS. gaps.md #216, forced by `als` on the day the axis was
    added. Two records sit in the same band and mean opposite things —
    pancreatic cancer's 13% are cured, ALS's 20% are still dying — and a view
    ranked on the band alone puts ALS above pancreatic cancer, which is exactly
    wrong about which one anybody survives.

    The fix added no field: `outcome` is read off `axes.intervention`, which the
    register already had. These tests exist so a later refactor cannot collapse
    the pair back into one number, and so the worked examples in SCHEMA.md and
    on the dashboard cannot go stale without failing.
    """

    @classmethod
    def setUpClass(cls):
        cls.recs = [check.load(p) for p in
                    sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
        cls.recs = [r for r in cls.recs if check.status(r) == "active"]
        cls.rated = [r for r in cls.recs if check.survival_band(r) != "n/a"]

    def test_the_worked_example_still_works(self):
        """0.55 and 0.55, and only the qualifier separates them."""
        by = {r["slug"]: r for r in self.recs}
        for slug, outcome in [("head-neck-cancer", "cured"),
                              ("heart-failure", "delayed")]:
            r = by.get(slug)
            if r is None:
                self.skipTest(f"{slug} not present")
            self.assertEqual(check.survival_band(r), "good chance",
                             f"{slug} left the band the example depends on")
            self.assertEqual(check.survival_outcome(r), outcome)
        self.assertEqual(by["head-neck-cancer"]["survival"]["treated"]["value"],
                         by["heart-failure"]["survival"]["treated"]["value"],
                         "the example needs both records on the SAME number")

    def test_the_inversion_that_forced_the_derivation(self):
        """ALS survives more than pancreatic cancer and is the worse outcome."""
        by = {r["slug"]: r for r in self.recs}
        als, panc = by.get("als"), by.get("pancreatic-cancer")
        if not als or not panc:
            self.skipTest("als/pancreatic-cancer not present")
        self.assertGreater(als["survival"]["treated"]["value"],
                           panc["survival"]["treated"]["value"])
        self.assertEqual(check.survival_band(als), check.survival_band(panc),
                         "same band is the premise of gaps.md #216")
        self.assertEqual(check.survival_outcome(als), "delayed")
        self.assertEqual(check.survival_outcome(panc), "cured")

    def test_outcome_never_disagrees_with_the_ladder(self):
        """`curative`/`suppressive` decide alone; `course` decides the rest."""
        want = {"curative": "cured", "suppressive": "held"}
        for r in self.rated:
            rung = r["axes"]["intervention"]
            if rung in want:
                self.assertEqual(check.survival_outcome(r), want[rung], r["slug"])
                self.assertIsNone(
                    check.survival_course(r),
                    f"{r['slug']}: declares `course` on a {rung} record, where it "
                    f"is never read — a declaration nothing consults will rot")
            else:
                self.assertEqual(
                    check.survival_outcome(r),
                    "recovered" if check.survival_course(r) == "acute" else "delayed",
                    r["slug"])

    def test_an_acute_disease_is_never_still_dying(self):
        """THE FALSE SENTENCE THAT FORCED `course`.

        The first version printed, for measles: *"99% at 30 days from rash onset
        — alive and still dying of it."* Measles is `symptomatic` because there
        is no antiviral; its survivors recovered. Six records said the same
        false thing, all acute infections.
        """
        for r in self.rated:
            if check.survival_course(r) == "acute":
                self.assertNotIn("still dying", check.survival_sentence(r), r["slug"])
        acute = {r["slug"] for r in self.rated
                 if check.survival_course(r) == "acute"}
        self.assertIn("measles", acute, "the record that forced the field")

    def test_a_misspelled_course_is_an_error_not_a_default(self):
        """Silently defaulting would restore the exact sentence it prevents."""
        import copy
        rec = copy.deepcopy(next(r for r in self.recs if r.get("survival")))
        rec["survival"]["course"] = "accute"
        errs, _ = check.check(rec, "x.yaml")
        self.assertTrue(any("course" in e for e in errs), errs)

    def test_a_fraction_below_one_never_prints_as_100_percent(self):
        """`asthma` is 0.997 and the missing 0.3% is 455,000 people a year."""
        for r in self.rated:
            v = r["survival"]["treated"]["value"]
            if v < 1:
                self.assertNotIn("100%", check.survival_sentence(r), r["slug"])

    def test_the_two_readings_are_independent(self):
        """Gating outcome on the band would lose the distinction it draws.

        A curative disease with 13% survival still cures 13% of people — a scale
        statement, not a kind statement. If a `terminal` or `a chance` record can
        never read `cured`, someone has reintroduced the gate.
        """
        outcomes = {check.survival_outcome(r) for r in self.rated
                    if check.survival_band(r) != "good chance"}
        self.assertIn("cured", outcomes,
                      "no low-survival record reads `cured` — the band and the "
                      "outcome have been coupled again (gaps.md #216)")

    def test_nobody_survives_reads_as_such(self):
        """"0% — alive and still dying of it" was the first version's output."""
        for r in self.rated:
            s = check.survival_sentence(r)
            if r["survival"]["treated"]["value"] < 0.005:
                self.assertIn("nobody survives", s, r["slug"])
            else:
                self.assertNotIn("nobody survives", s, r["slug"])
            self.assertTrue(s, r["slug"])

    def test_gain_is_a_difference_and_can_be_zero(self):
        by = {r["slug"]: r for r in self.recs}
        alz = by.get("alzheimers")
        if alz:
            self.assertEqual(check.survival_gain(alz), 0.0, (
                "alzheimers had identical treated and untreated survival — if a "
                "treatment now extends life the record should say so explicitly"))
        for r in self.rated:
            g = check.survival_gain(r)
            self.assertIsNotNone(g, r["slug"])
            self.assertGreaterEqual(g, 0.0,
                                    f"{r['slug']}: treatment made survival worse")

    def test_n_a_is_never_terminal(self):
        """The largest disability burdens here are invisible to this axis."""
        for r in self.recs:
            if not r.get("survival"):
                self.assertEqual(check.survival_band(r), "n/a", r["slug"])
                self.assertEqual(check.survival_outcome(r), "n/a", r["slug"])
                self.assertEqual(check.survival_sentence(r), "", r["slug"])


class TestMondoSubEntities(unittest.TestCase):
    """`mondo_sync.diff_subentities` — the check, and the ways it went wrong.

    WHY THIS EXISTS. Writing four fungal records in a day turned up the same
    hole three times — chronic pulmonary aspergillosis, coccidioidal meningitis
    and *Candida auris* have no Mondo term — and `acute bronchitis` showed the
    same thing outside mycology. All four were found by a person typing into a
    search box, so it became a check (gaps.md #227).

    **The first version of the check was worse than useless in two specific
    ways, and both are pinned below.** It proposed `MONDO:1017104` — *acute
    bronchitis, NON-HUMAN ANIMAL* — as the `fix` for the human bronchitis
    record, which is the `duodenal ulcer` failure with a veterinary flavour. And
    it produced 180 alias findings, roughly half junk, because Mondo's exact
    search matches synonyms as well as labels: `motor neurone disease` came back
    as *frontotemporal dementia and/or ALS 1*.
    """

    @classmethod
    def setUpClass(cls):
        import mondo_sync
        cls.ms = mondo_sync

    def test_veterinary_terms_can_never_be_proposed(self):
        """A human disease register must never cite a non-human-animal term."""
        hits = [{"id": "MONDO:1017104", "label": "acute bronchitis, non-human animal"},
                {"id": "MONDO:0003781", "label": "bronchitis"}]
        kept, ok = self.ms._lookup("x", {"search::x": {"response": {"docs": [
            {"obo_id": h["id"], "label": h["label"]} for h in hits]}}})
        self.assertTrue(ok)
        self.assertEqual([h["id"] for h in kept], ["MONDO:0003781"],
                         "a `non-human animal` term survived the filter")

    def test_a_lookup_that_could_not_run_is_never_a_null(self):
        """Offline must not turn a cache miss into 'Mondo does not have this'."""
        self.ms.rm.OFFLINE = True
        try:
            hits, ok = self.ms._lookup("nothing-was-ever-cached-for-this", {})
        finally:
            self.ms.rm.OFFLINE = False
        self.assertEqual(hits, [])
        self.assertFalse(ok, "an uncached lookup reported itself as checked")

    def test_only_a_matching_LABEL_counts_as_an_identification(self):
        """The tightening that took alias findings from 180 to 58.

        A term matching on a related synonym is not an identification of our
        alias, and treating it as one produced confident nonsense.
        """
        hits = [{"id": "MONDO:0007105",
                 "label": "frontotemporal dementia and/or amyotrophic lateral sclerosis 1"}]
        self.assertIsNone(self.ms._named(hits, "motor neurone disease", "MONDO:0004976"))
        hits = [{"id": "MONDO:0004784", "label": "allergic asthma"}]
        self.assertIsNotNone(self.ms._named(hits, "allergic asthma", "MONDO:0004979"))

    def test_british_and_american_spellings_compare_equal(self):
        """The register writes `anaemia`; Mondo writes `anemia`."""
        self.assertTrue(self.ms._same("pernicious anaemia", "pernicious anemia"))
        self.assertTrue(self.ms._same("subarachnoid haemorrhage", "subarachnoid hemorrhage"))
        self.assertTrue(self.ms._same("ischaemic stroke", "ischemic stroke"))
        self.assertFalse(self.ms._same("anaemia", "leukaemia"))

    def test_rm_norm_is_left_strict(self):
        """The ligature folding lives in mondo_sync, NOT in resolve_mondo.

        `rm.norm` decides exact matches when an identifier is first resolved.
        Loosening it there would let a near-miss through at the one moment the
        register is choosing a permanent join key.
        """
        self.assertNotEqual(self.ms.rm.norm("anaemia"), self.ms.rm.norm("anemia"))

    def test_a_precision_finding_is_never_an_auto_fix(self):
        """`--apply` writes only Mondo's own named replacement for a dead term.

        A narrower term for our entity cannot be told from a sibling sharing our
        words: `pleomorphic adenoma of the salivary gland` returns *carcinoma ex
        pleomorphic adenoma*, a malignant transformation and a different disease.
        """
        import inspect
        src = inspect.getsource(self.ms.diff_subentities)
        self.assertNotIn('"fix"', src,
                         "diff_subentities emits a `fix` — --apply would act on an "
                         "inference rather than on Mondo's own statement")

    def test_an_alias_with_its_own_term_is_not_reported_as_a_defect(self):
        """gaps.md #229 — the framing error this check shipped with.

        `also` is *"synonyms people actually search for"* (SCHEMA.md), which
        `resolve_mondo` states "may be broader or narrower than the entity", and
        whose only consumer in this codebase is free-text search in query.js.
        Somebody typing `pernicious anaemia` SHOULD reach the `anaemia` record.
        The first version called all 58 of these defects.
        """
        import inspect
        src = inspect.getsource(self.ms.diff_subentities)
        alias = src[src.index("# 2. ALIAS"):src.index("# 3. STRATA")]
        self.assertIn('"level": "info"', alias,
                      "an alias finding is informational — `also` is a search-alias "
                      "field and having its own Mondo term is the expected state")
        self.assertNotIn('"level": "warn"', alias)
        for bad in ("DIFFERENT Mondo entity", "read as equivalences", "distinct thing as an alias"):
            self.assertNotIn(bad, alias, f"defect framing survived: {bad!r}")


class TestBurdenGaps(unittest.TestCase):
    """`knowledge_gap` / `delivery_gap` — capability weighted by how many people get it.

    WHY THIS EXISTS. The register could already say *rabies is horrific and
    nothing treats it* and *heart disease kills nine million a year*, and had no
    way to say which one is a better place to work. The intuition it was built
    to test — *should we work on the rare terrible ones or the common ones* —
    turns out to be a false choice: **the largest knowledge gaps in the register
    are inside the common diseases.** `stroke` alone is ~3.3M against ~91,000
    attributed deaths across every record where `efficacy` is zero.

    These tests pin the two guards, because the guards are the entire design.
    A gap that returns 0 where it should return None would rank the diseases
    medicine is most helpless against *last*.
    """

    @classmethod
    def setUpClass(cls):
        cls.recs = {r["slug"]: r for r in
                    (check.load(p) for p in
                     sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml"))))}

    def test_a_record_with_no_deaths_has_no_gap(self):
        """None, never zero — and this is not a corner case.

        Four of the five diseases where medicine is most completely helpless —
        `huntington`, `me-cfs`, `msmds`, `heds` — have no attributed deaths at
        all. Engpass already recorded the rule this protects: **rank by records,
        not by burden**, because a mortality-weighted ranking makes the clearest
        scientific gap in the corpus invisible.
        """
        for slug in ("huntington", "me-cfs", "msmds"):
            r = self.recs[slug]
            self.assertIsNone(check.knowledge_gap(r), f"{slug} has no deaths")
            self.assertIsNone(check.delivery_gap(r), f"{slug} has no deaths")

    def test_a_record_that_declares_zero_deaths_gets_a_computed_zero(self):
        """`heds` declares `deaths: 0.0`, and the honest answer is 0, not None.

        THE TWO MEAN DIFFERENT THINGS AND BOTH ARE INVISIBLE IN A RANKING.
        `huntington` has no `deaths` key — nobody has attributed a figure, so
        the gap **cannot be computed**. `heds` has one and it is zero — hEDS is
        not fatal, so there is **no death for either kind of work to claim**.
        The same distinction the snapshot's `zero_gain` guard draws for
        `survival_gain`: a zero that means *nothing was at stake* is not a zero
        that means *medicine bought nothing*.

        Between them these two rows say what this metric cannot do: **it is
        mortality-shaped, and the diseases medicine is most helpless against do
        not kill people.** Rank by records as well, or lose them.
        """
        self.assertEqual(check.knowledge_gap(self.recs["heds"]), 0.0)
        self.assertEqual(check.delivery_gap(self.recs["heds"]), 0.0)

    def test_a_preventable_record_has_no_gap(self):
        """gaps.md #109 as arithmetic.

        `efficacy` and `access` describe only the treatment. For `rabies` both
        are 0.0 — there is no course-altering treatment — so the arithmetic
        would read a 59,000-death *knowledge* gap for a disease whose vaccine
        works essentially always and whose deaths are an access failure.
        `delivery()` withholds a band from the same five for the same reason.
        """
        prev = [s for s, r in self.recs.items() if check.capability(r) == "preventable"]
        self.assertIn("rabies", prev)
        for slug in prev:
            self.assertIsNone(check.knowledge_gap(self.recs[slug]), slug)
            self.assertIsNone(check.delivery_gap(self.recs[slug]), slug)

    def test_the_two_gaps_never_exceed_the_burden(self):
        """They partition the deaths; together they cannot exceed them.

        knowledge + delivery = deaths x (1 - efficacy x access), which is
        deaths x (1 - reach). The remainder is the burden that current medicine,
        fully delivered, does claim.
        """
        for slug, r in self.recs.items():
            k = check.knowledge_gap(r)
            if k is None:
                continue
            d = check.delivery_gap(r)
            deaths = r["burden"]["deaths"]["value"]
            self.assertLessEqual(k + d, deaths + 1e-6, slug)
            self.assertAlmostEqual(k + d, deaths * (1 - check.reach(r)), places=3,
                                   msg=f"{slug}: the two gaps must partition the burden")

    def test_the_finding_the_field_was_built_to_state(self):
        """The common diseases hold the bigger knowledge gaps — assert it, do not claim it.

        If a later re-rating overturns this, the test should fail and the
        finding should be rewritten. That is the point of pinning it.
        """
        gaps = {s: check.knowledge_gap(r) for s, r in self.recs.items()
                if check.knowledge_gap(r)}
        top = max(gaps, key=gaps.get)
        self.assertEqual(top, "stroke")
        helpless = sum(
            (r["burden"].get("deaths") or {}).get("value") or 0
            for r in self.recs.values() if r["axes"]["efficacy"]["value"] == 0)
        self.assertGreater(gaps[top], 10 * helpless,
                           "the largest single knowledge gap should dwarf the total "
                           "attributed deaths of every record where nothing works")

    def test_the_yld_gaps_are_a_parallel_reading_and_never_mixed(self):
        """Deaths and YLDs are different units. Adding them is meaningless.

        WHY THIS EXISTS. `burden.ylds` sat in the schema on four records,
        referenced once in a path list and read by nothing, while four
        consecutive records — `glaucoma`, `retinopathy-of-prematurity`,
        `refractive-error`, `migraine` — were written with a comment explaining
        that the mortality axes could not see them. Roughly two billion people
        and no attributed deaths between them.

        The fix is a PARALLEL pair, not a fallback. A single field that used
        deaths where available and YLDs otherwise would produce a column mixing
        people who died with years of disability, ranked against each other.
        """
        for r in self.recs.values():
            k, ky = check.knowledge_gap(r), check.knowledge_yld(r)
            b = r.get("burden") or {}
            # each is present exactly when its own burden metric is
            self.assertEqual(k is not None,
                             bool(b.get("deaths")) and check.capability(r) != "preventable",
                             f"{r['slug']}: deaths gap disagrees with burden.deaths")
            self.assertEqual(ky is not None,
                             bool(b.get("ylds")) and check.capability(r) != "preventable",
                             f"{r['slug']}: yld gap disagrees with burden.ylds")

    def test_the_yld_pair_finds_records_the_deaths_pair_cannot(self):
        """The whole point: records with disability burden and no mortality."""
        # TWO WAYS THE DEATHS PAIR FAILS THESE RECORDS, AND THE SECOND IS WORSE.
        # `low-back-pain` has no `deaths` at all, so the deaths gap is None and
        # it drops out. `anaemia` and `osteoarthritis` declare `deaths: 0.0`, so
        # the deaths gap is a computed **zero** — they do not drop out, they
        # rank LAST, while carrying 50 and 22 million years of disability a year.
        # A ranking that puts the largest disability burdens on earth at the
        # bottom is worse than one that omits them, because it looks complete.
        hidden = [s for s, r in self.recs.items()
                  if check.knowledge_yld(r) and not check.knowledge_gap(r)]
        self.assertGreaterEqual(len(hidden), 3,
            "the YLD pair exists for records the deaths pair drops or zeroes; "
            f"it currently rescues {hidden}")
        self.assertIn("low-back-pain", hidden,
            "the largest cause of years lived with disability on earth must be "
            "visible to at least one of the two gap metrics")
        self.assertIsNone(check.knowledge_gap(self.recs["low-back-pain"]),
                          "low-back-pain has no deaths figure — the deaths gap "
                          "must report None rather than invent a zero")

    def test_the_yld_gaps_partition_the_disability_burden(self):
        """Same invariant as the deaths pair: together they cannot exceed it."""
        for slug, r in self.recs.items():
            ky = check.knowledge_yld(r)
            if ky is None:
                continue
            dy = check.delivery_yld(r)
            ylds = r["burden"]["ylds"]["value"]
            self.assertAlmostEqual(ky + dy, ylds * (1 - check.reach(r)), places=2,
                                   msg=f"{slug}: the YLD gaps must partition the burden")

    def test_burden_scalars_are_shape_checked(self):
        """`burden.ylds` went unvalidated for as long as it went unread.

        A field nothing consumes is a field nothing checks, which is how a
        malformed value would have survived indefinitely. This pins that burden
        scalars are validated the way `axes` scalars always were.
        """
        import inspect
        src = inspect.getsource(check.check)
        self.assertIn('for key in ("deaths", "prevalence", "incidence", "ylds")', src,
                      "burden scalars must be shape-checked")
        for r in self.recs.values():
            for key in ("deaths", "prevalence", "incidence", "ylds"):
                s = (r.get("burden") or {}).get(key)
                if s is None:
                    continue
                self.assertIsInstance(s, dict, f"{r['slug']}: burden.{key}")
                for f in ("value", "units", "src"):
                    self.assertIn(f, s, f"{r['slug']}: burden.{key} missing {f}")

    def test_the_snapshot_carries_its_own_denominator(self):
        """A total whose denominator is invisible is a number that gets quoted wrongly."""
        snap = check.snapshot([{**r, "derived": check.derive(r)}
                               for r in self.recs.values()])["gaps"]
        self.assertLess(snap["rated"], len(self.recs),
                        "not every record can carry a gap; the count must say so")
        self.assertGreater(snap["delivery"], snap["knowledge"],
                           "the register's headline asymmetry, restated in lives")


class TestBuckets(unittest.TestCase):
    """The register read as a small set of named states — `buckets.yaml`.

    WHY THIS EXISTS. Nine charts do not add up to a statement, and the standfirst
    now says out loud that there is no single score. Buckets are the other half
    of that: not one number, but a handful of states a person can hold in their
    head, counted the same way every year.

    Two properties have to hold or the whole idea fails quietly. **Axis A must
    partition** — if a record lands in two buckets or none, a percentage of the
    register is meaningless. And **the definitions must be versioned** — a record
    moving between buckets is progress, but a bucket's *definition* moving makes
    next year's count answer a different question while wearing the same label.
    """

    @classmethod
    def setUpClass(cls):
        cls.recs = [check.load(p) for p in
                    sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
        cls.spec = check.load(os.path.join(HERE, "buckets.yaml"))

    def test_axis_a_is_a_partition(self):
        """Every record lands in exactly one bucket, and no bucket is a mistake."""
        got = [check.bucket(r) for r in self.recs]
        self.assertEqual(len(got), len(self.recs))
        unknown = set(got) - set(check.BUCKETS_A)
        self.assertEqual(unknown, set(), f"bucket() produced unnamed buckets: {unknown}")

    def test_no_record_needs_a_residual_bucket(self):
        """THE REASON THE AXIS IS NOT BUILT ON SURVIVAL.

        `survival` cannot rate 37 records — a mortality ladder is silent about
        hearing loss, cataract, osteoarthritis and low back pain, which are among
        the largest burdens here. An axis spined on death needs an "unrated"
        bucket holding a quarter of the register. This one does not.
        """
        unrated = [r for r in self.recs if check.survival_outcome(r) == "n/a"]
        self.assertGreater(len(unrated), 25, "expected many records survival cannot rate")
        for r in unrated:
            self.assertIn(check.bucket(r), check.BUCKETS_A,
                          f"{r['slug']}: placed by life impact, not by mortality")

    def test_the_yaml_and_the_code_name_the_same_buckets(self):
        """The definitions are the artefact; the rules are the implementation.

        They are separate on purpose — a rule expressed as an evaluable string in
        YAML would need an interpreter, and prose a reader can check is worth
        more than that. This test is what stops them drifting.
        """
        for axis, expect in (("A", check.BUCKETS_A), ("B", check.BUCKETS_B)):
            spec = next(a for a in self.spec["axes"] if a["id"] == axis)
            named = tuple(b["slug"] for b in spec["buckets"])
            self.assertEqual(named, tuple(expect),
                             f"axis {axis}: buckets.yaml and check.py disagree, "
                             f"including on ORDER — first match wins on axis A")

    def test_axis_b_is_tags_and_says_so(self):
        """B must never be summed. A record can carry several or none."""
        spec = next(a for a in self.spec["axes"] if a["id"] == "B")
        self.assertEqual(spec["kind"], "tags")
        self.assertEqual(next(a for a in self.spec["axes"] if a["id"] == "A")["kind"],
                         "partition")
        counts = [len(check.bucket_tags(r)) for r in self.recs]
        self.assertGreater(max(counts), 1, "no record carries multiple tags — "
                                           "then it would be a partition, not tags")
        self.assertEqual(min(counts), 0, "no record carries zero tags — "
                                         "B is not supposed to cover the register")

    def test_nobody_makes_it_excludes_diseases_with_no_answer(self):
        """`no-sponsor` means two different things and only one is this bucket.

        On a record where nothing works it is nobody funding the *research*; on a
        record with a real capability it is nobody producing the *cure*. Only the
        second is something a factory or a buyer could fix. Without the guard,
        `me-cfs` lands in a bucket about manufacturing.
        """
        by_slug = {r["slug"]: r for r in self.recs}
        for slug in ("me-cfs", "msmds"):
            self.assertIn("no-sponsor",
                          {b["kind"] for b in by_slug[slug]["blockers"]})
            self.assertNotIn("nobody-makes-it", check.bucket_tags(by_slug[slug]),
                             f"{slug} has no cure for anyone to fail to manufacture")
        # and the bucket is not empty of the cases it was built for
        got = {s for s, r in by_slug.items() if "nobody-makes-it" in check.bucket_tags(r)}
        for slug in ("snakebite", "bladder-cancer", "mrsa"):
            self.assertIn(slug, got)

    def test_a_rule_change_must_bump_the_version(self):
        """THE MACHINERY THAT MAKES THE COUNTS COMPARABLE NEXT YEAR.

        The snapshot stores buckets.yaml's `version` beside a digest of the rules
        themselves. If somebody edits a rule and leaves the version alone, the
        next snapshot silently redefines a label that a previous snapshot already
        used — and the resulting "trend" is an artefact of the edit.
        """
        import json as _json
        import re as _re
        d = os.path.join(HERE, "web", "snapshots", "nordstern")
        dated = sorted(f for f in os.listdir(d) if _re.fullmatch(r"\d{4}-\d\d-\d\d\.json", f))
        self.assertTrue(dated, "no dated snapshot on disk — run check.py --build")
        latest = _json.load(open(os.path.join(d, dated[-1]), encoding="utf-8"))
        b = latest["buckets"]
        self.assertEqual(b["digest"], check.bucket_digest(),
                         "the bucket rules changed since this snapshot was written — "
                         "bump `version` in buckets.yaml and rebuild")
        self.assertEqual(b["version"], check.bucket_version())
        self.assertEqual(sum(b["a"].values()), latest["records"]["active"],
                         "axis A must sum to the register — it is a partition")

    def test_a_version_never_names_two_different_rule_sets(self):
        """THE GUARD THAT ACTUALLY GUARDS, and the first one did not.

        `test_a_rule_change_must_bump_the_version` compares the newest snapshot
        against the code, so it catches a **stale** snapshot. It does not catch
        the case the versioning exists for: somebody edits a rule, rebuilds, and
        leaves `version` alone. Both digest and snapshot update together and the
        first test is happy — while two snapshots now carry the same version
        number for two different definitions, which is exactly the silent
        corruption the version was introduced to prevent.

        So: across every snapshot that carries buckets, **one version must map to
        exactly one digest.** Different rules require a different version; the
        same rules may of course be rebuilt any number of times.
        """
        import json as _json
        import re as _re
        d = os.path.join(HERE, "web", "snapshots", "nordstern")
        seen = {}
        for f in sorted(x for x in os.listdir(d)
                        if _re.fullmatch(r"\d{4}-\d\d-\d\d\.json", x)):
            snap = _json.load(open(os.path.join(d, f), encoding="utf-8"))
            b = snap.get("buckets")
            if not b:
                continue          # predates buckets; nothing to compare
            prev = seen.setdefault(b["version"], (b["digest"], f))
            self.assertEqual(prev[0], b["digest"],
                             f"version {b['version']} names two different rule sets "
                             f"({prev[1]} and {f}) — bump `version` in buckets.yaml "
                             f"when a rule changes, or the counts are not comparable")
        # and the live code must agree with whatever the newest one claims
        if seen:
            self.assertEqual(seen.get(check.bucket_version(), (check.bucket_digest(),))[0],
                             check.bucket_digest(),
                             "the code's rules differ from a snapshot sharing its version")

    def test_every_bucket_states_what_it_does_not_mean(self):
        """Same rule as Engpass's `what_it_unblocks` and the web glossary.

        A bucket name is a compression, and a compression on a public page gets
        read as a verdict. Every one of these has to say what it is not.
        """
        for axis in self.spec["axes"]:
            for b in axis["buckets"]:
                self.assertTrue(b.get("not", "").strip(),
                                f"{b['slug']} does not say what it does not mean")
                self.assertTrue(b.get("rule", "").strip(), f"{b['slug']} has no rule")


class TestBucketMembership(unittest.TestCase):
    """The snapshot stores WHO was in each bucket, not only how many.

    Added 2026-09-02, and the reason is worth keeping next to the tests: the
    bucket counts had been frozen since 2026-08-30 with no membership beside
    them, so `changes-you: 63` → `changes-you: 71` could not distinguish eight
    diseases getting worse from eight records being written. The register grew by
    three the same afternoon this was noticed, which is the whole argument.

    Membership cannot be backfilled, so a missing test here is a year of the
    time series that cannot be recovered rather than a bug that can be fixed.
    """

    @classmethod
    def setUpClass(cls):
        payload = [check.load(p) for p in
                   sorted(glob.glob(os.path.join(HERE, "entities", "*.yaml")))]
        cls.payload = [{**r, "derived": check.derive(r)} for r in payload]
        cls.snap = check.snapshot(cls.payload, on_date="TEST")
        cls.members = cls.snap["buckets"]["members"]

    def test_every_active_record_has_a_membership_entry(self):
        active = [r for r in self.payload if r["derived"]["status"] == "active"]
        self.assertEqual(len(self.members), len(active))
        for r in active:
            self.assertIn(r["slug"], self.members)

    def test_membership_agrees_with_the_counts_beside_it(self):
        """The two are the same object at different granularity. If they can
        disagree, one of them is decoration."""
        from collections import Counter
        by_a = Counter(v["a"] for v in self.members.values())
        self.assertEqual(dict(by_a), self.snap["buckets"]["a"])
        by_b = Counter(t for v in self.members.values() for t in v["b"])
        self.assertEqual(dict(by_b), self.snap["buckets"]["b"])
        self.assertEqual(sum(1 for v in self.members.values() if not v["b"]),
                         self.snap["buckets"]["b_untagged"])

    def test_membership_carries_the_permanent_id(self):
        """Slugs get renamed; ids never do. A diff that followed slugs would
        report a rename as a departure plus an arrival — two fabricated events
        standing in for nothing having happened."""
        for slug, v in self.members.items():
            self.assertTrue(str(v["id"]).startswith("FND-D-"), slug)

    # --- the diff -------------------------------------------------------

    @staticmethod
    def _snap(date, members, digest="d1", version=3, counts=None):
        from collections import Counter
        counts = counts or dict(Counter(v["a"] for v in members.values()))
        return {"date": date, "buckets": {"version": version, "digest": digest,
                                          "a": counts, "members": members}}

    def test_a_snapshot_against_itself_reports_nothing(self):
        d = check.bucket_diff(self.snap, self.snap)
        self.assertIsNone(d["skipped"])
        self.assertFalse(d["rules_changed"])
        self.assertEqual(d["movements"], [])
        self.assertEqual(d["arrivals"], [])
        self.assertEqual(d["departures"], [])

    def test_it_separates_a_movement_from_an_arrival(self):
        """THE ONE THING THIS WHOLE FIELD EXISTS FOR. A net count change of +1
        can be a disease improving or a record being written, and only the first
        is a fact about medicine."""
        old = self._snap("A", {
            "alpha": {"id": "FND-D-0001", "a": "ends-it-later", "b": []},
            "beta":  {"id": "FND-D-0002", "a": "changes-you", "b": []},
        })
        new = self._snap("B", {
            "alpha": {"id": "FND-D-0001", "a": "back-to-normal", "b": []},
            "beta":  {"id": "FND-D-0002", "a": "changes-you", "b": []},
            "gamma": {"id": "FND-D-0003", "a": "back-to-normal", "b": []},
        })
        d = check.bucket_diff(old, new)
        self.assertEqual([m["slug"] for m in d["movements"]], ["alpha"])
        self.assertEqual(d["movements"][0]["from"], "ends-it-later")
        self.assertEqual(d["movements"][0]["to"], "back-to-normal")
        self.assertEqual([a["slug"] for a in d["arrivals"]], ["gamma"])
        # back-to-normal went 0 -> 2, and the two came from different places.
        slot = d["by_bucket"]["back-to-normal"]
        self.assertEqual((slot["moved_in"], slot["arrived"]), (1, 1))
        self.assertEqual(slot["net"], 2)

    def test_it_follows_a_renamed_record_by_id(self):
        old = self._snap("A", {"befund": {"id": "FND-D-0007",
                                          "a": "held-off", "b": []}})
        new = self._snap("B", {"nordstern": {"id": "FND-D-0007",
                                             "a": "held-off", "b": []}})
        d = check.bucket_diff(old, new)
        self.assertEqual(d["arrivals"], [])
        self.assertEqual(d["departures"], [])
        self.assertEqual(d["movements"], [])

    def test_it_reports_a_departure(self):
        old = self._snap("A", {"alpha": {"id": "FND-D-0001",
                                         "a": "held-off", "b": []}})
        new = self._snap("B", {})
        d = check.bucket_diff(old, new)
        self.assertEqual([x["slug"] for x in d["departures"]], ["alpha"])
        self.assertEqual(d["by_bucket"]["held-off"]["left"], 1)

    def test_it_tracks_tags_in_both_directions(self):
        old = self._snap("A", {"alpha": {"id": "FND-D-0001", "a": "held-off",
                                         "b": ["cannot-aim-it"]}})
        new = self._snap("B", {"alpha": {"id": "FND-D-0001", "a": "held-off",
                                         "b": ["cannot-reach-people"]}})
        d = check.bucket_diff(old, new)
        self.assertEqual([x["tag"] for x in d["tags_gained"]], ["cannot-reach-people"])
        self.assertEqual([x["tag"] for x in d["tags_lost"]], ["cannot-aim-it"])

    def test_it_skips_rather_than_guesses_when_membership_is_absent(self):
        """A check that cannot run reports `skipped`, never `ok` — the same rule
        Sperrwerk holds. The pre-2026-09-02 snapshots are exactly this case."""
        old = {"date": "A", "buckets": {"version": 3, "digest": "d1",
                                        "a": {"held-off": 1}}}
        d = check.bucket_diff(old, self.snap)
        self.assertIsNotNone(d["skipped"])
        self.assertIn("A", d["skipped"])
        self.assertEqual(d["movements"], [])

    def test_a_rule_change_is_flagged_and_not_silently_counted(self):
        """If `digest` moved, a record can appear to move because the definition
        walked past it. v3 moved eight records on its own."""
        m = {"alpha": {"id": "FND-D-0001", "a": "changes-you", "b": []}}
        m2 = {"alpha": {"id": "FND-D-0001", "a": "back-to-normal", "b": []}}
        d = check.bucket_diff(self._snap("A", m, digest="d1", version=2),
                              self._snap("B", m2, digest="d2", version=3))
        self.assertTrue(d["rules_changed"])
        self.assertEqual(len(d["movements"]), 1)

    def test_the_live_snapshots_on_disk_diff_without_crashing(self):
        snaps = check.load_snapshots(HERE)
        self.assertGreaterEqual(len(snaps), 2)
        for a, b in zip(snaps, snaps[1:]):
            d = check.bucket_diff(a, b)
            self.assertIn("skipped", d)
