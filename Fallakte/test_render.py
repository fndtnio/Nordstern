#!/usr/bin/env python3
"""Tests for the case-file markdown renderer.

Run:  python3 test_render.py
      python3 -m unittest test_render

The renderer produces a PUBLIC PAGE, so two classes of test matter more than the
rest: that markdown cannot inject HTML, and that unknown syntax raises instead
of being passed through to be printed literally at a reader.
"""

from __future__ import annotations

import glob
import importlib.util
import re
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("fallakte_render", os.path.join(HERE, "render.py"))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)


class TestInline(unittest.TestCase):

    def test_the_four_inline_forms(self):
        self.assertEqual(R.inline("**a**"), "<b>a</b>")
        self.assertEqual(R.inline("*a*"), "<i>a</i>")
        self.assertEqual(R.inline("`a`"), "<code>a</code>")
        self.assertEqual(R.inline("[t](https://x.test/p)"),
                         '<a href="https://x.test/p">t</a>')

    def test_italics_nest_inside_bold(self):
        """The corpus does this, and `[^*]+` for bold silently broke on it."""
        self.assertEqual(R.inline("**a *b* c**"), "<b>a <i>b</i> c</b>")

    def test_a_code_span_is_literal_and_protects_what_is_in_it(self):
        """`**not bold**` inside backticks must survive as text."""
        self.assertEqual(R.inline("`**x**`"), "<code>**x**</code>")
        self.assertEqual(R.inline("`a*b`"), "<code>a*b</code>")

    def test_markdown_CANNOT_inject_html(self):
        """The single most important test here: this output is published."""
        for src in ("<script>alert(1)</script>",
                    "<img src=x onerror=alert(1)>",
                    "**<b>bold</b>**",
                    "`<script>`"):
            out = R.inline(src)
            self.assertNotIn("<script", out, src)
            self.assertNotIn("<img", out, src)
            self.assertIn("&lt;", out, src)

    def test_a_dangerous_link_target_is_refused(self):
        with self.assertRaises(R.RenderError):
            R.inline("[click](javascript:alert(1))")

    def test_strict_catches_what_it_cannot_consume(self):
        with self.assertRaises(R.RenderError):
            R.inline("an `unpaired backtick")
        with self.assertRaises(R.RenderError):
            R.inline("a stray * asterisk")
        # and lenient mode exists for a one-off, and is not what the build uses
        self.assertIn("*", R.inline("a stray * asterisk", strict=False))


class TestBlocks(unittest.TestCase):

    def test_headings_carry_a_stable_anchor(self):
        out = R.render("## Where it stands")
        self.assertEqual(out, '<h2 id="where-it-stands">Where it stands</h2>')
        # markup is stripped from the anchor but kept in the text
        out = R.render("### `iron` and **stores**")
        self.assertIn('id="iron-and-stores"', out)
        self.assertIn("<code>iron</code>", out)

    def test_headings_lists_itself(self):
        hs = R.headings("# A\n\n## B\n\npara\n\n### C\n")
        self.assertEqual([(1, "A", "a"), (2, "B", "b"), (3, "C", "c")], hs)

    def test_paragraph_joins_wrapped_lines(self):
        self.assertEqual(R.render("one\ntwo\n\nthree"),
                         "<p>one two</p>\n<p>three</p>")

    def test_table_with_alignment(self):
        out = R.render("| a | b |\n|---|---:|\n| 1 | 2 |")
        self.assertIn('<th style="text-align:left">a</th>', out)
        self.assertIn('<th style="text-align:right">b</th>', out)
        self.assertIn('<td style="text-align:right">2</td>', out)

    def test_a_table_may_have_blank_header_cells(self):
        """`| | |` collided with the separator pattern and refused to parse.

        The first case file opens with exactly that table — two columns, no
        headings — so this is a corpus-driven test rather than a hypothetical.
        """
        out = R.render("| | |\n|---|---|\n| k | v |")
        self.assertIn("<table>", out)
        self.assertIn(">k</td>", out)

    def test_a_table_without_a_separator_is_an_error(self):
        with self.assertRaises(R.RenderError):
            R.render("| a | b |\n| 1 | 2 |")

    def test_lists_absorb_their_continuation_lines(self):
        out = R.render("- first item\n  wrapped on\n  three lines\n- second")
        self.assertIn("<li>first item wrapped on three lines</li>", out)
        self.assertIn("<li>second</li>", out)
        self.assertTrue(out.startswith("<ul>"))

    def test_ordered_lists_are_ol(self):
        out = R.render("1. a\n2. b")
        self.assertTrue(out.startswith("<ol>"))
        self.assertIn("<li>b</li>", out)

    def test_indented_block_is_preformatted_and_not_reparsed(self):
        out = R.render("    the disease is not the mutation.\n    it is **x** times time.")
        self.assertIn("<pre>", out)
        self.assertIn("**x**", out)   # literal inside pre

    def test_fence_and_quote_and_rule(self):
        self.assertIn("<pre>", R.render("```\nx = 1\n```"))
        self.assertIn("<blockquote>", R.render("> a claim"))
        self.assertEqual(R.render("---"), "<hr>")

    def test_an_unparseable_line_raises_rather_than_passing_through(self):
        """A renderer that shrugs publishes `**bold**` at a reader."""
        with self.assertRaises(R.RenderError):
            R.render("| a | b |\n| no separator |")


class TestCorpus(unittest.TestCase):

    def test_every_markdown_file_in_the_register_renders_strictly(self):
        """The corpus is the test. A file that stops rendering fails the build."""
        files = sorted(glob.glob(os.path.join(HERE, "**", "*.md"), recursive=True))
        self.assertTrue(files, "no markdown found")
        for path in files:
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            try:
                out = R.render(src)
            except R.RenderError as exc:
                self.fail(f"{os.path.relpath(path, HERE)}: {exc}")
            # CODE AND PRE ARE STRIPPED FIRST. `**` inside a code span is the
            # renderer working, not failing — `<code>**bold**</code>` is how
            # this register's own prose quotes markdown at the reader. The
            # blanket check fired on exactly that sentence, which is the third
            # guard in this repo to trip over its own documentation.
            prose = re.sub(r"<(code|pre)>.*?</\1>", " ", out, flags=re.S)
            self.assertNotIn("**", prose, f"{path}: unrendered bold survived")
            self.assertNotIn("<script", out.lower(), f"{path}: raw html survived")


if __name__ == "__main__":
    unittest.main(verbosity=2)
