#!/usr/bin/env python3
"""Markdown -> HTML, for the exact subset the case files use and nothing else.

Run:  python3 render.py <file.md>     # print the HTML
      python3 test_render.py          # the tests

WHY THIS IS HERE RATHER THAN A LIBRARY IN THE BROWSER.

The family rule is zero dependencies and text as the interface, and Nordstern's
pages carry a second rule of their own: **every artifact arrives as a `<script>`
tag rather than a `fetch()`, so that each page also opens over `file://`.** A
markdown renderer pulled from a CDN breaks both. So the markdown is rendered
here, at build time, and the viewer receives finished HTML.

It also means the browser loads no markdown library and the pages open from a
folder over `file://`. **It does not mean the page works without JavaScript** —
the viewer still selects a case and inserts the finished HTML — and saying so
here because the first draft of this docstring claimed otherwise.

WHAT IT SUPPORTS, and the list is closed on purpose — `python3 -c` over the
corpus produced it, and anything not in it is a parse error rather than a
silent passthrough:

    # ## ###         headings
    paragraphs       blank-line separated
    **b** *i* `c`    inline, plus [text](url)
    | a | b |        tables, with an |---|---| separator and ---: alignment
    - item           unordered lists, with 2-3 space continuation lines
    1. item          ordered lists, same
    ---              horizontal rule
    (4 spaces)       preformatted block
    ``` ```          fenced block
    > quote          blockquote

**THE PARSE ERROR IS THE FEATURE.** A renderer that quietly passes unknown
syntax through produces a public page with `**bold**` printed literally in it,
which is exactly the class of failure the rest of this register is built to
avoid. `strict=False` is available for a one-off, and the build does not use it.
"""

from __future__ import annotations

import html
import re
import sys


class RenderError(ValueError):
    pass


# ---------------------------------------------------------------------------
# inline
# ---------------------------------------------------------------------------
# ORDER MATTERS AND CODE COMES FIRST. A backtick span is literal, so nothing
# inside it may be re-read as markup — `**not bold**` has to survive. The span
# is therefore cut out, replaced by a placeholder that cannot occur in the
# source, and restored at the end.
_CODE = re.compile(r"`([^`\n]+)`")
_LINK = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)")
# NON-GREEDY, AND IT MUST ALLOW SINGLE ASTERISKS INSIDE. `[^*]+` refused
# `**bold with *italics* inside**`, which the corpus uses, and left the stray
# asterisks for the strict check to trip over. The bold body is re-read for
# italics rather than being treated as literal.
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITAL = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
_SENTINEL = "\x00"


def inline(text: str, strict: bool = True) -> str:
    spans: list[str] = []

    def stash(m):
        spans.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"{_SENTINEL}{len(spans) - 1}{_SENTINEL}"

    text = _CODE.sub(stash, text)
    if "`" in text and strict:
        raise RenderError(f"unpaired backtick: {text[:70]!r}")

    text = html.escape(text)
    # the link target is escaped above; only http(s), mailto and relative paths
    # are allowed through, so an escaped `javascript:` cannot become a link
    def link(m):
        label, href = m.group(1), m.group(2)
        if not re.match(r"^(https?://|mailto:|[./#?]|[\w./#?-]+$)", href):
            raise RenderError(f"refusing link target {href!r}")
        return f'<a href="{href}">{label}</a>'

    text = _LINK.sub(link, text)
    text = _BOLD.sub(lambda m: "<b>" + _ITAL.sub(r"<i>\1</i>", m.group(1)) + "</b>", text)
    text = _ITAL.sub(r"<i>\1</i>", text)
    if strict and re.search(r"\*\*|(?<!\*)\*(?!\*)", text):
        raise RenderError(f"unconsumed asterisk: {text[:70]!r}")

    for i, span in enumerate(spans):
        text = text.replace(f"{_SENTINEL}{i}{_SENTINEL}", span)
    return text


# ---------------------------------------------------------------------------
# block
# ---------------------------------------------------------------------------
_H = re.compile(r"^(#{1,6}) +(.*)$")
_HR = re.compile(r"^-{3,}$")
_UL = re.compile(r"^- +(.*)$")
_OL = re.compile(r"^(\d+)\. +(.*)$")
_CONT = re.compile(r"^ {2,3}(\S.*)$")
_PRE = re.compile(r"^ {4,}(.*)$")
_ROW = re.compile(r"^\|(.*)\|$")
# A SEPARATOR MUST CONTAIN A DASH. Without that, `| | |` — a two-column table
# whose header cells are deliberately blank, which the first case file opens
# with — matched as a separator, the table branch declined it, and the
# paragraph branch then refused to parse it.
_SEP = re.compile(r"^\|[\s:|-]*-[\s:|-]*\|$")
_QUOTE = re.compile(r"^> ?(.*)$")


def _cells(line: str) -> list[str]:
    return [c.strip() for c in _ROW.match(line).group(1).split("|")]


