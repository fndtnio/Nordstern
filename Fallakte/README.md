# Fallakte — a register of case files

*German for a **case file** — the folder a case worker keeps open on one subject.
Started 2026-10-10 with `polycythaemia-vera`, the first disease anyone actually
began working on.*

**The name is provisional.** `FND-C-NNNN` identifiers are not: an id is permanent
and is what an outside citation resolves against, the same rule that holds for
Nordstern's `FND-D`/`FND-A` and Engpass's `FND-O`. Renaming the directory is
cheap for as long as nothing has been cited; renumbering is never cheap.

Nordstern asks, per disease, **do we understand it** and **can we do anything
about it**. Engpass asks **what is in the way**. Fallakte asks the fourth
question, and it is the only one of the four that is about us:

> **What are we actually doing about this one, what have we found, and what do we
> still not know?**

    python3 check.py          # validate every case file and its links
    python3 check.py --json   # the cases, machine-readable
    python3 test_boundary.py  # asserts Nordstern and Engpass still do not know this exists

## Why it is a third register and not more fields on the record

**Because a Nordstern record is a verdict and a case file is a workspace.**

A record says where a disease stands, rated on a date, by somebody who signed the
assertion, and it is append-only so that a citation keeps resolving. It is
deliberately hard to change. A case file is the opposite thing: notes that grow
weekly, half-answered questions, models that turn out to be wrong, a log, and a
list of things a stranger could pick up. Putting the second inside the first
would either bloat the verdict or freeze the workspace, and the first failure is
the dangerous one — a record that changes every week is not citable.

So the direction of reference is fixed and one-way:

1. **A case file points at a record. A record never points at a case file.**
   Nordstern does not read this directory, does not validate it, and does not
   know it exists. `test_boundary.py` asserts that rather than trusting it. This
   is the same rule Engpass lives under, for the same reason: the register has to
   stand alone.
2. **A case file never re-states a rating.** Where it needs the axes it cites the
   record. If the case file disagrees with the record, that disagreement is a
   finding and belongs in the log — and then in a re-rating, in Nordstern, with a
   new `FND-A` number.
3. **Most diseases will never have one**, and that is the signal. A case file
   exists where work has started. The register holds 146 records; this directory
   holds the ones somebody is carrying.

## What a case file is for

Two readers, and they want opposite things.

**Someone who might help.** They arrive from a search, know nothing, and need the
mechanism, the open questions, and a concrete ask, in that order, in ten minutes.

**Someone who knows the disease better than we do** — a clinician, a researcher,
the nonprofit we are working with. They will find our errors. The file is built
to make that easy: **every step of a mechanism is marked for whether it is
established, partial, or open, and every model says what it refuses to claim.**
A case file that is wrong in a markable place is doing its job. A case file whose
confident prose hides which half is guessed is not.

## The vocabulary rule

**A term defined loosely is worse than a term left out**, and the first case file
proved it inside a day. Its comparison table used *relevant cells* and *disease
at birth* as though both were obvious. Neither is. *Relevant to what?* hid the
fact that the answer is a different cell type per disease, and *disease at birth*
collapsed four separate questions — is the defect present, are the cells
misbehaving, would a test show it, is the person being harmed — which for most
genetic conditions have different answers.

So `GLOSSARY.md` defines the terms **once, for every case**, and each entry says
what the term does NOT mean, because in this vocabulary the near-miss is the
problem rather than the blank. A case file uses those definitions or adds to the
glossary; it does not redefine a term locally. Retired terms are listed there and
`check.py` **rejects a case file that uses one**, while allowing it to be named in
quotes, so the explanation of the retirement does not trip the guard that exists
because of it.

**The reader this is for is somebody new to the field.** They are the person most
likely to notice that a sentence does not actually say anything, and the least
likely to say so.

## The rule the whole thing rests on

**"This happens, then this."** Prose about one thing promoting another and
another thing tamping it down reads as understanding and cannot be checked. A
case file's mechanism section is therefore a numbered chain, one step per line,
and each step carries three things: what changes, whether we know it, and where
you can watch it happen.

Where a step has no model, the file says so and leaves the column empty. **An
empty column is the most useful thing in the file** — it is a piece of work
somebody could do this month.

## Layout

    Fallakte/
      README.md                  this
      TEMPLATE.md                the base template, and what each section is for
      GLOSSARY.md                terms, defined once, for every case
      check.py                   validation, and --build
      render.py                  markdown -> HTML, for the subset the cases use
      test_boundary.py           the one-way dependency, asserted
      test_check.py              link rewriting, which only matters once public
      test_render.py             the renderer, and that it cannot inject HTML
      cases/<slug>/
        case.yaml                the spine: ids, links, paths, dates, statuses
        README.md                the case file itself, and all of its prose

    ../web/                      written by --build, published with the register
      fallakte-data.js           the artifact: spines + rendered documents
      fallakte.html              the landing page — the list of open cases
      case.html                  the viewer — ?case=<slug>
      fallakte.css               shared by both, because they are one kind of page
      fallakte.test.js           run by `node --test web/` with the others

## Publishing

    python3 check.py --build        # writes ../web/fallakte-data.js
    python3 test_render.py && python3 test_check.py && python3 test_boundary.py
    node --test ../web/             # the page tests run with Nordstern's
    ../serve.sh                     # then open /web/fallakte.html

The pages are **pre-rendered and script-tagged**, which is Nordstern's own rule
for `web/`: no `fetch()`, so every page also opens over `file://` and a case file
can be sent to somebody as a folder. The markdown is rendered by `render.py` at
build time, so the browser loads no library. **The renderer is strict** — syntax
it does not know is an error, not something passed through to be printed at a
reader as `**bold**` — and **links are rewritten**, because a case file links to
its neighbours the way a file does and those paths are dead once published.

To put it on the site: commit and push `web/`, then in `site/frontend` run
`./sync-projects.sh` (it vendors from GitHub, so the push comes first),
`node build.js`, `npm run sync`, and `./clear-cache.sh` for the CloudFront
invalidation. It lands under `projects/nordstern/app/`.

`case.yaml` holds what a machine should check — that the disease exists in
Nordstern, that every Engpass slug resolves, that every model path resolves, that
every question has an id something can cite. `README.md` holds everything a
person should read. Nothing is stored in both.

Working notes, reading, and anything not ready to be read by a stranger stay in
`private/`, which is gitignored. **The repo is the artifact, not the ramblings.**
