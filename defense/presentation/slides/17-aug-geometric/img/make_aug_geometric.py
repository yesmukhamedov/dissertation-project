"""Slide 17: augmentation — scale (zoom + stretch) and shear: extreme samples and parameter distributions, kk/ru/en.

Samples: demo .../stage_6_augmentation/{2_scale,3_shear}/left_{min,max}.png (helpers/s6_augmentation.py, parameters of
experiments/configs/default.yaml). A dashed contour of the unaugmented field of view (stage_3_fov_mask) is drawn over each
sample — at slide size a 10 % zoom or a 2° shear is invisible without it.
Distributions: zoom log-uniform [0.9, 1.1]; shear uniform [−2°, 2°] applied with p = 0.3.
There is no translation in the pipeline (config.py has no shift parameter) — the former «сдвиг» panel is removed.
Replaces a19_1 … a19_10.
Run: python make_aug_geometric.py  ->  aug_geometric_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import BLUE, INK, INK2, LANGS, clean, img, save, show  # noqa: E402

T = {"kk": {"zoom": ("масштаб 0,9", "масштаб 1,1", "лог-біркелкі [0,9; 1,1]", "масштаб"),
            "shear": ("қисайту −2°", "қисайту +2°", "біркелкі [−2°; 2°], p = 0,3", "қисайту, °"),
            "none": "қисайтусыз: 70 %"},
     "ru": {"zoom": ("масштаб 0,9", "масштаб 1,1", "лог-равномерное [0,9; 1,1]", "масштаб"),
            "shear": ("скос −2°", "скос +2°", "равномерное [−2°; 2°], p = 0,3", "скос, °"),
            "none": "без скоса: 70 %"},
     "en": {"zoom": ("zoom 0.9", "zoom 1.1", "log-uniform [0.9, 1.1]", "zoom"),
            "shear": ("shear −2°", "shear +2°", "uniform [−2°, 2°], p = 0.3", "shear, °"),
            "none": "no shear: 70 %"}}


def main() -> None:
    """Write aug_geometric_{lang}.png: rows zoom / shear, columns min / max / distribution."""
    mask = img("preprocessing/stage_3_fov_mask/left.png")[..., 0]
    ims = {k: [img(f"preprocessing/stage_6_augmentation/{d}/left_{e}.png") for e in ("min", "max")]
           for k, d in (("zoom", "2_scale"), ("shear", "3_shear"))}
    for lang in LANGS:
        t = T[lang]
        fig, axes = plt.subplots(2, 3, figsize=(11, 7.4), gridspec_kw={"width_ratios": [1, 1, 1.5]})
        for r, k in enumerate(("zoom", "shear")):
            for c in range(2):
                show(axes[r, c], ims[k][c], t[k][c], 13)
                axes[r, c].contour(mask, levels=[127], colors="white", linewidths=1.3, linestyles="dashed")
            ax = axes[r, 2]
            if k == "zoom":
                x = np.linspace(0.85, 1.15, 600)
                y = np.where((x >= 0.9) & (x <= 1.1), 1 / (x * np.log(1.1 / 0.9)), 0)
                ax.fill_between(x, y, color=BLUE, alpha=0.25)
                ax.plot(x, y, color=BLUE, lw=2)
            else:
                x = np.linspace(-3, 3, 600)
                y = np.where(np.abs(x) <= 2, 0.3 / 4, 0)
                ax.fill_between(x, y, color=BLUE, alpha=0.25)
                ax.plot(x, y, color=BLUE, lw=2)
                ax.annotate(t["none"], xy=(0, 0.02), xytext=(0, 0.13), ha="center", color=INK, fontsize=11,
                            arrowprops=dict(arrowstyle="-|>", color=INK2))
                ax.set_ylim(0, 0.17)
            ax.set_title(t[k][2], fontsize=12, color=INK)
            ax.set_xlabel(t[k][3])
            clean(ax, left=False)
            if lang != "en":
                ax.xaxis.set_major_formatter(lambda v, _: f"{v:g}".replace(".", ",").replace("-", "−"))
        fig.subplots_adjust(left=0.01, right=0.98, top=0.93, bottom=0.08, wspace=0.08, hspace=0.3)
        save(fig, HERE / f"aug_geometric_{lang}.png")


if __name__ == "__main__":
    main()
