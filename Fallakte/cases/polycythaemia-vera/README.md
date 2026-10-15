# Polycythaemia vera — case file

`FND-C-0001` · opened 2026-10-10 · active · the disease record is
[`polycythaemia-vera`](../../../entities/polycythaemia-vera.yaml) (`FND-D-0145`,
`MONDO:0009891`)

**One mutation, found in 2005, in a gene whose job is understood, in a loop whose
physiology is textbook. And the standard treatment is to take blood out.** That
gap is why this case is open.

**Who is working on it.** A nonprofit brought this disease to the register as its
first case; they are not named here until they have agreed to appear in a public
repository, which is why `case.yaml` records `named: false` rather than a blank.
The models and the mistakes are ours.

---

## 1. Where it stands

Read off the record, not re-rated here.

| | |
|---|---|
| mechanism | `established`, with four named holes |
| intervention | `suppressive` — near-normal life, treated indefinitely |
| capability / delivery | **managed**, and reach is dominated by patients never found |
| what is suppressed | the **consequence**. The clone is untouched by venesection and aspirin |

The record's own summary of the gap: PV is the sibling of chronic myeloid
leukaemia, where a drug sits in the driver kinase and the clone shrinks until it
is hard to find. Here the available kinase inhibitor is not selective for the
mutant and does not do that. **So the disease is controlled by lowering a number,
and the thing that raises the number carries on.**

---

## 2. The mechanism, step by step

One step per row. `established` means it would survive a refutation attempt.
`partial` means the step is real and its terms are not settled. `open` means we
are naming a gap, not describing a finding. **The empty cells in the last column
are the list of things worth building.**

### How certain is step 1?

**Asked directly: are we certain it is the mutation?** As certain as this kind of
claim gets, with one precise limit.

Four independent things make it causal rather than correlated. Put the mutation
into a mouse and the mouse gets too many red cells, which is the experiment that
settles direction. The patients who do not have V617F mostly have a *different*
mutation in the *same gene*, in exon 12, and get the same disease, so two
unrelated lesions converge on one phenotype through one gene. Germline mutations
elsewhere in the same signalling pathway also produce too many red cells, which
is the contrast case on our own board. And the effect is dose-dependent: a higher
mutant fraction goes with more disease, and the highest fractions with the most
thrombosis.

**The limit is that it is necessary and NOT SUFFICIENT**, and the numbers are
blunt about it. Screening a general population with a sensitive assay finds the
mutation in about one adult in thirty. The disease occurs in about one person in
a hundred thousand per year. **The mutation is roughly three thousand times
commoner than the disease.** So "it is the mutation" is true of the
erythrocytosis and false as an account of who becomes ill. What is sufficient is
the mutation plus the clone plus time, which is why this chain has twelve rows
and not one.

| # | what changes | status | where you can watch it |
|---|---|---|---|
| 1 | A single haematopoietic stem cell acquires a point mutation in *JAK2*: valine 617 becomes phenylalanine. **Somatic. One cell, during life.** | `established` | Strangschrift `jak2-sites` |
| 1b | Whether this is the FIRST event. In some patients it is; in others *TET2* or *DNMT3A* arrived first, and the order appears to matter for which disease results. | `open` — see **Q8** | — |
| 2 | Why that cell, that base, that person | `open` | — |
| 3 | V617 sits in the pseudokinase domain, which normally holds the kinase domain shut. The substitution loosens the restraint. | `established` *that it does*; `partial` on *how* | Schaltwerk `jak2-brake` → `jak2-v617f` |
| 4 | The unrestrained kinase phosphorylates the erythropoietin receptor's tyrosines and then STAT5, **with no erythropoietin bound anywhere** | `established` | Schaltwerk `jak2-stat5` |
| 5 | The off switches still work. A phosphatase removes the phosphate; SOCS1 grips the kinase's own phosphotyrosine and takes it to be destroyed. **The disease is not a broken off switch — it is a stuck on switch the off switch cannot keep up with.** | `established` | Schaltwerk `jak2-off` |
| 6 | Phosphorylated STAT5 pairs, enters the nucleus, and binds its motif in target promoters | `established` *that it does*; `open` on which targets matter here | Strangschrift `stat5-target`, Schaltwerk `transcription` |
| 7 | The mutant erythroid progenitor survives and matures **without erythropoietin**. This is the 1974 observation that waited thirty-one years for its cause. | `established` | Strombild `erythropoiesis-pv` (the one deleted edge) |
| 8 | The mutant stem cell out-renews its neighbours and the clone grows, over **decades**, from one cell to a large fraction of the marrow | `established` that it happens; its magnitude is now **measured** per person; **`open` on what the advantage is made of, and on why some clones shrink** | Strombild `clonal-escape`, and see **Q1**, **Q2**, **Q7** |
| 9 | Once enough of the marrow descends from that cell, red-cell mass rises | `established` | Strombild `clonal-escape` |
| 9b | Building that extra red cell mass **consumes iron**, and the body holds only a few grams. The growth phase draws the iron stores down, which is why a substantial share of patients are already iron deficient when they are found. | `established` | Strombild `iron` |
| 9c | The over-driven marrow suppresses hepcidin, which opens the iron gate, so **the body increases the iron supply to the clone.** Iron deficiency opens the same gate further. | `established` | Strombild `iron` |
| 10 | The kidney reads the extra oxygen and turns erythropoietin **down**, to a fraction of normal. The sensor is intact. It is shouting *enough* at a marrow that has stopped listening. **High red cells with low erythropoietin is the loop's fingerprint, and it is the diagnostic signature.** | `established` | Strombild `erythropoiesis-pv`, `clonal-escape` |
| 11 | Viscosity rises with the haematocrit, and platelets, leukocytes and endothelium are activated too. The result is thrombosis — stroke, myocardial infarction, clots in the hepatic and portal veins. **This is what kills.** | `partial` — lowering the haematocrit below 45% lowers the risk and does **not** abolish it | — |
| 12 | In a minority, the clone goes on to myelofibrosis or acute leukaemia | `open` | — |

