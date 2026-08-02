"""Paired significance tests on Exp-1's LABEL metrics (G-11).

`TAB-5.1` already establishes significance for the *ranking* metric (DeLong on
referable ROC-AUC) and for raw agreement (McNemar). H-1 is however worded over
the whole metric list — accuracy, precision/recall, macro and weighted F1,
ROC-AUC, quadratic kappa — and the dominance criterion is stated on **weighted
F1**, for which no paired test existed. This script supplies it.

Method: paired bootstrap over the shared validation samples. The integrated arm
(B/D) and the baseline arm (A/C) were both re-inferred on the *same* images in
the same fold order, so each resample draws one index set and scores both arms
on it; the statistic is the per-resample difference. Reported per comparison:
observed Δ, bootstrap mean Δ, 95% CI, and a one-sided p (fraction of resamples
with Δ ≤ 0, i.e. evidence against "integrated > baseline"). Holm-Bonferroni is
applied across the whole family of tests.

Caveat recorded in the output: resampling is at IMAGE level (predictions.npz
carries no patient ids), so CIs are mildly anti-conservative for the two-eyes
-per-patient correlation.

Usage:
    python scripts/exp1_f1_significance.py --pred outputs/exp1/predictions.npz
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

import numpy as np
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.evaluation.statistical_tests import holm_bonferroni_correction  # noqa: E402

_COMPARISONS: list[tuple[str, str, str]] = [
    ("B", "A", "ResNet-50: integrated vs baseline"),
    ("D", "C", "EfficientNet-B3: integrated vs baseline"),
]

_METRICS: dict[str, Callable[[np.ndarray, np.ndarray], float]] = {
    "weighted_f1": lambda yt, yp: float(f1_score(yt, yp, average="weighted",
                                                 zero_division=0)),
    "macro_f1": lambda yt, yp: float(f1_score(yt, yp, average="macro",
                                              zero_division=0)),
    "accuracy": lambda yt, yp: float(accuracy_score(yt, yp)),
    "kappa_quadratic": lambda yt, yp: float(cohen_kappa_score(yt, yp,
                                                              weights="quadratic")),
}


def _config_arrays(data: Any, cfg: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (y_true, y_pred, fold) for a config, whatever layout it was dumped in.

    Configs A and C were dumped pooled with a fold index; B and D per fold.

    Args:
        data: Loaded npz archive.
        cfg: Config letter ("A".."D").

    Returns:
        Tuple of (y_true, y_pred, fold) arrays covering all folds in fold order.

    Raises:
        KeyError: If the config is absent from the archive.
    """
    if f"{cfg}_y_true" in data.files:
        return data[f"{cfg}_y_true"], data[f"{cfg}_y_pred"], data[f"{cfg}_fold"]
    yt, yp, fo = [], [], []
    for f in range(5):
        key = f"{cfg}_f{f}_y_true"
        if key not in data.files:
            continue
        yt.append(data[key])
        yp.append(data[f"{cfg}_f{f}_y_pred"])
        fo.append(np.full(len(data[key]), f, dtype=np.int64))
    if not yt:
        raise KeyError(f"config {cfg} not found in archive")
    return np.concatenate(yt), np.concatenate(yp), np.concatenate(fo)


def _paired_bootstrap(
    y_true: np.ndarray,
    y_pred_a: np.ndarray,
    y_pred_b: np.ndarray,
    metric: Callable[[np.ndarray, np.ndarray], float],
    n_boot: int,
    seed: int,
) -> dict[str, Any]:
    """Paired bootstrap of metric(b) − metric(a) on shared samples.

    Args:
        y_true: Shared ground truth, shape (N,).
        y_pred_a: Baseline-arm predictions, shape (N,).
        y_pred_b: Integrated-arm predictions, shape (N,).
        metric: Callable(y_true, y_pred) → float.
        n_boot: Number of bootstrap resamples.
        seed: RNG seed.

    Returns:
        Dict with observed metrics, observed and bootstrap-mean difference,
        95% CI of the difference, and the one-sided p-value.
    """
    obs_a = metric(y_true, y_pred_a)
    obs_b = metric(y_true, y_pred_b)
    rng = np.random.default_rng(seed)
    n = len(y_true)
    diffs = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        diffs[i] = metric(yt, y_pred_b[idx]) - metric(yt, y_pred_a[idx])
    # One-sided: H1 = integrated > baseline. p = P(bootstrap Δ ≤ 0).
    p_one_sided = float((diffs <= 0).mean())
    return {
        "metric_baseline": round(obs_a, 6),
        "metric_integrated": round(obs_b, 6),
        "difference_observed": round(obs_b - obs_a, 6),
        "difference_bootstrap_mean": round(float(diffs.mean()), 6),
        "ci95": [round(float(np.percentile(diffs, 2.5)), 6),
                 round(float(np.percentile(diffs, 97.5)), 6)],
        "p_one_sided": p_one_sided,
        "n_samples": int(n),
        "n_bootstrap": int(n_boot),
    }


