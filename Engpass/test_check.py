#!/usr/bin/env python3
"""Engpass's own guards. Run: python3 -m unittest test_check

WHY THIS FILE EXISTS, AND WHY IT IS SMALL. `test_boundary.py` covers the one
rule that makes this a separate register — the dependency runs one way and
nesting inside Nordstern did not change it — and deliberately covers nothing
else. What was missing was any guard on the snapshot, which is the artifact the
planned dashboard reads and the only thing here that becomes unrecoverable if it
is written wrongly.

THE SNAPSHOT IS THE ONE ARTIFACT THAT CANNOT BE FIXED LATER. A stale
`crud.md` regenerates. A wrong count in a report is corrected by rerunning. But
"which records cited `who-progresses` in September 2026" exists only in the file
written in September 2026 — the ratings move, the deriving code moves, and no
later run can reconstruct it. So membership gets a test on the day it is added
rather than on the day it is first read.
"""

import json
import os
import unittest

import check
import stages

HERE = os.path.dirname(os.path.abspath(__file__))


class TestSnapshotMembership(unittest.TestCase):
    """`blocks` says how many; `blocks_members` says which. Both, or neither
    means anything a year from now — see Nordstern's TestBucketMembership, which
    was added the same day for the identical reason.
    """

    @classmethod
    def setUpClass(cls):
        check.errors.clear()
        check.warnings.clear()
        cls.obstacles = check.read_questions()
        cls.records = check.read_nordstern()
        cls.cited, cls.untagged = check.link(cls.obstacles, cls.records)
        cls.snap = check.snapshot(cls.obstacles, cls.cited, cls.untagged,
                                  cls.records, on_date="TEST")

    def test_membership_agrees_with_the_counts_beside_it(self):
        """The same object at two granularities. If they can disagree, one of
        them is decoration and the dashboard will eventually print both."""
        for slug, n in self.snap["blocks"].items():
            self.assertEqual(len(self.snap["blocks_members"][slug]), n, slug)

    def test_every_obstacle_appears_in_both_maps(self):
        active = {q["slug"] for q in self.obstacles}
        self.assertEqual(set(self.snap["blocks_members"]), active)
        self.assertEqual(set(self.snap["resolution_members"]), active)

    def test_membership_lists_are_real_record_slugs(self):
        """A slug that no longer resolves is a citation that has rotted, and the
        register's whole append-only argument is that citations keep resolving."""
        known = {r["slug"] for r in self.records}
        for slug, members in self.snap["blocks_members"].items():
            for m in members:
                self.assertIn(m, known, f"{slug} cites unknown record {m}")

    def test_resolution_members_carry_the_permanent_id(self):
        """`slug` is the human handle and gets renamed — `questions/` became
        `obstacles/`. `id` is what a diff follows."""
        for slug, v in self.snap["resolution_members"].items():
            self.assertTrue(str(v["id"]).startswith("FND-O-"), slug)
            self.assertIn(v["resolution"], check.RESOLUTIONS)

    def test_the_snapshot_on_disk_is_not_stale(self):
        """Same guard Nordstern's TestSnapshot holds: recompute, do not trust.
        A snapshot left behind after the obstacles changed is `index.md`'s drift
        failure in a file nobody reads by eye."""
        today = check.snapshot(self.obstacles, self.cited, self.untagged,
                               self.records)["date"]
        path = os.path.join(HERE, "..", "web", "snapshots", "engpass",
                            today + ".json")
        if not os.path.exists(path):
            self.skipTest("no snapshot for today — run `python3 check.py --build`")
        with open(path, encoding="utf-8") as fh:
            on_disk = json.load(fh)
        fresh = check.snapshot(self.obstacles, self.cited, self.untagged,
                               self.records, on_date=on_disk["date"])
        self.assertEqual(on_disk, fresh,
                         "snapshot on disk disagrees with a fresh computation — "
                         "run `python3 check.py --build`")


