# Nordstern — the record format

One file per entity, in `entities/<slug>.yaml`. Read this before adding one.

A record answers two questions and refuses to answer a third. It says **do we
understand this** and **can we do anything about it**. It does not say whether
the entity is "solved" — that is *derived* from the axes, never stored, because a
stored verdict is an opinion that cannot be argued with and a derived one is a
calculation that can.

---

## The spine

```yaml
slug: hepatitis-c          # local stable handle; never reused, never renumbered
id: FND-D-0002             # PERMANENT record id — what an outside citation resolves against
name: hepatitis C
also: [HCV infection]      # synonyms people actually search for
mondo: unresolved          # MONDO:xxxxxxx once resolved against a release
kind: disease              # disease | syndrome | complaint  (see below)
residual: false            # true if this is an "idiopathic"/"non-specific" bucket
contested: false           # true if the entity's existence or definition is disputed
```

**Disease identifiers are borrowed, never minted.** `mondo:` points at the Mondo
Disease Ontology — open, stable, already a merge of DOID/OMIM/Orphanet/NCIt/ICD.
A parallel disease namespace would buy nothing but a permanent mapping burden.
What Nordstern mints is the **assertion** ID at the bottom of each file: the rating
is the new thing, so the rating is what gets an address.

**THE REGISTER IS APPEND-ONLY.** A record is never deleted and its `id` is never
reused, because a public dataset is only useful if a citation keeps resolving.

`slug` is the human handle — readable, and therefore tempting to rename. `id` is
opaque and permanent, and it is the one an outside reference should use.
`assertion.id` is a third thing again: it identifies the *rating*, and it changes
when the record is re-rated. All three are needed and they answer different
questions.

A record that stops being right is **deprecated in place**:

```yaml
deprecated:                # absence of this block is what makes a record active
  date: 2026-09-01
  why: >
    Mondo merged this term into MONDO:0005010; the entity as framed here no
    longer has a referent.
  see: coronary-artery-disease   # optional. THE 302. Absent means a 410 —
                                 # simply no longer needed, pointing nowhere.
```

`status` (`active` / `deprecated`) is **derived from the presence of that block**
rather than stored beside it, so the two cannot disagree — the same rule that
makes `capability` derived. `check.py` requires `date` and `why`, requires a
`see:` target to exist, and rejects a redirect chain that cycles or does not
terminate: an unresolvable 302 is worse than a 410.

Deprecated records stay in `--json` and in the built artifacts so they remain
readable, drop out of every derived table, and are **hidden from search unless
asked for** — `status:deprecated` shows only those, `status:any` shows
everything, and `id:FND-D-0007` resolves a citation directly. Note that `id:`
used to be a query alias for `slug:` and now means the permanent identifier;
`slug:` still does what it always did.

`kind` matters more than it looks. A **complaint** is a presentation (low back
pain, fatigue); a **disease** is a named entity with, in principle, a mechanism.
Rating the "mechanism" of a complaint is a category error, and marking the kind is
what stops the register from quietly committing one.

## Burden

```yaml
burden:
  prevalence:
    value: 5.0e7
    units: people
    src: recall
  dalys:
    value: 1.5e6
    units: DALY/year
    src: recall
```

Every empirical scalar is a `value` / `units` / `src` mapping, as in Sperrwerk,
**written as an indented block**. The bounded YAML loader in `check.py` does not
read inline flow mappings (`{value: 1, units: x}`) and now raises rather than
returning them as a string — which is what it used to do, silently, until a
record built from this file's own examples crashed a report emitter six hundred
lines away. **`units` are required; `src` is required to be present but may record its own
weakness.**

### `src` — three words, or a citation

`src` is either one of **three words that all mean "not a citation"**, or a
mapping that is one:

| value | means |
|---|---|
| `recall` | written from the author's memory, unverified |
| `reasoning` | arithmetic or inference over other numbers here |
| `unknown` | **nobody has this number** — used deliberately by `msmds`, `noma`, `hat` |

```yaml
    src:
      id: 10.1016/S0140-6736(20)30925-9      # DOI, URL, dataset release, whatever resolves
      retrieved: 2026-08-26
      quote: >
        Global prevalence of osteoarthritis was 595 million cases in 2020.
```

**A CITATION MUST CARRY WHAT IT READ.** All three fields are required and
`check.py` errors without them. An `id` and a date are unenforceable — *a
plausible DOI is exactly what a language model emits when it does not know, and
it looks like success.* A verbatim `quote` makes the claim checkable by a human
in ten seconds and makes fabrication a deliberate act rather than a slip. The
rule is inherited from `resolve_mondo.py`, which prints Mondo's own definition
beside every proposal so that review is verification rather than trust.

