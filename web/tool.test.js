/* =====================================================================
 * Nordstern query TOOL tests — `web/query.html` — run with: node --test web/
 *
 * Named for what it covers, which took three goes. `query.js` is the language
 * and has `query.test.js`; `index.html` is the map and has `dashboard.test.js`;
 * this is the tool. It was `app.test.js` back when there was one page and "the
 * app" named it unambiguously.
 *
 * The front end is a pure view over `web/data.js`, which `check.py --build`
 * generates from the YAML. These tests run the real inline script from
 * query.html against the real generated data, through a fake DOM.
 *
 * What they are for: the page will be public, and the failure that matters is
 * a filter that silently returns the wrong set or a record whose detail view
 * throws because it lacks an optional block (`window`, `strata`, `moved`).
 * Both are invisible until someone hits them.
 *
 * What they cannot check: layout, styling, and anything about how it looks.
 * Open the page for that.
 * ===================================================================== */
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const DIR = __dirname;

/* ---- fake DOM ------------------------------------------------------- */
function makeEl(id = "") {
  const el = {
    id, value: "", innerHTML: "", textContent: "", dataset: {},
    options: [], _children: [],
    classList: {
      _s: new Set(),
      add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
      toggle(c, on) { on === undefined ? (this._s.has(c) ? this._s.delete(c) : this._s.add(c)) : (on ? this._s.add(c) : this._s.delete(c)); },
      contains(c) { return this._s.has(c); },
    },
    add(opt) { this.options.push(opt); },
    querySelectorAll() { return []; },
    click() {},
  };
  el.tBodies = [makeElBare()];
  return el;
}
function makeElBare() { return { innerHTML: "", querySelectorAll: () => [] }; }

function boot(initialQuery = "") {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  assert.equal(blocks.length, 1, "expected exactly one inline <script>");

  const els = {};
  const get = id => (els[id] ||= makeEl(id));
  ["q", "qerr", "qfields", "qexamples", "prov", "reset", "dlJson", "dlCsv",
   "count", "tbl", "detail", "spec", "specBtn", "specClose", "specProv"].forEach(get);
  for (const d of [els.spec]) {
    d.showModal = function () { this.open = true; };
    d.close = function () { this.open = false; };
  }

  const exs = [], ths = [];
  const urls = [];
  const sandbox = {
    window: {},
    document: {
      getElementById: get,
      querySelectorAll(sel) {
        if (sel === ".exq") {
          // The page writes these into #qexamples and then queries for them, so
          // materialise from the markup it just produced rather than from the
          // file — that is what a browser does, and it means an example that is
          // never rendered is never wired up in the tests either.
          if (!exs.length)
            for (const m of (els.qexamples.innerHTML || "").matchAll(/data-q="([^"]+)"/g))
              exs.push(Object.assign(makeEl(), { dataset: {
                q: m[1].replace(/&amp;/g, "&").replace(/&lt;/g, "<")
                       .replace(/&gt;/g, ">").replace(/&quot;/g, '"') } }));
          return exs;
        }
        if (sel === "#tbl th") return ths;
        return [];
      },
      createElement: () => makeEl(),
    },
    // ?q= is the share link, so the harness carries a location and a history
    location: { search: initialQuery ? "?q=" + encodeURIComponent(initialQuery) : "" },
    history: { replaceState: (a, b, u) => urls.push(u) },
    URLSearchParams: global.URLSearchParams,
    encodeURIComponent, decodeURIComponent,
    Option: function (v, t) { return { value: v, text: t }; },
    Blob: function (parts) { this.parts = parts; },
    URL: { createObjectURL: () => "blob:x", revokeObjectURL() {} },
    JSON, Object, Array, Set, Map, String, Number, Math, Infinity, RegExp, console,
  };
  sandbox.window = sandbox;

  // The sortable columns the page declares, mirrored from the markup so the
  // tests break if one is added without a handler. The worked-example buttons
  // are built by the script rather than the markup, so `exs` is populated by
  // the page itself through querySelectorAll.
  for (const m of html.matchAll(/<th data-k="(\w+)"/g))
    ths.push(Object.assign(makeEl(), { dataset: { k: m[1] } }));

  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(path.join(DIR, "banner.js"), "utf8"), sandbox);
  vm.runInContext(fs.readFileSync(path.join(DIR, "snapshots.js"), "utf8"), sandbox);
  vm.runInContext(fs.readFileSync(path.join(DIR, "query.js"), "utf8"), sandbox);
  vm.runInContext(fs.readFileSync(path.join(DIR, "data.js"), "utf8"), sandbox);
  vm.runInContext(blocks[0][1], sandbox, { filename: "query.html:inline" });

  const rowSlugs = () =>
    [...els.tbl.tBodies[0].innerHTML.matchAll(/data-slug="([\w-]+)"/g)].map(m => m[1]);
  // typing into the query box, the way a keystroke does
  const type = q => { els.q.value = q; els.q.oninput({ target: { value: q } }); };
  // NOTE: records come from inside the vm context, so arrays derived from them
  // (`records.filter(...)`) have that realm's Array prototype and will FAIL
  // deepStrictEqual against a test-realm array with identical contents. Compare
  // slug lists as joined strings, not as arrays.
  return { els, exs, ths, sandbox, rowSlugs, type, urls,
           records: sandbox.window.NORDSTERN.records };
}

