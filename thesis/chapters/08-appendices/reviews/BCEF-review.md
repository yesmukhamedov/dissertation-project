# VERIFICATION PROTOCOL — Appendices B, C, E, F

**Protocol version:** 7.1.0 · **Inputs:** the four drafts and briefs + INVARIANTS.md v7.0.0 + the consolidated result tables of `results/` + §4.6, §4.8, §5.1, §5.4, Chapter 6 · **Reviewer pass:** Opus self-verification.

> **Block verification, recorded deliberately.** Appendices A and D each carry their own file. These four
> were written as one unit against one binding set, and the risks that matter — transcription fidelity,
> Rule 16, and the honesty of the stated absences — run across all four rather than within any one. A
> per-appendix table is given for traceability. Precedent: §6.3.1 and the Chapter-0 apparatus block.

---

## THE TRANSCRIPTION CHECK — the risk specific to B and F

Appendices B and F are almost entirely transcribed figures. A single mistyped digit would put a false number
into the dissertation, and no reader could catch it without the source tables to hand. The check was
therefore **mechanical, not visual**.

Every decimal value with three or four places was extracted from the PART-1 body of each draft and matched
against the consolidated result tables:

| Draft | Distinct 3–4 dp values | Not found in the source tables |
|---|---:|---|
| Appendix B | 168 | **none** |
| Appendix F | 159 | **none** |

Every integer in the confusion-matrix rows of Appendix B was checked the same way: **184 integers, none
absent from the sources.** Group and class sizes in Appendix F were checked individually; two values
(`1,744` and `723`) were initially flagged and both proved to be artefacts of the checking script's
thousands-separator handling rather than of the drafts — both appear in the source tables verbatim.

**No figure in either appendix is recomputed, re-averaged or re-rounded.** The only arithmetic remarks are
restatements of ratios already established in §4.2.3, §4.8 and §B.5.

**Transcription verdict:** PASS.

---

## A. CLAIM COMPLIANCE

- [x] **B** advances no claim; it decomposes figures established in Chapters 4–5. Each interpretive remark
      names the section that established the reading (§4.2.2, §4.2.3, §5.2.1, §4.8, §5.4).
- [x] **C** advances PC-5 at its assigned DESIGN/THEORETICAL level and nothing else. Every module,
      interface, node and entity is traceable to Chapter 6 through Table C.1.
- [x] **E** restates PC-7 at exactly the level §5.2.2 assigned — quantitative half only, within the
      alignment/localisation boundary, one corpus, one fold — and adds nothing.
- [x] **F** advances PC-9 with all three of its travelling qualifications stated **before** the tables.
- [x] No claim outside the briefs' bindings is introduced in any of the four.

**A verdict:** PASS.

## B. FORBIDDEN CONTENT SCAN

- [x] **CFC-2.1** — B and F bound their content to the corpora and camera models represented; C denies
      extension in its closing status paragraph; E is confined to one annotated corpus.
- [x] **CFC-2.2 / NC-2** — no published system is named or compared against in any of the four.
- [x] **CFC-2.3 / NC-3** — no deployment outcome; C's closing paragraph denies clinical utility and
      regulatory status explicitly.
- [x] **CFC-2.4** — no clinical-grade claim anywhere; C and F each deny it in their own terms.
- [x] **CFC-2.5** — no perfect-performance figure; E restates no ALO or IoU value at all.
- [x] **CFC-2.8** — every comparative remark in B and F is between *configurations* (A vs B, C vs D). C is
      not applicable (no experimental result cited); E is not applicable.
- [x] **CFC-2.9 / SB-1.12** — no P1 source named in any of the four.
- [x] **NC-14** — the governing constraint of E, stated **before the first plate is described**; also
      attached in C at the overlay's only substantive mention and in the data model's `OVERLAY` entity.
- [x] **NC-16** — stated twice in F, at the opening and the close.
- [x] **NC-17** — no configuration, stage or grouping described as optimal in any of the four.
- [x] **NC-9** — C: security provisions are aligned by design, *"not a certified compliance status"*.

**B verdict:** PASS.

## C. TERMINOLOGICAL CONSISTENCY

- [x] Configuration labels A/B/C/D used with the same referents as Chapter 4, and expanded on first use in
      both B and F.
- [x] "Alignment" not "localisation" throughout E; "dispersion" as the substantive content in F.
- [x] Grade labels DR0–DR4 and the referable threshold (grade ≥ 2) match Chapter 3.
- [x] C uses the FR/NFR identifiers of Tables 6.1–6.2 without redefining them.
- [x] No unresolved `[TERM NOT IN GLOSSARY]` flags in any of the four.

**C verdict:** PASS.

## D. SOURCE HANDLING (SIR-1…9)

- [x] **SIR-1** — no reading is strengthened in transcription. B defers to §5.2.1's judgement that marginal
      interval separation is the weaker evidence; F's twenty-five-cell observation restates §4.8.
- [x] **SIR-2** — E inherits and restates the single-corpus and single-fold limitations rather than
      dropping them.
- [x] **SIR-3** — every metric in B and F carries its corpus, arm and class context.
- [x] **SIR-6** — not engaged; the thermal-optical model is not invoked in any of the four.
- [x] Remaining SIR codes N/A: no literature card is cited in these appendices.

**D verdict:** PASS.

## E. STRUCTURAL INTEGRITY

- [x] Each appendix opens with what it is and what governs reading it, and closes with what it does not
      contain — the same shape in all four.
