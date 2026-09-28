"""Slide 25: the Grad-CAM pair of the volume (fig. D.1, IDRiD_007) with kk/ru/en captions.

Source: experiments/outputs/exp4/gradcam_maskset/IDRiD_007_comparison.png — the plate the thesis prints as FIG-D.1
(appendix D). Its four panels (original · baseline Grad-CAM · integrated Grad-CAM · expert lesion mask) are cut out of the
plate by locating the white gutters, their English titles dropped, and the last three redrawn with captions.
A new pair is deliberately not rendered from checkpoints: the checkpoints on disk belong to the run before 2026-08-03
(results/INTEGRITY_NOTE.md), so the slide shows exactly the pair the volume shows. Replaces a27_2.
Run: python make_gradcam.py  ->  gradcam_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import INK2, LANGS, ROOT, save, show  # noqa: E402

PLATE = ROOT / "experiments" / "outputs" / "exp4" / "gradcam_maskset" / "IDRiD_007_comparison.png"
CAP = {"kk": ("Базалық", "Интеграцияланған", "Сарапшы маскасы\n(жасыл — зақымдану)", "IDRiD_007 · томдағы D.1-сурет"),
       "ru": ("Базовая", "Интегрированная", "Маска эксперта\n(зелёный — поражение)", "IDRiD_007 · рис. D.1 тома"),
       "en": ("Baseline", "Integrated", "Expert mask\n(green — lesion)", "IDRiD_007 · fig. D.1 of the volume")}


def panels(a: np.ndarray) -> list[np.ndarray]:
    """Cut the plate into its image panels: columns and rows that are not near-white.

    Args:
        a: RGB plate.

    Returns:
        The panels, left to right.
    """
    dark = a.min(axis=2) < 235
    rows = np.nonzero(dark.mean(axis=1) > 0.5)[0]                 # image rows (titles are thin text lines)
    cols = dark[rows[0]:rows[-1]].mean(axis=0) > 0.5
    edges = np.flatnonzero(np.diff(np.r_[0, cols.astype(int), 0]))
    return [a[rows[0]:rows[-1] + 1, s:e] for s, e in zip(edges[::2], edges[1::2]) if e - s > 100]


def main() -> None:
    """Write gradcam_{lang}.png: baseline · integrated · expert mask."""
    p = panels(np.asarray(Image.open(PLATE).convert("RGB")))
    assert len(p) == 4, f"expected 4 panels, found {len(p)}"
    for lang in LANGS:
        c = CAP[lang]
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.6))
        for ax, im, t in zip(axes, p[1:], c[:3]):
            show(ax, im, t, 13)
        fig.text(0.99, 0.015, c[3], ha="right", fontsize=10, color=INK2, style="italic")
        fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.07, wspace=0.04)
        save(fig, HERE / f"gradcam_{lang}.png")


if __name__ == "__main__":
    main()
