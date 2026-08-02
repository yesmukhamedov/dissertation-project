"""Category B — dump per-sample predictions for Experiment 1 (predictions.npz).

Re-runs INFERENCE ONLY on the existing exp1 best checkpoints (A–D × 5 folds),
over each fold's held-out validation split, and saves raw per-sample
``y_true`` / ``y_pred`` / ``y_prob`` so the downstream analysis
(``analyze_exp1_predictions.py``) can compute per-class F1/AUC, confusion
matrices, calibration (ECE/Brier), clinical referable metrics, and paired
statistical tests (DeLong / McNemar) — none of which the training run saved
(only per-epoch aggregates were logged).

Reuses the EXACT split + preprocessing construction from
``src.experiments.exp1_factorial`` so the validation sets match training.

GPU box usage (RTX 3060 / WSL) — full run:
    conda activate dr-classifier
    python scripts/dump_exp1_predictions.py --config configs/<exp1-run>.yaml

Smoke (CPU, validates wiring on a few images):
    python scripts/dump_exp1_predictions.py --config configs/default.yaml \
        --smoke 48 --configs A --fold 0 --out outputs/exp1/predictions_smoke.npz

Output: an .npz with, per config key present, arrays
    <cfg>_y_true, <cfg>_y_pred, <cfg>_prob (N×5), <cfg>_fold  (fold id per row)
concatenated across folds (val sets are disjoint → one prediction per image).
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # experiments/ root for `src`

from src.utils.config import load_config, get_experiment_config
from src.utils.seed import set_seed
from src.data.datasets import CachedEyePACSDataset, EyePACSDataset, load_cache_meta
from src.data.splits import PatientLevelKFold
from src.models.factory import create_model
from src.experiments.exp1_factorial import (
    _CONFIGS,
    _make_preprocessing,
    _load_eyepacs_index,
    _load_cache_index,
)
from src.experiments._eval_utils import infer_dataset


def _build_index_and_splits(config: dict[str, Any], smoke: int | None):
    """Replicate exp1_factorial.run's index-load + subset + split, verbatim in effect."""
    eyepacs_root = config["paths"]["eyepacs"]
    labels_csv = str(Path(eyepacs_root) / "trainLabels.csv")
    images_root = str(Path(eyepacs_root) / "train")
    cache_dir = config.get("paths", {}).get("cache_dir")

    if cache_dir:
        all_paths, all_labels, all_pids, all_sides = _load_cache_index(cache_dir, subset_size=smoke)
        cache_meta = load_cache_meta(cache_dir)
    else:
        all_paths, all_labels, all_pids, all_sides = _load_eyepacs_index(
            images_root, labels_csv, subset_size=smoke
        )
        cache_meta = None

    # Stratified patient-level subset (identical block to exp1_factorial.run)
    subset_cfg = config.get("subset", {})
    if subset_cfg.get("enabled", False):
        from sklearn.model_selection import train_test_split

        fraction = subset_cfg["fraction"]
        sub_seed = subset_cfg.get("seed", 42)
        p2i: dict[str, list[int]] = defaultdict(list)
        for idx, pid in enumerate(all_pids):
            p2i[pid].append(idx)
        uniq = list(p2i.keys())
        plabels = [max(all_labels[i] for i in p2i[pid]) for pid in uniq]
        selected, _ = train_test_split(
            uniq, train_size=fraction, stratify=plabels, random_state=sub_seed
        )
        sel = set(selected)
        keep = [i for i, pid in enumerate(all_pids) if pid in sel]
        all_paths = [all_paths[i] for i in keep]
        all_labels = [all_labels[i] for i in keep]
        all_pids = [all_pids[i] for i in keep]
        all_sides = [all_sides[i] for i in keep]

    cv_cfg = config["cross_validation"]
    splitter = PatientLevelKFold(
        n_folds=cv_cfg["n_folds"], seed=config.get("seed", 42),
        stratified=cv_cfg.get("stratified", True),
    )
    splits = splitter.split(all_paths, all_labels, all_pids)
    return (all_paths, all_labels, all_pids, all_sides), splits, cache_dir, cache_meta


