/* =====================================================================
 * Nordstern query language tests — run with:  node --test web/
 *
 * tool.test.js covers the PAGE. This file covers the LANGUAGE, against the
 * real register, with no DOM anywhere. The split matters: the semantics of
 * `-blocker.kind:knowledge` should be checkable without booting a fake
 * browser, and a diagnostic's wording is a feature to be asserted, not an
 * implementation detail.
 *
 * The thing most worth protecting here is the failure behaviour. A filter
 * language that answers a typo with zero rows teaches the reader that the
 * register is empty rather than that they mistyped, and the register would
 * be lying by omission. Half these tests are about what happens when the
 * query is wrong.
 * ===================================================================== */
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const DIR = __dirname;
const Q = require("./query.js");

const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(DIR, "data.js"), "utf8"), ctx);
const R = ctx.window.NORDSTERN.records;
const DOM = Q.domains(R);

const run    = q => Q.run(R, q, DOM);
const slugs  = q => run(q).records.map(r => r.slug).sort().join(" ");
const errs   = q => run(q).errors;
const only   = q => { const e = errs(q); assert.equal(e.length, 1, JSON.stringify(e)); return e[0]; };
const clean  = q => { const e = errs(q); assert.equal(e.length, 0, JSON.stringify(e)); return run(q).records; };

/* ---- the grammar ---------------------------------------------------- */

test("an empty query is every record", () => {
  assert.equal(clean("").length, R.length);
  assert.equal(clean("   ").length, R.length);
});

test("field:value matches an enum exactly", () => {
  const got = clean("capability:curable");
  assert.ok(got.length > 0);
  assert.ok(got.every(r => r.derived.capability === "curable"));
});

test("a space means AND", () => {
  const wide = clean("capability:curable").length;
  const got = clean("capability:curable reach:<0.5");
  assert.ok(got.length < wide && got.length > 0);
  assert.ok(got.every(r => r.derived.capability === "curable" && r.derived.reach < 0.5));
});

test("a leading minus negates the whole term", () => {
  const yes = new Set(clean("quadrant:frontier").map(r => r.slug));
  const no  = clean("-quadrant:frontier").map(r => r.slug);
  assert.ok(yes.size > 0 && no.length > 0);
  assert.equal(yes.size + no.length, R.length, "negation must partition the register");
  assert.ok(no.every(s => !yes.has(s)));
});

test("value-level OR is a union within one field", () => {
  const a = new Set(clean("blocker.standing:alleged").map(r => r.slug));
  const b = new Set(clean("blocker.standing:disputed").map(r => r.slug));
  const u = clean("blocker.standing:(alleged OR disputed)").map(r => r.slug);
  assert.ok(a.size && b.size);
  assert.equal(u.length, new Set([...a, ...b]).size);
  for (const s of [...a, ...b]) assert.ok(u.includes(s), `${s} lost by the OR`);
});

test("`or` is matched case-insensitively but only as a whole word", () => {
  assert.equal(slugs("blocker.standing:(alleged or disputed)"),
               slugs("blocker.standing:(alleged OR disputed)"));
});

test("numeric comparison, with k/M/B suffixes", () => {
  const got = clean("deaths:>100k");
  assert.ok(got.length > 0);
  assert.ok(got.every(r => r.burden.deaths.value > 100000));
  assert.equal(slugs("deaths:>100k"), slugs("deaths:>100000"));
  assert.equal(slugs("deaths:>0.1M"), slugs("deaths:>100000"));
});

test("every comparator does what it says", () => {
  const n = q => clean(q).length;
  assert.equal(n("reach:<0.5") + n("reach:>=0.5"), R.length);
  assert.equal(n("reach:>0.5") + n("reach:<=0.5"), R.length);
});

test("quotes carry spaces and nothing else — the FIELD decides exactness", () => {
  // an enum stays exact when quoted...
  const q = clean('quadrant:"known & treatable"');
  assert.ok(q.length > 0 && q.every(r => r.derived.quadrant === "known & treatable"));
  // ...and a text field stays substring when bare
  assert.ok(clean("name:hepat").some(r => r.slug === "hepatitis-c"),
    "a text field must match on a substring without needing quotes");
});

test("a bare word is free text across the whole record, prose included", () => {
  assert.ok(clean("lithium").some(r => r.slug === "bipolar"),
    "free text must reach the witness prose, not just names");
  assert.equal(clean("zzzznotathing").length, 0);
});

test("free text can be negated too", () => {
  const with_ = clean("lithium").length;
  assert.equal(clean("-lithium").length, R.length - with_);
});

/* ---- arrays are `some` ---------------------------------------------- */

