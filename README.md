# Nordstern

> **Experimental.** This is a schema under test, not a data source. 144
> diseases rated by hand, mostly from memory; 71 of roughly 2,400 empirical
> numbers carry a citation. The ratings are meant to be argued with. Nothing
> here should be cited as a fact about medicine without reading the record and
> its `src` fields first. See *Before citing anything* below.

*Nordstern* — **north star**. A fixed reference you navigate by and can take a
bearing against every year.

## Why it exists

Nobody has a definition of *solved* in medicine. Without one there is no way to
say what is left, no way to rank it, and no way to tell a year later whether
anything moved.

The enumeration of diseases already exists and is open (Mondo). The burden data
already exists (GBD). What does not exist is the column in between: for each
disease, **where does it stand?** This register is an attempt at that column,
built so that it can be re-measured. The loop it is meant to close is *measure
where we are, take something off the queue, solve it, re-measure*.

## What it is trying to do

Each record answers two questions and refuses a third:

- **Do we understand it?** — `mechanism`: established · partial · correlates · none.
- **Can we do anything about it?** — `intervention`, on a five-rung ladder:

| rung | meaning | example |
|---|---|---|
| `none` | nothing alters the course | ME/CFS |
| `symptomatic` | masks the phenotype | Huntington's |
| `disease-modifying` | slows, does not arrest | ALS |
| `suppressive` | near-normal life, **treated indefinitely** | HIV |
| `curative` | a **finite** intervention ends it | hepatitis C |

HIV and hepatitis C are both triumphs and not the same triumph. A register that
files them together cannot say what is left to do.

**It never stores whether a disease is "solved".** That verdict is *derived*
from the axes by `check.py`, because a stored verdict is an opinion that cannot
be argued with and a derived one is a calculation that can. The derivation
splits into **capability** (what medicine can do at its best) and **delivery**
(`efficacy × access`, the fraction of patients it actually reaches), so
hepatitis C reads *curable / barely delivered* rather than *solved*.

Around those two axes the schema carries what the records forced it to:

- **`toll`** — what the cure takes permanently, and **`residue`** — what the
  disease already took before the cure arrived. Together they answer *are they
  back to the state they were in before any of this?*
- **`window`** — where capability depends on catching it in time.
- **`measurement`** — three questions, not one: is it there, what will it do if
  left alone, will *this* treatment work in *this* patient.
- **`strata`** — where one entity spans the ladder (stage I breast cancer is
  cured, stage IV is not), so that "is it solved" is reported as a malformed
  question rather than averaged.
- **`blockers`** — what stands in the way, **who could move it**, and roughly
  what it would cost. Twelve kinds, from `knowledge` to `cost` to `policy`,
  chosen so that different blockers name different actors. Every blocker
  carries a `standing` (documented · alleged · disputed · refuted), because
  *"it's solvable but industry won't allow it"* is a common claim of unknown
  truth and the register's job is to test it, not echo it.
- **`moved`** — dated changes on an axis with a reason. This is what makes a
  second pass a comparison rather than a fresh opinion. Hepatitis C moved from
  disease-modifying to curative in about three years; sickle cell took
  seventy-five years from solved mechanism to approved cure.

Disease identifiers are **borrowed, never minted**: `mondo:` points at the Mondo
Disease Ontology. The only IDs Nordstern creates are for its own records
(`FND-D-NNNN`) and ratings (`FND-A-NNNN`), and the register is append-only, so
a citation keeps resolving.

`SCHEMA.md` is the full specification. `gaps.md` is the design log: every
schema decision, named for the record that forced it.

## How to use it

Zero dependencies. PyYAML is used if importable; otherwise a bounded loader
built in reads the records.

```bash
python3 check.py              # validate every record, print the derived tables
python3 check.py --json       # the whole register + every derived field
python3 check.py --build      # YAML -> web/ artifacts, and today's snapshot
python3 check.py --diff       # what moved between the two latest snapshots
python3 -m unittest test_check   # 127 tests
node --test web/                 # 119 tests: query language, tool, map
```

