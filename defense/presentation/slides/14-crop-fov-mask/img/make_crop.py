"""Slide 14: stage 2 against the baseline, and stage 3 — stretch vs isotropic crop, FOV mask, kk/ru/en.

Baseline (configs A / C): stretch-resize of the raw frame to 512 × 512 — the round fundus becomes an ellipse
(here the raw frame is mirrored so that it matches the flipped eye of stage 2).
Stage 2: demo/web/public/pipeline/dr03/preprocessing/stage_2_fov_crop_resize/left.png; stage 3: stage_3_fov_mask/left.png.
Run: python make_crop.py  ->  crop_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import LANGS, img, save, show  # noqa: E402

CAP = {"kk": ("Базалық: 512 × 512-ге созу\n(көз түбі эллипске айналады)", "2-кезең: кесу және\nизотропты масштабтау",
              "3-кезең: көру алаңының\nмаскасы (4-арна)"),
       "ru": ("Базовая: растяжение до 512 × 512\n(глазное дно становится эллипсом)", "Этап 2: обрезка и\nизотропное масштабирование",
              "Этап 3: маска поля\nзрения (4-й канал)"),
       "en": ("Baseline: stretch to 512 × 512\n(the fundus becomes an ellipse)", "Stage 2: crop and\nisotropic scaling",
              "Stage 3: FOV mask\n(4th channel)")}


def main() -> None:
    """Write crop_{lang}.png."""
    raw = np.ascontiguousarray(img("input/left.png")[:, ::-1])
    stretched = cv2.resize(raw, (512, 512), interpolation=cv2.INTER_AREA)
    frames = (stretched, img("preprocessing/stage_2_fov_crop_resize/left.png"), img("preprocessing/stage_3_fov_mask/left.png"))
    for lang in LANGS:
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.8))
        for ax, a, t in zip(axes, frames, CAP[lang]):
            show(ax, a, t, 12.5)
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.84, wspace=0.06)
        save(fig, HERE / f"crop_{lang}.png")


if __name__ == "__main__":
    main()
