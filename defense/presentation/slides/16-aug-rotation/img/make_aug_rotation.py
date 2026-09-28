"""Slide 16: augmentation — rotation with the spread set by the OD / fovea localisation uncertainty, kk/ru/en.

Panels: (a) the uncertainty cone around the OD–fovea axis — demo .../stage_6_augmentation/1_rotation/left_variant_B.png
(helpers/s6_rotation_vis.py); (b) one sample rotated by +σ; (c) the angle distribution: truncated Gaussian, adaptive
σ = 9.1° for this eye (helpers/s6_rotation_vis.py, dr03 / left) against the fallback σ = 13°, clip ±40°
(experiments/configs/default.yaml: fallback_rotation_sigma, rotation_clip).
Replaces the stage-6 card a18_1, the construction a18_3 and the empirical histogram a18_4.
Run: python make_aug_rotation.py  ->  aug_rotation_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ACCENT, BLUE, GRAY, INK, LANGS, clean, dec, img, save, show  # noqa: E402

SIGMA_ADAPT, SIGMA_FALLBACK, CLIP = 9.1, 13.0, 40.0
T = {"kk": ("Диск пен фовеа орнының\nбелгісіздігі", "Мысал: бұру +σ", "Бұру бұрышының таралуы",
            "бейімделгіш σ = {s}°", "резервтік σ = 13°", "шек ±40°", "бұрыш, °"),
     "ru": ("Неопределённость положения\nдиска и фовеа", "Пример: поворот на +σ", "Распределение угла поворота",
            "адаптивная σ = {s}°", "резервная σ = 13°", "граница ±40°", "угол, °"),
     "en": ("Uncertainty of the disc\nand fovea positions", "Sample: rotation by +σ", "Rotation angle distribution",
            "adaptive σ = {s}°", "fallback σ = 13°", "clip ±40°", "angle, °")}


def main() -> None:
    """Write aug_rotation_{lang}.png."""
    cone = img("preprocessing/stage_6_augmentation/1_rotation/left_variant_B.png")
    base = img("preprocessing/stage_5_clahe/polar/left.png")
    mask = img("preprocessing/stage_3_fov_mask/left.png")[..., 0]
    rot = cv2.warpAffine(base, cv2.getRotationMatrix2D((256, 256), SIGMA_ADAPT, 1.0), (512, 512),
                         flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    rot[mask == 0] = 0
    x = np.linspace(-50, 50, 1001)
    for lang in LANGS:
        t = T[lang]
        fig = plt.figure(figsize=(13, 4.6))
        a1, a2 = fig.add_axes([0.0, 0.04, 0.27, 0.76]), fig.add_axes([0.28, 0.04, 0.27, 0.76])
        show(a1, cone, t[0], 13)
        show(a2, rot, t[1], 13)
        ax = fig.add_axes([0.61, 0.17, 0.37, 0.63])
        for s, col, lab, ls in ((SIGMA_FALLBACK, GRAY, t[4], "--"), (SIGMA_ADAPT, BLUE, t[3].format(s=dec(SIGMA_ADAPT, lang, 1)), "-")):
            pdf = np.where(np.abs(x) <= CLIP, np.exp(-x ** 2 / (2 * s ** 2)), 0)
            pdf /= np.trapezoid(pdf, x)
            ax.plot(x, pdf, color=col, lw=2.2, ls=ls, label=lab)
            if col == BLUE:
                ax.fill_between(x, pdf, color=BLUE, alpha=0.15)
        for v in (-CLIP, CLIP):
            ax.axvline(v, color=ACCENT, lw=1.2, ls=":")
        ax.plot([], [], color=ACCENT, ls=":", label=t[5])
        ax.set_xlabel(t[6])
        ax.set_title(t[2], fontsize=13, color=INK)
        clean(ax, left=False)
        ax.set_ylim(0, ax.get_ylim()[1] * 1.45)
        ax.legend(frameon=False, fontsize=11, loc="upper center", ncol=2)
        save(fig, HERE / f"aug_rotation_{lang}.png")


if __name__ == "__main__":
    main()
