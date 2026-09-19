# Buckets — a stable reading of the register

Feedback and a revision of a bucket sketch (an unpublished working note), which stays as the sketch.

**The idea is right and most of it already exists.** Eleven of the thirteen
proposed buckets map onto fields the register has been carrying for months. What
the sketch adds is not new data — it is the **naming**, which is the part that
was missing, and it is what turns nine charts into one readable statement.

---

## The one structural problem: this is three axes wearing one list

The sketch flags "might be duplicate" twice, and **both flags are the same
mistake in different places** — a bucket from one axis colliding with a bucket
from another:

- *"Get it — short window"* duplicates *"game over if not detected"* because a
  **window is a modifier on what happens to you, not a state of its own.**
- *"Not sure of the right path"* duplicates both *"% chance"* and *"needs more
  testing"* because those describe **why it is stuck**, not what happens.

Split them and the duplicates dissolve:

| axis | question | cardinality |
|---|---|---|
| **A — outcome** | what happens to you if you get it | **exactly one** per record |
| **B — obstacle** | why is it not better than that | **several** per record |
| **C — timing** | does it depend on catching it in time | a modifier on A |

**A disease has one answer on A and four on B.** That is why B cannot live in
the same list: a bucket set you can sum has to be a partition, and blockers are
not.

---

## Axis A — what happens to you (computed, 129/129)

Every record lands exactly once. Derived from `survival_outcome`, `restored` and
`has_window`, all of which already exist.

| # | bucket | n | sketch line |
|---|---|---|---|
| 1 | **Game over, whenever you find it** | **1** | "get it — game over" |
| 2 | **Game over unless caught in time** | **2** | "game over if not detected" |
| 3 | **Game over, but delayed** | **13** | "game over but delayed" |
| 5 | **Survive, and back to normal** | **9** | "survive at a high cost, roughly back to normal" |
| 6 | **Survive, permanently changed** | **53** | "survive but life-changing" |
| 7 | **Managed forever** | **14** | "needs to be managed forever" |
| 8 | **Mortality is the wrong question** | **37** | *missing from the sketch — see below* |

Bucket 4 is deliberately absent: *"% chance"* is not an outcome, it is a
**measurement** failure, and it belongs on axis B. See below.

### What the distribution says

**The horror bucket is almost empty.** *"You get it and it is over no matter what
anyone does"* is **one disease in 129** — Huntington's. Add the two that are
survivable only if caught in time (rabies, prion disease) and it is three.

**The enormous bucket is number 6: 53 records — survive, permanently changed.**
Against **9** who are simply restored. That is the register's most important
sentence and no chart currently says it:

> **Medicine's characteristic output is not death and it is not cure. It is
> survival in an altered body.**

That is a better headline than any score, and it falls straight out of the
buckets.

### Bucket 8 is not optional, and the sketch does not have it

**37 records — more than a quarter — cannot be placed on this axis at all**,
because a mortality ladder is silent about hearing loss, cataract, osteoarthritis
and low back pain, which are among the largest *disability* burdens here.

Without this bucket the other six do not sum to the register and every
percentage is wrong. Same rule as **`unrated` is never `unsolved`**, and as a
Sperrwerk check reporting `skipped` rather than `ok`.

**It should be named for what it is** — *mortality is the wrong question here* —
rather than "unrated", because these are not records awaiting work. They are
records where the axis does not apply, and calling them unrated invites somebody
to "finish" them by inventing a survival figure.

**Consequence: axis A needs a sibling.** A partition that cannot see a quarter of
the register is a reading, not the state of medicine — which is exactly the
standfirst's point. The natural sibling is a **disability/function** axis over
`residue` and `toll`, and the register already holds the data for it.

---

## Axis B — why it is not better than that (several per record)

These are the sketch's remaining buckets, and they are **blockers**, which the
register already models with a `standing` on each. They do not partition and must
not be summed as though they did.

