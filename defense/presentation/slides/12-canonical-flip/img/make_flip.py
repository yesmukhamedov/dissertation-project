"""Slide 12: stage 0 — the left eye before and after the canonical flip, kk/ru/en.

Frames: demo/web/public/pipeline/dr03/{input,preprocessing/stage_0_canonical_flip}/left.png (helpers/s0_canonical_flip.py).
The former a14_2 / a14_3 were copies of the input frames of slide 11 — the flip was not visible.
Run: python make_flip.py  ->  flip_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import LANGS, fov_crop, img, save, show  # noqa: E402

CAP = {"kk": ("Сол көз — кіріс:\nоптикалық диск сол жақта", "Айналдырудан кейін:\nдиск оң жақта, оң көздегідей"),
       "ru": ("Левый глаз — вход:\nдиск зрительного нерва слева", "После отражения:\nдиск справа, как у правого глаза"),
       "en": ("Left eye — input:\noptic disc on the left", "After the flip:\ndisc on the right, as in a right eye")}


def main() -> None:
    """Write flip_{lang}.png."""
    before = fov_crop(img("input/left.png"))
    after = fov_crop(img("preprocessing/stage_0_canonical_flip/left.png"))
    for lang in LANGS:
        fig, axes = plt.subplots(1, 2, figsize=(8, 4.7))
        for ax, a, t in zip(axes, (before, after), CAP[lang]):
            show(ax, a, t, 13)
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.84, wspace=0.05)
        save(fig, HERE / f"flip_{lang}.png")


if __name__ == "__main__":
    main()
