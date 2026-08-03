# CHAPTER_STATUS — status of the dissertation chapters and what each one needs

Source: `thesis/PLAN.md`, `thesis/outline/TABLE_OF_CONTENTS_EN.md`, the chapter READMEs,
`thesis/ASSET_INVENTORY.md`. Workflow for a single section:
`briefs/ → drafts/ → continuity/ → reviews/ → translations/` (the quintet).
State of the data — the **2026-08-03** run.

## What has already been written and approved (Phase 1)

| Chapter | Sections | Status |
|-------|--------|--------|
| Ch 1 Problem Domain | 11/11 | ✅ APPROVED |
| Ch 2 Theoretical Foundations | 14/14 (+§2.C) | ✅ APPROVED |
| Ch 3 Methodology | 13/13 | ✅ APPROVED |
| Ch 6 System Architecture | 9/9 | ✅ APPROVED |
| §4.1 Datasets & Configuration | 4.1.1–4.1.3 | ✅ APPROVED (no metrics — it fixes the data substrate) |
| App A (preprocessing code), App D (certificates) | — | ✅ APPROVED |

The approved chapters **contain no experimental metrics** (they were written before the runs) → they
are unaffected by the change of run.

## What has NOT been written — Phase 2

There are no placeholder files; the sections have not been created yet. They are held in
`thesis/PLAN.md` as `⛔ blocked-by <ID>`.

### Chapter 4 "Experiments" — §4.2–§4.8 + §4.C

| Section | Contents | Required assets | Data ready? |
|--------|--------------|---------------|----------------|
| §4.2 Exp 1 (H-1): 2×2 factorial A–D | §4.2.1 design · §4.2.2 training dynamics · §4.2.3 metric comparison | TAB-4.2, TAB-4.3, FIG-4.4–4.8 | ✅ full layer: `tables/TAB-4.2`, `TAB-4.3`, `exp1_per_class`, `exp1_clinical_indomain`, `exp1_convergence_ci`, `TAB-5.1`, `findings/exp1` |
| §4.3 Exp 2 (H-2): ablation + sweeps | §4.3.1 ablation · §4.3.2 CLAHE · §4.3.3 flat-field σ | TAB-4.4, TAB-4.5, FIG-4.9, FIG-4.10 | ✅ **all three parts closed** (the σ sweep has been run): `TAB-4.4`, `TAB-4.5`, `exp2_clahe_sweep`, `exp2_flatfield_sigma_sweep` |
| §4.4 Exp 3 (H-4): transfer to APTOS | §4.4.1 zero-shot · §4.4.2 baseline vs pipeline | TAB-4.6, FIG-4.11 | ✅ `TAB-4.6`, `per_class_and_confusion`, `findings/exp3` |
| §4.5 Exp 4 (H-5): Grad-CAM | §4.5.1 protocol · §4.5.2 ALO/IoU · §4.5.3 consistency | TAB-4.7, FIG-4.12–4.14 | 🟡 quantitative part ✅ (`TAB-4.7`, `exp4_classification`); **clinical (KZ) overlays NOT produced — G-3** |
| §4.6 Exp 5 (H-7): clinical degradation | — | TAB-4.8, FIG-4.15 | ✅ `TAB-4.8`, `findings/exp5`; ⚠️ requires careful wording (**not supported as written, 0/2**; the Δ_drop critique is the contribution) |
| §4.7 Exp 6 (H-6): device shift | — | TAB-4.9, App F | ✅ `TAB-4.9`, `per_class_and_confusion`; ⚠️ per-group confusion matrices are missing (R3) |
| §4.8 Exp 7: small-data training | — | TAB-4.10, FIG-4.16 | ✅ `TAB-4.10`, `findings/exp7-and-ssl` |
| **§4.x H-3: domain distance** ⭐ | new block — MMD/KL over 6 domains | new table + figure | ✅ the data exist (`tables/H-3_domain_distance.md`, `hypotheses/H-3.md`); **its place in the chapter structure is undecided** — decide whether it is its own section or part of §4.4 |
| §4.C Conclusions to chapter 4 | synthesis of §4.2–§4.8 | all of the above | ✅ `findings/summary-and-dominance.md` |

**Bottom line for ch. 4: the entire chapter is unblocked.** The only substantive limitation is that
§4.5 can be written only in its quantitative part (the clinical overlays require G-3).

