# CONTINUITY NOTE — Appendices B, C, E, F, and THE WRITTEN TEXT COMPLETE

**Covers:** Appendix B, Appendix C, Appendix E, Appendix F
**Version:** 7.1.0 · **APPENDICES COMPLETE — A–F.** With Chapters 0–7 already approved, **the dissertation's written text is finished.** Hands off to Phase 3.

> One continuity note covers the four, as one review file does. They were written as a single unit against
> one binding set and have no individual argumentative threads to hand forward.

---

**Key concepts established:**

- **Appendix B** decomposes the aggregate figures of Chapters 4–5 to the class and the confusion cell:
  per-class F1/precision/recall for all four configurations, four in-domain confusion matrices, two on the
  external public corpus, calibration, per-fold convergence, both kinds of interval estimate side by side
  with the difference between what each quantifies made explicit, and in-domain referable-DR metrics.
  **§B.8 states three absences with a distinct reason and consequence for each.**
- **Appendix C discharges DIA-6.3** — the last outstanding asset task in Chapter 6 — with four views
  (component, deployment, sequence, data) given as diagram source, plus a **module → FR → NFR traceability
  table** so the diagrams can be checked against Tables 6.1–6.3 rather than admired. Two design features
  are deliberate: the Preprocessing Engine is a first-class module *on the inference path*, which is the
  architectural expression of the central position; and the rejected-input path is drawn, because a system
  that fails silently on unusable input is a different and more dangerous system.
- **Appendix E** reproduces the **complete** annotated subset — all 54 paired plates, no selection, floor
  cases retained — with NC-14 stated **before the first plate** and the plates declared illustration
  carrying no measurement. Exhaustiveness is argued rather than assumed: *"A gallery that selects its
  plates can flatter the result it accompanies, and no reader can detect the selection from inside it."*
- **Appendix F** gives the per-group and per-class device evidence, with its **three qualifications stated
  before the first table** (two groupings coincide with the external clinical corpora; three aggregate
  several camera models; single fold, so dispersion is between groups not between folds), and explains the
  retention-ratio artefact as one instance of the §5.4 normalisation defect — **descriptive, rescuing
  nothing**.

**Terms introduced:** none.

**Verification of record:** every 3–4-decimal value in B (168) and F (159) and every confusion-matrix
integer in B (184) was matched mechanically against the consolidated result tables. **None absent.** No
figure is recomputed, re-averaged or re-rounded anywhere in either appendix.

**A correction recorded rather than buried:** an initial asset search was constructed wrongly and reported
no attention overlays on disk, which would have reduced Appendix E to a specification. The 54 plates exist
exactly where `ASSET_INVENTORY.md` records them. The inventory entry is confirmed, not contradicted.

---

## HAND-OFF TO PHASE 3

The writing is done. Everything that remains is assembly, asset resolution and conversion.

**1. Placeholder and asset resolution (§11.2).**
- Resolve every `[FIG-x.x]` / `[TAB-x.x]` marker to its real asset path.
- **Draw the still-undrawn diagrams:** FIG-2.1, FIG-2.3, FIG-2.4, FIG-2.5 (conceptual, Chapter 2),
  FIG-4.17 and FIG-5.2. **DIA-6.3 is no longer among them** — Appendix C discharges it.
- **Render Appendix C's Mermaid source** to images at conversion, or confirm the converter handles fenced
  Mermaid. This is the one new conversion requirement these appendices introduce.
- **Fill the four count placeholders in §0.16** (pages, tables, figures, references) from the assembled
  document, and revisit its appendix paragraph — it assumes six appendices, which is now correct.

**2. Assembly.** `_assemble_en.py` was repaired and now emits 94 sections cleanly; **it must be re-run so
the four new appendices enter the manuscript.** Chapter 0 assembles from its explicit ordered list.

**3. Citations and trim.** Author-year → GOST `[N]` in a single pass; then the trim queue (seven over-band
Chapter-0 sections plus several Chapter-1/2 sections carrying reconciliation overhang).

**4. Translations — now the largest remaining task.** KZ exists for Chapters 1, 2, 3, 6 and Appendices A/D.
**Missing: Chapter 0 (16), Chapter 4 (17 of 20), Chapter 5 (7), Chapter 7 (1), Appendices B, C, E, F (4)
— 45 units.** `_assemble_kz.py` is repaired and carries the Chapter-0 ordering, so the tooling is ready.

**Open items that these appendices did not close, and could not:**
- Per-epoch trajectories and per-class ROC/PR curves remain unavailable — the record does not contain them.
- Per-group confusion matrices remain unrecorded; closing that needs an export, not new training.
- The clinical attention overlays (G-3) remain unproduced; closing that needs generation and expert review,
  and again no retraining.
- **NEW-1 is untouched:** the run's raw artifacts are still not consolidated under `experiments/outputs/`
  in a form that makes every reported number traceable to a primary output file. Appendices B and F make
  the numbers auditable *against the consolidated result tables*, which is not the same thing. This should
  be closed before the defence.
