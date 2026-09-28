"""Slide 26: experiment 5 — weighted F1 on the external clinical corpora IDRiD and Messidor-2, kk/ru/en.

Numbers: results/tables/TAB-4.8_exp5_degradation.md (absolute performance: wF1 (C), wF1 (D), Δ, 95 % CI; MCID = 0.05).
Replaces a28_1 (old run, two small panels).
Run: python make_exp5.py  ->  exp5_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ARM, BLUE, GRAY, INK, INK2, LANGS, WF1, clean, commas, dec, md_table, num, save  # noqa: E402

T = {"kk": ("Δ ≥ MCID = 0,05", "СА"), "ru": ("Δ ≥ MCID = 0,05", "ДИ"), "en": ("Δ ≥ MCID = 0.05", "CI")}


def main() -> None:
    """Write exp5_{lang}.png."""
    rows = md_table("TAB-4.8_exp5_degradation.md", "Set", 0)
    for lang in LANGS:
        fig, ax = plt.subplots(figsize=(8.5, 4.9))
        x = np.arange(len(rows))
        for i, r in enumerate(rows):
            c, d = num(r["wF1 (C)"]), num(r["wF1 (D)"])
            ax.bar(i - 0.19, c, 0.36, color=GRAY, label=ARM[lang][0] if i == 0 else None)
            ax.bar(i + 0.19, d, 0.36, color=BLUE, label=ARM[lang][1] if i == 0 else None)
            ax.text(i - 0.19, c + 0.012, dec(c, lang), ha="center", fontsize=12, color=INK2)
            ax.text(i + 0.19, d + 0.012, dec(d, lang), ha="center", fontsize=12, color=INK)
            lo, hi = [num(v) for v in r["95% CI (Δ)"].strip("[]").split(",")]
            ax.text(i, d + 0.1, f"Δ = +{dec(num(r['Δ (D − C)']), lang)}\n95 % {T[lang][1]} [{dec(lo, lang)}; {dec(hi, lang)}]",
                    ha="center", fontsize=11, color=BLUE)
        ax.set_xticks(x, [f"{r['Set']}\nn = {r['n']}" for r in rows])
        ax.set_ylim(0, 1.0)
        ax.set_ylabel(WF1[lang])
        ax.text(1.0, -0.2, T[lang][0], transform=ax.transAxes, ha="right", fontsize=11, color=INK2)
        ax.legend(frameon=False, loc="upper center", ncol=2, fontsize=11, bbox_to_anchor=(0.5, 1.08))
        clean(ax)
        commas(ax, lang)
        fig.tight_layout()
        save(fig, HERE / f"exp5_{lang}.png")


if __name__ == "__main__":
    main()
