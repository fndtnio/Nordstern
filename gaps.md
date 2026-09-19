# Gaps — what the seed set forced

Each entry names the record that forced it, because a gap nothing forces is
speculation. Written during the first eleven ratings; the schema was corrected
mid-pass where the fix was obvious, and those corrections are marked **applied**.

---

## 1. A single verdict could not hold capability and delivery · **applied**
*Forced by:* `h-pylori-ulcer`, then confirmed by `hepatitis-c` and `sickle-cell`.

The original rule made "solved" require `efficacy × access > 0.8`. Under it, the
cleanest cure in medicine — a fortnight of antibiotics that ends the disease —
came out **not solved**, because roughly half of patients are never reached. That
is a true fact about the world and a useless verdict: it files a finished science
problem next to an unstarted one.

Fixed by splitting the verdict into **capability** and **delivery**. Hepatitis C
now reads *curable / barely delivered*, which is the sentence anyone would want.

## 2. `reach` conflated a biological ceiling with a supply failure · **applied**
*Forced by:* `epilepsy`, sharpened by `sickle-cell`.

About a third of epilepsy patients are drug-resistant in the best-funded health
systems on earth. That number will not move with money. Sickle-cell gene therapy
works nearly always and reaches nearly nobody, and that number is *only* money.
A single "reach" field would have averaged a fact about neurons with a fact about
procurement.

Fixed by splitting into **`efficacy`** (works in whom) and **`access`** (available
to whom), with `reach` derived. This is now the schema's most load-bearing
distinction.

## 3. `mechanism` needs coverage, not just depth · **ready to implement**
*Forced by:* `epilepsy`.

`partial` currently means two unlike things: *the chain has a named hole* (which
is Huntington's — genetics certain, pathogenesis open) and *the chain is complete
for some cases and absent for others* (which is epilepsy — decisive for SCN1A and
structural lesions, and no cause identified at all in roughly half). Rating those
the same is why epilepsy lands in the `known` column, which overstates it.

Proposal: `mechanism: {depth: established|partial|correlates|none, coverage:
{value: 0.5, units: fraction-of-cases, src: ...}}`. Cheap, and it would let the
headline metric weight burden by *how much* of an entity is understood.

## 4. Heterogeneous entities are being averaged into one record · **open**
*Forced by:* `epilepsy`, `low-back-pain`, `depression`.

Three of the eleven are bags rather than entities. Epilepsy should probably be
several records (Dravet, mesial temporal lobe epilepsy with sclerosis, idiopathic
generalised) which would land in *different quadrants*. Low back pain should be a
few specific causes plus an explicitly residual bucket. Whether MDD is one
condition is genuinely open, and if it is not, every number in that file is an
average over unlike things.

This is the neck-pain problem from the original discussion, arriving exactly where
predicted. Note it is **not** solved by `kind:` — marking low back pain as a
`complaint` correctly stops the category error, but does nothing about the fact
that the register's largest-burden entry cannot be rated coherently.

**This is also the most valuable thing here.** Splitting low back pain would let
Nordstern state how much of the world's leading cause of disability sits in a bucket
labelled "non-specific". That number does not currently exist anywhere.

## 5. No way to say "curative, demonstrated in n=6, not generalisable" · **open**
*Forced by:* `hiv`.

A handful of people have been genuinely cured of HIV by CCR5-delta-32 allogeneic
transplant. That is a real, load-bearing scientific fact — it proves cure is
physically possible — and it is not a rung the population can stand on, because
the procedure is only justifiable alongside a lethal malignancy. Rating HIV
`curative` would be absurd; rating it `suppressive` silently discards the most
important result in the field.

The `access: 0.0000001` dodge is wrong: this is not scarcity, it is
non-generalisability. Probably wants a separate `demonstrated:` block recording
proof-of-principle results with an explicit n and the reason they do not
generalise.

## 6. `contested` needs to say contested-by-whom, and about what · **open**
*Forced by:* `me-cfs`.

A bare boolean flattens two arguments with different shapes and different
resolutions: the *scientific* dispute (is it one entity, do the case definitions
select the same population) and the *political* one (is it real, a decades-long
conflict between patient organisations and parts of the research community, with
consequences for funding relative to burden). Recording `true` loses both.

Also: ME/CFS prevalence spans an eightfold range **as a function of which criteria
are used**. That is not measurement uncertainty and must not be stored as a value
with error bars. A prevalence conditional on a case definition needs the
definition attached.

## 7. High `access` can be bad news, and the schema cannot say so · **open**
*Forced by:* `low-back-pain`.

Back pain care is widely available and much of it is low-value or harmful —
routine imaging that finds irrelevant abnormalities, injections, opioids, fusion
for non-specific pain. `access: 0.8` reads as an achievement and describes a
harm. Every other record in the set treats access as monotonically good.

## 8. Ratings fall for reasons unrelated to knowledge · **open**
*Forced by:* `h-pylori-ulcer`.

First-line eradication efficacy has declined with clarithromycin resistance. The
register needs to distinguish *we learned something and revised* from *the world
changed under a stable understanding* — otherwise the time series reads as
scientific regress. `moved` records the change but not its kind.

## 9. Prevention and cure are independent axes · **applied**
*Forced by:* `pku`.

PKU's phenotype is prevented outright by newborn screening and diet, and the
disease is never cured — the enzyme defect is untouched and stopping the diet
raises phenylalanine again. Any single ladder ending in "cured" files this
wrongly. Smallpox makes the same point from the other end: eradicated, and
nobody can cure a case.

`prevention` is a separate axis for this reason, and `ongoing` exists because
"prevented" hides a lifelong severely restricted diet.

## 10. The headline metric is not yet computable · **open**
*Forced by:* the whole set.

Share of global DALYs under entities with no established mechanism — the intended
top-line number — cannot be computed from these eleven records: burden units are
inconsistent (YLD vs DALY), several records carry no DALY figure, and **every
scalar is `src: recall`**. Producing a number anyway would be precisely the
failure mode Sperrwerk exists to catch, so the register reports that it cannot
compute it.

One verification pass against a GBD release, with units normalised, unblocks it.

---

# Second pass — what the blocker axis forced

## 11. The no-champion rule was wrong twice, and running it said so · **applied**
*Forced by:* `sickle-cell` and `hiv`, on the first execution of `check.py`.

The first derivation of "orphaned" read: capability is curable or managed, **no
knowledge blocker**, and at least one documented blocker. It looked reasonable
and it was wrong in two directions.

- **Sickle cell fell off the list.** It carries a `knowledge` blocker for in vivo
  editing — a *better future* cure that would remove the transplant requirement —
  and that disqualified it, even though off-patent hydroxyurea is documented as
  undelivered. Wanting a better cure does not make the existing one delivered.
- **HIV appeared on it.** It has documented logistics and policy blockers and is
  simultaneously among the best-funded delivery efforts in history. "No champion"
  has to mean *under-delivered*, not merely imperfect.

Fixed by requiring a documented **non-knowledge** blocker, and adding a reach
ceiling of 0.6. The ceiling is a tunable, not a truth, and PKU sits just outside
it at 0.665 with a strong documented screening blocker.

**This is the argument for deriving rather than storing.** A hand-written
verdict column would have carried both errors indefinitely and looked
authoritative doing it.

## 12. Capability has to include prevention · **applied**
*Forced by:* `rheumatic-heart-disease`.

RHD's intervention rung is only `disease-modifying` — damaged valves are not
repaired — so the first rule excluded it from the actionable list entirely. But
its *prevention* is `prophylaxis` grade: a monthly penicillin injection from the
1940s prevents the damage, and the blocker is that the world periodically cannot
manufacture it. Excluding the register's clearest manufacturing failure because
it prevents rather than treats was plainly wrong.

`has_capability()` now reads prevention as well as intervention.

## 13. Tiered interventions finally have a home · **applied**
*Forced by:* `sickle-cell`, retiring a gap left open in the first pass.

Because each blocker names the intervention it `blocks:`, one record can now say
that gene therapy is blocked by **cost** while hydroxyurea is blocked by
**logistics** — two different tiers, two different actors, two different prices.
The single `access` number never could.

## 14. "Alleged" needs a work queue, not just a label · **open**
*Forced by:* `amr-infection` (phage), `epilepsy` (phenobarbital scheduling),
`me-cfs` (research funding), `rheumatic-heart-disease` (GAS vaccine hold).

Three `alleged` and one `disputed` blocker are now recorded, which is the schema
working as designed — but nothing tracks *what would settle them*. Each needs a
named check: the specific document, trial registry entry, funding line or
regulatory record that would flip it to `documented` or `refuted`.

Proposal: `resolves_by:` on any blocker whose standing is not `documented` — a
concrete, checkable task. That turns the register's soft spots into a to-do list
instead of a permanent hedge.

## 15. A high `access` figure can be bad news · **open, restated**
*Forced by:* `low-back-pain`, and sharpened by the blocker pass.

Back pain now carries a `policy` blocker whose content is *de-implementation* —
the obstacle is getting harmful care away from people, not getting good care to
them. It is the only inverted blocker in the register, and both `access: 0.8` and
`scale: null` misrepresent it: the fix costs less than the status quo.

## 16. The blocker ratio is a property of the sample · **open**
*Forced by:* the whole second pass.

Delivery blockers outnumber knowledge blockers roughly four to one, and exactly
one record has no delivery lever. This is **not a finding about medicine** —
three records were added specifically to exercise the blocker axis, so the
sample was constructed to produce it. Quoting the ratio as a result would be the
campaigning failure the `standing` field exists to prevent.

Fixing it needs a burden-weighted sample rather than a diagnostic one, which is
the same verification pass that unblocks the headline metric (gap 10).

---

# Third pass — what pleomorphic adenoma and Crohn's forced

Jeremy brought both, and named the missing category before either was written:
*"Sure you 'fixed' the thing but someone's life may be irreversibly and extremely
harmed."* It turned out to be **two** missing concepts that interact.

## 17. `toll` — the cure has a price, and it was invisible · **applied**
*Forced by:* `pleomorphic-adenoma` and `crohns`.

The register could say a thing was `curable` and could say treatment was
burdensome while it continued (`ongoing`). It had no way to record what success
**takes, permanently**: the facial nerve, the bowel, the fertility, the second
malignancy. Parotidectomy and a fortnight of antibiotics were filed identically.

`toll: {severity, permanent, what, incidence}` is now required on every record,
and `terms` (clean/costly/harsh) is derived beside `capability`. Backfilled
across all fourteen earlier records, which turned up major or catastrophic tolls
in six of sixteen — it was never a two-record problem.

`severity` describes the harm **when it occurs** and `incidence` how often, so a
rare catastrophe and a common nuisance stay distinguishable.

## 18. `window` — capability changes with timing · **applied**
*Forced by:* the same pair, then found retroactively in three earlier records.

*"If you find it early and you can use surgery, great. But if not…"* The axes rate
one state; some entities have two. Small superficial adenoma versus recurrent
deep-lobe disease. Crohn's inflammation, which drugs treat, versus Crohn's
fibrosis, which no drug touches because scar is mechanical.

Adding it retrospectively found windows already sitting in the prose of `pku`
(newborn screening, weeks), `rheumatic-heart-disease` (before the valve scars)
and `sickle-cell` (before the childhood stroke) — good evidence the concept was
real rather than invented for two records.

**The interaction is the payoff.** Four of five windows have a major toll
attached, meaning the price is largely the price of arriving late — which makes
`diagnosis` the cheapest lever in the register, buying more than any new therapy
would. `check.py` flags the link.

## 19. "Harm without benefit" appeared unbidden · **applied, and worth watching**
*Forced by:* nothing — it fell out of `toll` × `capability`.

Two records inflict major permanent harm while rated `unsolved`:
`low-back-pain` (opioids, fusion, at the scale of the world's leading cause of
disability) and `me-cfs` (graded exercise therapy, withdrawn 2021). Neither was
anticipated and the checker now lists them.

This is the strongest argument yet for deriving rather than storing. A hand-built
register would have had no reason to compute this cross-product, and it is
probably the most damning row the project can produce.

## 20. One `toll` per record cannot express tiers · **open**
*Forced by:* `sickle-cell`.

Its curative tier is `catastrophic` (myeloablative conditioning: infertility,
secondary malignancy) while hydroxyurea, the tier nearly every patient actually
receives, is `minor`. The record carries the catastrophic rating, which is true
of the cure and false of the treatment almost everyone gets.

`blockers` solved exactly this problem by naming the intervention each one
`blocks:`. `toll` should do the same — a list keyed to intervention rather than a
single severity. Deferred until a second record forces it; sickle cell alone is
one data point.

## 21. A `toll` can be historical, and the schema cannot date it · **open**
*Forced by:* `me-cfs`.

Graded exercise therapy is no longer recommended, so the current incidence is
zero while the severity is `major`. The checker very nearly rejected the
combination as contradictory, and the only reason it does not is that the
`severity: none` rule is one-directional.

A retired harm is worth recording — it explains the field's relationship with its
patients — but it needs a marker (`retired: true`, or a date) so that live and
historical tolls are not summed.

## 22. `caught_in_time` is an outcome, not a lever · **open**
*Forced by:* all five window records.

The field records the fraction reached in time, which is a *result* of screening
coverage, symptom awareness and referral speed — the same things `access` and the
`diagnosis` blocker already describe from different angles. Three fields now
partly encode "did the system find this person", and they should probably be
reconciled before the register grows much further.

---

# Fourth pass — what breast cancer forced

## 23. `strata` — one entity, more than one answer · **applied**
*Forced by:* `breast-cancer`.

Stage I is cured; stage IV is not; both are breast cancer. No single
`intervention` rating is true of both, and averaging them produces a record that
describes nobody. `strata` lets a record carry sub-populations with their own
`intervention`, `efficacy` and `toll`, each with a population `fraction`, and
`check.py` verifies **the fractions sum to 1** — arithmetic, not judgement: they
partition the patients or they are not strata.

Records that span more than one capability are flagged **⧉**, which is the
register's way of saying the question is *malformed rather than hard*. That
distinction did not exist before and is probably the most useful thing this pass
produced.

**This also supplies the second data point for gap 20**, and partly settles it:
stage strata handle *stage-determined* tiers. What remains open is sickle cell's
case — one population that could receive either gene therapy or hydroxyurea,
where the determinant is access rather than biology. Those are different
constructs and should not be forced together yet.

## 24. The window can cut both ways · **open, and important**
*Forced by:* `breast-cancer`.

Every previous window record assumed earlier is strictly better. Breast cancer
breaks it. Mammographic screening converts fatal cancers into curable ones **and**
inflicts the full toll on people whose cancer would never have surfaced —
overdiagnosis, estimated at somewhere between a tenth and a third of
screen-detected cancers, with the methods in genuine disagreement. Add DCIS and
the number grows.

So `harm without benefit` now occurs **inside a curable disease**, which the
schema did not anticipate: it currently only detects that category when
`capability` is `unsolved`. The checker cannot see the breast-cancer instance at
all.

The lever is neither more screening nor less; it is a way to tell which tumours
need treating, which is a `knowledge` blocker. Worth noting that the *disagreement
itself* may make this a `contested: true` case in disguise.

## 25. The quadrant map has one cell per entity · **open**
*Forced by:* `breast-cancer`, echoing `sickle-cell`.

Breast cancer belongs in `known/fixable` for its early strata and elsewhere for
its metastatic stratum. Sickle cell already needed two cells for a different
reason (de jure versus de facto). Two records now need to appear twice, so the
map is a presentation of a thing that is not two-dimensional.

## 26. Toll reduction is progress that moves no axis · **open**
*Forced by:* `breast-cancer`, retroactively visible in `hepatitis-c`.

Sentinel node biopsy replacing axillary clearance; genomic assays sparing
chemotherapy; hypofractionated radiotherapy; interferon giving way to DAAs. Each
removed enormous permanent harm and changed **capability not at all**, so the
register records them as nothing happening.

`toll` can now hold the fact but there is no way to see the *trajectory*. `moved`
already dates changes to the axes; it should probably accept `axis: toll` so a
falling toll reads as the progress it is.

## 27. Stratification is not one-dimensional · **open**
*Forced by:* `breast-cancer`.

Subtype (hormone-receptor-positive, HER2-positive, triple-negative) drives
prognosis and treatment at least as strongly as stage, and it cuts *across* stage
rather than nesting inside it. `strata` supports one axis. A second orthogonal one
would multiply cells rapidly, so the honest interim position is to stratify by
whichever axis most changes capability and state the other in `holes` — which is
what the record does.

---

# 28. `diagnosis` conflated three different measurements · **applied**

*Forced by:* `breast-cancer`, then found in twelve of seventeen records on a
census. Raised by Jeremy as a direction for fndtn: *"in some cases we have
treatments, but we can't determine if it is needed or not… chemo doesn't work on
certain variations, but we prescribe it because that is all we got."*

The `diagnosis` axis answers one question — **is the disease present**. Clinical
practice needs three, and the standard trichotomy names them:

| | question | what its absence causes |
|---|---|---|
| **diagnostic** | is it there? | the patient is never found |
| **prognostic** | what will it do if left alone? | **overtreatment** — treating people who were never going to be harmed |
| **predictive** | will *this treatment* work in *this* patient? | **futile treatment** — full toll, no benefit, discovered only in retrospect |

The register has no way to record the second two, so their absence is currently
scattered across `evidence-incomplete`, `tooling`, `knowledge` and prose.

## The census — Jeremy's suspicion holds

**Twelve of seventeen records carry a prognostic or predictive measurement gap**,
and it is frequently the binding constraint rather than a detail:

| record | missing | consequence |
|---|---|---|
| breast-cancer | prognostic + predictive | overdiagnosis; adjuvant chemo given to many to benefit few |
| crohns | prognostic + predictive | cannot tell who will fibrose; cycles through biologics while damage accrues |
| depression | predictive | months of sequential trial and error |
| bipolar | predictive | lithium responders are a subset, unidentifiable in advance |
| epilepsy | predictive + prognostic | the drug-resistant third is unknowable until proven |
| low-back-pain | prognostic | cannot tell who becomes chronic, i.e. who carries the burden |
| sickle-cell | prognostic | identical genotypes, wildly different severity |
| pleomorphic-adenoma | prognostic | cannot tell which will recur or transform |
| rheumatic-heart-disease | prognostic | cannot identify the minority who will get rheumatic fever |
| amr-infection | predictive (slow) | 48–72h to susceptibility; the first days are guesswork |
| h-pylori-ulcer | predictive (not done) | empiric regimens fail against unmeasured resistance |
| snakebite | predictive (absent) | no point-of-care venom test; antivenom chosen by geography |

## Four kinds of measurement gap, needing four different actors

The census splits cleanly, and the split is the actionable part:

1. **Does not exist** — indolent-vs-lethal breast cancer, Crohn's fibrosis
   prediction, lithium response. A `knowledge` blocker; researchers.
2. **Exists but too slow** — AMR susceptibility testing. A `tooling` blocker;
   assay developers.
3. **Exists but not deployed** — H. pylori resistance surveillance, breast
   genomic recurrence assays, newborn screening. A `logistics`/`cost` blocker;
   health systems and payers. **Cheapest of the four, and it reduces toll
   directly.**
4. **Made unnecessary by a better treatment** — hepatitis C. Pan-genotypic DAAs
   removed the need to genotype: when a treatment works on everything, you no
   longer have to predict who responds.

That fourth route matters strategically. There are **two ways to close a
measurement gap** — build the test, or build a treatment good enough that the
question stops being asked — and only the first is obvious.

## Huntington's is the inverse, and it is instructive

Diagnostic and prognostic measurement here are near-perfect: a definitive genetic
test, available pre-symptomatically, with CAG repeat length predicting age of
onset. And there is nothing to do with the information. **Measurement without
capability is as useless as capability without measurement** — the register's
two-axis argument, one level down. So "work on measurement" is not universally
right; it pays where a treatment exists and is being aimed badly.

Which is exactly the twelve records above.

## Proposed shape, not yet built

```yaml
measurement:
  diagnostic: objective          # replaces the current `diagnosis` axis
  prognostic: none               # none | partial | good
  predictive: partial            # none | partial | good
  witness: >
    Genomic recurrence assays identify many women who can safely skip
    chemotherapy — predictive measurement that exists and is unevenly deployed.
    Nothing distinguishes an indolent early cancer from a lethal one, so
    prognostic measurement is absent and overdiagnosis follows directly.
```

Derived: **`overtreatment risk`** = capability is real, toll is `costly`/`harsh`,
and `prognostic` is `none`. On the current records that flags breast cancer,
pleomorphic adenoma and low back pain — three entities where people are harmed
because nobody can say who needed it. That list is probably the sharpest argument
the register could make for funding measurement over therapeutics.

**Built 2026-08-11.** Three things came out of implementing it that the paper
census did not predict:

- **Breast cancer rates `partial`/`partial`, not `none`.** It is *strong* where
  people assume it is weak — ER/PR/HER2 status is the paradigm predictive
  biomarker for all of medicine — and weak only on the specific question of
  whether a screen-detected cancer would ever have harmed the patient. Rating it
  honestly means it does **not** trip the overtreatment flag, even though
  overdiagnosis is its defining problem. See gap 29.
- **`n/a` turned out to be the most interesting value.** It made the
  hepatitis C route structurally visible: a measurement gap closed by building a
  better *treatment* rather than a better *test*. The checker enforces it —
  claiming `n/a` with a course-altering treatment and efficacy below 0.85 is an
  error, so it cannot be used to dodge a real gap.
- **The count came out 14/17**, against 12 on the paper census, because the
  checker counts any non-`good` rating while the hand pass counted only gaps that
  were binding. Both are defensible; the checker's criterion is the stated one.

## 29. The measurement flags cannot see a stratum-level gap · **open**
*Forced by:* `breast-cancer`, immediately on implementing gap 28.

`overtreatment_risk` requires `prognostic: none` at record level. Breast cancer's
prognostic measurement is `partial` overall and absent *only for the
screen-detected stratum* — which is precisely where overdiagnosis happens. So the
register's clearest overtreatment case is the one the overtreatment flag misses.

This is the same shape as gaps 20 and 25: record-level ratings cannot express
stratum-level facts. Three gaps now point at it, which is usually the sign that
the fix is `strata` absorbing more fields rather than another special case.

---

## 30. The interface could not express the register's own questions · **applied**
*Forced by:* the six canned questions, and by reading the code that implemented
them.

The page offered seven AND-ed dropdowns. Not one of the six canned questions
could be assembled out of them, and the filter state had quietly grown **four
parallel escape hatches** to compensate: `facets`, a `flags` set, an `or` list
that existed for exactly one question, and `pred` — a raw JavaScript closure, for
"blocked only by knowledge".

That is the diagnostic. The canned questions are the most valuable thing on the
page (the register *answering* rather than being read), and every one of them had
to go around the interface to get built. **A question you cannot type is a
question only the author can ask** — which makes the register a document rather
than a database, whatever the file format says.

Applied as `web/query.js`: `field:value`, space-as-AND, `-` negation, value-level
`(a OR b)`, numeric comparison with k/M/B, quoted phrases, free text. The
dropdowns survive as **query writers** — they append text to the box rather than
holding state, which makes the AND visible and teaches the syntax to someone who
never meant to learn it. All six questions are now saved query strings; `or` and
`pred` are gone.

Two things this cost, both recorded rather than hidden:

- Cross-term `OR` and parentheses are **deferred**. Value-level alternation has
  no precedence to get wrong; cross-term boolean algebra is where readers reliably
  misread. Typing it returns an explanation and the syntax that works.
- Two concepts had to be **derived** to keep the grammar small
  (`only_knowledge_blockers`, `measurement_gap` — see SCHEMA.md). The rule that
  keeps this honest: derive a flag when it names a concept the register *has*,
  never merely to route around a missing operator. Both were canned questions
  long before they were fields. Watch this one — a derived flag invented to dodge
  a grammar gap is a grammar gap in disguise.

## 31. The query language was built ahead of the data · **open, deliberate**
*Forced by:* nothing. That is the point of logging it.

Seventeen records do not need a query language; the corpus-before-schema rule
that governs everything else here says wait until a record forces the feature.
This was built anyway, for two reasons worth stating so they can be judged later:
the query string is the register's **API** (an LLM can emit
`capability:unsolved -blocker.kind:knowledge deaths:>50k`; it cannot operate seven
dropdowns), and it is the **share link** (`?q=` round-trips a view).

If the register stalls around twenty records, this was premature and the honest
entry is that a nicer set of dropdowns would have done. Revisit at fifty.

## 32. `src:recall` is now a query, and it returns everything · **open**
*Forced by:* building the `src` field.

The provenance ledger became queryable almost by accident — `src` collects every
`src` string in a record. The result is that `src:recall` matches all seventeen
records, which is the correct answer and an uncomfortable one. It is the sharpest
statement of gap 10 the register has: the headline metric is not computable
because *nothing here is verified*.

Worth keeping visible rather than tidying away. When the verification pass lands,
`-src:recall` becomes the list of what can actually be cited, and the gap closes
by that query returning rows.

---

## 33. `unknown` is not `unverified`, and `src` cannot tell them apart · **open**
*Forced by:* `msmds`, on the first attempt to write its `burden` block.

Every scalar in the register is `src: recall` — written from memory, unverified,
**checkable**. Someone can go and look up breast cancer's annual deaths. Nobody
can look up the prevalence of MSMDS: GBD does not cover it, no registry publishes
a denominator, and the literature counts *case reports* rather than patients. The
number does not exist to be verified.

That distinction is load-bearing for a register whose stated purpose is
priority — *"if x affects 6 people or millions"*. `recall` means the priority
question is answerable and hasn't been answered yet. `unknown` means it is not
answerable from published sources, and no amount of verification effort will
change that. Filing both as "unsourced" would let the verification pass close
with a number in the field and nothing behind it, which is exactly the failure
the ledger exists to prevent.

Recorded provisionally as `src: unknown` with a placeholder value and a note
saying not to compute with it. That is a squatting fix, not a design:

- `src` is currently free text (`recall` ×147, `reasoning` ×4, now `unknown` ×2).
  It wants a controlled vocabulary with the ladder made explicit —
  `unknown` < `recall` < `reasoning` < a citation.
- `unsourced_scalars` counts only `recall`, so `msmds` derives `0` while carrying
  two unknowable numbers and two reasoned ones. The metric currently rewards not
  using the word `recall`.
- A placeholder value in a numeric field is still a number. Something downstream
  will eventually sort on it. Better would be a null value with the units and
  `src` retained — but that needs the checker to stop requiring `value`.

`src:unknown` is at least queryable now, which makes the hole visible from the
page rather than only from this file.

## 34. Heterogeneity within a patient has no home · **open**
*Forced by:* `msmds`.

`strata` exists for one entity with more than one answer, and it validates that
the fractions **sum to 1** — because strata partition a population. Breast cancer
stage I and stage IV are different patients.

MSMDS is heterogeneous in a way that construct cannot hold. One mutation disables
smooth muscle everywhere, and capability differs sharply *by organ within the
same patient*: the ductus arteriosus is closed and stays closed (a real fix), the
aorta is replaceable prophylactically (a fix with a permanent price), the cerebral
arteriopathy has essentially nothing, and the bladder and gut have management
only. Every patient has all four. Organs do not partition anybody.

This is **not** a variant of gaps 20, 25 and 27 — those are all about record-level
ratings being unable to express *sub-population* facts, and the fix they point at
is `strata` absorbing more fields. This is a second axis entirely: within-patient,
across systems. A schema that only knows how to split populations will keep
flattening multi-system disease to its worst organ, which is how MSMDS ends up
rated `symptomatic` with no trace that the PDA was genuinely fixed.

Worth resisting the obvious move of adding an `organs:` block until a second
record forces it — one example is a curiosity, two is a shape.

## 35. `harm_without_benefit` conflates the entity with the intervention · **open**
*Forced by:* `msmds`, which trips it and should not.

The rule is `capability == unsolved and terms != clean` — a major permanent toll
on an entity nothing can fix. It was never designed; it fell out of toll ×
capability, which is what made it interesting.

MSMDS satisfies it and the label is half wrong. The toll is real and permanent
(aortic replacement in childhood, lifelong anticoagulation, indefinite
catheterisation) and the entity is genuinely `unsolved`. But prophylactic aortic
surgery is not harm without benefit: it buys a specific death that does not
happen. The register is reading "the disease is not fixed" as "this intervention
gives nothing", and those come apart whenever an intervention prevents a discrete
fatal event without altering a course.

Huntington's could not have exposed this — it has no toll at all, so the rule
never fired on an entity where the toll bought something. Note the flag is not
simply wrong here either: the bladder and gut management genuinely is permanent
burden for no change in outcome. **One record, both readings, and the derivation
returns one boolean.** The fix is probably that toll belongs to an intervention
rather than to an entity, which is a larger change than it sounds and should wait
for a second forcing record.

## 36. A blocker can be conditional, and the schema states it as current · **open**
*Forced by:* `msmds`, and it sharpens gap 14.

MSMDS has perhaps a hundred described patients and no commercial route, so
`no-sponsor` looks like an obvious `documented` market failure. It is not one. No
sponsor has declined anything, because there is no candidate to decline — with
the knowledge and tooling blockers both closed, "nobody will fund it" is not
binding on anyone. It is a blocker that **would** bind if the ones above it
cleared.

Recorded as `alleged` to avoid overstating, which is the right call and the wrong
mechanism: `alleged` means *asserted but unverified*, and this is neither. It is
correctly predicted and not yet in force. The register now has a fourth thing the
standing axis is being asked to carry, alongside gap 14's want of a
`resolves_by:`.

This matters for the axis's original purpose. The refrain being tested is *"it is
solvable but pharma or the FDA will not allow it"* — and MSMDS is a clean case of
that refrain **not** applying, for a disease where it would have been extremely
easy to assume it did. Recording the negative result is as much the job as
finding the positive ones, and a schema that files a conditional blocker as a
current one would have quietly manufactured a fifth piece of evidence for a claim
Jeremy explicitly does not make.

---

## 37. An entity's definition can be a research instrument, and it has a version · **open**
*Forced by:* `heds`.

Every other record in the register has a boundary stable enough that nobody needs
to ask which version of it a figure refers to. hEDS does not, and the reason is
specific rather than accidental.

The 2017 International Classification deliberately **narrowed** hEDS, and said
why: to assemble a more homogeneous cohort in which to find the gene that twelve
of the thirteen EDS subtypes already have. Patients who no longer met the tighter
criteria were moved to a new category, hypermobility spectrum disorder. They were
not less unwell the following morning. **A definition was changed for the benefit
of researchers, and it reallocated patients.**

The register cannot say any of this. There is no `criteria:` or
`definition_version:` field, so:

- Prevalence is implicitly dated and the record cannot carry the date. Any figure
  means something different before and after 2017 (see #33).
- `residual: false` is true of hEDS and misses that hEDS **shed** a residual
  sibling. The flag describes an entity; it cannot describe a boundary's effect
  on the entity next door.
- The strongest reading of this record — that redrawing the line was a reasonable
  scientific move with an unreasonable clinical consequence — is expressible only
  in prose.

Do not add a field yet. ME/CFS has the same problem in weaker form (its
prevalence range is "a property of the definitions, not of measurement error"),
which is two records, but neither has yet been *misread* because of it. The thing
to watch for is the first time a query returns a number that is silently a
different entity's.

## 38. Both risk flags gate on capability, so the worst cases are invisible · **open**
*Forced by:* `heds`, and it retro-fits `low-back-pain`.

`overtreatment_risk` and `futile_treatment_risk` both begin with
`has_capability(rec)`, on the reasoning that a measurement gap only matters if
there is something real to aim. That reasoning has a hole.

hEDS is rated `predictive: none` — nothing says which patient will be helped by
joint stabilisation surgery or spinal fusion and which will be permanently worse.
Capability is `unsolved`, so neither flag fires, and the register's measurement
tables do not list it. Yet this is *futile treatment risk in its purest form*: an
irreversible intervention, offered widely, with no way to select. The same is true
of low back pain and failed fusion.

The distinction the flags are actually reaching for is not *is there capability*
but **is the intervention reversible**. Huntington's tetrabenazine is rated
`predictive: n/a` and that is fine — you stop the tablet. A craniocervical fusion
does not stop. An entity with no capability at all can still hand people
permanent harm on an unguessable coin flip, and that is a measurement problem
whatever the capability column says.

Both cases are currently caught by `harm_without_benefit` instead, so nothing is
being missed outright — but they are filed under *harm* when the actionable fact
is *unaimed*. Fixing this means the risk flags read the toll's reversibility
rather than the entity's capability.

## 39. An entity can be a final common pathway, and the register has no word for it · **open — NINE CITING RECORDS. `heart-failure`, THE CASE THIS GAP NAMED, IS HELD AS OF 2026-08-26. BUILD IT**
*Forced by:* `pots`.

POTS is defined by a measurement: a 30 bpm rise in heart rate on standing without
a fall in blood pressure. That criterion is objective, reproducible and nearly
free — and at least four distinct pathophysiologies produce it (partial autonomic
denervation, excess standing catecholamines, low plasma volume, and a probable
autoimmune group), which coexist and cannot be separated at the bedside.

The register has two words for "this entity is epistemically awkward" and neither
fits:

- `residual: true` means an idiopathic or non-specific bucket — *we found
  nothing*. Wrong here: POTS has positive, quantitative criteria.
- `contested: true` means the existence or definition is disputed. True here, but
  a different fact.

What POTS is, is **downstream**. It names an output that several mechanisms
share, and that is a legitimate and useful clinical category rather than a
defect — you can diagnose it, and the diagnosis carries real management
implications. But it guarantees three things the register currently has to
discover one field at a time: mechanism will read `partial` forever while
sub-mechanisms are individually solid, prognosis will be a population statement
and never a patient one, and **every unstratified trial will enrol a mixture and
dilute toward the null.**

That last consequence is the reason this deserves a field rather than a
paragraph. It supplies a *mechanical explanation* for a thin evidence base with
nobody having been negligent, and it makes a prediction: stratified trials should
succeed where unstratified ones have not. A register that could mark final-common-
pathway entities could ask "which of these has anyone tried to split", which is a
research-strategy question the axes cannot currently pose.

Do not add the field for one record. The candidates to watch are low back pain
(a presentation with many causes, but rated `residual` because nothing is found —
genuinely different) and heart failure, which is the textbook case and is not yet
in the register.

**UPDATE 2026-08-24 — `sepsis` is the third record and it is a better case than
heart failure.** Positive criteria, at least four distinct pathophysiologies
pooled under a clinical definition, a category that is genuinely useful at the
bedside, and eleven million deaths a year.

**And the prediction above came true at the largest scale medicine offers.** This
entry predicted that *"every unstratified trial will enrol a mixture and dilute
toward the null"* and that *"stratified trials should succeed where unstratified
ones have not"*. Sepsis has **over a hundred failed randomised trials** — anti-TNF,
IL-1 receptor antagonist, anti-endotoxin, nitric oxide synthase inhibitors, TLR4
antagonists, high-dose steroids, and drotrecogin alfa, approved in 2001 and
withdrawn in 2011 as the only sepsis drug ever licensed. The leading explanation
is precisely this mechanism, and the transcriptomic endotypes now described appear
to predict **opposite responses to corticosteroids**.

A gap written about a small autonomic condition predicted the largest trial
graveyard in medicine. Three records (`pots`, `low-back-pain` adjacent, `sepsis`),
a confirmed prediction, and a research-strategy question the axes cannot pose.
Build the field.

## 40. `predictive: none` means two different things, and POTS proves it · **applied to #38**
*Forced by:* `pots`, arriving directly after `heds`.

Not a new gap so much as the control case that confirms #38 and sharpens it into
something implementable.

hEDS and POTS both rate `predictive: none` — in neither can anyone say which
patient responds to which treatment. The stakes are not remotely comparable.
hEDS's unpredictable interventions include spinal and craniocervical fusion,
which do not come back. POTS's are salt, compression, reconditioning and a
sequence of cheap generics: try one, it fails, stop it, try the next.

So the register now holds a matched pair, and the variable that separates them is
**reversibility of the intervention**, not capability of the entity. #38 proposed
exactly that fix on the strength of one record; POTS supplies the other arm. The
concrete change: `futile_treatment_risk` should read `toll.permanent` rather than
gating on `has_capability()`. Under that rule hEDS fires and POTS does not, which
is the correct reading of both, and low back pain fires as well.

Left `open` rather than applied because changing a derivation rule mid-batch
would make the three new records unauditable against the ones already rated. It
should be the first thing done in the next pass.

## 41. A criterion that includes treatment response makes `efficacy` circular · **open, and the sharpest in this batch**
*Forced by:* `mcas`.

The consensus-1 criteria for MCAS require three things, and the third is
**response to mast-cell-targeting therapy**. A patient who does not respond does
not receive the diagnosis.

So `efficacy` — *the fraction of patients for whom the treatment works* — is
approximately 1.0 by construction, and it is not evidence of anything. It is the
criteria restated as a measurement. And `reach = efficacy × access` silently
collapses to `reach = access`, which means one of the register's two headline
numbers has quietly stopped carrying information for this record while looking
exactly like it does for every other one.

The second-order problem is worse than the first. **The non-responders are not
recorded as failures — they are removed from the denominator.** They do not
appear in this record with a poor outcome; they appear in whatever residual
bucket sits next door, or nowhere. A register built to count what is unsolved has
a blind spot precisely shaped like the people a treatment did not help, wherever
a diagnosis is partly defined by it having helped.

This is not an MCAS quirk. Any entity whose definition includes therapeutic
response has it — dopa-responsive dystonia is the textbook example, and
`steroid-responsive` and `treatment-resistant` qualifiers embed the same move
throughout medicine. The register cannot currently mark it, so:

- `efficacy` needs a flag for *circular — defined by response*, distinct from
  `src: recall` or `reasoning`, both of which imply the number means something.
- `reach` should probably refuse to compute rather than return a confident
  product of one real number and one tautology.
- The honest denominator is the population *before* the response criterion is
  applied, which is generally not published and may not exist.

Rated `0.9` rather than `1.0` in the record only to avoid a perfect score that
would look like a finding. That is itself a fudge and is noted here so it is not
mistaken for data.

## 42. Two live definitions is not one definition with versions · **open**
*Forced by:* `mcas`; escalates #37.

hEDS forced the observation that a definition has a **version** — 2017 narrowed
it, superseding 1997, and the register cannot date its figures. MCAS is a
harder case of the same family and needs saying separately, because the fix for
one does not fix the other.

MCAS has two criteria sets in **simultaneous** use, neither superseded:
consensus-1 requires an event-associated tryptase rise and makes the condition
rare; consensus-2 accepts a range of alternative mediators and makes it common —
by roughly three orders of magnitude. Each has its own literature, its own
clinicians and its own patient population.

A version field does not help here. There is no *later* definition to prefer;
there is a **fork**. And rating the entity at all requires choosing one, which
means:

- **The register took a side and cannot record that it did.** The file says so in
  a comment; nothing in the schema does, and nothing in the derived output does.
  A reader of `web/query.html` sees `capability: managed` with no indication that
  a different and equally live definition would produce a different record.
- **The register rated the uninteresting one.** Under consensus-1, MCAS is a
  small, real, reasonably managed condition. The disputed entity — the diagnosis
  given to large numbers of people with multisystem symptoms, the third leg of
  the asserted hEDS/POTS/MCAS triad, and the one carrying the overdiagnosis harm
  — is what makes MCAS worth arguing about, and it is not what this record rates.
  The toll reads `clean` while the harm everybody is arguing about sits under the
  other definition.

The candidate fix is that a record may carry more than one **rating context**,
each naming its criteria set, with the axes computed per context — closer to
`strata` than to anything else, except that it partitions definitions rather than
patients. Do not build it for one record. Watch for the second: chronic Lyme,
adrenal fatigue and the various long-COVID definitions are all shaped like this.

## 43. The borrowed identifier carries somebody else's boundary · **open**
*Forced by:* the Mondo resolution pass, `resolve_mondo.py`.

*"Disease identifiers are borrowed, never minted"* is the right rule and it has a
cost nobody had priced. Eighteen of twenty-one records now carry a `mondo:` id,
and in at least three the Mondo term and the register's entity **are not the same
thing**:

- **h-pylori-ulcer** → `MONDO:0004247` *peptic ulcer disease*. Ours is peptic
  ulcer caused by *Helicobacter pylori*; Mondo's term includes NSAID ulcers.
  A **parent**, accepted knowingly, and the record cannot say so.
- **heds** → `MONDO:0007523` *Ehlers-Danlos syndrome, hypermobility type* — the
  **pre-2017 name**, and therefore the pre-2017 boundary. This is gap #37
  arriving through the join key: anything joined on that id returns data
  assembled under criteria the record explicitly says were superseded.
- **mcas** → `MONDO:0100004`, one term for what gap #42 argues is two entities
  with a threefold-order-of-magnitude disagreement about who has it.

The join key is the whole point of resolving these — GBD, Orphanet and the trial
registries are all keyed on it — so a silent scope mismatch is exactly the kind
of error that produces a confident wrong number later. What is missing is a way
to record the relation: *same as*, *broader than*, *narrower than*, *dated to an
older definition*. SKOS has this vocabulary (`exactMatch`, `broadMatch`) and
that is probably the answer, but not for three records.

**The near-miss is worth keeping in view.** The tool's first run auto-accepted
`MONDO:0005412` *duodenal ulcer* for h-pylori-ulcer, because that string is in
the record's `also` list and exactly matches a Mondo label. It is the wrong
entity — it excludes gastric ulcers and says nothing about *Helicobacter* — and
it would have joined cleanly to somebody else's data forever. The fix was to
trust only `name` for auto-acceptance, since the schema defines `also` as
*"synonyms people actually search for"*, which are search aliases and not
equivalences. **A field that was documented as loose was being used as if it were
strict.** Worth checking whether anything else reads `also` that way.

## 44. Three records have no identifier, for three different reasons · **open**
*Forced by:* the same pass.

Not a failure of the lookup. Each says something:

- **low-back-pain** — `kind: complaint`. **Mondo is a *disease* ontology**, so a
  complaint has no term there by construction; symptoms live in HPO. The
  register's own `kind` axis therefore predicts which ontology can supply an id,
  and "borrow, never mint" needs a *second* source before it covers the whole
  register. This is the most structural of the three.
- **amr-infection** — antimicrobial resistance is a property of an organism, not
  a disease entity. No ontology *of diseases* will ever have it, and the record
  is arguably a category the register invented for good reasons that nothing
  external shares.
- **pots** — Mondo has `MONDO:0011479` *POTS due to NET deficiency* (a rare
  subtype) and `MONDO:0001315` *orthostatic intolerance* (the parent), and
  **nothing for POTS itself**. That is a plain gap in Mondo rather than a
  conceptual problem.

The last one has an action attached, and it is the more interesting half of
"borrow, never mint": **Mondo takes term requests.** A register that finds a
missing term can ask for it rather than minting a private id, which keeps the
borrowing rule intact while making the register a contributor upstream instead
of only a consumer. POTS is the first candidate.

## 45. "Did the treatment work" is a fourth measurement question · **open — THREE RECORDS; THE DEFERRAL NOTE WENT STALE AND WAS FOUND BY THE #69 AUDIT 2026-08-26. BUILD IT.**
*Forced by:* `chagas`.

The `measurement` block asks three questions — *is it there* (diagnostic), *what
will it do untreated* (prognostic), *will this treatment work in this patient*
(predictive). **All three are asked before treatment.** There is a fourth, asked
after, and Chagas has no answer to it: **did it work?**

Cure in Chagas is defined serologically, and antibodies take years to decades to
disappear after successful treatment. The endpoint lies beyond any episode of
care. So a patient completes sixty days of a drug that makes a large minority
ill and **never learns whether it worked** — and neither does their clinician,
and neither does a trialist, which is why the field leans on parasite detection
as a surrogate and why BENEFIT's result was so hard to read.

Hepatitis C is the contrast that shows how much this axis carries. A PCR at
twelve weeks says cured or not cured, definitively, inside one clinic visit. A
great deal of that record's optimism rests on a fact the schema never records.

Why it is not just `predictive` under another name:

- `predictive` is a **selection** question — pick the right treatment. It is
  answered by a marker measured *before*.
- test-of-cure is a **verification** question — confirm the outcome. Without it,
  trial-and-error has no feedback loop and cannot terminate. This is what
  separates Chagas from POTS: POTS is also `predictive: none`, but there you
  observe the outcome and move on, so the sequence converges. Chagas never
  converges, because nothing is ever observed.

Candidate field: `measurement.confirmatory: good | partial | none | n/a`, with
`n/a` for entities where cure is not a concept (Huntington's, hEDS). Do not add
it for one record. Watch for the second — tuberculosis, *H. pylori* eradication
(which does have a breath test, and is the positive case), and any oncology
record where "did we get it all" is the live question.

**AMENDED 2026-08-26 — the second and third arrived and both named candidates are
held.** `scabies` and `visceral-leishmaniasis` cite this gap, giving three
records with `chagas`. **And both diseases named in the paragraph above are now
in the corpus**: `h-pylori-ulcer` is held and is the positive case exactly as
predicted — a urea breath test confirms eradication, which is why that record can
rate `curative` without hedging. `tuberculosis` is held and its own text says
*"no test of cure, so treating them means giving drugs to ten or twenty people"*
— the negative case, in the largest infectious-disease record in the register,
not citing this gap number and demonstrating it anyway. Found by the audit in
#69, not by anybody re-reading this. **Build `measurement.confirmatory`.**

## 46. Curing the cause need not cure the disease · **open — THIRD RECORD ARRIVED 2026-08-24, FROM THE OPPOSITE POLE**
*Forced by:* `chagas`.

Every rung of the intervention ladder quietly assumes that removing the cause
removes the disease. `curative` is defined as *a finite intervention ends it*.

Chagas violates this, and not as a matter of interpretation. Benznidazole
clears *Trypanosoma cruzi* from most people who complete a course. The **BENEFIT
trial (2015)** gave it to patients with established Chagas cardiomyopathy,
reduced parasite detection as expected, and found **no reduction in cardiac
deterioration**. The parasite goes; the heart still fails, because conduction
tissue and enteric neurons do not come back and the process may by then be
self-sustaining.

So `intervention: curative` is true of the **infection** and possibly false of
the **disease**, and the axis cannot hold both. The record rates `curative` and
puts the qualification in prose, which is exactly the failure mode this register
exists to avoid — a rating that reads clean and needs a paragraph to be honest.

This is close to the register's `window` concept and is not the same thing. A
window says *capability changes with timing*. This says **the target of the cure
and the target of the disease are different objects**, which is why treating late
fails: not because you missed a deadline, but because you are curing the wrong
thing by then. Rheumatic heart disease has the same shape — the streptococcus is
long gone and the valve is still scarred — and the register did not notice
because that record rates `disease-modifying` and never had to claim a cure.

Two records now. Worth a field when a third arrives, probably distinguishing
*aetiological* from *clinical* cure.

**UPDATE 2026-08-24 — `sepsis` is the third, and it sits at the opposite end of
the same axis.** Chagas: aetiological cure succeeds, clinical cure fails — the
parasite clears and the heart still fails. Sepsis: **aetiological cure IS the
clinical cure**, and the entity has no therapy of its own and never has had one.
Antibiotics treat the infection, everything else holds the organs up, the syndrome
resolves, and `intervention: curative` is earned without a single treatment aimed
at sepsis. Over a hundred trials have tried and failed to produce one.

So the pair spans the range, which is what makes the distinction implementable
rather than a special case:

| record | aetiological cure | clinical cure |
|---|---|---|
| `chagas` | yes | **no** — the conduction tissue is gone |
| `rheumatic-heart-disease` | yes (long since) | **no** — the valve is scarred |
| `sepsis` | yes | **yes, and it is the only cure there is** |

The third record has arrived and the field it asked for is the same one #39 now
needs. Consider building them together — a final-common-pathway entity is exactly
the kind whose cure targets something other than itself.

## 47. Permanence is the wrong variable for the risk flags · **open, supersedes the fix proposed in #40**
*Forced by:* `chagas`, which is the register's clearest overtreatment case and
trips **neither** overtreatment flag.

The facts: roughly two thirds of people infected with *T. cruzi* never become
ill. Nothing identifies which. So everyone diagnosed is offered sixty days of a
drug that a large minority cannot tolerate, and afterwards nobody can tell
whether it worked. Two thirds of the treated were treated for nothing.

`overtreatment_risk` requires `terms in (costly, harsh)`, which requires a
**permanent** toll. Benznidazole's harms mostly reverse on stopping, so the toll
rates `minor`, the terms read `clean`, and the flag stays silent.

#40 proposed replacing the `has_capability()` gate with `toll.permanent`, on the
strength of the hEDS/POTS pair. **Chagas shows that is still wrong.** Permanence
is a proxy for the thing that actually matters, which is whether the cost can be
recovered — and there are at least two ways it cannot:

| | irreversible harm | unrecoverable burden |
|---|---|---|
| example | hEDS craniocervical fusion | Chagas, sixty days of benznidazole |
| what is lost | function, permanently | two months of being ill, for nothing |
| `toll.permanent` | true | **false** |
| flag fires today | no (capability gate) | no (permanence gate) |

POTS remains the case that should *not* fire, and the reason is now sharper than
"reversible": there, the outcome is observable, so the trial-and-error converges
and the cost per trial is small. The three variables the flags actually want are
**reversibility, magnitude, and observability of the outcome** — and the third is
gap #45.

Do not patch the rule again on one more record. Three records now disagree with
it in three different ways (hEDS, POTS, Chagas), which is enough to redesign it
rather than keep adding gates, and that redesign should wait until `confirmatory`
exists so it can read all three.

## 48. The register cannot rank by preventable burden · **open, and the most serious gap logged so far — AMENDED by #182: the missing multiplier is burden, not deaths**
*Forced by:* `tuberculosis`.

Every triage view here sorts on a **fraction** (`reach`) or a **price**
(`cheapest_priced_blocker`). None multiplies either by **magnitude**. So the
register's answer to its own stated purpose — *"based on the data, what should
the next project be"* — is systematically wrong in the one direction that
matters most.

Tuberculosis makes it undeniable. Reach 0.612, and **1.25 million deaths a
year** — the deadliest infection on earth, curable at every stratum, with drugs
older than most of the people taking them. Here is the ⚑ no-champion list, which
is what the *"where would $10M go furthest"* question returns, next to what the
entries actually kill:

| on the ⚑ list | reach | deaths/year |
|---|---|---|
| breast-cancer | 0.36 | 670,000 |
| rheumatic-heart-disease | 0.20 | 300,000 |
| hepatitis-c | 0.19 | 240,000 |
| snakebite | 0.225 | 100,000 |
| **tuberculosis — EXCLUDED** | **0.612** | **1,250,000** |

`orphaned` requires reach below `ORPHAN_REACH_CEILING = 0.6`. TB sits at
**0.612**. **The largest preventable-death entry in the register is excluded
from its flagship triage view by twelve thousandths of a fraction**, and every
number in that comparison is doing exactly what it was designed to do.

The ceiling is not the bug — moving it would only relocate the arbitrary line.
The bug is that **reach is a proportion and burden is a magnitude, and nothing
combines them.** A rare disease at reach 0.03 outranks TB at reach 0.6 in every
view here, while closing TB's delivery gap would save more lives than closing
every other gap in the register put together.

What is missing is a derived quantity along the lines of **unreached burden** —
deaths (or DALYs) × (1 − reach) — which would make the register answer the
question it was built for. Three obstacles, all real and none fatal:

- It requires a burden figure on every record, and three records have none that
  can be computed with (gaps #33, #44) — so the metric must report *uncomputable*
  for them rather than treat missing as zero, which would rank exactly the
  records the register knows least about at the very bottom.
- Deaths under-count morbidity-only entities. Four records — low back pain, hEDS,
  MCAS, POTS — have essentially zero mortality and enormous disability. DALYs
  are the right unit and the register does not carry them.
- It will be read as a funding recommendation, which is a much stronger claim
  than a register of `src: recall` values can support.

**This should be built before the crowd-contribution work.** The whole argument
for making Nordstern public is that it answers "what next", and right now it
answers it wrongly.

## 49. `prevention` carries no efficacy · **open**
*Forced by:* `tuberculosis`.

The `prevention` axis has four values — `eradicated`, `prophylaxis`,
`risk-reduction`, `none` — and **no number attached to any of them**.

BCG dates from 1921 and is the most widely administered vaccine in human
history. It reliably prevents disseminated and meningeal TB in young children.
It also largely fails against adult pulmonary disease — the form that drives the
epidemic — with measured efficacy ranging from roughly nothing to eighty percent
by latitude, unexplained for decades.

Rheumatic heart disease's monthly benzathine penicillin prophylaxis is close to
fully protective. **Both read `prophylaxis`.** The axis cannot distinguish a
prophylaxis that works from one that mostly does not.

The asymmetry is odd once seen: treatment carries `efficacy` *and* `access`, and
prevention carries neither. That is backwards for a register whose whole thesis
is that prevention is independent of treatment and not a continuation of it —
PKU's phenotype is prevented outright and the disease is never cured, and the
register can say the first half but not how well it works.

Cheap fix, and it should wait for the burden metric above rather than being
bolted on alone: `prevention` becomes a block with `rung`, `efficacy` and
`coverage`, mirroring the treatment axes. Note what it would immediately reveal —
a new TB vaccine that worked would move **nothing** on this record as it stands.

## 50. The cost ledger counts one of three costs · **cost 2 APPLIED; cost 3 still open**
*Forced by:* `tuberculosis`, which carries all three at once.

`toll` records **what the cure takes from the treated patient, permanently**.
That is one of at least three permanent costs a disease imposes, and the other
two have nowhere to go:

**1. What the cure takes from the patient.** `toll`. Present, and well
exercised — the facial nerve, the bowel, fertility.

**2. What the *disease* leaves behind in a patient who was successfully cured.**
**APPLIED 2026-08-21 as the `residue:` block**, after Jeremy read the TB entry and
said the obvious thing: *"half of people cured have lung damage, not a great cure
tbh."* He also supplied the better framing, which became the derived field —
**are they back to the state prior to disease and treatment?** That question
unifies the two costs, because `toll` and `residue` are simply the two ways the
answer is no. See SCHEMA.md; eight records carry a residue, `restored` is derived
from both halves, and sickle cell is the only `both`.
Left below as originally written, because the reasoning is what justified the
field:
Up to half of people cured of pulmonary TB have permanent lung impairment —
bronchiectasis, fibrosis, cavities. So the register records `toll: minor` and
`terms: clean` for a disease that permanently damages the lungs of millions of
*survivors*. This is not new to TB: hepatitis C's own witness notes that a cured
patient may keep established cirrhosis and its cancer risk, and rheumatic heart
disease is the scarred valve left by a streptococcus long gone. **Three records,
so it is a shape.** "Cured" is not one outcome, and the register currently says
it is.

**3. What treatment failure costs *third parties*.** Incomplete TB treatment
selects for resistance, and the resistant organism infects other people. The
whole MDR stratum in that record is that cost made visible — it is *manufactured*
rather than encountered. Nothing in this schema counts a harm to anyone other
than the treated patient, and this is the only record where the mechanism is
explicit enough to be undeniable. It is also why regimen shortening is not a
convenience: cutting six months to four is an adherence intervention delivered as
pharmacology, acting on transmission and resistance rather than on the individual.

Cost 2 became exactly that sibling field. What the migration taught, beyond the
design: **`minor` had to be a usable answer or the field would have collapsed
into a second `major` flag.** *H. pylori* eradication leaves permanent atrophic
gastritis and a residual gastric cancer risk in a minority — real, permanent, and
correctly not enough to stop the record deriving `restored`. And **suppressive
records ask the question differently**: nobody finishes treatment, so HIV's
residue is "back to baseline *while treated*", which turns out to be a function
of how late the diagnosis was — an argument for the `diagnosis` blocker rather
than a separate problem.

Cost 3 is a different animal — it is an externality, it belongs to the population and not to
a patient, and it may be the thing that finally forces the register to hold
something other than a per-entity row.

## 51. The residue can be the transmission reservoir · **open**
*Forced by:* `visceral-leishmaniasis`, one day after `residue` was added.

**Post-kala-azar dermal leishmaniasis** appears months to years after apparently
successful cure: a skin eruption, usually not severe enough to send anyone to a
clinic — and **infectious to sandflies**. In an anthroponotic disease where
humans are the only reservoir that matters, PKDL patients are what carries
transmission through the gaps between outbreaks. And because the rash rarely
makes anyone feel ill, **the people sustaining the epidemic are precisely the
people not seeking care.**

The record rates `residue.severity: minor` and it derives **`restored`**. Both
are honest: for the modal patient the rash self-heals or is treatable, and they
really are back to how they were. The register says the patient is restored and
cannot say the community is not.

This is uncomfortable in a specific way. `residue` was added *yesterday*,
precisely because `toll` could only see one kind of cost — and it has inherited
the same blind spot, because it also measures harm **to the treated patient**.
Tuberculosis had these as two separate objects: lung damage to the patient
(cost 2) and manufactured resistance to everyone else (cost 3). Here they are
**one object**, which is why a severity rating cannot be made to carry it: raise
PKDL to `major` and the record lies about the patient; leave it `minor` and the
record misses the mechanism by which the disease survives.

So gap #50's cost 3 is not an optional third field. It is a **different axis of
accounting** — the population, not the patient — and this record is the proof,
because no amount of tuning the patient-side fields reaches it. Note what it
would change if it existed: treating PKDL, which makes nobody feel much better
in a hurry, would be visible as one of the highest-value acts available in the
whole register.

**Method note worth keeping.** This was found by writing the twenty-fourth
record, not by thinking harder about the schema the day the field was designed.
Corpus before schema, again.

## 52. Solved here, not there — the register has one global row · **open — FIVE RECORDS; THE DEFERRAL NOTE WENT STALE AND WAS FOUND BY THE #69 AUDIT 2026-08-26. BUILD IT.**
*Forced by:* `visceral-leishmaniasis`.

Bangladesh was validated in 2023 as the **first country ever** to eliminate
visceral leishmaniasis as a public health problem. The Indian subcontinent went
from roughly seventy-seven thousand cases in 2007 to a few thousand. Over the
same period **East Africa became the majority of the world's burden** and is
getting harder — worse drug response, HIV co-infection, conflict.

Same disease. Same drugs. Opposite trajectories. One row.

What makes this more than an averaging complaint is that **the variation is not
only access**:

| | Indian subcontinent | East Africa |
|---|---|---|
| first-line | one infusion, one day | 17 days, includes a cardiotoxic antimonial |
| efficacy | ~0.95 | ~0.88 |
| rK39 sensitivity | ~95% | ~85% |
| PKDL after cure | ~5–10% | reported up to half |
| trajectory | eliminated / near-eliminated | rising share of global burden |

Efficacy, toll, diagnostic performance and residue all differ, and *why* the
same drug works less well in East Africa is genuinely unresolved. That is
biology, not logistics.

`strata` gets partway and then stops, and the stopping point is instructive:
**a stratum may override `intervention`, `efficacy` and `toll` — and not
`access`.** Geography's largest effect is on access, and access is exactly the
field strata cannot carry. So the record can say East African patients get a
worse regimen and cannot say South Sudanese patients are less likely to be
reached at all.

This generalises hard and the register should expect it — malaria, TB and HIV
are all far more geographically differentiated than a single global row admits,
and TB's record already blends them silently. The likely shape is that `access`
becomes stratifiable, which is a smaller change than a geography block and
covers most of the loss. Do not build it for one record; the second is
predictable and will arrive on its own.

**AMENDED 2026-08-26 — it did, four times, and "will arrive on its own" turned
out to describe the records rather than the fix.** Five cite it:
`visceral-leishmaniasis` (forcing), `hat`, `cataract`, `cervical-cancer` and
`gastric-cancer`. And the prediction in the paragraph above — *"malaria, TB and
HIV are all far more geographically differentiated than a single global row
admits"* — is now testable against three held records, all of which blend
geographies silently. **`tuberculosis` was re-rated on 2026-08-24 and the
re-rating did not fix this**, because there is nowhere to put it.

**One thing this record does say that no other does:** an entity can be
*eliminated somewhere*. The register has `moved:` for ratings changing over time
and nothing for a rating being true in one place and false in another, and the
first is only half of "are we winning".

## 53. Diagnosis can be skipped on purpose, and the register calls that a gap · **open**
*Forced by:* `schistosomiasis`.

The register has been repeating one claim for six records: the test exists, it is
cheap, it is not being done, and doing it is the cheapest lever available. The
`diagnosis` blocker is now the second commonest kind and `index.md` says so in
bold.

**Schistosomiasis does not diagnose people on purpose.** Control is mass drug
administration — praziquantel handed to whole populations of school-age children,
untested — because a tablet costs a few cents and a Kato-Katz slide costs more
than treating the child. That is arithmetic. It is the correct call. And the
register has no way to record a diagnosis gap that is a *decision* rather than a
failure, so this record's blocker reads like every other one and means the
opposite.

What the decision buys, and what nothing in the schema can hold:

- **No test of cure, structurally.** A programme that never tests cannot
  distinguish treatment failure from reinfection from surviving immature worms —
  so **reduced praziquantel susceptibility cannot be detected until it is large
  enough to show in aggregate egg counts.** For a disease with one drug, that is
  the whole surveillance question. (Gap #45, arriving by a fourth route: Chagas
  has no test of cure, TB has one only for active disease, VL's dipstick cannot
  become one, and here nobody looks.)
- **No individual denominator.** Coverage is the only measurable output, so the
  programme can report what it dispensed and not what it achieved.
- **The test degrades exactly as the programme succeeds.** Kato-Katz loses
  sensitivity at low infection intensity, which is the state a working programme
  creates. **The tool that works for control fails for elimination** — the same
  shape as VL, where the subcontinent's success made the remaining cases the hard
  ones to find.

The fix is probably that a blocker needs to distinguish *the lever is not being
pulled* from *the lever is deliberately not pulled, and here is what that costs*.
Until then, read the register's cheapest-lever claim as holding in the POTS and
Chagas sense and **not** here.

## 54. The register records what works, never how fragile it is · **open**
*Forced by:* `schistosomiasis`, and it retro-fits two records already written.

Praziquantel has been the entire chemotherapeutic answer to schistosomiasis
since the 1970s. **One drug. No second line. No alternative class. No licensed
vaccine. Two hundred and forty million infected people, and a control strategy
that depends on it and on a manufacturer donating hundreds of millions of tablets
a year.**

Every field here says that is fine. `intervention: curative`, `efficacy: 0.87`,
`toll: minor` — an excellent record. Nothing captures that it is a single point
of failure, or that the surveillance which would give early warning is the
surveillance gap #53 describes.

It is not one record. Now that it has a name it is visible in three:

| record | the concentration risk |
|---|---|
| schistosomiasis | one drug, since the 1970s, no backup |
| visceral leishmaniasis | the elimination programme's key drug arrives by manufacturer donation |
| tuberculosis | one new drug in 49 years, and the pipeline behind it is thin |

And all three sit next to the same finding — that the answer to neglected-disease
economics has been an improvised institution rather than a market. **A donation, a
product development partnership and a philanthropic pipeline are each a
dependency**, and the register currently reads them as solutions.

Candidate shape: `redundancy` on the intervention — how many independent things
work, and what happens if the first fails. It matters most exactly where the
register currently looks best, which is why it will keep being invisible until
something breaks.

## 55. The register is a table of nodes with no edges · **open**
*Forced by:* `schistosomiasis`, most sharply.

Female genital schistosomiasis affects tens of millions of women, is routinely
mistaken for a sexually transmitted infection, and is **associated with a
substantially raised risk of acquiring HIV.** So some share of HIV infections in
endemic Africa are caused by an untreated worm, and:

- the schistosomiasis record cannot count them in its burden,
- the HIV record cannot attribute them to a preventable cause,
- and treating schistosomiasis is therefore an HIV intervention that neither
  record can express.

One row per entity, and no way to say that one entity causes, worsens or gates
another. The edges are everywhere once looked for: TB is the leading cause of
death in HIV (handled by burying it in a stratum); MDR-TB is simultaneously a TB
record and an AMR record; *H. pylori* causes gastric cancer; hepatitis C causes
hepatocellular carcinoma; rheumatic heart disease is caused by a streptococcal
infection that has its own natural history.

This is not the same as gap #50's cost 3, which is about harm to *third parties*.
This is harm to the same patient, recorded under a different disease — and it
systematically **understates the value of treating whatever sits upstream.** Any
burden-weighted priority metric (gap #48) computed on a table with no edges will
rank the downstream disease and miss the lever.

The honest note: this is where a register becomes a graph, and that is a much
larger change than any field discussed so far. It should not be attempted before
the burden metric exists, because the burden metric is what would make the edges
worth traversing.

## 56. The endgame inverts everything, and the register is linear · **open — but two claims below were wrong; see `smallpox`**
*Forced by:* `hat`.

`reach = efficacy × access` treats delivery as a fraction, and a fraction has no
memory of where on the curve it sits. Getting from 20% to 30% and from 99.8% to
99.9% are the same ten-thousandths of arithmetic and nothing like the same
problem.

Human African trypanosomiasis is at the far end of that curve — from over
300,000 cases a year in the late 1990s to fewer than a thousand — and at that end
everything reverses:

- **The screening test gets worse without changing.** A test with excellent
  specificity produces *mostly false positives* when prevalence falls to a
  handful per hundred thousand. The test did not degrade; the population did.
  Schistosomiasis hit the same wall from the other direction, where Kato-Katz
  loses sensitivity at exactly the low infection intensities a successful
  programme creates. **Two records, same shape: the tools that achieve control
  are the wrong tools for elimination.**
- **Cost per case found rises steeply.** Screening ten thousand people to find
  one costs what screening ten thousand to find fifty costs. The economics
  worsen precisely as the political case for spending weakens.
- **The last cases are in the hardest places** — for HAT, the DRC and pockets of
  CAR, South Sudan, Angola. Last-mile in the literal sense.
- **`orphaned` switches off.** HAT derives reach 0.665, above the 0.6 ceiling, so
  it drops off the no-champion list — the same way tuberculosis does at 0.612
  (gap #48), and for the opposite reason. TB is excluded because the gap is
  enormous and the fraction looks fine; HAT is excluded because the gap really is
  nearly closed and closing the rest is the expensive part.

The register can say a thing is 66% delivered. It cannot say whether that is the
easy two thirds or the hard one, and those want opposite kinds of money.

## 57. The register cannot value maintenance · **open, and it is the sharpest limit found so far**
*Forced by:* `hat`.

**Everything this register measures is a gap.** Capability against reach, blockers
against cost, burden against what is preventable. A gap that closes becomes
invisible — and staying closed can cost money forever.

Human African trypanosomiasis is the proof, and it is not a thought experiment.
Cases were down to a few thousand around 1960. Colonial-era screening programmes
were wound down through independence, war and structural adjustment. **The
disease returned to hundreds of thousands of cases by the 1990s.** The current
achievement is a re-taking of a position that was previously held and lost.

So the honest reading of this record is two incompatible things at once:

| reading | verdict |
|---|---|
| against the 1990s | one of the great public health achievements of the century |
| on its own numbers | 800 cases a year — a rounding error |

And gap #48's burden-weighted priority metric, which I argued should be built
before anything else, **would rank HAT at approximately zero.** Accurately, for
the burden that exists. Catastrophically, for the value of not losing it again.

This is a genuine design problem rather than a missing field, and it should be
faced before the metric is built:

- A register of *what is unsolved* structurally cannot argue for spending on
  *what is solved*, and "keep paying to hold a zero at zero" is a real and
  frequently correct answer to "what should we work on next".
- The candidate shape is something like **`reversibility`** — what happens to
  this rating if the current effort stops — which is the achievement-side twin of
  gap #54's `redundancy`, which asks what happens if the current *tool* fails.
  Both are questions about fragility, and the register currently records only
  states.
- Smallpox is the control case the corpus is missing. It is the one entity where
  the answer is *nothing happens, it is over* — and until something in here can
  distinguish that from HAT, the register cannot tell a finished job from a job
  being held finished by continuous effort.

**Note the interaction with `moved:`.** The rename argued `moved:` is
load-bearing because it makes a second pass a comparison. Every `moved` entry so
far records an improvement. HAT's history says the field must be equally able to
record a rating going backwards — and that nobody has yet had to write one is a
property of which records were chosen, not of medicine.

## 58. The intervention axis is patient-scoped, and some interventions are not · **open**
*Forced by:* `onchocerciasis`.

**Ivermectin does not kill the adult worm.** It kills microfilariae. Given
annually it holds the microfilarial load near zero — which stops the eye and skin
damage and stops transmission — while the adult worms go on living for their ten
to fifteen years and then die of old age. **Nobody is ever cured by the drug.**
The infection ends by attrition, under suppression.

So the same tablet produces two different verdicts depending on what you point
the axis at:

| scope | verdict |
|---|---|
| the patient | `suppressive` — held, for fifteen years, never cured |
| the community | **eliminated** — Colombia, Ecuador, Mexico and Guatemala verified free of it |

The record rates `suppressive`, correctly, and a reader would never guess that
four countries have eradicated it. `capability: managed` is what the register
says about a disease being driven out of the hemisphere.

Two consequences worth separating:

- **`prevention: eradicated` exists as a value and is unreachable here**, because
  the eliminating act is *treatment*, filed under `intervention`. In an
  anthroponotic disease, treating people IS the prevention programme — the same
  observation visceral leishmaniasis forced and this record makes structural.
- **There is no field for the DURATION of commitment an intervention demands.**
  A single curative dose and a fifteen-year annual suppression programme read
  identically on `ongoing: low`, which is true of the patient and wildly false of
  everyone paying for it. This is the front-loaded twin of #57: HAT must keep
  spending *after* it has won; onchocerciasis must keep spending for fifteen
  years *before* it can, and stopping early loses most of what was bought.

The likely shape is that `intervention` needs a scope — *what this does to a
person* against *what sustained delivery does to a population* — which is a
larger change than a field. Note that it is also where a deployable
macrofilaricide would matter most: it would collapse a fifteen-year institutional
commitment into a course of treatment, and nothing on this record's axes would
move.

## 59. `predictive` asks about benefit; sometimes the question is harm · **open**
*Forced by:* `onchocerciasis`, and it is the sharpest form of #55.

The measurement block asks *will this treatment work in this patient*. In
onchocerciasis that is close to trivial — ivermectin clears microfilariae in
essentially everyone. **The question that matters is the opposite one: will this
treatment kill this patient?**

Where *Loa loa* is co-endemic — parts of Cameroon, the DRC, the Central African
Republic and Congo — ivermectin given to someone carrying a heavy Loa
microfilarial load can cause encephalopathy, coma and death. So mass distribution
is restricted or suspended in exactly the districts where onchocerciasis
persists: **the last reservoir of a nearly-eliminable disease is protected by a
second parasite.**

Three things the schema cannot say, in ascending order of importance:

1. **`predictive` has no room for harm.** It is benefit-scoped by construction.
   Yet the harm question here is *answerable*, which makes this the positive case
   the register lacked — gaps #40 and #47 are about unpredictable harm, and this
   is predictable, avoidable harm with a tool built for it.
2. **The tool is a diagnostic whose entire purpose is exclusion.** A
   point-of-care video microscope counts Loa microfilariae from a finger-prick in
   about two minutes, in a village, so the few people at risk can be identified
   and **not** given the tablet everyone else receives. Every other `diagnosis`
   blocker in this register is about finding people to treat. This is the third
   inversion in four records — schistosomiasis skips diagnosis because the drug
   is cheaper, HAT tests exhaustively because the drug was arsenic, and this one
   tests to withhold.
3. **This is gap #55 at its worst.** Not *disease A causes disease B*
   (schistosomiasis raising HIV acquisition), but **the treatment for A is lethal
   in the presence of B** — where B has no row in this register at all. The toll
   rating is a function of a co-infection the register does not track, so the
   strata can show the split and nothing can show its cause. A table of nodes
   with no edges cannot express a contraindication.

Do not add a harm-prediction field alone. It is one face of the missing relation
model, and building it separately would leave the same fact half-recorded in two
places.

## 60. `residue` has no capability of its own, and sometimes the residue is the treatable part · **open — SECOND FORCING RECORD ARRIVED 2026-08-26 (`cerebral-palsy`), AND IT IS THE EXTREME CASE; BUILD IT (see #208)**
*Forced by:* `lymphatic-filariasis`, six records after `residue` was added.

Every residue in the register so far has been damage nothing can touch: scarred
lungs, established cirrhosis, a blind eye, dead conduction tissue, neurological
deficit. So the field was built as a *description of harm* — severity,
permanence, incidence, a witness — with no room for what can be done about it.

Lymphatic filariasis breaks that completely:

| the residue | how many | what fixes it |
|---|---|---|
| hydrocele | ~25 million men | **a cheap day-case operation. It cures them.** |
| lymphoedema / elephantiasis | ~15–17 million | washing the limb with soap and water — prevents progression and the acute attacks that drive it |

**Neither involves the antiparasitic drug.** Killing worms in someone who already
has elephantiasis achieves nothing. So the single largest actionable intervention
in this record is aimed at the *residue*, and the field that records the residue
cannot say so.

`strata` gets partway, as it did for VL's geography, and the stopping point is
again instructive. The record derives ⧉ because the hydrocele stratum rates
`curative` against the rest — which is honest and is why the strata were used.
What strata cannot carry is that **the curable stratum is cured by surgery for a
sequela rather than by treating the disease**, so a reader sees `curative` and
will assume a drug.

The shape this wants is `residue` mirroring the axes it sits beside — its own
`intervention`, `efficacy`, `access` — which is a bigger change than a field and
should wait for a second forcing record. Watch for one: post-TB lung disease has
pulmonary rehabilitation, and cured-hepatitis-C cirrhosis has surveillance and
transplantation. Neither is as stark as a $50 operation that cures 25 million
men, which is why this is the record that forced it.

## 61. The infected and the diseased are different people · **open**
*Forced by:* `lymphatic-filariasis`.

About **51 million people are infected**, most of them without symptoms. About
**36 million have chronic morbidity**, most of them no longer infected — chronic
disease develops years after infection and persists long after the worms are
gone.

`reach = efficacy × access` describes treating the first group. **Mass drug
administration reaching every one of the 51 million would do nothing whatever for
the 36 million.** Every derived figure on this record — capability 0.72 reach,
`mostly` delivered — is a statement about a population that is not the population
with the disease.

The register has no way to hold two denominators for one entity. TB's version was
*ambiguity* between two well-measured numbers (gap #33's fifth mode) and could be
resolved by choosing one. This is not ambiguity: **both populations are real,
both need something, and the somethings are different.**

The consequence is a word doing damage. Around twenty countries have been
validated as having **eliminated lymphatic filariasis as a public health
problem**, which means transmission has stopped — with tens of millions of
disabled people still living in them. A programme can be validated as having
eliminated this disease with every one of those people exactly as they were.

This is the achievement-side twin of #57. HAT's problem is that a win can be
*lost*. This one is that a win can be **declared over a population it never
reached**, and the register will report the verdict without the qualifier. The
fix is probably the same fix as #60 — the residue needs its own axes, including
its own reach — because the 36 million are precisely the people the residue field
is describing.

## 62. `standing` exists only on blockers — a disputed RATING cannot be recorded · **open**
*Forced by:* `soil-transmitted-helminths`.

The blocker axis carries `standing`: `documented` · `alleged` · `disputed` ·
`refuted`. It was built to stop the register echoing the claim that things are
solvable but nobody will allow it, and it has done that job well.

**Nothing else in the schema has it.** Every axis rating, every severity, every
efficacy figure is asserted flat, and the register's whole ethos — derive never
store, witness not boolean, a claim you can argue with — has no way to say *this
number is genuinely in dispute among people who have looked*.

Soil-transmitted helminthiasis is where that bites. The contested thing is not
the entity — nobody doubts hookworm causes anaemia — it is **whether mass
deworming produces measurable benefit**, with systematic reviews finding little
or no average effect on weight, haemoglobin, cognition or school attendance,
against long-run trial follow-ups and a substantial funder community reaching the
opposite conclusion. That argument has stayed open through decades and many
hundreds of millions of doses.

So the most consequential number in the file is `efficacy`, and it is the one
number that most needs a standing and cannot have one. Note the two knock-ons:

- **`contested: true` does not fit either.** It is defined as the entity's
  existence or definition being disputed, so this record rates `false` —
  correctly, and uselessly. `contested` is entity-scoped; the dispute here is
  intervention-scoped. That is a **sixth** distinct meaning the axis is being
  asked to carry (see #6), and the first that it correctly refuses.
- **The prose is doing a field's job.** The `residue` witness on this record
  spends a paragraph explaining that rating it `major` would smuggle in one side
  of the argument and omitting it would smuggle in the other. That paragraph is
  a `standing: disputed` written out longhand.

The fix is small and general: allow `standing` on any rated value, defaulting to
`documented`. The reason to wait is that it would be easy to over-apply — half
the register is `src: recall` and *unverified* is not the same as *disputed*, and
collapsing those would destroy the distinction gap #33 spent four modes building.

## 63. `efficacy` conflates what the drug does with whether it helps · **open**
*Forced by:* `soil-transmitted-helminths`.

`efficacy` is defined as the fraction of patients whose disease course is altered
by the best available treatment. For almost every record that is one question,
because killing the pathogen and helping the patient are the same event.

Here they have come apart, publicly, at the scale of hundreds of millions of
children:

| question | answer |
|---|---|
| does albendazole clear the worms? | **yes** — ~95% for *Ascaris*, less for hookworm, ~30% for *Trichuris* |
| does clearing the worms help the child? | **genuinely disputed** |

The record rates `efficacy: 0.70` — parasitological, blended across species, with
the units shouting that this is what the drug does to the worm. A reader will
take it for the second question. And `reach = efficacy × access` then produces
`curable, partly delivered`, which reads as an ordinary delivery problem in a file
whose central fact is an evidence problem.

This is the mirror of MCAS (gap #41), and the pair defines the axis's failure
range. There, response to treatment is built into the diagnostic criteria, so
`efficacy` is ~1.0 *by construction* and means nothing. Here, `efficacy` measures
a real and measurable thing that is **not the thing anyone cares about**. Both
break the same field, from opposite ends.

The likely shape is two fields — parasitological or biomarker response against
patient-relevant outcome — which is the distinction clinical trials have made for
decades between surrogate and clinical endpoints. **The register has been using a
surrogate endpoint without saying so**, and mostly getting away with it because
for most diseases the surrogate is the outcome.

Note this also gives the mechanism axis a reading. This record rates `mechanism:
partial` while the four neighbouring parasitic records rate `established` — not
because the parasitology is weaker, but because the chain from *light and
moderate* infection to the stunting and cognitive deficit attributed to it is the
named hole. **A negative trial is evidence about mechanism**, and the register
had not previously had to notice that.

## 64. `strata` presume the partition is observable · **open**
*Forced by:* `mycetoma`.

Every strata set in the register so far can be assigned at the bedside or by a
routine test. Breast cancer stage: imaging and biopsy. Chagas phase: an ECG.
Tuberculosis resistance: a molecular test that returns in hours. Lymphatic
filariasis: you can see the hydrocele.

**Mycetoma's cannot.** It is caused either by fungi (eumycetoma) or by
filamentous bacteria (actinomycetoma), the two are clinically near-identical —
painless subcutaneous swelling, sinus tracts, grains — and the treatments have
nothing in common:

| | actinomycetoma | eumycetoma |
|---|---|---|
| treatment | combination antibiotics | azoles for 12+ months |
| efficacy | **~0.90** | **~0.35** medical cure |
| toll | minor | **catastrophic — amputation is common** |

Telling them apart needs grain microscopy, culture over weeks, histopathology or
PCR, none of which exists in rural Sudan, Chad or Senegal. Grain colour helps and
is not reliable.

So the record carries a perfectly valid `strata` block describing two groups **a
clinician in front of the patient often cannot sort them into.** The schema
treats that identically to breast cancer's stages. It should not: a stratum you
can assign is a clinical category and a stratum you cannot is a *research*
category, and the difference is the whole disease here.

Note what this does to the measurement axes. `diagnostic` asks whether the
disease can be shown to be present — and it can, unmistakably. The question that
decides the patient's life is *which* mycetoma, and the schema has nowhere to put
it, so it falls onto `predictive: none` and reads as an ordinary
which-drug-works gap rather than as two diseases wearing one name.

Candidate fix: strata carry an `assignable` flag, or the `diagnostic` axis gains
a second question — *can you tell which one*. The second is probably right and
would also serve POTS, whose four mechanisms are similarly unresolvable at the
bedside (#39). Two records; wait for a third.

## 65. The register inherits somebody else's attention · **open, and it is about the method rather than the schema**
*Forced by:* `mycetoma`.

Mycetoma was described in the medical literature in the **1840s**. It was added
to the WHO neglected tropical disease list in **2016**. Its first double-blind
randomised controlled trial ran in the **2020s**. There is still no reliable
global burden estimate.

Read the blockers on that record and they look like four separate problems — no
burden data, thin evidence, a bad antifungal, no field diagnostic. **They have
one upstream cause: for 174 years nobody was looking**, and there is no field in
this schema that records it, because it is not a property of the disease.

That matters beyond this record, because of how the register is built.
`README.md` says disease identifiers are borrowed, never minted — Nordstern
points at Mondo, which merges DOID, OMIM, Orphanet, NCIt and ICD. Every one of
those was assembled by people who studied things. So:

> **Every record in this register exists because somebody already decided it was
> a disease worth naming.** The register's stated purpose is to say what is left,
> and it can only say what is left *among things already recognised*.

Mycetoma is the proof, because it is a disease that was fully describable in 1842
and invisible to the system until nine years ago. It is now in Mondo
(`MONDO:0016823`) and would have been picked up by any modern enumeration — which
is exactly the point: **it entered the enumeration because a research centre in
Khartoum spent decades campaigning for it to.** Recognition preceded the data,
not the other way round.

There is no clean fix and it should not be pretended otherwise. Three partial
responses worth holding:

- **Record the recognition date** where it is late and consequential, so a reader
  can see that the absence of evidence is downstream of the absence of attention
  rather than of difficulty. Cheap, and honest.
- **Treat "what is missing from the enumeration" as its own question**, separate
  from "what is unsolved in it". They have different answers and the register
  currently conflates them by construction.
- **Do not let the corpus drift toward the well-studied**, which is the natural
  direction of travel when records are added by whatever comes to mind. The seed
  set was chosen for structural diversity; a burden-weighted or attention-weighted
  sample would have missed this record entirely, and it has now produced two gaps.

## 66. `prevention` is one word doing five jobs, and `capability` ignores it · **HALF CLOSED 2026-08-24 — see the note at the end of this entry**
*Forced by:* `dengue`. Subsumes and promotes #49.

**Dengue derives `capability: unsolved`, quadrant `engineering problem` — the
same cell as Huntington's disease.**

That is what the rules say and the rules are wrong here. `capability()` reads the
intervention ladder and ignores prevention unless prevention is `eradicated`.
Dengue has no antiviral, so `intervention: symptomatic`, so `unsolved`. It also
has two licensed vaccines and a vector intervention that cut incidence by around
77% in a cluster-randomised trial. All of that lives on `prevention`, which is a
single enum word.

**And two functions in `check.py` now disagree about the same concept:**

```
capability(dengue)      -> "unsolved"
has_capability(dengue)  -> True        # because prevention == "prophylaxis"
```

`has_capability()` was widened to count prevention so that rheumatic heart
disease's penicillin would not be dropped from the no-champion list.
`capability()` never was. The register therefore says *capability: unsolved* and
*has capability: yes* about the same record, and dengue is the first entity where
the two come apart. That is a bug, not a philosophical difficulty, and it should
be fixed before the burden metric (#48) is built on top of either.

Beyond the contradiction, the axis is being asked to carry five things and
answers one:

| question | dengue's answer | where it is recorded |
|---|---|---|
| does prevention exist? | yes | `prevention: prophylaxis` ✓ |
| how well does it work? | varies by serotype | nowhere (#49) |
| how many does it reach? | small | nowhere |
| **does it harm anyone?** | **yes — see below** | **nowhere** |
| does it stay done once done? | Wolbachia: yes. Vaccine: no. | nowhere |

**The harm question is not hypothetical.** The first dengue vaccine increased the
risk of severe dengue in recipients who had never been infected — a vaccine that
primes like a first infection makes the next natural infection behave like a
second one, which is the dangerous one. `toll` cannot hold it: `toll` is what the
*cure* takes from the patient, and this is a preventive intervention harming the
people it was given to protect.

**And the persistence question is new.** Releasing Wolbachia-carrying *Aedes*
establishes the bacterium in the wild mosquito population and it stays there — a
one-off, self-sustaining modification of the vector, closer in shape to building
a sewer than to spraying. The enum has `prophylaxis` (given to a person) and
`risk-reduction` (an ongoing activity) and nothing for a preventive act that
persists after you stop paying for it. Note this is the inverse of #58's
duration problem: onchocerciasis must be sustained for fifteen years before it
works; this works once and keeps working.

The shape wanted is `prevention` mirroring the treatment axes — a rung, an
efficacy, an access, a harm, and a persistence — and `capability` reading both.
#49 proposed the first two and rated it cheap and non-urgent. It is now urgent.

### Fixed — `capability` now reads the prevention axis, 2026-08-24

**Measles ended it**, four records after dengue raised it. A two-dose vaccine,
~97% effective, in use since 1963, off patent, which eliminated the disease from
the entire American continent and took deaths from ~2.6 million a year to
~100,000 — filed `unsolved`, in `engineering problem`, *understood and nothing
can be done*.

`capability()` gained a fourth value, **`preventable`**, rather than being
promoted into an existing one, because none of the others was true. **Nobody is
cured of measles. Nobody is managed.** *"Don't get it, because if you do we
cannot help you much"* is a distinct answer, and it is the honest one for three
records: measles, rabies (essentially 100% fatal once symptomatic, essentially
100% preventable) and dengue.

| record | was | is |
|---|---|---|
| measles | `unsolved` · engineering problem | **`preventable`** · known & treatable |
| rabies | `unsolved` · engineering problem | **`preventable`** · known & treatable |
| dengue | `unsolved` · engineering problem | **`preventable`** · known & treatable |
| rheumatic-heart-disease | `partial` · known & modifiable | **unchanged** |
| h5n1 | `partial` · known & modifiable | **unchanged** |

Four decisions, each of which was a real choice:

- **Prevention rescues only what would otherwise read *nothing can be done*.**
  The first attempt promoted any record with prophylaxis to the `treatable` tier
  and immediately moved rheumatic heart disease out of `known & modifiable` —
  hiding its disease-modifying treatment behind its penicillin prophylaxis. A
  test caught it. Where the map already says something works, there is nothing to
  rescue.
- **`risk-reduction` does not count.** Smoking cessation and diet are real and
  they do not make a disease preventable in the sense that a vaccine does.
- **`delivery` is withheld for a preventable record, not guessed.** `reach` is
  `efficacy × access` and **both scalars describe the treatment**, so for measles
  the number describes the wrong thing entirely. `—` rather than a misleading
  band. This is #109, below.
- **`harm_without_benefit` was re-scoped to read the intervention axis
  directly.** That section means *a permanent toll while the course is
  unchanged*, which is a claim about treatment; once `capability` also answered
  for prevention it would have silently stopped firing on preventable records
  whose treatment still maims.

**Still open, and it is the half the gap's title names:** `prevention` remains
one word doing five jobs. `prophylaxis` covers a vaccine given once, a monthly
injection for years, post-exposure prophylaxis inside a 72-hour window, and a
bed net. Those differ in cost, in toll, in who administers them and in whether
they need to be sustained, and the enum flattens all of it.

## 67. The externality can be trust, and it lands on a different disease · **open**
*Forced by:* `dengue`.

After the seronegative finding, the Philippine dengue vaccination programme —
several hundred thousand children — was suspended amid criminal investigations
and sustained public alarm. Survey data recorded a collapse in public confidence
in **vaccines generally**, not in dengue vaccines. Coverage of other childhood
immunisations fell. A large measles outbreak followed in 2019.

So: **an intervention for one disease damaged the control of another, by damaging
the institution both depend on.**

The register has recorded externalities before and all of them were biological —
incomplete TB treatment manufacturing resistant organisms (#50 cost 3), PKDL
patients sustaining leishmaniasis transmission (#51), *Loa loa* making
onchocerciasis treatment lethal (#59). This one is **social**, it travels through
public trust rather than through a pathogen, and it is plausibly the most
consequential edge in the corpus.

Three things follow:

- **It is the sharpest case yet for gap #55.** A table of nodes with no edges
  cannot record that a dengue programme caused measles deaths. And unlike the
  biological edges, this one has no obvious pair of records to connect — the harm
  ran through *every* vaccine-preventable disease at once.
- **It cuts against the register's own instincts.** Every triage view here asks
  where a marginal intervention would do the most good. None can ask **what a
  failed intervention would cost beyond its own disease**, and that cost is
  sometimes larger than the benefit sought.
- **The evidence is asymmetric and should be stated as such.** The confidence
  collapse is documented in survey data and the coverage fall and the outbreak
  followed; the causal attribution is strongly argued and remains an inference.
  Recorded in the record's `holes` rather than asserted.

There is no field to propose yet. The honest version is that this is what a
`standing`-carrying claim about an inter-entity relationship would look like, and
the register has neither the relations (#55) nor the standing on ratings (#62)
that would be needed to hold it.

## 68. The ladder has no rung for correctly doing nothing · **open**
*Forced by:* `echinococcosis`.

Hydatid cysts are staged by ultrasound on the WHO-IWGE scale. CE1 and CE3a are
active and get punctured or operated on or given albendazole. **CE4 and CE5 are
degenerated and inactive, and the correct management is to leave them alone** —
operating takes the whole surgical toll and delivers nothing.

The intervention ladder cannot express that. Its bottom rung, `none`, means
*nothing alters the course* — a statement of **incapacity**, which is what
Huntington's and ME/CFS have. Deciding not to treat a CE4 cyst is the opposite:
it requires knowing the natural history, staging the lesion, and acting on the
knowledge that intervening would harm. **That is capability, and the register has
one word that means its absence.**

Two things follow, and the second is the more useful.

**The ladder is monotonic in a way medicine is not.** Every rung from `none` to
`curative` is more doing. There is no position for *doing less, knowingly* — no
rung for de-escalation, active surveillance, or watchful waiting. The register
has already brushed against this twice without noticing: breast cancer's
overdiagnosis problem is a plea for exactly this rung (a screen-detected cancer
that would never have harmed anyone should be *watched*), and the toll-reduction
gap (#26) is the same instinct applied to treatment intensity rather than to the
decision to treat at all.

**And this is the positive case for measurement the register has been missing.**
Every measurement argument on this page has been about aiming treatment better —
Huntington's has perfect measurement and nothing to aim, POTS has an objective
test that buys nothing, breast cancer cannot say who needed treating. Here
**good prognostic measurement pays by telling you to stop.** A battery-powered
ultrasound in a herding community prevents a laparotomy on a dead cyst. Note that
`overtreatment_risk` correctly stays silent on this record, and the reason is the
achievement: the flag requires `prognostic: none`, and prognosis is precisely
what is good.

Candidate shape: a rung between `none` and `symptomatic` — call it
`surveillance` — meaning *the course is known well enough to decide not to
intervene*. It would immediately want a second record, and breast cancer's
screen-detected stratum is the obvious candidate.

## 69. The intervention can be administered to a different species · **open — FIVE RECORDS, NOT ONE. THE "WATCH FOR THE SECOND" NOTE WAS STALE FROM 2026-08-23; CORRECTED 2026-08-26. BUILD IT.**
*Forced by:* `echinococcosis`.

Humans are an accidental dead end for both echinococcus species. A person with a
hydatid cyst infects nobody. The parasite cycles between **dogs and sheep**, or
foxes and rodents, and everything that controls the disease happens there:

- deworming dogs with praziquantel, at intervals
- keeping raw offal away from dogs — abattoir control and home slaughter practice
- stray dog population control
- **vaccinating sheep**, for which a licensed, effective vaccine exists

Not one of those is given to a human being. So the `prevention` axis — which is
scoped to what protects the patient — rates `risk-reduction` and conveys none of
it, and **a licensed working vaccine sits in this record without counting as
prevention, because it is administered to livestock.**

`who_could` cannot name the actor either. The list runs academic · nonprofit ·
philanthropy · sponsor · regulator · payer · government · legislator ·
health-system · software · patient-org · manufacturer. **There is no veterinary
service and no agriculture ministry**, and those are the people who would end
this disease. The record falls back on `government`, which is true and useless.

This is one step beyond schistosomiasis's and soil-transmitted helminths' problem
(#53, the durable fix is sanitation and lives in a water ministry). There the
intervention was in a different sector; here it is in a **different organism**,
and the register's whole model assumes the thing you do is done to the patient or
their environment.

It is not a curiosity. Iceland eliminated cystic echinococcosis through dog
control and slaughter practice, with no medical intervention at all, and New
Zealand and Tasmania ran successful long programmes. **The demonstrated solution
to this record is entirely veterinary**, and the register can neither rate it nor
name who would deliver it.

---

**AMENDED 2026-08-26 — the waiting is over and had been for three days when this
was found.**

The paragraph that used to close this gap read: *"Watch for the second record
before building anything — rabies is the obvious one and is not in the corpus,
and its answer is also to vaccinate dogs."*

**Rabies was added on 2026-08-23 as record 37, and its own `witness.prevention`
says so explicitly** — *"Echinococcosis raised this (gaps.md #69) and predicted
rabies as the second record. It is."* `taeniasis-cysticercosis` then counted
itself as the **third** — *"sheep for echinococcosis, dogs for rabies, pigs here
— with `who_could` still unable to name a veterinary service."* **The records
kept the count. The gap header did not.** That is `index.md`'s drift failure
happening inside `gaps.md`, where there is no test to catch it.

There are at least five, and one of them is the largest preparedness record in
the corpus:

| record | the species | the intervention |
|---|---|---|
| **echinococcosis** | dogs, sheep | praziquantel for dogs, offal control, **a licensed sheep vaccine** |
| **rabies** | dogs | vaccinate ~70% of the dog population and transmission stops; Latin America did it, western Europe finished it |
| **taeniasis-cysticercosis** | pigs | oxfendazole, confinement, and **a working pig vaccine, TSOL18** |
| **h5n1** | poultry, and now dairy cattle | culling, biosecurity, movement restriction, contested poultry vaccination |
| **visceral-leishmaniasis** | dogs | the zoonotic Mediterranean and Brazilian form has a canine reservoir |
| **hat** (partial) | cattle, wildlife | rhodesiense disease is zoonotic and no human-side effort reaches the reservoir |

**And the gap file has been fragmenting its own observation.** `h5n1` records
that *"the effective prevention is an agricultural programme"* and files it under
**#103** (preparedness) rather than here — which is defensible, and means the
same structural fact has been landing in two gaps depending on which record
noticed it. **Five instances split across two gap numbers is how a shape stays
unbuilt.**

**Three concrete changes, and the first is trivial.**

1. **`ACTORS` gains a veterinary and agriculture actor.** The set is twelve
   values — academic · nonprofit · philanthropy · sponsor · regulator · payer ·
   government · legislator · health-system · software · patient-org ·
   manufacturer — and **five records currently fall back on `government`, which
   is true and useless.** A `veterinary` actor, or a broader `agriculture`, is a
   one-line change to a validated enum and would immediately make five records
   say who would actually end them.
2. **`prevention` needs a scope**, because `risk-reduction` and `prophylaxis`
   both presume the recipient is the patient. A licensed, effective, deployed
   vaccine that ends a human disease currently does not count as prevention in
   this register **because it is injected into a sheep.**
3. **`capability` should be able to read it.** Rabies rates `intervention: none`
   — correct, and once symptomatic it is essentially universally fatal — and is
   rescued to `preventable` only by post-exposure prophylaxis. **The thing that
   has actually eliminated it from whole continents is not on any axis.**

**AND `gaps.md` ALREADY CONTAINED THE CORRECTION.** The `**Strengthened by
`rabies`, not new:**` block, roughly nine thousand four hundred lines below this
gap's header, says: *"#69 (the intervention is administered to another species) —
second record, and it was predicted."* **The file held the claim and its
refutation at the same time, and both were written by the same process.** This
gap was not un-updated for want of the information. It was un-updated because
nothing re-reads a gap when a record answers it.

**And it is not one gap. It is seven.** Counting how many records cite each gap
that carries a "watch for the second" instruction:

| gap | records citing it | still says "watch for the second" |
|---:|---:|---|
| **#39** final common pathway | **8** | updated 2026-08-24, then again 2026-08-26 |
| **#170** early treatment pulls the definition back | **5** | **yes — and Parkinson's, the named candidate, is held** |
| **#52** solved here, not there | **5** | **yes** |
| **#60** residue with capability of its own | **5** | updated 2026-08-26 |
| **#69** a different species | **4** | **this one** |
| **#45** test of cure | **3** | **yes — and both named candidates are held** |
| **#201** a population disputes the category | 2 | **no — and the count is a false positive**, see below |
| **#42** two live definitions | 1 | correctly still waiting |

**Seven of the eight had their forcing record and none of the headers knew.**
The three fixed on 2026-08-26 were fixed because a record happened to be written
that day; the rest were found by counting, which nobody had done in ninety-nine
records.

**The `#201` row is the reason a count is a trigger and not a verdict.**
`osteoarthritis` cites #201 to say it is *not* that case — a citation by
contrast, which a regex cannot tell from an instance. A check here must report a
gap worth re-reading, never a gap that has been answered. Same rule as everywhere
else in this project: **a bad value is a witness, never a conclusion.**

**The structural point is about the toolchain and it is uncomfortable.**
`check.py` validates every record; `test_check.py` guards `index.md` against
exactly this kind of drift, and was added because `index.md` drifted. **`gaps.md`
is the one artefact in the register that every record cites, that carries all of
its deferred design decisions, and that nothing verifies at all** — and it is the
file the project's own working rule depends on, since *corpus before schema* only
works if somebody re-reads the gap when the corpus answers it.

The check is cheap and the same shape as the quadrant test: parse gap numbers out
of `entities/*.yaml`, and flag any gap whose body defers a decision pending a
second record while two or more records cite it. **It would have fired on
2026-08-23**, and it fires on six gaps today.

## 70. An axis rating can be the consequence of another axis's hole · **open**
*Forced by:* `buruli-ulcer`.

Buruli ulcer rates `prevention: none`. That is correct and it means something
completely different from what the same rating means elsewhere.

**Nobody knows how *Mycobacterium ulcerans* is transmitted.** After decades: an
unexplained association with slow-moving water, aquatic insects proposed, possums
and mosquitoes strongly implicated in the Australian focus, and no confirmed
route in West Africa where most of the disease is. So there is no vector to
control, no water source to treat, no reservoir to target, and no behaviour to
change with confidence.

**`prevention: none` here is not a fact about prevention. It is a hole in
`mechanism` showing through a different field.** Every other infectious record in
this register is controlled by attacking its transmission route — the tsetse, the
snail, the blackfly, the sandfly, the dog, the *Aedes*. Each of those prevention
programmes *is* the transmission route turned into a policy. Buruli has no route,
so it has no programme, and the axis reports the same word it would report for a
disease where prevention had been tried and had failed.

The axes are designed as independent ratings and several of them are causally
chained. Now that it is named, it is visible everywhere:

| record | the rating | is a consequence of |
|---|---|---|
| Buruli ulcer | `prevention: none` | transmission route unknown |
| dengue | no vaccine that is safe in everyone | no correlate of protection |
| tuberculosis | one vaccine in a century | no correlate of protection |
| soil-transmitted helminths | `efficacy` disputed | the mechanism hole — does light infection cause the harm? |
| Chagas | cannot run the trial that matters | no test of cure |

A reader sees five independent ratings; there are three underlying holes. And it
matters for triage, which is the register's purpose: **money aimed at the
downstream rating is wasted, and the register points at the downstream rating.**
Funding "prevention research" for Buruli ulcer means funding a transmission
study, and nothing on the record says so except prose.

Cheapest fix: let a `holes` entry name the axis it gates. That is a small change
and it would let the register answer *what one answer would move the most
fields*, which is a question it currently cannot form.

## 71. `window` records that people are late, never why · **open**
*Forced by:* `buruli-ulcer`, and evidenced by six records already written.

`window` carries `what`, `closes_on` and `caught_in_time` — a fraction. It has
nowhere to say **why** the people outside that fraction were late, and across
this corpus the reasons are entirely different and want entirely different levers:

| record | why people are late | the lever |
|---|---|---|
| **Buruli ulcer** | **the pathogen anaesthetises the lesion** | teach a community to act on something that does not hurt |
| Chagas | no symptoms for two decades | serological screening of at-risk adults |
| mycetoma | painless, rural, days from a clinic | a field test, and a reason to travel |
| hEDS | clinicians do not believe the patient | clinician education |
| breast cancer | screening finds too much, not too little | a prognostic marker |
| dengue | the window is hours and the patient is already in the clinic | triage training and a bed |

Buruli is what forced it because its answer is not a health-system failure at
all. **Mycolactone is analgesic** — the toxin that destroys the tissue also
removes the pain that would send someone to a clinic. Late presentation is a
virulence strategy. So the usual awareness message, *come when it hurts*, is
exactly the wrong instruction, and the intervention has to teach people to act on
a painless nodule.

The register's most repeated claim is that `diagnosis` is its cheapest lever.
Six records now show that **which** diagnosis lever depends entirely on why
people are late, and the field records only that they were.

## 72. The register can record that a disease WAS eradicated, never whether one COULD be · **open**
*Forced by:* `yaws`.

`prevention: eradicated` is a **state**. It says a thing has happened. Nothing in
the schema says whether it *could* happen — and eradicability is the single most
useful input to "what should we work on next" that this register does not carry.

It is also not a matter of effort. It is a property of the pathogen's natural
history, and the corpus already contains the whole checklist scattered across a
dozen records in prose:

| requirement | who has it |
|---|---|
| no non-human reservoir | yaws ✓ · HAT-*gambiense* ✓ · HAT-*rhodesiense* ✗ · echinococcosis ✗ · dengue ✗ |
| an intervention that interrupts transmission | yaws ✓ (one oral dose) · dengue partial · Buruli **unknown — no route** |
| a way to find every infection, including silent ones | **yaws ✗ — latency** · TB ✗ (2bn latent) · Chagas ✗ |
| lasting immunity after infection or vaccination | smallpox ✓ · yaws ✗ · dengue ✗ (worse than ✗ — see ADE) |

**Yaws is the record that forces it because it scores so well and still failed.**
No animal reservoir. A single cheap oral dose that cures in 95%. Fifty million
people treated in twelve years and prevalence cut by ninety-five percent. And it
came back, because of the one box it does not tick: **latent asymptomatic
infection**, invisible to any clinical survey, relapsing years later and
transmitting when it does.

That is why the current strategy treats whole communities rather than the people
who look ill — mass treatment is the workaround for a diagnostic that does not
exist. And it is why gap #57's missing control case matters: **smallpox is
eradicable and yaws is not, and the difference is latency and lasting immunity,
not commitment.** A register that cannot say which is which will keep filing
"nearly eradicated" as an achievement rather than as a warning.

Candidate shape: a small structured `eradicability` block — reservoir, silent
infection, immunity, interruption — derived where possible from fields the
records already carry. Cheap, and it would let the register answer a question it
currently cannot form: *of the things that are curable and cheap, which ones can
actually be finished?*

## 73. The register has no memory of prior attempts · **open**
*Forced by:* `yaws`.

Read the yaws row: curable, one oral dose, ninety-five percent efficacy, eighty
thousand reported cases, cheapest blocker $50M, ⚑ no champion. It reads as an
unusually attractive untried opportunity.

**It has been attempted three times.** 1952–64 (near-success, then abandoned).
The 1980s (did not hold). 2012 onward (target slipped from 2020 to 2030). Any
funder looking at that row should know that before anything else, and the
register has nowhere to put it.

`moved:` records that a *rating* changed. It does not record that **a programme
was run and stopped**, which is a different kind of fact and often the more
important one. The distinction matters because the two imply opposite readings of
the same row:

- *nobody has tried this* → the blockers are the obstacle, fund them
- *this has been nearly won twice and lost twice* → **the blockers are not the
  obstacle**, and the thing to understand is why it was stopped

For yaws the answer is documented and administrative: in 1964 the vertical
campaign, having cut prevalence by ninety-five percent, was folded into general
primary health care and dedicated surveillance ended. No war, no funding
collapse, no resistance, no new science. **The programme was stopped because it
had nearly succeeded.**

Sleeping sickness has the same history and the same shape. Two records now, and
in both the most decision-relevant fact about the entity is its own programme
history — which the register treats as background.

Minimum viable version is a `attempts:` list alongside `moved:` — dates, what was
done, what happened, why it stopped. It is prose the records already contain;
what is missing is somewhere structured to put it so a query can find it.

## 74. `also` is doing two jobs, and Mondo's scope vocabulary proves it · **open**
*Forced by:* `mondo_sync.py`, on its first run.

`SCHEMA.md` defines `also` as *"synonyms people actually search for"* — a search
alias list. `resolve_mondo.py` searches on it to find candidate identifiers.
Those are different jobs, and #43 recorded the near-miss they produced (`duodenal
ulcer` in `h-pylori-ulcer`'s `also`, exactly matching a Mondo label, and the
wrong entity).

**Mondo scopes every synonym it carries** — `hasExactSynonym`,
`hasRelatedSynonym`, `hasBroadSynonym`, `hasNarrowSynonym` — and only the first
is an equivalence. So the conflict is now measurable rather than anecdotal, and
the first run found one:

> **lymphatic-filariasis** — `also: elephantiasis` — Mondo scopes this
> **hasBroadSynonym**. Elephantiasis includes podoconiosis and other causes of
> lymphatic obstruction; filarial elephantiasis is a subset of it.

I added that synonym by hand, two records ago, to make the identifier resolve
reproducibly. **The tool caught my own error on its first pass**, which is the
best evidence for it that could have been produced.

Left in the record deliberately rather than deleted, because people *do* search
"elephantiasis" for this disease and the field says that is what it is for. The
honest resolution is that `also` should be split — `searches_as` for retrieval,
`same_as` for equivalence — with only the second ever used to propose an
identifier. Until then `mondo_sync.py` audits the difference on every run, which
is most of the benefit at none of the migration cost.

## 75. The register borrowed one identifier and did not notice it came with twenty · **applied in part**
*Forced by:* `mondo_sync.py`.

*"Disease identifiers are borrowed, never minted"* was adopted so the register
would not maintain a parallel namespace. What went unremarked is that **Mondo is
not just an identifier, it is a junction.** Every resolved term carries
cross-references, and across the thirty resolved records:

| source | records | what it unlocks |
|---|---|---|
| `MEDGEN` · `UMLS` | 28/30 | concept hubs into OMIM, GTR, literature |
| `MESH` | 27/30 | literature search |
| `SCTID` (SNOMED) | 26/30 | clinical coding |
| `ICD10CM` | 16/30 | **burden — the route into GBD cause mappings** |
| `icd11.foundation` | 15/30 | current WHO classification |
| **`Orphanet`** | **17/30** | **rare disease prevalence, as published classes** |
| `OMIM` | 7/30 | gene and variant level |

The scalar-sourcing plan (see the memory note and README) assumed the next step
after MONDO was building retrieval against GBD and Orphanet. **Half that work was
already done and sitting inside the identifier we had already resolved.**

**It has already corrected a record.** `msmds` carried
`prevalence: {src: unknown}` with a note reading *"no registry publishes a
denominator"*. Its Mondo term cross-references **Orphanet:404463** and
**OMIM:613834**, and Orphanet publishes prevalence *classes*. So the claim was
too strong: there is very likely a published prevalence class that nobody here
had looked up. The record now says so, and the correction is dated and
attributed to the tool.

That is a small thing that matters for the method: **the register's own
uncertainty markers can be wrong in the optimistic direction as well as the
pessimistic one.** `src: unknown` asserts that nobody knows, which is a claim
about the world and needs checking like any other.

Not fully applied because the xrefs are *reported*, not imported. They live in
the generated `mondo-terms.json` snapshot rather than in the records, which is
the right side of borrow-don't-copy — the record holds one key and the snapshot
holds what it opens.

## 76. A metric can be satisfied by moving its denominator · **open, and it is a warning about #48**
*Forced by:* `leprosy`.

WHO's target was **"elimination of leprosy as a public health problem"**, defined
as fewer than **one registered case per 10,000 population**. A registered case is
somebody *currently on treatment*.

Multidrug therapy shortened treatment from years of dapsone to six or twelve
months. **So the number of people registered at any instant fell mechanically,
because the treatment got shorter.** The target was declared met globally in
2000. New case detection has sat at roughly 200,000 a year ever since —
essentially flat for two decades.

Nothing about the organism changed. The metric was satisfied by a change in
treatment protocol, and what followed was the yaws pattern with better
documentation: vertical programmes wound into general health services, and the
clinical expertise needed to diagnose a disease with **no laboratory test** went
with them.

**This register is about to build a headline burden metric.** Gap #48 argues for
*unreached burden* — deaths or DALYs × (1 − reach) — and argues it should be
built before the crowd-contribution work because the register currently answers
"what next" wrongly. Leprosy is the reason to build it carefully:

- **`reach = efficacy × access` has the same vulnerability.** Redefine who counts
  as a patient and reach moves without anything improving. Narrow a case
  definition and access rises. Every denominator here is a modelling choice.
- **The register's own numbers are already exposed to this.** `access` is
  "fraction of patients diagnosed and treated" — over a denominator of estimated
  cases, which is itself a model. Tighten the estimate and access improves.
- **A published metric gets optimised.** That is not cynicism, it is what
  happened: a reasonable target, honestly set, was reached by an honest
  improvement in treatment, and the consequence was that a still-transmitting
  disease was declared finished.

The concrete ask is small and should be done at the same time as #48: **every
derived metric states what would move it that is not progress.** For
`unreached burden` that is at least three things — narrowing the case definition,
improving the burden estimate, and shortening treatment. Write them next to the
number.

Note the interaction with #57 and #73. Yaws was stopped after a *real* success it
could not hold. Leprosy was stopped after a **definitional** one. The register
cannot tell those apart, and they call for opposite responses.

## 77. Stigma is a first-order property of some diseases, and there is no field for it · **open**
*Forced by:* `leprosy`.

Leprosy's disability is caused by a loop the schema cannot draw:

> **stigma** → people conceal a painless numb patch → **late presentation** →
> **irreversible nerve damage** → visible deformity → **more stigma**

Every field in this register is a static property of an entity. `ongoing` is the
burden of *being treated*. `toll` is what the *cure* takes. `blockers` name what
stands in the way *now*. None of them can hold a self-reinforcing cycle in which
the disease's outcome is its own cause.

And it is not soft. Three concrete things sit inside that loop:

- **Clofazimine darkens the skin.** The drug that cures leprosy visibly marks the
  patient as someone being treated for it, in communities where that affects
  marriage, employment and housing. **A toll that interacts with stigma** is a
  documented reason for treatment default, and `toll: minor` cannot say it.
- **Discriminatory law.** Provisions permitting divorce on grounds of leprosy,
  barring public office, and authorising segregation persisted in national law
  long after the disease was curable and free to treat; some were repealed only
  in the last decade. That is a `policy` blocker in the register and a cause of
  the late presentation in the `window`, and it is filed as one thing.
- **The register cannot distinguish stigma-driven delay from distance-driven
  delay**, which is gap #71 again (`window` records that people are late, never
  why) — and here the "why" is the disease's own reputation.

Do not add a `stigma:` severity field. It would be a number standing in for a
mechanism. The more useful shape is the one #70 already proposes — letting a hole
or a blocker name the axis it gates — extended so a blocker can name a field it
*feeds back into*. Leprosy is the first record where the loop is undeniable;
mental illness records (bipolar, depression) and hEDS have weaker versions of it
already.

## 78. Externalities run both ways, and the register has a sign error · **open**
*Forced by:* `trachoma`.

Every externality the register has recorded is a **harm**. Incomplete TB
treatment manufacturing resistant organisms (#50 cost 3). PKDL patients
sustaining leishmaniasis transmission (#51). *Loa loa* making ivermectin lethal
(#59). A dengue vaccine collapsing confidence in all vaccines (#67).

Trachoma's is a **benefit, and it may be larger than the primary effect.**

Mass azithromycin distribution for trachoma was tested against child mortality in
the **MORDOR** trial and reduced **all-cause deaths in children by around a
seventh**, far more in the highest-mortality settings. That has nothing to do
with trachoma, with eyes, or with *Chlamydia*. It is plausibly the largest single
benefit the programme produces, and it is invisible to a record filed under an
eye disease — which reports `deaths: 0.0`.

And the same act carries a **paired off-target cost**: mass macrolide
administration selects for resistance in organisms that were never the target.
So one intervention has a large unmeasured benefit and a real unmeasured harm,
both landing on entities other than the one being treated.

Three consequences:

- **Cost 3 is misnamed.** It is not "what treatment failure costs third parties";
  it is **the effect of an intervention on people other than the treated
  patient**, and it has a sign. Trachoma is the record that makes that obvious.
- **The justification for a programme can sit outside its own record.** If MORDOR
  is right, a substantial part of the case for trachoma MDA is child survival —
  and any burden-weighted ranking (#48) computed per-entity will miss it entirely
  and rank the programme on blindness alone.
- **The two effects are not separable in practice.** You cannot take the child
  mortality benefit without the resistance cost; they are the same tablets. A
  register that could hold one and not the other would be worse than one that
  holds neither.

Do not build a signed-externality field before #55 (the register is a table of
nodes with no edges). This is more evidence that the relation model is the
missing piece, not another column.

## 79. `orphaned` asserts something the rule does not test · **open, and it is the `solved` mistake again**
*Forced by:* `trachoma`, which trips it and should not.

The flag is called **⚑ no champion**, and `README.md` glosses it as *"the science
is done and nobody is carrying it."* What the rule actually computes is:

```
capability is real  AND  reach < 0.6  AND  ≥1 documented non-knowledge blocker
```

**Nothing in that tests whether anyone is carrying it.**

Trachoma derives reach 0.5525 and trips the flag. It also has one of the
best-resourced programmes in global health: a dedicated international coalition,
a manufacturer donation running to hundreds of millions of doses a year, an
official four-part WHO strategy, and **more than twenty countries validated as
having eliminated it**. Its "at risk" population has fallen from roughly 1.5
billion to around 120 million — the steepest decline in this register.

It is heavily championed and still under 0.6, because the remaining problem is
genuinely large and hard, not because nobody cares.

This is structurally the same defect Jeremy caught on `quadrant: solved` early
on: **a derived cell whose name makes a claim the derivation does not support**,
sitting on a public page where a reader will take the name at face value. The fix
then was to rename the cell to what it actually computes. The same fix applies:

- The rule computes **"real capability, a delivery gap, and a lever that is not
  knowledge."** That is a useful thing to compute. Call it that — something like
  **`delivery gap`** — and stop implying an absent actor.
- If "is anybody working on this" is wanted, it needs a field. It is not
  derivable from reach, and the register has no data on funding, programmes or
  institutional attention at all.
- Note the collision with #48: the flagship *"where would $10M go furthest"*
  question is built on `orphaned`, so it is currently answering **"where is the
  delivery gap"** while claiming to answer **"where is nobody looking."** Those
  differ most exactly where the well-run programmes are.

## 80. The decisive question is sometimes not about the patient · **open**
*Forced by:* `rabies`.

The measurement block asks three questions about a patient's disease: *is it
there*, *what will it do*, *will this treatment work*. Rabies answers all three
and the answers are useless.

- `diagnostic: clinical` — the syndrome is unmistakable, and confirmation is by
  immunofluorescence on brain tissue, which is to say after death.
- `prognostic: good` — untreated symptomatic rabies is fatal within days, in
  essentially every case. **Perfect prognosis, zero capability**, the Huntington's
  lesson compressed from decades into a week.
- `predictive: n/a` — there is no course-altering therapy to predict response to.

**The decision that saves a life was made weeks earlier and is not in any of
those fields.** It is: *was that dog rabid?* — a question about **an animal, in
the past, that has usually run away.**

No test answers it for the person who needs the answer. The animal can be
observed for ten days if it is owned and findable, or killed and its brain
examined. In the settings where rabies kills, it has gone. So prophylaxis is
given on the possibility, to **twenty-nine million people a year**, to prevent
fifty-nine thousand deaths — and the axis that would rate the quality of that
decision does not exist.

Once named, the register has the shape elsewhere and did not notice:

| record | the decisive question | what it is about |
|---|---|---|
| **rabies** | was that dog rabid? | an animal, weeks ago |
| onchocerciasis | does this person carry *Loa loa*? | **a different parasite** (#59) |
| dengue | has this person been infected before? | **a past exposure** |
| lymphatic filariasis | is onchocerciasis co-endemic here? | **a district, not a patient** |

All four decide whether an intervention helps or harms, none is a question about
the patient's own disease, and the `measurement` block cannot express any of
them. #59 named the harm half of this; rabies shows the axis is wrong about
*subject* as well as about *sign*.

## 81. Blockers can be substitutes, and the stopgap eats the cure's budget · **open**
*Forced by:* `rabies`.

The register treats blockers as an independent list with independent prices.
Rabies has two that are **substitutes**, and the cheap one is the answer:

| | post-exposure prophylaxis | dog vaccination |
|---|---|---|
| cost | tens of dollars per course | a dollar or two per dog |
| recipients | ~29 million people a year | the dog population, once, then maintained |
| effect | saves the person in front of you | **removes the exposures entirely** |
| what it buys | one life at a time, forever | an end to the problem |

Latin America cut human rabies deaths by more than 95% and western Europe
eliminated dog-mediated rabies, both by the second route. And **you cannot stop
funding the first in order to pay for the second**, because the first is what
keeps people alive in the meantime. The palliative consumes the budget of the
cure, and it is nobody's error.

Three things the schema cannot say:

- **That two blockers compete for one budget.** Each has a `scale` and they are
  read as additive.
- **That clearing one blocker removes the need for the other's expenditure.** Dog
  vaccination does not merely help; it retires the prophylaxis bill.
- **That the substitution runs across sectors and budgets.** The vaccine is bought
  by agriculture and the deaths prevented appear in health, which is #69's
  problem seen from the finance side.

This is not unique once looked for. Schistosomiasis and soil-transmitted
helminths run mass drug administration indefinitely while sanitation would end
both; trachoma's SAFE names the same trade inside one strategy. What makes rabies
the forcing record is the **price ratio**: elsewhere the stopgap is cheap and the
permanent fix is expensive, and here it is the other way round, which makes the
trap visible.

Do not add a `substitutes:` link before #55. This is a relation between blockers,
and the register still has no relations at all.

## 82. Strata are treated as independent, and sometimes one causes the others · **open**
*Forced by:* `scabies`.

`strata` partition a population and rate each partition separately —
intervention, efficacy, toll. The partitions are assumed to be independent
groups of patients who happen to share a name.

**Crusted scabies is not independent of ordinary scabies. It is where ordinary
scabies comes from.**

Ordinary scabies carries ten or fifteen mites on an entire body. Crusted scabies
— in people whose cell-mediated immunity is impaired — carries millions, in
hyperkeratotic crusts, and often does not itch, so it is missed. Those patients
are **hyperinfectious**: one seeds an outbreak through a care home, a household,
a community.

So roughly two percent of patients drive transmission for the other
ninety-eight, and the schema records them as two rows with different efficacy
figures.

The consequence is a triage answer the register cannot produce: **finding and
treating the crusted stratum is worth more than treating most of the ordinary
one**, and nothing in the record says so. Ordinary scabies rates efficacy 0.85
and crusted rates 0.60, which reads as *the second group is harder to treat* —
true, and beside the point.

This is #55 (a table of nodes with no edges) turned inward. Every previous
instance was a relation between *entities*; this is a relation **between strata
of one entity**, and it is the same missing capability. Two other records already
have weaker versions: visceral leishmaniasis's PKDL patients sustain transmission
for everyone else (#51), and tuberculosis's MDR stratum is *manufactured* by
incomplete treatment of the drug-susceptible one. **Three records, and in all
three the causal stratum is the small one.**

Do not add a `feeds:` link to strata before the relation model exists. This is
more evidence for #55 and not a separate feature.

## 83. An entity can be two diseases, one of which causes the other · **open**
*Forced by:* `taeniasis-cysticercosis`.

*Taenia solium* produces two entirely different human diseases depending on which
life stage you swallow:

- **Taeniasis** — you eat undercooked pork, an adult tapeworm grows in your gut,
  and **you are almost entirely well.** You shed eggs.
- **Cysticercosis** — you swallow those eggs and the larvae encyst in your
  tissues. In the brain: **neurocysticercosis**, the leading preventable cause of
  epilepsy in the world.

**The reservoir is asymptomatic and the victim is somebody else.** A carrier can
give epilepsy to a family member who has never eaten pork — which is why
cysticercosis appears in communities that do not eat pork at all, beside
neighbours who do.

The register has one row per entity and three ways of subdividing one, and none
of them fits:

- **Not `strata`.** Strata partition patients. These are two diseases in
  different people, and a carrier can have both simultaneously by autoinfection,
  so the fractions cannot sum to one because the sets overlap.
- **Not two records.** Splitting them loses the only fact that matters — that one
  causes the other — which is #55 again.
- **Not one record.** Which is what this is, and it means every derived figure
  blends a one-dose cure for a well person with lifelong epilepsy in someone
  else.

**Mondo agrees with the split and not with WHO.** It carries `taeniasis`
(`MONDO:0000367`) and `cysticercosis` (`MONDO:0015484`) as separate terms and has
nothing for the WHO NTD grouping — so this record stays `unresolved`, and for a
**fifth distinct reason** (see #44): *the register's entity is a programme
grouping that the ontology correctly declines to have.* Note it is the exact
mirror of soil-transmitted helminths, where WHO groups four organisms and Mondo
has no term for the group either. **Both times the programme category and the
taxonomy disagree, and both times the register sided with the programme.**

The shape wanted is not a subdivision at all. It is a relation — *entity A's
reservoir population causes entity B* — which is #55, and this is the third
consecutive record to need it.

## 84. `toll` cannot tell drug toxicity from the harm of the treatment working · **open**
*Forced by:* `taeniasis-cysticercosis`, and evidenced by four records.

Albendazole is a safe drug. Giving it for neurocysticercosis can cause seizures,
cerebral oedema, raised intracranial pressure and death — **because the cysts
die.** The dying parasite releases antigen, the immune system responds, and the
response happens inside a rigid skull. Corticosteroids are given alongside to
blunt it, and in heavy or racemose infection the drug is withheld entirely.

**That is not drug toxicity. It is the treatment succeeding.** And `toll`,
defined as *what the cure takes from the patient*, records the two identically.

The distinction matters because **the levers are completely different**:

| | drug toxicity | harm from the treatment working |
|---|---|---|
| reduced by | a better drug, a lower dose | steroids, staging, patient selection, treating *slower* |
| example | dapsone haemolysis, azole hepatotoxicity | the four below |

Four records already carry it and the register reports them as ordinary side
effects:

- **onchocerciasis** — the Mazzotti reaction, from dying microfilariae
- **leprosy** — type 1 and type 2 reactions, during and after multidrug therapy,
  and the principal cause of the disease's permanent nerve damage
- **yaws** — the Jarisch-Herxheimer reaction
- **taeniasis-cysticercosis** — inflammation around dying cysts, in the brain

Note the pattern: it is a parasitic and mycobacterial phenomenon, it is
**proportional to how well the treatment works**, and in leprosy's case it
produces more permanent damage than the infection does. A field that cannot see
it cannot express the most counter-intuitive fact in that record — that the
better the drug works, the more likely the patient is to be harmed.

Cheapest fix is a `toll.kind` — `drug` · `response` · `procedure` — which would
also let the register say something it currently cannot: that a better drug does
not help here, and better *sequencing* does.

## 85. Eradicability is revisable, and the endgame is when you find out · **open, and it amends #72**
*Forced by:* `dracunculiasis`.

Gap #72 proposed an **eradicability** field — reservoir, silent infection,
immunity, interruptibility — so the register could say which curable diseases can
actually be *finished*. Yaws forced it and leprosy confirmed it.

**Dracunculiasis would have scored perfectly on that checklist in 2010, and the
score would have been wrong.**

No animal reservoir. Every link in the cycle interruptible. A cheap intervention.
Cases down from 3.5 million a year in 1986 to double digits. It was the flagship
of the whole idea.

Then, from around 2012, **infected dogs began appearing in Chad** — now in
numbers vastly exceeding human cases, along with cats and baboons. How they are
infected is unsettled: copepods in drinking water, or eating raw fish and
amphibian viscera acting as paratenic hosts, and the interventions differ
completely depending on the answer. The eradication target has slipped from 2009
to 2015 to 2020 to 2030.

So the amendment is not small:

- **The reservoir question is answered by the programme, not before it.** With
  3.5 million human cases a year, a few thousand infected dogs are invisible. At
  fourteen human cases they are the entire problem. **The signal only emerges as
  the noise falls** — which means eradicability is *least* knowable exactly when
  the answer matters most.
- **A stored eradicability score would be authoritative and stale**, and the
  register's founding rule is derive-never-store precisely because a stored
  verdict cannot be argued with. Any such field needs a date and a standing, and
  probably wants to be a *question* — "what would have to be true" — rather than a
  score.
- **It compounds #56.** The endgame already inverts test performance, cost per
  case and political will. Add to that: the biology you thought you understood
  can turn out to have been an artefact of scale.

Not an argument against the field. An argument that it must be built to be
**revised**, and that "eradicable" is a claim with a confidence, not a property
with a value.

## 86. A symptom can be the transmission mechanism · **open**
*Forced by:* `dracunculiasis`.

The female Guinea worm reaches the skin and raises a blister. **The blister
burns** — intensely, unrelentingly — and the sufferer does the only thing that
relieves it: puts the limb in water. Contact with water causes the worm to
discharge hundreds of thousands of larvae. Copepods eat them. The cycle closes.

**The symptom is not a side effect of the parasite's presence. It is the
dispersal strategy.**

And the entire eradication programme — the second-largest reduction in human
disease in history — consists of interrupting that one behaviour: teaching people
with an emerging worm not to enter drinking water, and filtering the copepods
out.

The register records symptoms as burden to the patient. It has no way to record
that a symptom has a *function for the pathogen*, and the distinction is
operational rather than academic: **it tells you where to intervene.** Guinea worm
control is not treating the blister; it is breaking what the blister is for.

Once named, the corpus has both signs of it:

| record | the symptom | what it does for the pathogen |
|---|---|---|
| **dracunculiasis** | a burning blister | drives the host into water — **transmission** |
| **Buruli ulcer** | *no pain at all* — mycolactone is analgesic | removes the signal that would bring the host to a clinic |

Two records, opposite manipulations, and in both the pathogen is shaping host
behaviour rather than merely damaging tissue. Cholera's diarrhoea and
tuberculosis's cough are the same shape and neither record says so.

The cheap version is a flag on the mechanism witness. The useful version is
whatever eventually holds #55's relations, because "this symptom serves
transmission" is a relation between a clinical fact and an epidemiological one.

## 87. The intervention is non-specific, and nothing here can price a share of it · **open**
*Forced by:* `noma`.

Noma is a gangrene of the face caused by ordinary oral bacteria — *Fusobacterium*,
*Prevotella*, organisms already present in every child's mouth. They do nothing at
all until severe malnutrition and an immune insult let them. **The necessary cause
is an absence, not an agent.**

Which means what prevents it is: **feeding children.** Plus measles vaccination,
plus treating malaria and diarrhoea, plus a household not in destitution. Noma
disappeared from Europe with the general nutrition of European children, not
through any medical advance, and nobody was aiming at it.

The register cannot represent this, in two distinct ways.

**Interventions are assumed to map to entities.** Every `blockers.scale` prices
something against the record it treats — a drug, a surgery, a diagnostic, a
delivery programme. Child nutrition prevents noma *and* pneumonia *and* diarrhoeal
death *and* most of what kills under-fives. There is no share of it to charge
here, and charging the whole thing to this record would be absurd. So the record
either understates the intervention or invents an allocation.

**And the disease has no owner because of it.** Noma is a dental problem, a
nutrition problem, a paediatric emergency, a maxillofacial surgery problem and a
poverty problem, and it sat outside every international framework until
**December 2023** — the most recent NTD listing of all, later even than mycetoma.
A disease whose prevention belongs to everybody belongs to nobody.

This is not #53 (the intervention is in another ministry — sanitation for schisto,
STH, trachoma). Those diseases have an agent you can *also* attack with a drug;
the ministry problem is about the cheaper of two routes. Here **there is no
disease-specific prevention to fund at all.**

The inverse of trachoma's MORDOR finding, too: there, an intervention for one
disease turned out to benefit another and the register had no way to credit it
(#63). Here an intervention for *no* disease in particular prevents many, and the
register has no way to charge it. Both are the same missing thing — **benefits
that cross entity boundaries** — and #63 should probably be merged into this.

The cheap version is a blocker flag meaning *non-specific*, so these are not
summed with disease-specific costs. The honest version admits the register's unit
of account is the entity, and some of the best buys in global health are not
denominated in it.

## 88. The register counts what presents, and noma's victims do not · **open**
*Forced by:* `noma`.

Roughly **nine in ten children with noma die** — at home, aged two to six,
recorded as malnutrition or as nothing. The survivors are hidden by their
families, because a face with a hole in it is read as a curse. And until the end
of 2023 there was no framework under which anybody was required to count.

So the incidence figure in this record — ~140,000/year — **dates from 1998, is
derived from survivors, and is widely regarded as a guess.** Everything else in
the record inherits that. The deaths figure compounds it with an uncertain case
fatality, which is why both are `src: unknown` and the record says they should not
be quoted.

The general problem is sharper than "the number is bad" (#33's `unknown` mode
already covers that):

**The undercount scales with the severity of the outcome.** A disease that
disables gets counted at clinics. A disease that kills quickly at home does not.
Noma is the extreme — the register's entire evidentiary base for this record is
the minority who survived *and* were found *and* were brought forward — but the
corpus has the pattern repeatedly: rabies deaths at home, snakebite deaths before
reaching a facility, mycetoma amputations in villages.

**So the register is systematically biased toward diseases whose victims live long
enough to be seen**, and it does not say so anywhere. Every `access` figure, every
`caught_in_time`, every incidence estimate rests on presentation.

And it closes on itself, the third loop in the corpus after leprosy's and scabies'
(#77): **not counted → not costed → not funded → not counted.** Noma's December
2023 listing is the first crack in it, and the first thing that should follow is
a defensible burden estimate — which the record files as its `knowledge` blocker
for exactly that reason.

For #48's burden metric this is load-bearing. Ranking by recorded deaths would
rank noma near zero. The right response is probably a **confidence on the burden
figure** rather than a correction to it: the register can honestly say *this is
unknown and the direction of the error is known*, and that is more useful than a
number.

## 89. `disease-modifying` is binned with `none`, so the largest victory in medicine reads as nothing · **CLOSED 2026-08-23**
*Forced by:* `ischaemic-heart-disease`.

`quadrant()` computes `fixable = intervention in ("suppressive", "curative")`.
Everything below that — `disease-modifying`, `symptomatic`, `none` — falls into
the same bucket.

So ischaemic heart disease, **~9 million deaths a year, the largest cause of
death on Earth**, lands in `engineering problem`: *the mechanism is known and
nothing can be done.*

That is said about a disease whose age-standardised death rate in high-income
countries **has more than halved since about 1980** — statins, blood-pressure
control, smoking cessation, coronary care, and opening the artery in time. It is
the largest public-health victory anywhere in this register.

**The ladder is right and the binning is wrong.** `disease-modifying` genuinely
is the honest rung for IHD: statins slow plaque accumulation, they do not stop or
clear it; antiplatelets make thrombosis on a ruptured cap less likely, they do
not prevent the rupture. The process is slowed, not held. That is the definition.

But the gap between `symptomatic` (masks the phenotype, course unchanged) and
`disease-modifying` (slows the course) is **the difference between paracetamol
and a statin**, and the 2×2 cannot see it. A binary "fixable" cannot carry a
five-rung ladder; that is what the ladder was built to replace.

This is **not** #66. That one says `capability()` ignores the prevention axis —
true here too, and it costs more on this record than on any other, since most of
the IHD decline is preventive. This one is about the treatment axis itself:
even scoring *only* what treatment achieved, the derivation gets it backwards.

Three candidate fixes, and the choice is a real one:

- **Add a middle column.** `known & treatable` / **`known & modifiable`** /
  `engineering problem`. Honest, and turns a 2×2 into a 2×3.
- **Move `disease-modifying` up.** One character of change, and it would file
  IHD next to hepatitis C, which is worse than the current error.
- **Stop deriving a quadrant at all** and let `capability` + `reach` + `terms`
  carry it. The 2×2 is the most quotable thing on the public page and the least
  able to hold a qualifier — the same problem that forced the `solved` →
  `known & treatable` rename.

Note that only one other record is `disease-modifying` — rheumatic heart disease,
also filed `engineering problem`, also cardiac, and there the label happens to
read acceptably. **One record made a broken rule look fine.** Forty-two records
in, that is the argument for corpus-before-schema stated as compactly as it gets.

### Fixed — the middle column, 2026-08-23

**COPD adjudicated it** (record 44, added deliberately before the repair). It is
`symptomatic`, so it belongs in the bottom band and the harsh verdict on its
*course* is deserved. Moving the rung up would have left `symptomatic` and
`none` conflated — which #98 then showed is its own error — and deleting the map
would have lost a true statement about COPD. **A third band separates all three
records correctly**, and forty-three records had not supplied a case where the
harsh verdict was earned.

The second axis is now the ladder in three bands: the course is **held or
ended** (`suppressive`, `curative`) · **slowed** (`disease-modifying`) ·
**unchanged** (`symptomatic`, `none`).

|  | treatable | modifiable | neither |
|---|---|---|---|
| **known** | known & treatable (30) | **known & modifiable (3)** | engineering problem (6) |
| **not known** | empirical luck (1) | *empirical foothold* (0) | frontier (4) |

`ischaemic-heart-disease`, `stroke` and `rheumatic-heart-disease` moved out of
*understood and nothing can be done*. Nothing else moved.

Four decisions worth recording, because each was a real choice:

- **The field is still called `quadrant`** with six cells. The name is now
  literally wrong and was kept because `quadrant:frontier` is a canned question
  on the public page and `quadrant:"known & treatable"` is the documented
  example of quoting in the query language. **Accuracy in a field name is worth
  less than not breaking a query somebody bookmarked.** The user-facing labels —
  the part that can state a verdict about a disease — say *map* and *cell*.
- **`empirical foothold` is named although no record occupies it.** The
  derivation has to be total. If it is still empty at a hundred records that is
  a finding, not dead code.
- **Every new cell carries its qualifier in the verdict sentence**, not only in
  the glossary — the rule the `solved` → `known & treatable` rename established.
  `engineering problem` now says explicitly that it does *not* mean treatment
  does nothing, which is #98 in the one place a reader will actually meet it.
- **A test that hardcoded the four cell names passed throughout.** It listed the
  names that already existed, so growing the map could not fail it. Replaced
  with a general rule — *every cell a record lands in must be defined in the
  glossary* — plus a pin on the three records that forced the change. The
  hardcoded list is what went stale, so the fix is to stop having one.

Still open and untouched by this: **#66** (`capability()` ignores the prevention
axis) — which is why dengue, rabies and dracunculiasis are still in
`engineering problem`, and it is the next-cheapest repair. And **#98** (symptom
relief is not benefit anywhere in this schema), which the new bottom band makes
more visible rather than less.

## 90. Who counts as a patient is a threshold somebody chose · **open**
*Forced by:* `ischaemic-heart-disease`.

Coronary atherosclerosis is a continuum. Fatty streaks appear in adolescence and
subclinical plaque is close to universal with age. **There is no point on that
continuum where the disease begins** — there is a risk threshold in a guideline,
and it decides who is a patient.

Move the ten-year-risk threshold for starting a statin and tens of millions of
people change category overnight. The biology does not move. This has happened.

The register's two most-used scalars are both **fractions of patients**:

- `efficacy` — fraction of patients in whom the best intervention works
- `access` — fraction of patients who can get it

**Both denominators are set by a committee vote, not by biology**, and the
register records neither the threshold nor its provenance. Two registers using
different guidelines would report different `access` for identical care.

It generalises well beyond this record. Hypertension (the threshold moved from
140/90 to 130/80 in one guideline and not another, reclassifying a large share of
adults). Diabetes and prediabetes. Chronic kidney disease staging. Osteoporosis
by bone-density T-score. Obesity by BMI cut-point. In every case a continuous
variable is dichotomised and the cut-point is contested, consequential, and
absent from this schema.

And it interacts badly with the burden metric (#48): **you cannot compute
unreached burden when the size of the population needing treatment is a policy
choice.** The number can be moved by writing a guideline rather than by treating
anybody.

The minimal fix is to let a record declare the threshold that defines its
denominator, with a source and a date, the way `moved:` dates a rating. The
deeper question — whether the register should carry entities whose boundary is
a decision rather than a fact — is the same one `contested:` gestures at and
does not answer.

## 91. The register has no memory before its own first pass · **PARTLY WRONG when written; corrected at `smallpox`**
*Forced by:* `ischaemic-heart-disease`.

The rename argued that `moved:` is load-bearing because it makes a second pass a
*comparison* rather than a fresh opinion. That is right, and it only works
forward. `moved` records **this register's rating changing between its own
passes.** The first pass has nothing to compare to.

Ischaemic heart disease arrives carrying **fifty years of trajectory that cannot
be written down.** Rated in 1970 it would have been `symptomatic` — no statins,
no thrombolysis, no angioplasty, no coronary care units, and a large infarct
carried roughly a one-in-three chance of dying in hospital. Rated today it is
`disease-modifying` with in-hospital mortality in the low single digits and the
age-standardised death rate more than halved.

**The register can state neither of those facts, nor the distance between them.**
It records a position. The thing it exists to measure is a trajectory.

That matters more here than anywhere else in the corpus, because IHD is the best
evidence in medicine that **the loop this project is built around actually
works** — measure, pull something off the queue, solve it, re-measure. It ran for
fifty years on the largest killer there is and it moved. A register meant to be
the north star for exactly that loop cannot currently cite its best precedent.

Related and distinct:

- **#26** wants `moved: axis: toll` so falling treatment harm reads as progress.
  Same instinct, one axis, and forward-looking.
- **#56** (HAT) asks the *opposite* question — whether a good rating is being held
  in place by continuous effort, and notes that every `moved` entry so far
  records an improvement.
- This one asks for **backdated entries**: `moved:` with a date before the
  register existed, an axis, a rating, and a source. Cheap to add and it makes
  every record able to say which direction it is travelling.

The obvious objection is that backdating is retrospective opinion rather than
measurement, and it is a fair one. The answer is that it is exactly as much an
opinion as the current rating, dated and attributable in the same way, and that
**a north star with no history is a snapshot with ambitions.**

## 92. The lesion you can see is not the lesion that kills you · **open**
*Forced by:* `ischaemic-heart-disease`.

A tight coronary stenosis causes angina, shows up on every imaging modality, and
can be stented. **Most myocardial infarctions arise from rupture of a plaque that
was not flow-limiting** — one that would not have caused symptoms and would not
have been treated.

So the thing that is **detectable** and the thing that is **lethal** are different
objects. Which explains, without any further hypothesis, why an era of stenting
stable coronary disease produced enormous procedural volume and little mortality
benefit, and why a cheap generic tablet that treats the whole arterial tree
outperformed a procedure that treats one segment of it perfectly.

The register's `measurement` trichotomy cannot express this. All three questions
presuppose the target is right:

| | question | what it assumes |
|---|---|---|
| diagnostic | is it there? | *it* is the thing that matters |
| prognostic | what will it do untreated? | *it* is the thing that will do it |
| predictive | will this treatment work? | the treatment is aimed at *it* |

IHD rates `objective` on diagnostic — troponin, angiography, calcium scoring are
all excellent — and the rating is true and beside the point.

**And this is the mechanism behind overdiagnosis**, which the register already
derives a flag for (`overtreatment_risk`) without ever saying why it happens.
The corpus has the pattern repeatedly and names it nowhere:

| record | what is detected | what actually kills |
|---|---|---|
| **ischaemic-heart-disease** | flow-limiting stenosis | rupture of a non-obstructive plaque |
| **breast-cancer** | any screen-detected lesion, DCIS included | the subset that would have progressed |
| **prostate cancer** (absent) | PSA elevation | the small aggressive fraction |
| **thyroid cancer** (absent) | incidentally imaged nodules | almost none of them |

Two of the four canonical cases are not in the register, which is #48's coverage
problem showing up as a *conceptual* hole rather than an arithmetic one.

The cheap version is a fourth measurement question — *is the detectable feature
the causal one?* The honest version is that this is a claim about the disease
model rather than about a test, and it may belong wherever #55's relations
eventually live.

## 93. `strata` cannot override `mechanism`, and the justification is false here · **open**
*Forced by:* `stroke`.

SCHEMA.md says a stratum overrides only `intervention`, `efficacy` and `toll`,
because *"`mechanism` and `diagnosis` do not vary by stage; it is the same
disease."*

That is true of breast cancer, which forced the field. **It is flatly untrue of
stroke.**

| stratum | mechanism | acute treatment |
|---|---|---|
| ischaemic (~65%) | thrombosis or embolism occludes a vessel | dissolve or remove the clot |
| intracerebral haemorrhage (~27%) | a vessel ruptures into brain | **giving the above kills the patient** |
| subarachnoid (~8%) | a saccular aneurysm ruptures | secure the aneurysm |

These are different mechanisms with opposite treatments and **identical
presentations**. Nothing at the bedside distinguishes them; a CT scan is the
entire decision.

The record is forced to rate `mechanism: established` once, at record level, for
three different chains — which happens to be defensible only because all three
are individually well understood. A record where one stratum's mechanism was
`established` and another's `correlates` could not be written at all.

The deeper issue is that **`strata` was built for severity and is being used for
kind.** Breast cancer stage I vs IV is one disease caught at two points. Ischaemic
vs haemorrhagic stroke is two diseases sharing a name because they share a
presentation — a *clinical syndrome* rather than a mechanism-defined entity.
The register has no way to say which of those two things a `strata` block is
doing, and the answer changes what may vary.

Note this is the mirror of what #89's record could not do. Ischaemic heart
disease has genuine sub-populations and carries **no** `strata` block, because
its divisions are phases of one trajectory rather than a partition. Stroke's
divisions are a true partition and it needs a field that partitions more than
the schema allows. **Two consecutive cardiovascular records, opposite failures,
one field.**

## 94. A window can be measured rather than assumed · **open, and it is a win the register cannot record**
*Forced by:* `stroke`.

Every `window` in this register is a duration. Hours for dengue. Days for noma.
Minutes for myocardial infarction. `caught_in_time` then asks what fraction of
patients arrived inside it.

**Stroke proved the duration is a population average standing in for a
patient-specific fact — and that the fact is directly measurable.**

Thrombectomy for large-vessel occlusion was established within six hours of
onset. Trials that selected patients by *perfusion imaging* — a small completed
core, a large volume of still-salvageable tissue — extended it to twenty-four
hours, in patients the clock excluded. Collateral circulation varies enormously:
one person's penumbra is gone in ninety minutes, another's survives most of a
day. It also partly rescues the wake-up stroke, where onset time is not merely
late but *unknown*.

The window was not extended. **It was measured.**

That is a genuinely different kind of answer, and it is a general one:

- A window stated as a duration is a **claim about the average patient**.
- A window stated as a measurement is a **procedure for interrogating this
  patient**.
- The second converts an eligibility rule into a test — which is the register's
  own thesis about measurement, arriving from the direction it least expects.

The schema cannot express it. `closes_on` takes prose, `caught_in_time` takes a
fraction, and neither can say *the window is imageable, and here is what images
it.* Stroke's record says so in prose and the derivation cannot see it.

It also reframes several open items. **#84** (diagnosis is a trained person, not
a device) and the noma diagnosis blocker both assume the window is fixed and the
problem is arrival. Here the problem was partly the *rule*, and the fix was a
better measurement of the patient rather than a faster ambulance. Where else in
the corpus is a window a guideline rather than a biological fact? Dengue's fluid
window and Buruli's are both stated as durations and neither has been asked.

And it is the answer to ischaemic heart disease's unanswerable question in a
different key. IHD's `knowledge` blocker wants to *predict* which plaque will
rupture. Stroke did not predict anything — **it measured the current state of the
tissue instead.** Prediction is not always the only way out of a prognostic gap.

## 95. `efficacy` assumes everyone agrees what "works" means · **open**
*Forced by:* `stroke`.

`efficacy` is defined as the fraction of patients in whom the best intervention
*works*. The schema treats "works" as given.

**In severe stroke it is contested, by the people it is done to.**

Decompressive hemicraniectomy for a malignant middle cerebral artery infarct
reliably prevents death by removing part of the skull. What it delivers is
survival with major disability. The operation succeeds at what it does. Whether
that is a good outcome is a question patients and families answer differently,
and answer differently *before* and *after*.

The same argument runs through the trial literature as a methodological one:
where the "good outcome" threshold is drawn on a disability scale changes what a
trial found. Move it one point and treatments change from effective to not. That
is not measurement error — it is a **value judgement inside the numerator**.

Which pairs exactly with #90, forced by the previous record:

| | what is chosen | example |
|---|---|---|
| **#90** | the **denominator** — who counts as a patient | the risk threshold that starts a statin |
| **#95** | the **numerator** — what counts as working | which disability level counts as a good outcome |

Both are guideline decisions wearing the clothes of empirical scalars. Together
they say something uncomfortable about the register's two most-used numbers:
**`efficacy` and `access` are not measurements of the world, they are
measurements of the world relative to two conventions the register does not
record.**

It generalises well beyond stroke. Progression-free versus overall survival in
oncology. Symptom scores versus function in psychiatry and in chronic pain.
Biochemical control versus how a patient feels in endocrinology. In every case
`efficacy: 0.7` conceals which question was asked.

The cheap fix is a required `units:` string that names the success criterion —
which the corpus has been informally doing for a while, and which nothing checks.
The honest fix admits that for some entities there is no single defensible
number, and that the strata carry the truth while the record-level scalar exists
because the schema demands one. Stroke says exactly that in its `holes`.

## 96. A window can close before there is anything to diagnose · **open**
*Forced by:* `copd`.

Lung function rises through childhood, peaks in the early twenties, then
declines. COPD arrives by either of two routes:

- **accelerated decline from a normal peak** — the classic smoking picture, and
  the one the register's instincts were built on; or
- **never reaching a normal peak** — prematurity, childhood respiratory
  infection, malnutrition, early-life smoke exposure, impaired lung growth from
  any cause.

**Roughly half of COPD comes by the second route.** For those people the
determinative period was gestation to about age twenty-five, the disease appears
at sixty, and nothing they did as an adult caused it.

The register's `window` field cannot hold this, and the reason is structural
rather than a missing enum. Every window in the corpus assumes **the disease is
present and a clock is running on treating it**: minutes for stroke, hours for
dengue, days for noma, decades for COPD's own smoking-cessation window. Here
there was no disease during the window. There was a child growing lungs.

It is not the same as rheumatic heart disease or schistosomiasis, which look
similar. In those, something is present and treatable inside the window — a
streptococcal infection, a fluke. Here **the intervention is optimising a normal
developmental process**, and there is nothing to diagnose, nothing to treat, and
no patient.

The consequences are uncomfortable for a register organised by entity:

- **The highest-leverage intervention for an adult disease is paediatric, and
  not disease-directed.** Neonatal care, childhood nutrition, vaccination against
  respiratory infection, and keeping smoke out of houses with small children in
  them.
- It is **#87 fused with `window`** — the intervention is non-specific *and* it
  is decades early, so it is doubly unchargeable to this record.
- And it cannot be validated by the register's own arithmetic. `caught_in_time`
  asks what fraction of *cases* were reached in time; here the denominator is
  the whole birth cohort, most of whom will never get the disease.

Worth asking across the corpus once the field exists, because COPD is unlikely to
be alone: how much of adult disease was decided before adulthood, and does any
record say so?

## 97. The permanent damage of a disease that never ends has nowhere to go · **open**
*Forced by:* `copd`.

The schema holds two permanent prices and COPD's is neither:

| field | what it holds |
|---|---|
| `toll` | what the **treatment** took |
| `residue` | what the **disease** left in someone the treatment worked on |

COPD's destroyed alveoli are not what the disease left behind. They are the
disease, still doing it — which is exactly the case the dracunculiasis
correction wrote into `check.py`, and COPD is its cleanest instance. The record
carries no `residue` block and says why.

But then **the register cannot state the single most important fact about a
living COPD patient**: how much lung they have permanently lost. It is
irreversible, it is the whole of their prognosis, and there is no field for it.
The axes say the intervention is `symptomatic` and the burden block counts
people; neither says *this person has lost half their lung and will not get it
back.*

**And the generated report shows the cost immediately.** `window_toll_link`
fires on COPD and reports *"the toll is the price of missing it."* The price of
missing COPD's twenty-year window is **lung**, not corticosteroids. The flag is
right and its stated reason is wrong, because the only permanent price the schema
can see is the one treatment charged. Second false-reason flag in five records,
after noma's `overtreatment_risk` (#61).

There is a second scoping problem underneath it. **Exacerbations end.** Each one
is an episode that resolves, and each leaves a permanent step-down in function
that never fully recovers. By the corrected rule that is a textbook `residue` —
an episode that ended, leaving damage — and the field cannot express it because
it is scoped to the *disease* rather than to the *episode*. A person with twenty
exacerbations over fifteen years has twenty residues and the schema records none.

Candidate: a third permanent-damage field scoped to *accumulated loss in a
continuing disease*, or `residue` gaining an explicit scope (`disease` |
`episode`). The second is smaller and probably right.

## 98. Symptom relief is not a benefit anywhere in this schema · **open, and the report says so out loud**
*Forced by:* `copd`, and *found by running `check.py`* rather than by reasoning
about the record.

COPD landed in the generated section headed **"Harm without benefit — a major
toll and nothing to show for it."** It is the second record ever to appear there,
after low back pain.

The derivation is internally correct. The toll is `major` — dozens of oral
corticosteroid courses over a decade produce osteoporosis, fragility fracture,
diabetes, cataracts, adrenal suppression, and each course is individually
justified while the total is nobody's decision. And `capability` is `unsolved`,
because nothing alters the decline in lung function.

**But "nothing to show for it" is false.** Long-acting bronchodilators
substantially relieve breathlessness. For a disease whose entire burden *is*
breathlessness — a symptom that is not pain and is worse than most pain to live
with, and which constricts a life to a few rooms — that is a large benefit
delivered to hundreds of millions of people.

The register has exactly one notion of benefit and it is **course alteration**.
`capability` reads `intervention`; the ladder's bottom rung is defined as *masks
the phenotype, course unchanged*; `reach` multiplies two fractions that both
inherit that meaning. Nowhere does anything record that the phenotype being
masked was the thing ruining the patient's life.

It is not a COPD problem. It is the whole of symptomatic and palliative
medicine, and the corpus already carries the cases:

| record | the symptom | what relieving it is worth |
|---|---|---|
| **copd** | breathlessness | the difference between two rooms and a life |
| **low-back-pain** | pain | the register's other "harm without benefit" record |
| **crohns**, **sickle-cell** | pain crises | recorded only as `ongoing` cost |
| **me-cfs** | exhaustion | `intervention: none`, and nothing about symptom care |

And note it interacts with **#95**, one record earlier. That gap said `efficacy`
assumes agreement about what "works" means. This says something stronger:
**the schema has already decided, and it decided against the patient.** A
treatment that changes how someone feels every day, and does not change when
they die, scores zero.

Minimal fix: `capability` is a claim about the disease and should stay that way,
but the report must stop asserting *"nothing to show for it"* — that sentence is
a verdict the data does not support, and it is the same defect as the
`solved` → `known & treatable` rename. Larger fix: a symptom-control axis read
alongside `ongoing`, which currently records only the cost of treatment and
never its felt benefit.

## 99. The register assumes a steady state, and epidemic disease is not one · **open**
*Forced by:* `ebola`.

Ebola's burden is zero in most years, **11,300 deaths in 2014-16**, 2,300 in
2018-20, and zero again. The record's `burden.deaths` field says **310 per
year** — fifteen thousand deaths since 1976 divided by the years since — and
**no year has ever resembled it.** A burden-ranked register would file Ebola
below mycetoma on the strength of that number.

Four fields break, and they break in different ways:

- **`burden`** wants an annual rate. There isn't one. The mean is a fiction, the
  peak is a fiction, and the distribution is the actual fact.
- **`access`** is defined as the fraction of patients who can get the treatment.
  Between outbreaks there are no patients. During one, "access" means **how fast
  an emergency deploys into somewhere remote that may be at war** — a rate, not
  a state, and not remotely the same quantity as whether a pharmacy stocks a
  drug.
- **`reach = efficacy × access`** therefore multiplies a good number by a
  category error.
- **`window`** holds the patient's clock and not the outbreak's. West Africa
  2014 went roughly three months unrecognised and produced 28,600 cases;
  outbreaks caught in weeks produce dozens. **The difference between a dozen
  cases and twenty-eight thousand is not biology**, and the field that would say
  so does not exist.

That last one is the most interesting, because it says the `window` concept
**scales from patient to population** and the schema only implemented the
patient version. Stroke's window is minutes for one person. Ebola's decisive
window is weeks for an epidemic. Same idea, different unit.

And it explains the funding pathology without needing a separate gap.
**rVSV-ZEBOV was built in the early 2000s and sat unlicensed for roughly a
decade**, because a vaccine against a disease that kills a few dozen people in a
bad year has no market. What changed in 2014 was not a discovery. Worse, for
*Sudan* ebolavirus there is still nothing licensed, because the trial that would
license it can only run during an outbreak — and the 2022 Uganda outbreak ended
before its vaccine trial could enrol. **Success at containment is failure at
evidence**, which is a trap no steady-state disease can fall into.

Minimal fix: `burden` accepts a distribution or an explicit `episodic: true`
with the outbreak history, so the annual figure stops pretending. Larger fix:
an outbreak-scoped window, and an `access` that can express *time to deploy*
rather than *fraction stocked*. Every remaining record on the queue that is
outbreak-shaped — marburg, h5n1, covid-19, cholera, influenza — hits this, so
it is worth doing before them rather than after.

## 100. The schema is patient-scoped, and cure does not end transmissibility · **open**
*Forced by:* `ebola`.

Ebola virus persists in immune-privileged sites — the eye, the testis — for
months to years after the blood has cleared and the patient has been declared
cured. Live virus has been recovered from the aqueous humour of a survivor
months after recovery. **Sexual transmission from recovered survivors has
restarted outbreaks.**

The schema has two fields for what is left afterwards and this is neither:

| field | scope | Ebola persistence |
|---|---|---|
| `toll` | what the **treatment** took from the patient | no |
| `residue` | what the **disease** left in the patient | no — it is not damage |

It is not damage to the survivor at all. **It is a risk they carry for everybody
else**, and the consequence is real: every survivor enters a semen testing and
counselling programme, on a timescale set by guesswork, which is surveillance of
the patient on the population's behalf rather than treatment of the patient.
`ongoing` records the cost of being treated and cannot hold it either.

The general shape is that **every field in this register is scoped to one
patient**, and some of the most important facts about an infectious disease are
epidemiological. The corpus already has the pattern and names it nowhere:

| record | the fact | why the schema misses it |
|---|---|---|
| **ebola** | cured survivors remain infectious for months | not damage, not treatment cost |
| **dracunculiasis** | the burning blister drives the host into water (#86) | a symptom with a function for the pathogen |
| **stroke** ↔ **atrial fibrillation** | treating one causes the other | harm lands in a different entity |
| **taeniasis-cysticercosis**, **echinococcosis** | the intervention goes to another species (#69) | no veterinary actor exists |

And Ebola adds a nasty variant of **#77** (stigma is a feedback loop). Survivors
lose homes, jobs and marriages, as with leprosy and noma — except that here
**the stigma has a factual kernel.** A community's fear is wrong about the person
in front of them and not wrong about the biology. Nothing in this register can
express *a prejudice that is unjust and not baseless*, and the difference matters
for what you would do about it.

Candidate: a `transmits` block scoped to the population rather than the patient —
after cure, from a vector, to another species — which would absorb #69 and #86
as well. That is three gaps pointing at one missing scope, which is usually the
signal that the field is real.

## 101. A knowledge question can be answered and change nothing · **open, and it corrects the previous record**
*Forced by:* `marburg`, against `ebola`.

One record ago, Ebola's `knowledge` blocker read:

> **THE RESERVOIR IS NOT ESTABLISHED.** [...] Without it there is no way to
> predict a spillover, no way to target surveillance, and no possibility of
> acting before the first human case — which is the only intervention that would
> ever be cheap.

**Marburg's reservoir is established.** The Egyptian rousette bat. Not inferred
from antibodies — infectious virus isolated from wild colonies, and outbreaks
traced repeatedly to named caves and to the Durba mine.

What followed was: tell miners.

The bats cannot be eliminated and should not be. The timing of spillover is still
unpredictable. No product, no surveillance system and no capability came of it,
and Marburg remains `unsolved` fifty-eight years after it was the *first*
filovirus ever identified — nine years before Ebola.

So the claim Ebola's record made is **necessary but nowhere near sufficient**,
and the register's blocker model quietly assumes otherwise. A `knowledge` blocker
carries `scale: null`, and the stated asymmetry is that *knowledge blockers
cannot be triaged with money, delivery blockers can*. Both halves of that assume
the same thing: **that answering the question unblocks something.** Marburg is
the case where it was answered and nothing moved.

Which means a `knowledge` blocker should have to say **what becomes possible if
it is answered**, and the honest answer is sometimes *nothing much*. Candidates
elsewhere in the corpus that deserve the same interrogation:

- **copd** — knowing which smokers are susceptible would aim cessation effort.
  Plausible lever. Probably real.
- **ischaemic-heart-disease** — knowing which plaque will rupture. Enormous
  lever, if it were ever answerable.
- **ebola** — the reservoir. **Marburg now says: little to no lever.** Ebola's
  file should be revised when this is fixed rather than quietly left.
- **me-cfs**, **heds** — mechanism unknown, and nobody can say in advance what
  answering it would unlock, which is the honest position and is not currently
  distinguishable from the confident cases.

This is a mirror of #57 (the register cannot value maintenance). There, doing
nothing new looks like no progress. Here, learning something true looks like
progress and may not be.

## 102. Some diseases can never generate the evidence their own approval requires · **open**
*Forced by:* `marburg`.

**Roughly 600 to 700 human cases in fifty-eight years.**

A phase III efficacy trial for Marburg is not slow, or expensive, or
under-prioritised. **It is impossible.** There is no plausible future in which
enough people are infected, in one place, at one time, to power one. The 2024
Rwandan outbreak deployed candidate products under protocol and ended —
correctly, by design, because containment worked — before enrolment could reach
anything like significance.

Ebola's #99 called this *success at containment is failure at evidence*, and
treated it as an unlucky outcome for Sudan ebolavirus. **For Marburg it is not
an outcome, it is the permanent condition.**

A route exists — licensure on animal efficacy data plus human safety data, a
pathway written for exactly this — and using it needs a regulator to accept it, a
sponsor to build the animal-model package, and someone to pay for both in advance
of any demand. That is the **second use of the `regulatory` blocker kind in
forty-six records**, and the first where the obstacle is *the evidentiary
standard itself* rather than a decision taken under it.

The register cannot currently distinguish three very different situations that
all present as "no licensed product":

| situation | example | what would fix it |
|---|---|---|
| nobody has tried | many rare diseases | a sponsor |
| tried and failed | Alzheimer's, for decades | science |
| **cannot be tried** | **marburg** | **a different evidentiary standard** |

Only the third is a `regulatory` problem, and only the third is fixable by a
decision rather than by work. It generalises past filoviruses to any
ultra-rare disease, to bioterror agents, and to anything where the trial that
would license the product cannot ethically or practically be run.

Worth adding a blocker field naming *what evidence would suffice*, since for this
class the answer is not "a bigger trial."

## 103. The register rates what exists, and preparedness is a capability no axis holds · **open**
*Forced by:* `h5n1`.

About 950 confirmed human cases since 2003 and about 465 deaths — **21 a year**,
smaller than mycetoma, and completely beside the point.

**H5N1 matters because of something that has not happened.** It is not
efficiently transmissible between humans; a small number of molecular changes
might make it so, and clade 2.3.4.4b has meanwhile produced the largest animal
influenza panzootic ever recorded — every continent including Antarctica, mass
mortality in marine mammals, and since 2024 sustained cow-to-cow spread in US
dairy herds.

This is **not** #99. Ebola and Marburg have real recurring burden that arrives in
clumps; the fields are the wrong shape but they are measuring something that
happened. Here the entire content of the record is a **conditional probability
about a virus that does not exist**, and the register has no grammar for a
conditional.

The concrete missing piece is that **preparedness is not on any axis**:

| what exists | why no axis holds it |
|---|---|
| stockpiled H5N1 vaccines, matched to clades chosen years ago | not `intervention` — nobody is a patient; not `prevention` — nobody is vaccinated |
| antiviral reserves | held against demand that may never arrive |
| wild bird, poultry, dairy and worker surveillance | detects an event rather than treating a person |
| manufacturing surge capacity | the single most important number here, and it is a *lead time* |

The register's most important figure for this record would be **time from strain
identification to a hundred million matched doses** — currently about six months
by egg-based manufacture, against a first pandemic wave that does not wait.
`window` is scoped to a patient and cannot say it.

Two consequences worth stating plainly:

- **`prophylaxis` is true here and means something else.** Post-exposure
  oseltamivir for cullers is genuine prophylaxis. The prevention that has
  actually worked is *culling hundreds of millions of birds*, and the pandemic
  prevention is *a warehouse*. Neither is what the enum means anywhere else.
- **The most effective pandemic prevention available may be an agricultural
  compensation scheme.** Culling works only if farmers report early, and they
  report early only if compensation is prompt. No axis here can represent that as
  capability of any kind.

Every remaining outbreak record on the queue — covid-19, influenza, and to a
lesser extent cholera — carries some of this. H5N1 is the pure case because the
disease of concern has no cases at all.

## 104. What a disease appears to do depends on how hard you looked · **open**
*Forced by:* `h5n1`. **The complement of #88.**

The famous number about H5N1 is a **~50% case fatality rate**. It is a statement
about surveillance.

Confirmation has historically required someone to fall ill enough to reach a
hospital, for a clinician to think of a rare avian subtype, and for the test to
exist. Mild infection is invisible by construction in that regime.

Then in 2024 active surveillance was applied to exposed US dairy workers, and
what it found was mostly **conjunctivitis** — mild, self-limiting, and it would
never have entered the historical count.

**The same pathogen family looks like a fifty-percent killer under one
ascertainment regime and a nuisance under another, and the number driving every
pandemic plan in the world is the first one.** Some of the gap is real virology
and some is certainly ascertainment; nobody can say how much is which, which is
why the record declines to stratify.

This is **not** #90. That gap says the *denominator is a threshold somebody
chose* — where hypertension starts, what FEV1/FVC counts as COPD. This says the
denominator is set by **how many people you bothered to look at**, which is an
effort, not a definition, and it changes not who is a patient but **what the
disease appears to do**.

And it is the exact mirror of **#88**, which noma forced:

| | what goes uncounted | what it does to the record |
|---|---|---|
| **#88** (noma) | the **dead** — nine in ten die at home, uncounted | burden looks small; the disease looks survivable |
| **#104** (h5n1) | the **mildly ill** — never tested, never confirmed | burden looks small; the disease looks lethal |

Together they say something the register nowhere admits: **its picture of a
disease is a picture of that disease's surveillance system.** Both distortions
shrink the burden figure, and they push the apparent severity in opposite
directions.

The corpus has more instances than these two. Ebola's case fatality varies across
outbreaks partly through ascertainment. Marburg's ranges from a quarter to ninety
percent. COPD's prevalence counts only the diagnosed half.

Minimal fix: an ascertainment note on `burden`, saying how cases were found —
passive hospital detection, active surveillance of an exposed group, screening,
serosurvey — because that determines what the numbers mean. The register already
requires `src` for every scalar; **this is `src` for the denominator.**

## 105. `toll` is what the cure costs, and prevention has costs too · **open**
*Forced by:* `smallpox`.

The smallpox vaccine killed people. Progressive vaccinia in the
immunosuppressed, eczema vaccinatum in the atopic, post-vaccinial encephalitis,
myocarditis and pericarditis — at population scale, deaths per million per year,
in healthy people protected against a disease most of them would never have met.

**That number is why routine vaccination stopped.** Once incidence fell far
enough, the vaccine became more dangerous than the disease. There is a crossing
point, it is computable in principle, and **it is the thing that actually ends an
eradication programme.**

The register holds one of the two quantities. `toll` is defined as what the
*cure* costs the patient, so smallpox's `toll` reads `minor` — accurately, since
there is no treatment — and the harm that decided the entire endgame has nowhere
to go.

It is not a smallpox problem. The corpus is full of preventive interventions with
real costs and no field for them:

| record | preventive intervention | its cost |
|---|---|---|
| **smallpox** | vaccinia vaccination | deaths per million, and it ended the programme |
| **pku** | newborn screening + lifelong diet | the diet is the whole burden of the disease |
| **rheumatic-heart-disease** | monthly benzathine penicillin for years | injections, anaphylaxis risk, adherence |
| **ischaemic-heart-disease** | statins in primary prevention | myalgia, and half stop taking them |
| **h5n1** | culling | hundreds of millions of animals, and farmers ruined |

And note the asymmetry it creates in the derivations. `cured_at_a_price` and
`restored` both read `toll`, so a disease prevented at great cost and treated at
none reads as **`restored` — nothing permanent from either side**. PKU is the
existing case and smallpox is the extreme.

Minimal fix: `toll` gains a scope (`treatment` | `prevention`), or a parallel
block. The harder question is the crossing point — **the register cannot say when
an intervention should stop**, and for the one disease that finished, that is the
most interesting number in the file.

## 106. Winning removes capability · **open**
*Forced by:* `smallpox`.

**No clinician now practising has seen a case of smallpox.**

The clinical diagnosis that made eradication possible — an unmistakable rash, in
a single crop, centrifugal, on palms and soles — was a skill distributed to
village health workers with laminated recognition cards. It is what allowed
surveillance-containment to work where the nearest laboratory was days away.
That skill no longer exists anywhere. PCR would confirm a case instantly, and
somebody has to order it, which requires believing that a disease eradicated in
1980 is in the room.

Three capabilities were spent to win, and the register records none of the loss:

- **Clinical recognition.** Gone with the generation that saw it.
- **Population immunity.** Routine vaccination ended in the late 1970s, leaving a
  growing majority with no orthopoxvirus cross-protection — which is widely
  argued to be part of why **mpox** is now doing what it is doing. *Eradicating
  one disease contributed to the rise of another.*
- **Institutional expertise.** The people who ran the programme dispersed, and
  the next one starts from documents.

The general form is that **the register treats capability as a property of the
disease, and it is a stock held by people and institutions that depletes when
unused.** Nothing here can say that a rating was true in 1975 and would not
survive being tested today. Smallpox's `caught_in_time` is recorded at 0.80 —
a real historical figure from the containment era — and for a case occurring now
it would be near zero, for reasons that have nothing to do with the virus.

It has a nasty corollary for the whole project. **The register is a snapshot of
what is currently possible, and what is currently possible decays.** Polio, if it
finishes, will hit this immediately. So will any disease whose elimination ends
the training that detects it.

And it is a *harm* crossing an entity boundary, where #87 and #63 were about
benefits crossing. Three gaps now describe effects that land outside the record
that caused them, which is the same missing structure #100 named.

---

### Two corrections to this file, found by querying instead of remembering

Writing smallpox's `moved:` block meant checking what `moved` could actually do,
and two claims made in this file were wrong.

**#91 said `moved` only works forward** — that it *"records this register's
rating changing between its own passes"* and that backdated entries were the
thing to build. **They already existed.** Nine records carry `moved` entries and
every one of them is backdated, ranging from **yaws in 1964** to sickle cell in
2023. HIV's 1996 entry — `intervention: symptomatic → suppressive` — was in the
corpus long before #91 was written at record 42.

What survives of #91 is narrower and still real: the register records a
*position* and offers no *trajectory view*, no way to see all the `moved` entries
as a series, and no account of **why** a rating is what it is — which is what
Marburg needed and could not have. The mechanism was never the problem.

**#56 said every `moved` entry records an improvement**, and asked for the field
to be able to record a rating going backwards. **Yaws already did, two records
later, and nobody marked it:** `access: 0.9 → 0.2` in 1964, when the global
campaign that had nearly finished the disease was wound down and the disease came
back. The gap was closed by the corpus and left open in the file.

Both errors have the same cause — **a claim about the register written from
memory of the register** — which is precisely what it exists to prevent. The
lesson is the cheap one: query before asserting. `test_check.py` now reconciles
index.md's blocker census against the records for the same reason.

## 107. A refuted claim can be a documented obstacle · **open**
*Forced by:* `measles`, and by the first use of `standing: refuted` in 175 blockers.

The claim that MMR causes autism originates in a retracted 1998 paper, has failed
replication in cohort studies covering millions of children across several
countries, and its author lost his medical licence. **There is no association.**

It is also, demonstrably, one of the largest obstacles to measles control on
earth. Coverage falls, coverage below ~95% lets transmission re-establish, and
children have died.

So the record needs to say two things at once:

| | |
|---|---|
| the **causal claim** — *the vaccine causes autism* | **refuted** |
| the **blocking effect** — *this claim reduces coverage* | **documented** |

`standing` has one slot and is forced onto both. Filed as `refuted`, the record
reads as though the obstacle were imaginary, which is exactly backwards — it is
the most consequential blocker in the file. Filed as `documented`, the register
would be recording a falsehood as though it were a finding.

This matters beyond one record, because **`standing` was built precisely to test
claims of this shape.** The register's stated purpose for the field is to
interrogate the widely-repeated *"it's solvable but pharma/FDA won't allow it"*
refrain, and the rule attached to it is that **a project that only ever finds
`documented` blockers is campaigning rather than investigating.** After 175
blockers this is the first time the register has been able to say *people assert
this and it is not true* — and the field cannot carry the answer cleanly.

Minimal fix: two fields. `standing` for the truth of the claim, and something
like `effect: documented | alleged` for whether it actually blocks anything. The
four combinations are all real:

- **true and blocking** — most of the corpus
- **false and blocking** — MMR/autism; also every vaccine-hesitancy obstacle to
  come, and there are several in the queue
- **true and not blocking** — a real constraint nobody is actually hitting
- **false and not blocking** — noise, and worth being able to dismiss explicitly

## 108. `access` is linear, and some interventions have thresholds · **open**
*Forced by:* `measles`, seen once before in `copd`.

Measles has an R0 usually cited between 12 and 18, the highest in the register.
The herd immunity threshold follows as roughly 1 − 1/R0, which is about **95%**.

Below that number, transmission chains re-establish. Above it, they do not.
**Coverage of 90% is not 95% of the benefit of 95% — it is a different regime**,
and a national average of 90% concealing a 70% pocket is an outbreak living in
the pocket.

`access` is a fraction between 0 and 1 that multiplies into `reach`, and it says
the opposite: that half the coverage buys half the benefit.

COPD raised the same shape from a different direction. Cleaner-cookstove trials
repeatedly underdelivered, and the most credible explanation is that households
kept the old stove alongside the new one, so the exposure reduction achieved was
below whatever level matters. **A programme that reaches everybody halfway may be
worth less than one that reaches half of them completely** — and the register's
arithmetic prefers the first.

Two records is a pattern and the queue will add more: polio, rubella, and any
elimination programme has a threshold; malaria's insecticide-treated net coverage
has one; antibiotic stewardship arguably has one.

**Note what kind of number 95% is.** Gap #90 said the thresholds in this register
are chosen — a guideline committee moves the ASCVD risk cut-point or the
FEV1/FVC ratio and millions change category. **This one is not chosen. It is
arithmetic on the pathogen's own transmissibility**, and nobody voted on it. The
register cannot currently distinguish a threshold that is a policy from a
threshold that is a fact about the world, and they should be argued about very
differently.

## 109. Prevention has no efficacy and no access · **open**
*Forced by:* fixing #66.

`capability` now reads the prevention axis. **Nothing else does.**

`efficacy` and `access` are both defined as fractions *of patients*, and both
describe the treatment. Everything downstream inherits that:

- `reach = efficacy × access` — for measles this multiplies the mortality
  averted by vitamin A against the fraction of sick children reaching care, and
  says nothing whatever about the vaccine.
- `delivery` — now withheld for preventable records rather than reported,
  because the band would be computed from the wrong numbers.
- `orphaned` — gated on `reach` under a ceiling, so it is testing treatment
  delivery on records whose capability is entirely preventive.

**The number that matters for measles is vaccination coverage: about 83%
against a threshold of 95%.** It is the single most important figure in that
record, it is a fraction, the register is built to hold fractions, and there is
nowhere to put it.

The same hole swallows: rabies post-exposure prophylaxis coverage among people
actually bitten; benzathine penicillin adherence in rheumatic heart disease;
bed-net coverage for malaria, which is next but one in the queue; and every
vaccine record still to be written — hepatitis B, cervical cancer, typhoid,
cholera, childhood pneumonia, diarrhoeal disease.

Minimal fix: `prevention_efficacy` and `prevention_coverage` alongside the
existing pair, with `reach` computed per axis and the better of the two
reported. It also gives #108 somewhere to live — a coverage threshold is a
property of a prevention scalar, not of a treatment one.

Note this is the second time a fix has surfaced its own successor: closing #89
produced #98, and closing #66 produced this. That is the schema being pulled
forward by the corpus rather than designed ahead of it, which is the intended
direction.

## 110. The register cannot record that the patient is blamed · **open — FLAGSHIP ARRIVED 2026-08-24 (`cirrhosis`); BUILD THE RECORD-LEVEL FIELD**
*Forced by:* `lung-cancer`.

Lung cancer research funding per death sits far below breast or prostate cancer.
Patients report being asked, on diagnosis, whether they smoked. Screening is
offered less readily and accepted less readily than it would be for a disease
nobody held anyone responsible for.

**Attributed responsibility is a determinant of capability**, and every field in
this register is blind to it. `blockers` can hold *no-sponsor* and *policy*, and
neither says *because people think they brought it on themselves.*

It is not one record's problem. The queue is full of it:

| record | what the patient is held responsible for |
|---|---|
| **lung-cancer** | smoking — 80-90% attributable, and it is the whole of the stigma |
| **cirrhosis** (queued) | alcohol, and transplant eligibility is explicitly gated on it |
| **opioid-use-disorder** (queued) | the thing that is itself the disease |
| **alcohol-use-disorder** (queued) | as above |
| **obesity**, **type-2-diabetes** (queued) | diet and exercise, against strong biology |
| **hiv** (held) | historically, and it shaped two decades of the response |

Note what makes it different from **#77** (stigma is a feedback loop). Leprosy,
noma and scabies patients are *hidden* — concealment breaks the count, which
breaks the funding. Lung cancer patients are entirely visible and are **blamed**,
and the funding gap follows from the blame rather than from any missing number.
Two mechanisms, opposite in structure, and the register has no vocabulary for
either.

There is a real risk in building this and it should be stated. A field recording
*attributed responsibility* could read as the register endorsing the attribution.
It must record **that the judgement is made and what it costs**, not whether it is
correct — the same discipline `standing` applies to blocker claims, and the same
one that keeps `contested:` from taking a side on whether hEDS is real.

The cheapest version is a blocker kind. The honest version is a record-level
field, because it affects funding, screening uptake, transplant eligibility and
policy simultaneously, and filing it under one blocker would understate it.

## 111. The disease evolves under treatment, and `strata` assumes it does not · **open**
*Forced by:* `lung-cancer`.

`strata` requires `fraction:` values summing to 1 — a partition of a population
into disjoint buckets. Stroke's three strata satisfy it: a stroke is ischaemic or
haemorrhagic and stays that way.

**Lung cancer's do not, because the tumour moves between them.**

An EGFR-mutant adenocarcinoma is in the *targetable driver* stratum, on a tablet,
controlled for years. Then it acquires a resistance mutation, or bypasses the
pathway, or — and this is the part with no precedent in the register —
**transforms histologically into small cell carcinoma**, which is a different row
of the same table. Same patient, same cancer, different stratum, and **the
treatment caused the move.**

So the partition is not of patients but of *tumour states*, and the states are
traversed under selection pressure applied deliberately by the clinician.

This is not an oncology curiosity. It is the same shape wherever an intervention
selects:

| record | the intervention | what it selects for |
|---|---|---|
| **lung-cancer** | targeted therapy | resistance mutation, or a new histology |
| **amr-infection** | antibiotics | the resistant organism — the entire record |
| **tuberculosis** | incomplete therapy | MDR-TB, which its own blocker calls *manufacturing resistance* |
| **hiv** | non-suppressive therapy | resistance, which is why adherence is load-bearing |
| **h5n1** (queued forward) | antivirals | oseltamivir resistance markers |

**The register treats disease identity as static and treatment as acting on it.**
For this class, treatment acts on a population of variants and changes which one
you have — the entity in the record is not the entity in the patient a year
later.

Two consequences worth separating:

- **`strata` needs to be able to say *reachable from***, not merely *fraction of*.
  A stratum a patient enters because of the treatment is different from one they
  were diagnosed in.
- **`efficacy` measures the wrong interval.** For the driver-positive stratum
  the honest number is not "does it work" — it works in most — but *for how long
  before it stops*, which is why that stratum is `suppressive` rather than
  `curative` and why the register keeps wanting a duration where it has a
  fraction.

## 112. A window that is not always worth catching · **open**
*Forced by:* `prostate-cancer`.

Every `window` in this register carries an unstated assumption: **catching the
disease earlier is good.** Reach the stroke in ninety minutes, the noma in three
days, the infarct before the muscle dies. The only question the schema asks is
what fraction arrived in time.

Prostate cancer breaks it. Localised disease is curable and metastatic disease is
not, so the window is real, and PSA screening does reduce prostate cancer
mortality. **And somewhere between a fifth and a half of screen-detected cancers
would never have caused a symptom** — those men gain nothing and can lose
continence and sexual function permanently.

Same act, benefit for a minority, harm for a majority, and **no way to aim it at
the time.**

The derivation says the opposite out loud. `window_toll_link` fires on this
record and reports:

> *the toll is the price of missing it → `diagnosis` is the cheap lever*

**For prostate cancer the toll is the price of CATCHING it, and more diagnosis is
the problem.** That is the third false-reason flag in the corpus — after noma's
`overtreatment_risk` and COPD's `window_toll_link` — and the first where the flag
is not merely mis-explained but pointed in the wrong direction.

What the schema needs is a sign on the window: does catching it earlier help, and
in whom. The corpus already contains all three answers:

| record | catching it earlier |
|---|---|
| **stroke**, **noma**, **measles** | unambiguously good |
| **lung-cancer** | good on net — overdiagnosis is real and mortality still falls |
| **prostate-cancer** | good for a minority, harmful for the majority, unaimable |
| **thyroid cancer** (queued) | found a great deal, changed no mortality at all |

And note what makes prostate different from lung. Both overdiagnose. Lung
cancer's screen-detected cancers are mostly lethal, so the harm is a tax on a
benefit. Prostate's are mostly not, so the benefit is a rebate on a harm. **The
ratio decides whether a window is worth having, and the register records neither
number.**

## 113. `efficacy` is measured in one population and applied to another · **open**
*Forced by:* `prostate-cancer`.

Men of African ancestry have roughly twice the prostate cancer mortality of white
men, with earlier onset and more aggressive disease. **The randomised trials that
set screening policy under-enrolled them substantially**, and the guidelines
derived from those trials — the age bands, the risk-benefit arithmetic, the
recommendation to discuss rather than offer — are applied to them anyway.

The register has an `efficacy` field for every record, and **nothing anywhere
records who it was measured in.**

That is not a prostate problem. It is a property of the whole corpus:

- **Ebola's** monoclonal efficacy comes from trial arms in one outbreak, in one
  country, in one health system.
- **Marburg's** is confounded by candidate therapeutics used under protocol in a
  single Rwandan outbreak, and the record says so.
- **Lung cancer's** screening figures come from populations defined by a
  pack-year threshold somebody chose.
- **Cardiovascular** trials historically under-enrolled women; oncology trials
  under-enrol the elderly; and the large majority of trials underpinning every
  number in this register were run in high-income countries and are applied
  globally.

`src` records *where a number came from* in the sense of a citation. It does not
record **whom it came from**, and for a register whose entire purpose is to say
what is possible and for whom, that is a strange thing to be missing.

It compounds two existing gaps rather than duplicating them. **#95** says the
*numerator* is a choice — which outcome counts as working. **#90** says the
*denominator* is a choice — who counts as a patient. This says the **sample** is
a choice, and unlike the other two it is usually not a deliberate one.

Minimal fix: every `{value, units, src}` scalar gains an optional `population:`
string. It costs nothing to add, it can be filled in during the verification
pass that must happen anyway, and an empty one is itself informative.

## 114. A precursor is neither disease nor health, and the best interventions act on it · **open**
*Forced by:* `colorectal-cancer`.

An adenomatous polyp is not colorectal cancer. It is also not nothing. It takes
roughly a decade to become carcinoma, it is visible to a colonoscope for that
whole period, and **removing it is the highest-value intervention in the entire
record** — the reason colorectal screening lowers *incidence* and not merely
mortality.

The register has two states: a person has the entity or does not. There is no
third, and the third is where the leverage is.

| record | the precursor | what acting on it achieves |
|---|---|---|
| **colorectal-cancer** | adenomatous polyp | the cancer never happens |
| **cervical-cancer** (queued) | CIN 2/3 | the cancer never happens — and this is why cervical screening works |
| **h-pylori-ulcer** (held) | chronic gastritis / intestinal metaplasia | and it is upstream of gastric cancer, also queued |
| **msmds**, **crohns** (held) | — | no precursor, and that is itself informative |
| **ischaemic-heart-disease** (held) | subclinical atherosclerosis | universal with age, which is why #90 bites there |

Four consequences, and they are not cosmetic:

- **`burden` counts cases, and the programme's largest effect is cases that
  never occurred.** Colorectal's `caught_in_time` records the fraction of
  *cancers* found while curable and cannot count the polyps removed. The number
  understates the benefit by the whole of the mechanism.
- **`prevention: prophylaxis` is doing work it was not designed for.** Recorded
  here on the strength of a snare rather than a vaccine — the fifth job in the
  open half of #66.
- **Overdiagnosis nearly disappears as a concern.** Prostate's whole problem is
  that finding indolent cancer makes people cancer patients. **Nobody is turned
  into a cancer patient by having a polyp removed**, which is why the same act —
  screening — is contested for prostate and settled for colon.
- **And one act is screen, diagnosis and prevention simultaneously.**
  Colonoscopy visualises, samples and removes in ten minutes. The schema
  separates `measurement`, `prevention` and `intervention` as different kinds of
  thing, and here they are one thing done once.

The minimal move is a `precursor:` block — what it is, how long the transition
takes, whether it is detectable, and whether removing it is curative. It would
also give #112 the vocabulary it needs: **a window on a precursor is
unambiguously worth catching; a window on an indolent cancer is not.** That
distinction is the entire difference between colorectal and prostate screening,
and neither record can currently state it in a field.

## 115. Four records now need a blocker kind for *the intervention is refused*, and the reasons differ in kind · **open**
*Forced by:* `colorectal-cancer`. Named after four records asked for it.

The blocker taxonomy has twelve kinds. **None of them is: the intervention
exists, is available, and the people it is offered to will not take it.**

Four records have now needed it and — this is why it is one gap rather than four
strengthenings — **the reasons are different in kind, and the response to each is
different:**

| record | why it is refused | what would change it |
|---|---|---|
| **ebola** | the response arrived with an armed escort into a place with a history of extraction and violence | trust, built slowly, by people from there |
| **h5n1** | farm workers cannot afford to be the ones who report it — no sick pay, sometimes no immigration status | pay them, and protect them |
| **measles** | a refuted belief that the vaccine causes autism | not more information; that has been tried |
| **colorectal-cancer** | the test involves stool, or a scope, and people find it degrading | a different test — blood-based, non-invasive |

Filed variously as `policy` and `adherence`, and neither fits. **`adherence` means
a patient continuing a therapy they started**; three of these people never
started. `policy` means legislation and it is what Ebola's Kivu blocker was
labelled for want of anywhere better.

The four reasons are: **distrust**, **exposure to consequences**, **false
belief**, and **unacceptability**. They call for reparation, protection,
something other than argument, and product redesign respectively — which is why
collapsing them into one word would be almost as bad as having no word.

It matters more than a taxonomy tidy-up because of what it is blocking. In every
one of these four records the science is finished and the product exists. **This
is the largest category of undelivered capability in the register that is not
about money**, and the register cannot name it.

Note also that it interacts with #107: measles' entry is a *refuted claim* that
is a *documented obstacle*, and the taxonomy would need to carry both.

## 116. Somebody has already defined "solved" numerically, for one disease · **open, and it is about this register rather than about medicine**
*Forced by:* `cervical-cancer`.

Nordstern exists because **nobody has a definition of solved.** That is the
founding claim, and for cervical cancer it is not true.

WHO's elimination initiative sets, by 2030:

| | target |
|---|---|
| **90** | of girls fully vaccinated against HPV by age 15 |
| **70** | of women screened twice in a lifetime with a high-performance test |
| **90** | of women with disease treated |
| **< 4 per 100,000 women-years** | the threshold at which the disease counts as eliminated as a public health problem |

That is a dated, quantified, publicly agreed definition of solved for one entity,
with the coverage fractions that get you there — **which is the artefact this
project is trying to build in general.** The register neither uses it, cites it,
nor explains why not.

Three things follow, and none of them is comfortable:

- **It is the worked example #109 asked for.** That gap said prevention has no
  efficacy and no coverage field, and that measles' 83%-against-95% has nowhere
  to go. Here are three prevention coverage fractions, already agreed, already
  measured annually, already reported by country. The field the register needs is
  not hypothetical; it exists in somebody else's spreadsheet.
- **It is #108's threshold with a source.** *Fewer than four per 100,000* is a
  chosen number rather than one arithmetic on the pathogen forces, unlike
  measles' 95%. Both kinds exist, both matter, and the register can record
  neither.
- **The founding claim needs qualifying.** Nobody has a *general* definition of
  solved — that part holds. But per-disease elimination targets exist for
  cervical cancer, for the guinea worm, for several NTDs, and for polio, and they
  are the closest thing to prior art this project has. **A register that borrows
  MONDO's identifiers rather than minting its own should be asking the same
  question about these.**

The honest options are to adopt them where they exist, or to state clearly why a
cross-disease register needs a different instrument from a per-disease campaign
target. Not to leave the best existing answer uncited.

## 117. The toll can land on a person who does not exist yet · **open**
*Forced by:* `cervical-cancer`.

Excising a high-grade cervical lesion — LEEP, or a cone biopsy — removes part of
the cervix and **raises the risk of preterm birth in a subsequent pregnancy**,
with the risk increasing with the depth of tissue taken.

Roughly half of CIN2 in young women regresses without any treatment, and nobody
can say which half.

So: a proportion of these women are being made more likely to have a premature
baby, in order to prevent a cancer that was not coming. **The harm is real, it is
caused by the intervention, and the person who pays it has not been conceived.**

`toll` records what the cure costs *the patient*. Every field in this register is
scoped to one living person (gaps.md #100), and this is that gap pointing forward
in time rather than sideways to another patient.

It is not rare once looked for:

| record | the intervention | who pays |
|---|---|---|
| **cervical-cancer** | excision of a precursor | a future pregnancy |
| **epilepsy** (held) | sodium valproate, which works | a fetus — malformation and neurodevelopmental harm |
| **lung-cancer**, **cervical-cancer** | pelvic or systemic cytotoxic therapy | fertility, ended |
| **hiv** (held) | historically, some regimens in pregnancy | the infant |
| germline editing (not in the corpus) | — | every descendant |

The register can already record that a treatment ends fertility, because that
happens to the patient. It cannot record that a treatment leaves the patient
fertile and **damages the child she goes on to have.**

Note the interaction with #114. This is a *precursor* treatment, given to
someone who does not have the disease, to prevent something that in half of them
was not coming — so the harm falls on the wrong side of three separate lines at
once: not the patient, not the disease, and not yet existing.

## 118. Some ratings require a future that has not happened · **open**
*Forced by:* `melanoma`.

Metastatic melanoma on combination checkpoint blockade has roughly fifty percent
five-year survival, against under a tenth before 2011. **And the survival curve
flattens.** People stop progressing and stay stopped, a proportion of them years
after stopping treatment.

A flat tail is what a cure looks like from inside. It is also what a very long
suppression looks like from inside. **The difference only becomes visible with
time this treatment has not yet had**, and the ladder has a separate rung for
each:

| rung | meaning |
|---|---|
| `suppressive` | near-normal life, **indefinitely treated** |
| `curative` | a **finite** intervention ends it |

The record reads `suppressive` for that stratum, on the conservative choice, and
**the choice is arbitrary.** Nothing in the data settles it and nothing will for
another decade.

This is not #91. That gap says the register records a position rather than a
trajectory — a problem about the past. This one says **the present rating is not
knowable in the present**, and no amount of recording history fixes it.

The corpus is already full of it and the queue is worse:

| record | the claim | how long until it is settled |
|---|---|---|
| **melanoma** | the plateau is cure | a decade, maybe two |
| **sickle-cell** (held, rated `curative` in 2023) | gene therapy is a cure | the first patients are ~a decade out |
| **hepatitis-c** (held) | SVR is cure | settled — and it took fifteen years to be sure |
| **cervical-cancer** (held) | HPV vaccination prevents invasive cancer | the vaccinated cohorts are only now reaching the relevant ages |
| **cml** (queued) | treatment-free remission | actively being tested by stopping the drug |
| CAR-T, gene therapy generally (queued) | — | unsettled by construction |

Hepatitis C is the encouraging case: the claim was eventually settled and the
answer was yes. It is also the warning, because for fifteen years the honest
rating and the eventual rating were different, and a register taking an annual
bearing would have recorded the wrong one every year until it did not.

The minimal move is a **confidence or maturity marker on the rating itself** —
distinct from `src`, which describes where a number came from, and from
`standing`, which describes a blocker claim. Something that says *this rating
depends on follow-up that does not exist yet.* Strangschrift already carries a
confidence label for the same reason and for the same kind of honesty.

## 119. A diagnostic threshold can drift with no number, no committee and no announcement · **open**
*Forced by:* `melanoma`.

Melanoma incidence has risen steeply across several high-income countries for
decades while **mortality stayed roughly flat.** That is the overdiagnosis
signature, and a substantial part of the gap is not more disease and not more
looking. It is **pathologists calling lesions melanoma that would once have been
called atypical naevi.**

Reproducibility for borderline melanocytic lesions is poor — pathologists
disagree with one another and, on re-reading, with themselves — and the boundary
has moved in one direction.

Gap **#90** already says the thresholds in this register are chosen: ASCVD risk
cut-points, FEV1/FVC below 0.70, a pack-year eligibility band, a screening age
moved from fifty to forty-five. Every one of those is **a number, set by a named
committee, on a stated date.** The register cannot record them, and at least a
reader could go and look them up.

**This threshold has none of those properties.** There is no number to record, no
committee to name, and no date on which it changed. It drifted, inside
microscopes, across a profession, over decades — and the consequence is that a
country's melanoma incidence figure is partly a measurement of its pathologists.

That makes it worse than #90 rather than a variation on it:

- **It is invisible.** A guideline change leaves a paper trail; this leaves an
  incidence curve that looks like an epidemic.
- **It is self-reinforcing.** More melanoma diagnosed means better apparent
  survival — the added lesions were never going to kill anyone — which is taken
  as evidence that finding more of them works.
- **It cannot be corrected retrospectively**, because the historical slides were
  read under the old threshold and the modern comparison does not exist.

Where else does the corpus depend on a qualitative judgement that could move
without announcement? **Every `diagnostic: clinical` record** — noma, smallpox,
rabies, epilepsy, bipolar, depression — and every histological grade in the
cancer records. Prostate cancer's Gleason grading has been formally revised, at
least, which is #90's kind of change. Melanoma's has not.

## 120. The register records that a rating changed, never how · **open, and it is the project's own question**
*Forced by:* `childhood-all`.

Childhood acute lymphoblastic leukaemia was uniformly fatal in 1948 and is cured
in roughly nine children in ten now. It is the largest capability change in this
register, and **there was no breakthrough.**

Almost every drug in the modern protocol predates 1980 and is generic. What
produced the cure was: combination chemotherapy, prophylaxis of a sanctuary site
in patients with no disease in it, risk stratification, and **fifty years of
successive cooperative-group randomised trials in which a majority of affected
children were enrolled** — each testing one modification, each adding a few
percentage points, each generation's standard arm being the last generation's
experimental one.

`moved` records that the rating changed and when. **Nothing records how**, and
the how is different in kind between records that look identical in the field:

| record | the same `moved` shape | what actually happened |
|---|---|---|
| **childhood-all** | intervention: none → curative | **iteration** — 50 years of trials, no new drug |
| **hepatitis-c** | disease-modifying → curative | **discovery** — a new drug class, fast |
| **melanoma** | efficacy 0.65 → 0.80 | **discovery** — checkpoint blockade |
| **prostate-cancer** | toll 0.85 → 0.45 | **measurement** — nothing new to give, better sorting |
| **childhood-all** | efficacy 0.7 → 0.9 | **measurement** — MRD, same backbone |
| **cervical-cancer**, **colorectal-cancer** | access ↑ | **delivery** — old tools, more people |
| **yaws** | access 0.9 → 0.2 | **abandonment** — a campaign wound down |

Those are at least five different mechanisms of progress, and **a register built
to answer "what should we work on next" cannot distinguish between them.** If the
answer to how ALL was solved is *run trials for fifty years*, that is a
completely different instruction from *find a drug*, and both are recorded as an
arrow between two enum values.

This matters more here than in most gaps because of what the project says it is
for. **fndtn's stated goal is to build the process that solves medicine.
Childhood ALL is a process that solved a disease** — the most complete example
available — and the register can describe the before, the after, and nothing in
between.

Minimal fix: `moved` gains a `how:` with a closed vocabulary — `discovery`,
`iteration`, `measurement`, `delivery`, `policy`, `abandonment`. Cheap, and it
makes the corpus answerable to the question *which kinds of effort have actually
moved things.*

## 121. The toll's latency exceeds the follow-up that declared the cure · **open**
*Forced by:* `childhood-all`.

A child cured of leukaemia at five is counted as a success at ten. **The
anthracycline cardiomyopathy arrives in their thirties.** The second cancer, the
endocrine failure, the cognitive consequences of cranial irradiation, the
osteonecrosis needing a hip replaced at twenty-five — all of it lands decades
after the survival statistic was recorded.

Around two thirds of childhood cancer survivors carry at least one chronic
health condition by their forties; roughly a quarter carry a severe or
life-threatening one.

**The success metric is five-year survival and the harm metric is a lifetime**,
and the register reports both as present-tense fields of equal standing.

Two consequences, and the second is worse:

- **The toll figure in this record describes a cure delivered thirty years ago.**
  It comes from survivorship cohorts of people treated with far more cranial
  irradiation and anthracycline than a child receives today. The price of a cure
  delivered *now* is unknown and will be for thirty more years. The register
  states a number that is simultaneously the best available and certainly wrong
  for the current cohort.
- **De-escalation — the main work in the largest stratum — is unmeasurable on
  any relevant timescale.** Giving less anthracycline is worth doing precisely
  because of harms that will not be observable for decades, which means the
  evidence for the most important current activity in childhood oncology cannot
  exist yet.

It is #118's problem with the sign reversed. There, the *benefit* is not yet
knowable and the register must rate anyway. Here the benefit was declared long
ago and **the cost is still arriving.** Both say the rating's timescale does not
match the phenomenon's; only this one has already produced a number people quote.

It generalises to everything given young or given once: HPV vaccination, gene
therapy, CAR-T, paediatric surgery, and every "cure" whose recipients are still
in their forties.

## 122. `access` records whether you reached care, not whether you reached the right care · **open**
*Forced by:* `childhood-all`.

Cure rates in ALL fall steeply through adolescence into adulthood. A substantial
part of that gradient is not biology: **adolescents and young adults do
materially better on paediatric protocols than on adult ones.** Same disease,
same age, different department, different result.

Which department admits a nineteen-year-old is a matter of local referral custom
and where an institutional age boundary happens to sit.

`access` is defined as *the fraction of patients who can get* the best
intervention. It is a binary about arrival. It cannot say that a patient arrived,
was treated, and **received a version of the treatment known to be worse.**

The corpus is full of it once named:

| record | reached care | and got |
|---|---|---|
| **childhood-all** | a hospital | an adult protocol, at nineteen |
| **stroke** | a hospital | one without a stroke unit or a cath lab |
| **prostate-cancer** | a urologist | surgery, where surveillance was indicated |
| **copd** | a GP | a diagnosis made without spirometry |
| **cervical-cancer** | a cancer centre | chemoradiation without brachytherapy, which materially worsens survival |

**Every one of those is a treated patient counted as reached.** `reach = efficacy
× access` therefore overstates delivery systematically, and by an amount nobody
has estimated.

It is not #113 (`efficacy` measured in one population, applied to another) —
that is about whom the evidence came from. This is about what the patient in
front of you actually received. And unlike most gaps here, **the fix is usually a
referral pathway rather than a discovery**, which makes it among the cheapest
things in the register to act on and the hardest to see.

## 123. The ladder is ordered by finality, not by value · **open**
*Forced by:* `cml`.

The intervention ladder puts `curative` above `suppressive`, on the reasoning
that a finite intervention ending a disease beats indefinite treatment. That is
usually right.

**In 2001 it was wrong, and the whole of chronic myeloid leukaemia is the proof.**

Before imatinib, CML had a cure: allogeneic stem cell transplant. It was
available to a minority with a donor and the fitness to survive it, it cured
perhaps half of those, and **it killed a substantial fraction outright.**

Imatinib is `suppressive`. Stop it and most patients relapse. It made the
curative option obsolete for almost everybody, and it was unambiguously the
largest advance in the disease's history.

So the record's `moved` entry reads `disease-modifying → suppressive`, and by the
ladder's own ordering the best available option went **down** a rung at the
moment the disease was transformed.

The corpus already contains the pattern:

| record | the curative option | the lower rung that beat it |
|---|---|---|
| **cml** | allogeneic transplant — cures ~half, kills a fraction | a daily tablet, near-normal lifespan |
| **sickle-cell** | gene therapy and transplant — curative, brutal, scarce | hydroxyurea, cheap, `disease-modifying` |
| **prostate-cancer** | radical prostatectomy | **active surveillance — no treatment at all** |
| **colorectal-cancer** | resection for rectal cancer | watch-and-wait after complete response |

The ladder is a good instrument for what it measures — **does the intervention
end the disease** — and it is being read as though it measured *how good the
intervention is*. Those come apart whenever the cure is dangerous or scarce, and
the register's own `toll`, `ongoing` and `access` fields exist precisely because
they come apart often.

The fix is not to reorder the ladder. It is that **`capability` must never be
read alone**, which the register says in prose and contradicts in every table
that sorts by it. `check.py` sorts records with `capability != "curable"` first;
`index.md` leads with the word. A record like CML — `managed`, `clean`,
`restored`, near-normal lifespan — ranks below records where the cure maims.

## 124. A cure is a one-time sale and a suppression is an annuity · **open**
*Forced by:* `cml`.

**Because imatinib works, patients stop dying, so the prevalent population climbs
every year at constant incidence.** CML's incidence has not changed since 2001
and the number of people taking a tyrosine kinase inhibitor grows continuously
and will for decades.

The drug's price rose over its patented life while that was happening. In 2013
roughly a hundred CML specialists published a joint objection to it.

That is not a story about one company. It is a structural property of the
`suppressive` rung, and the register's `cost` blocker cannot see it:

| rung | the commercial object | what the incentive is |
|---|---|---|
| `curative` | **a single sale per patient**, ever | price the whole course; the market shrinks as you succeed |
| `suppressive` | **an annuity**, for decades | the market grows as you succeed |
| `preventable` | a sale to people who are well | the benefit is invisible and the payer is a government |

Every one of those distorts differently and the corpus has all three:

- **hepatitis-c** — a cure, priced as a whole course, and the pricing argument
  that followed was about exactly that arithmetic. **Curing patients removes them
  from the market**, which is a sentence nobody should have to write.
- **cml** — a suppression whose market grows because it works.
- **marburg**, **ebola (Sudan)** — no market at all, so no product (gaps.md #99).
- **measles**, **cervical-cancer** — prevention, where the payer is a health
  ministry and the benefit accrues to a government twenty years later.

The register records `cost` as a number and `no-sponsor` as a fact. **It has no
way to record that the *shape* of the intervention determines whether anybody
wants to make it**, which is upstream of both and explains several records that
currently look like unrelated failures.

Note this is the other half of Engpass's `donation-dependency`. That obstacle
records five diseases whose supply rests on a corporate decision. This records
why the decision goes the way it does.

## 125. `residual: true` marks a category error and then permits every rating anyway · **open — partly fixed**
*Forced by:* `non-hodgkin-lymphoma`.

"Non-Hodgkin lymphoma" means *the lymphomas that are not Hodgkin's*. It is a
leftover. The WHO classification recognises somewhere between sixty and a hundred
distinct diseases inside it, and they differ in cell of origin, in genetics, in
natural history, and in whether they can be cured at all.

The schema has a field for exactly this — `residual: true`, *"an idiopathic or
non-specific bucket"* — and it is the third record in fifty-seven to set it,
after low back pain and MCAS.

**And the flag does nothing.** It is stored, it is exported, it is queryable, and
**no derivation reads it and no check tests it.** The record then produces
`efficacy: 0.55`, `mechanism: established` and `capability: curable` exactly as
if it described one disease.

Every one of those is false in a specific way:

- **`mechanism: established`** aggregates six unrelated causal chains — a *BCL2*
  translocation, a *MYC* translocation, cyclin D1, cell-of-origin subtypes, and
  chronic bacterial antigenic stimulation. Rating them as one says nothing.
- **`efficacy: 0.55`** averages diseases whose individual figures run from about
  0.30 to about 0.85. It describes nobody.
- **`capability: curable`** is true of the largest stratum and false of the
  second largest, which is `suppressive` and genuinely incurable.

The schema already understands this pattern elsewhere: `kind: complaint` exists
because *rating the mechanism of a complaint is a category error, and marking the
kind is what stops the register from quietly committing one.* **`residual` was
given the same job and none of the enforcement.**

**Partly fixed:** `check.py` now emits residual records in its own section and
warns that their record-level scalars are averages over a bucket, so the flag is
at least visible rather than merely stored. What is still open is the harder
question — whether a residual record should be **forbidden** from carrying
record-level `efficacy` and `mechanism` at all, and required to carry strata
instead. That is a real design decision: it would make NHL, low back pain and
MCAS structurally different from every other record, and it might be correct.

## 126. A diagnostic disagreement can move a patient between strata with different capability · **open**
*Forced by:* `non-hodgkin-lymphoma`.

In lymphoma the subtype **is** the treatment decision:

| subtype | what happens |
|---|---|
| diffuse large B-cell | six cycles of immunochemotherapy, **curative intent** |
| follicular, asymptomatic | **watched. No treatment at all.** |
| gastric MALT | **antibiotics** |
| T-cell | borrowed regimens, poor outcomes |

And the subtype is a haematopathologist's judgement across morphology,
immunophenotype and genetics. **Expert review changes the diagnosis in a
meaningful share of referred cases**, particularly at the borders — follicular
grade 3B against DLBCL, mantle cell against the other small B-cell lymphomas,
and across the T-cell entities where morphology helps least.

Melanoma's **#119** was a threshold drifting: the boundary between naevus and
melanoma moved, and the consequence was over-diagnosis of one disease.

**This is worse in kind.** The categories a disagreement moves a patient between
have **different rows in the `strata` block and different capability ratings** —
`curable`, `managed`, `partial`. A misclassification here does not over- or
under-treat one disease. It assigns the patient to a different disease, with a
different answer to *is it solved*.

The register's `strata` block assumes membership is a fact. For NHL it is a
reading, and the reading is wrong often enough to matter.

Where else does this hold in the corpus?

- **stroke** — ischaemic against haemorrhagic is a CT scan, and it is not in
  doubt. The best case.
- **lung-cancer** — small cell against non-small cell is a real pathological
  judgement with genuinely different capability, and it is less contested than
  lymphoma's.
- **melanoma** — one threshold, one disease, drifting.
- **mcas**, **heds**, **pots** — the categories themselves are contested, which
  is a third thing again and is what `contested:` records.

The minimal move is a confidence on stratum assignment, or a note that the
partition is a reading rather than a fact. The larger point is that **`strata`
inherits all of `diagnostic`'s uncertainty and reports none of it.**

## 127. The disease and its host organ can fail together, and no field holds the organ · **open**
*Forced by:* `liver-cancer`.

Almost all hepatocellular carcinoma arises in a cirrhotic liver, and **every
treatment decision depends on how much liver function is left.** Resection takes
liver away from someone who has none to spare. Chemoembolisation deliberately
infarcts part of it. Systemic therapy is metabolised by it, and checkpoint
blockade can inflame it.

BCLC is the only staging system in oncology that stages **the organ alongside the
tumour**, and its worst stage — BCLC D — is defined by the liver rather than by
the cancer. **Fifteen percent of diagnoses are untreatable because of a different
disease**, and some of them have tumours that would be curable in a working
liver.

Three separate things the register cannot say:

- **The treatment and the host organ are in direct competition.** No other record
  has this. Everywhere else the patient is a background against which the disease
  happens; here the background is the co-star.
- **Curing the tumour does not cure the field.** Recurrence after resection or
  ablation approaches seventy percent at five years and much of it is *new
  primary* disease, because the whole organ is premalignant. `residue` means what
  the disease left behind; this is **what was there before and still is**, and
  the only treatment that removes it is replacing the organ.
- **The comorbidity is itself a queued record.** Cirrhosis is on the list.
  Hepatitis B is on the list. When they are written, the register will hold four
  rows describing one causal chain with no way to connect them.

It generalises immediately once named, and the corpus already contains it:

| record | the cancer | the organ already failing |
|---|---|---|
| **liver-cancer** | HCC | cirrhosis — and it is 15% of diagnoses untreatable |
| **lung-cancer** | NSCLC | COPD, from the same exposure; the record says so in `toll` |
| **childhood-all** | ALL | none — and that is why the cure rate is 90% |
| kidney cancer, CKD (queued) | — | dialysis-dependent patients |

**Comorbidity determines capability**, and there is no field for it — not in the
axes, not in `strata`, not in `toll`. The nearest available move is a
`comorbidity:` block naming the entity and what it forecloses, which would also
give #100's relations somewhere concrete to start.

## 128. Some capability is zero-sum, and `access` cannot say so · **open**
*Forced by:* `liver-cancer`.

Transplantation is the only treatment that addresses both the cancer and the
liver it grew in. It is also, uniquely in this register, **capped by a supply
that cannot be increased with money.**

Every other access constraint here is in principle relievable. Build factories,
train endoscopists, buy brachytherapy machines, let the patent expire, pay for
the cold chain. **A liver given to one patient is a liver another patient does
not receive.**

`access` is defined as *the fraction of patients who can get the best
intervention*, and it silently assumes the intervention is reproducible. For a
zero-sum resource the fraction is not a delivery failure to be fixed — it is an
allocation rule, and raising one patient's access necessarily lowers another's.

That changes what the register's own output means. `orphaned` means *science
done, nobody carrying it*; for transplant the science is done, somebody is
carrying it, and there is nothing more to carry. **A blocker with `scale:
3.0e9` implies that money would fix it. Here money buys allocation systems and
opt-out legislation and living-donor programmes, all of which help at the
margin, and none of which makes another liver.**

The corpus has more of this than it looks:

| resource | why it is capped |
|---|---|
| **solid organs** (liver-cancer; CKD and cirrhosis queued) | donation, and a donor must die |
| **blood products** (childhood-all's induction deaths; NHL's CAR-T) | donation |
| **ICU beds in a surge** (covid-19 queued) | staffed capacity, not equipment |
| **specialist attention** (NHL haematopathology; #122's paediatric protocols) | trained humans, made slowly |

The last one is the most interesting because it looks fixable and behaves like a
scarce resource on any timescale shorter than a training programme.

Minimal move: a flag on a blocker marking the constraint as **rationed rather
than under-supplied**, so that `scale` stops implying purchasability and the
`orphaned` derivation stops firing on records where nobody is failing to carry
anything.

## 129. Prevention can be unintentional, and the largest examples are · **open**
*Forced by:* `gastric-cancer`.

Gastric cancer incidence has been falling across the developed world since
roughly the 1930s — decades before *Helicobacter pylori* was discovered, and long
before anybody could have intended it.

The leading explanation is **domestic refrigeration**, replacing salting and
smoking as the way food is preserved, together with falling *H. pylori*
transmission as sanitation improved and households became less crowded.

**Nobody did any of that to prevent cancer.** It is plausibly the largest cancer
prevention in human history and it has no programme, no ministry, no trial and
no budget line.

The register's `prevention` axis records deliberate acts — a vaccine, a
prophylactic drug, a screening programme, a behaviour change campaign. It has no
way to record that the disease receded because the world changed.

Once named, it is most of how mortality actually improved:

| record | the deliberate intervention | the undeliberate one that did more |
|---|---|---|
| **gastric-cancer** | *H. pylori* eradication, 2013 onward | **the refrigerator**, from the 1930s |
| **tuberculosis** (held) | BCG, then chemotherapy from 1946 | housing, nutrition and crowding — mortality was already collapsing |
| **h-pylori-ulcer** (held) | triple therapy | sanitation reducing childhood acquisition |
| **diarrhoeal-disease** (queued) | ORS, rotavirus vaccine | piped water and sewers |
| **noma** (held) | nothing | **it disappeared from Europe with nutrition, and nobody was aiming at it** |
| **rheumatic-heart-disease** (held) | benzathine penicillin | crowding, again |

This is the McKeown argument, and the register should not have to relearn it one
record at a time. **It matters for what the project claims to be building**: if
the largest historical reductions in disease came from things done for other
reasons, then a register of medical capability is measuring a minority of the
mechanism.

It is also the mirror of #87. That gap says a deliberate intervention's benefits
spill across entities and cannot be charged to any of them. **This says the
benefit may not have come from an intervention at all.**

Minimal move: `prevention` gains a way to record an undeliberate or structural
contribution — with the honest caveat that attribution here is inference from
time trends rather than measurement, and the record says so.

## 130. An intervention's harm can land in a different entity · **open**
*Forced by:* `gastric-cancer`.

Eradicating *Helicobacter pylori* to prevent gastric cancer means **giving
antibiotics to roughly half of humanity to prevent cancer in one or two percent
of them.**

The benefit is demonstrated in high-incidence populations. One of the costs is
**antimicrobial resistance** — clarithromycin resistance in *H. pylori* is
already the main reason first-line regimens fail, and population-scale use would
accelerate it across every organism exposed.

That cost lands in `amr-infection`, **which is a record in this register**, and
nothing can say so.

`toll` records what an intervention costs *the patient*. There is no field for
what it costs *another disease*, and the corpus keeps producing instances:

| the intervention | the entity that pays |
|---|---|
| **gastric-cancer**: mass *H. pylori* eradication | **amr-infection** |
| **tuberculosis**: incomplete therapy | MDR-TB, which its own blocker calls *manufacturing resistance* |
| **smallpox**: ending routine vaccination | mpox, via lost orthopox immunity (#106) |
| **stroke**: anticoagulation for atrial fibrillation | intracerebral haemorrhage — **a stratum of the same record** |
| **non-hodgkin-lymphoma**: anti-CD20 antibodies | hepatitis B reactivation |

Note the difference from #106. That gap is about **winning** removing a
capability — a consequence of success. This is about **the intervention itself**
having a cost that is paid somewhere the record cannot see, whether it succeeds
or not.

And it is the exact inverse of #87, which the corpus has now stated eight times:
a tobacco tax prevents four diseases and is chargeable to none. **A course of
antibiotics prevents one disease and damages another, and is debitable to none.**
Benefits and harms both cross entity boundaries and the register is blind in both
directions.

**It changes a policy question the record cannot currently pose.** Japan decided
mass eradication was worth it and treats it as cancer policy. Most countries have
not decided, and the undecided position is a choice being made every year — one
that requires weighing a cancer against a resistance burden, in two different
rows, with no shared unit.

## 131. Nobody knows whether this window exists · **open**
*Forced by:* `pancreatic-cancer`.

Every `window` record in this corpus rests on an assumption so basic it is never
stated: **the disease is local before it is systemic, so catching it earlier
catches less disease.**

Prostate cancer showed the assumption can be *harmful* — catching an indolent
cancer makes somebody a patient for nothing (#112).

**Pancreatic cancer shows it can be unknown.**

Sequencing and modelling work suggests PDAC acquires metastatic capacity very
early — that cells able to seed the liver and peritoneum leave before the primary
is large enough to find, and that a share of patients with apparently localised
disease already carry micrometastases. If that is substantially right, then
earlier detection buys **lead time rather than life**, and the survival gain from
finding smaller tumours is partly an artefact of starting the clock sooner.

Nobody knows how large the effect is. It is a live scientific question, it is why
population screening is not recommended even setting cost aside, and it is why
high-risk surveillance is studied rather than assumed.

So the corpus now holds three answers to one question, and records
`has_window: true` for all three:

| record | catching it earlier |
|---|---|
| **colorectal-cancer** | unambiguously good — the target is a precursor, so the cancer never happens |
| **prostate-cancer** | harmful for the majority, and unaimable |
| **pancreatic-cancer** | **unknown, and the uncertainty is the reason nothing is being rolled out** |

#112 asked for a **sign** on the window — does catching it earlier help, and in
whom. This asks for something the register has avoided everywhere: **a confidence
on the claim itself.** `caught_in_time: 0.20` here is a precise-looking number
attached to a proposition that may not hold, and the field gives no way to say so.

It is the same shape as #118 (a rating that needs a future that has not happened)
pointed at a different field. There the uncertainty was about *durability of
benefit*; here it is about *whether the benefit exists at all*. **Both are cases
where the honest entry is a number plus a warning, and the schema accepts only
the number.**

## 132. The earliest sign of one entity can be the onset of another · **open**
*Forced by:* `pancreatic-cancer`.

**Roughly one percent of people over fifty who develop new diabetes turn out to
have pancreatic cancer**, and the tumour appears to cause the diabetes months
before it is visible on any scan.

That is a large enrichment in a population that presents itself to primary care
without being sought. For a cancer with no screening test and no definable
pre-clinical population, it is the best available handle there is — and it is
being actively pursued as an early-detection strategy.

**The register cannot record it.** `measurement.diagnostic` describes how *this*
disease is detected. There is no field for *the disease that heralds it*, and
the herald here is a separate entity — two of them, queued as type 1 and type 2
diabetes.

Once named, the corpus has more:

| the herald | the entity it announces |
|---|---|
| **new-onset diabetes over 50** | **pancreatic-cancer**, months before imaging |
| migratory thrombophlebitis | pancreatic and other adenocarcinomas — described in 1865 |
| **iron-deficiency anaemia in an older adult** | **colorectal-cancer**, and it is already a referral criterion |
| **atrial fibrillation** (queued) | thyrotoxicosis, and it is routinely tested for |
| new-onset **epilepsy** (held) in an adult | brain tumour, and it triggers imaging |
| **h-pylori-ulcer** (held) presentation | occasionally the first sign of **gastric-cancer** |

Some of these are already codified as referral rules in clinical practice —
which is exactly the point. **The knowledge exists in guidelines and not in the
register**, and a register meant to say where measurement would pay cannot see
one of the few places it demonstrably does.

Note the relationship to #130, which this completes. That gap says **an
intervention's harm can land in another entity.** This says **a disease's signal
can appear in another entity.** Together with #87's benefits and #55's unbuilt
relations, four gaps now describe things crossing the boundary between rows, and
the register is blind in every direction.

## 133. A disease definition is an instrument, and this register treats it as data · **open**
*Forced by:* `thyroid-cancer`.

**In 2016 a cancer was deliberately un-named.**

The encapsulated follicular variant of papillary thyroid carcinoma was
reclassified as **NIFTP** — *noninvasive follicular thyroid neoplasm with
papillary-like nuclear features* — and the word *carcinoma* was removed on
purpose, by a working group, published, **explicitly so that people would stop
being treated for it.**

Tens of thousands of diagnoses a year moved out of the disease. No biology
changed. No treatment changed. **The definition was used as a therapeutic
intervention and it worked.**

Nordstern's founding rule is that **disease identifiers are borrowed, never
minted** — MONDO already enumerates the entities, so the register takes them and
adds a rating. That rule is right and it carries an assumption it never states:
**that the enumeration is a description of the world rather than a lever on it.**

The corpus is now full of counterexamples:

| record | the definitional act | the effect |
|---|---|---|
| **thyroid-cancer** | NIFTP renaming, 2016 | tens of thousands a year cease to have cancer |
| **prostate-cancer** | live argument that Gleason 6 should not be called cancer | would do the same again |
| **copd** | FEV1/FVC < 0.70, a fixed ratio with a known age bias | decides who has the disease at all (#90) |
| **hypertension** (queued) | 140/90 → 130/80 in one guideline and not another | reclassified a large share of adults overnight |
| **melanoma** | a threshold that drifted without announcement | manufactured an epidemic (#119) |
| **non-hodgkin-lymphoma** | an entity defined by what it is not | sixty diseases in one row (#125) |

This is **#90 and #119 pointed one level up.** Those gaps say a *threshold inside*
a disease is chosen and can drift. This says **the boundary of the entity is
itself an act**, sometimes deliberate, sometimes announced, and occasionally the
single most effective intervention available.

Two consequences the register should face:

- **A borrowed identifier inherits somebody else's decisions**, including their
  timing. If MONDO splits, merges or retires a term, the register's row changes
  meaning and the append-only machinery records only that the identifier moved.
- **The register cannot recommend a definitional change**, which for thyroid
  cancer was the highest-value action available and for prostate cancer may be.
  *Rename it* is not in the vocabulary of blockers, and it should be.

## 134. The diagnosis is itself a harm, and `toll` only counts treatment · **open**
*Forced by:* `thyroid-cancer`.

A person with a papillary microcarcinoma managed correctly — active surveillance,
no surgery, no radioiodine, no levothyroxine — has received **no treatment at
all**, and is a cancer patient for the rest of their life.

That costs them: insurance and mortgage terms, employment decisions, the
psychological weight of a diagnosis, periodic scans and the anticipation before
each one, and an identity they did not have last week. **None of it is inflicted
by an intervention**, so `toll` — *what the cure costs* — records nothing, and
`ongoing` — *the cost of being treated* — records nothing either, because they
are not being treated.

**This is the entire harm of overdiagnosis in the patients who are then correctly
left alone**, and the register is blind to exactly the group the overdiagnosis
literature exists to protect.

#105 asked for `toll` to gain a scope, and named three: treatment, prevention,
and diagnosis. **The diagnostic one it named was physical** — colonoscopy
perforating a bowel, a biopsy causing pneumothorax after a false-positive CT.
This is a fourth thing again: **the label, with no procedure attached.**

Where it bites in the existing corpus:

| record | who carries a diagnosis without treatment | what it costs them |
|---|---|---|
| **thyroid-cancer** | microcarcinoma on active surveillance | insurance, employment, identity, scan anxiety |
| **prostate-cancer** | ~40% of diagnoses, on surveillance | the same, plus repeat biopsies |
| **h5n1**, **huntington** | pre-symptomatic gene carriers | Huntington's is the extreme — decades of knowing |
| **heds**, **mcas**, **pots** | contested diagnoses | and here the label is also *sought*, which cuts both ways |
| **colorectal-cancer**, **cervical-cancer** | people with precursors removed | almost none — **and that is why those screens are good** |

That last row is the point. **The reason colorectal screening is unambiguously
worth it and thyroid screening is not is partly that nobody is made a cancer
patient by having a polyp removed.** The register credits the difference to
overdiagnosis rates and cannot name the mechanism.

Minimal move: `toll` gains the scope #105 asked for, with a fourth value —
*diagnosis, without intervention* — so that a record can say what being told
costs, separately from what being treated costs.

## 135. `mechanism` rates why the disease happens, never why the treatment works · **open**
*Forced by:* `bladder-cancer`.

Bacillus Calmette-Guérin — live attenuated *Mycobacterium bovis*, the
tuberculosis vaccine — has been instilled into bladders since 1976. It reduces
recurrence and progression in high-risk non-muscle-invasive disease and it
predates every checkpoint inhibitor by four decades.

**Nobody fully knows why it works.**

The account is mycobacterial attachment to urothelium, cytokine release,
granulocyte and T cell recruitment, trained innate immunity. After fifty years it
remains a description rather than a mechanism.

The record still rates `mechanism: established`, and correctly — the *disease*
mechanism is excellent. Carcinogens are excreted in urine and held against the
urothelium; *FGFR3*-mutant papillary tumours recur and rarely invade;
*TP53*-mutant flat lesions invade. **The axis is answering a different question
from the one that matters here.**

The quadrant cannot rescue it either. `empirical luck` — *something works and
nobody can say why* — requires `mechanism` to be **not known**, and bladder
cancer's is. So a record can sit in `known & treatable` with a therapy nobody
understands, and nothing shows it.

What it costs is concrete rather than academic:

- **No biomarker for response.** Nothing predicts who benefits from the most-used
  therapy in the record.
- **No rational route to improvement.** Fifty years and no better version.
- **No synthetic equivalent** — which is why the manufacturing blocker below is
  as serious as it is. If anybody knew which component of a live bacterium did
  the work, the shortage would be an engineering problem instead of a crisis.

The corpus has more of this than it looks, and the existing schema hides all of
it inside `established`:

| record | disease mechanism | why the treatment works |
|---|---|---|
| **bladder-cancer** | established | **unknown after 50 years** |
| **bipolar** (held) | `correlates` — so the quadrant *does* catch it | lithium, unknown since 1949 |
| **depression** (held) | `correlates` | SSRIs, and the monoamine account is not a mechanism |
| **crohns**, **me-cfs** | partial / none | — |
| **h-pylori-ulcer**, **cml**, **hepatitis-c** | established | **and the drug's action is understood exactly** |

That last row is the point. **Understanding the disease and understanding the
drug are independent, and only one of them has a field.**

## 136. The pathway performs differently depending on who presents · **open**
*Forced by:* `bladder-cancer`.

Painless visible haematuria is bladder cancer's presenting symptom, a recognised
red flag, with established referral pathways. It is why this record has one of
the highest `caught_in_time` figures in the register.

**In women the same symptom is attributed to urinary infection or to
gynaecological causes more often, investigated later, and the cancer is found at
a worse stage.** The test is identical. What differs is whether it gets ordered.

`measurement.diagnostic` grades **the kind of evidence available** — objective,
clinical, complaint. It says nothing about whether the evidence gets sought, and
a register built to say *why a treatment is being aimed badly* is silent on one
of the commonest reasons.

It is not #122, which says a patient reached care and got the wrong version of
it. **These patients did not get referred at all**, and the reason is a
demographic prior applied to a symptom.

It is not #113 either. That says `efficacy` was measured in one population and
applied to another — a property of the evidence. **This is a property of the
clinical encounter**, and it happens at the front door.

The corpus already contains it, mostly unstated:

| record | the symptom | who gets it attributed elsewhere |
|---|---|---|
| **bladder-cancer** | visible haematuria | women — to infection |
| **ischaemic-heart-disease** (held) | chest pain | women — atypical presentation, and MI is missed more often |
| **melanoma** | a changing pigmented lesion | acral disease in darker skin — **nobody examines a sole** |
| **prostate-cancer** | — | men of African ancestry, twice the mortality, under-enrolled in the trials (#113) |
| **noma**, **buruli-ulcer** | a sore mouth, a painless nodule | children of the very poor — to nothing at all |
| **me-cfs**, **pots**, **heds** | fatigue, dizziness, pain | **women — to psychological causes**, which is what `contested:` records the downstream of |

The last row matters because the register already holds those three and treats
the contestation as a fact about the entity. **Some of it is a fact about who
presents with it.**

Cheap and worth doing: a `disparity:` note on `measurement`, recording who the
pathway underserves and by what mechanism — referral, attribution, examination,
or enrolment. Most of these are documented in the literature already and none of
them is in this register.

## 137. Overdiagnosis without a screening programme · **open**
*Forced by:* `renal-cell-carcinoma`.

More than half of renal cancers are now found by accident — on an abdominal CT
for pain, an ultrasound for gallstones, a scan for trauma. Incidence has risen
substantially over three decades and mortality much less.

**Nobody decided to look.** There is no screening programme for kidney cancer,
none is recommended, and the imaging that finds it is being done for a hundred
other reasons and is not going to stop.

Every previous overdiagnosis record in this corpus involved a choice:

| record | somebody chose to |
|---|---|
| **thyroid-cancer** | offer ultrasound as a screening add-on |
| **prostate-cancer** | send a PSA |
| **lung-cancer** | run a low-dose CT programme |
| **melanoma** | *(no programme — a pathological threshold drifted, #119)* |
| **renal-cell-carcinoma** | **nothing. The scanner was already on.** |

This is a different object and it needs a different lever. Screening
overdiagnosis is addressed by not screening — thyroid cancer's Korean reversal
proves it works. **Incidental overdiagnosis cannot be addressed by not scanning**,
because the scan was justified by something else entirely.

So the register inherits a whole category it cannot name: the **incidentaloma**.
Adrenal masses, thyroid nodules on carotid ultrasound, pulmonary nodules on CT
for something else, pancreatic IPMNs, meningiomas on head CT for headache —
findings generated by **imaging capacity rather than by clinical intent**, each
requiring a decision nobody planned to make.

And it is not simply harm. RCC's accidental detection has genuinely shifted stage
at diagnosis and cured people. **It sits between thyroid cancer's pure loss and
colorectal cancer's pure gain, and nobody chose where.** A fifth of small renal
masses are benign, many of the rest never declare themselves, and some are
curable cancers found in time.

The minimal move is a flag on `window` or `measurement` marking detection as
**incidental rather than sought**, because the two have different costs,
different remedies, and different people responsible. The larger point is that
**as imaging gets cheaper this category grows without anybody deciding it
should**, and a register built around deliberate acts will keep missing it.

## 138. Stopping is progress, and the register can only record starting · **open**
*Forced by:* `renal-cell-carcinoma`. **Eight records deep.**

Renal cell carcinoma's history is largely a history of subtraction. Radical
nephrectomy gave way to partial. **Cytoreductive nephrectomy — standard practice
for two decades — was de-adopted when a randomised trial found it unnecessary.**
High-dose interleukin-2, with its capillary leak and its intensive care, was
abandoned. Small masses that would have been removed are watched.

Every one of those improved care. **None of them changed `capability`, and the
register records nothing.**

It is not one record's quirk. Counting the corpus:

| record | what was stopped |
|---|---|
| **breast-cancer** | axillary clearance → sentinel node biopsy |
| **melanoma** | completion lymphadenectomy, abandoned after trials |
| **childhood-all** | cranial irradiation → intrathecal chemotherapy |
| **prostate-cancer** | immediate radical treatment → active surveillance |
| **thyroid-cancer** | screening itself, plus total thyroidectomy and radioiodine |
| **gastric-cancer** | gastrectomy → endoscopic submucosal dissection |
| **bladder-cancer** | early cystectomy → BCG |
| **renal-cell-carcinoma** | cytoreductive nephrectomy, IL-2, radical nephrectomy |

**Eight of the twelve cancers in this register improved substantially by doing
less**, and in several of them it is the largest improvement of the last twenty
years.

Gap **#26** noticed the symptom — *toll reduction is progress that moves no
axis* — and asked for `axis: toll`. Four records have since hit the narrower
version of that (`toll.incidence`, which `moved` cannot express). **This is the
underlying thing: subtraction is a category of medical progress with no field, no
vocabulary, and — critically — no champion.**

The barriers to stopping are specific and different from the barriers to
starting, and the corpus has already named several:

- **No advocate.** Thyroid cancer's blocker: *"there is no constituency for a
  test not done, and every individual step is defensible."*
- **No product.** Nobody markets not operating. There is no sponsor for a trial
  showing an existing practice is useless, and the trials that did exist —
  CARMENA, the melanoma lymphadenectomy trials — were largely publicly funded.
- **Defensive asymmetry.** A doctor who operates unnecessarily is doing their
  best; a doctor who watches and is wrong is culpable.
- **Sunk skill.** A surgeon trained in an operation has a legitimate interest in
  the operation continuing, and de-adoption stranded real expertise.

**And this matters for what the project says it is building.** fndtn's goal is
the process that solves medicine. **A large share of the improvement in cancer
care over thirty years has been subtraction** — and the register, the funding
system, the regulator and the trial apparatus are all built for addition. A
process that only adds cannot produce half of what the last three decades
produced.

Minimal move: `moved` gains `how: de-adoption` alongside the vocabulary #120
proposed, and a blocker kind for *a practice that should stop and has not.*

## 139. Risk factors have trajectories and the register records only their existence · **open**
*Forced by:* `uterine-cancer`.

Endometrial cancer incidence **and mortality** are both rising in high-income
countries. Almost nothing else in this corpus can say that.

The cause is obesity. Adipose tissue aromatises androgens to oestrogen;
unopposed oestrogen drives endometrial proliferation; it is the most
obesity-attributable cancer there is, the bariatric surgery evidence makes the
association causal, and obesity prevalence has risen for four decades.

The record states `prevention: risk-reduction`, which is a **state**. It cannot
say that the risk is **growing**, and that the burden figure above will be wrong
next year in a predictable direction.

**This is the mirror of #129.** There, gastric cancer receded because the world
changed — refrigeration replaced salt preservation — and nobody intended it.
Here the world changed the other way and a cancer is advancing, and nobody
intended that either. **Same mechanism, opposite sign, and the schema records
neither.**

Sorted by which way the exposure is moving, the corpus splits cleanly:

| exposure | direction | records affected |
|---|---|---|
| **tobacco** | falling, in high-income countries | lung, bladder, gastric, renal, IHD, stroke, COPD — **seven records improving for free** |
| **salt preservation** | fell, 1930s onward | gastric — the largest cancer prevention in history (#129) |
| **H. pylori, sanitation** | falling | gastric, h-pylori-ulcer, MALT lymphoma |
| **obesity** | **rising, everywhere** | **uterine, liver, renal, colorectal (young-onset), pancreatic, oesophageal** |
| **ageing** | rising | nearly everything here |

**Seven records are quietly improving because of a habit change nobody in
medicine controls, and at least five are quietly worsening for the same reason.**
The register reports all twelve as static numbers with a `prevention` enum.

It matters directly for the project's purpose. *What should we work on next*
answered from a snapshot will systematically under-weight the diseases whose
cause is accelerating and over-weight the ones coasting downward on a trend that
has already happened. **Endometrial cancer is a smaller number than lung cancer
and it is going the wrong way**, and nothing in this register can show that.

Minimal move: a `trend:` on `burden` — rising, flat, falling — with the driver
named. It is cheap, it is knowable, and it converts every burden figure from a
point into a direction.

## 140. The patient may rationally choose the worse outcome · **open**
*Forced by:* `uterine-cancer`.

A young woman with low-grade endometrial cancer confined to the endometrium can
be treated with progestins instead of hysterectomy. A majority respond. A
substantial minority recur. Hysterectomy remains available afterwards.

**She is choosing a less certain cancer outcome in order to be able to have
children, and she is not making a mistake.**

`efficacy` is *the fraction of patients in whom the best intervention works*, and
it assumes there is one best intervention. For a growing number of records there
are two, with different tolls, and **the choice belongs to the patient and is not
a failure of care.**

The corpus is already full of it:

| record | the effective option | the option a patient may rationally prefer |
|---|---|---|
| **uterine-cancer** | hysterectomy | progestins, to keep fertility |
| **prostate-cancer** | radical prostatectomy | active surveillance, to keep continence and potency |
| **bladder-cancer** | radical cystectomy | trimodal therapy, to keep the bladder |
| **colorectal-cancer** | resection of rectal cancer | watch-and-wait after complete response, to avoid a stoma |
| **thyroid-cancer** | total thyroidectomy | lobectomy or surveillance |
| **breast-cancer** | mastectomy | breast-conserving surgery with radiotherapy |
| **cml** | *(historically)* transplant, curative | imatinib, `suppressive`, **and better** (#123) |

That last row is the giveaway. **#123 said the ladder is ordered by finality
rather than by value.** This is the same problem one level down: even within a
rung, the register assumes more effective is better, and for a large class of
decisions the trade is between *how likely the cancer is gone* and *what is left
of the person afterwards*.

The register has the raw material — `toll` records what the cure costs — and no
way to connect it to `efficacy` as a **trade the patient makes** rather than as
two independent facts. `restored` gets closest and is derived after the fact.

And note what makes uterine cancer's version different from the others.
Prostate, bladder, thyroid and rectal preservation trade a quantity of function
for a quantity of risk. **Here what is preserved is the ability to have children**,
which is not a smaller version of the same good, and which is the clearest case
in the corpus that `efficacy` alone cannot rank two options.

## 141. The burden figure can be negotiated rather than measured · **open**
*Forced by:* `cholera`.

WHO's estimate of annual cholera deaths runs from roughly **21,000 to 143,000** —
a seven-fold spread, in a disease with a pathognomonic presentation, a rapid
diagnostic test, and a treatment so simple that any health worker can confirm the
diagnosis by watching it work.

**The uncertainty is not epidemiological. It is diplomatic.**

Cholera is notifiable under the International Health Regulations, and declaring
it costs a country trade restrictions, tourism collapse, and a public signal that
it cannot supply clean water. So states report late, report partially, report
under the heading *acute watery diarrhoea*, or do not report. The official count
is low by a factor everyone involved knows and nobody can state.

The register has **three** ways a burden figure goes wrong and this is a fourth:

| gap | mechanism | who is responsible |
|---|---|---|
| **#88** (noma) | the dead are never counted — they die at home | nobody; it is structural |
| **#104** (h5n1) | the mildly ill are never tested — ascertainment intensity | nobody; it is a design choice |
| **#33** (msmds) | the disease is too rare to count | nobody |
| **#141** (cholera) | **the state chooses not to report** | **a named ministry, for a stated reason** |

That last row is different in kind. The first three are failures of capacity or
of method. **This one is a decision, made deliberately, by an actor with an
interest** — and it is the only one that could be fixed by changing an incentive
rather than by building something.

It matters beyond cholera. Any notifiable disease with trade or reputational
consequences carries the same distortion: **plague, yellow fever, and — within
living memory — the early reporting of SARS and of COVID-19.** The
register's `src` vocabulary has `recall`, `reasoning` and citations. None of them
says *this number was negotiated*, and for a project that intends to rank
diseases by burden that is a load-bearing omission.

And it compounds: suppressed reporting distorts stockpile allocation, research
priority, and every cross-disease comparison the register might eventually make.
**Cholera would sit anywhere between rabies and tuberculosis in a
mortality-ranked list depending on which end of WHO's own range is used.**

## 142. The register assumes a health system exists · **open**
*Forced by:* `cholera`.

Cholera's current burden is in **Yemen, Haiti, Sudan, the Democratic Republic of
the Congo, Syria and Zimbabwe.** That is not a list of the poorest countries. It
is a list of the countries at war or in state collapse.

The treatment is a sachet of powder costing cents, on every essential medicines
list, that takes case fatality from around fifty percent to under one. **People
die six hours from it.**

Not because it is expensive. Not because supply failed. Not because they refused
it, or because it does not work, or because nobody has invented it. **Because
there is no longer anybody in charge of the water, the clinic, or the road
between them.**

The blocker taxonomy has twelve kinds — `knowledge`, `candidate-untested`,
`evidence-incomplete`, `no-sponsor`, `regulatory`, `manufacturing`, `cost`,
`logistics`, `diagnosis`, `adherence`, `tooling`, `policy` — and **every one of
them presumes an institution capable of acting.** `logistics` means a supply
chain that could be improved; `policy` means a government that could decide
differently.

Filed here as `logistics` and `policy`, and neither is true. The constraint is
that the state has stopped functioning.

It is not a cholera peculiarity, and the corpus has been circling it:

| record | where the burden is | what is actually missing |
|---|---|---|
| **cholera** | Yemen, Haiti, Sudan, DRC | **anyone in charge of the water** |
| **ebola** | Kivu, during an armed conflict | filed as `policy`; treatment centres were burned |
| **measles** | conflict zones and displaced populations | the routine immunisation service stopped existing |
| **visceral-leishmaniasis** | East Africa — and #52 named conflict as a driver | — |
| **noma** | the Sahel | a health system that was never built rather than one that collapsed |
| **tuberculosis** | prisons, displacement | — |
| **h5n1**, **covid-19** (queued) | — | the inverse: **surveillance requires a state too** |

Two things follow that the register should be able to say:

- **Capability is conditional on governance**, and for a substantial share of the
  world's remaining burden that condition is the binding one. A register that
  reports `access: 0.55` for cholera is averaging a functioning treatment centre
  and a besieged city, and SCHEMA.md correctly forbids splitting them because
  access tiers are not strata.
- **The actor who could move it is not in `who_could`.** That field holds
  `health-system`, `government`, `regulator`, `payer`, `manufacturer` and the
  rest. It has no entry for a peace process, a ceasefire, or a humanitarian
  corridor — and for these records those are the intervention.

The honest minimum is a blocker kind — `conflict`, or `state-capacity` — with the
explicit understanding that the register is recording a constraint it cannot
recommend anything about. **That is uncomfortable and it is better than filing a
war under `logistics`.**

## 143. Capability can be a race rather than a state · **open**
*Forced by:* `typhoid`.

Typhoid's `efficacy` reads 0.95. It was effectively 0.99 for decades and it is
falling, and the reason it is falling is that the drugs have been used.

Chloramphenicol in 1948, then ampicillin and co-trimoxazole, then the
fluoroquinolones, then in 2016 an **extensively drug-resistant clone in Pakistan
that defeats third-generation cephalosporins too.** What remains is azithromycin —
to which resistance is already reported — and the carbapenems, which cannot be
given at a health post.

At the same time the **typhoid conjugate vaccine** was prequalified in 2018: one
dose, roughly eighty percent effective, immunogenic in infants, durable. Pakistan
deployed it in direct response to the outbreak.

**Two capabilities inside one record, moving in opposite directions, at
comparable speed, and the outcome for the disease depends on which arrives
first.** The register reports `efficacy: 0.95` and `prevention: prophylaxis` as
two static facts.

This is not **#139**. That gap says a *risk factor* is trending — obesity rising,
smoking falling — which is a fact about the world outside the record. **This is
the capability itself degrading, and degrading because it is being used.** #130
said an intervention's harm can land in a different entity; this is the same
mechanism pointed inward, at the record's own future.

The corpus is full of it and reports none of it:

| record | what is eroding | what is arriving |
|---|---|---|
| **typhoid** | five antibiotic classes, one at a time since 1948 | a conjugate vaccine, 2018 |
| **tuberculosis** | MDR and XDR | bedaquiline, pretomanid, shorter regimens |
| **amr-infection** | **the entire record is this gap** | almost nothing |
| **malaria** (queued) | artemisinin and insecticide resistance | a vaccine, at last |
| **hiv** | resistance where suppression fails | long-acting injectables |
| **h-pylori-ulcer** | clarithromycin resistance | — |
| **gastric-cancer** | *(and mass eradication would accelerate it — #130)* | — |

Two consequences worth separating:

- **`efficacy` is a snapshot of a quantity with a derivative**, and for the
  anti-infectives that derivative is reliably negative. A register taking an
  annual bearing will record the level and miss the slope, which is the whole
  point of taking bearings.
- **The two trends have different owners.** Slowing the erosion is stewardship,
  diagnostics and prescribing policy. Speeding the arrival is vaccine
  introduction and financing. They compete for the same budget and the register
  cannot show that they are the same fight.

Minimal move: a direction on `efficacy` — the same `trend:` #139 asked for on
`burden`, applied one field over. **The erosion is measurable, it is measured, and
it has nowhere to go.**

## 144. Public health does things TO people, and `toll` only records treatment · **open**
*Forced by:* `typhoid`.

Two to five percent of people infected with *S.* Typhi become chronic
gallbladder carriers — shedding for years, entirely well, frequently unaware.

**Mary Mallon was detained for roughly twenty-six years for being one.** She was
never ill. She was quarantined on an island for the protection of other people,
released on a promise she broke, and re-detained for the rest of her life.

Managing carriers today means prolonged antibiotics, sometimes **removal of a
healthy gallbladder from a healthy person**, and in many jurisdictions permanent
exclusion from food handling and from healthcare work.

None of that is treatment. The person has no symptoms and derives no benefit.
**`toll` is defined as what the cure costs the patient, and there is no field for
what public health costs somebody on everybody else's behalf.**

#134 came close and is not the same thing. That gap says **the diagnosis is
itself a harm** — the thyroid microcarcinoma patient on surveillance carries a
label, insurance consequences and scan anxiety. That is a harm the person absorbs
passively. **This is a harm applied to them deliberately, by an institution, for
somebody else's benefit, and sometimes against their will.**

The corpus already holds it and has been filing it as prose:

| record | what is done to a well person |
|---|---|
| **typhoid** | detention, cholecystectomy, lifetime occupational exclusion |
| **ebola** | semen testing and counselling programmes for cured survivors |
| **tuberculosis** | isolation, and in some jurisdictions detention for non-adherence |
| **leprosy** | historically, segregation — and #77's stigma outlives the policy |
| **h5n1** | **culling**, which falls on farmers and on birds |
| **measles** | school exclusion of unvaccinated children |
| **cholera**, **covid-19** (queued) | movement restriction, cordons |
| **gastric-cancer** | *(the inverse: mass antibiotic treatment of the well)* |

Three things the register should be able to distinguish and cannot:

- **Who benefits.** Treatment benefits the patient; this benefits third parties.
  The corpus's whole toll vocabulary assumes the first.
- **Whether it is consented.** Semen testing after Ebola is offered; detention is
  not. The difference is the difference between a health service and a police
  power, and it is invisible here.
- **Whether it is proportionate**, which is the only question that matters and
  which requires knowing the first two.

This is uncomfortable to build and it is squarely inside what the register claims
to be for. **It says it measures capability and what capability costs.** Coercion
is a capability — it worked, repeatedly, and it is how several diseases in this
corpus were controlled — and its cost is currently recorded nowhere.

## 145. An antibiotic's value to its maker is inverse to its correct use · **open**
*Forced by:* `mrsa`.

**Achaogen took plazomicin through approval in 2018 and filed for bankruptcy
within a year.** Melinta Therapeutics, with several approved antibacterials,
filed in 2019. Tetraphase and Aradigm followed.

None of those were failed drugs. They were approved products with real activity
against resistant organisms, owned by companies that could not survive selling
them.

**The correct use of a new antibiotic is to hold it in reserve** — used sparingly,
only when the older agents fail, precisely so resistance does not develop.
Stewardship is a policy of not selling the product. Meanwhile it is priced
against generics costing pennies, taken for a week rather than for a lifetime,
and its patent runs while it sits on a shelf.

**#124** set out three commercial shapes. This is a fourth and it is the only one
where success and revenue point in opposite directions:

| shape | the commercial object | what happens if it works |
|---|---|---|
| `curative` | one sale per patient | **the market shrinks** — hepatitis C |
| `suppressive` | an annuity | the market grows — CML |
| `preventable` | a sale to well people | the payer is a government, the benefit is invisible |
| **reserve antibiotic** | **a product you are supposed to withhold** | **you should sell almost none of it** |

It has a distinct fix that none of the other three implies. **Delinkage**: pay for
availability rather than for volume. The United Kingdom's and Japan's subscription
pilots and the PASTEUR Act proposed in the United States all do exactly that, and
they are the right shape and they are small.

And the corpus can already see who it hits. Every record whose blocker is *no new
antibiotic* — `typhoid`'s resistance ladder, `amr-infection`, `tuberculosis`'s
forty-nine-year drug gap, `gastric-cancer`'s clarithromycin problem — is
downstream of this one market failure, and the register records four separate
`no-sponsor` blockers rather than one structural cause.

## 146. Resistance can remove the best option without removing all of them · **open**
*Forced by:* `mrsa`.

MRSA bacteraemia kills more people than methicillin-*susceptible* *S. aureus*
bacteraemia. The usual reading is that the resistant organism is worse.

**A substantial part of it is that vancomycin is a worse drug than
flucloxacillin.** Slower killing, poorer tissue penetration, serum monitoring,
nephrotoxicity. For susceptible infection an antistaphylococcal beta-lactam
outperforms vancomycin; resistance removes that option and forces the
second-best.

**So a share of MRSA's excess mortality is attributable to the replacement drug
rather than to the bug**, and `efficacy` cannot tell those apart.

The distinction is not academic, because the two readings imply opposite work:

- **If the organism is worse** — you need a better drug against it, and the
  answer is discovery.
- **If the replacement is worse** — you need to preserve the first-line agent, and
  the answer is stewardship, diagnostics and infection control.

For MRSA the second is demonstrably true, and it is why the record's largest
`moved` entry is an infection control programme rather than a molecule.

It reframes what resistance *is* across the corpus. **Resistance is usually
described as capability being destroyed. Mostly it is capability being
degraded** — the ladder in `typhoid` is not five drugs failing to nothing, it is
five steps down from a cheap oral tablet to an intravenous carbapenem that cannot
be given at a health post:

| record | what resistance actually took |
|---|---|
| **mrsa** | a better beta-lactam, replaced by a mediocre glycopeptide |
| **typhoid** | cheapness, oralness, and empirical treatment — not curability |
| **tuberculosis** | six months became eighteen, with injectables and hearing loss |
| **h-pylori-ulcer** | first-line success rates, not the possibility of cure |
| **hiv** | a regimen, replaced by another regimen |

**None of those is "nothing works".** Each is a step down a staircase with a
bottom, and the register has one word — `curative` — for every step. #143 said
capability can be a race; this says **what the race is losing is usually
quality, not existence**, and that the quality is measurable and unrecorded.

---

**Strengthened by `mrsa`, not new:**

- **#120 (the register records that a rating changed, never how) — AND THIS IS
  THE CLEANEST `delivery` CASE IN THE CORPUS.** England's MRSA bacteraemia rate
  fell by roughly eighty percent from the mid-2000s. Hand hygiene, line bundles,
  admission screening, decolonisation, isolation, mandatory published
  trust-level surveillance, and a national target with a chief executive's job
  attached. **Every element was already known. What changed was that somebody was
  held responsible for doing them.** No discovery, no product, no new molecule —
  and the `how:` vocabulary #120 proposed would say `delivery` in one word.
- **#143 (capability is a race) — THE INVERSE CASE, ONE RECORD LATER.** Typhoid is
  resistance rising because the drugs are used. **MRSA is resistance prevalence
  falling because the organism was stopped from spreading.** You can win the race
  without a new antibiotic, by attacking transmission instead of the bug — and
  the register can record neither direction.
- **#66's open half (prevention is one word doing five jobs) — SIXTH JOB, AND
  NOBODY RECEIVES IT.** `prophylaxis` now covers a childhood vaccine, a monthly
  injection, a seventy-two-hour post-exposure course, a bed net, a colonoscopic
  polypectomy — and **infection control, which is applied to staff, surfaces and
  procedures rather than to any patient.** There is no dose and no recipient, it
  is the most effective intervention in this record by a wide margin, and it is
  filed under `access` improving.
- **#109 (prevention has no coverage field) — fifth record.** The 2004 `moved`
  entry records an infection control programme under `access` because there is
  nowhere else. Measles, cervical cancer, colorectal cancer, typhoid, MRSA.
- **#144 (public health does things TO people) — one record later, and this one is
  routine.** A patient labelled MRSA-colonised carries the flag on every
  subsequent admission: contact precautions, gowns, a side room, for a state they
  have no symptoms from. **Isolated patients receive less clinical contact, more
  anxiety and depression, and more preventable adverse events.** Typhoid's version
  was Mary Mallon and an island; this version happens thousands of times a day and
  nobody calls it coercion.
- **A vaccine failure worth recording rather than forgetting.** Every *S. aureus*
  vaccine candidate has failed, and one was stopped because **vaccinated patients
  who became infected anyway died more often than placebo recipients.** In an
  organism a fifth of humanity carries in their nose without harm. It suggests the
  problem is the wrong kind of immunity rather than insufficient immunity, and
  nobody knows what protective immunity to *S. aureus* would look like.
- **`predictive: good` here and `partial` in typhoid, for the same test.**
  Antimicrobial susceptibility testing is the paradigm case of predictive
  measurement and it is seventy years old. MRSA earns `good` because a hospital
  laboratory runs it; typhoid earns `partial` because a blood culture mostly does
  not happen. **The measurement axis is absorbing an access problem**, which is
  worth noticing before the register concludes anything about where measurement
  is weak.

---

## 147. The disease is a byproduct of capability, and nothing records that · **open**
*Forced by:* `cre`.

Carbapenem-resistant Enterobacterales is overwhelmingly a disease of medical
intensity. Its patients are on ventilators, carrying central lines,
immunosuppressed after transplant, neutropenic after chemotherapy, or newborn and
surviving in an intensive care unit that would not have existed fifty years ago —
and they have all received broad-spectrum antibiotics, which is what selected the
organism in the first place.

**CRE exists because medicine got good enough to keep those people alive.**

That is not a side effect of one drug. It is the aggregate output of the entire
enterprise, and it has its own name in the literature — healthcare-associated
infection — which the register cannot express, because every entity in this
register has causes and none of them is *the rest of this register*:

| entity | produced by |
|---|---|
| **cre**, **mrsa** | intensive care, devices, broad-spectrum antibiotics |
| *C. difficile* colitis | antibiotics given for something else |
| prosthetic joint infection | joint replacement working |
| neutropenic sepsis | curative chemotherapy |
| post-transplant lymphoproliferative disease | transplant immunosuppression |
| ventilator-associated pneumonia | mechanical ventilation |

#130 said an intervention's harm can land in a different entity, and it was about
one drug causing one problem. **This is the same shape at the scale of the whole
practice**, and it has a consequence #130 does not: the burden *grows as
capability grows*. A health system that becomes able to do more intensive
medicine acquires more of these diseases, and a system that cannot do intensive
medicine does not have a CRE problem, because its patients die of the thing that
would have put them in the unit.

**Which makes the register's arithmetic quietly wrong in a specific way.**
Summing burden across records treats these as independent quantities to be
reduced. They are not independent — some of them are the price of the others, and
a register aimed at "solve medicine" should be able to say which reductions would
cost it something elsewhere.

The minimal form is a link — `iatrogenic_from: [list of slugs]`, or an obstacle
in Engpass that several records point at. The maximal form is a second class of
entity for *the costs of capability*, which is a bigger claim than this register
is ready to make on one record.

**Do not resolve this by deleting the entities.** CRE is a real disease that
kills real people and needs its own answer. The gap is that the register has no
way to say where it came from.

---

## 148. Toll is judged against the alternative, and recorded as absolute · **open**

*Forced by:* `cre`.

Colistin was introduced in the 1950s and largely abandoned in the 1970s because
its nephrotoxicity was not worth it when safer antibiotics existed. It came back
in the 2000s, unchanged, as a last line against carbapenem-resistant
Gram-negatives — same molecule, same kidney, same third-to-a-half rate of acute
kidney injury.

**Nothing about the drug's toll changed. What changed is what it was being
compared against.**

`toll` is a property of the treatment in this schema — a severity, a permanence,
an incidence. It reads as an absolute fact about a molecule. It is not. It is a
judgement about a molecule *relative to the best available alternative*, and the
alternative moves:

| treatment | acceptable when | unacceptable when |
|---|---|---|
| **colistin** | nothing else touches the organism | a beta-lactam combination works |
| **thalidomide** | myeloma has no good options | later agents arrive |
| **high-dose IL-2** (`renal-cell-carcinoma`) | it is the only thing producing durable remissions | checkpoint inhibitors do it more safely |
| **cranial irradiation** (`childhood-all`) | relapse in the brain is otherwise routine | intrathecal chemotherapy prevents it |
| **radical mastectomy** | the alternative is believed to be death | lumpectomy is shown equivalent |

Three of those five are already records in this register, so this is not a
hypothetical.

**Two consequences.**

First, a `moved` entry on `toll` frequently records **no change in the
treatment** — only that something better arrived and displaced it. The `why:`
field carries that today by prose, and #120's proposed `how:` vocabulary would
need a value for *superseded* distinct from *improved*.

Second, and more awkward: **a record's `toll` is only meaningful alongside the
year and the setting.** CRE's toll is `major` globally because colistin remains
the default over most of the burden, and `minor` in a hospital with cefiderocol
on the shelf. Same disease, same date, and the schema has one field.

That is #52 (solved here, not there) reaching a field nobody expected it to
touch, and it suggests the axes that *look* like properties of a disease —
`toll`, `efficacy`, `ongoing` — are mostly properties of **a disease under a
particular standard of care**, which the register does not name.

---

**Strengthened by `cre`, not new:**

- **#146 (resistance degrades rather than destroys) — confirmed one record later,
  and this record is the strongest case.** "Carbapenem-resistant" is used as a
  synonym for untreatable and in 2026 it is not. Six agents were approved between
  2015 and 2019 against exactly these organisms. What resistance took is not
  curability — it is **cheapness, availability, and the ability to treat
  empirically.** All three CRE strata rate `curative`; they differ in which drug,
  and the drug is the constraint.
- **#145 (the antibiotic market is inverted) — the same bankruptcy, from the other
  side.** Achaogen's plazomicin was developed *specifically* for
  carbapenem-resistant Enterobacterales, approved in 2018, and the company filed
  the following year. So the pipeline that produced this record's only `moved`
  entry is one nobody has a commercial reason to maintain, and the register can
  see the effect in two records without being able to link them.
- **#52 (solved here, not there) — WITH A BIOLOGICAL CAUSE RATHER THAN AN ECONOMIC
  ONE, WHICH IS NEW FOR THIS GAP.** Which carbapenemase an organism carries
  decides which drug works: serine enzymes fall to avibactam and vaborbactam,
  metallo-beta-lactamases are untouched by both. **And the enzymes have a
  geography** — KPC in the Americas and southern Europe, NDM across the Indian
  subcontinent. So the hardest enzyme sits where the expensive drugs that beat it
  are least available. Visceral leishmaniasis's version of #52 was money; this
  one is money **aligned with chemistry**, which is worse, because it will not be
  fixed by the same drug getting cheaper.
- **#142 (the register assumes a health system exists) — and here it corrupts the
  burden figure as well as the rating.** Carbapenem resistance is only counted
  where a laboratory can test for it. The same missing microbiology causes the
  wrong treatment *and* the invisible epidemiology, so the record's `cases` value
  and its `access` value have a single common cause. It is the first record where
  a derived number and an input number fail together for one reason.
- **#144 (a colonisation label is imposed indefinitely) — one degree worse than
  MRSA.** A CRE-colonised patient is flagged, isolated and gowned-and-gloved on
  every subsequent admission for a state with no symptoms — and unlike MRSA
  **there is no decolonisation that works**, so the label cannot be removed. The
  flag is permanent in practice.
- **#66's open half — seventh job for `prophylaxis`, except this record could not
  use it.** MRSA earned `prophylaxis` on decolonisation; CRE has none, so it rates
  `risk-reduction` and its entire prevention story — hand hygiene, screening,
  cohorting, stewardship, and refurbishing the sink drains that harbour the
  organism — has no home. **The most consequential prevention here is prescribing
  fewer carbapenems, which nobody counts as prevention at all.**
- **`who_could` still has no multilateral procurement body**, four records after
  the veterinary-service complaint. The actor who could actually move CRE's `cost`
  blocker is a pooled-procurement or prequalification mechanism of the WHO / Global
  Fund / Gavi kind — demonstrably the thing that worked for HIV and hepatitis C
  antivirals — and this record files it under `nonprofit` for want of a term.

---

## 149. The pathogen can evolve against the *test* · **open**
*Forced by:* `malaria`.

The dominant malaria rapid diagnostic test detects histidine-rich protein 2.
Parasites carrying deletions of *pfhrp2* and *pfhrp3* cause perfectly ordinary
disease and return a **negative** result.

**The deletions are under positive selection precisely because testing is
universal.** A parasite that the test misses is a parasite that goes untreated,
survives, and transmits. Hundreds of millions of tests a year is a selection
pressure, and it selects for invisibility. Eritrea has already abandoned
HRP2-based testing nationally; deletions are documented across the Horn of Africa
and in South America.

**Nothing else in this register does this.** The corpus is full of resistance to
*drugs* — chloroquine, artemisinin, methicillin, carbapenems, rifampicin — and it
has one axis (`efficacy`) and one blocker kind (`knowledge`, `tooling`) that
between them can hold it. **Resistance to a diagnostic has no home at all**,
because `measurement` is written as though a test were an instrument with a fixed
quality:

| the register assumes | malaria shows |
|---|---|
| a test's sensitivity is a property of the test | it is a property of the test *and the current parasite population* |
| a test improves or stays the same | it can silently degrade in the field |
| `diagnostic: objective` is stable | the objectivity is exactly what is being escaped |

The nearest analogue in the corpus is **vaccine escape** — pneumococcal serotype
replacement after conjugate vaccination, which the register also cannot say. The
common shape is that **any intervention applied at population scale is a
selection pressure**, and this register has language for that only when the
intervention is a drug.

Three consequences worth separating:

1. `measurement` needs to be datable, or at least to carry a witness that names
   the escape. `diagnostic: objective` is true of malaria RDTs and is becoming
   less true every year, and nothing on the record says which direction it moves.
2. **A degraded diagnostic corrupts the burden data too.** Cases the test misses
   are not counted, so the surveillance that would detect the problem is the thing
   the problem breaks. Compare `cre` one record earlier, where the missing
   laboratory corrupted the rating and the epidemiology from one cause — here the
   *present* laboratory does it.
3. It is a `tooling` blocker that looks like a solved problem. The register's
   diagnosis blockers are almost all "the test exists and does not reach people".
   This one is "the test reaches people and is ceasing to work".

---

## 150. The vector is a second adversary, evolving, and only the pathogen is representable · **open**

*Forced by:* `malaria`.

Malaria is simultaneously losing two arms races and the register can express one
of them:

| adversary | what it is doing | where it lands in the schema |
|---|---|---|
| *Plasmodium* | artemisinin partial resistance, independently emerged in East Africa | `efficacy`, a `moved` entry, #146 |
| *Anopheles* | **pyrethroid resistance now near-universal in Africa** | nowhere |

Pyrethroids were the only insecticide class ever approved for treating bed nets —
two decades of monoculture selection applied to billions of nets. The mosquitoes
also evolved *behaviourally*, shifting toward biting outdoors and earlier in the
evening, which defeats an intervention whose entire logic is that people are
indoors and asleep. **Insecticide-treated nets are credited with the largest
single share of the 2000-2015 mortality decline**, so this is not a marginal
component degrading; it is the main one.

**And a vector can arrive.** *Anopheles stephensi* is an Asian, urban-adapted,
container-breeding, multiply-insecticide-resistant mosquito that reached Djibouti
around 2012 and has since spread across the Horn of Africa and into West Africa.
Djibouti had **27 malaria cases in 2012** and tens of thousands within a decade.

Nothing about the parasite changed. Nothing about the drugs, the health system,
the population or the money changed. **A different insect arrived and the disease
came back**, and there is no field in this register in which that event is an
event.

This generalises across a large fraction of the infectious corpus — `dengue`
(*Aedes*, insecticide resistance and Wolbachia), `chagas` (pyrethroid-resistant
triatomines in the Gran Chaco), `visceral-leishmaniasis` (sandflies),
`lymphatic-filariasis`, `onchocerciasis`, `schistosomiasis` (snails). In every
one, a second organism's evolution and geography set the disease's trajectory,
and in every one the register records only what is done to the human.

**This is one step past #69**, which said the intervention can be administered to
a different species (deworming dogs, vaccinating sheep). That gap is about *who
receives* the intervention. This one is about *who fights back* — and it means
the register's implicit model, where capability is a state that improves with
effort, is wrong for a whole class of disease in two independent ways at once.

The minimal form is a `vector:` block carrying the species, what is used against
it, and whether that is still working — parallel to how `efficacy` carries the
drug's standing. The cheap form is to admit that `prevention` is a portfolio
(#109) and give each component its own coverage and its own trend, at which point
"nets, degrading" becomes sayable.

---

**Strengthened by `malaria`, not new:**

- **#109 (prevention has no coverage field) — SIXTH RECORD, AND THIS ONE BREAKS
  THE FIELD OUTRIGHT.** Malaria's prevention is not an intervention, it is a
  portfolio: insecticide-treated nets, indoor residual spraying, seasonal
  chemoprevention for tens of millions of Sahelian children, intermittent
  preventive treatment in pregnancy, two recommended vaccines, larval source
  management, mass drug administration. **Each has its own coverage, its own
  failure mode, its own funder, and its own direction of travel** — the nets are
  losing to resistance while the vaccines are being introduced — and the axis
  holds the single word `prophylaxis`. Every other record could pretend one value
  described one thing. This one cannot.
- **A recommended vaccine that is 40-75% effective and wanes.** RTS,S and R21 are
  the first vaccines ever recommended against a human parasite and they are
  nothing like the register's other vaccines. Measles is >90% for life. These are
  four doses for partial, waning protection, **deployed anyway because the burden
  justifies a bad vaccine** — a tradeoff the schema cannot represent, since
  `prophylaxis` is one value covering both.
- **#146 (degradation, not destruction) — and here it is happening to the last
  class.** Chloroquine gone, sulfadoxine-pyrimethamine gone from treatment,
  artemisinin partially resistant in Southeast Asia and now *independently* in
  East Africa. Independent emergence is the part that matters: containing a
  geographic focus does not contain the phenomenon. And **unlike the bacterial
  records there is no per-patient susceptibility test**, so the clinician cannot
  see it arriving — resistance is measured by population-level efficacy studies,
  years late.
- **#70 (an axis rating is the consequence of another axis's hole) — the vaccine
  line again.** Malaria joins tuberculosis, dengue and *S. aureus*: four records,
  four disappointing vaccines, **one underlying hole — no correlate of
  protection.** Malaria makes it starker than the others because natural immunity
  demonstrably exists and is itself poor: slow, non-sterilising, waning. The
  immune system's own answer is bad, so there is nothing to imitate.
- **#120 (the register records that a rating changed, never how) — and the second
  `moved` entry here is filed on the wrong axis on purpose.** The 2015-2020 stall
  was caused by insecticide resistance, an invading vector species, a funding
  plateau, and diagnostic escape. **Not one of those is a patient's ability to
  obtain a drug**, and `access` is the only axis that could hold any of it.
- **#130 (an intervention's harm lands elsewhere) — inverted: the *disease's* harm
  lands elsewhere.** Malaria in pregnancy sequesters in the placenta and produces
  low birth weight; the mother is cured and the child starts life behind.
  `residue` is scoped to the patient and this residue is in a second person.
- **The restored verdict is the exact inverse of `cre`, one record earlier.** CRE
  derives `cure-costs` — the treatment takes the kidney, the disease leaves little.
  Malaria derives `disease-residue` — the treatment is a dollar and three days and
  costs almost nothing, and **a quarter of cerebral malaria survivors do not get
  their brain back.** Two consecutive infectious records, opposite answers to
  "what is left afterwards", and the pair is a good argument that splitting `toll`
  from `residue` was right.
- **A ratchet the register cannot express: partial funding can be worse than
  none.** Malaria coverage that lapses does not merely stop preventing cases —
  transmission rebounds into a population whose acquired immunity declined during
  the good years, historically producing epidemics worse than the pre-control
  baseline. Sri Lanka in the 1960s is the standing example. **A `cost` blocker in
  this register is implicitly linear**, and this one is not.

---

## 151. A stratum can be transformed without the record moving · **open**
*Forced by:* `tuberculosis` (re-rated).

Between 2019 and 2022, multidrug-resistant tuberculosis went from **eighteen to
twenty-four months of treatment, daily injections, permanent deafness in a
substantial fraction, and treatment success around six in ten** to **six months,
entirely oral, success around 89%.**

In shape that is hepatitis C's direct-acting antivirals. The TB record itself
calls it "a transformation on the scale of hepatitis C's, achieved with almost
none of the attention."

**It moves this record's `efficacy` from 0.83 to 0.85**, because MDR/RR-TB is
about five percent of notified cases.

So the register's headline scalars are weighted averages, and a weighted average
is structurally blind to exactly the kind of progress that actually happens:

| | where progress happens | why |
|---|---|---|
| **small, severe strata** | the unmet need is concentrated there | that is where the trial incentive is, and where a bad outcome is common enough to power a trial |
| **large, mild strata** | rarely | already mostly cured; the marginal gain is small and expensive to demonstrate |

**A register that ranked diseases by how much they had moved would rank
tuberculosis as barely moving in the decade its hardest stratum was
transformed.** That is the wrong answer to the register's own question, and
`moved` is the field the whole "measure → solve → re-measure" loop rests on.

Three separable problems:

1. **`moved` has no `stratum:` scope.** It records a change to a record-level
   axis, and the change frequently belongs to one stratum. The minimal fix is an
   optional `stratum:` naming which one, so the entry can carry the real numbers
   (0.65 → 0.9) instead of the diluted ones (0.83 → 0.85).
2. **The dilution is invisible in the artifacts.** Nothing in `index.md` or the
   web view shows that a two-point move was a thirty-point move somewhere. A
   reader sees the small number and draws the wrong conclusion about where effort
   paid off.
3. **It compounds with #48** (the register cannot rank, because reach is a
   proportion and burden is a magnitude). TB is already the record that forced
   #48; it now also under-reports its own movement. **The single largest entry in
   the register is invisible to the register on two independent axes.**

Related but not the same: **#29** says the measurement flags cannot see a
stratum-level gap. That is about a flag failing to fire. This is about a
*quantity* being averaged into nothing, and it affects every scalar the register
has.

---

**Strengthened by `tuberculosis` (re-rated), not new:**

- **#148 (toll is judged against the alternative) — A CLEANER INSTANCE THAN THE
  ONE THAT FORCED IT, TWO RECORDS LATER.** For decades, treating MDR-TB meant
  months of injected aminoglycosides causing **permanent sensorineural hearing
  loss in a substantial fraction**. It was standard of care, in a disease
  concentrated among poor adults of working age, where deafness frequently ended
  their employment. WHO moved injectables down the priority ordering in 2019.
  **Nothing about amikacin changed.** An alternative existed, and a toll accepted
  for fifty years became unacceptable within about a year. Colistin forced #148;
  TB is the better witness for it, and this register contained the witness the
  whole time without the field to hold it.
- **#146 (resistance degrades rather than destroys) — the record the gap's own
  table already cited, now saying it in its own witness.** What resistance took
  from TB was never curability: it took six months and made it eighteen, took
  tablets and made them injections, took an outpatient course and made it a job
  somebody had to give up. **BPaLM took most of that back.** No stratum of
  tuberculosis has ever fallen off the ladder, and the register has one word for
  every step of that staircase.
- **#145 (the antibiotic market is inverted) — and bedaquiline is the fifty-year
  exhibit.** Its 2012 approval ended a **forty-nine year gap since the last novel
  TB drug**, against the deadliest infectious disease on earth. No other entity in
  this register went half a century without a new agent, and the reason is the
  same market failure that bankrupted Achaogen and Melinta.
- **#49 / #109 (prevention has no efficacy or coverage) — the record that first
  broke the field, unchanged.** BCG is the most widely administered vaccine in
  human history, reliably prevents disseminated disease in young children, and
  its efficacy against adult pulmonary TB ranges from roughly nothing to eighty
  percent by latitude for reasons nobody has explained. It reads `prophylaxis`,
  identically to rheumatic heart disease's near-fully-protective monthly
  penicillin. **The first promising new candidate in a century is in late-stage
  trials, and if it works it moves nothing on this record.**
- **The register's first re-rating, and the loop it is supposed to close.** This
  is assertion `FND-A-0070` superseding `FND-A-0023` from three days earlier —
  no scalar changed, and what the pass added was **four dated `moved` entries
  reconstructed from prose the record already contained.** The record knew its own
  history and had not recorded it in the field designed to hold it. Worth
  watching for on the next re-rating pass: a record that narrates a change in a
  witness is a record with a missing `moved` entry.

---

## 152. `toll` and `residue` cannot be separated when the disease and its treatment are the same event · **open**
*Forced by:* `sepsis`.

The register split what the cure costs (`toll`) from what the disease costs
(`residue`) because tuberculosis proved it had to: the drugs take almost nothing
permanent and the disease scars the lungs of millions of survivors. The last
three records made the split look robust in both directions — `cre` derives
`cure-costs` (colistin takes the kidney, the organism leaves little), `malaria`
derives `disease-residue` (three dollars of tablets, and a quarter of cerebral
malaria survivors do not get their brain back).

**Sepsis derives `both`, and the two numbers are not actually separable.**

Take ICU-acquired weakness — survivors unable to walk for months, some
permanently weaker. It is caused by:

| | attributable to |
|---|---|
| immobility, sedation, neuromuscular blockade, corticosteroids | **treatment** |
| the inflammatory myopathy of sepsis itself | **disease** |

No study can apportion it, and the reason is not that nobody has tried. **The
counterfactual to treatment is death.** There is no untreated arm, there will
never be one, and every quantity in `toll` for this record is therefore an
estimate over a boundary that does not exist in nature.

The same holds for the cognitive impairment (delirium from sedation, and the
septic encephalopathy) and for renal non-recovery (nephrotoxic antibiotics, and
the septic kidney).

**This is a different claim from #84** ("`toll` cannot tell drug toxicity from
the harm of the treatment working"). There the two causes are distinguishable in
principle and the field lacks a slot. Here they are **not distinguishable in
principle**, because the comparison that would separate them is unethical and
unrunnable.

Where else this bites, once named: any condition whose untreated course is
rapidly fatal — the queued `neonatal-conditions` and `maternal-haemorrhage`
obviously, and cancer records where the residue of chemotherapy and the residue
of the tumour arrive in the same organ.

**Do not fix this by merging the fields.** The split is right and TB proves it.
The fix is smaller and duller: an honesty marker on the pair — something like
`attribution: entangled` — so a reader knows the two incidences are a partition
of a total rather than two measurements. The register's existing habit is to put
that in prose, and prose does not survive being turned into a table.

---

## 153. A definition can assert a mechanism nothing can measure · **open**

*Forced by:* `sepsis`.

Sepsis-3 (2016) defines sepsis as *"life-threatening organ dysfunction caused by
a **dysregulated** host response to infection."*

**Nobody can measure dysregulation.** There is no assay, no threshold, and no
statement of what the regulated response would have looked like in this patient.
So the diagnosis runs backwards: organ failure is observed, and dysregulation is
inferred *because the outcome was bad*.

The definition contains a causal claim that nothing can verify, and it is
load-bearing — it is the clause that distinguishes sepsis from "an infection, and
also organ failure".

**Two consequences, and the second is the expensive one.**

*The `mechanism` axis rates the wrong thing.* Sepsis's molecular pathways are
described in detail — PAMPs and PRRs, NF-κB, complement, glycocalyx shedding,
tissue factor and DIC, mitochondrial cytopathic hypoxia, and simultaneous
immunoparalysis. A register reading that literature would rate `established`.
The record rates `partial` on the strength of the definitional hole, and **the
axis has no way to say which of the two it is reporting.** #135 says `mechanism`
never rates why the treatment works; this says it can also silently rate the
pathophysiology while the *definition's own claim* goes unrated.

*You cannot build a test for a concept that has never been operationally
defined.* This is why eleven million deaths a year have no diagnostic. Every
candidate marker — lactate, procalcitonin, blood cultures — measures a
consequence or a correlate, because there is no referent to build an assay
against. The `diagnosis` blocker on that record is downstream of this one, which
is #70's shape (an axis rating is the consequence of another axis's hole) reaching
a new place: **the hole is in the definition rather than in any axis.**

Related and distinct: **#133** says a disease definition is an instrument with a
version. That is about definitions *changing* and the register storing them as
data. This is about a definition *containing an unfalsifiable clause* while it
sits still.

Worth scanning the corpus for others rather than assuming this is unique. The
test is: does the definition name a mechanism, and can that mechanism be
measured independently of the outcome it is invoked to explain? Most descriptive
definitions pass trivially (POTS names a heart-rate rise; depression names
symptoms). The ones to check are those with a mechanism in the name.

---

**Strengthened by `sepsis`, and two gaps can now be built:**

- **#39 (an entity can be a final common pathway) — THE THIRD RECORD, AND IT
  ASKED FOR ONE.** #39 was forced by `pots`, said *"do not add the field for one
  record"*, and named heart failure as the textbook case to wait for. Sepsis is
  a better one: positive criteria, several distinct pathophysiologies, and a
  clinical category that is genuinely useful. **More importantly, #39's
  prediction came true at the largest scale available.** It predicted that "every
  unstratified trial will enrol a mixture and dilute toward the null". Sepsis has
  **over a hundred failed randomised trials** — anti-TNF, IL-1ra, anti-endotoxin,
  NOS inhibitors, TLR4 antagonists, steroids, drotrecogin alfa approved in 2001
  and withdrawn in 2011 — and the current best explanation is exactly that
  mechanism. The endotype literature reports **opposite corticosteroid responses**
  in transcriptomic subtypes, which is the shape the hypothesis predicts. A gap
  written about a small autonomic condition predicted the largest trial graveyard
  in medicine. **Build the field.**
- **#46 (curing the cause need not cure the disease) — THE THIRD RECORD, FROM THE
  OPPOSITE POLE.** #46 was forced by `chagas` — parasite cleared, heart still
  fails — with rheumatic heart disease as the second, and said *"worth a field
  when a third arrives, probably distinguishing aetiological from clinical cure"*.
  Sepsis is the inverse: **curing the cause IS the cure**, and the entity itself
  has no therapy and never has had one. `intervention: curative` is earned
  entirely by treating the infection and holding the organs up. So the pair spans
  the whole range — one record where aetiological cure fails to deliver clinical
  cure, one where aetiological cure *is* clinical cure and no clinical therapy
  exists. **That is the argument for the distinction, and the third record has
  arrived.**
- **#147 (the disease is a byproduct of capability) — IN ITS STRONGEST FORM,
  TWICE OVER.** First, causally: a large fraction of adult sepsis in wealthy
  countries is generated by central lines, catheters, ventilators, surgery,
  chemotherapy-induced neutropenia and transplant immunosuppression. Second, and
  worse, **arithmetically**: sepsis's eleven million deaths are *entirely*
  somebody else's. Every other record's burden is at least partly its own; this
  one's is not. Adding the record moves the register's death total from ~31M to
  ~42M and adds zero deaths to the world. **#147 said summing burden treats
  records as independent when they are not. This is the record where that stops
  being a caveat and becomes a defect.**
- **#149 (the pathogen evolves against the test) — the loop closes here.** The
  one-hour antibiotic mandate that saves septic patients drives broad-spectrum
  use into large numbers of people who are not septic, selecting the organisms in
  `cre` and `mrsa`, which cause sepsis. The Infectious Diseases Society of America
  declined to endorse the bundle for this reason. **The tie-breaker would be a
  diagnostic test and there isn't one**, so a question with a factual answer is
  settled between guideline committees.
- **#64 (strata presume the partition is observable) — and here the unobservable
  partition has a hundred-trial price tag.** The record's strata are severity
  bands because severity is what can be seen. The strata that matter are the
  endotypes, which exist in the literature and at no bedside.
- **#82 (the Mondo join can fail structurally) — third record running.** Mondo
  merges DOID, OMIM, Orphanet, NCIt and ICD, and **has no disease term for
  sepsis** — only an HPO *phenotype* and a modifier on other diseases. The
  ontology's spine is aetiology and sepsis has none of its own. `cre` failed
  because resistance crosses genera; this fails because the entity is a mode of
  dying. **Roughly one death in five worldwide has no address in the enumeration
  this register borrows from.**

---

## 154. Some interventions are infrastructure, and the register can only price products · **open**
*Forced by:* `childhood-pneumonia`.

Hypoxaemia is the strongest predictor of death in childhood pneumonia. Systematic
oxygen provision cuts mortality by roughly a third. Oxygen has been on the WHO
Essential Medicines List since 2017. **Reliable oxygen is absent from well over
half the health facilities in the regions where these children die.**

Not because it is expensive, unknown, patented, or refused. Because **oxygen is
not a product.**

| | a drug / vaccine / test | oxygen |
|---|---|---|
| unit | one course, one dose, one strip | **none — a facility has a working system or it does not** |
| procurement | buy it, ship it, donate it | buy a *plant*, then run it for twenty years |
| dependencies | a cold chain at worst | mains power, spare parts, a trained technician, a refilling chain |
| who wants it adopted | a manufacturer with a margin | **nobody** |
| failure mode | stockout — visible | **the concentrator is in the corner, broken** — invisible |

Every blocker kind the register has is a procurement concept. `cost`,
`manufacturing`, `logistics`, `no-sponsor` all presume a thing that can be
obtained. **There is no kind for "requires continuous local operation by somebody
competent", and that is what a large share of the world's remaining capability
gap actually is.**

**Two fields break, not one.**

`access` is defined as the fraction of *patients* who can obtain the
intervention. For oxygen that quantity does not exist — availability is a property
of facilities, and the patient-level number is a fiction computed backwards from
one. Same for an ICU bed (`sepsis`), a functioning microbiology laboratory
(`cre`), a blood bank (queued `maternal-haemorrhage`), an operating theatre
(queued `cataract`, `congenital-heart-disease`), and a radiotherapy machine
(several cancers).

`scale` — the blocker price — **systematically under-reads infrastructure**,
because a capital figure without an operating budget looks cheap and is the
number anybody quotes.

**COVID-19 ran the experiment and the result is in.** The global oxygen shortage
was front-page news in 2020-21, an emergency taskforce was convened, billions were
pledged, and plants and concentrators were delivered. Much of it arrived as
capital with no operating budget, no technician cadre and no power guarantee. **A
plant that is not running is indistinguishable from no plant, and it looks like
success in a procurement report.** The register would have recorded the pledge as
the blocker closing.

This is adjacent to two existing gaps and is neither:

- **#57** (the register cannot value maintenance) is about *sustaining an
  achievement* — HAT's screening programmes wound down and the disease came back.
  This is about an intervention that requires operation *before it ever works
  once*.
- **#142** (the register assumes a health system exists) is about *state
  collapse* — Yemen, Haiti, Sudan. A district hospital in Nigeria or Uttar Pradesh
  is a functioning institution with a budget, and it still has no oxygen.

The minimal fix is a blocker kind — `operations`, or a flag on `logistics` — that
distinguishes *procure it* from *run it*. The more honest fix is admitting
`access` has two denominators, patients and facilities, and the register only has
the word for one.

---

## 155. A case definition can be optimised for action rather than accuracy, and the register reads its output as burden · **open**

*Forced by:* `childhood-pneumonia`.

The WHO algorithm for childhood pneumonia is: cough or difficult breathing, plus
fast breathing for age — fifty a minute under one year, forty from one to five.
That child has pneumonia and gets amoxicillin.

It fires on bronchiolitis, asthma, malaria, severe anaemia and metabolic
acidosis, all of which cause tachypnoea. **It is not trying to be accurate.**
With a dead child on one side and a three-cent antibiotic on the other, a rule
optimised for sensitivity dominates a rule optimised for correctness, and the
people who wrote it knew exactly what they were doing.

**Then the register counts what it fires on and calls the total a disease
burden.** 140 million episodes a year is a count of an algorithm activating.
Meanwhile the PERCH study found most severe childhood pneumonia is viral, so the
*majority of the patients in the denominator do not have the disease the
numerator's treatment targets* — which makes `efficacy`, "the fraction of
patients cured", quietly incoherent.

Three things the register cannot currently say:

1. **This count is an instrument reading, and the instrument has a calibration.**
   Widen or narrow the respiratory-rate threshold and the burden moves by tens of
   millions without a child changing.
2. **The false positives are not free, and their cost lands in other records.**
   140 million paediatric antibiotic courses a year, mostly for viral illness, is
   a substantial input to `cre`, `mrsa` and `typhoid`. `toll` records what the
   cure costs *this patient* and correctly reports `minor`.
3. **The rule is right and should not be changed** until a point-of-care
   bacterial-versus-viral test exists. This is not a criticism of anyone.

Where else this bites, once the shape is named:

| rule | optimised for | what it over-calls |
|---|---|---|
| **IMCI fast breathing** | not missing a dying child | bronchiolitis, asthma, malaria, anaemia |
| **qSOFA / sepsis screening** (`sepsis`) | triggering escalation | any sick patient |
| **cancer two-week-wait referral criteria** | not missing a tumour | almost everything referred |
| **`snakebite` syndromic antivenom** (held) | not missing envenomation | dry bites |

Distinguish from two neighbours. **#133** says a definition is a *lever* — NIFTP
was renamed deliberately to stop people being treated. That is a definition
changed to cause an effect. This is a definition that **was never about accuracy
in the first place**, sitting still and being read as though it were. **#141**
says a burden figure can be negotiated; this says it can be *manufactured by a
decision rule*, which is a sharper and more common thing.

The cheap fix is a marker on `burden.cases` distinguishing *confirmed entity* from
*case-definition activations* — the register already distinguishes latent from
active infection in `tuberculosis` by prose, and this is the same problem with a
larger denominator.

---

**Strengthened by `childhood-pneumonia`, not new:**

- **#109 (prevention has no efficacy and no coverage) — AND THE `moved` ENTRY IN
  THIS RECORD IS DELIBERATELY EMPTY TO PROVE IT.** RSV is the leading cause of
  severe childhood pneumonia and had nothing against it for fifty years. In
  2022-23 **nirsevimab** and a **maternal RSV vaccine** arrived, and countries that
  introduced them reported seventy to ninety percent reductions in infant RSV
  hospitalisation in a single season. The `prevention` axis reads `prophylaxis`
  before and `prophylaxis` after. **Second record in three where a major event
  moves no axis** — `sepsis` recorded the approval and withdrawal of the only
  sepsis drug in history the same way, on `intervention`. Two different fields,
  one failure: the schema records rungs, and most of what happens in medicine
  happens between them.
- **#70 (an axis rating is the consequence of another axis's hole) — the vaccine
  line gains a fifth record, and this one has a body count.** The 1960s
  formalin-inactivated RSV vaccine caused **enhanced disease**: vaccinated children
  who later caught RSV were hospitalised more often and two died. That result
  froze RSV vaccinology for half a century, and what finally worked in 2023 was a
  *structural* insight — stabilising the pre-fusion conformation of the F protein
  — rather than an immunological one. **Nobody can still state what protective
  immunity to RSV consists of.** Tuberculosis, malaria, dengue, *S. aureus*, RSV.
- **#87 (the intervention is non-specific) — clean cooking is the cleanest instance
  yet.** Around two billion people cook over solid fuel indoors. A clean stove
  prevents childhood pneumonia, COPD, ischaemic heart disease, stroke and lung
  cancer — **five records, each rated separately, so no one record can justify the
  cost and the register cannot sum the benefit.** It also belongs to an energy
  ministry, which is #53.
- **#130 / #147 (harm lands in a different entity) — and here it lands fifty years
  later.** Severe pneumonia in early childhood lowers peak lung function and is an
  established risk factor for **chronic obstructive pulmonary disease** decades on,
  in people who may never smoke. `copd` is already a record here and a share of it
  is manufactured in this one. Two records, one causal arrow, no field.
- **#64 (strata presume the partition is observable) — third record running.** The
  partition that matters here is bacterial versus viral, it decides whether the
  treatment can work, and nothing at the point of care can see it. So the strata
  are severity bands, because severity is what a health worker can observe.

---

## 156. A death before the first breath is not counted as a death · **open**
*Forced by:* `neonatal-conditions`.

**Roughly 1.9 million stillbirths a year.** That is comparable to the 2.3 million
neonatal deaths in the same record and larger than malaria's entire toll.

They appear in **no** global mortality total. They generate **no** DALYs under
standard methodology. They were absent from the Sustainable Development Goal
indicators as originally written. **It is the largest single category of death
excluded from global health accounting**, and the exclusion is methodological
rather than accidental — a DALY values a death by years of life lost, and a
stillbirth has no birth to lose them from.

There is a real philosophical question at the boundary and this gap does not
need to resolve it. **The practical consequence is what matters, and it is
perverse:**

- The interventions that prevent stillbirth are **the same interventions** that
  prevent neonatal death — antenatal care, syphilis screening, malaria
  prophylaxis in pregnancy, intrapartum monitoring, timely caesarean section,
  skilled attendance.
- So **the benefit of that care is systematically under-counted by roughly half,
  by the very metric used to decide how much of it to fund.**
- A programme that halved both would be credited with one of the two.

This is not confined to stillbirth. The register's unit of account is a *death*
or a *case*, and several things it cares about are neither:

| the thing | why it does not count |
|---|---|
| **stillbirth** (~1.9M/yr) | no birth, therefore no life-years lost |
| **miscarriage** | same, earlier |
| maternal near-miss | survived, so not a death; permanently injured, so not nothing |
| a child who never reaches peak lung function (`childhood-pneumonia`) | the loss is a *ceiling*, not an event |

Nordstern is better placed to hold this than a burden metric is, because it
already refuses to reduce a record to one number — `residue`, `toll`, `window`
and `strata` all exist to carry things a death count cannot. **The minimal fix is
a burden field that is explicitly not a death: something like
`burden.uncounted`, with the reason stated.** The register's own rule applies —
a check that cannot run reports `skipped`, never `ok`, and a burden that is not
counted should say so rather than be absent.

---

## 157. An intervention's effect has a *sign*, and the sign can flip with the setting · **open — TWO MORE INSTANCES 2026-08-26 (`anaemia` iron-in-malaria, `cerebral-palsy` hypothermia in South Asia)**

*Forced by:* `neonatal-conditions`.

**Antenatal corticosteroids.** A dollar of dexamethasone to a mother in preterm
labour matures the fetal lung and saves the baby. It is among the best-evidenced
interventions in obstetrics. A cluster-randomised trial across six
low-and-middle-income countries, reporting in 2015, promoted its use at community
level and found **higher neonatal mortality and more maternal infection.** A WHO
trial in 2020, restricted to hospitals with adequate newborn care and confirmed
gestational age, found the expected **reduction** in neonatal death.

**Therapeutic hypothermia.** Standard of care for neonatal encephalopathy in
high-income units for two decades. A randomised trial across India, Sri Lanka and
Bangladesh, reporting in 2021, found **increased mortality.**

Two interventions, in one record, both unambiguous standard of care in a Boston
NICU, both shown by randomised trial to **kill babies** in the settings that carry
most of the deaths.

**This breaks the register's central model.** The schema is built on a division of
labour:

- `efficacy` — what medicine can do at its best. A property of the intervention.
- `access` — the fraction of patients who can obtain it. A property of a place.
- `reach = efficacy × access` — and the arithmetic assumes the first is constant
  and the second is a fraction between 0 and 1.

**If the sign flips, the multiplication is meaningless.** Half the access does not
give half the benefit; it gives *harm*. And this is not #52 (solved here, not
there), which is about a good thing failing to arrive. This is a good thing
arriving and being bad.

The mechanism is a **co-requisite capability**, and it is legible in both cases:

| intervention | requires | if absent |
|---|---|---|
| antenatal steroids | gestational dating, and newborn care for the survivors | given to term babies who are harmed; preterm survivors gain little |
| therapeutic hypothermia | intensive support during the cooling; a different injury profile | a sick baby is cooled and destabilised |

So an intervention is not a scalar with a coverage fraction. It is a **conditional**
— *if these other capabilities are present, then this much benefit; if not, this
much harm* — and the register records only the antecedent's absence, as a smaller
number.

Where else to look, once the shape is named. The pattern is: **an intervention
proven in a high-capability setting and exported on the strength of that proof.**
Oxygen without a blender or a saturation monitor blinds premature babies, and is
doing so now (the third ROP epidemic) — same record, third instance. Aggressive
fluid resuscitation in `sepsis` failed to replicate and the FEAST trial found
harm in African children. Surgical interventions generally. **Every "scale it up"
programme in global health is an implicit claim that the sign does not flip**, and
this register has no field in which that claim can be false.

Minimal fix: `efficacy` gains a companion — a `requires:` list naming the
co-requisite capabilities, so that a low `access` figure can be read as *not
reaching people* or as *reaching them without the things that make it work*, which
are different facts with opposite implications for what to fund next.

---

**Strengthened by `neonatal-conditions`, not new:**

- **#154 (some interventions are infrastructure) — SECOND RECORD, IMMEDIATELY, AND
  IN ITS PUREST FORM.** The best-return intervention here is a trained person and
  a bag-valve mask within sixty seconds of birth. The equipment costs a few
  dollars. **The constraint is that somebody who has practised the skill recently
  is standing there**, at a birth that may be at night or at home. Resuscitation
  competence decays measurably within months, so it is a recurring operating cost
  wearing the costume of a one-off intervention — #154 and #57 at once. Oxygen
  forced the gap one record ago; this confirms it is not a pneumonia peculiarity.
- **#64 (strata presume the partition is observable) — fourth record running**, and
  here the unobservable variable is **gestational age**, which decides whether the
  treatment helps or harms. A large fraction of the world's pregnancies have no
  reliable date. The register has no way to record that an *input* to a rating is
  systematically mismeasured rather than unknown.
- **The `clin·part·none` measurement profile is now three records in a row** —
  `sepsis`, `childhood-pneumonia`, `neonatal-conditions` — and that is a finding
  rather than a coincidence. **The register's diagnostic floor is concentrated in
  acute severe illness in the very young**, which is also where the deaths are.
  Thyroid cancer has an apparatus that finds disease nobody needed found; a dying
  newborn has a nurse's judgement. Worth a query, not a field.
- **#130 / #147 (harm and burden land in other entities) — this record
  manufactures at least four.** `cerebral-palsy` (queued, and explicitly the
  residue of this one), `copd` (via bronchopulmonary dysplasia — arriving at that
  record from a second direction after `childhood-pneumonia`), and via reduced
  nephron endowment and the developmental-origins literature, the queued
  `hypertension` and `chronic-kidney-disease`. **Four causal arrows out of one
  record and no field holds any of them.**
- **#48 (the register cannot rank) gains an asymmetry worth stating.** Neonatal
  deaths halved since 1990 **and their share of under-five deaths rose**, from
  roughly 40% to 47%, because deaths in older children fell faster. That is a
  general rule the register cannot express: **as a burden falls, what remains is
  the part that was hardest to prevent.** Diarrhoea and pneumonia in a
  two-year-old yield to commodities. A baby that does not breathe requires a
  competent person present at that second, which is not a commodity — and every
  remaining fraction of any burden is enriched for exactly that kind of problem.
- **#25 (one cell per entity) — the strongest strata-should-be-records case in the
  corpus.** Preterm birth, intrapartum hypoxia, neonatal infection and congenital
  anomaly share a denominator and an age band and almost nothing else: different
  mechanisms, interventions, windows and residues, and one of the four rates
  `disease-modifying` while the others rate `curative`, which is why the record
  flags ⧉.

---

## 158. The enumeration is assumed to cover the world, and for acute events it does not · **open**
*Forced by:* `maternal-haemorrhage`, after four records circling it.

Nordstern's founding rule is that **disease identifiers are borrowed, never
minted** — Mondo already enumerates the entities, so the register takes an
identifier and adds a rating. That rule is right. #133 noted it carries one
unstated assumption, that the enumeration is a *description* rather than a lever.

**Here is a second one: that the enumeration is complete.**

Mondo contains `postpartum thyroiditis`, `postpartum depression`, `postpartum
psychosis`, `postpartum amenorrhea-galactorrhea syndrome`, `Sheehan syndrome`,
`puerperal infection`, `puerperal pulmonary embolism`, and `placenta accreta`.

**It contains no term for postpartum haemorrhage** — the leading direct cause of
maternal death worldwide, roughly seventy thousand deaths a year. It has the rare
permanent sequela (`Sheehan syndrome`) and one of the causes (`placenta accreta`)
and not the thing itself.

Five consecutive records have now hit this, and the reason is the same each time
with a different surface:

| record | what is missing | why |
|---|---|---|
| `cre` | carbapenem resistance, in any genus | the spine is taxonomy; resistance crosses genera on plasmids |
| `sepsis` | sepsis, as a disease | the spine is aetiology; sepsis is a *mode of dying* |
| `neonatal-conditions` | preterm birth, stillbirth | **events**, so they exist only as HPO *phenotypes* |
| `childhood-pneumonia` | an age-scoped term | minor — joined to the parent |
| `maternal-haemorrhage` | postpartum haemorrhage | **an event**, and its rare sequela has a term |

**An ontology of diseases enumerates diseases. A great deal of what kills people
is an event, a mode, or a resistance mechanism.**

The empirical size of it, computed rather than asserted: **8 of 73 records carry
`mondo: unresolved`, and between them they account for about 11.2 million deaths
a year** — dominated by sepsis, which alone is roughly one death in five
worldwide. Three more resolve only to a grouping term with a caveat in the file
header. So **around one record in six has a compromised join, and they are
concentrated at the high-burden acute end** — precisely the part a register aimed
at "what should we work on next" most needs to be able to address.

Three things follow, in increasing order of awkwardness:

1. `mondo: unresolved` should carry a *reason code*, not just a null. "No term
   exists", "the term is a phenotype not a disease", and "resolved to a parent
   that is too broad" are different facts and only the first argues for proposing
   a term upstream.
2. **Mondo takes submissions.** The register's rule forbids minting identifiers,
   and it does not forbid *contributing* them. A register that has systematically
   found seven gaps in a public ontology has something to give back, and doing so
   is the only fix that survives.
3. If a large fraction of high-burden entities cannot be addressed in the
   borrowed namespace, then "borrow, never mint" needs an explicit escape hatch
   with provenance, rather than an `unresolved` string that reads like a to-do.

---

## 159. The entity can be a complication of a chosen physiological process · **open**

*Forced by:* `maternal-haemorrhage`.

Every record in this register up to now describes something that happened *to*
somebody. You catch an infection, you develop a tumour, you inherit a variant,
your arteries fur up. Nobody elects to get malaria.

**Pregnancy is not a disease.** It is a physiological state, usually chosen and
usually wanted, and obstetric haemorrhage is a complication of undergoing it.

That breaks two fields quietly.

**`kind` has no value for it.** `disease`, `syndrome`, `complaint` — and this is a
complication of a normal process. The record uses `syndrome` because it has
multiple causes, which is true and is not what makes it unusual.

**`prevention` means something different here, and the difference is not small.**
The axis was built to record preventing a *disease* — a vaccine, a prophylactic
drug, a bed net. Applied honestly to this record, the most powerful preventive
lever is **preventing the exposure**: over two hundred million women have an unmet
need for modern contraception, and meeting it reduces maternal deaths
arithmetically and disproportionately, because it removes the high-parity and
closely-spaced pregnancies that carry the most risk.

So `prevention: prophylaxis` covers, with one word:

- a uterotonic given to a woman who has just given birth, and
- a woman deciding not to become pregnant.

Those are not the same kind of object, and the register cannot tell them apart.
**Note carefully what this gap does and does not claim.** It is an arithmetic
observation about exposure and risk, of the same form as noting that not smoking
prevents lung cancer. It is not a claim about what anyone should choose, and the
register has no standing to make one. It is here because leaving it out would
misstate where the preventable deaths are.

Once named, the corpus has more of this than it looks, and the shape has a spine:
**an entity that exists only because somebody underwent something.**

| entity | the chosen exposure |
|---|---|
| **maternal-haemorrhage**, and maternal mortality generally | pregnancy |
| **placenta accreta** (a stratum here) | a previous caesarean — *chosen, and medical* |
| surgical complications generally | the operation |
| **road-injury** (queued) | travel |
| occupational injury and disease | the job |
| **opioid-use-disorder** (queued) | a prescription for something else |

The last two rows connect this to #147 (the disease is a byproduct of capability)
from the patient's side rather than the system's. #147 says medicine manufactures
disease; this says **some entities are the price of a life somebody is choosing to
live**, and the register's implicit frame — disease as misfortune to be reduced —
has no place to put that.

Do not build a field for this yet. Watch `road-injury`, `opioid-use-disorder` and
whichever maternal record comes next; three records with a `kind` the enum cannot
express is the threshold this register has used before.

---

**Strengthened by `maternal-haemorrhage`, not new:**

- **#128 (capability that is rationed rather than under-supplied) — ITS FLAGSHIP,
  AND IT SHOULD PROBABLY BE PROMOTED TO A FIELD ON THAT BASIS.** #128 was forced by
  `liver-cancer`, where transplant was one option among several, and it named blood
  products in its table as a secondary case. **Here blood is the binding
  constraint on the entire record.** Every other rung of the ladder — uterotonics,
  tranexamic acid, massage, a condom tied to a catheter — is cheap, off-patent,
  improvisable and works. Blood comes only from another person, expires in six
  weeks, needs a cold chain, screening, typing, and a standing institution of
  voluntary donation. **The whole distance between a maternal mortality ratio of
  12 and one of 545 sits in the last two rungs of a ladder whose first five cost
  almost nothing**, and `scale` on that blocker buys collection systems, not blood.
- **#147 (the disease is a byproduct of capability) — third record, and this one
  has a named stratum.** **Placenta accreta spectrum** occurs at the site of a
  previous caesarean scar, its incidence has risen several-fold in step with
  caesarean rates, and it causes catastrophic haemorrhage usually managed by
  planned hysterectomy. The commonest major operation in the world is generating a
  lethal complication of the *next* pregnancy. Unlike `cre` and `sepsis`, where the
  iatrogenic share is diffuse, here it is a row in the strata table with a
  fraction attached.
- **#154 (interventions that are infrastructure) — third record running**, and
  obstetrics named it first. The **three delays** model (1994) separates deciding
  to seek care, reaching a facility, and **receiving adequate care once there** —
  and the third is exactly what this register keeps recording as `access`
  succeeding. Facility birth rates rose substantially across low-income countries
  over two decades and maternal mortality fell far less than that predicts. **A
  woman who reaches a hospital with no blood in the fridge has arrived and has not
  been treated.**
- **#156 (a death that is not counted) — the mirror case, one record later.**
  Obstetrics has a term for the survivors: **maternal near-miss**, a woman who
  nearly died and did not, estimated at twenty or more per maternal death. That is
  well over a million women a year, some permanently injured, and the mortality
  statistics record the event as not having happened. #156 was about deaths
  excluded from the count; this is about **catastrophes excluded because they were
  survived**, and neither has a field.
- **The register's two highest-return unexploited interventions are now both
  cheap plastic.** `childhood-pneumonia`'s pulse oximeter and this record's
  calibrated blood-collection drape. Both convert a clinician's judgement into a
  number, both were shown in trials to produce large mortality effects — E-MOTIVE
  cut severe postpartum haemorrhage by around sixty percent — and both are
  undeployed. That is a pattern worth a query: **where does the register's
  `diagnosis` blocker mean "nobody has built it" and where does it mean "it costs
  five dollars and nobody bought it"?**
- **An intervention can be delivered and not work, and no field records it.**
  Oxytocin needs 2-8°C storage and is given in some of the hottest places on
  earth; quality surveys have repeatedly found substantial proportions failing
  assay. A woman recorded as having received prophylaxis may have received water.
  That corrupts her care *and the evidence base*, since programme evaluations run
  with degraded drug understate a real effect. Heat-stable carbetocin exists and is
  gated on price.

---

## 160. The register is a flat list and medicine is a graph · **open — flagged in three records' holes before anyone wrote it down**
*Forced by:* `diarrhoeal-disease`, after `mrsa` and `cre` each filed it as prose.

`diarrhoeal-disease` **contains** `cholera`. Not overlaps, not resembles —
contains. Ninety-five thousand of its deaths are the cholera record's deaths.
`amr-infection` likewise contains `mrsa` and `cre`, and both of those records
said so in their `holes`, in almost the same words, and neither produced a gap
number because each looked like a local awkwardness.

Three records is the threshold this register uses. **The relation is not
expressible and there are at least four kinds of it.**

| relation | instances already in the corpus |
|---|---|
| **contains** | `diarrhoeal-disease` ⊃ `cholera`; `amr-infection` ⊃ `mrsa`, `cre`; `sepsis` ⊃ most of the infectious block |
| **causes** | `h-pylori-ulcer` → `gastric-cancer`; `hepatitis-b`/`hepatitis-c` → `liver-cancer`; `hiv` → `tuberculosis`; `childhood-pneumonia` → `copd`; `neonatal-conditions` → `cerebral-palsy` (queued) |
| **is manufactured by** | caesarean → placenta accreta (a stratum of `maternal-haemorrhage`); antibiotic use in `childhood-pneumonia`/`sepsis` → `cre`, `mrsa`; `low-back-pain` → `opioid-use-disorder` (queued) |
| **is the mode of death of** | `sepsis` for a large share of every infectious record |

**Four consequences, and they are not cosmetic.**

1. **Burden cannot be summed** and the register reports a total anyway. #147
   raised this; `sepsis` made it unavoidable at 11 million wholly-borrowed
   deaths; this record adds 95,000 more. The coverage figure in `remaining.org`
   is an upper bound presented as a measurement.
2. **Blockers duplicate silently.** `cholera` and `diarrhoeal-disease` both carry
   a water-and-sanitation blocker. So do `typhoid`, `schistosomiasis`,
   `soil-transmitted-helminths` and `trachoma`. The blocker census counts six
   separate policy blockers where there is one sewer, which inflates `policy`
   and makes the census a count of *mentions* rather than of obstacles.
3. **The register cannot answer its own question.** "What should we work on
   next" over a causal graph has a correct answer — work upstream — and over a
   flat list it does not. Curing hepatitis C prevents liver cancer; eradicating
   *H. pylori* prevents gastric cancer; sanitation prevents six records at once.
   **Every one of those is invisible to a per-record ranking**, and #48 already
   says the ranking is broken for a different reason.
4. **An umbrella record's value is unmeasurable.** What does `amr-infection` add
   over `mrsa` and `cre`? What does this record add over `cholera` plus the
   pathogens it does not hold separately? Right now: nothing checkable.

**The fix is small and the register already has the machinery.** Nordstern gave
every record a permanent `FND-D-NNNN` precisely so it could be referenced. A
`relations:` block naming `contains`/`caused_by`/`iatrogenic_from` with target
ids, validated by `check.py` the way `deprecated.see` already is, would let the
build derive a graph and refuse to sum burden across a containment edge.

**Do not model it as a hierarchy.** The relations cross — `sepsis` is a mode of
death for records that also contain each other — so it is a directed graph with
typed edges, and pretending otherwise will produce a taxonomy nobody can file
into. And note that Engpass already solved the harder half of this problem for
*obstacles*: the link is stored once, in one direction, and derived the other
way. Same rule applies here.

---

## 161. The treatment can address the thing that kills you rather than the thing that bothers you · **open**

*Forced by:* `diarrhoeal-disease`.

Oral rehydration solution costs a few cents, needs no cold chain, no prescriber
and no sterile equipment, is on every essential medicines list, and is arguably
the largest life-saving intervention of the twentieth century.

**It reaches under half the children who need it, and coverage has been flat for
twenty years.**

The register would file that as `access`, and `access` is the wrong word, because
supply is demonstrably not the constraint. The reason is in what the treatment
does:

- A caregiver with a child who has diarrhoea wants **the diarrhoea to stop**.
- ORS **does not stop diarrhoea.** It replaces what the diarrhoea is taking, so
  that the child survives it.

So **the correct treatment looks like it is failing** — the stools keep coming —
and an antibiotic or antimotility agent **looks like it is working**, because the
episode ends when it was going to end anyway. Provider incentives compound it:
the first contact is often a retail drug seller whose margin is on the antibiotic
and whose satisfied customer is one whose complaint was addressed.

**The general shape: the patient's objective and the intervention's objective are
different, and adherence follows the patient's.** `efficacy` measures the
outcome medicine cares about. Nothing measures whether that outcome is the one
being sought in the room.

This is not the same as asymptomatic prevention, which is well understood and is
what the `adherence` kind was built for:

| | patient's state | what the treatment addresses | why compliance fails |
|---|---|---|---|
| statins, antihypertensives | **asymptomatic** | a future event | no felt problem to solve |
| latent TB therapy | **asymptomatic** | a future event | ditto, for months |
| **ORS** | **acutely, visibly ill** | **the lethal consequence, not the symptom** | the treatment visibly does not work |
| zinc for diarrhoea | ill, then better | the tail of the episode and the next one | the child recovers before the course ends |

**The third row is the rare one and it is much harder.** With a statin you can at
least tell someone there is nothing to feel. Here the caregiver has direct
sensory evidence, every hour, that the recommended treatment is not doing the
thing they can see needs doing — and they are right, and it is still the correct
treatment.

Two things follow for the register:

1. **`access` conflates *could not get it* with *did not use it*, and this record
   is where the conflation is total.** `access: 0.45` here is an ORS coverage
   figure that is mostly belief and incentive. A blocker kind exists —
   `adherence` — and the axis it should modify does not distinguish them.
2. **A `no-sponsor` blocker can mean *undefended* rather than *undeveloped*.**
   ORS is unpatentable, unbranded, and displaces the profitable product in the
   same retail encounter, so nobody promotes it. #145 recorded the antibiotic
   market as the one case where a medicine's value to society and to its maker
   point in *opposite* directions. **This is a second and simpler failure: not
   inverted, absent.** The kind was written for drugs nobody will develop; it is
   being used here for a drug nobody will advertise.

Where else to look: `hearing-loss` and `osteoarthritis` (queued) invert it —
there the patient's objective is symptom relief and the register's `efficacy`
has nothing to measure, which is #98 approaching the same seam from the other
side.

---

**Strengthened by `diarrhoeal-disease`, not new:**

- **#157 (efficacy is not a constant) — A SECOND MECHANISM, AND IT IS
  BIOLOGICAL.** Rotavirus vaccine efficacy is roughly 85-98% in high-income
  countries and roughly **40-60% in low-income ones**; oral polio and oral cholera
  vaccines show the same pattern. The leading explanation is **environmental
  enteric dysfunction** — the blunted, inflamed gut of a child under continuous
  faecal-oral exposure — plus maternal antibody and concurrent infection. **The
  vaccine is degraded by the conditions that make the disease lethal.**
  #157's cases were sign flips caused by *missing co-requisite capability*
  (dating, newborn care). This is magnitude attenuation caused by **the disease
  environment itself**, which no `requires:` list of capabilities would capture.
  The register defines `efficacy` as "what medicine can do at its best" — a
  property of the intervention — and here it is a property of the patient's
  village.
- **#53 / #87 (the intervention is non-specific and lives in another ministry) —
  and the trial literature adds a twist worth recording.** Water and sanitation
  is the durable answer to this record, `cholera`, `typhoid`,
  `soil-transmitted-helminths`, `schistosomiasis` and `trachoma`. **And
  household-level WASH trials have repeatedly failed to show the effects the
  historical record of sewered cities would predict.** The leading explanation is
  that partial coverage does not work — a clean latrine in a contaminated
  environment does not break transmission — which is a **threshold effect** the
  register cannot express. `access: 0.5` implies half the benefit; for
  transmission interruption it may imply none.
- **#151 (a stratum can be transformed without the record moving) — and here the
  inverse.** Persistent diarrhoea is a tenth of episodes and a wildly
  disproportionate share of deaths, is the only stratum rating
  `disease-modifying`, and has **no useful drug for its leading cause**
  (*Cryptosporidium*). The record-level `curative` averages it away, and the ⧉
  flag is the only sign anything is wrong.
- **#48 (the register cannot rank) — the cheapest unclaimed win in the corpus is
  here and is invisible.** A sachet costing a few cents, proven in 1971, is at
  45% coverage after two decades of flatness. There is no discovery to fund and
  no product to buy. Every triage view this register has sorts on fractions and
  prices, and none of them surfaces *finish the thing that already worked.*

---

## 162. The gate can cost more than the thing behind it · **open**
*Forced by:* `hepatitis-b`.

Generic tenofovir costs on the order of **thirty dollars a year** and suppresses
hepatitis B in almost everybody who takes it.

Establishing that a patient *qualifies* for it has required HBV DNA
quantification on a PCR platform, ALT repeated over months, HBeAg status, and
fibrosis staging by elastography — **a workup costing several times the annual
drug**, needing equipment most of the burden cannot reach, repeated indefinitely
for the half of patients told to come back in six months.

So in most of the world **"not eligible" and "not assessable" produce the same
outcome**, and the outcome is no treatment. About 3% of infected people receive
the drug.

The register files that under `access`, which is wrong in an instructive way.
`access` means *the fraction who can obtain the intervention*, and here the
intervention is cheap and available. **What cannot be obtained is permission.**

Three things this makes visible:

1. **Eligibility criteria are a rationing instrument in clinical costume.** They
   are written as a statement about who benefits, they function as a statement
   about who gets treated, and when the assessment is unavailable the criteria
   default to exclusion rather than to inclusion. Nothing in the schema
   distinguishes a criterion that selects from one that rations.
2. **Simplifying the gate is a therapeutic act, and the register cannot record
   one.** WHO's 2024 hepatitis B guidelines expanded eligibility on the explicit
   reasoning that **a simpler rule treats more people even if it treats some who
   would not have benefited** — a deliberate trade of precision for coverage. That
   moved more patients toward treatment than any drug has since tenofovir, and it
   moves no axis in this register.
3. **The precedent is one record over and the register already half-noticed it.**
   Hepatitis C once required genotyping to choose a regimen; pan-genotypic
   direct-acting antivirals abolished the question, and Nordstern records that as
   `predictive: n/a` — *a measurement question closed by a better treatment.* Same
   phenomenon, opposite direction: there the treatment removed the gate, here the
   guideline lowered it.

Where else the shape appears:

| record | the gate | the thing behind it |
|---|---|---|
| **hepatitis-b** | PCR, elastography, serial ALT | $30/yr generic |
| **hepatitis-c** (held) | genotyping — **abolished** | 12 weeks of DAAs |
| **cre** (held) | molecular carbapenemase panel | the correct beta-lactam |
| **childhood-pneumonia** (held) | a bacterial/viral test that does not exist | 3¢ of amoxicillin |
| **sickle-cell**, thalassaemia | confirmatory genotyping | hydroxyurea |

Minimal move: a blocker sub-kind, or a flag on `diagnosis`, marking **the test as
a gate rather than as information** — because the two have opposite fixes. An
informational gap wants a better test. A gate wants a cheaper rule.

---

## 163. A prevention that works can abandon the people already infected · **open**

*Forced by:* `hepatitis-b`, with `chagas` as the second record and `hiv` as the
control that proves it is not inevitable.

The hepatitis B vaccine is one of the great achievements in this register — the
first vaccine against a human cancer, ~95% effective, and new chronic infections
have collapsed wherever the birth dose reaches.

**Two hundred and fifty-four million people are already infected**, almost all of
them infected before the vaccine reached them, and **about 3% are on a
thirty-dollar-a-year generic** that would prevent a large share of their deaths.

**Prevalence is a stock. Vaccination acts on the flow.** The two numbers move
independently, attention follows the flow, and the stock dies quietly over the
following forty years in a record called something else — cirrhosis, or liver
cancer.

The register has the pair to prove this is a pattern and the control to prove it
is a choice:

| record | prevention that worked | prevalent cohort | reach |
|---|---|---|---|
| **hepatitis-b** | vaccine, 1982 | 254M infected | **0.08** |
| **chagas** | vector control | ~6M infected, >90% never diagnosed | **0.03** |
| **hiv** | PrEP, PMTCT, treatment-as-prevention | ~39M infected | **0.72** |

**HIV is the same shape of problem** — chronic virus, no cure, lifelong
suppression, cheap generics, stigma, silent for years — and it delivers roughly
twenty-five times better. It was not biologically easier. It got an emergency
framing, dedicated financing at PEPFAR and Global Fund scale, sustained patient
activism, price negotiation conducted as a public campaign, and named
international targets that governments were measured against.

**Hepatitis B got a vaccine and was filed as handled.**

So the gap is not "prevention causes neglect" — HIV has excellent prevention and
excellent treatment. It is that **a prevention that is dramatic enough to change
the incidence curve can substitute, in the mind of a funder and of a register,
for the question of what happens to everybody already carrying the disease.**

What Nordstern should be able to say and cannot:

- **Incidence and prevalence trends are different facts and the register stores
  neither.** `burden` holds a level. A record whose incidence is collapsing and
  whose prevalent cohort is untreated looks identical to one where nothing is
  happening.
- **`prevention` and `intervention` are already independent axes** — this record
  is the register's cleanest demonstration of it, since hepatitis B and C are
  mirror images on the two. The derivation reads them together for `capability`.
  Nothing reads them for *this*: a strong prevention beside a barely-delivered
  treatment is a specific and actionable configuration, and it is invisible.
- The other direction is worth watching too: **`hepatitis-c` has a cure and no
  vaccine**, so its prevalent cohort is the one being cleared while new infections
  continue. Opposite failure, same missing field.

Candidates to check: post-polio syndrome, silicosis and asbestos-related disease
(exposure stopped, exposed cohort still presenting), congenital rubella, and
whichever tobacco-attributable record is examined after prevalence peaks.

---

**Strengthened by `hepatitis-b`, not new:**

- **#160 (the register is a flat list and medicine is a graph) — this record is a
  *cause*, and its deaths are filed under its effects.** Hepatitis B kills through
  cirrhosis and hepatocellular carcinoma. `liver-cancer` is held and already
  carries `prevention: prophylaxis` — **which is this record's vaccine, showing up
  in a different file.** The queued `cirrhosis` will do the same. Three records,
  one causal chain, and the only thing linking them is prose.
- **#141 (the burden figure can be negotiated) — the prevalence was revised down
  by tens of millions and nobody recovered.** From roughly 296 million to roughly
  254 million, by a change in modelling. That is the largest single burden
  revision in the corpus and it happened to a chronic-infection count that reads
  as though it were measured.
- **#154 (interventions that are infrastructure) — fourth record running, and the
  same room as the second.** Birth-dose coverage is ~45% against ~85% for the
  infant series that follows it. The later doses are scheduled clinic visits; the
  birth dose requires somebody with a vaccine and a cold chain **at the birth**,
  which is precisely `neonatal-conditions`' bag-valve-mask constraint at the same
  moment. Every missed birth dose creates a chronic carrier who needs lifelong
  treatment or dies of liver cancer around 2065.
- **An intervention whose *interruption* is more dangerous than its absence, and
  no field records it.** Stopping a nucleos(t)ide analogue causes viral rebound and
  in a substantial minority a severe hepatitis flare, occasionally fatal. So a
  patient who starts and then hits a stockout is worse off than one who never
  started — which makes supply-chain reliability part of the treatment rather than
  an implementation detail. `hiv` shares this and nothing else held here does.
  `ongoing: moderate` cannot say it.
- **#25 / #151 (record-level scalars average away the strata) — and here half the
  patients rate `intervention: none`.** The middle stratum is the standard of care
  being *deliberate non-treatment with indefinite monitoring*, its size is a
  guideline judgement that already moved once in 2024, and the record-level
  `suppressive` conceals that half the prevalent population is receiving nothing
  at all. The ⧉ flag is the only signal.

---

## 164. The register holds interventions, not the capabilities that produce and evaluate them · **open**
*Forced by:* `covid-19`.

Two of the largest returns of the pandemic were not treatments.

**The mRNA platform.** Sequence published January 2020, authorised vaccine
December 2020 — eleven months against a prior record measured in decades. The
decisive move was organisational: phases in parallel, manufacturing at risk. What
came out of it is not a COVID intervention. It is **a machine for making
vaccines**, now aimed at RSV, influenza, and cancer.

**The RECOVERY trial.** An adaptive platform embedded in a health system, with a
consent process short enough to use on a breathless patient. It found
dexamethasone — a sixty-year-old generic costing pennies, cutting mortality by a
third — in three months, and **ruled out** hydroxychloroquine, lopinavir-ritonavir,
azithromycin, colchicine and convalescent plasma. Meanwhile hundreds of
underpowered trials elsewhere answered nothing and consumed the patients who could
have answered something.

**The difference between a health system that can run a trial and one that cannot
was worth more than any molecule discovered during the pandemic.**

Neither is expressible here. The register's unit is *a disease*, and its `blockers`
ask what stands in the way of **this** entity. A capability that would move forty
records at once has no record to belong to, so no record argues for it and the
triage views cannot see it.

The corpus is full of these once you look:

| capability | records it moves |
|---|---|
| **mRNA / platform vaccine design** | covid-19, childhood-pneumonia (RSV), influenza (queued), and whatever spills over next |
| **adaptive platform trials** | sepsis's hundred failures, neonatal-conditions' exported sign flips, me-cfs's absent evidence base |
| **pre-fusion antigen stabilisation** | RSV *and* SARS-CoV-2 — the same structural trick produced both |
| **genomic + wastewater surveillance** | covid-19, h5n1, cre, typhoid, measles |
| **gene editing** | sickle-cell, and the queued genetic block entire |
| **a method for silencing episomal genomes** | hepatitis-b's cccDNA *and* hiv's latent reservoir |

`tooling` exists as a blocker kind and is the closest thing, but it is scoped the
wrong way round — it says *this record lacks a tool*, never *this tool would
unlock those thirty*.

**Engpass is the right home and its schema already almost fits.** Its obstacle
kinds include `tooling` and `capability`, its whole purpose is the
many-to-many link, and its stated value is answering *what does solving this
unblock*. What is missing is that Nordstern blockers currently point at obstacles
only from `knowledge` blockers in practice — the `obstacles:` field is available
on any kind and is barely used elsewhere. **Tagging `tooling` and
`evidence-incomplete` blockers into shared Engpass obstacles would make
cross-cutting capability visible without any new field in Nordstern at all.**

That is the cheapest fix in this file and it is a data-entry job, not a schema
change.

---

## 165. Surveillance is a capability that can be switched off, and its loss erases its own evidence · **open**

*Forced by:* `covid-19`.

COVID-19 was measured more intensively than any disease in history. PCR within
days of the sequence, at-home antigen tests distributed by the billion, genomic
sequencing at a scale that let variants be named as they emerged, wastewater
monitoring, and daily national reporting.

**This register cannot state its current annual death toll within an order of
magnitude**, and neither can anybody else. Free testing ended, reporting became
voluntary or stopped, sequencing volumes collapsed, wastewater programmes were
defunded. **The instruments all still work. Almost nobody runs them and almost
nowhere reports the result.**

Every individual decision was defensible. The emergency ended; surveillance at
pandemic intensity is not a permanent condition; the money was needed. The
aggregate is that the world switched off its ability to know.

**Three properties make this different from every other measurement gap in the
corpus.**

1. **It is a loss, not an absence.** `burden-unknown` in Engpass collects eleven
   records where nobody ever built the counting — HAT, scabies, Buruli ulcer,
   yaws. This is the only one where it was built, at extraordinary cost, and then
   dismantled. #57 says the register cannot value *maintenance* of a control
   programme; this is maintenance of the **instrument**, which is worse, because
   the instrument is what tells you whether the programme is needed.
2. **The loss is self-concealing.** A dismantled surveillance system removes the
   signal that would demonstrate it was needed. The evidence for rebuilding can
   only arrive as a surprise, by which point the argument is moot. **You cannot
   measure the loss of measurement**, and no register whose inputs are measurements
   can detect this from the inside.
3. **Its value mostly belongs to other records.** Sequencing, wastewater and
   excess-mortality monitoring are what would detect the *next* pathogen. `h5n1`
   is in this register precisely as a threat rather than a burden, and its entire
   argument depends on surveillance existing. So this is #164's shape again — a
   capability whose beneficiaries are records that do not exist yet.

**What the register should be able to say and cannot:** that `diagnostic:
objective` describes a test that exists and is not being run. **Fifty-seven of
seventy-six records carry an `objective` diagnostic rating** — three quarters of
the corpus — and nothing distinguishes one in routine national use from one that
is technically available and operationally extinct.

The minimal move is a modifier on `measurement.diagnostic` — *in use* versus
*available* — which would also catch `hepatitis-b` (a one-dollar test, 13%
diagnosed) and `chagas` (cheap serology, >90% never diagnosed). **Three records,
same shape: the test is not the problem and the rating says it is fine.**

---

**Strengthened by `covid-19`, not new:**

- **#157 (an intervention's sign can flip) — AND THIS IS THE MORE COMMON FORM.**
  RECOVERY found dexamethasone cut mortality by roughly a third in ventilated
  patients, about a fifth in those on oxygen, and showed **a trend toward harm in
  patients not requiring oxygen at all.** Same drug, same disease, same week — the
  sign flips with the **stage**, because early disease is viral replication and
  late disease is the immune response to it. #157's cases were sign flips across
  *settings* (antenatal steroids, therapeutic hypothermia). Flipping across
  *stages of the same illness in the same patient* is likely commoner and is
  entirely invisible to an `efficacy` scalar.
- **#105 (prevention has costs and `toll` cannot hold them) — the best-quantified
  instance medicine has ever produced.** Myocarditis after mRNA vaccination,
  concentrated in young males after dose two; vaccine-induced immune thrombotic
  thrombocytopenia after adenovirus-vector vaccines, rare, often fatal, and it
  changed national programmes. Both were detected within months by
  pharmacovigilance working exactly as designed, both are vastly outweighed by
  benefit, and **the register has nowhere to put either.** Treating quantified
  vaccine harms as unrecordable is how a register loses the readers who most want
  it to be honest.
- **#160 (the register is a flat list) — long COVID poured patients into three
  existing records.** A substantial share of long COVID patients meet ME/CFS
  criteria; POTS is a documented post-COVID outcome; MCAS is asserted as one. All
  three are held, all three sit under Engpass's `unexplained-illness`, and nothing
  connects them to this record. **And the arrow runs both ways** — COVID handed the
  ME/CFS field the thing it never had, a known index infection at population scale
  with prospective follow-up, at a price nobody would have chosen.
- **#91 (the register cannot show a trajectory) — three axis moves in eighteen
  months.** `intervention` symptomatic → disease-modifying (June 2020) → curative
  (December 2021), and `prevention` none → prophylaxis (December 2020). Nothing
  else in the corpus has moved that fast and the register shows only a sequence of
  dated states, never a rate.
- **#141 (the burden figure can be negotiated) — three numbers, factor of four.**
  ~7 million reported, ~15 million excess for 2020-21 alone, modelled figures into
  the mid-20-millions through 2022. Excess mortality needs no test, which makes it
  both more reliable and more arguable, since it counts deaths caused by the
  response as well as by the virus.
- **#144 / #66's open half (things done TO populations) — the largest instance in
  the register and it is entirely absent from every axis.** Distancing,
  ventilation, masking and closures were the dominant intervention for a year.
  They were administered to populations rather than patients, their costs landed
  on education, employment and mental health rather than on any patient, and
  **this record would rate identically if none of it had happened.**

---

## 166. A rating can be a distribution redrawn every cycle, and the register stores a scalar · **open**
*Forced by:* `influenza`.

WHO selects the strains for the northern hemisphere's influenza vaccine in
**February**, for a season beginning in **October**, because manufacturing half a
billion doses takes that long. The vaccine's composition is therefore a
**prediction** about which variants will be circulating six months later.

Vaccine effectiveness follows: roughly **40-60% in a well-matched season, and as
low as about 20% in a badly-mismatched one.** Same technology, same delivery
system, same population — different draw.

**There is a second, independent way for it to miss.** Most vaccine is grown in
embryonated chicken eggs, and the virus adapts to the egg during manufacture,
acquiring haemagglutinin substitutions that improve yield and degrade the match.
So the product can fail because the virus moved *after* selection, or because the
virus changed *during production*.

**Every rating in this register is stored as a state.** `efficacy: 0.35`.
`access: 0.30`. The whole apparatus — `reach = efficacy × access`, the delivery
bands, the triage views — treats those as properties that hold until something
changes them.

**Influenza's are random variables with an annual redraw, and any single number is
a lie about a distribution.**

Two specific things break:

1. **`moved` presumes a ratchet.** Every `moved` entry in this corpus records a
   state change that *persists* — isoniazid, the vaccine, BPaLM, tranexamic acid.
   Influenza's effectiveness has no ratchet. It oscillates around a mean that has
   not improved much in decades. **The field designed to make a second pass a
   comparison cannot describe a record whose value is re-rolled before the
   comparison happens.**
2. **The variance is the actionable quantity, not the mean.** A vaccine that is
   reliably 45% effective and one that alternates between 20% and 60% have the
   same mean and demand different responses — the second is an argument for
   shortening the manufacturing lead time, which is exactly this record's
   `manufacturing` blocker. **The register can express the mean and not the thing
   worth fixing.**

Where else the shape appears, once named:

| record | what is redrawn | on what cycle |
|---|---|---|
| **influenza** | vaccine match | annual, by committee, six months ahead |
| **cre**, **mrsa** (held) | whether empirical therapy covers the organism | continuously, locally |
| **snakebite** (held) | whether the available antivenom matches the species | per region, per bite |
| **malaria** (held) | whether the ACT partner drug still works | slowly, and one-way |

The last row is the contrast that makes the point: malaria's is **degradation**
(#146) — one-way, cumulative, and a `moved` entry describes it fine. Influenza's
is **oscillation**, and nothing describes it.

Minimal move: allow a scalar to carry a range or a variance alongside its value,
and mark ratings whose value is re-established on a cycle. `range: [0.2, 0.6]`
would say more about influenza vaccine than any point estimate can.

---

## 167. Missing evidence and withheld evidence look identical here, and have opposite fixes · **open**

*Forced by:* `influenza`.

Oseltamivir was licensed from 1999 and stockpiled by governments at a cost of
billions of dollars — the United Kingdom alone spent several hundred million
pounds — on the strength of published summaries of trials whose **full clinical
study reports the sponsor did not release.**

A campaign by the BMJ and Cochrane reviewers ran from 2009 until the reports were
obtained. The 2014 analysis of the complete data found about **seventeen hours**
of symptom reduction in adults, no support for the claimed reduction in
hospitalisation, insufficient evidence on complications, and more nausea and
vomiting than the summaries had shown.

**This record's `intervention` rating is `symptomatic` because of that analysis.
On the evidence available in 2009 it would have been `disease-modifying`, and it
would have been wrong for fifteen years — not because anyone had failed to do the
research, but because the research had been done and was being held.**

The register cannot express the difference:

| | `evidence-incomplete` means | what it should mean here |
|---|---|---|
| the trials | were never run, or were too small | **were run, competently, at scale** |
| the answer | does not exist | **exists and was not released** |
| the fix | fund a trial | **disclosure, regulation, litigation** |
| who could move it | academic, sponsor, philanthropy | **regulator, legislator** |

Every scalar in this register carries a `src`. None of them can say *this number
comes from a trial whose full report was never published*. And `standing` —
`documented` / `alleged` / `disputed` / `refuted` — describes how well a
**blocker** is established, not how well the evidence behind a **rating** is.

**Two consequences.**

*The register can be confidently wrong, at scale, with no internal signal.* This
is the failure mode it was built to prevent. `src: recall` at least announces
itself. A rating derived from selectively published trials looks exactly like a
well-founded one.

*The fix is a cross-cutting capability, so no record argues for it.* Trial
registration, results-reporting mandates, and access to clinical study reports
belong to no disease — they are #164's problem again, and they are incompletely
implemented, with substantial proportions of registered trials still not
reporting results within required timeframes.

Where else to look, and it is not a historical curiosity: **`depression` (held)**
is the other famous case, where the published antidepressant literature was
materially more favourable than the full regulatory dataset. Any record whose
efficacy figure rests on industry-sponsored trials is in scope, which is most of
the therapeutic corpus.

Minimal move: a value on `src` — or a flag beside it — distinguishing *published
summary* from *full data available*. It would be uncomfortable to fill in
honestly, which is the argument for it.

---

**Strengthened by `influenza`, and one prediction refuted:**

- **#149 (the pathogen evolves against the intervention) — THE QUEUE PREDICTED
  THIS RECORD WOULD BE ITS SIBLING AND THE BIOLOGY DOES NOT SUPPORT IT.**
  `remaining.org` listed influenza and covid-19 as carrying "the sibling case —
  antigenic drift is evolution against the *vaccine*". **It is not.** Antigenic
  drift is driven by immune selection in the human population as a whole, and that
  immunity is overwhelmingly from natural infection: global seasonal vaccine
  coverage is low and reaches a minority even where programmes are best funded.
  Vaccine-driven escape is theoretically real and is not the dominant force.
  **Influenza drifts because people have had influenza, and it would drift almost
  as fast if no vaccine existed.** Malaria's HRP2 deletions remain the clean case,
  because there the selection pressure *is* the intervention. Recorded because a
  register that only confirms its own predictions is not measuring anything.
- **#157 (an intervention's sign can flip) — THIRD VARIANT, AND THE VARIABLE IS
  NOW THE PATHOGEN.** Corticosteroids reduce mortality in severe COVID-19 and are
  associated with **increased** mortality in severe influenza — same drug, same
  clinical picture of viral pneumonia progressing to ARDS, same chest radiograph,
  opposite sign. #157's original cases flipped with **setting** (antenatal
  steroids, therapeutic hypothermia); `covid-19` added flipping with **stage**
  (dexamethasone early versus late); this flips with **which virus it is.** Three
  distinct axes of flip in four records suggests the underlying fact is that
  `efficacy` is not a property of an intervention at all.
- **#57 (the register cannot value maintenance) — as a permanent operating
  condition rather than as a risk.** A global surveillance network, two
  strain-selection meetings, half a billion doses manufactured and an entire
  vaccination campaign, **every year, forever, to hold a position that cannot be
  consolidated.** HAT's version was an achievement that decayed when funding
  stopped. This one can never be finished at all, and the register has no way to
  distinguish a job that is done from one that is being redone annually.
- **#54 (single points of failure) — with an unpleasant feedback loop.** Influenza
  vaccine manufacture depends on embryonated chicken eggs. A severe avian
  influenza panzootic — which is `h5n1`'s subject — threatens the egg supply on
  which the response to it depends.
- **#160 (the flat list) — twice in one record.** Influenza deaths are certified
  as pneumonia, heart failure or old age, and the sixfold elevation of myocardial
  infarction risk in the week after infection puts a real share of them inside
  `ischaemic-heart-disease`. And the register splits seasonal from pandemic
  influenza across this record and `h5n1`, so **neither holds the thing that
  matters most: the seasonal programme IS the pandemic programme's standing
  capability** — same surveillance, same manufacturing base, same antiviral class.
- **Two records now rate the same intervention differently on purpose, and nothing
  flags it.** `h5n1` rates neuraminidase inhibitors `disease-modifying` on
  observational survival data in a disease that kills half its cases; this record
  rates them `symptomatic` on randomised data in healthy adults. Both are
  defensible. A reader comparing the two axes has no way to know the disagreement
  is deliberate.

---

## 168. `efficacy` is a fraction of patients, and some interventions shift a trajectory in everybody · **open**
*Forced by:* `alzheimers`.

Lecanemab slows cognitive decline in early Alzheimer's by roughly **27%** — an
absolute difference of **0.45 points on an 18-point scale** over eighteen months.

**What fraction of patients does it work in?**

The question has no answer. There is no responder subgroup. Everybody in the
treatment arm declined; they declined slightly less. `efficacy: 0.25` on that
record is a number I made up to satisfy a field, and the units string says so.

**The schema's definition is *fraction-of-patients*, and it is load-bearing** —
`reach = efficacy × access` multiplies two proportions, the delivery bands are
cut on the product, and `orphaned` and every triage view read it. That
arithmetic is coherent for interventions with a binary outcome per patient:

| shape | example | fraction is meaningful |
|---|---|---|
| cured / not cured | `hepatitis-c`, `cre` | **yes** |
| survived / died | `sepsis`, `maternal-haemorrhage` | **yes** |
| suppressed / not suppressed | `hiv`, `hepatitis-b` | **yes** |
| **everybody's trajectory bends a little** | **`alzheimers`** | **no** |

And the fourth row is not rare. It is most of chronic medicine: statins and LDL,
antihypertensives and blood pressure, disease-modifying therapy in multiple
sclerosis, riluzole in ALS, nearly everything the queued `hypertension`,
`type-2-diabetes` and `chronic-kidney-disease` records will contain. **The
register has been forcing continuous effects into a proportion and hiding the
conversion inside a prose units string.**

Two things are lost by the forcing, and the second is worse:

1. **The effect size disappears.** A drug that halves decline and one that slows
   it by five percent can be given the same fraction by whoever writes the record.
   Nothing constrains the choice.
2. **The comparison to the minimal clinically important difference is
   unrepresentable.** That is the whole argument about this drug class — a real,
   statistically robust effect that is **smaller than the smallest difference
   anybody thinks is noticeable.** A register whose purpose is "what should we
   work on next" cannot afford to lose the distinction between *works a little*
   and *works imperceptibly*.

Minimal move: let `efficacy` carry a second shape — an effect size with its
comparator, or explicitly `n/a` with the trajectory described — the way
`measurement.predictive` already accepts `n/a` for a question that does not
apply. Deriving `reach` would then have to refuse rather than multiply, which is
the correct behaviour and the register already has the pattern: **a check that
cannot run reports `skipped`, never `ok`.**

---

## 169. The carer is a second patient with no field anywhere in the schema · **open**

*Forced by:* `alzheimers`.

Dementia costs something over **a trillion dollars a year**, and roughly **half of
that is unpaid care by family members** — valued by imputation, paid by nobody,
appearing in no health budget.

That is the largest single quantity attached to any record in this register, and
it belongs to **people who do not have the disease.**

It is not only money. Carers of people with dementia have measurably higher rates
of depression and anxiety, worse physical health, worse sleep, reduced income and
pension contributions from leaving employment, and — in several cohorts —
elevated mortality. A carer is typically a spouse of similar age, so the burden
lands on somebody who is themselves old, or on a daughter in her fifties.

**Every field in this schema is scoped to the patient.** `toll` is what the cure
costs *them*. `residue` is what the disease leaves in *them*. `ongoing` is the
cost of being treated, to *them*. `burden` counts *their* deaths.

The corpus has been circling this for a long time without naming it:

| record | who else pays |
|---|---|
| **alzheimers** | ~half a trillion dollars a year of unpaid family care |
| **cerebral-palsy** (queued) | a lifetime of it, starting at birth |
| **maternal-haemorrhage** | the household of a woman who dies at 24 |
| **neonatal-conditions** | the parents of a child with permanent impairment |
| **me-cfs**, **heds** (held) | families providing care the health system does not |
| **schizophrenia** (queued) | the same, with stigma attached |

**And there is a specific consequence for triage, which is this register's
purpose.** Interventions aimed at the carer — respite, support programmes, paid
family leave, care coordination — have real evidence behind them, cost far less
than an anti-amyloid antibody, and **cannot be argued for anywhere in this
schema**, because they do not improve any axis of any record. A register that
cannot see them will systematically recommend the drug.

Note the asymmetry with #159 (the entity is a complication of a chosen process)
and #117 (the toll can land on a person who does not exist yet). Those are about
*harms* landing outside the patient. This is about **the disease's ongoing burden
being borne outside the patient as a matter of routine**, at a scale that dwarfs
the formal health system's share.

Minimal move: `ongoing` gains a second value, or a `carer_burden` block — scale,
who, and whether anything is provided. It would be filled in for perhaps a dozen
records and it would change what those records recommend.

---

**Strengthened by `alzheimers`, not new:**

- **#123 (the ladder is ordered by finality, not by value) — A SECOND CASE, AND IT
  RUNS THE OPPOSITE WAY.** #123 was forced by `cml`, where a `curative` option
  (transplant) killed a substantial fraction and a `suppressive` one (imatinib)
  was better for almost everybody — the higher rung was worse. **Here the higher
  rung is a fortnightly $26,000 infusion producing a slowing of decline below the
  threshold anybody perceives, with a one-in-four rate of brain oedema, and the
  lower rung is a cheap generic tablet producing a small improvement a family can
  sometimes see.** `disease-modifying` outranks `symptomatic` because it addresses
  the pathology, which is a claim about mechanism wearing the costume of a claim
  about benefit. Two records, opposite directions, same defect.
- **#148 (toll is judged against the alternative and recorded as absolute) — its
  sharpest case yet, and the third in six records.** A one-in-four rate of brain
  oedema is tolerated because the alternative is a disease that dismantles a
  person over eight years and nothing else touches it. **If a genuinely effective
  treatment arrived, these agents would be withdrawn within a year and nothing
  about the molecules would have changed.** Colistin forced the gap; tuberculosis's
  aminoglycosides sharpened it; this is the version where the comparator is not a
  better drug but the absence of hope.
- **#90 / #133 (who counts as a patient; a definition is an instrument) — the
  largest stroke-of-the-pen expansion in the corpus.** The 2024 Alzheimer's
  Association criteria define the disease **biologically**, so an asymptomatic
  amyloid-positive person has Alzheimer's; the International Working Group
  dissented. Perhaps a third of cognitively normal over-75s are amyloid-positive.
  One definition makes tens of millions of well people patients.
- **#162 (the gate costs more than the thing behind it) — inverted, and therefore
  unfixable by the usual route.** For `hepatitis-b` a $30 generic sat behind an
  expensive assessment, so simplifying the gate rescues it. **Here the gate and
  the thing are both expensive** — PET or CSF, APOE genotyping, serial MRI, an
  infusion suite, and a $26,000 drug. The p-tau217 blood test cleared in 2025 may
  collapse the gate by an order of magnitude and touches nothing else.
- **And the ordering of arrivals is the worst possible one.** A cheap accurate
  blood test for a biologically-defined disease, in a population where a third of
  the cognitively normal are positive, is an overdiagnosis engine of exactly the
  kind `prostate-cancer` and `thyroid-cancer` document — **arriving before the
  treatment is clearly worth having.** The register should be able to flag *a
  diagnostic advancing ahead of a therapeutic* as a risk state, and cannot.
- **#129 (prevention can be unintentional, and the largest examples are) —
  possibly the largest example.** Age-specific dementia incidence has **fallen** in
  several high-income countries over recent decades while total cases rise with
  ageing. Nobody prescribed it. The leading candidates are blood pressure control
  and education. The Lancet Commission's fourteen modifiable factors — with
  **hearing loss the largest single contributor**, and `hearing-loss` a queued
  record here — put a claimed 45% of dementia in reach of things that are not drugs.

---

## 170. An early-acting treatment pulls the disease definition backwards in time · **open — SIX RECORDS, AND `heart-failure` WROTE IT INTO A GUIDELINE (Stages A and B). STOP WAITING; BUILD IT.**
*Forced by:* `type-1-diabetes`, one record after `alzheimers` did the same thing.

Teplizumab delays clinical type 1 diabetes by about two years. It only works
**before** the disease arrives, in people with islet autoantibodies and
dysglycaemia and no symptoms.

So type 1 diabetes was restaged. **Stage 1** is two or more autoantibodies with
normal glucose. **Stage 2** adds dysglycaemia. **Stage 3** is what everybody used
to mean by "having diabetes." A child in Stage 1 has type 1 diabetes and can eat
whatever they like.

Alzheimer's did the same thing in the same three years and for the same reason.
Anti-amyloid antibodies work only in early disease, so the 2024 criteria define
Alzheimer's **biologically** — amyloid and tau positivity is the disease,
symptomatic or not.

**Two records, two fields, one causal arrow: the drug's requirements moved the
definition upstream.**

This inverts #133, and the inversion is the point. **#133** (forced by
`thyroid-cancer`) says a definition is a *lever* — NIFTP was deliberately renamed
so that people would stop being treated, a definition changed **to change
treatment**. Here **treatment changed the definition**, and nobody decided to; it
followed from what the molecule could do.

What follows is not symmetric between the two records, and the register should be
able to tell them apart:

| | `type-1-diabetes` | `alzheimers` |
|---|---|---|
| progression if untreated | **~85% within 15 years** with multiple autoantibodies | a substantial share **never become impaired** |
| so the new "patients" are | almost all genuinely pre-symptomatic | **partly people who would have died well** |
| overdiagnosis risk | low | **high, and #90's shape exactly** |
| what is missing | a screening programme nobody runs | a reason to want the answer |

**Both create a population of asymptomatic people with a disease name**, and the
register has one `prevalence` field, no way to mark a stage as preclinical, and
no way to say whether the redefinition was epistemically earned.

Three consequences worth separating:

1. **`burden.prevalence` silently changes meaning.** Nine million people have
   type 1 diabetes; an unknown and much larger number have Stage 1 or 2 and are
   not counted because nobody screened them. The number is now a function of
   testing effort.
2. **`window` acquires a segment that opens before symptoms**, which the field
   handles by accident rather than design — `window` was built for *catching it
   in time*, and this is *catching it before it starts*.
3. **A licensed therapy can have almost no eligible patients** because the
   population it treats is defined by a test nobody runs. That is #162's gate
   with the price removed: **the gate is cheap and simply is not opened.**

Watch for the third case. The pattern — an early-acting drug forcing a
biological restaging — is likely to repeat wherever a disease has a long
preclinical phase and a treatment that only works in it. Parkinson's and
prodromal disease is the obvious candidate and is queued.

**AMENDED 2026-08-26 — the third, fourth and fifth arrived, and the named
candidate has been held since record 87.** Five records cite this gap:
`type-1-diabetes` (forcing), `atrial-fibrillation`, `multiple-sclerosis`,
`rheumatoid-arthritis`, and **`parkinsons`** — whose record describes one of the
strongest prodromes in medicine, with idiopathic REM sleep behaviour disorder
converting to Parkinson's or dementia with Lewy bodies in around three quarters of
those who have it, and anosmia and constipation preceding tremor by years. **It
is the case this paragraph asked for, it was written three days after the
paragraph, and the paragraph still says "is queued."**

The prediction in it was correct and should be recorded as such: the pattern does
repeat wherever a disease has a long preclinical phase and a treatment that only
works inside it. **Five records is not a pattern to watch for. It is a field that
has not been built**, and the register has now rated five diseases whose
`burden.prevalence` silently means different things depending on how hard anyone
looked.

---

## 171. `ongoing` measures how much the treatment demands, not what kind of demand it is · **open**

*Forced by:* `type-1-diabetes`, the record the rung was named for.

`ongoing` has four values — none, low, moderate, high — and within the
`suppressive` rung the corpus already uses three of them:

| record | ongoing | what is actually demanded |
|---|---|---|
| **hiv** | `low` | **one tablet a day** |
| **cml**, **hepatitis-b** | `moderate` | a tablet plus periodic monitoring |
| **pku** | `high` | **a lifelong restrictive diet** |
| **crohns** | `high` | flares, immunosuppression, unpredictability |
| **type-1-diabetes** | `high` | **a continuous computation, roughly 180 decisions a day, with seizures at one end and blindness at the other** |

Three of those are `high` and they are not the same problem. And the difference
is not severity — it is **kind**, which determines what could possibly fix it:

- **A pill** needs supply. Fix: a reliable supply chain.
- **A diet** needs food products, counselling, and a household that cooperates.
  Fix: money and support. Nobody can automate it.
- **A continuous decision** needs the decisions made. **Fix: an algorithm.**

**And that last one actually happened, which is why this is a gap and not a
complaint.** Automated insulin delivery is exactly an algorithm making the
judgments the patient was making. It improved control *and* cut severe
hypoglycaemia simultaneously — something no amount of patient effort had ever
achieved, because the constraint was never effort. It is the clearest case in the
register of an `ongoing` burden being **engineered away rather than endured**,
and the register records it only as `efficacy` going up.

**The register also cannot see who did it.** From about 2013, patients and
parents reverse-engineered pump protocols and built open-source closed-loop
systems — running them on their own children — years before any manufacturer
would connect components that had all existed for a decade. A randomised trial of
an open-source system published in 2022 found it worked. `who_could` has
`patient-org`; nothing records that the patients were the ones who built the
standard of care.

Minimal move: `ongoing` gains a **type** alongside its magnitude — supply,
regimen, restriction, decision-load, surveillance — so that a record can say
*this burden is automatable and nobody has automated it*, which is a research
programme rather than a lament. `chronic-kidney-disease` and `asthma` are queued
and will both need it.

---

**Strengthened by `type-1-diabetes`, not new:**

- **#123 (the ladder is ordered by finality, not by value) — third record in three,
  and this time the higher rung HIDES the progress.** Teplizumab is the first
  therapy in a century to alter the underlying autoimmune process, and it **cannot
  raise this record's `intervention` rating**, because `suppressive` (insulin)
  already outranks `disease-modifying` by construction. So a genuine first is
  invisible to the axis. `cml` showed the ladder ranking a worse option higher;
  `alzheimers` showed it ranking an imperceptible benefit above a perceptible one;
  this shows it **unable to record a new kind of progress at all** because the
  existing rung is already above it.
- **#154 (interventions that are infrastructure) — in a chronic disease, and it is
  education.** Structured self-management education has evidence comparable to
  some technologies, changes outcomes, is staff time rather than a product, and is
  chronically unfunded. Also: insulin without a way to measure glucose is not
  treatment, so `access` here is a conjunction of four things — drug, cold chain,
  measurement, teaching — any one of which nullifies the rest.
- **#162 (the gate) — with the price removed, which is a new variant.** For
  `hepatitis-b` the gate was expensive; for `alzheimers` the gate and the drug were
  both expensive. Here **autoantibody screening is cheap and simply is not run**,
  so a licensed disease-modifying therapy has almost no eligible patients. The
  fix is not a cheaper test. It is deciding to look.
- **`toll` and `efficacy` are coupled and the schema stores them as independent.**
  Severe hypoglycaemia is the treatment's harm; fear of it causes people to run
  their glucose deliberately high; that produces the retinopathy and nephropathy
  twenty years later. **The treatment's toll causes the disease's complications**,
  and no field connects them. Anticoagulation and bleeding, and opioid
  undertreatment of pain, are the same shape.
- **#48 (the register cannot rank) — and here is a burden figure it cannot hold at
  all.** Modelling estimates roughly **3.9 million people "missing"** from the
  world's type 1 diabetes prevalence: alive if they had received care available
  since 1922, and dead. It is a *prevalence deficit*, not a mortality count, and it
  is the single most useful number about this disease. `burden` has fields for
  deaths, cases and prevalence, and nothing for **the people who are not here.**
- **#145's inverse.** `mrsa` recorded the antibiotic market as the case where a
  medicine's value to society and to its maker point in opposite directions. Insulin
  is the case where **the discoverers gave it away for a dollar each to prevent
  exactly what happened anyway** — an off-patent century-old molecule with no
  generic competition until the 2020s, reaching list prices that made a quarter of
  American patients ration it. Not a market failure of neglect: a market with
  three participants and a hundred-year head start.

---

## 172. The entity can be defined by a surrogate that the best treatments bypass · **open**
*Forced by:* `type-2-diabetes`.

Type 2 diabetes is defined by a glucose threshold. HbA1c 6.5% was chosen because
that is roughly where diabetic retinopathy prevalence inflects — a defensible
cut on a continuum, and a choice.

**Three facts about the treatments then follow, and together they say the
definition is not the harm.**

- **The drugs that reduce cardiovascular death and slow kidney disease do not do
  it through glucose.** SGLT2 inhibitors and GLP-1 receptor agonists produce
  effects too large and too early to be explained by their HbA1c reduction, and
  the SGLT2 benefit holds in people **without diabetes.** They are heart failure
  and kidney drugs that arrived through a diabetes indication.
- **A drug that lowered glucose well was withdrawn for cardiovascular harm.**
- **Driving the defining biomarker down hard killed people.** The ACCORD trial's
  intensive glycaemic arm was stopped early for excess mortality.

So for fifty years the field optimised the variable the disease is named for, and
the agents that turned out to save lives work around it.

**This is #63 one level up, and the distinction matters.** #63 (forced by
`soil-transmitted-helminths`) says the **`efficacy` field** can measure what the
drug does to the pathogen rather than whether the patient is helped — a
measurement problem inside a record. **This says the entity's own defining
criterion is the surrogate**, so the measurement problem is upstream of every
record, every trial endpoint and every guideline built on it.

The register inherits the confusion in a specific place. `efficacy` asks whether
the treatment works. For fifty years "works" meant lowering HbA1c. A register
written in 2005 would have recorded high efficacy for rosiglitazone.

**Where to look for others** — the test is: *is the entity named for a number,
and is that number the thing that hurts you?*

| entity | defined by | is the definition the harm? |
|---|---|---|
| **type-2-diabetes** | HbA1c / glucose | **no** — the harm is vascular, and the best drugs bypass glucose |
| **hypertension** (queued) | blood pressure | **closer to yes** — lowering it is the benefit |
| osteoporosis | bone density | **partly** — some agents raise density without preventing fractures |
| **alzheimers** (held) | amyloid and tau, since 2024 | **unresolved, and that is the whole argument** |

The last row is the live one. Alzheimer's has just been redefined by biomarkers
(#170), and whether removing amyloid helps is precisely the dispute — **the same
structure as diabetes in 1998, before ACCORD.**

Minimal move: mark whether an entity's diagnostic criterion is a **surrogate** or
the **harm itself**, and require `efficacy` to state which one it measures. The
register already forces `units` to be a sentence; this is one more clause in it.

---

## 173. `curative` has no durability, and cures have half-lives · **open**

*Forced by:* `type-2-diabetes`.

The intervention ladder defines `curative` as **a finite intervention ends it.**
It is a boolean rung, and the corpus has been quietly using it for at least three
different things.

Type 2 diabetes remission: three to five months of total diet replacement,
producing normal HbA1c off all medication in **46% at one year, 36% at two, and a
small fraction at five.** Metabolic surgery holds it better — durable remission
in roughly a third at fifteen years.

Hepatitis C: twelve weeks, >95%, and it does not come back.

**Both rate `curative` and they are not the same claim.**

| record | what "cured" means | half-life |
|---|---|---|
| **hepatitis-c**, **h-pylori-ulcer** | the pathogen is gone | **permanent** (barring reinfection) |
| **childhood-all**, most cancers | no detectable disease at five years | **a convention** — breast cancer relapses at twenty |
| **type-2-diabetes** | a physiological state, maintained | **a few years, decaying** |
| **cml** | not claimed — rates `suppressive`, correctly | — |

**Oncology's version is the one to be most careful about**, because "cure" there
is a statistical convention that the register imports as a rung. Five-year
survival is a reporting standard, not a biological claim, and hormone-receptor-
positive breast cancer recurs at fifteen and twenty years — after the register has
recorded it as cured and the patient has been discharged.

Three things follow:

1. **`efficacy` is doing double duty and hiding the decay.** This record's 0.35
   is the *durable* remission fraction rather than the initial one, chosen by the
   author. Nothing in the schema required that choice or records that it was made.
2. **A cure that decays and a treatment that must be continued are closer than the
   ladder admits.** Maintained remission in type 2 diabetes is lifelong work with
   no drug to be adherent to — `curative` on the ladder, `suppressive` in the
   patient's life. **#123 says the ladder is ordered by finality rather than
   value; this says the finality itself is often unmeasured.**
3. **A pharmacological way to *hold* a remitted state would convert a decaying
   cure into a stable one**, and that is a research programme the register cannot
   currently express, because it has no field for the difference.

Minimal move: `intervention: curative` gains a durability — a horizon over which
the cure has been demonstrated, or `permanent` where the mechanism makes relapse
impossible. It is one more scalar and it would separate hepatitis C from a
twelve-week diet with a five-year decay curve.

---

**Strengthened by `type-2-diabetes`, not new:**

- **#171 (`ongoing` measures how much, not what kind) — confirmed one record later,
  and here both kinds are in ONE record.** The `suppressive` route is a **regimen**
  — tablets, appointments, a supply problem. The `curative` route is a
  **restriction, permanently**, maintained by the patient with no drug to be
  adherent to. Same disease, same file, one enum value. The gap was written at
  `type-1-diabetes` on a comparison *between* records; this is the same split
  *inside* one.
- **#154 (interventions that are infrastructure) — and this is the sharpest
  version yet, because the thing that cannot be procured is the CURE.** What
  produced 46% remission was total diet replacement plus structured support plus
  a maintenance year, delivered by dietitians and nurses. **No product exists.**
  Every previous instance of #154 was a delivery constraint on a treatment; here
  the register's most striking capability finding — that this disease can be ended
  — is gated entirely on staff time, the thing this register has learned it is
  worst at buying.
- **#87 / #53 (the intervention is non-specific and lives in another ministry) — at
  the largest scale in the corpus.** The drivers are food price and availability,
  built environment, and how much of the day is spent sitting. The best population
  evidence is for taxation, reformulation and marketing restriction — finance,
  agriculture, trade and planning. The benefit spreads across this record, the
  queued `hypertension`, `cirrhosis` and `chronic-kidney-disease`, and the held
  `ischaemic-heart-disease`, `stroke` and several cancers. **`who_could` still has
  no finance ministry.**
- **#90 (who counts as a patient is a threshold somebody chose) — over a billion
  people.** "Prediabetes" is defined differently by the American Diabetes
  Association and the World Health Organization, and the wider band labels well
  over a billion adults. None are in this record's prevalence. Whether they belong
  is unresolved and the schema offers no way to hold the question.
- **#160 (the flat list) — this record's deaths are almost entirely in other
  records.** People with type 2 diabetes die of cardiovascular disease and kidney
  failure. `ischaemic-heart-disease` and `stroke` are held, `chronic-kidney-disease`
  is queued, and the 3.4 million figure here is an attribution across all of them.
- **The `undelivered` artefact, second record running.** Like `alzheimers`, this
  derives a very low reach because `efficacy` and `access` describe the *best*
  capability — remission — while hundreds of millions receive `suppressive`
  therapy that does not set the rung. The axes are working exactly as designed and
  the row reads wrongly at a glance. **Two records in three now show it, which
  makes it a presentation defect rather than a coincidence.**

---

## 174. `access` cannot say you got the worse version of the treatment · **open**
*Forced by:* `chronic-kidney-disease`, which contains the only natural experiment
the register has on what happens when access is solved.

In 1962 Seattle had more dialysis candidates than machines and convened an
anonymous lay committee to decide who was treated, on criteria including
employment and dependants. *Life* magazine published it. The reaction is widely
credited as a founding event of modern bioethics, and in 1972 the United States
extended Medicare to **end-stage renal disease regardless of age** — the only
disease-specific universal entitlement in American health care, and still the
only one.

**So one record in this register has had its `access` figure legislated to nearly
one. Here is what happened.**

Spending grew to roughly seven percent of Medicare's fee-for-service budget for
about one percent of beneficiaries. And **outcomes did not become the world's
best.** United States dialysis survival trails several peer countries. Home
dialysis is a small minority where other systems use it for most patients.
Transplant rates are lower than organ supply permits.

`reach = efficacy × access` predicts that solving access solves the record. **It
did not, because everybody got the worse version of the treatment.**

The register's `access` is effectively binary — obtained or not — and for a
disease with several tiers of the same intervention, the tier is worth more
life-years than the fraction:

| record | got *an* intervention | got the *right* one |
|---|---|---|
| **chronic-kidney-disease** | dialysis | **transplant**: better survival, better life, cheaper after two years |
| same again | in-centre haemodialysis | **home dialysis or peritoneal**: cheaper, better tolerated, a minority almost everywhere |
| **type-2-diabetes** (held) | metformin | **a remission programme**, offered to almost nobody |
| **alzheimers** (held) | a cholinesterase inhibitor | arguable, and that is #123's problem |
| **sepsis** (held) | antibiotics | antibiotics **in the first hour** |

Three consequences:

1. **A high `access` figure can conceal the entire problem.** A record reading
   `access: 0.95` looks solved and may be systematically delivering the third-best
   option. Nothing in the schema distinguishes them.
2. **The fix is different in kind.** Raising access means supply, money and
   logistics. Improving the modality mix means referral pathways, reimbursement
   design and clinician behaviour — and in `chronic-kidney-disease` the incentive
   points the wrong way, which is #124's annuity problem doing the selecting.
3. **This is the strongest argument in the corpus against the register's own
   headline arithmetic.** `reach` is the number every triage view sorts on, and
   here it would have declared victory in 1973.

Minimal move: `access` gains a companion — a modality mix, or simply a flag that
the intervention has tiers and which one is modal. `chronic-kidney-disease`,
`type-2-diabetes` and `sepsis` would all fill it in today.

---

## 175. The measuring instrument can encode a population correction that changes who gets treated · **open — AMENDED 2026-08-25 (`obesity`); the direction of effect decides, not the presence of the term**

*Forced by:* `chronic-kidney-disease`.

Kidney function is not measured. It is **estimated by an equation** from serum
creatinine, age and sex — and from 1999 until 2021 the standard equations also
contained a **coefficient for Black race**, which raised the estimated filtration
rate by around sixteen percent.

The effect was mechanical and one-directional: Black patients' kidneys looked
healthier than they were. Later nephrology referral. Later transplant
waitlisting, in a system where waiting time accrues from listing. A large share
reclassified into a less severe stage than their kidneys warranted. A national
task force removed it in 2021, and studies of the change found meaningful numbers
of patients becoming eligible for referral and for the transplant list **with no
change in their kidneys.**

**Every measurement gap in this register so far has been about a test that does
not exist, does not reach people, or has been evolved against.** This is a
different thing: **the test exists, reaches people, works — and has a term in it
that decides who is treated.**

It is not confined to one equation, and one of the others is a device this
register has twice called among its cheapest unexploited interventions:

| instrument | the correction | consequence |
|---|---|---|
| **eGFR equations** | a race coefficient, 1999-2021 | delayed referral and transplant listing |
| **pulse oximetry** (`childhood-pneumonia`, `covid-19`) | none, but **accuracy varies with skin pigmentation** | occult hypoxaemia missed several times more often in dark-skinned patients — and oxygen is the binding constraint in both records |
| **spirometry** | race correction, removed 2023 | altered thresholds for diagnosis and for occupational compensation |
| clinical risk calculators | race and ethnicity terms | altered eligibility for procedures |

**The pulse oximeter row is the one that should worry this register most**, because
it has no correction at all — the bias is physical, in how light passes through
pigmented skin, and the register has recommended the device twice on the strength
of an `objective` diagnostic rating that is not equally objective for everybody.

Two things the schema cannot say:

- **`measurement.diagnostic: objective` is a claim about a test, and a test can
  be objective and unequal.** Sixty-two of eighty-one records carry that rating
  and none of them qualifies it.
- **An instrument can be the blocker.** The register's `diagnosis` blocker kind
  means the test is missing or unreachable. Here the fix was deleting a term from
  an equation — it cost nothing, took two decades, and is invisible to every
  field.

The minimal move is small and awkward: a flag on `measurement` that the
instrument's performance is known to vary by population, with the direction
stated. It would be filled in for few records and it would be the first thing a
reader of those records needs to know.

**AMENDED 2026-08-25 by `obesity`, and the amendment is load-bearing — this entry
as first written would have got the next case wrong.**

Body mass index carries **lower action points for Asian populations** — around 23
and 27.5 rather than 25 and 30 — because the same BMI corresponds to more visceral
fat and higher cardiometabolic risk where body composition differs. **That
correction was examined and kept.** The kidney equation's race coefficient was
examined and removed. Same structural feature, opposite verdict:

| | eGFR race coefficient | BMI Asian action points |
|---|---|---|
| the term | race, standing in for muscle mass | ethnicity, standing in for body composition |
| direction | **raised** apparent function → **delayed** referral and transplant listing | **lowered** the threshold → **earlier** intervention |
| better non-social measure exists? | **yes** — cystatin C | **yes** — waist circumference, direct adiposity |
| verdict | **removed, 2021** | **retained** |

So "the instrument contains a population term" is **not** the finding, and a flag
that only says that would argue for deleting both. Three questions separate them:

1. **Does the term track something measurable, or is it a social category standing
   in for one?** Both are proxies — this alone does not decide it.
2. **Which way does it move care for the group it applies to?** This is the one
   that did the work in both cases.
3. **Is there a non-social measure that would make the proxy unnecessary?** Where
   there is — cystatin C, waist circumference — the honest answer is to use it and
   retire the term either way.

The amended minimal move: the flag records the term, **its direction of effect**,
and whether a direct measure exists — not merely that a correction is present.

---

**Strengthened by `chronic-kidney-disease`, not new:**

- **#124 (a cure is a one-time sale and a suppression is an annuity) — ITS
  CLEAREST CASE, AND THE ANNUITY IS WINNING.** Transplantation is better for the
  patient and cheaper for the payer after about two years. In-centre dialysis is
  billed three times a week for years and, in several countries, delivered by
  consolidated for-profit chains. Transplant rates vary several-fold between
  countries with comparable donation rates. **Nobody has to intend a bad outcome
  for the incentives to select one.**
- **#128 (rationed rather than under-supplied) — and here the two kinds sit side
  by side, which sharpens the gap.** Kidneys are genuinely capped: a transplant for
  one patient is not available to another, and no money makes more. **Dialysis is
  not capped by anything physical** — machines can be built and nurses trained —
  and between 2.3 and 7.1 million people die each year for want of it. Same record,
  same organ, one constraint that money cannot move and one that is purely money,
  and `access` reports a single fraction over both.
- **#140 (the patient may rationally choose the worse outcome) — and here it is
  routine, supported and planned.** Withdrawal from dialysis precedes something
  like a fifth of dialysis deaths in several national registries. Conservative
  kidney management is a recognised pathway with guidelines. **A significant number
  of people find this treatment worse than the death it prevents**, and the
  register reads their decision as `access` failing.
- **#171 (`ongoing` measures how much, not what kind) — a FOURTH kind, one record
  after the gap was written.** Supply, regimen, restriction, decision-load — and now
  **time**, taken in twelve-hour blocks out of a working week, indefinitely.
  `type-1-diabetes`'s decision load was automated away by an algorithm. **Nothing
  automates this: the thing that gives the time back is a transplant, and there
  are not enough kidneys.**
- **#147 (the disease is a byproduct of capability) — and this record is
  downstream of half the register.** Two thirds of CKD is caused by diabetes and
  hypertension; a further share by nephrotoxins medicine supplies in quantity —
  NSAIDs, aminoglycosides, contrast, calcineurin inhibitors, several of which this
  register has recommended elsewhere.
- **`prognostic: good` — one of only twelve records, and the tool is exactly what
  this register keeps saying does not exist.** The Kidney Failure Risk Equation
  predicts an individual's two- and five-year probability of kidney failure from
  four routine variables, validated across more than a million patients in dozens
  of countries. **Worth studying rather than just recording**: it is cheap,
  individual, actionable, and it is the counter-example to the corpus's dominant
  finding that prognosis is a population statement.
- **The register has no field for climate or occupation, and CKDu needs both.**
  Chronic kidney disease of unknown aetiology kills young agricultural labourers in
  Central America and Sri Lanka, has resisted twenty years of investigation, and
  its leading hypothesis is **recurrent heat stress** — which makes it the clearest
  climate-attributable signal in the corpus. `who_could` has no labour ministry.
  Climate appears in this entire gaps file once.

---

## 176. `residue.permanent` is a boolean, and some damage regresses if the cause is removed in time · **open**
*Forced by:* `cirrhosis`.

The textbook position for a century was that cirrhosis is irreversible. **It is
not.** Cure hepatitis C and fibrosis regresses over years, including from
established cirrhosis. Suppress hepatitis B, stop drinking, or lose substantial
weight in metabolic liver disease, and the same happens — stellate cells
deactivate, collagen is degraded, function returns. Some decompensated patients
recompensate and come off the transplant list.

**Up to a point.** Past a threshold of vascular remodelling and portosystemic
shunting the distortion is fixed, and regression stops being available.

`residue` records `permanent: true` or `permanent: false`. **Both are wrong
here**, and the record had to write a paragraph in a units string to say so.

**The residue has its own window**, and the register's `window` field is about
capability changing with timing — not about *damage already done* becoming
undoable if you act soon enough. Those are different claims and the second one is
worth more, because it changes what early treatment is for:

- If residue is permanent, treating early **prevents further damage.**
- If residue regresses, treating early **also recovers damage already present.**

The register counts only the first, so **it systematically under-values early
intervention in every record where the second is true** — and it is true more
often than the corpus currently admits:

| record | residue | regresses? |
|---|---|---|
| **cirrhosis** | fibrosis | **yes, before the vascular threshold** |
| **cirrhosis** | hepatocellular carcinoma risk after cure | **no** — surveillance for life |
| **type-2-diabetes** (held) | albuminuria | partly, with control |
| heart failure | cardiac remodelling | **yes**, reverses on treatment |
| **tuberculosis** (held) | post-TB lung damage | **no** |
| **neonatal-conditions** (held) | retinopathy blindness, cerebral palsy | **no** |
| **childhood-pneumonia** (held) | lowered peak lung function | **no** — a ceiling, not a lesion |

**Note that cirrhosis contains both answers**, which is why one boolean per record
cannot work even in principle: the fibrosis regresses and the cancer risk does
not, in the same patient, from the same disease.

Minimal move: `permanent` becomes three-valued — `yes` / `no` / **`if-caught`**,
with the threshold named. It is one enum widening, and it would let the register
say the thing that most changes what a health system should do: *find these
people early and some of the damage undoes itself.*

---

**Strengthened by `cirrhosis`, and one gap is now ready to build:**

- **#110 (the register cannot record that the patient is blamed) — ITS FLAGSHIP
  ARRIVED, IT NAMED THIS RECORD BY NAME WHILE QUEUED, AND THE CASE IS WORSE THAN
  IT ASSUMED. BUILD IT.**
  #110 was forced by `lung-cancer`, where blame is **diffuse**: less research
  funding per death, lower screening uptake, being asked whether you smoked. It
  listed "cirrhosis (queued) — alcohol, and transplant eligibility is explicitly
  gated on it" as a future case.
  **Here the blame is operational.** A written eligibility criterion — six months
  of documented abstinence — applied to a named individual, with a mortality
  consequence measured in a trial. Severe alcohol-associated hepatitis kills
  roughly three quarters of patients inside the waiting period, so the rule
  excluded most candidates by killing them. Early transplantation produces
  something like 94% six-month survival against about 11% with medical management.
  **The distinction is not cosmetic, because it determines the fix**:

  | | diffuse blame | operational blame |
  |---|---|---|
  | example | `lung-cancer` research funding | `cirrhosis` transplant eligibility |
  | mechanism | attitudes, aggregated | **a written rule** |
  | visible? | only in statistics | **in a protocol document** |
  | fix | culture, advocacy, time | **change the criterion** — and a trial can force it |

  And there is a structure worth naming that #110 did not have: **a rule justified
  on clinical grounds and functioning on moral ones is only falsifiable on the
  clinical claim.** The six-month rule's stated basis was prognostic. Refuting the
  prognostic claim did not remove the rule, because the prognostic claim was never
  why it was there — which is why practice shifted slowly after 2019 and has not
  shifted everywhere. **#110 asked whether to build a blocker kind or a
  record-level field. Build the record-level field, and give it the diffuse /
  operational distinction**, because only one of the two can be fixed by a trial.
- **#175 (the instrument encodes a population correction) — CONFIRMED ONE RECORD
  LATER, WITH A DIFFERENT VARIABLE AND HIGHER STAKES.** The kidney equation carried
  a race coefficient that delayed referral. **MELD carries creatinine, which
  reflects muscle mass, so a woman in identical renal failure scores lower than a
  man, ranks lower for a liver, and dies waiting more often.** MELD 3.0 added a sex
  adjustment in 2023 to correct it. The kidney instrument delayed care; **this
  instrument IS the allocation mechanism** — it does not advise the queue, it is
  the queue. Two records, two instruments, two population terms, both corrected in
  the last five years. It was not a one-off.
- **A pattern in `prognostic: good` worth reporting rather than filing.** Twelve
  of eighty-two records rate `good`, and most are trivial — rabies is uniformly
  fatal, Huntington's is genetic, smallpox is eradicated. **The two non-trivial
  individual predictors in the whole corpus are MELD and the Kidney Failure Risk
  Equation, and both exist because a scarce thing had to be handed out.** That
  suggests prognostic accuracy in medicine tracks *whether a decision forced it*
  rather than whether the biology is knowable — which is an actionable claim: if
  you want better prognosis, create a decision that requires one.
- **#39 (an entity can be a final common pathway) — fourth record.** Fibrosis with
  regenerative nodules, reached from hepatitis B, hepatitis C, alcohol, metabolic
  dysfunction, autoimmune and biliary disease. Mondo concedes it by holding
  `alcoholic liver cirrhosis` and `hepatitis C induced liver cirrhosis` as separate
  terms alongside the parent. #39 was marked **BUILD IT** at `sepsis`; this is
  further confirmation and the aetiologies here are individually *solvable*, which
  makes the missing partition costlier than usual.
- **#160 (the flat list) — this record is downstream of five held or queued
  records and upstream of one.** `hepatitis-b`, `hepatitis-c`, `type-2-diabetes`,
  and the queued `alcohol-use-disorder` and `obesity` flow in; `liver-cancer` flows
  out. **And the causal mix has changed completely within one generation** — viral
  falling because two records were solved, alcohol and metabolic rising — so every
  blocker in the file would have been a different blocker in 1995 and the schema
  stores one undated snapshot.
- **Two records now rate transplantation differently on purpose.**
  `chronic-kidney-disease` rates it `suppressive`; this rates `curative`. The
  argument is real — a kidney recipient still has chronic kidney disease by
  definition, on a graft with reduced filtration, while a liver recipient does not
  have cirrhosis because the cirrhotic liver was removed. **Both defensible,
  nothing flags that the disagreement is deliberate** — the third instance of this
  after `influenza`/`h5n1` on neuraminidase inhibitors.
- **#171 (`ongoing` measures how much, not what kind) — a FIFTH kind: surveillance.**
  A cured hepatitis C patient with cirrhosis needs six-monthly ultrasound for life,
  because the cancer risk does not go with the virus. **Nothing is being treated.
  Somebody is being watched** — and it is the same shape as `hepatitis-b`'s
  untreated half, told to come back in six months forever.

---

## 177. The benefit and the harm can land in the same other entity, in opposite directions · **open**
*Forced by:* `atrial-fibrillation`.

Anticoagulation for atrial fibrillation prevents roughly two thirds of
AF-related **ischaemic strokes**. It causes **intracranial haemorrhage** at
roughly 0.3-0.5% a year, which kills about half of the people it happens to.

Both of those are strata of `stroke`, which is held in this register:

| `stroke` stratum | fraction | rating | what AF's treatment does to it |
|---|---|---|---|
| ischaemic stroke | 0.65 | `disease-modifying` | **prevents many** |
| intracerebral haemorrhage | 0.27 | **`symptomatic`** | **causes some** |

So one record's intervention moves two strata of a second record in **opposite
directions** — and it converts a preventable, partly treatable stroke into the
stratum where least can be done.

**This extends #130 rather than repeating it.** #130 (forced by `gastric-cancer`)
says an intervention's *harm* can land in a different entity: mass *H. pylori*
eradication pays for itself in `amr-infection`. That is one arrow. Here the
benefit and the harm land in the **same** other record, and the net effect is a
subtraction neither file can perform:

- `atrial-fibrillation` records `efficacy: 0.70` and `toll: major`. Neither
  number is about atrial fibrillation.
- `stroke` records its own strata and cannot see that a third of its ischaemic
  cases have a preventable upstream cause, or that some of its haemorrhagic cases
  were manufactured preventing them.

**And it is not a curiosity — it is the commonest structure in cardiovascular
medicine.** Every antithrombotic decision is this shape, and the corpus already
contains several:

| intervention | prevents (in another record) | causes (in another record) |
|---|---|---|
| **anticoagulation for AF** | ischaemic stroke | **intracerebral haemorrhage** — same record |
| antiplatelets after MI | reinfarction | GI and intracranial bleeding |
| thrombolysis in stroke | infarct extension | haemorrhagic transformation — **same record, same patient** |
| **immunosuppression** (`cirrhosis`, `chronic-kidney-disease`) | graft loss | malignancy, and CKD from calcineurin inhibitors |

The minimal move is the one #160 already proposed — typed edges between records —
with one addition: **the edge needs a sign.** `prevents` and `causes` are the
same relation with opposite polarity, and a record can carry both to the same
target.

Until then, the register's most quantified everyday risk-benefit decision is
invisible to it, and the number that actually governs practice — expected strokes
prevented minus expected bleeds caused, per patient — exists in neither file.

---

## 178. Prognostic quality is a property of the decision, not of the disease · **open**
*Forced by:* `atrial-fibrillation`, confirming a pattern visible at
`chronic-kidney-disease` and `cirrhosis`.

Fourteen of eighty-three records rate `prognostic: good`. **Most of them
are trivial.** Rabies is uniformly fatal. Huntington's is genetic and the repeat
length predicts onset. Smallpox is eradicated. Dracunculiasis resolves. Cholera's
prognosis is a function of how dehydrated you are.

**Strip those out and three non-trivial individual prognostic instruments remain
in the entire corpus:**

| record | instrument | the decision that forced it |
|---|---|---|
| **chronic-kidney-disease** | Kidney Failure Risk Equation | when to refer, when to build a fistula, when to list |
| **cirrhosis** | MELD | **who gets the liver** |
| **atrial-fibrillation** | CHA₂DS₂-VASc | anticoagulate or not, with harm on both sides |

Two were forced by **scarcity** — something had to be allocated. One was forced by
**two-sided harm** — the choice could not be deferred and both answers hurt
somebody. None was forced by the biology being unusually tractable, and
CHA₂DS₂-VASc in particular has a c-statistic around 0.6-0.7, which would be
unremarkable in a research paper and is nonetheless deciding treatment for tens
of millions of people.

**The register reads `prognostic` as a fact about the disease. It is mostly a fact
about the decision architecture around the disease**, and the two readings imply
opposite work:

- If `prognostic: none` means the biology is opaque, the answer is research.
- If it means **nobody ever had to choose**, the answer is to create the choice —
  and the prognostic tool follows, as it did three times above.

That reframing is testable and it is actionable. `sepsis` rates `prognostic:
partial` with a hundred failed trials behind it and no forced allocation decision;
`me-cfs` rates it low with no decision at all. Meanwhile the field that had to
hand out livers built the best-validated score in medicine.

**It also explains a puzzle in the corpus.** This register has repeatedly
concluded that prognosis is a population statement and never a patient one, and
has treated that as a fact about medicine. It is better read as a fact about
**what medicine has been obliged to answer.**

Minimal move: record, alongside `prognostic`, whether a **forcing decision**
exists. It is one field, it is knowable from the record, and it converts a
lament into a research strategy.

---

**Strengthened by `atrial-fibrillation`, not new:**

- **#160 (the flat list) — the strongest instance yet, because this record has
  almost no content of its own.** Atrial fibrillation is frequently asymptomatic,
  rarely kills directly, and is important entirely because it causes a fifth to a
  third of ischaemic strokes. Its `deaths` field is close to meaningless in
  isolation and the record says so. **It has no `residue` block, because what AF
  leaves behind is a stroke and the disability belongs to `stroke`.** An entity
  whose burden, harm and benefit are all filed elsewhere.
- **#157 (an intervention's effect depends on stage) — and here it overturned a
  settled guideline rather than a marginal one.** A large trial in 2002 found no
  advantage to rhythm control over rate control and set eighteen years of
  practice. A trial in 2020 randomised patients **within twelve months of
  diagnosis** and found reductions in cardiovascular death, stroke and
  hospitalisation. Same intervention, opposite conclusion, and the variable was
  *when*. #120's proposed `how:` vocabulary would need a value for **we learned
  when, not what.**
- **#170 (an early-acting treatment pulls the definition upstream) — RUNNING
  BACKWARDS, WHICH IS THE USEFUL CONTROL.** For `alzheimers` and
  `type-1-diabetes`, a drug that worked only early dragged the disease definition
  into the presymptomatic phase. **Here the detector moved first**: wearables and
  implantable monitors found large amounts of short-duration, device-detected
  atrial fibrillation — and the treatment did not follow. A loop-recorder trial
  found three times as much AF, tripled anticoagulation, and **did not
  significantly reduce stroke**; two trials of anticoagulating subclinical AF
  netted out close to neutral. **A definition can be pulled upstream by a
  diagnostic and leave the therapeutics behind**, which is the failure mode
  `alzheimers` was warned about and this record is already living in.
- **#148 (toll judged against the alternative) — amiodarone.** The most effective
  antiarrhythmic available causes thyroid disease in both directions, pulmonary
  fibrosis, hepatotoxicity, corneal deposits and permanent skin discolouration,
  and is prescribed anyway because the alternatives work less well. **Here the
  comparator is not death — it is an arrhythmia**, which makes it the mildest
  comparator yet to justify a toll this size.
- **An asymmetry of attribution the register cannot hold, and it costs half the
  eligible patients their treatment.** A patient who bleeds on a drug you
  prescribed presents to you and is attributed to you. A patient who has the
  stroke you did not prevent is a counterfactual — invisible, unattributed, never
  presented as your decision. **The two harms are not weighted equally by the
  person choosing, and the error always points the same way.** `access: 0.45` in
  that record is mostly this, and the axis cannot distinguish it from a supply
  failure.

---

## 179. The entity can be a risk factor rather than a disease, and every field assumes a disease · **open — IT NAMED `osteoporosis` BEFORE THE RECORD EXISTED AND WAS RIGHT; HELD 2026-08-26**
*Forced by:* `hypertension`.

Raised blood pressure is the leading single risk factor for death worldwide —
around **10.8 million attributable deaths a year, more than any disease in this
register.**

**Essentially none of them is a death from hypertension.** They are strokes,
myocardial infarctions, heart failure, kidney failure and dementia, filed in
`stroke`, `ischaemic-heart-disease`, `chronic-kidney-disease` and records still
queued.

Hypertension has no symptoms, no natural history of its own beyond the rare
malignant form, and no lesion. **It is a number above a line in a person who
feels well.** And the schema, built for diseases, produces a series of technically
correct and substantively empty answers:

| field | what it says for `hypertension` | why it is empty |
|---|---|---|
| `burden.deaths` | 10.8 million | **all counted in other records** |
| `residue` | absent | the disease leaves nothing — its *consequences* are other entities |
| `restored` | **`restored`** | derives cleanly and means nothing |
| `toll` | `minor` | correct, and it is a pure subtraction from someone who felt fine |
| `kind` | `disease` | it is not one, and there is no other value |

**This is not the same as #90**, which was forced by `ischaemic-heart-disease` and
says the *threshold* is a committee choice on a continuum. That record has a
disease — plaque, infarction, a lesion you can see — and #90 is about where the
line goes. **Here there is no disease at either side of the line.** Nobody has "a
case of hypertension" the way they have a case of ischaemic heart disease.

The corpus has more of these and the queue holds several:

| entity | the number | the disease is elsewhere |
|---|---|---|
| **hypertension** | blood pressure | stroke, IHD, CKD, dementia |
| **obesity** (queued) | BMI | T2D, IHD, several cancers, osteoarthritis |
| hyperlipidaemia (not held) | LDL | IHD, stroke |
| prediabetes (excluded from `type-2-diabetes`) | HbA1c | T2D |
| osteoporosis (not held) | bone density | fracture |

**Two consequences that matter for the register's stated purpose.**

*Triage is distorted in both directions.* Ranked by its own `deaths` field,
hypertension is enormous and every one of those deaths is double-counted against
another record (#160, #147). Ranked by `restored` or `residue` it looks trivially
solved. **The largest preventable cause of death on earth cannot be positioned
correctly by any view this register has.**

*And the thing worth working on is invisible.* This record's answer is not a drug
— the drugs are generic and cost pennies and reach a quarter of patients. It is a
registry, a protocol, a combination pill and somebody accountable for a control
rate, which one health system used to take control from 44% to 90% and published.

Minimal move: a `kind` value — `risk-factor` — that makes the downstream fields
behave differently: no `residue`, no `restored`, and `burden` explicitly
attributed rather than owned. It would apply to perhaps five records and it would
stop the register reporting a number it should never sum.

---

## 180. The diagnostic threshold and the measurement method are set independently · **open**
*Forced by:* `hypertension`.

The trial that justified lowering the American hypertension threshold to 130/80
measured blood pressure by **unattended automated office readings** — patient
alone, machine averaging several measurements after a rest period. That method
reads materially lower than a conventional clinic measurement, by something in
the range of five to fifteen millimetres of mercury depending on the comparison.

**The threshold derived from it is applied, in most clinics in the world, using
the higher-reading method.**

So a number that means one thing in the trial means something else at the point
of care, and the gap is in the direction that creates patients.

**#90 says the threshold is chosen. #175 says the instrument can carry a
population correction. This is a third thing: the threshold and the instrument
are specified by different people, at different times, and nobody reconciles
them.**

Blood pressure is the clearest case and not the only one:

| entity | threshold set from | measured in practice by |
|---|---|---|
| **hypertension** | unattended automated readings in a trial | conventional office cuff, often mis-sized |
| **chronic-kidney-disease** | eGFR stages | **an estimating equation that changed in 2021** (#175) |
| **type-2-diabetes** | HbA1c 6.5%, from retinopathy inflection | assays now internationally standardised — **the counter-example** |
| osteoporosis | T-score −2.5 | DXA, referenced to a specific young-adult population |
| **alzheimers** (held) | amyloid and tau positivity, since 2024 | PET, CSF, or a blood assay cleared in 2025 — **three methods, one label** |

The diabetes row is the one to learn from: HbA1c assays were deliberately
harmonised internationally so that the number means the same thing everywhere.
**It is the only entity in this table where somebody did that work**, and it is
invisible in the register because it looks like nothing happened.

The Alzheimer's row is the one to worry about, and it is live: a biological
definition adopted in 2024, and a cheap blood test cleared in 2025 that will be
used far more widely than the PET scans the criteria were validated against.
**The threshold and the instrument are diverging in real time, in the record this
register already flagged as an overdiagnosis engine.**

Two consequences:

- **Prevalence is a function of method, not only of threshold.** Switch every
  clinic to unattended automated measurement and hypertension prevalence at
  130/80 would fall substantially with nobody's arteries changing. The register
  reports 1.28 billion with no method attached.
- **The fix is cheap and nobody owns it.** Harmonising an assay or specifying a
  measurement protocol alongside a threshold costs a fraction of any trial, and
  it belongs to standards bodies rather than to a disease — which is #164's
  problem again: **a capability that improves every record and is nobody's
  record.**

Minimal move: whatever field records a diagnostic threshold must record **the
method it was derived under.** A threshold without its instrument is not a
specification.

---

**Strengthened by `hypertension`, not new:**

- **#90 (who counts as a patient is a threshold somebody chose) — ITS PUREST CASE,
  AND #90 NAMED IT WHILE THIS RECORD WAS QUEUED.** In 2017 an American guideline
  moved the line from 140/90 to 130/80 and reclassified roughly **31 million more
  United States adults** as hypertensive overnight — national prevalence from
  about 32% to about 46%. The European body did not follow and retains 140/90 for
  the diagnosis. **The same person is hypertensive in Atlanta and not in
  Amsterdam**, and this record's `prevalence: 1.28e9` is a policy output that any
  quotation must carry the threshold with.
- **#178 (prognostic quality is a property of the decision) — a FOURTH independent
  case, and it was not forced.** Blood pressure plus a ten-year risk calculator
  performs comparably to CHA₂DS₂-VASc, MELD and the Kidney Failure Risk Equation.
  All four are cardiometabolic records in which a **treat-or-not decision could
  not be deferred**, and none of the eleven other `prognostic: good` ratings in
  the corpus is a non-trivial individual predictor. The pattern now has four
  observations and a mechanism.
- **#161 (the treatment addresses what kills you, not what bothers you) — its
  flagship, at 1.28 billion people.** #161 was forced by oral rehydration, where
  the patient is acutely ill and the treatment does not touch the visible symptom.
  **Here the patient is not ill at all.** Roughly half of people started on
  antihypertensives are not taking them a year later, and nothing about persisting
  is reinforced by anything they can perceive. #161 called this the
  well-understood asymptomatic case; this is what it looks like at the largest
  scale in medicine.
- **#171 (`ongoing` measures how much, not what kind) — a SIXTH kind.** Supply,
  regimen, restriction, decision-load, time, surveillance — and now **a burden
  that is objectively trivial and subjectively unjustifiable.** One generic tablet
  a day, rated `ongoing: low`, correctly, and it defeats the largest preventable
  cause of death on earth.
- **#154 (interventions that are infrastructure) — and the demonstration is
  published.** A large integrated health system took hypertension control from
  about 44% to about 90% over twelve years using a registry, one simplified
  algorithm, single-pill combinations, and blood pressure checks performed by
  non-physicians with somebody accountable for the number. **No discovery, no new
  drug, nothing to procure** — and globally the control figure remains around 21%.
- **A curable disease affecting tens of millions, found by a blood test, screened
  for almost never.** Primary aldosteronism plausibly accounts for 5-10% of all
  hypertension and up to a fifth of resistant hypertension, and is diagnosed in
  well under one percent of hypertensive patients. Unilateral disease is cured by
  removing an adrenal gland. **Nothing in this register is a better argument that
  the binding constraint is frequently not knowledge but the decision to look.**

---

## 181. The body can defend the state being treated, so the intervention cannot be finite · **open**
*Forced by:* `obesity`.

After weight reduction, ghrelin rises, leptin and PYY fall, hunger increases, and
resting energy expenditure drops **below what the smaller body mass predicts.**
These changes persist at twelve months after diet-induced loss and were still
measurable at six years in one intensively followed cohort. Two thirds of the
weight lost on a GLP-1 receptor agonist returns within a year of stopping it.

**A person maintaining a reduced weight is hungrier, and burning less, than
somebody of the same size who was never heavier.**

That is not non-adherence and it is not a weak drug. It is a **homeostatic
controller opposing the intervention in real time**, in one patient, for years.

**This is a distinct failure mode from the two the register already has.**

| | what opposes the treatment | timescale | over what |
|---|---|---|---|
| **#146 / #111** resistance | a **population of organisms or cells** evolving | months to years | selection |
| **#173** decaying cure | nothing in particular — the state simply lapses | years | — |
| **#181** counter-regulation | **the patient's own regulatory system**, purposefully | immediately, and permanently | a defended set point |

Resistance requires a population and mutation. This requires neither: it is the
same physiology that keeps a healthy person's weight stable, working correctly,
against a treatment.

Once named, the corpus has more of it:

| record | the treatment | what pushes back |
|---|---|---|
| **obesity** | caloric reduction, GLP-1 agonists | hypothalamic set-point defence |
| **hypertension** (held) | diuretics, vasodilators | RAAS activation and sodium retention — why monotherapy fails |
| heart failure (queued) | loop diuretics | neurohormonal activation, and diuretic resistance |
| **low-back-pain** (held) | opioids | tolerance, and opioid-induced hyperalgesia |
| **type-1-diabetes** (held) | insulin | counter-regulatory hormones — the reason hypoglycaemia is survivable |

**Three consequences for the schema.**

1. **`intervention: suppressive` records the rung and not the reason.** A drug that
   is suppressive because the pathogen persists (`hepatitis-b`'s cccDNA) and one
   that is suppressive because the patient's brain is defending a set point are
   the same value, and they imply completely different research programmes:
   *eliminate the reservoir* versus *reset the controller.*
2. **It supplies the mechanism #173 was missing.** That gap observed that cures
   have half-lives; this says why some of them do. A cure decays *because
   something is actively restoring the prior state.*
3. **It is the strongest available argument against the blame in #110**, and it
   is mechanical rather than moral. The willpower framing describes somebody
   losing a contest with their own hypothalamus and attributes the outcome to
   character.

The research question this makes visible is the one nothing in development
addresses: **every effective obesity treatment continuously supplies a satiety
signal, and none resets the reference point it is arguing with.** A therapy that
lowered the set point would convert this record from `suppressive` to `curative`
and delete its cost blocker at the same time, because the treatment would end.

Minimal move: a reason code on `suppressive` — `reservoir` / `counter-regulation`
/ `substrate` — which is one enum and would tell a reader what would have to be
solved.

---

**Strengthened by `obesity`, and #179 has been partly answered from outside:**

- **#179 (the entity can be a risk factor rather than a disease) — WRITTEN ONE
  RECORD AGO, AND THE FIELD HAD ALREADY DONE IT.** #179 proposed splitting risk
  factors from diseases and named obesity as the next case. **In January 2025 a
  Lancet Diabetes & Endocrinology Commission proposed exactly that**: *clinical
  obesity*, where excess adiposity has produced organ dysfunction or limited daily
  activities, is a disease; *preclinical obesity*, where function is preserved, is
  a risk state. It also recommended BMI not be used alone to diagnose either.
  **This record's strata are that split.** Two things follow. The register did not
  need to invent the distinction — it needed to notice a field had made it, which
  is an argument for reading guidelines as data. And **the split is functional
  rather than numerical**: not a better threshold on the measure, but a second
  question about whether anything is actually wrong. **That is the design #179
  should adopt**, and it generalises to `hypertension`, prediabetes and
  osteoporosis immediately.
- **#175 (the instrument can encode a population correction) — AMENDED, AND THE
  AMENDMENT MATTERS.** See the dated note added to that entry: BMI carries lower
  action points for Asian populations and they are **kept**, while the kidney
  equation's race coefficient was **removed**. #175 as written would have argued
  against both.
- **#110 (the register cannot record that the patient is blamed) — THIRD
  OPERATIONAL CASE, AND IT IS THE WIDEST.** `lung-cancer` showed blame as diffuse
  under-funding. `cirrhosis` showed it as a written transplant eligibility rule
  applied per patient. **Here it is primary legislation**: the largest public drug
  benefit in the world carries a statutory exclusion of agents used for weight
  loss, written in 2003, resting on a view of obesity as a lifestyle matter — and
  left in place while the evidence changed underneath it. The revealing part is how
  it is opening: **the drug became payable when it stopped being about the
  weight**, under a cardiovascular indication.
- **#124 (a cure is a one-time sale and a suppression is an annuity) — the largest
  instance that will ever exist.** A weekly injection, indefinitely, for a
  condition affecting nearly nine hundred million adults, where stopping causes
  regain. And the alternative — metabolic surgery, more weight lost, more durably,
  cheaper over a decade — reaches one or two percent of eligible people. **#174's
  worse-version problem and #124's annuity problem are the same fact seen twice.**
- **#160 (the flat list) — and here it hides a rung change.** Substantial weight
  loss is `curative` for `type-2-diabetes` — remission off all medication — and
  `suppressive` for obesity itself. **The same intervention holds different rungs
  in the upstream and downstream records**, and nothing can say that treating one
  thing cures another. The 2023 cardiovascular outcome trial makes this record's
  entire benefit a benefit in other records.
- **An intervention can widen the inequality it was meant to close, and no field
  records it.** Obesity prevalence is highest in the most deprived populations in
  most high-income countries, and a thousand-dollar-a-month drug reaches the least
  deprived first. `access: 0.08` is a single fraction over a population in which
  the distribution is the point.

---

## 182. The register's magnitude is deaths, and some diseases are disability · **open — amends #48**
*Forced by:* `multiple-sclerosis`.

Multiple sclerosis kills around **22,000 people a year**, among the smallest death
figures in this register. What it does is take an adult at twenty-five or thirty
and impose four or five decades of accumulating physical and cognitive
disability, in the years they would have been working and raising children.

**#48 is this register's most serious logged gap** — triage views sort on a
fraction (`reach`) or a price (`cheapest_priced_blocker`) and never multiply by
magnitude, so the answer to "what should we work on next" is systematically
wrong. Its worked example is tuberculosis and its table is deaths per year.

**Its proposed fix would rank multiple sclerosis at approximately zero.**

The missing multiplier is not deaths. It is burden, and burden has two components
that this schema stores one of:

| `burden` field | holds | what it misses |
|---|---|---|
| `deaths` | mortality | — |
| `cases`, `prevalence` | headcount | **for how long, and how badly** |
| — | — | **years lived with disability, and severity** |

Diseases whose weight is duration × severity rather than death are not a corner
case. `remaining.org` has a section called *Disability, not death* holding four of
them, and the corpus already contains more:

| record | deaths/yr | what it actually does |
|---|---|---|
| **multiple-sclerosis** | ~22,000 | decades of disability from age 25 |
| **low-back-pain** (held) | ~0 | the leading cause of years lived with disability worldwide |
| **hearing-loss** (queued) | ~0 | a leading cause of disability, and a dementia risk factor |
| **osteoarthritis** (queued) | ~0 | leading cause of disability in older adults |
| **anaemia** (queued) | few | enormous, and invisible in a death-ranked view |
| **me-cfs**, **heds**, **pots** (held) | ~0 | Engpass's `unexplained-illness`, zero attributed deaths, six of seven blocked by nothing else |

Engpass already discovered a version of this and stated it as a rule: **rank by
records, not by burden**, because `unexplained-illness` has zero attributed deaths
and is the clearest scientific gap in that corpus. That was the right call for
obstacles. **It is a workaround for a missing field, not a solution.**

**Two things follow, and the second is uncomfortable.**

*The fix is available and standardised.* Years lived with disability and
disability-adjusted life years are computed by GBD for every entity here. The
register does not have to invent a weighting — it has to stop refusing to carry
one.

*And a DALY-weighted register would be a different instrument.* Disability
weights are contested, they embed value judgements about what impairment is worth,
and adopting them imports that argument wholesale. **This register's founding
discipline is to derive rather than store opinions**, and a disability weight is
an opinion with a decimal point. That is an argument for carrying the number with
its provenance and its dispute attached — not for continuing to count only deaths,
which is also a value judgement and merely an unstated one.

---

## 183. The `mechanism` axis has never moved in eighty-six records · **open**
*Forced by:* `multiple-sclerosis`, which supplies the first entry.

Ninety-seven `moved` entries across forty-eight records. Their axes:

| axis | entries |
|---|---|
| `efficacy` | 33 |
| `intervention` | 21 |
| `access` | 18 |
| `prevention` | 12 |
| `toll` | 11 |
| `ongoing` | 2 |
| **`mechanism`** | **0** |

**The register records changes in what medicine can DO and has never once
recorded a change in what it KNOWS.**

That is not because mechanism does not change. It changed in 2022 for this
record: a cohort of ten million military personnel with stored serial sera showed
Epstein-Barr virus infection raises multiple sclerosis risk roughly
thirty-two-fold, and that of 801 cases only one was EBV-negative at onset. The
cause of a major chronic disease of young adults was established, and this
record's first `moved` entry on `mechanism` is the register's first anywhere.

**The corpus is full of ones that were missed:**

| record | the mechanism change | year |
|---|---|---|
| **h-pylori-ulcer** | peptic ulcer is an infection | 1982-2005 |
| **multiple-sclerosis** | EBV is near-necessary | 2022 |
| **alzheimers** | amyloid confirmed causal by clearing it — and insufficient | 2023 |
| **type-2-diabetes** | ectopic fat and a personal threshold, so remission is possible | 2018 |
| **multiple-sclerosis** again | B cells matter as presenters, not antibody factories — **taught by a drug** | 2017 |
| **cirrhosis** | fibrosis is reversible, contradicting a century of teaching | 2010s |

**Why it matters, and it is not bookkeeping.**

This register holds **79 `knowledge` blockers and prices none of them** — `scale:
null` on every one, by design, because knowledge cannot be triaged with money. The
register's most-quoted internal finding is that most of what blocks medicine is
delivery rather than knowledge.

**But it cannot show a single instance of a knowledge blocker being closed and
what that bought**, because closing one moves `mechanism` and nothing has ever
moved `mechanism`. So the 79 knowledge blockers have **no track record at all** —
no evidence that answering such a question has ever changed a rating, and no
evidence that it has not.

That is precisely what Engpass exists to argue about. Its top-down records store
`claims` about what answering a question would unblock, carrying
`alleged`/`documented`/`refuted` standing, **on the explicit understanding that
when the question is answered the claims resolve and become a record of whether
the field's intuitions about payoff were any good.** Nothing can resolve if the
answers are never recorded.

Three things to do, in order of cost:

1. **Backfill.** The table above is six entries and took one pass to find. `moved`
   already accepts `axis: mechanism` — the loader does not validate the axis list —
   so this is data entry, not schema work.
2. **When a `mechanism` move is recorded, record what it bought**, on the same
   date or later: `h-pylori-ulcer`'s move to `established` was followed by
   `intervention` going to `curative`. That pair is the evidence a knowledge
   blocker's value can be demonstrated at all.
3. **Then Engpass can resolve claims against it**, which is the only route this
   family has to answering *does understanding a mechanism pay, and how often.*

---

**Strengthened by `multiple-sclerosis`, and one queue expectation superseded:**

- **#89 (`disease-modifying` binned with `none`) — THE RECORD QUEUED TO VINDICATE
  IT HAS CLIMBED PAST THE RUNG.** `remaining.org` listed multiple sclerosis as
  "the positive exemplar for gap #89". On close reading, relapsing MS on
  high-efficacy therapy meets the register's own definition of `suppressive` —
  near-normal life, treated indefinitely, with relapses and new lesions abolished
  — so the record rates `suppressive` and `disease-modifying` survives only in the
  progressive strata. #89's fix was still right and this record is not its
  exhibit.
- **#172 (the entity is defined by a surrogate the best treatments bypass) — A
  SECOND ORGAN, AND THE FIELD FOUND OUT THE HARD WAY.** MS was defined and treated
  by relapses and MRI lesions. **Disability accrues in treated patients without
  relapses and without new lesions** — progression independent of relapse activity
  — and in modern cohorts that accounts for most disability accumulation.
  `type-2-diabetes` is defined by glucose and its best drugs work around glucose;
  this is defined by inflammation and its disability arrives without it. In both
  cases only outcome data revealed it.
- **#170 (an early-acting treatment pulls the definition upstream) — THIRD CASE,
  AND THE GOOD END OF THE RANGE.** The McDonald criteria have been revised five
  times, each enabling earlier diagnosis, and treating radiologically isolated
  syndrome reduces conversion. Unlike `alzheimers` — where the treatment is
  marginal and the overdiagnosis risk high — **here the treatment is transformative
  and the damage prevented is irreversible.** #170 now spans from "clearly right"
  to "clearly risky" and the distinguishing variable is how good the treatment is.
- **#123 (the ladder is ordered by finality, not value) — with a numerical
  coincidence worth recording.** Ocrelizumab in primary progressive MS reduces
  confirmed disability progression by roughly a quarter. Lecanemab in early
  Alzheimer's slows decline by roughly 27%. **Same rung, near-identical effect
  size, and one is celebrated as the first thing that ever worked while the other
  is contested as imperceptible.** The difference is the counterfactual, not the
  drug.
- **#111 (the disease evolves and `strata` assume it does not) — second clean
  case.** Most people with relapsing MS eventually transition to secondary
  progressive disease, so the strata are stages of one course rather than a
  partition of people, and **the entire purpose of treatment is to prevent the
  transition.** The fractions are a snapshot of a cohort in motion.
- **A test rather than a molecule delivered the capability.** Natalizumab was
  withdrawn in 2005 for causing progressive multifocal leukoencephalopathy and
  returned in 2006 because JC virus serology stratifies that risk across two orders
  of magnitude. The register records the drug's return under `intervention` and has
  nowhere to record that **a diagnostic is what made an unusable drug usable** —
  the same shape as G6PD in `malaria` and APOE in `alzheimers`, and the third
  instance of a predictive test that earns its place by preventing harm.
- **Patients rank fatigue and cognitive impairment as their worst symptoms, both
  are untreatable, and neither appears anywhere in this schema** — not `toll`, not
  `residue`, not `ongoing`. They are also absent from the trial endpoints, which is
  where the register inherited the omission from.

---

## 184. `moved` has no convention for measurement, and measurement is what changes most · **open — companion to #183**
*Forced by:* `parkinsons`.

In 2023 an **alpha-synuclein seed amplification assay** was shown to detect
misfolded synuclein in cerebrospinal fluid with roughly 88% sensitivity and 96%
specificity — and to be positive **years before motor symptoms**, in people with
REM sleep behaviour disorder and isolated hyposmia. In 2024 two working groups
proposed redefining Parkinson's disease biologically on the strength of it.

**It is the largest thing to happen to this record in a decade and there is
nowhere to record that anything happened.**

`moved` entries carry an `axis`, and across **103 entries in 49 records** the axes
used are `intervention`, `prevention`, `ongoing`, `efficacy`, `access`, `toll` —
and `mechanism` exactly once, added yesterday at `multiple-sclerosis`. **`measurement` has never appeared**, and nor has `residue`, `window` or
`strata`. The loader does not validate the field, so nothing forbids it — there is
simply no convention, and no record has invented one.

Meanwhile measurement is arguably the fastest-moving thing in the corpus:

| record | the measurement change | year |
|---|---|---|
| **parkinsons** | alpha-synuclein seed assay, positive years early | 2023 |
| **alzheimers** | p-tau217 blood test cleared, replacing PET and lumbar puncture | 2025 |
| **multiple-sclerosis** | McDonald criteria revised **five times**, each enabling earlier diagnosis | 2001-2024 |
| **chronic-kidney-disease** | the race coefficient removed from the eGFR equation | 2021 |
| **cirrhosis** | transient elastography replacing biopsy; MELD 3.0 sex adjustment | 2010s, 2023 |
| **tuberculosis** | rapid molecular testing reporting rifampicin resistance in the same run | 2010s |
| **maternal-haemorrhage** | calibrated drape converting an eyeball estimate into a measurement | 2023 |

**This is #183's twin and the pair says something specific.** #183 found that
`mechanism` has never moved — the register records what medicine can DO and never
what it KNOWS. This finds the same for what medicine can SEE. Between them, the
two axes that are not "capability" have **one recorded change in eighty-seven
records**, and it was added yesterday.

Three consequences:

1. **A record can be transformed with no trace.** `alzheimers` acquired a cheap
   accurate blood test in 2025 and its file reads as though the diagnostic
   situation were static.
2. **The register cannot show that better measurement ever paid.** Which is the
   same failure #183 identified for knowledge, and it matters more here because
   **61 of the corpus's 354 blockers are `diagnosis` blockers** — the third
   largest kind — and none has a demonstrated precedent for being closed.
3. **The direction is unrecordable too.** `covid-19` documented surveillance being
   *dismantled* (#165), which is a measurement change going backwards, and had to
   put it in prose.

The fix is the same as #183's and cheaper: adopt `axis: measurement.diagnostic`
(and the other two) as a convention, and backfill the table above. Nothing in
`check.py` needs to change.

---

## 185. A window can be open, measurable, populated — and empty · **open**
*Forced by:* `parkinsons`.

By the time the first tremor appears, roughly half to seventy percent of a
Parkinson's patient's dopaminergic neurons are already gone. The prodrome runs for
years to decades and is **not silent if anybody looks**: anosmia, constipation,
depression, and above all **REM sleep behaviour disorder**, which converts to
Parkinson's or dementia with Lewy bodies in around three quarters of people within
twelve years. The alpha-synuclein seed assay is positive in many of them.

**So the window is open, the biology is understood, the population can be
identified with near-deterministic accuracy — and every neuroprotection trial has
failed.** Selegiline, coenzyme Q10, creatine, isradipine, inosine, a large phase 3
of exenatide, and the alpha-synuclein antibodies.

That record's `caught_in_time` reads **0.05**, and a reader will draw exactly the
wrong conclusion from it. The schema's `window` block asks *what fraction reached
effective treatment in time*, so a low number means **people are arriving late.**
Here nobody is arriving late. **There is nothing to arrive for.**

**The existing window gaps do not cover this**, and the distinction is clean:

| gap | the problem |
|---|---|
| **#131** (`pancreatic-cancer`) | nobody knows whether the window exists |
| **#112** (`prostate-cancer`) | it exists and catching is not always worth it |
| **#96** | it closes before there is anything to diagnose |
| **#94** | it can be measured rather than assumed — *a win* |
| **#185** | **it exists, is measurable, has an identifiable population, and there is nothing to give them** |

**And the register's existing convention for this hides it.** `huntington` is the
extreme case — a genetic test available decades in advance, and nothing to do —
and that record simply **has no `window` block at all.** Omission is a workable
convention when capability is zero everywhere.

**It fails for Parkinson's**, which has excellent capability — levodopa returns
people to work for years — just not the kind the window is about. Omitting the
window would hide the single most consequential fact in the record; including it
produces a number that reads as a delivery failure. **Neither option is honest,
which is the definition of a missing field.**

Where else this bites, once named: `huntington` (which should carry an explicit
empty window rather than none), prodromal Alzheimer's before 2023, familial
cancers before targeted therapy existed, and any disease where a genetic or
biomarker test outruns the therapeutics — **which #170 says is now happening
routinely.**

Minimal move: `caught_in_time` gains a companion stating **what they would be
caught for**, or `n/a` where the answer is nothing. A window with no intervention
behind it is a research target, not a delivery gap, and the register currently
files them identically.

---

**Strengthened by `parkinsons`, not new:**

- **#170 (an early-acting treatment pulls the definition upstream) — FOURTH CASE,
  AND THE MOST PREMATURE.** Two working groups proposed defining Parkinson's
  **biologically** by synuclein positivity in 2024. `multiple-sclerosis` pulled its
  definition upstream with transformative therapy waiting; `type-1-diabetes` had
  teplizumab; `alzheimers` had a marginal drug, and that record flagged the risk of
  *a diagnostic advancing ahead of a therapeutic*. **Parkinson's has redefined
  itself biologically with nothing whatever to offer the people it newly
  identifies.** #170 now spans the full range and the ordering principle is
  visible: **the value of pulling a definition upstream is entirely a function of
  what is waiting there.**
- **#89 / #123 — `capability` still bins `symptomatic` with `none`, and this
  record makes it visible.** `huntington` rates `intervention: symptomatic` with
  `efficacy: 0.0`. `parkinsons` rates `symptomatic` with `efficacy: 0.65` — a cheap
  generic tablet that gives somebody their life back for a decade. **Both derive
  `capability: unsolved`.** #89 fixed the quadrant's three bands and left this
  behind, and the register's own naming discipline — *never a bare one-word verdict*
  — applies here as much as it did to `solved`.
- **The "permanent toll while the course is unchanged" table gains its clearest
  entry.** Levodopa-induced dyskinesia affects the majority of long-treated
  patients and does not resolve; **dopamine agonists cause impulse control
  disorders in roughly one in seven**, and people have lost houses, savings and
  marriages to a Parkinson's tablet. The behaviour stops when the drug is
  withdrawn; the bankruptcy does not unwind. It is among the most under-known
  iatrogenic harms in medicine.
- **#87 / #53 (the intervention lives in another ministry) — and here the exposure
  is chemical and the proof is an accident.** MPTP, a contaminant in an illicitly
  synthesised opioid, caused irreversible parkinsonism in young people within days
  in 1982. **Paraquat** is banned in the European Union and widely used elsewhere;
  **trichloroethylene** is one of the commonest groundwater contaminants, with
  around a seventy percent excess risk in one large contaminated-site cohort.
  Age-standardised prevalence is rising, which means this is not only ageing.
  **The largest substantially preventable neurodegenerative disease, and nobody
  treats it as preventable** — because the levers are pesticide registration and
  solvent regulation, the benefit appears thirty years later, and `who_could` has
  no environmental agency.
- **#111 (strata are stages, not a partition) — third record running**, after
  `multiple-sclerosis` and `hepatitis-b`. And **#169 (the carer)** again: a spouse
  of similar age, for the ten to twenty years between diagnosis and death.
- **Two of the most replicated findings in this record's epidemiology are
  protective, unexplained, and unusable.** Smoking and caffeine both lower
  Parkinson's risk, consistently, across decades and populations. Nicotine trials
  failed; caffeine trials failed. **Something real is being detected and nobody can
  convert it into an intervention** — a kind of open question the register has no
  vocabulary for, since it is neither a `knowledge` blocker with a target nor an
  `evidence-incomplete` one with a study design.

---

## 186. A diagnosis can degrade access to care for everything else · **open**
*Forced by:* `schizophrenia`.

People with schizophrenia die roughly **fifteen to twenty years early**, one of
the largest mortality gaps in this register. Suicide accounts for perhaps one
death in twenty. **The majority is cardiovascular and metabolic.**

Part of that is manufactured by the treatment — antipsychotic-induced weight gain
and diabetes — which the register can at least record as `toll`. Part is smoking
and poverty. **And part is that people with severe mental illness receive less
cardiac investigation and revascularisation, fewer statins and less cancer
screening than other people presenting with the same findings.** The phenomenon
has a name in the literature — **diagnostic overshadowing** — and it means
physical symptoms get attributed to the psychiatric diagnosis, or to the drugs,
and are not pursued.

**So this record's largest mortality effect is another record's `access` failing,
selectively, because of this record's label.**

Nothing in the schema can hold that. `access` in `schizophrenia` describes access
to antipsychotics. `access` in `ischaemic-heart-disease` is a single fraction over
everybody, and the fraction is lower for this subgroup for a reason that belongs
to neither file.

**This is a new edge type for the graph #160 asked for**, and #177 already
established that edges need a sign. The corpus now needs three:

| edge | example |
|---|---|
| **causes** | `hepatitis-b` → `liver-cancer` |
| **prevents / causes** (signed, #177) | `atrial-fibrillation`'s treatment → both strata of `stroke` |
| **degrades access to** | **`schizophrenia` → every physical health record** |

And the third is not rare. Once named, the corpus has it repeatedly:

| the label | what it degrades access to |
|---|---|
| **schizophrenia**, and severe mental illness generally | cardiac, cancer and diabetes care |
| **obesity** (held) | symptoms attributed to weight before they are investigated |
| **me-cfs**, **heds** (held) | everything, and the records say so in prose |
| learning disability (not held) | the same, and it is the subject of national mortality reviews |
| **low-back-pain** (held) → opioid history | pain taken less seriously afterwards |

**Distinguish it from #110 carefully, because the fix is different.** #110 is
*blame* — the patient is held responsible, and the consequence is diffuse
under-funding (`lung-cancer`) or a written eligibility rule (`cirrhosis`).
Overshadowing is not moral. **It is a clinician with a plausible explanation
already in hand, not looking further** — a cognitive failure rather than a
judgement, which means it responds to prompts, protocols and physical-health
checks rather than to advocacy.

Minimal move: the `degrades access to` edge, and a note on any record whose
`access` is known to be depressed for an identifiable subgroup. It would let the
register answer a question it currently cannot: **which records are quietly paying
for another record's label?**

---

## 187. Treatment can be delivered by force, and liberty is in no field · **open**
*Forced by:* `schizophrenia`.

For a substantial minority of people in this record, treatment is delivered under
legal compulsion: detention in hospital, involuntary medication, and community
treatment orders that make continued liberty conditional on accepting a depot
injection. Entire statutes exist for it, and it is routine rather than
exceptional.

**`toll` records what the cure costs the patient.** Weight gain, tardive
dyskinesia, agranulocytosis. **It has no way to record that the cure was
administered against their will.**

**#144 is adjacent and is not this.** That gap — forced by `typhoid` and Mary
Mallon, sharpened by `mrsa`'s contact precautions — is about **public health doing
things to people for the protection of others.** The person is well; the
imposition protects somebody else.

Here the justification is the opposite: **the compulsion is for the patient's own
benefit, and it is the delivery mechanism for the treatment itself.** That is a
different claim, with a different ethical structure and a different evidence base
— community treatment orders, for instance, have been randomised, and the trials
did not show the reduction in readmission they were introduced to achieve.

Where else it appears, and the list is longer than psychiatry:

| record | the compulsion |
|---|---|
| **schizophrenia** | detention, involuntary medication, community treatment orders |
| **tuberculosis** (held) | detention for non-adherent drug-resistant disease, in several countries |
| **typhoid** (held) | Mary Mallon, and modern carrier restrictions — **#144's kind** |
| **covid-19** (held) | isolation and quarantine — **#144's kind** |
| dementia (`alzheimers`, held) | deprivation of liberty safeguards, guardianship, covert medication |
| **opioid-use-disorder** (queued) | court-mandated treatment |

**Two things the register should be able to say and cannot.**

*That a treatment's delivery is coercive at all*, which is a fact about the
intervention as consequential as its side-effect profile and is currently
invisible. A reader comparing `schizophrenia` to `bipolar` — same rung, same
`ongoing`, similar efficacy — has no way to learn that one of them routinely
involves detention.

*And what the coercion buys.* This is the harder half and it is empirical rather
than ethical: compulsory community treatment has been tested and the evidence is
weak. **A field that recorded coercion would make its evidence base a question
somebody had to answer**, rather than a background condition of care.

Minimal move: a flag on the record — `compulsion: routine / occasional / none` —
with the legal instrument named. It applies to perhaps six records, it takes no
position on whether compulsion is justified, and it is the same discipline
`standing` applies to blocker claims: **record that the thing happens and what it
costs, not whether it is right.**

---

**Strengthened by `schizophrenia`, not new:**

- **#135 (`mechanism` rates why the disease happens, never why the treatment
  works) — AND HERE IT INFLATES A RATING INTO A DIFFERENT QUADRANT.** This record
  rates `mechanism: partial` on the strength of D2 pharmacology, a measured
  presynaptic dopamine abnormality, 287 loci and the complement/pruning finding —
  and lands in **`known & treatable`**, alongside hepatitis C and lung cancer. A
  strict reading that excluded *how the drug works* would rate `correlates` and
  file it beside `bipolar` in `empirical luck`. **The psychiatric trio's quadrant
  assignments turn on this distinction and nothing in the schema forces the
  question.**
- **#172 (the entity is defined by a surrogate the best treatments bypass) — THIRD
  ORGAN, AND THE STARKEST.** Schizophrenia is defined and treated by positive
  symptoms. **Negative symptoms and cognitive impairment predict employment and
  independent living far better, and respond to nothing.** Seventy years of drug
  development produced excellent control of the symptoms that frighten other people
  and almost nothing for the symptoms that disable the patient. After
  `type-2-diabetes` (glucose) and `multiple-sclerosis` (relapses), the pattern is
  established enough to be a design rule: **check whether the defining feature is
  the disabling one.**
- **#185 (a window that is open, populated and empty) — one record later, twice
  over.** The clinical high-risk state converts to psychosis in twenty to thirty
  percent within a few years, is identifiable, and interventions there have been
  small and disappointing. **And the early-intervention window is stranger**: the
  service demonstrably works, and long-term follow-up shows the groups converging
  after it ends. **An intervention that works while running and leaves no durable
  change** — #173's decaying cure applied to a *service* rather than a drug, and
  #57's maintenance problem at the level of one patient.
- **#174 (you got the worse version) — with a retrospective definition making it
  worse.** Clozapine is the only agent with proven efficacy in the
  treatment-resistant third, reduces suicide, and is under-prescribed by
  several-fold margins between comparable health systems. **And treatment
  resistance is defined by having already failed two drugs**, so the criterion for
  reaching the one that works can only be met by spending a year or more not
  getting better — during which the functional losses the `window` describes
  accumulate permanently.
- **#169 (the carer) and the prisons.** Deinstitutionalisation closed the asylums
  and in several countries did not build what was meant to replace them; the
  largest institutions now housing people with schizophrenia are prisons and
  homeless shelters. That is neither `access` nor `toll` nor `residue`, and it is a
  consequence of a health policy decision recorded nowhere.

---

## 188. The register records what blocks, never what has been demonstrated and not copied · **open**
*Forced by:* `cataract`.

An Indian eye hospital system set out in 1976 to eliminate needless blindness and
solved the delivery problem. Extreme division of labour, two tables per surgeon,
standardised technique, **surgeon volumes several times Western norms with
comparable complication rates**, and roughly half to two thirds of patients
treated free — cross-subsidised by paying patients inside the same institution, so
the programme sustains itself rather than depending on donors. When the
intraocular lens was the binding cost at over a hundred dollars, they **built a
factory in 1992 and took it to a few dollars**, then supplied other countries.

Every element is published. None is proprietary. **Global effective cataract
surgical coverage is around a third.**

The register can record the blocker — surgeons, theatres, money — and has **no
field for the demonstrated answer.** `blockers` says what is in the way.
Nothing says *this has been done, here, at this cost, with this result, and not
copied.*

**And the corpus has been accumulating these for eighty-nine records, filing every
one of them in prose:**

| record | what was demonstrated | and then |
|---|---|---|
| **cataract** | Aravind: high-volume surgery, cross-subsidy, $2 lenses | coverage ≈ ⅓ |
| **hypertension** | one system took control from **44% to 90%** with a registry and a protocol | global control ≈ 21% |
| **mrsa** | England cut bacteraemia ~**80%** with hand hygiene and accountability | not general |
| **diarrhoeal-disease** | ORS: the largest life-saving intervention of the century | coverage flat at ~45% for two decades |
| **chronic-kidney-disease** | peritoneal-dialysis-first is cheaper and at least as good | a minority almost everywhere |
| **tuberculosis** | BPaLM: six months oral, ~89% success | rollout partial |
| **maternal-haemorrhage** | E-MOTIVE bundle cut severe haemorrhage ~**60%** | not standard |

**A demonstrated solution is a stronger object than a blocker and the register
treats it as decoration.** A blocker says *something is in the way*. A worked
example says *here is the thing, the cost, the outcome, and the name of the place
that did it* — which is what a health minister, a funder or a foundation actually
needs, and it is the only form of evidence that answers "can this be done?" rather
than "why has it not been?"

**Three things follow.**

1. **The register's stated purpose is served better by this than by blockers.**
   "What should we work on next" over a corpus of demonstrated-and-uncopied
   solutions has an obvious answer shape: copy them. Over a corpus of blockers it
   returns a list of obstacles.
2. **It is a natural home for #57's problem.** That gap says the register cannot
   value maintenance — that a closed gap becomes invisible. A `demonstrated` field
   is where an achievement stays visible after it stops being a gap.
3. **And it makes the failure to copy the finding.** Every row above is a solved
   problem that did not spread, and the reasons differ — no product to sell
   (`diarrhoeal-disease`), a payment structure favouring the worse option
   (`chronic-kidney-disease`), no accountable owner (`hypertension`). **Those are
   the actual research questions in delivery**, and none of them is visible while
   the answer is a sentence in a witness.

Minimal move: a `demonstrated:` block — what was done, where, what it cost, what
result, and whether it spread. It would be filled in for perhaps fifteen records
today and it is the only field in this file that would make the register
*encouraging* without making it dishonest.

---

## 189. The treatment threshold is set by capacity, not by the patient · **open**
*Forced by:* `cataract`.

When cataract surgery meant a week in hospital lying still with sandbags beside
your head, you waited until the cataract was **"ripe"** — until you were blind.
Now it takes fifteen minutes under topical anaesthetic, and in well-resourced
health systems the indication has drifted down to visual acuities that would not
have been considered remotely operable in 1960 — and increasingly to refractive
reasons in an eye that still sees well.

**Meanwhile fifteen million people are blind from the same disease, and where
capacity is scarce the effective threshold is still "ripe".**

Same operation, same evidence, same surgeons' training. **The threshold is set by
supply.**

**This is not #90 and the difference matters.** #90 says a threshold is a
committee's choice on a continuum — the statin risk cut-point, 140/90 versus
130/80. Those are deliberate decisions, argued in guidelines, applied uniformly.
**This threshold is nobody's decision.** It is an emergent property of how many
surgeons there are, and it moves in **opposite directions** in rich and poor
settings for the same disease in the same year.

Nor is it quite #52 (solved here, not there), which is about a good thing failing
to arrive. Here the *definition of who needs it* has quietly diverged, so the two
settings are not even measuring the same population:

| | high-capacity setting | low-capacity setting |
|---|---|---|
| operate at | 6/9, or refractive indication | 3/60, or blind, or never |
| "needs surgery" means | impaired enough to be worth fifteen minutes | **blind in both eyes** |
| unmet need looks like | small | small — *because the threshold moved to match supply* |

**That last cell is the dangerous one.** A capacity-set threshold makes unmet need
look manageable everywhere, because the definition of need adjusts to what can be
supplied. It is the reason effective coverage had to be defined against a fixed
visual-acuity outcome rather than against "cases needing surgery" — somebody in
that field noticed this and built the metric to defeat it.

Where else it applies — anywhere the intervention is a **procedure or a
practitioner's time** rather than a molecule:

| record | the threshold that moves with capacity |
|---|---|
| **cataract** | acuity at which surgery is offered |
| **chronic-kidney-disease** (held) | who is listed for transplant, and who is offered conservative management |
| **cirrhosis** (held) | MELD score at which a liver is realistically obtainable |
| **type-2-diabetes** (held) | who is offered a remission programme or metabolic surgery |
| **obesity** (held) | BMI threshold for bariatric referral |
| joint replacement (queued `osteoarthritis`) | pain and function score at which it is offered |

Minimal move: where a record's threshold is capacity-determined, say so, and
record the outcome-anchored coverage figure rather than a "proportion of need
met". **The second number is unfalsifiable when need is defined by supply.**

---

**Strengthened by `cataract`, not new:**

- **#182 (the magnitude is deaths, and some diseases are disability) — ITS
  FLAGSHIP, ONE RECORD AFTER IT WAS WRITTEN.** `deaths: 0`. Ninety-four million
  people with vision impairment or blindness. Cataract surgery is repeatedly
  identified as among the most cost-effective interventions in any health system.
  **#48 proposes fixing the register's ranking with a mortality weight, and that
  fix would rank this record at exactly zero** — and the record demonstrates the
  same mechanism operating on real budgets, since eye care loses every priority
  argument for precisely this reason.
- **And `deaths: 0` is wrong in BOTH directions, which #182 did not anticipate.**
  Cataract blindness causes falls and hip fractures, which kill and are counted
  elsewhere. **And cataract surgery is associated with substantially lower
  subsequent mortality** in older people in cohort studies. So the register holds
  a record with no attributed deaths whose treatment may be a mortality
  intervention, and can say neither thing.
- **#178 (prognostic quality is a property of the decision) — a FOURTH
  independent case and the cleanest.** Optical biometry predicts an individual's
  post-operative refraction to a fraction of a dioptre. **The forcing decision is
  which lens to implant** — undeferrable, unrepeatable — and the prediction exists
  because of it. After MELD, KFRE and CHA₂DS₂-VASc, all four non-trivial
  individual prognostic instruments in this corpus were built because somebody had
  to choose something they could not take back.
- **#124 (a cure is a one-time sale and a suppression is an annuity) — THE
  COUNTER-EXAMPLE.** Cataract surgery is the purest one-time cure in the register:
  `ongoing: none`, no follow-up therapy, the patient leaves. #124 predicts that
  such a thing struggles to find a business model. **Aravind found one** — internal
  cross-subsidy — and it has been self-sustaining for decades at enormous volume.
  The gap stands and now has a demonstrated exception, which is more useful than
  another confirmation.
- **#170 (a treatment pulls the definition) — a fifth case, and it moves severity
  rather than time.** `alzheimers`, `type-1-diabetes`, `multiple-sclerosis` and
  `parkinsons` all had their definitions dragged **earlier**. Here a safer
  operation dragged the definition **milder** — the same mechanism acting on a
  different axis of the disease's boundary.
- **A hard developmental deadline, and it is the only one in the corpus.**
  Congenital cataract must be operated within roughly the first six to ten weeks
  or deprivation amblyopia is permanent — the eye becomes optically perfect and the
  child remains blind in it. Detecting it requires a red reflex check on a newborn,
  thirty seconds with an ophthalmoscope, **and most of the world has no systematic
  newborn eye examination.**

---

## 190. Rescuing the majority makes the remainder harder to rescue · **open**
*Forced by:* `cystic-fibrosis`.

CFTR modulators reach roughly **nine in ten** people with cystic fibrosis. In
countries that funded them, lung function rose sharply, exacerbations fell by
around two thirds, and transplant referrals and deaths dropped within a few years.

**Roughly one in ten carry nonsense or severe splice mutations that produce no
CFTR protein at all.** A modulator cannot correct a protein that was never made.
They get the pre-2012 disease.

**And their position is now worse than it was before the drugs worked**, for
reasons that have nothing to do with their biology:

| | before | after |
|---|---|---|
| trial population | the whole disease | **a tenth of a rare disease, dispersed** |
| commercial case | the whole market | a tenth of it |
| comparator | the same as everyone's | **a standard of care they cannot reach** |
| field attention | one problem | the solved majority's remaining questions |
| clinical expertise | universal | concentrating on modulator management |

**This is not #56 and the difference is the mechanism.** #56 (forced by `hat`) is
about **elimination endgames** — prevalence falls toward zero, so the screening
test's positive predictive value collapses, cost per case found rises, and the
last cases are in the hardest places. That is a numbers game driven by declining
prevalence.

**Here the remainder did not shrink.** It was always a tenth. What changed is that
the other nine tenths left, and took the trial infrastructure, the market and the
attention with them. **A fixed subgroup got harder to help because its neighbours
were rescued.**

Once named, the corpus has it repeatedly:

| record | the majority rescued | the remainder |
|---|---|---|
| **cystic-fibrosis** | ~90% on modulators | **nonsense mutations — nothing** |
| **hepatitis-c** (held) | DAAs cured the reachable | the hardest-to-reach populations, now the whole problem |
| **cml** (held) | TKIs | those failing every generation of them |
| **childhood-all** (held) | ~90% cured | relapsed and refractory disease |
| **tuberculosis** (held) | BPaLM transformed MDR-TB | XDR, and the un-diagnosable |
| breast cancer (held) | hormone- and HER2-directed therapy | **triple-negative** |

**Two consequences the register should be able to express.**

*The record's improving `efficacy` actively conceals it.* This record went from
0.25 to 0.80 and the untreatable tenth did not move at all. A reader sees a
transformed disease. **#151 said a transformed stratum can hide inside a static
record; this is the inverse and it is worse, because the stratum left behind is
the one that needed the most.**

*And "orphan within an orphan" is a real category with no funding mechanism.*
Orphan drug incentives were built for rare diseases. They were not built for the
residue of a rare disease after most of it was solved, which is rarer still, and
in which the trial is harder and the comparator is now unethical.

Minimal move: where a stratum is excluded by mechanism rather than by access,
mark it — and record whether its position improved, held, or **worsened** when the
record's headline number moved.

---

## 191. The outcome that matters can be outside any measurable horizon · **open**
*Forced by:* `cystic-fibrosis`.

A two-year-old starting a CFTR modulator today will take it for **sixty years.**

Approval rested on lung function, sweat chloride and exacerbation rate measured
over weeks to months. **The question everybody actually has is whether a child
treated from infancy develops bronchiectasis, pancreatic insufficiency and
CF-related diabetes at all** — whether they simply have a normal life.

**The answer arrives around 2080.** Decades after the patent expires, after the
pricing negotiation concluded, after the clinical convention hardened, and after
every person who made those decisions has retired.

This is not #172 (an entity defined by a surrogate its treatments bypass) or #168
(an efficacy fraction that cannot hold a continuous shift). **It is a horizon
problem**: the trial that would answer the question cannot be run, not because
nobody will fund it but because it would take longer than the careers, the
patents and the institutions involved.

Where it applies is broader than it first looks — **anywhere a therapy starts in
childhood or middle age and its value is realised in old age**:

| record | given at | the outcome that matters | measurable? |
|---|---|---|---|
| **cystic-fibrosis** | age 2 | a normal lifespan | **~2080** |
| **spinal-muscular-atrophy** (queued) | weeks old, one dose, irreversible | decades of function | no |
| **hepatitis-b** (held) | lifelong from diagnosis | liver cancer avoided at 65 | partially |
| **hypertension** (held) | age 50 | stroke at 75 | **yes — outcome trials were run** |
| statins | age 50 | infarct at 70 | **yes** |
| **obesity** (held) | indefinitely | cardiovascular events | **yes, since 2023** |

**The last three rows are the important ones**, because they show the problem is
sometimes soluble: cardiovascular medicine ran the long outcome trials and got
answers. What makes cystic fibrosis different is that the horizon is a *lifetime*
rather than a decade, and the population is too small to power anything shorter.

**Two things follow.**

*Registries are the only instrument that works on this timescale*, which makes
them **infrastructure rather than research** — and they are funded, staffed and
evaluated as research. That is #164's problem again: a capability that improves
every question in a record and belongs to no trial.

*And a decision has to be made anyway.* The register should be able to record
that a rating rests on a surrogate **whose validation is scheduled for a date
beyond the decision it is informing** — which is a different and more honest
statement than `src: reasoning`.

Minimal move: alongside `efficacy`, record the **horizon** of the evidence behind
it — the follow-up duration actually observed — and whether the outcome of
interest lies beyond it.

---

**Strengthened by `cystic-fibrosis`, not new:**

- **#183 (`mechanism` has never moved) — A SECOND ENTRY, AND IT DOES EXACTLY WHAT
  THE GAP ASKED FOR.** CFTR was cloned in 1989. The expectation was universal and
  explicit: the cure would be gene therapy, within a few years. **Gene therapy
  trials began in 1993 and thirty-plus years later there is no approved product** —
  the lung's mucus barrier, vector immunity and epithelial turnover defeated all
  of it. What worked was **small-molecule protein-folding chemistry found by
  high-throughput screening**, which nobody proposed in 1989. So the mechanism move
  bought everything, twenty-three years later, through a door nobody was watching.
  **#183 asked for mechanism moves *and* a record of what they bought. This is the
  first entry with both**, and its lesson is that the payoff lag is measured in
  decades and the route is not predictable from the mechanism.
- **#188 (demonstrated and not copied) — a second case, and it is a FINANCING
  model rather than a delivery one.** The Cystic Fibrosis Foundation put roughly
  $150 million of philanthropic money into research no company would carry, and
  sold the resulting royalty rights for **$3.3 billion**. Venture philanthropy by a
  disease foundation, at a scale nobody had attempted, producing three approved
  drugs. Other foundations have tried to copy it with mixed results. **#188's
  proposed `demonstrated:` block needs to cover how something was paid for, not
  only how it was delivered.**
- **#151 (a stratum transformed without the record moving) — INVERTED, which is
  the finding.** The queue predicted this record would be #151's sharpest instance.
  It is the opposite: the transformed stratum is nine tenths, so the record moved
  from 0.25 to 0.80 — **and the untouched tenth became invisible inside a success.**
  Both directions of the same defect: a record-level scalar cannot describe a
  disease whose strata moved differently.
- **`predictive: good` — one of ten records, and the only one whose test never
  expires.** `cre` and `tuberculosis` rate `good` on susceptibility testing and
  those answers decay, because the organism evolves and can defeat the assay
  (#149). **A CFTR genotype is fixed at conception.** Genotype names the drug
  almost deterministically: gating mutations need a
  potentiator, F508del needs correctors too, nonsense mutations respond to nothing.
  **This is what precision medicine was supposed to look like.** And the same test
  that identifies who benefits identifies who cannot, permanently, at birth.
- **#147 (the disease is a byproduct of capability) — operating INSIDE one
  record.** There are now more adults than children with cystic fibrosis, and with
  them came CF-related diabetes in a large share of adults, male infertility that
  matters because men with CF now expect to have children, and pregnancy
  management. **Success created new disease within the entity**, and the register
  stores an undated snapshot of a record whose `strata`, `ongoing` and `residue`
  all move as survival extends.
- **#159's shape again on `prevention`.** `risk-reduction` here covers carrier
  screening, prenatal diagnosis and preimplantation testing — **prevention of a
  birth rather than of a disease**, resting on a decision that belongs to
  prospective parents. The register uses the same field it uses for a bed net.

---

## 192. Some interventions cannot be revised, and the register has no field for it · **open**
*Forced by:* `spinal-muscular-atrophy`.

Onasemnogene abeparvovec is a **single intravenous infusion**, given to an infant,
at roughly $2.1 million. Neutralising antibodies to the viral vector make
**redosing impossible.** It cannot be stopped, cannot be titrated, and cannot be
repeated.

The schema records that as `ongoing: none` and a small `toll.incidence`, and both
readings are wrong in the same direction.

**`ongoing: none` means two opposite things and the register cannot tell them
apart:**

| record | `ongoing: none` means |
|---|---|
| **cataract** | **it is finished.** Fifteen minutes, the lens is replaced, nothing more is needed |
| **hepatitis-c** | it is finished — twelve weeks, cured |
| **spinal-muscular-atrophy** (gene therapy) | **there is nothing more you CAN do.** One dose, irrevocable, durability unproven |

The first is the absence of a burden. The second is the absence of an option.
#171 asked what *kind* of ongoing burden a record carries and listed six —
supply, regimen, restriction, decision-load, time, surveillance. **This is not a
seventh kind of burden. It is a property of the decision**, and it cuts across
`intervention`, `toll` and `ongoing` at once.

**The intervention ladder has nowhere to put it either.** Not `curative` — the
deletion remains, the vector genome is episomal, durability beyond a few years is
unproven, and a substantial share of treated children are subsequently started on
a second drug off-label. Not `suppressive` — nothing is being continued. **The
vocabulary assumes a treatment is either ongoing or finished, and this is a third
thing.**

Where else, once named — and the list is longer than gene therapy:

| intervention | what cannot be undone |
|---|---|
| **onasemnogene** (`spinal-muscular-atrophy`) | the vector dose, and the antibodies that preclude another |
| **exa-cel / lovo-cel** (`sickle-cell`, held) | myeloablative conditioning, and the fertility it costs |
| **cranial irradiation** (`childhood-all`, held) | the dose, and the cognition |
| **hysterectomy** (`maternal-haemorrhage`, held) | fertility, decided during a haemorrhage |
| **metabolic surgery** (`obesity`, `type-2-diabetes`, held) | the anatomy |
| **transplant** (several) | the native organ, and the immunosuppression that follows |

**Three properties compound in the SMA case and the register should be able to
flag each.** The decision is **irreversible**; it rests on a **surrogate whose
validation is decades away** (#191); and it is made **by a proxy for somebody who
cannot consent** — an infant, days old.

None of those is a side effect and all of them are what a parent is actually
being asked about. The `toll` field records hepatotoxicity, correctly, and says
nothing about the fact that this is the only decision they will get to make.

Minimal move: a `reversible: yes / no / partial` field on the intervention. One
enum, filled in for perhaps ten records, and it separates *finished* from
*irrevocable* — which `ongoing: none` currently conflates.

---

## 193. Some `knowledge` blockers are engineering blockers, and those have a price · **open**
*Forced by:* `spinal-muscular-atrophy`, against `cystic-fibrosis` one record
earlier.

Two records, a controlled comparison, and the register should not waste it:

| | `cystic-fibrosis` | `spinal-muscular-atrophy` |
|---|---|---|
| gene identified | **CFTR, 1989** | **SMN1, 1995** |
| obvious approach | gene therapy | gene therapy |
| trials from | 1993 | 2014 |
| **result** | **thirty-five years, no approved product** | **approved 2019** |
| what worked instead | small-molecule protein folding | gene therapy *and* two splicing drugs |

Same era, same logic, comparable understanding. **The variable is not knowledge.
It is whether the vector can reach the cell.**

Motor neurons are **post-mitotic** — they do not divide, so an episomal genome
persists — and in an infant an intravenous AAV9 crosses the blood-brain barrier.
Airway epithelium sits **behind mucus**, is defended by immunity that neutralises
repeat dosing, and **turns over**, so anything delivered is shed.

That is an engineering problem: vector tropism, barrier penetration, immune
evasion, redosing. **And engineering problems have prices.**

**Which matters because of a number this register keeps repeating.** It holds
**84 `knowledge` blockers and prices none of them** — `scale: null` on every one,
by design, on the reasoning that knowledge cannot be triaged with money. Engpass
built its whole case on that asymmetry: knowledge blockers are *categorically* the
ones money cannot move.

**A subset of them are not knowledge blockers at all.** They are delivery
problems, or assay problems, or manufacturing problems, wearing a knowledge
costume — and they can be costed, scheduled and bought:

| record | filed as `knowledge` | actually |
|---|---|---|
| **cystic-fibrosis** | gene therapy for nonsense mutations | **delivery to airway epithelium** |
| **parkinsons** | measuring whether anything slowed the disease | **a validated progression biomarker** — an instrumentation problem |
| **alzheimers** | — | the p-tau217 assay was an assay problem and it was solved |
| **sepsis** (held) | what "dysregulated" means | partly a **partition** problem — endotypes |
| **schizophrenia** (held) | negative symptoms | partly a **measurement** problem — nobody agrees on the endpoint |

**The test is simple and worth applying across the corpus**: *if you had unlimited
money, is there a programme somebody could run?* If yes, it is engineering and it
has a price. If the answer is "we would not know what to fund," it is knowledge.

Two things follow:

1. **Engpass's headline finding needs qualifying.** "Zero of 42 knowledge blockers
   carry a price — categorically the ones money cannot triage" was the register's
   most-quoted asymmetry. It is right about the residue and wrong about the
   category, and the split it implies — `mechanism-unknown` versus
   `no-candidate` — was already flagged in Engpass's own gaps as an unmade schema
   change. **This is the argument for making it**, and it should be three-way:
   mechanism unknown, candidate untested, **and delivery unsolved.**
2. **A priced engineering blocker changes what the register recommends.** "Nobody
   knows why motor neurons die" and "we cannot get a vector past airway mucus" are
   both `knowledge` today, and only one of them is something a foundation could put
   fifty million dollars behind next year.

---

**Strengthened by `spinal-muscular-atrophy`, not new:**

- **#183 (`mechanism` has never moved) — A THIRD ENTRY, AND A PATTERN IS NOW
  VISIBLE.** SMN1 identified 1995, first drug 2016: **twenty-one years.** CFTR
  cloned 1989, first modulator 2012: **twenty-three years.** Two records, two
  mechanism moves, two lags of about two decades — and in both cases **the route
  was not predictable from the mechanism.** Cystic fibrosis expected gene therapy
  and got protein chemistry; spinal muscular atrophy's mechanism handed the field a
  splicing target nobody would otherwise have looked for. #183 asked what a
  mechanism move buys. Answer so far: **everything, eventually, about twenty years
  later, by a door nobody was watching.**
- **#191 (the outcome is beyond any measurable horizon) — its sharpest case, one
  record after it was written.** A single irreversible infusion in a newborn, whose
  durability beyond a few years is unproven and cannot be proven for decades — and
  whose alternative was tested against a surrogate. **#191's problem plus #192's
  irreversibility is a genuinely new combination**: the decision cannot be
  verified and cannot be revised.
- **#178 (prognostic quality follows a forcing decision) — a fifth case, and the
  mechanism hands it over directly.** *SMN2* copy number predicts severity
  inversely and reliably, from a blood test at birth. The forcing decision is
  explicit: **screening finds presymptomatic infants and somebody must decide whom
  to treat within weeks.** For two and three copies the answer is settled; for four
  it is contested, and the trial to settle it would take decades.
- **#170 (a treatment pulls the definition upstream) — the BEST case in the
  corpus.** `alzheimers` was the most premature and `parkinsons` worse still.
  Here, newborn screening plus treatment within days produces children who **sit,
  walk and run on a normal schedule**, in a disease whose type 1 form means never
  sitting and dying by two. **#170's range is now fully mapped and the ordering
  variable is confirmed: the value of pulling a definition upstream is entirely a
  function of what is waiting there.**
- **#147 (the disease is a byproduct of capability) — inside one record, and it is
  brand new disease.** SMN assembles the spliceosome in every cell. Children now
  surviving with restored but sub-normal SMN are showing sensory, autonomic,
  cardiac and metabolic features **nobody had ever seen, because nobody lived long
  enough to show them.** Whether the treated phenotype is a milder version of the
  same disease or a different one is open, and it determines what these children
  are monitored for over sixty years.
- **#124 (a cure is a one-time sale) — and the financing had to be reinvented.** A
  single seven-figure payment for a benefit realised over sixty years fits no
  annual budget, no formulary and no cost-effectiveness threshold. **Outcomes-based
  agreements and annuity-style instalments were invented because the product forced
  them**, which is #188's demonstrated-and-not-copied shape arriving in payment
  design rather than in delivery.

---

## 194. An approval can foreclose the evidence that would have justified it · **open**
*Forced by:* `duchenne`.

Four exon-skipping drugs were licensed between 2016 and 2021 on **accelerated
approval**, on the strength of dystrophin measured by western blot at a fraction
of one percent of normal. The agency's own statistical and clinical reviewers
recommended against the first; the advisory committee voted against it; the centre
director approved it; and the decision was appealed internally and allowed to
stand. In 2023 a micro-dystrophin gene therapy was approved after its confirmatory
trial **missed its primary endpoint**.

**A decade later nobody knows whether any of them work — and the approvals are
part of why.**

Accelerated approval is a promise: license now on a surrogate, prove clinical
benefit afterwards. **The act of licensing systematically degrades the conditions
for keeping that promise:**

| after approval | consequence for the confirmatory trial |
|---|---|
| the drug is available | **randomising a boy to placebo becomes very hard to justify to a family** |
| the standard of care shifts | the comparator arm is no longer standard care |
| the eligible population is on the drug | recruitment collapses |
| the sponsor holds a licensed product | the incentive is to complete slowly, if at all |
| withdrawal is politically costly | a failed trial does not reliably remove the drug |

**This is not #102, and the distinction is the whole point.** #102 (forced by
`marburg`) says some diseases can never generate the evidence their approval
requires — six hundred cases in fifty-eight years, and a phase III trial is
**impossible in nature.** Here the trial was entirely possible in 2015.
**The approval is what made it hard.** It is a self-inflicted version of the same
condition.

Nor is it #167 (missing versus withheld evidence). The evidence is neither
missing nor concealed. **It has been rendered unobtainable by a decision taken to
help.**

**The case for accelerated approval in this record is real and should be stated
plainly**: a fatal childhood disease, no alternatives, a slow noisy course, and
families for whom waiting is not a neutral option. The pathway exists for exactly
this. **The observation is that it carries a cost nobody prices** — the option
value of being able to find out — and that cost falls on the next cohort of
children, who inherit a treatment landscape of unknown value and no clean way to
evaluate it.

One counter-example exists and took about a decade: a European conditional
authorisation for a readthrough agent in the same disease **was not renewed**
after its confirmatory trial failed. That is the mechanism working, slowly, once.

Where else it applies: `alzheimers` (aducanumab, approved over its advisory
committee, later withdrawn commercially), and any oncology approval on
progression-free survival where the overall-survival question then becomes
unrecruitable.

Minimal move: record, alongside a conditional or accelerated approval, **whether
the confirmatory evidence is still obtainable.** It is a yes/no a regulator could
answer at the time of approval, and it would make the trade explicit rather than
implicit.

---

## 195. `src` records where a number came from, not how good the evidence behind it is · **open**
*Forced by:* `duchenne`.

Three records, three efficacy figures, all `src: reasoning`:

| record | `efficacy` | what it rests on |
|---|---|---|
| **hepatitis-c** | 0.95 | sustained virological response — a definitive binary endpoint in large trials |
| **cystic-fibrosis** | 0.80 | large randomised trials with unambiguous functional endpoints |
| **duchenne** | **0.40** | a corticosteroid, plus **four approved drugs whose benefit is unestablished after a decade** |

**A reader cannot tell them apart, and the schema offers nothing that would.**

`src` has two values in practice — `recall` and `reasoning` — and both describe
**how the author of the record obtained the number**, not **how good the world's
evidence for it is.** `check.py` warns on `src: recall`, which polices the
register's own diligence and says nothing about whether the underlying literature
is a definitive trial or a contested western blot.

The register already has the right instrument and applies it to the wrong object.
**`standing` — `documented` / `alleged` / `disputed` / `refuted` — exists to
grade how well-established a *blocker* claim is**, and it was built precisely so
the register could test the "it's solvable, pharma won't allow it" refrain
instead of echoing it. **Nothing grades the record's own ratings that way.**

This completes a family of three, all about a number the register cannot be
trusted on for a different reason:

- **#167** — the evidence exists and was **withheld** (oseltamivir; the rating was
  wrong for fifteen years)
- **#191** — the evidence cannot exist **yet**, and will not within the decision's
  horizon (cystic fibrosis modulators; the answer arrives around 2080)
- **#195** — the evidence exists, is public, and **people who have read it
  disagree about what it shows**

Each has a different fix — disclosure, waiting, or marking the dispute — and one
`src` field for all three.

**And the consequence is not academic.** `duchenne` derives `capability: partial`
and `reach: 0.14`, and those numbers would be approximately unchanged if the four
accelerated-approval drugs did not exist. **A register whose purpose is "what
should we work on next" should be able to say that a record's headline figure is
carried entirely by a 1950s steroid and a ventilator**, and that the expensive
part of the landscape is unevidenced.

Minimal move: extend `standing` to ratings, or add an `evidence:` qualifier
alongside `src` — trial / surrogate / observational / **contested** / unproven. It
would be uncomfortable to fill in honestly, which is the argument for it.

---

**Strengthened by `duchenne`, not new:**

- **#193 (some `knowledge` blockers are engineering blockers) — THE THIRD DATA
  POINT, AND IT COMPLETES THE PATTERN EXACTLY BACKWARDS.** *DMD* was cloned in
  **1986**, *CFTR* in **1989**, *SMN1* in **1995** — and the therapeutic outcomes
  run in the opposite order. Duchenne has no proven disease-modifying drug beyond a
  corticosteroid found empirically in the 1950s. **The explanatory variable is
  deliverability every time**: motor neurons are post-mitotic and reachable by an
  intravenous vector; airway epithelium sits behind mucus and turns over; and
  Duchenne needs a 2.4-megabase gene delivered to forty percent of body mass, into
  tissue that regenerates, against an immune system that treats dystrophin as
  foreign. **Three records, three decades of biology, and the constraint was never
  understanding.**
- **#183 (`mechanism` has never moved) — a FOURTH entry, and the earliest gene
  with the worst return.** Four mechanism moves now, four lags of decades, and in
  three of four the route was not predictable from the mechanism. **Duchenne is the
  exception that proves it**: the difficulty *was* predictable in 1986 — the gene
  was known to be enormous and the target tissue known to be the whole body — and
  the field proceeded anyway.
- **#148 (toll judged against the alternative) — with children.** The only
  treatment of unambiguous benefit is a daily corticosteroid given to a growing boy
  for a decade, producing growth suppression, **vertebral compression fractures**,
  cataracts, adrenal suppression and delayed puberty. It is given universally
  **because the alternative is a wheelchair at ten instead of thirteen.**
  Vamorolone, approved in 2023, is the first improvement to that trade in thirty
  years.
- **#147 (the disease is a byproduct of capability) — inside one record, third
  time.** Ventilation solved respiratory failure and **revealed cardiomyopathy**,
  which is now the leading cause of death. `cystic-fibrosis` produced CF-related
  diabetes the same way; `spinal-muscular-atrophy` is producing a treated phenotype
  nobody had seen.
- **#170's inverse: a screening decision lagging the treatment by thirty years.**
  Creatine kinase is elevated from birth and costs almost nothing to measure.
  Newborn screening was piloted and **discontinued in several places on the
  explicit ground that there was no treatment** — reasoning that has since expired,
  since steroids and cardiac medication both work better started early. `spinal-
  muscular-atrophy` got the screen and the drug together; this got neither, then
  the drug, and still no screen.
- **#174 (you got the worse version) — and here the cheap thing is what works.**
  Corticosteroids, ventilation and cardiac care doubled median survival, cost very
  little, and are unavailable to most of the world's patients — **while the
  expensive and unevidenced part of the landscape absorbs the attention, the
  litigation and the money.**
- **A population absent from every field.** Duchenne is X-linked and female
  carriers are not uniformly unaffected: a minority have skeletal muscle
  involvement and a substantial fraction develop cardiomyopathy warranting
  surveillance. They are in no prevalence figure, no burden figure, and no
  register.

---

## 196. Interventions are shared across records, and the graph has only disease-to-disease edges · **open**
*Forced by:* `rheumatoid-arthritis`.

Adalimumab is licensed for rheumatoid arthritis, **Crohn's disease** (held),
ulcerative colitis, psoriasis, psoriatic arthritis, ankylosing spondylitis,
uveitis and hidradenitis suppurativa. One molecule, one mechanism, eight
entities.

**#160 gave the register disease-to-disease edges** — contains, causes, is
manufactured by, is the mode of death of. **#177 gave them a sign.** Neither
covers this: the shared object is not a cause, it is **the treatment**, and it
means several records' blockers are the same blocker wearing different names.

Four consequences, and none is visible in any file:

1. **A price change moves every record at once.** European biosimilar entry in
   2018 cut adalimumab's price by seventy to ninety percent — for rheumatoid
   arthritis *and* Crohn's *and* psoriasis *and* the rest. The register records a
   `cost` blocker in each, with no way to say they are one negotiation.
2. **A safety signal is shared.** Latent tuberculosis screening is mandatory
   before TNF inhibition **in every one of those indications**, which is a live
   link between this record and `tuberculosis` that appears in neither. The JAK
   inhibitor cardiovascular and malignancy warnings propagated across indications
   the same way.
3. **Evidence transfers unevenly and nobody tracks it.** A mechanism proven in one
   indication is tried in the others, and the sequencing question —
   *which biologic first* — is asked independently in each, with no shared answer.
4. **And it is a finding about the diseases.** If one mechanism treats eight
   entities, those entities share something their names conceal. **The
   intervention is evidence about the taxonomy.**

Once named, the corpus is full of it:

| intervention | records it serves |
|---|---|
| **TNF inhibition** | rheumatoid-arthritis, **crohns**, psoriasis, ankylosing spondylitis, uveitis |
| **GLP-1 agonists** | **obesity**, **type-2-diabetes**, **chronic-kidney-disease**, **cirrhosis** (MASH), heart failure |
| **SGLT2 inhibitors** | **type-2-diabetes**, **chronic-kidney-disease**, heart failure |
| **corticosteroids** | **duchenne**, **covid-19**, **multiple-sclerosis**, and half the corpus |
| **transplantation** | **cirrhosis**, **chronic-kidney-disease**, **cystic-fibrosis**, liver-cancer |

**Distinguish it from #87 carefully, because the fix differs.** #87 (forced by
`noma`) is about *non-specific preventive* interventions — child nutrition,
tobacco control — whose benefit spreads across entities so that **no record can
justify a share of the cost.** That is an allocation problem.

**This is a specific licensed product with a specific mechanism**, and the problem
is not apportionment — it is that **solving one record's blocker solves several,
and the register cannot see the leverage.** A foundation deciding where to put
money at the TNF or GLP-1 node is buying movement in four to eight records at
once, and every triage view here would show it one.

Minimal move: intervention nodes in the graph #160 proposed, with edges to every
record they serve. It is the same data model, extended by one node type, and it
would make the register's answer to "what should we work on next" include *the
things that move several records at once.*

---

## 197. A price is a policy outcome, and `scale` records it as a measurement · **open**
*Forced by:* `rheumatoid-arthritis`, and it resolves a question `multiple-sclerosis`
left open.

Adalimumab was the best-selling medicine in the world. **European biosimilars
entered in late 2018 and prices fell by roughly seventy to ninety percent.** In
the United States the same molecule held its price until **2023**, because the
originator had assembled a patent estate numbering in the hundreds around
formulation, manufacturing and injection device, and biosimilar applicants
settled for delayed entry.

**Same molecule. Same evidence. Same year. An order of magnitude apart. The
variable is patent law.**

The register's `cost` blockers carry a `scale` — a number — which reads as a
property of the intervention. **It is the current state of a negotiation.** And
the corpus now holds four on-patent products with four completely different price
trajectories:

| record | what happened | why |
|---|---|---|
| **rheumatoid-arthritis** | fell ~80% in Europe 2018, **five years later in the US** | biosimilar pathway working, versus a patent thicket |
| **multiple-sclerosis** | **rose** when competitors entered | rebate-driven list pricing, patients who cannot switch on price |
| **type-1-diabetes** | **no generic for a century**, then fixed | insulin sat in a regulatory category with no abbreviated pathway until a 2020 statute |
| **hepatitis-c** | from ~$84,000 to under $100 in some markets | voluntary licensing and generic manufacture |

**Four records, four trajectories, and the molecule is never the variable.** It is
patent strategy, regulatory pathway design, licensing policy and procurement.

**#52 (solved here, not there) is about access differing.** This is about **the
price itself being an artefact of policy**, which is upstream of access and is
moved by different people — legislators, patent offices, regulators writing
approval pathways, and procurement agencies — none of whom appear prominently in
`who_could`.

Two things follow:

- **`scale` is not forecastable and the register presents it as though it were.**
  A `cost` blocker priced at today's list is describing a number that has
  historically moved by an order of magnitude in either direction within five
  years.
- **The interventions that fix it are cross-cutting and belong to no record** —
  biosimilar pathway design, patent thicket reform, pooled procurement, voluntary
  licensing. That is #164's shape, and #188's: **hepatitis C's voluntary licensing
  and Europe's biosimilar pathway are demonstrated and unevenly copied.**

Minimal move: on a `cost` blocker, record **what determines the price** — on
patent, thicketed, biosimilar-eligible, generic, licensed — rather than only what
it currently is.

---

**Strengthened by `rheumatoid-arthritis`, not new:**

- **#89's second failed exemplar, and the rung is fine.** `remaining.org` queued
  both `multiple-sclerosis` and this record as "positive exemplars for
  `disease-modifying`", and **both climbed past it to `suppressive`.** The
  hypothesis that `disease-modifying` is a waiting room is **refuted by the data**:
  its seven occupants run from `alzheimers` at efficacy 0.25 to **`cholera` at
  0.98**. It is a wide rung, and `efficacy` is what separates its inhabitants —
  which is the schema working, not failing.
- **#39 (an entity can be a final common pathway) — SECOND CONFIRMATION OF ITS
  PREDICTION.** Five licensed mechanisms, each working in roughly half of
  recipients, and nothing predicting which. #39 predicted that **stratified trials
  would succeed where unstratified ones do not**; a randomised trial stratifying
  patients by **synovial biopsy B-cell status** found differential response between
  anti-B-cell and anti-IL-6 therapy. That is the second confirmation after
  `sepsis`'s endotypes, in a completely different disease, and #39 was marked
  **BUILD IT** two records ago.
- **#194's counter-example, and it is worth recording.** Regulators mandated a
  post-authorisation safety trial for JAK inhibitors; **the trial ran, found higher
  cardiovascular and malignancy rates than TNF inhibitors, and boxed warnings
  followed across the class.** #194 says accelerated approval degrades the
  conditions for confirmatory evidence. **Here the confirmatory requirement
  worked** — which suggests the difference is whether the question is about *harm*
  (answerable in a comparative safety trial nobody has to be randomised to
  placebo for) or about *benefit* (which needs the placebo arm the approval just
  made unrecruitable).
- **#182 (the magnitude is deaths) — a second disability record, and one whose
  disability is disappearing.** Thirty-five thousand attributed deaths against
  eighteen million people, joint surgery rates falling substantially, and the
  textbook deformities becoming uncommon where treatment reaches. **Medical
  students are taught to recognise signs they will increasingly not see** — and the
  register stores an undated snapshot of a clinical picture that has moved (#91).
- **#170 (a treatment pulls the definition upstream) — the same middling answer as
  `type-1-diabetes`, in a completely different organ.** Anti-citrullinated protein
  antibodies precede arthritis by years; randomised trials of treating at-risk
  people with rituximab, abatacept and methotrexate consistently show **delayed
  onset rather than prevention** — the curves separate during treatment and
  converge after. Teplizumab does the same thing in type 1 diabetes. **Two records,
  two organs, same result: pulling the definition upstream bought time, not
  avoidance.**
- **#188 (demonstrated and copied, for once).** Treat-to-target is a decision rule
  rather than a molecule — measure disease activity every visit, escalate until
  remission — and it moved outcomes as much as several of the drugs did. **It was
  copied**, quickly and widely, because it cost nothing and professional societies
  pushed it. That is worth recording next to the demonstrated-and-*not*-copied
  entries, because it identifies the conditions under which copying happens.

---

## 198. `mechanism` is not always on the path to the treatment · **open**
*Forced by:* `congenital-heart-disease`, against the three records before it.

The last three records built an arc: a gene is found, and a therapy follows after
about two decades, by a route nobody predicted.

| record | gene | first real therapy | lag |
|---|---|---|---|
| **duchenne** | 1986 | — *still nothing that works well* | 40 years |
| **cystic-fibrosis** | 1989 | 2012 | 23 years |
| **spinal-muscular-atrophy** | 1995 | 2016 | 21 years |
| **congenital-heart-disease** | *various, from the 1990s* | **1944** | **minus fifty years** |

The Blalock-Taussig shunt was performed in 1944 and cardiopulmonary bypass in
1953 — decades before anybody had sequenced anything, and the operations were not
derived from any molecular understanding because there was none to derive them
from. **Genetics has since identified 22q11.2, *NKX2-5*, *GATA4*, *TBX5* and the
rest, explained a minority of cases, and produced no therapy whatever** — and
would not be expected to. **You do not need to know why a septum failed to close
in order to close it.**

**The register's implicit causal model is understand → treat**, and every gap in
the #183 family assumes it: `mechanism` moves, and the question is what it buys.
For a whole class of disease that arrow does not exist.

| class | is mechanism on the path? |
|---|---|
| infectious, metabolic, autoimmune, monogenic | **yes** — the target is molecular |
| **structural and mechanical** | **no** — the target is anatomical |

And the second row is not small: **congenital heart disease** (the commonest
birth defect), **cataract** (the leading cause of blindness, cured by carpentry
with no molecular understanding whatever), fractures, hernia, appendicitis, cleft
palate, obstetric fistula, and most of surgery.

**Two consequences, and the second is a triage claim.**

*The `mechanism` rating misleads by omission.* This record rates `partial`, which
reads as a deficiency, and the deficiency is irrelevant to whether children live.
A reader ranking research priorities by mechanism-uncertainty would fund
embryology here and be wrong.

***For structural disease the answer to "what should we work on next" is
surgeons.*** Not targets, not trials, not platforms. The intervention has existed
for eighty years and reaches roughly one child in seven. **#193 said some
`knowledge` blockers are really engineering blockers with a price. This says some
records have no meaningful knowledge blocker at all**, and the register's habit of
filing one in every record obscures that.

Minimal move: mark whether a record's `mechanism` is **on the causal path to its
treatment.** It is one boolean, it would be `false` for perhaps ten records, and
it changes what those records recommend.

---

## 199. A window can close by inverting the intervention, not by expiring it · **open**
*Forced by:* `congenital-heart-disease`.

A large unrepaired left-to-right shunt sends excess blood to the lungs, and the
pulmonary arterioles remodel irreversibly. Once pulmonary resistance exceeds
systemic, the shunt **reverses** — **Eisenmenger syndrome** — and at that point
closing the defect is **contraindicated and would kill the patient**, because the
shunt has become the right ventricle's only escape from a circulation it can no
longer drive.

**The same operation, on the same anatomy, that would have cured this child at six
months will kill them at five years.**

The register has eight `window` gaps and none says this:

| gap | what happens when the window closes |
|---|---|
| **#18** | capability changes with timing |
| **#24** | the window cuts both ways |
| **#71** | records that people are late, never why |
| **#94** | it can be measured rather than assumed |
| **#96** | it closes before there is anything to diagnose |
| **#112** | catching it is not always worth it |
| **#131** | nobody knows whether it exists |
| **#185** | it is open, populated, and empty |
| **#199** | **the intervention becomes harmful** |

Every one of the others treats window closure as **loss of benefit**. The schema
follows: `caught_in_time` is a fraction, and missing it means the intervention
was wasted. **Here missing it means the intervention is now a way to kill
somebody**, and the schema has no way to distinguish *too late to help* from *too
late, and now dangerous.*

Once named, the corpus has more:

| record | after the window |
|---|---|
| **congenital-heart-disease** | closing the shunt is fatal |
| **stroke** (held) | thrombolysis causes haemorrhagic transformation |
| **sepsis** (held) | fluid resuscitation that helps early harms late |
| **covid-19** (held) | dexamethasone helps late and trends toward harm early — **the same inversion, running the other way** (#157) |
| reperfusion after prolonged limb or bowel ischaemia | restoring flow causes reperfusion injury |

**And it explains something the register keeps recording as a coincidence.** #157
collected interventions whose *sign* flips — with setting, with stage, with which
pathogen. **This is the same phenomenon indexed by time**, and the two gaps are
probably one: **an intervention's effect has a sign, and several variables can
flip it, of which elapsed time is the commonest.**

Minimal move: `window` gains a statement of what happens *after* it — nothing,
less benefit, or **harm.** Where the answer is harm, the record is describing a
contraindication rather than a missed opportunity, and clinicians and funders need
to read it differently.

---

**Strengthened by `congenital-heart-disease`, not new:**

- **#147 (the disease is a byproduct of capability) — ITS SHARPEST INSTANCE,
  BECAUSE IT WAS DESIGNED AND PREDICTED.** A child with one functional ventricle
  cannot be repaired, so surgeons **substitute a circulation**: venous blood routed
  passively to the lungs, which requires permanently elevated venous pressure and
  was known to from 1971. Three decades later: **Fontan-associated liver disease**,
  with fibrosis close to universal and cirrhosis and hepatocellular carcinoma
  occurring, plus protein-losing enteropathy and lymphatic failure. **A cardiac
  operation produces a liver disease on a thirty-year timetable, and `cirrhosis`
  is a record here with no way to say where a share of it came from.** Unlike
  `sepsis`'s diffuse iatrogenic share, this one is a row in a strata table.
- **#154 (interventions that are infrastructure) — in its most personnel-intensive
  form, and with a delivery-model dispute the register should name.** A paediatric
  cardiac programme needs a congenital surgeon, a paediatric cardiac
  anaesthetist, a **perfusionist**, a trained cardiac ICU, an echocardiographer who
  can read a neonate, a cath lab and a blood bank — every one a years-long
  training pipeline, and removing any one stops the rest. **Visiting surgical
  missions operate on children who would otherwise die and then leave; local
  capacity building takes a decade and lasts.** The evidence favours the second and
  the funding favours the first, because a mission produces photographs within a
  budget cycle.
- **#175 (the instrument carries a population-dependent inaccuracy) — THIRD RECORD
  RECOMMENDING PULSE OXIMETRY WITHOUT QUALIFYING IT.** After `childhood-pneumonia`
  and `covid-19`, this record's newborn screen for critical congenital heart
  disease depends on detecting a few percentage points of desaturation — and pulse
  oximetry accuracy varies with skin pigmentation. `measurement.diagnostic:
  objective` says nothing about it, in a screen aimed at newborns.
- **#124 / #188 (a one-time cure struggles to be financed) — and here there is
  nobody on the other side of the table.** An operation costing a few thousand
  dollars buys seventy years of normal life, competes as a lump sum against
  recurring line items, and **has no patent and no manufacturer to negotiate
  with** — which makes it unusual in this register and, in principle, easier than
  every drug-pricing blocker in the corpus.
- **#147, administratively: capability created a cohort with no home.** There are
  now more adults than children living with congenital heart disease in several
  countries, and a substantial share are **lost to specialist follow-up at the
  transition from paediatric services** — reappearing years later with arrhythmias
  and heart failure that were manageable. `cystic-fibrosis` and
  `spinal-muscular-atrophy` are generating the identical problem a generation
  behind.
- **#159 (prevention of a birth rather than of a disease) — and sharper here.**
  Fetal echocardiography identifies major lesions and a substantial share of
  pregnancies with severe diagnoses are terminated. **Many of these lesions are
  correctable**, so what is being weighed is not a fatal condition but a difficult
  one — and the register files it in the same field it uses for a bed net.

---

## 200. The remedy can be in the environment, and every axis is patient-scoped · **open**
*Forced by:* `hearing-loss`.

**Automatic captioning has probably done more for more people with hearing loss
in the last decade than any device**, and it appears nowhere in this schema — not
in `intervention`, not in `efficacy`, not in `access`, not in `blockers`.

Nor do hearing loops in public buildings, sign language interpretation, acoustic
design that does not defeat a hearing aid, or text alternatives to voice-only
systems. **Each removes a disability without touching an ear.**

The register's axes are all applied to the patient's body:

| field | what it asks | what it cannot ask |
|---|---|---|
| `intervention` | what can be done **to the patient** | what can be changed **around them** |
| `efficacy` | fraction of patients in whom it works | whether the environment was altered instead |
| `access` | fraction who can obtain it | whether they needed to obtain anything |
| `residue` | what the disease left in the patient | what the built world does to them |

That is the **medical model of disability**, encoded structurally, and the record
that forces it is the one where the alternative model has been argued for fifty
years. **The social model holds that impairment and disability are different
things**: the ear is impaired, and the disability is produced by a meeting whose
audio is not captioned.

**This is not #58 and not #87.** #58 (forced by `onchocerciasis`) says an
intervention can be scoped to transmission rather than to the patient — it is
still administered to bodies. #87 (forced by `noma`) says a *preventive*
intervention can be non-specific and unpriceable across records — child
nutrition, tobacco control. **This says the remedy need not be an intervention on
a person at all.**

It applies immediately across the block this record opens:

| record | the environmental remedy |
|---|---|
| **hearing-loss** | captioning, loops, interpretation, acoustic design |
| **cataract** (held) | — *genuinely medical; the useful contrast* |
| low vision (not held) | screen readers, contrast standards, tactile paving |
| **osteoarthritis** (queued) | step-free access, seating, workplace adaptation |
| mobility impairment (not held) | the entire built environment |
| **me-cfs**, **heds** (held) | remote work, flexible hours, pacing |

**And it changes what the register recommends.** A funder reading this record sees
`access: 0.20` — a device-fitting figure — and concludes: buy hearing aids. **The
intervention with the largest reach in the last decade was a regulatory
requirement and a speech recognition model**, and no field here can say so.

Minimal move: `intervention` gains a scope — **person / environment / both** — and
`blockers` can name an accessibility regulator. It would be filled in for perhaps
eight records and it is the difference between a register of medicine and a
register of what actually helps people.

---

## 201. A population can dispute that the record is a disease · **open**
*Forced by:* `hearing-loss`.

Every `contested: true` record in this register disputes a **boundary**: where
sepsis begins, whether obesity is a disease or a risk state, whether
schizophrenia is one thing, where the hypertension threshold goes. Those are
arguments among clinicians and researchers about definitions, conducted in
journals, and `contested` was built for them.

**Here the argument is different in kind.** Many culturally Deaf people hold that
deafness is not a pathology but a **linguistic and cultural identity** — sign
languages being full natural languages with their own grammar, literature and
communities — and that the disadvantage is produced by the hearing world's
arrangements rather than by the ear.

**It is a position held by the people the record is about, and its history is
why it is held so firmly.** An international congress in 1880 voted to exclude
sign language from deaf education in favour of forced speech and lip-reading, and
for roughly a century deaf children were punished for using their language. The
documented result was worse literacy and worse outcomes. **A medical and
educational consensus harmed a population for a hundred years**, and scepticism
about the next confident intervention is earned rather than irrational.

**The register's axes all presume the patient wants the intervention.**
`efficacy` is the fraction in whom it works; `access` is the fraction who can get
it; `orphaned` means nobody is delivering something people want. **None can
express that a meaningful share of the affected population disputes the framing.**

**Distinguish it from #140 carefully.** That gap (forced by `uterine-cancer`) is
an **individual** choosing a worse clinical outcome for a reason — fertility over
certainty — and not making a mistake. **This is a population disputing the
category**, which is upstream of any individual choice and is not resolvable by
better shared decision-making.

Where else it will arrive, and the register should be ready:

| entity | the contesting position |
|---|---|
| **hearing-loss** | Deaf culture; opposition to routine paediatric implantation |
| autism (not held) | neurodiversity; that it is a difference rather than a disorder |
| dwarfism (not held) | opposition to limb lengthening |
| intersex variation (not held) | opposition to infant surgery |
| **me-cfs**, **heds** (held) | the inverse — a population **demanding** disease status the medical system withholds |

**That last row matters and it is the reason to build this carefully.** The same
field must be able to record a population saying *this is not a disease* and a
population saying *this is a disease and you will not admit it*. They are the same
structural fact — **who gets to decide what counts as pathology** — pointing in
opposite directions.

**The discipline is the one `standing` already applies.** Record that the dispute
exists, who holds it, and what it is about. Do not adjudicate it, and do not let
the register's silence read as agreement with the medical framing by default.

Note what is *not* disputed in this record, because it is the model for how to
write these: **language deprivation is real, and both spoken and signed language
prevent it.** The parties agree on the developmental fact. What they disagree
about is which language a child should be given, and by whom that is decided.

---

**Strengthened by `hearing-loss`, not new:**

- **#182 (the magnitude is deaths) — ITS STRONGEST CASE, AND IT IS NOT CLOSE.**
  Roughly **430 million** people with disabling hearing loss and **zero** attributed
  deaths — four and a half times `cataract`'s headcount, in the same
  no-mortality position. #48's proposed fix, a mortality weight, would rank the
  largest disability burden in this corpus at exactly zero. **And the same
  arithmetic operates on real budgets**: a major public insurer has excluded
  hearing aids by statute since 1965, which is `obesity`'s categorical legislative
  carve-out in a second record.
- **#160 (the flat list) — a substantial and unquantified share of this record is
  manufactured by other records in it.** Aminoglycosides cause permanent deafness,
  and `tuberculosis` documents that injectable aminoglycosides were standard
  MDR-TB therapy for decades; `cre` and `sepsis` record their use too, and `cre`'s
  own `toll` field names "aminoglycoside hearing loss" explicitly. **Cisplatin
  deafens a large share of children treated for cancer.** The people deafened by
  those decisions are in this record and nothing connects them.
- **#175 (population-dependent instruments) — the counter-example, and it is
  useful.** Newborn hearing screening uses otoacoustic emissions and automated
  auditory brainstem response, which are physiological and do not carry the
  population-dependent inaccuracy that pulse oximetry does. **After three records
  in which this register recommended a pulse oximeter without qualifying it, it is
  worth recording an infant screen that does not have the problem.**
- **#161 (the treatment addresses what kills you, not what bothers you) — with an
  unusual twist.** People wait **eight to ten years** from noticing hearing loss to
  obtaining a hearing aid, and a third to a half of dispensed devices go unworn.
  Unlike the asymptomatic cases #161 was built for, **here the patient perceives
  the problem perfectly well and declines to name it** — stigma specific to a
  device that marks age in a way spectacles stopped doing decades ago. And the
  delay is not free: duration of deafness predicts how much benefit a device
  delivers.
- **#189 (the treatment threshold is set by capacity) — and here the outcome
  measured is the wrong one.** `efficacy: 0.75` describes benefit in people who use
  a device, and fitting is what the field counts. **A hearing aid in a drawer is
  recorded as coverage.** The same problem `maternal-haemorrhage` solved by
  anchoring effective coverage to an outcome rather than to a procedure.

---































































**Strengthened by `typhoid`, not new:**

- **THE THIRD BACKWARDS `moved` ENTRY, AND THE FIRST CAUSED BY THE TREATMENT
  ITSELF.** Yaws' 1964 regression was a campaign wound down; measles' 2020 was
  coverage falling. **Typhoid's 2016 entry — `efficacy: 0.99 → 0.95` — is the
  antibiotics being used**, which is the only way they could have failed. Nothing
  about the disease changed. It has simply been treated for seventy-five years.
- **The diagnostic enum needs a fourth value: *a test exists, is in routine use,
  and misleads.*** Blood culture misses a third to a half of typhoid cases and is
  largely unavailable; the **Widal test** is a century old, performs poorly, and
  is the mainstay across much of the endemic world. `objective`, `clinical` and
  `complaint` cannot express that — and the distinction matters, because **a bad
  test produces confident wrong answers, and confident wrong answers get
  antibiotics.** The record rates `clinical` as the honest description of what the
  diagnosis actually rests on.
- **And the loop closes on itself.** A bad test produces empirical antibiotics,
  which produce resistance, which raises the value of the vaccine — **which is
  hard to argue for because the bad test means nobody can say how many cases there
  are.** Over-diagnosed clinically, under-diagnosed microbiologically, in the same
  disease, for the same reason.
- **#100 (patient-scoped) — and here chronic carriage is how the species
  survives.** Ebola forced this gap: cure does not end transmissibility, and
  filovirus persistence occasionally restarts an outbreak. **Typhoid's carriers
  are not an occasional complication — they are the reservoir**, and *S.* Typhi
  has no animal host, so the disease persists between epidemics entirely inside
  well people.
- **#85 (eradicability is revisable) — and typhoid is on the shortest list with
  the worst asterisk.** No animal reservoir, like smallpox and dracunculiasis. And
  the human reservoir is asymptomatic, undiagnosable without culture, and
  uncleavable with current drugs. **Eradicable in principle and blocked by the
  fact that you cannot find the people who have it.**
- **#87 (the intervention is non-specific) — the same pipes, the eleventh
  instance.** Sewers and water treatment prevent typhoid, cholera, hepatitis A,
  diarrhoeal disease and much of the helminth burden. Two consecutive records now
  point at one civil engineering programme costing tens of billions and
  chargeable to none of them.
- **#109 (prevention has no coverage field) — fourth record.** The 2018 `moved`
  entry records the conjugate vaccine under `access`, because what actually rose
  was vaccination coverage and there is nowhere to put it. Measles, cervical
  cancer, colorectal cancer and now typhoid.
- **A policy blocker where both directions kill people.** In much of the endemic
  world antibiotics are sold without prescription — which gets a febrile person
  treated quickly and **is a principal driver of the resistance dismantling this
  record.** Restricting sales before providing diagnosis and reliable care would
  kill people. The blocker vocabulary assumes obstacles are things somebody is
  failing to do, and has no way to record a genuine dilemma.

---

**Strengthened by `cholera`, not new:**

- **#98 (benefit is only course alteration) — THE SHARPEST CASE THE CORPUS WILL
  PRODUCE, AND IT SHOULD SETTLE THE GAP.** Oral rehydration solution takes cholera
  case fatality from about fifty percent to under one percent. It costs cents. It
  is salt, sugar and clean water, derived directly from the observation that
  cholera toxin destroys secretion and leaves glucose-coupled sodium absorption
  intact. **It does not touch the bacterium, so it is `symptomatic`.** This
  record rates `disease-modifying` and **earns that from the antibiotic** — an
  optional adjunct that shortens the illness. *The dispensable half of the
  treatment supplies the rating and the indispensable half is invisible.*
- **`toll: none` and `restored: restored` on a disease that kills half its severe
  untreated cases.** Fifth record in sixty-five to carry a zero toll, alongside
  H. pylori ulcer, hepatitis C, PKU and rabies. **Enormous lethality, complete
  recovery, a treatment that costs cents and harms nobody** — and `capability:
  partial`.
- **#129 (prevention can be unintentional) — THE CONTROL CASE, AND IT WAS
  DELIBERATE.** Cholera left Europe and North America because sewers were built
  and water was treated, on purpose, partly for this reason. #129 said the
  register can only record deliberate acts and therefore misses the undeliberate
  ones. **Cholera shows the deliberate ones are unrecordable too, when they are
  civil engineering rather than medicine.** The problem is not intent — it is
  that `prevention` is scoped to things clinicians do.
- **#87 (the intervention is non-specific) — and water is the largest instance in
  the register.** Sewers and water treatment prevent cholera, typhoid, hepatitis
  A, most diarrhoeal disease and much of the soil-transmitted helminth burden
  simultaneously. **Five records, one set of pipes, chargeable to none of them**,
  and the cost is in the tens of billions. Ten gaps now point at #87.
- **`manufacturing` — SIXTH INSTANCE, AND THE PATTERN IS NOW EXHAUSTIVE.**
  Snakebite antivenom, benzathine penicillin, pandemic influenza vaccine,
  smallpox vaccine, BCG, and oral cholera vaccine. Every one decades old, cheap,
  biologically produced, essential, and chronically short — and in 2022 the
  international coordinating group **suspended the standard two-dose cholera
  regimen in favour of one dose specifically to stretch the stockpile.** That is
  announced rationing of a product costing a few dollars.
- **#85 (eradicability is revisable) — and here the answer is settled and
  negative.** *Vibrio cholerae* is a free-living marine organism persisting in
  estuaries with copepods and plankton. **The reservoir is the ocean**, and no
  amount of case-finding removes it. Dracunculiasis warned that eradicability
  scores can be wrong; cholera is the case where the negative answer will not
  revise.
- **A mechanism complete enough to have produced its own therapy.** Toxin →
  ADP-ribosylation of Gs → constitutive adenylate cyclase → cAMP → CFTR → litres
  of water. **And the same chain explains the cure**, because the toxin acts on
  secretion and leaves absorption intact. The register keeps looking for cases
  where understanding the mechanism produced the treatment; alongside CML's
  imatinib and RCC's belzutifan, this is the third — and it is the cheapest by
  several orders of magnitude.

---

**Strengthened by `uterine-cancer`, not new:**

- **#136 (the pathway performs differently depending on who presents) — SHARPEST
  INSTANCE, ONE RECORD AFTER IT WAS NAMED.** Postmenopausal bleeding is specific,
  early and unmistakable; the test is an office biopsy taking minutes and costing
  very little; and **Black women in the United States are diagnosed later and have
  roughly double the mortality.** Aggressive histology explains part of it and
  delayed evaluation of bleeding explains part of it. **Because the test is so
  cheap and so quick, almost nothing else can account for the delay** — which
  makes this the cleanest case the register will produce, and auditing
  time-from-bleeding-to-biopsy by group is entirely feasible.
- **#138 (stopping is progress) — NINTH DE-ADOPTION.** Sentinel lymph node
  biopsy replaced full pelvic lymphadenectomy and removed a large amount of
  permanent lymphoedema; **POLE-mutated tumours are now being given no adjuvant
  treatment at all** because their outcomes are excellent regardless. Nine of the
  register's fourteen cancer records have improved substantially by subtraction.
- **#130 (an intervention's harm lands in a different entity) — and here the
  entity is held.** Tamoxifen, given for breast cancer, causes endometrial
  cancer. `breast-cancer` is a record in this register. **One row's treatment is
  another row's cause**, and three records now show the pattern in three
  directions — gastric's antibiotics feeding AMR, pancreatic's Whipple causing
  diabetes, and this.
- **#125 (a residual bucket permits every rating anyway) — ONE LEVEL DOWN, INSIDE
  A PROGNOSTIC CLASSIFIER.** The 2013 molecular classification has four groups
  and the largest is **"no specific molecular profile"** — defined by not being
  the other three, containing more patients than any real group, and used to
  guide adjuvant therapy. A leftover inside the instrument.
- **#114 (the precursor has nowhere to live) — and this one is reversible with a
  tablet.** Atypical endometrial hyperplasia progresses to carcinoma and
  **regresses on progestins**, which is precursor treatment by hormone rather
  than by excision. Colorectal's polyp is cut out; cervical's CIN is excised;
  this one is talked out of it.
- **#87 (the intervention is non-specific) — and here it runs in the register's
  favour, uncounted.** **Combined oral contraceptives roughly halve endometrial
  cancer risk**, with protection persisting decades after stopping, and hundreds
  of millions of women have taken them for contraception. An enormous cancer
  prevention delivered as a side effect of a completely different intervention,
  chargeable to nobody — the same shape as HPV vaccination preventing five
  cancers while being costed against one.
- **The counterexample to every silent cancer in the corpus.** Ovarian cancer is
  centimetres away, presents late and is lethal; endometrial cancer bleeds,
  presents at stage I and is mostly cured. **Same pelvis, same access to care,
  same surgeons** — and the entire difference in outcome is whether the disease
  tells you it is there. Ovarian cancer is absent from this register and belongs
  beside this record for exactly that reason.

---

**Strengthened by `renal-cell-carcinoma`, not new:**

- **#127 (the disease and its host organ fail together) — and here THE CURE
  CAUSES THE COMORBIDITY.** Radical nephrectomy roughly halves nephron mass in a
  patient who frequently has hypertension and diabetes already, and the reduction
  in filtration is permanent. **Chronic kidney disease is a queued record**, it is
  a risk factor for this cancer through acquired cystic disease, and it is a
  consequence of the cure. Upstream and downstream of the same record, and
  unrecordable in both directions.
- **#87 (the intervention is non-specific) — SIXTH TOBACCO RECORD, and now three
  queued entities upstream.** Smoking, obesity, hypertension and chronic kidney
  disease are the risk factors; the last three are all queued records. Nine gaps
  point at #87 and this one adds that **the causes are increasingly other rows in
  the same table.**
- **#122 (`access` records whether you reached care, not the right care) — and
  the difference is which operation.** Partial nephrectomy preserves kidney
  function, is technically harder, and its adoption varies substantially between
  centres for reasons about surgical capability rather than about patients. The
  patient reached surgery. **Which one they got depended on who was holding the
  instrument.**
- **#135 (mechanism rates the disease, not the treatment) — the positive
  control, one record later.** Bladder cancer has an established disease
  mechanism and a therapy nobody understands. **RCC has both halves**: *VHL* loss
  stabilises HIF-2α, which drives VEGF, which is why anti-angiogenic therapy —
  disappointing nearly everywhere else — worked here, and why belzutifan exists.
  **A hereditary syndrome gave the gene, the gene gave the pathway, the pathway
  gave a drug for people who never had the syndrome.** Two adjacent records
  showing what the missing field would distinguish.
- **And two absences worth recording rather than eliding.** *No cytotoxic
  chemotherapy works in RCC*, the reason is unknown, and it is why the field went
  to immunotherapy and anti-angiogenics in the first place — **an accident of
  failure that turned out well.** And *metastatic RCC occasionally regresses
  spontaneously*: rare, repeatedly documented, unexplained, and the original
  reason anybody tried immunotherapy here.

---

**Strengthened by `bladder-cancer`, not new:**

- **`manufacturing` — FIFTH USE IN SIXTY-TWO RECORDS, AND EVERY ONE IS THE SAME
  SHAPE.** Snakebite antivenom, benzathine penicillin, pandemic influenza
  vaccine, smallpox vaccine, and now BCG. **All old, all cheap, all biologically
  produced, all essential, and all in chronic short supply.** BCG is the sharpest:
  a live bacterium that must be grown rather than synthesised, with the oncology
  market at times down to essentially one producer, and urologists splitting
  doses for years. **The consequence is measurable in bladders** — patients who
  would have kept theirs have them removed because the drug was rationed. Five
  instances is no longer a coincidence and the blocker kind deserves the same
  cross-record treatment Engpass gave `donation-dependency`.
- **#55 / the relations gap — AND HERE ONE PRODUCT IS TWO RECORDS.** BCG is the
  bladder cancer therapy *and* the tuberculosis vaccine. **A single supply
  failure degrades a cancer treatment and an infant immunisation
  simultaneously**, and `tuberculosis` is a held record. Meanwhile *Schistosoma
  haematobium* causes squamous bladder cancer and `schistosomiasis` is also held,
  with Egypt's shifting histology as the evidence that controlling one changed
  the other. **Two held records touch this one, in opposite directions —
  supply and causation — and neither link exists.**
- **#87 (the intervention is non-specific) — fifth record in the tobacco family**,
  after ischaemic heart disease, stroke, COPD and lung cancer. Smoking accounts
  for roughly half of bladder cancer. Nine gaps now point at #87.
- **And a prevention that worked without any medicine.** Aromatic amines in the
  dye and rubber industries were described as a cause in 1895, regulated over the
  following century, and incidence in those workers fell as a direct consequence.
  **Industrial regulation prevented a cancer**, with no drug, no screen and no
  clinician — which is #129's undeliberate prevention with the deliberation put
  back in, and the register has no more room for one than the other.
- **#26 (toll reduction moves no axis) — fourth record.** BCG's principal effect
  is that patients keep their bladders: capability barely moved, and the fraction
  needing cystectomy collapsed. That is `toll.incidence`, and `moved` records a
  change on an axis rather than in one of its components. Breast, prostate,
  gastric and now bladder cancer have all hit the same wall.
- **The burden is the surveillance, not the illness.** Three quarters of bladder
  cancer never invades muscle, most of those patients never die of it, and most
  of them are never free of it either — **a cystoscopy every few months for
  years, in a population with a median age in the seventies.** It is the most
  expensive cancer per patient to manage over a lifetime and `ongoing: high` is
  one word for all of it.

---

**Strengthened by `thyroid-cancer`, not new:**

- **#112 (a window not always worth catching) — FIVE ANSWERS NOW, AND THIS IS THE
  ZERO.** South Korea offered thyroid ultrasound from 1999; incidence rose
  roughly **fifteen-fold** by 2011 and became the country's most common cancer;
  **mortality did not move at all**; physicians publicly called for it to stop in
  2014 and incidence fell. Prostate cancer screening is a bad trade — real
  mortality benefit, majority harmed. **This is a pure loss, measured at national
  scale, with a reversal to confirm it.** No other record in this register
  contains an experiment like that.
- **And the record has NO `window` block for a new reason.** Childhood ALL and
  non-Hodgkin lymphoma have none because the disease is disseminated from the
  start. **Thyroid cancer has none because catching it earlier does not help** —
  Japanese active-surveillance cohorts show most low-risk papillary
  microcarcinoma does not grow, and patients who eventually operate do no worse
  for having waited.
- **#91 (position, not trajectory) — SECOND RECORD WHERE IT MAKES A FLAG MISS ITS
  OWN CASE.** `overtreatment_risk` requires `prognostic: none` and **does not
  fire on the most overtreated cancer in the world**, because size, extension,
  nodal status and TERT-plus-BRAF do stratify. Prostate cancer produced the same
  miss for the same reason. **A flag that misses both of its canonical cases is
  measuring something other than what it is named after.**
- **#125 (a bucket permits every rating anyway) — and here the bucket is not
  flagged.** `residual: false`, correctly by the schema's definition, and the
  record still contains **the most overdiagnosed cancer in the world and one of
  the most lethal** in the same row. Anaplastic carcinoma has a median survival
  around half a year and supplies a large share of the deaths from two percent of
  the diagnoses. `strata` carries it and `efficacy: 0.95` does not.
- **#105 (`toll` needs a scope) — and the second prophylactic organ removal in
  three records.** Germline **RET** carriers are offered thyroidectomy in
  childhood, exactly as *CDH1* carriers are offered gastrectomy. A certain,
  permanent intervention in a well child to prevent a probable cancer, and
  `toll` means what the cure costs.
- **The `moved` block cannot see the largest event in the disease's history.**
  The fifteen-fold Korean incidence rise and its reversal moved **no axis** — not
  capability, not efficacy, not access, not toll severity. What changed was how
  many people were called patients, and the register has no field that counts
  that.
- **A blocker that is something being done rather than something missing.**
  Thyroid ultrasound screening of asymptomatic people is recommended against by
  essentially every body that has examined it, and it continues — as a paid
  add-on, opportunistically, and because a nodule found must be explained.
  **De-implementation has no advocate**: there is no constituency for a test not
  done, and every individual step is defensible. The register's blocker
  vocabulary assumes obstacles are absences, and gastric cancer's *rationally
  declined screening* was the first hint of the same shape.

---

**Strengthened by `pancreatic-cancer`, not new:**

- **#98 (benefit is only course alteration) — AND HERE PALLIATION IS THE MAIN
  INTERVENTION, NOT THE FALLBACK.** For the forty-five percent of patients with
  unselected metastatic disease, what medicine actually provides is biliary
  stenting, coeliac plexus neurolysis for the back pain that is this cancer's
  signature, pancreatic enzymes so food can be absorbed, nutritional support
  against cachexia, and early hospice referral. **None of it alters the course
  and all of it is the treatment.** Marburg made this point with survival and
  COPD with breathlessness; this record makes it with the largest stratum of a
  half-million-death disease.
- **#122 (`access` records whether you reached care, not the right care) — and
  the volume-outcome gradient here is among the steepest in medicine.** Operative
  mortality after pancreaticoduodenectomy differs several-fold between
  high-volume and low-volume centres after case-mix adjustment. **A patient in
  the only stratum where cure is possible has their chance substantially
  determined by which hospital operates**, and `access: 0.30` records that they
  reached surgery.
- **#130 (an intervention's harm lands in another entity) — and here it lands in
  the same patient.** The Whipple procedure that cures this cancer produces
  **exocrine insufficiency requiring enzymes with every meal for life, and
  diabetes in a large share of survivors.** Type 1 and type 2 diabetes are both
  queued records. The cure for one entity manufactures another, in one person,
  and `toll` records it as prose.
- **#114 (the precursor has nowhere to live) — RUNNING BACKWARDS.** Colorectal's
  adenoma and cervical's CIN are precursors worth removing. Pancreatic
  intraductal papillary mucinous neoplasms are **found incidentally on scans done
  for other reasons, in large numbers, and mostly never progress** — so the same
  field would here describe an *overdiagnosed precursor of an underdiagnosed
  cancer*, and the two halves of the record pull in opposite directions.
- **#91 (position, not trajectory) — and rank is relative.** Pancreatic cancer is
  projected to become the second leading cause of cancer death in several
  high-income countries. **Not because it is getting worse — because lung,
  colorectal, breast and prostate cancer are getting better around it.** The
  register records absolutes, *what should we work on next* answered by burden
  rank will increasingly point here, and that is correct for a reason the
  register cannot state.
- **#110 (the patient is blamed) — inverted into an absence of advocates.**
  Pancreatic cancer research funding has been low relative to its share of deaths
  for years, and one documented reason is structural rather than attitudinal:
  **almost nobody survives to campaign.** The survivor constituencies that drove
  breast and prostate cancer funding barely exist here because patients are dead
  within a year. It is the first record where the funding gap is explained by the
  mortality rather than by a judgement about the patient.
- **`predictive: partial` reaching one patient in twelve.** BRCA1, BRCA2 and
  PALB2 predict platinum sensitivity and PARP benefit in perhaps five to seven
  percent; mismatch-repair deficiency about one percent; KRAS G12C one to two.
  Liver cancer earned `none` for having nothing at all. **The distance between
  `none` and `partial` here is five percent of a record**, which is a lot of
  meaning for one enum step to carry.

---

**Strengthened by `gastric-cancer`, not new:**

- **THREE CONSECUTIVE CANCERS WHOSE CAUSE IS ANOTHER RECORD.** Non-Hodgkin
  lymphoma's gastric MALT is *H. pylori*. Liver cancer is hepatitis B and C.
  Gastric cancer is *H. pylori* again. **`h-pylori-ulcer` is a held record whose
  treatment — two weeks of triple therapy — is the prevention for two of the
  cancers in this register**, and hepatitis C's cure is the prevention for a
  third. Roughly an eighth of cancer worldwide is infection-attributable and the
  register has now hit it four times in nine cancer records. #55's relations are
  no longer a nice-to-have.
- **#105 (`toll` is scoped to treatment) — SHARPEST INSTANCE IN THE CORPUS.**
  Carriers of a pathogenic *CDH1* variant face a lifetime gastric cancer risk
  around seventy percent in a mucosa endoscopy cannot survey, and the standard
  recommendation is **prophylactic total gastrectomy in a person's twenties or
  thirties.** A certain, permanent, life-altering harm — B12 injections for life,
  six meals a day, dumping syndrome — inflicted on somebody who is well, to
  prevent a probable cancer. The most damaging procedure in the record is given
  to people who do not have the disease.
- **#52 (solved here, not there) — and none of it is biology.** Five-year
  survival runs around a third in most of the world and **around seventy percent
  in Japan and Korea**, which screen. Same disease, same operations, same drugs.
  Visceral leishmaniasis' regional divergence involved genuinely different
  biology; cervical cancer's involved none; this involves none either and the gap
  is bigger.
- **#112 (a window not always worth catching) — and here it is worth catching
  twice over.** `window_toll_link` fires and reports that *the toll is the price
  of missing it and diagnosis is the cheap lever*. For prostate cancer that was
  exactly backwards. **Here the window buys the patient their life and their
  stomach**: mucosal disease is cured endoscopically with the organ intact, and
  the next stratum down loses it. `toll: minor` against `toll: major` on adjacent
  rows is the largest within-record toll gap in the corpus.
- **#26 (toll reduction moves no axis) — third time, same shape.** Endoscopic
  submucosal dissection made mucosal gastric cancer curable without an operation.
  Capability unchanged — those patients were curable by gastrectomy before — and
  the price collapsed. The `moved` entry records `toll` incidence rather than
  severity, which the field cannot distinguish, exactly as prostate cancer's 2012
  entry could not.
- **#127 (the field is still there) — second consecutive record.** A patient
  cured endoscopically of early gastric cancer **still has the atrophic,
  metaplastic stomach the cancer grew in** and remains at risk of a second
  primary. Liver cancer said the same about the cirrhotic liver. Neither
  `residue` nor `toll` nor `ongoing` can hold *the diseased organ that was there
  first and still is*.
- **A blocker that is correct, demonstrated, and rationally declined.** Japan and
  Korea screen at national scale and double everybody else's survival. At low
  incidence the same programme costs more per cancer found than any payer will
  meet, and the endoscopy carries its own small risk. **The strategy is right and
  most of the world is right to refuse it** — a shape the register's blocker
  vocabulary, which assumes obstacles are failures, has no word for.

---

**Strengthened by `liver-cancer`, not new:**

- **#110 (the register cannot record that the patient is blamed) — and here the
  consequence is whether they are offered the only curative treatment.** That gap
  described blame affecting research funding and screening uptake. **Transplant
  allocation for alcohol-related liver disease has historically turned on
  abstinence periods** — a rule about how the patient came to need the organ,
  applied to a zero-sum resource, deciding who lives. It is the sharpest instance
  the corpus will produce and it arrived four records after the gap was named.
- **#87 (the intervention is non-specific) — five programmes, five ministries,
  one cancer.** Hepatitis B birth-dose vaccination, hepatitis C diagnosis and
  cure, alcohol policy, obesity policy, and **grain drying and storage** to
  control aflatoxin. **Not one item on that list belongs to oncology**, and two
  of them are separate records in this register. Eight gaps now point here.
- **The second vaccine-preventable cancer, and it was the first.** Taiwan's
  universal infant hepatitis B programme from 1984 is the earliest demonstration
  anywhere that a vaccine prevents a human cancer — **two decades before HPV** —
  and the vaccine is against a disease that is a separate, queued record. The
  prevention of this cancer belongs entirely to another entity.
- **#114 (the precursor has nowhere to live) — and here the precursor is a
  DISEASE WITH ITS OWN RECORD.** Colorectal's adenoma and cervical's CIN are
  lesions nobody tracks as entities. **Cirrhosis is queued as a record in this
  register**, is diagnosed, is under clinical care, and is the surveillance
  population for this cancer. The precursor problem and the relations problem are
  the same problem here.
- **#122 (`access` records whether you reached care, not the right care) — and
  the population is a list of names.** Surveillance uptake among eligible
  cirrhotics runs between a fifth and two fifths in well-resourced systems. Lung
  cancer's eligible population must be reconstructed from smoking histories
  nobody wrote down; **here the health system already knows exactly who to call
  and does not.** No organised recall, cirrhosis managed across several
  specialties with nobody owning the surveillance.
- **`predictive: none` — the first cancer in the register to earn it, and
  `futile_treatment_risk` fires correctly.** No validated biomarker selects any
  systemic therapy in HCC. Patients in the largest stratum receive expensive
  drugs with real toxicity, **in a body with very little reserve**, and find out
  by waiting.
- **The incidence-to-mortality ratio is the register's extreme.** Prostate cancer
  runs 1.5 million diagnoses against 400,000 deaths; liver cancer runs 870,000
  against 760,000. Those two records bound this corpus, and everything about them
  — window, toll, overdiagnosis, `caught_in_time` — differs accordingly.

---

**Strengthened by `non-hodgkin-lymphoma`, not new:**

- **#123 (the ladder is ordered by finality, not by value) — and here the
  ordering is not merely unhelpful, it is BACKWARDS.** Diffuse large B-cell
  lymphoma kills within months untreated and is **cured** in two thirds.
  Follicular lymphoma is compatible with twenty years and is **not curable at
  all** — asymptomatic disease is watched, because trials found no survival
  benefit to treating early. A patient told they have the slow-growing lymphoma
  has been given worse news in one specific sense, and `capability` read alone
  reverses it. **Every intuition the word "cancer" carries runs the wrong way in
  this record.**
- **#100 / the relations gap — ONE RECORD'S TREATMENT IS ANOTHER RECORD'S CURE.**
  Gastric MALT lymphoma is driven by *Helicobacter pylori* and regresses in most
  patients when the bacterium is eradicated. **The register already holds
  `h-pylori-ulcer`, with the same two weeks of triple therapy as its treatment.**
  Add HIV suppression preventing AIDS-associated lymphoma, and hepatitis C cure
  causing regression of some marginal zone disease, and **three held records are
  upstream of this one** with no way to say so. The prevention of this cancer is
  largely the treatment of other entities.
- **#111 (the disease evolves under treatment) — and here it evolves WITHOUT
  treatment.** About a quarter of follicular lymphomas transform into aggressive
  disease on their own, moving the patient from the `suppressive` row to the
  `curative` one. And gastric MALT carrying t(11;18) has become
  antigen-independent — **the tumour graduating from needing the infection that
  caused it**, which is clonal evolution without a drug applying the pressure.
- **#61 (one record, several populations) — and the CAR-T `moved` entry moves the
  record five points.** Roughly forty percent durable remission in patients who
  had exhausted chemotherapy and transplant, in a minority of a minority. Both
  sentences are true and the register reports only the small one.
- **A stratum the antibody era passed over, for a reason.** T-cell lymphomas have
  no CD20, so rituximab — the drug that transformed B-cell lymphoma and founded
  antibody therapy in oncology — does nothing for them, and thirty years of
  derivative advances went with it. Third instance of the shape, after small cell
  lung cancer and infant ALL, and **the first where the reason the era missed is
  a single surface molecule.**
- **No `window`, and for a reason that inverts the corpus.** Aggressive lymphoma
  is usually disseminated at diagnosis and **is cured anyway** — stage matters
  far less than in any solid tumour. And for indolent lymphoma **treating earlier
  is actively pointless**: trials of immediate versus deferred therapy found no
  survival benefit, so watching is standard. This is the only record in the
  register where the correct response to finding the disease sooner is to do
  nothing about it for longer.
- **A cure that leaves you permanently dependent on a blood product.** CD19 CAR-T
  destroys the lineage its target belongs to, and prolonged B-cell aplasia leaves
  some patients on immunoglobulin replacement indefinitely. `toll` records it as
  permanent harm, correctly, and there is no shape in this register quite like
  *cured, and now requiring an infusion forever*.

---

**Strengthened by `cml`, not new:**

- **#118 (ratings that need a future) — and here the experiment is DELIBERATE.**
  Melanoma's plateau might be cure and nobody is testing it on purpose. **CML's
  field systematically stops effective therapy to find out**: patients with
  sustained deep molecular response attempt treatment-free remission, roughly
  half hold it, and those who relapse almost always respond again on restarting.
  So roughly half of the largest stratum in this record may belong on a different
  rung, the question is being actively resolved, and the register must pick one
  today.
- **#111 (the disease evolves under treatment) — the founding case.** Kinase
  domain mutations under TKI pressure, T315I above all, then compound mutations
  after sequential therapy, then blast crisis. Lung cancer's EGFR-to-small-cell
  transformation and prostate's castration resistance are the same shape; CML is
  where it was first characterised and where the counter-move — asciminib binding
  a different pocket entirely — was first designed.
- **`toll: minor` and `restored: restored` on a disease nobody is cured of.**
  Both derivations are correct and the record is not, quite. CML takes almost
  nothing permanent and **never lets you stop** — a daily tablet, a molecular
  test every three months, and a pregnancy that has to be planned around a
  teratogen. That is `ongoing` doing work `toll` cannot, and it is the clearest
  statement in the corpus that the two fields divide the space wrongly.
- **A generic drug and a monitoring test that is not.** CML is managed by
  watching a number — *BCR-ABL1* on the International Scale, quarterly — which
  decides when to switch drug, which mutation to look for and who may attempt to
  stop. **The tablet costs a few dollars and the laboratory does not**, which is
  the inverse of every other cost blocker here and which `access` records as one
  fraction.
- **#66's `prevention: none` — third record, and they share a shape.** Prostate
  cancer, childhood ALL and CML all have `prevention: none` and all have
  `mechanism: established`. **A complete chain from cause to phenotype, and no
  known cause.** The mechanism axis rates how the cause produces the disease and
  says nothing about whether the cause is known, and for these three that is the
  most important missing fact.
- **The window closes because the treatment works.** Progression to blast crisis
  was CML's ending and is now uncommon in treated patients, so the accelerated
  and blast strata have shrunk since 2001. **A stratum that shrank because
  therapy improved** is a form of progress the register records nowhere — the
  fractions are a moving target and the record says so.

### And a bug in Engpass, found by this record

CML's knowledge blocker cites `pathogen-persistence` and its logistics blocker
cites `donation-dependency`, which pushed prostate cancer into a row where it
appeared **twice**. A record with two blockers citing the same obstacle was
counted once per blocker rather than once per record, inflating the headline
`records` column — `who-progresses` read 21 and should have read 20.

Fixed: **one record, one vote.** The question a Engpass row answers is *which
diseases does this block*, not *how many times was it mentioned*. Worth logging
because it is the second defect found by adding a record rather than by looking
for defects, and the first in the second register.

---

**Strengthened by `childhood-all`, not new:**

- **#115 (the intervention is refused) — a SIXTH reason, and it is duration.**
  **Treatment abandonment** is the specific, documented way this cure fails in
  poor countries: families stop coming. Not refusal, not non-adherence — the
  protocol runs two and a half years, the hospital is far away, the parent cannot
  keep working, and there are other children at home. **The length of the
  treatment is itself the barrier**, and programmes providing accommodation,
  transport and income support reduce abandonment substantially, which is the
  clearest evidence of what is actually blocking the cure.
- **#52 (solved here, not there) — and the drugs are already generic.** Roughly
  nine in ten cured in high-income countries; reported figures from a fifth to a
  half elsewhere. **What is missing is not a molecule.** It is a blood bank that
  can supply platelets for two years, antibiotics for neutropenic sepsis,
  intensive care during induction, and a family that can stay. Most induction
  deaths in low-income settings are from infection, not leukaemia.
- **#26 (toll reduction moves no axis) — and here a generation carries the old
  toll.** Cranial irradiation was given to nearly every child from the 1970s and
  has largely been replaced by intrathecal chemotherapy, removing cognitive
  impairment, growth failure and second brain tumours from every child treated
  since. Capability unchanged, register records nothing — **and the survivors who
  received it are now in middle age, so the toll applies to a cohort rather than
  to a disease**, which is a distinction the schema has no way to make.
- **The register's measurement thesis, demonstrated twice in one record.** MRD
  quantification after induction took survival from roughly 70% to roughly 90%
  **with no change to the drug backbone**, by sorting children on how their
  disease was actually responding. It is the same move prostate cancer's active
  surveillance made a decade later in a different organ, and it is `prognostic:
  good` and `predictive: good` — one of only four records in the corpus with
  both.
- **#66's other half — `prevention: none`, and here it is the loudest sentence in
  the file.** A disease of two- to five-year-olds that cannot be prevented,
  cannot be screened for, and has no window. Nothing reliably causes it: a
  prenatal initiating lesion plus a delayed immune challenge is the best
  available account and it is not established. **Everything this record achieves,
  it achieves after the child is already ill.**
- **Two structural absences worth stating rather than leaving empty.** No
  `window` — the first cancer in the register without one, because leukaemia is
  disseminated the moment it exists, and **time from symptom to diagnosis does
  not reliably predict outcome**, with some series finding it runs the wrong way
  because the most aggressive disease declares itself fastest. And no ⧉ — the
  first record with `strata` where *is it solved* is **not** malformed, because
  every stratum is curable and they differ in probability rather than in kind.

---

**Strengthened by `melanoma`, not new:**

- **#61 (one record, several populations) — AT ITS WIDEST, AND IT NEARLY HIDES
  THE LARGEST ADVANCE IN ONCOLOGY.** Metastatic melanoma went from under a tenth
  five-year survival to roughly half. The record-level `moved` entry moves
  `efficacy` from about 0.65 to about 0.80 — because most melanoma was already
  cured by cutting it out, and the transformation reached a tenth of diagnoses.
  **A fifteen-point move in a scalar is what the register has to say about it.**
- **#92 (the detectable feature is not the causal one) — a FOURTH case, and a
  new mechanism.** Lung: overdiagnosis real, net benefit clear. Prostate:
  overdiagnosis dominant. Colorectal: no overdiagnosis, because the target is a
  precursor. **Melanoma: overdiagnosis substantially manufactured by
  reclassification** rather than by detection. Four cancers, four different
  answers to the same question, and `has_window: true` for all of them.
- **#26 (toll reduction moves no axis) — and here the reduction was to stop doing
  something.** Completion lymphadenectomy was largely abandoned after trials
  showed it did not improve survival, removing substantial lymphoedema from a
  large number of patients. Capability unchanged, toll materially lower, register
  records nothing — the same shape as sentinel node biopsy replacing axillary
  clearance in breast cancer, which forced #26 in the first place.
- **#100 (patient-scoped) — and here the register's own pattern breaks
  usefully.** Melanoma is the **first cancer in the corpus to derive
  `restored`** — nothing permanent from either side. Lung, prostate, colorectal,
  cervical and breast all derived `cure-costs`. That pattern was never about
  cancer; **it was about surgery**, and melanoma is the case that shows it: where
  the tumour comes out with a scalpel and a margin, the patient genuinely returns
  to baseline.
- **#113 (`efficacy` is measured in one population and applied to another) —
  and here it has a biological edge.** Acral and mucosal melanoma are not
  UV-driven, carry a far lower mutational burden, and respond much less to the
  therapies that transformed cutaneous disease. They are a much larger *share* of
  melanoma in people with darker skin, are diagnosed later because nobody
  examines a sole, and the trials that produced every number in this record were
  overwhelmingly in light-skinned cutaneous disease.
- **The cause is the reason it is treatable, and nothing else in the register has
  that shape.** Ultraviolet light mutates DNA; melanoma carries one of the
  highest mutational burdens of any cancer; those mutations make neoantigens;
  neoantigens are what checkpoint blockade unleashes the immune system against.
  It also explains the failure: acral and mucosal melanoma have few mutations,
  so few neoantigens, so little response. **One mechanism accounts for both the
  triumph and the exception**, and the schema records them as two strata.

---

**Strengthened by `cervical-cancer`, not new:**

- **#52 (solved here, not there) — and this is a purer case than the one that
  forced it.** Visceral leishmaniasis' regional divergence involves real biology:
  different first-line drugs, different efficacy, different diagnostic
  performance, different residue. **Cervical cancer's involves none.** Same
  virus, same vaccine, same test, same excision — and roughly nine in ten deaths
  occur in low- and middle-income countries, with a tenfold difference in
  age-standardised mortality between the highest- and lowest-burden countries.
  `access: 0.30` is a single scalar describing a bimodal world.
- **#114 (the precursor has nowhere to live) — second record running, and here
  there are THREE interventions on one causal chain.** Vaccinate before
  infection; excise the precursor after infection and before cancer; treat the
  cancer. The schema has two slots — `prevention` and `intervention` — and the
  middle one is the most effective of the three.
- **#66's open half (prevention is one word doing five jobs) — and cervical
  cancer needs two of them at once.** `prophylaxis` here covers *a vaccine given
  twice at age twelve, through schools* and *HPV testing every five to ten years
  from thirty, followed by an excisional procedure*. Different deliverer,
  different cost, different cadence, different toll, different target
  population, one word.
- **#115 (the intervention is refused) — a FIFTH reason, and it is not about the
  vaccine at all.** Objection to vaccinating a twelve-year-old girl against a
  sexually transmitted infection is substantially about what that is taken to
  imply or license. **A values objection does not yield to safety data, because
  safety data is not what is in dispute.** And separately, Japan's programme
  collapsed on a safety scare and took most of a decade to recover — which is
  measles' refuted-claim category, in the same record. One entity needing two of
  the five.
- **#105 (`toll` needs a scope) — third consecutive record.** Colonoscopy
  perforates. Low-dose CT biopsies false positives. Cervical excision damages a
  future pregnancy. **All three are harms inflicted by looking, on people who do
  not have the disease**, and `toll` means what the cure costs.
- **#100 (patient-scoped) — two entities in this register compound and neither
  can say so.** HIV co-infection multiplies cervical cancer risk several-fold and
  accelerates progression, which is why the burden concentrates further in
  southern and eastern Africa. Both records are held; the relationship is
  unrecordable.
- **#87 (the intervention is non-specific) — in miniature, and it understates
  rather than overstates.** HPV vaccination also prevents anal, oropharyngeal,
  vulvar, vaginal and penile cancers, none of which is in this register. **Every
  cost-effectiveness figure charged to cervical cancer therefore understates what
  the intervention buys** — the first instance in the corpus where the
  non-specificity works in the intervention's favour and is still invisible.

---

**Strengthened by `colorectal-cancer`, not new:**

- **#112 (a window not always worth catching) — THE POSITIVE CONTROL ARRIVES ONE
  RECORD LATER.** Prostate's window is good for a minority and harmful for the
  majority. Lung's is good on net with a real overdiagnosis tax. **Colorectal's
  is good, full stop** — because it acts on a precursor rather than on an
  indolent cancer, so there is no overdiagnosis to trade against. Three cancers,
  three answers to the same question, and the schema records the same
  `has_window: true` for all of them.
- **#66's open half (prevention is one word doing five jobs) — the fifth job.**
  `prophylaxis` now covers a vaccine given twice in childhood, a monthly
  injection for years, post-exposure prophylaxis inside 72 hours, a bed net, and
  **a colonoscopic polypectomy repeated every few years for decades by a trained
  endoscopist, which perforates the bowel about once in a thousand procedures.**
  These differ in cost, toll, deliverer and cadence, and the enum says one word.
- **#109 (prevention has no efficacy and no access) — and here it swallows the
  record's main `moved` entry.** Colorectal's 2000 entry records organised
  screening lowering both incidence and mortality, and it is filed under `access`
  because there is nowhere else. **What actually rose was screening
  participation, which is prevention coverage.** Same hole that has nowhere to
  put measles' 83%-against-95%.
- **#105 (`toll` needs a scope) — second consecutive record needing the
  diagnostic one.** Colonoscopy perforates the bowel roughly once in a thousand
  procedures, in people who are well. Lung cancer's low-dose CT causes
  pneumothorax through biopsy of false positives. **Harm inflicted by the process
  of looking, on people who do not have the disease**, and `toll` means what the
  cure costs.
- **#91 (position, not trajectory) — and here the trajectory is the record.**
  Colorectal cancer incidence *and* mortality have fallen in screened age groups
  and are **rising in adults under fifty**, for reasons nobody knows. Two
  opposite trends inside one entity, and the register reports one number for
  each field.
- **A diagnosis in one patient producing prevention in another.** Universal
  tumour testing identifies Lynch syndrome in roughly one in thirty colorectal
  cancers; cascade testing then finds relatives who do not have cancer and
  prevents theirs. It is a real and cheap mechanism, it belongs to neither
  `measurement` nor `prevention` as scoped, and it is #100's patient-scoping
  problem in a new place.

---

**Strengthened by `prostate-cancer`, not new:**

- **#92 (the detectable feature is not the causal one) — THE TRIAD IS NOW
  COMPLETE, and this is its centre.** Prostate cancer is where the detectable
  feature and the lethal feature diverge most sharply: autopsy series find the
  disease in a large fraction of men who died of other causes, so it is close to
  a normal feature of ageing that occasionally kills. Lung cancer is the case
  where screening works despite overdiagnosis; prostate is the contested middle;
  thyroid, queued, is the case where screening found a great deal and changed no
  mortality. #92 named prostate as missing from the corpus. It is now here.
- **#91 (the register records a position, not a trajectory) — and here it makes a
  flag miss its own definitive case.** `overtreatment_risk` requires
  `prognostic: none` and **does not fire on prostate cancer**, the canonical
  overtreatment disease — because prostate's prognostic measurement *improved out
  of that band*, which is exactly why the overtreatment fell. **The flag is right
  today and would have fired in 1995.** A register that cannot see that is
  describing the wrong thing.
- **#26 (toll reduction moves no axis) — and it needs to go one level finer.**
  The record carries a `moved` entry dated 2012 for active surveillance, and it
  is the register's best evidence for its own central claim: grade grouping, MRI
  and genomic classifiers made low-risk disease safe to watch, the share of men
  receiving immediate radical treatment collapsed, and mortality did not rise.
  **Same benefit, far less harm, by measuring better rather than treating
  better.** But the toll's *severity* did not change — prostatectomy is exactly
  as damaging as it was — what fell is `toll.incidence`, and `moved` records a
  change on an axis rather than in one of its components. #26 asked for
  `axis: toll`; this asks for `axis: toll.incidence`.
- **#111 (the disease evolves under treatment) — second record, and the selection
  pressure is eighty years old.** Castration has worked since 1941 and has always
  eventually stopped working, through receptor amplification, splice variants,
  intratumoural androgen synthesis, and lineage plasticity into neuroendocrine
  disease that no longer needs the receptor at all. Same shape as lung cancer's
  EGFR-to-small-cell transformation, with a much longer history.
- **#104 (what a disease appears to do depends on how hard you looked) — and here
  it corrupts the headline statistic.** Recorded prostate cancer incidence
  roughly doubled within a few years of PSA testing becoming widespread, and
  mortality did not move in step. Five-year survival is very high and screening
  raises it further — partly by curing people and partly by **adding to the
  denominator cancers that were never going to kill anyone.** A rising survival
  rate here is not straightforwardly good news, and no field in the register can
  say so.
- **#87 (the intervention is non-specific) — the contrast case, and it is
  useful.** The four records before this one share a preventable exposure worth
  more than all their therapies combined. **Prostate cancer has nothing to
  prevent** — `prevention: none`, honestly rather than for want of looking — so
  every unit of its capability is downstream, and its only lever on mortality is
  deciding better who needs treating. It is the cleanest demonstration in the
  corpus that measurement and prevention are substitutes for each other at the
  level of a whole record.

---

**Strengthened by `lung-cancer`, not new:**

- **#87 (the intervention is non-specific) — LARGEST INSTANCE, AND THE QUARTET IS
  NOW COMPLETE.** Ischaemic heart disease, stroke, COPD and lung cancer:
  **roughly 20.9 million deaths a year across four records, driven substantially
  by one exposure**, and the intervention against it — taxation, advertising
  bans, smoke-free legislation — is chargeable to none of them. Seven gaps now
  point here. It should stop being a gap and become a field.
- **#92 (the detectable feature is not the causal one) — and lung cancer is the
  POSITIVE control.** #92 named prostate and thyroid as the canonical
  overdiagnosis cases and noted both were missing from the corpus. Lung cancer is
  the third and the most instructive: **overdiagnosis is real — perhaps a tenth
  to a fifth of screen-detected cancers — and the net mortality effect is still
  a clear reduction.** So the triad is: lung (screening works despite
  overdiagnosis), prostate (contested), thyroid (screening found a great deal and
  changed no mortality). Any account of screening needs all three.
- **#27 (stratification is not one-dimensional) — three axes, not two.** Breast
  cancer forced this with stage × subtype. Lung cancer has **stage × histology ×
  driver mutation**, and they cut across each other completely. The record
  collapses them into four hand-built rows and says so.
- **#95 (`efficacy` assumes agreement about what "works" means) — worst instance
  in the register.** Oncology has no agreed numerator: response rate,
  progression-free survival, five-year survival and overall survival give
  materially different answers about the same drugs, and which one a trial
  reports is itself contested. Eleven more cancer records are queued and every
  one of them will carry this.
- **#105 (`toll` is scoped to treatment) — and now there are THREE scopes.**
  Smallpox needed a *prevention* toll, because the vaccine's harm ended the
  programme. Lung cancer needs a **diagnostic** one: low-dose CT produces mostly
  false positives, the workup includes biopsies that cause pneumothorax, and
  occasionally a lobe is removed for benign disease. **That harm is inflicted on
  people who do not have the disease**, by the process of looking for it.
- **#98 (benefit is only course alteration) — inverted here, and it still bites.**
  The driver-positive stratum is `suppressive` and its toll is `minor`: a rash
  and diarrhoea in exchange for years of control over a metastatic cancer. The
  register can say that. What it cannot say is that the *same* record's largest
  stratum buys a few months at the price of permanent neuropathy and permanent
  endocrine failure — because record-level `toll` and record-level `efficacy` are
  single values and the strata carry only `efficacy` and a toll *severity*.
- **#90 (the denominator is a threshold somebody chose) — screening eligibility.**
  Who counts as "high risk" enough to be screened is an age band and a pack-year
  cut-off written by a committee, and moving it changes who is a patient in
  exactly the way the ASCVD risk threshold does.

---

**Strengthened by `measles`, not new:**

- **#66 (`capability()` ignores prevention) — THIS SHOULD END IT.** A two-dose
  vaccine, ~97% effective, in use since 1963, off patent, a couple of dollars a
  course, which **eliminated measles from the entire American continent** and
  took deaths from ~2.6 million a year to ~100,000. There is no antiviral and
  never has been, so `intervention: symptomatic`, so `capability: unsolved`, so
  the quadrant reads **`engineering problem` — understood, and nothing can be
  done.** Dengue, rabies and dracunculiasis were the previous arguments; this one
  is not arguable. And note it is an internal contradiction, not just a
  misfiling: `has_capability()` already counts prevention at `prophylaxis` and
  above, and `capability()` does not, so the two functions disagree about the
  same record.
- **#100 (the schema is patient-scoped) — and here the harm lands in OTHER
  RECORDS.** Measles destroys existing immunological memory, erasing much of the
  antibody repertoire a child had built against everything else, and elevates
  mortality **from other infections for two to three years afterwards.** A
  substantial share of measles' true burden is pneumonia and diarrhoea deaths
  filed under pneumonia and diarrhoea. `residue` holds what the disease left in
  *this* patient; there is no field for a deficit whose consequences are counted
  against other entities.
- **#106 (winning removes capability) — second record, and now generalisable.**
  Smallpox: no clinician has seen a case. Measles: a doctor trained where measles
  was eliminated has probably never seen one either, so the first cases of an
  outbreak are diagnosed late — as a viral exanthem, as drug rash — while the
  patient sits in a waiting room seeding it. **With an R0 of fifteen, a few days
  of that is the outbreak.** This is not a smallpox peculiarity; it happens to
  any eliminated disease, and polio is next.
- **#56 (`moved` must record regressions) — SECOND backwards entry, and the first
  written while it was happening.** Yaws' 1964 entry was archaeology. Measles'
  2020 entry — `access: 0.8 → 0.55` — is a rating going down in the present
  tense, for reasons that have nothing to do with the virus or the vaccine.
  **The register's first contemporaneous regression**, which is what a north star
  is for.
- **#98 (symptom relief is not benefit) — third record in a row.** Vitamin A, two
  cheap doses, roughly halves measles mortality where deficiency is common, and
  it scores as `symptomatic` because it does not touch the virus. After Marburg's
  supportive care and COPD's bronchodilators, the pattern is established rather
  than argued.
- **#105 (prevention has costs and no field) — inverted, and it still bites.**
  Smallpox needed the field because its vaccine's toll ended the programme. For
  measles the honest entry would be **almost nothing** — the MMR vaccine is among
  the best-tolerated products in medicine — and the register still cannot say it.
  **The gap between the measured toll and the perceived toll is doing more damage
  to this record than any biological obstacle**, and neither number has a home.
- **The missing blocker kind — third record.** Ebola's Kivu response (treatment
  centres burned), H5N1's farm workers (cannot afford to be tested), and now
  measles refusal. In all three the obstacle is *the affected people have reasons
  not to cooperate with the intervention* — and the reasons run from entirely
  justified to demonstrably false, which is #107's problem in the taxonomy rather
  than in a field.

---

**Strengthened by `smallpox`, not new:**

- **#56 (a finished job vs one held finished) — ANSWERED, and the answer is that
  there may be no finished jobs.** This gap asked for smallpox by name as the
  control where *nothing happens, it is over*. It does not hold. Live variola
  sits in two freezers and its destruction has been deferred at the World Health
  Assembly since 1986; the genome is published; orthopoxviruses have been
  synthesised de novo from ordered DNA; and vaccine stockpiles are maintained
  against exactly that. **Smallpox is not over, it is held over** — by a
  stockpile, a treaty, and a standing decision not to rebuild it. That is
  different in kind from sleeping sickness, and not in the direction #56 hoped.
- **#66 (capability ignores prevention) — fifth instance, and this one was an
  outright contradiction rather than a misfiling.** `capability()` special-cased
  `prevention: eradicated` and `quadrant()` did not, so smallpox derived
  **`capability: curable` and `quadrant: engineering problem` at the same time**,
  and `orphaned` fired — *science done, nobody carrying it* — about a disease
  nobody has. **Fixed**, by applying the one already-decided special case
  consistently through a new `is_eradicated()` helper, with tests. That is not
  #66, which remains open: the design question of whether prevention should count
  as capability in general is untouched.
- **#102 (some diseases can never generate the evidence approval requires) —
  tempered by its own solution.** Marburg's record named licensure on animal
  efficacy data as the way out. **Smallpox used it**: tecovirimat is licensed for
  a disease that has not existed since 1978. And its one randomised human test in
  a related orthopoxvirus disease — clade I mpox in the DRC — did not show the
  expected benefit on lesion resolution. That result is about mpox, not smallpox,
  and it is still the closest thing to evidence there is. **The pathway lets a
  product be licensed; it does not tell you the product works**, and #102 should
  be read with that attached.
- **#57 (the register cannot value maintenance) — fifth direction, and the
  purest.** Two secure freezers, a vaccine stockpile, a surveillance obligation
  and a recurring diplomatic argument, funded indefinitely, for a disease with
  zero cases. Every arithmetic in this register argues against it.
- **`delivery: barely` on a disease with no cases.** `reach` is 0.255 because
  `efficacy` and `access` describe a hypothetical patient, so the band comes out
  *barely*. Left unfixed deliberately: it is the same category error #103 named
  for H5N1 — scalars defined over patients, applied to a record that has none —
  and patching the band would hide it.

- **#69 (the intervention is administered to another species) — fifth record and
  a different order of magnitude.** Sheep, dogs, pigs, dogs again — and now
  **hundreds of millions of poultry culled**, every chicken in Hong Kong in 1997,
  whole dairy herds under movement restriction. It is the intervention that has
  actually worked against this disease, it is deliberately inflicted, and the
  cost falls on farmers and on birds. `who_could` still has no veterinary
  service, five records later, and now no agriculture ministry either.
- **#100 (the schema is patient-scoped) — and here the *toll* escapes it.**
  Ebola showed a cured patient carrying risk for others. H5N1 shows the largest
  harm of the response falling on people who are not patients at all: farms
  ruined, flocks destroyed. `toll` reads `minor` and is accurate by its own
  definition, which is the problem.
- **#101 (a knowledge question can be answered and change nothing) — and this
  record's knowledge blocker was written to that standard.** It states what
  becomes possible if answered, and for *will it become transmissible* the honest
  answer is **better watching, not prediction** — a question about a stochastic
  process does not become a forecast however much is spent on it. First blocker
  in the corpus written with #101's discipline.
- **#102 (some diseases can never generate the evidence approval requires) —
  inverted.** Marburg cannot run an efficacy trial because there are too few
  cases. A pandemic influenza vaccine cannot run one because **the pandemic has
  not happened**, and by the time it has, the trial is moot. Same wall, opposite
  reason.
- **#57 (the register cannot value maintenance) — fourth direction.**
  Dracunculiasis: paying to hold a count at fourteen. Ebola and Marburg: paying
  for a stockpile that is useful intermittently. H5N1: **paying continuously to
  watch for an event that may never come.** The register's arithmetic argues
  against all four and is wrong all four times.
- **A body of knowledge that is itself the subject of a safety argument.** The
  ferret transmission experiments that produced most of what this record relies
  on prompted a research moratorium and remain contested. `standing` records
  whether a *blocker* is documented or alleged; there is no way to record that
  the **evidence** is disputed on grounds of danger rather than validity. Unique
  to this record so far, and the queue has nothing else like it.
- **The people best placed to detect the start of a pandemic are the least able
  to afford reporting it.** Poultry workers in rural Asia and Egypt; US farm
  labourers frequently without sick pay, regular healthcare, or immigration
  status. Filed as `logistics`, and it is really the same missing blocker kind
  Ebola's Kivu record needed — *the affected people have good reasons not to
  cooperate with the response*. **Second record in three needing it.**

---

**Strengthened by `marburg`, not new:**

- **#98 (symptom relief is not benefit) — and here the benefit is SURVIVAL.**
  COPD made the point with breathlessness. Marburg makes it with death.
  Intensive supportive care — fluids, electrolytes, organ support — appears to
  move case fatality from near ninety percent to near a quarter, and it is
  `symptomatic` by the schema's own words because the virus replicates and
  clears on exactly the same schedule. **The register scores that as no
  capability at all.** If #98 needed a second witness, this is a much sharper one
  than the first.
- **AND THE `orphaned` FLAG MISSES THE RECORD THAT MOST EXEMPLIFIES IT.**
  `orphaned` means *science done, nobody carrying it* and is described as the
  register's actionable output. Marburg has a vaccine candidate **on the same
  rVSV platform as the licensed Ebola vaccine**, candidate monoclonals that
  protect primates, and no licensee, because the market is about ten cases a year
  in the poorest places. It does not fire, because `has_capability()` is false,
  because `capability()` reads only `intervention`. **Ebola gets the flag and
  Marburg does not**, which is precisely backwards. Same root as #66 and #98.
- **`restored: n/a` on a disease most people survive.** The value means *nothing
  to be restored from — no capability, so nobody reaches the end of successful
  treatment*. Around sixty percent of Marburg patients given good supportive care
  live, and they carry arthralgia, fatigue, uveitis and worse. The register says
  the question does not apply. Third derivation broken by the same root in one
  record.
- **#91 (the register has no memory before its own first pass) — and no account
  of causes either.** Marburg and Ebola are the same virus family, clinically
  indistinguishable, comparably lethal, with the same bat-reservoir shape and
  **the same working vaccine platform.** One is `curable` and one is `unsolved`.
  The difference is not scientific: **Ebola had 2014** — 28,600 cases, 11,300
  deaths, cases in Europe and the United States — and Marburg's largest outbreak
  ever was 252 people in Angola. The register can state both ratings and cannot
  say that the second is a consequence of the first's history. #91 asked for
  backdated `moved:` entries; this asks for something harder — *why the rating is
  what it is* — and both are the same missing dimension.
- **#99 (the register assumes a steady state) — the extreme.** Marburg's
  `burden.deaths` reads **8 per year**, the smallest figure in the register,
  computed as ~475 deaths since 1967 divided by the years since. Ebola's 310 was
  already an artefact; this is an artefact an order of magnitude smaller, for a
  disease with a ninety percent case fatality in living memory.
- **Rarity lengthens the outbreak window, which is what makes the disease
  dangerous.** Ebola is a name every clinician in the region knows. Marburg has
  produced fewer than a dozen recognised outbreaks in fifty-eight years, so the
  prior a clinician assigns it is near zero and index cases are identified
  retrospectively. **The rarer the disease, the later the diagnosis, and the
  later the diagnosis the larger the outbreak** — a feedback loop with the same
  shape as #77's stigma loops, running on clinical suspicion instead.
- **`strata` correctly absent, one record after Ebola correctly had it.** Marburg
  virus and Ravn virus are as distinct as Zaire and Sudan ebolavirus, and it
  changes nothing, because nothing is licensed against either. **A partition that
  does not disagree about capability is taxonomy, not a stratum** — and the two
  records together are the cleanest available statement of what the field is for.

---

**Strengthened by `ebola`, not new:**

- **#93 (`strata` cannot override `mechanism`) — and here `strata` works exactly
  as designed, one record after stroke broke it.** Zaire, Sudan and Bundibugyo
  ebolavirus are a genuine partition: a case is one species, the fractions sum,
  and the mechanism is the same across them. What differs is *what is licensed* —
  Zaire has a vaccine and two monoclonals, Sudan has neither, and the products do
  not cross-protect. So **"is Ebola solved" depends on which Ebola**, ⧉ fires,
  and the register says the question is malformed rather than picking a side.
  The contrast with stroke is instructive: stroke's strata differ in *mechanism*
  and the field forbids it; Ebola's differ only in capability and it is fine.
- **#57 (the register cannot value maintenance) — from a new direction.**
  Dracunculiasis raised it as paying tens of millions a year to hold a count at
  fourteen. Ebola raises it as **a stockpile**: vaccine under ultra-cold storage,
  monoclonals, laboratories, trained responders — all of which must be paid for
  continuously to be useful intermittently. The register's arithmetic argues
  against both, for the same reason, and it is wrong both times.
- **The blocker taxonomy has twelve kinds and none of them is *the affected
  community does not trust the people who arrived*.** In Kivu, treatment centres
  were burned and responders killed; safe burial teams were resisted because they
  asked families not to wash their own dead. **Where trust failed, every
  technical capability in the record became unusable** — the vaccine, the
  monoclonals, the tracing, all of it. Filed as `policy` in the record, with the
  mismatch stated rather than hidden. This is not `adherence` (that is a patient
  continuing a therapy) and not `logistics` (the supplies arrived).
- **#61 (one record, several populations) — and the toll is a community's, not a
  body's.** Ebola's treatment toll is `minor` and correctly so: the monoclonals
  are benign. What treatment actually costs is dying inside plastic sheeting
  without your family, and families being forbidden to bury their dead as their
  culture requires. That is a real harm, caused by the intervention, and it is
  not permanent damage to a body — so the field records `minor` and means it.
  **It also has an epidemiological consequence**: fear of the treatment unit
  delays presentation, which is the single thing that most determines survival.
- **#84 (the diagnostic failure is not the assay) — third instance, new
  mechanism.** RT-PCR is definitive. **The early presentation is
  indistinguishable from malaria**, which is endemic everywhere Ebola emerges,
  so the first cases are treated as malaria — correctly, on the base rates — and
  the outbreak is recognised only once a cluster forms or a health worker dies.
  No improvement to the test fixes that.
- **`mechanism` asks how the cause produces the phenotype, and for an emerging
  zoonosis the decisive question is upstream of that.** Ebola's pathogenesis is
  well characterised; **the reservoir is still not established, nearly fifty
  years after 1976.** Bats are strongly suspected and infectious virus has
  essentially never been isolated from a wild population. Without it there is no
  predicting a spillover and no acting before the first human case — the only
  intervention that would ever be cheap. The axis has no place for *where does it
  come from*, and h5n1 (next but one) will make this much worse.

---

**Strengthened by `copd`, not new:**

- **#89 (`disease-modifying` binned with `none`) — COPD ADJUDICATES BETWEEN THE
  THREE PROPOSED FIXES, which is why it was added now.** Ischaemic heart disease
  and stroke were misfiled into `engineering problem`. COPD lands in the same
  cell and **the verdict on the course is deserved**: nothing but removing the
  exposure alters the decline in lung function, which is `symptomatic` by the
  schema's own words. So:
  - *Move `disease-modifying` up a rung* — would drag nothing here, since COPD is
    `symptomatic`, but leaves `symptomatic` and `none` conflated, which #98 now
    shows is its own error.
  - *Delete the quadrant* — loses a true statement about COPD.
  - **Add a middle column** — separates all three records correctly. This is the
    fix.
  A record where the harsh verdict is deserved was needed to tell the repairs
  apart, and forty-three records had not supplied one.
- **#90 (the denominator is a threshold somebody chose) — past its logical end.**
  For ischaemic heart disease a threshold decided whom to *treat*, and the
  disease existed either way. **COPD is diagnosed by a number: FEV1/FVC below
  0.70.** A person with visible emphysema on CT and a ratio of 0.72 does not have
  the disease. Worse, the cut-point is *known to be biased* — the ratio falls
  naturally with age, so a fixed threshold overdiagnoses the old and
  underdiagnoses the young, and switching to an age-adjusted limit moves millions
  across the line in both directions. **The entity is the threshold**, and the
  register's prevalence figure counts people on one side of a contested line.
- **#87 (the intervention is non-specific) — third consecutive record, and the
  register has now described the same two exposures from three organs.** Tobacco
  and air pollution drive ischaemic heart disease, stroke and COPD — 19.1 million
  deaths a year across three records — and lung cancer, which is missing. **Six
  gaps now point at this.** It should stop being a gap and start being a field.
- **A prevention with a threshold, which `access` cannot express.**
  Cleaner-cookstove trials have repeatedly underdelivered, and the most credible
  explanation is that households kept the old stove alongside the new one, so the
  exposure reduction achieved was too small to matter. **A programme reaching
  everybody halfway may be worth less than one reaching half of them
  completely**, and `access` is a linear fraction that says the opposite.
  First instance in the corpus; adherence in ischaemic heart disease is the
  nearest neighbour and is not the same shape.
- **"The intervention nobody profits from is the one nobody delivers" — fourth
  instance and the purest.** Pulmonary rehabilitation matches or beats the drugs
  on symptoms, exercise capacity and admissions, involves no drug, device or
  patent, and reaches under a tenth of eligible patients in wealthy systems.
  Alongside stroke units, leprosy self-care and hydrocelectomy. Four records is
  a pattern, and the register has no field for *who would be paid if this
  happened*.

---

**Strengthened by `stroke`, not new:**

- **#89 (`disease-modifying` binned with `none`) — no longer needs arguing.**
  Stroke lands in `engineering problem` one record after ischaemic heart disease
  did. **The register now says "the mechanism is known and nothing can be done"
  about the first and third largest causes of death on Earth** — 15.6 million
  deaths a year between them, against thrombectomy effect sizes that are among
  the largest in medicine. Fix this before the next cardiovascular or oncology
  record; every one of them will land in the same cell.
- **#87 (the intervention is non-specific) — and now with a reordering that
  matters.** Stroke's prevention list is almost identical to IHD's, except that
  **blood pressure is the dominant factor and overwhelmingly so for the
  haemorrhagic stratum** — the one where acute treatment does not work. So here
  prevention is not a cheaper alternative to treatment, it is *the entire
  strategy against the untreatable quarter*. Which is #66 (capability ignores
  prevention) at its most consequential: the register scores zero capability for
  the only thing that works.
- **#61 (one record, several populations) — and this time it is the axes, not a
  flag.** `efficacy: 0.50` averages a stratum where thrombectomy needs a handful
  of patients treated to leave one more independent, against a stratum where
  essentially nothing works. **The resulting number describes no actual patient.**
  The strata carry the honest figures and the record-level scalar is an artefact
  of the schema requiring one.
- **#63/#87 (benefits crossing entity boundaries) — a new direction: a treatment
  that causes another record.** Anticoagulation for atrial fibrillation prevents
  ischaemic stroke and causes intracerebral haemorrhage — **one stratum of this
  record treated at the expense of another stratum of the same record.** The
  schema can hold that as `toll`; it cannot hold that the harm lands in a named
  entity the register also tracks.
- **A disease that disables the alarm — third instance, and now named twice.**
  Buruli ulcer's mycolactone is analgesic. Noma's early stage looks like a sore
  mouth. Stroke removes, via aphasia and neglect, *the patient's ability to
  report that anything is wrong*. #86 named symptom-as-transmission-mechanism;
  this is the neighbouring shape — **symptom-as-suppressor-of-help-seeking** —
  and three records now carry it.

### And the register's own tooling had a silent failure — logged because it is the kind it is built to catch

Writing stroke's `strata` from **SCHEMA.md's own example** produced
`fraction: {value: 0.65, units: ..., src: recall}`. The bounded YAML loader in
`check.py` does not read inline flow mappings — and did not say so. It returned
the text as a **string**, the record passed every schema check, and it crashed six
hundred lines later inside a report emitter with a `TypeError` naming neither the
file nor the field.

Two defects, and the second is the real one:

1. **SCHEMA.md documented a syntax the loader cannot read**, in six places,
   including the passage that introduces the `{value, units, src}` convention.
   Both are now block form and the loader's limitation is stated where the
   convention is introduced.
2. **The loader guessed instead of refusing.** Its own header comment claims
   *"anything else raises"*, and it did not. It now raises `NordsternError` with
   the offending text and the fix.

This is the family's oldest rule arriving from an unexpected direction: *a check
that cannot run reports `skipped`, never `ok`*. A parser that cannot read a value
must not return something that looks like one. Forty-three records in, the only
reason this had never fired is that every previous record was written by copying
a neighbouring file rather than the documentation.

**And fixing it exposed a third defect, which is still open.** `load()` uses
PyYAML when it is importable and the bounded loader otherwise — and the two now
**disagree**: PyYAML reads inline flow mappings, the bounded loader refuses them.
So a record written from SCHEMA.md's old examples would work on a machine with
PyYAML installed and fail on one without, which is the worst possible failure
mode for a register whose whole claim is that the same input gives the same
answer. **Sperrwerk tests that its two loaders produce identical reports for
exactly this reason.** Nordstern should do the same; `test_check.py` currently
skips the refusal tests when PyYAML is present and says why, which records the
divergence without resolving it.

**The Python side had no tests at all** until this record — `node --test web/`
covers the front end and the built artifacts, so it exercised the derivations
only through whatever the corpus happened to contain. `test_check.py` (17 tests)
now pins the loader contract and the three derivations that have been
demonstrably wrong at least once: `restored`, `window_toll_link` (schistosomiasis
forced it) and the `residue`-without-capability rule (dracunculiasis forced it).
It is deliberately small and is not a suite.

---

**Strengthened by `ischaemic-heart-disease`, not new:**

- **#66 (capability ignores prevention) — most expensive instance yet.** Most of
  the coronary mortality decline is preventive: smoking collapse, blood-pressure
  control, primary-prevention lipid lowering. `capability()` reads only
  `intervention` and scores none of it. Combined with #89, the register misses
  the victory on *both* axes at once.
- **#87 (the intervention is non-specific) — the other end of the wealth
  distribution, three records later.** Noma is prevented by feeding children;
  IHD is prevented by people not smoking. Both prevent half a dozen diseases at
  once, neither is chargeable to any entity in this schema, and between them they
  are plausibly the two highest-value interventions in the history of public
  health. **A child's nutrition and an adult's cigarettes are the same schema
  problem**, and that it took a fatal facial gangrene and the world's largest
  killer to show it is the point.
- **`orphaned` fires on ischaemic heart disease, and the flag means something
  different than it says.** The docstring reads *"science done, nobody carrying
  it"*, and a reach ceiling of 0.6 was added specifically so HIV — heavily funded
  but imperfectly delivered — would not qualify. IHD is among the most funded and
  most studied diseases in medicine and sails under the ceiling at reach 0.30,
  because the global denominator is dominated by places where generic secondary
  prevention is not delivered at all. **The flag is measuring geography, not
  championship.** The docstring already concedes the ceiling is "a tunable, not a
  truth"; this says the tunable is standing in for a distinction the register has
  not made — *unowned* versus *under-delivered*.
- **#48 (rank by burden) — the arithmetic just changed shape.** One record took
  the register's accounted mortality from ~3.5M/yr to ~12.5M/yr. **A single
  entity is now 72% of the total.** Any burden-weighted view is currently a view
  of ischaemic heart disease plus noise, which is an argument for adding stroke,
  COPD and the major cancers *before* building the metric, not after.
- **`strata` assumes a partition and IHD is a trajectory.** The natural
  sub-populations — stable disease, acute coronary syndrome, post-infarct
  ischaemic cardiomyopathy — are phases of one person's course, and `fraction:`
  must sum to 1 over disjoint buckets that do not refill from each other. Breast
  cancer's stages are diagnosed as one or the other; these are passed through.
  The record carries no `strata` block and says why.
- **#59-adjacent (`window_toll_link` reads both costs) — second instance, and
  the largest.** Schistosomiasis forced the fix; IHD confirms it at nine million
  deaths. The treatment toll is `clean` (generic tablets), the residue is
  `costly` (myocardium does not regenerate), and **the window and the residue are
  the same fact seen from two ends** — every minute of occlusion converts
  salvageable muscle into scar. `time is muscle` is the most literal window in
  the register and the only one health systems have been engineered against this
  hard.
- **#33-adjacent — `efficacy` has no natural meaning for a risk-shifting
  therapy.** The axis is defined as the fraction of patients in whom the
  intervention *works*. Statins do not cure individuals; they shift a
  distribution. The 0.75 recorded here is target attainment, and a different
  defensible reading — events prevented, absolute risk reduction, lives saved —
  gives a very different number. Every chronic-disease record still to be added
  will hit this.

---

**Strengthened by `noma`, not new:**

- **#60 (the intervention is aimed at the residue) — fourth record, and the first
  where it is expensive.** Hydrocelectomy takes minutes. A trichiasis lid rotation
  takes minutes. Leprosy self-care is soap and inspection. **Noma reconstruction
  is staged maxillofacial surgery** — free tissue transfer, trismus release that
  recurs and needs redoing, general anaesthesia in a malnourished child — mostly
  delivered by visiting missions, so children wait years and are operated on once
  by a team that will not return for the revision. The proposed `residue`
  capability field therefore needs its **own cost and its own access**, not just
  its own rung; three cheap instances made it look like a rung.
- **#61 (one record, several populations) — and here it produces a wrong flag,
  visibly.** `overtreatment_risk` fires on noma: capability + costly toll +
  `prognostic: none`. But the prognostic gap is *which malnourished child with
  gingivitis will progress*, and the costly toll is *reconstructive surgery on
  survivors* — **two different populations, multiplied together by a derivation
  that assumes one.** The first false positive in the corpus traceable to this,
  which makes it a testable case rather than an argument.
- **#33 (the burden is unknown) — the worst instance, and worse than MSMDS's.**
  MSMDS is unknown because it is rare. Noma may be common; the number is 28 years
  old and structurally biased. See #88.
- **#77 (stigma is a feedback loop) — third instance and the tightest.** For
  leprosy stigma delays presentation; for scabies it suppresses reporting. For
  noma the disfigurement *is* the stigma is *why the survivors are hidden* is
  *why the burden is unknown* is *why nobody funded it*. Four steps, one object.
- **#65 (the register inherits somebody else's attention) — the sharpest date.**
  Noma was listed as an NTD in **December 2023**. It is in this corpus because of
  that listing, and it was exactly as bad in 2022.
- **#84 (diagnosis is a trained person, not a device) — third record, most
  acute.** Established noma needs no test; it is a hole in a child's face, and by
  then it is too late. Early noma is a wasted toddler with a sore mouth, and what
  distinguishes it is a health worker who knows the disease exists and looks
  inside the mouth *that day*. Before December 2023 no curriculum mentioned it.
  **The cheapest lever in the register, and it is training.**

---

**Strengthened by `dracunculiasis`, not new:**

- **#66 (capability ignores prevention) — this is the reductio, and it should now
  be fixed without waiting for anything else.** Dengue was the argument: two
  licensed vaccines, filed `unsolved`. Rabies was worse: near-perfect
  post-exposure prophylaxis against a 100%-fatal disease, filed `unsolved`.
  **Dracunculiasis has no drug and no vaccine and has never had either**, is
  down from 3.5 million cases a year to about fourteen, and is filed `unsolved`
  in the `engineering problem` quadrant — *understood, and nothing can be done* —
  for a disease that is about to stop existing. Three records, escalating, and
  this one cannot be argued with.
- **THE CHECKER CAUGHT AN ERROR IN MY OWN RULE, which is what it is for.**
  `residue` required capability, on the reasoning that with nothing that works
  nobody survives to be left with anything. Dracunculiasis is **self-limiting**:
  there is no treatment, the worm emerges over weeks, the episode ends, and a
  minority are permanently disabled by the secondary infection. So a residue
  exists with no cure anywhere near it. The precondition was wrong — the real
  test is whether the **episode ends**, by cure *or* by resolving on its own, and
  what a residue cannot mean is damage from a disease still doing it
  (Huntington's). Downgraded to a warning that states both cases, because the
  distinction needs a person.
- **#69 (intervention administered to another species) — fourth record.** Sheep
  (echinococcosis), dogs (rabies), pigs (taeniasis), and now dogs again: infected
  animals are tethered while the worm emerges and larvicide is applied to their
  water. `who_could` still has no veterinary service, four records later.
- **#48 (rank by burden) — below the resolution of any metric.** Sleeping
  sickness at 800 cases already broke the ranking. **Fourteen** is not a rounding
  error; it is beneath one. And the programme costs tens of millions a year, is
  entirely correct to, and the register's own arithmetic argues against it —
  which is #57 (cannot value maintenance) stated as starkly as it can be.
- **#54 (fragility) — a single philanthropic institution has carried this for
  four decades.** That persistence is why dracunculiasis did not become yaws.
  It is also, by the register's own reckoning, a dependency.

---

**Strengthened by `taeniasis-cysticercosis`, not new:**

- **#55 (no edges) — third consecutive record, and this edge is `documented`
  where scabies's was `alleged`.** Neurocysticercosis causes something on the
  order of a third of epilepsy in endemic areas and is described as the leading
  preventable cause of epilepsy worldwide. **Epilepsy is a record in this
  register** — rated `mechanism: partial`, reach 0.272, blockers logistics and
  policy — and it does not mention parasites. Scabies→rheumatic heart disease is
  actively researched and unsettled; this one is textbook. **Two consecutive
  records supply the two standings a relation model would need**, which is the
  cleanest possible argument for building #55 and #62 together.
- **#68 (no rung for correctly doing nothing) — second record, different reason.**
  Echinococcosis watches CE4/CE5 cysts because they are inactive. Here some
  patients are not given anticysticidal drugs **because killing the parasite
  could kill them.** Same missing rung, opposite justification — and both are
  clinical achievements the ladder records as `none`.
- **#69 (the intervention is administered to another species) — third record, and
  there is a working vaccine again.** Sheep (echinococcosis), dogs (rabies), and
  now **pigs: TSOL18 plus oxfendazole**, which clears porcine cysticercosis.
  `who_could` still has no veterinary service. Three records with three vaccines
  for three species, none of which counts as prevention.
- **#72 (eradicability is a property) — this one passes the checklist.** Humans
  are the only definitive host, there is no wildlife reservoir that matters, and
  every link in the cycle is interruptible — which is why *T. solium* appears on
  lists of potentially eradicable diseases. What it lacks is the one thing yaws
  also lacked: **a way to find the asymptomatic carriers.** Second record where
  eradicability turns entirely on finding silent infection.
- **Both risk flags fire, correctly, for the third time.** `overtreatment_risk`
  and `futile_treatment_risk` both trip — real capability, a permanent price, no
  way to say who needs treating and no way to say who will be harmed by it. It
  joins Crohn's, bipolar and mycetoma, and it is the cleanest instance yet
  because the harm and the benefit come from the same mechanism.

---

**Strengthened by `scabies`, not new:**

- **#55 (no edges) gets its sharpest and first ACTIONABLE instance, with both
  endpoints already in the register.** Scratching scabies breaks the skin; Group
  A *Streptococcus* enters; impetigo follows; and streptococcal **skin** infection
  is increasingly implicated in acute rheumatic fever and therefore in
  **rheumatic heart disease** — a record this register already holds, rates
  `partial` with reach 0.2 and ⚑, and whose own blocker list says the problem is
  benzathine penicillin supply.

  Ivermectin mass administration for scabies cut impetigo by around two thirds in
  Pacific island trials. **So a cheap, tested intervention on one record may be
  an upstream intervention against another, and neither record can say it.**
  Earlier edges were a constraint (*Loa loa*), a harm (dengue → measles) or an
  association (schistosomiasis → HIV). This one **would change what a funder
  does**, which is the first time that has been true.

  Note what it also needs: the skin route to rheumatic fever is *actively
  researched and not settled* against the classical throat model. So a relation
  between records would need a **standing** — documented, alleged, disputed —
  exactly as blockers have and ratings do not (#62). The relation model and the
  standing problem are the same problem.
- **#48 (rank by burden) — the proposed fix would still under-count this
  record.** The register ranks on deaths and scabies has none. The remedy
  proposed was DALYs — and **standard disability weights for itch and skin
  disease are low** relative to what three hundred million people describe:
  relentless nocturnal itch, sleep deprivation, school absence, social exclusion.
  So the metric that rescues tuberculosis from the no-champion list would still
  discount the second-largest prevalence in the corpus. **Third consecutive
  warning about that metric** — leprosy on gameable denominators (#76), trachoma
  on unpriced externalities (#78), and now weighting.
- **#77 (feedback loops) gets a second instance, and the first purely clinical
  one.** Itch persists for weeks after cure, because it is a hypersensitivity
  reaction to dead mite antigen rather than an injury. There is no test of cure.
  So treatment failure, reinfestation, resistance and normal post-treatment itch
  are indistinguishable — and the usual response is to re-treat with a topical
  agent **that is itself an irritant**, which causes itch, which prompts further
  treatment. Leprosy's loop ran through stigma; this one runs entirely through a
  missing measurement.
- **#45 (no test of cure) — fifth record, and the first where the absence does
  active harm** rather than merely preventing audit. Chagas cannot confirm cure;
  TB cannot for latent infection; visceral leishmaniasis's dipstick structurally
  cannot; schistosomiasis does not look. Here the missing test *drives
  over-treatment* and would hide emerging drug resistance until it was
  widespread.
- **No `window`, and the reason is new.** The schema's test is whether capability
  changes with timing, and scabies is curable on the last day as readily as the
  first. What accumulates while nobody treats it is impetigo, streptococcal
  infection and probably rheumatic heart disease — **so the price of delay is
  real, large, and paid on somebody else's record.** A window here would claim
  the damage lands on this entity. It does not.

---

**Strengthened by `rabies`, not new:**

- **#66 (capability ignores prevention) at maximum severity — this should now be
  fixed.** Dengue raised it: two licensed vaccines, filed `unsolved`. Rabies is
  worse in every direction. Post-exposure prophylaxis is **close to perfectly
  effective at preventing a disease that is otherwise ~100% fatal**; dog
  vaccination has eliminated dog-mediated rabies from western Europe and cut
  Latin American deaths by over 95%; and because nothing works once symptoms
  begin, `intervention: none` → `capability: unsolved` → quadrant **engineering
  problem**, next to Huntington's. **Nowhere else in this register is the gap
  between what is possible and what is recorded so large.** Two records, one of
  them extreme; the `capability()` / `has_capability()` contradiction should be
  resolved before anything is built on either.
- **#69 (the intervention is administered to another species) — second record,
  and it was predicted.** The echinococcosis entry said: *"Watch for the second
  record before building anything — rabies is the obvious one and is not in the
  corpus, and its answer is also to vaccinate dogs."* It is, and it is: ~99% of
  human rabies is dog-mediated and 70% dog vaccination coverage interrupts
  transmission. `who_could` still has no veterinary service and no agriculture
  ministry. Two records is what that gap said to wait for.
- **#61 (the infected and the diseased are different people) — the furthest apart
  yet.** Filariasis was 51 million infected against 36 million disabled. Leprosy
  was 200,000 treated against 3–4 million disabled. Rabies is **29 million given
  prophylaxis against 59,000 who would have died** — a factor of five hundred,
  and almost everyone treated was never going to develop the disease. There is no
  way to know which of them would have, which is #80.
- **`toll: none` appears for the first time, and it is not good news.** There is
  no treatment, so there is no price for treatment. Meanwhile the *prevention's*
  toll collapsed historically — nerve-tissue vaccines caused neuroparalytic
  complications at rates around one in several hundred to one in a couple of
  thousand and were in use into this century; cell-culture vaccines are very
  safe. **That is a large real improvement in the intervention that actually
  works, and there is nowhere to record it**: `toll` is defined as what the cure
  takes, `moved` needs an axis, and prevention has neither toll nor efficacy
  (#49, #66).

---

**Strengthened by `trachoma`, not new:**

- **#76 (a metric satisfied by moving its denominator) gets its counterexample,
  one record later.** Leprosy's elimination target was registered prevalence —
  people currently on treatment — and shortening treatment moved it. **Trachoma's
  criteria are follicular trachoma prevalence in children aged one to nine, plus
  trichiasis prevalence, plus demonstrated system capacity.** None of those moves
  when a treatment schedule changes; the first is a transmission proxy in the age
  group that carries transmission. Same phrase, *"elimination as a public health
  problem"*, and one is gameable by construction and the other is not. **A metric
  can be built well**, which is the more useful half of #76.
- **#60 (the residue is the treatable part) — third record.** Filariasis:
  hydrocelectomy. Leprosy: self-care for insensate limbs. Trachoma: **a
  lid-rotation operation for 1.5 million people with in-turned lashes**, which
  antibiotics do nothing for. Three records, three times the largest available
  intervention is aimed at the residue, and `residue` still has no capability
  axis. Note the wrinkle trachoma adds: the operation **recurs** in a substantial
  minority, so the backlog is partly self-refilling — a residue intervention with
  its own efficacy problem, which is exactly the field the residue block lacks.
- **#58 and #60 are symptoms of one thing, and WHO already solved it
  operationally.** Trachoma's strategy is **SAFE** — Surgery, Antibiotics, Facial
  cleanliness, Environmental improvement. Four components, four actors, four
  timescales, and a package: antibiotics without F and E means reinfection;
  surgery without antibiotics means operating into a continuing epidemic. **The
  register models an intervention as a single act with a single rung.** The
  operational world worked out decades ago that disease control is a portfolio,
  and the schema has not caught up.
- **`moved` reaches a fifth axis.** Single-dose annual azithromycin replaced six
  weeks of twice-daily topical tetracycline ointment in a child's eyes:
  `ongoing` moderate → low. The corpus now has `moved` entries on `toll` (×3),
  `intervention` (×2), `access` (×1, backward) and `ongoing` (×1) — which is
  enough to say the field is general and was never only about capability.

---

**Strengthened by `leprosy`, not new:**

- **#61 (the infected and the diseased are different people) gets its second
  record, and the ratio is worse.** Lymphatic filariasis: 51 million infected
  against 36 million with chronic morbidity. Leprosy: **200,000 diagnosed a year
  against three to four million living with disability.** The treatment programme
  is for the first number and nothing in it is for the second.
- **#60 (the residue is the treatable part) gets its second record, and this one
  needs no drug at all.** Leprosy's deformity is not the bacterium eating flesh —
  it is unnoticed injury to insensate limbs, and the ulcer-injury-resorption
  cycle is stopped by **daily inspection, protective footwear, wound care and
  splinting**. As with hydrocelectomy in filariasis, the largest available
  intervention is aimed at the residue, and `residue` still has no capability
  axis to say so. Two records now.
- **#72 (eradicability is a property, not a state) — the checklist applied, and
  leprosy fails it.** Armadillos in the Americas and red squirrels in the British
  Isles carry *M. leprae*, so there is an **animal reservoir**; incubation runs
  two to twenty years; subclinical infection is common; there is no vaccine
  beyond BCG's partial effect. On the yaws checklist leprosy scores worse than
  yaws — **and leprosy is the one that was declared eliminated.** That is the
  clearest possible argument for putting eradicability in the schema rather than
  leaving it to a target-setting committee.
- **`strata` partition by a fourth thing.** Breast cancer partitions by stage,
  Chagas by phase, echinococcosis by species, visceral leishmaniasis by
  geography, mycetoma by an unobservable cause. Leprosy partitions by **HOST
  IMMUNE RESPONSE** — the Ridley-Jopling spectrum is a classification of the
  patient, not of the pathogen, and the same organism produces tuberculoid
  disease in one person and lepromatous in another. The schema is indifferent to
  which kind of partition it is holding, which #64 already flagged for
  observability and this extends to *kind*.
- **A `moved` on the intervention axis — only the second in the corpus.** MDT in
  1982 took leprosy from `suppressive` (years of dapsone, widespread resistance,
  many patients on indefinite treatment) to `curative`. Every other `moved` entry
  here is a toll reduction; this and hepatitis C's direct-acting antivirals are
  the only genuine capability changes recorded.

---

**Strengthened by `yaws`, not new:**

- **#57 (the register cannot value maintenance) — CLOSED as a question, and the
  register now has its backward entry.** #57 noted that `moved:` must be able to
  record a rating going the wrong way and that no record had needed to. Yaws
  needed to:

  ```yaml
  moved:
    - date: 1964
      axis: access
      from: 0.9
      to: 0.2
      why: the vertical campaign was integrated into primary health care and
           surveillance stopped; yaws resurged through the 1970s and 80s
  ```

  First backward entry in the corpus and the first on a **scalar** rather than an
  enum. The numbers are reasoned rather than measured and are there to make
  direction and scale legible. Note what the entry does *not* say: no drug
  stopped working, no resistance emerged, no reservoir appeared. Nothing about
  the disease changed at all.
- **`residue` is small here BECAUSE the maintenance was performed.** Tertiary
  yaws — gangosa, sabre tibia, joint destruction — is now uncommon, and it is
  uncommon because a generation of children were treated in the 1950s before
  their infections had years to destroy anything. **The best evidence in this
  register for the value of sustained programmes is a low number in a field
  designed to record harm.**
- **#54 (fragility / improvised institutions) — eighth instance, and the first
  that is administrative rather than economic.** Azithromycin is donated at a
  scale of hundreds of millions of doses for **trachoma**, through one of the
  largest drug donation programmes in existence. The same drug, at a small
  fraction of that volume, has no equivalent architecture for yaws. That is not a
  market failure of the usual kind — the product exists and the manufacturer
  already donates it — and it should therefore be easier to fix than any of the
  seven before it.
- **#71 (why late) — and the first high `caught_in_time` in the corpus.** Yaws
  rates 0.95, against 0.1 for Chagas and 0.2 for mycetoma and hEDS. That is what
  a window looks like when a programme is broadly working, and it is worth having
  one in the file so the low numbers elsewhere read as a variable rather than a
  constant.
- **`predictive: n/a`, the good version, third instance.** One dose works in
  ninety-five percent, so there is nothing to select between — the hepatitis C
  and Buruli reason, not the schistosomiasis one. Three clean instances of the
  good version now sit against one of the bad, which is enough to split the value.

---

**Strengthened by `buruli-ulcer`, not new:**

- **#26 (toll reduction moves no axis) — third `moved` entry, and it is now the
  commonest kind of progress in this corpus.** Until the early 2000s Buruli ulcer
  was treated by wide surgical excision, grafting and sometimes amputation;
  since, by eight weeks of oral rifampicin and clarithromycin. `toll`
  catastrophic → minor, capability unchanged. That is the third such transition
  after visceral leishmaniasis (2011) and sleeping sickness (2019), and worth
  stating plainly: **most of the disfigurement people associate with Buruli ulcer
  is the disfigurement of its former treatment.** The register acquired the means
  to record this three records ago and has now used it three times.
- **`predictive: n/a` — the good version, and the contrast is now on the page.**
  Schistosomiasis's `n/a` means *there is one drug, so there is nothing to choose
  between* — abolished by monopoly. Buruli's means *one regimen works in nine in
  ten* — abolished by success, the hepatitis C reason. The register records them
  identically and they are opposite situations. Two clean instances now sit
  beside each other, which strengthens the case for splitting the value.
- **#65 (the register inherits somebody else's attention) gets a sharper form.**
  Much of what is understood about how this organism might reach people has been
  worked out in **Victoria, Australia**, where a growing focus made it a
  wealthy-country problem with research capacity attached. The disease is the
  same in Benin and the evidence base is not. Mycetoma showed attention arriving
  174 years late; this shows attention arriving *from the wrong place*, and the
  register cannot record that a disease's evidence base is uneven because of
  where its patients live.

---

**Strengthened by `echinococcosis`, not new:**

- **#64 (strata presume the partition is observable) gets its control case, one
  record later.** Mycetoma's two causes are clinically indistinguishable without
  a laboratory that is not there. Echinococcosis's two forms — cystic and
  alveolar — are **cleanly separable by the same ultrasound that diagnoses
  them**, and the separation determines everything: one stratum is
  straightforwardly curable, the other is an infiltrating lesion staged with a
  system borrowed from oncology and treated with lifelong albendazole when it
  cannot be resected. Same structural situation, opposite answer, and the schema
  records both identically. Two records is enough to act on.
- **#59 (harm-scoped prediction)** appears again in a third form. Onchocerciasis
  tests to decide who must not receive ivermectin; dengue screens serostatus to
  decide who must not be vaccinated; here the staging scan decides who must not
  be **operated on**. Three records, three interventions, one question the
  `predictive` axis cannot ask: *who will this hurt?*
- **#33 (burden)** — both forms are silent for years and chronically
  underdiagnosed, so prevalence rests on ultrasound surveys in a handful of
  well-studied communities. Same `src: recall` shape as elsewhere, with the
  additional wrinkle that the very tool that would count the disease is the one
  that is not deployed.

---

**Strengthened by `dengue`, not new:**

- **#57 (the register records states, not trajectories) gets its other pole.**
  Sleeping sickness is falling — from over 300,000 cases a year to fewer than a
  thousand — and can be lost. **Dengue is rising**, with its vector's range
  expanding through urbanisation and a warming climate and 2024 the worst year on
  record. Both read as a static row. A register whose purpose is *measure, take
  something off the queue, solve it, re-measure* must be able to represent
  direction of travel, and it cannot.
- **#59 (harm-scoped prediction) gets its second record**, and this one is about
  a vaccine. Whether a person has been infected before determines whether
  vaccination protects or endangers them, so guidance now requires serostatus
  screening — a test to decide who must **not** receive something, exactly as
  the *Loa loa* device is for ivermectin. And it is worse here, because
  `predictive` is treatment-scoped: a decisive, answerable, harm-scoped question
  about a *preventive* intervention is invisible on that axis and on every other.
- **Windows differ in timescale by five orders of magnitude and the field has no
  unit.** Chagas and schistosomiasis close over decades; onchocerciasis and
  lymphatic filariasis over years; mycetoma over years; sleeping sickness over
  months. **Dengue's closes in hours** — severe disease declares itself around
  defervescence and the difference between survival and death is whether someone
  recognised it and started fluids that afternoon. That changes what the "cheap
  lever" is: a decade-long window wants a screening programme, an hours-long one
  wants clinical training and a bed. `window` records what it closes on and never
  how fast.
- **A record with no `residue`, deliberately, after six consecutive ones that had
  it.** Post-dengue fatigue and post-severe-dengue organ sequelae are described
  and thinly characterised. Asserting a residue on that evidence would have been
  the same error as asserting a window in soil-transmitted helminths.

---

**Strengthened by `mycetoma`, not new:**

- **The risk flags fire correctly, and it is the first time in this batch.**
  Gaps #38, #40 and #47 documented three consecutive records where
  `overtreatment_risk` and `futile_treatment_risk` failed — hEDS invisible
  because it has no capability, POTS correctly silent, Chagas missed because the
  toll is not permanent. **Mycetoma trips both**, and it is exactly the case they
  were designed for: real capability, a harsh permanent price (amputation), no
  way to say who will respond and no way to say who needed it. It joins Crohn's
  and bipolar as the only records to fire both. Worth recording that the rules
  work when the shape is the one they describe — the redesign proposed in #47
  should preserve this case, not just fix the three failures.
- **`restored: both` gets its second record.** Sickle cell was the first: the
  cure takes fertility and does not undo the strokes. Here the cure takes a leg
  and does not undo the deformity the disease caused while nobody could identify
  it. Both fields earn their place, and the levers differ — a better antifungal
  reduces the toll, and earlier diagnosis reduces the residue.
- **#33 (burden) — the `unknown` mode at a scale that matters.** MSMDS's
  prevalence is unpublished because roughly a hundred people have it. Mycetoma's
  is unpublished across a belt spanning a dozen countries, because nobody
  counted. Same `src: unknown`, entirely different meaning, and the field cannot
  distinguish *nobody has this* from *nobody looked*.
- **`diagnosis` is a sixth kind of blocker.** Not finding cases (POTS, Chagas),
  not an absent test (hEDS), not a skipped one (schistosomiasis, STH), not an
  exclusionary one (onchocerciasis) — **telling two diseases apart when the answer
  decides between cheap tablets and losing a leg.** A field-deployable
  fungal-or-bacterial test would move roughly forty percent of patients straight
  onto a cure, and it is an assay development problem rather than a scientific
  one.

---

**Strengthened by `soil-transmitted-helminths`, not new:**

- **#44 (records with no Mondo id) gains a fourth reason, and a concrete
  contribution to make.** Mondo has no term for **soil-transmitted
  helminthiasis**. It has the four species individually, and `intestinal
  helminthiasis` as a broader parent whose own editor note reads *"this is a
  vague grouping and does not correspond to any one taxon"*. The reason is new
  and interesting: **this entity is a programmatic category, not an ontological
  one.** WHO groups these four organisms because one tablet treats them and one
  MDA round delivers it — an operational fact about a *response*, not a fact
  about taxonomy. Left `unresolved` rather than accepting the broader parent (see
  #43). So: low back pain has no id because it is a complaint and Mondo is a
  disease ontology; AMR has none because it is a property of an organism; POTS
  has none because Mondo simply lacks the term; and this has none because the
  entity is defined by its programme. **The last two are exactly the cases where
  the register should file a Mondo term request** rather than mint a private id.
- **#53 (diagnosis skipped on purpose)** repeats and compounds. Same arithmetic
  as schistosomiasis — the tablet costs less than the slide — and here the
  consequence lands directly on #63: because nobody types species, nobody knows
  the species mix, so the parasitological efficacy of a deworming round is a
  function of a composition that is never measured, *in the middle of an argument
  about whether deworming works*.
- **`strata` requires a partition, and polyparasitism is not one.** The four
  species have different drug responses and different morbidity, which looks like
  the textbook case for strata — except that co-infection is the norm rather than
  the exception, so they do not partition a population. The schema's one
  available subdivision does not fit, and the record carries the differences in
  prose instead.
- **No `window`, deliberately, and the absence is the finding.** Five NTDs in a
  row could have carried one. Schistosomiasis, onchocerciasis, lymphatic
  filariasis and sleeping sickness all do, because the irreversible damage and
  its timing are not in dispute. Here the claim that childhood treatment prevents
  permanent harm **is** the disputed claim, and putting it in a derived field
  would place the register on one side of its own open question.

---

**Strengthened by `lymphatic-filariasis`, not new:**

- **#54 (fragility) is six for six, and this record shows what donations do not
  cover.** Albendazole, ivermectin and diethylcarbamazine all arrive by
  manufacturer donation, at a scale of billions of treatments. **Hydrocele
  surgery and hygiene kits do not.** So the response is generously supplied
  exactly where a product exists to donate, and thin exactly where the
  intervention is an operation or a bar of soap — which is also where the 36
  million disabled people are. The improvised institution that answered the drug
  problem could not have answered this one.
- **#59 (harm-scoped prediction) gets a second record and a sharper edge.** The
  triple-drug regimen recommended from 2017 is markedly more effective and
  **cannot be used where onchocerciasis or Loa loa are co-endemic**, because
  diethylcarbamazine provokes severe reactions in the presence of either. So
  what can be given here is determined by a map of *other diseases* — the second
  filarial record in a row where the binding constraint on treatment is a
  co-infection. **And Loa loa has a Mondo ID (`MONDO:0016566`).** The edge is
  missing from this register, not from the ontology, which makes it a modelling
  choice rather than a data limitation.
- **#58 (patient-scoped intervention)** repeats exactly: mass administration
  suppresses microfilariae in individuals and eliminates transmission in
  communities, and `intervention: suppressive` records only the first. Two
  filarial records, same structure, which is enough to say the axis needs a scope
  rather than that these two diseases are unusual.
- **Mondo names it after the residue too.** The entity resolved to
  `MONDO:0005761`, whose label is **"filarial elephantiasis"** — the ontology
  identifies the disease by its sequela rather than by its infection, which is
  the same conflation this record exists to unpick, arrived at independently by
  a different project.

---

**Strengthened by `onchocerciasis`, not new:**

- **#54 (fragility) is five for five, and this is the largest instance.**
  Ivermectin for onchocerciasis has been donated by its manufacturer since 1987 —
  the first and biggest drug donation programme in history, billions of
  treatments, given for as long as needed. It has worked completely for nearly
  four decades. Chagas, tuberculosis, visceral leishmaniasis, sleeping sickness
  and now this: **five neglected diseases, five improvised institutions, none of
  them a market**, and the register reads each as a solution rather than a
  dependency.
- **#48 (cannot rank by burden) — fourth consecutive record falling off
  `orphaned`.** Onchocerciasis derives reach 0.675, so like tuberculosis (0.612),
  HAT (0.665) and schistosomiasis's near-miss, it is excluded from the flagship
  triage view. The pattern is now unmistakable: **the register's no-champion list
  systematically excludes large, well-run, still-unfinished programmes**, which
  is precisely the category where sustained money does the most good.
- **The `who_could` vocabulary has no term for the affected community.** Delivery
  here is *community-directed treatment* — villages select their own distributors
  and set their own timing, rather than receiving a vertical programme. It is one
  of the few genuinely community-owned mechanisms operating at this scale, and
  the closest available actor is `patient-org`, which means an advocacy
  organisation and is a different thing entirely.
- **Burden units, again.** The West African control programme's benefit was
  partly counted in **arable land returned to settlement** — tens of millions of
  hectares of river valley. No health register would think to record that, and
  for a vector-borne disease that depopulated the land it was transmitted beside,
  it may be the largest single benefit anyone obtained.

---

**Strengthened by `hat`, not new:**

- **#52 (solved here, not there)** gets its hardest version. Visceral
  leishmaniasis differs by *geography* — Bangladesh and South Sudan differ in
  circumstance. HAT differs by **subspecies, in what is achievable at all**:
  gambiense disease is anthroponotic, so finding and treating people *is*
  transmission control and elimination is genuinely reachable; rhodesiense
  disease has a cattle and wildlife reservoir and **structurally cannot be
  eliminated by treating humans**. One name, one `prevention` field, and one form
  on course for `eradicated` while the other cannot get there by any amount of
  effort.
- **#53 (diagnosis skipped on purpose)** gains its mirror image, and the pair
  brackets the question. Schistosomiasis: the drug is cheap and safe and the
  disease is common, so *skip diagnosis and treat everyone*. HAT: the disease was
  rare and the drug was arsenic, so *test exhaustively before treating anyone* —
  serology, then microscopy, then a lumbar puncture to stage. **Both are correct,
  and they are opposite.** Whether to diagnose is a function of test cost, drug
  cost, drug toll and prevalence; the register treats `diagnosis` as an
  unqualified good and cannot express the trade.
- **#54 (fragility) is now four for four.** Schistosomiasis has one drug; VL
  depends on a donation; TB's pipeline is thin; HAT needs somebody to keep
  manufacturing for eight hundred patients a year, indefinitely, after the
  disease stops being newsworthy — and its historical survival owes something to
  eflornithine having a cosmetic application in wealthy markets. **A treatment for
  a fatal African disease was kept available partly by a facial hair cream.**
  That is the most vivid documented market failure in the corpus and it resolved
  by accident.
- **#26 (toll reduction moves no axis) — closed by a second instance.** VL
  supplied the first `moved` entry on `toll`; HAT supplies the largest movement
  in the register: **`catastrophic` → `minor`**, when fexinidazole displaced an
  arsenical that killed three to five percent of the people it was given to and
  had been first-line since 1949. Capability never changed. The disease was
  curable throughout, and what collapsed was the price the patient paid.
- **A better treatment can abolish a diagnostic *procedure*.** Hepatitis C showed
  a measurement gap closed by better treatment rather than a better test. HAT
  extends it: the lumbar puncture existed to justify giving arsenic, and an oral
  drug effective at both stages largely removed the need to stage at all.

---

**Strengthened by `schistosomiasis`, not new:**

- **#33 (burden)** gains a **sixth** mode: contested by **causal attribution**.
  Schistosomiasis mortality estimates differ by more than tenfold — roughly twelve
  thousand against figures running to two hundred thousand — and everyone agrees
  how many people die of bladder cancer and variceal haemorrhage. The
  disagreement is about how many of those deaths belong to a fluke that caused the
  fibrosis twenty years earlier. At the low figure this is a minor problem; at the
  high one it is a major one; the difference is methodology, not evidence.
- **`predictive: n/a` has a third meaning.** Huntington's: no course-altering
  therapy to predict a response to. Hepatitis C: a treatment that works in
  essentially everyone, so the question was abolished by success. Schistosomiasis:
  **there is only one drug, so there is nothing to choose between.** The selection
  question is abolished by monopoly, which looks identical in this field and is
  the opposite situation.
- **`window_toll_link` was fixed, not merely noted.** It read only `terms`, having
  been written before `residue` existed. Schistosomiasis is the first record whose
  window is paid for entirely in residue — praziquantel is a safe cheap tablet, so
  the toll is `clean` — and the old rule would have reported *no link* on the most
  window-dependent record in the register. It now reads both costs and names which
  one the window is charging.
- **The overtreatment flag got a case right, for once.** Roughly a hundred million
  children a year receive praziquantel untested, and most are not infected in any
  given round. That is overtreatment by any literal reading and it is not a harm,
  because the drug is safe and cheap. `overtreatment_risk` correctly stays silent.
  After three records exposing that rule as too narrow, worth recording that the
  narrowness is sometimes exactly right.

---

**Strengthened by `visceral-leishmaniasis`, not new:**

- **#45 (test of cure)** gets a **third** record and its cleanest statement. rK39
  detects antibody and stays positive for years, so the dipstick that made field
  diagnosis possible is *structurally incapable* of confirming cure, detecting
  relapse, or finding PKDL. Three records now: Chagas has no test of cure at all,
  TB has one for active disease and none for latent infection, and here the test
  that solved diagnosis cannot be turned into one. That is enough to build
  `measurement.confirmatory`.
- **#26 (toll reduction is progress no axis records) — partially answered.**
  It moves `toll`, and `moved:` can carry it. This record's `moved` entry is the
  register's first on an axis other than `intervention`: 2011, `toll` from
  `major` to `minor`, when a single infusion of liposomal amphotericin B replaced
  thirty days of cardiotoxic injections. Capability did not change; the price
  paid for it collapsed. That is the shape of progress the register kept failing
  to see, and it turns out to have had a home all along.
- **The improvised-institution pattern is now three for three.** Chagas got a
  nonprofit product development partnership; tuberculosis got philanthropic and
  public funding; visceral leishmaniasis gets a manufacturer donation to WHO.
  Three neglected diseases, three different patches over the same missing
  incentive, **and none of them a market.** The donation is the most fragile of
  the three: a public health programme across a dozen countries resting on a
  commercial decision that could be revisited.

---

**Strengthened by `tuberculosis`, not new:**

- **#47 (permanence is the wrong variable)** gets its **second** forcing record,
  and the scale is absurd. Latent TB is Chagas at two hundred times the size: two
  billion people infected, five to ten percent will ever progress, nothing
  identifies which, preventive therapy works, and there is no test of cure. So
  ten to twenty people take months of drugs to prevent one case and none of them
  can be told whether it worked. The overtreatment flags miss it for the same
  reason they miss Chagas — the toll is not permanent. **Two records, a quarter
  of the human race, invisible to the flags built to find exactly this.**
- **#45 (test of cure)** likewise gets a second: latent TB infection has no test
  of cure either, and TST and IGRA cannot distinguish latent infection from
  cleared infection at all. TB also supplies the *positive* case the axis needs
  for calibration — for active disease, culture conversion IS a test of cure, and
  it is why active TB treatment can be audited and preventive therapy cannot.
- **#33 (burden)** gains a **fifth** mode, and it is not about data quality:
  **ambiguity between two well-measured quantities.** TB's prevalence is either
  ten million (active disease) or two billion (infection), both well counted,
  two hundred times apart, and the schema has one field and no way to say which
  it wants. Chagas has the same problem at 6.5 million and it went unremarked.
- **The refrain gets its strongest instance, and it resolved.** Bedaquiline is
  the key drug of the regimens that turned resistant TB from a two-year ordeal
  into a six-month course; its price and secondary patents were publicly
  contested, and after sustained pressure the originator undertook in 2023 not to
  enforce them across most low- and middle-income countries. A working therapy, a
  real access barrier, an identifiable actor, and public pressure that **moved
  it**. That is the closest the register has come to the claim it was built to
  test — and the resolution is the half that usually goes unmentioned. Meanwhile
  the forty-nine-year gap between rifampicin (1966) and bedaquiline (2012) was
  broken by philanthropic funding and nonprofit product development, not by a
  change of heart in industry: **the same institutional answer as Chagas, arrived
  at independently.**

---

**Strengthened by `chagas`, not new:**

- **`diagnosis` is not one blocker kind** — Chagas is the POTS variant (a test
  that exists, costs almost nothing, and is not performed) **at the scale of six
  and a half million people**, with a window measured in decades. Over ninety
  percent have never been diagnosed. Nothing scientific is in the way; the
  infected are poor, rural, often migrant and asymptomatic for twenty years, so
  nobody presents and no system looks. It is now the largest cheap lever in the
  register by a wide margin.
- **#33 (burden)** — Chagas is the counter-example that makes the earlier
  entries legible. It is a *neglected* disease and its numbers are the most
  solid in this batch, because WHO and PAHO count it. Neglect and
  uncountability are separable, and it was starting to look as though they were
  not.
- **The market-failure column gains its strongest documented entry.** Both drugs
  date from around 1970 and remained the entire pharmacopoeia for fifty years;
  US approval came in 2017 and 2020 respectively, for a disease with several
  hundred thousand infected people in that country. Nothing was suppressed and
  no regulator refused anything — the incentive was absent, and the response was
  to build a nonprofit product development partnership that does not need one.
  That is now the sixth documented instance and the pattern is consistent: **the
  refrain the blocker axis exists to test keeps resolving into absent incentive
  rather than active obstruction.**

---

**Strengthened by `mcas`, not new:**

- **#33 (burden)** crosses a threshold rather than gaining a fourth mode. hEDS is
  contested by one order of magnitude; MCAS by about three. Past that, the
  problem stops being that a midpoint is inaccurate and becomes that **a single
  number is the wrong shape of answer**. `1.0e-4` in that field is a
  placeholder with a criteria set attached, and nothing in the schema attaches
  it.
- **`diagnosis` is not one blocker kind** — now demonstrated three ways across
  three consecutive records, which is enough to act on:
  | record | the blocker | convertible with money? |
  |---|---|---|
  | hEDS | no test exists | partly — downstream of knowledge |
  | POTS | test exists, free, ten minutes, not performed | **yes, entirely** — recognition and referral |
  | MCAS | test exists and is agreed, but must be caught within ~4h of an unpredictable event | **yes, by engineering** — point-of-care assay, patient-held sampling, standing orders |
  Same taxonomy entry, three different problems, three different buyers. The
  register's claim that `diagnosis` is its cheapest lever is true in the POTS
  sense, sometimes true in the MCAS sense, and false in the hEDS sense.
- **#6 (`contested`)** now has a **fifth** shape and the axis is past saving as a
  boolean: *is it real* (ME/CFS), *where is its edge* (hEDS), *what comes with
  it* (hEDS, POTS, MCAS), *which way does the arrow point* (POTS), and now
  *whose criteria* (MCAS) — the last being the only one that makes two records
  out of one entity.

---

**Strengthened by `pots`, not new:**

- **#6 (`contested` needs to say by-whom and about-what)** gains a **fourth**
  line, and it is the most consequential yet. ME/CFS forced *scientific* vs
  *political*; hEDS added *scope*; POTS adds **causal direction** — whether
  deconditioning is a cause of POTS or a consequence of it. That is not a dispute
  about whether the entity exists, where its edge lies, or what travels with it.
  It is a dispute about which way an arrow points, and it is the only one of the
  four with an immediate bedside consequence, because the two answers prescribe
  opposite advice to the same patient. Four lines under one boolean is now
  clearly untenable.
- **`diagnosis` is not one blocker kind.** hEDS and POTS carry it with opposite
  convertibility and the pair makes the distinction concrete. In hEDS there is no
  test to apply, so the blocker is downstream of a knowledge blocker and money
  moves only part of it. In POTS the test exists, costs nothing and takes ten
  minutes — the entire blocker is recognition, referral and undoing an anxiety
  attribution, which is training and process. Same kind, same taxonomy entry,
  and one is purchasable while the other is not. `scale` carries this today only
  by convention; nothing in the schema enforces that a `diagnosis` blocker with a
  number attached is genuinely buyable.

---

**Strengthened by `heds`, not new:**

- **#33 (`unknown` vs `unverified`)** has a **third** mode. Breast cancer's
  numbers are *unverified and checkable*; MSMDS's are *unknown and unpublished*;
  hEDS's are **contested** — several published figures spanning an order of
  magnitude, disagreeing because they applied different criteria, not because
  anyone measured badly. A single `src` string cannot hold "which of these do you
  mean", and a midpoint is the one answer that is certainly wrong.
- **#34 (heterogeneity within a patient)** now has its **second** record, which
  was the stated threshold for taking it seriously — *"one example is a
  curiosity, two is a shape."* The shape is confirmed and it is broader than it
  looked. In MSMDS, **capability** varies by organ inside one patient. In hEDS,
  **mechanism confidence** does: the musculoskeletal chain (laxity → subluxation
  → pain and degeneration) would survive a refutation attempt, while the systemic
  features have associations and no chain. Rated `correlates`, because the field
  must pick one and picks the lower. So it is not one field that needs splitting
  by system — it is potentially any of them.
- **#6 (`contested` needs to say by-whom and about-what)** gains a **third**
  line. ME/CFS forced the split between *scientific* dispute and *political*
  dispute. hEDS adds **scope** — how much belongs to the entity, as in the
  asserted hEDS/POTS/MCAS triad. "Does it exist", "where is its edge" and "what
  comes with it" have entirely different resolutions, and one boolean carries all
  three.

---

## 202. A replacement has a service life, and the ladder cannot see it · **open**
*Forced by:* `osteoarthritis`.

Total hip and knee arthroplasty rate `curative` and the rating is correct by the
ladder's own words — *a finite intervention ends it.* Nothing is taken daily,
nothing is worn, most recipients need no further treatment, and for the hip the
result is one of the best in this register.

**Nothing was cured.** The joint was not healed; it was excised and replaced with
cobalt-chrome and polyethylene. That is a fourth kind of thing, and the corpus
has been quietly sorting the family for ninety-five records:

| record | the replacement | rated | needs continuous input? |
|---|---|---|---|
| **cataract** | intraocular lens | `curative` | no |
| **osteoarthritis** | joint prosthesis | `curative` | no |
| **congenital-heart-disease** | valve, conduit, patch | `curative` | no |
| **hearing-loss** | cochlear implant + worn processor | `suppressive` | yes |
| **type-1-diabetes** | insulin | `suppressive` | yes |
| **chronic-kidney-disease** | dialysis, or a transplanted kidney | `suppressive` | yes |

**The register has been applying a consistent unwritten rule** — *continuous
input means `suppressive`, fitted-once means `curative`* — and it is a defensible
rule. Write it down.

**Then notice what it cannot see, which is durability.** A joint prosthesis has a
service life of roughly twenty to twenty-five years, and the patient may not.
The same operation on the same joint by the same surgeon is:

- **curative at seventy-five** — the implant outlives the patient, the disease is
  over, `finite` is literally true; and
- **not curative at fifty** — one revision is near-certain and a second is
  likely, each giving worse function, a higher infection risk and a
  shorter-lived implant than the one before.

**No axis in this register is a function of the patient's age**, so the record
must pick one answer and it picks the flattering one.

It is not confined to joints. Prosthetic heart valves and conduits are the same
shape and `congenital-heart-disease` already carries it — a child's conduit is
outgrown and replaced repeatedly, and the record's own `holes` say the Fontan is
a human experiment in its sixth decade with nobody knowing how it ends. An
intraocular lens genuinely does not have this problem, which is why `cataract` is
the clean case and the others are not.

Candidates, in order of how much they'd cost to build:

- a **`durability`** field on the intervention — expected service life, or
  `indefinite` — which makes the `cataract`/`osteoarthritis` difference visible
  without touching the ladder;
- `toll` gaining the revision explicitly, since a second operation twenty years
  later is a price the first one charged and the schema currently files it
  nowhere;
- and the honest but expensive one: **accepting that `intervention` is not a
  property of the disease alone.** It is already partly a property of the
  stratum (`strata[].intervention` exists). This says it can also be a property
  of the patient.

---

## 203. The treatment window can have a lower bound, and `window` is built entirely for lateness · **open**
*Forced by:* `osteoarthritis`.

Every `window` in this corpus is an upper bound. Minutes for stroke, hours for
sepsis and dengue, days for noma and smallpox, a decade for a colorectal adenoma,
twenty years for smoking cessation in COPD. The field's own key is
**`closes_on`**, `caught_in_time` asks what fraction were reached **before** it
shut, and the derived flag reports *the toll is the price of **missing** it.*

**Osteoarthritis is the mirror.** You are not offered a joint replacement when
your knee starts to hurt. You are offered it when the joint is destroyed, the
pain is constant, and everything else has failed — and **that is not rationing
and not a failure. It is correct advice**, because of #202: the implant has a
service life, so every year of waiting is a revision avoided, and operating early
commits a fifty-year-old to two more operations.

So the window **opens** late, on purpose, and never closes. The patient's
suffering during those years is real, is most of the record's disability, and is
the `residue` — muscle and conditioning that do not come back.

**And the register's own machinery reports it wrongly, which is the evidence.**
`window_toll_link` fires on this record and says:

> the toll is the price of missing it → `diagnosis` is the cheap lever

Every clause is false here. Nothing was missed; the diagnosis is easy, early,
radiographic and usually made years before treatment; and the toll is the price
of **having** the treatment, not of being late for it. **This is the third
false-reason flag in the register's history** — after noma's `overtreatment_risk`
(#61) and COPD's `window_toll_link` (#97) — and all three fired because a derived
sentence assumed a shape the record does not have.

**Distinguish it from #199 precisely**, because they look like the same gap and
they are mirrored. In `congenital-heart-disease`, the window closes by
**inverting**: after Eisenmenger physiology is established, closing the defect
kills, so an intervention that was correct becomes fatal. Here the intervention
is **harmful before a point rather than after one** — the same inversion, run
backwards. Together they say the field is not a deadline at all: it is a
**window** in the literal sense, with two edges, and the schema models one.

Where else the lower bound already operates, unnamed:

| record | why you are made to wait |
|---|---|
| **osteoarthritis** | the prosthesis has a service life |
| **chronic-kidney-disease** | dialysis is started at a threshold, not at diagnosis |
| **hepatitis-b** | treatment is deferred in the immune-tolerant phase |
| **prostate-cancer** | active surveillance — treating early is the harm |
| **crohns**, **rheumatoid-arthritis** | *the opposite*, and it is a real finding: both moved to treating **earlier**, and RA's "window of opportunity" is a genuine upper bound |

**That last row is why this must be a field rather than a note.** Two diseases in
the same clinic, one where waiting is correct and one where waiting is the
error, and the register currently cannot tell them apart — it has one field, and
it means "late".

The cheap version is a **`window.direction`** of `late` | `early` | `both`, which
would also stop the derived sentence lying. The honest version is two bounds and
a reason for each.

---

**Strengthened by `osteoarthritis`, not new:**

- **#34 (heterogeneity within a patient) — THIRD RECORD, AND THE THRESHOLD WAS
  TWO.** In `msmds` capability varies by **organ** inside one patient; in `heds`
  mechanism confidence varies by **system**; here **capability varies by joint**.
  A hip can be replaced and a finger cannot, in the same seventy-year-old, on the
  same afternoon. Two of the four strata rate `curable` and two rate `unsolved`,
  and forty percent of the prevalence is in the half that has nothing.
- **#89 / #98 (what counts as benefit) — the inverse case, and it is instructive.**
  #98 complained that symptom relief is invisible to a schema whose only notion of
  benefit is course alteration. Osteoarthritis says the same thing from the other
  end: **no drug has ever altered this disease's course, and an operation that
  alters nothing about the disease is one of the most valuable things medicine
  does.** The register rates it `curative` and is right to; the pathophysiology is
  untouched.
- **#193 / #198 (mechanism is not on the path to the treatment) — the strongest
  case yet, and from the far end.** CF, SMA and DMD showed that the order of gene
  discovery is inverse to therapeutic success. Here the mechanism is still
  `partial` after a century and the intervention is excellent, and it arrived in
  1962 from **tribology** — a small femoral head, high-density polyethylene, bone
  cement. Nobody understood osteoarthritis better in 1962 than in 1952. An
  engineer worked out how to build a bearing that survives inside a person.
- **#164 (the register holds interventions, not the capabilities that produce and
  evaluate them) — in its positive form, and it is the best example in the
  corpus.** The Swedish knee and hip registries from 1979 improved outcomes with
  no new science, no new device and no trial: when you can see which implants
  fail, the bad ones stop being used. They also caught the metal-on-metal
  resurfacing disaster that pre-market trials had missed. **A post-market
  surveillance system that actually works is a capability, it is the reason this
  record's efficacy moved twice, and there is no field for it.**
- **#182 (the magnitude is deaths) — with a twist `hearing-loss` did not have.**
  There the zero is close to literal. **Here it is an accounting choice**: NSAID
  gastrointestinal bleeding kills, opioids prescribed for joint pain kill, and
  osteoarthritis is a documented contributor to cardiovascular mortality through
  enforced inactivity. Every one of those deaths is attributed to another cause,
  and the record that generated them reads `0`.
- **#160 (the flat list) — the arrow is quantified and the schema still cannot
  draw it.** The largest modifiable cause of the largest stratum is `obesity`;
  roughly half of ACL and meniscal injuries become radiographic knee
  osteoarthritis within twenty years; and **the most promising thing to happen to
  osteoarthritis symptoms in decades is a drug for a different disease** — a
  randomised trial of semaglutide reported pain reduction well beyond what
  analgesics achieve. A funder reading this record alone would not learn that the
  best available lever sits in a different file.
- **#189 (the treatment threshold is set by capacity, not by the patient) — a
  second cause for the same effect.** There the threshold moved with rationing.
  Here it moves with **hardware**, and the two stack: a publicly funded system
  with a year-long waiting list adds capacity-delay on top of a clinically
  correct hardware-delay, and the patient cannot tell which one is costing them
  their quadriceps.
- **#90 / #119 (the threshold is a choice somebody made) — and it moved
  recently.** This record's prevalence rose by something like seventy percent in a
  single GBD revision, from around 344 million to around 595 million, because the
  case definition was broadened. No biology changed. **The largest single-revision
  move in any burden figure in this corpus**, and the register stores the new
  number with a `src: recall`.
- **#48 (the register cannot rank by preventable burden) — its most embarrassing
  instance, because the data exist.** The national joint registries are among the
  best outcome datasets in medicine, they are public, they cover millions of
  procedures with implant, indication, surgeon and revision, and not one of this
  record's scalars cites them.

---

## 204. `access` is one number for a regimen with more than one part, and the parts are not substitutes · **open**
*Forced by:* `asthma`.

Asthma is treated with two drugs that do different jobs. The **reliever** — a
short-acting beta-agonist — opens the airway now. The **preventer** — an inhaled
corticosteroid, off patent since the 1980s — suppresses the inflammation
underneath and is what prevents deaths.

Medicine availability surveys in low- and middle-income countries find the
reliever commonly stocked and **the preventer frequently absent or
unaffordable.** So the world's default asthma treatment, in the countries
carrying essentially all of the 455,000 annual deaths, is reliever monotherapy.

**In 2019 the Global Initiative for Asthma abolished that regimen.** After nearly
fifty years of recommending as-needed reliever alone for mild asthma, the
recommendation was withdrawn outright: no adult or adolescent should be treated
with a short-acting beta-agonist alone. The evidence was that three or more
reliever canisters a year is associated with death — **because the drug works.**
It relieves the symptom that would otherwise have driven escalation, and the
inflammation proceeds unopposed underneath a patient who feels fine.

**So half the regimen is not half the benefit. It is a hazard**, and the register
computes `reach = efficacy × access` with a single `access` fraction that says
the opposite.

This is not the gaps already logged, and the distinction is worth being exact
about:

| gap | its claim | why asthma is different |
|---|---|---|
| **#122** | you reached care, not the *right* care | both drugs are the right care; one alone is not |
| **#174** (`chronic-kidney-disease`) | you got the **worse tier** of one intervention | dialysis is worse than transplant; salbutamol is not a worse budesonide, it is a different job |
| **#108** (`measles`) | **population** coverage has a threshold | this is inside one patient, on one day |
| **#7**, **#15** | high `access` can be bad news | those are low-value care; this is high-value care, half-delivered |

**The general form is complementarity.** Where an intervention is a combination
whose components are not substitutes, partial delivery has a sign that depends on
*which* part arrived, and the corpus already carries the other instances without
naming them:

- **tuberculosis** and **hiv** — monotherapy does not half-treat, it manufactures
  resistance, and both records say so in prose;
- **sepsis** — antibiotics without source control;
- **cystic-fibrosis** — a modulator without the airway clearance around it;
- **congenital-heart-disease** and **hearing-loss** — a screen delivered without
  the service behind it, which both records call out and which is the same shape
  one level up.

Candidates:

- **`access` becomes a list** — per-component fractions, which is honest and
  makes every existing record's single number a special case;
- or a minimal **`access.components`** annotation naming any component whose
  absence changes the sign, so a record can say *the dangerous partial delivery
  is this one*;
- and either way, **`reach` needs to stop being a product** for these records,
  because multiplying by the availability of the harmful half flatters it.

Note what the 2019 guideline change demonstrates about the register's own
`moved` field, because it is the encouraging half of this gap: **no drug changed.
Both were decades old.** What changed was the recognition that one of them, given
by itself, is worse than nothing would have been — since nothing would not have
hidden the deterioration. A `moved` entry with no new science in it is the
cheapest kind there is, and this register should be able to find more of them.

---

## 205. A disease can end on its own, and nothing in the register records it · **open**
*Forced by:* `asthma`.

Asthma is the commonest chronic disease of childhood and **a large fraction of
the children who have it stop having it.** Most preschool wheezers do not become
asthmatic adults; a substantial share of school-age asthma is symptom-free by the
mid-twenties. Relapse happens, and lung function may not be normal even in those
who remit — but the symptomatic disease ends, on its own, in a great many
people, and nobody knows why.

**There is no field for this anywhere in the schema**, and the search is not
close: no `remission`, no spontaneous resolution, nothing. The register has
`intervention` (what we can do), `prevention` (stopping it starting) and
`window` (a clock on treating it). All three assume the disease persists unless
acted upon.

Four things break:

- **`intervention: suppressive` describes a lifelong treatment for a disease many
  patients will stop having.** The rating is correct for the disease as it
  presents and misleading about what a given child faces.
- **Treated remission and natural remission are indistinguishable**, so the
  efficacy of long-term childhood treatment is uninterpretable at the individual
  level — and this is the same structural problem as the arthroscopy story in
  `osteoarthritis`, where a treatment that does nothing looks effective because
  the condition improves anyway.
- **`toll` is charged to people who did not need the treatment.** A centimetre of
  final adult height, and years of a daily steroid, taken by children whose
  disease was going to end regardless — and no way to say which ones.
- **The corpus's implicit theory of disease is monotone.** Diseases in this
  register get worse or get treated. `residue` and `toll` are both permanent by
  construction; `#176` had to be written to record that some damage *regresses*
  when the cause is removed. **This is that observation one level up: the entity
  itself can go away.**

It is not confined to asthma, and the corpus already holds the cases:

| record | what remits, and how often |
|---|---|
| **asthma** | symptomatic disease in a large share of children |
| **hepatitis-b** | the great majority of adult acute infections clear without treatment |
| **epilepsy** | several childhood syndromes remit reliably enough to be named for it |
| **crohns**, **rheumatoid-arthritis** | drug-free remission in a minority, and nobody can predict who |
| **obesity**, **type-2-diabetes** | remission is a stated treatment goal, which is the opposite case — *induced* remission, and it has no field either |

**That last row is why this should be a field rather than a footnote.** The
register can already say a disease is *cured* by a finite intervention
(`curative`) and *controlled* by a continuing one (`suppressive`). It cannot say
a disease **stopped** — whether by itself, or as the intended endpoint of a
treatment that is then withdrawn. Type-2 diabetes remission programmes and
drug-free remission in inflammatory disease are both aimed squarely at that
state, and it does not exist in the schema.

The cheap version is a **`remission`** block — fraction, typical timing, and
whether it is spontaneous, induced, or both. The valuable version is what it
would force: **`prognostic` measurement acquiring the question "will this end by
itself"**, which is the question every parent of an asthmatic child actually
asks, and which nothing currently answers.

And it is a research direction rather than only a schema note. **Whatever ends
asthma in a large fraction of children is the most direct route to a cure anyone
could ask for**, it happens at scale, it is observable, and the field has no
mechanism for it.

---

**Strengthened by `asthma`, not new:**

- **#193 / #198 (mechanism is not on the path to the treatment) — and this is the
  designated pair, so read them together.** `copd` rates `mechanism: established`
  and `intervention: symptomatic`: the mechanism is known and nothing alters the
  course. **Asthma rates `mechanism: partial` and `intervention: suppressive`** —
  a whole stratum has no identified mechanism, and it is nonetheless one of the
  best-controlled chronic diseases there is. Same organ, same symptom, same
  inhaler cabinet, opposite ratings on both axes. **Two records queued explicitly
  as each other's contrast, and the contrast is invisible to the schema**
  (gaps.md #160).
- **#48 (the register cannot rank by preventable burden) — its cleanest case.**
  455,000 deaths a year, the great majority preventable by a drug invented in
  1972 that is off patent and costs a few dollars a month to make. Nothing in this
  corpus has a shorter distance between what exists and what is delivered.
- **#98 (symptom relief is not a benefit anywhere in this schema) — the reply
  from the other side of the ward.** #98 was forced by COPD, where relieving
  breathlessness is a large benefit the schema cannot see. Asthma says the
  opposite can also be true: **relieving the symptom without treating the disease
  is associated with death**, and the 2019 guideline change is a field acting on
  exactly that. So symptom relief is not automatically a benefit *or* automatically
  not one — **it depends on whether relieving it removes the signal that would have
  triggered escalation**, and that is a property of the pair, not of the symptom.
- **#96 (a window can close before there is anything to diagnose) — seen from the
  other end, and this closes a loop.** COPD's gap records that roughly half of
  COPD comes from never reaching a normal peak of lung function, during a window
  running from gestation to about twenty-five, with nothing to diagnose and no
  patient. **Childhood asthma is one of the things that happens during that
  window** — persistent poorly controlled asthma lowers attained lung function
  permanently, and some of those children meet the spirometric definition of COPD
  in middle age without ever smoking. So COPD's un-diagnosable window contains a
  diagnosable, treatable, cheap-to-treat disease, **and the benefit of treating it
  arrives forty years later in a different record.**
- **#90 / #119 (the threshold is a choice somebody made) — with the variable
  changed from where to when.** COPD's boundary is a fixed FEV1/FVC ratio known to
  overdiagnose the old. Asthma's confirmatory tests are all measures of
  *variability*, so they are normal between attacks and normal on treatment —
  **the test is abolished by the disease being quiet and by the treatment
  working.** Roughly a third of adults carrying a physician diagnosis fail
  objective re-testing, while most asthma elsewhere is never diagnosed. One
  entity, overdiagnosed and underdiagnosed simultaneously, and the register has one
  `diagnostic` rating.
- **#78 (externalities run both ways) — a third sign, and it has no address in
  this register at all.** Pressurised metered-dose inhalers use propellants with a
  high global warming potential and are a measurable share of some health systems'
  carbon footprint. #78's externalities land on other *entities* — resistant
  organisms, vaccine confidence, child mortality. **This one lands on nobody in
  the corpus**, `scale` is denominated in money, and the caveat is essential: the
  answer is not fewer inhalers, and better-controlled asthma uses fewer relievers,
  so the clinical and environmental fixes point the same way.
- **#161 (the treatment addresses what kills you, not what bothers you) — and
  asthma supplies the best *solution* the register has seen to it.** The preventer
  cannot be felt working and the reliever can, so patients rationally conclude the
  reliever is the medicine. The fix was not education: it was **putting both drugs
  in one device**, so reaching for relief delivers the preventer. A design solution
  to an adherence problem, and the model for the whole class.
- **#4 / #34 (heterogeneous entities, heterogeneity within a patient).** Asthma's
  own field increasingly writes *"the asthmas"*, and the type-2-high / type-2-low
  split decides whether a patient has four working biologics or none. **A record
  where 4% of patients rate `symptomatic` and 96% rate `suppressive`**, and where
  a patient can cross the boundary by losing weight or stopping smoking — which
  is a phenotype that moves, and #34 has no such case yet.

---

## 206. The reference population that defined "normal" can have had the disease · **open**
*Forced by:* `anaemia`.

A "normal range" is made by measuring a population presumed healthy and taking
the central part of the distribution. That procedure has an assumption inside it
that is almost never checked: **the reference population did not have the thing
being defined.**

Anaemia is the case where the assumption is doubtful and the stakes are two
billion people. The haemoglobin thresholds in near-universal use were derived
decades ago from reference samples that were small, geographically narrow, and
**not screened for iron deficiency** — which is the commonest nutritional
disorder on earth, concentrated overwhelmingly in women of reproductive age.
**If the reference women were iron-deficient, the threshold encodes the
deficiency as normal**, and the disease was defined by measuring people who had
it. WHO revised the values in 2024 after re-analysing healthier reference
populations.

**The sex difference is the sharpest form of it.** The accepted cut-off for women
sits roughly a gram per decilitre below the male one, and the standard
explanation is menstrual loss and hormonal differences in erythropoiesis. The
counter-position is that some of the gap is the artefact above — a lower "normal"
learned from a population whose iron stores were depleted by exactly the process
being normalised. **Nordstern takes no position and records that this is an
argument about the diagnostic status of a quarter of humanity.**

This is a **third distinct way a threshold goes wrong**, and the register now has
all three:

| gap | what is wrong with the number |
|---|---|
| **#90** (`ischaemic-heart-disease`) | a committee **chose** it, and could have chosen otherwise |
| **#119** | it **drifted** — no number, no committee, no announcement |
| **#206** (`anaemia`) | it was **measured from people who had the disease** |

The first two are decisions. **This one is a methodological defect**, and it is
falsifiable: re-derive the range from a population screened for the deficiency
and see whether the number moves. That has now been done once, and it moved.

Where else it should be checked, because anaemia will not be alone:

- **vitamin D and B12 cut-offs**, derived from populations with widespread
  insufficiency, and disputed for the same reason;
- **ferritin's lower limit**, which is the same problem one test deeper;
- **`hypertension`** and **`type-2-diabetes`**, where the reference populations
  are contemporary and increasingly unhealthy — a "normal" blood pressure or
  fasting glucose learned from a population with rising `obesity` drifts *upward*,
  which is #119's mechanism with #206's cause;
- **spirometry reference equations**, which `copd` already flags for a related
  reason.

**The consequence for this register is concrete.** `check.py` records prevalence
as a scalar with a `src`. It has no way to record that the scalar is a count of
people on one side of a line whose derivation is disputed — and for the two
largest prevalence figures in the corpus, `anaemia` and `hypertension`, that is
the single most important fact about the number.

---

## 207. The intervention can reach a population that contains no patients · **open**
*Forced by:* `anaemia`.

The largest single intervention in this record is **adding iron to flour.**

It costs a fraction of a cent per person per year. It requires no clinical
encounter, no diagnosis, no prescription and no adherence. It reaches people who
do not know they received it, most of whom do not have the disease, and it works.
Mandatory staple fortification is among the highest-return interventions in the
history of public health.

**`access` cannot express any of that**, and the reason is definitional: it is
*the fraction of patients who can obtain the treatment*, and here there are no
patients. The denominator is everyone who eats bread. The register scored this
record `access: 0.45` on the basis of who gets diagnosed and treated, which
describes the second-best intervention while being silent about the best one.

**And it collapses a distinction the schema treats as two separate axes.** A
person who is already anaemic and starts eating fortified flour is being
**treated**. A person who is not is being **prevented**. It is the same act, the
same cent, and the same loaf, and `intervention` and `prevention` are different
fields with different vocabularies. Fortification is both at once, and delivered
without anyone knowing which they received.

The corpus has more of these than it looks, once named:

| record | the intervention with no patient |
|---|---|
| **anaemia** | iron in flour; **delayed cord clamping**, which is free and happens at every birth |
| **pku** | newborn screening — but it produces a patient, which is the contrast |
| **cirrhosis**, **liver-cancer** | hepatitis B birth-dose vaccination |
| **noma**, **diarrhoeal-disease** | water and sanitation |
| **osteoarthritis** | neuromuscular training in young athletes, delivered by sports coaches |
| **asthma** | air quality regulation |

**Distinguish it from the two neighbours carefully.** #109 says prevention has no
`efficacy` and no `access` fields at all — true, and this is why one of them would
be hard to write. #200 (`hearing-loss`) says the remedy can be in the
environment rather than applied to the patient — captioning, hearing loops. **This
is the third position: the remedy IS applied to bodies, one at a time, and the
bodies are not patients and are not counted.**

What it argues for:

- **a population-delivered intervention needs its own reach**, denominated in
  *coverage of the vehicle* — what share of milled flour in a country is
  fortified — rather than in fraction-of-patients;
- and that number is **already collected by somebody**, in food regulation rather
  than in health, which is the same lesson `osteoarthritis` learned from the joint
  registries: the measurement exists and lives outside medicine.

**The reason it matters for ranking and not only for tidiness**: a funder reading
`anaemia` sees `access: 0.45` and buys iron tablets and diagnostic tests. The
intervention with the highest return in the record is a **line in a food
standard**, and no field in this register points at it.

---

**Strengthened by `anaemia`, not new:**

- **#39 (a final common pathway has no word) — FOURTH RECORD, AND THE EXTREME
  CASE. It was marked BUILD IT two records ago and this settles it.** POTS's four
  mechanisms are unnamed pathophysiologies. **Anaemia's causes are other rows in
  this register** — `sickle-cell`, `malaria`, `soil-transmitted-helminths`,
  `schistosomiasis`, `chronic-kidney-disease`, `colorectal-cancer`,
  `h-pylori-ulcer`, `tuberculosis`, `hiv` — each already rated, with its own
  capability, access and blockers. So the register now contains a record composed
  of its other records, **and its 1.92 billion double-counts most of the corpus in
  a way no better data can fix.** #179 noted the same for `hypertension`'s deaths;
  this is the prevalence version and it is larger.
- **#157 (an intervention's effect has a sign, and the sign flips with the
  setting) — its cleanest instance, and the flip is fatal.** A trial of routine
  iron and folic acid supplementation in children in a malaria-endemic area was
  stopped early for **excess serious adverse events and deaths**, and global
  policy changed: no universal iron supplementation where malaria transmission is
  intense without malaria control alongside. **A cheap tablet that prevents
  disability in one setting killed children in another, and the condition is
  another record in this register.** No field holds a conditional of that form.
- **#175 (the instrument encodes a correction that changes who gets treated) — a
  different mechanism, the same direction of effect.** Ferritin is the test for
  iron deficiency and ferritin is an acute-phase reactant, so infection and
  inflammation raise it. **In the populations with the most anaemia — endemic
  malaria, helminths, tuberculosis — a normal ferritin does not exclude iron
  deficiency**, and the error runs toward undertreating the poorest. Not a
  population correction written into the device, but a confounder co-located with
  the disease, arriving at the same place.
- **#182 (the magnitude is deaths) — a THIRD kind of zero, and the register now
  has all three.** `hearing-loss`'s zero is close to literal. `osteoarthritis`'s is
  an attribution artefact — the NSAID bleeds and the inactivity deaths are real
  and filed elsewhere. **Anaemia's is multiplicative**: it makes other records'
  events lethal. An anaemic woman dies at a lower blood loss and the death is
  correctly `maternal-haemorrhage`. Three records, three zeros, three different
  reasons, one field.
- **#193 / #198 (mechanism is not on the path to the treatment) — and this is the
  oldest example in the corpus by four decades.** Pernicious anaemia was
  universally fatal and was cured in 1926 by feeding people large quantities of
  liver. **Vitamin B12 was not isolated until 1948.** A complete cure preceded
  identification of the molecule by twenty-two years.
- **#161 (the treatment addresses what kills you, not what bothers you) — with the
  timing inverted, and a mechanistic fix.** Oral iron's side effects begin
  immediately and its benefit arrives in weeks, so the patient's own evidence says
  the tablet is making them worse. **And here mechanism did pay**: the hepcidin
  discovery produced alternate-day dosing, which is better absorbed and better
  tolerated than the daily regimen used for decades — a free fix, and a small
  honest point in favour of mechanism after several records arguing the other way.
- **#202 (no axis is a function of age) — a second record, one after the first.**
  The identical haemoglobin value is fully reversible fatigue at thirty and a
  permanent developmental deficit at eighteen months. `osteoarthritis` said the
  same about an operation. **Two consecutive records where the correct rating
  depends on the patient's age and the schema cannot ask.**
- **#48 (the register cannot rank by preventable burden) — and this record supplies
  the counterweight the gap needs.** Anaemia looks like the highest-return line in
  the corpus: two billion people, a treatment costing pennies, an enormous
  disability burden. **The `knowledge` blocker exists to say that most of that
  case is association rather than trial evidence** — supplementation trials on
  cognitive and developmental outcomes have been inconsistent, and the strongest
  evidence sits at the severe end, which is not where most of the two billion are.
  A ranking built on attributed burden would put this first on numbers that the
  record itself flags as unconfirmed.

---

## 208. The entity can BE the residue — the disease is over and the patient is not · **open**
*Forced by:* `cerebral-palsy`, the ninety-ninth record, and it sits exactly
between two gaps that each got half of it.

Cerebral palsy is **defined as non-progressive**. A lesion occurred once, in a
developing brain, before or around birth, and it is finished. It will not spread,
worsen or recur. Everything the person lives with for the next seventy years is
consequence.

The register has two gaps about permanent damage and this is neither:

| gap | its case | why cerebral palsy is not it |
|---|---|---|
| **#97** (`copd`) | the permanent damage **is the disease still doing it**, so `residue` cannot hold it | here the disease is not doing anything. It finished. |
| **#60** (`lymphatic-filariasis`) | the residue can be **the treatable part**, and `residue` has no capability of its own | true here, and understated: the residue is not *a* treatable part, it is **the entire record** |

**#60 asked for a second forcing record before making the change. This is it, and
it is the extreme form**: not a record with a treatable sequela beside a treatable
disease, but a record where the sequela is all there is.

What breaks, in order of how badly:

- **`mechanism: established` describes an event in the past.** It is an accurate
  and complete account of a hypoxic-ischaemic injury or a preterm white-matter
  lesion, and no intervention can reach it, because the neurons died before the
  patient could speak. The rating is true and carries none of its usual
  implication — that understanding is a route in.
- **`intervention` can never address the entity.** Everything on offer works
  around the lesion, and much of what works best is not medical at all: a
  communication device, powered mobility, seating, inclusive education, a kerb
  cut. `intervention: symptomatic` is correct about the entity and close to
  slander about the person.
- **`window` has no upper bound to close.** The prevention window shut at birth;
  the second window — peak neuroplasticity in the first two years — governs *how
  much function is built around a fixed lesion*, which is a different kind of
  deadline than anything else in the corpus.
- **And the derived verdict is the sharpest demonstration.** The record lands in
  `engineering problem` — *understood, and nothing can be done* — and in the
  generated section headed **"A permanent toll while the course is unchanged."**
  Both derivations are internally correct. **Both are among the most misleading
  sentences this register can produce**, because the course was over before the
  patient was a patient, and "nothing can be done" is false about a life in which
  a great deal can be done. This is the fourth time a derived verdict has been
  right about the entity and wrong about the person — after ischaemic heart
  disease and stroke (#89), and COPD (#98).

**The register should be able to mark an entity as `completed`**: a record whose
subject is a finished event, so that `mechanism` is read as history rather than
as a target, `intervention` is read as scoped to consequences, and the quadrant
derivation stops answering a question nobody asked. The corpus has more of these
than it looks:

| record | the finished event | what is lived with |
|---|---|---|
| **cerebral-palsy** | a perinatal brain injury | everything |
| **stroke** | an infarct, minutes long | the deficit, for decades |
| **noma** | an acute gangrene, over in weeks | a face |
| **amr-infection**, **sepsis** | an episode that resolved | amputation, dialysis, weakness |
| **taeniasis-cysticercosis** | cysts, killed | epilepsy |
| **trachoma** | an infection cleared | a scarred cornea |

**Note the pattern in that column**: several are already among the register's
`disease-residue` records, which means the machinery has been half-detecting this
for a long time without a name for it. The difference cerebral palsy makes is
that in every other row there was a period during which the person had a disease
and could have been treated for it. **Here there never was one.**

The honest version of the change is #60's: `residue` mirrors the axes beside it,
gaining its own `intervention`, `efficacy` and `access`. **For this record that
would move the entire content of the file into the residue block**, which is the
clearest possible argument that the schema's centre of gravity is in the wrong
place for an entire class of entity.

---

## 209. The disease can corrupt the measurement of the PERSON, and every measurement field is about the disease · **open**
*Forced by:* `cerebral-palsy`.

The `measurement` block asks three questions and they are all about the disease:
is it there (`diagnostic`), what will it do (`prognostic`), will this treatment
work (`predictive`). Gap #45 proposed a fourth — did the treatment work.

**Cerebral palsy forces a fifth, and it is of a different kind.** Roughly a
quarter of people with cerebral palsy have severe speech impairment, and many
more have unreliable hand control. **Standard cognitive assessment requires
speech or pointing.** So intelligence is measured with an instrument that
requires the exact capacities the disease removed, and it is systematically
underestimated in precisely the people who cannot demonstrate it.

The consequences are not academic and they compound for a lifetime: educational
placement, what a teacher expects, whether anyone funds a communication device,
whether decisions are made *with* the person or *about* them. **And the
provision of communication devices is in several systems contingent on
demonstrating cognitive ability — using the speech the device would supply**,
which is the failure written into a procurement rule.

**Pain is the same failure in a second domain.** Pain is measured by self-report.
So it is under-recorded in exactly the population most likely to be in it, and
surveys of adults with cerebral palsy find chronic pain in a majority, most of it
inadequately treated.

**This is not #175 and the distinction matters.** #175 (`obesity`, `hypertension`,
pulse oximetry) is about an instrument encoding a *population correction* that
changes who gets treated — the instrument measures the right variable with a
biased calibration. **Here the instrument measures the right variable and the
patient cannot operate it.** The reading is not miscalibrated; it is unobtainable,
and an unobtainable reading is recorded as a low one.

Nor is it #29 or #153. Those are about the register's flags and definitions.
**This is about the patient being mis-described by medicine**, which is upstream
of anything the register stores.

The corpus already holds the other instances, and one of them is this register's
own history:

| record | what cannot be measured, and why |
|---|---|
| **cerebral-palsy** | cognition, without speech or pointing; pain, without report |
| **hearing-loss** | **deaf children were classified as intellectually disabled for a century**, because the test was spoken — which is the documented basis of the contestation in #201 |
| **stroke** | cognition and pain in aphasia; the deficit assessed through the deficit |
| **alzheimers** | pain in advanced dementia, which is a large and well-documented under-treatment |
| **me-cfs** | function measured by tests whose performance the disease alters, and repeat testing is itself harmful |

**That second row is the argument for building this rather than noting it.** The
register already carries a record in which this exact failure — testing a
population with an instrument their impairment defeats — produced a century of
harm, and it is filed there as history in a `toll` block. **A field would have
caught it as a live property of the record instead of as a retrospective.**

What it argues for: a `measurement` entry for **assessability** — whether the
person can be measured at all, in cognition, in symptom report, in function — with
the standard note that a test that cannot be run reports `skipped`, never a low
score. That is Sperrwerk's rule, and it applies here exactly: **an unobtainable
measurement recorded as a poor one is the same error as a check that cannot run
reporting `ok`.**

---

**Strengthened by `cerebral-palsy`, not new:**

- **#157 (an intervention's effect has a sign, and the sign flips with the
  setting) — SECOND INSTANCE IN TWO RECORDS, and this one is a standard of care
  rather than a tablet.** Therapeutic hypothermia for neonatal encephalopathy
  reduces death and disability in high-income units and became standard through
  the 2000s. **A large randomised trial in South Asia found no benefit and
  increased mortality**, and the conclusion drawn was that it should not be used
  in low-resource settings. After `anaemia`'s iron-in-malaria result one record
  earlier, this is no longer a curiosity: **two consecutive records in which the
  register's single `efficacy` number covers a setting where the intervention
  helps and a setting where it kills.**
- **#89 / #98 (the derived verdict is right about the entity and wrong about the
  person) — the fourth record, and the one where the middle column does not
  help.** Ischaemic heart disease and stroke were rescued by adding
  `disease-modifying` as its own band. COPD earned its harsh verdict. **Cerebral
  palsy earns it too, on the entity, and it is still wrong** — because the benefit
  is not course alteration or symptom relief but *function and participation*,
  which is a third kind of benefit the schema has no name for.
- **#200 (the remedy can be in the environment) — the record where it decides the
  outcome outright.** `hearing-loss` forced it and captioning was the example.
  **Motor impairment is the impairment that built environments most directly
  convert into disability**: the same body produces a very different life in two
  countries, depending on transport, buildings, education, personal assistance and
  employment law. A powered wheelchair is medicine's contribution and a kerb cut
  is not, and without the second the first buys much less.
- **#66 (`preventable` reads both axes) — and it applies to whole records, which
  is not fine-grained enough.** **Kernicterus is fully preventable** — a bilirubin
  measurement and a lamp — and it produced a distinctive dyskinetic cerebral palsy
  that has effectively vanished from high-income countries while remaining a
  leading cause elsewhere. **One route into this record is preventable and the
  rest is not**, and the capability value cannot say so. This is #109's neighbour:
  there, `delivery` was withheld rather than guessed; here, a fully preventable
  route is invisible because the record as a whole is not.
- **#184 (`moved` has no convention for measurement) — and this record exercises
  it deliberately.** The single most consequential change in cerebral palsy this
  century was **moving diagnosis from about nineteen months to three to six
  months**, using video of an infant's spontaneous movements and a bedside
  neurological examination. It required no new technology, and it moves the
  intervention inside the neuroplasticity window — which is worth as much as a
  treatment. The `moved` entry is written on a `measurement` axis that `check.py`
  does not validate, so the register accepts it and can do nothing with it.
- **#160 (the register is a flat list) — one child, three files.** Untreated
  neonatal jaundice belongs to `neonatal-conditions`; the deafness it causes
  belongs to `hearing-loss`; the movement disorder is here. Same infant, same
  missing lamp, three records and no edge between them.
- **#147 (the disease is a byproduct of capability) — in its gentlest and most
  uncomfortable form.** Neonatal intensive care saves extremely preterm infants who
  would previously have died, and a fraction of the survivors have cerebral palsy.
  **Improving survival and reducing prevalence pull against each other**, this
  record's incidence has barely moved in fifty years partly for that reason, and
  no field can express a prevention that is also a cause.
- **#171 (`ongoing` measures how much, not what kind) — and the largest component
  here is not billed.** Care is delivered overwhelmingly by families, commonly by
  a parent who left paid employment. Neither `ongoing` nor `scale` has any way to
  hold decades of unpaid labour, and it is plausibly the largest single cost in
  the record.

---

## 210. The treatment exists, is cheap, is stocked — and is not prescribed. No blocker kind is the clinician · **open**
*Forced by:* `heart-failure`, and confirmed from the other direction by
`osteoporosis` in the same pass.

Four drug classes independently reduce mortality in heart failure with reduced
ejection fraction. Most are off patent. All are stocked and reimbursed across
every high-income health system. **Registries consistently find that only a small
percentage of eligible patients are on all of them at target dose**, and that a
large share of those prescribed sit on a fraction of the trial dose and are never
up-titrated.

Not cost. Not supply. Not knowledge — the guidelines are unambiguous and everyone
has read them. **The prescription is not written.**

The register's blocker vocabulary has twelve kinds and none of them is this:

| kind | why it does not fit |
|---|---|
| `adherence` | that is the **patient** not taking a prescribed drug. Here there was no prescription. |
| `cost` | not binding where most of the shortfall is |
| `logistics` | closest, and describes a **missing service** rather than a decision not made |
| `policy` | where the record files it, and it is an approximation |
| `evidence-incomplete` | the evidence is as good as evidence gets |
| `no-sponsor` | there is nothing to sponsor; the drugs are generic |

**The causes are known and none is a shortage.** Titration takes repeated visits
with blood tests that nobody is paid to do. An expected, transient rise in
creatinine or potassium causes the drug to be stopped. Responsibility is diffuse
between hospital and primary care, so each assumes the other will escalate. The
patient feels well. And **the post-discharge window, when initiation works best
and the patient is present and willing, is spent arranging follow-up.**

**`osteoporosis` is the same effect with the opposite engine, which is what makes
this a kind rather than an anecdote.** There the therapy is not merely omitted —
**it is actively stopped**, by prescribers and patients both, and that record has
two population-scale retreats eight years apart. Heart failure is inertia;
osteoporosis is fear. Both produce a treatment that works and is not given, and
neither has a home in this schema.

Once named, the corpus is full of it:

| record | what is not prescribed |
|---|---|
| **heart-failure** | all four pillars, at dose |
| **osteoporosis** | anything at all, after a fragility fracture |
| **atrial-fibrillation** | anticoagulation, withheld for fear of bleeding |
| **chronic-kidney-disease** | SGLT2 inhibitors and referral, both late |
| **asthma** | the preventer, where guidelines abolished reliever-alone in 2019 |
| **copd** | pulmonary rehabilitation, reaching under a tenth of eligible patients |

**Propose a `practice` blocker kind** — the intervention exists and is available
and the clinical system does not deliver it — with the standard discipline that
its `who_could` is `health-system` and `payer` rather than `academic` or
`sponsor`, because what fixes it is service design: in-hospital initiation,
nurse- or pharmacist-led titration, audit with feedback, and default-on
prescribing. All are tested and all work.

**And it changes what the register recommends.** A funder reading `heart-failure`
sees `access: 0.30` and buys drugs into a system that already has them. The
binding constraint is that nobody is paid to titrate.

---

## 211. The identifier says it is a disease and the burden dataset says it is a sequela · **open**
*Forced by:* `heart-failure`, and it applies retroactively to `anaemia`.

Nordstern borrows identity from **Mondo** — *"disease identifiers are borrowed,
never minted"* — and magnitude from **GBD**, whose cause hierarchy is where every
prevalence and deaths figure in this corpus ultimately comes from.

**For heart failure the two disagree about what kind of thing it is.** Mondo
issues `MONDO:0005252`. GBD models heart failure as an **impairment** — a sequela
of underlying causes, not a cause of death — so the deaths are distributed to
`ischaemic-heart-disease`, `hypertension`, `rheumatic-heart-disease`,
`congenital-heart-disease` and the cardiomyopathies, and heart failure has **no
attributable mortality to record.**

That is not an attribution habit and not a rounding artefact. **It is a modelling
decision in the dataset**, made for a good reason — deaths must sum to the total
and a cause hierarchy has to be exclusive — and it means the register cannot
source a deaths figure for one of the highest-mortality syndromes in medicine.
Around half of people diagnosed have historically been dead within five years,
and the field reads zero.

**`anaemia` is modelled the same way**, which is what makes this a gap rather than
a curiosity: two records, both large, both filed as impairments, both reading
`deaths: 0` for reasons that have nothing in common with the other zeros in this
register.

The register now has **six kinds of zero in one field** and they mean entirely
different things:

| record | why `deaths: 0` |
|---|---|
| **hearing-loss** | literal — it does not kill |
| **osteoarthritis** | attribution habit — NSAID bleeds and inactivity deaths filed elsewhere |
| **anaemia** | **multiplicative** — it makes other things lethal |
| **cerebral-palsy** | filed under the complication (aspiration pneumonia) |
| **heart-failure** | **the burden dataset does not model it as a cause** |
| **osteoporosis** | filed under the **physical event** — hip fracture deaths are counted as falls |

**One field, six meanings, and a reader cannot tell them apart.** #182 said the
register's magnitude is deaths and some diseases are disability; that is true and
it is now the smaller half of the problem. The larger half is that **`deaths: 0`
is not a measurement at all in four of these six rows — it is an artefact of
somebody else's accounting scheme**, and the register stores it beside figures
that are measurements.

The minimum fix is a **reason code on a zero**, so `burden.deaths` can say
*not-a-cause-in-source* rather than implying nobody dies. The better fix touches
`mondo:`'s own rule: **the identifier and the burden source are two different
external dependencies with two different ontologies**, and #43 already noted that
a borrowed identifier carries somebody else's boundary. This is the same
observation about the *other* dependency, and the register has been treating GBD
as neutral infrastructure rather than as a second opinionated source.

**A concrete check exists**: `mondo_sync.py` already diffs the register against
Mondo. Nothing diffs it against the burden source, and for at least two records
the two disagree about whether the entity is a cause.

---

## 212. A treatment can be lost to the salience of its harm, and `toll` records only the size · **open**
*Forced by:* `osteoporosis`, which contains two of them eight years apart.

`toll` holds **severity** and **incidence**. Those are the variables a
decision-theorist would want, and they are not the variables that decided whether
this treatment was used.

**Twice, in one disease, a fracture-preventing therapy was abandoned at
population scale on the perception of a harm rather than its size.**

- **2002 — hormone therapy.** The Women's Health Initiative found increased breast
  cancer and cardiovascular events in a population whose mean age was sixty-three.
  It also found a **reduction in hip fracture**, one of its clearest results. Use
  fell by something like eighty percent within a few years, worldwide. Later
  analysis gave a substantially more favourable picture for women starting near
  the menopause. **The prescribing never returned.**
- **2010 — bisphosphonates.** Atypical femoral fracture and osteonecrosis of the
  jaw were characterised. Both are real, permanent and **rare at osteoporosis
  doses**. Oral bisphosphonate use in the United States fell by more than half in
  about four years, post-fracture treatment rates fell with it, and the long
  decline in hip fracture rates flattened. **No efficacy estimate changed. No
  trial was retracted.** Every quantitative analysis of the trade-off continued to
  favour treatment by a wide margin.

**So what decided it?** Three properties of the harm that this schema cannot
record:

1. **Attributability.** An atypical femoral fracture is transverse, often
   bilateral, preceded by thigh pain, and looks like nothing else — **the drug's
   fingerprint is on the radiograph.** A prevented hip fracture has no fingerprint
   because it did not happen.
2. **Vividness.** One side of the ledger acquired a name, a picture and a story.
   The other side remained a counterfactual, and counterfactuals have no
   constituency — the same asymmetry #113's de-implementation note observes from
   the opposite direction.
3. **Agency.** A harm the clinician *caused* is weighted differently from a harm
   they *failed to prevent*, and that asymmetry is a professional norm rather than
   an error. It is not irrational and it is not in any field here.

**Distinguish it from the neighbours.** #98 says symptom relief is not counted as
a benefit. #161 says the patient may undervalue the benefit. #110 says the patient
can be blamed. **None of them says the harm and the benefit are weighed on
different scales because one is nameable.** And it is not #35's
`harm_without_benefit` conflation either: here the benefit is large, established,
and abandoned anyway.

Where else the corpus already carries it:

| record | the vivid harm | what was lost |
|---|---|---|
| **osteoporosis** | atypical femoral fracture; the WHI | two therapies, twice |
| **atrial-fibrillation** | intracranial haemorrhage on anticoagulation | stroke prevention, systematically withheld |
| **low-back-pain** | the opioid crisis | analgesia in people who need it — the pendulum, now overswung |
| **hearing-loss** | *the inverse* — the harm was invisible and the treatment was given for a century (oralism) |
| **type-2-diabetes**, **obesity** | historical drug withdrawals shaping caution for decades |

**What to build.** `toll` gains **`attributable`** — can this harm be pointed at
in an individual patient — and optionally a note on whether the treatment was
withdrawn or curtailed as a result. That second field is the one with teeth,
because it turns a story into a countable event: **the register would then be able
to ask how many of its records lost a working treatment to a rare harm, which is a
question nobody has a dataset for.**

**And the register should record its own version of the asymmetry.** `moved:`
entries in this corpus are overwhelmingly progress. `osteoporosis` carries **two
that go backwards**, and they are among the most informative entries written so
far. A register whose memory only records improvement cannot support the second
pass it exists to enable.

---

**Strengthened by `heart-failure` and `osteoporosis`, not new:**

- **#39 (a final common pathway) — THE RECORD IT NAMED IS NOW HELD.** The gap said
  heart failure was *"the textbook case and it is not yet in the register"*, and
  five of its causes were rated first. Its `mechanism: partial` is entirely #39's
  prediction: sub-mechanisms individually solid, the entity without one, and
  **thirty years of neutral trials in preserved ejection fraction as the
  mechanical consequence of enrolling a mixture.** Nine citing records.
- **#170 (an early-acting treatment pulls the definition backwards) — SIXTH
  RECORD, and this one wrote it into a guideline.** Heart failure is formally
  staged **A** (at risk) and **B** (structural abnormality, no symptoms) before it
  is staged as the syndrome. The field did deliberately and explicitly what #170
  describes, and published it. **This gap should stop waiting.**
- **#205 (a disease can end on its own) — THE DECISIVE DATUM, AND IT COMES FROM A
  WITHDRAWAL TRIAL.** Heart failure with recovered ejection fraction looks like a
  cure: function normalises on therapy. A randomised withdrawal trial stopped
  treatment in exactly those patients and **a large fraction relapsed within six
  months.** So the state is an *induced remission maintained by continuing
  treatment*, proven by taking the treatment away — and the register has neither
  the concept nor, until now, the evidence that it is distinct from cure.
  **`osteoporosis` supplies the stronger form**: stopping denosumab causes
  **rebound vertebral fractures**, in some patients to below baseline. **A
  treatment whose withdrawal is worse than never starting** is not on the ladder
  at any rung.
- **#160 (the register is a flat list) — THREE MORE ARROWS, AND ONE OF THEM
  REPEATS FOR THE THIRD TIME IN FIVE RECORDS.** SGLT2 inhibitors, developed to
  lower blood glucose, are the fourth pillar in reduced ejection fraction and the
  *only* therapy that works in preserved. Semaglutide, developed for diabetes and
  obesity, is the best recent result in both `osteoarthritis` and heart failure's
  preserved stratum. **The most important new therapy in three consecutive records
  was developed for a different disease.** And `osteoporosis` supplies the
  iatrogenic arrow: glucocorticoids documented in `asthma`, `copd`,
  `rheumatoid-arthritis` and `crohns` produce fractures that are counted here.
- **#193 / #198 (mechanism is not on the path to the treatment) — THE STRONGEST
  COUNTEREXAMPLE THE REGISTER HAS, and it should be recorded as such.** Heart
  failure's physiology said beta-blockers would kill these patients; textbooks
  listed it as a contraindication; two trials in 1999 stopped early for a mortality
  reduction of around a third. **Here mechanism was on the path and pointing the
  wrong way, and only an experiment could tell.** After a run of records arguing
  that understanding is not required, this is the case where confident
  understanding was the obstacle.
- **#179 (the entity is a risk factor rather than a disease) — IT PREDICTED
  `osteoporosis` BY NAME.** The table written at `hypertension` reads *"osteoporosis
  (not held) | bone density | fracture"*, and every consequence it forecast holds:
  strained `efficacy` units, `deaths: 0`, and the outcome living in another
  entity. **A gap that named an unwritten record and was right about it is the
  best evidence in this project that the schema work is doing something.**
- **#90 / #180 / #206 (thresholds) — two more, and both decide treatment.** Heart
  failure's ejection-fraction boundaries at 40% and 50% are **narrower than the
  test's own inter-reader variation**, so which drugs a patient is offered can turn
  on which sonographer scanned them. Osteoporosis's T-score of −2.5 was chosen by a
  working group in 1994 against a **young adult reference population** — #206
  exactly — and, because the osteopenic range holds far more people, **most
  fragility fractures occur in people who do not meet the diagnostic criteria.**
- **#202 (a replacement has a service life) — in two non-orthopaedic forms.**
  Defibrillator and resynchronisation generators need replacing every several
  years, which is `osteoarthritis`'s bearing with a battery. And bisphosphonate
  **drug holidays** are a treatment with a duration ceiling set by its own toll —
  the same structure in pharmacological form.
- **#161 (the patient undervalues the benefit) — its purest statement.**
  Osteoporosis is a disease with no symptoms, treated with a drug with no
  perceptible effect, to prevent an event that may not happen, at `ongoing: low`.
  Persistence at one year is around half. **There is nothing on the patient's side
  of the ledger at all.**
- **#96 (a window closes before there is anything to diagnose) — a third tissue.**
  After COPD's lung growth and `asthma`'s childhood airways, **peak bone mass** is
  attained by about thirty and everything after is withdrawal from it. Three
  records now share one shape: a determinative developmental window, no patient, no
  diagnosis, and no health system that owns it.

---

## 213. `empirical foothold` is still empty at 101 records, and `check.py` asked to be told · **open**
*Forced by:* building the dashboard, which drew the map and left one cell blank.

`QUADRANTS` in `check.py` carries this comment, written at record 44:

> Unoccupied at 44 records, and named anyway because the derivation must be
> total. Something that slows a disease nobody understands — weaker than lithium
> in bipolar disorder, which is the `empirical luck` case. **If this cell is
> still empty at a hundred records that is worth reporting, not worth deleting.**

**It is a hundred and one records, and the cell is still empty.** Nothing found
it; the dashboard drew a map with a hole in it and the query link for that cell
was rejected by the engine, because enum domains are read off the data and
`quadrant` has no value nobody occupies.

**The whole `empirical` row is five records out of 101:**

| record | mechanism | intervention | cell |
|---|---|---|---|
| **bipolar** | correlates | suppressive | empirical luck |
| **depression** | correlates | symptomatic | frontier |
| **heds** | correlates | symptomatic | frontier |
| **me-cfs** | correlates | none | frontier |
| **low-back-pain** | none | symptomatic | frontier |

So the missing cell needs a disease that is **not understood** and has a
treatment that **alters its course** — and the two readings of its emptiness are
very different.

**The structural reading, and it is the interesting one.** You may not be able to
demonstrate that something *slows* a disease you cannot describe. Symptom relief
is measurable with a questionnaire and needs no theory. **Course alteration
requires a marker, a trajectory and an endpoint — which is most of what
`mechanism: established` means.** On that reading `empirical foothold` is not
under-sampled, it is close to a contradiction: the evidence that would put a
record in it is the evidence that would move it out of the `empirical` row.
`osteoarthritis` is the near-miss and it lands elsewhere — `mechanism: partial`,
so it counts as known, and its intervention is `curative` rather than modifying.

**The sampling reading, and it is the one that should be stated on the public
page.** Five of 101 records is a very thin column, four of the five are the
psychiatric and unexplained-illness cluster, and **the corpus was chosen for
structural diversity rather than by any sampling frame**. The register's
optimistic-looking shape — 81 of 101 in `known & treatable` — is partly a fact
about which records got written. The empty cell is a reminder of that in the
most visible possible form, which is an argument for drawing it rather than
hiding it.

**And the meta-point is the third instance of a pattern this project keeps
finding in itself.** `check.py` made a dated, checkable prediction about its own
output — *report this at a hundred records* — and nothing reports it. Same shape
as the seven stale "watch for the second record" notes in this file (see #69),
and same shape as `index.md` drifting from its own derivations. **Every artefact
here that carries a claim about the future is unguarded except the two that were
caught drifting.**

The dashboard now renders an empty cell in vermilion with *"empty — no record in
the corpus has this shape"*, which discharges the comment's request. **The
general fix is a check that fails when a derivation's codomain has an unoccupied
value that a comment predicted would fill**, and that is probably over-engineering
for one cell — but a test that simply lists unoccupied enum values on every run
would have found this a year of records ago.

---

## 214. A figure you cannot type is a figure nobody can check · **open**
*Forced by:* the dashboard, and it is the query language's founding sentence
turned around.

`web/query.js` exists because seven AND-ed dropdowns could not express a single
one of the register's six canned questions, and the rule written down at the time
was: **a question you cannot type is a question only the author can ask.**

Building the dashboard produced the inverse. Three of the most informative
figures on the page have no query that returns them:

| figure | what it counts | why no query returns it |
|---|---|---|
| **`knowledge 95` / `logistics 80`** | blockers | the engine counts **records**; `blocker.kind:knowledge` returns the 94 records with at least one |
| **`127 changes in what we can DO`** | `moved` entries | `moved` is not a field, and an entry is not a record |
| **`government 293`** | actor mentions | same — `blocker.who_could:government` returns 96 records |
| **Engpass's `who-progresses 29`** | records per obstacle | `blockers[].obstacles` is not queryable, deliberately: Nordstern records the slug and does not know what it refers to |

**The first version of the dashboard linked all of them anyway**, to
plausible-looking queries, and printed **127** beside a query returning **54**.
`web/dashboard.test.js` caught it on its first run — which is the good news, and
the reason that test was written before the page was finished.

**Why it matters more on a public page than in the tool.** A visitor who clicks a
figure and lands on a different number concludes that one of them is broken, and
they are right. **The page is the one with the big number on it, so the page
wins**, and the register has just taught somebody a wrong fact with its own
tooling. The current fix is honest and unsatisfying: those figures carry no link,
and the footer says why.

**What would actually close it.** The query engine has one collection and returns
subsets of it. What the dashboard wants is an aggregate over *sub-objects* —
blockers, strata, `moved` entries — with a projection and a count. Options, from
cheapest:

- **A second entry point**, `count(blockers) by kind`, kept deliberately separate
  from the record query so the tool stays one idea;
- **Sub-object queries** returning blockers rather than records —
  `blockers where kind:knowledge` — which is a genuine language change and would
  need its own result view;
- or **accept the boundary and say so**, which is what the page does now, and
  which has the merit of being true.

**The third is defensible and should be revisited only when a real question
forces it** — the same discipline that deferred cross-term `OR` and parens. But
note what has changed: those were deferred because no one had asked. **This one
has already been asked, by the dashboard, four times.**

---

## 215. A new treatment raises `efficacy` and lowers `access`, and nobody lost anything · **open**
*Forced by:* `pancreatic-cancer`, on the day the approval happened — 26 August
2026, daraxonrasib.

`efficacy` is defined in SCHEMA.md as **what the best available treatment
achieves**. `access` is **the fraction of patients who can obtain it**. Both
definitions are right, and together they have a property nobody noticed until a
drug was approved while the register was open:

**The moment a better treatment exists, `efficacy` rises and `access` must fall
— without one patient being worse off than they were the day before.** The
denominator of `access` is *the best available treatment*, and the best available
treatment just changed to something approved in one country, priced like a new
oncology drug, and obtainable by almost nobody.

Pancreatic cancer, in one day:

| | before | after |
|---|---|---|
| `efficacy` | 0.15 | **0.22** — daraxonrasib halves the hazard in the second line |
| `access` | 0.30 | **still 0.30, and that is now wrong** |
| `reach` | 0.045 | 0.066 |
| `delivery` | **undelivered** | **barely** |

**The record's derived verdict improved because a drug that nearly nobody can get
was approved.** `reach = efficacy × access` multiplied a rise against a figure
that had not yet been re-measured, and the register reported progress in
delivery on a day when delivery did not change.

**It is not #174 and it is not #108.** #174 (`chronic-kidney-disease`) is
*you got the worse tier of an intervention that exists*. #108 (`measles`) is
*coverage has a threshold*. This is upstream of both: **the yardstick moved.**
It is closest to #76 — *a metric can be satisfied by moving its denominator* —
except that #76 is a warning about ranking burden, and this is the register's own
two central axes disagreeing by construction.

Three consequences, and the third is the one that matters:

1. **A record can look better the instant a drug is approved and before anybody
   is treated.** Every oncology approval in this corpus will do this.
2. **`access` needs re-measuring whenever `efficacy` moves**, and nothing links
   them. A `moved:` entry on `efficacy` should probably *require* an `access`
   entry, or explicitly state that it was left alone and why — which is what
   `pancreatic-cancer`'s 2026 entry does by hand.
3. **The register will systematically overstate rich-country medicine at the
   moment of approval**, because that is when efficacy jumps and access has not
   been looked at. Given that the whole point of splitting the two axes was to
   keep *biology* apart from *money*, an arithmetic that quietly merges them at
   the moment of maximum publicity is worth fixing.

**The cheap fix is a rule rather than a field**: an `efficacy` move that comes
from a newly approved treatment must be paired with an `access` move, even if
that move is *down*. The honest version is that `access` is not one number when
the best available treatment is new — it is high for the old standard and near
zero for the new one, which is #204's shape (`access` is one number for a regimen
with more than one part) arriving from a different direction.

**Note how this was found.** Not by reasoning about the schema — by somebody
sending a link to an FDA press release and the register being edited the same
day. Every other `moved:` entry in the corpus is history, written with the
outcome known. This is the first one written while the change was still
happening, and it exposed an arithmetic error in the register's central
derivation on its first outing. **That is an argument for keeping the register
current rather than revisiting it annually.**

---

## 216. `survival` at a horizon cannot tell cure from delay · **partly closed**
*Closed part (2026-08-28):* the derivation proposed at the end of this entry is
built — `survival_outcome` reads `axes.intervention` and returns `cured` /
`held` / `delayed`, with no new field, exactly as sketched. It is queryable as
`outcome:`, it is on the dashboard as the colour of the survival chart, and
`survival_sentence` renders the pair as one line: *"20% at 5 years from symptom
onset — alive and still dying of it."* **The urge to add a field was correctly
resisted; the information was one column over the whole time.**
*Still open:* `no_longer_terminal` remains unqualified — `pancreatic-cancer`
crosses at 0.13 and `type-1-diabetes` at 0.95, and the flag cannot tell them
apart. The dashboard says so in the card's own note rather than fixing it.
Tempo is still nowhere in the schema.

*Forced by:* `als`, on the day the `survival` field was added — the first record
rated on the new axis broke it.

The `survival` field was built because `efficacy` is not comparable across
records: it reads 0.55 for `head-neck-cancer` (alive and disease-free at five
years) and 0.85 for `asthma` (good symptom control), and `reach = efficacy ×
access` multiplies across them as though they commuted. **Survival is the one
axis that means the same thing everywhere** — the fraction of people alive at a
stated horizon.

Except that it does not.

| record | 5-year survival | band | what the number means |
|---|---:|---|---|
| **pancreatic-cancer** | 0.13 | `a chance` | **thirteen percent are CURED** — alive, disease gone |
| **als** | 0.20 | `a chance` | **twenty percent are STILL DYING OF IT** — nobody is ever cured |

**Same band, same axis, opposite facts.** ALS is universally fatal: no
treatment arrests it, nobody recovers, and the only variable is tempo.
Pancreatic cancer kills most people and cures a real minority. A view built on
`survival` alone would rank ALS *above* pancreatic cancer and be exactly wrong
about which one anybody survives.

**The horizon papers over it and cannot fix it.** ALS at ten years is ~0.10 and
at twenty approaches zero, so the band is a function of the horizon in a way it
is not for a disease some people survive outright. `huntington` is rated at a
twenty-year horizon precisely to force it into `terminal`, and that works —
**but choosing the horizon to produce the right band is fitting the instrument to
the answer**, which is what the register exists not to do.

**What is actually missing is a second question: does the disease end?**
Three states, not one:

| | example |
|---|---|
| **cured** — alive and the disease is gone | childhood ALL, early breast cancer, hepatitis C |
| **suppressed** — alive and the disease is held | HIV, type 1 diabetes, CML on a TKI |
| **delayed** — alive and the disease is still killing them | ALS, Huntington's, IPF, glioblastoma |

The register already distinguishes the first two on the intervention ladder
(`curative` versus `suppressive`), which is why this is not simply a missing
enum — **the information exists in a different field and `survival` does not
read it.** A derivation combining `survival_band` with `intervention` would
separate the three today, without new data:

```
survival ≥ 0.10  and  intervention: curative      → some are cured
survival ≥ 0.10  and  intervention: suppressive   → alive and held
survival ≥ 0.10  and  intervention ≤ disease-modifying → alive and still dying
```

That is cheap and probably right, and it is worth resisting the urge to add a
field before trying it.

**Two things this makes visible that the register had not stated.**

**Tempo is not severity, and the corpus conflates them.** A disease that kills
everybody in thirty months and one that kills everybody in twenty years are
equally lethal and completely different to live through and to treat. Nothing in
the schema holds duration; `ongoing` holds the burden of *being treated*, not
how long the illness lasts.

**And the progress claim needs the same distinction.** `no_longer_terminal`
counts records that were uniformly fatal untreated and are not terminal treated —
seven of the first ten rated. **But "no longer terminal" means something
categorically different for type 1 diabetes (0.0 → 0.95, held indefinitely) than
it would for a disease whose treated survival rose from 0.05 to 0.15 while
remaining uniformly fatal.** Both would count. Only one is what anybody means by
progress, and the flag as written cannot tell them apart.

**Where this bites hardest is the dashboard**, which is why it is logged before
that page is built. A "state of medicine" view ranked on survival, with no
cure/delay distinction, would report ALS as better off than pancreatic cancer and
`head-neck-cancer` — a `good chance` record with a `catastrophic` toll — as an
unqualified success. **The axis is a genuine improvement on `efficacy` and it is
not safe to display on its own.**

---

## 217. The route to burden data runs through UMLS, and MONDO's ICD coverage is worst where burden is highest · **open**
*Forced by:* asking whether the register should adopt WHO ICD, then running
`icd_coverage.py` before answering. **The report contradicted the answer that was
about to be given.**

The register's largest unsourced block is `burden` — 205 `sourceable` scalars,
every one a figure some statistics office publishes, all of them `src: recall`.
The join key to that data is an **ICD code**, and `mondo_sync.py` had already
fetched ICD cross-references, annotated them *"burden — the route into GBD cause
mappings"*, committed them to `mondo-terms.json`, and **nothing had ever read
them.** So the question was cheap to answer and had gone unanswered for months.

**89 of 100 records have an ICD cross-reference. That number is true and nearly
useless**, because the flavours are not interchangeable:

| flavour | records | with deaths | what it is for |
|---|---:|---:|---|
| `ICD9` | 74 | 50 | retired from mortality coding ~1999 |
| `icd11.foundation` | 62 | 45 | an entity id, **not a code** — needs the MMS linearization |
| `ICD10CM` | 56 | 38 | one country's billing modification |
| **`ICD10WHO`** | **27** | **15** | **the international mortality standard — the only one that joins to the WHO Mortality Database** |

**15 of 73.** The flavour that answers the register's actual question covers a
fifth of the records that have a death toll. And **`ICD9` beats it nearly three to
one** — a vocabulary two decades out of use has the better coverage, because
those xrefs arrived through legacy DOID and OMIM merges. *Coverage here reflects
MONDO's merge history, not the usefulness of the code.*

**The missing 58 are not a random 58.** `stroke` and `colorectal-cancer` carry no
ICD code of any flavour while carrying SNOMED, UMLS, MeSH, NCIt and DOID — so
this is MONDO's ICD coverage being patchy, **not our identifier being odd**. Both
are among the largest killers in the corpus. Coverage is worst exactly where
burden is highest, which is the reverse of what a sourcing pass needs.

**The census answers a question that was not asked, and it is the answer.**
`UMLS` reaches **97 of 108 records and 66 of 73 with deaths**, against
`ICD10WHO`'s 27 and 15. UMLS is a *crosswalk* — its entire job is holding one
concept's identifiers across vocabularies, ICD-10 included. **The route is MONDO
→ UMLS → ICD, and the direct MONDO → ICD edge this report set out to measure is
the wrong edge.** The cost is a licence gate: UMLS is free but requires
registration and terms acceptance, the same shape of gate as ICD-11's API, and
unlike MONDO's CC BY it cannot simply be committed to a public repo.

**A prediction this refuted.** Before running it, the caution given was *the
mapping is many-to-many, so `icd:` must be a list and never auto-accepted*. It is
**0 of 27** — every `ICD10WHO` xref MONDO carries is a single code. That is not
evidence the real mapping is 1:1; it is evidence **MONDO records only exact
matches**, the same property that makes `also` untrustworthy for auto-accept.
The rule survives; the stated reason for it did not, and would have been asserted
in a schema comment had the report not been run first.

**What stands.** ICD is not a competitor to MONDO for identity — statistical
classification versus ontology, and ICD's mutually-exclusive single-underlying-cause
rule is the *source* of most of this register's complaints, not a fix for them.
`heart-failure` is the clean demonstration: it **has** its code (`I50`) and still
carries `deaths: 0`, because the cause hierarchy re-assigns them. **The code being
present does not make the number sourceable.** Five of the six kinds of zero
(#182, #211) are artefacts of that rule, and #211 describes it without naming it.

So: **ICD belongs as a `burden` provenance key, never an identity key** — and it
is not reachable today at a coverage that would justify the schema change.
Sequenced: resolve the **8** records whose `mondo:` is still unresolved first
(`amr-infection`, `cre`, `low-back-pain`, `maternal-haemorrhage`, `pots`,
`sepsis`, `soil-transmitted-helminths`, `taeniasis-cysticercosis`) — a record
with no ontology id has no bridge to anything — then decide UMLS, then ICD.

---

## 218. `deaths:0` returned 92 of 108 records, and the tool is public · **closed**
*Forced by:* adding `gain` to the query language and noticing that `gain:0`
matched every rated record.

A bare number on a numeric field fell through to the **substring** matcher. So
`deaths:0` asked *which diseases kill nobody* and answered with the list of
diseases that kill the most people — `ischaemic-heart-disease` matched because
`6600000` contains the character `0`.

**This is rule one of the query language, skipped in the one place it mattered
most.** *The field decides how it matches* — `capability:curable` is exact
because capability is an enum, and `deaths:0` should have been numeric because
deaths is numeric. The operator forms (`deaths:>100k`) were always correct;
only the bare form was wrong, which is why it survived a redesign and a test
suite.

**And the query it broke is the register's own headline.** `deaths: 0` is the
subject of gaps.md #182 and #211 — *six distinct kinds of zero, five of them ICD
artefacts* — so a visitor following that finding into the tool got the exact
opposite of the record set it describes. It is fixed, and pinned by a test that
asserts the biggest killer in the register is **not** in `deaths:0`.

**The general lesson is about fall-through.** Text matching is the default arm of
`matches()`, so any field whose value shape the parser fails to recognise
degrades to substring silently and returns *plausible* rows rather than none.
A bad value is supposed to be a witness; this was a bad *parse* producing
confident nonsense, which is worse. Worth an audit of the other arms.

---

## 219. `survival` is built, and it does not fit a risk factor · **open**
*Forced by:* rating the batch after `heart-failure` — the three largest
unrated killers in the register are `hypertension` (10.8M), `obesity` (5.0M) and
`atrial-fibrillation`, and **not one of them has a survival.**

Nobody has a five-year survival from hypertension. It is a risk factor: it
raises the hazard of the diseases in other records, and an "untreated survival"
for it would be a number about nothing. `asthma` fails differently — 455,000
deaths a year and roughly 99.9% five-year survival, so the band reads
`good chance` and conveys nothing at all.

**So the axis covers events, not exposures**, and the register now has two
mortality columns that disagree about which diseases matter:

| | ranked by `deaths` | ranked by `survival` |
|---|---|---|
| top | hypertension, ischaemic heart disease, stroke | rabies, Huntington's, prion disease |
| invisible | heart failure, Ebola (`deaths: 0`) | hypertension, obesity, asthma |

Both are right. **`heart-failure` is the clean demonstration**: `deaths: 0`
because GBD models it as an impairment, and a five-year survival of 0.55 that is
worse than breast cancer's. The burden column loses the disease entirely and the
survival column finds it — which is the argument for having a second,
differently-derived axis rather than a better version of the first.

**RESOLVED (2026-08-28) BY NAMING THE POPULATION, not by declaring them
inapplicable.** All three are now rated, at horizons that make the question
answerable — *"10 years from diagnosis of stage 2 hypertension, untreated, at
age 50"*, which is what the VA Cooperative trials measured. Asthma is rated at
0.98 → 0.997 and produced finding #221 rather than being skipped. **The horizon
field was already load-bearing and this is what it is for.** The rows carry an
explicit caveat in their own witness that they are not comparable to a disease's
own lethality.

**What is not yet decided** is whether an inapplicable record should say so.
Today it is simply absent, and absence conflates *nobody has rated this* with
*this question does not apply here* — the exact distinction `predictive: n/a`
exists to draw, and `unrated is never unsolved` in another costume. An explicit
`survival: n/a` with a reason would fix it and would need a schema change; it is
logged rather than made, because the forcing argument should be a second reader
misreading the chart, not this note.

---

## 220. The four biggest killers are all `delayed` · **open**
*Forced by:* the survival dashboard section, on the first render.

With 31 records rated, the `outcome` derivation splits them 14 `cured`, 5
`held`, 12 `delayed` — and **the four largest single causes of death in the
register are all in the last group**, with the smallest gains:

| record | deaths | gain | outcome |
|---|---:|---:|---|
| ischaemic-heart-disease | 9.0M | +0.35 | delayed |
| stroke | 6.6M | +0.15 | delayed |
| copd | 3.5M | +0.05 | delayed |
| heart-failure | — | +0.30 | delayed |

Nobody is cured of any of them. Meanwhile the `cured` column is **infections and
cancers** — tuberculosis, malaria, diarrhoeal disease, childhood pneumonia,
Ebola, and the resectable solid tumours.

**The one-sentence reading is: medicine cures infections and some cancers, and
delays the chronic diseases that kill most people.** That is a real finding and
it is *not yet safe to publish*, for three reasons the register can state
precisely:

- **31 of 108 records are rated**, and they were rated in two batches chosen for
  what they would demonstrate — the terminal set first, then the biggest killers.
  That is the opposite of a sample.
- **The corpus itself is chosen for structural diversity, not importance**, which
  is a standing caveat on every aggregate here.
- **A deaths-weighted version is contaminated by double-counting.** `sepsis`
  carries 11M and is `cured`, which flips the weighted split — and a sepsis death
  is usually also a pneumonia death. The register already knows its mortality
  column exceeds all human mortality (72.2M attributed against ~62M actual).

**The finding is stated on the page as a shape, not a statistic**, and the
weighting is left out entirely. Revisit when the rated set passes 60 and is no
longer chosen for what it will show.

Four records have `gain: 0` — `alzheimers`, `huntington`, `prion-disease`,
`rabies`. **Alzheimer's is the one that ought to sting**: on the most comparable
axis the register has, the commonest cause of dementia has bought no additional
life at all, while its `efficacy` reads 0.25 and sounds like partial success.

---

## 221. `gain` is anti-correlated with how much a treatment matters · **open**
*Forced by:* completing the rating pass — all 76 records with a death toll now
carry a survival, and sorting them by `gain` puts the wrong things at the bottom.

`gain` is `treated − untreated`, the register's most direct statement of what
medicine bought. Sorted ascending, the smallest non-zero gains are:

| record | gain | deaths/year |
|---|---:|---:|
| covid-19 | **+0.006** | 200k (and millions in 2020-21) |
| measles | +0.010 | 110k |
| asthma | +0.017 | 455k |
| influenza | +0.020 | 400k |

And the largest:

| record | gain | deaths/year |
|---|---:|---:|
| hat | +0.950 | ~0 |
| cystic-fibrosis | +0.900 | 2k |
| visceral-leishmaniasis | +0.900 | 20k |

**The column is close to inverted against burden.** A difference of fractions
compresses catastrophically at the top: 0.98 → 0.997 in asthma is +0.017 and is
most of 455,000 annual deaths, because the prevalence underneath it is enormous.
Meanwhile human African trypanosomiasis went from uniformly fatal to 95%
survival — the largest gain in the register — for a few hundred people a year.

**Both facts are real and the axis can state only one of them.** `gain` answers
*how much does this treatment change one patient's odds*, which is the right
question for a patient and the wrong one for a funder. The missing quantity is
**deaths averted** — `gain × incidence` — and the register has no field for it
because `burden.incidence` is populated on far fewer records than `deaths`, and
multiplying a `src: recall` fraction by a `src: recall` incidence produces a
confident number from two guesses.

**So it is not computed, and the dashboard does not sort by `gain`.** The
survival chart sorts by treated survival, which has no such inversion. This is
logged so that the first person who thinks to add a "biggest wins" ranking finds
out here rather than after publishing it.

**A related asymmetry the register also cannot express:** `atrial-fibrillation`'s
survival gain is almost entirely *stroke prevented*, so one record's treatment
moves another record's mortality. That is the same double-counting that makes
the deaths column exceed all human mortality (72.2M attributed against ~62M
actual), seen from the treatment side.

---

## 222. The ladder says what treatment achieves, not what happens to the patient · **closed**
*Forced by:* `measles`, on the first render after the rating pass completed.
The dashboard printed: **"99% at 30 days from rash onset — alive and still
dying of it."**

That is not imprecise, it is false. Measles is `symptomatic` because there is no
antiviral; its survivors recovered, because the immune system ended it. Six
records produced the same false sentence — `measles`, `dengue`, `influenza`,
`cholera`, `h5n1`, `marburg` — every one an acute infection that is
self-limiting in survivors.

**The derivation (#216) read the intervention rung alone**, which works for
chronic disease because there the rung and the patient's fate coincide closely
enough. For an acute infection they come apart completely: the ladder describes
*what treatment achieves*, and "nothing" is a statement about the pharmacopoeia,
not about whether the patient stays ill.

#216 had already noted that **nothing in the schema holds duration.** This is
that gap arriving with a bill, eight days later, in the form of a public page
telling people that measles survivors are dying.

**Fixed with a fourth outcome and a declared field.** `survival.course: acute |
chronic`, defaulting to chronic, consulted **only** for records below
`suppressive` — an acute disease that antibiotics cure (`typhoid`, treated
`cholera`, `malaria`) is `cured`, because there the treatment genuinely ended
it. Outcomes are now `cured` · `recovered` · `held` · `delayed`.

**It is declared rather than derived because nothing in the register implies
it** — not the ladder, not `kind`, not the horizon, which is prose. A test
asserts no acute record can print "still dying", and a misspelled `course` is an
error rather than a silent default to the sentence it exists to prevent.

**Two smaller things the same pass caught.** The bounded YAML loader does not
strip trailing `#` comments from a plain scalar, so `course: acute  # why` was
read as the whole string — caught immediately by the enum check, and worth
knowing before someone writes a comment on a value that has no enum behind it.
And `survival_sentence` was rounding 0.997 to **"100%"** for asthma and cholera;
it now prints `>99%`, because "100% survive" is a different claim and the
missing 0.3% of asthmatics is 455,000 people a year.

---

## 223. The first fungal record broke four things, and three of them were guards working · **closed**
*Forced by:* `cryptococcal-meningitis` (FND-D-0109), the register's first
invasive fungal disease. **The corpus had 108 records and one fungal entry —
`mycetoma`, a neglected foot infection carrying `deaths: 0`.** Invasive fungal
disease plausibly kills more people annually than tuberculosis, HIV and malaria
combined, and `amr-infection` is scoped in its own name to *"multidrug-resistant
**bacteria**"*, so antifungal resistance had nowhere to live either.

**1. A CRASH IN DEAD CODE THAT HAD NEVER RUN.** A copy of the
measurement-validation block from `check()` had been pasted into the middle of
`spans_ladder()` — a pure derivation with no `errors` or `here` in scope. It
could only ever raise `NameError`. Reaching it required `predictive: n/a`
together with efficacy below 0.85, and `hepatitis-c`, the register's only other
`n/a`, sits at 0.95. **This record was the first to reach it in 109.** Removed;
a derivation must not validate.

**2. THE RULE IT WAS TRYING TO ENFORCE WAS RIGHT, AND THE RATING WAS WRONG.**
Once the crash was fixed the check fired properly: `predictive: n/a` with
`intervention: curative` and efficacy 0.75. The claim had been that a
good-enough treatment abolishes the question, the way pan-genotypic antivirals
did for hepatitis C. But hepatitis C cures 95%, and this regimen **leaves a
quarter of optimally treated patients dead at ten weeks.** A treatment failing
one patient in four has a selection question by definition. Corrected to
`partial`. **The validator caught an over-claim that no human reviewer would
have.**

**3. THE MONDO ID RESOLVED TO THE WRONG DISEASE.** `MONDO:0005704` was written
from recall. It is a real term — **"Ciliophora infectious disease"**, a
ciliate-protozoan entity with no relation to cryptococcosis. The correct id is
`MONDO:0005723`. This is the *worse* failure mode, the same one as
`MONDO:0007403` (inherited CJD standing in for all prion disease): an identifier
that resolves to nothing is recoverable, one that resolves to a plausible wrong
thing is not. `TestMondoIdentifiers`, added after the fabricated IPF id, caught
it before the record was ever built.

**4. AND ONE GUARD CAUGHT A DECLARATION THAT WOULD HAVE ROTTED.** `course:
acute` was declared, correctly as biology — and `survival_outcome` checks
`curative` first, so it is never read on this record. The test added eight days
earlier (#222) rejects declaring a field nothing consults. Removed, with the
reason written into the witness.

**Three of the four were the register defending itself.** That is the return on
`test_check.py`, which did not exist until record 43.

---

## 224. index.md was hand-maintained, and I destroyed it · **closed**
*Forced by:* regenerating `index.md` with `check.py --markdown` after adding a
record, on the assumption — stated in CLAUDE.md and in this file — that
**`index.md` is generated.**

It was not, entirely. `--markdown` emitted the tables; the **2×3 quadrant map
and the blocker-census total were maintained by hand**, and overwriting the file
lost them. Nordstern is not in git (`git ls-files Nordstern` returns 0) and no
Dropbox cache copy survived locally, so the original wording is recoverable only
from Dropbox's own web version history.

**The section that was lost is the section this file already records as
drifting twice.** #46 caught two blocker counts patched in wrong by hand.
`test_index_md_quadrant_cells_match_the_derived_map` was written after four
consecutive records — typhoid, mrsa, cre, malaria — were appended to the map by
a first-occurrence string replacement and every one landed in the wrong cell.
**A guard was written to detect the drift and nobody removed the cause.**

So the map is now **generated**, which is what the register's own first rule says
it should always have been. Cross-listing a footnoted slug (`sickle-cell\*`) is
the only thing left by hand, and the test still treats an unannotated slug in the
wrong cell as an error.

**Two things worth keeping from this.**
**The row labels are load-bearing and it is not obvious.** The guard finds rows
by their leading cell — `| **known** |` strictly, `| **not known** |` for total
membership — so relabelling the second row to `**empirical**`, which is the
wording `web/index.html` uses, silently disabled half the check. It is now
commented at the emitter. **The two pages disagree about that label and should
converge.**
**"It is generated" was believed of a file that was two-thirds generated**, and
the belief was written in three places. A file that is partly generated is worse
than one that is not, because the generated part licenses overwriting the rest.
**Nordstern should be in git before the next structural change** — the user has
said it is becoming its own public repo, and this is the argument for doing that
first rather than after.

---

## 225. The register has no way to hold a disease driven by weather and land use · **open**
*Forced by:* `coccidioidomycosis` (FND-D-0111), the third fungal record and the
purest environmental one.

**The epidemiology is a map, not a network.** There is no person-to-person
transmission — none, beyond a handful of transplant and wound-inoculation
reports. You get Valley fever by breathing air in a specific place. So there is
no chain to interrupt, no contact to trace, no reservoir host, no vector, and no
herd effect from treating anybody. gaps.md #70 states the register's implicit
model — *"every other infectious record in this register is controlled by
attacking its transmission route"* — and this is the record where the absence is
total.

**And the incidence is a function of the weather.** Drought followed by heavy
rain drives outbreak years; dust storms and soil disturbance drive exposure; the
endemic area is defined by aridity and is projected to expand, with locally
acquired cases already appearing well north of the historical range. **Two
records in the corpus mention warming at all and neither holds it as a
mechanism.** No axis, no blocker kind and no actor in this schema describes a
disease whose driver is climate.

**Three things the schema could not express in this one record:**

- **A court as the actor.** The most concentrated involuntary exposure the
  register holds is a *prison siting decision* — state institutions built in the
  hyperendemic San Joaquin Valley, sustained outbreaks, disproportionate harm to
  Black and Filipino inmates, and a remedy delivered by **court-supervised
  transfer of susceptible prisoners.** `ACTORS` has no entry for a court, and
  no blocker kind describes an exposure somebody is legally compelled to endure.
- **A disease that ends without medicine ending it.** 94% of infections resolve
  unaided, and the stratum is rated `curative` because the disease ends. The
  ladder describes *what treatment achieves* and has no rung for "resolves on its
  own" — **the same gap `course: acute` patched on the survival axis** (#222),
  arriving on the intervention axis six days later.
- **A cure that is over while the therapy is not.** Coccidioidal meningitis is
  controlled by fluconazole and relapses in about four of five who stop, so
  treatment is lifelong. There is no active infection to measure and nothing to
  be cured of. `residue` had to carry it, and does so badly.

---

## 226. Three records are now rated on a named severe subpopulation, and there is no rule · **open**
*Forced by:* `coccidioidomycosis`, which is the third.

`survival` is meant to be **the one axis that means the same thing in every
record** — the fraction of people alive at a stated horizon. Three records now
quietly rate a subpopulation instead of the entity:

| record | horizon as declared |
|---|---|
| hypertension | *10 years from diagnosis of stage 2 hypertension, untreated, at age 50* |
| asthma | *5 years from diagnosis of severe asthma* |
| coccidioidomycosis | *2 years from diagnosis of disseminated disease* |

Each was written for a good reason — across all infection, Valley fever is
survived by essentially everyone, and the axis would report a triumph about a
condition that puts people on antifungals for life (#221's compression, again).
**The horizon field carries the qualifier honestly and that is not the same as
having a rule.** Nothing stops the next record narrowing its population until
the number looks interesting, which is fitting the instrument to the answer —
the thing #216 already warned about for the horizon length.

What is missing is a stated test for when narrowing is legitimate. A candidate:
*narrow only when the excluded population has no mortality question at all, and
say so in the witness.* Not adopted, because three instances is enough to notice
a pattern and not enough to know its shape.

---

## 227. MONDO has the parent diseases and not the clinically decisive sub-entities · **partly closed**
*Forced by:* looking up an identifier before writing each of the four fungal
records, and finding the same hole three times.

Every parent entity resolved cleanly and quickly — `MONDO:0005723` cryptococcal
meningitis, `MONDO:0000240` invasive aspergillosis, `MONDO:0005706`
coccidioidomycosis, `MONDO:0044070` candidemia. **Three sub-entities returned
nothing at all:**

| missing term | why it matters |
|---|---|
| **chronic pulmonary aspergillosis** | probably a larger burden than invasive aspergillosis; follows tuberculosis into a healed cavity; one to two million people |
| **coccidioidal meningitis** | the only `suppressive` stratum in its record — lifelong fluconazole, relapse in four of five who stop |
| **Candida auris** | the only fungus in the register that transmits patient-to-patient; a WHO critical-priority pathogen since 2016 |

**A FIFTH INSTANCE, AND THE LEAST DEFENSIBLE (2026-08-28).** `MONDO:0005701`
is *Chlamydia trachomatis infectious disease*, and its four children are
**trachoma, inclusion conjunctivitis, lymphogranuloma venereum and chlamydial
pneumonia** — two eye diseases, a rare proctitis syndrome and a neonatal
pneumonia. **Genital chlamydia has no term**, and it is the commonest bacterial
sexually transmitted infection in the world at roughly 130 million infections a
year, larger than all four children combined. The ontology holds the rare
presentations of an organism and not the common one.

**A COUNTER-EXAMPLE ARRIVED WITH `toxoplasmosis` (FND-D-0114) AND IT NARROWS
THIS ENTRY SHARPLY.** Mondo holds **every** decisive sub-entity of toxoplasmosis
— `MONDO:0005715` congenital, `MONDO:0005879` ocular, `MONDO:0005697` cerebral —
and the sub-entity check found all three automatically once the strata were named
to match. So the ontology is **not** uniformly missing clinical sub-entities.
Where it is thin is mycology and common acute illness; where a disease has a long
literature and named clinical syndromes, the terms exist. **The original framing
of this entry — an ontology-wide gap — was too broad.**

**A FOURTH MISSING-TERM INSTANCE ARRIVED THE SAME DAY AND IT IS NOT FUNGAL.** `acute
bronchitis` — among the commonest reasons a human being consults a doctor —
**has no human MONDO term.** `bronchitis` and `chronic bronchitis` exist, and so
does **`acute bronchitis, non-human animal`**. So this is not a mycology problem,
which is what the first three instances suggested; it is a gap in how the
ontology covers common acute illness generally.

**In each case the missing term is the one carrying the clinically decisive
distinction.** Invasive and chronic pulmonary aspergillosis share a genus and
almost nothing else — different hosts, different course, different rung on the
ladder. Coccidioidal meningitis is the reason its record spans the ladder.
*C. auris* is the reason candidaemia has an infection-control blocker at all.

**This is a gap in the borrowed enumeration, not in Nordstern**, and the
register's own rule is that disease IDs are borrowed and never minted — so the
options are to file the terms upstream, or to hold these as `strata` and accept
that a sub-entity the register treats as decisive has no address anyone outside
can cite. **Two of the three are already held as strata** and the third is a
missing record.

**BUILT 2026-08-28 as `mondo_sync.diff_subentities`**, and the first version was
worse than useless in two ways worth recording.

It **proposed `MONDO:1017104` — *acute bronchitis, non-human animal* — as the
`fix` for the human bronchitis record.** That is the `duodenal ulcer` failure
with a veterinary flavour, and it would have been written by `--apply`. Two
corrections followed: Mondo's `non-human animal` namespace is filtered
unconditionally, because not one of those terms can ever be right for this
register; and **the precision finding no longer carries a `fix` at all.**
`--apply` writes only an obsoleted term's own named replacement, because that is
Mondo's statement rather than an inference — and this check cannot tell a
narrower term for our entity from a sibling sharing its words. `pleomorphic
adenoma of the salivary gland` returns *carcinoma ex pleomorphic adenoma*, a
malignant transformation and a different disease.

It also produced **180 alias findings, about half of them junk**, because Mondo's
exact search matches synonyms as well as labels — `motor neurone disease` came
back as *frontotemporal dementia and/or ALS 1*, `Alzheimer's` as *Alzheimer
disease 3*. Requiring the hit's **label** to be the name, rather than merely to
match it, cut that to 58 and left the real ones standing.

**What it found, on 113 records:**

| finding | n | what it means |
|---|---:|---|
| no term exists | 5 | acute bronchitis · pneumonia in under-fives · H. pylori peptic ulcer · H5N1 avian influenza · seasonal influenza |
| pointing at a parent | 1 | pleomorphic adenoma of the salivary gland — a candidate to review, not a fix |
| `also` is a different entity | 58 | pernicious anaemia, allergic asthma, atrial flutter, urothelial carcinoma… |
| strata the ontology holds | 7 | dysentery, resistant hypertension, hydrocele, sporadic CJD, ischaemic stroke, subarachnoid haemorrhage |

**The 58 are the biggest surprise and are the `duodenal ulcer` class at scale.**
`also` is read as a list of equivalences, and it is carrying terms Mondo holds as
distinct entities. The existing scope audit could not see them: it only checks
`also` entries Mondo lists as synonyms *of our term*, so an alias that is
somebody else's term entirely passed straight through.

**One junk finding is left visible on purpose.** `prion-disease`'s stratum
`acquired` matches a Mondo term literally labelled *acquired*. No filter removes
it without also removing `dysentery` and `hydrocele`, which are one word and
genuine, so the report names the problem instead of hiding it.

**And the check is only positive on strata.** A stratum name is often a
descriptive phrase — *"fluconazole-susceptible, chiefly C. albicans"* — so
searching one and finding nothing is uninformative, and reporting that null
would be a check that could not run reporting a result.

---

## 228. The register cannot see its own largest avoidable harm · **open**
*Forced by:* `acute-bronchitis` (FND-D-0113), added because it is the textbook
case of antibiotic overprescription.

The record derives, correctly under every existing rule:

| derivation | value |
|---|---|
| `capability` | **unsolved** |
| `quadrant` | engineering problem |
| `terms` | clean |
| `harm_without_benefit` | **False** |
| `futile_treatment_risk` | **False** |
| `overtreatment_risk` | **False** |
| `measurement_gap` | **False** |

**Not one flag fires**, on a record describing roughly three hundred million
episodes a year of a self-limiting illness, most of them medicated with an
antibiotic that on the best evidence shortens the cough by under a day, with a
prescribing rate that has sat near 70-80% for four decades against a guideline
target of approximately zero.

**Four separate reasons, and each is a different hole.**

**1. `capability: unsolved` for an illness everybody recovers from.**
`intervention` is `symptomatic` because that is literally what treatment
achieves — nothing shortens this illness — so the ladder files acute bronchitis
beside depression and ME/CFS. This is #225's third bullet in its purest form:
**the ladder describes what TREATMENT achieves and has no rung for *resolves on
its own*.** `coccidioidomycosis` forced the observation with a stratum; this
record is the whole entity. It is left standing rather than fudged, because the
schema breaking in public is the point of a corpus.

**2. The toll is per-patient and the harm is per-population.**
`harm_without_benefit` requires a non-clean toll. One patient taking one
unnecessary antibiotic course has a `minor`, transient toll — diarrhoea, rash,
thrush — and that rating is honest. **`minor` × three hundred million is not
minor**, and nothing in the schema multiplies. Inflating the severity so the
flag fires would be fitting the instrument to the answer.

**3. Most of the harm lands on somebody who is not the patient.** The resistance
selected by an unnecessary course is paid by whoever gets the resistant
infection later. #51 logged this externality for tuberculosis and visceral
leishmaniasis — where the *residue* was the transmission reservoir. Here the
externality is not the disease at all, **it is the treatment**, and the register
still has no field for a harm to third parties.

**4. There is no blocker kind for a clinician knowingly doing the wrong thing.**
`adherence` is used throughout this corpus for patients: taking the tablet,
accepting the test. The blocker here is prescriber behaviour under time
pressure, diagnostic uncertainty and expected patient demand — and it is filed
as `policy` because nothing fits better. **The most documented behavioural
failure in medicine has no home in the taxonomy.**

**A fifth thing, smaller and stranger.** `access` reads 0.95 and means nothing:
what is recommended for this illness is an explanation and time, both free and
universal. `reach = efficacy × access` assumes there is something to reach people
*with*, and here it produces 0.285 — a low delivery score for a benign,
self-limiting, universally survived illness.

**And the `moved:` entry is a non-move, deliberately.** `from: 0.30, to: 0.30`,
dated 2001, recording that guidelines said antibiotics are not indicated and
**prescribing did not fall.** `moved:` exists so a second pass is a comparison
rather than a fresh opinion; the comparison here is four decades of accumulating
evidence changing the axis by nothing.

**One honest counter-argument is recorded in the record and should not be lost.**
"Antibiotics do not work for acute bronchitis" is true of the *population* and
may be false of a patient nobody can identify — *Mycoplasma*, *Chlamydia
pneumoniae* and *Bordetella pertussis* do cause a minority and do respond. The
stewardship argument rests on an average, which is a weaker foundation than the
confidence with which it is usually asserted.

---

## 229. I shipped a check that called 58 correct entries defects · **closed**
*Forced by:* being asked to work through the 58 `also` findings from #227's new
sub-entity check, and looking at what `also` is for before starting.

The check reported, 58 times: *"`also: pernicious anaemia` resolves to
`MONDO:0008228` **pernicious anemia** — a DIFFERENT Mondo entity. `also` is read
as equivalences, so this files a distinct thing as an alias."*

**`also` is not read as equivalences, and three places in this repository say
so.** SCHEMA.md defines it as *"synonyms people actually search for"*.
`resolve_mondo.py` states the rule at length and in capitals — search aliases
*"which may be broader or narrower than the entity"*, and it *"never decides
anything"*. And the field's **only consumer in the entire codebase** is
`web/query.js`, which concatenates it into the free-text `name` field.

**Somebody typing `pernicious anaemia` should land on the `anaemia` record. That
is this field working.** All 58 were correct.

**How it happened is worth more than the fix.** The check was written the same
afternoon as `#227`, whose real finding was that Mondo lacks terms the register
needs. Generalising from "the ontology is missing our distinctions" to "our
aliases are somebody else's terms" felt like the same shape and is the opposite
claim — one is about the ontology being too coarse, the other asserts the
register is being sloppy. **The `duodenal ulcer` story was in the docstring I was
editing**, and I read it as evidence that `also` must be equivalences, when it is
the record of learning that `also` must *never* be trusted as one.

**Reframed rather than deleted, because the list turned out to be useful.** These
are the `also` entries Mondo holds as **entities in their own right** — candidate
sub-records or strata the register currently folds into a parent. Read that way
it earns its place beside the strata check, and several entries are records the
corpus already suspects it is over-merging:

| record | aliases Mondo holds separately | the record's own view |
|---|---|---|
| `non-hodgkin-lymphoma` | DLBCL · follicular · MALT · Burkitt | already `strata`; the record calls its own average *"meaningless"* |
| `echinococcosis` | cystic · alveolar | `holes` says the two forms *"diverge completely"* |
| `mesothelioma` | pleural · peritoneal | — |
| `osteoporosis` | postmenopausal · glucocorticoid-induced | — |
| `head-neck-cancer` | oral cavity · tongue | the record holds four subsites as one entity |
| `prion-disease` | fatal familial insomnia · kuru | already `strata` |

**One tension is left standing for a person to settle.** The pre-existing scope
audit warns on `also` entries Mondo scopes broad or narrow — currently
`hearing-loss: deafness` and `lymphatic-filariasis: elephantiasis`. Both are good
search aliases under the schema's own definition, so that check has a milder
version of the same framing problem. It is **not** changed here: it is
pre-existing, it is two findings, and it has a defensible purpose as a hedge
against some future consumer reading `also` as equivalences — which is exactly
what `resolve_mondo --apply` once did. **But `warn` implies a defect, and by the
schema these are not defects.**

**The general lesson.** A check is a claim about what the data should be, and
this one was written without reading the field's own definition — in a
repository where that definition appears three times, once in the file being
edited. **The register's rule is derive-never-store because a stored verdict
cannot be argued with; a check encodes a verdict too**, and this one would have
produced 58 "corrections" degrading a working search field.

---

## 230. The register's eukaryotic-pathogen coverage tracks control programmes, not burden · **open**
*Forced by:* auditing protist coverage before writing `toxoplasmosis`, and
finding the same bias the fungal pass had found a day earlier.

**Before this record the register held four protist diseases and every one was
vector-borne:** malaria, visceral leishmaniasis, Chagas, sleeping sickness. All
four have an insect vector and an established control programme.

**Absent entirely:** *Toxoplasma*, *Entamoeba*, *Giardia*, *Trichomonas*,
*Naegleria*, *Acanthamoeba*, *Babesia*. *Cryptosporidium* appeared only inside
`diarrhoeal-disease`. Every one of those is waterborne, foodborne, congenital,
sexually transmitted or free-living — **no vector, and no programme.**

That is exactly the fungal pattern: before this week the corpus held one fungal
record, `mycetoma`, which is a neglected tropical disease with a WHO listing.
Two kingdoms, one bias: **what got recorded is what somebody already runs a
programme against**, and the register's own rule is that records are chosen for
structural diversity, not importance. This is neither — it is chosen by
inheritance from whoever chose first.

**Three structural facts the protist pass established, worth keeping:**

**"Protist" is not a natural kind and there is no shared drug story.**
Apicomplexa, kinetoplastids, metamonads, amoebozoa and heterolobosea are about
as related to one another as we are to fungi. The fungal argument — *four drug
classes against a kingdom, because they are eukaryotes* — does not transfer.
There is no coherent "antiprotozoal class" to be missing.

**Except the apicoplast, which is the best drug target in eukaryotic
pathogens.** Apicomplexans carry a relict non-photosynthetic plastid from a
swallowed alga: essential, prokaryote-like, and **absent in humans.** It is why
clindamycin and azithromycin work against *Plasmodium* and *Toxoplasma* at all.
**And the register already contains the negative control**: *Cryptosporidium*
lost its apicoplast, and `diarrhoeal-disease` records that it has *"no useful
drug… hard to culture and hard to screen against."* The one apicomplexan that
discarded the target is the one with nothing to aim at. **That is checkable and
should be checked.**

**Protists split across `protective-immunity` the way fungi did.** Malaria is the
flagship *no natural template* case in FND-O-0009. *Leishmania* is the opposite —
infection confers durable immunity and deliberate inoculation was historically
practised — and consistent with that, the VL record frames its vaccine gap as an
elimination-endgame problem rather than an immunological mystery. `toxoplasmosis`
sits with *Leishmania*: natural infection protects against reinfection, **and a
live attenuated vaccine is licensed for sheep.**

**Two records now show the veterinary-product asymmetry** — `coccidioidomycosis`
has a canine vaccine, `toxoplasmosis` an ovine one, and neither has a human
product. In the first the obstacle is purely `no-sponsor`; in the second it is
partly a real design constraint, since a live parasite that establishes lifelong
cysts cannot be given to the seronegative pregnant women and immunosuppressed
patients who most need it. **Same asymmetry, different cause**, which is worth
keeping straight before it becomes a slogan.

**Also found:** the register has **no syphilis, gonorrhoea, HPV or herpes
record.** STI coverage is HIV, hepatitis B and chlamydia.

---

## 231. `residue` now holds damage to someone who was never treated · **open**
*Forced by:* `cryptosporidiosis` (FND-D-0115), which tripped
`tool.test.js`'s residue guard on its first build.

The schema defines `residue` as **what the disease leaves in someone it was
cured in** — tuberculosis scarring a lung it was cleared from. The guard exists
to stop it drifting into *damage a disease is still doing*, which belongs on the
axes; it already carries two argued exceptions, `dracunculiasis` and `marburg`,
where an episode ended on its own and left sequelae.

**Cryptosporidiosis is the third and it stretches the field past both.** The
diarrhoea resolves, so the episode-ends test is satisfied. But the residue is
**stunting and cognitive deficit**, and the birth-cohort evidence attaches it to
infection that caused *no diarrhoea at all*. So the damage lands on a child who
was never ill enough to be diagnosed, never treated, and never cured — and
`residue` is now holding it because no other field can.

**Three things this makes visible.**

**The definition should move, not the record.** *"What the disease leaves behind
after the acute episode, whether or not anyone treated it"* covers all three
exceptions and the original tuberculosis case. The current wording quietly
assumes every consequential infection is diagnosed.

**And it is entangled with #182 and #228.** The harm here is not death, not
treatment toll, and not a named disability — it is a child ending up shorter and
behind. The register's magnitude is deaths; this record's `deaths` is 50,000 and
its probable larger harm has no column. **The residue incidence is 0.20 of an
infected population numbering in the millions, and the schema cannot multiply a
fraction by a denominator** (#228).

**The evidence is association, not intervention, and the record says so.** No
trial has shown that preventing the infection prevents the deficit, and the
confounding — poverty, unsafe water, coinfection, prior malnutrition — is
severe. It is recorded because the harm is probably real and otherwise invisible,
and filed as an `evidence-incomplete` blocker rather than asserted.

---

## 232. Two consecutive records declined to rate survival, which makes #226 urgent · **open**
*Forced by:* `toxoplasmosis` and `cryptosporidiosis`, written back to back.

Both declined a `survival` block, for the same stated reason: across the whole
entity almost everybody survives, and the informative population is a narrow
severe one — cerebral toxoplasmosis, malnourished children under five. Rating
either would have been the **fourth** instance of scoring a named severe
subpopulation, after `asthma`, `hypertension` and `coccidioidomycosis`, which
#226 logged as a pattern needing a rule that was never written.

**So the register is now accumulating unrated survival on exactly the records
where the axis would say something**, which is a worse outcome than either
answer. Declining twice was the disciplined choice given no rule exists; doing it
a third time would be avoidance.

The candidate rule, from #226 and unchanged: **narrow only when the excluded
population has no mortality question at all, and say so in the horizon.** Both
records satisfy it — nobody has a mortality question about latent toxoplasmosis
or about cryptosporidiosis in a well-nourished adult. **Adopting it would let
both be rated immediately**, and would retrospectively license the three existing
instances rather than leaving them as unexplained precedent.

---

## 233. Sexually transmitted infection was two records, and the pair that fixed it breaks the magnitude fields · **open**
*Forced by:* checking STI coverage while discussing phage therapy, and finding
it was **HIV and hepatitis B**. An earlier pass had reported chlamydia as
present; that was a false positive — the match was `trachoma`, ocular
*C. trachomatis*, a different disease of a different organ.

`syphilis` (FND-D-0116) and `gonorrhoea` (FND-D-0117) were added. Still absent:
**HPV, herpes simplex, genital chlamydia, trichomoniasis.**

**The two new records are exact inverses and that is why both were written.**
Two sexually transmitted bacteria, managed in the same clinics by the same
people for eighty years:

| | syphilis | gonorrhoea |
|---|---|---|
| resistance | **none, ever** — penicillin has never failed | lost **six drug classes** in sequence |
| what fails | the delivery chain: antenatal screening, follow-up, supply | the drug itself |
| survival gain | +0.11 | **+0.0009** |

Nothing about how the two are managed explains the difference. **The difference
is that one organism is naturally competent and the other is not.**

**AND GONORRHOEA BREAKS THE REGISTER'S MAGNITUDE FIELDS COMPLETELY.**
82 million infections a year. `deaths: 0` — genuinely, not as an artefact.
Survival 0.999 → 0.9999, **the smallest non-zero gain in the corpus**, an order
of magnitude below `covid-19` and `asthma`, which were the previous worst cases
of #221's compression. Every ranking view in this register would place it near
the bottom.

**Its actual burden is tubal infertility, ectopic pregnancy and neonatal
blindness** — and the first of those is not death, not treatment toll, and not a
named disability. **It is a future child who does not exist.** `residue` is
carrying it because nothing else can, which is the third record in a week to
stretch that field past its definition (#231), and **no ranking view in this
register reads `residue`.**

**Two smaller things the pair established.**

**`amr-infection`'s scope has now done damage twice in a week.** It is named for
*multidrug-resistant bacteria* and its content is hospital organisms with
stewardship and infection control as levers. `invasive-aspergillosis` found
antifungal resistance had nowhere to live; `gonorrhoea` is a community organism
acquired by healthy people during sex, and none of that record's levers touch
it. **The entity needs splitting or renaming, and its own `holes` said so before
either record arrived.**

**Both `moved:` entries on `gonorrhoea` are non-moves, recorded deliberately.**
`efficacy` has been stable at 0.95 for eighty years *across six drug classes*,
because a replacement was always found. It would stay stable right up to the
point where one was not. **A field that cannot fall until it falls
catastrophically is a bad instrument**, and the register has no way to express a
number whose stability is the warning sign.

---

## 234. A survival gain of zero means two opposite things · **closed**
*Forced by:* `genital-herpes` (FND-D-0118), and it was nearly missed by
declining to rate it.

`survival_gain` is `treated − untreated`, and the snapshot listed every record
where it was zero under the dashboard heading **"where treatment bought no extra
life at all."** Four records qualified — `alzheimers`, `huntington`,
`prion-disease`, `rabies` — with untreated survival of 0.45, 0.0, 0.02 and 0.0.
For those the sentence is exactly right and it is the most uncomfortable figure
on the page.

**Genital herpes has a gain of zero because nobody dies of it.** Untreated
survival 0.9999, treated 0.9999. Listing it beside rabies under that heading
would have been true, useless, and read as damning.

**Two different claims had one derivation:** *medicine buys no life against a
course that kills you*, and *there was no death to buy against*. The second is
not a finding about medicine at all.

Fixed by guarding `zero_gain` on untreated survival below 0.95 — deliberately
loose, meaning "essentially nobody was going to die of this anyway".

**And the dashboard test caught the second half within a minute.** `zero_gain`
now returned 4 while its linked query `gain:0` still returned 5 — the exact
failure gaps.md #214 was written for, *a figure whose link disagrees with it is
worse than a figure with no link*. The fix was to make the concept **expressible
rather than to add a flag**: a new numeric field `untreated:` in the query
language, and the link became `gain:0 untreated:<0.95`. That respects the
standing rule — *derive a flag when it names a concept the register has, never
to dodge a gap in the grammar* — because this needed two ordinary terms, not new
grammar.

**The process lesson is the one worth keeping.** Two records earlier
(`toxoplasmosis`, `cryptosporidiosis`) survival was left unrated on the argument
that the axis would say nothing useful, and #232 warned that a third decline
would be avoidance. **Rating this one exposed a derivation bug that had been
live since the axis was built.** Declining would have left it — the bug needed a
record where a zero gain meant something harmless, and every such record had
been skipped for looking uninformative. *A row that says nothing about the
disease can still say something about the instrument.*

---

## 235. The public map told visitors rabies has "a treatment that works" · **closed**
*Forced by:* `hpv-infection` (FND-D-0119) deriving `capability: preventable` and
landing in the `known & treatable` quadrant, which prompted checking what that
cell actually says on the page.

`capability_tier` maps `preventable` into the top tier — correctly, since #66
added that value precisely so measles and rabies would not read as *nothing can
be done*. But `web/index.html` labelled the cell **"a mechanism, and a treatment
that works"**, and five records sit in it for which the treatment does nothing:
`measles`, `influenza`, `dengue`, `hpv-infection` — all `intervention:
symptomatic` — and **`rabies`, which is `intervention: none` and kills
essentially everyone who reaches symptoms.**

**The register was publishing, on its landing page, that rabies has a treatment
that works.** Fixed to *"a mechanism, and something that works — a treatment, or
a vaccine."*

**The derivation was right and the sentence under it was wrong**, which is a
distinction worth keeping: no rating changed, no query changed, and every test
passed throughout — because the tests check that figures match their queries and
that cells match the derivation, and **nothing checks that a cell's prose
matches what is in it.** CLAUDE.md already warns that naming is load-bearing on
a public page and that the quadrant must never read as a bare verdict; this is
the same failure one layer down, in the explanatory sentence rather than the
label.

---

## 236. HPV makes gaps.md #109 unavoidable: a preventable disease has no coverage field · **open**
*Forced by:* `hpv-infection`, where the only number that matters cannot be
written down.

The HPV vaccine is among the best in medicine — titres an order of magnitude
above natural infection, durable beyond fifteen years, and **Scotland reporting
no cervical cancer at all among women vaccinated at twelve or thirteen.** Global
coverage is roughly a fifth to a quarter of adolescent girls, against a WHO
target of ninety percent.

**Neither figure has a field.**

- `prevention` is an enum. It says `prophylaxis` and cannot say *how well* or *to
  how many*.
- `efficacy` and `access` describe **the treatment**, by definition — and the
  treatment here is wart removal, which is irrelevant to everything this record
  is about.
- `delivery` is withheld from `preventable` records on purpose (#109), because a
  delivery figure for a treatment that does not exist would be a number about
  nothing.

So a disease that a vaccine prevents almost perfectly, reaching a fifth of the
people who need it, **produces no low number anywhere in this register.** Its
`reach` is 0.36 and describes cryotherapy for warts.

**This is #109 with teeth.** That entry recorded the withholding as correct and
noted the gap; HPV shows the gap is not a corner case — it applies to every
`preventable` record, and for measles, HPV and dengue the prophylaxis coverage
figure is the single most decision-relevant number the record could carry.

The 2022 WHO single-dose recommendation is the sharpest demonstration: it roughly
halved the cost per girl protected at a moment when supply constrained coverage,
and the register logs it as a **non-move** — `prophylaxis` before and after.
That is the third non-move logged in a fortnight, after `gonorrhoea`'s two, and
they are all the same complaint: **an enum cannot record a change in degree.**

---

## 237. A screening programme was narrowed on evidence, and the register has no other · **open**
*Forced by:* `genital-chlamydia` (FND-D-0120).

The logic was as good as public health logic gets: a common asymptomatic
infection, an excellent cheap test that works on posted urine, a cheap generic
cure, and a serious late consequence. Screen widely, treat early, prevent
infertility.

**It has not clearly worked at population level.** The Netherlands ran an
implementation trial over three rounds, found no reduction in prevalence, and
discontinued it. England refocused its National Chlamydia Screening Programme in
2021 from everyone aged 15-24 to women only, on insufficient evidence of benefit
in men. The POPI trial did reduce pelvic inflammatory disease — **and much of the
PID occurred in women who tested negative at baseline**, meaning the infections
that mattered were acquired after the screen.

**Two explanations compete and both are actionable, and nobody has separated
them.** *Frequency*: a single opportunistic test cannot catch an infection
acquired next month, so the programme was under-dosed rather than wrong.
*Denominator*: the risk of tubal damage from asymptomatic screen-detected
infection may be far lower than the figures derived from hospitalised PID, in
which case the programmes were sized against an inflated estimate. **The answer
decides whether to intensify screening or stop it.**

**The register recorded this as `prevention` moving BACKWARDS, from `prophylaxis`
to `risk-reduction`** — the fourth backwards `moved:` entry in the corpus, and
the only one caused by evidence rather than by supply failure, price rises or
system decay. **It is a deterioration in the axis and an improvement in honesty,
and the schema cannot tell those apart.**

**And the record carries a `disputed` blocker that would invert the
intervention.** The arrested-immunity hypothesis holds that treating early —
which is what screening does by design — interrupts the partial natural immunity
that repeated exposure builds, leaving treated people *more* susceptible. High
reinfection rates and flat prevalence under scaled-up screening are consistent
with it; so is ongoing exposure from untreated partners, which is the obvious
confounder. **If it is right, the programme is not merely less effective than
assumed but counterproductive.** It joins `amr-infection`'s phage entry,
`toxoplasmosis`'s psychiatric association and `mesothelioma`'s asbestos trade as
the corpus's four `disputed` blockers — and it is the only one where the disputed
claim is about *the register's own recommended intervention*.

**The triad is the other finding.** Syphilis, gonorrhoea and chlamydia are
managed in the same clinics by the same people with the same tests:

| | resistance after eighty years |
|---|---|
| **syphilis** | none, ever |
| **gonorrhoea** | six drug classes lost in sequence |
| **genital-chlamydia** | none worth naming |

**Nothing about how they are managed explains the spread.** Gonorrhoea's natural
competence does. That is an argument that antimicrobial resistance is a property
of organisms at least as much as of stewardship — which is not how
`amr-infection` frames it, and that record's levers are all stewardship.

---

## 238. The STI branch is complete, and the largest record in it has no programme to argue about · **open**
*Forced by:* `trichomoniasis` (FND-D-0121), the sixth and last of the pass that
began when STI coverage turned out to be HIV and hepatitis B (#233).

**Six records, ~440 million new infections a year, and every one of the six is
`curable`, `managed` or `preventable`.** Not one is blocked on not knowing what
to do:

| record | incidence/yr | reach | what actually blocks it |
|---|---:|---:|---|
| trichomoniasis | **156M** | 0.32 | **nobody is looking** |
| genital-chlamydia | 130M | 0.48 | whether screening works at all |
| gonorrhoea | 82M | 0.52 | the last drug class |
| hpv-infection | 40M | 0.36 | vaccine coverage, ~20% |
| genital-herpes | 24M | 0.45 | a neuron you cannot sacrifice |
| syphilis | 8M | 0.44 | the antenatal chain, and penicillin supply |

**The largest is the one nobody counts.** Trichomoniasis exceeds chlamydia,
gonorrhoea and syphilis combined, is **notifiable almost nowhere**, has no
screening recommendation, no elimination target and no advocacy organisation —
and is routinely omitted from the multiplex panel a patient is *already having*
for the two infections they are less likely to have. It has the lowest `reach`
in the set. **The other five records' blockers are arguments about programmes;
this one's is that there is no programme to argue about.**

**Three findings the record carries that are not about trichomoniasis.**

**The dose was wrong for women for fifty years.** Single-dose metronidazole was
standard from the 1960s; a trial reporting in 2017 found seven days roughly
halved repeat infection in women, and guidelines followed around 2021. Nothing
was discovered — somebody finally compared two schedules of a 1959 generic in the
commonest curable STI on earth. **It is the cheapest efficacy gain in the
register and a standing argument for funding trials of things nobody expects to
be interesting.**

**And the obvious intervention against its worst association made things worse.**
Trichomoniasis is consistently associated with preterm birth. A randomised trial
in 2001 gave metronidazole to infected pregnant women and found **more** preterm
delivery in the treated arm. Never satisfactorily explained, never overturned.
**That belongs beside FND-O-0009's three vaccine harms**: an association plus a
plausible mechanism plus an obvious intervention is not a prediction, and acting
on it hurt people. The register rates this record's `residue` conservatively
because of it, and says so.

**It also closes the protist argument from #230.** *Trichomonas* is a metamonad —
a third lineage, as distant from the apicomplexans as we are from fungi. It has
no mitochondrion and runs anaerobic metabolism in a **hydrogenosome**, which is
exactly what metronidazole exploits: reductive activation in a compartment we do
not have. **Two protist lineages, two unrelated exploitable organelles, and
`cryptosporidiosis` — which discarded its apicoplast and has neither — with no
drug.** #230 argued there is no shared antiprotozoal target and that the
exploitable difference has to be found lineage by lineage. Three lineages in, it
holds.

**What remains absent:** the four HPV-attributable cancers with no record — anal,
vulvar, vaginal, penile — and *Mycoplasma genitalium*, which has a resistance
trajectory resembling `gonorrhoea`'s and arrived too recently to have a
programme either.

---

## 239. Treating one disease made another one resistant, and no field holds it · **open**
*Forced by:* `mycoplasma-genitalium` (FND-D-0122).

Single-dose azithromycin was the standard cure for `genital-chlamydia` for two
decades. Co-infection with *M. genitalium* is common, there was no test for it
until around 2019, and a single macrolide dose that reliably cures chlamydia does
not reliably clear *M. genitalium* — **it selects within it.** Macrolide
resistance now exceeds fifty percent across much of the high-income world and
approaches eighty in some populations.

**The register has said four times that it cannot express a harm landing on
somebody other than the patient** — tuberculosis's transmission (#51),
`acute-bronchitis`'s resistance externality (#228), `syphilis`'s doxycycline
prophylaxis, `visceral-leishmaniasis`'s PKDL reservoir. **This is the sharpest
instance yet, because the harm landed on a different disease**, and it is now
part of why chlamydia treatment moved to doxycycline.

**And it makes an existing derivation visibly blind.** `overtreatment_risk`
requires real capability, `prognostic: none`, and a `costly`/`harsh` toll. This
record has the first two exactly — **nobody can say which infection needed
treating** — and a `minor` toll, because a course of antibiotics does the patient
little harm. **The price of overtreating here is paid in resistance, by people
not yet infected.** The flag does not fire. `acute-bronchitis` fails it for the
same reason. **Two records where the overtreatment guard is blind precisely
because the harm is not the patient's.**

**Three other things this record establishes.**

**It is the proof of concept for what `gonorrhoea` is asking for.**
Resistance-guided therapy — detect the 23S rRNA mutation from the diagnostic
sample, choose the drug accordingly — raises cure from roughly 40% to above 90%
and is standard in Australia and parts of Europe. `gonorrhoea`'s `diagnosis`
blocker asks for exactly this capability and does not have it. **It exists, it
works, and it needs no new science** — which is the strongest available argument
for funding the equivalent in an organism that has lost six drug classes.

**It is the second "do not screen" record and the reason is new.**
`genital-herpes` carries the first, on the grounds that a diagnosis harms the
person. Here the recommendation is not about the patient at all: screening leads
to treatment, treatment selects resistance, and the prognostic gap means nobody
can say the infection needed treating. **Do not look, because looking harms
people who are not yet infected.**

**And `mechanism: partial` is carrying two things that have come apart.** The
*organism* is exceptionally well characterised — smallest self-replicating genome
known, the template for the synthetic-cell work. The *disease* is not: whether it
causes pelvic inflammatory disease, preterm birth or infertility is unresolved.
The axis conflates organism and disease, and **this is the clearest record in the
corpus where knowing everything about a pathogen tells you nothing about whether
it matters.** Every rating here — `residue: minor`, the screening position, the
urgency of a second drug class — is downstream of a natural-history question
nobody has run the cohort for.

**A sixth #227 instance, and the most extreme.** Mondo has terms for *Mycoplasma
haemocanis* (dogs), *haemofelis* (cats), *wenyonii* (cattle), *gallisepticum*
(poultry) and *pulmonis* (rodents), plus two human *Mycoplasma* syndromes — and
**nothing for the sexually transmitted human pathogen with fifty percent
macrolide resistance.** The record points at the genus.

---

## 240. The four HPV cancers nobody screens for, and the one place cervical prevention generalised · **open**
*Forced by:* writing `anal-cancer`, `penile-cancer`, `vulvar-cancer` and
`vaginal-cancer` (FND-D-0123 to 0126) after `hpv-infection` flagged that four
HPV-attributable cancers had no record at all.

`hpv-infection` argued that **cervical prevention did not generalise, and the
reason is anatomy rather than biology** — the cervix is accessible, has a
recognised precursor with a long dwell time, and can be sampled cheaply and
repeatedly. Writing the four confirms it and finds one exception.

**THE EXCEPTION IS ANAL CANCER, AND IT IS RECENT.** The ANCHOR trial reported in
2022, was stopped early for efficacy, and showed that treating high-grade anal
lesions in people with HIV reduced progression to cancer by roughly 57%.
Guidelines followed in 2024. **Anal screening had been plausible-by-analogy with
the cervix for twenty years and unproven.** It is the first demonstration that
cervical-style secondary prevention transfers to another HPV site, and the
binding constraint is now the supply of clinicians trained in high-resolution
anoscopy — **a logistics blocker created by a trial result.**

**A pattern across three of the four that the register had not named.** Anal,
penile and vulvar cancer are all **on or near the surface of the body**, all
diagnosable by looking and biopsying, and **all routinely diagnosed late for
reasons of embarrassment.** Penile lesions wait many months and often over a
year; vulvar symptoms are treated as thrush for years; anal symptoms are
attributed to haemorrhoids.

**In `penile-cancer` the mechanism is sharper than distress.** The delay converts
an organ-preserving problem into an amputating one — early disease is treated by
glansectomy or laser with comparable cure, the same disease a year later requires
penectomy. **Stigma is not causing suffering there, it is causing stage
migration**, which is a different and far more actionable claim than the one
`genital-herpes` records. And the most persuasive intervention is telling men
that the organ is usually preserved if they come early, **which is now true and
is not widely known.**

**Two toll reductions the register would otherwise never have recorded.**
`anal-cancer`: Nigro's chemoradiation protocol in the 1970s replaced
abdominoperineal resection with permanent colostomy — survival changed little,
the toll changed by an entire operation. `vulvar-cancer`: radical en-bloc
vulvectomy with butterfly incision gave way to wide local excision with sentinel
node biopsy, with equivalent survival and a fraction of the disfigurement,
wound breakdown and lymphoedema. **Both are among the largest toll reductions in
the corpus and neither appears in any history of cancer progress**, because
survival-ranked accounts cannot see them.

**And the same organisational fix is unmade twice.** Sentinel node biopsy in
vulvar cancer and organ-preserving surgery in penile cancer both require case
volume that rare cancers do not generate outside specialist centres. The UK's
penile supranetwork improved both preservation and survival. **Two rare genital
cancers, one centralisation argument, and most health systems have made it for
neither.**

**`vulvar-cancer` is the odd one and should probably be two records.** Only ~40%
is HPV-driven; the rest arises on **lichen sclerosus**, carries TP53 mutation,
occurs in older women, is more aggressive — and is the **larger** share. So a
vaccine removes the minority of that record. The precursor is a skin condition
diagnosable by looking and treatable with topical steroid, and it is routinely
missed. **The commoner and worse half of the cancer has the thinner evidence
base**, which is a pattern the register keeps finding wherever a disease has a
viral and a non-viral form.

**`vaginal-cancer` carries the register's only transplacental carcinogen.**
Clear cell adenocarcinoma traced in 1971 to **diethylstilbestrol given to the
patients' mothers in pregnancy** — the first demonstration that a drug could
cause cancer in the next generation, decades later. Its `moved:` entry records a
prevention gain that consisted of *stopping doing something*. The schema has no
field for a harm that crosses a generation, and this is the only record that
needs one.

**A process note.** `vaginal-cancer` was written with `predictive: n/a` and the
validator refused it — **the third time**, after `cryptococcal-meningitis` and
`genital-herpes`. Every time the reasoning was the same: one treatment for
everybody, so nothing to select between. Every time `efficacy` was well below
0.85, meaning a substantial minority are not cured and nobody can say which.
**`n/a` is attractive because it looks clean, and the rule catching it three
times is the rule working.**

---

## 241. Eight age-related records are waiting on "nobody knows the mechanism", and there is no obstacle for it · **open**
*Forced by:* testing the geroscience hypothesis against the corpus and then
trying to tag the twelve untagged knowledge blockers in the age-related set.

**The geroscience test first, because it produced the tagging job.** The claim is
that aging is the upstream driver of most chronic disease, so intervening on it
moves everything downstream at once. Against 16 age-related, non-cancer,
non-infectious records carrying the largest mortality block in the register:

**Not one names aging as the thing that is blocked.** Word-bounded, three mention
ageing at all, and all three use it against the hypothesis — `alzheimers` as a
cause of *diagnostic delay*, `parkinsons` stating *"age-standardised prevalence is
rising, which means this is not only ageing"*, `atrial-fibrillation` listing it as
a risk factor that *"does not identify the individual"*.

**What they do share is CREATE.** Five to seven of the sixteen are waiting on
tissue repair — replace lost myocardium, regrow hair cells, reverse fibrosis,
restore cartilage. **The chronic block converges on an operation, not on a
cause**, which supports the CRUD framing (`Engpass/crud.md`) and not geroscience
as the operative frame.

**Two limits stated plainly.** An earlier comparison — 4 of 16 age-related records
carrying obstacle tags against 16 of 16 infectious — was **confounded and is
retracted**: the infectious records were written and tagged this week, and two of
those obstacles did not exist when the age-related ones were written. And the
register cannot refute geroscience, only report that **nobody writing 126 records
reached for aging as the blocker.** A geroscientist would say the corpus reflects
specialty silos; testing the strong claim needs multimorbidity data the register
does not hold.

### The tagging pass, and what it could not place

Twelve age-related knowledge blockers carried `obstacles: []`. **Four were
tagged. Eight could not be, and they share a shape.**

Tagged: `hearing-loss` → `tissue-repair` (birds regrow hair cells and we do not —
the purest instance of that obstacle in the corpus); `heart-failure` →
`tissue-repair` (*"any way to replace lost muscle"*, and the obstacle names
myocardium in its own question); `atrial-fibrillation` → **both**
`who-progresses` (nothing predicts which ablation recurs) and `tissue-repair`
(there is no treatment for atrial fibrosis at all); `osteoporosis` →
`who-progresses`, **stretching it**, because the divergent outcome follows a drug
rather than a disease.

**The eight that could not be tagged are all waiting on the same thing:**

| record | what it is actually waiting on |
|---|---|
| `alzheimers` | *the amyloid hypothesis was right and was not enough* |
| `hypertension` | *"essential" means cause unknown, and it is 90-95% of the disease* |
| `parkinsons` | *nobody knows why the neurons die* |
| `osteoarthritis` | *what flips the chondrocyte, and what causes the pain* |
| `type-2-diabetes` | *whether this is one disease at all* |
| `obesity` | *why the set point defends itself* |
| `chronic-kidney-disease` | *why young farm workers develop kidney failure* |
| `cataract` | *how to protect a protein for eighty years in a cell with no turnover* |

**Engpass has no obstacle for "nobody knows the mechanism", and if it did it
would immediately be among the largest in the register** — eight citations from
this set alone, before looking at the other 110 records. Its absence is why the
age-related block looked untagged and therefore unshared, which is what made the
first geroscience comparison misleading.

**This is the pending `mechanism-unknown` / `no-candidate` split arriving from a
third direction.** Engpass surfaced it from the untagged pile; `coccidioidomycosis`
forced it by having a vaccine blocked by money rather than ignorance; and it now
turns out to be the reason the register cannot say what the commonest chronic
diseases have in common. **The split is no longer a tidiness question.**

One further decision it forces: `who-progresses` currently means *the same
insult, a divergent outcome*. `osteoporosis` files a divergent response to a
**drug** there. If the obstacle is meant to cover only disease progression, that
link is wrong and the record is the one that makes the choice unavoidable.

---

## 242. Adding a record exposed a hole in an existing one, and nothing checks for that · **open**
*Forced by:* `cmv-infection` (FND-D-0128) and `varicella-zoster` (FND-D-0127),
added to close the herpesvirus gap after `genital-herpes` turned out to be the
family's only entry.

**`hearing-loss`'s prevention section named rubella, measles, mumps,
meningococcal, pneumococcal and *Haemophilus influenzae* type b — and omitted
congenital cytomegalovirus, which is the leading non-genetic cause of childhood
sensorineural hearing loss in high-income countries.** The omission has a
structure: every infection that section lists is prevented by a vaccine, and
**CMV is the one that is not.** Vaccination removed congenital rubella and CMV is
what was left underneath it.

That link is now written into both records. **The general problem is that
nothing found it.** The register has guards for a figure disagreeing with its
query, an index disagreeing with its derivation, a `mondo:` id that does not
resolve, a residue on a record with no capability — and none for **one record
naming a cause that is another record.**

**A cheap check exists and would have caught this.** Every record's prose is
searchable and every record has a `name` and an `also` list. A pass asking *which
records name an entity that is itself a record, without linking to it* would have
flagged `hearing-loss` the moment `cmv-infection` was written. It would also have
found the `mycoplasma-genitalium` ↔ `genital-chlamydia` resistance link and the
`syphilis` ↔ `rheumatic-heart-disease` benzathine penicillin shortage before I
noticed them by hand.

**This is the case for `sqlite_probe.py` doing more than it does.** Cross-record
questions are exactly what a join answers and what `query.js` cannot express —
and the probe already demonstrates the shape by validating the `attempts/`
drafts' cross-references against real record slugs.

**Two other things the herpesvirus pass established.**

**`varicella-zoster` names ageing as the mechanism, and #241 said nothing did.**
Zoster incidence rising steeply after sixty is one of the clearest clinical
manifestations of immunosenescence there is, and the record says so. It is a
genuine counter-example to that entry's finding — and it is also a special case,
because here ageing has a single measurable consequence, where in Alzheimer's or
osteoarthritis it would be a label rather than a mechanism. **The finding stands
with one exception and the exception is instructive.**

**And the recombinant zoster vaccine is the third instance of FND-O-0009's
counter-pattern.** `hpv-infection` (virus-like particle) and `childhood-pneumonia`
(stabilised pre-fusion F) showed a structural insight substituting for a natural
template. Shingrix is the third and it substitutes for something worse than an
absent template: **nature's answer here is cell-mediated immunity that decays
with age**, and an engineered adjuvant restores protection in exactly the
population where vaccines characteristically fail. Above ninety percent, sustained,
in people over eighty. **The obstacle's `why_hard` should be updated a second
time.**

---

## 243. The cross-record check is built, and it found two more of the same shape · **open**
*Forced by:* #242 — `hearing-loss` omitting congenital CMV, and nothing in the
register noticing.

Built into `sqlite_probe.py` as a `claims` table: **one record naming another as
a cause.**

**A bare mention is not a finding, and the first version proved it.** Matching
record names against record prose produced **254 unlinked pairs** — `stroke`,
`tuberculosis` and `malaria` appear in dozens of records as comparisons and
comorbidities. That is a list, not a work-list. **Requiring causal language near
the name** — *leading cause*, *causes*, *drives*, *complication of* — cuts it to
**53 claims**, of which 15 already cite the other record's slug, 18 are mentioned
back, and **27 are neither.**

**Two hits of the CMV shape, found automatically:**

**`obesity` is named as a cause by `uterine-cancer`, `colorectal-cancer` and
`liver-cancer`, and its own record says *cancer* generically while naming none of
them.** Exactly the structure of the CMV omission: a record enumerating its
effects at the wrong level of specificity, so the link exists in one direction
and evaporates in the other.

**`epilepsy` is named as a cause by `taeniasis-cysticercosis` and
`onchocerciasis`**, and names neurocysticercosis back but not onchocerciasis —
where the association with nodding syndrome and onchocerciasis-associated
epilepsy is real.

**And the check corrected itself on the first run.** It reported the
cysticercosis link as unreciprocated, which was wrong: `epilepsy` does name it,
as *neurocysticercosis*, while the record is called *taeniasis and
cysticercosis*. **Records refer to each other in clinical rather than canonical
form**, so reciprocity now matches `name` *and* `also`. That removed a whole
false-positive class and is the kind of error the register's own `also` field
exists to absorb.

**Roughly half of the 27 remain false positives and the classes are
predictable**: comparison prose (*"unlike X"*, *"the same arithmetic as X"*),
shared risk-factor lists (*"ischaemic heart disease, stroke, COPD and lung
cancer"*), and sub-entity collisions — *portal hypertension* matching the
`hypertension` record. The report says so and says to read rather than apply.

### Fixing the first hit exposed two bugs in the check

**`obesity` said *"roughly thirteen cancers"*** — a count, where every other
downstream record (`type-2-diabetes`, `hypertension`, `ischaemic-heart-disease`,
`stroke`, `cirrhosis`, `osteoarthritis`) was named by slug. **A number is not a
link, and a count is the form an omission takes when it looks like precision.**
Eight of those cancers are records here and are now named, with the strength of
each association stated — including that `thyroid-cancer`'s is weakest and
entangled with the overdiagnosis that record is largely about.

**Then the check kept flagging it.** The reciprocity test matched a record's
`name` and `also` — and **not the backtick slug, which is how this register
actually links.** `obesity` cited `uterine-cancer` and the test looked for
*uterine cancer*. Fixed; the work-list fell 27 → 23 and reciprocated claims rose
18 → 24, meaning **four other pairs were already linked correctly and being
reported as broken.**

**And the report contained a hand-written sentence that went stale on contact.**
It said in prose that `obesity` was the clearest hit; `obesity` was then fixed,
and the sentence stayed true-looking and false **inside a generated file** —
which is precisely the failure that broke `index.md` (#224), reproduced inside
the tool built to catch that class of failure. The headline example is now
computed from the data, with the fixed cases named as history.

**The general lesson is about what the register's guards were shaped like.**
Every existing check tests a record against itself (`check.py`), against a
derivation (`index.md`, the snapshot), or against an external source
(`mondo_sync.py`). **None tested a record against another record**, because the
schema has no field for a relationship between diseases — `blockers[].obstacles`
is the only cross-record link and it points at Engpass, not at Nordstern. So the
corpus accumulated one-way causal claims for 128 records with nothing looking.

---

## 244. I over-claimed two superlatives in one record, and both were checkable · **open**
*Forced by:* `bacterial-meningitis` (FND-D-0129), written to close a gap
`hearing-loss` had been pointing at since it was written.

The record as first drafted said the `window` field had been *"built for"* it and
that its survival gain was *"one of the largest in the register, comparable to
`hat` and `visceral-leishmaniasis`."* **Both were false and both took one query
to disprove.**

- **86 of 129 records carry a `window`**, and **19 close in hours** — cholera,
  maternal haemorrhage, infant diarrhoea, asthma, sepsis, myocardial infarction.
  The field was not waiting for this record.
- **The gain of +0.73 ranks eleventh of ninety-two.** `hat` and
  `type-1-diabetes` are +0.95; `visceral-leishmaniasis` and `cystic-fibrosis`
  +0.90.

Both are corrected in place, and the correction is stated in the record rather
than the claim quietly deleted.

**What survived is narrower and is the actual finding.** Nineteen records have an
hours-scale window; in cholera the patient is visibly dehydrated, in maternal
haemorrhage visibly bleeding, in sepsis visibly ill. **Here the first hours look
like a viral illness**, and the classical signs arrive after the window has
partly closed or, in infants, never. **The window is short *and* the prompt to
act is absent for most of it**, which is a harder problem than either alone and
is a claim the corpus supports.

**THIS IS THE THIRD SUPERLATIVE I HAVE GOT WRONG IN THIS CORPUS**, after
`cryptosporidiosis`'s *"the register's first `tooling` blocker"* (there were
eleven) and the `attempts_extract` modality count (searched whole records instead
of failure sentences). **The pattern is specific: comparative claims — first,
only, largest, most — written from impression while composing prose, in a corpus
that can answer every one of them in a single query.**

**And there is a check.** Records make comparative claims in fixed language:
*the first*, *the only*, *the largest*, *the highest*, *the worst*, *nothing else
in this register*. Those phrases are extractable, and roughly half of them name a
field the register holds. A pass that lists every superlative alongside the query
that would test it would not verify them automatically — but it would put them
in front of a person, which is all the `mondo_sync` and cross-record checks do.

**It belongs in `sqlite_probe.py` with the others**, and it is the same family:
every existing guard checks a record against a derivation, and none checks a
record's *prose* against the corpus it is describing.

---

## 245. `animal-translation`, and a boundary violation I introduced and did not test for · **open**
*Forced by:* a proposed blocker on the translatability of animal research —
*"mice are not humans, and humans are not mice"* — and Geoffrey West's scaling
argument alongside it.

**It is an Engpass obstacle rather than a Nordstern blocker**, because it cuts
across diseases and the useful direction is backwards. `animal-translation`
(FND-O-0010), and it is **bottom-up**: two records already name it in a blocker.

- **`als`** states it more sharply than any external source: *"the SOD1 mouse
  became the standard preclinical gate for all ALS, including the 98% of patients
  without SOD1 mutations, and it predicted a long series of human failures."* A
  faithful model of 2% of a disease made the entry requirement for all of it.
- **`cataract`**: *"Aldose reductase inhibitors work in diabetic animal models
  and not in people."* A whole drug class carried into human trials on animal
  data.

**The framing was sharpened on the way in, and the corpus did the sharpening.**
The proposed claim was that an animal result teaches *nothing*. **The register
falsifies that**: insulin came from depancreatised dogs and is `type-1-diabetes`'s
founding intervention; polio vaccine needed monkeys; antibiotics, cytotoxic
chemotherapy, monoclonals and the GLP-1 agonists reshaping `obesity` all came
through animals. **The defensible claim is not that the gate is empty but that it
is uncalibrated** — nobody can say in advance which results transfer, and nothing
states the transfer function. That is a claim about calibration, and it is
checkable.

**Two statistical problems with the 92% figure are recorded in the obstacle's own
`holes`.** It is close to the base rate of the whole enterprise — phase 2 failure
alone runs near 70% — so attributing all attrition to one stage overstates it.
And **a screening filter cannot be scored on its false positives alone**: the
compounds the gate stopped never reach humans and are unobservable, so the true
negatives are missing from the denominator. That cuts both ways, and the other
direction is this record's strongest claim — **an unknown number of workable
human therapies discarded at a gate with no right to stop them, and nobody can
estimate it.**

**Four uses of the same tool, and the record covers one.** As a *gate* (this
obstacle); as an *absence* — `cryptosporidiosis`, `heds` and enteric dysfunction
are blocked by there being no model at all, which is the opposite complaint with
the opposite fix; and as the *sole permissible evidence* — `marburg`'s
regulatory Animal Rule, where a human efficacy trial cannot ethically be run.
Scoping is stated in the record so it cannot drift into meaning anything.

### And the boundary test caught something I broke

`sqlite_probe.py` read `Engpass/obstacles/` directly — **Nordstern code reaching
into the Engpass source**, which `test_boundary.py` exists to forbid. I wrote it
that way several turns ago **and did not run the boundary suite**, so it sat
undetected while I ran every other check.

Fixed by moving the tool into `Engpass/`, which is the correct home rather than a
workaround: **it joins both registers, and only one side is permitted to see
both.** Engpass reads Nordstern's built artifact; Nordstern does not know Engpass
exists. A joining tool belongs on the side allowed to know.

**The lesson is about which suites get run.** `check.py`, `test_check`, `node
--test web/` and the Engpass build were run after every change this week;
`test_boundary.py` was not, because it guards an architectural rule rather than
the data, and nothing about editing records suggests running it. **A guard that
is only run when you remember it is a guard on your memory.**

---

## For Sperrwerk

**A checker over this register is the obvious next artifact**, and it is
arithmetic over a declaration, exactly like the kernel:

- a `capability: curable` claim requires a citation naming a finite regimen and a
  cure fraction
- any `efficacy` or `access` value requires a `src` that is not `recall`
- `mechanism: established` requires the chain to be stated in the witness, not
  merely asserted
- `contested: true` requires the parties
- a record with any axis absent must derive `unrated`, never `unsolved`
- the derived table in `index.md` must be reproducible from the records, so the
  index cannot drift

That last one is the same test that keeps `Sperrwerk/examples/insulin.yaml` from
drifting from its generator.

## 246. Capability had no weight, so the register could not say where to work · **closed**

*Forced by:* the question *"should fndtn work on rabies or Huntington's, or on
heart disease — those seem horrific and there is practically nothing, but tons of
people get heart disease?"*

The register could state both halves and **could not put them together.** Every
view was either a capability view that treated a disease killing 59,000 as
equivalent to one killing nine million, or a burden view that said nothing about
whether anybody could do anything.

**`knowledge_gap` and `delivery_gap` close it** — see SCHEMA.md. And the answer
turned out to dissolve the question rather than settle it:

**The premise about rabies was wrong.** It is `capability: preventable`. The
vaccine and post-exposure prophylaxis work; 59,000 people die because they do
not reach them. Its blockers are `cost`, `logistics`, `policy`, `knowledge`.
**Rabies is a delivery failure wearing a horror costume**, and the derivation has
to exclude it explicitly or the arithmetic reports the opposite of the truth
(gaps.md #109, appearing for the third time).

**The premise about heart disease was also wrong.** `stroke` carries a knowledge
gap of ~3.3M and `ischaemic-heart-disease` ~2.25M — deaths that remain **after
perfect delivery.** Half of stroke patients get no meaningful benefit from
anything medicine has. These are not solved diseases with a distribution
problem.

**So: ~3.3M for stroke alone, against ~91,000 attributed deaths across all eight
records where `efficacy` is zero.** The biggest untouched-by-knowledge problems
are inside the common diseases, and no previous view could show it.

### Three things this cannot do, and one of them is a real objection

- **It is mortality-shaped.** Four of the five diseases medicine is most
  completely helpless against — `huntington`, `me-cfs`, `msmds`, `heds` — have no
  attributed deaths, and `heds` declares `deaths: 0.0` outright. **Engpass
  already recorded the rule this obeys: rank by records, not by burden.** The
  figure says how many records it cannot see, and that is the mitigation, not a
  fix.
- **`efficacy` is not a mortality reduction.** It is the fraction of patients
  whose course is altered, and `stroke`'s own field calls itself *"A CONSTRUCT,
  not a measurement."* The product is a shape.
- **IT IS THE MULTIPLICATION #221 REFUSED.** `gain × incidence` was rejected for
  making a confident number out of two `src: recall` guesses. The defence is that
  this one is built for rank rather than level — but **the dashboard prints a
  total**, and a total is a level. Published with the caveat attached because the
  asymmetry is the register's founding claim; the sentence goes before the chart
  does if a sourcing pass contradicts it.

*Left open:* whether the totals should be shown at all before any `judged` scalar
is sourced. 0 of 1,158 are.
