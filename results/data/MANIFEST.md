# data/ MANIFEST — canonical result files

> 🔴 **WARNING: the files in this folder belong to the PREVIOUS run (snapshot of 2026-07-24…28).**
> The tables and verdicts in `results/tables/`, `results/hypotheses/`, `results/findings/` and
> `results/STATUS.md` have been updated for the **2026-08-02** run (source — `VALUES.md`), while the
> raw artifacts of that run have not yet been published into the repository — neither here nor into
> `experiments/outputs/` (the latest files there date from 2026-07-30).
>
> **Until that is closed out, the JSON files below are NOT confirmation of the numbers in the
> tables** — they will yield different values and the opposite verdicts (`h1_supported=false`, etc.).
> They must not be used for cross-checking. Item **NEW-1** in `HYPOTHESIS_COVERAGE.md`.

The source of truth is always `experiments/outputs/`; this folder is a snapshot for portability.

## What needs to be done to restore provenance

1. Publish the raw artifacts of the 2026-08-02 run into `experiments/outputs/exp{1..7}/` and
   `outputs/ssl*/` (`summary.json`, `*_results.json`, `metrics.csv`, `predictions.npz`, the σ-sweep
   and two-dimensional CLAHE grid artifacts, the MMD/KL results for H-3).
2. Update the copies in this folder and rewrite the table below.
3. Reconcile the numbers in `results/tables/` with the new JSON and remove the warning above.
4. This also closes **G-10** along the way (verifying that the offline B/D predictions reproduce training).

## Current contents (stale — the run prior to 2026-07-28)

| File | Source | Experiment | Key contents | Status |
|------|----------|-------------|---------------------|--------|
| `exp1_summary.json` | `outputs/exp1/summary.json` | exp1 (H-1) | 4 configs × metrics, `dominance_tests`, `h1_supported=false` | ⚠️ stale |
| `exp2_ablation_summary.json` | `outputs/exp2/ablation_summary.json` | exp2 (H-2) | individual 6-level ablation + quality; 15% / 3 folds | ⚠️ stale (the new run has 8 levels, 100% / 5 folds) |
| `exp2_clahe_sweep.json` | `outputs/exp2/clahe_sweep.json` | exp2 (H-2) | one-dimensional clip sweep on IDRiD | ⚠️ stale (the new one is a two-dimensional grid on EyePACS) |
| `exp3_transferability_results.json` | `outputs/exp3/transferability_results.json` | exp3 (H-4) | APTOS, `h4_supported=false` | ⚠️ stale |
| `exp4_iou_results_maskset.json` | `outputs/exp4/iou_results_maskset.json` | exp4 (H-5) | ALO/IoU over 54 masks, `h5_alo_supported=false` | ⚠️ stale |
| `exp4_iou_results.json` | `outputs/exp4/iou_results.json` | exp4 (H-5) | the same metric at n_masks = 5 (a sampling artifact) | ⚠️ long stale |
| `exp5_clinical_degradation_results.json` | `outputs/exp5/clinical_degradation_results.json` | exp5 (H-7) | IDRiD/Messidor-2, `h7_supported=false` | ⚠️ stale |
| `exp6_device_shift_results.json` | `outputs/exp6/device_shift_results.json` | exp6 (H-6) | 5 camera groups, `h6_supported=false`; RFMiD binary | ⚠️ stale |
| `exp7_small_data_results.json` | `outputs/exp7/small_data_results.json` | exp7 | baseline/full per fold, `full_minus_baseline_weighted_f1=0.0899` | ⚠️ stale |
| `ssl_COMPARISON.txt` | `outputs/ssl/COMPARISON.txt` | SSL | from-scratch probe gate: BYOL/MoCo-v2/DINO — all passed=False | 🟡 partially current (SIP was added in the new run, passed=True) |
| `ssl_gate_continual_{resnet50,efficientnet_b3}.json` | `outputs/ssl_run_artifacts/sip/v1.0/gate_report_CONTINUAL_*.json` | SSL-continual | linear-probe gate for the B/D init | ⚠️ stale (in the new run EffNet-B3 does gain; previously it did not) |
| `ssl_gate_run2_{resnet50,efficientnet_b3}.json` | `outputs/ssl_run_artifacts/sip/v1.0/gate_report_*.json` | SSL-continual | second run of the probe gate | ⚠️ stale |

## What the snapshot does not contain at all (new in the 2026-08-02 run)

- **H-3** — MMD over penultimate-layer features and KL over per-channel histograms for 6 domains
  (`tables/H-3_domain_distance.md`). There is no source file.
- **Flat-field σ sweep** — 6 points 0.05–0.10·D + CNR (`tables/exp2_flatfield_sigma_sweep.md`).
- **The two-dimensional CLAHE grid** (clip × global_threshold) and the separate F1(DR1) / F1(DR2) grids.
- **The 8-level cumulative ablation** with per-fold values and σ_fold.
- **The Holm correction and mixed-effects ANOVA** for exp1 (`tables/TAB-5.1_statistical.md`).

## Per-fold CSVs (not copied — links to the source)

- exp1: `experiments/outputs/exp1/metrics.csv` — history for 4 configs × 5 folds.
- exp2: `experiments/outputs/exp2/metrics.csv`, `metrics_clahe_sweep.csv`.
- exp4: `experiments/outputs/exp4/metrics_{baseline,full_pipeline}.csv`; overlays —
  `outputs/exp4/gradcam_maskset/*.png` (54 of them, all with masks).
- exp7: `experiments/outputs/exp7/metrics.csv`.
- exp3/5/6: the `metrics.csv` files contain only a header (these are evaluation experiments).