**Steps 1b, 2, 11 and 12 have no model and no mechanism.** Step 8 is the
sharpest row in the table: we can say the clone expands, we can now put a
measured number on how fast in a given person, and we cannot say what sets that
number or why it sometimes reverses. The model is a precise statement of the
ignorance rather than a cover for it, and on 2026-10-10 that was tested when
somebody else's data contradicted it. See section 3.

---

## 3. What we got wrong

**2026-10-10 — "it's genetic, so you get bad code and a faulty protein."** That is
the ordinary framing and it fails the obvious test. If the mutation were inherited
the disease would arrive in childhood. Median age at diagnosis is about sixty.

The test is worth keeping because it generalises: **a germline defect in a
clearance or control pathway shows up early.** Familial hypercholesterolaemia is
the clean control — a cholesterol clearance pathway broken from conception, and
the homozygous form produces skin deposits in childhood and coronary disease in
the teens. It was absent from Nordstern and that argument is what queued it.

And the control *inside this very phenotype* is sharper still. Familial
erythrocytosis is germline: the erythropoietin receptor is truncated so the site
its off switch grips is simply gone. Too many red cells, from a different step,
**and it presents in childhood.** Same phenotype in words. Different age of onset,
because one defect was there from conception and the other arrived later.
Schaltwerk's `pfcp` is on the board beside `jak2-v617f` for exactly this reason.

**The resolution: V617F is somatic.** Not in the egg or the sperm, not in every
cell, not passed to children.

### "Born with it" is not the same as "inherited"

**The question that forced this section, asked 2026-10-10:** *if a child is born
with the mutation, then every cell has the faulty protein, so every cell should
be overproducing. How can a population of cells exist that does not have the
faulty protein?*

**Because the mutation was never in the egg.** Inherited means the typo is in the
fertilised egg, so every cell copied from it carries the typo, and there is no
clean population anywhere in the body. Somatic means the typo happens in **one
cell of a body that is already built.** At thirty-three weeks of gestation a
fetus is of the order of a trillion cells. One of its blood stem cells mistypes
one base while copying its own DNA. **That cell's descendants carry it. Nothing
else in the body does, because nothing else is descended from it.**

So the clean population exists for the dullest possible reason: those cells were
never copied from the mutated one. The word for a person in this state is a
**mosaic** — two genetically different populations of cells in one body.

**And nothing is silenced, and there is no other version of the protein.** The
mutant gene is transcribed, the overactive kinase is made, and it is overactive
in every cell of the clone from the first day. There is no regulation story to
find here and no second mechanism. The entire explanation is **how many cells**.
At birth that is roughly one mutant among a hundred thousand blood stem cells,
and the other ninety-nine thousand nine hundred and ninety-nine make essentially
all of the blood.

Two consequences worth stating because they follow immediately and both surprise
people:

- **It is not passed to the patient's children.** The mutation is in a blood stem
  cell, not in egg or sperm. What *is* inherited in some families is a variant
  that makes acquiring the mutation, or expanding it, a little more likely. Two
  different layers.
- **Where it lands decides whether it matters at all.** JAK2 sits under the
  cytokine receptors of blood cells. The identical substitution in a skin or
  liver stem cell would do nothing observable, which is part of why the mutation
  is so much commoner than the disease.

### "Do they have the disease?" is four questions

The first version of the table below said *disease at birth* and *relevant cells*
and assumed those were clear. They were not, and the terms are now defined once
in [`../../GLOSSARY.md`](../../GLOSSARY.md). The distinction that matters:

| state | the question |
|---|---|
| **defect present** | is the broken instruction there? |
| **cells misbehaving** | are the affected cells doing the wrong thing *now*? |
| **detectable** | would an ordinary test be abnormal? |
| **harming** | is the person being damaged? |

**"They are born with it" answers the first question only.** That is the sentence
that makes people expect a sick baby, and it is why this needed four rows.

### The two diseases, side by side, with the cell type named

| | familial hypercholesterolaemia | polycythaemia vera |
|---|---|---|
| where the mutation is | **every cell**, from conception | **one blood stem cell**, acquired later |
| how it got there | inherited from a parent | a copying error during that person's life, often before birth |
| the cells whose malfunction makes the phenotype | **liver cells that clear LDL from blood** | **blood stem cells in the marrow** |
| what share of those cells carry it at birth | **all of them** | **one in about a hundred thousand** |
| are cells misbehaving at birth | **yes, all of them.** Clearance is impaired immediately | yes, but only that one cell, which makes a thousandth of one per cent of the blood |
| is an ordinary test abnormal in childhood | **yes.** The cholesterol is high from infancy | **no.** The blood count is normal |
| what the delay before harm is made of | **accumulation.** The artery has to take the damage | **expansion, and then accumulation.** The clone has to grow first, and only then does anything start to damage the person |
| first harm, untreated | teens with two bad copies; fifth decade with one | sixth decade |
| passed to the person's children | **yes, to about half** | **no.** It is not in egg or sperm |

### So, answering the questions directly

