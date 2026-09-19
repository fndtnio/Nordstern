/* ============================================================================
 * The provenance banner, in one place, for both pages.
 *
 * WHY THIS IS A FILE AND NOT TWO PARAGRAPHS OF HTML.
 *
 * The map and the tool each carried their own hand-written version. They said
 * different things, and the tool's had gone quietly wrong: it told visitors that
 * `mondo:` was "unresolved on every record" long after 93 of 101 had been
 * resolved. Nobody edits a warning banner when they resolve an ontology id.
 *
 * **This register's whole method is that a derived number is computed once and
 * never copied.** A hand-written sentence about the data is a stored opinion
 * with the same failure mode as a stored verdict — it is right when written and
 * silently wrong afterwards. So the numbers come from the snapshot `check.py`
 * built, and the sentence exists once.
 *
 * The banner is deliberately unflattering and deliberately first on the page. A
 * public state-of-the-world assembled from unverified numbers must say so before
 * it says anything else, and this is the same discipline as Sperrwerk's ledger:
 * report what was computed, not only what was concluded.
 *
 * UMD-wrapped so the tests can require() it.
 * ========================================================================== */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.NordsternBanner = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const n = v => Number(v || 0).toLocaleString("en-US");

  /* `snap` is a snapshot from web/snapshots/nordstern/. `opts.tone` is "lead"
     on the map, where the banner is the headline, and "warn" on the tool, where
     it sits above a table somebody is about to read numbers out of. The facts
     are identical; only the opening sentence differs, because "0 of 1,582" is a
     finding on a landing page and an instruction on a query tool. */
  function render(snap, opts) {
    if (!snap || !snap.provenance) return "";
    const p = snap.provenance;
    const tone = (opts && opts.tone) || "warn";
    const link = (opts && opts.queryHref) || "query.html?q=";

    // THE DENOMINATOR IS THE HONEST PART. `by_tier` arrived because this banner
    // used to say "0 of 1,582", which reads as a backlog of 1,582 lookups —
    // and more than half of them are quantities no dataset holds. A citation
    // SETTLES a burden figure, SUPPORTS a dated event, and cannot touch the
    // fraction of patients a treatment works for, because this register is
    // where that number is defined.
    const t = p.by_tier || null;
    const src = t ? t.sourceable : { total: p.scalars, cited: p.verified };

    // THE WARNING IS ONE SENTENCE AND THE EVIDENCE IS ONE CLICK AWAY.
    //
    // The first version said all of this at full length, above everything, on
    // both pages. It was accurate and nobody read it — a warning long enough to
    // skip is a warning that does not warn. What survives at the top is the
    // claim a visitor has to carry away: **experimental, and not sourced.**
    //
    // The detail is not deleted, because the numbers ARE the honesty and
    // deleting them would leave a vague disclaimer that cannot be checked. It
    // moves into a `<details>` that is closed by default, so the page is short
    // and the ledger is still on it. Same trade Sperrwerk makes with
    // `--derived`: the verdict is small, the working is available.
    const lead = tone === "lead"
      ? `<span class="big">An experimental dataset.</span>
         <b>Not everything here is verified or sourced.</b>`
      : `<b>Experimental dataset — not a data source.</b> Not everything here is
         verified or sourced.`;

    // Progress on the middle tier is reported rather than buried. The first
    // sourcing pass cited 43 `moved:` entries and the banner initially did not
    // mention them at all — which understates the register in the same way the
    // single denominator overstated its problem.
    const sup = t && t.supportable.cited
      ? `<b>${n(t.supportable.cited)} of ${n(t.supportable.total)} supporting
         references are in place</b> — the <code>moved:</code> entries, which are
         this register's only time series and the first thing a sourcing pass
         should reach.`
      : "";

    const tiers = t ? `
      <b>The other ${n(t.supportable.total + t.judged.total)} are not a backlog
      of lookups.</b> ${sup} ${n(t.supportable.total)} could carry a
      <i>supporting</i> reference — a dated event, an incidence from one cohort —
      without a citation determining the number. And ${n(t.judged.total)} are
      <b>judgements this register makes</b>: nothing published anywhere holds
      the fraction of patients in whom the best available treatment works, and
      that is the axis the register exists to supply. Blockers are counted here
      and carry their evidential status in <code>standing</code> instead.` : "";

    const mondo = p.mondo_unresolved === 0
      ? `Every record now carries a resolved <code>mondo:</code> identifier.`
      : `<code>mondo:</code> is resolved on ${n(p.mondo_resolved)} records and
         unresolved on ${n(p.mondo_unresolved)}.`;

    return `${lead}
      <b>Do not cite a figure from this page.</b>
      <details class="provmore"><summary>${n(src.cited)} of ${n(src.total)}
        numbers a public dataset could settle carry a citation — what that
        means</summary>
        <div>
        Every empirical scalar carries a <code>src</code>:
        ${n(p.by_src.recall)} are <code>recall</code> — a model's memory —
        ${n(p.by_src.reasoning)} are <code>reasoning</code>, its arithmetic, and
        ${n(p.unknown)} are <code>unknown</code>, meaning nobody has the number.
        <b>None of the three is a citation.</b>
        ${mondo}
        ${tiers}
        <b>The <i>ratings</i> are the work product and are meant to be argued
        with</b>; the numbers are placeholders with their weakness recorded.
        A sourcing pass is this register's own next piece of work.
        <a href="${link}src%3Arecall">see every unsourced record →</a>
        </div></details>`;
  }

  return { render, VERSION: "1.0" };
});
