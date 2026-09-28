"""Slide 20: training set-up — focal loss (γ = 2 vs cross-entropy) and 5-fold patient-level cross-validation, kk/ru/en.

Content: CLAUDE.md (focal loss γ = 2, α = inverse class frequency; 5-fold patient-level stratified CV).
The metric definitions are formulas on the slide itself. Replaces a23_1 … a23_5: the worked F1 / κ example (a23_3) and
the G scale with the old numbers (a23_4, baseline G = 0.82 «fail» — results/ gives 0.858, it passes) are dropped;
the ALO sketch moved to slide 25.
Run: python make_training.py  ->  training_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import BLUE, GRAY, INK, INK2, LANGS, clean, commas, save  # noqa: E402

VAL = "#e08a2c"
T = {"kk": (r"Focal loss: FL = $-\alpha\,(1-p)^{\gamma}\,\log p$", "дұрыс класс ықтималдығы p", "шығын", "γ = 0 (кросс-энтропия)",
            "γ = 2 (осы жұмыс)", "жеңіл мысалдардың салмағы төмендейді", "5 фолд, пациент деңгейінде",
            "фолд", "пациент топтары", "оқыту", "валидация"),
     "ru": (r"Focal loss: FL = $-\alpha\,(1-p)^{\gamma}\,\log p$", "вероятность верного класса p", "потеря", "γ = 0 (кросс-энтропия)",
            "γ = 2 (в работе)", "лёгкие примеры получают меньший вес", "5 фолдов на уровне пациента",
            "фолд", "группы пациентов", "обучение", "валидация"),
     "en": (r"Focal loss: FL = $-\alpha\,(1-p)^{\gamma}\,\log p$", "probability of the true class p", "loss", "γ = 0 (cross-entropy)",
            "γ = 2 (this work)", "easy examples are down-weighted", "5 folds at the patient level",
            "fold", "patient groups", "training", "validation")}


def main() -> None:
    """Write training_{lang}.png: loss curves (left) and the fold scheme (right)."""
    p = np.linspace(0.01, 1, 400)
    for lang in LANGS:
        t = T[lang]
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={"width_ratios": [1.1, 1]})
        a1.plot(p, -np.log(p), color=GRAY, lw=2.2, ls="--", label=t[3])
        a1.plot(p, -(1 - p) ** 2 * np.log(p), color=BLUE, lw=2.6, label=t[4])
        a1.annotate(t[5], xy=(0.75, 0.02), xytext=(0.45, 1.6), fontsize=11, color=INK,
                    arrowprops=dict(arrowstyle="-|>", color=INK2))
        a1.set_xlabel(t[1])
        a1.set_ylabel(t[2])
        a1.set_ylim(0, 4)
        a1.set_title(t[0], fontsize=13, color=INK)
        a1.legend(frameon=False, fontsize=11)
        clean(a1)
        commas(a1, lang, 1, "xy")
        for f in range(5):
            for g in range(5):
                a2.add_patch(plt.Rectangle((g + 0.06, -f - 0.9), 0.88, 0.8, color=VAL if f == g else "#2e9e6b"))
            a2.text(-0.1, -f - 0.5, f"{t[7]} {f + 1}", ha="right", va="center", fontsize=11.5, color=INK)
        a2.text(2.5, 0.3, t[8], ha="center", fontsize=11.5, color=INK2)
        for i, (col, lab) in enumerate((("#2e9e6b", t[9]), (VAL, t[10]))):
            a2.add_patch(plt.Rectangle((i * 2.6, -5.85), 0.3, 0.3, color=col))
            a2.text(i * 2.6 + 0.42, -5.7, lab, va="center", fontsize=11, color=INK)
        a2.set_xlim(-1.4, 5.1)
        a2.set_ylim(-6.1, 0.9)
        a2.axis("off")
        a2.set_title(t[6], fontsize=13, color=INK)
        fig.tight_layout(w_pad=2)
        save(fig, HERE / f"training_{lang}.png")


if __name__ == "__main__":
    main()