**If you inherit it, do you start over-producing straight away?** Yes. In
hypercholesterolaemia the failure to clear LDL is running from infancy and the
blood test is already abnormal in a young child. **Nothing is waiting.** What
takes forty years is the artery accumulating the damage, which is a different
clock from the defect.

**So a germline disease has a delay too?** It does, and that is worth being clear
about because it is where the two look alike. **The difference is what the delay
is made of.** In the inherited disease the misbehaving cells are all present from
the start and the *damage* accumulates. In the somatic disease the misbehaving
cells are almost absent from the start and have to *multiply* before any damage
can begin. **Polycythaemia vera carries both delays, stacked**, which is the real
reason it presents later.

**Somatic: the mutation arrives after a functional population already exists?**
**Yes. That is exactly it, and it is the whole answer to the question.** There is
a working marrow, built normally, running normally. One of its stem cells makes a
copying error. From that moment the person has two populations: a very large
normal one that is making all of their blood, and a clone of one that is making
almost none of it. Nothing about the normal population changed, and nothing
protects it. It simply was never descended from the cell that made the error.

**And the mutation never spreads.** This is the point most worth holding onto. A
mutation cannot move from one cell to another. The only way it gets into more
cells is for the cell that has it to divide. So "the clone grew" always means
*that cell's descendants became a larger share of the marrow*, and never *the
mutation got into other cells*.

One refinement for completeness, which is a dose effect inside the clone and not
an answer to the question above: the mutant cells are usually heterozygous, so
even they carry one normal copy of the gene. Some clones later lose it, and a
mutant fraction above half marks those patients, who carry more risk.

**2026-10-10 — and then the resolution turned out to be too simple.** Lineage
work published in 2022 dated the mutation's acquisition in individual patients to
childhood, in some cases before birth. So the mutation frequently *is* early.
What takes forty years is the clone.

    the disease is not the mutation.
    the disease is the mutation x the share of your marrow descended from it x time.

**2026-10-10 — our own Strombild model was modelling the wrong thing, and we only
noticed by arguing.** `erythropoiesis-pv.strombild` has the disease as one edge
with a fixed constant. That is a marrow already taken over: right about the steady
state, silent about the forty years, and therefore unable to express the question
the case is actually about. A share and a rate is a stock and a flow, so the
natural history became `clonal-escape.strombild` the same day.

**2026-10-10, second pass — the model's own falsifier fired, in four hours.**
Section 8 lists route R1 as "measure the growth advantage in carriers", with the
falsifier: *if growth rates in carriers and patients are indistinguishable, the
escape-velocity account is wrong.* Checking whether anyone had the data found
that they do, and that the answer is in between.

A Danish general-population study screened 19,958 people and followed 67 carriers
for more than ten years with serial allele fractions. Snyder and colleagues
(PNAS, 2026) fitted a **Moran process** to them: a fixed stem-cell population,
mutant and wild-type competing for it, one parameter for the mutant's
self-replication advantage. **That is the same structure as `clonal-escape`,
arrived at independently, which is reassuring and is also why their result lands
on us so directly.**

Three findings, and two of them hurt:

| finding | what it does to our model |
|---|---|
| The advantage is measurable per person, and higher on average in those who progressed | supports the mechanism |
| It has **limited predictive value for an individual**. Some with a negative advantage progressed; some whose clones clearly expanded did not | **the escape-velocity account is incomplete**, and Q2's answer is neither "rate" nor "dice" |
| **12 of 67 clones were significantly SHRINKING** | `clonal-escape` cannot produce this at all. It holds the advantage fixed for life, so a clone can only stall or grow |

So the headline correction is to the method, not the biology. **An ask is a claim
that nobody has done something, and it carries the same standing as any other
claim in this project.** Ours was `alleged`, was never checked, and was published
in this file for four hours. It has been rewritten as a calibration task and Q7
exists because of the twelve shrinking clones.

**One refinement that is easy to get backwards.** Inheritance does participate,
one level up. A common inherited variant in the same gene raises the chance of
*acquiring* the mutation, and the disease clusters in families. **Two layers:
something inherited changes the odds of the somatic event; the somatic event plus
time changes the blood.** Neither layer is actionable today, which is why the
record rates prevention `none`.

### Why does one cell win? And does it ever happen at birth?

Both asked on 2026-10-10, and they are the same arithmetic from two ends.

**It does happen at birth, or before it.** The lineage-tracing work dated the
mutation in the patients where *JAK2* was the first event to somewhere between
33 weeks of gestation and 10.8 years of age, and for the earliest case the
interval runs from about 11 weeks after conception. So the answer to "does it
ever happen at birth" is yes, routinely.

**And that is exactly why it does not present early.** One cell is one cell. The
stem-cell pool that keeps an adult in blood is of the order of a hundred thousand
actively contributing cells, which is the number the published model assumes.
A single mutant among them is about a thousandth of one per cent of the marrow,
and it produces about a thousandth of one per cent of the blood. **Nothing is
wrong with that person's blood count, because almost nothing about their blood
comes from that cell.** The disease is not waiting for a second event; it is
waiting for arithmetic.

**Why one cell wins at all is the part that sounds implausible, and the first
thing to say is that it is not special to this disease.** Expanded clones from
one driver or another are found in most people by their seventies. A blood system
that is still one diverse population at eighty is the exception. So "one cell
takes over a large share of the marrow" is close to the normal ageing of blood,
and PV is a case where the driver that won happens to also raise the red cell
count.

