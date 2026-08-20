# CONTINUITY NOTE — §7 Conclusion

**Version:** 7.1.0 · **CHAPTER 7 COMPLETE — and with it the chapter body of the dissertation.**
Chapters 0–7 are drafted, reviewed and approved. Hands off to the appendices and to Phase 3.

---

**Key concepts established:**
- **The question restated as a question about specification, not about accuracy** — if the transform before
  the first convolution determines the feature space, a model reported without it *"has not been fully
  described, and a comparison between two such models is a comparison between partly unknown systems."*
  The kind of result is named plainly: **methodological**, bounded to the corpora, architectures and
  hardware used.
- **All seven hypothesis outcomes restated with their fences intact**, in the wordings fixed in Chapter 4
  and §5.C rather than in paraphrase — decomposes-without-dissolving; a grouping not an ordering; direction
  with magnitude denied; thresholds cleared by both arms; alignment not localisation with the qualitative
  half unevaluated; dispersion as the substantive content with two groupings not independent; absolute
  performance not resistance, thin second margin. Small data: **comparable, not larger**.
- **The principal finding stated as consistency, not effect size** — present in-domain, decomposable,
  traceable to a measured distance reduction, observable on every corpus and camera grouping in both
  regimes — with the argument for why that matters (*"more plausibly a property of the feature space the
  model is given than an artefact of any one evaluation"*) and, in the same movement, what it does not license.
- **Four kinds of contribution** — conceptual, engineering, metrological, methodological — none newly
  asserted, all traceable to `CONTRIBUTIONS.md` v7.1.0 and to §0.8. The methodological one is kept
  **strictly descriptive**: it rehabilitates no result.
- **VCR-3 discharged in its own paragraph:** the from-scratch label-free initialisation that failed the
  acceptance gate is reported, with the reason — *"a conclusion that reported only the branch that succeeded
  would misrepresent the record."*
- **Limitations named by shape in five kinds**, with §5.4 identified as the enumeration and the explicit
  undertaking that none is softened **and none is added**.
- **Eight open questions sorted by what closing them would cost** — four without training a new model, three
  needing new experiments or data, and **one that measurement cannot close** (whether the differenced and
  ratio-based transfer measures should serve as criteria of external quality at all).
- **The closing position stated narrowly enough to be checked**, ending on the reason narrowness is the
  point: *"a claim narrow enough to be checked is the only kind worth defending."*
- **No metric value anywhere.** The thin external margin is stated in words rather than digits, following
  §5.C's precedent. The only numerals are counts.

**Terms introduced:** none.

**Argument thread:** Closed. Chapters 0–7 are complete and mutually consistent: §0.8 submits, Chapters 4–5
establish and price, §7 restates without exceeding. The ceiling audit in `reviews/7-review.md` records the
provision-by-provision check, including one **deliberate omission** — §0.8's provisions 11 (the
thermal-optical model and the screening architecture) are not restated among the conclusion's contributions,
because doing so would have implied an empirical standing they do not have.

**Final topic:** The position the dissertation ends on, and the boundaries within which it stands.

---

## WHAT REMAINS IN THE DISSERTATION

**Appendices B, C, E, F** — the only unwritten text. Each is bounded by what was recorded, and the bounds
are known in advance:
- **App B** (confusion matrices and training curves) — per-epoch trajectories and per-class curves were not
  retained, so its scope is bounded accordingly; ROC/PR curves need per-sample prediction dumps.
- **App C** (system-architecture diagrams) — an asset task, not experiment-gated: the UML must be drawn.
- **App E** (attention-map gallery) — annotated public corpus only; the clinical overlays were never
  produced, and §4.6.3 and §7 both record that as an absence.
- **App F** (device-domain supplementary tables) — per-grouping confusion matrices were not recorded.
- **§0.16 depends on this.** Its appendix paragraph assumes six appendices; if any of B, C, E or F does not
  survive to the final document, that paragraph changes with it.

**Translations.** KZ translations exist for Chapters 1, 2, 3, 6 and the appendices. **Missing: Chapter 4
(3 of 20), Chapter 5 (0 of 7), Chapter 0 (0 of 13), Chapter 7 (0 of 1)** — 38 sections.

**Sync passes now due, both of them derivable from finished text.**
- **Abstract** (`thesis/output/abstract_en.md`), four items: "seven experiments" → **eight** investigations;
  H-3 absent → now a hypothesis, a novelty item and a provision; the statements-for-defence list has six
  items, one still in the retired Δ_drop form → §0.8 submits **eleven provisions plus one observation**; and
  **the Vessel Visibility Index is listed as a method although §4.3.3 excluded it** for want of an
  implementation and a source — that one is an error, not merely stale. The abstract can now be rewritten
  directly against §0.2, §0.6, §0.8 and §7.
- **Governance:** `CORE_OBJECTIVE.md` v5.0 and `MASTER_OUTLINE.md` v6.0.0 (H-7 form, H-3, duplicated
  objective numbering, object-of-research category error); `results/tables/TAB-5.2` (PC-11's register
  position, which `ARGUMENT_MAP.md` v7.1.0 has already fixed).

**Phase 3, with two known defects to clear first.**
1. **`assembly/_assemble_en.py` extracts only text under a `## PART 1` marker.** Chapter 1 has it 11/11;
   **Chapter 4 has it 3/20 and Chapter 5 0/7** — 24 sections would assemble empty. Chapters 0 and 7 use the
   marker. Fix by adding the markers or by relaxing the extractor.
2. **Chapter 0 must be assembled from an explicit ordered list**, since the assembler sorts numerically and
   that is not the manuscript order for that chapter alone.
3. Then: resolve every `[FIG/TAB]` placeholder and the four count placeholders in §0.16; draw the deferred
   diagrams (FIG-2.1, FIG-2.3, FIG-2.4, FIG-2.5, FIG-4.17, FIG-5.1, FIG-5.2, DIA-6.3); run the citation
   conversion from author-year to numbered form; work the trim queue; convert to a single `.docx`.

**Trim queue, whole document.** Chapter 0 carries seven over-band sections plus §0.16 (which drops below
band once its placeholders resolve); several Chapter-1 and Chapter-2 sections sit at or slightly over their
bands from the earlier coverage-matrix reconciliation. **Chapter 7 is in band and carries no flag.**
