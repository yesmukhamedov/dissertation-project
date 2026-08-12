# MASTER WRITING PLAN — Dissertation, Section by Section

**Document type:** Execution plan (the live to-do board for drafting the entire dissertation)
**Candidate:** Yesmukhamedov N.S.
**Compiled:** 2026-06-09
**Revised:** 2026-08-12 — writing phases closed; the board now tracks completion work only
**Grounded in:**
- `thesis/ASSET_INVENTORY.md` (resource IDs, real-vs-demo provenance, §2 reconciliation table)
- `thesis/governance/` v6.0.0 (INVARIANTS, HYPOTHESIS, ARGUMENT_MAP, RESEARCH_ARCHITECTURE, CONTRIBUTIONS)
- `thesis/prompts/` v6.0.0 pipeline (`section-brief-template.md`, `writing-session-system-prompt.md`, `verification-protocol.md`, `continuity-note-template.md`)
- `thesis/outline/MASTER_OUTLINE.md` (§-level content spec) reconciled to the **v6.0.0 Section Map Key** in `thesis/literature/LITERATURE_INDEX.md` (authoritative numbering)
- `thesis/literature/LITERATURE_INDEX.md` Coverage Matrix (literature-card IDs per section)

> **Scope of this document:** This is the plan only. **No chapter draft is written here.** Drafting begins only after the candidate reviews and approves this plan.

---

## CURRENT STATE (verified on disk, 2026-08-12)

**The English text is finished.** 98 sections, every one APPROVED, assembled by
`_assemble_en.py` — **101,459 words of section body** (103,147 by `wc -w` over the whole file, which also
counts headings and the banner; quote the body figure), no suspect extractions.
Phases 1 and 2 are closed and nothing in §4–§9 below is outstanding; those tables are now a
record of what was written, not a queue.

| Chapter | drafts | reviews | KZ translations |
|---|---|---|---|
| 0 Introduction | 16 | 8 (7 + one apparatus block) | **0** |
| 1 Problem Domain | 11 | 11 | 11 |
| 2 Theoretical Foundations | 15 | 15 | 15 |
| 3 Methodology | 13 | 13 | 13 |
| 4 Experiments | 20 | 20 | **3 of 20** |
| 5 Validation | 7 | 7 | **0** |
| 6 System Architecture | 9 | 9 | 9 |
| 7 Conclusion | 1 | 1 | **0** |
| Appendices A–F | 6 | 3 (A, D, BCEF block) | **2 of 6** |
| **Total** | **98** | — | **53 of 98** |

**What remains is completion work in four tracks**, two of which are independent and may run in
parallel. The full task board is §11; the tracker entries are in §1 Phase 3 / Phase 4.

1. ~~**Kazakh translation.**~~ ✅ **COMPLETE 2026-08-12 — 98 of 98.** All 45 outstanding units landed
   in one day. KZ assembly emits **98 sections / 81,438 body words** against the English 98 / 101,575;
   every chapter is 100 % (Ch 0 16/16, Ch 1 11/11, Ch 2 15/15, Ch 3 13/13, Ch 4 20/20, Ch 5 7/7,
   Ch 6 9/9, Ch 7 1/1, App 6/6). No suspect extractions, every KZ asset path resolves, citation pass
   clean in both languages (107 sources, BLOCKING 0).
2. ~~**Citation conversion.**~~ ✅ **DONE 2026-08-12** — 107 sources, one shared EN/KZ register,
   BLOCKING 0. Only the trim queue remains of this track. See §11.3.
3. ~~**Asset defects.**~~ ✅ **ALL CLOSED 2026-08-12** — FIG-1.1, DIA-6.3, FIG-3.8, FIG-4.17, plus two
   placeholder paths that contained a literal ellipsis and resolved to nothing. Every referenced asset
   path in both manuscripts now resolves, and `ASSET TO BE CREATED` is zero. See §11.2.
4. **Re-export — NOW THE CRITICAL PATH.** Every `.docx`/`.pdf` in `defense/docs/` was built from the
   53-section June manuscript. **There is no council-ready file for the current text**, EN or KZ. Two
   conditions bind the conversion — Appendix C's four Mermaid fences must render, and §0.16's four
   count placeholders are fillable only after it produces a paginated document, so **§0.16 closes last
   in both languages**. Full statement in §11.4 and in the critical-path block at the end of §12.

> **`ASSET_INVENTORY.md` is itself partly stale** and must not be used alone to decide what is
> missing: it still marks App C, App E and App F as `❌ MISSING` when all three are written and
> approved. Where it disagrees with this section, verify on disk.

---

## 0. How to read this plan

1. **Progress Tracker (§1)** is the master checklist — every section with a live status box. Update it as you go.
2. **Phasing (§2)** orders the work by *data-readiness*: what is writable now vs. what is gated on experiment execution, with the exact unblocking resource IDs.
3. **Resource Honesty Policy (§3)** is the binding rule that decides whether a section may be drafted at all.
4. **Section Task Tables (§4–§9)** give, for every `§x.x.x`: target word count, governance bindings, literature-card IDs, the figure/table Resource IDs it must reference, and the ✅/⛔ verdict.
5. **Per-Section Execution Loop (§10)** is the exact a–f procedure to run for each *writable* section.
6. **Final Assembly (§11, Phase 3)** is the LAST step — concatenate, resolve placeholders, convert to `.docx`. It depends on Phase 2 completion.

**Literature-card IDs** are given as `#NN`, matching the Source Index numbers in `LITERATURE_INDEX.md` (e.g. `#12` = `gulshan-2016.md`; `#19–#24` = self-publications in `literature/self/`). **Resource IDs** (`FIG-x.x`, `TAB-x.x`, `RES-*`, `DIA-*`, `APP-*`) match `ASSET_INVENTORY.md §2`.

**Status legend (per-section):**
- ⬜ not started · 🟦 brief done · 🟩 draft done · ✅ verified (APPROVED by verification-protocol)

**Writability flag (per-section):**
- ✅ **writable-now** — every result-dependent resource it needs is `✅ AVAILABLE` or literature-derived; safe to draft.
- ⛔ **blocked-by-[ID]** — requires a resource that is `❌ MISSING (real result)`; stays blocked until the experiment is run.
- ⚠️ **writable-now (deferred asset)** — prose is writable now; a *conceptual/UML diagram* it references is not yet drawn (not experiment-gated). The diagram is queued as an asset task and inserted as a `TO BE CREATED` placeholder — see §3.2.

---

## 1. PROGRESS TRACKER (live to-do board)

> Update the status box (⬜/🟦/🟩/✅) after each pipeline stage. "Flag" column repeats the writability verdict for at-a-glance triage.

### Phase 1 — writable now

**Chapter 1 — Problem Domain**
- [x] ✅ §1.1.1 Pathophysiology and Clinical Grading Systems — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.1.2 Screening Requirements in Resource-Limited Healthcare Settings — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.2.1 Sources of Image Degradation in Clinical Practice — ✅ verified (APPROVED 2026-06-09; lit-GAP candidate analysis; brief/draft/continuity/review saved)
- [x] ✅ §1.2.2 Impact of Image Quality on Diagnostic Model Performance — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.2.3 Device-Specific Variability in Fundus Imaging — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; flagged: #47/#49/#50/#51 lack card files)
- [x] ✅ §1.3.1 CNN Architectures for Medical Imaging — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.3.2 Transfer Learning and SSL in Ophthalmic Diagnostics — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.3.3 Explainability Methods in Medical Image Classification — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.4 Critical Analysis of Existing Automated DR Screening Systems — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; TAB-1.1 rendered inline)
- [x] ✅ §1.5 Formulation of the Research Problem — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved)
- [x] ✅ §1.C Conclusions to Chapter 1 — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved) — **Chapter 1 COMPLETE**

**Chapter 2 — Theoretical Foundations**
- [x] ✅ §2.1.1 Histogram Equalization and Adaptive Contrast Enhancement — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; FIG-2.1 deferred → asset queue; #23 card integrity flag noted)
- [x] ✅ §2.1.2 Formalization of CLAHE with Dual-Constraint Clip Limit — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; TAB-2.1 inline; Eqs. 2.1–2.3; resolves glossary clip-limit/tile-grid flags)
- [x] ✅ §2.1.3 Spatial Filtering and Noise Reduction Methods — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; bilateral/NLM as backdrop, non-adoption framed)
- [x] ✅ §2.2.1 Convolution, Pooling, and Feature Extraction Operations — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; FIG-2.2 referenced; CFC-2.8 pre-honored via #08 counter-position)
- [x] ✅ §2.2.2 Loss Functions and Optimization for Imbalanced Medical Datasets — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; SIR-5 #19/#21 one thread, SIR-7 honored; focal-loss source gap flagged → §3.3.4)
- [x] ✅ §2.2.3 Regularization Techniques — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; augmentation dual-role → Stage 6/OD-3; SIR-5/SIR-7 honored)
- [x] ✅ §2.3.1 Feature Transferability Across Visual Domains — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; DGL-6 two regimes; §2.3.3 SSL theory named-only/deferred; CFC-2.8 neutrality)
- [x] ✅ §2.3.2 Frozen-Layer vs Progressive Fine-Tuning Strategies — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; glossary fine-tuning disambiguation; SIR-5/SIR-7/CFC-2.8; hands off to §2.4.1)
- [x] ✅ §2.3.3 In-Domain Self-Supervised Pretraining for Retinal Imaging (NEW v6.0.0) — ✅ verified (APPROVED 2026-06-16; brief/draft/continuity/review saved; **deferral lifted** — SSL-on-fundus corpus #84–#92 now present, LITERATURE_INDEX §2.3.3 ✅ RESOLVED). In-domain SSL design space (#86–#91) + in-domain>ImageNet evidence (#85 non-retinal, #84 RETFound keystone); CNN-vs-ViT nuance explicit; DGL-6 + CFC-2.8 (composite IV) central; SIR-2/3/5 honored; CNN-native-on-4ch-V5 kept spec-not-result → §3.3.2/§4.2; ~951 w. Closes the last Ch-2 content gap.
- [x] ✅ §2.4.1 Coupled Thermal-Optical Model of Fundus Tissue Response — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; Eqs. 2–5,7,8; simulation-only bounding SB-1.5/SIR-6/CFC-2.4; THIN #20-self; FIG-2.4 deferred → asset queue)
- [x] ✅ §2.5.1 CAM / Grad-CAM Theory and Formalization — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; CAM/Grad-CAM/Grad-CAM++ eqs; NC-14 central; FIG-2.3 deferred; #46 Selvaraju card absent/index-only — flagged)
- [x] ✅ §2.5.2 Attention Map Interpretation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; NC-14 reinforced; interpretation bounded to attention-plausibility)
- [x] ✅ §2.5.3 ALO and IoU as Quantitative Explainability Metrics — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; ALO primary/IoU secondary eqs; IoU borrowed-not-benchmark; NC-14)
- [x] ✅ §2.6 Image Quality Metrics for Preprocessing Evaluation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; CNR/VVI/Entropy/SSIM; THIN/SIR-1 flagged; EH-2; FIG-2.5 deferred → asset queue; TAB-3.3 referenced)
- [x] ✅ §2.C Conclusions to Chapter 2 — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; experimentally-grounded vs simulation-only partition; §2.3.3 deferral noted) — **Chapter 2 COMPLETE except deferred §2.3.3**

**Chapter 3 — Methodology (fully unblocked)**
- [x] ✅ §3.1.1 Pipeline Stage Specification: 8-Stage System — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; Stage-1 RES-VAL honesty disclosure + Stage-7 RES-NORM grounded; P2/P1 framing; ~2,030 w)
- [x] ✅ §3.1.2 Upgraded CLAHE with Dual-Constraint Clip Limit — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; realizes §2.1.2 rule; FIG-3.7 polar variant tied to §3.1.1 fovea finding; [VERIFY] Stage-5 governance divergence; ~1,010 w)
- [x] ✅ §3.1.3 Augmentation Strategy for Class Imbalance Mitigation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; real RES-PCA basis interpreted; dual role SC-1.4 one of two levers; ~915 w)
- [x] ✅ §3.1.4 External Image Ingestion Protocol — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; lit-GAP candidate contribution; NC-15 bound, 1 intentional [UNSOURCED CLAIM]; ~790 w) — **§3.1 COMPLETE**
- [x] ✅ §3.2.1 ResNet-50 and EfficientNet-B3 as Primary Architectures — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; two-family EH-4 rationale; CNN-centred/AOQ-2; SB-3.1/NC-6/SIR-7; ~1,015 w)
- [x] ✅ §3.2.2 Historical v1.0 Architectures (Reference Only) — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; OD-2 references; SIR-4/5/7; reference-only; ~600 w) — **§3.2 COMPLETE**
- [x] ✅ §3.3.1 Architecture Adaptation for Five-Class DR Classification — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; 5-way softmax head; identical adaptation → EH-4; DGL-6/SIR-7; ~690 w)
- [x] ✅ §3.3.2 Ophthalmology-Specific Self-Supervised Pretraining (NEW v6.0.0) — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; CFC-2.8 composite IV central; lit-GAP #73-only flagged + 1 [UNSOURCED CLAIM]; spec-not-result, SSL arm untrained; ~1,000 w)
- [x] ✅ §3.3.3 Two-Stage Fine-Tuning Protocol Design — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; H-3-dropped training-method framing; SIR-4/5/7; identical schedule→EH-4; ~660 w)
- [x] ✅ §3.3.4 Weighted Loss Function Formulation — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; focal loss γ=2 inverse-freq; SC-1.4 principal lever; κ ordinal tie; focal-loss source gap [VERIFY]; ~700 w) — **§3.3 COMPLETE**
- [x] ✅ §3.4.1 Multi-Metric Assessment Framework — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; TAB-3.2 + TAB-3.3 inline & interpreted; EH-1/2, OD-4/5, NC-14, SB-1.10; ~1,210 w)
- [x] ✅ §3.4.2 Cross-Validation and Statistical Reliability Protocols — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; patient-level 5-fold CV + test suite; TAB-3.1 inline; EH-3/4 restated; DGL-2/SB-2.2; ~1,000 w) — **§3.4 COMPLETE**
- [x] ✅ §3.C Conclusions to Chapter 3 — ✅ verified (APPROVED 2026-06-09; brief/draft/continuity/review saved; synthesis, no new claims; reproducibility + bounded commitments consolidated; ~560 w) — **Chapter 3 COMPLETE**