def _load_norm_stats(config: dict[str, Any]):
    """EyePACS Stage-7 normalize stats (full configs), mirroring exp1_factorial.run."""
    import json
    processed_dir = Path(config.get("paths", {}).get("output_dir", "outputs/")).parent / "data" / "processed"
    p = processed_dir / "eyepacs_norm_stats.json"
    if p.exists():
        s = json.load(open(p))
        return tuple(s["mean"]), tuple(s["std"])
    print("  [warn] eyepacs_norm_stats.json not found — full configs fall back to ImageNet.")
    return None, None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--experiment", default="exp1")
    ap.add_argument("--configs", default="A,B,C,D", help="comma list of config keys")
    ap.add_argument("--fold", type=int, default=None, help="single fold (default: all)")
    ap.add_argument("--smoke", type=int, default=None, help="limit CSV rows for a CPU smoke test")
    ap.add_argument("--val-frac", type=float, default=None,
                    help="evaluate only this fraction OF EACH FOLD'S HELD-OUT val set "
                         "(leakage-safe: split is deterministic; same subsample across configs "
                         "so B-vs-A / D-vs-C stay aligned). Use e.g. 0.01 for a fast preview.")
    ap.add_argument("--out", default="outputs/exp1/predictions.npz")
    args = ap.parse_args()

    config = load_config(args.config)
    try:
        config = get_experiment_config(config, args.experiment)
    except KeyError:
        pass  # config may already be a flat merged run-config without 'experiments'
    set_seed(config.get("seed", 42))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    (all_paths, all_labels, all_pids, all_sides), splits, cache_dir, cache_meta = \
        _build_index_and_splits(config, args.smoke)
    dataset_mean, dataset_std = _load_norm_stats(config)

    cfg_keys = [c.strip().upper() for c in args.configs.split(",")]
    n_folds = config["cross_validation"]["n_folds"]
    fold_range = [args.fold] if args.fold is not None else list(range(n_folds))
    ckpt_root = Path(config["paths"]["output_dir"]) / "exp1" / "checkpoints"

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out: dict[str, np.ndarray] = {}
    if out_path.exists():
        try:
            out = {k: v for k, v in np.load(out_path).items()}
            done = sorted({k.split("_")[0] for k in out})
            print(f"Resume: existing {out_path} has configs {done} — will skip them.")
        except Exception as e:
            print(f"  [warn] could not load existing {out_path}: {e}")
    for cfg_key in cfg_keys:
      try:
        if f"{cfg_key}_y_true" in out:
            print(f"  [skip] {cfg_key} already present in {out_path}")
            continue
        spec = _CONFIGS[cfg_key]
        model_name, preproc_kind = spec["model"], spec["preprocessing"]
        in_channels = spec.get("in_channels", 4)
        model_cfg = {**config["models"][model_name], "in_channels": in_channels}

        for fold_idx in fold_range:
            fk = f"{cfg_key}_f{fold_idx}"
            if f"{fk}_y_true" in out:
                print(f"  [skip] {cfg_key} fold{fold_idx}: already saved")
                continue
            ckpt = ckpt_root / f"{cfg_key}_fold{fold_idx}" / "best_model.pt"
            if not ckpt.exists():
                print(f"  [skip] {cfg_key} fold{fold_idx}: no checkpoint at {ckpt}")
                continue
            _, val_idx = splits[fold_idx]
            if args.val_frac is not None and 0 < args.val_frac < 1:
                # Subsample within THIS fold's held-out val set. Seed by fold only
                # (not config) so the same images are used for A/B and C/D → paired
                # tests stay aligned. No leakage: val_idx is already the checkpoint's
                # own held-out fold.
                rng = np.random.default_rng(1000 + fold_idx)
                k = max(1, int(round(len(val_idx) * args.val_frac)))
                val_idx = sorted(int(i) for i in rng.choice(val_idx, size=k, replace=False))
            va_paths = [all_paths[i] for i in val_idx]
            va_labels = [all_labels[i] for i in val_idx]
            va_pids = [all_pids[i] for i in val_idx]
            va_sides = [all_sides[i] for i in val_idx]

            val_preproc = _make_preprocessing(
                preproc_kind, model_name, is_training=False,
                dataset_mean=dataset_mean, dataset_std=dataset_std,
            )
            if cache_dir and preproc_kind == "full":
                val_ds = CachedEyePACSDataset(
                    image_paths=va_paths, labels=va_labels, patient_ids=va_pids,
                    preprocessing=val_preproc, cache_meta=cache_meta, eye_sides=va_sides,
                )
            else:
                val_ds = EyePACSDataset(
                    image_paths=va_paths, labels=va_labels, patient_ids=va_pids,
                    preprocessing=val_preproc, augmentation=None, eye_sides=va_sides,
                )

            model = create_model(model_name, model_cfg)
            state = torch.load(ckpt, map_location="cpu", weights_only=False)
            model.load_state_dict(state["model_state_dict"])
            model.to(device).eval()

            y_true, y_pred, y_prob, metrics = infer_dataset(model, val_ds, config, device)
            print(f"  {cfg_key} fold{fold_idx}: n={len(y_true)} "
                  f"wF1={metrics.get('val_weighted_f1', float('nan')):.4f} "
                  f"labels={dict(sorted(Counter(y_true.tolist()).items()))}")
            out[f"{fk}_y_true"] = y_true
            out[f"{fk}_y_pred"] = y_pred
            out[f"{fk}_prob"] = y_prob
            np.savez_compressed(out_path, **out)   # per-fold save (reap/crash-safe)
            print(f"  [saved] {cfg_key} fold{fold_idx} -> {out_path}", flush=True)
      except Exception as e:
        print(f"  [ERROR] config {cfg_key} failed: {e}", flush=True)
        import traceback
        traceback.print_exc()

    cfgs_present = sorted({k.split("_")[0] for k in out})
    print(f"\nDone. Configs with data in {out_path}: {cfgs_present}")


if __name__ == "__main__":
    main()