/* ---- data ----------------------------------------------------------- */

test("data.js is generated and carries derived fields", () => {
  const { records } = boot();
  assert.ok(records.length >= 17, `only ${records.length} records`);
  for (const r of records) {
    assert.ok(r.derived, `${r.slug} has no derived block`);
    for (const k of ["capability", "terms", "reach", "quadrant", "orphaned",
                     "overtreatment_risk", "futile_treatment_risk", "harm_without_benefit"])
      assert.ok(k in r.derived, `${r.slug}.derived is missing ${k}`);
    assert.ok(r.measurement && r.toll, `${r.slug} missing measurement/toll`);
  }
});

test("data.js is in step with the YAML", () => {
  // The build artifact is generated; if someone edits a record and forgets to
  // rebuild, this is the only thing that would notice.
  const yamls = fs.readdirSync(path.join(DIR, "..", "entities")).filter(f => f.endsWith(".yaml"));
  const { records } = boot();
  assert.equal(records.length, yamls.length,
    "web/data.js is stale — run `python3 check.py --build`");
});

/* ---- boot ----------------------------------------------------------- */

test("boots with every record listed", () => {
  const { rowSlugs, records } = boot();
  assert.equal(rowSlugs().length, records.length);
});

test("a query narrows the set", () => {
  const { type, rowSlugs, records } = boot();
  type("capability:unsolved");
  const got = rowSlugs();
  assert.ok(got.length > 0 && got.length < records.length);
  for (const slug of got)
    assert.equal(records.find(r => r.slug === slug).derived.capability, "unsolved");
});

test("two terms are ANDed", () => {
  const { type, rowSlugs, records } = boot();
  type("capability:curable");
  const wide = rowSlugs().length;
  type("capability:curable reach:<0.5");
  const got = rowSlugs();
  assert.ok(got.length > 0 && got.length < wide, `${got.length} vs ${wide}`);
  for (const slug of got) {
    const r = records.find(x => x.slug === slug);
    assert.equal(r.derived.capability, "curable");
    assert.ok(r.derived.reach < 0.5, `${slug} reach ${r.derived.reach}`);
  }
});

test("a leading minus negates, over an array field", () => {
  // `-blocker.kind:knowledge` must mean NO blocker is knowledge, not
  // "some blocker is not knowledge" — the two differ on most records.
  const { type, rowSlugs, records } = boot();
  type("-blocker.kind:knowledge");
  const got = rowSlugs();
  assert.ok(got.length > 0 && got.length < records.length);
  for (const slug of got)
    assert.ok(!records.find(r => r.slug === slug).derived.blocker_kinds.includes("knowledge"),
      `${slug} has a knowledge blocker and should have been excluded`);
});

test("value-level OR is a union, not an intersection", () => {
  const { type, rowSlugs } = boot();
  type("blocker.standing:alleged");
  const a = rowSlugs();
  type("blocker.standing:disputed");
  const b = rowSlugs();
  type("blocker.standing:(alleged OR disputed)");
  const both = rowSlugs();
  assert.ok(a.length > 0 && b.length > 0);
  assert.ok(both.length >= Math.max(a.length, b.length), "OR narrowed instead of widening");
  for (const s of a.concat(b)) assert.ok(both.includes(s), `${s} dropped by the OR`);
});

test("free text still matches witness prose, not just names", () => {
  const { type, rowSlugs } = boot();
  type("lithium");
  assert.ok(rowSlugs().includes("bipolar"));
});

test("a query that matches nothing yields an empty table, not a crash", () => {
  const { type, rowSlugs } = boot();
  type("zzzznotathing");
  assert.deepEqual(rowSlugs(), []);
});

test("clear empties the query", () => {
  const { els, type, rowSlugs, records } = boot();
  type("capability:curable orphaned:true");
  assert.notEqual(rowSlugs().length, records.length);
  els.reset.onclick();
  assert.equal(els.q.value, "");
  assert.equal(rowSlugs().length, records.length);
});

/* ---- diagnostics: a bad term is answered, never silently dropped ---- */

test("an unknown field names the nearest real one", () => {
  const { els, type } = boot();
  type("capabilty:curable");
  assert.ok(els.qerr.classList.contains("on"), "the error panel stayed hidden");
  assert.match(els.qerr.innerHTML, /no field/);
  assert.match(els.qerr.innerHTML, /capability/);
});

