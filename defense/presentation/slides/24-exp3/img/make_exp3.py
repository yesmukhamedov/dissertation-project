"""Slide 24: experiment 3 — transfer EyePACS → APTOS 2019 without fine-tuning: weighted F1 and G, kk/ru/en.

Numbers: results/tables/TAB-4.6_exp3_transfer.md (in-domain and APTOS wF1, G per arm; Δ wF1 with 95 % CI).
Replaces a26_1 (old run) and a26_2 (G on IDRiD / Messidor-2 — experiment 5, old run, baseline shown failing the threshold
it actually clears).
Run: python make_exp3.py  ->  exp3_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ACCENT, ARM, BLUE, GRAY, INK, LANGS, WF1, clean, commas, dec, md_table, num, save  # noqa: E402

T = {"kk": ("Салмақталған F1", "EyePACS\n(өз домені)", "APTOS 2019\n(қайта оқытусыз)", "Жалпылау қатынасы G", "шек 0,85"),
     "ru": ("Взвешенный F1", "EyePACS\n(свой домен)", "APTOS 2019\n(без дообучения)", "Коэффициент обобщения G", "порог 0,85"),
     "en": ("Weighted F1", "EyePACS\n(own domain)", "APTOS 2019\n(no fine-tuning)", "Generalisation ratio G", "threshold 0.85")}


def main() -> None:
    """Write exp3_{lang}.png: grouped wF1 bars (left) and G per arm (right)."""
    rows = md_table("TAB-4.6_exp3_transfer.md", "Arm")
    c, d = rows[0], rows[1]
    ind = [num(c["In-domain wF1 (EyePACS)"]), num(d["In-domain wF1 (EyePACS)"])]
    apt = [num(c["APTOS wF1"]), num(d["APTOS wF1"])]
    g = [num(c["G"]), num(d["G"])]
    dlt = [r for r in md_table("TAB-4.6_exp3_transfer.md", "Metric") if r["Metric"] == "wF1"][0]
    for lang in LANGS:
        t = T[lang]
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [1.5, 1]})
        x = np.arange(2)
        for k, vals in enumerate(((ind[0], apt[0]), (ind[1], apt[1]))):
            xs = x + (k - 0.5) * 0.38
            a1.bar(xs, vals, 0.34, color=(GRAY, BLUE)[k], label=ARM[lang][k])
            for xx, v in zip(xs, vals):
                a1.text(xx, v + 0.015, dec(v, lang), ha="center", fontsize=12, color=INK)
        a1.text(1, 0.9, f"Δ = +{dec(num(dlt['Δ (D − C)']), lang)}", ha="center", fontsize=13, color=BLUE, fontweight="bold")
        a1.set_xticks(x, t[1:3])
        a1.set_ylim(0, 1.0)
        a1.set_title(t[0], fontsize=13, color=INK)
        a1.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=11)
        clean(a1)
        commas(a1, lang)
        a2.bar([0, 1], g, 0.55, color=(GRAY, BLUE))
        for xx, v in zip([0, 1], g):
            a2.text(xx, v + 0.01, dec(v, lang), ha="center", fontsize=12, color=INK)
        a2.axhline(0.85, color=ACCENT, lw=1.3, ls="--")
        a2.text(0.5, 0.86, t[4], color=ACCENT, fontsize=11, ha="center", va="bottom")
        a2.set_xticks([0, 1], ARM[lang], fontsize=11)
        a2.set_ylim(0, 1.0)
        a2.set_title(t[3], fontsize=13, color=INK)
        clean(a2)
        commas(a2, lang)
        fig.tight_layout(w_pad=3)
        save(fig, HERE / f"exp3_{lang}.png")


if __name__ == "__main__":
    main()
