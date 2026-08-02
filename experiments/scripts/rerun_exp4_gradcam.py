"""Re-run the Exp-4 Grad-CAM / ALO / IoU analysis on the FULL IDRiD mask set (G-1).

The original Exp-4 run sampled 50 images from IDRiD's *Disease Grading* training
set (413 images) while the lesion masks live in the *Segmentation* training set
(54 images) — the intersection was only **5** images, so every ALO/IoU mean in
``outputs/exp4/iou_results.json`` rests on 1–2 images per lesion type.

This script re-runs ONLY the explainability stage, from the already-trained
EfficientNet-B4 checkpoints, over **all IDRiD images that actually carry lesion
masks**, and adds a paired significance test (Wilcoxon signed-rank + bootstrap
CI of the mean difference) that H-5's wording ("significantly higher") requires.

No training happens here and nothing from the original run is overwritten:
results go to ``iou_results_maskset.json`` and ``gradcam_maskset/``.

Usage (WSL, GPU env):
    python scripts/rerun_exp4_gradcam.py --config configs/_run_gen_wsl.yaml
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.datasets import IDRiDDataset  # noqa: E402
from src.experiments.exp4_explainability import (  # noqa: E402
    _LESION_TYPES,
    _build_pipeline,
    _image_to_tensor,
)
from src.explainability.gradcam import GradCAMGenerator  # noqa: E402
from src.explainability.iou import (  # noqa: E402
    compute_alo_per_lesion_type,
    compute_attention_overlap,
    compute_iou_per_lesion_type,
)
from src.explainability.visualization import create_comparison_figure  # noqa: E402
from src.models.efficientnet import create_efficientnet, get_gradcam_target_layer  # noqa: E402
from src.training.checkpoint import CheckpointManager  # noqa: E402
from src.utils.config import load_config  # noqa: E402
from src.utils.seed import set_seed  # noqa: E402


def _load_trained_model(
    config: dict[str, Any],
    config_name: str,
    output_dir: Path,
    device: torch.device,
) -> torch.nn.Module:
    """Load a trained Exp-4 EfficientNet-B4 from its checkpoint directory.

    Args:
        config: Merged experiment config.
        config_name: "baseline" (3ch) or "full_pipeline" (4ch).
        output_dir: Exp-4 output root containing ``checkpoints/<config_name>``.
        device: Device to place the model on.

    Returns:
        The model in eval mode on ``device``.

    Raises:
        FileNotFoundError: If no best checkpoint exists for this configuration.
    """
    model_cfg = dict(config["models"]["efficientnet_b4"])
    in_channels = 3 if config_name == "baseline" else 4
    model = create_efficientnet(
        variant="b4",
        num_classes=model_cfg.get("num_classes", 5),
        pretrained=False,          # weights come from the checkpoint
        dropout=model_cfg.get("dropout", 0.4),
        freeze_base=False,
        in_channels=in_channels,
    )
    ckpt_dir = output_dir / "checkpoints" / config_name
    if not (ckpt_dir / "best_model.pt").exists():
        raise FileNotFoundError(f"No best_model.pt in {ckpt_dir}")
    CheckpointManager(ckpt_dir, max_keep=5).load_best(model)
    return model.to(device).eval()


def _paired_stats(
    baseline: list[float],
    preprocessed: list[float],
    n_boot: int = 10000,
    seed: int = 42,
) -> dict[str, Any]:
    """Paired comparison of a per-image metric (preprocessed vs baseline).

    Args:
        baseline: Per-image metric values for the baseline model.
        preprocessed: Per-image metric values for the full-pipeline model.
        n_boot: Bootstrap resamples for the CI of the mean difference.
        seed: RNG seed for the bootstrap.

    Returns:
        Dict with n, means, mean difference, bootstrap 95% CI, Wilcoxon p-value
        (None when scipy is unavailable or all differences are zero), and the
        count of images where the preprocessed model scored higher.
    """
    b = np.asarray(baseline, dtype=np.float64)
    p = np.asarray(preprocessed, dtype=np.float64)
    diff = p - b
    n = int(diff.size)
    out: dict[str, Any] = {
        "n_images": n,
        "mean_baseline": float(b.mean()) if n else float("nan"),
        "mean_preprocessed": float(p.mean()) if n else float("nan"),
        "mean_difference": float(diff.mean()) if n else float("nan"),
        "n_improved": int((diff > 0).sum()),
        "n_worse": int((diff < 0).sum()),
        "n_tied": int((diff == 0).sum()),
    }
    if n < 2:
        out["ci95_difference"] = None
        out["wilcoxon_p"] = None
        return out

    rng = np.random.default_rng(seed)
    boot = np.array([
        rng.choice(diff, size=n, replace=True).mean() for _ in range(n_boot)
    ])
    out["ci95_difference"] = [float(np.percentile(boot, 2.5)),
                              float(np.percentile(boot, 97.5))]
    try:
        from scipy.stats import wilcoxon
        if np.allclose(diff, 0.0):
            out["wilcoxon_p"] = None
            out["wilcoxon_note"] = "all paired differences are zero"
        else:
            # One-sided: H-5 predicts preprocessed > baseline.
            stat, pval = wilcoxon(p, b, alternative="greater",
                                  zero_method="zsplit")
            out["wilcoxon_statistic"] = float(stat)
            out["wilcoxon_p"] = float(pval)
    except ImportError:
        out["wilcoxon_p"] = None
        out["wilcoxon_note"] = "scipy unavailable"
    return out


def main() -> None:
    """Run the mask-complete Exp-4 explainability re-analysis."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True,
                        help="Merged run config (paths must resolve on this box)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Analyse only the first N masked images (smoke test)")
    parser.add_argument("--no-figures", action="store_true",
                        help="Skip writing comparison overlays")
    parser.add_argument("--out-name", type=str, default="iou_results_maskset",
                        help="Output JSON stem inside outputs/exp4/")
    parser.add_argument("--thresholds", type=str, default="0.2,0.3,0.5,0.7",
                        help="Extra Grad-CAM binarisation thresholds to report "
                             "alongside the canonical 0.5 (sensitivity check)")
    args = parser.parse_args()
    thresholds = sorted({float(t) for t in args.thresholds.split(",")} | {0.5})

    config = load_config(str(args.config))
    seed = config.get("seed", 42)
    set_seed(seed)

    output_dir = Path(config["paths"]["output_dir"]) / "exp4"
    fig_dir = output_dir / "gradcam_maskset"
    if not args.no_figures:
        fig_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── IDRiD: keep only images that actually carry lesion masks ─────────────
    idrid_root = config["paths"]["idrid"]
    idrid_ds = IDRiDDataset.from_directory(
        root=str(Path(idrid_root) / "B. Disease Grading" /
                 "1. Original Images" / "a. Training Set"),
        labels_csv=str(Path(idrid_root) / "B. Disease Grading" / "2. Groundtruths" /
                       "a. IDRiD_Disease Grading_Training Labels.csv"),
        lesion_mask_dir=str(Path(idrid_root) / "A. Segmentation" /
                            "2. All Segmentation Groundtruths" / "a. Training Set"),
    )
    masked_indices = [i for i in range(len(idrid_ds))
                      if idrid_ds.get_lesion_masks(i) is not None]
    if args.limit:
        masked_indices = masked_indices[:args.limit]
    print(f"IDRiD: {len(idrid_ds)} graded images | "
          f"{len(masked_indices)} carry lesion masks → analysing all of them")

    # ── Models (already trained — no training here) ──────────────────────────
    pipeline_baseline = _build_pipeline(config, full=False, is_training=False)
    pipeline_full = _build_pipeline(config, full=True, is_training=False)
    model_baseline = _load_trained_model(config, "baseline", output_dir, device)
    model_full = _load_trained_model(config, "full_pipeline", output_dir, device)
    cam_baseline = GradCAMGenerator(
        model_baseline, get_gradcam_target_layer(model_baseline, variant="b4"),
        device=str(device))
    cam_full = GradCAMGenerator(
        model_full, get_gradcam_target_layer(model_full, variant="b4"),
        device=str(device))

    # ── Per-image Grad-CAM + ALO/IoU ─────────────────────────────────────────
    per_image: list[dict[str, Any]] = []
    for n_done, idx in enumerate(masked_indices, start=1):
        stem = idrid_ds.image_stems[idx]
        raw = cv2.imread(str(idrid_ds.image_paths[idx]))
        if raw is None:
            print(f"  WARNING: could not read {idrid_ds.image_paths[idx]}")
            continue
        masks = idrid_ds.get_lesion_masks(idx) or {}
        img_base = pipeline_baseline(raw)
        img_full = pipeline_full(raw)
        hm_base = cam_baseline.generate(_image_to_tensor(img_base, device),
                                        target_class=None)
        hm_full = cam_full.generate(_image_to_tensor(img_full, device),
                                    target_class=None)
        entry = {
            "image": stem,
            "dr_grade": int(idrid_ds.labels[idx]),
            "has_lesion_masks": bool(masks),
            "lesion_types_present": sorted(masks.keys()),
            "baseline_iou": compute_iou_per_lesion_type(hm_base, masks),
            "preprocessed_iou": compute_iou_per_lesion_type(hm_full, masks),
            "baseline_alo": compute_alo_per_lesion_type(hm_base, masks),
            "preprocessed_alo": compute_alo_per_lesion_type(hm_full, masks),
            "attention_overlap": compute_attention_overlap(hm_full, hm_base),
        }
        # Threshold sensitivity: ALO/IoU binarise the heatmap at a fixed 0.5 by
        # default. Lesions are small, so a null result must be shown not to be
        # an artefact of that one threshold.
        entry["by_threshold"] = {
            f"{thr:g}": {
                "baseline_alo": compute_alo_per_lesion_type(hm_base, masks, thr),
                "preprocessed_alo": compute_alo_per_lesion_type(hm_full, masks, thr),
                "baseline_iou": compute_iou_per_lesion_type(hm_base, masks, thr),
                "preprocessed_iou": compute_iou_per_lesion_type(hm_full, masks, thr),
            }
            for thr in thresholds
        }
        per_image.append(entry)

        if not args.no_figures:
            if isinstance(img_base, torch.Tensor):
                ph, pw = int(img_base.shape[-2]), int(img_base.shape[-1])
            else:
                ph, pw = img_base.shape[:2]
            create_comparison_figure(
                image=cv2.resize(raw, (pw, ph)),
                heatmap_baseline=hm_base,
                heatmap_preproc=hm_full,
                lesion_masks=masks,
                save_path=fig_dir / f"{stem}_comparison.png",
            )
        print(f"  [{n_done}/{len(masked_indices)}] {stem} grade="
              f"{entry['dr_grade']} types={len(masks)} "
              f"attn={entry['attention_overlap']:.3f}", flush=True)

    # ── Paired statistics per lesion type ────────────────────────────────────
    stats: dict[str, dict[str, Any]] = {}
    for metric, base_key, prep_key in (("alo", "baseline_alo", "preprocessed_alo"),
                                       ("iou", "baseline_iou", "preprocessed_iou")):
        stats[metric] = {}
        for lt in _LESION_TYPES:
            pairs = [(r[base_key][lt], r[prep_key][lt]) for r in per_image
                     if lt in r[base_key] and lt in r[prep_key]]
            if not pairs:
                continue
            stats[metric][lt] = _paired_stats([b for b, _ in pairs],
                                              [p for _, p in pairs], seed=seed)

    # Same paired comparison at every threshold — is the verdict threshold-stable?
    thr_sensitivity: dict[str, Any] = {}
    for thr in thresholds:
        key = f"{thr:g}"
        per_type: dict[str, Any] = {}
        for lt in _LESION_TYPES:
            pairs = [(r["by_threshold"][key]["baseline_alo"][lt],
                      r["by_threshold"][key]["preprocessed_alo"][lt])
                     for r in per_image
                     if lt in r["by_threshold"][key]["baseline_alo"]]
            if not pairs:
                continue
            per_type[lt] = _paired_stats([b for b, _ in pairs],
                                         [p for _, p in pairs], seed=seed)
        improved = [lt for lt, s in per_type.items() if s["mean_difference"] > 0]
        signif = [lt for lt, s in per_type.items()
                  if s.get("wilcoxon_p") is not None and s["wilcoxon_p"] < 0.05]
        thr_sensitivity[key] = {
            "alo_per_lesion_type": per_type,
            "lesion_types_improved": improved,
            "lesion_types_significant_p05": signif,
            "h5_alo_supported": len(improved) >= 3,
        }

    improved_alo = [lt for lt, s in stats["alo"].items() if s["mean_difference"] > 0]
    improved_iou = [lt for lt, s in stats["iou"].items() if s["mean_difference"] > 0]
    signif_alo = [lt for lt, s in stats["alo"].items()
                  if s.get("wilcoxon_p") is not None and s["wilcoxon_p"] < 0.05]

    results = {
        "per_image": per_image,
        "summary": {
            "n_images_analysed": len(per_image),
            "n_images_with_masks": len(per_image),
            "mean_alo_baseline": {lt: s["mean_baseline"]
                                  for lt, s in stats["alo"].items()},
            "mean_alo_preprocessed": {lt: s["mean_preprocessed"]
                                      for lt, s in stats["alo"].items()},
            "mean_iou_baseline": {lt: s["mean_baseline"]
                                  for lt, s in stats["iou"].items()},
            "mean_iou_preprocessed": {lt: s["mean_preprocessed"]
                                      for lt, s in stats["iou"].items()},
            "lesion_types_improved_alo": improved_alo,
            "lesion_types_improved_iou": improved_iou,
            "lesion_types_significant_alo_p05": signif_alo,
            "h5_alo_supported": len(improved_alo) >= 3,
            "h5_supported": len(improved_iou) >= 3,
            "h5_alo_significant": len(signif_alo) >= 3,
            "paired_stats": stats,
            "threshold_sensitivity_alo": thr_sensitivity,
            "provenance": (
                "Eval-only re-run over ALL IDRiD grading images carrying lesion "
                "masks; models loaded from outputs/exp4/checkpoints/*/best_model.pt. "
                "Supersedes iou_results.json, whose sample intersected the "
                "segmentation set on only 5 images."
            ),
            "nc14_note": (
                "Grad-CAM activation does NOT constitute clinical localization of "
                "pathology (INVARIANTS NC-14). Interpretability evidence only."
            ),
        },
    }

    out_path = output_dir / f"{args.out_name}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False,
                  default=lambda x: float(x) if isinstance(x, np.floating) else x)

    print(f"\n{'='*72}\nExp-4 re-analysis — {len(per_image)} images WITH masks\n{'='*72}")
    for metric in ("alo", "iou"):
        print(f"\n  {metric.upper()} (baseline → preprocessed, paired):")
        for lt, s in stats[metric].items():
            ci = s.get("ci95_difference")
            ci_s = f"[{ci[0]:+.5f}, {ci[1]:+.5f}]" if ci else "—"
            p = s.get("wilcoxon_p")
            p_s = f"p={p:.4g}" if p is not None else "p=—"
            print(f"    {lt:<16} n={s['n_images']:>3}  "
                  f"{s['mean_baseline']:.5f} → {s['mean_preprocessed']:.5f}  "
                  f"Δ={s['mean_difference']:+.5f}  CI95 {ci_s}  {p_s}  "
                  f"(↑{s['n_improved']}/↓{s['n_worse']}/={s['n_tied']})")
    print("\n  Threshold sensitivity (ALO, lesion types improved / significant):")
    for key, s in thr_sensitivity.items():
        print(f"    thr={key:<4} improved {len(s['lesion_types_improved'])}/4 "
              f"· significant {len(s['lesion_types_significant_p05'])}/4 "
              f"· h5_alo_supported={s['h5_alo_supported']}")
    print(f"\n  ALO improved on {len(improved_alo)}/4 lesion types "
          f"(significant at p<0.05: {len(signif_alo)}/4)")
    print(f"  Results → {out_path}")


if __name__ == "__main__":
    main()
