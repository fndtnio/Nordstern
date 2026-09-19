#!/usr/bin/env python3
"""Assert that Nordstern still does not know Engpass exists.

Run:  python3 test_boundary.py
      python3 -m unittest test_boundary

WHY THIS FILE EXISTS. Engpass used to be a sibling directory. On 2026-08-26 it
moved to `Nordstern/Engpass/`, because the two registers are published together
and the dashboard wants both. **Nesting is exactly where a one-way dependency
goes to die**: the first person who writes `from ..check import load` inside
Nordstern, or globs `*/obstacles/*.yaml` from the build, destroys the property
that makes the link between the registers trustworthy.

THE PROPERTY. Nordstern records `blockers[].obstacles: [slug]` and nothing more.
It does not validate those slugs, does not read this directory, and does not know
what is in it. Engpass reads Nordstern's built `web/nordstern.json` and
reconciles. Same rule as Strangschrift and Sperrwerk: **neither tool imports the
other, a text file is the whole interface.**

The dependency is asymmetric on purpose, so this test is asymmetric too. Engpass
importing Nordstern's loader is fine and is the one permitted crossing. Nordstern
importing anything from here is the failure.
"""

from __future__ import annotations

import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
NORDSTERN = os.path.normpath(os.path.join(HERE, ".."))
SELF_DIRNAME = os.path.basename(HERE)

# Files under Nordstern/ that are allowed to say "Engpass" and why.
#   SCHEMA.md / gaps.md / index.md  — prose describing the link, which is the
#     documentation of the boundary and would be worse if absent.
#   web/data.js                     — generated from entities/*.yaml, whose
#     record prose mentions the register by name. Text, not a dependency.
PROSE_OK = {".md", ".org", ".txt"}


def _nordstern_files():
    """Every file under Nordstern/, excluding this directory."""
    for root, dirs, files in os.walk(NORDSTERN):
        dirs[:] = [d for d in dirs
                   if d not in (SELF_DIRNAME, "__pycache__", ".git", "node_modules")]
        for f in files:
            yield os.path.join(root, f)


class TestBoundary(unittest.TestCase):

    def test_nordstern_has_no_python_import_from_engpass(self):
        """The failure mode this file was written for.

        Engpass imports Nordstern's YAML loader — that is the permitted
        direction. Anything the other way makes the registers one program and
        the derived disease list stops being independent evidence.
        """
        bad = re.compile(r"^\s*(from|import)\s+.*\b(engpass|Engpass|neuland|Neuland)\b",
                         re.MULTILINE)
        offenders = []
        for path in _nordstern_files():
            if not path.endswith(".py"):
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                if bad.search(fh.read()):
                    offenders.append(os.path.relpath(path, NORDSTERN))
        self.assertEqual(offenders, [], (
            "Nordstern imports Engpass. The dependency runs one way: Nordstern "
            "records obstacle slugs and nothing more; Engpass reads Nordstern's "
            "built artifact. See Engpass/README.md rule 1."))

    def test_nordstern_code_does_not_read_the_engpass_directory(self):
        """A path reference is the same failure wearing different clothes.

        Reaching into `Engpass/obstacles/` from Nordstern's build or checker
        would let the two files disagree about what blocks what, which is the
        thing `check.py` was written to prevent.

        THIS TEST LOOKS FOR PATH CONSTRUCTION, NOT FOR THE WORD. The first
        version matched any line containing `Engpass/` and immediately fired on
        a docstring in Nordstern's own `check.py` that names this file while
        explaining the boundary. **A guard that fires on prose gets suppressed**,
        and a suppressed guard is worse than none — so it now matches only the
        idioms that actually open or fetch something.

        `web/snapshots/engpass/` is explicitly ALLOWED. Engpass writes its
        snapshot into Nordstern's `web/` because that is the permitted direction
        and it is where the dashboard looks. A published artifact in the shared
        output directory is a text file, which is the whole interface; the
        register's source directory is not.
        """
        opens = re.compile(
            r"""(?ix)
            (?: os\.path\.join | open | glob | fetch | require | import\s*\(
              | src\s*=      | href\s*=  | \bPath\s*\( )
            [^\n]{0,120}? (Engpass|Neuland) [/\\'"]
            """)
        allowed = re.compile(r"snapshots[/\\]engpass", re.I)
        offenders = []
        for path in _nordstern_files():
            if os.path.splitext(path)[1] not in (".py", ".js", ".html"):
                continue
            rel = os.path.relpath(path, NORDSTERN)
            if rel == os.path.join("web", "data.js"):
                continue  # generated from record prose; text, not a dependency
            with open(path, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if opens.search(line) and not allowed.search(line):
                        offenders.append(f"{rel}:{i}: {line.strip()[:90]}")
        self.assertEqual(offenders, [], (
            "Nordstern code opens a path inside the Engpass source directory:\n  "
            + "\n  ".join(offenders)))

    def test_engpass_writes_its_snapshot_rather_than_appearing_in_nordsterns(self):
        """The snapshot design, pinned, because it is the tempting shortcut.

        The dashboard wants both registers on one page, and the obvious way to
        get that is for Nordstern's `--build` to reach in here and total up the
        obstacles. That would invert the dependency for the sake of one chart.

        Instead Engpass writes its own snapshot into the shared `web/` output —
        arrow unchanged — and the page reads two files.
        """
        with open(os.path.join(NORDSTERN, "check.py"), encoding="utf-8") as fh:
            nordstern_src = fh.read()
        self.assertNotIn('"engpass"', nordstern_src.lower(), (
            "Nordstern's snapshot appears to include Engpass data. Engpass "
            "writes its own; see Engpass/check.py:write_snapshot."))
        with open(os.path.join(HERE, "check.py"), encoding="utf-8") as fh:
            self.assertIn("write_snapshot", fh.read(),
                          "Engpass should emit its own snapshot")

    def test_engpass_reads_nordstern_only_through_the_built_artifact(self):
        """The permitted crossing, pinned so it cannot quietly widen.

        `check.py` may import Nordstern's bounded YAML loader — it is a loader,
        not a model — and may read `web/nordstern.json`. It must NOT walk
        `entities/*.yaml` itself, because then it would be re-deriving ratings
        rather than consuming the artifact Nordstern published.
        """
        with open(os.path.join(HERE, "check.py"), encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn("nordstern.json", src,
                      "Engpass should consume Nordstern's built artifact")
        self.assertNotIn("entities", src, (
            "Engpass reads entities/*.yaml directly. It must consume the built "
            "artifact instead, or it is re-deriving what Nordstern published."))

    def test_nordstern_blocker_obstacle_slugs_are_still_unvalidated(self):
        """Nordstern must NOT check that an obstacle slug exists.

        This looks like a missing validation and is the design. A typo'd slug is
        caught here, by Engpass, as an error. If Nordstern validated it, the
        registers would be coupled and Nordstern could no longer be edited
        without this directory present.
        """
        with open(os.path.join(NORDSTERN, "check.py"), encoding="utf-8") as fh:
            src = fh.read()
        for line in src.splitlines():
            if "obstacles" in line and ("not in" in line or "unknown" in line.lower()):
                self.fail(
                    "Nordstern appears to validate obstacle slugs: " + line.strip()
                    + "\nThat coupling is what the split exists to avoid.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