test("an array field matches with `some`", () => {
  const got = clean("blocker.kind:cost");
  assert.ok(got.length > 0);
  assert.ok(got.every(r => r.blockers.some(b => b.kind === "cost")));
});

test("negating an array field means NONE, not `some ... not`", () => {
  // The distinction that would silently give wrong answers: nearly every
  // record has some blocker that is not `knowledge`.
  const got = clean("-blocker.kind:knowledge");
  assert.ok(got.length > 0);
  assert.ok(got.every(r => !r.blockers.some(b => b.kind === "knowledge")));
  const loose = R.filter(r => r.blockers.some(b => b.kind !== "knowledge"));
  assert.ok(loose.length > got.length,
    "test is vacuous unless the two readings actually differ on this data");
});

test("`every` is not in the grammar — it is a derived flag", () => {
  const got = clean("only_knowledge_blockers:true");
  assert.ok(got.length > 0);
  assert.ok(got.every(r => r.blockers.length && r.blockers.every(b => b.kind === "knowledge")));
});

/* ---- diagnostics ---------------------------------------------------- */

test("an unknown field is a witness with a suggestion, not zero rows", () => {
  const e = only("capabilty:curable");
  assert.match(e.message, /no field `capabilty`/);
  assert.match(e.hint, /capability/);
  assert.equal(run("capabilty:curable").records.length, R.length,
    "an unparseable term must be skipped, never applied as a filter");
});

test("a bad enum value lists the legal values, read off the data", () => {
  const e = only("capability:cured");
  assert.match(e.message, /has no value `cured`/);
  assert.match(e.hint, /did you mean `curable`/);
  for (const v of DOM.capability) assert.ok(e.hint.includes(v), `hint omits "${v}"`);
});

test("the valid-value list cannot drift from what is loadable", () => {
  // The list in the diagnostic IS the set present in the records.
  const e = only("quadrant:nonsense");
  const listed = e.hint.split("valid:")[1].split("·").map(s => s.trim());
  assert.deepEqual(listed.slice().sort(), [...new Set(R.map(r => r.derived.quadrant))].sort());
});

test("a comparison on a non-numeric field explains and gives an example", () => {
  const e = only("capability:>0.5");
  assert.match(e.message, /not numeric/);
  assert.match(e.hint, /capability:/);
});

test("a flag rejects a value that is not a boolean", () => {
  const e = only("orphaned:maybe");
  assert.match(e.message, /is a flag/);
  assert.match(e.hint, /orphaned:true/);
});

test("a non-number after a comparator says so", () => {
  const e = only("deaths:>lots");
  assert.match(e.message, /not a number/);
  assert.match(e.hint, /k, M or B/);
});

test("cross-term OR is refused by name, with the syntax that does work", () => {
  const e = only('quadrant:frontier OR quadrant:"empirical luck"');
  assert.match(e.message, /not supported yet/);
  assert.match(e.hint, /blocker\.kind:\(cost OR logistics\)/);
});

test("a stray AND between terms says a space already means AND", () => {
  const e = only("capability:curable AND orphaned:true");
  assert.match(e.hint, /space already means AND/);
});

test("unbalanced syntax is caught rather than mis-parsed", () => {
  assert.match(only("blocker.kind:(cost").message, /unclosed/);
  assert.match(only('name:"unterminated').message, /unterminated quote/);
});

test("an empty value is not an error — it is mid-typing", () => {
  assert.equal(errs("capability:").length, 0);
  assert.equal(run("capability:").records.length, R.length);
  assert.equal(errs("capability: reach:<0.5").length, 0);
});

test("a broken term is skipped but the rest of the query still runs", () => {
  const r = run("capability:curable bogusfield:x");
  assert.equal(r.errors.length, 1);
  assert.equal(r.ignored, 1);
  assert.ok(r.records.length > 0);
  assert.ok(r.records.every(x => x.derived.capability === "curable"),
    "the valid half of the query must still apply");
});

/* ---- aliases and the field registry --------------------------------- */

test("the old facet names still land somewhere real", () => {
  assert.equal(slugs("blocker:cost"), slugs("blocker.kind:cost"));
  assert.equal(slugs("actor:nonprofit"), slugs("blocker.who_could:nonprofit"));
  assert.equal(slugs("toll:catastrophic"), slugs("toll.severity:catastrophic"));
});

test("every declared field can be read off every record without throwing", () => {
  for (const [name, spec] of Object.entries(Q.FIELDS))
    for (const r of R)
      assert.doesNotThrow(() => spec.get(r), `${name} threw on ${r.slug}`);
});

test("every alias points at a field that exists", () => {
  for (const [alias, target] of Object.entries(Q.ALIASES))
    assert.ok(Q.FIELDS[target], `alias ${alias} -> ${target}, which is not a field`);
});

