"""Category B — turn exp1 predictions.npz into dissertation result tables.

Consumes the ``predictions.npz`` written by ``dump_exp1_predictions.py`` and
computes, per config (A–D), the quantities the training run did NOT save:
  - per-class F1/precision/recall + confusion matrix (TAB-4.6-style, exp1)
  - calibration: ECE + Brier (TAB-4.3)
  - clinical referable-DR: Sensitivity/Specificity/PPV/NPV + referable AUC (TAB-5.4 in-domain)
  - bootstrap 95% CI on weighted-F1
  - paired tests B-vs-A and D-vs-C: DeLong (referable AUC) + McNemar (TAB-5.1)

Writes Markdown tables to --out-dir (default ../results/tables).

Usage (after dump, on any machine — this step is CPU-only and fast):
    python scripts/analyze_exp1_predictions.py --pred outputs/exp1/predictions.npz
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # experiments/ root

from src.evaluation.metrics import (
    compute_primary_metrics,
    compute_secondary_metrics,
    compute_clinical_metrics,
)
from src.evaluation.calibration import compute_ece, compute_brier_score
from src.evaluation.statistical_tests import mcnemar_test, delong_test, bootstrap_ci

_LABELS = {"A": "baseline+ResNet-50", "B": "pipeline+ResNet-50",
           "C": "baseline+EffNet-B3", "D": "pipeline+EffNet-B3"}


def _referable_auc(y_true, y_prob):
    y_bin = (y_true >= 2).astype(int)
    ref = y_prob[:, 2:].sum(axis=1)
    try:
        return float(roc_auc_score(y_bin, ref))
    except ValueError:
        return float("nan")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", nargs="+", default=["outputs/exp1/predictions.npz"],
                    help="one or more predictions.npz files; config keys are merged across files "
                         "(e.g. pred_AC.npz pred_B.npz pred_D.npz)")
    ap.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[2] / "results" / "tables"))
    ap.add_argument("--tag", default="", help="suffix for output filenames (e.g. _smoke)")
    args = ap.parse_args()

    d: dict[str, np.ndarray] = {}
    for pth in args.pred:
        npz = np.load(pth)
        for k in npz.files:
            d[k] = npz[k]

    def config_arrays(cfg):
        """Return (y_true, y_pred, y_prob) for a config, handling both storage schemas:
        legacy per-config keys (`A_y_true`) OR per-fold keys (`A_f0_y_true`, ...)."""
        if f"{cfg}_y_true" in d:
            return d[f"{cfg}_y_true"], d[f"{cfg}_y_pred"], d[f"{cfg}_prob"]
        folds = sorted(int(kk[len(cfg) + 2:-len("_y_true")])
                       for kk in d if kk.startswith(f"{cfg}_f") and kk.endswith("_y_true"))
        if not folds:
            return None
        yt = np.concatenate([d[f"{cfg}_f{f}_y_true"] for f in folds])
        yp = np.concatenate([d[f"{cfg}_f{f}_y_pred"] for f in folds])
        pr = np.concatenate([d[f"{cfg}_f{f}_prob"] for f in folds])
        return yt, yp, pr

    keys = [k for k in ("A", "B", "C", "D") if config_arrays(k) is not None]
    print(f"Configs across {len(args.pred)} file(s): {keys}")
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    per: dict[str, dict] = {}
    for k in keys:
        yt, yp, pr = config_arrays(k)
        prim = compute_primary_metrics(yt, yp, pr)
        sec = compute_secondary_metrics(yt, yp)
        clin = compute_clinical_metrics(yt, yp)
        clin["referable_auc"] = _referable_auc(yt, pr)
        ece = compute_ece(yt, pr); brier = compute_brier_score(yt, pr)
        boot = bootstrap_ci(yt, yp)
        per[k] = dict(prim=prim, sec=sec, clin=clin, ece=ece, brier=brier, boot=boot, n=len(yt),
                      yt=yt, yp=yp, pr=pr)
        print(f"  {k}: n={len(yt)} wF1={prim['weighted_f1']:.4f} ECE={ece:.4f} Brier={brier:.4f}")

    def w(name, text):
        p = out_dir / f"{name}{args.tag}.md"; p.write_text(text, encoding="utf-8")
        print(f"  wrote {p}")

    # ── Per-class F1/precision/recall ──────────────────────────────────────────
    lines = ["# exp1 per-class metrics (Category B — из predictions.npz)\n",
             "Реальные per-class F1/precision/recall на объединённых val-фолдах.\n"]
    for k in keys:
        s = per[k]["sec"]
        lines.append(f"\n## Config {k} ({_LABELS[k]}), n={per[k]['n']}\n")
        lines.append("| Класс | F1 | Precision | Recall |\n|---|---|---|---|")
        for c in range(5):
            lines.append(f"| {c} | {s['per_class_f1'][c]:.3f} | {s['per_class_precision'][c]:.3f} | {s['per_class_recall'][c]:.3f} |")
        lines.append(f"\nmacro-F1 = {s['macro_f1']:.4f}. Матрица ошибок:\n")
        lines.append("| ист\\пред | 0 | 1 | 2 | 3 | 4 |\n|---|---|---|---|---|---|")
        for i, row in enumerate(s["confusion_matrix"]):
            lines.append(f"| {i} | " + " | ".join(str(x) for x in row) + " |")
    w("exp1_per_class", "\n".join(lines) + "\n")

    # ── Calibration TAB-4.3 ────────────────────────────────────────────────────
    lines = ["# TAB-4.3 — exp1 калибровка (ECE, Brier) (Category B)\n",
             "| Config | Арм | ECE | Brier |\n|---|---|---|---|"]
    for k in keys:
        lines.append(f"| {k} | {_LABELS[k]} | {per[k]['ece']:.4f} | {per[k]['brier']:.4f} |")
    w("TAB-4.3_exp1_calibration", "\n".join(lines) + "\n")

    # ── Clinical in-domain (completes TAB-5.4 B3) ──────────────────────────────
    lines = ["# exp1 in-domain клинические метрики (referable≥2) (Category B — B3)\n",
             "| Config | Sensitivity | Specificity | PPV | NPV | Referable AUC |\n|---|---|---|---|---|---|"]
    for k in keys:
        c = per[k]["clin"]
        lines.append(f"| {k} | {c['sensitivity']:.3f} | {c['specificity']:.3f} | {c['ppv']:.3f} | {c['npv']:.3f} | {c['referable_auc']:.3f} |")
    w("exp1_clinical_indomain", "\n".join(lines) + "\n")

    # ── Statistical tests TAB-5.1 ──────────────────────────────────────────────
    lines = ["# TAB-5.1 — exp1 статистические тесты (Category B)\n",
             "Bootstrap 95% CI (weighted-F1, 1000 итер.) по конфигам:\n",
             "| Config | wF1 mean | 95% CI | std |\n|---|---|---|---|"]
    for k in keys:
        b = per[k]["boot"]
        lines.append(f"| {k} | {b['mean']:.4f} | [{b['ci_lower']:.4f}, {b['ci_upper']:.4f}] | {b['std']:.4f} |")
    lines.append("\n## Парные тесты (та же val-выборка по фолдам)\n")
    lines.append("| Пара | DeLong ΔAUC (referable) | z | p | McNemar b/c | McNemar p |\n|---|---|---|---|---|---|")
    for a, b in [("B", "A"), ("D", "C")]:
        if a in per and b in per:
            ya, yb = per[a]["yt"], per[b]["yt"]
            if len(ya) == len(yb) and np.array_equal(ya, yb):
                dl = delong_test(ya, per[a]["pr"], per[b]["pr"])
                mc = mcnemar_test(ya, per[a]["yp"], per[b]["yp"])
                lines.append(f"| {a} vs {b} | {dl['auc_diff']:+.4f} | {dl['z_statistic']} | {dl['p_value']} | {mc['b']}/{mc['c']} | {mc['p_value']} |")
            else:
                lines.append(f"| {a} vs {b} | НЕ ВЫРОВНЕНЫ (разные val-порядки) — пропуск | | | | |")
    lines.append("\n> DeLong тестирует разницу referable-AUC (grade≥2); McNemar — разницу доли верных предсказаний. "
                 "Пары B-vs-A и D-vs-C оцениваются на одной и той же val-выборке по фолдам (сплиты идентичны).")
    w("TAB-5.1_statistical", "\n".join(lines) + "\n")

    print("\nDone. Category-B tables written.")


if __name__ == "__main__":
    main()