**`src: recall` is honest. A fabricated citation is not.** Recording the weakness
is the point — a value with a missing source that *looks* sourced is exactly what
the ledger exists to prevent, and it is the one failure that would be invisible.

### What a citation could even settle — three tiers

Derived from the field path, never stored, and reported in every snapshot:

| tier | n | a citation… | where |
|---|---:|---|---|
| **sourceable** | 205 | **settles** it | all of `burden.*` — GBD and WHO publish these against an identifier this register now carries |
| **supportable** | 462 | **supports** it without determining it | `moved[]` (a dated event with a canonical reference), `toll.incidence`, `residue.incidence`, `strata[].fraction` |
| **judged** | 915 | **cannot touch** it | `axes.efficacy`, `axes.access`, `window.caught_in_time`, `strata[].efficacy`, and all 427 `blockers[]` |

**The third tier is not a backlog.** Nothing published anywhere holds *the
fraction of patients in whom the best available treatment works* — that is the
axis this register exists to supply, and a sourcing pass that treats it like a
lookup will invent citations for it.

**Blockers are `judged` and carry their evidential status in `standing`**
(`documented` / `alleged` / `disputed` / `refuted`) rather than in `src`, so
counting them in a sourcing denominator counts the same problem twice.

This split exists because the public banner said *"0 of 1,582 sourced"*, which
reads as 1,582 lookups nobody had done. It was honest about direction and wrong
about magnitude, on the page most likely to be quoted.

## The axes

Five, each a closed enum except the two fractions. Best-demonstrated value, not
typical practice.

```yaml
axes:
  mechanism:    established     # established | partial | correlates | none
  intervention: curative        # curative | suppressive | disease-modifying
                                # | symptomatic | none
  prevention:   risk-reduction  # eradicated | prophylaxis | risk-reduction | none
  ongoing:      none            # none | low | moderate | high
  efficacy:
    value: 0.95
    units: fraction-of-patients
    src: recall
  access:
    value: 0.15
    units: fraction-of-patients
    src: recall
```

**mechanism** — `established` means a causal chain from cause to phenotype that
would survive a refutation attempt. `partial` means the chain has a named hole.
`correlates` means reproducible associations and no chain. `none` means not even
that.

**intervention** — the ladder, and the reason this register exists:

| rung | meaning |
|---|---|
| `none` | nothing alters the course |
| `symptomatic` | masks the phenotype; course unchanged |
| `disease-modifying` | slows the course; does not arrest it |
| `suppressive` | restores near-normal life and lifespan, **indefinitely treated** |
| `curative` | a **finite** intervention ends the disease |

`suppressive` is the rung that stops HIV and type 1 diabetes from being filed
next to hepatitis C. Not a death sentence and not over. Everything above
`symptomatic` should be read together with `ongoing`, which is the cost of being
treated — the gulf between one levothyroxine tablet and thrice-weekly dialysis.

**prevention** is independent of intervention, not a continuation of it. PKU
proves it: the phenotype is prevented outright and the disease is never cured.