test("a bad enum value lists the legal ones instead of returning nothing", () => {
  const { els, type, rowSlugs, records } = boot();
  type("capability:cured");
  assert.match(els.qerr.innerHTML, /has no value/);
  for (const v of ["curable", "managed", "partial", "unsolved"])
    assert.match(els.qerr.innerHTML, new RegExp(v), `did not offer "${v}"`);
  assert.equal(rowSlugs().length, records.length,
    "a term that could not be understood must be skipped, not applied");
  assert.match(els.count.textContent, /1 term ignored/);
});

test("a comparison on a non-numeric field says so", () => {
  const { els, type } = boot();
  type("capability:>0.5");
  assert.match(els.qerr.innerHTML, /not numeric/);
});

test("cross-term OR is refused with the syntax that does work", () => {
  // The deferred feature. Saying "not yet, here is what to type instead"
  // is the whole reason this is a hand-written parser.
  const { els, type } = boot();
  type("quadrant:frontier OR quadrant:\"empirical luck\"");
  assert.match(els.qerr.innerHTML, /not supported yet/);
  assert.match(els.qerr.innerHTML, /cost OR logistics/, "must show the alternation that works");
});

test("a half-typed term is not an error", () => {
  // `capability:` on the way to `capability:curable` must not flash red.
  const { els, type, rowSlugs, records } = boot();
  type("capability:");
  assert.ok(!els.qerr.classList.contains("on"), els.qerr.innerHTML);
  assert.equal(rowSlugs().length, records.length);
});

test("the error panel clears once the query is fixed", () => {
  const { els, type } = boot();
  type("capability:cured");
  assert.ok(els.qerr.classList.contains("on"));
  type("capability:curable");
  assert.ok(!els.qerr.classList.contains("on"), els.qerr.innerHTML);
});

test("nothing typed into the query box is injected as HTML", () => {
  // The diagnostics echo the offending token back, the page is public, and
  // ?q= means an attacker controls that token via a link. So: escaped.
  const { els, type } = boot();
  type("<script>alert(1)</script>:x");
  assert.ok(!/<script|<img/i.test(els.qerr.innerHTML), els.qerr.innerHTML);
  assert.match(els.qerr.innerHTML, /&lt;/, "the offending character must arrive escaped");
});

/* ---- the query is the share link ------------------------------------ */

test("a query in the URL is applied on boot", () => {
  const { els, rowSlugs, records } = boot("capability:unsolved");
  assert.equal(els.q.value, "capability:unsolved");
  for (const slug of rowSlugs())
    assert.equal(records.find(r => r.slug === slug).derived.capability, "unsolved");
  assert.ok(rowSlugs().length < records.length);
});

test("typing updates the URL so the view can be linked", () => {
  const { type, urls } = boot();
  type("capability:curable reach:<0.5");
  const last = urls[urls.length - 1];
  assert.match(last, /^\?q=/);
  assert.equal(decodeURIComponent(last.slice(3)), "capability:curable reach:<0.5");
});

/* ---- the canned questions ------------------------------------------ */

test("the two derived flags that keep the grammar small are real and non-empty", () => {
  // `measurement_gap` and `only_knowledge_blockers` exist so the query
  // language needs neither a cross-term OR nor an `every` quantifier. If
  // check.py stops emitting them, two Asks silently return nothing.
  const { records } = boot();
  for (const f of ["measurement_gap", "only_knowledge_blockers"]) {
    assert.ok(records.every(r => f in r.derived), `check.py no longer derives ${f}`);
    assert.ok(records.some(r => r.derived[f]), `${f} matches nothing — rebuild or re-check the rule`);
  }
  for (const r of records) {
    assert.equal(r.derived.measurement_gap,
      r.derived.overtreatment_risk || r.derived.futile_treatment_risk,
      `${r.slug}: measurement_gap disagrees with the two risks it unions`);
    assert.equal(r.derived.only_knowledge_blockers,
      r.blockers.length > 0 && r.blockers.every(b => b.kind === "knowledge"),
      `${r.slug}: only_knowledge_blockers disagrees with its blockers`);
  }
});

test("clicking a column sorts, and clicking again flips the direction", () => {
  // Asserted as monotonicity rather than exact reversal: `reach` has a tie at 0
  // (huntington and me-cfs), and a reversed sort is not a mirror image when
  // keys are equal.
  const { ths, rowSlugs, records } = boot();
  const reach = s => records.find(r => r.slug === s).derived.reach;
  const th = ths.find(t => t.dataset.k === "reach");
  const monotone = (vals, dir) =>
    vals.every((v, i) => i === 0 || (dir > 0 ? v >= vals[i - 1] : v <= vals[i - 1]));

  th.onclick();
  const first = rowSlugs().map(reach);
  const dirFirst = monotone(first, 1) ? 1 : -1;
  assert.ok(monotone(first, dirFirst), "first click did not sort: " + first.join(","));

  th.onclick();
  const second = rowSlugs().map(reach);
  assert.ok(monotone(second, -dirFirst),
    "second click did not flip direction: " + second.join(","));
  assert.equal(second.length, first.length, "rows were dropped by sorting");
});

