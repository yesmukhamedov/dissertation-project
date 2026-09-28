"""Slide 18: augmentation — ColorJitter and acquisition variability (Gaussian noise + JPEG), kk/ru/en.

Samples: demo .../stage_6_augmentation/4_color_jitter/left_{min,max}.png (brightness / contrast / saturation 0.9 or 1.1,
hue ∓0.02) and 5_acquisition_variability/left_max.png (noise σ = 6, JPEG quality 70), helpers/s6_augmentation.py with
experiments/configs/default.yaml. Noise and JPEG are shown as a 4× zoom of one region next to the same region unchanged.
There is no PCA colour jitter in the pipeline — the former PCA panel (a20_3) is removed.
Replaces a20_1 … a20_7.
Run: python make_aug_photometric.py  ->  aug_photometric_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import LANGS, img, save, show  # noqa: E402

BOX = (150, 230, 96)   # y, x, side of the zoomed region (exudates)
T = {"kk": ("Бастапқы", "Түс ауытқуы: ең аз\n(×0,9, реңк −0,02)", "Түс ауытқуы: ең көп\n(×1,1, реңк +0,02)",
            "Шу σ = 6 + JPEG q = 70\n(×4 үлкейтілген)", "бастапқы", "шу + JPEG"),
     "ru": ("Исходный", "Цветовые искажения: мин.\n(×0,9, оттенок −0,02)", "Цветовые искажения: макс.\n(×1,1, оттенок +0,02)",
            "Шум σ = 6 + JPEG q = 70\n(увеличено ×4)", "исходный", "шум + JPEG"),
     "en": ("Original", "Colour jitter: min\n(×0.9, hue −0.02)", "Colour jitter: max\n(×1.1, hue +0.02)",
            "Noise σ = 6 + JPEG q = 70\n(4× zoom)", "original", "noise + JPEG")}


def main() -> None:
    """Write aug_photometric_{lang}.png."""
    d = "preprocessing/stage_6_augmentation/"
    orig = img("preprocessing/stage_5_clahe/polar/left.png")
    cmin, cmax = img(d + "4_color_jitter/left_min.png"), img(d + "4_color_jitter/left_max.png")
    noisy = img(d + "5_acquisition_variability/left_max.png")
    y, x, s = BOX
    zoom = np.concatenate([orig[y:y + s, x:x + s], np.full((s, 3, 3), 255, np.uint8), noisy[y:y + s, x:x + s]], axis=1)
    zoom = zoom.repeat(4, axis=0).repeat(4, axis=1)
    for lang in LANGS:
        t = T[lang]
        fig, axes = plt.subplots(1, 4, figsize=(15, 4.6), gridspec_kw={"width_ratios": [1, 1, 1, 2]})
        for ax, a, cap in zip(axes, (orig, cmin, cmax, zoom), t[:4]):
            show(ax, a, cap, 13)
        axes[0].add_patch(plt.Rectangle((x, y), s, s, fill=False, ec="white", lw=1.2))
        w = zoom.shape[1]
        axes[3].text(w * 0.25, zoom.shape[0] - 20, t[4], color="white", ha="center", fontsize=12, fontweight="bold")
        axes[3].text(w * 0.75, zoom.shape[0] - 20, t[5], color="white", ha="center", fontsize=12, fontweight="bold")
        fig.subplots_adjust(left=0.01, right=0.99, top=0.84, bottom=0.02, wspace=0.05)
        save(fig, HERE / f"aug_photometric_{lang}.png")


if __name__ == "__main__":
    main()
