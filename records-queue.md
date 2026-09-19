# Records queue — the non-mortality pass

Started 2026-09-01, after four records (`glaucoma`, `retinopathy-of-prematurity`,
`refractive-error`, `migraine`) established that **the register was built to see
things that kill people** and most of what disables people does not.

Those four carry roughly two billion people and **zero attributed deaths between
them.** Every one has a `# NO survival: BLOCK` comment explaining why the axis
does not apply — which is four independent instances of the same missing thing.

---

## FIRST: wire up `ylds`, before writing more records

**The field already exists and is orphaned.** Four records carry it —
`low-back-pain` 60M, `anaemia` 50M, `osteoarthritis` 22M, `asthma` 13M YLD/year
— `check.py` mentions it once in a path list, and `query.js` has never heard of
it.

This matters more than the next seven records, because it is the fix for a
complaint that has now appeared four times in a row:

- **`knowledge_gap` and `delivery_gap` return `None` for every record without
  `deaths`.** Computed on `ylds` instead, `migraine` and `refractive-error`
  become visible and are probably enormous.
- **The burden-weighted dashboard chart does not draw any of the four.**
- **Axis A's disability sibling** — the piece `bucket-design.md` has listed as
  missing since it was written — needs a burden metric to weight against, and
  this is it.

**The order matters.** Populating `ylds` on 130 records is a sourcing pass; GBD
publishes these figures, which puts them in the `sourceable` tier — *the only
tier where a citation settles the question*. So this is also the register's best
available first sourcing target, and better than `moved:` because one dataset
answers all of it.

**Do not invent YLD figures from recall.** A YLD is prevalence × disability
weight, and the disability weights are a published, argued-over table. A recalled
YLD is two guesses multiplied. Either source them or leave the field absent —
`unrated` is never `unsolved`.

---

## The seven, with what each would exercise

Ordered by what they would teach the schema, not by burden.

### 1. `clubfoot` — the best efficacy-to-cost ratio in the register

~1 in 800 births, roughly 150–200k a year, overwhelmingly in countries with no
paediatric orthopaedics. **The Ponseti method** — serial casting, a percutaneous
tenotomy, then bracing — corrects the large majority at a cost of tens of
dollars, needs no operating theatre, and **can be delivered by trained
non-physicians.** Untreated, the child walks on the side or top of the foot for
life, with the exclusion from school and work that follows.

**What it exercises:** the counterpart to `refractive-error` — a near-total cure,
almost free, reaching a fraction. And a distinctive blocker the register has not
recorded: **four years of night bracing**, where the failure mode is adherence
in a child who is now walking normally and whose family cannot see the point.

### 2. `obstetric-fistula` — the register's clearest case of social death

~2 million women living with it, 50–100k new cases a year. Caused by obstructed
labour without a timely caesarean: the tissue necroses, leaving continuous
incontinence. **Surgical repair cures most of them.** What follows untreated is
not medical — it is divorce, ostracism and destitution.

**What it exercises:** a `residue` that is entirely social, which the schema
currently has no way to weight; and the fact that it is a **complication of
another record's failure** — `maternal-haemorrhage` and emergency obstetric
access — which raises the cross-record link question `sqlite_probe.py` was built
for.

### 3. `endometriosis` — the worst diagnostic delay in the register

~190 million women. **Diagnostic delay commonly quoted at seven to ten years**,
which would be the longest in the corpus by a wide margin. Definitive diagnosis
historically required laparoscopy; treatment is hormonal suppression or surgery,
recurrence is common, and hysterectomy is not reliably curative.

**What it exercises:** the delay itself, and **the second instance of the gender
dimension** after `migraine` — a condition with no objective test, historically
dismissed, predominantly affecting women. One instance is an observation; two is
a pattern the register should decide how to record, and `migraine`'s holes
already flag that the current framing may be dodging it.

### 4. `diabetic-retinopathy` — a complication record, and the AI screening case

Leading cause of blindness in working-age adults. ~100 million affected,
vision-threatening in a large minority. Prevented by glycaemic and blood-pressure
control, treated by laser and anti-VEGF.

**What it exercises:** it is a **complication of `type-2-diabetes` and
`type-1-diabetes`**, and the register has few of those — it would test whether
complications should be records or strata. And it is the clearest case in
medicine of **autonomous AI diagnosis**: retinal photography with automated
grading is deployed, regulator-cleared, and is exactly the substitution
`retinopathy-of-prematurity`'s tooling blocker wants and cannot get.

### 5. `macular-degeneration` — where the treatment burden *is* the blocker

~200 million worldwide, leading cause of blindness in over-50s in high-income
countries. Two diseases in one name: **wet AMD**, transformed by anti-VEGF
injections — and the injections are **monthly, into the eye, forever**, which has
become a capacity crisis in every system that adopted them. **Dry AMD /
geographic atrophy**, where until very recently there was nothing, and the
complement inhibitors approved in 2023 have contested benefit.

**What it exercises:** `ongoing` as a genuine binding constraint rather than a
descriptor — a treatment that works and whose delivery volume is the limit. And
a rare case of a **recently approved treatment whose benefit is disputed**, which
`standing: disputed` exists for.

### 6. `anxiety-disorders` — the largest missing mental health record

~300 million people, consistently top-ten YLD. The register holds `depression`,
`bipolar` and `schizophrenia` and not this.

**What it exercises:** whether it is one entity at all — generalised anxiety,
panic, social anxiety and phobias are rated together by GBD and treated
differently. Effective treatment exists (CBT, SSRIs) and **the binding constraint
is therapist supply**, which is the `refractive-error` shape again: the skill,
not the product.

### 7. `cleft-lip-and-palate` — the team problem

~1 in 700 births, ~200k a year. Surgical repair in infancy is highly effective
and **requires a team over years**: surgeon, paediatric anaesthetist, speech and
language therapy, orthodontics, ENT for the associated hearing loss. Untreated:
feeding failure, speech that cannot be understood, hearing loss, and in some
settings abandonment.

**What it exercises:** `congenital-heart-disease`'s constraint — *a programme,
not a product* — in a cheaper and more tractable form, plus the childhood window
for speech development that closes the way `hearing-loss`'s and
`refractive-error`'s do.

---

## Also absent, noted and not queued

`neck-pain` (top-ten YLD, and `low-back-pain` already flags the shared problem
that these are complaints rather than diseases) · `tinnitus` · `infertility` ·
`incontinence` · `psoriasis` · `eczema` · `spina-bifida` · `autism` ·
`intellectual-disability`.

**`neck-pain` is the one most likely to be a mistake to leave out**, on burden
alone. It is left out because it would duplicate `low-back-pain`'s schema
problems exactly without teaching anything new — which is the corpus-before-
schema rule working, but it is a judgement and it is arguable.

---

## Two schema decisions this pass has forced, still open

1. **A field for harm displaced onto someone who is not the patient.**
   `retinopathy-of-prematurity` (sixteen infant deaths per case of blindness
   prevented, from oxygen restriction) and `migraine` (valproate teratogenicity)
   are two independent instances in three records. Both currently live in prose
   and are invisible to every derived view. **Two instances is the bar this
   corpus normally uses.**
2. **`held-off` is absorbing too much.** Three of the four new records land
   there — `glaucoma`, `refractive-error`, `migraine` — and they are not alike:
   glasses, eye drops and a monthly biologic for a disease that halves rather
   than remits. The bucket may need splitting, or `ongoing` may need to carry
   more weight in the rule.
