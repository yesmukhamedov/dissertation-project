# GAP_ANALYSIS — what is assembled, what is missing (dissertation + presentation + demo)

A reconciliation of the requirements of three consumers against what has been assembled in
`results/`. State as of the **2026-08-03** run. The requirements are taken from
`thesis/ASSET_INVENTORY.md` (the list of what is needed is current, the statuses are stale),
`demo/web/src/data.js` and `defense/presentation/slides/*`.

## Short answer

`results/` **fully covers** the results layer of all the experiments: metrics, verdicts, tables and
narrative conclusions for exp1–exp7, SSL and the new H-3 block. Categories A, B and C are closed.

Three things remain, and the first is blocking:

1. 🔴 **Provenance.** The numbers were taken from `VALUES.md`; the raw run artifacts are present
   neither in `experiments/outputs/` nor in `results/data/` (which hold numbers from the previous run).
   → `INTEGRITY_NOTE.md` §1, `HYPOTHESIS_COVERAGE.md` NEW-1.
2. 🔴 **G-3** — qualitative Grad-CAM overlays on the clinical (KZ) dataset (required by the wording of H-5).
3. 🟡 **G-8 remainder** — Stage 3 (FOV mask) is not isolated in the ablation.

⚠️ And separately: the demo/defense are built on a third, even older set of numbers — see
`INTEGRITY_NOTE.md` §2.

## What is ALREADY assembled (✅)

| Quantity | Experiment | Where in results/ |
|----------|-------------|----------------|
| Factorial F1/AUC/κ/Acc (A–D) + EH-3 dominance | exp1 | `tables/TAB-4.2`, `findings/exp1`, `hypotheses/H-1` |
| exp1 per-class F1/precision/recall + confusion matrices | exp1 | `tables/exp1_per_class.md` |
| exp1 calibration ECE/Brier | exp1 | `tables/TAB-4.3_exp1_calibration.md` |
| exp1 in-domain clinical metrics | exp1 | `tables/exp1_clinical_indomain.md` |
| exp1 convergence, loss gap, CV CIs, bootstrap CIs | exp1 | `tables/exp1_convergence_ci.md` |
| Statistical tests: DeLong, McNemar, **Holm**, **mixed-effects ANOVA** | exp1 | `tables/TAB-5.1_statistical.md` |
| Cumulative 8-level ablation + per-fold values | exp2 | `tables/TAB-4.4_exp2_ablation.md` |
| Per-stage image quality (CNR/Entropy/SSIM) across 8 levels | exp2 | `tables/TAB-4.5_exp2_image_quality.md` |
| Two-dimensional CLAHE sweep + F1(DR1)/F1(DR2) grids | exp2 | `tables/exp2_clahe_sweep.md` |
| **Flat-field σ sweep** (new) | exp2 | `tables/exp2_flatfield_sigma_sweep.md` |
| **Domain distance MMD/KL, 6 domains** (new) | H-3 | `tables/H-3_domain_distance.md`, `hypotheses/H-3.md` |
| APTOS transfer + G + per-class + matrices + referable | exp3 | `tables/TAB-4.6`, `per_class_and_confusion`, `findings/exp3` |
| Grad-CAM ALO/IoU + threshold sweep + floor effect | exp4 | `tables/TAB-4.7_exp4_alo_iou.md` |
| B4 arm classification | exp4 | `tables/exp4_classification.md` |
| Clinical degradation Δ + CI + p + Δ_drop | exp5 | `tables/TAB-4.8`, `hypotheses/H-7` |
| Device shift (5 groups) + spread + per-class | exp6 | `tables/TAB-4.9`, `per_class_and_confusion` |
| Small-data IDRiD→Clinical + preregistered | exp7 | `tables/TAB-4.10_exp7_smalldata.md` |
| SSL probe gate (from-scratch + SIP + continual) | SSL | `tables/SSL_continual_gate.md` |
| Referable clinical metrics across three scenarios | 1/3/6 | `tables/TAB-5.4_clinical_referable.md` |
| Claim strength PC-0…PC-10 | all | `tables/TAB-5.2_claim_strength.md` |
| Hypothesis summary + end-to-end mechanism + radar data | all | `findings/summary-and-dominance.md` |
| Computational benchmarks (params/FLOPs/latency/VRAM) | — | `tables/computational_and_iq.md` |

## What is MISSING

### Blocking

| # | Item | How to obtain | What it blocks |
|---|------|--------------|---------------|
| **NEW-1** | Raw artifacts of the 2026-08-03 run in `experiments/outputs/` + update of `results/data/*.json` | publish the run files; then reconcile with `results/tables/` | traceability of the numbers in the chapters; cross-checking; closing G-10 |