The mechanism of the winning is compounding. Stem cells self-renew, so any
inherited change that tilts renewal against differentiation even slightly is
multiplied every generation of cells. The published estimates are of a
self-replication advantage of the order of tens of per cent, over a forty-year
run. **A small edge and a long time, which is the same arithmetic as interest.**
Our model's shipped dial corresponds to roughly a ten per cent advantage, by my
own conversion from their units, and that is the number to calibrate properly.

What the advantage is MADE OF is Q1 and is open. The leading candidates are that
the mutant kinase signals through the thrombopoietin receptor without a ligand,
which is the stem cell's own self-renewal pathway rather than the erythropoietin
receptor that produces the visible phenotype; and that chronic inflammation
favours mutant stem cells over their neighbours, which would mean the clone
partly manufactures its own advantage. Neither is settled.

**And it frequently does not win, which is the honest other half.** About one
adult in thirty carries the mutation and about one in a hundred thousand per year
gets the disease. Three reasons it fails, in rough order of how much they
probably matter:

1. **The mutation has to land in a cell that lives long enough.** Most
   divisions in the marrow happen in progenitors, which die with their lineage.
   A V617F progenitor takes the mutation to the grave in weeks. Only a hit in a
   long-lived stem cell persists at all.
2. **A clone of one cell is easily lost by chance.** Early on, the numbers are
   small enough that the stochastic term dominates the advantage.
3. **The advantage can be too small, or can reverse.** Twelve of the sixty-seven
   followed carriers were losing ground. Inherited variants affecting blood-cell
   traits are known to influence how strongly the clone is selected, which is a
   second, quieter way in which inheritance participates in a somatic disease.

---

## 4. Open questions

Numbered to match `case.yaml`. Each is tagged with the Engpass obstacle it
belongs to where one exists.

**Q1 · What is the renewal advantage made of?** Its MAGNITUDE is now measured
per person. What it is made of is not. Is it a property of the mutation, of the
host, or of the niche? Those are three different interventions, and the leading
candidates are ligand-free signalling through the stem cell's own self-renewal
receptor and inflammation that favours the mutant over its neighbours. *(Engpass:
`who-progresses`)*

**Q2 · Why do most carriers never get the disease?** `partial`, as of the second
pass on 2026-10-10. Posed as "smaller advantage or unluckier dice", and the
evidence says neither alone: the growth advantage is higher on average in those
who progress and is a poor predictor of any individual. **The residual after
growth rate is accounted for is now a quantified residual rather than a shrug**,
and it is what caps the record's `prognostic` rating and gates route R3.
*(Engpass: `who-progresses`)*

**Q7 · Why do some clones shrink?** Twelve of sixty-seven followed carriers had a
significantly negative advantage. A clone that expands for years and then declines
means the advantage is not a constant of the person, and something switched it.
An adaptive immune response is the authors' leading suggestion. **This would be
the first thing resembling a natural control of the clone, and therefore a
direction that is not a kinase inhibitor.** It also breaks `clonal-escape` as
written. *(Engpass: `who-progresses`)*

**Q9 · Which constraint actually binds in a patient: the marrow's capacity, or the
iron supply?** Raised 2026-10-11 by our own two models disagreeing. In
`erythropoiesis-pv` the marrow edge is the only brake, so weakening it works. In
`iron` the iron supply is the only brake, so weakening the marrow does **nothing at
any dose**. Real marrow has both limits and nobody measures which is binding in a
given person. **It decides whether a kinase inhibitor, a hepcidin mimetic or a needle
is the right lever for them**, which is a live clinical question now that all three
exist, and it is answerable with existing measurements rather than new science.

**Q8 · Is V617F always the first event?** In some patients it is, and in others
*TET2* or *DNMT3A* came first, with the order apparently mattering for which
disease results. **If a prior mutation is what makes a *JAK2* clone able to
expand, the advantage in Q1 is a property of the cell's history rather than of
the mutation**, and the earlier event is the target. This is step 1b of the chain.

**Q3 · One mutation, three diseases.** The same V617F is found in essential
thrombocythaemia and primary myelofibrosis. Allele burden, homozygosity, the order
in which co-mutations arrive and host factors all contribute, and none of it
predicts the phenotype. The record's `mechanism: established` has a stated case
for `partial` resting on this hole alone. *(Engpass: `who-progresses`)*

**Q4 · Why is the thrombosis not only viscosity?** Lowering the haematocrit lowers
the risk and does not abolish it. This is the residual harm in the patients
treatment already reaches, and **no model of ours covers the step.**

**Q5 · What drives transformation to myelofibrosis or leukaemia, and can it be
seen coming?** It is what kills the patients whose thrombosis has been controlled.
*(Engpass: `who-progresses`)*

**Q6 · Does lowering the mutant allele burden change what happens to a patient?**
Interferon alfa lowers it and produces molecular remissions in some patients.
Whether that means fewer transformations or a longer life rests on retrospective
comparison. **It is the difference between treating the stock and treating the
mechanism, and the record has one slot for both.**

---

## 5. Models and data

### Ours

Each is a text file and the published ones run in a browser. **What each one
REFUSES to claim is the more useful half**, so both are written out. The paths are
in `case.yaml`, which checks that they resolve and that each is discussed here.

**Strangschrift `jak2-sites`.** Shows the real JAK2 and erythropoietin-receptor
sequences with the residues that matter marked on them: V617 in the pseudokinase
domain, Y1007 in the activation loop, the receptor tyrosines a mutant kinase
phosphorylates. Refuses any claim about shape. It never computes a fold, and the
two domains being adjacent in the folded protein is not visible in a sequence.