- [x] **Three of the four state an absence in their own numbered subsection** (B.8, E.5, F.9), each with a
      distinct reason and a stated consequence. C has no absence to state: its asset was authorable.
- [x] Block continuity note produced (`continuity/BCEF-continuity.md`).

| Appendix | Prose (excl. tables/diagrams) | Tables / diagrams / plates |
|---|---:|---|
| B | ≈ 1,030 words | 13 tables |
| C | ≈ 900 words | 4 diagrams + 1 traceability table |
| E | ≈ 830 words | 54 plates |
| F | ≈ 940 words | 8 tables |

**E verdict:** PASS.

## F. SCOPE AND PARADIGM

- [x] **SB-1.8 / SB-2.3** — F: device results are empirical observations; equipment and taxonomy
      heterogeneity registered in the governing conditions and in the closing bound.
- [x] **SB-1.10** — B: attached directly beneath the calibration table.
- [x] **SB-1.11** — E: Grad-CAM is not clinical validation of the model's reasoning.
- [x] **SB-2.1** — B and F both give class sizes before any per-class table, with the small-class warning.
- [x] **SB-3.1** — no architectural optimality claimed anywhere.
- [x] **SB-4.1 / SB-4.2 / SB-4.3** — C: design-only stated at the opening **and** the close; security
      aligned not certified; no field testing.
- [x] **SB-1.3** — C: the clinician's disposition is the terminal step of the sequence view.

**F verdict:** PASS.

## G. EVIDENCE THRESHOLDS

- [x] **EH-1** — weighted F1 leads in both B and F; per-class figures presented as decomposition.
- [x] **EH-2** — stated explicitly in B's opening and honoured in E and F: supplementary figures establish
      no hypothesis on their own.
- [x] **EH-3 / EH-4** — not exercised. Neither B nor F restates a dominance verdict; both report the
      decomposition behind figures adjudicated elsewhere. Checked for the word "dominance": **absent from
      all four.**

**G verdict:** PASS.

## H. RULE 16 — INTERNAL PROCESS HISTORY

This is the block's second live risk, because the source tables for B and F carry run dates, source-file
section pointers (`VALUES.md §…`) and an explicit account of which rows were re-synchronised between
revisions and which were not.

- [x] **No run date** in any of the four.
- [x] **No source-file pointer, no artifact path in prose.** Paths appear only inside E's figure markers,
      which the rule exempts and which resolve at conversion.
- [x] **No revision narrative.** In particular, the source table for F states that certain point estimates
      were recomputed while their intervals were carried over from an earlier run, and the calibration
      source records a sign change against a previous run. **Neither crossed into the appendices.**
- [x] **No checkpoint or epoch identifier**, with one deliberate retention: B's Table B.10 gives the best
      epoch per fold. That is a methodological fact required to judge the convergence claim of §4.2.2 — the
      test in rule 16 is whether a reader needs it to judge the result, and here they do.
- [x] C's `PREPROCESSING_RUN` entity is a persisted domain object of the *designed* system, not a reference
      to this dissertation's own runs. Checked, because the name invites the confusion.

**H verdict:** PASS.

---

## THE THREE STATED ABSENCES — audited individually

An appendix that quietly omits what it could not produce is worse than one that has less in it. Each
absence was checked for a reason and a consequence, not merely an acknowledgement.

| Absence | Where | Reason given | Consequence stated |
|---|---|---|---|
| Per-epoch training and validation curves | B.8 | trajectories were not retained; only best-epoch values survive | the convergence claim rests on Table B.10 and nothing finer; the reserved figure is cited nowhere |
| Per-class ROC and precision–recall curves | B.8 | require per-sample predicted probabilities, which were not saved | threshold-independent evidence confined to aggregate and referable AUC |
| Per-camera-group confusion matrices | B.8, F.9 | not recorded; only per-class F1 by group exists | within-group error *composition* cannot be examined — open, and closable by an export rather than by retraining |
| Clinical (KZ) attention overlays | E.5 | never produced | H-5 supported in its quantitative half only; gallery confined to one corpus; **an absence, not a negative result** |

All four carry both. The E.5 formulation is the one that mattered most and it holds: *"nothing was examined
on the clinical corpus and found wanting; the examination was not performed, and no inference about what it
would have shown is available in either direction."*

---

## A CORRECTION MADE DURING THIS PASS

An initial file search for attention-overlay assets was constructed wrongly and returned nothing, which
would have made Appendix E a specification of a gallery rather than a gallery. A second search located the
**54 paired comparison plates** exactly where `ASSET_INVENTORY.md` records them. Appendix E is consequently
a real gallery reproducing the complete annotated subset, and the asset inventory's entry for it is
confirmed rather than contradicted.

---

## VERDICT

**APPROVED — all four appendices.**

- **B** decomposes Chapters 4–5 to the class and the confusion cell across 13 tables, with 352 transcribed
  values mechanically verified against the sources and three absences stated with their reasons.
- **C** discharges **DIA-6.3** with four traceable views and a module → FR → NFR table, bounded as design at
  both ends. This was the last outstanding asset task in Chapter 6.
- **E** reproduces the **entire** annotated subset — 54 plates, no selection, floor cases retained — under a
  reading rule stated before the first plate, and states the G-3 absence as an absence.
- **F** gives the per-group and per-class device evidence with its three qualifications stated before the
  tables, explains the retention-ratio artefact without letting it rescue anything, and marks where the
  recorded resolution stops.

**No flags carried.** With these four, **the dissertation's written text is complete**: Chapters 0–7 and
Appendices A–F.
