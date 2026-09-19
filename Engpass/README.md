# Engpass — a register of obstacles

*German for a **bottleneck** — literally a narrow pass. Named 2026-08-26,
replacing **Engpass** ("uncharted territory"), which was recorded from the start
as a placeholder and which described only the open-question half of what this
holds. **The new name names the function rather than the content**: the register
exists to find the binding constraint and rank by what clearing it would release.*

***`FND-O-NNNN` identifiers did NOT change.*** An ID is permanent and is what an
outside citation should resolve against, and the same rule holds for
Nordstern's `FND-D`/`FND-A` ids. The directory `questions/` became `obstacles/`,
matching Nordstern's own link field (`blockers[].obstacles`), which had been
inconsistent since the first pass found that most of these are not questions.

**It also moved**, from a sibling directory to `Nordstern/Engpass/`, because the
two registers are published together. **That is a publishing convenience and
changes nothing about the dependency** — see rule 1 below, which is now enforced
by `test_boundary.py` rather than by good intentions.

Nordstern asks, per disease, **do we understand it** and **can we do anything
about it**. Engpass asks the other half: **what is in the way, and how much does
each obstacle hold up?**

**It is not only open questions**, and the data forced that. Five Nordstern
records independently record *the drug supply depends on a corporate donation
that could stop* — one obstacle, written five times, connected by nothing. The
non-knowledge blockers cluster at least as hard as the knowledge ones, so `kind`
tracks Nordstern's blocker kinds: `mechanism` · `entity` · `capability` ·
`measurement` · `tooling` · `epidemiology` · `economic` · `manufacturing` ·
`regulatory`.

    python3 check.py          # the derived tables
    python3 check.py --json   # obstacles + their derived disease lists
    python3 test_boundary.py  # asserts Nordstern still does not know this exists

## Why it is a second register and not more fields

Because the link is many-to-many and the interesting direction is backwards.

A disease record can name several questions — 24 of Nordstern's 42 knowledge
blockers ask more than one thing, which is why the link is a list. And one
question blocks many diseases: `who-progresses` is cited by thirteen records
that look unrelated until they are put side by side.

Nordstern can say *this disease is blocked by that question*. Only a second
register can say **answering this would unblock these thirteen**, which is the
form the question *what should we work on next* actually needs.

## Bottom-up and top-down, and the difference is recorded

**Bottom-up** records earn their disease list: a Nordstern blocker cites them, so
somebody rating that disease said this is what they were waiting on. That link is
**derived**, and it is evidence.

**Top-down** records — *"if we understood how RNA folds, that would unblock X"* —
have no such link. The claim may simply be wrong, and this is the hard part of
the whole idea: **you often cannot know what answering a question buys until you
have answered it.**

The register does not dodge that. It stores those assertions as `claims`, each
carrying Nordstern's `standing` vocabulary — `alleged` · `documented` ·
`disputed` · `refuted` — which exists precisely to test a widely-repeated
assertion rather than echo it. **When a question is answered, its `alleged`
claims become `documented` or `refuted`, and that is a record of whether the
field's intuitions about payoff were any good.**

Marburg is the standing warning. Its reservoir *was* identified, everybody
expected that to unblock something, and what followed was advice to miners. Under
this machinery that claim would have been `alleged` in 1970 and `refuted` now.

`rna-folding` is the first top-down record and every one of its four claims is
`alleged`. `check.py` errors if a claim names a disease that already cites the
record — that link is derived, not claimed, and storing it twice lets them drift.

## Append-only, and why

Both registers are **append-only**. A record is never deleted and its `id` is
never reused, because the point of a public dataset is that a citation keeps
resolving — including one made by somebody who is no longer reading.

| field | what it is |
|---|---|
| `slug` | the human handle. Readable, and therefore tempting to rename |
| `id` | `FND-O-0007`. Opaque, sequential, permanent. **What an outside citation resolves against** |
| `resolution` | how far along the *question* is — `open` · `partly-answered` · `answered` · `dissolved` |
| `deprecated:` | absent on a live record. Its presence is what makes the record deprecated |
| `deprecated.see` | **the 302.** Optional — absent means *simply no longer needed*, a 410 |

