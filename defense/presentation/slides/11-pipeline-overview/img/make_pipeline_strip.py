"""Slide 11: one eye (DR03, left) through all eight stages — the pipeline as a film strip, kk/ru/en.

Frames: demo/web/public/pipeline/dr03/ (helpers/ reproduce them with the experiments/ code). Stage 5 — the
polar CLAHE (experiments/configs/default.yaml: clahe_mode: polar). Stage 6 — one sample, a rotation by 12°.
Group colours as in the talk: geometric — green, photometric — orange, augmentation — purple dashed,
normalisation — red.
Run: python make_pipeline_strip.py  ->  strip_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import INK, INK2, LANGS, fov_crop, img, save, show  # noqa: E402

GEO, PHOTO, AUG, NORM = "#2e9e6b", "#e08a2c", "#7a5bd6", "#c8442a"
CAP = {
    "kk": ["Кіріс", "0 · Канондық\nайналдыру", "1 · Диск пен фовеа\nбойынша бұру", "2 · Кесу,\n512 × 512",
           "3 · Көру алаңының\nмаскасы", "4 · Жарықтандыруды\nтүзету", "5 · CLAHE", "6 · Аугментация\n(тек оқытуда)",
           "7 · Нормалау →\nтензор 4 × 512 × 512"],
    "ru": ["Вход", "0 · Каноническое\nотражение", "1 · Поворот по диску\nи фовеа", "2 · Обрезка,\n512 × 512",
           "3 · Маска поля\nзрения", "4 · Коррекция\nосвещённости", "5 · CLAHE", "6 · Аугментация\n(только обучение)",
           "7 · Нормализация →\nтензор 4 × 512 × 512"],
    "en": ["Input", "0 · Canonical\nflip", "1 · OD–fovea\nrotation", "2 · Crop,\n512 × 512", "3 · FOV\nmask",
           "4 · Flat-field\ncorrection", "5 · CLAHE", "6 · Augmentation\n(training only)",
           "7 · Normalisation →\ntensor 4 × 512 × 512"],
}
COLOR = [INK2, GEO, GEO, GEO, GEO, PHOTO, PHOTO, AUG, NORM]
LEGEND = {"kk": ["геометриялық", "фотометриялық", "аугментация", "нормалау"],
          "ru": ["геометрические", "фотометрические", "аугментация", "нормализация"],
          "en": ["geometric", "photometric", "augmentation", "normalisation"]}


def frames() -> list:
    """Nine frames: input and the output of stages 0–7."""
    s5 = img("preprocessing/stage_5_clahe/polar/left.png")
    m = cv2.getRotationMatrix2D((256, 256), 12, 1.0)
    s6 = cv2.warpAffine(s5, m, (512, 512), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    mask = img("preprocessing/stage_3_fov_mask/left.png")
    s6[mask[..., 0] == 0] = 0
    return [fov_crop(img("input/left.png")), img("preprocessing/stage_0_canonical_flip/left.png"),
            img("preprocessing/stage_1_od_fovea_rotation/midpoint/left.png"),
            img("preprocessing/stage_2_fov_crop_resize/left.png"), mask,
            img("preprocessing/stage_4_flatfield/left.png"), s5, s6,
            img("preprocessing/stage_7_normalize/left.png")]


def main() -> None:
    """Write strip_{lang}.png: two rows (input + stages 0–3; stages 4–7)."""
    fr = frames()
    for lang in LANGS:
        fig, axes = plt.subplots(2, 5, figsize=(13, 6.6))
        cells = [axes[0, i] for i in range(5)] + [axes[1, i] for i in range(4)]
        for k, (ax, a, cap, col) in enumerate(zip(cells, fr, CAP[lang], COLOR)):
            show(ax, a)
            ax.set_title(cap, fontsize=12, color=INK, pad=6)
            ls = (0, (4, 3)) if col == AUG else "solid"
            ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, fill=False, ec=col, lw=3.2, ls=ls,
                                       clip_on=False))
        leg = axes[1, 4]
        leg.axis("off")
        for i, (col, name) in enumerate(zip((GEO, PHOTO, AUG, NORM), LEGEND[lang])):
            y = 0.8 - i * 0.2
            leg.add_patch(plt.Rectangle((0.08, y - 0.05), 0.16, 0.1, fill=False, ec=col, lw=3,
                                        ls=(0, (4, 3)) if col == AUG else "solid", transform=leg.transAxes))
            leg.text(0.32, y, name, va="center", fontsize=12, color=INK, transform=leg.transAxes)
        fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.02, wspace=0.18, hspace=0.42)
        for a, b in zip(cells[:-1], cells[1:]):
            if a in axes[0] and b in axes[1]:
                continue
            p0, p1 = a.get_position(), b.get_position()
            fig.add_artist(FancyArrowPatch((p0.x1 + 0.002, (p0.y0 + p0.y1) / 2), (p1.x0 - 0.002, (p1.y0 + p1.y1) / 2),
                                           transform=fig.transFigure, arrowstyle="-|>", mutation_scale=14, color=INK2))
        save(fig, HERE / f"strip_{lang}.png")


if __name__ == "__main__":
    main()