**Strangschrift `stat5-target`.** Shows a promoter carrying the motif that
activated STAT5 binds. Refuses the claim that these are the targets that matter
in this disease. The motif is real and the gene is invented.

**Schaltwerk `jak2-brake`.** Shows the restraint itself as a rule you can step:
while the pseudokinase site reads `braked`, the kinase cannot phosphorylate, and
nothing fires. Refuses rates. Schaltwerk has no time in it, so it says which
events are possible and never how fast.

**Schaltwerk `jak2-v617f`.** Shows the same board with the substitution. The
brake rule no longer matches, so phosphorylation fires with no erythropoietin
anywhere on the board, which is the step the prose calls constitutive
activation. Refuses to explain WHY the substitution loosens the restraint. That
is declared, not derived from structure.

**Schaltwerk `jak2-stat5`.** Shows the signal continuing past the receptor:
STAT5 phosphorylated, paired, and leaving. Refuses to say which genes it then
turns on, which is step 6 and is open.

**Schaltwerk `jak2-off`.** Shows that the off switches still work. A phosphatase
removes the phosphate, and SOCS1 grips the kinase's own phosphotyrosine and takes
it to be destroyed. Refuses any statement about whether the off switch can keep
up, which is a rate question and therefore Strombild's.

**Schaltwerk `pfcp`.** Shows the contrast case: a germline truncation of the
erythropoietin receptor that deletes the site the off switch grips. Too many red
cells, from a different step, present from birth. Refuses to be a model of PV. It
is on the board to be told apart from PV.

**Strombild `erythropoiesis`.** Shows the healthy loop, settling where the
textbook says and defending a bleed in three weeks. Refuses anything below the
stock level. There are no cells in it, only amounts.

**Strombild `erythropoiesis-pv`.** Shows the disease as ONE EDGE: maturation
stops reading erythropoietin, the haematocrit climbs into the sixties, and the
kidney turns erythropoietin down below 1 while working perfectly. A phlebotomy
event shows the sawtooth that never ends. Refuses the forty years before that
steady state. It models a marrow already taken over.

**Strombild `clonal-escape`.** Shows the forty years, with the clone as a stock
and the renewal advantage as one dial. Refuses probability: the expansion is
deterministic here and stochastic in a person, so it can say whether a given
advantage escapes on average and not how often it does. It also refuses to
predict an individual, and says why.

**Strombild `iron`.** Shows the supply side: iron recycling between red cells and
stores, the hepcidin gate, and what phlebotomy costs. Its unit is the trick — iron
measured in haematocrit points it could build — so taking blood out takes the iron
with it and needs no separate rule. Produces the lengthening phlebotomy interval,
and separates a third lever from the other two. Refuses to have any brake except
iron. The marrow is a catalyst in it, never consumed, which is the mirror image of
`erythropoiesis-pv` where iron does not exist. It also cannot model the induction
phase, for a reason that is about the language rather than the disease.

### Can a reader actually open these?

**Today, none of them**, and the case file says so rather than implying otherwise.
`case.yaml` records one of three states per model and `check.py` prints the tally:

| state | count | what it means |
|---|---:|---|
| `live` | **0** | openable on the public site right now |
| `repo` | 6 | the source is public; **the playground on the site is a sync behind it** |
| `private` | 5 | Schaltwerk. It exists here and nowhere a reader can reach |

The six `repo` models are two commands away from being `live`: the Strangschrift and
Strombild playgrounds on the site predate every model in this case file. Until then,
a reader can read the text files and not run them, which is a worse version of this
case file than it should be. **It is the first thing on the list in section 9.** `check.py` prints that count rather than letting it pass.

`clonal-escape` is the one to read first. It makes the hypothesis runnable: the
stem-cell niche is a fixed pool, the clone is a stock in it, and the mutant's
renewal advantage is a single dial. Three outcomes fall out of that one number.

| advantage | clone at 85 | haematocrit | what that is |
|---|---|---|---|
| low | nothing | normal | no escape — nothing to find |
| middle | a few percent | **normal for life** | **clonal haematopoiesis** |
| shipped value | most of the marrow | mid-sixties | PV, criteria met at **age 60** |
| high | most of the marrow | seventies | PV, criteria met at **age 31** |

The middle row is the finding. *Most people who carry V617F never get PV*, and the
model produces them **without a second mechanism** — same mutation, same
physiology, a slightly smaller advantage, and the disease runs out of lifetime.
The shipped value puts the diagnostic threshold at sixty, which is the real median
age at diagnosis and was not fitted to it.

And the sensitivity is the warning rather than the result: doubling the dial moves
first abnormality from age 74 to age 38. **The model cannot predict an individual's
onset, and saying so is what makes it useful** — it states how precisely that
growth rate would have to be measured to be worth anything.

### Other people's

**What exists and is strong.** Randomised trial evidence on the treatment:
low-dose aspirin (ECLAP, 2004), a haematocrit target below 45% against 45–50%
(CYTO-PV, 2013), ruxolitinib after hydroxyurea failure (RESPONSE, 2015), and
ropeginterferon in low-risk patients (Low-PV, 2021). Large modern cohorts carry
survival, thrombosis at diagnosis and transformation rates. **None of it is in
this repository yet**; the record's own `holes` say every figure in it is from
memory and has not been read against the papers.

**The 2022 lineage-tracing work is the most important single result for this
case**, because it is what makes the natural history a quantitative question
rather than a mystery.