`status` (`active` / `deprecated`) is **derived from the presence of the block**,
never stored beside it, so the two cannot disagree. Same rule as `capability` in
Nordstern.

A deprecated record stays in the repository, stays in `--json`, and drops out of
every derived table. In Nordstern the same machinery hides it from search unless
asked for: `status:deprecated` shows only those, `status:any` shows everything,
and `id:FND-D-0007` resolves a citation directly.

**The reasons this will be needed**, none of them hypothetical: a better frame
arrives and one record becomes two; MONDO merges a term out from under a record;
an obstacle turns out to have been three obstacles. Renaming a slug or deleting
a file would break every reference. Deprecating in place does not.

*(The `FND-Q-` ids these records were minted with became `FND-O-` when the
register turned out to hold obstacles rather than questions. That is a renumber,
which the rule forbids — permitted exactly once, hours after minting and before
anything outside this repository had ever seen them. It would not be permitted
now.)*

## The three rules

**1. The dependency runs one way.** Nordstern does not know Engpass exists. It
records a list of slugs on a blocker and nothing else; `check.py` here reads
Nordstern's built artifact and reconciles. Same rule as Strangschrift and
Sperrwerk — *neither tool imports the other, a text file is the whole interface.*
The single `import` is Nordstern's YAML loader, rather than carrying a second
copy of it. A loader, not a model.

**2. The disease list is derived, never stored.** A question does not declare
what it blocks. If it did, the two files could disagree, and a question could
claim to block something the disease record does not cite. **Nordstern is truth
for the link**, because the blocker is a claim about that disease made by
whoever rated it. A question may mention unrecorded diseases in prose; they do
not count.

**3. Every question must say what becomes possible if answered.** `check.py`
errors without it. This is not tidiness — it is the whole difference between a
register and a list of things nobody knows:

> Ebola's record filed its unknown reservoir as the headline knowledge blocker,
> reasoning that identifying it would allow action before the first human case.
> **Marburg's reservoir is established** — Egyptian rousette bats, infectious
> virus isolated from wild colonies, outbreaks traced to named caves and mines.
> What followed was advice to miners. No product, no surveillance system, no
> capability.