test("sorting by a column with missing values does not drop rows", () => {
  const { ths, rowSlugs, records } = boot();
  ths.find(t => t.dataset.k === "_cost").onclick();   // many records have no price
  assert.equal(rowSlugs().length, records.length);
});

/* ---- the detail panel ---------------------------------------------- */

test("every record renders a detail view without throwing", () => {
  // The real risk: optional blocks. Only some records have `window`, `strata`
  // or `moved`, and a missing one must not take the page down.
  const { els, records } = boot();
  for (const r of records) {
    els.tbl.tBodies[0].innerHTML = "";
    const rows = [];
    els.tbl.querySelectorAll = () => rows;
    // drive selection the way a click would
    const before = els.detail.innerHTML;
    assert.doesNotThrow(() => {
      const tr = { dataset: { slug: r.slug }, onclick: null };
      rows.push(tr);
      // re-render with this row selected
      els.q.oninput({ target: { value: "" } });
      tr.onclick && tr.onclick();
    }, `${r.slug} threw while rendering`);
    void before;
  }
});

test("the detail panel shows the empty state before anything is picked", () => {
  const { els } = boot();
  assert.match(els.detail.innerHTML, /ask the register a question/i);
});

test("a record with strata renders them; one without does not fake them", () => {
  const { records } = boot();
  const withStrata = records.filter(r => r.strata);
  assert.ok(withStrata.length >= 1, "expected at least breast-cancer to have strata");
  for (const r of withStrata) {
    const total = r.strata.reduce((s, x) => s + x.fraction.value, 0);
    assert.ok(Math.abs(total - 1) < 0.05, `${r.slug} strata sum to ${total}`);
  }
});

/* ---- saying what the words mean ------------------------------------ */

test("the quadrant is never labelled \"solved\"", () => {
  // The label meant "the known x fixable cell of the 2x2" and read, on a card,
  // as a verdict on the disease. Breast cancer and Crohn's both sit in that
  // cell; neither is solved by any reading.
  const { records } = boot();
  const quadrants = new Set(records.map(r => r.derived.quadrant));
  assert.ok(!quadrants.has("solved"), [...quadrants].join(", "));
  assert.ok(quadrants.has("known & treatable"));
});

test("every map cell a record lands in is defined in the glossary", () => {
  // A GENERAL RULE RATHER THAN A LIST, because the list is what went stale.
  // The map grew from four cells to six (gaps.md #89) and the hardcoded
  // glossary test below still passed, because it only checked the four names
  // that already existed. A new cell can now reach the public page undefined
  // exactly once — here.
  const { records } = boot();
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const spec = html.slice(html.indexOf('<dialog id="spec">'), html.indexOf("</dialog>"));
  const flat = spec.replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
  for (const cell of new Set(records.map(r => r.derived.quadrant)))
    assert.ok(flat.includes(cell), `map cell "${cell}" is not defined in the spec`);
});

test("disease-modifying is not filed as untreatable", () => {
  // gaps.md #89. The boolean this replaced put `disease-modifying` in the same
  // bucket as `none`, so ischaemic heart disease and stroke — the first and
  // third largest causes of death on Earth — read as "nothing can be done".
  const { records } = boot();
  const by = Object.fromEntries(records.map(r => [r.slug, r.derived.quadrant]));
  for (const slug of ["ischaemic-heart-disease", "stroke", "rheumatic-heart-disease"])
    assert.equal(by[slug], "known & modifiable", slug);
  // COPD is `symptomatic` and stays put; it is the record that chose this
  // repair over moving the rung or deleting the map.
  assert.equal(by["copd"], "engineering problem");
});

test("the spec defines the load-bearing terms", () => {
  // The vocabulary used to be a second dialog behind a second button. Stripping
  // the tool merged it into the spec, because "what the words mean" and "how to
  // ask" are the same document for anyone who arrived on purpose.
  const { els } = boot();
  els.specBtn.onclick();
  assert.equal(els.spec.open, true, "spec did not open");
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const gloss = html.slice(html.indexOf('<dialog id="spec">'), html.indexOf("</dialog>"))
                     .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
  for (const term of ["capability", "terms", "reach", "delivery", "quadrant",
                      "known", "engineering problem", "empirical luck", "frontier",
                      "suppressive", "curative", "prognostic", "predictive", "n/a",
                      "toll", "window", "strata", "standing", "no champion",
                      "overtreatment risk", "futile treatment risk", "harm without benefit",
                      "known & modifiable", "empirical foothold"])
    assert.ok(gloss.includes(term), `glossary does not define "${term}"`);
  assert.match(gloss, /not "solved"|<b>not<\/b> that the disease is solved|malformed question/,
    "the spec must say what the quadrant does NOT mean");
  els.specClose.onclick();
  assert.equal(els.spec.open, false);
});