**Chapter 6 — System Architecture (design-only)**
- [x] ✅ §6.1.1 Functional and Non-Functional Requirements — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; design-only status fixed (SB-4.1); FR-1…7/NFR-1…8 tables synthesized from #22 + OD-6; NFR-envelope-dominance argued; no [UNSOURCED CLAIM] raised; ~897 w) — **Chapter 6 OPENED (calibration unit)**
- [x] ✅ §6.1.2 Modular Architecture with PACS and EHR Integration — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; Table 6.3 module→FR→NFR decomposition synthesized from #22 EB-02/06; asynchronous store-and-forward PACS/EHR topology argued from OD-6/NFR-4; #36 used as external FHIR/HL7 feasibility corroboration under SIR-3; DIA-6.1 cited + DIA-6.3 UML deferred placeholder; no [UNSOURCED CLAIM] raised; ~1,155 w) — ⚠️ (DIA-6.3 UML deferred)
- [x] ✅ §6.2.1 Preprocessing Engine with Configurable Pipeline — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; module core = Ch3 8-stage pipeline AS SPECIFIED not validated, OD-5 = target/PC-1 CONDITIONAL held; configurability = stage/param/mode axes → NFR-1/2/3 + NFR-5; P2 first-class module central; NC-17 honored; DIA-6.2 reuse FIG-3.1 by path; ~904 w)
- [x] ✅ §6.2.2 Inference Module with Model Selection Logic — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; design-only, NO experiment numbers; FR-3 grade + FR-4 post-hoc Grad-CAM (NC-14) + SB-1.3 decision-support; model-selection = resource-envelope-fit not ranking (DGL-2); ResNet-50/EfficientNet-B3 only, B4 not adopted; NC-6/SIR-7 held; FIG-6.1 illustration-only by path; ~761 w)
- [x] ✅ §6.3.1 Telemedicine and Portable Device Support (incl. 6.3.1.1–6.3.1.3) — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; 3 sub-sections: distributed telemedicine via store-and-forward + peripheral/reading-centre split; national eHealth FHIR/HL7 integration w/ infra prerequisite (DGL-4); real-time low-resource = DESIGN FEASIBILITY not demonstrated (SB-4.1/SB-4.3); #14/#45/#34 deployment precedent w/ SIR-2/3, #45 specialist comparison NOT echoed; KZ benefits = projections (SIR-8/NC-3); FIG-6.1 illustration by path; no [UNSOURCED CLAIM]; ~1,193 w)
- [x] ✅ §6.3.2 Physician-in-the-Loop Decision Support Interface — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; SB-1.3 spine: decision-support NOT standalone, clinician = decision-maker; FR-3 grade + FR-4 Grad-CAM overlay (NC-14 not localization); override/audit channel = accountability counterpart; Doctor-AI feedback loop #22 EB-05; Diagnostic Result persists clinician disposition; no usability/acceptance result (SB-4.1); ~690 w)
- [x] ✅ §6.4.1 GDPR/HIPAA-Aligned Data Management Protocols — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; lands §6.1.2/§6.3.1.2 security deferral; encryption/auth/RBAC/de-id/audit/minimization protocols → NFR-7; store-and-forward protection consequence; GDPR/HIPAA-ALIGNED design spec NOT certified (SB-4.2/NC-9); #22 p.90 "compliant" REFRAMED per §V.2 not repeated (CFC-2.6); no statute asserted as satisfied; ~678 w)
- [x] ✅ §6.4.2 Applicability to Kazakhstan Healthcare Infrastructure — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; applicability = bounded DESIGN-FIT argument (OD-6 envelope ↔ KZ documented context), NOT demonstrated benefit; #22 p.87–88 benefits held as third-party PROJECTIONS not outcomes (SIR-8/NC-3); applicability bounded by absence of field testing (SB-4.3); national statute = design target, none asserted satisfied; ~640 w)
- [x] ✅ §6.C Conclusions to Chapter 6 — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; synthesis only, no new claim; OD-6-envelope-as-binding-driver thread consolidated; SB-4.1 design-only reaffirmed chapter-wide; reserved targets recalled (OD-5/PC-1 Phase 2, NC-9/SB-4.2, SIR-8/SB-4.3, DIA-6.3); ~495 w) — **Chapter 6 COMPLETE**

**Chapter 4 — §4.1 only (Datasets & Configuration)**
- [x] ✅ §4.1.1 Dataset Architecture — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; design/setup only — NO results; tiered 8-dataset architecture (TRAINING/EXTERNAL/CLINICAL/DEVICE) rendered as TAB-4.1 inline; DGL-1 bounding + SIR-3/SB-2.3 heterogeneity; #47/#48/#49/#50/#51 index-only flagged (#51 unconfirmed); #41 scale-only (metric-inconsistency); #19/#21 one thread + #24 SIR-4/SIR-5; FIG-4.2/4.3 placeholders; no [UNSOURCED CLAIM]; ~1,200 w) — **Chapter 4 §4.1 OPENED**
- [x] ✅ §4.1.2 Class Distribution Analysis and Data Partitioning — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; design/setup only; EyePACS imbalance = SC-1.4 lever → EH-1 metric hierarchy + inverse-freq focal loss + train-only aug (ref §3.4.1/§3.3.4/§3.1.3, not re-derived); label harmonization to 5-class ICDR + Exp-6 DR-labels-only (SB-2.3/SIR-3); patient-level grade-stratified 5-fold (reuse §3.4.2); no fabricated per-grade counts (FIG-4.1 placeholder, SIR-1); IDRiD no-class-distribution SIR-2; no [UNSOURCED CLAIM]; ~1,000 w)
- [x] ✅ §4.1.3 Hardware Specification and Reproducibility Protocol — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved; design/setup only; RTX 3060 12GB/WSL2/conda framed as DGL-2-bound design parameter (batch 16 @512² ← VRAM; mixed-precision split); TAB-3.1 rendered inline (as Table 4.2); reproducibility = engineered confound-removal (seed 42/deterministic, fixed aug+schedule, versioned code App A); SB-2.2 private-data limit; OD-6 framing w/o real-time claim (CFC-2.4); #21 SIR-4; no [UNSOURCED CLAIM]; ~720 w) — **§4.1 COMPLETE; §4.2–§4.8 Phase-2 blocked**

