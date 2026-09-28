"""Before/after figure for stage 4 (flat-field illumination correction), kk/ru/en.

Source images: demo/web/public/pipeline/dr03/preprocessing/stage_{2,4}_*/left.png — produced by
demo/web/public/pipeline/helpers/s4_flatfield.py, the same formula as experiments/src/preprocessing/flat_field.py:
corrected = image − GaussianBlur(image, σ) + 128, σ = 0.07 · D (D — FOV diameter).
Run: python make_flatfield.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[4] / "demo" / "web" / "public" / "pipeline" / "dr03" / "preprocessing"
LABELS = {
    "kk": ("Түзетуге дейін", "Жарықтандыруды түзетуден кейін\nσ = 0,07·D"),
    "ru": ("До коррекции", "После коррекции освещённости\nσ = 0,07·D"),
    "en": ("Before correction", "After flat-field correction\nσ = 0.07·D"),
}


def main() -> None:
    """Write flatfield_{lang}.png for every language."""
    before = Image.open(SRC / "stage_2_fov_crop_resize" / "left.png")
    after = Image.open(SRC / "stage_4_flatfield" / "left.png")
    for lang, (t0, t1) in LABELS.items():
        fig, axes = plt.subplots(1, 2, figsize=(8, 4.9), dpi=200)
        for ax, im, t in zip(axes, (before, after), (t0, t1)):
            ax.imshow(im)
            ax.set_title(t, fontsize=13, color="#0b0b0b", loc="center")
            ax.axis("off")
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.86, wspace=0.03)
        fig.savefig(HERE / f"flatfield_{lang}.png", facecolor="white")
        plt.close(fig)


if __name__ == "__main__":
    main()
