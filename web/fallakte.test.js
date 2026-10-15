/* =====================================================================
 * Fallakte page tests — run with:  node --test web/
 *
 * THESE PAGES ARE MEANT TO BE SHARED WITH STRANGERS, so the tests are about
 * the two ways a shared page fails: a link that goes nowhere, and a claim on
 * the page that the data does not support.
 *
 * The register's own rule applies here too — a sentence about the data is a
 * stored opinion that is right when written and silently wrong afterwards. So
 * these assert that the pages COMPUTE what they display rather than stating it.
 * ===================================================================== */
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const DIR = __dirname;
const read = f => fs.readFileSync(path.join(DIR, f), "utf8");

function data() {
  const src = read("fallakte-data.js");
  const sandbox = { window: {} };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox);
  return sandbox.window.FALLAKTE;
}

const D = data();
const LANDING = read("fallakte.html");
const VIEWER = read("case.html");

test("the artifact is there and shaped the way the pages expect", () => {
  assert.equal(D.register, "fallakte");
  assert.ok(/^\d{4}-\d{2}-\d{2}$/.test(D.generated), "a build date");
  assert.ok(D.cases.length >= 1, "at least one case");
  assert.ok(D.about.glossary.html.length > 500, "the glossary travels with it");
  for (const c of D.cases) {
    for (const k of ["slug", "id", "name", "one_line", "status", "opened", "updated"])
      assert.ok(c[k], `${c.slug} has ${k}`);
    assert.ok(c.doc.html.length > 1000, `${c.slug} has a rendered document`);
    assert.ok(c.doc.headings.length > 5, `${c.slug} has a contents list`);
  }
});

test("NO LINK IN A PUBLISHED CASE FILE POINTS AT A REPOSITORY PATH", () => {
  // The failure this exists for: a case file links to `../../GLOSSARY.md`
  // because that is where the file is in the repo, and the published page then
  // 404s for every reader. The build rewrites them; this proves it happened.
  const bodies = D.cases.map(c => c.doc.html).concat(
    Object.values(D.about).map(a => a.html));
  const bad = [];
  for (const html of bodies)
    for (const m of html.matchAll(/href="([^"]+)"/g))
      if (!/^(https?:\/\/|#|query\.html|fallakte\.html|case\.html|index\.html|engpass\.html)/
            .test(m[1])) bad.push(m[1]);
  assert.deepEqual(bad, [], "links that would be dead once published");
});

test("the rendered documents carry no unrendered markdown and no raw HTML", () => {
  for (const c of D.cases) {
    assert.ok(!c.doc.html.includes("**"), `${c.slug}: unrendered bold`);
    assert.ok(!/<script/i.test(c.doc.html), `${c.slug}: raw script tag`);
  }
});

test("every contents anchor resolves to a heading in the same document", () => {
  for (const c of D.cases) {
    for (const h of c.doc.headings)
      assert.ok(c.doc.html.includes(`id="${h.anchor}"`),
        `${c.slug}: contents entry ${h.anchor} has no heading`);
  }
});

test("a model is either openable with a URL, or says it is not", () => {
  for (const c of D.cases)
    for (const m of c.models) {
      assert.ok(["live", "repo", "private"].includes(m.access),
        `${c.slug}/${m.name}: access ${m.access}`);
      if (m.access === "live") assert.ok(/^https:\/\//.test(m.live || ""),
        `${c.slug}/${m.name}: live with no URL`);
      else assert.equal(m.live, null, `${c.slug}/${m.name}: a link nobody can follow`);
    }
});

test("the pages state nothing about a case that the data does not carry", () => {
  // Any case name, id or count hard-coded into the HTML would be a stored
  // opinion. The pages may name the register and the tooling and nothing else.
  for (const c of D.cases) {
    assert.ok(!LANDING.includes(c.name), `landing page hard-codes ${c.name}`);
    assert.ok(!LANDING.includes(c.id), `landing page hard-codes ${c.id}`);
    assert.ok(!VIEWER.includes(c.name), `viewer hard-codes ${c.name}`);
  }
});

test("both pages load the artifact as a <script>, never a fetch", () => {
  // Nordstern's rule for web/: every page also opens over file://, so that a
  // case file can be sent to somebody as a folder and still work.
  for (const [name, html] of [["fallakte.html", LANDING], ["case.html", VIEWER]]) {
    assert.ok(html.includes('<script src="fallakte-data.js"></script>'),
      `${name} does not load the artifact as a script tag`);
    assert.ok(!/\bfetch\s*\(/.test(html), `${name} uses fetch(), which breaks file://`);
  }
});

test("the viewer handles a case that does not exist instead of showing nothing", () => {
  assert.ok(VIEWER.includes("No case file for"),
    "an unknown ?case= should say so and fall back");
});

test("the landing page links the viewer, and the viewer links back", () => {
  assert.ok(LANDING.includes('href="case.html?case='), "landing links into a case");
  assert.ok(VIEWER.includes('href="fallakte.html"'), "viewer links back to the list");
  for (const page of [LANDING, VIEWER])
    assert.ok(page.includes('href="fallakte.css"'), "both share one stylesheet");
});
