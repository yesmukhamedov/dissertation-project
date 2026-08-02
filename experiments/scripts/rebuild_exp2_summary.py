"""Rebuild exp2 ``ablation_summary.json`` from the authoritative ``metrics.csv``.

WHY THIS EXISTS
---------------
``run_exp2_partA.py`` writes ``ablation_summary.json`` from the levels of the
CURRENT invocation only, so a partial re-run overwrites the file and drops the
levels it did not touch. That is how the canonical summary ended up holding just
``baseline`` / ``baseline_canonical_flip`` / ``baseline_flat_field`` while
``metrics.csv`` still held all six levels.

This script reconstructs the per-level aggregates from ``metrics.csv`` (the
append-only source of truth) so that back-filled folds land in the summary:
per (level, fold) it takes the best epoch by ``weighted_f1`` — the same rule the
trainer uses to pick ``best_model.pt`` — then aggregates mean ± std (population,
matching ``_compute_summary``) across folds.

``quality`` blocks (CNR / entropy / SSIM) are NOT in metrics.csv; they are
carried over from the existing summary and any ``ablation_partial_*.json`` side
files, and can be recomputed for the levels still missing them with
``--recompute-quality`` (needs the EyePACS images; ~100 images per level).

Usage (from experiments/):
    python scripts/rebuild_exp2_summary.py
    python scripts/rebuild_exp2_summary.py --recompute-quality \
        --config configs/_run_exp2_wsl.yaml --subset-fraction 0.15
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # experiments/ root

from src.experiments.exp2_ablation import _ABLATION_LEVELS

# metrics.csv column -> summary key (matches _compute_summary's naming)
_METRIC_KEYS = {
    "weighted_f1": "weighted_f1",
    "roc_auc": "roc_auc",
    "kappa": "cohen_kappa_quadratic",
    "accuracy": "accuracy",
}


def _best_epoch_per_fold(metrics_csv: Path, level_names: set[str]) -> dict[str, dict[int, dict]]:
    """Pick each (level, fold)'s best epoch by weighted_f1 from metrics.csv.

    Rows are append-only and a resumed run can re-emit an epoch, so the LAST row
    for a given (level, fold, epoch) wins before the best-epoch selection.

    Args:
        metrics_csv: Path to the exp2 ``metrics.csv``.
        level_names: Ablation level names to keep (other configs, e.g. the CLAHE
            sweep rows, are ignored).

    Returns:
        Mapping level -> fold -> the winning row (as a dict of floats).
    """
    latest: dict[tuple[str, int, int], dict] = {}
    with open(metrics_csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            level = row["config"]
            if level not in level_names:
                continue
            latest[(level, int(row["fold"]), int(row["epoch"]))] = row

    best: dict[str, dict[int, dict]] = defaultdict(dict)
    for (level, fold, _epoch), row in latest.items():
        cur = best[level].get(fold)
        if cur is None or float(row["weighted_f1"]) > float(cur["weighted_f1"]):
            best[level][fold] = row
    return best


def _aggregate(rows_by_fold: dict[int, dict]) -> dict[str, str]:
    """Aggregate per-fold best rows into ``mean ± std`` strings.

    Args:
        rows_by_fold: Mapping fold index -> best-epoch metrics row.

    Returns:
        Mapping summary metric name -> ``"mean ± std"`` (std is population std,
        as in ``exp2_ablation._compute_summary``).
    """
    out: dict[str, str] = {}
    for csv_key, summary_key in _METRIC_KEYS.items():
        vals = [float(r[csv_key]) for r in rows_by_fold.values()
                if r.get(csv_key) not in (None, "") and not np.isnan(float(r[csv_key]))]
        if vals:
            out[summary_key] = f"{np.mean(vals):.4f} ± {np.std(vals):.4f}"
    return out


def _collect_quality(output_dir: Path) -> dict[str, dict]:
    """Harvest per-level quality blocks from the summary + partial side files.

    Args:
        output_dir: The exp2 output directory.

    Returns:
        Mapping level name -> quality dict (CNR / entropy / SSIM).
    """
    quality: dict[str, dict] = {}
    sources = sorted(output_dir.glob("ablation_partial_*.json"))
    summary_path = output_dir / "ablation_summary.json"
    if summary_path.exists():
        sources.append(summary_path)  # canonical wins over partials
    for src in sources:
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
        for level, entry in data.items():
            if level.startswith("_") or not isinstance(entry, dict):
                continue
            if entry.get("quality"):
                quality[level] = entry["quality"]
    return quality


def _recompute_quality(levels: list[str], config_path: str, subset_fraction: float,
                       n_samples: int) -> dict[str, dict]:
    """Re-measure image quality for levels whose quality block was lost.

    Mirrors what ``_run_ablation`` measures: the fold-0 train split of the same
    stratified patient subset, with the level's validation-mode pipeline.

    Args:
        levels: Ablation level names to measure.
        config_path: Config YAML (must carry the EyePACS path used for the run).
        subset_fraction: The ``--subset-fraction`` of the original run.
        n_samples: Number of images to sample per level.

    Returns:
        Mapping level name -> quality dict.
    """
    from src.utils.config import load_config
    from src.utils.seed import set_seed
    from src.data.splits import PatientLevelKFold
    from src.experiments.exp2_ablation import (
        _PipelineAdapter, _build_pipeline, _load_eyepacs_index,
        _measure_quality_on_sample,
    )
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "outputs" / "ssl_run_artifacts"))
    from run_exp2_partA import _stratified_patient_subset

    config = load_config(config_path)
    seed = config.get("seed", 42)
    set_seed(seed)
    eyepacs_root = config["paths"]["eyepacs"]
    paths, labels, pids = _load_eyepacs_index(
        str(Path(eyepacs_root) / "train"), str(Path(eyepacs_root) / "trainLabels.csv"))
    paths, labels, pids = _stratified_patient_subset(
        paths, labels, pids, subset_fraction, seed)
    splitter = PatientLevelKFold(
        n_folds=config["cross_validation"]["n_folds"], seed=seed,
        stratified=config["cross_validation"].get("stratified", True))
    train_idx_0 = splitter.split(paths, labels, pids)[0][0]
    sample_paths = [paths[i] for i in train_idx_0]

    prep_cfg = config.get("preprocessing", {})
    flags_by_name = {lv["name"]: lv["flags"] for lv in _ABLATION_LEVELS}
    out: dict[str, dict] = {}
    for level in levels:
        pipeline_val = _PipelineAdapter(
            _build_pipeline(prep_cfg, flags_by_name[level], is_training=False))
        out[level] = _measure_quality_on_sample(
            sample_paths, pipeline_val, n_samples=n_samples, seed=seed)
        print(f"  quality[{level}]: CNR={out[level].get('mean_cnr', float('nan')):.3f}",
              flush=True)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Rebuild exp2 ablation_summary.json from metrics.csv")
    ap.add_argument("--output-dir", default="outputs/exp2")
    ap.add_argument("--recompute-quality", action="store_true",
                    help="Re-measure CNR/entropy/SSIM for levels missing a quality block.")
    ap.add_argument("--config", default="configs/_run_exp2_wsl.yaml",
                    help="Config used by the original run (only for --recompute-quality).")
    ap.add_argument("--subset-fraction", type=float, default=0.15,
                    help="Subset fraction of the original run (only for --recompute-quality).")
    ap.add_argument("--quality-samples", type=int, default=100)
    args = ap.parse_args()

    output_dir = Path(args.output_dir)
    metrics_csv = output_dir / "metrics.csv"
    if not metrics_csv.exists():
        raise SystemExit(f"{metrics_csv} not found")

    level_names = [lv["name"] for lv in _ABLATION_LEVELS]
    best = _best_epoch_per_fold(metrics_csv, set(level_names))
    quality = _collect_quality(output_dir)

    missing_quality = [lv for lv in level_names if lv in best and lv not in quality]
    if missing_quality and args.recompute_quality:
        print(f"Recomputing quality for {missing_quality} ...", flush=True)
        quality.update(_recompute_quality(
            missing_quality, args.config, args.subset_fraction, args.quality_samples))
        missing_quality = [lv for lv in level_names if lv in best and lv not in quality]

    # Preserve bookkeeping blocks that are not derivable from metrics.csv.
    summary_path = output_dir / "ablation_summary.json"
    old: dict = {}
    if summary_path.exists():
        with open(summary_path, encoding="utf-8") as f:
            old = json.load(f)

    summary: dict = {}
    print(f"\nRebuilt from {metrics_csv}:")
    for level in level_names:
        if level not in best:
            print(f"  {level:<26s}: NO ROWS — skipped")
            continue
        folds = sorted(best[level])
        entry = {"metrics": _aggregate(best[level]), "folds": folds}
        if level in quality:
            entry["quality"] = quality[level]
        summary[level] = entry
        print(f"  {level:<26s}: F1={entry['metrics'].get('weighted_f1', 'N/A')}  folds={folds}"
              + ("" if level in quality else "  [quality missing]"))

    meta = dict(old.get("_meta", {}))
    meta["rebuilt_by"] = "scripts/rebuild_exp2_summary.py (source of truth: metrics.csv)"
    meta["folds_run"] = sorted({f for lv in summary.values() for f in lv["folds"]})
    if missing_quality:
        meta["quality_missing_for"] = missing_quality
    summary["_meta"] = meta
    if "_clahe_sweep" in old:
        summary["_clahe_sweep"] = old["_clahe_sweep"]

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
