"""Render the drawings (фигуры) for both patent applications as grayscale PNGs.

Patent drawings must be monochrome, so every figure is rendered in black/white or
grayscale. The fundus example is IDRiD image 01 (CC BY 4.0); every processing
step is executed by the production modules in experiments/src/preprocessing, so
the drawings show exactly what the claimed method produces.

Usage (from the repo root):
    python ip/patent/make_figures.py [--idrid <IDRiD root>] [--image IDRiD_01]

Output: ip/patent/um/figures/fig{1..3}.png and ip/patent/inv/figures/fig{1..4}.png
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image

BASE = Path(__file__).resolve().parent
PRE = BASE.parents[1] / "experiments" / "src" / "preprocessing"
DEFAULT_IDRID = Path("E:/personal/phd/datasets/IDRiD/A. Segmentation/1. Original Images/a. Training Set")

plt.rcParams.update({"font.family": "Times New Roman", "font.size": 11})


def _load(name: str):
    """Import a preprocessing module by file path (the package __init__ pulls in torch)."""
    spec = importlib.util.spec_from_file_location(name, PRE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _gray(rgb: np.ndarray) -> np.ndarray:
    """Luminance of an RGB image for monochrome printing."""
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)


def _flowchart(steps: list[str], path: Path, width: float = 8.0) -> None:
    """Vertical block diagram: one box per step, arrows between boxes."""
    h = 0.62 * len(steps) + 0.3
    fig, ax = plt.subplots(figsize=(width, h))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(steps))
    ax.axis("off")
    for i, text in enumerate(steps):
        y = len(steps) - i - 0.5
        ax.add_patch(FancyBboxPatch((0.4, y - 0.3), 9.2, 0.6, boxstyle="round,pad=0.02",
                                    fc="white", ec="black", lw=1.0))
        ax.text(5, y, text, ha="center", va="center", fontsize=9.5)
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((5, y - 0.3), (5, y - 0.7), arrowstyle="-|>",
                                         mutation_scale=10, color="black", lw=1.0))
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _panel(images: list[np.ndarray], labels: list[str], path: Path, cols: int) -> None:
    """Grid of grayscale images with lettered captions under each."""
    rows = int(np.ceil(len(images) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(2.3 * cols, 2.55 * rows))
    for ax in np.atleast_1d(axes).ravel():
        ax.axis("off")
    for ax, img, lab in zip(np.atleast_1d(axes).ravel(), images, labels):
        ax.imshow(img, cmap="gray", vmin=0, vmax=255 if img.dtype == np.uint8 else 1)
        ax.set_title(lab, y=-0.16, fontsize=10.5)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--idrid", type=Path, default=DEFAULT_IDRID)
    ap.add_argument("--image", default="IDRiD_01")
    args = ap.parse_args()

    crop = _load("crop_resize")
    ff = _load("flat_field")
    polar = _load("polar_clahe")

    um_dir, inv_dir = BASE / "um" / "figures", BASE / "inv" / "figures"
    um_dir.mkdir(parents=True, exist_ok=True)
    inv_dir.mkdir(parents=True, exist_ok=True)

    # ---- the example image through stages 2-5 --------------------------------
    rgb0 = np.array(Image.open(args.idrid / f"{args.image}.jpg").convert("RGB"))
    raw_mask = (crop._fov_foreground_mask(rgb0) > 0).astype(np.float32)
    img, fovm, _ = crop.crop_and_resize(rgb0, 512, return_transform=True, fov_mask=raw_mask)
    fov = fovm > 0
    d = float(np.any(fov, axis=1).sum())
    flat = ff.apply_flat_field(img, sigma=0.07 * d, mask=fovm)
    # Prototype for comparison: classic interpolated CLAHE (OpenCV), L channel, 8x8 grid, clip 2.0.
    lab_t = cv2.cvtColor(flat, cv2.COLOR_RGB2LAB)
    lab_t[:, :, 0] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(lab_t[:, :, 0])
    tl = cv2.cvtColor(lab_t, cv2.COLOR_LAB2RGB)
    pl = polar.apply_polar_clahe(flat, fovm, polar.PolarClaheParams())

    # ---- UM fig 1: block diagram of the claimed pre-processing method ---------
    _flowchart([
        "1 — ввод цветного изображения глазного дна и признака глаза (левый / правый)",
        "2 — зеркальное отражение изображения левого глаза",
        "3 — определение центров ДЗН и фовеа, поворот до горизонтали оси ДЗН–фовеа",
        "4 — выделение поля зрения, обрезка, изотропное масштабирование, дополнение",
        "5 — формирование бинарной маски поля зрения",
        "6 — коррекция освещённости: I − G$_σ$(I) + 128, σ = k·D, внутри маски",
        "7 — выравнивание гистограммы канала L (CIELAB) внутри маски",
        "8 — нормализация каналов по статистикам внутри маски",
        "9 — формирование 4-канального входа (R, G, B, маска) → СНС → стадия ДР",
    ], um_dir / "fig1.png")

    # ---- UM fig 2: the example image after each stage -------------------------
    _panel(
        [_gray(rgb0), _gray(img), (fov * 255).astype(np.uint8), _gray(flat), _gray(pl)],
        ["а", "б", "в", "г", "д"], um_dir / "fig2.png", cols=5,
    )

    # ---- UM fig 3: 4-channel input and first convolution ----------------------
    fig, ax = plt.subplots(figsize=(6.3, 2.4))
    ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 4)
    for i, name in enumerate(["R", "G", "B", "маска поля зрения"]):
        ax.add_patch(FancyBboxPatch((0.3 + 0.25 * i, 0.4 + 0.25 * i), 2.2, 2.2,
                                    boxstyle="square,pad=0", fc="white", ec="black"))
        ax.text(1.4 + 0.25 * i, 0.55 + 0.25 * i, name, ha="center", fontsize=9)
    ax.add_patch(FancyArrowPatch((3.5, 2), (4.6, 2), arrowstyle="-|>", mutation_scale=12, color="black"))
    ax.add_patch(FancyBboxPatch((4.7, 1.2), 2.4, 1.6, boxstyle="round,pad=0.03", fc="white", ec="black"))
    ax.text(5.9, 2.0, "первый свёрточный\nслой, 4 входных канала\nW₄ = (W_R+W_G+W_B)/3",
            ha="center", va="center", fontsize=9)
    ax.add_patch(FancyArrowPatch((7.2, 2), (8.1, 2), arrowstyle="-|>", mutation_scale=12, color="black"))
    ax.add_patch(FancyBboxPatch((8.2, 1.4), 1.6, 1.2, boxstyle="round,pad=0.03", fc="white", ec="black"))
    ax.text(9.0, 2.0, "СНС →\nстадия 0–4", ha="center", va="center", fontsize=9)
    fig.savefig(um_dir / "fig3.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # ---- INV fig 1: block diagram of polar CLAHE ------------------------------
    _flowchart([
        "1 — преобразование в CIELAB, выделение канала L; маска поля зрения",
        "2 — центр полярной системы: фовеа (если достоверна) либо центроид маски",
        "3 — кольца: rᵢ = R·(i/N)$^p$, p > 1",
        "4 — карта выраженности сосудов (матрица Гессе, несколько масштабов)",
        "5 — угловые секторы переменной ширины в каждом кольце по выраженности сосудов",
        "6 — гистограмма ячейки внутри маски, отсечение min(c₁S/256, c₂S), таблица",
        "7 — билинейная интерполяция таблиц по углу и радиусу",
        "8 — замена канала L, обратное преобразование в RGB",
    ], inv_dir / "fig1.png")

    # ---- INV fig 2: the polar grid over the image -----------------------------
    params = polar.PolarClaheParams()
    lab = cv2.cvtColor(flat, cv2.COLOR_RGB2LAB)
    l_ch = lab[:, :, 0]
    cx, cy = polar.resolve_pivot(fovm, None)
    h, w = l_ch.shape
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2).astype(np.float32)
    theta = (np.arctan2(yy - cy, xx - cx) + np.pi).astype(np.float32)
    r_max = float(r[fov].max())
    rb = np.array([(i / params.radial_rings) ** params.radial_exponent * r_max
                   for i in range(params.radial_rings + 1)])
    vmap = polar._vessel_detection(l_ch, params.vessel_sigmas)
    vmap[~fov] = 0
    sectors = polar._compute_nonuniform_sectors(vmap, r, theta, rb, fovm, int(fov.sum()), params)

    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.imshow(_gray(flat), cmap="gray", vmin=0, vmax=255)
    t = np.linspace(0, 2 * np.pi, 400)
    for rad in rb[1:]:
        ax.plot(cx + rad * np.cos(t), cy + rad * np.sin(t), color="white", lw=0.7)
    for ri, bounds in enumerate(sectors):
        for b in bounds[1:-1]:
            ang = b - np.pi  # theta was shifted by +pi
            ax.plot([cx + rb[ri] * np.cos(ang), cx + rb[ri + 1] * np.cos(ang)],
                    [cy + rb[ri] * np.sin(ang), cy + rb[ri + 1] * np.sin(ang)], color="white", lw=0.7)
    ax.plot(cx, cy, marker="+", color="white", ms=10, mew=1.5)
    ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
    fig.savefig(inv_dir / "fig2.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # ---- INV fig 3: vesselness map (inverted for print) -----------------------
    vis = (255 - np.clip(np.sqrt(vmap) * 255 * 1.5, 0, 255)).astype(np.uint8)
    _panel([_gray(flat), vis], ["а", "б"], inv_dir / "fig3.png", cols=2)

    # ---- INV fig 4: none / tiles / polar -------------------------------------
    _panel([_gray(flat), _gray(tl), _gray(pl)], ["а", "б", "в"], inv_dir / "fig4.png", cols=3)

    n_sec = [len(b) - 1 for b in sectors]
    print(f"D={d:.0f}px sigma={0.07 * d:.1f} pivot=({cx:.0f},{cy:.0f}) "
          f"ring radii={np.round(rb).astype(int).tolist()} sectors/ring={n_sec}")


if __name__ == "__main__":
    main()