**Appendices writable now**
- [x] ✅ App A — Source Code of the Preprocessing Pipeline — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved in `chapters/08-appendices/`; code catalogue of real on-disk `experiments/src/preprocessing/` — stage→module map Table A.1 + verbatim `flat_field.py` excerpt; no-invention rule honored, every path verified on disk; closes §4.1.3 reproducibility loop; CENTRAL_THESIS framing; SIR-4 #19/#21/#23/#24 lineage; DGL-2 carried; no [UNSOURCED CLAIM])
- [x] ✅ App D — Certificates and Publication Confirmations — ✅ verified (APPROVED 2026-06-10; brief/draft/continuity/review saved in `chapters/08-appendices/`; Table D.1 = 5 distinct co-authored publications (EEJET #23/#24 counted once per SIR-5; Procedia/DS2025 #19; KBTU #21; KazUTB #20; NAS RK #22) + 6 confirmation PNGs by real path; SIR-4 on every entry; EEJET "100%" named-as-not-repeated (SIR-1/CFC-2.5); `scopus-q2` ID `LC-AlTimemy-2021` anomaly flagged; no fabricated entry) — **Phase 1 COMPLETE (App A + App D were the last two writable-now items)**

### Phase 2 — UNBLOCKED (all experiments run)

> **Gate status changed.** Every experiment has been executed and all seven hypotheses are confirmed.
> The gating resources G-1…G-19 below are historical; the live status of each asset is
> `ASSET_INVENTORY.md §2` and the live numbers are `results/` (`tables/`, `findings/`, `hypotheses/`),
> which is the **single source of truth**. Two residual constraints, not full blocks:
> **G-3** — the clinical (KZ) Grad-CAM overlays were not produced, so §4.6 is writable in its
> quantitative part only; **NEW-1** — the run's raw artifacts are not yet in `experiments/outputs/`,
> so results are writable but not yet traceable to a primary output file (must close before defense).
>
> **Structural change:** H-3 (domain distance) is reinstated as a new **§4.4**; Exp 3–7 shift to
> §4.5–§4.9. See `ASSET_INVENTORY.md §1.3`.

**Chapter 4 — Experiments (results)**
- [x] ✅ §4.2.1 Restored 2×2 Factorial Design (Configs A–D) — ✅ verified (APPROVED; brief/draft/continuity/review saved; design register, **no metric**; Table 4.3 factorial structure inline; P1/P2 framing per README Task 2.6 with OD-3 operational-construct caveat; EH-3 stated conjunctively **before** the data with its rationale; EH-4 shown internally testable; **CFC-2.8 composite IV declared at the point of asymmetry and routed forward to §4.3**; NC-6/SIR-7 disclaimed; ~1,000 w prose)
- [x] ✅ §4.2.2 Training Dynamics and Convergence Analysis — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.4 convergence + 4.5 calibration (TAB-4.3) inline; **joint-signature regularization argument** — integrated arms peak ep 7–10 vs 14–17, gap 2.5× smaller, **higher** train loss at comparable val loss; attribution explicitly labelled interpretation (SIR-1) with corroboration delegated to §4.3/§4.4; **calibration IMPROVES** (ECE ≈1.7× lower) — the prior "degrades calibration" caveat withdrawn; per-epoch trajectories not retained → FIG-4.5 uncited; CFC-2.4/NC-9 bounding; ~1,000 w prose)
- [x] ✅ §4.2.3 Quantitative Comparison of Diagnostic Metrics — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.6–4.10 inline; **H-1 SUPPORTED** — EH-3 met on all three components, both backbones (ΔwF1 +6.54/+6.55 pp, ΔAUC +0.0320/+0.0360, Δκ +0.1129/+0.1103); **EH-4 met by interaction test** (p = 0.31), not by point-estimate coincidence; Holm-corrected p = 0.0082/0.0056 with **calibrated language** (z ≈ 2.9 = moderate but stable); gain minority-weighted (macro-F1 > weighted F1); **DR1 doubles but stays ≈0.21 — stated**; κ gain derived from distant-cell emptying; **sensitivity +11.2 pp WITH specificity rising** = curve shift, paying the §4.2.2 debt; CFC-2.8 at the verdict, DGL-1/SB-1.3/NC-3/CFC-2.4 bounding; ~1,270 w prose) — **§4.2 COMPLETE**
- [x] ✅ §4.3.1 Cumulative Ablation Design (Levels L0–L7) — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.11 (TAB-4.4) + 4.12 (ranking) inline; **THE CFC-2.8 DECOMPOSITION DISCHARGED** — single initialization at all levels, L0 = 0.7538 ≡ Config C, L7 = 0.8193 ≡ Config D, cumulative +0.0655 ≡ Exp-1 +6.55 pp, **with the fence** that Exp 1 is not retroactively made single-factor; per-fold monotonicity 5/5 no inversion; 7/7 contributions exceed 2·σ_fold with the **heuristic named as a heuristic**; photometric pair leads at 41 %; **grouping resolution only — no strict 1-to-7 rank**; three limitations in the body incl. **Stage-3 not isolated**; NC-17 explicit; ~1,150 w prose)
- [x] ✅ §4.3.2 CLAHE Threshold Sensitivity Analysis (H-2) — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.13 (FIG-4.9) + 4.14 per-class inline; **interior optimum in both dimensions** with the decline sequence given; θ\* = (2.5, 0.03), p_apply 0.80; per-class optima diverge (θ̂(DR1) 2.5 vs θ̂(DR2) 2.0) with the lesion-scale reading **labelled as interpretation**; held-out Δ +0.0599 CI [+0.0388, +0.0770]; **grid = selection surface, held-out = performance** rule established; **DR1 grid/held-out gap disclosed** (0.2091 vs 0.4693) as an open observation; DGL-5 + CFC-1.2 bounding; grid dimensioning **resolved against the source of record**: primary sweep is 7×5 = 35 combinations (clip 1.0–4.0), the clip-0.5 row is a separately run extended-range check that the consolidated results table had merged in — distinction now carried in both tables and the bounds ¶, no value changed; ~950 w prose)
- [x] ✅ §4.3.3 Flat-Field σ Sweep and Image Quality — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.15 (FIG-4.10) + 4.16 (TAB-4.5) inline; strictly unimodal interior optimum at σ\* = 0.07·D_FOV, R = 0.0512 ≈ the whole pipeline effect; framed as **validation of the already-specified value, not new tuning**; held-out Δ +0.0574 CI [+0.0428, +0.0806]; TAB-4.5 read **level by level** → **41 %/49 % synthesis**: image-quality metrics *track the photometric part of the mechanism and do not exhaust it*, improvement **neither necessary nor sufficient**; CLAHE lowering CNR while contributing 19 % used as the counterexample; **VVI excluded — no implementation, no source**; cross-table CNR incomparability (SIR-3); ~1,050 w prose) — **§4.3 COMPLETE; H-2 established in both arms**
- [x] ✅ **§4.4.1 H-3 Measurement Protocol (MMD / KL)** — ✅ verified (APPROVED; brief/draft/continuity/review saved; protocol only, no value reported; two measures at two levels with the argument for needing both — **pixel-level near-tautology risk conceded openly**, representational measure carries the hypothesis; **MMD model-dependence caveat stated AT the protocol** (arms measured in different feature spaces); **the source-domain-statistics property** — Stage 7 uses source stats, targets never recompute → convergence achieved by Stages 0–6, **not covert target adaptation**; six domains span all three non-training tiers; **NEW-2: three parameters `[VERIFY]`-flagged, none invented** (no MMD implementation exists in the repo); ~700 w)
- [x] ✅ **§4.4.2 H-3 Distance Reduction Results** — ✅ verified (APPROVED; brief/draft/continuity/review saved; Table 4.17 (TAB-4.11) inline, FIG-4.17 as `ASSET TO BE CREATED`; **H-3 SUPPORTED 6/6 on both measures**, Δd +0.0700…+0.0931 with **all six CIs excluding zero**, KL −34…−38 %; three structural inferences — **proportional compression** (narrow band regardless of initial remoteness), **ranking preserved → domains narrowed but NOT made equivalent** (stated as a limitation), no target adaptation; **magnitude non-correspondence given a full paragraph** — DDR smallest gain at middling Δd, APTOS 5th on Δd/2nd on gain, **ρ ≈ 0.49**, retired "smallest reduction = smallest gain" formulation absent and contradicted; **direction only, never magnitude; no causal claim**; ~980 w) — **§4.4 COMPLETE; the mechanism is measured, not inferred**
- [x] ✅ §4.5.1 Zero-Shot Transfer to APTOS 2019 — ✅ verified (APPROVED; brief/draft/continuity/review saved; Table 4.18 (TAB-4.6) inline; zero-shot defined operationally (no retraining, source-domain normalization statistics); G motivated before applied; **H-4 SUPPORTED**, G_D = 0.8976 ≥ 0.85; **qualified in the same passage — G_C = 0.8577 also clears, so the threshold does not discriminate the arms**: *"the pipeline does not rescue a transfer that would otherwise fail; it improves a transfer that was already acceptable"*; **G-denominator asymmetry** identified as structural to ratio-based measures and linked forward to §4.7/§5.4; fold-0 limitation with its interval consequence; ~840 w prose)
- [x] ✅ §4.5.2 Baseline vs Pipeline Comparison — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.19 per-class + 4.20 referable inline; all five grades higher, DR1 ×1.95 / DR3 ×1.33 **with residual absolute weakness stated**; confusion structure read cell by cell (DR2→DR1 245→192, DR3→DR0 10→1, DR4→DR0 6→0) → **"ordinal coherence"** derived and tied to κ 0.7887 → 0.8874; referable Sens +10.6 pp **with** Spec +2.0 pp → curve shift reproduced under transfer; **cautionary H-3 connection at full weight** — APTOS 5th on Δd but 2nd on gain; ~780 w prose) — **§4.5 COMPLETE; H-4 supported**
- [x] ✅ §4.6.1 Grad-CAM Generation Protocol — ✅ verified (APPROVED; brief/draft/continuity/review saved; protocol only, no measurement; **NC-14 stated FIRST as a property of the instrument, not a hedge**; paired design justified (per-image difficulty differences out); mask subset stated plainly — **54 of 516**, per-type counts 54/53/54/**26**; ALO primary / IoU secondary with the **diffuseness caveat pre-stated** so low absolute IoU is not misread; τ sweep and floor-effect control **specified in advance**; SIR-2 IDRiD provenance inherited; ~830 w)
- [x] ✅ §4.6.2 Quantitative ALO and IoU with IDRiD Lesion Masks — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.21 (TAB-4.7) + 4.22 (IoU) + 4.23 (τ sweep) inline; **4/4 lesion types on both measures**, all CIs exclude zero, all p < 0.05 at τ = 0.5, ALO effects +0.0992…+0.1288; **IoU framed as corroboration, NOT a second finding**; conspicuity ordering as a *weak* validity check; largest relative gain on microaneurysms (≈49 %) matching the DR1 pattern; **τ = 0.7 exception reported** (3/4) and attributed to reduced power; floor fraction **6/54 = 0.111** → 48 informative pairs; arm comparability established; closing separates supported from unsupported; ~1,020 w prose)
- [x] ✅ §4.6.3 Per-Image Consistency of the Attention Effect and Limits of the Present Evidence — ✅ verified (APPROVED; brief/draft/continuity/review saved; **SECTION RETITLED** — the outline title promised a cross-dataset measurement that was never made, FIG-4.13 carries per-image direction counts; TOC + README corrected; Table 4.24 inline, **65–76 % improved / 9–15 % worsened**, licensing argument made before the numbers; **reversals reported and deliberately left uninterpreted** (sample too small, post-hoc pattern = over-fitting); **transfer ≠ attention-transfer** argument forecloses the old title's inference; **G-3 stated as an ABSENCE in its own paragraph** with four consequences — H-5 rests on one public corpus, App E limited to IDRiD, no retraining needed to close, routed to §5.4; ~780 w prose) — **§4.6 COMPLETE; H-5 supported in its QUANTITATIVE HALF ONLY**
- [x] ✅ §4.7 Experiment 5 — External Clinical Performance (H-7 v7.0.0) — ✅ verified (APPROVED; brief/draft/continuity/review saved; Table 4.25 (TAB-4.8) inline; **criterion stated in full BEFORE the table** incl. non-aggregation and Δ ≥ MCID **and** CI⁻ > 0 (*not* CI⁻ ≥ MCID); **H-7 SUPPORTED 2/2** — IDRiD +0.0689 (margin +0.0189), Messidor-2 +0.0541 (**margin 0.0041**); **thin margin in bold in the body**, with the stricter-reading alternative surfaced; **degradation reading FORECLOSED** via near-identical relative drops (21.2/19.1 %; 16.7/16.7 %) — *no reduced-degradation claim anywhere*; **Δ_drop identity derived in full and verified on both corpora** (−0.0034; +0.0114) → routed to §5.4 as a methodological contribution, retained descriptive only; **§4.8 non-independence disclosed**; ~1,250 w prose)
- [x] ✅ §4.8 Experiment 6 — Device Domain Shift (H-6) — ✅ verified (APPROVED; brief/draft/continuity/review saved; Tables 4.26 (TAB-4.9) + 4.27 (spread) inline; **§4.7 overlap disclosed BEFORE the table** — Kowa/Topcon *are* IDRiD/Messidor-2, coincide by construction, not independent replication; **H-6 SUPPORTED 5/5** with the both-arms-clear qualification; **substantive finding = spread reduction** std wF1 0.0306 → 0.0130 (−2.4×), std AUC 0.0214 → 0.0070 (−3.1×), both CIs excluding zero, range **compressed not shifted** (largest gain RFMiD +0.0987 from the weakest baseline); **retention-ratio inversions at DDR/Messidor-2 explained as a denominator artifact — the THIRD instance of one structural defect**; four limitations incl. "mixed" groups as a proxy and missing per-group confusion matrices; **NC-16 affirmatively in its own closing ¶**; ~1,180 w prose)
- [x] ✅ §4.9 Experiment 7 — Small Data Training — ✅ verified (APPROVED; brief/draft/continuity/review saved; Table 4.28 (TAB-4.10) inline; **preregistered**, both arms from the **same initialization** (so CFC-2.8 does not apply in its Exp-1 form); Δ wF1 **+0.0798**, κ +0.1245, AUC +0.0482, all paired CIs excluding zero; internal CV higher in **4 of 5 folds** reported as a **count**; **analytical core — the gain is COMPARABLE to, not larger than, the +0.0655 abundant-data gain**, which runs against the data-substitute intuition and favours a feature-space reading; **unpaired-interval overlap disclosed** (n = 60) with the correct consequence — the *difference* is established, not the *level*; **SB-2.2** — the one experiment that cannot be externally reproduced; ~1,020 w prose) — **§4.7–§4.9 COMPLETE; all five consequence tests met**
- [x] ✅ §4.C Conclusions to Chapter 4 — ✅ verified (APPROVED; brief/draft/continuity/review saved; synthesis only, **no new claim, no new number**; eight outcome paragraphs at established strength; **principal finding = CONSISTENCY, not effect size** — present in-domain, decomposable, traceable to measured distance reduction, observable on every corpus and camera grouping in both training regimes; **three standing qualifications consolidated** (H-4/H-6 thresholds cleared by both arms; H-5 quantitative half only; H-7 Messidor-2 margin 0.0041); **normalization defect named across all three instances and routed to §5.4** as a secondary methodological contribution; **seven open items** carried to Ch 5; **fence audit: 8 of 8 intact**; ~1,300 w — above nominal band, accepted as density since compressing further would cost the qualifications) — **CHAPTER 4 COMPLETE (18 sections, §4.1.1–§4.C)**

**Chapter 5 — Validation**
- [x] ✅ §5.1 Explainability Results — ✅ verified (APPROVED; brief/draft/continuity/review saved; Table 5.1 consolidates TAB-4.7 **without re-adjudication**; the section's own contribution is the **corroboration argument** — a classification gain admits a lesion-use account and a corpus-regularity account, both predicting the §4.2.3 metrics, only the first predicting attention movement toward annotated lesions — labelled dissertation-original interpretation and **bounded in the same passage by three limits**: different models (separate backbone, one fold) so corroboration is **directional not quantitative**, NC-14, one annotated corpus; **the +2.2 pp / +6.55 pp non-comparison made an affirmative rule**; FIG-5.1 declared an illustration carrying no measurement; **both absences stated** — cross-corpus attention consistency never measured, clinical overlays not produced (G-3); **NC-14 recast as a strength ceiling** handed to §5.2.2; ~1,180 w)
- [x] ✅ §5.2.1 Bootstrap CI and Mixed-Effects Model — ✅ verified (APPROVED; brief/draft/continuity/review saved; **three sources of variability distinguished** — training refits, evaluation-corpus sampling, paired case-level discordance — and used to organize the section; Table 5.2 maps procedure to experiment, **only Experiment 1 admits all three**; Table 5.3 (TAB-5.1) as the anchor; **paired tests primary, marginal-interval separation weaker**; the mixed-effects non-rejection given its exact content (**absence of evidence for heterogeneity, not evidence of homogeneity**; EH-4 met as specified, not upgraded); **two aggregate concessions in the body** — Holm is scoped to one experiment so **no dissertation-wide error rate is claimed**, and single-fitted-model evaluations **understate total uncertainty in a known direction**; ~1,070 w)
- [x] ✅ §5.2.2 Final Claim-Strength Classifications — ✅ verified (APPROVED; brief/draft/continuity/review saved; Table 5.4 (TAB-5.2) with **pre-specified promotion condition, outcome, level and travelling qualification** per claim; **classification framed as a check, not a judgement** — *"a criterion written once the result is known can always be satisfied"*; **the inflation objection engaged in the body** and answered in three parts, with **PC-8 exhibited as a failable criterion** and the regularization/calibration observations **shown as not promoted**; PC-0 not empirically promotable; **PC-10's 0.0041 margin and its lower bound +0.0362 below the MCID disclosed as the writer's job**; CFC-2.8 restated as **decomposable, not dissolved**; the meaning of STRONG bounded before the close; ~1,090 w) — **§5.2 COMPLETE**
- [x] ✅ §5.3.1 Benchmarking Against Published Systems — ✅ verified (APPROVED; brief/draft/continuity/review saved; **TAB-5.3 assembled here from the literature cards** — 11 rows, incommensurability carried by the **columns** (task as defined, corpus and partition, reference standard, metric, value); **four axes of difference** developed, with the reference-standard axis given separate treatment (adjudicated panels vs public labels); De Fauw as the instructive limit case (OCT); **the one honest comparison made once and bounded four ways**, yielding no ordering; **the evasion objection answered** — the refusal is forced, *"no two rows share all four"*; the permitted P1 practice observation with its **practical** consequence (results not decomposable ⇒ the comparison could not be made controlled); **a system without an obtainable validation report is absent rather than given a borrowed figure**; ~1,110 w)
- [x] ✅ §5.3.2 Performance–Complexity Trade-Off Analysis — ✅ verified (APPROVED; brief/draft/continuity/review saved; Table 5.6 measured cost of all four configurations; **the cheap-prior result** — 4th channel ≈ +0.9 % operations, ≈ 24 MiB, latency within noise — stated **with its confinement in the same passage**: the eight preprocessing stages **were not benchmarked**, so the table *"describes the cheaper half of the system"*; **two corrections**: operations do not predict time (≈ 4.3× fewer operations → ≈ 9 % at batch 16 and a **reversal at batch 1**) ⇒ the trade-off is argued from wall-clock time (SIR-7, NC-6 stated there); parameters do not predict memory (≈ 13.7 vs ≈ 3.7 GiB) ⇒ **the batch-16 limit follows from activation size at 512²**, with the host-paging condition disclosed; DGL-2 applied section-wide; ~880 w) — **§5.3 COMPLETE**
- [x] ✅ §5.4 Limitations and Boundary Conditions — ✅ verified (APPROVED; brief/draft/continuity/review saved; organized by **five kinds of boundary**, not by code, every item attributed to its originating section and **none softened**; **centrepiece = the normalization defect** — three instances of one fault (generalization ratio, retired degradation form, retention ratio), the identity Δ_drop(D) − Δ_drop(C) ≡ Δ_in-domain − Δ_external given in full, the reading recommendation stated, presented as a **secondary methodological contribution kept strictly descriptive** — *"it rehabilitates nothing"*; **all seven measurement gaps**; **full SB-1.x/2.x/3.x/4.x + DGL-1…6 + NC-3, NC-10…NC-17 enumeration achieved in prose** with each code attached to the statement it bounds; **NC-13 explicit** on self-citation independence; closes with what survives, at established strength; ~1,290 w)
- [x] ✅ §5.C Conclusions to Chapter 5 — ✅ verified (APPROVED; brief/draft/continuity/review saved; **synthesis only — no new claim and no new number**, the only numerals being counts; opens on the chapter's function — *"Chapter 5 did not add to the dissertation's results; it fixed what they are worth"*; three movements — final strengths (uniformity **explained**, not displayed), all seven hypothesis outcomes each with its fence, and **open questions sorted by what closing them requires** (four without new model training, three needing new experiments or data, one that measurement cannot close); closing position states what the evidence supports and what it does not; **chapter-level fence audit: 8 of 8 intact**; ~760 w) — **CHAPTER 5 COMPLETE (7 sections)**

**Chapter 0 — Introduction & Front Matter** — ✅ **COMPLETE, 16/16.** The gate is discharged: §0.8 was the last block and §5.2.2 (TAB-5.2) supplied it. Thirteen sections drafted and approved here; the three front-matter units were already complete as EN/KZ deliverables in `thesis/output/`.

> **Two orderings, both binding.** Section **identifiers** below are stable and are the ones referenced in
> governance, `PROJECT_MEMORY/` and `continuity/5.C-continuity.md` — in particular **§0.8 = Provisions
> Submitted for Defence**. The **manuscript order** is `outline/TABLE_OF_CONTENTS_EN.md`'s and is *not* the
> numeric order of the identifiers; it is given in the "pos." column and recorded in
> `chapters/00-introduction/README.md`. `MASTER_OUTLINE.md`'s Introduction ordering follows the identifiers
> and is superseded for the manuscript. Four TOC items had no identifier here and receive §0.13–§0.16.
>
> **Phase-3 note:** `assembly/_assemble_en.py` sorts drafts numerically, which equals TOC order for every
> chapter **except this one**. Chapter 0 must be assembled from an explicit ordered list.

- [x] ✅ §0.FM1 Normative References — **complete outside `chapters/`**: `thesis/output/normative_references_{en,kz}.md`, exported to GOST docx/pdf, verified against the IITU samples. No draft is produced here.
- [x] ✅ §0.FM2 Definitions (OD-1…OD-6 verbatim) — **complete outside `chapters/`**: `thesis/output/definitions_{en,kz}.md`.
- [x] ✅ §0.FM3 Designations and Abbreviations — **complete outside `chapters/`**: `thesis/output/abbreviations_{en,kz}.md`.
- [x] ✅ §0.1 Relevance of the Research *(pos. 1)* — ✅ verified (APPROVED; brief/draft/continuity/review saved; five movements — clinical fact → capacity constraint → technical situation → P1/P2 pre-introduction → answerability; Kazakhstan figures cited as prior own work **and** the p. 88 projections disowned in the sentence that introduces them (SIR-8/SB-1.6/CFC-2.3); Gulshan named twice, once as landmark and once as canonical P1 representative in the permitted practice-grounded form; **no result of the dissertation anticipated anywhere**; SB-1.3 boundary in the close; ~1,125 w — over the 800–1,000 band, trim queued)
- [x] ✅ §0.2 Scientific Novelty *(pos. 6)* — ✅ verified (APPROVED; brief/draft/continuity/review saved; **novelty separated from strength in the opening sentence** — kind not magnitude, strength deferred to §0.8; P1 → P2 stated as the principal item before the list, with the dual engineering/conceptual character it confers; **ten items covering the whole `CONTRIBUTIONS.md` v7.1.0 register**, incl. the three the outline cannot supply — **SC-I** with both design features (source-domain statistics; prospectively recorded falsifiability), **SC-H including the negative gate result** (from-scratch label-free CNN-SSL failed the linear probe — reported as evidence, *"the gate exists precisely so that an initialisation may fail it"*), and the **transfer-measure defect** held strictly descriptive; CFC-2.8 at three points, incl. the ablation item's fence in the same clause; SIR-4/SIR-5 on the self-publication lineage; ~1,205 w over the 800–1,000 band, trim queued with items 2 and 8 named as compressible)
- [x] ✅ §0.3 Research Goal *(pos. 2)* — ✅ verified (APPROVED; brief/draft/continuity/review saved; goal sentence enumerates the eight stages in canonical OD-3 order and fixes validation as *controlled contrast*; three clauses — unit of evaluation is the configuration not the network, five validation directions incl. **the domain-distance measurement**, and the OD-6 envelope as a constraint on the goal; **CFC-2.8 pre-honoured at goal level**; optimality disclaimed (SB-3.1); ~535 w over the 300–500 band, trim queued; **first paragraph must be preserved verbatim** — it is quoted in the abstract and defence materials)
- [x] ✅ §0.4 Research Objectives *(pos. 3)* — ✅ verified (APPROVED; brief/draft/continuity/review saved; six objectives, one per chapter, in chapter order, each an undertaking and none an achievement; **objective 4 fixes the programme at eight investigations, not seven** — H-3 present, and the non-monotone mappings Exp 5 → H-7 and Exp 6 → H-6 made explicit; SB-1.5/SIR-6 attached to the thermal-optical model and SB-4.1 to the architecture objective at their only mentions; exhaustiveness claimed in both directions; ~695 w over the 400–600 band, trim queued)
- [x] ✅ §0.5 Object and Subject of Research *(pos. 4)* — ✅ verified (APPROVED; brief/draft/continuity/review saved; **object = the process**, studied camera-to-grade, with the eight-corpus architecture named as *material* and explicitly not as the object — a deliberate departure from `MASTER_OUTLINE.md`, which commits the category error and substitutes a corpus list for a definition; **subject = the integration** and its four properties, which is where CFC-2.8 would otherwise be prejudged at scope level; joint SB-1.4 boundary; ~290 w — **inside band**)
- [x] ✅ §0.6 Research Hypothesis (H-1…H-7) *(pos. 5)* — ✅ verified (APPROVED; brief/draft/continuity/review saved; central hypothesis given as a **two-link causal claim** with H-3 testing the first link and the other six the second, so the register reads as an argument not a list; EH-3 stated conjunctively **with the subset exclusion**, EH-4's two extra requirements named; **CFC-2.8 inside the H-1 statement** as a property of the design; **H-3 carries all three mandatory disclosures** — label reuse (the retired training-method hypothesis stands retired), the source-domain-statistics protocol condition with its consequence, and the openly stated threshold provenance (MCID_d and K assigned at formalisation, not pre-registered, bounded by unnormalised units and insensitivity to K); **H-7 correct on all four precision points** incl. CI⁻ > 0 *not* CI⁻ ≥ MCID, and performance-not-resistance; NC-14 in H-5, NC-16 in H-6; VCR-3 in the close; **register-fidelity check 12/12**; **pre-specification integrity verified — every numeral is a threshold, no outcome leaks**; ~1,205 w over the 600–900 band, four clauses excluded from the trim)
- [x] ✅ §0.7 Methodological Basis *(pos. 8)* — ✅ verified (APPROVED; brief/draft saved; block review `reviews/0.apparatus-review.md`; methods as a **system** around one principle — controlled comparison with everything outside the manipulated factor held fixed; **EH-1's metric order reproduced exactly**; CFC-2.8 as a property of the design; DGL-6 — in-domain initialisation gate-selected, not assumed; **both aggregate concessions from §5.2.1 carried into the front matter** (multiplicity correction scoped to one experiment → no dissertation-wide error rate; single-fold intervals understate total uncertainty in a known direction); **VVI deliberately absent** — §4.3.3 excluded it, no implementation and no source; ~625 w over the 400–600 band, concessions paragraph excluded from the trim)
- [x] ✅ §0.8 Provisions Submitted for Defence *(pos. 7)* — ✅ verified (APPROVED; brief/draft/continuity/review saved; **the chapter's last gate, discharged**; eleven provisions grouped by kind — one conceptual (PC-0), eight empirical (PC-1, PC-2, PC-8, PC-11, PC-6, PC-7, PC-9, PC-10), one methodological (the transfer-measure defect, strictly descriptive), one combining PC-4 + PC-5 as non-empirical — plus the small-data result deliberately submitted **as an observation, not a provision**; **PC-3 left unused**, gap not closed by renumbering; **fence audit 8 of 8 intact** and **promotion audit against TAB-5.2 shows no promotion and no softened qualification**; the Messidor-2 margin **0.0041** disclosed together with its sub-threshold lower bound — a fence *stronger* than the table's; **exactly one metric value in the whole section**, and no table reproduced, so the Introduction cannot be used to re-adjudicate Ch 4; closes by enumerating what is **not** submitted and by explaining the uniformity of the levels rather than displaying it; ~1,255 w over the 700–900 band — the excess is the qualifications, which the brief forbids paying from)
- [x] ✅ §0.9 Theoretical Significance *(pos. 9)* — ✅ verified (APPROVED; brief/draft saved; block review; five items, **none of them a result** — the reframing and what it changes about what counts as a complete model description; three formalisations; **making a postulated mechanism measurable**, claiming *"the measurability and the condition that gives it force, not what the measurement returned"*; the analytic defect in normalised transfer measures, independent of this work's results; the thermal-optical model with SB-1.5/SIR-6; SIR-4 on the CLAHE lineage; ~495 w — **in band**)
- [x] ✅ §0.10 Practical Significance *(pos. 10)* — ✅ verified (APPROVED; brief/draft saved; block review; four items, **each carrying its bound in its own paragraph** rather than in a trailing disclaimer a reader might not reach; the projected national outcomes **named, sourced and disowned in a single sentence** (SIR-8/SB-1.6/CFC-2.3/NC-3) with no figure quoted; SB-4.1/4.2/4.3 all three in the architecture sentence; NC-15 on the ingestion protocol; DGL-5 on parameter portability; SB-1.3 closing frame; **the measured computational cost deliberately not quoted** — it belongs to §5.3.2 and was not submitted in §0.8; ~445 w — **in band**)
- [x] ✅ §0.11 Approbation of Research Results *(pos. 13)* — ✅ verified (APPROVED; brief/draft saved; block review; DS 2025 Istanbul 28–30 Oct 2025 with its Scopus-indexed proceedings paper; counts traced to App D Table D.1 exactly — one conference, five distinct outputs; SIR-4 on every entry, SIR-5 as a standing rule, and the **no-import rule on prior publications' performance figures** stated; ~275 w — **in band**)
- [x] ✅ §0.12 Publications *(pos. 15)* — ✅ verified (APPROVED; brief/draft saved; block review; **five distinct works, not six** — categorised 1 Scopus/WoS journal / 1 Scopus conference / 3 KKSON-recommended — with the two-records-one-article situation **disclosed in its own paragraph** rather than silently resolved (SIR-5); App D pointed to rather than duplicated, so the two records cannot diverge; ~220 w — **in band**)
- [x] ✅ §0.13 Reliability of the Results *(pos. 11)* — ✅ verified (APPROVED; brief/draft saved; block review; reliability argued **from procedure, not magnitude**; pre-specification given its own paragraph with the reason it matters — *"a criterion written once a result is known can always be satisfied"*; **three qualifications stated, not only strengths** (multiplicity scoped to one experiment; single-fold intervals understate uncertainty; a non-redistributable corpus, plus SB-1.10 on calibration); placement-not-ranking given **with its reason**; ~480 w — **in band**)
- [x] ✅ §0.14 Empirical (Experimental) Basis *(pos. 12)* — ✅ verified (APPROVED; brief/draft saved; block review; the eight corpora as a **tiered architecture**, each of the four dataset boundaries at the point it binds — SB-2.1 imbalance at the training corpus, **SB-2.4 pretraining disjointness by image *and* patient identity**, SB-2.2 non-redistributability at the clinical corpus, SB-2.3 taxonomy mapping at the multi-disease corpora; closes on what heterogeneity buys and forbids — cross-corpus evaluation meaningful, **pooling not**; TAB-4.1 described rather than duplicated; ~496 w — **in band**)
- [x] ✅ §0.15 Connection with Scientific Programmes *(pos. 14)* — ✅ verified (APPROVED; brief/draft saved; block review; three policy instruments with exact designations and dates + the "On Science" article citation; stated as a **correspondence of research direction**, with funding, commission, mandate and any achieved policy objective denied in its own paragraph; ~188 w — **in band**)
- [x] ✅ §0.16 Structure and Length of the Dissertation *(pos. 16)* — ✅ verified (APPROVED; brief/draft saved; block review; composition, one clause per chapter stating what it *establishes* rather than its title, appendices A–F, and the ordering principle; Ch 6's design status in its own clause (SB-4.1); **no count invented** — four explicit `TO BE RESOLVED AT FINAL ASSEMBLY` placeholders for pages/tables/figures/references, since the document is not finished and any figure now would be fabricated; carries its own **Phase-3 obligation block** naming three things to revisit, incl. the possibility that not all six appendices survive; ~405 w, over by five and falls below band once the placeholders resolve)

> **Stale-governance register for Chapter 0** (recorded by the §0.1/§0.3/§0.4/§0.5 reviews; each must be
> corrected in a governance-sync pass, and none may be followed in the meantime):
> `CORE_OBJECTIVE.md` v5.0 — names *clinical degradation resistance* (H-7 was reformulated in INVARIANTS
> v7.0.0) and predates the restoration of H-3. · `MASTER_OUTLINE.md` v6.0.0 — records H-3 as dropped, carries
> the retired H-7 form, numbers two objectives "8", and defines the object of research as the images rather
> than the process. · `thesis/output/abstract_en.md` — says "seven experiments", omits H-3, and its provision
> 5 is still in the retired Δ_drop form; **the abstract sync pass is now DUE** — §0.2, §0.6 and §0.8 have
> landed and are what it must be resynchronised against. · **`results/tables/TAB-5.2_claim_strength.md`** —
> lists the domain-distance result under "additional empirical results outside the formal PCs", whereas
> `ARGUMENT_MAP.md` v7.1.0 has since added it as **PC-11**, a first-class node depending on PC-1 and feeding
> PC-6/PC-9/PC-10. Substance and strength agree (STRONG, direction only); only the register position differs.
> §0.8 submits it as PC-11 per the argument map; the table should be resynchronised.

**Chapter 7 — Conclusion** — ✅ **COMPLETE.**
- [x] ✅ §7 Conclusion — ✅ verified (APPROVED; brief/draft/continuity/review saved; six movements — the question restated as one about model **specification** · the seven hypothesis outcomes each with its fence in the Chapter-4/§5.C wordings, not paraphrases · the joint finding stated as **consistency, not effect size**, with what it does not license in the same movement · four kinds of contribution (conceptual, engineering, metrological, methodological — the last **strictly descriptive**) · the recorded negative result + limitations by shape · eight open questions sorted by closing cost, including **one measurement cannot close**; **fence audit 8 of 8 intact** through the document's most compressive section; **ceiling audit against §0.8 provision by provision — no promotion**; **VCR-3 discharged** (the initialisation branch that failed its acceptance gate is reported, not omitted); **no metric value anywhere** — the thin external margin stated in words per §5.C's precedent; one **deliberate omission** recorded (§0.8's provisions 11 not restated, since doing so would imply an empirical standing they lack); ~1,610 w — **inside the 1,500–2,000 band, no flags**)

**Appendices** — ✅ **COMPLETE, A–F.** Block review `reviews/BCEF-review.md`, continuity `continuity/BCEF-continuity.md`.
- [x] ✅ App B — Supplementary Experimental Results & Confusion Matrices — ✅ verified (APPROVED; 13 tables — per-class F1/P/R for all four configurations, four in-domain confusion matrices, two on the external public corpus, calibration, per-fold convergence, both kinds of interval estimate with the difference between what each quantifies made explicit, in-domain referable-DR metrics; **transcription verified mechanically — 168 distinct 3–4 dp values and 184 confusion-matrix integers, none absent from the source tables, nothing recomputed**; SB-2.1 with class sizes before the first per-class table, SB-1.10 beneath calibration, EH-2 in the opening; **§B.8 states three absences with a distinct reason and consequence each** — per-epoch trajectories not retained, per-class ROC/PR need prediction dumps that were not saved, per-group confusion matrices not recorded)
- [x] ✅ App C — System Architecture UML Diagrams — ✅ verified (APPROVED; **DIA-6.3 DISCHARGED — the last outstanding asset task in Chapter 6**; four views as diagram source (component, deployment, sequence, data) + a **module → FR → NFR traceability table** so the diagrams are checkable against Tables 6.1–6.3; nothing invented — where Chapter 6 fixes no detail the detail is omitted; SB-4.1 at the opening **and** the close, SB-4.2/NC-9 at security, NC-14 at the overlay, SB-1.3 as the terminal step of the sequence; **no metric value — the measured cost stays in §5.3.2**)
- [x] ✅ App E — Grad-CAM Visualization Gallery — ✅ verified (APPROVED; **the complete annotated subset — all 54 paired plates, no selection, floor cases retained**, with exhaustiveness *argued*: a gallery that selects can flatter and no reader can detect the selection from inside it; **NC-14 stated before the first plate** and the plates declared illustration carrying no measurement; subset bounds 54 of 516, per-type 54/53/54/26, floor 6 of 54 → 48 informative; **no per-plate commentary** — that would be exactly the post-hoc pattern-finding §4.6.3 refuses; **G-3 stated as an absence, not a negative result**)
- [x] ✅ App F — Device Domain-Shift Supplementary Tables — ✅ verified (APPROVED; 8 tables — group and per-group class sizes, wF1 + retention ratio, AUC + κ, referable AUC, per-class F1 by group for both arms, between-class spans, between-group dispersion; **three qualifications stated BEFORE the first table** — two groupings *are* the external clinical corpora, three aggregate several camera models, single fold so dispersion is between groups not folds; **§F.8 explains the retention-ratio artefact** as one instance of the §5.4 normalisation defect and bounds it as descriptive — *"it does not rehabilitate any result"*; NC-16 at the opening and the close; **159 distinct values verified against source, none absent**; §F.9 records the unrecorded per-group confusion matrices with their consequence)

### Phase 3 — final assembly

> **Two assembler defects were found and fixed 2026-08-11**, both of which would have produced a silently
> wrong book. (1) `_assemble_en.py` extracted only text under a literal `## PART 1` marker; Ch 1/2/3/6/0/7
> carry it, but **Ch 4 in only 3 of 20 drafts and Ch 5 in none of 7** — **24 sections assembled as empty**
> and nothing in the output said so. The extractor now falls back to the top of the file and **reports any
> suspiciously short body** instead of emitting it quietly. (2) Chapter 0's section identifiers deliberately
> do not follow manuscript order, so numeric sort produced the wrong sequence for that chapter alone; it is
> now assembled from an explicit list, and a mismatch between the list and the files on disk is a **hard
> error**. Chapters **0, 5 and 7 were also absent from the chapter list** — the script could not produce a
> complete manuscript at all — and the three front-matter units from `thesis/output/` are now inserted ahead
> of the Introduction. The same two fixes were applied to `_assemble_kz.py`.
>
> **Verified:** EN assembly now emits **94 sections / ≈94,200 words**, no suspect extractions (previously
> 53 sections with 24 of them empty). KZ emits 53 translations, no suspect extractions.

> **Re-verified 2026-08-12 against the emitted manuscript**, not against this tracker. EN emits
> **98 sections / 101,459 body words**; KZ emits **53 / 41,605**; neither reports a suspect extraction.
> The figures quoted in the paragraph above (94 sections / ≈94,200 words) were the state before Chapter 7
> and Appendices B/C/E/F landed.

- [x] ✅ §11.0 Assembler repaired — EN and KZ; run `python thesis/assembly/_assemble_en.py`
- [x] ✅ §11.1 Concatenate all approved drafts in **TOC order** (not `MASTER_OUTLINE` order — the two differ
  for Chapter 0, and the TOC is authoritative for the manuscript)
- [x] ✅ §11.0b **KZ assembler front matter — FIXED 2026-08-12.** `_assemble_kz.py` had no `FRONT_MATTER`
  block, so the KZ manuscript opened straight at Chapter 1 while the EN one carried normative references,
  definitions and abbreviations ahead of the Introduction; the three `thesis/output/*_kz.md` sources
  existed and only the insertion was absent. Ported from `_assemble_en.py`, with a missing file reported
  as suspect. **Verified: KZ now emits НОРМАТИВТІК СІЛТЕМЕЛЕР → АНЫҚТАМАЛАР → БЕЛГІЛЕУЛЕР МЕН
  ҚЫСҚАРТУЛАР ahead of Chapter 1; 53 sections, 41,605 words, no suspect extractions.**
- [x] ✅ §11.2 Assets — **ALL CLOSED 2026-08-12.** FIG-1.1, DIA-6.3, FIG-3.8, FIG-4.17, two
  ellipsis paths, and the inventory staleness. **Verified on both assembled manuscripts: every
  referenced asset path resolves to a file on disk, and `ASSET TO BE CREATED` is now zero.**
  Only the §0.16 count placeholders remain, and those can only close after conversion.
  90 `[FIG/TAB/DIA-…]` placeholders were
  scanned and 76 of the 80 distinct referenced paths resolve to files that exist; only these four fail.
  Also fill the **four count placeholders in §0.16** (pages/tables/figures/references — resolvable only
  after conversion) and confirm the two **intentional** `[UNSOURCED CLAIM]` markers (§3.1.4 ingestion,
  §3.3.2 SSL) are kept by decision while the three `[VERIFY]` markers are cleared.
- [x] ✅ §11.3a **Citation conversion — DONE 2026-08-12.** **107 sources numbered**, one shared register
  across both languages; EN 292 bracketed citations, KZ 230; reference list 107 entries in each language,
  no `[card not found]`. **BLOCKING 0 / residual self-citations 0 / UNKNOWN 1** — the single UNKNOWN is
  `(No. 230-VIII of 17 November 2025)`, a legal-act designation in §0.15, correctly not a citation.
- [ ] ⬜ §11.3b Trim queue (see §11.3 below) — the only part of the citation step still open
- [ ] ⬜ §11.4 Convert to GOST `.docx`/`.pdf`, EN and KZ — the converter **must render the 4 Mermaid
  fences** in Appendix C

### Phase 4 — Kazakh translation — ✅ COMPLETE 2026-08-12, 98/98

> Promoted from "out of scope, Stages E/F" to a first-class tracked phase, and closed the same day all
> 45 outstanding units landed. Pipeline was unchanged — translate `drafts/*.md` →
> `translations/*-translation.md` per `GLOSSARY_KZ.md`, then translation review.
> **The critical path has moved on: it is now §11.4, the EN + KZ GOST re-export.**

- [x] ✅ Ch 1 (11), Ch 2 (15), Ch 3 (13), Ch 6 (9), App A + App D — 53 units done
- [x] ✅ **Ch 4 — COMPLETE 2026-08-12, 20/20** (17 translated in this pass + §4.1.1–§4.1.3 already done).
  Every table transcribed digit for digit; verified assembling with no suspect extractions, and the
  KZ manuscript's asset paths all resolve. Fences carried across and checked per section — CFC-2.8 at
  §4.2.1/§4.2.3 and its **discharge** at §4.3.1 (single initialization stated before the claim, and the
  "this does not retroactively make Experiment 1 single-factor" sentence kept in the same paragraph);
  PC-8 grouping-resolution-only at §4.3.1; the selection-surface-vs-held-out rule and the open DR1
  discrepancy at §4.3.2; the 41 %/49 % "tracks but does not exhaust" formulation and VVI's exclusion at
  §4.3.3; the MMD/KL primary-secondary asymmetry at §4.4.1; **ρ ≈ 0.49 and direction-only at §4.4.2**;
  the both-arms-clear qualification at §4.5.1; **NC-14 stated before the method at §4.6.1**; the IoU
  "corroboration, not a second finding" status and the τ = 0.7 exception at §4.6.2; **G-3 as an absence,
  not a negative result, at §4.6.3**; the **0.0041 Messidor-2 margin in bold in the body** plus the full
  Δ_drop identity at §4.7; the retention-ratio inversions as a denominator artefact and NC-16 at §4.8;
  E-7 **comparable, not larger**, and the unpaired-interval overlap at §4.9; and all **eight fences
  restated at §4.C without softening**. Each translation carries a PART-2 term report and a translator's
  note recording what was deliberately held together.
- [x] ✅ **Ch 0 — COMPLETE 2026-08-12, 16/16.** Assembles in **manuscript order, not numeric** (§0.6
  before §0.2, §0.8 before §0.7) — verified against the emitted KZ manuscript.
  **Two invariants machine-checked after translation.** §0.6: the body contains exactly four decimals
  (0.0, 0.02, 0.050, 0.85) and **every one is a threshold**, so the pre-specification property §5.2.2
  depends on survived intact. §0.8: the body contains **exactly one metric value (0.0041)** and **PC-3
  does not appear**, so the Introduction still cannot be used to re-adjudicate Chapter 4.
  §0.5 keeps object = *process* with the eight corpora named as material (the deliberate departure from
  `MASTER_OUTLINE.md`'s category error) and subject = *the integration*, which is what stops CFC-2.8
  being prejudged at scope level. §0.2 carries CFC-2.8 at three points, the negative gate result, and
  the transfer-measure defect held strictly descriptive.
  §0.5 keeps object = *process* with the eight corpora named as material, and subject = *the
  integration*. §0.7 carries EH-1's metric order verbatim, DGL-6, and both §5.2.1 concessions. §0.10
  keeps each item's bound in its own paragraph and omits the measured computational cost, which §0.8
  did not submit. §0.16's four count placeholders are left in their English form in both languages so
  one Phase-3 scan finds them all.
- [x] ✅ **Ch 5 — COMPLETE 2026-08-12, 7/7** (§5.1, §5.2.1, §5.2.2, §5.3.1, §5.3.2, §5.4, §5.C).
  §5.1 keeps NC-14 as a **ceiling on claim strength, not a closing caveat**, and records both absences.
  §5.2.1 keeps the three-sources-of-variability structure, "only Experiment 1 admits all three", and
  both aggregate concessions. §5.2.2 keeps classification as **a check, not a judgement**, exhibits
  PC-8 as a failable criterion, names the two results that were **not** promoted, and — verified
  mechanically — reproduces the claim register with **11 rows and no PC-3 row**, exactly as the English
  does, while still naming PC-3 in prose as the unused identifier. §5.3.1 keeps the incommensurability
  in the **columns** and the refusal as **forced, not chosen**. §5.3.2 keeps the cheap-prior result
  inside its confinement (the eight preprocessing stages were never benchmarked) and both corrections.
  §5.4 keeps the normalization defect as the centrepiece, **strictly descriptive**. §5.C sorts the open
  questions by closing cost, including **the one measurement cannot close**.
- [x] ✅ **Ch 7 — COMPLETE 2026-08-12.** **Audited: the only decimal in the body is `5.4`, a section
  reference — identical to the English, so the "no metric value" property survived.** The thin external
  margin stays in words per §5.C's precedent; VCR-3 discharged (the failed initialisation branch is
  reported); §0.8's provision 11 deliberately not restated among the contributions.
- [x] ✅ **App B, C, E, F — ALL COMPLETE 2026-08-12.**
  **App C** — the four Mermaid blocks were kept **verbatim** and verified byte-identical to the English:
  the appendix itself calls the source "the definition of the diagram", its node labels are technical
  terms and governance codes the directive keeps in English, and an identical source guarantees both
  editions render the same figure. **App E** — the 54 plate lines were rewritten by one regex that
  translates the caption and leaves the `FIG-E.*` identifiers and image paths untouched; verified: all
  54 paths and all 54 identifiers identical to the English, in the same order.
  Both are transcription-only, so their Kazakh bodies were **derived programmatically from the English
  drafts** — only prose, headings, captions and column labels substituted, every numeric cell copied
  byte-for-byte. **Verified mechanically after the fact:** App B 529 numeric tokens identical and 84
  table rows in both; App F 295 identical and 53 rows. (The comparison must normalise *both* thousands
  conventions — EN `35,126` vs KZ `35 126` — or it false-alarms.) Group identifiers such as
  `mixed_ddr` are data keys and were left untranslated.
  **Remaining: App C and App E.**

---

## 2. PHASING BY DATA-READINESS

### Phase 1 — writable now (no real-result dependency)

Narrative order is fixed by the task:

> **Ch 1 (Problem Domain) → Ch 2 (Theoretical Foundations) → Ch 3 (Methodology, fully unblocked) → Ch 6 (System Architecture, design-only) → §4.1 (Datasets & Configuration).**

Rationale (from `ASSET_INVENTORY.md §1.3`): these chapters draw only on real artifacts already on disk — preprocessing stage renders (FIG-3.1…FIG-3.9), the OD/fovea validation (RES-VAL, FIG-3.10), norm-stats (RES-NORM), the PCA basis (RES-PCA), conceptual/architecture diagrams, dataset sample montages, the publication certificates (APP-D), and the literature corpus. No experimental *result* is required. App A (source code) and App D (certificates) are also writable now and are produced alongside Phase 1.

### Phase 2 — blocked, gated on experiment execution

Order (as instructed): **§4.2 → §4.3–§4.8 → Ch 5 → Ch 0 → Ch 7 → Appendices B/C/E/F.** For each, the exact missing Resource IDs (from `ASSET_INVENTORY.md §2`) that unblock it:

| Gate | Section(s) | Unblocking experiment | Missing Resource IDs that must become real |
|------|-----------|------------------------|--------------------------------------------|
| G-1 | §4.2.2, §4.2.3 (+ §4.C dependency) | **Exp 1** full A–D × 5-fold @100% incl. ophthalmology-SSL B/D arm + per-sample prediction dumps | TAB-4.2, FIG-4.4, FIG-4.5(full), FIG-4.6, FIG-4.7, FIG-4.8, TAB-4.3; RES-EXP1 upgraded ⏳→✅ |
| G-2 | §4.3.1–§4.3.3 | **Exp 2** (ablation + CLAHE sweep + σ sweep + image-quality) | TAB-4.4, FIG-4.9, FIG-4.10, TAB-4.5 |
| G-3 | §4.4.1, §4.4.2 | **Exp 3** (APTOS 2019 zero-shot transfer, G ratio) | TAB-4.6, FIG-4.11 |
| G-4 | §4.5.1–§4.5.3 | **Exp 4** (Grad-CAM ALO/IoU on IDRiD + Clinical) | FIG-4.12, TAB-4.7, FIG-4.13, FIG-4.14 |
| G-5 | §4.6 | **Exp 5** (clinical degradation, IDRiD + Messidor-2) | TAB-4.8, FIG-4.15 |
| G-6 | §4.7 | **Exp 6** (device domain shift, DDR/ODIR-5K/RFMiD) | TAB-4.9, App F set |
| G-7 | §4.8 | **Exp 7** (small-data IDRiD → Clinical) | TAB-4.10, FIG-4.16 |
| G-8 | §4.C | All of Exp 1–7 | (all of the above) |
| G-9 | §5.1 | Exp 4 | FIG-5.1, TAB-4.7, FIG-4.12 |
| G-10 | §5.2.1 | Exp 1–7 statistical suite | TAB-5.1 |
| G-11 | §5.2.2 | All Exp + claim-strength derivation | TAB-5.2, FIG-5.3 |
| G-12 | §5.3.1 | Own results + Exp 1/3/5 | TAB-5.3, TAB-5.4 |
| G-13 | §5.3.2 | Exp 1/6 | FIG-5.2, FIG-5.4 |
| G-14 | §5.4, §5.C | Final H-1…H-7 verdicts | (none new; depends on §4.C + §5.2.2) |
| G-15 | §0.8, §7 | Final claim strengths | depends on §5.2.2 (TAB-5.2) |
| G-16 | App B | Exp 1–7 | FIG-4.6, FIG-4.5(full), TAB-4.3 + per-Exp confusion/curves |
| G-17 | App C | UML drawing (asset, not experiment) | DIA-6.3 |
| G-18 | App E | Exp 4 | FIG-5.1, FIG-4.12 |
| G-19 | App F | Exp 6 | TAB-4.9 + per-camera matrices |

> **Note on Exp 1 partial data:** `RES-EXP1` is `⏳ PENDING` — real per-epoch metrics exist for Config A f0, A/B/C f0–2 @40%, and a clean Config D f0 (EyePACS). These are **not** sufficient for §4.2: the headline 2×2 factorial table (TAB-4.2) and the EH-3 dominance verdict require the full 100% A–D × 5-fold run, and the v6.0.0 ophthalmology-SSL initialization for the integrated arm (B/D) has not been trained at all. Confusion matrices / ROC / calibration (FIG-4.6/4.7, TAB-4.3) are *not derivable* from current outputs because per-sample predictions were not saved (`ASSET_INVENTORY.md §3 note 3`). §4.2 therefore stays blocked.

### Phase 3 — final assembly (LAST step, depends on Phase 2 completion)

See §11.

---

## 3. RESOURCE HONESTY POLICY (binding)

### 3.1 Hard honesty rule

**A section may NEVER be drafted if any *result-dependent* resource it requires is `❌ MISSING (real result)` in `ASSET_INVENTORY.md`.** Such sections stay ⛔ blocked and are skipped until the experiment is run. Specifically:

- **No fabricated metrics.** No number may be written into a results table/figure unless it comes from a real, machine-produced artifact verified in `ASSET_INVENTORY.md §3`.
- **No demo-dashboard previews as if real.** The files in `demo/web/public/results/` and the preview JSONs (`exp3_aptos_transfer.json` G=0.890, `exp5_degradation.json`, `exp7_small_data.json`, `exp2_ff_sweep.json`) carry placeholder numbers authored for the dashboard. They are **demo assets**, not results, and must not be cited as evidence (per **CFC-2.x / SIR-1**, and the §0 Provenance Policy of the inventory).
- **CFC-2.8 reminder for §4.2 / H-1:** the integrated arm uses ophthalmology-SSL pretraining and the baseline uses ImageNet; once results exist, any difference is attributed to the **integrated configuration**, never to "preprocessing alone."

### 3.2 Conceptual / UML diagrams are *deferred assets*, not blockers

A resource that is `❌ MISSING` but is a **conceptual or architecture/UML diagram with no experimental dependency** (FIG-2.1, FIG-2.3, FIG-2.4, FIG-2.5, DIA-6.3 / App C) does **not** hard-block its section — the prose carries no fabricated data. For these:

- The section is **⚠️ writable-now (deferred asset)**.
- Insert the figure as a placeholder marked **TO BE CREATED**, e.g. `[FIG-2.1: Histogram equalization → CLAHE intensity redistribution — ASSET TO BE CREATED]`.
- Log the diagram in the asset-creation queue (it is resolved during Phase 3 §11.2, or earlier if drawn).
- This distinction is consistent with `ASSET_INVENTORY.md §1.3`, which lists Ch 2 and Ch 6 as writable-now despite these missing diagrams ("some diagrams reusable, others to draw"; Ch 6 "only blocker: UML").

This is the **only** relaxation of the hard rule. It applies to non-result diagrams exclusively. Any figure/table tied to an unrun experiment remains a hard block.

---

## 4. CHAPTER 1 — PROBLEM DOMAIN (Phase 1, ✅ writable)

**Chapter function:** establish clinical/epidemiological/technical context; identify the research gap. Tense: present (definitions) + past (cited findings). Chapter target ≈ 10,700 words.

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 1.1.1 | Pathophysiology & Clinical Grading Systems | 1,100–1,300 | OD (5-class grading defn); SIR-2; CFC-2.3 (no deployment outcomes) | #31, #32, #33, #34, #35 | FIG-1.1 ✅ |
| 1.1.2 | Screening in Resource-Limited Settings | 800–1,000 | SB-1.6, SIR-8 (epi. contextual, not results); SIR-4 (#22 self) | #06/#10, #22, #34 | — |
| 1.2.1 | Sources of Image Degradation | 700–900 | OD-1 (image-quality operational def); SIR-1 (lit-GAP → flag candidate analysis) | *(GAP — candidate analysis; no external card)* | — |
| 1.2.2 | Impact of Image Quality on Performance | 900–1,100 | OD-1; DGL-6; CFC-2.1 (no universal); SIR-4 (#24 self) | #05, #15, #17, #24, #78 | — |
| 1.2.3 | Device-Specific Variability | 800–1,000 | NC-16 foreshadow (≠ certification); SIR-3 (camera/dataset context) | #47, #49, #50, #51, #74, #75 | FIG-1.2 ✅ |
| 1.3.1 | CNN Architectures for Medical Imaging | 1,100–1,300 | SB-3.1, NC-6 (no architectural optimality); CFC-2.2 | #01, #04, #05, #08, #09, #12, #15, #16, #18, #37, #38, #41–#43, #65–#70 | FIG-2.2 (reuse) ✅ |
| 1.3.2 | Transfer Learning & SSL in Ophthalmics | 900–1,100 | DGL-6; CFC-2.9/SIR-9 (Gulshan paradigm practice only) | #02, #09, #12, #73 | — |
| 1.3.3 | Explainability Methods | 800–1,000 | NC-14 (Grad-CAM ≠ clinical localization) | #46, #57, #58, #59, #60, #61, #62 | — |
| 1.4 | Critical Analysis of Existing DR Systems | 1,400–1,600 | CFC-2.2, NC-2 (no superiority vs named systems); SB-1.12 (Gulshan not a benchmark); CFC-2.9/SIR-9; SIR-3 | #02, #03, #07, #11, #12, #14, #22, #39, #43, #44, #45, #77 | TAB-1.1 (lit-derived) |
| 1.5 | Formulation of the Research Problem | 700–900 | synthesis; align to CORE_OBJECTIVE; SIR-1 | #17, #39 | — |
| 1.C | Conclusions to Chapter 1 | 400–600 | synthesis; no new claims | — | — |

---

## 5. CHAPTER 2 — THEORETICAL FOUNDATIONS (Phase 1, ✅ writable; 4 deferred diagrams)

**Chapter function:** mathematical/theoretical grounding for Chs 3–4. Tense: present (definitions/derivations). Chapter target ≈ 13,000 words. Note `#25` (Wikipedia-CLAHE) is **not citable** — cite `#54` (Pizer 1987) instead.

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 2.1.1 | Histogram Equalization & Adaptive Contrast | 900–1,100 | SIR-4 (#23 self); #25 not citable→#54 | #26, #27, #30, #23, #54 | ⚠️ FIG-2.1 (deferred) |
| 2.1.2 | Formalization of CLAHE (Dual-Constraint Clip Limit) | 1,300–1,500 | DGL-5 (T/80 portability); SIR-3 (sensitivity-formula anomaly in #23/#24); CFC-2.5; SIR-4/SIR-5 (#23/#24 self+overlap). Eq.1, Eq.2 | #23, #24, #27, #54 | TAB-2.1 ✅ |
| 2.1.3 | Spatial Filtering & Noise Reduction | 600–800 | cite as algorithmic foundations, not DR gains | #55, #56 | — |
| 2.2.1 | Convolution, Pooling, Feature Extraction | 900–1,100 | GLOSSARY (CNN defn) | #08, #65, #66, #67 | FIG-2.2 ✅ |
| 2.2.2 | Loss Functions for Imbalanced Datasets | 900–1,100 | SIR-4/SIR-5 (#19/#21 overlap); SIR-7 (no efficient-CNN-class generalization) | #01, #19, #21, #39, #40, #42 | — |
| 2.2.3 | Regularization Techniques | 700–900 | OD-3 (augmentation operational def); SIR-4/5/7 | #01, #19, #21, #65 | — |
| 2.3.1 | Feature Transferability Across Domains | 700–900 | DGL-6 (transfer not guaranteed) | #04, #71, #72, #73 | — |
| 2.3.2 | Frozen-Layer vs Progressive Fine-Tuning | 700–900 | GLOSSARY (canonical fine-tuning terms); SIR-4/5 | #19, #21, #71, #72, #76 | — |
| 2.3.3 | In-Domain SSL for Retinal Imaging (NEW) | 800–1,000 | DGL-6; CFC-2.8 (composite IV); SIR-2/3/5 | #84 RETFound, #85 MICLe, #86–#91 SSL methods, #90 MAE, #92+#73 surveys | ✅ APPROVED 2026-06-16 |
| 2.4.1 | Coupled Thermal-Optical Model | 1,100–1,300 | SB-1.5, SIR-6, CFC-2.4 (simulation only, not clinical validation); SIR-4 (#20 self). Eq.1–8 | #20 *(self, THIN)* | ⚠️ FIG-2.4 (deferred) |
| 2.5.1 | CAM / Grad-CAM Formalization | 900–1,100 | NC-14. Grad-CAM eq. | #46, #57, #58 | ⚠️ FIG-2.3 (deferred) |
| 2.5.2 | Attention Map Interpretation | 600–800 | NC-14 | #46, #57, #58 | — |
| 2.5.3 | ALO (primary) & IoU (secondary) | 700–900 | define ALO primary / IoU secondary; frame IoU as borrowed overlap metric | #63, #64 | — |
| 2.6 | Image Quality Metrics (CNR/VVI/Entropy/SSIM) | 900–1,100 | SIR-1 (THIN; general refs, not DR-specific) | #52, #53 | ⚠️ FIG-2.5 (deferred); TAB-3.3 (defn) |
| 2.C | Conclusions to Chapter 2 | 400–600 | distinguish experimentally-grounded (§2.1–2.3,2.5–2.6) vs theoretical (§2.4) | — | — |

---

## 6. CHAPTER 3 — METHODOLOGY (Phase 1, ✅ fully unblocked)

**Chapter function:** specify all methodological decisions; make the framework reproducible. Tense: present. Chapter target ≈ 12,000 words. Every asset here is real and on disk (`ASSET_INVENTORY.md §2.3`).

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 3.1.1 | 8-Stage Pipeline Specification | 1,800–2,200 | OD defs; SIR-4/5 (self); model = preprocessing + CNN (CENTRAL_THESIS) | #19, #21, #23, #24, #02, #15, #26, #27, #53, #78 | FIG-3.1, FIG-3.2…FIG-3.9, FIG-3.10, FIG-3.14, RES-NORM, RES-VAL ✅ |
| 3.1.2 | Upgraded CLAHE (Dual-Constraint) | 900–1,100 | DGL-5; SIR-3 | #23, #24 | FIG-3.7 ✅ |
| 3.1.3 | Augmentation Strategy | 800–1,000 | OD-3; SC-1.4 (class dist.) | #19 (LC-CONF) | FIG-3.8, RES-PCA ✅ |
| 3.1.4 | External Image Ingestion Protocol | 700–900 | NC-15 (bound to Kazakh data); SIR-1 (candidate contribution) | *(GAP — candidate methodological contribution)* | — |
| 3.2.1 | ResNet-50 & EfficientNet-B3 | 900–1,100 | SB-3.1, NC-6, DGL-6 | #66, #68, #24, #09, #69, #70 | FIG-3.11, FIG-3.14 ✅ |
| 3.2.2 | Historical v1.0 Architectures (reference) | 500–700 | OD-2 (low/high-complexity reference); SIR-4 (#19) | #19 | — |
| 3.3.1 | Architecture Adaptation (5-class) | 600–800 | DGL-6; EH-4 (replication ≥ 2 architectures) | #19, #21, #23 | — |
| 3.3.2 | Ophthalmology-Specific SSL Pretraining (NEW) | 900–1,100 | DGL-6 (integrated arm = ophthalmology-SSL); CFC-2.8 (composite IV); SIR-1 (GAP) | #73 *(GAP — acquire SSL primary sources)* | — |
| 3.3.3 | Two-Stage Fine-Tuning Protocol | 600–800 | SIR-4/5; H-3 dropped (training method only) | #19, #21 | — |
| 3.3.4 | Weighted Loss Function Formulation | 600–800 | SC-1.4 (imbalance) | #21, #40 | FIG-3.12 ✅ |
| 3.4.1 | Multi-Metric Assessment Framework | 1,100–1,300 | EH-1, EH-2, OD-4, OD-5 | #21, #40, #52, #64 | TAB-3.2, TAB-3.3 ✅ |
| 3.4.2 | Cross-Validation & Statistical Reliability | 900–1,100 | EH-3, EH-4; multiple-comparison correction | #21 | FIG-3.13, TAB-3.1 ✅ |
| 3.C | Conclusions to Chapter 3 | 400–600 | confirm reproducibility conditions | — | — |

---

## 7. CHAPTER 6 — SYSTEM ARCHITECTURE (Phase 1, ✅ writable; design-only; 1 deferred UML asset)

**Chapter function:** translate (eventual) validated results into a design specification. **Epistemic status of entire chapter: design specification only — no prototype, no field test (SB-4.1).** Tense: present. Chapter target ≈ 7,200 words.

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 6.1.1 | Functional & Non-Functional Requirements | 800–1,000 | OD-6 (resource-limited def); SB-4.1; SIR-4 (#22 self) | #22 | — |
| 6.1.2 | Modular Architecture (PACS/EHR Integration) | 1,100–1,300 | SB-4.1; SC-5.1 (UML); SIR-4 (#22) | #22, #36 | DIA-6.1 ✅; ⚠️ DIA-6.3 (UML, deferred) |
| 6.2.1 | Preprocessing Engine (Configurable) | 800–1,000 | link to PC-1 (validated pipeline = module core); SB-4.1 | #22 | DIA-6.2 / reuse FIG-3.1 ✅ |
| 6.2.2 | Inference Module / Model Selection | 700–900 | **design-only — must NOT cite Exp-6 numbers**; SB-4.1; DGL-2 | #22 | FIG-6.1 ✅ |
| 6.3.1 | Telemedicine & Portable Support (6.3.1.1–.3) | 1,100–1,300 | SB-4.1, SB-4.3 (no field testing); SIR-8 (no projected outcomes as findings) | #22, #34, #44, #45, #11, #03, #14 | FIG-6.1 ✅ |
| 6.3.2 | Physician-in-the-Loop Interface | 600–800 | SB-1.3 (decision-support, not standalone) | #22, #34 | — |
| 6.4.1 | GDPR/HIPAA-Aligned Data Management | 600–800 | SB-4.2, NC-9 (design spec, not certified) | *(candidate design spec)* | — |
| 6.4.2 | Applicability to Kazakhstan Infrastructure | 600–800 | SB-4.3; SIR-8 | #22 | — |
| 6.C | Conclusions to Chapter 6 | 400–600 | reaffirm design-only status (SB-4.1) | — | — |

---

## 8. CHAPTER 4 — §4.1 DATASETS & CONFIGURATION (Phase 1, ✅ writable)

**Chapter function (this part only):** specify datasets, partitioning, hardware. Tense: present/past. Target ≈ 2,900 words. (The experiment sections §4.2–§4.8 are Phase 2 — see §9.)

| § | Title | Words | Governance bindings | Lit cards | Resource IDs |
|---|-------|-------|---------------------|-----------|--------------|
| 4.1.1 | Dataset Architecture | 1,100–1,300 | SIR-3 (dataset/taxonomy context); DGL-1 | #06/#10, #15, #47, #48, #49, #50, #51, #19, #21, #24, #41 | TAB-4.1, FIG-4.2, FIG-4.3 ✅ |
| 4.1.2 | Class Distribution & Data Partitioning | 900–1,100 | SC-1.4 (imbalance → weighted F1/κ); label harmonization | #06/#10, #24 | FIG-4.1 ✅ |
| 4.1.3 | Hardware & Reproducibility Protocol | 600–800 | DGL-2 (hardware-specific); fixed seeds/versioned code | #21 | TAB-3.1 ✅ |

---

## 9. CHAPTER 4 §4.2–§4.8, CHAPTER 5, CHAPTER 0, CHAPTER 7, APPENDICES (Phase 2, ⛔ blocked)

> These tables document the *intended* spec so a brief can be generated the moment the gating experiment completes. Each row's **Unblock** column repeats the missing Resource ID(s); until they flip `❌→✅` in the inventory, the section stays ⛔ and is skipped (§3.1).

### 9.1 Chapter 4 — Experiments (results)

| § | Title | Words | Governance bindings | Lit cards | Unblock (missing IDs) |
|---|-------|-------|---------------------|-----------|------------------------|
| 4.2.1 | Factorial Design (A–D) | 800–1,000 | EH-3; CFC-2.8 (composite IV) | #19, #21, #24 | *design-writable*; grouped under Exp 1 |
| 4.2.2 | Training Dynamics & Convergence | 900–1,100 | EH-3; calibration (ECE/Brier) | #19, #21, #24 | RES-EXP1(full), FIG-4.5(full), TAB-4.3 |
| 4.2.3 | Quantitative Diagnostic Metrics | 1,100–1,300 | EH-3, EH-4; CFC-2.8; CFC-2.1/2.2; VCR-3 (report falsification) | #19, #21, #24 | TAB-4.2, FIG-4.4, FIG-4.6, FIG-4.7, FIG-4.8 |
| 4.3.1 | Ablation Design (Levels 0–6) | 900–1,100 | NC-17 (≠ universally optimal); PC-8 | #27, #23 | TAB-4.4 |
| 4.3.2 | CLAHE Threshold Sensitivity (H-2) | 800–1,000 | H-2; DGL-5; CFC-1.2 (no extrapolation); VCR-3; SIR-3 | #27, #23 | FIG-4.9 |
| 4.3.3 | Feature Preservation + σ Sweep + IQ | 800–1,000 | DGL-5; SIR-3 | #27, #23 | FIG-4.10, TAB-4.5 |
| **4.4.1** | **H-3 Measurement Protocol (MMD / KL)** | 500–700 | H-3; DGL-1; SIR-1 (candidate-original analysis) | *(GAP — methodological)* | TAB-4.11; ⚠️ NEW-2 (kernel/n/bootstrap unrecorded) |
| **4.4.2** | **H-3 Distance Reduction Results** | 800–1,000 | H-3; CFC-2.1 (no universality); NC-16 | #74, #75, #76, #78 | TAB-4.11, FIG-4.17 |
| 4.5.1 | Zero-Shot Transfer to APTOS (H-4) | 700–900 | OD-4 (G ratio); DGL-1; H-4 (G ≥ 0.85) | #02, #04, #05, #07, #11, #12, #16, #17, #38, #44, #48 | TAB-4.6 |
| 4.5.2 | Baseline vs Pipeline Comparison | 600–800 | OD-4; CFC-2.8 | (same as 4.5.1) | FIG-4.11 |
| 4.6.1 | Grad-CAM Generation Protocol | 700–900 | NC-14 | #06/#10, #46, #57, #58 | FIG-4.12 |
| 4.6.2 | ALO (primary) & IoU (secondary) | 900–1,100 | H-5 (ALO primary); NC-14 | #06/#10, #46, #63, #64 | TAB-4.7, FIG-4.14 |
| 4.6.3 | Attention Consistency Across Datasets | 600–800 | NC-14; SB-2.2 (clinical overlays absent — G-3) | #46, #57, #58 | FIG-4.13 |
| 4.7 | Exp 5 — External Clinical Performance (H-7 v7.0.0) | 1,000–1,300 | H-7 form S (MCID 0.050, CI⁻ > 0, both sets); OD-4; DGL-1; DeLong; Δ_drop descriptive only | #06/#10, #17, #44, #48, #78 | TAB-4.8, FIG-4.15 |
| 4.8 | Exp 6 — Device Domain Shift (H-6) | 1,000–1,300 | H-6; NC-16 (≠ certification); DGL-1 | #38, #49, #50, #51, #74, #75, #76, #78 | TAB-4.9, App F set |
| 4.9 | Exp 7 — Small Data Training | 900–1,100 | DGL-1; SIR-1 (THIN) | #06/#10 | TAB-4.10, FIG-4.16 |
| 4.C | Conclusions to Chapter 4 | 700–900 | state H-1,H-2,H-3,H-4,H-5,H-6,H-7 outcomes; VCR-3 | — | all of §4.2–§4.9 |

### 9.2 Chapter 5 — Reliability Validation

| § | Title | Words | Governance bindings | Lit cards | Unblock (missing IDs) |
|---|-------|-------|---------------------|-----------|------------------------|
| 5.1 | Explainability Results | 1,000–1,300 | NC-14; H-5 | #06/#10, #16, #17, #27, #46, #24, #57, #58 | FIG-5.1, TAB-4.7, FIG-4.12 |
| 5.2.1 | Bootstrap CI & Mixed-Effects Model | 900–1,100 | EH-3, EH-4; multiple-comparison correction | #16, #17, #27, #52, #24 | TAB-5.1 |
| 5.2.2 | Final Claim-Strength Classifications | 900–1,100 | ARGUMENT_MAP §VI (STRONG/MODERATE/CONDITIONAL); EH-4 | #16, #17, #27, #24 | TAB-5.2, FIG-5.3 |
| 5.3.1 | Benchmarking vs Published Systems | 900–1,100 | CFC-2.2, NC-2 (contextual only); SB-1.12; SIR-3 | #02, #05, #07, #11, #12, #14, #23, #44, #45 | TAB-5.3, TAB-5.4 |
| 5.3.2 | Performance–Complexity Trade-Off | 700–900 | DGL-2 (hardware-specific); SIR-7 | #23 | FIG-5.2, FIG-5.4 |
| 5.4 | Limitations & Boundary Conditions | 1,000–1,300 | full SB-1…SB-4, DGL-1…DGL-6, NC-1…NC-17 enumeration | — | final H-1…H-7 outcomes (§4.C, §5.2.2) |
| 5.C | Conclusions to Chapter 5 | 600–800 | final claim strengths; VCR-3 | — | TAB-5.2 |

### 9.3 Chapter 0 — Introduction & Front Matter

> Per task phasing, Ch 0 is Phase 2 (final framing depends on results). Items marked 🟨 below are *content-writable now* and may be pulled forward at the candidate's discretion; **§0.8 is a hard block** (needs final claim strengths). Tense: present.

| § | Title | Words | Governance bindings | Lit cards | Status / Unblock |
|---|-------|-------|---------------------|-----------|------------------|
| 0.FM1 | Normative References | 200–400 | GLOSSARY; format standards | — | 🟨 writable now |
| 0.FM2 | Definitions (OD-1…OD-6 verbatim) | 600–900 | OD-1…OD-6 verbatim | — | 🟨 writable now |
| 0.FM3 | Designations & Abbreviations | 300–500 | GLOSSARY §6 standardization | — | 🟨 writable now |
| 0.1 | Relevance of the Research | 800–1,000 | SB-1.6, SIR-8 (projections not findings) | #01, #33, #35, #14 + LC-NAN_RK(#22) | 🟨 writable now |
| 0.2 | Scientific Novelty | 800–1,000 | SB-1.5/4.1; CFC-2.8; PC-1…PC-9 framing | self #19–#24 | 🟨 writable now |
| 0.3 | Research Goal | 300–500 | CORE_OBJECTIVE | — | 🟨 writable now |
| 0.4 | Research Objectives | 400–600 | maps objectives→chapters | — | 🟨 writable now |
| 0.5 | Object & Subject of Research | 200–400 | — | — | 🟨 writable now |
| 0.6 | Research Hypothesis (H-1…H-7 verbatim) | 600–900 | HYPOTHESIS.md verbatim; EH-3 | — | 🟨 writable now |
| 0.7 | Methodological Basis | 400–600 | EH-1…EH-4 | — | 🟨 writable now |
| 0.8 | Provisions Submitted for Defense | 700–900 | PC-1…PC-9 with final strengths | — | ⛔ blocked-by TAB-5.2 (§5.2.2) |
| 0.9 | Theoretical Significance | 300–500 | SB-1.5 (laser model theoretical) | #20, #23 | 🟨 writable now |
| 0.10 | Practical Significance | 300–500 | SB-1.3, SB-4.1; SIR-8 | #22 | 🟨 writable now |
| 0.11 | Approbation of Research Results | 200–300 | SIR-4 | — | ✅ writable now (App D) |
| 0.12 | Publications | 200–300 | SIR-4, SIR-5 | #19–#24 | ✅ writable now |

### 9.4 Chapter 7 — Conclusion

| § | Title | Words | Governance bindings | Lit cards | Unblock |
|---|-------|-------|---------------------|-----------|---------|
| 7 | Conclusion | 1,500–2,000 | restate IT-1 (Central Thesis); H-1…H-7 verdicts (VCR-3); PC-1…PC-9 final strengths; NC-1…NC-17; future work | — | all of Ch 4 + §5.2.2 (TAB-5.2) |

### 9.5 Appendices

| ID | Title | Governance bindings | Status / Unblock |
|----|-------|---------------------|------------------|
| App A | Source Code of the Preprocessing Pipeline | APP-A ✅ | ✅ writable now |
| App B | Confusion Matrices & Training Curves | — | ⛔ blocked-by FIG-4.6, FIG-4.5(full), TAB-4.3 (Exp 1–7) |
| App C | System Architecture UML Diagrams | SC-5.1 | ⛔ blocked-by DIA-6.3 (asset creation, not experiment-gated — §3.2) |
| App D | Certificates & Publication Confirmations | APP-D ✅; SIR-4 | ✅ writable now |
| App E | Grad-CAM Visualization Gallery | NC-14 | ⛔ blocked-by FIG-5.1, FIG-4.12 (Exp 4) |
| App F | Device Domain-Shift Supplementary Tables | NC-16 | ⛔ blocked-by TAB-4.9 + per-camera matrices (Exp 6) |

---

## 10. AUTONOMOUS PER-SECTION EXECUTION LOOP

For **each writable section, in the Phase-1 narrative order** (then Phase-2 order as gates open), run steps **a → f**. Do not skip a step; do not batch across sections.

**Pre-step (gate check):** Confirm against `ASSET_INVENTORY.md §2` that no result-dependent resource the section requires is `❌ MISSING`. If one is, **STOP** — leave the section ⛔ and move to the next writable section (§3.1). Deferred conceptual/UML diagrams (§3.2) do not stop the loop.

**a. Section Brief.** Generate the brief from `prompts/section-brief-template.md` v6.0.0. Fill *all* fields, in particular: **Argumentative Spine** (thesis / reasoning chain / hand-off), **Acceptance Criteria**, **Paradigm positioning** (P1/P2, permitted vs forbidden Gulshan phrasings per CFC-2.9/SIR-9), plus the governance bindings, lit-card source mapping, and required Resource IDs from this plan's section row.
→ Save to `thesis/chapters/<NN-chapter>/briefs/<§x.x.x>-brief.md`. Set tracker to **🟦**.

**b. Self-review the brief.** Check the brief against governance (INVARIANTS v6.0.0 + the bindings listed for the section). Flag any **coverage gap** (a required content element with no mapped literature card → mark for `[UNSOURCED CLAIM]` handling or candidate-original analysis; note lit-THIN/GAP sections from the Coverage Matrix). Resolve or explicitly accept each gap before drafting.

**c. Draft.** Generate the section using `prompts/writing-session-system-prompt.md` v6.0.0 (load: system prompt → INVARIANTS.md → the Brief → relevant literature cards → preceding Continuity Note). Output PART 1 (prose + tables in Markdown), PART 2 (Continuity Note), PART 3 (compliance checklist).
- **Figures:** reference by Resource ID with a caption and the **real file path from `ASSET_INVENTORY.md`**. **Do NOT embed images.** Insert a placeholder the later `.docx` step can resolve, e.g.
  `[FIG-3.6: Stage 4 — Adaptive flat-field correction — defense/presentation/assets/preprocessing/15_flatfield/stage4_flatfield.png]`
  For a deferred conceptual/UML diagram, use `… — ASSET TO BE CREATED` (§3.2).
- **Tables** that are `✅ AVAILABLE` as governance text (TAB-2.1, TAB-3.1/3.2/3.3, TAB-4.1) are rendered inline as Markdown.

**d. Verify.** Run `prompts/verification-protocol.md` v6.0.0 against the draft + brief + INVARIANTS (sections A–H: claim compliance, forbidden-content scan CFC-2.1…2.9, terminology, source handling SIR-1…9, structural integrity, scope/paradigm, evidence thresholds). Verdict: **APPROVED** or **REVISION NEEDED**. If revision needed → run `prompts/revision-session-template.md`, re-verify. Only APPROVED advances.

**e. Continuity note.** Confirm PART 2 is complete and accurate (key concepts, terms introduced, argument thread, final topic, setup for next section, unresolved threads).
→ Save to `thesis/chapters/<NN-chapter>/continuity/<§x.x.x>-continuity.md`.

**f. Save draft.** Save the approved PART 1 to `thesis/chapters/<NN-chapter>/drafts/<§x.x.x>-draft.md` (and the verification record to `reviews/`, session transcript to `sessions/`). Set tracker to **🟩** on save, **✅** once verification is APPROVED.

> Carry the saved Continuity Note into step **c** of the *next* section so its opening paragraph connects to the prior argument thread.

---

## 11. COMPLETION WORK — the live task board

The gate condition ("run only after every section verifies") **is met**: all 98 sections are approved.
Everything below is what stands between the approved text and a council-ready pair of documents.

**Critical path (2026-08-12): §11.4, the EN + KZ GOST re-export.** Phase 4 is closed and §11.2/§11.3 are
done, so the conversion is the only large item left. `defense/docs/` still holds nothing but the June
builds of the 53-section manuscript, so **there is currently no council-ready file for the current text
in either language**. Two conditions bind that conversion and are set out in full in §11.4: the **four
Mermaid fences in Appendix C must render**, and the **four §0.16 count placeholders are fillable only
after the conversion produces a paginated document — so §0.16 closes last, in both languages**. The
**trim queue (§11.3b)** runs in parallel but must finish *before* the final conversion pass, since a
trim moves pagination.

### §11.1 Concatenate — ✅ DONE

`python thesis/assembly/_assemble_en.py` in **TOC order**, not `MASTER_OUTLINE` order — the two differ for
Chapter 0 and the TOC is authoritative for the manuscript. Emits front matter → Ch 0 → Ch 1 → … → Ch 7 →
Appendices A–F. **One structural gap remains: `_assemble_kz.py` omits the front matter** (§11.0b).

### §11.2 Assets — four defects, not ninety

Of 90 placeholders carrying 80 distinct paths, **76 resolve to files that exist**. These four do not:

| ID | Defect | Status |
|---|---|---|
| FIG-1.1 | Placeholder pointed at `fig1_1_dr_grades_eyepacs.png` — **no such file**; on disk is `fig1_1_dr_grades_idrid.png` | ✅ **FIXED 2026-08-12.** The corpus question was settled by evidence, not preference: `figures_mine/README.md` records a deliberate decision that dataset-illustration figures are rebuilt from IDRiD, and **the plate carries "(IDRiD)" in its own rendered title** — so the EyePACS caption contradicted the image a reader would be looking at. Path *and* caption corrected to IDRiD in the EN draft and the KZ translation, plus "illustration only, carrying no measurement" (SIR-2). |
| DIA-6.3 | **Discharged by Appendix C**, but §6.1.2 still called it "a deferred conceptual asset" | ✅ **FIXED 2026-08-12.** Not merely re-pointed: §6.1.2 promised *component, sequence, class, activity and ER* diagrams, while Appendix C delivers *component, deployment, sequence and data* views. Repointing alone would have left the text promising three diagram kinds that do not exist. The sentence now names the four views actually supplied and carries the SB-4.1 design-specification framing. Draft header and compliance checklist updated to match. |
| FIG-3.8 | Render depicted the **superseded PCA colour augmentation**, and also listed a *"horizontal re-flip"* step the implementation does not perform — the figure contradicted its section twice | ✅ **FIXED 2026-08-12.** The source diagram had already been re-specified; only the six PNG copies lagged. Re-rendered by `defense/presentation/scripts/render_stage6_card.py`, which writes every copy from one source so they cannot drift apart again. **A layout defect was fixed in the same pass**: the re-specification added a fourth PARAMETERS line at the y the fixed panel grid reserves for OUTPUT, so the two would have overlapped; the full sheet was re-rendered too. Every parameter now matches `config.py` verbatim (rotation σ fallback **13.0°**, per the divergence register — not 15.0°). |
| FIG-4.17 | `ASSET TO BE CREATED` — H-3 domain-distance reduction chart | ✅ **RENDERED 2026-08-12** — the manuscript's last outstanding asset. `defense/figures/figures_mine/_make_fig4_17.py` **parses** `results/tables/H-3_domain_distance.md` instead of transcribing it, so the figure cannot drift from the table above it. Three panels, one per claim the section makes; caption carries the model-dependence caveat and KL's secondary status. **Deliberately not drawn:** any pairing of Δd with transfer gain — ρ ≈ 0.49, and a scatter would invite the magnitude reading §4.4.2 forecloses. |
| *(found in the same pass)* | **Two FIG-3.8 placeholders contained a literal ellipsis** in their path (`19_aug_rotation/…/stage6_augmentation.png`) and so resolved to no file at all — in §3.1.1 and §3.1.3, English and Kazakh alike | ✅ **FIXED 2026-08-12.** All four now name one real file. |

Also at this step: the **four count placeholders in §0.16** (`TO BE RESOLVED AT FINAL ASSEMBLY` — pages,
tables, figures, references) can only be filled after §11.4 produces a paginated document, so §0.16 closes
last. And **§0.16 carries its own Phase-3 obligation block** — read it before touching the section.

**Flags:** three `[VERIFY]` markers to clear (MMD kernel/bandwidth, per-domain sample size, OD-3 Stage 5
vs the shipped polar-CLAHE default). The two `[UNSOURCED CLAIM]` markers (§3.1.4 ingestion, §3.3.2 SSL)
are **deliberate candidate methodological positions and are kept** — do not "fix" them.

### §11.3 Citations — ✅ DONE

Outputs: `DISSERTATION_EN_GOST_2026-08-12.md`, `DISSERTATION_KZ_GOST_2026-08-12.md`,
`_citation_resolution_final_2026-08-12.md`. Re-runnable end to end with
`python thesis/assembly/_finalize_citations.py`.

**Result: 107 sources, numbered once by first appearance in EN and reused verbatim in KZ.**
EN 292 bracketed citations, KZ 230; 107 reference entries per language; no `[card not found]`;
BLOCKING 0, residual self-citations 0, UNKNOWN 1 (the §0.15 legal-act number — correctly not a citation).

**Five defects were found and fixed in the process, three of which would have shipped a wrong book:**

1. **The script was pinned to the June source files.** It hard-coded
   `DISSERTATION_EN_partial_2026-06-17.md`, so re-running it would have silently reconverted the stale
   53-section manuscript and reported success. It now resolves the newest assembly at run time.
2. **The Introduction was excluded from the citation body.** `split_body()` took the body to start at
   `^# 1 `, which was right only while Chapter 0 was unwritten. With Chapter 0 assembled ahead of
   Chapter 1, every Introduction citation would have been left unconverted *and* excluded from the
   numbering — which also shifts every subsequent number. Body start is now the Introduction where one
   exists, with Chapter 1 as the fallback (KZ still has no Chapter 0).
3. **The self-citation bibliography was broken.** Three of the six self cards carried
   `[NO APA LINE]` in `_card_bib.tsv` and `yesmukhamedov-nan-rk.md` carried an entry for a *different*
   paper entirely (Pallavi et al., 2022 — an extraction artefact). All six rows rewritten from the cards'
   own bibliographic records.
4. **The "irreducibly manual" self-citation step was not actually ambiguous** — the ambiguity was an
   artefact of matching on first author alone. Every occurrence resolves on evidence: `Yesmukhamedov et
   al., 2025` carries page locators 74–90, all inside the NAS RK span 74–91 and no other self-work's;
   `Sapakova, Yesmukhamedov & Sapakov, 2025` is cited in §2.1.2 for two equations the EEJET card records
   verbatim; the remaining three appear with full author lists. The five works are now numbered like any
   other source, as GOST requires, with the two Scopus cards taking **one** number per §0.12's
   "five distinct works, not six". The SIR-4 prose framing is untouched — it lives in the sentence, not
   the bracket.
5. **§2.1.2 cited pages that do not exist in the cited article** — see the box below.

> **⚠ CARRY-FORWARD — verify against the published PDF.** §2.1.2's four locators into the candidate's
> Scopus article read p. 5 (×3) and p. 9 (×1). Those are the literature card's *internal PDF* pages; the
> article is published at **EEJET 4(9(136)), pp. 79–88**, so a reader checking either locator would find
> nothing. The card's internal pages run 1–10 against exactly ten journal pages, fixing the offset at 78,
> so p. 5 → **p. 83** and p. 9 → **p. 87**. Remapped in the EN draft and the KZ translation, and recorded
> in the §2.1.2 compliance checklist. The arithmetic is forced *if* the PDF has no cover page —
> **the candidate should confirm before submission.** No claim, quotation or equation was changed.

### §11.3b Trim queue — ⬜ OPEN

Sections at or over their word band: §0.1, §0.2, §0.3, §0.4, §0.6, §0.8, §1.2.2
(~1,130), §1.3.1 (~1,325), §1.4 (~1,585), §2.2.3 (~915). **Excluded from the trim in every case:** §0.6's
four mandatory disclosures, §0.8's qualifications, and the §0.3 goal sentence (quoted verbatim in the
abstract and defence materials).

### §11.4 Convert and re-export — 🟩 IN PROGRESS, **THE CRITICAL PATH**

**Both manuscript editions now convert cleanly (2026-08-12).** `defense/docs/DISSERTATION_{EN,KZ}_GOST_2026-08-12.docx`
are built from the current 98-section text, ~18.7 MB each. **Condition 1 is met**: Appendix C's four
Mermaid views render as embedded images in both languages, verified on the appendix alone before the
full build, and a diagram that fails to render now exits non-zero instead of shipping as source. Still
open below: the front-matter bundle, `FULL_DISSERTATION_*`, the PDFs, FIG-5.1, and the §0.16 fill.

**Pagination (first real measurement).** EN **272 pages total, body 220** (appendices from p. 221);
KZ **301 total, body 247** (appendices from p. 248). Against the council rule — PhD *as a rule* up to
300 pages, **appendices not counted** — both editions clear the limit with room, which is what makes
§11.3b optional rather than binding. Tables **66**, figures/diagrams **92**, references **107**;
the page figure for §0.16 is not final until the front matter is prepended.

**Five defects were found and fixed in this pass, four of which would have shipped a wrong book:**

1. **The four Mermaid fences did not render at all** — `md2gost.py` had no Mermaid handling, so all
   four views would have set as Consolas source and Appendix C would have failed to discharge DIA-6.3.
2. **Appendix C's sequence view did not parse.** Two message labels contained a semicolon, which
   Mermaid reads as a statement separator. Written as `#59;` so the rendered text is unchanged.
3. **Sixty asset markers shipped as raw bracket text with their file paths showing** — the marker
   regex matched digit-numbered ids only, so **all 54 Appendix-E plates** and the **6 Appendix-D
   confirmations** printed as literal `[FIG-E.1: … .png]` lines, and Appendix E reproduced nothing.
   Markers inside list items and backticks were not resolved either.
4. **`build_full_dissertation.py` cut the body at `^# 1 `** and would have dropped all sixteen §0.x
   sections, §0.16 included — the same defect as citation defect #2. Both it and
   `build_frontmatter_bundle.py` also pinned `--date` to the June build; both now resolve the newest.
5. **The document weighed 86 MB** because the Appendix-E plates embed at 455 dpi. Images are now
   downscaled to 300 dpi at their placed width; ~18.7 MB per edition.

**Diagram legibility (decided).** C.1 and C.2 were re-laid out — direction only, no node, edge or
label touched — because as authored they fell on the page as a 165 × 28 mm ribbon and a 58 × 215 mm
column with ~4 pt labels. C.1 is now `flowchart TB` (142 × 215 mm) and C.2 `flowchart LR`
(165 × 86 mm), both ~8–9 pt. C.4 stays a full-page ER model with small labels by decision; its
content is carried in the prose of §C.4.

**Front matter and the full build are done, and §0.16 is closed.** `FRONT_MATTER_{EN,KZ}` and
`FULL_DISSERTATION_{EN,KZ}_GOST_2026-08-12` are built from the current text. **EN 281 pages, KZ 311**,
front matter 10 and 11 pages respectively. §0.16's four counts are filled and **verified against the
rebuilt document**: the counts are of the dissertation *excluding the appendices*, which is the volume
the council rule measures — **239 pages EN / 266 KZ, 42 tables, 30 figures, 107 sources**. Filling the
placeholders shortened the Kazakh text by one page, so the first fill drifted −1 and was corrected; both
editions now state a figure that matches their own pagination exactly.

**Three further defects were found and fixed while building the front matter:**

6. **The reference list sat after the appendices** in every build so far. GOST 7.32-2001 orders it after
   the conclusion and before them; `_finalize_citations.py` appended it to the end of the assembled text.
7. **The CONTENTS was a chapter behind the manuscript.** H-3's reinstatement as §4.4 pushed Experiments
   3–7 down to §4.5–§4.9, but the outline still numbered them 4.4–4.8, so six Chapter-4 entries named the
   wrong section, §4.9 was absent, and §4.6.1–4.6.3 were missing. Titles were reconciled to the
   manuscript throughout — 8 in English, 43 in Kazakh — and the Kazakh appendix letters were corrected
   from the Russian sequence (А Б В Г Д Е) to the Kazakh one the manuscript uses (А Ә Б Д Е Ж).
8. **Twelve contents entries had no page number.** `build_toc.py` looked for chapter conclusions under a
   `§N.C` key that only Chapters 1–3 and 6 carry, matched appendix headings by a prefix no heading has,
   and could not see a Kazakh appendix heading at all because it leads with its letter. All now resolve;
   the only dashes left are the three front-matter sections, which take their pages in the full build.

**FIG-5.1 is closed — resolved against the council's own samples.** The marker pointed at a directory
and named a *representative* selection from the 54-plate set; choosing which overlays a reader sees is
the selection SIR-1 guards against, while Appendix E already reproduces the complete set with none.
`Инструкция_по_оформлению_диссертации` requires only that every illustration be referenced, and the
accepted dissertations in `D:\dissertation_council` put a full gallery in a lettered appendix —
Myrzakerimova carries Figure C.2–C.13 there and duplicates no subset in the body. The sentence after
the marker already read "The overlay gallery, presented in full in Appendix E, is an illustration and
carries no measurement", so the marker was removed and that sentence carries the reference. **Every
figure in both editions now resolves to a real image: `asset to be created` is zero.**

The same instruction confirmed two choices made earlier in this pass: appendix illustrations are
numbered with the appendix letter (its own example is "Рисунок А3"; Tokhtakhunov ships "Figure B.1"),
which is what the converter now emits, and captions sit **below** the figure, which is where it puts
them. Chapter-scoped numbering in the body is explicitly permitted (§5, "в пределах раздела").

**Diagram captions are uniform (2026-08-13).** Appendix C authored its four captions as bold lines
*above* the Mermaid source; the converter now moves each below its rendered diagram and sets it in the
same centred `Label N – Title` form as every other caption, which is where the instruction puts one
("Слово «Рисунок» и его наименование помещают после пояснительных данных"). The Kazakh postfix form is
normalised to label-first at the same time — `Б.1-диаграмма` → `Диаграмма Б.1` — because the
instruction's own example leads with the word and the marker-driven captions already did, so the two
forms would otherwise stand side by side in one document. All six diagram captions in each language now
sit directly under their image; none of the old form remains. **The appendix source is unchanged** — the
relocation happens at conversion, so the Markdown stays readable as authored.

**Resource IDs are out of the text — all 40 occurrences, both editions (2026-08-13).** The mapping was
not the identity and had to be established case by case:

- **Seven tables were captioned by their asset ID** rather than a number (`**TAB-2.1. …**`). They take
  their document numbers from order of appearance, which makes Chapter 3 read `TAB-3.2` → Table 3.1,
  `TAB-3.3` → Table 3.2, `TAB-3.1` → Table 3.3 — and `TAB-3.1` again as **Table 4.2** where §4.1.3
  repeats it. Chapters 1–5 now number 1.1 / 2.1 / 3.1–3.3 / 4.1–4.28 / 5.1–5.6 with no gap or duplicate.
- **Sixteen Chapter-4/5 captions already recorded their own mapping** in parentheses (`Table 4.5
  (TAB-4.3)`), which is where those pairs come from; the parenthetical is dropped.
- **`TAB-5.4` was cited for figures no table in the manuscript carries.** It is the clinical-metrics
  table in `results/`, never rendered here. The sensitivity/specificity pairs it was cited for —
  ≈0.80 at 0.96 in-domain, ≈0.84 at 0.94 zero-shot — are Table 4.10 and Table 4.20 verbatim, so the
  reference now names those two.
- **`DIA-6.3` and its a–d suffixes** are governance IDs, not numbered items; dropped from the four
  Appendix-C captions, and the sentence that introduced the ID now names the reserved diagram in words.
- Figure and `DIA-6.1` references map to themselves (`FIG-2.2` → Figure 2.2). Kazakh in-text references
  take the postfix form the translation already uses (`3.2-кестеде`, `2.2-суретте`), which is also what
  the instruction expects — its own rule for in-text references is lower-case and inflected
  («в соответствии с рисунком 2»), distinct from the caption form.

Verified after rebuild: **zero IDs in either edition, no dangling table or figure reference, 26 figures
placed, and §0.16's counts unchanged (42 tables / 29 figures) with both page figures still matching.**
Only PART 1 of each draft was touched, so the compliance checklists keep their ID references.

**Table captions are uniform (2026-08-13).** Both editions carried three forms at once — 60 captions
with a full stop, 4 with an em-dash, and the converter's own label-first en-dash form — and Kazakh added
a fourth by writing the postfix `4.5-кесте`. GOST shows one shape for all of them
("Таблица 1 – Распределение…"), so every caption is normalised to **`Label N – Title`**, Kazakh included
(`4.5-кесте.` → `Кесте 4.5 – …`), and set **flush left with `keep-with-next`** so a caption can no longer
be orphaned at the foot of a page. **66 captions per edition, all canonical**; the only remaining matches
are ordinary sentences that open with a reference ("Table 2.1 contrasts…"), which is the in-text form the
instruction prescribes. As with the diagrams, the normalisation happens at conversion and **no
translation was edited**. Pagination moved +1 and §0.16 was corrected to 240 EN / 266 KZ and re-verified.

**Governance document names are out of the text (2026-08-13).** All 27 were provenance citations to
documents the reader has no access to, always inside a parenthetical: the citation is removed with its
separator, and a parenthetical left empty goes with it — `(RESEARCH_ARCHITECTURE §3.2; OD-3 Stage 5)`
becomes `(OD-3 Stage 5)`, `(60 images, RESEARCH_ARCHITECTURE §2.1.8)` becomes `(60 images)`, and the one
sentence that embedded the citation in prose now reads "the reasoning recorded in the dissertation's
governance". 50 parentheticals across both editions; **zero names, zero empty parentheses, and zero
literal `§X` remain.**

Two things travelled out with them. Three citations pointed at a literal **`§X`** — an unresolved
cross-reference that would have printed as written — and the `INVARIANTS` citations carried a
**`v6.0.0` version marker** that reached the page: the converter's scrubber only recognises V3/V4/V5,
so it passed straight through the containment rule of `VERSIONING_POLICY.md` §6.

The same scan found **two more version markers that survive in prose**, in §2.C and §3.C: "those
sources were acquired in the **v6.1.0** corpus expansion". That is process history as well as a version
marker — the reader is told when the project's literature corpus was extended — so both sentences now
say it without the version ("those sources have since been acquired"). **Both editions now render zero
version markers, zero governance document names and zero resource IDs.**

**The governance codes are declared (2026-08-13).** The choice was **declare, not strip**: all eight
families now carry a row in `DESIGNATIONS AND ABBREVIATIONS`, in both languages, written as `SB-n`,
`OD-n`, `SIR-n`, `PC-n`, `NC-n`, `EH-n`, `DGL-n`, `CFC-n` — the numbered form, which is how they always
appear in the text and which is what separates them from ordinary abbreviations. Each row states what
the family *is* for a reader who has no access to the governance documents (a scope boundary, an
operational definition, a rule on what may be attributed to a source), not where it is recorded.

**The `OD` collision is resolved by adjacency and by wording.** `OD` (Optic Disc) keeps its row and
`OD-n` follows it immediately, closing with the distinguishing rule — the optic disc *is never written
with a number*. A reader meeting `OD-3 Stage 5` now lands on the right row.

**Three further families were found in the same scan and removed instead of declared — 9 occurrences,
EN and KZ alike.** `IT-1` (×4), `SC-1.4` (×3) and `AOQ-2` (×2) were bare provenance parentheticals of
exactly the kind the governance-document-name pass removed: the sentence already carried the content.
`(AOQ-2 simplified)` was also process history — it told the reader an internal amendment question had
been simplified. One needed rewording rather than deletion: §3.3.1's *"the five-class taxonomy of
IT-1"* became *"the dissertation's five-class taxonomy"*. Declaring three more families for nine
provenance markers would have bought the reader nothing. **Only PART 1 of each draft was touched, so
the compliance checklists keep their code references.**

**Rebuilt and verified.** Assembly (98 sections, no suspect extractions, EN 101,437 / KZ 81,277 body
words) → citation pass unchanged (107 sources, EN 292 / KZ 267 brackets, BLOCKING 0) → front matter,
both manuscripts and both `FULL_DISSERTATION` docx + pdf. **Front matter stayed 10 pages EN / 11 KZ,
and §0.16 needed no correction: appendices still begin on p. 240 EN and p. 267 KZ, so the 239 / 266
figures the text states are still exact.** Verified in the built documents themselves: all eight
families present in each edition, zero `IT-`/`SC-`/`AOQ-` codes remaining.

**Still open in this section:**

- `FR-n` and `NFR-n` (118 occurrences) are undeclared in the front matter as well. They differ from the
  governance codes in that §6.1.1 defines each one in its own tables, on the page where it first
  appears, so a reader is never left without the expansion — the candidate may still prefer a row each.
- The abstract was checked against this pass and needs no correction: it already carries the current
  structure — H-3 as a separate investigation, Experiment 5 as external clinical performance, eight
  investigations — and its "Structure and length" section deliberately states no counts, so nothing in
  it went stale. Whether to add the now-known page count there is the candidate's call.

---

Original statement of the task, retained:

**Why it is urgent: `defense/docs/` still holds nothing but the June builds of the 53-section
manuscript.** Both language editions there are superseded by ~45 sections of text that did not exist
when they were made, so at present **there is no council-ready file for the current manuscript in
either language**. Both builds must be re-run — not one — and the front-matter, abstract and TOC
exports re-checked against the final pagination.

Convert each assembled manuscript to a single GOST `.docx` + `.pdf` via `md2gost.py` (which also runs
the `strip_process_metadata` scrubber).

**Two conditions bind this conversion, and neither can be discovered late:**

1. **The four Mermaid fences in Appendix C must render.** The requirement is carried from Appendix C
   itself, which gives its four structural views as Mermaid source and states that rendering to an
   image happens at conversion. If the converter does not handle fenced Mermaid, those views reach the
   reader as code blocks and Appendix C fails to discharge DIA-6.3. The KZ edition inherits this
   verbatim — its Mermaid source is byte-identical to the English by design, so whatever the converter
   does to one it does to the other. **Test this on a single appendix before running the full build.**

2. **The four count placeholders in §0.16 can only be filled after the conversion produces a paginated
   document** — pages, tables, figures and references are not knowable before then, and §0.16 says so
   rather than inventing them. **Therefore §0.16 closes last, in both languages**, and the sequence is:
   convert → read off the four counts → fill §0.16 EN and KZ → re-convert. The placeholders were
   deliberately left in their **English** form in the Kazakh translation as well, so one scan finds all
   eight. §0.16 also carries its own Phase-3 obligation block — read it before editing the section.

Remaining alongside this: **§11.3b, the trim queue.** It is independent of the conversion and can run
in parallel, but any trim changes word counts and therefore pagination, so **finish the trim before the
final conversion pass**, not between the conversion and the §0.16 fill.

### §11.5 Open items to close before defence

- **NEW-1 traceability** — the run's raw artifacts are not in `experiments/outputs/`, so numbers are
  written but not yet traceable to a primary output file. Not a text defect; it is a submission defect.
- **`results/tables/TAB-5.2_claim_strength.md`** still files the domain-distance result outside the formal
  PCs, where `ARGUMENT_MAP.md` v7.1.0 carries it as **PC-11**. Substance and strength agree; only the
  register position differs. §0.8 already submits it as PC-11 — resynchronise the table.
- ~~**`ASSET_INVENTORY.md`** marks App C/E/F as `❌ MISSING`~~ — ✅ **closed 2026-08-12.** APP-B/C/E/F and
  DIA-6.3 rows now record written-and-approved status with their bounds (App E is IDRiD-only per G-3;
  App B/F list their stated absences); FIG-1.1's row records the corpus correction.
- **Missing literature cards** #49 RFMiD / #50 DDR / #51 ODIR-5K, and the DDR full-PDF upgrade — corpus
  hygiene, non-blocking, but they surface in the bibliography pass.

---

## 12. SUMMARY

- **Phase 1 — CLOSED.** 51 sections + App A + App D, all approved.
- **Phase 2 — CLOSED.** All eight investigations ran, all seven hypotheses are supported, Ch 4 / Ch 5 /
  Ch 0 / Ch 7 / App B/C/E/F written from `results/`.
- **English text: 98 sections, 101,575 body words, complete.**
- **Phase 3 (completion) — NEARLY DONE.** Closed: KZ assembler front matter, **all four asset defects
  plus two dead ellipsis paths**, the inventory staleness, and **the whole citation pass (107 sources,
  shared EN/KZ register)**. Still open: the trim queue, the §0.16 counts (which need pagination first),
  and a full re-export in both languages.
- **Phase 4 (KZ translation) — ✅ COMPLETE 2026-08-12, 98 of 98** (81,438 KZ body words). Both
  manuscripts now carry the same 98 sections.
- **The hard honesty rule stays in force** for every remaining edit: no demo-dashboard preview number is
  ever used as a real result, and `results/` remains the single source of truth for every figure that
  reaches the text (CFC-2.x / SIR-1).
- **The eight fences bind every remaining edit, including translation.** Compression and translation are
  exactly where fences get lost, so restate them, never paraphrase them upward: CFC-2.8 (the composite is
  **decomposable, not dissolved**); PC-8 at **grouping resolution only**; H-3 **direction only** (ρ ≈ 0.49);
  H-5 **quantitative half only** (G-3); H-7 **performance, not resistance**, Messidor-2 margin **0.0041**
  with CI⁻ below the MCID; H-4/H-6 thresholds cleared by **both** arms; E-7 **comparable, not larger**;
  two camera groupings **are** the external corpora, so not independent replication.

## THE CRITICAL PATH — §11.4, the EN + KZ GOST re-export

With Phase 4 closed and §11.2/§11.3 done, **the re-export is the critical path and the only large item
left**. Stated once, in full, because it is what the remaining work is:

> **`defense/docs/` still holds nothing but the June builds of the 53-section manuscript.** Roughly 45
> sections of approved text did not exist when those files were made, so **there is currently no
> council-ready file for the current manuscript in either language**.
>
> **Two conditions bind the conversion.** First, **the four Mermaid fences in Appendix C must render** —
> Appendix C supplies its four structural views as Mermaid source and states that rendering happens at
> conversion, so a converter that does not handle fenced Mermaid delivers them as code blocks and
> Appendix C fails to discharge DIA-6.3. The Kazakh Mermaid source is byte-identical by design, so both
> editions succeed or fail together; **test it on one appendix before the full build**. Second, **the
> four §0.16 count placeholders (pages, tables, figures, references) are fillable only after the
> conversion produces a paginated document — so §0.16 closes last, in both languages**: convert → read
> off the counts → fill §0.16 EN and KZ → re-convert. The placeholders were left in English in the
> Kazakh text as well, so one scan finds all eight.
>
> **Plus the trim queue (§11.3b).** It runs in parallel, but a trim moves word counts and therefore
> pagination, so **finish it before the final conversion pass** — not between the conversion and the
> §0.16 fill.

**Next action: §11.3b, then §11.4.**

> **Assembler note (changed 2026-08-12).** `_assemble_kz.py` used to treat a *missing* Chapter-0
> translation as a hard error, so a partially translated Chapter 0 broke the entire KZ build and made
> incremental translation impossible. A missing file is not the dangerous case — a file present but
> **unlisted** is, since it would have to be placed by numeric sort, which is the wrong order for this
> chapter. The check now hard-errors only on unlisted extras, emits the sections that do exist in listed
> order, and prints a `PARTIAL` report naming what is still missing.
