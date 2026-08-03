# Category B — runbook (exp1 re-inference → tables)

> **Status as of 2026-08-03.** Category B as a task is **closed** — all of its quantities (per-class,
> calibration, in-domain clinical, paired statistical tests) are present in `results/tables/` for the
> 2026-08-03 run. This runbook is retained as a **procedure**: it will be needed to obtain the new
> run's `predictions.npz` for the ROC/PR curves (item R2) and to reconcile the offline predictions
> with training (gap G-10) once the run artifacts have been published (NEW-1).
> The numeric reference points in the "Verification" section below refer to the previous run.

Category B = the quantities that exp1 training did NOT save (only per-epoch aggregates):
per-class F1/AUC, confusion matrices, ROC/PR, ECE/Brier calibration, in-domain clinical metrics,
the DeLong/McNemar statistical tests. All of them require **per-instance probabilities** → one
inference pass over the best exp1 checkpoints (A–D × 5 folds) on their val splits is needed.

## Why on the GPU box

A full re-inference = ~35 126 images × 4 configs at 512². **Measured in this CPU environment
(2026-07-27): 0.46 img/s** for config A (baseline, the lightest) → ~21 hours for A ALONE; configs
B/D (full 4ch pipeline) are slower still → a full pass ≈ **several days**, and fragile (background
jobs get reaped here). On an RTX 3060/WSL it is on the order of **minutes to an hour**. Hence step 1
(the dump) runs on the GPU box; step 2 (analysis) is CPU-cheap and can run anywhere.

## Scripts (ready, validated by a CPU smoke test)

- `experiments/scripts/dump_exp1_predictions.py` — checkpoint inference → `predictions.npz`
  (reuses the exact splits/preprocessing from `exp1_factorial`, so the val splits match training).
- `experiments/scripts/analyze_exp1_predictions.py` — `predictions.npz` → markdown tables in `results/tables/`.

## Step 1 — dump on the GPU box (RTX 3060/WSL), 3 runs

Separately: baseline A/C (no cache) and full B/D (each with its own `_run_exp1{B,D}.yaml`, which
already sets `paths.cache_dir: C:/ssl_data/cache_512` → stages 0–4 come from the cache). All three
configs produce the same seed-42 5-fold split as training → the val folds match.

```bash
cd <repo>/experiments
conda activate dr-classifier
python scripts/dump_exp1_predictions.py --config configs/_run_exp1AC.yaml --configs A,C --out outputs/exp1/pred_AC.npz
python scripts/dump_exp1_predictions.py --config configs/_run_exp1B.yaml  --configs B   --out outputs/exp1/pred_B.npz
python scripts/dump_exp1_predictions.py --config configs/_run_exp1D.yaml  --configs D   --out outputs/exp1/pred_D.npz
```

Check: in the log, the wF1 for each `<cfg> foldN` should match `exp1/summary.json` (±). If it does
not — see the "Verification" section below (most likely the 512² cache was regenerated after the
FOV-crop fix of 2026-07-19).

Then copy the three files to `E:\dissertation-project\experiments\outputs\exp1\`:
`pred_AC.npz`, `pred_B.npz`, `pred_D.npz`.

## Step 2 — analysis (CPU, fast; on the E: machine)

```bash
python scripts/analyze_exp1_predictions.py \
    --pred outputs/exp1/pred_AC.npz outputs/exp1/pred_B.npz outputs/exp1/pred_D.npz
# --pred accepts several files and merges the configs (for the paired B-vs-A / D-vs-C tests).
# writes into results/tables/: exp1_per_class.md, TAB-4.3_exp1_calibration.md,
#                              exp1_clinical_indomain.md, TAB-5.1_statistical.md
```

## Verification

- The per-fold wF1 in the logs ≈ `outputs/exp1/summary.json`. If they diverge: the exp1 checkpoints
  were trained on 10–14 July (before the FOV-crop fix of 19 July), while `cache_512` may have been
  regenerated AFTER the fix → the B/D preprocessing at inference ≠ that at training. Fix: (a) use the
  cache as of training time, or (b) accept the re-inference as a self-consistent evaluation and flag
  it with a caveat. A/C (baseline, no cache) are unaffected.
- `analyze` checks pair alignment (`np.array_equal(y_true_a, y_true_b)`) and skips a pair if it does not match.

## After the tables are obtained — update

- `results/GAP_ANALYSIS.md` (category B → closed), `results/TODO_BEFORE_WRITING.md` (B0–B4).
- `results/tables/TAB-5.4_clinical_referable.md` — add the exp1 in-domain rows (B3).
- `results/tables/TAB-5.2_claim_strength.md` — if DeLong shows ΔAUC to be significant (B vs A / D vs C),
  strengthen the wording about the AUC gain (currently MODERATE, based on the per-fold CIs).

## Notes on correctness

- The **B vs A** and **D vs C** pairs are evaluated on the SAME val split per fold (the splits are
  identical across configs) → the rows of predictions.npz are aligned; `analyze_*` checks
  `np.array_equal(y_true_a,y_true_b)` before the paired tests and skips a pair if they are not aligned.
- DeLong tests the referable AUC (grade≥2); McNemar tests the fraction of correct predictions.
- If `cache_dir` is set for B/D, the dump uses `CachedEyePACSDataset` (as in training).
- Local smoke test: `--smoke 64 --configs A --fold 0 --out outputs/exp1/predictions_smoke.npz` (≈14 img, CPU).
