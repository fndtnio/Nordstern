# A register of open questions — design note, not yet built

Jeremy's proposal, 2026-08-23: progress is not only a disease count. What blocks
a disease matters as much, and the biggest **open questions in biology** are
themselves a list worth holding as data. The two registers feed each other —
*disease X is blocked by question Y*, and *answering Y would unblock these N
diseases.*

This note records what the existing corpus says about that idea, the decisions it
forces, and what to build first. **Nothing here is built.**

---

## What 48 records already say

### 1. Most of what blocks medicine is not an open question in biology

```
179 blockers across 48 records
  knowledge        42  (23%)
  everything else 137  (77%)   logistics 35 · diagnosis 31 · policy 22 ·
                               no-sponsor 15 · evidence-incomplete 10 ·
                               cost 7 · tooling 7 · manufacturing 4 ·
                               adherence 3 · regulatory 2 · candidate-untested 1
```

A questions register addresses **under a quarter** of what the corpus records as
standing in the way. That is not an argument against building it — it is the size
of it, and it should be stated up front rather than discovered later.

Two things cut the other way and both matter:

- **`scale: null` on 42 of 42.** Not one knowledge blocker in the register has a
  price. They are categorically the ones money cannot triage, which is exactly
  why they need a different instrument from the delivery blockers.
- **Only one record is blocked *solely* by knowledge** — Huntington's. Everywhere
  else, answering the question still leaves a delivery problem behind it.

The register's own warning applies: the 4:1 ratio is partly a **sampling
artefact**, since several records were added specifically to exercise the
delivery axis. It should be recomputed at 100 records before anyone quotes it.

### 2. Forty-two blockers are about five or six questions

Read together rather than one record at a time, the knowledge blockers collapse
hard. Rough clustering, with the mortality of the records citing each:

| deaths/yr | records | the question |
|---|---|---|
| ~19.3M | 10 | **Why this person and not that one?** — same exposure, same infection, and some progress. COPD susceptibility · which plaque ruptures · which child crosses into noma · who gets a leprosy reaction · who develops PKDL · who recurs after trachoma treatment · which third of Chagas patients ever gets ill |
| ~19.1M | 6 | **Can destroyed tissue be repaired?** — myocardium, brain, alveolus, bowel wall, striatum |
| ~0.7M | 7 | **Why does the pathogen survive treatment?** — HIV latency, adult filarial worms, hydatid cysts, filovirus persistence in the eye and testis |
| ~0.15M | 7 | **How many are there, and how does it spread?** — epidemiology and surveillance, not biology |
| **0** | 7 | **What is actually wrong in these people?** — ME/CFS, hEDS, POTS, MCAS, low back pain, depression, bipolar |

**Nine or ten records asking one question is the finding.** The register has been
recording it forty-two separate times, in forty-two different phrasings, with no
way to see that they are the same thing.

Two cautions about the table, both important:

- **The top two rows are large because they contain ischaemic heart disease,
  stroke and COPD**, not because the questions are deeper. Burden-weighting a
  question inherits every problem #48 already has with burden-weighting a
  disease.
- **The bottom row has zero deaths and is the purest open question in the
  register.** Seven records where nobody can say what is physically wrong with
  the patient. A mortality-ranked view makes the clearest scientific gap in the
  corpus invisible, which is #88 and #104 arriving in a new place.

### 3. `knowledge` is doing at least three jobs

Roughly a quarter of the 42 are **not open questions at all** — they are missing
products:

> a vaccine that prevents adult pulmonary tuberculosis · a macrofilaricide · a
> drug that kills the adult worm and can be given in a village · an antifungal
> that works for eumycetoma · a second drug for schistosomiasis · an antiviral
> for dengue · a regimen that works on all four helminth species

"Nobody has made the drug" is a different object from "nobody knows how this
works", and the distinction decides which register the blocker belongs in. Some
of these are blocked by science; several are blocked by **no market**, and are
`no-sponsor` wearing a lab coat.

**This is a Nordstern schema change that the second register would force**, which
is the corpus-before-schema rule working as intended. Candidate split:

