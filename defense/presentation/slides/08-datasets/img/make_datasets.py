"""Slide 08: DR grades 0–4 on real fundus images, and the class balance of the five-grade corpora, kk/ru/en.

Examples: demo/web/public/pipeline/dr0{0..4}/input/left.png (one image per grade).
Class shares, %: the archived slide script defense/_archive/presentation_2026-09-26/scripts/generate_kz_class_distribution.py
(corpus metadata, not results). ODIR-5K (DR-positive only) and RFMiD (binary labels) have no five-grade balance and are
left out. Replaces a10_1 (kk only), a10_2 (English table — duplicates the table on the slide) and a10_3 … a10_7.
Run: python make_datasets.py  ->  datasets_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import DEMO, INK, INK2, LANGS, fov_crop, save, show  # noqa: E402

# (corpus, DR0 … DR4 %) — archive generate_kz_class_distribution.py, DATASETS_5CLASS
SHARES = [("EyePACS", 73.5, 6.9, 15.1, 2.5, 2.0), ("Messidor-2", 58.3, 15.5, 19.9, 4.3, 2.0),
          ("DDR", 50.0, 5.0, 35.8, 1.9, 7.3), ("APTOS 2019", 49.3, 10.1, 27.3, 5.3, 8.1),
          ("IDRiD", 32.6, 4.8, 32.6, 18.0, 12.0)]
RAMP = ["#e9e4dc", "#f2c38b", "#e58a45", "#c0502a", "#7e2412"]  # sequential: grade = severity
G = {"kk": ["0 · ДР жоқ", "1 · жеңіл", "2 · орташа", "3 · ауыр", "4 · пролиферативті"],
     "ru": ["0 · нет ДР", "1 · лёгкая", "2 · умеренная", "3 · тяжёлая", "4 · пролиферативная"],
     "en": ["0 · no DR", "1 · mild", "2 · moderate", "3 · severe", "4 · proliferative"]}
TITLE = {"kk": "Дәрежелер үлесі, %", "ru": "Доли степеней, %", "en": "Share of grades, %"}


def main() -> None:
    """Write datasets_{lang}.png: five examples on top, stacked 100 % bars below."""
    ex = [fov_crop(np.asarray(Image.open(DEMO / f"dr0{g}" / "input" / "left.png").convert("RGB"))) for g in range(5)]
    for lang in LANGS:
        fig = plt.figure(figsize=(13, 7))
        for g in range(5):
            ax = fig.add_axes([0.01 + g * 0.198, 0.56, 0.18, 0.36])
            show(ax, ex[g], G[lang][g], 12.5)
            ax.add_patch(plt.Rectangle((0, 1.0), 1, 0.03, transform=ax.transAxes, color=RAMP[g], clip_on=False))
        ax = fig.add_axes([0.12, 0.06, 0.85, 0.4])
        left = np.zeros(len(SHARES))
        for g in range(5):
            v = np.array([r[g + 1] for r in SHARES])
            ax.barh(range(len(SHARES)), v, left=left, color=RAMP[g], edgecolor="white", linewidth=2, height=0.7)
            for y, (l, w) in enumerate(zip(left, v)):
                if w >= 5:
                    ax.text(l + w / 2, y, f"{w:.0f}", ha="center", va="center", fontsize=11,
                            color=INK if g < 3 else "white")
            left += v
        ax.set_yticks(range(len(SHARES)), [r[0] for r in SHARES], fontsize=12)
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(left=False)
        ax.set_title(TITLE[lang], fontsize=13, color=INK, loc="left")
        save(fig, HERE / f"datasets_{lang}.png")


if __name__ == "__main__":
    main()