**And `capability` reads it.** Where `intervention` is `none` or `symptomatic`
but `prevention` is `prophylaxis` or `eradicated`, the derived capability is
**`preventable`** — a fourth value alongside `curable`, `managed` and `partial`,
added because none of them was true of measles. Nobody is cured of measles and
nobody is managed; *"don't get it, because if you do we cannot help you much"* is
a distinct answer, and it is also the right one for rabies and dengue. Before
this the register filed the most preventable disease it holds as `unsolved`
(gaps.md #66).

Two limits, both deliberate. **`risk-reduction` does not count** — smoking
cessation is real and is not a vaccine. And prevention **rescues only what would
otherwise read *nothing can be done***: rheumatic heart disease has prophylaxis
*and* disease-modifying treatment, and promoting it would hide the treatment
behind the prophylaxis.

**efficacy vs access** — deliberately two numbers, and **both describe the
treatment.** There is no `prevention_efficacy` and no coverage figure anywhere in
this schema, so `reach`, `delivery` and `orphaned` all silently answer for
treatment even on a record whose capability is entirely preventive. `delivery` is
withheld (`—`) rather than reported for a `preventable` record for that reason.
The single most important number about measles — vaccination coverage, ~83%
against a threshold of 95% — has nowhere to go. See gaps.md #109. `efficacy` is the fraction of
patients in whom the best intervention *works*; `access` is the fraction who can
*get* it. Collapsing them hides the two most important stories in the register:
epilepsy is ~30% drug-resistant regardless of wealth, and sickle-cell gene
therapy works nearly always and reaches nearly nobody.

## Measurement — three questions, not one

```yaml
measurement:
  diagnostic: objective     # objective | clinical | complaint
  prognostic: none          # good | partial | none
  predictive: partial       # good | partial | none | n/a
  witness: >
    ...
```

The old `diagnosis` axis asked one question — **is the disease present** — and
clinical practice needs three. Splitting them is what lets the register say *why*
a treatment is being aimed badly:

| | question | what its absence causes |
|---|---|---|
| **diagnostic** | is it there? | the patient is never found |
| **prognostic** | what will it do if left alone? | **overtreatment** — treating people who were never going to be harmed |
| **predictive** | will *this* treatment work in *this* patient? | **futile treatment** — full toll, no benefit, discovered only in retrospect |

`diagnostic` keeps its own vocabulary because the *kind* of evidence is more
informative there than a quality grade. The other two are graded.

**`predictive: n/a`** means there is no selection question to answer — either
nothing course-altering to predict a response to (ME/CFS, Huntington's), or a
treatment that works in essentially everyone. Hepatitis C is the important case:
interferon-era therapy needed genotype and IL28B status to predict response, and
pan-genotypic DAAs **abolished the question**. A measurement gap can be closed by
building a better treatment rather than a better test, and the schema should be
able to show that. `check.py` rejects an `n/a` that is really a dodge — claiming
it with a course-altering treatment and efficacy below 0.85 is an error.

Two derived flags, neither stored:

- **overtreatment risk** — real capability, a `costly`/`harsh` toll, and
  `prognostic: none`. People permanently harmed because nobody could say who
  needed it.
- **futile treatment risk** — real capability, a `costly`/`harsh` toll, and
  `predictive: none`. *"We prescribe it because that is all we've got."*

**Huntington's is the control case.** Diagnostic and prognostic measurement there
are near-perfect and there is nothing to do with the information. Measurement
without capability is as useless as capability without measurement — so "work on
measurement" pays where a treatment exists and is being aimed badly, not
everywhere.

## Toll — what the cure costs

```yaml
toll:
  severity: major           # none | minor | major | catastrophic
  permanent: true
  what: >
    The facial nerve runs through the parotid gland. Cure means dissecting the
    tumour off it, and sometimes through it.
  incidence:
    value: 0.03
    units: fraction-of-treated (permanent facial weakness, primary surgery)
    src: recall
```

**Required on every record.** A cure that ends the disease and takes your face is
not the same event as a cure that costs a fortnight of antibiotics, and until
this field existed the register filed them identically.

`toll` is **not** `ongoing` and **not** `efficacy`. `ongoing` is the burden of
*continuing* treatment — dialysis, a restricted diet, monthly injections.
`efficacy` is whether the treatment works. `toll` is the permanent price of it
**working**: the nerve, the bowel, the fertility, the second malignancy.

| severity | meaning |
|---|---|
| `none` | takes nothing permanent |
| `minor` | permanent but not life-altering — a scar, mild gustatory sweating |
| `major` | permanently alters function or appearance — facial palsy, a stoma, infertility |
| `catastrophic` | permanently disabling or life-shortening in its own right — intestinal failure, a treatment-caused cancer |

`severity` describes the harm **when it occurs**; `incidence` carries how often.
A rare catastrophe and a common nuisance are different things and neither should
be averaged into the other.

Derived: **`terms`** = `clean` (none/minor) · `costly` (major) · `harsh`
(catastrophic). It appears beside `capability` in `index.md`, because "curable"
alone was hiding the question a patient actually asks.

## Residue — what the disease leaves in someone it was cured in

Optional, and shaped deliberately like `toll`, because the two answer halves of
one question: **are they back to the state they were in before any of this?**

```yaml
residue:
  severity: major              # none | minor | major | catastrophic
  permanent: true
  what: >
    ...
  incidence:
    value: 0.30
    units: fraction-of-cured (permanent lung function impairment)
    src: reasoning
```

**`toll` is what the CURE takes. `residue` is what the DISEASE already took, and
the cure arrives too late to give back.** Tuberculosis forced the field. The
drugs take almost nothing permanent, so the register derived `terms: clean` and
the card read *"A finite treatment ends this."* — full stop — for a disease that
permanently scars the lungs of a large share of the people it cures. The field
was correct and the sentence was a lie, because there was nowhere to put the
other cost.

It is not a TB quirk. Hepatitis C cures the virus and leaves established
cirrhosis with lifelong cancer surveillance; antivenom neutralises venom and does
not regrow the digested limb; gene therapy stops the sickling and does not give
back the strokes. **For any tissue-destroying disease, cure means the destruction
stopped, not that it was reversed** — and a patient hears the second.

**Why the two are kept apart rather than summed.** The levers differ. A better
*treatment* reduces the toll. Only an *earlier* treatment reduces the residue —
which is why `residue` and `window` almost always travel together, and why the
pair is an argument for the `diagnosis` blocker rather than for new therapeutics.

Rules:

- **Only where there is capability.** `check.py` rejects a residue on a record
  with none: with nothing that works, nobody reaches the end of successful
  treatment, and the damage is just the disease running its course — which the
  axes already say.
- **`minor` is a real answer and should be used.** *H. pylori* eradication leaves
  atrophic gastritis and a residual gastric cancer risk, which is permanent,
  asymptomatic, and consequential for a minority. That is `minor`, and the record
  still derives `restored`. A field that rated everything `major` would stop
  distinguishing anything.
- **Suppressive records ask it differently.** Nobody finishes treatment, so "back
  to the state before" means "back to baseline while treated". HIV started early
  is close to yes; started late it is not, and the residue is a function of how
  late the diagnosis was.
- **Not the same as `window`.** A window says capability changes with timing.
  Residue says damage persists after success. Crohn's fibrosis is deliberately
  left in `window` rather than duplicated here.
- **Rheumatic heart disease deliberately has none.** The scarred valve *is* the
  entity, not a residue of it. A residue has to be left in the patient after the
  thing the record is about has been dealt with.

### Derived: `restored`

Not stored. Reads `terms` and `residue_terms` together and answers the question
in one word:

| | meaning |
|---|---|
| `restored` | nothing permanent from either side |
| `cure-costs` | the treatment took something |
| `disease-residue` | the treatment worked and the damage was already done |
| `both` | the cure took something **and** the disease left something |
| `n/a` | no capability — nobody reaches the end of successful treatment |

**`n/a` is never `restored`**, the same rule as `unrated` never being `unsolved`
and a Sperrwerk check reporting `skipped` rather than `ok`. Sickle cell is the
register's only `both`: myeloablative conditioning takes fertility, and the cure
at thirty does not undo the strokes at eight.

## Strata — when one entity spans the ladder

Optional, and present only where the entity genuinely contains clinically
distinct sub-populations with **different capability**. Breast cancer is the
forcing case: stage I is curable and stage IV is not, and no single
`intervention` rating is true of both.

```yaml
strata:
  - name: stage I-II (early, operable)
    fraction:
      value: 0.62
      units: fraction-of-diagnoses
      src: recall
    intervention: curative
    efficacy:
      value: 0.9
      units: fraction-of-stratum (disease-free long-term)
      src: recall
    toll: major                  # severity only; the full toll block stays at record level
    what: >
      ...
```

A stratum overrides only what actually varies — `intervention`, `efficacy` and
`toll`. `mechanism` and `diagnosis` do not vary by stage; it is the same disease.

**The record-level axes describe the modal patient**, and the strata refine.
`check.py` checks that the fractions sum to 1, and flags any record whose strata
span more than one capability with **⧉**. That flag is the honest answer to "is
breast cancer solved" — the question is malformed, and the register should say so
rather than pick a side.

Strata are **not** the same as treatment tiers determined by access (sickle
cell's gene therapy versus hydroxyurea). Those are one population that could
receive either; these are different populations that cannot. Whether the two
constructs eventually unify is open — see `gaps.md`.

## Survival — "you get it, and then what?"

Optional. Present where mortality is the question; **genuinely absent where it
is not**, which is a large part of the corpus.

```yaml
survival:
  horizon: 5 years from diagnosis
  untreated:
    value: 0.25
    units: fraction alive — the Framingham natural history, before ACE inhibitors
    src: recall
  treated:
    value: 0.55
    units: fraction alive on guideline-directed therapy
    src: reasoning
  witness: >
    Why these two numbers, and what they conceal.
```

**IT EXISTS BECAUSE `efficacy` IS NOT COMPARABLE ACROSS RECORDS.** `efficacy`
reads 0.55 for head and neck cancer (alive and disease-free at five years), 0.85
for asthma (good symptom control) and 0.75 for hearing loss (meaningful benefit
from a hearing aid). The register's central axis measures a different thing in
each record, and `reach = efficacy × access` multiplies across them as though
they commuted. Survival measures one thing everywhere.

**THE UNTREATED VALUE IS THE INTERESTING HALF.** `treated` says where medicine
is; `untreated` says what the disease does when left alone. The difference —
derived as `gain` — is the most direct statement of progress the register can
make, and it is computed by subtracting two measured numbers rather than by
judging an axis. It also produces the least comfortable rows: **Alzheimer's is
+0.00.**

**THE HORIZON IS DECLARED PER RECORD BECAUSE IT HAS TO BE.** Rabies kills within
a month of symptoms; Huntington's takes twenty years and is equally certain.
A five-year constant would call one terminal and the other excellent.

### Derived: `survival` band, and `outcome` — two questions, never one

| derivation | asks | values |
|---|---|---|
| `survival` | **how many** reach the horizon | `terminal` <0.10 · `a chance` <0.50 · `good chance` · `n/a` |
| `outcome` | **what reaching it means** | `cured` · `recovered` · `held` · `delayed` · `n/a` |

`outcome` is read off `axes.intervention` — `curative` → `cured`, `suppressive`
→ `held` — plus the optional `course` below, so it costs almost nothing and
cannot disagree with the ladder.

### `course: acute | chronic` — optional, and the ladder is not enough without it

**THE LADDER SAYS WHAT TREATMENT ACHIEVES, NOT WHAT HAPPENS TO THE PATIENT.**
For chronic disease those coincide. For an acute infection they do not, and the
first version of this derivation printed, for measles: *"99% at 30 days from
rash onset — **alive and still dying of it**."* Measles is `symptomatic` because
there is no antiviral, and its survivors recovered.

Six records said the same false thing — measles, dengue, influenza, cholera,
H5N1, Marburg. `course: acute` gives them the fourth outcome, `recovered`.

It is **declared, never inferred**: nothing in the register implies it, not the
ladder, not `kind`, and not the horizon, which is prose. It is consulted **only
for records below `suppressive`** — an acute disease that antibiotics cure
(typhoid, treated cholera, malaria) is `cured`, because there the treatment
genuinely ended it. Default is `chronic`; a misspelling is an error rather than
a silent default back to the sentence it exists to prevent. See `gaps.md` #222.

### Derived: `gain`, and why nothing is sorted by it

`gain` is `treated − untreated`. It is the register's most direct statement of
progress and **it is close to inverted against burden**: COVID-19 is +0.006,
asthma +0.017, measles +0.010, while human African trypanosomiasis — a few
hundred cases a year — is +0.950. A difference of fractions compresses
catastrophically where prevalence is large, and asthma's missing 0.3% is 455,000
deaths a year.

**So no view sorts by it.** The missing quantity is deaths averted
(`gain × incidence`), which is not computed because multiplying two `src: recall`
figures produces a confident number from two guesses. `gaps.md` #221.

**NEITHER IS SAFE TO DISPLAY ALONE, AND THAT IS THE WHOLE DESIGN.** Two records
at 0.13 and 0.20 sit in the same band and mean opposite things: pancreatic
cancer's 13% are *cured*, ALS's 20% are *still dying of it*. A view ranked on
the band alone puts ALS above pancreatic cancer and is exactly wrong about which
one anybody survives. `head-neck-cancer` and `heart-failure` both land on 0.55
and only the qualifier separates them. See `gaps.md` #216.

The two readings are deliberately **independent**: gating the outcome on the
band would fold them back together. A curative disease with 2% survival still
cures 2% of people — that is a scale statement, not a kind statement.

### Derived: `know-gap` / `deliv-gap` — and the rule they bend

`knowledge_gap` is `deaths × (1 − efficacy)`: deaths a year that remain **with
delivery already perfect**. `delivery_gap` is `deaths × efficacy × (1 − access)`:
deaths a year claimable by **what already exists**. Together they are
`deaths × (1 − reach)`, so they partition the burden current medicine does not
reach, and a test asserts that they do.

They exist because the register could say *rabies is horrific and nothing treats
it* and *heart disease kills nine million a year* and had **no way to say which
is the better place to work**. Weighted, the intuition behind that question turns
out to be a false choice: `stroke` alone carries ~3.3M, against ~91,000
attributed deaths across every record where `efficacy` is zero. **The largest
knowledge gaps in this register are inside the common diseases.**

**THIS IS THE SAME MULTIPLICATION #221 REFUSED, AND THE REFUSAL STILL STANDS FOR
WHAT IT COVERED.** `gain × incidence` was rejected above because multiplying two
`src: recall` figures produces a confident number from two guesses. `deaths ×
(1 − efficacy)` has exactly that shape. Three things separate them, and none of
them is that the arithmetic got safer:

- **It is built for rank, not for level.** A shared multiplicative error moves
  every record together and leaves the ordering largely intact. #221's objection
  was to publishing *deaths averted* as a quantity — a positive claim about
  medicine's achievement — where the number **is** the claim.
- **Both guards return `None`, never a plausible zero.** No `deaths` figure, or
  `capability: preventable`, and there is no gap — see `_gap_inputs`. Rabies
  would otherwise read as a 59,000-death *knowledge* gap when its vaccine works
  and its deaths are access.
- **The figure states its own denominator and its own exclusions**, on the page,
  including the count of records it cannot see.

**Where it still bends the rule: the dashboard prints a total** — *"22.2M
knowledge against 36.3M delivery"* — and that is a level, not a rank, so #221
lands on it squarely. It is published anyway, with the caveat attached, because
the asymmetry it states is the register's founding claim and stating it in lives
is more legible than stating it in blocker counts. **If a sourcing pass ever
contradicts it, that sentence goes before the chart does.** `gaps.md` #246.

### `n/a` is never `terminal`

Same rule as `predictive: n/a` and as a Sperrwerk check reporting `skipped`.
A mortality ladder is silent by construction about hearing loss, cataract,
osteoarthritis and low back pain — **which are among the largest disability
burdens in the register.** Any view built on this axis must say what it cannot
see.

**Risk factors are rateable only by naming the population.** Hypertension,
obesity and atrial fibrillation are *exposures* — they raise the hazard of the
diseases in other records rather than having a course of their own — so a bare
survival figure for them would be a number about nothing. Naming the horizon
precisely makes the question real (*"10 years from diagnosis of stage 2
hypertension, untreated, at age 50"*), and the VA Cooperative trials answer it.

**But those rows are not comparable to the rest.** Pancreatic cancer's 0.13
measures a disease's own lethality; hypertension's 0.70 measures a risk factor's
contribution to somebody else's. The horizon carries the qualifier and the
witness states it. See `gaps.md` #219.

## Window — when the answer depends on catching it

Optional, and present only where capability genuinely changes with timing.

```yaml
window:
  what: >
    Small and superficial, it comes out with the nerve intact. Left to grow,
    recur, or transform, cure costs the nerve.
  closes_on: tumour growth, recurrence, malignant transformation
  caught_in_time:
    value: 0.7
    units: fraction-of-patients
    src: recall
```

The axes rate one state, and some entities have two. PKU is the purest case in
the register: caught in the first weeks of life, a normal life; missed, severe
irreversible intellectual disability — the *same disease*, the *same treatment*,
and an entirely different answer to "is it solved".

**The window and the toll usually interact, and that interaction is the most
actionable thing in a record.** Where the toll is the price of having missed the
window, the highest-leverage blocker is `diagnosis` — earlier detection converts a
mutilating cure into a clean one, without any new therapy. `check.py` lists
these, because they are the cheapest wins in the register.

## The witness

```yaml
witness:
  mechanism: >
    Prose naming the specific finding, who found it, and what is still open.
  intervention: >
    Which treatment, which trial, what effect size, what fraction left over.
```

**The output is a witness, never a boolean.** `intervention: curative` is
useless to anyone who wants to argue; "8–12 weeks of a DAA regimen, SVR above
95%, but cirrhosis already established does not reverse" is a design review. A
record whose witness does not justify its axes is not finished.

## Blockers — why it isn't delivered

The axes say where a thing stands. `blockers` says **what stands in the way, who
could move it, and roughly what that would cost.** It is the only part of a record
a reader can act on, and it is the part that decides whether an entity belongs on
a research agenda or a delivery agenda.

```yaml
blockers:
  - kind: cost
    blocks: exagamglogene autotemcel (curative)
    what: >
      List price around two to three million dollars, plus myeloablative
      conditioning at a transplant-capable centre.
    who_could: [payer, manufacturer, philanthropy]
    scale: 1e9              # order-of-magnitude USD to clear it; null if unpriceable
    standing: documented
    src: recall
```

A record has a **list** of blockers, each naming the intervention it blocks —
which is also how tiered interventions finally get a home: sickle cell's gene
therapy is blocked by cost while hydroxyurea, off-patent and cheap, is blocked by
logistics. One `access` number could never say that.

**`kind`** — the taxonomy is deliberately broad here, unlike every other enum in
this schema, because the whole purpose is that **different blockers need different
actors**:

| kind | the thing that is stuck | who typically clears it |
|---|---|---|
| `knowledge` | nobody knows what to do | researchers |
| `candidate-untested` | a plausible intervention has never had an adequate trial | academic, nonprofit |
| `evidence-incomplete` | trialled, but not decisively | academic, nonprofit, sponsor |
| `no-sponsor` | works, or nearly — nobody will fund or make it | nonprofit, philanthropy, government |
| `regulatory` | no approval route, or the framework does not fit the thing | regulator, legislator |
| `manufacturing` | cannot be made at the needed scale or quality | manufacturer, government |
| `cost` | approved, and priced out of reach | payer, manufacturer |
| `logistics` | staff, supply, cold chain, the last mile | health-system, nonprofit |
| `diagnosis` | the treatment exists; the patients are not found | health-system, software |
| `adherence` | requires sustained effort from the patient | health-system, patient-org |
| `tooling` | the bottleneck is software, data, or coordination | software, academic |
| `policy` | law or politics forbids or impedes it | government, legislator |

**`obstacles:`** — an optional list of slugs on ANY blocker, pointing at records
in the **Engpass** obstacle register. It is the only
cross-project field in this schema, and it is deliberately inert here: Nordstern
does not validate it, does not read Engpass, and does not know it exists. A
blocker names what it is waiting on; Engpass reconciles and derives *answering
this would unblock these N diseases*, which is the direction that can be acted
on.

It is a **list** because 24 of the register's 42 knowledge blockers ask more than
one question — *"intracerebral haemorrhage, cryptogenic stroke, and repair"* is
three. A typo'd slug is caught by Engpass's checker as an error; a blocker with
no `obstacles:` shows up there as untagged, which is usually the right answer,
because *nobody has made the drug* is not an open question.

**`standing`** is the field that makes this an instrument rather than an echo
chamber, and it exists because "it's solvable, but pharma/the FDA won't allow it"
is a *very* commonly asserted claim of unknown truth:

- **`documented`** — a named trial, a named rejected application, a published
  price, a dated discontinuation. Checkable.
- **`alleged`** — widely asserted, not verified. **The default for anything heard
  rather than read.**
- **`disputed`** — the parties disagree about the facts, and the disagreement is
  itself the finding.
- **`refuted`** — checked, and false.

**The register's job is to convert `alleged` into `documented` or `refuted`.** A
project that only ever finds `documented` blockers is not investigating, it is
campaigning. Finding that the refrain is mostly false would be a real and useful
result, and the schema has to be able to record it.

### The triage this enables

Two derived quantities, neither stored:

- **`reach-gap`** = `burden × (1 − reach)` — the burden that existing capability
  already ought to be reaching and does not.
- **`clearing cost per unit burden`** = `scale ÷ reach-gap` — only defined when
  `scale` is not null.

`scale: null` is the honest entry for a `knowledge` blocker, and that asymmetry is
the point: **knowledge blockers cannot be triaged with money; delivery blockers
can.** Huntington's has no price. Snakebite does.

### Derived: the no-champion list

An entity is **orphaned** when capability is `curable` or `managed`, every blocker
is of a non-`knowledge` kind, and at least one is `documented`. Meaning: *the
science is done and nobody is carrying it.* That list is the register's most
directly actionable output — the things a nonprofit could take off the board — and
it is derived, so it cannot be padded by enthusiasm.

## Holes and provenance

```yaml
holes:
  - What is not known, stated as the thing that would move a rating.

moved:
  - {date: 2014, axis: intervention, from: disease-modifying, to: curative,
     why: "DAA regimens reached >95% SVR"}

assertion:
  id: FND-A-0002
  rated: 2026-08-11
  by: [claude, jeremy]
```

`assertion.supersedes` names the assertion this rating replaces, and is present
only on a **re-rating**. `id` (`FND-A-NNNN`) identifies the *rating*, not the
record, so it takes a new number every pass while the record's `FND-D-NNNN` stays
put — that is what makes a second look a comparison rather than a fresh opinion.
Tuberculosis is the first: `FND-A-0070 supersedes: FND-A-0023`, and **not one
scalar changed** — the pass added four dated `moved` entries reconstructed from
prose the record already contained. A record that narrates a change in a witness
and has no `moved` entry for it is the shape to look for.

`moved` exists because ratings change and an undated rating is a rumour.
Hepatitis C went from `none` to `curative` in about three years; sickle cell took
seventy-five to go from a solved mechanism to an approved cure.

## Deriving the verdict

Not stored anywhere. The verdict is **two parts, not one** — a correction forced
by the first eleven records, where a single word could not hold the fact that
H. pylori ulcers are curable and reach barely half of patients (see `gaps.md`).

**Capability** — what medicine can do at its best, for anyone:

- **curable** — `intervention: curative`, or `prevention: eradicated`
- **managed** — `intervention: suppressive`
- **partial** — `intervention: disease-modifying`
- **unsolved** — `intervention` is `symptomatic` or `none`
- **unrated** — any axis absent

**Delivery** — `reach = efficacy × access`, the fraction of patients for whom
the capability is real:

- **delivered** ≥ 0.8 · **mostly** ≥ 0.6 · **partly** ≥ 0.3 · **barely** ≥ 0.05
  · **undelivered** < 0.05

So hepatitis C reads *curable / barely delivered* and sickle cell *curable /
undelivered*, and neither collapses into "solved". Keeping the two apart is what
stops a knowledge win from being reported as a health outcome.

**`unrated` is never `unsolved`.** A record that cannot be rated says so, in the
same way a Sperrwerk check that cannot run reports `skipped` and never `ok`.

The map is `mechanism` (`established`/`partial` = known) against the
**intervention ladder in three bands** — because a five-rung ladder cannot be
flattened to a yes/no:

| band | rungs | the course is |
|---|---|---|
| `treatable` | `suppressive`, `curative` | held, or ended |
| `modifiable` | `disease-modifying` | slowed, and not arrested |
| `neither` | `symptomatic`, `none` | unchanged |

|  | treatable | modifiable | neither |
|---|---|---|---|
| **known** | **known & treatable** | **known & modifiable** | **engineering problem** |
| **not known** | **empirical luck** | *empirical foothold* | frontier |

**The middle column exists because leaving it out was wrong**, and the field is
still called `quadrant` because the term is the query language's API
(gaps.md #89). `fixable = intervention in ("suppressive", "curative")` put
`disease-modifying` in the same bucket as `none`, so **ischaemic heart disease
and stroke — the first and third largest causes of death on Earth, 15.6 million
deaths a year — were filed as "understood, and nothing can be done"**, against a
coronary death rate that has more than halved since about 1980.

COPD chose this repair over the alternatives. It is `symptomatic`, so it belongs
in the bottom band and the harsh verdict on its *course* is deserved — which
moving the rung up would have obscured and deleting the map would have lost.
Note what `engineering problem` still does **not** mean: bronchodilators
genuinely relieve breathlessness, and this register measures benefit only as
course alteration (gaps.md #98).

*empirical foothold* — something slows a disease nobody understands — is
**unoccupied at 44 records.** It is named because the derivation must be total,
and an empty cell is worth reporting rather than hiding.

**The known/treatable cell is called `known & treatable`, never "solved".** It
means the mechanism is understood and a treatment exists — nothing more. Reach,
toll and whether anyone is cured are separate fields, and a label that implies
otherwise misleads exactly the reader who most needs the truth. Breast cancer and
Crohn's both sit in that cell.

The off-diagonals are the interesting ones. Huntington's is an engineering
problem; depression is empirical luck; ischaemic heart disease is
`known & modifiable`. And sickle cell shows the map has to be
read twice — *de jure* it is solved, *de facto* it sits in the engineering-problem
cell, and only the `access` field tells you which map you are looking at.

### Two derived flags that exist so the query language can stay small

`web/query.js` filters the register with `field:value` terms. Two of the six
canned questions could not be said in that grammar, and rather than grow the
grammar, both concepts were **named and derived** — which is where they belonged,
since the register was already talking about them:

- **`only_knowledge_blockers`** — *every* blocker is `knowledge`. A query term
  over a list asks whether **some** element matches, which is a much weaker claim
  (`blocker.kind:knowledge` catches any record with one research problem among
  five delivery problems). This flag is the "money cannot move it at any price"
  set, and adding an `every` quantifier to the query language to say it would have
  been the wrong trade.
- **`measurement_gap`** — `overtreatment_risk` **or** `futile_treatment_risk`.
  The query language deliberately has no cross-term `OR`; but these two are not
  really separate questions. *Can we aim what we already have?* fails either
  because we cannot say who needed it or because we cannot say who will respond.

**The rule, and it matters:** derive a flag when it names a concept the register
*has* — never merely to route around a gap in the grammar. Both of these were
canned questions long before they were fields. A derived flag invented to dodge a
missing operator is a grammar gap in disguise, and it will be discovered later by
someone who cannot find it.