test("the query reference opens and lists every field the parser knows", () => {
  // The field list is rendered from the parser's own registry, so a field
  // that exists is documented and a documented field exists. Asserting it
  // here is what stops the reference drifting into fiction.
  const { els, sandbox } = boot();
  els.specBtn.onclick();
  assert.equal(els.spec.open, true, "the query reference did not open");
  const listed = els.qfields.innerHTML;
  for (const name of Object.keys(sandbox.NordsternQuery.FIELDS))
    assert.ok(listed.includes(">" + name + "<"), `the reference omits the field "${name}"`);
  assert.match(listed, /derived/, "derived fields must be marked as calculations");
  assert.match(listed, /curable/, "enum fields must list their legal values");
  els.specClose.onclick();
  assert.equal(els.spec.open, false);
});

test("the query reference states the two rules and the deferred feature", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const from = html.indexOf('<dialog id="spec">');
  assert.ok(from > 0, "no query reference dialog on the page");
  const help = html.slice(from, html.indexOf("</dialog>", from));
  for (const bit of ["the field decides", "some", "only_knowledge_blockers",
                     "OR across terms", "did you mean"])
    assert.ok(help.includes(bit), `the query reference does not explain "${bit}"`);
});

test("a card states its verdict in a sentence, with the qualifier attached", () => {
  const { els, records } = boot();
  const bc = records.find(r => r.slug === "breast-cancer");
  assert.ok(bc, "breast-cancer record missing");
  els.q.oninput({ target: { value: "breast-cancer" } });
  // select it the way a click does
  const rows = [];
  els.tbl.querySelectorAll = () => rows;
  els.q.oninput({ target: { value: "breast-cancer" } });
  assert.match(els.tbl.tBodies[0].innerHTML, /data-slug="breast-cancer"/);
});

test("every record produces a verdict sentence and no undefined leaks in", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const { records } = boot();
  // LEAD and PRICE must cover every value the data actually contains.
  const leads = html.slice(html.indexOf("const LEAD"), html.indexOf("const PRICE"));
  const prices = html.slice(html.indexOf("const PRICE"), html.indexOf("function verdict"));
  for (const r of records) {
    assert.ok(leads.includes(r.derived.capability + ":"),
      `no verdict sentence for capability "${r.derived.capability}"`);
    assert.ok(prices.includes(r.derived.terms + ":"),
      `no price clause for terms "${r.derived.terms}"`);
  }
});

/* ---- residue: what the disease leaves in someone it cured ----------- */

test("`restored` is derived from both halves and never claims too much", () => {
  // The question the field exists to answer: are they back to the state they
  // were in before any of it? It is wrong in two directions if it reads only
  // one half — which is exactly what the page did before `residue` existed.
  const { records } = boot();
  const CLEAN = new Set(["none", "minor"]);
  for (const r of records) {
    const took = !CLEAN.has(r.toll.severity);
    const left = !CLEAN.has((r.residue || {}).severity || "none");
    const cap = r.derived.capability !== "unsolved"
      || ["prophylaxis", "eradicated"].includes(r.axes.prevention);
    const want = !cap ? "n/a"
      : took && left ? "both" : took ? "cure-costs" : left ? "disease-residue" : "restored";
    assert.equal(r.derived.restored, want, `${r.slug}: restored disagrees with toll x residue`);
  }
});

test("tuberculosis no longer claims a clean cure", () => {
  // The specific defect this field was added for. TB's card read "A finite
  // treatment ends this." with no qualifier, for a disease that permanently
  // scars the lungs of a large share of the people it cures.
  const { records } = boot();
  const tb = records.find(r => r.slug === "tuberculosis");
  assert.ok(tb.residue, "tuberculosis has no residue block");
  assert.equal(tb.derived.terms, "clean", "the DRUGS still take almost nothing — that part was right");
  assert.equal(tb.derived.restored, "disease-residue");
  assert.match(tb.residue.what, /lung|bronchiectasis|fibrosis/i);
});

