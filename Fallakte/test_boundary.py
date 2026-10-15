#!/usr/bin/env python3
"""Assert that neither Nordstern nor Engpass knows Fallakte exists.

Run:  python3 test_boundary.py
      python3 -m unittest test_boundary

WHY THIS FILE EXISTS. Fallakte is the third register under `Nordstern/`, and the
first two already proved where a one-way dependency goes to die: nesting. The
moment Nordstern's build globs `*/cases/*.yaml`, or a record gains a `case_file:`
field, the case file stops being a workspace and becomes part of the verdict —
which is the exact coupling the split was made to avoid.

THE PROPERTY, IN BOTH DIRECTIONS.

  * **Outward is allowed.** A case file names a Nordstern slug and Engpass
    obstacle slugs, and `check.py` resolves them. That is Fallakte's job.
  * **Inward is the failure.** Nordstern does not read this directory. Neither
    does Engpass. A case file is never cited by a record, because a record is
    append-only and citable and a case file changes every week.
  * **And the crossings go through BUILT ARTIFACTS.** Fallakte reads
    `web/nordstern.json` and Engpass's published snapshot — not `entities/` and
    not Engpass's obstacle source. Same rule Engpass lives under: re-deriving
    somebody else's ratings is how two files start disagreeing.

The one permitted import, as in Engpass, is Nordstern's bounded YAML loader by
explicit file path. It is a loader, not a model.
"""

from __future__ import annotations

import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
NORDSTERN = os.path.normpath(os.path.join(HERE, ".."))
SELF_DIRNAME = os.path.basename(HERE)


def _other_register_files():
    """Every file under Nordstern/, excluding this directory."""
    for root, dirs, files in os.walk(NORDSTERN):
        dirs[:] = [d for d in dirs
                   if d not in (SELF_DIRNAME, "__pycache__", ".git", "node_modules")]
        for f in files:
            yield os.path.join(root, f)


class TestBoundary(unittest.TestCase):

    def test_nothing_else_imports_fallakte(self):
        """Neither register may import this one. Outward only."""
        bad = re.compile(r"^\s*(from|import)\s+.*\b[Ff]allakte\b", re.MULTILINE)
        offenders = []
        for path in _other_register_files():
            if not path.endswith(".py"):
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                if bad.search(fh.read()):
                    offenders.append(os.path.relpath(path, NORDSTERN))
        self.assertEqual(offenders, [], (
            "Something outside Fallakte imports it. The dependency runs outward: a "
            "case file cites a record, never the reverse. See Fallakte/README.md rule 1."))

    def test_no_other_register_code_reads_the_cases_directory(self):
        """A path reference is the same failure wearing different clothes.

        Looks for the idioms that actually open or fetch something, NOT for the
        word — Engpass learned that the hard way, because a guard that fires on
        its own documentation gets suppressed, and a suppressed guard is worse
        than none.
        """
        opens = re.compile(
            r"""(?ix)
            (?: os\.path\.join | open | glob | fetch | require | import\s*\(
              | src\s*=      | href\s*=  | \bPath\s*\( )
            [^\n]{0,120}? (Fallakte) [/\\'"]
            """)
        offenders = []
        for path in _other_register_files():
            if os.path.splitext(path)[1] not in (".py", ".js", ".html"):
                continue
            rel = os.path.relpath(path, NORDSTERN)
            with open(path, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if opens.search(line):
                        offenders.append(f"{rel}:{i}: {line.strip()[:90]}")
        self.assertEqual(offenders, [], (
            "Code outside Fallakte opens a path inside it:\n  " + "\n  ".join(offenders)))

    def test_no_record_has_a_case_file_field(self):
        """The tempting shortcut, pinned.

        A `case_file:` key on a record would put a weekly-changing pointer inside
        an append-only verdict, and the schema would then have to validate it.
        If a reader needs to get from a record to a case file, the published
        query tool joins them on the slug — a text key, which is the whole
        interface.
        """
        entities = os.path.join(NORDSTERN, "entities")
        offenders = []
        for name in sorted(os.listdir(entities)):
            if not name.endswith(".yaml"):
                continue
            with open(os.path.join(entities, name), encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    if re.match(r"^\s*(case_file|fallakte|case)\s*:", line):
                        offenders.append(f"entities/{name}:{i}: {line.strip()[:80]}")
        self.assertEqual(offenders, [], (
            "A record carries a case-file pointer:\n  " + "\n  ".join(offenders)))

    def test_fallakte_reads_the_others_only_through_built_artifacts(self):
        """The permitted crossings, pinned so they cannot quietly widen."""
        with open(os.path.join(HERE, "check.py"), encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn("nordstern.json", src,
                      "Fallakte should consume Nordstern's built artifact")
        self.assertIn("snapshots/engpass", src,
                      "Fallakte should consume Engpass's published snapshot")
        code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
        # Path construction into either register's SOURCE directory. Matched as
        # literal path fragments rather than as bare field names: the first
        # version of this test fired on `case.get("obstacles")`, which is this
        # register reading its OWN field, and a guard that fires on correct code
        # gets deleted rather than heeded.
        # MATCH THE IDIOM THAT OPENS SOMETHING, not the word. The bare fragment
        # `entities/` fired on a REGEX that recognises a link target of the form
        # `entities/<slug>.yaml` so the build can turn it into a query-tool
        # link. Recognising a path in a string is not reading a directory, and
        # a guard that cannot tell them apart gets deleted rather than heeded.
        opens = re.compile(
            r"""(?x)
            (?: os\.path\.join | glob\.glob | os\.listdir | os\.walk | open )
            \s*\( [^\n]{0,120}? (entities|obstacles) [/\\'"]
            """)
        offenders = [f"{m.group(0).strip()[:70]}  (reads another register's source)"
                     for m in opens.finditer(code)]
        if "Engpass/obstacles" in code:
            offenders.append("Engpass/obstacles  (reads Engpass's source directory)")
        self.assertEqual(offenders, [], (
            "Fallakte builds a path into another register's source:\n  "
            + "\n  ".join(offenders)
            + "\nIt must consume the built artifact instead, or it is re-deriving "
              "what that register published."))

    def test_every_case_file_names_a_real_record(self):
        """The register's own reason to exist: the outward link resolves.

        This duplicates `check.py` on purpose. `check.py` is run by a person;
        this is run by CI, and the link is the one thing that must not rot.
        """
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "fallakte_check", os.path.join(HERE, "check.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        records = mod.nordstern_records()
        if not records:
            self.skipTest("Nordstern's built artifact is absent; run check.py --build")
        found = mod.cases()
        self.assertTrue(found, "no case files on disk")
        for case in found:
            self.assertIn(case.get("disease"), records,
                          f"{case.get('slug')} names a disease that is not a record")


if __name__ == "__main__":
    unittest.main(verbosity=2)
