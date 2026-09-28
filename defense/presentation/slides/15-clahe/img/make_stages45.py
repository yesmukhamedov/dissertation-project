"""Slide 15: stages 4 and 5 — after crop → flat-field correction → CLAHE, one eye, kk/ru/en.

Frames: demo/web/public/pipeline/dr03/preprocessing/stage_2_fov_crop_resize, stage_4_flatfield (helpers/s4_flatfield.py:
corrected = image − GaussianBlur(image, σ) + 128, σ = 0.07 · D, as experiments/src/preprocessing/flat_field.py) and
stage_5_clahe/polar (the mode set in experiments/configs/default.yaml: clahe_mode: polar).
Replaces make_flatfield.py (stage 4 only) and the stage-5 card a17_1.
Run: python make_stages45.py  ->  stages45_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import LANGS, img, save, show  # noqa: E402

CAP = {"kk": ("Кесуден кейін", "4 · Жарықтандыруды түзету\nσ = 0,07·D", "5 · Полярлы CLAHE\n(LAB, L арнасы)"),
       "ru": ("После обрезки", "4 · Коррекция освещённости\nσ = 0,07·D", "5 · Полярный CLAHE\n(LAB, канал L)"),
       "en": ("After cropping", "4 · Flat-field correction\nσ = 0.07·D", "5 · Polar CLAHE\n(LAB, L channel)")}


def main() -> None:
    """Write stages45_{lang}.png."""
    frames = [img(f"preprocessing/{p}/left.png") for p in ("stage_2_fov_crop_resize", "stage_4_flatfield", "stage_5_clahe/polar")]
    for lang in LANGS:
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.7))
        for ax, a, t in zip(axes, frames, CAP[lang]):
            show(ax, a, t, 13)
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.85, wspace=0.05)
        save(fig, HERE / f"stages45_{lang}.png")


if __name__ == "__main__":
    main()