def _aligns(sep: str) -> list[str]:
    out = []
    for c in _cells(sep):
        out.append("right" if c.endswith(":") and not c.startswith(":")
                   else "center" if c.startswith(":") and c.endswith(":")
                   else "left")
    return out


def _slug(text: str) -> str:
    """A stable anchor id, so a section of a case file can be linked to."""
    plain = re.sub(r"[`*]", "", text)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", plain.lower())).strip("-")


def render(md: str, strict: bool = True) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i, n = 0, len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if line.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            if i >= n and strict:
                raise RenderError("unclosed ``` fence")
            i += 1
            out.append("<pre>" + "\n".join(buf) + "</pre>")
            continue

        m = _H.match(line)
        if m:
            level = len(m.group(1))
            body = inline(m.group(2), strict)
            out.append(f'<h{level} id="{_slug(m.group(2))}">{body}</h{level}>')
            i += 1
            continue

        if _HR.match(line):
            out.append("<hr>")
            i += 1
            continue

        if _PRE.match(line):
            buf = []
            while i < n and (_PRE.match(lines[i]) or not lines[i].strip()):
                if not lines[i].strip() and not (i + 1 < n and _PRE.match(lines[i + 1])):
                    break
                buf.append(html.escape(_PRE.match(lines[i]).group(1))
                           if _PRE.match(lines[i]) else "")
                i += 1
            out.append("<pre>" + "\n".join(buf).rstrip() + "</pre>")
            continue

        if _ROW.match(line) and not _SEP.match(line):
            head = _cells(line)
            if i + 1 < n and _SEP.match(lines[i + 1]):
                aligns = _aligns(lines[i + 1])
                i += 2
                cols = "".join(
                    f'<th style="text-align:{aligns[k] if k < len(aligns) else "left"}">'
                    f"{inline(c, strict)}</th>" for k, c in enumerate(head))
                rows = [f"<tr>{cols}</tr>"]
            else:
                # A table with no separator row is a mistake, not a table: every
                # renderer treats it differently and the published page would be
                # wrong in a way nobody notices.
                if strict:
                    raise RenderError(f"table has no |---| separator: {line[:70]!r}")
                aligns, rows, i = ["left"] * len(head), [], i + 1
            while i < n and _ROW.match(lines[i]) and not _SEP.match(lines[i]):
                cells = _cells(lines[i])
                rows.append("<tr>" + "".join(
                    f'<td style="text-align:{aligns[k] if k < len(aligns) else "left"}">'
                    f"{inline(c, strict)}</td>" for k, c in enumerate(cells)) + "</tr>")
                i += 1
            out.append("<table>" + "".join(rows) + "</table>")
            continue

        if _QUOTE.match(line):
            buf = []
            while i < n and _QUOTE.match(lines[i]):
                buf.append(_QUOTE.match(lines[i]).group(1))
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf).strip(), strict)}</blockquote>")
            continue

        if _UL.match(line) or _OL.match(line):
            ordered = bool(_OL.match(line))
            items: list[str] = []
            while i < n:
                m = _OL.match(lines[i]) if ordered else _UL.match(lines[i])
                if not m:
                    break
                text = m.group(2) if ordered else m.group(1)
                i += 1
                # continuation lines are indented 2-3 spaces and belong to the item
                while i < n and _CONT.match(lines[i]) and not _PRE.match(lines[i]):
                    text += " " + _CONT.match(lines[i]).group(1)
                    i += 1
                items.append(f"<li>{inline(text, strict)}</li>")
                while i < n and not lines[i].strip():
                    nxt = lines[i + 1] if i + 1 < n else ""
                    if (_OL.match(nxt) if ordered else _UL.match(nxt)):
                        i += 1
                    else:
                        break
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue

        # paragraph: consecutive non-blank lines that start nothing else
        buf = []
        while i < n and lines[i].strip():
            nxt = lines[i]
            if (_H.match(nxt) or _HR.match(nxt) or _ROW.match(nxt) or _UL.match(nxt)
                    or _OL.match(nxt) or _PRE.match(nxt) or _QUOTE.match(nxt)
                    or nxt.startswith("```")):
                break
            buf.append(nxt.strip())
            i += 1
        if buf:
            out.append(f"<p>{inline(' '.join(buf), strict)}</p>")
        else:
            if strict:
                raise RenderError(f"cannot parse line {i + 1}: {lines[i][:70]!r}")
            i += 1

    return "\n".join(x for x in out if x)


def headings(md: str) -> list:
    """(level, text, anchor) for every heading — the viewer's contents list."""
    found = []
    for line in md.replace("\r\n", "\n").split("\n"):
        m = _H.match(line)
        if m:
            found.append((len(m.group(1)), re.sub(r"[`*]", "", m.group(2)), _slug(m.group(2))))
    return found


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        print(render(fh.read()))
