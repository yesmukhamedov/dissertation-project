"""Slide 27: experiment 6 — weighted F1 by camera group and the spread between groups, kk/ru/en.

Numbers: results/tables/TAB-4.9_exp6_device.md (wF1 (C), wF1 (D) per group; between-group std of wF1 and ROC-AUC).
Groups ordered by the baseline wF1 (weakest first). Replaces a29_1 (old run: σ² −46 %, «H-6» in the title, EyePACS drawn
as a camera group).
Run: python make_exp6.py  ->  exp6_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ARM, BLUE, GRAY, INK, INK2, LANGS, WF1, clean, commas, dec, md_table, num, save  # noqa: E402

MIXED = {"kk": "аралас", "ru": "смешанные", "en": "mixed"}
T = {"kk": "Топтар арасындағы шашырау (std):", "ru": "Разброс между группами (std):", "en": "Spread between groups (std):"}


def label(group: str, lang: str) -> str:
    """'mixed_rfmid' → 'аралас\\n(RFMiD)', 'kowa_idrid' → 'Kowa\\n(IDRiD)'."""
    cam, corp = group.split("_")
    corp = {"idrid": "IDRiD", "ddr": "DDR", "odir5k": "ODIR-5K", "messidor2": "Messidor-2", "rfmid": "RFMiD"}[corp]
    return f"{MIXED[lang] if cam == 'mixed' else cam.capitalize()}\n({corp})"


def main() -> None:
    """Write exp6_{lang}.png."""
    rows = sorted(md_table("TAB-4.9_exp6_device.md", "Camera group"), key=lambda r: num(r["wF1 (C)"]))
    sp = {r["Quantity"]: r for r in md_table("TAB-4.9_exp6_device.md", "Quantity")}
    f1, auc = sp["std (wF1, 5 groups)"], sp["std (ROC-AUC, 5 groups)"]
    for lang in LANGS:
        fig, ax = plt.subplots(figsize=(11, 4.9))
        x = np.arange(len(rows))
        c, d = [num(r["wF1 (C)"]) for r in rows], [num(r["wF1 (D)"]) for r in rows]
        ax.bar(x - 0.19, c, 0.36, color=GRAY, label=ARM[lang][0])
        ax.bar(x + 0.19, d, 0.36, color=BLUE, label=ARM[lang][1])
        for i in x:
            ax.text(i - 0.19, c[i] + 0.012, dec(c[i], lang), ha="center", fontsize=10.5, color=INK2)
            ax.text(i + 0.19, d[i] + 0.012, dec(d[i], lang), ha="center", fontsize=10.5, color=INK)
        ax.set_xticks(x, [label(r["Camera group"], lang) for r in rows], fontsize=11)
        ax.set_ylim(0, 0.9)
        ax.set_ylabel(WF1[lang])
        ax.legend(frameon=False, loc="upper left", ncol=2, fontsize=11)
        ax.text(0.99, 0.97, f"{T[lang]}\nF1: {dec(num(f1['C']), lang, 4)} → {dec(num(f1['D']), lang, 4)}"
                f"\nAUC: {dec(num(auc['C']), lang, 4)} → {dec(num(auc['D']), lang, 4)}", transform=ax.transAxes,
                ha="right", va="top", fontsize=11.5, color=INK)
        clean(ax)
        commas(ax, lang)
        fig.tight_layout()
        save(fig, HERE / f"exp6_{lang}.png")


if __name__ == "__main__":
    main()
