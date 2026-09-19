/* =====================================================================
 * Engpass dashboard tests — run with:  node --test web/
 *
 * SAME RULE AS `dashboard.test.js`, ONE REGISTER OVER: every figure links to
 * the query that produces it, and that query must actually return that number.
 *
 * AND ONE RULE THAT IS ONLY THIS PAGE'S. A derived link is evidence — somebody
 * rating that disease said this is what they were waiting on. A claim is an
 * assertion that may simply be wrong. **The entire value of this register is
 * that the two are not confused**, so the tests below check that they are drawn
 * differently and never counted together.
 * ===================================================================== */
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const DIR = __dirname;
const Query = require("./query.js");

/* The query engine runs over the FULL payload, not over slim.js — slim carries
   the derived fields the dashboard draws and not the stored ones the language
   also indexes, so a query touching `axes.*` throws against it. Same loader
   dashboard.test.js uses. */
function loadRecords() {
  const s = { window: {}, JSON, Object, Array, console };
  s.window = s;
  vm.createContext(s);
  vm.runInContext(fs.readFileSync(path.join(DIR, "data.js"), "utf8"), s);
  return s.window.NORDSTERN.records;
}

function boot() {
  const html = fs.readFileSync(path.join(DIR, "engpass.html"), "utf8");
  const inline = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  assert.equal(inline.length, 1, "expected exactly one inline <script>");

  const els = {};
  const get = id => (els[id] ||= { id, innerHTML: "" });
  ["prov", "body"].forEach(get);

  const sandbox = {
    window: {},
    document: { getElementById: get },
    location: { href: "" },
    encodeURIComponent, decodeURIComponent,
    JSON, Object, Array, Set, Map, String, Number, Math, RegExp, console,
  };
  sandbox.window = sandbox;
  for (const f of ["banner.js", "slim.js", "snapshots.js", "engpass-snapshots.js"])
    vm.runInContext(fs.readFileSync(path.join(DIR, f), "utf8"), vm.createContext(sandbox));
  vm.runInContext(inline[0][1], sandbox, { filename: "engpass.html:inline" });

  return { html, rendered: els.prov.innerHTML + els.body.innerHTML, sandbox,
           snap: sandbox.window.ENGPASS_SNAPSHOTS.at(-1),
           nsnap: sandbox.window.NORDSTERN_SNAPSHOTS.at(-1),
           slim: sandbox.window.NORDSTERN_SLIM };
}

const sections = rendered =>
  [...rendered.matchAll(/<h2><span class="n">(\d\d)<\/span>([\s\S]*?)<\/h2>/g)]
    .map(m => m[2].replace(/\s+/g, " ").trim());

/* NORMALISE ARRAYS ACROSS THE VM BOUNDARY BEFORE COMPARING THEM.
   `snap` is parsed inside the vm context, so its arrays carry that realm's
   `Array.prototype` — and `deepStrictEqual` compares prototypes, so two arrays
   holding the identical single string fail with an error message showing two
   identical values. Spreading rebuilds them in this realm. Cost an hour once;
   written down so it costs nobody else one. */
const here = xs => [...(xs || [])];

function sectionBody(rendered, heading) {
  const start = rendered.indexOf(`</span>${heading}</h2>`);
  assert.ok(start > -1, `no section headed ${heading}`);
  const rest = rendered.slice(start);
  const end = rest.indexOf("<h2>", 1);
  return end > -1 ? rest.slice(0, end) : rest;
}

test("every obstacle in the snapshot gets exactly one section", () => {
  const { rendered, snap } = sections ? boot() : boot();
  const heads = sections(rendered);
  const names = Object.values(snap.resolution_members).map(m => m.name);
  for (const nm of names) {
    const hits = heads.filter(h => h === nm.replace(/\s+/g, " ").trim()).length;
    assert.equal(hits, 1, `expected exactly one section for ${JSON.stringify(nm)}`);
  }
});

test("sections are ranked by how many records each obstacle blocks", () => {
  /* The whole reason this register exists is the backward direction — answering
     this releases those — so the ordering IS the argument. */
  const { rendered, snap } = boot();
  const byName = {};
  Object.entries(snap.resolution_members).forEach(([slug, m]) => {
    byName[m.name.replace(/\s+/g, " ").trim()] =
      (snap.blocks_members[slug] || []).length;
  });
  const counts = sections(rendered).filter(h => h in byName).map(h => byName[h]);
  assert.equal(counts.length, Object.keys(snap.resolution_members).length);
  const sorted = counts.slice().sort((a, b) => b - a);
  assert.deepEqual(counts, sorted, "obstacle sections must run most-blocking first");
});

test("each section lists exactly the records the snapshot says it blocks", () => {
  const { rendered, snap } = boot();
  for (const [slug, m] of Object.entries(snap.resolution_members)) {
    const body = sectionBody(rendered, m.name.replace(/\s+/g, " ").trim());
    const derived = [...body.matchAll(/<a class="chip "[^>]*>([a-z0-9-]+)/g)]
      .map(x => x[1]);
    assert.deepEqual(derived.sort(), here(snap.blocks_members[slug]).sort(),
                     `${slug}: derived chips disagree with blocks_members`);
    const head = body.match(/<span class="obn">(\d+)<\/span>/);
    assert.equal(Number(head[1]), (snap.blocks_members[slug] || []).length,
                 `${slug}: the headline count and the names printed disagree`);
  }
});