def main() -> None:
    """Run the paired label-metric tests and write JSON + Markdown."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pred", type=Path,
                        default=Path("outputs/exp1/predictions.npz"))
    parser.add_argument("--out", type=Path,
                        default=Path("outputs/exp1/f1_significance"),
                        help="Output stem (writes .json and .md)")
    parser.add_argument("--n-boot", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    data = np.load(args.pred, allow_pickle=True)
    arrays = {cfg: _config_arrays(data, cfg) for cfg in "ABCD"}

    results: dict[str, Any] = {"pooled": {}, "per_fold": {}, "alignment": {}}
    p_index: list[tuple[str, str]] = []
    p_values: list[float] = []

    for hi, lo, label in _COMPARISONS:
        yt_hi, yp_hi, fo_hi = arrays[hi]
        yt_lo, yp_lo, fo_lo = arrays[lo]

        # The two arms must be sample-aligned for a paired test. Both dumps walk
        # the same PatientLevelKFold splits, so verify rather than assume.
        aligned = (yt_hi.shape == yt_lo.shape
                   and bool(np.array_equal(yt_hi, yt_lo))
                   and bool(np.array_equal(fo_hi, fo_lo)))
        results["alignment"][f"{hi}_vs_{lo}"] = {
            "sample_aligned": aligned,
            "n": int(len(yt_hi)),
        }
        if not aligned:
            print(f"  !! {hi} vs {lo}: samples NOT aligned — skipping paired test")
            continue

        print(f"\n{label}  ({hi} vs {lo}, n={len(yt_hi)})")
        results["pooled"][f"{hi}_vs_{lo}"] = {"label": label, "metrics": {}}
        for m_name, m_fn in _METRICS.items():
            res = _paired_bootstrap(yt_hi, yp_lo, yp_hi, m_fn,
                                    args.n_boot, args.seed)
            results["pooled"][f"{hi}_vs_{lo}"]["metrics"][m_name] = res
            p_index.append((f"{hi}_vs_{lo}", m_name))
            p_values.append(res["p_one_sided"])
            print(f"  {m_name:<16} {res['metric_baseline']:.4f} → "
                  f"{res['metric_integrated']:.4f}  Δ={res['difference_observed']:+.4f}  "
                  f"CI95 [{res['ci95'][0]:+.4f}, {res['ci95'][1]:+.4f}]  "
                  f"p={res['p_one_sided']:.4g}")

        # Per-fold Δ (5 paired observations) — the cross-validation view.
        per_fold: dict[str, list[float]] = {m: [] for m in _METRICS}
        for f in sorted(set(fo_hi.tolist())):
            sel = fo_hi == f
            for m_name, m_fn in _METRICS.items():
                per_fold[m_name].append(
                    round(m_fn(yt_hi[sel], yp_hi[sel])
                          - m_fn(yt_lo[sel], yp_lo[sel]), 6))
        results["per_fold"][f"{hi}_vs_{lo}"] = {
            m: {"deltas": v,
                "n_folds_positive": int(sum(1 for x in v if x > 0)),
                "mean": round(float(np.mean(v)), 6)}
            for m, v in per_fold.items()
        }

    holm = holm_bonferroni_correction(p_values) if p_values else []
    results["holm_bonferroni"] = [
        {"comparison": c, "metric": m, **h}
        for (c, m), h in zip(p_index, holm)
    ]
    results["_meta"] = {
        "source": str(args.pred),
        "test": "paired bootstrap over shared validation samples; one-sided "
                "H1 = integrated > baseline; Holm-Bonferroni across the family",
        "caveat": "resampling is at IMAGE level (predictions.npz carries no "
                  "patient ids); CIs are mildly anti-conservative w.r.t. the "
                  "two-eyes-per-patient correlation",
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    lines = [
        "# Exp-1 — paired significance on label metrics (G-11)",
        "",
        f"Source: `{args.pred}` · paired bootstrap, {args.n_boot} resamples, "
        "one-sided H1 = integrated > baseline, Holm-Bonferroni across the family.",
        "",
        "| Comparison | Metric | Baseline | Integrated | Δ | 95% CI (Δ) | p | p (Holm) | signif. |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    holm_map = {(r["comparison"], r["metric"]): r for r in results["holm_bonferroni"]}
    for key, block in results["pooled"].items():
        for m_name, r in block["metrics"].items():
            h = holm_map.get((key, m_name), {})
            lines.append(
                f"| {key.replace('_vs_', ' vs ')} | {m_name} | "
                f"{r['metric_baseline']:.4f} | {r['metric_integrated']:.4f} | "
                f"{r['difference_observed']:+.4f} | "
                f"[{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}] | "
                f"{r['p_one_sided']:.4g} | {h.get('adjusted_p', float('nan')):.4g} | "
                f"{'**yes**' if h.get('significant') else 'no'} |")
    lines += ["", "Per-fold deltas (5 paired CV observations):", ""]
    for key, block in results["per_fold"].items():
        for m_name, r in block.items():
            lines.append(f"- `{key}` {m_name}: {r['deltas']} · "
                         f"positive in {r['n_folds_positive']}/5 folds · "
                         f"mean {r['mean']:+.4f}")
    lines += ["", f"Caveat: {results['_meta']['caveat']}."]
    with open(args.out.with_suffix(".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nSaved: {args.out.with_suffix('.json')} and {args.out.with_suffix('.md')}")


if __name__ == "__main__":
    main()
