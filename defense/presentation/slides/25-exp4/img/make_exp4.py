"""Slide 25: experiment 4 — ALO by lesion type, baseline vs integrated arm, with the ALO definition, kk/ru/en.

Numbers: results/tables/TAB-4.7_exp4_alo_iou.md (ALO table, τ = 0.5: ALO (C), ALO (D), Δ, p).
Replaces a27_1 (old run, +31…+61 %) and a27_3 (cross-corpus attention consistency — never measured); the ALO sketch
from slide 20 (a23_5, English) is redrawn here as a small inset.
Run: python make_exp4.py  ->  exp4_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ARM, BLUE, GRAY, INK, INK2, LANGS, clean, commas, dec, md_table, num, save  # noqa: E402

TYPES = {"kk": ["Микро-\nаневризмалар", "Қанталаулар", "Қатты\nэкссудаттар", "Жұмсақ\nэкссудаттар"],
         "ru": ["Микро-\nаневризмы", "Кровоизлияния", "Твёрдые\nэкссудаты", "Мягкие\nэкссудаты"],
         "en": ["Micro-\naneurysms", "Haemorrhages", "Hard\nexudates", "Soft\nexudates"]}
T = {"kk": ("ALO, τ = 0,5 (IDRiD, n = 26–54)", "A — Grad-CAM назары\nL — зақымдану маскасы", "ALO = |A ∩ L| / |L|"),
     "ru": ("ALO, τ = 0,5 (IDRiD, n = 26–54)", "A — внимание Grad-CAM\nL — маска поражения", "ALO = |A ∩ L| / |L|"),
     "en": ("ALO, τ = 0.5 (IDRiD, n = 26–54)", "A — Grad-CAM attention\nL — lesion mask", "ALO = |A ∩ L| / |L|")}


def main() -> None:
    """Write exp4_{lang}.png: grouped ALO bars and the definition sketch."""
    rows = md_table("TAB-4.7_exp4_alo_iou.md", "Lesion type", 0)
    c, d = [num(r["ALO (C)"]) for r in rows], [num(r["ALO (D)"]) for r in rows]
    p = [num(r["p (Wilcoxon, 1-sided)"]) for r in rows]
    for lang in LANGS:
        t = T[lang]
        fig = plt.figure(figsize=(13, 5))
        ax = fig.add_axes([0.06, 0.17, 0.6, 0.72])
        x = np.arange(4)
        ax.bar(x - 0.19, c, 0.36, color=GRAY, label=ARM[lang][0])
        ax.bar(x + 0.19, d, 0.36, color=BLUE, label=ARM[lang][1])
        for i in x:
            ax.text(i - 0.19, c[i] + 0.01, dec(c[i], lang, 2), ha="center", fontsize=11, color=INK2)
            ax.text(i + 0.19, d[i] + 0.01, dec(d[i], lang, 2), ha="center", fontsize=11, color=INK)
            ax.text(i, d[i] + 0.07, f"+{dec(d[i] - c[i], lang)}\np = {dec(p[i], lang, 4)}", ha="center", fontsize=10.5,
                    color=BLUE)
        ax.set_xticks(x, TYPES[lang], fontsize=11)
        ax.set_ylim(0, 0.65)
        ax.set_title(t[0], fontsize=13, color=INK)
        ax.legend(frameon=False, loc="upper left", fontsize=11)
        clean(ax)
        commas(ax, lang)
        s = fig.add_axes([0.72, 0.3, 0.24, 0.55])
        s.add_patch(Circle((0.42, 0.5), 0.3, color="#f0b4a8", alpha=0.8))
        s.add_patch(Circle((0.68, 0.5), 0.2, fill=False, ec="#1f6b45", lw=2.5))
        s.text(0.2, 0.86, "A", fontsize=15, color="#c8442a", fontweight="bold")
        s.text(0.84, 0.72, "L", fontsize=15, color="#1f6b45", fontweight="bold")
        s.set_xlim(0, 1)
        s.set_ylim(0, 1)
        s.set_aspect("equal")
        s.axis("off")
        fig.text(0.84, 0.2, t[2], ha="center", fontsize=14, color=INK, fontweight="bold")
        fig.text(0.84, 0.07, t[1], ha="center", fontsize=11, color=INK2)
        save(fig, HERE / f"exp4_{lang}.png")


if __name__ == "__main__":
    main()