class TestStages(unittest.TestCase):
    """`stages.py` tests a framing against the corpus; these test the test.

    Same contract as `crud.py`: the argument is generated, so it cannot go stale
    — but a generated argument can still be arithmetically wrong, and this one
    makes a strong claim (the gates get tighter, and the tightest is not a
    science gate) that would be embarrassing to publish from a bug.
    """

    @classmethod
    def setUpClass(cls):
        cls.recs = stages.load()

    def test_every_record_gets_a_verdict_at_every_gate(self):
        for r in self.recs:
            for name, _, fn in stages.GATES:
                v = fn(r)
                self.assertIn(v, (True, False, None), f"{r['slug']}/{name}")
                if name != "reach":
                    self.assertIsNot(v, None,
                                     f"{r['slug']}: only `reach` may be n/a")

    def test_reach_is_n_a_for_exactly_two_reasons(self):
        """A disease with no capability has nothing to deliver, and counting it
        as a delivery failure would charge one failure to two gates.

        AND A SECOND REASON THIS TEST FOUND ON ITS FIRST RUN. Nordstern withholds
        `delivery` from a `preventable` record too — `efficacy` and `access`
        describe only the TREATMENT, and a record rescued from "nothing can be
        done" by a vaccine has no treatment those numbers are about (Nordstern
        gaps.md #109). `hpv-infection` is the case that surfaced it. So gate 4
        cannot be asked of six records for a reason that has nothing to do with
        gate 2, and `stages.md` says so rather than counting them as failures."""
        for r in self.recs:
            if stages.gate_reach(r) is None:
                self.assertTrue(
                    not stages.gate_do(r)
                    or r["derived"]["capability"] == "preventable",
                    f"{r['slug']}: reach is n/a and neither reason applies")

    def test_the_gates_get_tighter_which_is_the_documents_whole_claim(self):
        shut = [sum(1 for r in self.recs if fn(r) is False)
                for _, _, fn in stages.GATES]
        self.assertEqual(shut, sorted(shut),
                         f"the funnel is not monotonic: {shut} — stages.md leads "
                         f"with 'each gate is tighter than the one before it'")

    def test_the_delivery_gate_dominates_on_the_loosest_reading_too(self):
        """The document's main result must not rest on where a band was drawn."""
        loose = sum(1 for r in self.recs
                    if r["derived"]["delivery"] in stages.LOOSE_SHUT)
        science = sum(1 for r in self.recs
                      if any(fn(r) is False for _, _, fn in stages.GATES[:3]))
        self.assertGreater(loose, science,
                           "on the loosest reading the delivery gate no longer "
                           "exceeds the three science gates combined — stages.md "
                           "claims it does")

    def test_the_report_on_disk_is_not_stale(self):
        path = os.path.join(HERE, "stages.md")
        if not os.path.exists(path):
            self.skipTest("run `python3 stages.py`")
        with open(path, encoding="utf-8") as fh:
            on_disk = fh.read()
        for _, _, fn in stages.GATES:
            n = sum(1 for r in self.recs if fn(r) is False)
            self.assertIn(f"| {n} |", on_disk,
                          f"stages.md does not contain the current count {n} — "
                          f"run `python3 stages.py`")


if __name__ == "__main__":
    unittest.main()


class TestDerivedStanding(unittest.TestCase):
    """`derived` is a receipt, not a grade, and it has an inverted guard.

    The other four standings say how an assertion about payoff stood up, and a
    claim moves between them when the QUESTION is answered. `derived` says the
    register caught up with itself: somebody rating the disease agreed, so the
    link is earned. It exists because the transition happened twice in one
    afternoon and both times the claim was DELETED — destroying the only
    evidence that the assertion came first, which is the one thing `claims` is
    for.
    """

    @classmethod
    def setUpClass(cls):
        check.errors.clear()
        check.warnings.clear()
        cls.obstacles = check.read_questions()
        cls.records = check.read_nordstern()
        cls.cited, _ = check.link(cls.obstacles, cls.records)
        cls.snap = check.snapshot(cls.obstacles, cls.cited, [], cls.records,
                                  on_date="TEST")

    def test_a_derived_claim_names_a_record_that_actually_cites_it(self):
        """The inverted guard. A normal claim must NOT name a citing record; a
        `derived` one MUST, or it is a receipt for a link that is not there."""
        for q in self.obstacles:
            have = {r["slug"] for r in self.cited[q["slug"]]}
            for c in q.get("claims") or []:
                if c["standing"] == "derived":
                    self.assertIn(c["unblocks"], have,
                                  f"{q['slug']}: derived claim on {c['unblocks']} "
                                  f"has no matching citation")

    def test_derived_claims_are_not_drawn_as_unconfirmed_assertions(self):
        """`claims_by_obstacle` feeds the dashboard's dashed claim chips. A
        derived claim is already in `blocks_members`; drawing it again as an
        unconfirmed assertion is the double-count the guard exists to stop."""
        for slug, cs in (self.snap.get("claims_by_obstacle") or {}).items():
            for c in cs:
                self.assertNotEqual(c["standing"], "derived", slug)
                self.assertNotIn(c["unblocks"], self.snap["blocks_members"][slug],
                                 f"{slug}: {c['unblocks']} is drawn as a claim "
                                 f"and is also a derived link")

    def test_earned_claims_are_reported_separately_and_agree_with_the_links(self):
        for slug, earned in (self.snap.get("claims_earned") or {}).items():
            for e in earned:
                self.assertIn(e, self.snap["blocks_members"][slug],
                              f"{slug}: claims to have earned {e}, which does not "
                              f"cite it")

    def test_an_obstacle_with_only_derived_claims_is_not_called_top_down(self):
        """A record whose every claim was earned is not carrying assertions —
        and by the inverted guard it necessarily has citations, so the
        `no Nordstern record cites this` warning could never be right about it."""
        for q in self.obstacles:
            cs = q.get("claims") or []
            if cs and all(c["standing"] == "derived" for c in cs):
                self.assertTrue(self.cited[q["slug"]],
                                f"{q['slug']}: all claims derived but nothing cites it")