**The open protein models are a supplier, not an answer.** Biohub publishes an
open, MIT-licensed protein stack — a sequence language model, a structure
predictor for complexes, and an atlas of predicted structures — which can be
pointed at JAK2 and the erythropoietin receptor today. **It buys geometry and
variant scoring. It does not buy a single step of the chain in section 2.** Every
model listed there answers *what happens next*, which is the layer the protein
stack stops below. The honest use is to cite its structures as declared facts
rather than recomputing them, and the same group's binder-design results are the
right shape for a route: a named target, a method, and a measured hit rate.

**The carrier data exists, and this file said it did not.** Two
general-population efforts, and together they are the most important external
input to this case:

| | |
|---|---|
| screened, Danish general-population study | 19,958 |
| carrying V617F, sensitive assay | 3.1%, the large majority under 1% allele fraction |
| carriers above 1% followed with serial measurements | 67, over more than ten years |
| their clones: increasing · neutral · **decreasing** | 47 · 8 · **12** |
| of those 67, diagnosed with a neoplasm during follow-up | 37 |
| a second, less sensitive cohort at median age 63 | 0.1% carrying it |

Two cautions on reading that table. The 37 of 67 is **not** a population
progression rate, because the 67 were selected for already having an allele
fraction above 1%, which is the high end of carriage. And the gap between the two
prevalence figures, 3.1% against 0.1%, is mostly the assay rather than the
populations: **how common this mutation is depends on how hard you look.**

The modelling paper on that cohort fits a Moran process and reports a
self-replication advantage per person. It is the right comparator for
`clonal-escape` and the first ask is now to calibrate against it rather than to
go and collect what it already holds.

---

## 6. Detection

**The test is a single blood sample and it is cheap. The problem is that the
question is not asked.** A raised haematocrit has many commoner explanations —
smoking, dehydration, lung disease, sleep apnoea, altitude, testosterone — so the
result is seen, attributed, and not repeated. The record rates diagnostic
measurement `objective` and the `access` number is dominated by patients never
found, not by missing drugs.

Two ways it is missed, and they are different problems:

- **Explained away.** The count is abnormal and a plausible cause is to hand.
  A *JAK2* test would settle it.
- **Masked.** The haematocrit is normal and the disease is present, because iron
  deficiency, an enlarged spleen or an expanded plasma volume hide the red-cell
  mass. This is how someone presents with a hepatic vein thrombosis and an
  unremarkable blood count.

**What the window costs.** About a quarter of patients have a major thrombosis at
or before diagnosis. Treatment started afterwards lowers the risk of the next
event and gives nothing back. The record files that under `residue`, severity
`major`, and it is the strongest argument in the case for working on detection
rather than on therapeutics.

**What could be built.** Opportunistic flagging on an already-ordered full blood
count is software, not science, and `clonal-escape` says where to look: a
haematocrit drifting upward across repeated counts in someone's fifties, with a
*falling* erythropoietin, is the loop's fingerprint appearing years before any
threshold is crossed.

---

## 7. Treatments, and the distinction that matters

**Rewritten 2026-10-11.** This section had two categories, stock and edge. Modelling
the iron supply produced a third, and then produced a warning about all three.

**The three levers.**

| | acts on | what that means |
|---|---|---|
| **the stock** | red cells that already exist | take them out. The number falls and nothing about why it rose has changed |
| **the edge** | the marrow's ability to build | make it less able, whatever material is available |
| **the substrate** | the iron it builds with | leave the marrow alone and starve its supply |

| treatment | lever | what it does |
|---|---|---|
| venesection to a haematocrit under 45% | **stock**, and **substrate** by accident | removes red cells, and the iron inside them. **The iron loss is not a side effect, it is the slow half of the mechanism** |
| low-dose aspirin | downstream of the stock | the platelet contribution to step 11 |
| hydroxyurea | edge, bluntly | suppresses marrow output without distinguishing mutant from wild-type |
| **rusfertide** (hepcidin mimetic, approved 2026-08-28) | **substrate** | mimics the gate hormone, so iron stops reaching the marrow **while the stores stay full.** Functional restriction rather than true deficiency |
| ruxolitinib | edge, bluntly | inhibits JAK2, mutant and wild-type alike. Lowers allele burden modestly |
| interferon alfa | **the clone** | lowers allele burden over years. Whether that changes outcomes is **Q6** |
| a mutant-selective JAK2 inhibitor | the edge, precisely | does not exist in practice. Early trials |

### Why iron is not a side effect

Venesection works twice. It removes red cells immediately, and it removes **iron**,
because the iron is inside the cells. Haemoglobin is where most of the body's iron
is, and the body is a nearly closed iron loop: red cells live about four months,
macrophages recover their iron, and diet contributes a small fraction of the daily
throughput. So repeated venesection empties the stores, and **an iron-starved marrow
cannot rebuild the red cell mass quickly.**

That is why maintaining the deficiency *is* the treatment, and why giving iron back
undoes it. The register's record files the deliberate deficiency under what treatment
costs: fatigue, restless legs, poor concentration, uncorrected on purpose.

And the body fights it. The over-driven marrow suppresses hepcidin, and iron
deficiency suppresses it further, which opens the gate and raises absorption. **That
counter-regulation is why venesection is for life rather than a course of treatment.**

`iron.strombild` reproduces the clinical rhythm from this alone. Its phlebotomy
interval starts at 73 days and settles at 130 as the stores empty, against the
record's own prose of "every few weeks at first and every few months once stable".
The lengthening is an output, not a setting.

### What rusfertide changes, and it is the comparison that matters