test("a residue on a no-capability record is a reviewed exception, not a habit", () => {
  // This test used to assert that a residue NEVER appears without capability.
  // Dracunculiasis broke it and the rule was wrong, not the record: there is no
  // drug and no vaccine, the worm emerges over weeks, the episode ENDS, and a
  // minority are permanently disabled by the secondary infection. A residue can
  // outlast an episode that resolved on its own.
  //
  // What a residue still cannot mean is damage from a disease that is STILL
  // doing it — Huntington's, ME/CFS — where the damage is the disease and the
  // axes already say so. check.py cannot tell those apart, so it warns.
  //
  // This pins the exceptions instead: a new one has to be argued for rather
  // than appearing quietly.
  const { records } = boot();
  const EXPECTED = new Set([
    "dracunculiasis",   // self-limiting; no drug, worm emerges over weeks, episode ends
    "marburg",          // survivors recover on supportive care and carry sequelae
    // Cryptosporidiosis is the third and it stretches the field further than
    // either. The diarrhoea resolves — so the episode ends, satisfying the rule
    // above — but the residue is STUNTING AND COGNITIVE DEFICIT, and the cohort
    // evidence attaches it to infection that caused no diarrhoea at all. So the
    // damage lands on a child who was never ill enough to be diagnosed, let
    // alone cured, and `residue` is defined as what the disease leaves in
    // someone it was CURED in. Admitted because the harm is real and no other
    // field can hold it; flagged in the record's own `holes` and in gaps.md
    // #231, because the definition is what should move, not the record.
    "cryptosporidiosis",
    // Disorders of consciousness is the fourth, and it satisfies the rule more
    // cleanly than the three above. THE INJURY IS A COMPLETED EVENT — the
    // anoxia is over, the impact was a moment — and what persists is the damage
    // it left, exactly as in `stroke`. It is not the case the warning exists to
    // catch, where the disease is still doing harm and the damage belongs in
    // the axes.
    //
    // What makes it land here at all is that `capability` reads `unsolved`,
    // because the intervention rung is `symptomatic`: nothing reliably restores
    // consciousness. So the register has a completed injury with a catastrophic
    // permanent residue and no capability to cure anyone of it — which is
    // arguably a gap in `restored` rather than in the record, since "back to
    // the state before it all" is a meaningful question here and `n/a` refuses
    // to answer it. Argued in the record's own `holes`.
    "disorders-of-consciousness",
  ]);
  const found = records.filter(r => r.residue && r.derived.restored === "n/a")
                       .map(r => r.slug).sort();
  assert.equal(found.join(" "), [...EXPECTED].sort().join(" "),
    "a residue appeared on a record with no capability. If the episode genuinely " +
    "ends (self-limiting), add it to EXPECTED with a note. If the disease is " +
    "still causing the damage, the residue belongs in the axes, not here.");
});

test("the verdict sentence carries a residue clause, and covers every value", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const { records } = boot();
  const res = html.slice(html.indexOf("const RESIDUE"), html.indexOf("function verdict"));
  assert.ok(res.length > 0, "no RESIDUE map in the verdict block");
  for (const r of records)
    assert.ok(res.includes(r.derived.residue_terms + ":"),
      `no residue clause for "${r.derived.residue_terms}"`);
  // and every `restored` value must have wording, or the card renders undefined
  const verdict = html.slice(html.indexOf("function verdict"), html.indexOf("function detail"));
  for (const v of new Set(records.map(r => r.derived.restored)))
    assert.ok(v === "n/a" || v === "restored" || verdict.includes(`"${v}"`),
      `the card has no wording for restored="${v}"`);
});

test("the spec defines residue and says how it differs from toll", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const gloss = html.slice(html.indexOf('<dialog id="spec">'), html.indexOf("</dialog>"));
  for (const term of ["residue", "restored", "disease-residue", "cure-costs"])
    assert.ok(gloss.includes(term), `spec does not define "${term}"`);
  assert.match(gloss, /n\/a is not <\/b>|<b>n\/a is not restored/,
    "the spec must say n/a is not restored");
});