⚠️ **Organizational question requiring a decision:** H-3 is a new hypothesis with results that is
absent from the current structure of chapter 4. A decision is needed on where to place it (its own
section §4.x before §4.4, or a subsection of §4.4 as the mechanistic justification of transfer). The
numbering of the subsequent sections and of TAB/FIG depends on this.

### Chapter 5 "Validation"

| Section | Contents | Required | Ready? |
|--------|--------------|--------|---------|
| §5.1 Explainability Results | Grad-CAM results | FIG-5.1, TAB-4.7, FIG-4.12 | 🟡 quantitatively ✅; the IDRiD overlays exist; KZ — G-3 |
| §5.2.1 Bootstrap CIs + mixed effects | statistics on exp1 | TAB-5.1 | ✅ `TAB-5.1` (DeLong, McNemar, Holm, ANOVA, bootstrap) |
| §5.2.2 Final Claim Strength | classification of claim strength | TAB-5.2, FIG-5.3 | ✅ `TAB-5.2`, radar data in `findings/summary-and-dominance` |
| §5.3 Comparison with published systems | IDx-DR, EyeNuk, DeepMind + complexity | TAB-5.3, TAB-5.4, FIG-5.2 | 🟡 `TAB-5.4` ✅, `computational_and_iq` ✅; **TAB-5.3 (literature) — not assembled** |
| §5.4 Limitations | limits of applicability | outcome of H-1…H-7 | ✅ `findings/summary-and-dominance.md`, section "What remains honestly limited" |

### Chapter 7 "Conclusion"

A synthesis of the hypothesis outcomes + contributions + future work. **Unblocked** — all verdicts
are in place. Depends on §0.8 "Statements submitted for defense".

### Introduction (ch. 0) and appendices B/C/E/F

Ch 0 (especially §0.8) rests on the final verdicts and is unblocked. App B (confusion/curves) — the
data exist, the ROC/PR curves require the new run's `predictions.npz` (R2). App E (Grad-CAM gallery) —
the IDRiD overlays exist, KZ ones do not (G-3). App F (device tables) — the data exist, the per-group
confusion matrices are missing (R3). App C (UML) — an asset task, not experiment-gated.

## What changed in the content relative to the previous revision

Formulations that must be **replaced** when writing (they rested on the previous run):

| Previous claim | Current state |
|---|---|
| "The strict H-1 dominance criterion is not met; the F1 gain is within noise" | EH-3 is met on both backbones, ΔF1 +6.5 pp |
| "The pipeline degrades calibration; recalibration is needed before deployment" | Calibration **improves** (ECE ~1.7× lower) |
| "Preprocessing on its own does not improve classification; the exp1 effect is an indivisible composite with the SSL init" | The ablation under a single initialization yields the whole gain (+0.0655); the composite has been decomposed |
| "The baseline transfers to APTOS better than the pipeline" | The pipeline is better: G 0.8976 vs 0.8577 |
| "Attention does not align with lesions; PC-7 REFUTED" | 4/4 types significant, PC-7 STRONG (within the bounds of NC-14) |
| "3 of 5 camera groups fall below the generalization floor; device-specific threshold recalibration is required" | 5/5 groups are above the floor; the spread shrinks by a factor of 2.6 |
| "EfficientNet-B3 gains nothing from continual-SSL (asymmetry)" | Both backbones gain comparably |
| "exp7 is the work's only clean positive" | One of several consistent results; the gain is comparable to EyePACS |
| "Not a single hypothesis is confirmed" | 6 of 7 are confirmed; H-7 is not supported as written (0/2), but absolute external performance is significantly higher on both sets |

## Writing order (recommendation)

1. **Decide where H-3 goes** in the structure of chapter 4 — this affects the numbering of everything else.
2. **Now:** §4.2 (H-1), §4.3 (H-2), §4.4 (H-4), §4.6 (H-7), §4.7 (H-6), §4.8 (exp7), H-3.
3. **§5.2.1 / §5.2.2** — the data are ready.
4. **§4.5 + §5.1** — the quantitative part; finalize after G-3.
5. **At the end:** §4.C, §5.4, §5.3 (needs TAB-5.3 from the literature), ch. 7, ch. 0/§0.8.

⚠️ **Framing mandate (README of ch. 4/5):** configs A/C = paradigm P1 (baseline), B/D = paradigm P2
(integrated); it is **forbidden** to call A/C "Gulshan" or to write "We outperform Gulshan".

⚠️ **Provenance:** until NEW-1 (`GAP_ANALYSIS.md`) is closed, the numbers in the chapters will not be
traceable to `experiments/outputs/`. Writing can proceed, but this must be closed before the defense.