The drug mimics hepcidin, so it closes the gate instead of draining the tank. In the
model, same haematocrit, opposite iron:

| | phlebotomy | rusfertide |
|---|---|---|
| haematocrit held | yes | yes |
| iron stores after 2500 days | 11.1 | **19.2** |
| needles | for life | weekly injection, no venesection |

**This also closes a named hole in the disease record**, which says rusfertide's
regulatory status was unchecked. It was approved on 28 August 2026. Whether that
moves any axis is a rating decision and belongs in Nordstern, not here.

### The warning the model produced, which is worth more than the levers

In `iron.strombild`, **pushing on the marrow edge does nothing at any dose.** At a
sixth of normal maturation the haematocrit, the stores and the phlebotomy interval
are unchanged; the only thing that moves is iron backing up in front of a slower
marrow.

That is not a claim about ruxolitinib. It is a claim about models: **where one
constraint binds, every lever is either inert or decisive, and none is
therapeutic.** Iron is the only brake in that file, so the iron lever is nearly
decisive and the marrow lever is inert. `erythropoiesis-pv.strombild` has the
opposite fault, with the marrow edge as the only brake and no iron at all, so there
the marrow lever works and iron cannot be asked about.

**Neither file can say which constraint binds in a real patient, and that is the
question a clinician has.** It is now **Q9**.

---

## 8. Routes

Each with a falsifier. **A route without a falsifier is a wish.**

**R1 · Calibrate against the measurements that exist.** Rewritten 2026-10-10;
it previously read "measure the advantage in carriers", which had already been
done twice. Map our dial onto the published per-person advantage, re-run the three
regimes against their distribution, and publish where our file loses.
*Falsifier, and it has already partly fired:* the published estimates show the
advantage is a poor predictor of an individual's progression, so the
escape-velocity account is incomplete as an explanation of WHO becomes ill. It
survives as an account of the three regimes and of why onset is late. **If
calibration shows our shipped dial is outside the observed distribution, the
age-60 result is a coincidence and should be withdrawn.**

**R2 · Turn the model into a prediction and test it against stored cohorts.**
Given an allele burden at one age, predict the blood count at the next.
*Falsifier:* the predicted ages of crossing are no better than age alone.

**R3 · Early, low-intensity clone reduction in people who have not yet crossed.**
`clonal-escape` is the argument: act on the slope decades before the threshold.
*Falsifier:* **this route is blocked, not merely untested, until Q2 is answered.**
Treating carriers means treating a large majority who were never going to progress,
which is the overtreatment the register derives as a flag. The ethics follow the
measurement, not the other way round.

**R4 · Mutant-selective inhibition.** The thing that made imatinib work for the
sibling disease. In early trials.
*Falsifier:* selectivity achieved and allele burden falls without a change in
thrombosis or transformation, which would fold R4 back into Q6.

**R6 · Merge the two one-sided models and ask which constraint binds.** One file
where the marrow's capacity and the iron supply are both limits, then fit it to the
thing that is already measured in every patient on treatment: the phlebotomy interval
and the ferritin. **A patient whose interval lengthens as their ferritin falls is
iron-limited. One whose interval stays short with an empty ferritin is marrow-limited**
and is the patient a kinase inhibitor should help.
*Falsifier:* the interval and the ferritin turn out to carry no information about
which lever works, in which case Q9 is not answerable this cheaply and needs
something measured in the marrow rather than in the blood.

**R5 · A model of step 11.** The thrombosis is not only viscosity and nothing here
covers it. Platelets, leukocytes and endothelium in a Strombild-shaped loop would
at minimum say what the residual risk after a haematocrit of 45% is made of.
*Falsifier:* it reproduces nothing that the haematocrit alone does not already
explain.

---

## 9. How to help

The file is public and the models are text. Three concrete things, in order of
how much they would change:

1. **Calibrate the model against the published carrier estimates** (R1). The
   data exists and has been modelled with the same structure we used. The work
   is the mapping, the re-run, and an honest account of where our file loses.
2. **Rebuild `clonal-escape` with an advantage that can change over a life**
   (Q7), so a clone can expand and then decline. That is structural, not a
   parameter, and it needs a hypothesis for what switches it.
3. **Read `clonal-escape` and try to break it.** It needs erythropoiesis, not
   programming. The constants are declared in the file and the header states what
   the model refuses to claim; the most useful contribution is a sentence saying
   which of those claims is wrong.
4. **A model of the thrombosis step** (R5), one of four empty rows in section 2.

Corrections to the mechanism chain are the most valuable thing anybody can send,
and section 3 is where they go. **A case file that is wrong in a markable place is
doing its job.**

---

## 10. Log

Append-only, newest last. `case.yaml` carries only the date of the newest entry,
and `check.py` fails if that date is not found here.

**2026-10-10 · case opened.** First disease anyone started on, for a nonprofit
partner. The opening discussion was a correction: the working assumption was the
ordinary one, a genetic disease with bad code and a faulty protein, which fails
the obvious test. If the mutation were inherited the disease would arrive in
childhood, and it arrives at sixty. The resolution is that V617F is somatic. The
germline control is familial hypercholesterolaemia, which that argument queued as
a new Nordstern record. The control inside this phenotype is familial
erythrocytosis, which is germline and does present in childhood. Then the
lineage-tracing result made it stranger: the mutation is often acquired before
birth, and the clone is what takes decades. That is a share and a rate, so it is
a stock and a flow, and it became `clonal-escape.strombild` the same day. The
model produced a third outcome nobody put in: a clone that escapes and never
causes disease in a lifetime, which is clonal haematopoiesis and which most
carriers have.