test("a spanning record warns that the question is malformed", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const { records } = boot();
  assert.ok(records.some(r => r.derived.spans_ladder), "no spanning record to warn about");
  assert.match(html, /spans_ladder \? `/, "no strata banner in the verdict block");
  assert.match(html, /malformed\s*\n?\s*question/, "the banner must say the question is malformed");
});

/* ---- the public-facing caveat -------------------------------------- */

test("the unverified-data warning is rendered, not written, and carries the counts", () => {
  // This page is going public with numbers written from memory, so the warning
  // is load-bearing. It USED TO BE hand-written HTML on each page, and the
  // tool's copy went stale: it told visitors `mondo:` was unresolved on every
  // record long after 93 of 101 had been resolved. Nobody edits a warning banner
  // when they resolve an ontology id.
  //
  // So it is rendered from the snapshot now, by banner.js, which both pages
  // load. This test checks the OUTPUT rather than the markup, and checks that
  // the markup no longer contains a figure anybody could forget to update.
  const { els, sandbox } = boot();
  const snap = sandbox.window.NORDSTERN_SNAPSHOTS.at(-1);
  const shown = els.prov.innerHTML;
  const p = snap.provenance;

  assert.ok(shown.length > 200, "the provenance banner rendered nothing");
  assert.match(shown, /[Dd]o not cite/);
  assert.match(shown, /recall/);
  assert.match(shown, /reasoning/);
  assert.match(shown, /unknown/);
  assert.ok(shown.includes(String(p.mondo_resolved)) || p.mondo_unresolved === 0,
            "the banner must state the real mondo resolution count");

  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  assert.match(html, /class="warn"/);
  assert.ok(/src="banner\.js"/.test(html), "the tool must load the shared renderer");
  assert.ok(!/unresolved on every record/.test(html),
            "the stale mondo claim is back, hand-written");
});

test("both pages render the same provenance facts from the same numbers", () => {
  // The failure this guards is drift between two pages that describe one
  // dataset. They may open differently — "0 of 1,582" is a finding on a landing
  // page and an instruction on a query tool — and every number must agree.
  const Banner = require("./banner.js");
  const { sandbox } = boot();
  const snap = sandbox.window.NORDSTERN_SNAPSHOTS.at(-1);
  const lead = Banner.render(snap, { tone: "lead", queryHref: "query.html?q=" });
  const warn = Banner.render(snap, { tone: "warn", queryHref: "?q=" });

  const figures = t => (t.match(/\d[\d,]*/g) || []).sort().join(" ");
  assert.equal(figures(lead), figures(warn),
               "the two banners quote different numbers for the same register");

  // THE DENOMINATOR IS THE CONTRACT. The banner used to say "0 of 1,582
  // sourced", which reads as a backlog of 1,582 lookups — and 915 of those are
  // quantities no dataset holds, because this register is where they are
  // defined. The tiers exist to stop the page overstating its own problem.
  const t = snap.provenance.by_tier;
  const fmt = v => v.toLocaleString("en-US");
  for (const src of [lead, warn]) {
    assert.ok(src.includes(fmt(t.sourceable.total)),
              "the banner must state the SOURCEABLE denominator, not the raw total");
    assert.ok(src.includes(fmt(t.supportable.total)) &&
              src.includes(fmt(t.judged.total)),
              "the banner must break out supportable and judged, or the number " +
              "it leads with is unexplained");
    assert.ok(!new RegExp(`of ${fmt(snap.provenance.scalars)}\\b`).test(src),
              "the banner presents every scalar as sourceable again");
    assert.match(src, /None of the three is a citation|None of them yet/);
  }

  const idx = fs.readFileSync(path.join(DIR, "index.html"), "utf8");
  const qry = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  for (const [name, html] of [["index.html", idx], ["query.html", qry]])
    assert.ok(/src="banner\.js"/.test(html), `${name} does not load banner.js`);
});

test("no external dependency other than fonts", () => {
  // The register should stay readable if a CDN dies.
  // A dependency is something the page LOADS — a script or stylesheet. A link
  // the reader may click (the challenge issue on GitHub) is not one; if GitHub
  // dies the register still renders.
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const loads = [...html.matchAll(/<(?:script|link)\b[^>]*?(?:src|href)="(https?:\/\/[^"]+)"/g)].map(m => m[1]);
  assert.ok(loads.length > 0, "expected at least the font stylesheet");
  for (const u of loads)
    assert.match(u, /fonts\.(googleapis|gstatic)\.com/, `unexpected external dependency: ${u}`);
  const others = [...html.matchAll(/https?:\/\/[^"' `]+/g)].map(m => m[0])
    .filter(u => !/fonts\.(googleapis|gstatic)\.com/.test(u));
  for (const u of others)
    assert.match(u, /^https:\/\/github\.com\/fndtnio\/Nordstern/, `unexpected external URL: ${u}`);
});

/* ---- challenge a rating ---------------------------------------------
 * The unit of disagreement is an assertion, so every card carries a link that
 * opens a GitHub issue already naming the record id, the assertion id and the
 * evidence rule. If the ids were missing, the maintainer's first reply would
 * be "which record?", and the challenge would be a comment, not a challenge.
 * ------------------------------------------------------------------- */
