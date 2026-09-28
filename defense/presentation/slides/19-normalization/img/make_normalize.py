"""Slide 19: stage 7 — the network input as a 4-channel tensor: normalised R, G, B and the FOV mask, kk/ru/en.

A before/after pair of stage 7 looks identical to the eye (the shift and scale are per channel), so the figure
shows what the stage produces instead: the four channels of the 4 × 512 × 512 tensor.
Frames: demo/web/public/pipeline/dr03/preprocessing/stage_7_normalize/left.png (helpers/s7_normalize.py, rescaled to
[0, 255] for display) and stage_3_fov_mask/left.png.
Run: python make_normalize.py  ->  normalize_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import INK, INK2, LANGS, img, save  # noqa: E402

NAMES = {"kk": ("R", "G", "B", "маска"), "ru": ("R", "G", "B", "маска"), "en": ("R", "G", "B", "mask")}
NOTE = {"kk": "x′_c = (x_c − μ_c) / σ_c,  μ, σ — EyePACS жарамды пикселдері бойынша\nтензор 4 × 512 × 512",
        "ru": "x′_c = (x_c − μ_c) / σ_c,  μ, σ — по пригодным пикселям EyePACS\nтензор 4 × 512 × 512",
        "en": "x′_c = (x_c − μ_c) / σ_c,  μ, σ from the valid pixels of EyePACS\ntensor 4 × 512 × 512"}
EDGE = ("#d0453a", "#2e9e6b", "#2a78d6", INK2)


def main() -> None:
    """Write normalize_{lang}.png: four channel planes stacked with an offset."""
    x = img("preprocessing/stage_7_normalize/left.png")
    planes = [x[..., 0], x[..., 1], x[..., 2], img("preprocessing/stage_3_fov_mask/left.png")[..., 0]]
    for lang in LANGS:
        fig = plt.figure(figsize=(8, 5.2))
        for i, (p, name, col) in enumerate(zip(planes, NAMES[lang], EDGE)):
            ax = fig.add_axes([0.06 + i * 0.13, 0.30 - i * 0.055, 0.42, 0.62])
            ax.imshow(p, cmap="gray", vmin=0, vmax=255)
            ax.set_xticks([])
            ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor(col)
                s.set_linewidth(3)
            ax.text(1.02, 0.97, name, transform=ax.transAxes, color=col, fontsize=14, fontweight="bold", va="top")
        fig.text(0.5, 0.04, NOTE[lang], ha="center", fontsize=13, color=INK)
        save(fig, HERE / f"normalize_{lang}.png")


if __name__ == "__main__":
    main()
