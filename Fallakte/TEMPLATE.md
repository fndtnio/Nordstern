# The case file template

Copy `cases/polycythaemia-vera/` and replace. Sections are in this order because
it is the order a stranger needs them in. **A section with nothing in it stays,
holding the sentence that says so** — an empty section is a statement about the
field, and deleting it makes the file look finished when it is not.

---

## The split, and it is enforced

**`case.yaml` holds nothing a person would rather read.** Ids, links, paths,
dates and statuses: the things a checker can verify. **`README.md` holds
everything else.** Nothing is stored in both.

The first version of this register put a model's `shows`/`refuses`, each
question's text, the asks and the whole log inside the YAML, where prose goes to
die in an eighty-column gutter. `check.py` now enforces the split **in both
directions**:

- It **rejects** the prose keys if they come back (`shows`, `refuses`, `ask`,
  `would_move`, `asks`, `log`, `routes`, `role`, `what`), naming the README
  section each belongs in.
- It **fails** if a question id or a model path in the spine is never discussed
  in the README. *A question with a status and no text is a number, not a
  question. A model listed with no prose is a citation, not a case file.*
- It **fails** if the README carries no entry dated `updated`. The log lives in
  the README; the spine points at its newest date.

`one_line` is the single exception, capped at a sentence, because a register
listing needs something to show.

## `case.yaml` — the spine

```yaml
slug: <same as the Nordstern slug>
id: FND-C-0001              # PERMANENT. Next number, never reused.
disease: <nordstern slug>   # must resolve in Nordstern's built artifact
disease_id: FND-D-0145      # must match that record's id
opened: 2026-10-10
updated: 2026-10-10         # the newest log date, which must appear in README
status: active              # active | dormant | closed

one_line: >
  Why this case is open, in one sentence a register listing can print.

working_with:
  - kind: nonprofit         # nonprofit | clinic | academic | patient-org | company | individual
    named: false            # has this partner agreed to appear in a public repo?

obstacles: [who-progresses] # Engpass slugs this case is working on

models:                     # OUR artifacts. Paths are checked; so is discussion.
  - tool: Strombild
    ref: ../../../../strombild/examples/clonal-escape.strombild
    access: repo            # live | repo | private  — see below
    # live: https://...     # REQUIRED when access is `live`, forbidden otherwise

questions:                  # the id and its state; the question itself is prose
  - id: Q1
    status: open            # open | partial | answered | abandoned
    obstacles: [who-progresses]
```

**`access` IS NOT A BOOLEAN, and it used to be.** `published: true` turned out to
mean three different things at once: the repo is public, the playground on the site
is current, and a reader can click it. Those came apart immediately — the site's
playgrounds were a sync behind every model in the first case file, so a boolean
would have told readers they could open eleven things they could not open any of.

| `access` | means |
|---|---|
| `live` | openable on the public site today. **`live:` must give the URL** |
| `repo` | the source is public; the playground on the site is behind it |
| `private` | neither. It exists in-tree and nowhere a reader can reach |

A `live:` URL on anything but `live` is an error, because **a link a reader cannot
follow is worse than no link.**

**BLOCK MAPPINGS ONLY.** Nordstern's bounded loader does not read inline flow
mappings (`{tool: x, ref: y}`) and hands them back as strings. It does not
complain, and the checker then sees ten strings where it expected ten mappings.

---

## `README.md` — the sections, and what each is for

**0. Terms.** Link `GLOSSARY.md` and define only what is specific to this
disease. **Do not redefine a shared term locally.** If the case needs a term the
glossary lacks, add it to the glossary. `check.py` warns on a case file that
never links the glossary, and errors on one that uses a retired term.

**1. Where it stands.** Three or four lines, then the citation. Capability,
delivery, and the blockers, read off the Nordstern record, **never re-rated
here**. A reader has to know whether this is an unsolved mechanism or an
undelivered cure before anything else makes sense.

**2. The mechanism, step by step.** The heart of the file, and the reason the
register exists. A numbered chain, one step per row, each carrying:

| | |
|---|---|
| **what changes** | the actual event, in the smallest terms that are true |
| **status** | `established` · `partial` · `open` — the same vocabulary as the record's `mechanism` axis, applied *per step* |
| **where you can watch it** | the model, or empty |

Two rules. **No step may be a verb like "promotes" or "modulates" standing
alone** — say which thing moves where, or mark the step `open`. And **an empty
model column is left empty**, because that is the list of things worth building.

**3. What we got wrong.** Dated, kept, never edited away. The file's credibility
rests on this section more than on any other.

**4. Open questions.** Numbered to match `case.yaml`, each with what an answer
would change, and each pointing at an Engpass obstacle where one exists. A
question with no obstacle is either new, or not really an open question.

**5. Models and data.** Ours, by tool, each with what it shows and what it
refuses. Then other people's: datasets, cohorts, registries, published models,
and the tools that can be pointed at this disease. **Say what each one buys and
what it does not.** A protein structure predictor buys geometry; it does not buy
mechanism, and a case file that lists it without saying so is misleading.

**6. Detection.** How it is found, how it is missed, what the miss costs, and
what could be built. The most common thing a case file discovers is that the
test exists and the question is not asked.

**7. Treatments.** The current ladder. For each, the one distinction that has
turned out to matter: **does it act on the stock or on the edge?** Taking blood
out lowers a number and changes nothing about why the number rose. Lowering the
clone changes the mechanism. A ladder that does not separate those two is
describing care, not strategy.

**8. Routes.** Candidate interventions, each with a falsifier. **A route without
a falsifier is a wish** — write what result would kill it, or do not write it.

**9. How to help.** The `asks` from the spine, in prose, with a way to make
contact.

**10. Log.** Dated, append-only. What happened and what changed.

**11. Sources.** Pointers with resolvable identifiers, and **a mark on every one
that has not actually been read.** Nordstern requires an identifier, a date and a
verbatim quote for a sourced scalar; a case file is not held to that, so the
compensating rule is that an unread source says so. A list in which everything
looks equally solid is worse than no list.

---

## The rule that cost the most to learn

**AN ASK IS A CLAIM.** "Nobody has measured this" has exactly the same standing
as any other assertion in this project, and Engpass's vocabulary applies to it:
`alleged` until checked. The first case file published an ask for data that
already existed in two published cohorts, and it survived four hours.

So before writing anything into `asks`, search for it. And when the search finds
that it was done, **the correction goes in section 3 with its date** rather than
quietly replacing the ask, because the mistake is more instructive than the fix.
