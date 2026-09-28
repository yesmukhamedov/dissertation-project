"""Slide 13: stage 1 — optic disc and fovea found, the OD–fovea axis turned to one direction, kk/ru/en.

Frames: demo/web/public/pipeline/dr03/preprocessing/stage_0_canonical_flip/left.png and
stage_1_od_fovea_rotation/midpoint/left.png; landmark coordinates and the angle — helpers/coords.json (dr03 / left).
Rotation about the midpoint of the axis (helpers/s1_rotate.py).
Run: python make_rotation.py  ->  rotation_<lang>.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import DEMO, LANGS, dec, img, save, show  # noqa: E402

CAP = {"kk": ("Оптикалық диск (OD)\nпен фовеа табылды", "Ось ортаңғы нүкте\nбойынша бұрылды, θ = {a}°"),
       "ru": ("Найдены диск (OD)\nи фовеа", "Ось повёрнута вокруг\nсередины, θ = {a}°"),
       "en": ("Optic disc (OD)\nand fovea detected", "Axis rotated about\nits midpoint, θ = {a}°")}
LBL = {"kk": ("OD", "фовеа"), "ru": ("OD", "фовеа"), "en": ("OD", "fovea")}


def main() -> None:
    """Write rotation_{lang}.png."""
    c = json.loads((DEMO / "helpers" / "coords.json").read_text(encoding="utf-8"))["dr03"]["left"]
    before = img("preprocessing/stage_0_canonical_flip/left.png")
    after = img("preprocessing/stage_1_od_fovea_rotation/midpoint/left.png")
    (ox, oy), (fx, fy), (mx, my) = c["od"], c["fovea"], c["midpoint"]
    for lang in LANGS:
        fig, axes = plt.subplots(1, 2, figsize=(8, 4.6))
        ax = axes[0]
        show(ax, before, CAP[lang][0], 13)
        ax.plot([ox, fx], [oy, fy], color="white", lw=2)
        ax.plot([fx - 60, ox + 140], [my, my], color="white", lw=1.2, ls=(0, (4, 3)))
        for (x, y), col, name, dy in (((ox, oy), "#35c4f0", LBL[lang][0], -60), ((fx, fy), "#ff5aa0", LBL[lang][1], 110),
                                      ((mx, my), "#3ddc84", None, 0)):
            ax.plot(x, y, "o", ms=9, mfc=col, mec="white", mew=1.5)
            if name:
                ax.text(x, y + dy, name, color="white", fontsize=13, ha="center", fontweight="bold")
        show(axes[1], after, CAP[lang][1].format(a=dec(abs(c["angle_deg"]), lang, 1)), 13)
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.85, wspace=0.05)
        save(fig, HERE / f"rotation_{lang}.png")


if __name__ == "__main__":
    main()