test("a claim is drawn as a claim and is never counted as a derived link", () => {
  /* `check.py` errors if a claim names a disease that already cites the record —
     the link would be stored twice and the copies could drift. The page has the
     matching obligation: never render one as the other. */
  const { rendered, snap } = boot();
  for (const [slug, claims] of Object.entries(snap.claims_by_obstacle || {})) {
    const m = snap.resolution_members[slug];
    const body = sectionBody(rendered, m.name.replace(/\s+/g, " ").trim());
    const claimed = [...body.matchAll(/<a class="chip claim"[\s\S]*?>([a-z0-9-]+)/g)]
      .map(x => x[1]);
    assert.deepEqual(claimed.sort(), here(claims).map(c => c.unblocks).sort(),
                     `${slug}: claim chips disagree with the snapshot`);
    const derived = here(snap.blocks_members[slug]);
    for (const c of claimed)
      assert.ok(!derived.includes(c),
        `${slug}: ${c} is both claimed and derived — that link is derived, not claimed`);
  }
});

test("every chip resolves to exactly the record it names", () => {
  /* The dashboard rule: a figure whose link disagrees with it is worse than a
     figure with no link, because the visitor believes the page. */
  const { rendered } = boot();
  const recs = loadRecords();
  const links = [...rendered.matchAll(
    /<a class="chip[^"]*" href="query\.html\?q=([^"]+)"[^>]*>([a-z0-9-]+)/g)];
  assert.ok(links.length > 100, "expected the chip fields to produce many links");
  const bad = [];
  const seen = new Set();
  for (const [, q, slug] of links) {
    const query = decodeURIComponent(q);
    if (seen.has(query + "|" + slug)) continue;
    seen.add(query + "|" + slug);
    const rows = Query.run(recs, query).records;
    if (rows.length !== 1 || rows[0].slug !== slug)
      bad.push(`${query} → ${rows.length} row(s)` +
               (rows.length === 1 ? `, ${rows[0].slug}` : "") + `, expected ${slug}`);
  }
  assert.deepEqual(bad, [], "a chip links to a query that returns something else:\n  "
    + bad.join("\n  "));
});

test("the untagged pile is listed, not just counted", () => {
  /* Its size is a number; its CONTENT is the argument for splitting Nordstern's
     `knowledge` kind, because several entries are not questions at all. */
  const { rendered, snap } = boot();
  assert.equal(snap.untagged_list.length, snap.untagged_knowledge_blockers);
  const items = [...rendered.matchAll(/<li><a [^>]*><b>([a-z0-9-]+)<\/b><\/a>/g)];
  assert.equal(items.length, snap.untagged_list.length,
    "every untagged blocker should be printed, not summarised");
});

test("the diff is computed at build time, not in the page", () => {
  const { html, sandbox } = boot();
  assert.ok(Array.isArray(sandbox.window.ENGPASS_DIFFS),
    "engpass-snapshots.js must publish the build-time diffs");
  assert.match(html, /ENGPASS_DIFFS/, "the page must read the generated diff");
  assert.ok(!/SNAPS\s*\[\s*SNAPS\.length\s*-\s*2\s*\]/.test(html),
    "the page appears to compare two snapshots itself — that derivation is check.py's");
});

test("with nothing comparable behind it, the page says so", () => {
  const { rendered, sandbox } = boot();
  const d = sandbox.window.ENGPASS_DIFFS.at(-1);
  if (!d || d.skipped) {
    assert.match(rendered, /No comparison\s+yet/);
    assert.ok(!/questions? changed resolution/.test(rendered),
      "must not print a movement figure it cannot compute");
  }
});

test("the page separates earned obstacles from ones cited by nothing", () => {
  const { rendered, snap } = boot();
  const top = Object.keys(snap.resolution_members)
    .filter(s => !(snap.blocks_members[s] || []).length);
  if (top.length) {
    assert.match(rendered, /Cited by nothing/,
      "top-down obstacles must be labelled, not mixed in with earned ones");
    assert.match(rendered, /marburg/,
      "the Marburg warning belongs beside the top-down entries");
  }
  for (const s of top) {
    const body = sectionBody(rendered,
      snap.resolution_members[s].name.replace(/\s+/g, " ").trim());
    assert.match(body, /class="ob topdown"/, `${s} should be marked top-down`);
  }
});

test("the provenance banner is Nordstern's, with the Engpass-only clause added", () => {
  /* Three hand-written copies of one warning drifted once already. This page
     inherits the register whose ratings every number here derives from, and
     adds only the sentence that is untrue over there. */
  const { rendered } = boot();
  assert.match(rendered, /Experimental dataset/);
  // whitespace-insensitive: the sentence wraps in the source
  assert.match(rendered.replace(/\s+/g, " "),
    /that link is <b>derived<\/b> and it is evidence/);
});