*(Nordstern gaps.md #101.)* **"Nothing much" is a legal answer**, and recording
it is the point.

## What the passes have found

*Current, against 103 Nordstern records. The first pass ran against 48.*

| question | kind | records | deaths/yr | blocked **only** by this |
|---|---|---|---|---|
| who-progresses | mechanism | **29** | 37.8M | 20 |
| burden-unknown | epidemiology | 11 | 0.24M | 7 |
| pathogen-persistence | mechanism | 10 | 2.6M | 6 |
| unexplained-illness | entity | 8 | **0** | **8 of 8** |
| tissue-repair | capability | 6 | 19.1M | 3 |
| donation-dependency | economic | 6 | 0.06M | 0 |
| **cell-targeting** | capability | **4** | **0.014M** | **3 of 4** |
| rna-folding | mechanism | 0 | 0 | — *(top-down)* |

**`cell-targeting` is the newest and it arrived from a conversation rather than
from the corpus** — proposed as *"drugs go everywhere, so you need one that isn't
toxic, and that may not exist"*. Checking it against the records found the
sharper version already written in `msmds`: **"What does not exist is delivery —
no modality reaches vascular and visceral smooth muscle throughout the body at
therapeutic dose. So the conceptual route is open and the physical route is
not."**

**Three of its four records are blocked by nothing else** — `sickle-cell`,
`cystic-fibrosis` and `duchenne`, which is three of the register's four monogenic
records. Their genes were found in 1957, 1989 and 1986. **The variable that
separates them from the diseases that got treatments is not understanding; it is
whether anybody can reach the tissue**, which is Nordstern gaps.md #193 and #198
given a name and a slug.

**It is also the entry most likely to falsify this register's headline claim.**
Every other knowledge obstacle here carries `scale: null` on the argument that
knowledge cannot be triaged with money. **Delivery modalities are engineering** —
capsid libraries, nanoparticle screens, conjugate chemistry — and that is
parallelisable, buyable work. If any obstacle in this file has a price, it is
this one, and none of the records citing it has put a number on it. The record
says so in its own `holes`.

**Note the name.** It is not `drug-delivery`, because Nordstern already uses
"delivery" for getting a product to a patient — `tuberculosis` says *"Everything
else here is delivery"* and `hiv` says *"no amount of delivery funding touches
it"*. Sharing the word would have merged the register's most-priced obstacle with
one of its least priceable.

**The last column is the one to read.** *Blocked only by this* means every
knowledge blocker on that record cites this question and no other — answer it
and nothing scientific remains in the way.

By that measure the leader is **`unexplained-illness`**: six of its seven
records are blocked by nothing else, and it carries **zero attributed deaths.**
Any mortality-weighted ranking makes the clearest scientific gap in the corpus
invisible. That is Nordstern gaps.md #88 and #104 arriving in a new place, and
it is an argument for ranking questions by **records** rather than by burden.

The two large-mortality rows are large because they contain ischaemic heart
disease, stroke and COPD — not because the questions are deeper.

## The untagged pile is a finding, not a backlog

Eight knowledge blockers carry no question, and seven of them are **not open
questions at all**:

> a vaccine that prevents adult pulmonary tuberculosis · a second drug for
> schistosomiasis · an antifungal for eumycetoma · a regimen for all four
> helminth species · in vivo gene editing for sickle cell · a cure for PKU

*Nobody has made the drug* is a different object from *nobody knows how this
works*, and several of these are `no-sponsor` wearing a lab coat. **This is a
Nordstern schema change that Engpass surfaced** — splitting `knowledge` into
`mechanism-unknown` and `no-candidate` — and it is not yet made. Rabies is the
one genuine unnamed question in the pile.

**AMENDED 2026-08-25 — THE SPLIT NEEDS A THIRD ARM, AND IT CHANGES THIS
REGISTER'S HEADLINE FINDING.** Nordstern's `cystic-fibrosis` and
`spinal-muscular-atrophy` records are a controlled comparison: CFTR was cloned in
1989 and SMN1 in 1995, both had an obvious gene-therapy route, and one worked and
one did not. **The variable was not understanding — it was whether the vector can
reach the cell.** Motor neurons are post-mitotic and reachable by an intravenous
AAV in an infant; airway epithelium sits behind mucus, neutralises repeat dosing
and turns over.

That is an engineering problem, and **engineering problems have prices.** So the
split should be three-way — `mechanism-unknown` · `no-candidate` ·
**`delivery-unsolved`** — and the third arm is costable, schedulable and buyable
in a way the first is not.

**Which qualifies the finding this register was built on.** *Zero of the
knowledge blockers carry a price — categorically the ones money cannot triage*
is the most-quoted line in this README and it is right about the residue and
wrong about the category. Applying the test — *if you had unlimited money, is
there a programme somebody could run?* — moves several of Nordstern's 84
knowledge blockers into a priceable class: CF's airway delivery, Parkinson's
missing progression biomarker, sepsis's absent endotype partition,
schizophrenia's unmeasurable negative-symptom endpoint. See Nordstern gaps.md
#193.

## Open decisions

- ~~**The name.**~~ **Settled 2026-08-26: Engpass.** See above.
- **Whether `burden-unknown` belongs here at all.** It is epidemiology, not
  biology, and unlike the other four it is answered with money rather than
  discovery — which makes `scale: null` wrong on every blocker citing it.
- **The granularity rule.** Currently proposed: *a question earns a record when
  at least two disease records cite it.* `check.py` warns below that threshold.
  This makes the corpus the arbiter rather than an author.
- **Whether these are really single questions.** `unexplained-illness` groups
  depression with hEDS on the structural ground that both are defined by
  criteria rather than mechanism. It will probably split. The register expects
  that and each record says so in its own `holes`.
