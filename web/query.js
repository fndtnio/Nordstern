/* =====================================================================
 * Nordstern query language — rung 1
 *
 * A Datadog-shaped filter language over the register. Pure: no DOM, no
 * data. UMD-wrapped — `window.NordsternQuery` in the page, `require()` in the
 * tests. The only place the query semantics live.
 *
 * WHY THIS EXISTS. The page had seven AND-ed dropdowns, and the six canned
 * questions — the most valuable thing on it — could none of them be built
 * out of those dropdowns. The filter state had grown four parallel escape
 * hatches (`facets`, `flags`, `or`, and a raw JS `pred`) to express them.
 * A question you cannot type is a question only the author can ask.
 *
 * THE GRAMMAR, ENTIRE
 *
 *     query  := term*                        space between terms means AND
 *     term   := ['-'] field ':' value        '-' negates the whole term
 *             | ['-'] word | ['-'] "phrase"  no field = free text over the record
 *     value  := atom
 *             | '(' atom (OR atom)* ')'      alternation WITHIN one field
 *             | ('>'|'>='|'<'|'<='|'=') num  numeric fields only
 *     num    := 0.45 | 100000 | 100k | 2.3M | 1B
 *
 *   capability:curable reach:<0.5
 *   -blocker.kind:knowledge  blocker.standing:(alleged OR disputed)
 *   deaths:>100k  witness:"overdiagnosis"
 *
 * TWO DECISIONS WORTH ARGUING WITH
 *
 * 1. THE FIELD DECIDES HOW IT MATCHES, not the quoting. An enum field is
 *    always exact; a text field is always substring. Quotes only carry
 *    spaces, so `quadrant:"known & treatable"` is exact and `name:hepat`
 *    is a substring — and nobody has to remember which rule they invoked.
 *    Enum domains are read off the DATA at compile time, so a new value in
 *    the YAML is queryable without touching this file.
 *
 * 2. A BAD VALUE IS A WITNESS, NEVER ZERO ROWS. `capability:cured` names
 *    the four valid values and points at `curable`. Silent zero-results is
 *    the failure that makes a query tool untrustworthy, and it is the same
 *    rule Sperrwerk holds to: never answer a question with a bare false.
 *
 * ARRAYS ARE `some`. `blocker.kind:cost` means SOME blocker is a cost
 * blocker; `-blocker.kind:cost` therefore means NO blocker is. `every` is
 * deliberately absent — "all blockers are knowledge" is a named concept in
 * the register, so check.py derives it as `only_knowledge_blockers:true`
 * rather than the grammar growing a quantifier for it.
 *
 * NOT HERE YET, on purpose: cross-term OR and parentheses. Value-level
 * alternation covers most of it without any precedence to get wrong, and
 * `a OR b` across fields is refused with an explanation rather than a
 * parse error. Build it when a question you actually want forces it.
 * ===================================================================== */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.NordsternQuery = factory();
})(typeof self !== "undefined" ? self : this, function () {
"use strict";

/* ---------------------------------------------------------------------
 * The field registry.
 *
 * `get` may return a scalar or an array; an array matches with `some`.
 * Enum domains are NOT listed here — they are read off the records, so
 * that adding a blocker kind to a YAML file needs no code change.
 * ------------------------------------------------------------------- */
const FIELDS = {
  // identity
  slug:  { type:"text", get: r => r.slug,  help:"the record's stable id" },
  name:  { type:"text", get: r => r.name + " " + (r.also||[]).join(" "), help:"name and synonyms" },
  kind:  { type:"enum", get: r => r.kind,  help:"disease · syndrome · injury · …" },
  mondo: { type:"text", get: r => r.mondo, help:"the borrowed ontology id (unresolved everywhere, so far)" },

  // the axes, as declared
  mechanism:    { type:"enum", get: r => r.axes.mechanism,    help:"do we understand it" },
  intervention: { type:"enum", get: r => r.axes.intervention, help:"the ladder rung, as declared" },
  prevention:   { type:"enum", get: r => r.axes.prevention,   help:"independent of treatment" },
  ongoing:      { type:"enum", get: r => r.axes.ongoing,      help:"the burden of being treated" },
  efficacy:     { type:"num",  get: r => r.axes.efficacy.value, help:"works, at best (0–1)" },
  access:       { type:"num",  get: r => r.axes.access.value,   help:"reaches people (0–1)" },

  // measurement
  diagnostic: { type:"enum", get: r => r.measurement.diagnostic, help:"is it there" },
  prognostic: { type:"enum", get: r => r.measurement.prognostic, help:"what will it do untreated" },
  predictive: { type:"enum", get: r => r.measurement.predictive, help:"will THIS treatment work here" },

  // toll / window
  "toll.severity":  { type:"enum", get: r => r.toll.severity, help:"what the cure takes" },
  "residue.severity": { type:"enum", get: r => (r.residue || {}).severity,
                        help:"what the DISEASE leaves in someone it was cured in" },
  "residue.incidence": { type:"num", get: r => r.residue && r.residue.incidence && r.residue.incidence.value },
  "toll.permanent": { type:"bool", get: r => !!r.toll.permanent },
  "toll.incidence": { type:"num",  get: r => r.toll.incidence && r.toll.incidence.value,
                      help:"fraction of treated who pay it" },
  "window.closes_on": { type:"text", get: r => (r.window && r.window.closes_on) || "" },

  // burden
  deaths:     { type:"num", get: r => r.burden.deaths     && r.burden.deaths.value,     help:"deaths/year" },
  /* YEARS LIVED WITH DISABILITY. The burden metric for everything that does not
     kill people — `low-back-pain` is the largest cause on earth and has no
     `deaths` figure at all. Carried by few records so far; GBD publishes these,
     which puts them in the `sourceable` tier where a citation settles it. */
  ylds:       { type:"num", get: r => r.burden.ylds       && r.burden.ylds.value,       help:"years lived with disability/year" },
  incidence:  { type:"num", get: r => r.burden.incidence  && r.burden.incidence.value,  help:"new cases/year" },
  prevalence: { type:"num", get: r => r.burden.prevalence && r.burden.prevalence.value, help:"people alive with it" },

  // blockers — arrays, so `some`
  "blocker.kind":      { type:"enum", get: r => r.blockers.map(b => b.kind), help:"what is stuck" },
  "blocker.standing":  { type:"enum", get: r => r.blockers.map(b => b.standing),
                          help:"documented · alleged · disputed · refuted" },
  "blocker.who_could": { type:"enum", get: r => r.derived.actors, help:"who could move it" },
  "blocker.scale":     { type:"num",  get: r => r.blockers.map(b => b.scale).filter(v => v != null),
                          help:"rough cost to clear a blocker" },
  "blocker.what":      { type:"text", get: r => r.blockers.map(b => b.what + " " + b.blocks).join(" ") },
  "residue.what":      { type:"text", get: r => (r.residue || {}).what || "" },

  // strata
  "strata.intervention": { type:"enum", get: r => (r.strata||[]).map(s => s.intervention) },
  "strata.toll":         { type:"enum", get: r => (r.strata||[]).map(s => s.toll) },

  // derived — every one of these is a calculation you can argue with, not a
  // stored opinion. check.py owns them; this file only reads them.
  capability: { type:"enum", get: r => r.derived.capability, derived:true, help:"what medicine can do at its best" },
  terms:      { type:"enum", get: r => r.derived.terms,      derived:true, help:"clean · costly · harsh" },
  quadrant:   { type:"enum", get: r => r.derived.quadrant,   derived:true, help:"mechanism known? × what treatment achieves (six cells)" },
  /* The register is append-only: a deprecated record is never deleted and its
     `id` is never reused, so an outside citation keeps resolving. It stays in
     the data and out of the way — hidden from search unless asked for by name.
     `status:deprecated` shows only those; `status:any` shows everything. */
  status:     { type:"enum", get: r => r.derived.status,     derived:true, help:"active | deprecated (deprecated is hidden unless asked for)" },
  id:         { type:"text", get: r => r.id,                              help:"permanent record id, e.g. FND-D-0007" },
  delivery:   { type:"enum", get: r => r.derived.delivery,   derived:true, help:"reach, in words" },
  reach:      { type:"num",  get: r => r.derived.reach,      derived:true, help:"efficacy × access" },

  /* "You get it, and then what?" weighted by how many people get it.
     `know-gap` is deaths/year that remain WITH PERFECT DELIVERY — the burden
     money cannot claim. `deliv-gap` is deaths/year that what already exists
     would claim if it reached everyone. Both are null where they cannot be
     computed (no `deaths`, or `capability:preventable`, whose efficacy/access
     describe the treatment and not the prevention that is doing the work) —
     null never matches a numeric comparison, so those records drop out of a
     ranking rather than ranking last.
     A PROXY OVER UNSOURCED JUDGEMENT: `efficacy` is the fraction whose course
     is altered, not a mortality reduction, and 0 of the 915 `judged` scalars
     are sourced. Read as a shape; do not quote as a figure. */
  /* THE BUCKETS — see buckets.yaml. `bucket` is a PARTITION: every record has
     exactly one, so counts sum to the register and a percentage means something.
     `tag` is NOT: a record carries several or none, so `tag:` asks whether SOME
     tag matches and totalling them counts some diseases more than once. */
  bucket:      { type:"enum", get: r => r.derived.bucket, derived:true,
                 help:"what it does to your life — one per record" },
  tag:         { type:"enum", get: r => r.derived.bucket_tags, derived:true,
                 help:"why it is not better than that — several per record, never summed" },

  /* The YLD twins of `know-gap`/`deliv-gap`. SAME ARITHMETIC, DIFFERENT UNIT —
     these are years of disability, those are deaths, and the two must never be
     added or ranked against each other. A record may carry both, one or
     neither. */
  "know-yld":  { type:"num",  get: r => r.derived.knowledge_yld, derived:true,
                 help:"YLD/year remaining if delivery were perfect" },
  "deliv-yld": { type:"num",  get: r => r.derived.delivery_yld,  derived:true,
                 help:"YLD/year claimable by what already exists" },

  "know-gap":  { type:"num",  get: r => r.derived.knowledge_gap, derived:true,
                 help:"deaths/year remaining if delivery were perfect" },
  "deliv-gap": { type:"num",  get: r => r.derived.delivery_gap,  derived:true,
                 help:"deaths/year claimable by what already exists" },
  cost:       { type:"num",  get: r => r.derived.cheapest_priced_blocker, derived:true,
                help:"cheapest priced blocker — the entry price" },
  residue:    { type:"enum", get: r => r.derived.residue_terms, derived:true,
                help:"what the disease leaves behind: clean · costly · harsh" },
  restored:   { type:"enum", get: r => r.derived.restored, derived:true,
                help:"back to the state before it all? restored · cure-costs · disease-residue · both · n/a" },

  /* "You get it, and then what?" — the two must be asked together.
     `survival` says HOW MANY reach the horizon; `outcome` says WHAT REACHING IT
     MEANS. On the band alone `head-neck-cancer` and `heart-failure` are both
     0.55 `good chance`, and one of them is cured (gaps.md #216). */
  survival:  { type:"enum", get: r => r.derived.survival_band, derived:true,
               help:"terminal · a chance · good chance · n/a — fraction alive at the record's own horizon" },
  outcome:   { type:"enum", get: r => r.derived.survival_outcome, derived:true,
               help:"cured · recovered · held · delayed — what surviving means; read WITH survival, never instead of it" },
  course:    { type:"enum", get: r => r.survival && r.survival.course,
               help:"acute · chronic — declared, and only for records below `suppressive`" },
  gain:      { type:"num",  get: r => r.derived.survival_gain, derived:true,
               help:"treated − untreated survival: what medicine actually bought" },
  survived:  { type:"num",  get: r => r.survival && r.survival.treated && r.survival.treated.value,
               help:"fraction alive at the horizon, treated" },
  /* The UNTREATED half, and it is not decoration. `gain:0` alone conflates
     "medicine buys no life against something that kills you" (alzheimers,
     rabies) with "there was no death to prevent" (genital-herpes) — and the
     second is not a finding about medicine at all. `gain:0 untreated:<0.95` is
     the question the dashboard actually asks, and the snapshot's `zero_gain`
     carries the same guard. Added with `genital-herpes`; gaps.md #234. */
  untreated: { type:"num",  get: r => r.survival && r.survival.untreated && r.survival.untreated.value,
               help:"fraction alive at the horizon, UNTREATED — what the disease does on its own" },
  was_fatal: { type:"bool", get: r => r.derived.was_uniformly_fatal, derived:true,
               help:"untreated, essentially nobody survived" },
  no_longer_terminal: { type:"bool", get: r => r.derived.no_longer_terminal, derived:true,
               help:"was uniformly fatal, is not terminal now — read with `outcome`, see gaps.md #216" },

  // flags (all derived booleans)
  orphaned:              { type:"bool", get: r => r.derived.orphaned, derived:true, help:"⚑ no champion" },
  has_window:            { type:"bool", get: r => r.derived.has_window, derived:true, help:"⧗ timing changes what is possible" },
  spans_ladder:          { type:"bool", get: r => r.derived.spans_ladder, derived:true, help:"⧉ the strata disagree" },
  cured_at_a_price:      { type:"bool", get: r => r.derived.cured_at_a_price, derived:true },
  harm_without_benefit:  { type:"bool", get: r => r.derived.harm_without_benefit, derived:true },
  overtreatment_risk:    { type:"bool", get: r => r.derived.overtreatment_risk, derived:true },
  futile_treatment_risk: { type:"bool", get: r => r.derived.futile_treatment_risk, derived:true },
  measurement_gap:       { type:"bool", get: r => r.derived.measurement_gap, derived:true,
                            help:"either measurement failure — can we aim what we have" },
  only_knowledge_blockers:{ type:"bool", get: r => r.derived.only_knowledge_blockers, derived:true,
                            help:"EVERY blocker is knowledge — money cannot move it" },
  has_residue: { type:"bool", get: r => !!r.residue, derived:true,
                 help:"the disease leaves something permanent behind" },
  contested: { type:"bool", get: r => !!r.contested },
  residual:  { type:"bool", get: r => !!r.residual },

  // prose
  witness: { type:"text", get: r => Object.values(r.witness || {}).join(" ") + " " +
                                    ((r.measurement && r.measurement.witness) || "") },
  holes:   { type:"text", get: r => (r.holes || []).join(" ") },

  // provenance. `src:recall` currently returns the whole register, and the
  // register would rather be asked that than quietly imply otherwise.
  src:       { type:"enum", get: r => collectSrc(r), help:"where the numbers came from" },
  unsourced: { type:"num",  get: r => r.derived.unsourced_scalars, derived:true },
};

// Old facet ids and the obvious near-misses, so muscle memory and the
// dropdowns both land somewhere real.
const ALIASES = {
  blocker: "blocker.kind", actor: "blocker.who_could", standing: "blocker.standing",
  toll: "toll.severity", severity: "toll.severity", scale: "blocker.scale",
  window: "has_window", strata: "spans_ladder", price: "cost",
  // `id` was an alias for `slug` until records gained a permanent identifier.
  // It now resolves to that identifier, which is the whole point of having one:
  // an outside citation must not depend on a human-readable handle that someone
  // may rename. `slug:` still does what `id:` used to.
};

function collectSrc(r, out) {
  out = out || new Set();
  if (r && typeof r === "object") {
    if (typeof r.src === "string") out.add(r.src);
    for (const v of Object.values(r)) if (v && typeof v === "object") collectSrc(v, out);
  }
  return [...out];
}

/* ---------------------------------------------------------------------
 * Tokenising: split on whitespace, but never inside "quotes" or (parens).
 * Every chunk keeps its offsets so a diagnostic can point at the column.
 * ------------------------------------------------------------------- */
function chunk(src) {
  const out = [];
  let i = 0;
  while (i < src.length) {
    while (i < src.length && /\s/.test(src[i])) i++;
    if (i >= src.length) break;
    const start = i;
    let quote = null, depth = 0;
    while (i < src.length) {
      const c = src[i];
      if (quote) { if (c === quote) quote = null; }
      else if (c === '"' || c === "'") quote = c;
      else if (c === "(") depth++;
      else if (c === ")") depth = Math.max(0, depth - 1);
      else if (/\s/.test(c) && depth === 0) break;
      i++;
    }
    out.push({ text: src.slice(start, i), start, end: i, unterminated: !!quote });
  }
  return out;
}

const unquote = s => (/^(["']).*\1$/.test(s) && s.length >= 2) ? s.slice(1, -1) : s;

/* number literals, with the k/M/B suffixes the burden figures need */
function parseNum(s) {
  const m = /^([+-]?(?:\d+\.?\d*|\.\d+))([kKmMbB]?)$/.exec(s.trim());
  if (!m) return null;
  const mult = { k:1e3, K:1e3, m:1e6, M:1e6, b:1e9, B:1e9 }[m[2]] || 1;
  return parseFloat(m[1]) * mult;
}

/* did-you-mean, by edit distance */
function editDistance(a, b) {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
  for (let j = 0; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++)
    for (let j = 1; j <= b.length; j++)
      d[i][j] = Math.min(d[i-1][j] + 1, d[i][j-1] + 1,
                         d[i-1][j-1] + (a[i-1] === b[j-1] ? 0 : 1));
  return d[a.length][b.length];
}
function nearest(word, candidates) {
  const w = String(word).toLowerCase();
  let best = null, bestScore = Infinity;
  for (const c of candidates) {
    const s = String(c).toLowerCase();
    // Credit a shared prefix: someone typing `cured` for `curable` is four
    // edits away, which plain distance calls too far — but the three letters
    // they got right are strong evidence they were reaching for it.
    let p = 0;
    while (p < w.length && p < s.length && w[p] === s[p]) p++;
    const score = editDistance(w, s) - p;
    if (score < bestScore) { bestScore = score; best = c; }
  }
  // beyond that, a "did you mean" is noise rather than help — better to just
  // print the valid list and let the reader pick
  return bestScore <= Math.max(2, Math.ceil(w.length / 2)) ? best : null;
}

/* ---------------------------------------------------------------------
 * parse(src, domains) -> { terms, errors }
 *
 * `domains` maps an enum field to its valid values (see compile()). Parsing
 * without it still works — enum values just go unvalidated, which is what
 * the tests for pure syntax want.
 * ------------------------------------------------------------------- */
function parse(src, domains) {
  const terms = [], errors = [];
  const fieldNames = Object.keys(FIELDS).concat(Object.keys(ALIASES));

  for (const tok of chunk(String(src || ""))) {
    let { text, start, end } = tok;
    if (tok.unterminated) {
      errors.push({ start, end, message: `unterminated quote in \`${text}\``,
                    hint: "close it, or drop the quote if the value has no spaces" });
      continue;
    }

    // A bare OR between terms is the deferred feature, and saying so beats
    // "unknown field: OR". Name the thing that DOES work instead.
    if (/^(OR|AND)$/i.test(text)) {
      errors.push({ start, end, message: `\`${text}\` between terms is not supported yet`,
        hint: text.toUpperCase() === "AND"
          ? "a space already means AND — just remove it"
          : "alternation works inside one field: blocker.kind:(cost OR logistics)" });
      continue;
    }

    let negate = false;
    if (text[0] === "-" && text.length > 1) { negate = true; text = text.slice(1); }

    // find the field separator, ignoring one inside quotes
    let sep = -1, q = null;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (q) { if (c === q) q = null; }
      else if (c === '"' || c === "'") q = c;
      else if (c === ":") { sep = i; break; }
    }

    if (sep === -1) {                       // free text over the whole record
      const v = unquote(text).toLowerCase();
      if (v) terms.push({ kind:"free", value:v, negate, raw:text, start, end });
      continue;
    }

    const rawField = text.slice(0, sep);
    const rawValue = text.slice(sep + 1);
    const field = ALIASES[rawField] || rawField;
    const spec = FIELDS[field];

    if (!spec) {
      const near = nearest(rawField, fieldNames);
      errors.push({ start, end, message: `no field \`${rawField}\``,
                    hint: near ? `did you mean \`${near}\`?` : "press ? for the field list" });
      continue;
    }
    if (rawValue === "") continue;          // mid-typing: not an error yet

    // ---- alternation: field:(a OR b) --------------------------------
    let atoms = null;
    if (rawValue[0] === "(") {
      if (rawValue[rawValue.length - 1] !== ")") {
        errors.push({ start, end, message: `unclosed \`(\` in \`${rawField}:${rawValue}\``,
                      hint: "alternation looks like blocker.kind:(cost OR logistics)" });
        continue;
      }
      const inner = rawValue.slice(1, -1).trim();
      atoms = inner.split(/\s+OR\s+/i).map(s => unquote(s.trim())).filter(Boolean);
      if (!atoms.length) continue;
      if (/\s+AND\s+/i.test(inner)) {
        errors.push({ start, end, message: "AND inside a value is not supported",
          hint: `a field holds one value at a time; write two terms: ${rawField}:x ${rawField}:y` });
        continue;
      }
    }

    // ---- numeric comparison -----------------------------------------
    const cmp = /^(>=|<=|>|<|=)\s*(.+)$/.exec(rawValue);
    if (cmp && !atoms) {
      if (spec.type !== "num") {
        errors.push({ start, end, message: `\`${field}\` is not numeric`,
                      hint: `it holds ${spec.type === "bool" ? "true/false" : spec.type + " values"} — try ${field}:${exampleFor(spec, field, domains)}` });
        continue;
      }
      const n = parseNum(cmp[2]);
      if (n === null) {
        errors.push({ start, end, message: `\`${cmp[2]}\` is not a number`,
                      hint: "numbers may carry k, M or B — deaths:>100k" });
        continue;
      }
      terms.push({ kind:"num", field, op:cmp[1], value:n, negate, raw:rawValue, start, end });
      continue;
    }

    /* A BARE NUMBER ON A NUMERIC FIELD MEANS EQUALS. It used to fall through to
     * the substring matcher, and the result was not a near-miss: `deaths:0`
     * returned 92 of 108 records, because "6600000" contains the character "0".
     * Every record with a death toll matched a query asking for the ones with
     * none — and `deaths: 0` is the subject of a documented finding here
     * (six distinct kinds of zero, gaps.md #182/#211), so the register was
     * shipping a public tool that answered its own headline question backwards.
     *
     * This is rule one — THE FIELD DECIDES HOW IT MATCHES — applied where it had
     * been skipped. `deaths:0` is numeric because `deaths` is numeric, exactly
     * as `capability:curable` is exact because `capability` is an enum. */
    if (spec.type === "num" && !atoms) {
      const n = parseNum(rawValue);
      if (n !== null) {
        terms.push({ kind:"num", field, op:"=", value:n, negate, raw:rawValue, start, end });
        continue;
      }
      errors.push({ start, end, message: `\`${field}\` is numeric — \`${rawValue}\` is not a number`,
                    hint: "numbers may carry k, M or B, and take > >= < <= — try "
                          + `${field}:>0 or ${field}:0` });
      continue;
    }

    const values = atoms || [unquote(rawValue)];

    // ---- booleans ----------------------------------------------------
    if (spec.type === "bool") {
      const bad = values.find(v => !/^(true|false|yes|no)$/i.test(v));
      if (bad !== undefined) {
        errors.push({ start, end, message: `\`${field}\` is a flag, and \`${bad}\` is not true or false`,
                      hint: `write ${field}:true, or -${field}:true for the ones without it` });
        continue;
      }
      terms.push({ kind:"bool", field, value:/^(true|yes)$/i.test(values[0]), negate,
                   raw:rawValue, start, end });
      continue;
    }

    // ---- enums: exact, and validated against the data ----------------
    if (spec.type === "enum") {
      const dom = domains && domains[field];
      if (dom && dom.length) {
        const bad = values.find(v => !dom.some(d => d.toLowerCase() === v.toLowerCase()));
        if (bad !== undefined) {
          const near = nearest(bad, dom);
          errors.push({ start, end,
            message: `\`${field}\` has no value \`${bad}\``,
            hint: (near ? `did you mean \`${near}\`? ` : "") +
                  `valid: ${dom.join(" · ")}` });
          continue;
        }
      }
      terms.push({ kind:"enum", field, values: values.map(v => v.toLowerCase()), negate,
                   raw:rawValue, start, end });
      continue;
    }

    // ---- text: substring ---------------------------------------------
    terms.push({ kind:"text", field, values: values.map(v => v.toLowerCase()), negate,
                 raw:rawValue, start, end });
  }
  return { terms, errors };
}

function exampleFor(spec, field, domains) {
  const dom = domains && domains[field];
  if (spec.type === "bool") return "true";
  if (dom && dom.length) return dom[0];
  return "value";
}

/* ---------------------------------------------------------------------
 * Evaluation
 * ------------------------------------------------------------------- */
const asList = v => v == null ? [] : (Array.isArray(v) ? v : [v]);

function matches(term, rec) {
  let hit;
  if (term.kind === "free") {
    hit = JSON.stringify(rec).toLowerCase().includes(term.value);
  } else {
    const got = asList(FIELDS[term.field].get(rec));
    if (term.kind === "num") {
      const ok = { ">":(a,b)=>a>b, ">=":(a,b)=>a>=b, "<":(a,b)=>a<b,
                   "<=":(a,b)=>a<=b, "=":(a,b)=>a===b }[term.op];
      hit = got.some(v => typeof v === "number" && ok(v, term.value));
    } else if (term.kind === "bool") {
      hit = got.some(v => !!v === term.value);
    } else if (term.kind === "enum") {
      hit = got.some(v => term.values.includes(String(v).toLowerCase()));
    } else {
      hit = got.some(v => String(v).toLowerCase().includes(term.values[0]) ||
                          term.values.some(t => String(v).toLowerCase().includes(t)));
    }
  }
  return term.negate ? !hit : hit;
}

/* domains(records) — read every enum field's real values off the data, so
 * the validator's "valid: …" list can never drift from what is loadable. */
function domains(records) {
  const out = {};
  for (const [name, spec] of Object.entries(FIELDS)) {
    if (spec.type !== "enum") continue;
    const vals = new Set();
    for (const r of records) for (const v of asList(spec.get(r))) if (v != null && v !== "") vals.add(String(v));
    // `status:any` is a legal query and no record has that status. It belongs in
    // the domain so the validator accepts it and the "valid: …" witness lists
    // it — a reader needs to be told the escape hatch exists.
    if (name === "status") vals.add("any");
    out[name] = [...vals].sort();
  }
  return out;
}

/* run(records, src) -> { records, terms, errors, ignored }
 *
 * Terms that failed to parse are REPORTED and SKIPPED, not fatal. Half a
 * query still answers half a question while you type — but the count of
 * what was dropped comes back with the result, because a filter that is
 * silently ignored is the one bug that would make this untrustworthy.
 */
function run(records, src, dom) {
  dom = dom || domains(records);
  const { terms, errors } = parse(src, dom);
  let out = terms.length ? records.filter(r => terms.every(t => matches(t, r))) : records.slice();

  /* DEPRECATED RECORDS ARE HIDDEN BY DEFAULT AND NEVER DELETED.
     A query that does not mention `status` gets the live register; one that does
     gets exactly what it asked for. `status:any` is the escape hatch and is
     handled here rather than as an enum value, because "any" is not a status a
     record can have — putting it in the domain would make it a suggestion in
     the did-you-mean list, which would be wrong. */
  const isAny = t => t.field === "status" && (t.values || []).includes("any");
  const anyTerm = terms.find(isAny);
  if (anyTerm) {
    /* `status:any` is a switch, not a filter — no record HAS that status. Drop
       it and apply whatever else was asked, across the whole register. */
    const rest = terms.filter(t => t !== anyTerm);
    out = rest.length ? records.filter(r => rest.every(t => matches(t, r))) : records.slice();
  } else if (!terms.some(t => t.field === "status")) {
    out = out.filter(r => r.derived.status !== "deprecated");
  }
  return { records: out, terms, errors, ignored: errors.length };
}

/* The field list, for the help panel and for autocomplete later. */
function describe(dom) {
  return Object.entries(FIELDS).map(([name, spec]) => ({
    name, type: spec.type, derived: !!spec.derived, help: spec.help || "",
    values: spec.type === "enum" && dom ? (dom[name] || []) : null,
  }));
}

return { FIELDS, ALIASES, parse, run, matches, domains, describe,
         chunk, parseNum, nearest, VERSION: "1.0" };
});
