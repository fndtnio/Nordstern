#!/usr/bin/env python3
"""Tests for the build half of Fallakte's checker.

Run:  python3 test_check.py

`check.py`'s validation is exercised constantly by running it. What is NOT
exercised by running it is the part that only matters once a page is public:
turning a repo path into a link a stranger can follow.
"""

from __future__ import annotations

import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("fallakte_check", os.path.join(HERE, "check.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

CASE_DIR = os.path.join(HERE, "cases", "polycythaemia-vera")


class TestLinkRewriting(unittest.TestCase):

    def r(self, href):
        return C._rewrite_link(href, CASE_DIR)

    def test_an_absolute_link_is_left_alone(self):
        for href in ("https://x.test/a", "http://x.test/a", "mailto:a@x.test", "#anchor"):
            self.assertEqual(self.r(href), href)

    def test_a_sibling_register_document_becomes_a_site_page(self):
        self.assertEqual(self.r("../../GLOSSARY.md"), "fallakte.html#terms")
        self.assertEqual(self.r("../../TEMPLATE.md"), "fallakte.html#template")
        self.assertEqual(self.r("../../README.md"), "fallakte.html")

    def test_a_disease_record_becomes_a_query_rather_than_raw_yaml(self):
        """A reader clicking a disease wants the record, not a YAML file."""
        self.assertEqual(self.r("../../../entities/polycythaemia-vera.yaml"),
                         "query.html?q=slug:polycythaemia-vera")

    def test_anything_else_in_a_known_repo_resolves_to_public_source(self):
        out = self.r("../../../SCHEMA.md")
        self.assertTrue(out.startswith("https://github.com/fndtnio/Nordstern/blob/main/"), out)
        self.assertTrue(out.endswith("SCHEMA.md"), out)
        out = self.r("../../../../strombild/examples/iron.strombild")
        self.assertIn("fndtnio/Strombild", out)

    def test_a_link_that_cannot_be_made_public_FAILS_THE_BUILD(self):
        """The whole point. A dead link in a shared page is the failure mode."""
        html = '<p><a href="../../../../Schaltwerk/examples/pfcp.schalt">x</a></p>'
        out, bad = C._rewrite(html, CASE_DIR)
        self.assertEqual(len(bad), 1, out)

    def test_the_real_corpus_rewrites_with_nothing_left_over(self):
        doc = C._doc(os.path.join(CASE_DIR, "README.md"))   # raises on a dead link
        self.assertNotIn('href="../', doc["html"])
        self.assertTrue(doc["headings"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
