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

## Named across records and deliberately NOT a record

**`skin-microbiome-mosquito-attraction` — ruled out 2026-11-07, not forgotten.**
Skin bacteria metabolise sweat into the volatiles *Anopheles* follows, and
composition decides how attractive a person is. **It is a mechanism inside
`malaria` and a claim on an Engpass obstacle, and it is not an entity**: nobody
has it, nobody is treated for it, and it has no burden, no window and no axes.
It is written into `malaria`'s `witness.mechanism`, blocked in that record's new
`candidate-untested` blocker, and held as a `derived` claim on
`microbiome-control` (FND-O-0018). Recorded here because a striking mechanism
with a disease attached is exactly the thing that gets queued as a record by
mistake, and because the queue should be able to say *no* in writing.

**The general rule, from three instances — gaps.md #251.** A thing named across
many records is one of two things. **An agent** becomes a Nordstern record: EBV
did (#247), *H. pylori* did (#249). **A capability** cannot — it has no patients
— and becomes an Engpass obstacle instead: `microbiome-control` did. **A
mechanism becomes neither.** It stays inside the records that name it.

## Also absent, noted and not queued

`neck-pain` (top-ten YLD, and `low-back-pain` already flags the shared problem
that these are complaints rather than diseases) · `tinnitus` · `infertility` ·
`incontinence` · `psoriasis` · `eczema` · `spina-bifida` · `autism` ·
`intellectual-disability`.

**`neck-pain` is the one most likely to be a mistake to leave out**, on burden
alone. It is left out because it would duplicate `low-back-pain`'s schema
problems exactly without teaching anything new — which is the corpus-before-
schema rule working, but it is a judgement and it is arguable.

### `familial-hypercholesterolaemia` — noted 2026-10-10, out of the PV discussion

Absent from the 145, and it should not be. It is the register's cleanest
**germline control.** A clearance pathway broken from conception, and the
disease arrives on schedule in childhood — xanthomas and coronary disease in
the teens in the homozygous form. That is the test that separates an inherited
defect from an acquired one, and it is the reasoning that correctly places
`polycythaemia-vera` as somatic: if V617F were germline, PV would be a
paediatric disease, and it is not.

It would also exercise the one-slot problem `polycythaemia-vera` hit, from the
other side: statins and apheresis suppress, while PCSK9 inhibition, evinacumab
and the gene-editing trials argue for a higher rung on the same record.

Axes unrated here on purpose.

---

### `acute-myeloid-leukaemia` — written 2026-10-19, out of the PV discussion

Absent from the 146 and not in this queue either, which was an oversight rather
than a decision. `polycythaemia-vera` names transformation to acute leukaemia as
its terminal outcome seven times, puts it inside its own `efficacy` figure, and
records that an older PV treatment *caused* it — and the disease it transforms
into had no record. A register that holds the precursor and not the endpoint is
not holding the natural history.

It earns its place twice over as **the control for `cml`.** Same lineage,
opposite answer: one translocation and one drug against a few dozen driver
combinations and nine approvals between 2017 and 2020 that moved median
survival by months. Written as FND-D-0147.

**One rating left deliberately unsettled: `intervention`.** It is recorded as
`disease-modifying` on the reasoning that the ladder should describe the modal
patient, and the modal AML patient is seventy. The case for `curative` is real —
a third of all patients reach five years, APL is cured at 99%, and curative
intent is standard wherever intensive therapy can be given. The call turns on
whether the ladder means "a cure exists" or "the typical patient is cured",
which is a register-wide question this record happens to put most sharply.
`uveal-melanoma` answers it the other way round and gets `curative` for it.

---

### `ebv-infection` — written 2026-11-05, out of the infection-attributable tally

Absent from the 148, **named as a cause in five records**, and the fourth-largest
carcinogenic infection on earth by attributed cases — about one percent of all
cancer worldwide, on the order of a quarter of a million cases a year (IARC 2024
tally; gaps.md #247).

**The reason it is absent has a shape.** `h-pylori-ulcer` entered this register
as an *ulcer*, not as a bacterium. `hpv-infection` entered as an infection
because its cancers forced it. **EBV has no disease of its own that anybody wants
a record for** — its own illness is infectious mononucleosis, self-limiting — and
everything that makes it matter is somebody else's record: `nasopharyngeal-
carcinoma` (built on it entirely), endemic Burkitt lymphoma inside
`non-hodgkin-lymphoma`, a share of `gastric-cancer`, Hodgkin lymphoma and
post-transplant lymphoproliferative disease (neither held), and
`multiple-sclerosis`, which rates it **near-necessary** at a thirty-two-fold risk
increase with essentially no MS in the EBV-negative.

**What it would exercise.** First, the scoping question `hpv-infection` left open
in its first hole — infection and its cancers as separate records, or the cancers
as strata of the infection — asked in the hardest place: **more than nine in ten
adults alive carry this virus and essentially none of them get any of it.**
`nasopharyngeal-carcinoma` already states that necessary-and-nowhere-near-
sufficient problem precisely, and it is the same problem `gastric-cancer` has
with half of humanity carrying *H. pylori*.

Second, and this is the part no held record can express: **two records already
contain the same mass-prevention argument about a near-universal benign
infection, independently, and neither can see the other.** `gastric-cancer`
says eradicating *H. pylori* at population scale means treating roughly half of
humanity to prevent cancer in one or two percent of them, with the resistance
cost landing in `amr-infection` (gaps.md #130). `multiple-sclerosis` says
vaccinating against EBV to prevent MS means vaccinating everybody against a
near-universal benign infection to prevent a disease in a fraction of a percent
of them. **Same structure, different agent, different organ, no field.**

Third, `prevention`. There is no EBV vaccine; `multiple-sclerosis` records
candidates in early trials. A record would have to say what the axis means when
the prophylaxis is real, plausible and absent.

**Written as FND-D-0149 the same day**, and the ratings it landed on are
`mechanism: established`, `intervention: symptomatic`, `prevention: none`,
`ongoing: none` — so the derived capability is `unsolved` and the record carries
⧉, because two of its three strata are `curable`. All three of those are argued
in the record's own `holes` rather than asserted. What writing it found is in
gaps.md #247.

---

### `h-pylori-infection` — written 2026-11-07, out of the protective-edge question

**The agent had a record and it was pointed at the wrong entity.** `h-pylori-ulcer`
is FND-D-0001, written to be the register's reference `curative`, and it is scoped
to peptic ulcer disease. Eight records name *H. pylori* and gaps.md #247's
coverage table listed that one file as the register's entire holding for the agent
IARC credits with about four percent of all cancer worldwide. **That is
`ebv-infection`'s problem one record later with the opposite cause**: there the
agent had no node at all, here it had one aimed at a disease.

**What it exercises that nothing else does.**

- **A cure with no delivery, and nothing missing but the looking.** Every other
  carcinogenic infection in the register needed something invented — a vaccine for
  HPV and hepatitis B, a drug class for hepatitis C, nothing at all exists for
  EBV. This one needs a fortnight of generics that have existed since the 1990s,
  and `access` against the colonised is **0.10**. It is a `diagnosis` blocker
  wearing a cancer's burden.
- **An `access` denominator that is not patients.** Four in five carriers will
  never be ill, so the figure is honest about this record and **corrupting to any
  aggregate that includes it.** Written up as a hole; it is a schema problem.
- **The register's longest and quietest `window`** — opens in early childhood,
  closes over decades on a histological stage with no symptom, and what degrades
  is not the treatment's effect but its worth.
- **The first `resistance` backwards move since gaps.md #248 needed the word.**
  Clarithromycin resistance took `efficacy` down with nobody learning anything.
- **A non-move that is the loudest entry in the file.** A three-dose oral vaccine
  reported 71.8% efficacy in a phase 3 trial of 4,464 children in 2015 and
  `prevention` is still `risk-reduction` eleven years later.
- **`standing: disputed`, used for the first time in this neighbourhood**:
  clarithromycin-resistant *H. pylori* was a WHO high-priority pathogen in 2017
  and was dropped in the 2024 revision, which a published open letter contests.

**Where it landed.** `mechanism: established`, `intervention: curative`,
`prevention: risk-reduction`, `ongoing: none`, efficacy 0.90, access 0.10 —
`curable`, `restored`, `clean`, reach 0.09, and `contested: true` for the
eliminate-it-versus-ancient-commensal argument, which the record states from both
sides and does not settle.

### `oesophageal-cancer` — queued 2026-11-07, out of the H. pylori protective edge

**Flagged as absent in `gastric-cancer`'s holes since that record was written,
and now flagged twice.** Two separate things want it and neither can be written
without it.

**The cardia boundary.** Gastric and oesophageal adenocarcinoma meet at the
gastro-oesophageal junction, the two are classified differently in different
decades, and `gastric-cancer` already carries a hole saying its cardia and
non-cardia strata are diverging in opposite directions with different causes.
A boundary dispute needs records on both sides of the boundary.

**The protective edge, which is the new reason.** *H. pylori* is inversely
associated with oesophageal adenocarcinoma (pooled OR 0.52) and with Barrett's
(0.64), the association concentrating in cagA-positive strains and vanishing
against reflux controls. **That edge cannot be written, because one of its two
ends is not a record** — which is gaps.md #247's finding repeating itself
exactly: the cross-record check searches for edges whose both ends exist, so a
missing node is outside the query rather than merely missed. #247 found it for
EBV and the fix was to write the node. Same shape, different agent.

What the record would also hold that nothing else does: a cancer whose dominant
risk factors are **reflux and obesity** rather than an infection or a toxin, so
its upstream record is `obesity`; the two-histology split, squamous and
adenocarcinoma, with different causes, different geography and opposite time
trends, which is `strata` doing real work; Barrett's oesophagus as a
surveillance-and-ablation programme, which is a `window` with a measurable
screening arm; and a dismal survival figure in a disease that is often
operable-in-principle and rarely caught in time.

**Why it is queued rather than written.** It is a sixth upstream entity the
queue has produced, the queue already has seven numbered records ahead of it,
and the `ylds` job at the top of this file still comes first.

## The injury path — opened 2026-11-07, and deliberately slowly

**Of 150 records the only injury is `snakebite`.** No road injury, no falls, no
burns, no drowning, no self-harm, no interpersonal violence — one of the three
top-level cause groups in global burden accounting is absent. The register knows
it obliquely: `icd-coverage.md` records that hip fracture deaths code to the
external cause, which is why `osteoporosis` carries zero.

### Why it is a different kind of entity, and why that is the reason to go slowly

Every record in this register describes **a course**: something begins, proceeds,
and is intervened upon. **An injury is an event.** It is over in seconds, and
what remains is not a disease progressing but a person in a permanently altered
state — and often a trap, because the state closes off the means of escaping it.
That is a shape the schema has never had to hold, and five fields bend under it:

- **`mechanism` stops being a biology question.** For a road injury the mechanism
  is kinetic energy, a vehicle, a road layout and a speed limit. `established`
  would be true and useless. The axis was built to ask *do we understand the
  disease process*, and here the process is physics.
- **`prevention` leaves medicine almost entirely.** Helmets, seatbelts, speed
  limits, building codes, smoke alarms, water-heater thermostats, pool fencing,
  cookstove design, means restriction. The enum describes medical prophylaxis and
  the actors are `legislator`, `government` and `manufacturer`. This is
  `osteoarthritis`'s neuromuscular-training blocker — *the best prevention is
  delivered by people no health ministry commissions* — as the normal case rather
  than the exception.
- **`window` collapses to minutes and becomes the whole outcome.** The golden
  hour; fluid resuscitation in the first day of a major burn. Orders of magnitude
  shorter than anything here, and `caught_in_time` would be dominated by whether
  an ambulance exists, which is not a clinical variable.
- **`residue` stops being a footnote and becomes the record.** Contracture,
  amputation, paraplegia, disfigurement, dependency. gaps.md #60 already says
  `residue` has no capability of its own and sometimes the residue is the treatable
  part; **injury is that gap's limiting case**, where the residue is the entity and
  the acute event is the footnote.
- **And the burden is an incidence over an exposure somebody underwent** —
  gaps.md #159 exactly, which names `road-injury` as one of three records it is
  waiting on before deciding whether `kind` needs a value the enum cannot
  express.

**Axis A of `buckets.yaml` is where this will show up first.** Injury should land
in `changes-you` almost uniformly, and that bucket already holds 53 records. A
block arriving there by a completely different route is either fine or evidence
that `changes-you` has been hiding a distinction, and **the only way to find out
is to write one record and look.**

### The order, and the rule

**One record, then stop and read what it broke.** The corpus-before-schema rule
that governs the rest of this repository applies with more force here than
anywhere, because the first injury record will probably force a field, and six
written in a pass would all need rewriting around it.

1. **`burns` — WRITTEN 2026-11-07 (FND-D-0151).** It was the sharpest available
   test of the thesis above rather than the largest number, which is what a first
   record should be, and **it broke six things — gaps.md #250.** The residue *is* the record. The access gradient is extreme
   and is about a burns unit rather than a product — `maternal-haemorrhage`'s
   *hospital-grade capability, not a product* argument in a second place. The
   prevention is cheap, non-medical and unowned. The social consequence invites
   direct comparison with `obstetric-fistula`, the register's existing social-death
   record. And it is mostly children, mostly in low-income settings.
2. **`road-injury` — next**, on burden and because gaps.md #159 is explicitly
   waiting for it. **Read #250 before writing it**: `burns` has already forced
   `kind`, `prevalence`, `window` and the blocker-sign question, and road injury
   will hit all four again plus the chosen-exposure problem #159 is actually
   about. Do not write it until the decisions in #250 are made, or the second
   record will have to be rewritten around them.
3. **Then one of `spinal-cord-injury` or `traumatic-brain-injury`**, whichever the
   first two argue for — the purest residue-is-the-record shapes, and `tbi` would
   also give `disorders-of-consciousness` an upstream record it currently lacks.

Not queued and named so nobody thinks they were forgotten: falls, drowning,
poisoning, self-harm, interpersonal violence, occupational injury, frostbite and
heat illness.

### The `gaps.md` entry now exists, because something forced it

This section originally closed by saying there was no gap entry yet, because
every entry in that file names the record that forced it and nothing here had
been forced by anything. **`burns` was written the same day and gaps.md #250 is
what it broke** — six fields, one Engpass obstacle with its own counterexample
inside it, and the discovery that a blocker can mean *the technique arrives and
kills people* rather than *the treatment does not arrive*.

Four of the six predictions in this section held. **Two were wrong**: `residue:
catastrophic` was expected to be new and eleven records already use it, and
`mechanism` turned out to break in a more interesting way than predicted — not
because `established` is unavailable but because it is *true and buys nothing*.

## Three records that other files called "queued" and this one did not

**Found 2026-11-07.** `road-injury`, `opioid-use-disorder` and
`alcohol-use-disorder` are referred to as *(queued)* nine times across `gaps.md`
and inside two records — `cirrhosis` names two of them in its own prose — and
**not one of them appeared anywhere in this file**, including the
noted-and-not-queued list below.

That is worse than untidy, because **gaps.md #159 builds a decision rule on
them**: *"Watch `road-injury`, `opioid-use-disorder` and whichever maternal record
comes next; three records with a `kind` the enum cannot express is the threshold
this register has used before."* A threshold waiting on records nobody had
queued cannot fire. Third instance this week of the same failure, after #184's
stale counts and `h-pylori-ulcer`'s scope hole — **a cross-reference to a record
is a claim, and nothing checks it.**

- **`road-injury`** — now queued above, second in the injury path.
- **`opioid-use-disorder`** — genuinely wanted and not queued here before. It is
  #159's cleanest case (*the chosen exposure is a prescription for something
  else*), it is #147's flagship from the patient's side (*the disease is a
  byproduct of capability*), and `low-back-pain` and `osteoarthritis` both carry
  its toll without it existing. **Queued, after the injury path's first record.**
- **`alcohol-use-disorder`** — named by `cirrhosis` as its largest upstream cause.
  Queued behind `opioid-use-disorder`, on the same argument as every other
  upstream entity this queue keeps producing.

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

## Two from the negative-trial pass — queued 2026-11-09, out of gaps #252

Both arrive from `Lp(a)HORIZON` and `CARDIO-TTRansform`, and the reason to write
them is the same in each case: **the register has no row where a validated
causal target was hit hard and the patient was not helped**, so the most
informative drug result of 2026 has nowhere to land.

### `attr-cardiomyopathy` — queued, and the stronger of the two

Transthyretin amyloid cardiomyopathy. What it exercises that nothing here does:

- **`efficacy` with an *on top of what*.** It is the register's first entity
  where the same drug is effective as monotherapy and adds nothing on existing
  care — nominally 0.71 off a stabiliser, no additional benefit on one. Writing
  the record is what would force the missing clause in `efficacy.units`.
- **A disease that was rare until the test got good.** Wild-type ATTR is a
  diagnosis of the old, was long read as ordinary heart failure, and its
  prevalence moved because imaging moved rather than because anything else did —
  which is #170's territory from a different side.
- Two drug classes with different mechanisms (stabiliser, silencer) and a live
  question about whether stacking them does anything, which is a `toll` and a
  cost question at once.

Needs: a Mondo term, and the stabiliser trial numbers checked rather than
recalled. **Do not write it from the blog post** — the subgroup figures in
circulation disagree.

### `lipoprotein-a-elevation` — queued behind it, with a known problem

An inherited, lifelong, largely unmodifiable exposure present in roughly a fifth
of people. The problem is stated before it is written: **it is a risk factor, not
a disease**, so it lands squarely on #219 (*rateable only by naming the
population*) and would need its horizon stated the way `hypertension` does.

It is worth having anyway, and Lp(a)HORIZON is why: the register would otherwise
have no place to record that the single cleanest Mendelian-randomisation result
in cardiovascular medicine produced **HR 1.02** when acted on, and **HR 1.00 in
the highest-exposure subgroup**. That is a fact about the limits of causal
inference as a guide to treatment, and it has no home.

**Neither is written, and neither is first.** The injury path (`road-injury`)
keeps its place at the head of the queue; these two sit behind
`opioid-use-disorder` unless the schema question in #252 is taken up first, in
which case `attr-cardiomyopathy` is the record that forces it.

---

### `neonatal-diabetes` — written 2026-11-12, out of the bioelectricity discussion

Absent from the 161, and it arrived from an odd direction: a conversation about
whether Michael Levin can prove that bioelectricity controls development. The
honest answer was that the field is small, concentrated in one lab, and thin on
independent replication — and that the way to see what a *proven* bioelectric
claim looks like is to find one that was nailed. This is it.

**It is the register's shortest complete chain.** Glucose → ATP → the KATP
channel closes → the beta cell depolarises → insulin. An activating mutation in
`KCNJ11` or `ABCC8` leaves the channel stuck open and step three fails. A
seventy-year-old oral drug closes that channel by an ATP-independent route, so
it corrects the defect rather than working around it: **44 of 49 patients (90%)
discontinued insulin in 2006, and 93% were still off it a decade later with no
severe hypoglycaemia in 809 patient-years.** Two years from gene to tablet, with
no new molecule — the missing thing was knowing who to give it to. Written as
FND-D-0162, with real citations on three of the four `moved` entries.

It also lands next to `pku`, `wilsons-disease` and `tay-sachs` as the fourth
monogenic-disease-with-a-cheap-lever, and `window` has the same shape as
Wilson's: the lever costs almost nothing and the delay is a habit of mind.

**One rating left deliberately unsettled: `intervention`.** Recorded as
`suppressive` — the mutation is still there, the tablet is daily and lifelong,
and stopping it brings the diabetes back, which is the same reasoning that rates
`wilsons-disease` suppressive. What makes it uncomfortable is that the ladder
cannot see the difference between *one cheap tablet at a falling dose with
better control than the alternative* and *lifelong chelation with 24-hour urine
collections*. `ongoing` is doing all of that work with one word and four values.

**And the record's main finding is about the schema, not the disease.** The 2006
transfer moved **nobody** from dead to alive — insulin did that in 1922 — so the
axes record one of the most complete mechanism-to-treatment stories in medicine
as a move within `efficacy` plus a notch in `ongoing`. Nothing anywhere says
*these people stopped injecting four times a day*. `heds`, `pku`,
`type-1-diabetes` and `macular-degeneration` each carry a version of this
complaint; none states it as cleanly, because in those the treatment burden is
the status quo rather than something that was lifted. **If "same survival,
transformed life" ever becomes a field, this is the record that forced it.**