`--json` is what makes this a database rather than a document:

```bash
# Where would a nonprofit get the most for $10M?
python3 check.py --json | jq -r '.records[] | select(.derived.orphaned and
  (.derived.cheapest_priced_blocker // 1e99) <= 1e7) | .slug'
```

**The web pages** are static files built from the YAML and committed:

- `web/index.html` — **the map.** The derived state of the register as charts;
  every figure links to the query that produces it.
- `web/query.html` — **the tool.** A query bar over the whole register, with
  the spec at `?spec`. The query lives in the URL, so a view is a link.

```
capability:curable reach:<0.5            space means AND
-blocker.kind:knowledge                  a leading minus negates
blocker.standing:(alleged OR disputed)   alternation within one field
deaths:>100k  witness:"overdiagnosis"    comparisons with k/M/B; quotes carry spaces
lithium                                  no field = free text over the whole record
```

A wrong value answers with the valid ones rather than with zero rows.

**Adding a record.** Copy the shape of any file in `entities/`, read
`SCHEMA.md`, and run `check.py`. Every empirical number is a
`{value, units, src}` block; `units` are required, and `src` is either one of
three honest words (`recall` · `reasoning` · `unknown`) or a citation carrying
the quote it read. Then:

```bash
python3 resolve_mondo.py            # proposes a Mondo id; writes nothing without --apply
python3 check.py --markdown > index.md
python3 check.py --build
python3 mondo_sync.py               # checks every id against the live ontology
```

**Files.**

- `entities/*.yaml` — one record per disease. The data. CC BY 4.0.
- `SCHEMA.md` — the record format and the derivation rules. Read first.
- `check.py` — validation and every derived field, in one place.
- `index.md` — generated: the derived tables and the quadrant map.
- `gaps.md` — the design log.
- `resolve_mondo.py`, `mondo_sync.py`, `mondo.md`, `mondo-sync.md` — the join
  to Mondo: proposals a person confirms, and a ledger of what matched and
  against which release.
- `source_moved.py`, `moved-sources.md` — the first sourcing pass, against
  PubMed. The tool copies a quote out of a paper; it cannot compose one.
- `web/` — the map, the tool, the query language (`query.js`), the built
  artifacts, and their tests.
- `Engpass/` — a sibling register of *obstacles*, so that a blocker can say what
  open question it is waiting on, and the obstacle can say how many diseases
  answering it would unblock. It reads Nordstern's built artifact and nothing
  else.

## Before citing anything

Provenance is recorded, not assumed. Every empirical scalar says where it came
from, and most say `recall`: written from the author's memory, unverified.
`check.py` refuses a citation that does not carry the verbatim quote it read,
because a plausible DOI is exactly what a language model produces when it does
not know.

What a citation could even settle is tiered and reported on every build:
burden figures are **sourceable** (GBD publishes them); dated `moved` events
are **supportable**; and the axes themselves, the fraction of patients a
treatment works for and reaches, are **judged**. Nothing published holds those
numbers. They are the thing this register exists to supply, and a sourcing
pass that treats them as lookups will invent citations for them.

The ratings on the axes are the work product. The numbers are placeholders with
their weakness recorded. Disagree with a rating by opening a record and arguing
with its `witness`; that is what it is for.

## Method

Corpus before schema. Records were chosen for **structural diversity rather
than importance**, and the schema was extended only when a real record broke
it. Each such break is an entry in `gaps.md`, named for the record that forced
it.

## Licence

Code and documentation are **MIT** (`LICENSE`). The register itself, every
record under `entities/` and every obstacle under `Engpass/obstacles/`, is data
and is **CC BY 4.0** (`entities/LICENSE`). Cite a record by its permanent
`FND-D-NNNN` id and a rating by its `FND-A-NNNN` assertion id.