test("every enum field has a non-empty domain", () => {
  // An enum with no values would validate nothing and silently accept typos.
  for (const [name, spec] of Object.entries(Q.FIELDS)) {
    if (spec.type !== "enum") continue;
    assert.ok(DOM[name] && DOM[name].length, `${name} has an empty domain`);
  }
});

test("describe() is the field list the help panel renders", () => {
  const d = Q.describe(DOM);
  assert.equal(d.length, Object.keys(Q.FIELDS).length);
  assert.ok(d.find(f => f.name === "capability").derived, "capability is derived and must say so");
  assert.ok(!d.find(f => f.name === "mechanism").derived, "mechanism is declared, not derived");
  assert.ok(d.find(f => f.name === "capability").values.includes("curable"));
});

/* ---- the register answering its own questions ----------------------- */

test("the six canned questions are expressible as queries", () => {
  // If one of these stops parsing or stops matching, an Ask button on a
  // public page silently returns an empty table.
  for (const q of ["orphaned:true", "measurement_gap:true", "harm_without_benefit:true",
                   "only_knowledge_blockers:true", "quadrant:frontier"]) {
    const r = run(q);
    assert.equal(r.errors.length, 0, `${q}: ${JSON.stringify(r.errors)}`);
    assert.ok(r.records.length > 0, `${q} matches nothing`);
  }
});

test("src:recall matches the whole register, and the page says so", () => {
  // Not a curiosity: the provenance ledger is queryable, and today the
  // honest answer to "what here is verified" is "nothing".
  assert.equal(clean("src:recall").length, R.length);
});

/* ---- numeric fields compare numerically ------------------------------ */

test("a bare number on a numeric field means EQUALS, not substring", () => {
  // THE BUG THIS PINS. `deaths:0` used to fall through to the substring
  // matcher and return 92 of 108 records, because "6600000" contains "0".
  // A public tool answered "which diseases kill nobody" with the list of
  // diseases that kill the most people.
  const zero = clean("deaths:0");
  assert.ok(zero.length > 0, "some records genuinely carry deaths: 0");
  assert.ok(zero.length < R.length / 2,
            `deaths:0 matched ${zero.length}/${R.length} — substring matching is back`);
  for (const r of zero) {
    const v = r.burden.deaths && r.burden.deaths.value;
    assert.ok(v === 0 || v == null, `${r.slug} has deaths ${v} and matched deaths:0`);
  }
  // and the record with the largest toll must NOT be in it
  assert.ok(!zero.some(r => r.slug === "ischaemic-heart-disease"),
            "the register's biggest killer matched deaths:0");
});

test("a non-number on a numeric field is a witness, never zero rows", () => {
  const r = run("deaths:lots");
  assert.equal(r.errors.length, 1);
  assert.match(r.errors[0].message, /numeric/);
  assert.match(r.errors[0].hint, /k, M or B/);
});

/* ---- survival: you get it, and then what? ---------------------------- */

test("survival and outcome are separate questions and both are askable", () => {
  // gaps.md #216: on the band alone, head-neck-cancer and heart-failure are
  // both 0.55 `good chance`. One of them is cured. If `outcome` ever
  // disappears the register is back to publishing that as one number.
  for (const q of ["survival:terminal", "outcome:cured", "outcome:held",
                   "outcome:delayed", "no_longer_terminal:true", "was_fatal:true"]) {
    const r = run(q);
    assert.equal(r.errors.length, 0, `${q}: ${JSON.stringify(r.errors)}`);
    assert.ok(r.records.length > 0, `${q} matches nothing`);
  }
  const hn = clean("outcome:cured").map(r => r.slug);
  const hf = clean("outcome:delayed").map(r => r.slug);
  assert.ok(hn.includes("head-neck-cancer"), "head-neck-cancer is curative — cured");
  assert.ok(hf.includes("heart-failure"), "heart-failure is disease-modifying — delayed");
  // ...and they sit in the same band, which is the whole point.
  for (const s of ["head-neck-cancer", "heart-failure"]) {
    const rec = R.find(r => r.slug === s);
    assert.equal(rec.derived.survival_band, "good chance", `${s} band moved`);
  }
});

test("gain:0 finds the records where medicine bought nothing", () => {
  const z = clean("gain:0").map(r => r.slug).sort();
  assert.ok(z.length > 0 && z.length < 10, `gain:0 returned ${z.length}`);
  assert.ok(z.includes("alzheimers"),
            "alzheimers has identical treated and untreated survival — if this "
            + "changed, a treatment extended life and the record should say so");
  for (const r of clean("gain:0")) {
    assert.equal(r.survival.treated.value, r.survival.untreated.value, r.slug);
  }
});