| sketch line | already exists as | records |
|---|---|---|
| "no access to medicine" | `delivery` band + `deliv-gap` | 56 `barely`, 4 `undelivered` |
| "we have things but they don't really do anything" | `futile_treatment_risk` — *"we prescribe it because that's all we've got"* | **20** |
| "% chance — some respond, some don't, reason not understood" | `measurement.predictive` | 34 `none`, 64 `partial` |
| "possible path but needs more testing" | `blocker.kind:evidence-incomplete` | 35 |
| "no real known path forward" | see below — **the sketch guessed wrong** | 5 |

### The guess worth correcting

> *"Seems like stroke, heart disease maybe. I give someone 100 million dollars
> but they don't even know where to start."*

**Both are `mechanism: established`.** Nobody is short of a starting point on
stroke — its blockers are `diagnosis`, `logistics`, `policy` and `knowledge`, and
its knowledge blocker is about *which* strategy, not *whether* there is one.
Stroke is bucket 3 on axis A with a 3.3M knowledge gap: **a disease we understand
and cannot fix**, which is a different and less hopeless thing than not knowing
where to start.

**The records that actually fit are:** `low-back-pain`, `bipolar`, `depression`,
`heds`, `me-cfs` — the five with `mechanism` at `none` or `correlates`. Engpass
already has the obstacle: **`unexplained-illness`**, whose own note says 6 of its
7 records are blocked by nothing else and that it has **zero attributed deaths**.

**So the "hand them $100M and they cannot start" set is not the famous killers.
It is the diseases nobody dies of.** That is a sharper version of the sketch's
instinct than the sketch had, and it is the same lesson as the rabies correction:
the intuitive example is usually a different bucket.

Note also **only one record in 129 has *every* blocker as knowledge** (Huntington's).
Almost nothing is purely a science problem.

---

## Axis C — timing

`has_window` is on **86 records**, which is too many to be interesting as a
bucket. It earns its place as a **modifier**: it is what separates bucket 1 from
bucket 2, and it is where screening arguments live. The sketch's instinct —
*"this leads to areas where screening should be a priority"* — is right, and the
register already derives `window_toll_link` for it.

---

## Making them stable, which is the actual hard part

The sketch's goal is *"buckets we can use over time"*. Two threats, and they are
not equally obvious:

1. **A record moves between buckets.** This is **fine and is the point** — it is
   what `moved:` records and what a second snapshot is for.
2. **A bucket's *definition* changes.** This is **fatal and silent.** If bucket 6
   is redefined, next year's snapshot compares two different questions and the
   chart shows a trend that is an artefact of the edit.

**So bucket definitions must be versioned and stored with each snapshot**, not
just the counts. A snapshot that records `{bucket: 6, n: 53}` is not comparable
to next year's unless it also records what bucket 6 *meant*. That is the one
piece of machinery this needs that the register does not already have.

Proposed: a `buckets.yaml` holding slug, name, axis, rule and a `version`; the
snapshot stores the version alongside the counts; `check.py` errors if a rule
changes without the version being bumped. **Same discipline as append-only IDs
— a reading nobody can cite over time is not a reading.**

---

## What I would build, in order

1. **`buckets.yaml` + derive `bucket` on axis A.** It is ~15 lines of rule over
   fields that already exist, and it makes the 53/9 sentence sayable.
2. **Bucket 8 named honestly**, and the counts stated as *"6 buckets over 92
   records, 37 where the axis does not apply"* rather than as percentages of 129.
3. **Version the definitions into the snapshot** before the second bearing is
   taken, not after — retrofitting history is impossible, which is why the
   snapshot was built before there was anything to compare against.
4. **A disability sibling to axis A**, so the register stops being mortality-only.
   This is the largest piece and probably its own pass.

*Open:* whether bucket 5 ("back to normal") is real. It has 9 records and
`restored: restored` is one of the register's least-tested derivations — a
plausible read is that it means "we did not look hard enough at the toll", and
that a genuinely clean recovery is rarer than 9 in 129.