test("every card carries a pre-filled challenge link naming its assertion", () => {
  const { els, records } = boot();
  for (const r of records) {
    const rows = [];
    els.tbl.querySelectorAll = () => rows;
    const tr = { dataset: { slug: r.slug }, onclick: null };
    rows.push(tr);
    els.q.oninput({ target: { value: "" } });
    tr.onclick();
    const html = els.detail.innerHTML;
    const m = html.match(/<a class="challenge" href="([^"]+)"/);
    assert.ok(m, `${r.slug}: no challenge link`);
    const url = new URL(m[1]);
    assert.equal(url.origin + url.pathname, "https://github.com/fndtnio/Nordstern/issues/new");
    const title = url.searchParams.get("title"), body = url.searchParams.get("body");
    assert.ok(title.includes(r.assertion.id), `${r.slug}: title lacks assertion id`);
    assert.ok(body.includes(r.id) && body.includes(r.assertion.id), `${r.slug}: body lacks an id`);
    assert.ok(body.includes(`entities/${r.slug}.yaml`), `${r.slug}: body lacks the file path`);
    assert.match(body, /quote/i, `${r.slug}: body does not state the evidence rule`);
    assert.ok(!/undefined|NaN/.test(title + body), `${r.slug}: undefined leaked into the issue`);
  }
});

/* ---- the tool stays a tool ------------------------------------------
 * Stripped on 2026-08-26 to the query bar and four utilities. The controls
 * that went — six canned questions, seven dropdowns, seven flag chips — were
 * all *query writers*, which was itself the fix for an earlier version whose
 * filter state could not express its own canned questions. They were removed
 * for a different reason: **an answer supplied before the question is clutter
 * on a tool somebody came to on purpose.** The map at index.html is where a
 * figure hands you a query.
 *
 * Clutter comes back one control at a time and each one looks reasonable, so
 * the constraint is written down here rather than remembered.
 * ------------------------------------------------------------------- */

test("the query page carries the bar and nothing that answers for you", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const body = html.slice(html.indexOf("<body>"), html.indexOf('<dialog id="spec">'));

  assert.ok(!/<select/.test(body), "a dropdown is back on the query page");
  assert.ok(!/class="chip"/.test(body), "a flag chip is back on the query page");
  assert.ok(!/class="ask"/.test(body), "a canned question is back on the query page");

  // and what must stay
  assert.match(body, /id="q"/, "the query bar is the tool");
  assert.match(body, /id="qerr"/, "a bad term must still be answered, not dropped");
  assert.match(body, /id="specBtn"/, "the spec must be one click away");
  for (const id of ["reset", "dlJson", "dlCsv", "count", "tbl", "detail"])
    assert.ok(body.includes(`id="${id}"`), `the page lost #${id}`);
});

test("the worked examples all run, and none returns nothing", () => {
  // An example you cannot run is a screenshot, and an example that has rotted
  // into a query returning nothing is worse than none — it teaches a visitor
  // that the tool is broken. These were canned buttons and are now the only
  // place a first-time reader is shown a real query, so they carry more weight
  // than they did.
  const { els, sandbox, records } = boot();
  const Q = sandbox.NordsternQuery;
  const html = els.qexamples.innerHTML;
  const qs = [...html.matchAll(/data-q="([^"]+)"/g)]
    .map(m => m[1].replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
                  .replace(/&quot;/g, '"'));

  assert.ok(qs.length >= 6, `only ${qs.length} worked examples rendered`);
  for (const q of qs) {
    const res = Q.run(records, q);
    // errors come from inside the vm realm, so compare the length rather
    // than deepEqual against a test-realm [] — see the note in boot()
    assert.equal(res.errors.length, 0,
                 `example "${q}" does not parse: ${JSON.stringify(res.errors)}`);
    assert.ok(res.records.length > 0, `example "${q}" returns nothing`);
    assert.ok(res.records.length < records.length,
              `example "${q}" returns the whole register — it demonstrates nothing`);
  }
});

test("clicking a worked example runs it and closes the spec", () => {
  const { els, exs, rowSlugs, records } = boot();
  els.specBtn.onclick();
  assert.equal(els.spec.open, true);
  assert.ok(exs.length >= 6, "the example buttons were not wired up");
  const ex = exs.find(e => e.dataset.q === "quadrant:frontier");
  assert.ok(ex, "the frontier example is missing");
  ex.onclick();
  assert.equal(els.spec.open, false, "running an example should close the spec");
  assert.equal(els.q.value, "quadrant:frontier", "the query box must show what ran");
  assert.equal(rowSlugs().length,
               records.filter(r => r.derived.quadrant === "frontier").length);
});

test("the spec is linkable, because a reference nobody can send is a screenshot", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  assert.match(html, /p\.has\("spec"\)/,
    "?spec must open the reference on load, so it can be linked to");
});

test("the spec documents the grammar, the fields and the vocabulary in one place", () => {
  const html = fs.readFileSync(path.join(DIR, "query.html"), "utf8");
  const spec = html.slice(html.indexOf('<dialog id="spec">'), html.indexOf("</dialog>"));
  for (const section of ["The grammar, entire", "Worked examples", "Every field",
                         "What the words mean"])
    assert.ok(spec.includes(section), `the spec has no "${section}" section`);
  assert.ok(!/<dialog id="gloss"/.test(html),
    "the glossary is a second dialog again — it belongs in the spec");
});
