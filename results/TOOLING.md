# TOOLING — tooling for tables/figures/statistics

What to reuse when assembling the dissertation's results material, and where the gaps are.
State — after the **2026-08-03** run.

## Reuse as is

| Module | What it provides |
|--------|----------|
| `experiments/src/evaluation/metrics.py` | `compute_primary_metrics` (weighted_f1, roc_auc macro-OvR robust to missing classes, cohen_kappa_quadratic, accuracy); `compute_secondary_metrics` (per-class f1/prec/recall, macro_f1, confusion_matrix); `compute_clinical_metrics` (sensitivity/specificity/ppv/npv, referable≥2); `check_dominance` (EH-3: ΔF1≥0.05, ΔAUC≥0.02, Δκ≥0); `check_overfitting`. |
| `experiments/src/evaluation/statistical_tests.py` | `mcnemar_test`, `delong_test` (full DeLong variance for AUC comparison), `bootstrap_ci` / `bootstrap_ci_all_primary` (95% CI, 1000 iterations), `holm_bonferroni_correction`, `compute_mixed_effects_summary`. |
| `experiments/src/evaluation/calibration.py` | ECE, Brier score. |
| `experiments/src/explainability/visualization.py` | `overlay_gradcam`, `create_comparison_figure` — the actual Grad-CAM rendering (for exp4). |
| `experiments/src/experiments/_eval_utils.py` | `evaluate_dataset`, `infer_dataset` (raw y_true/y_pred/y_prob for paired tests), `evaluate_dataset_binary` (RFMiD). |

## Aggregator scripts

- `experiments/scripts/generate_report.py` — JSON→Markdown tables of hypotheses/claims →
  `outputs/final_report.md`. **There is a filename mismatch:** the script expects
  `degradation_results.json` / `generalization_results.json` / `iou_results.json` /
  `ablation_summary.json`, whereas on disk there are `transferability_results.json` /
  `clinical_degradation_results.json` / `device_shift_results.json` / `small_data_results.json`.
  → Fix the name mapping before running it as a cross-check of `results/tables/`.
- `experiments/scripts/verify_exp1.py … verify_exp5_exp6.py` — run verification.

## ⚠️ DO NOT reuse directly (contaminated with hardcoded numbers — see INTEGRITY_NOTE.md)

- `demo/web/generate_charts_01_14.py` / `_15_28.py` / `_29_30.py` — figures built on constants from `data.js`.
- `defense/figures/scripts/fig9_confusion_matrix.py` — the matrices are hardcoded.
- What is worth keeping from them: **the house palette** (`BLUE #378ADD`, `TEAL #1D9E75`,
  `CORAL #D85A30`, `PURPLE #7F77DD`, `AMBER #EF9F27`, `GRAY #888780`, `GREEN #639922`, `RED #E24B4A`) —
  it can be retained as a common style, with the data rebound to `outputs/`.

## Gaps (to build/fix)

1. 🔴 **The 2026-08-03 run artifacts have not been published** into `experiments/outputs/` — every
   script below reads from there and will currently return numbers from the **previous** run. Close
   this first (item NEW-1 in `GAP_ANALYSIS.md`), otherwise any cross-check is misleading.
2. **An outputs→figures bridge** — there is no script that reads
   `experiments/outputs/exp*/{summary.json, *_results.json, metrics.csv}` and draws
   publication-quality figures. Build one (reusing the palette) to eliminate manual transcription as
   a class of error.
3. **`predictions.npz` from the new run** — needed for ROC/PR curves and confusion matrices
   (`fig7_pr_curves.py` requires it). Source: `infer_dataset` on the best checkpoints; the procedure
   is in `CATEGORY_B_RUNBOOK.md`.
4. **Confusion matrices by camera group (exp6)** — the run data record only per-class F1; an
   additional export is needed for App F (item R3).
5. **Not implemented in code:** the flat-field σ sweep has now been run, but there is still no Part C
   function in `src/experiments/exp2_ablation.py` — if it needs to be reproduced, the code has to be
   written; **VVI** is absent from `src/utils/image_quality.py`; there is no **FOV-mask toggle** in
   `PreprocessingConfig` (which blocks isolating Stage 3, item G-8); and there is no **clinical
   branch** in `exp4_explainability.py` (which blocks G-3).
6. **GOST tables** — `generate_report.py` produces Markdown only; for .docx/.pdf there is the
   `council-docs` skill / `md2gost.py` (`.claude/skills/council-docs/`) as the target converter.

## What has already been computed (code applied, results in `results/tables/`)

- `statistical_tests.py` — bootstrap CIs, DeLong, McNemar, **Holm correction**, **mixed-effects ANOVA**
  → `TAB-5.1_statistical.md`.
- `calibration.py` — ECE/Brier → `TAB-4.3_exp1_calibration.md`.
- `metrics.py` — per-class, confusion, clinical metrics → `exp1_per_class.md`,
  `exp1_clinical_indomain.md`, `TAB-5.4_clinical_referable.md`.
- `image_quality.py` — CNR/Entropy/SSIM across the ablation levels → `TAB-4.5_exp2_image_quality.md`.

## Output formats and locations

- Per-fold metrics → CSV: `outputs/exp{1..7}/metrics.csv` (columns: `epoch,fold,config,
  train_loss,val_loss,weighted_f1,roc_auc,kappa,accuracy`). exp2 also has `metrics_clahe_sweep.csv`;
  exp4 also has `metrics_baseline.csv`, `metrics_full_pipeline.csv`.
- Aggregates → JSON: `outputs/exp1/summary.json`, `exp3/transferability_results.json`,
  `exp5/clinical_degradation_results.json`, `exp6/device_shift_results.json`,
  `exp7/small_data_results.json`. SSL: `outputs/ssl*/**/gate_report*.json`, `ssl/COMPARISON.txt`.
- Experiment sources: `experiments/src/experiments/exp{1..7}_*.py`.
