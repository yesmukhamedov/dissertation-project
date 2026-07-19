#!/usr/bin/env python3
"""Redraw the dataset-illustration figures on the IDRiD dataset (instead of EyePACS).

Regenerates the three figures whose content is drawn from a DR-graded fundus set:
  FIG 1.1  1x5 montage — one representative fundus per DR grade 0..4     (IDRiD)
  FIG 1    5x4 grid    — four fundus per DR grade 0..4                   (IDRiD)
  FIG 3    3x5 grid    — graded fundus tiles + class-distribution CSV    (IDRiD)

FIG 2 (lesion overlays) already uses IDRiD segmentation groundtruth and is left
as-is. Source is the authoritative IDRiD "B. Disease Grading" set (516 images,
train 413 + test 103) with its official per-image grade labels — high-resolution,
single-camera, clean; a deliberate contrast to EyePACS's variable field quality.

Deterministic (fixed seeds). English labels only. Run: python _make_idrid_figures.py
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from PIL import Image

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 11,
    "savefig.dpi": 200,
})

HERE = Path(__file__).resolve().parent
INK = "#1a1a1a"

# ----------------------------------------------------------------------------- IDRiD source
IDRID_GRADING = Path(r"D:/datasets/IDRiD/B. Disease Grading")
SPLITS = [
    (IDRID_GRADING / "1. Original Images" / "a. Training Set",
     IDRID_GRADING / "2. Groundtruths" / "a. IDRiD_Disease Grading_Training Labels.csv"),
    (IDRID_GRADING / "1. Original Images" / "b. Testing Set",
     IDRID_GRADING / "2. Groundtruths" / "b. IDRiD_Disease Grading_Testing Labels.csv"),
]

GRADES = [0, 1, 2, 3, 4]
GRADE_LABELS = ["DR 0\n(No DR)", "DR 1\n(Mild)", "DR 2\n(Moderate)",
                "DR 3\n(Severe)", "DR 4\n(Proliferative)"]
GRADE_SHORT = {0: "No DR", 1: "Mild", 2: "Moderate", 3: "Severe", 4: "Proliferative DR"}
ROW_LABELS = [
    "(a) DR 0 — No DR",
    "(b) DR 1 — Mild NPDR",
    "(c) DR 2 — Moderate NPDR",
    "(d) DR 3 — Severe NPDR",
    "(e) DR 4 — Proliferative DR",
]


def build_index() -> dict[int, list[Path]]:
    """Map each DR grade -> sorted list of IDRiD image paths (train + test)."""
    by_grade: dict[int, list[Path]] = {g: [] for g in GRADES}
    for img_dir, csv_path in SPLITS:
        with open(csv_path, newline="") as fh:
            for row in csv.reader(fh):
                if not row or row[0].strip() in ("", "Image name"):
                    continue
                name, grade = row[0].strip(), row[1].strip()
                if not grade.isdigit():
                    continue
                p = img_dir / f"{name}.jpg"
                if p.is_file():
                    by_grade[int(grade)].append(p)
    for g in GRADES:
        by_grade[g].sort()
    return by_grade


def load_square(path: Path, size: int = 512) -> np.ndarray:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((size, size))
    return np.asarray(im)


# ----------------------------------------------------------------------------- FIG 1.1
def fig_grades_montage(idx: dict[int, list[Path]], path: Path):
    rng = random.Random(11)
    fig, axes = plt.subplots(1, 5, figsize=(12, 3.1))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.80, bottom=0.14, wspace=0.06)
    for ax, g, lab in zip(axes, GRADES, GRADE_LABELS):
        pool = idx[g]
        ax.imshow(load_square(rng.choice(pool)))
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(INK); s.set_linewidth(1.0)
        ax.set_title(lab, fontsize=10.5, color=INK)
    fig.suptitle("Representative fundus images across the five-class DR grading scale (IDRiD)",
                 fontsize=12.5, y=0.975, color=INK)
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)
    print(f"WROTE {path.name}")


# ----------------------------------------------------------------------------- FIG 1
def fig_per_class_grid(idx: dict[int, list[Path]], path: Path, n_cols: int = 4):
    fig, axes = plt.subplots(5, n_cols, figsize=(n_cols * 2.8, 5 * 2.8),
                             gridspec_kw={"wspace": 0.04, "hspace": 0.40})
    for row, g in enumerate(GRADES):
        rng = random.Random(42 + g)
        pool = list(idx[g]); rng.shuffle(pool)
        picks = pool[:n_cols]
        for col in range(n_cols):
            ax = axes[row, col]
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_visible(False)
            if col < len(picks):
                ax.imshow(load_square(picks[col]))
        axes[row, 0].set_ylabel(ROW_LABELS[row], labelpad=18, rotation=0, ha="right",
                                va="center", fontsize=11, fontweight="bold")
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print(f"WROTE {path.name}")


# ----------------------------------------------------------------------------- FIG 3
def fig_dataset_contents(idx: dict[int, list[Path]], img_path: Path, csv_path: Path,
                         n_rows: int = 3, n_cols: int = 5):
    total = n_rows * n_cols
    rng = random.Random(7)
    # balanced quota across the 5 grades (3 each for a 3x5 grid)
    quota = total // 5
    leftover = total - 5 * quota
    picks: list[tuple[Path, int]] = []
    for g in GRADES:
        pool = list(idx[g]); rng.shuffle(pool)
        n = quota + (1 if g < leftover else 0)
        picks.extend((p, g) for p in pool[:n])
    rng.shuffle(picks)
    picks = picks[:total]

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 2.6, n_rows * 2.9),
                             gridspec_kw={"wspace": 0.06, "hspace": 0.35})
    for i in range(total):
        r, c = divmod(i, n_cols)
        ax = axes[r, c]
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        if i < len(picks):
            p, g = picks[i]
            ax.imshow(load_square(p))
            ax.set_title(GRADE_SHORT[g], fontsize=10, fontweight="bold")
    fig.savefig(img_path, dpi=180, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print(f"WROTE {img_path.name}")

    # class-distribution CSV from the official IDRiD grade labels
    counts = {g: len(idx[g]) for g in GRADES}
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "grade", "label", "count"])
        for g in GRADES:
            w.writerow(["IDRiD (grading, train+test)", g, GRADE_SHORT[g], counts[g]])
    print(f"WROTE {csv_path.name}  (grade counts: {counts})")


def main():
    idx = build_index()
    if any(not idx[g] for g in GRADES):
        raise RuntimeError(f"missing IDRiD images for some grade: "
                           f"{ {g: len(idx[g]) for g in GRADES} }")
    fig_grades_montage(idx, HERE / "fig1_1_dr_grades_idrid.png")
    fig_per_class_grid(idx, HERE / "fig1_per_class.png")
    fig_dataset_contents(idx, HERE / "fig3_dataset_contents.png",
                         HERE / "fig3_dataset_distribution.csv")


if __name__ == "__main__":
    main()