### Requires a run / code

| # | Item | Status | Target asset |
|---|------|--------|---------------|
| **G-3** | Grad-CAM overlays on the clinical (KZ) dataset | 🔴 `exp4_explainability.py` has no clinical branch; the dataset is available (`E:/datasets/clinical`) | the qualitative part of H-5, App E, FIG-4.13/4.14 |
| **G-8 rem.** | Isolating Stage 3 (FOV mask) in the ablation | 🟡 needs a flag in `PreprocessingConfig` + a 3-channel model variant + one level | completeness of TAB-4.4 |
| **NEW-2** | MMD parameters (kernel, sample size, number of bootstrap iterations) | 🟡 extract from the experiment configuration | the methodological part of §4/§5 on H-3 |

### Computations from existing numbers (no run required)

| # | Item | How to obtain |
|---|------|--------------|
| R1 | Relative degradation (Δ_drop / in-domain) for H-7 | arithmetic over `TAB-4.8`; needed for an honest formulation of §4.6 and §5.4 |
| R2 | ROC/PR curves as figures | from the `predictions.npz` of the new run (after NEW-1) |
| R3 | Confusion matrices by camera group (exp6) | the run data record only per-class F1 → an additional export is needed for App F |

### Known implementation gaps

| # | Item | Status |
|---|------|--------|
| VVI | Not implemented in `src/utils/image_quality.py`; in the demo `data.js` it is an invented value | declare as a limitation or implement |

## Consolidated checklist (quantity → status)

| Result quantity | Assembled? | Where / how to obtain |
|-----------------------|----------|--------------------|
| Factorial metrics A–D + EH-3 | ✅ | `TAB-4.2` |
| exp1 per-class / confusion / calibration / clinical | ✅ | `exp1_per_class`, `TAB-4.3`, `exp1_clinical_indomain` |
| Statistical tests (DeLong/McNemar/Holm/ANOVA) | ✅ | `TAB-5.1` |
| Ablation (cumulative, 8 levels) | ✅ | `TAB-4.4` — ⚠️ Stage 3 not isolated |
| CLAHE sweep (two-dimensional, on EyePACS) | ✅ | `exp2_clahe_sweep` |
| Flat-field σ sweep | ✅ | `exp2_flatfield_sigma_sweep` |
| Per-stage image quality | ✅ | `TAB-4.5` — ⚠️ VVI not implemented |
| Domain distance MMD/KL | ✅ | `H-3_domain_distance` — ⚠️ NEW-2 |
| APTOS G + per-class + matrices | ✅ | `TAB-4.6`, `per_class_and_confusion` |
| Grad-CAM ALO/IoU (IDRiD) | ✅ | `TAB-4.7` |
| Grad-CAM overlays (Clinical KZ) | ❌ | **G-3** |
| Clinical degradation Δ | ✅ | `TAB-4.8` — ⚠️ R1 |
| Device shift + spread | ✅ | `TAB-4.9` — ⚠️ R3 (matrices) |
| Small-data training | ✅ | `TAB-4.10` |
| SSL probe gate | ✅ | `SSL_continual_gate` |
| Computational benchmarks | ✅ | `computational_and_iq` |
| Claim strength PC-0…10 | ✅ | `TAB-5.2` |
| Summary radar / dominance | ✅ | `findings/summary-and-dominance` |
| Hypothesis verdicts | ✅ | `STATUS.md` — ⚠️ demo/defense contradict them |
| Traceability down to `outputs/` | ❌ | **NEW-1** |

## Recommended order of closure

1. **NEW-1** — restore provenance. Without it, everything else has the character of a draft.
2. **G-3** (~2 h) and **NEW-2** (minutes) — close the letter of H-5 and H-3.
3. **R1, R3** — computations/exports from existing data for §4.6 and App F.
4. **G-8 remainder** — expensive training; can be declared as a limitation if the schedule is tight.
5. Then — **re-synchronize `demo/web/data.js` + defense/slides** to the real numbers and verdicts
   (`INTEGRITY_NOTE.md` §2).

## Note on ASSET_INVENTORY.md

`thesis/ASSET_INVENTORY.md` predates the runs and marks exp1–7 as ⏳/❌ NOT RUN. In fact all of them
are complete. The inventory should be updated (RES-EXP1 ✅, TAB-4.2…4.10 ✅ with real numbers,
hypothesis verdicts — all 7 confirmed, H-7 under the re-specified External Clinical Performance form,
the H-3 block added) — a separate step after NEW-1.
