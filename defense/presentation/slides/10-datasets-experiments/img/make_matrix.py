"""Slide 10: which corpus each experiment trains on and evaluates on — a 7 × 8 matrix, kk/ru/en.

Content: CLAUDE.md experiment table and the talk of slide 10; corpus sizes as in the table of slide 08. Rows are named by
what the experiment tests, without hypothesis codes (slide 03 does not introduce them); experiment 5 is external
clinical accuracy, not «degradation». Replaces a12_1.
Run: python make_matrix.py  ->  matrix_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import INK, INK2, LANGS, save  # noqa: E402

TRAIN, EVAL, EMPTY = "#2a78d6", "#2e9e6b", "#f1f0ed"
CORPORA = [("EyePACS", "35 126"), ("APTOS", "3 662"), ("IDRiD", "516"), ("Messidor-2", "1 748"), ("DDR", "13 673"),
           ("ODIR-5K", "~5 000"), ("RFMiD", "3 200"), ("KZ", "60")]
PLAN = [("T",), ("T",), ("T", "E"), ("T", None, "E"), ("T", None, "E", "E"), ("T", None, None, None, "E", "E", "E"),
        (None, None, "T", None, None, None, None, "E")]
ROWS = {"kk": ["артықшылық 2 × 2", "кезеңдер абляциясы", "басқа корпусқа тасымалдау", "назардың үйлесімі (ALO)",
               "сыртқы клиникалық дәлдік", "камераның ауысуы", "аз деректермен оқыту"],
        "ru": ["превосходство 2 × 2", "абляция этапов", "перенос на другой корпус", "согласованность внимания (ALO)",
               "внешняя клиническая точность", "смена камеры", "обучение на малых данных"],
        "en": ["superiority 2 × 2", "stage ablation", "transfer to another corpus", "attention alignment (ALO)",
               "external clinical accuracy", "camera shift", "small-data training"]}
LEG = {"kk": ("оқыту", "қайта оқытусыз тексеру"), "ru": ("обучение", "проверка без дообучения"),
       "en": ("training", "evaluation without fine-tuning")}
EXP = {"kk": "{}-эксп.", "ru": "Эксп. {}", "en": "Exp. {}"}


def main() -> None:
    """Write matrix_{lang}.png."""
    for lang in LANGS:
        fig, ax = plt.subplots(figsize=(13, 5.4))
        for r, plan in enumerate(PLAN):
            for c in range(len(CORPORA)):
                k = plan[c] if c < len(plan) else None
                col = {"T": TRAIN, "E": EVAL}.get(k, EMPTY)
                ax.add_patch(plt.Rectangle((c + 0.06, -r - 0.9), 0.88, 0.8, color=col))
            ax.text(-0.15, -r - 0.5, f"{EXP[lang].format(r + 1)}  {ROWS[lang][r]}", ha="right", va="center", fontsize=12,
                    color=INK)
        for c, (name, n) in enumerate(CORPORA):
            ax.text(c + 0.5, 0.45, name, ha="center", va="bottom", fontsize=10.5, color=INK, fontweight="bold")
            ax.text(c + 0.5, 0.12, f"n = {n}", ha="center", va="bottom", fontsize=9.5, color=INK2)
        for i, (col, lab) in enumerate(zip((TRAIN, EVAL), LEG[lang])):
            ax.add_patch(plt.Rectangle((i * 3.2, -8.0), 0.35, 0.35, color=col))
            ax.text(i * 3.2 + 0.5, -7.83, lab, va="center", fontsize=11.5, color=INK)
        ax.set_xlim(-5.6, len(CORPORA))
        ax.set_ylim(-8.3, 1.0)
        ax.axis("off")
        fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
        save(fig, HERE / f"matrix_{lang}.png")


if __name__ == "__main__":
    main()