**2026-10-10 · second entry, and it corrects the first.** Four questions were put
to the file: are we certain it is the mutation, does it ever happen at birth, why
does one cell win, and do some people get it without the cell winning. Checking
the last found that the measurement this file had just listed as its number one
missing input **already existed**, in two published cohorts. The result is partly
a refutation of our own model, in exactly the place route R1 said to look. See
section 3. Q2 moved from `open` to `partial`, Q7 and Q8 were added, and the first
ask became a calibration task. The lesson is about method rather than disease:
**an ask is a claim, and it has the same standing as any other claim.**

**2026-10-10 · third entry.** The spine was emptied of prose. `case.yaml` now
holds ids, links, paths, dates and statuses only; everything a person would
rather read lives here. `check.py` enforces it in both directions: it rejects the
prose keys if they come back, and it fails if a question id or a model path in
the spine is never discussed in this file. Also added: section 11, and the
explanation of mosaicism in section 3, after the question *how can a population
of cells exist that does not have the faulty protein?*

**2026-10-11 · iron, and a question we were not expecting.** Asked why PV patients are
not iron deficient from making all that extra blood. **They are, and it is worse than
that: the deficiency is also the treatment.** Phlebotomy removes iron inside the red
cells, an iron-starved marrow cannot rebuild quickly, and giving iron back undoes the
treatment. Built `iron.strombild` for the supply side. Its one trick is the unit —
iron measured in haematocrit points it could build — which makes phlebotomy's iron
cost fall out with no extra rule. It reproduces the clinical rhythm from iron alone:
the phlebotomy interval starts at 73 days and settles at 130 as the stores empty,
against the record's own "every few weeks at first and every few months once stable".
It also separates a third lever, the substrate, from stock and edge, and shows the
hepcidin mimetic holding the haematocrit with the stores still full.
Two things came out that were not asked for. **Pushing on the marrow edge in that file
does nothing at any dose**, which is a statement about models rather than about
ruxolitinib: where one constraint binds, every lever is inert or decisive and none is
therapeutic. That became **Q9** and route **R6**. And one bug worth recording: the
release edge first read hepcidin without reading `stores`, so an empty store went on
releasing iron for ever. **The model manufactured the material it was supposed to be
running out of**, and produced a tidy steady phlebotomy rhythm that was pure artefact.
A conservation test now guards it.
Also checked and resolved: the disease record's hole about rusfertide's regulatory
status. Approved 28 August 2026.

**2026-10-10 · fourth entry, and the correction is to our own writing.** The
comparison table added that morning was challenged for exactly the right reason:
it used *relevant cells* and *disease at birth* as though both were clear, and
neither is. Both terms are now retired, `GLOSSARY.md` was written to define the
vocabulary once for every case, and `check.py` rejects a case file that uses a
retired term. The table was rebuilt with the cell type named on each side and
with the delay before harm split into its two kinds, **accumulation** and
**expansion**, which is what actually distinguishes an inherited disease from an
acquired one. The question that forced it: *if you inherit it, do you start
over-producing?* The answer is yes, immediately, and it had not been said
anywhere in the file.

---

## 11. Sources

**Not yet held to the register's citation standard.** Nordstern requires an
identifier, a retrieval date and a verbatim quote for every sourced scalar, and
nothing in this file has been through that. These are pointers, read on
2026-10-10, so that a reader can check the claims rather than trust them.

- **Mutation timing, and whether V617F is the first event.** Williams et al.,
  *Life histories of myeloproliferative neoplasms inferred from phylogenies*,
  Nature 602:162–168 (2022). `doi:10.1038/s41586-021-04312-6`. Phylogenies from
  1,013 single-cell-derived colonies across 12 patients; V617F dated to between
  33 weeks of gestation and 10.8 years in the patients where it was the first
  driver.
- **Carrier prevalence and per-person growth advantage.** Snyder et al.,
  *Mathematical modeling of JAK2V617F clonal expansion in a general population
  cohort*, PNAS (2026). `doi:10.1073/pnas.2507773123`. Danish General Suburban
  Population Study; Moran process with a stem-cell population of 10^5, fitted by
  approximate Bayesian computation.
- **Inherited modifiers of clonal selection.** Work on polygenic scores for
  blood-cell traits influencing selection on V617F and progression to a
  neoplasm. **Not read; cited from a secondary description.**
- **Inflammation as a source of the advantage.** Preprint work on interleukin-1
  favouring early expansion of *JAK2*-mutant stem cells. **Not read; cited from
  a secondary description and it is a preprint.**
- **Rusfertide approval and the trial behind it.** Approved 28 August 2026 as
  Mimrylo, for erythrocytosis in adults with polycythaemia vera inadequately
  controlled on existing therapy; weekly subcutaneous, titrated to hold the
  haematocrit below 45%. Phase 3 VERIFY, 293 patients, clinical response 76.9%
  against 32.9% on placebo added to standard of care, with phlebotomy need more than
  halved; commonest adverse events injection-site reactions and **anaemia**, which is
  the dose-limiting toxicity the model's narrow window reflects. Read 2026-10-11 from
  secondary coverage, not from the trial report.

- **Protein structure and variant scoring.** The Biohub open protein stack, at
  `biohub.org/ai-models`. Relevant to geometry and to binder design, and to no
  step of section 2.

**Two of the five above are marked as not read**, which is the point of having
the list. The trial evidence named in section 7 is from memory and is in the same
state as the disease record's own, which says so in its `holes`.