| kind | meaning | goes to |
|---|---|---|
| `mechanism-unknown` | nobody knows what is happening | the questions register |
| `no-candidate` | the mechanism is known, nothing has been built | Nordstern, priced |
| `candidate-untested` | something exists, nobody ran the trial | Nordstern, priced (exists already) |

---

## Decisions this needs before anything is built

### A. Top-down or bottom-up? — **recommend bottom-up**

"The biggest open questions in biology" is a *Science*-125 kind of list: how does
memory work, what is consciousness, how did life begin. Interesting, and
**an opinion nobody can argue with** — which is the exact thing Nordstern refuses
to do with the word "solved".

The corpus-derived list is different, smaller, and defensible: *these are the
questions that are demonstrably blocking records we hold.* Every entry arrives
with the diseases that forced it, the same way every gap in `gaps.md` names the
record that forced it.

Start there. If a great curiosity-driven question turns out to block nothing, the
register should be able to say so — and that is more interesting than omitting it.

### B. Every question must say what becomes possible if answered — **non-negotiable**

This comes straight out of `gaps.md #101`, which Marburg forced:

> Ebola's record filed the unknown reservoir as its headline knowledge blocker,
> reasoning that identifying it would let you act before the first human case.
> **Marburg's reservoir is established** — Egyptian rousette bats, virus isolated
> from wild colonies, outbreaks traced to named caves. What followed was: tell
> miners. No product, no surveillance system, no capability.

**A knowledge question can be answered and change nothing.** Without a
`what_it_unblocks` field, a questions register is an infinite list of things
nobody knows, which is not a register, it is a mood.

The honest values include *nothing much*, and recording that is the point.

### C. What is the unit? — the hardest one, unresolved

Nordstern's founding rule is **"disease IDs are borrowed, never minted"** —
MONDO exists, is open, and already merges DOID/OMIM/Orphanet/ICD. **There is
nothing to borrow for open questions.** This would be the first time the project
mints entity identifiers rather than assertion identifiers, and that is a real
commitment with a permanent maintenance cost.

The granularity problem is worse than it looks. All three of these are "open
questions" and none of them is the same kind of object:

- *Why does a chronic plaque suddenly rupture?* — a mechanism
- *What is wrong in ME/CFS?* — an entity-shaped hole
- *Can adult human myocardium be made to regenerate?* — a capability target

A rule is needed before the first record, not after the twentieth. The candidate
worth trying: **a question earns a record when at least two disease records cite
it.** That makes the corpus the arbiter of granularity, keeps the list finite,
and means the first version can be *derived* rather than authored.

### D. Naming

Deferred, deliberately. Nordstern's own name changed once, because the first
name described the artefact and the second described the work. Do not name this until
it is clear whether it is a register of *questions*, of *obstacles*, or of
*what the process must produce* — those are three different projects.

---

## What to build first — one afternoon, no new schema

**A derived view, not a new register.** `check.py` already holds every knowledge
blocker. A `--questions` report could:

1. Group knowledge blockers by hand-assigned cluster tags added to the existing
   records — one new optional field, `blockers[].question: <slug>`.
2. Emit, per cluster: the diseases citing it, their combined burden, their
   combined `reach`, and how many are blocked *only* by that question.
3. Report the questions that block the most **records**, not the most deaths —
   because of the caution in §2, and because the zero-mortality cluster is the
   most purely scientific one in the corpus.

That is enough to test whether the idea earns its own database. If the derived
view is useful, the register is worth building; if the clusters do not hold up
under a real tagging pass, better to find out from one field than from a schema.

**And it answers the question this project exists to answer** — *based on the
data, what should the next project be* — in a form nothing currently can:
not *which disease*, but *which question, and how much does it unblock.*

---

## The honest summary for fndtn's thesis

If the goal is a process that solves medicine, this corpus currently says:

- **~23% of what blocks the diseases in it is an open question in biology.**
- **~77% is delivery, money, policy, regulation and manufacturing** — and those
  have prices, which means they are triable with resources rather than with
  discovery.
- **The knowledge blockers are the ones no amount of money resolves**, so they
  need a different instrument, which is what this register would be.
- The single largest cluster is **"why this person and not that one"** — and it
  is a measurement question as much as a biological one, which points back at
  Nordstern's own `prognostic` axis rather than away from it.

Both halves are the process. Neither register is the whole of it.
