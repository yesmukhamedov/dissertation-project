"""Tiles vs polar CLAHE on IDRiD lesion-segmentation images (patent evidence).

Pipeline per image: FOV crop + isotropic resize to 512 (stage 2/3), adaptive
flat-field sigma = 0.07*D (stage 4), then one of: none / classic OpenCV CLAHE 8x8 (prototype) / polar.
Lesion masks go through the identical crop/resize (Lanczos, re-binarised at 127).
Metrics are computed on the L channel inside the FOV mask.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

PRE = Path(r"E:/personal/phd/dissertation/experiments/src/preprocessing")
ROOT = Path(r"E:/personal/phd/datasets/IDRiD/A. Segmentation")
OUT = Path(__file__).resolve().parent / "clahe_compare.json"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, PRE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


crop_mod = load("crop_resize")
ff_mod = load("flat_field")
polar_mod = load("polar_clahe")

LESIONS = {"MA": "1. Microaneurysms", "HE": "2. Haemorrhages",
           "EX": "3. Hard Exudates", "SE": "4. Soft Exudates"}


def lesion_contrast(L: np.ndarray, les: np.ndarray, fov: np.ndarray) -> float | None:
    """|mean(lesion) - mean(surround)| / std(surround), surround = 7px ring."""
    les = les & fov
    if les.sum() < 5:
        return None
    ring = cv2.dilate(les.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0
    ring = ring & ~les & fov
    if ring.sum() < 20:
        return None
    sd = L[ring].std()
    if sd < 1e-6:
        return None
    return float(abs(L[les].mean() - L[ring].mean()) / sd)


def cv_clahe(rgb: np.ndarray) -> np.ndarray:
    """Prototype: classic CLAHE (Zuiderveld, bilinear-interpolated), OpenCV, L-channel, 8x8, clip 2.0."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    lab[:, :, 0] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def metrics(rgb: np.ndarray, fov: np.ndarray, les: dict[str, np.ndarray], L_in: np.ndarray) -> dict:
    L = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)[:, :, 0].astype(np.float64)
    G = L - L_in
    ys, xs = np.where(fov)
    cy, cx = ys.mean(), xs.mean()
    r = np.sqrt((np.arange(L.shape[0])[:, None] - cy) ** 2 + (np.arange(L.shape[1])[None, :] - cx) ** 2)
    rmax = r[fov].max()
    ring_means = []
    for i in range(8):
        m = fov & (r >= rmax * i / 8) & (r < rmax * (i + 1) / 8)
        if m.sum() > 50:
            ring_means.append(L[m].mean())
    ring_means = np.array(ring_means)
    # local contrast: std in 15x15 window
    mu = cv2.blur(L, (15, 15)); mu2 = cv2.blur(L * L, (15, 15))
    lstd = np.sqrt(np.maximum(mu2 - mu * mu, 0))
    inner = fov & (r < 0.5 * rmax)
    outer = fov & (r >= 0.8 * rmax)
    eroded = cv2.erode(fov.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    rim = fov & (r >= 0.9 * rmax) & eroded
    hist = np.bincount(L[fov].astype(np.uint8), minlength=256).astype(np.float64)
    p = hist / hist.sum(); p = p[p > 0]
    out = {
        "radial_cv": float(ring_means.std() / ring_means.mean()),
        "local_std_inner": float(lstd[inner].mean()),
        "local_std_outer": float(lstd[outer].mean()),
        "rim_clip_frac": float(((L[rim] >= 250) | (L[rim] <= 5)).mean()),
        "entropy": float(-(p * np.log2(p)).sum()),
        "rim_gain_bias": float(G[rim].mean() - G[fov & (r < 0.8 * rmax)].mean()),
        "gain_rough": float(np.abs(cv2.Laplacian(cv2.GaussianBlur(G, (0, 0), 1.0), cv2.CV_64F))[eroded].mean()),
    }
    for k, m in les.items():
        out[f"lc_{k}"] = lesion_contrast(L, m, fov)
    return out


def main() -> None:
    rows = []
    for split in ("a. Training Set", "b. Testing Set"):
        for img_path in sorted((ROOT / "1. Original Images" / split).glob("*.jpg")):
            stem = img_path.stem
            rgb0 = np.array(Image.open(img_path).convert("RGB"))
            raw_mask = crop_mod._fov_foreground_mask(rgb0)
            img, fovm, tf = crop_mod.crop_and_resize(rgb0, 512, return_transform=True,
                                                     fov_mask=(raw_mask > 0).astype(np.float32))
            les = {}
            for k, d in LESIONS.items():
                p = ROOT / "2. All Segmentation Groundtruths" / split / d / f"{stem}_{k}.tif"
                if not p.exists():
                    continue
                m = np.array(Image.open(p).convert("L")) > 0
                m_img = np.stack([m.astype(np.uint8) * 255] * 3, -1)
                m_c, _, _ = crop_mod.crop_and_resize(m_img, 512, return_transform=True,
                                                     fov_mask=(raw_mask > 0).astype(np.float32))
                les[k] = m_c[:, :, 0] > 127
            fov = fovm > 0
            D = float(np.any(fov, axis=1).sum())
            ff = ff_mod.apply_flat_field(img, sigma=0.07 * D, mask=fovm)
            variants = {
                "none": ff,
                "tiles": cv_clahe(ff),
                "polar": polar_mod.apply_polar_clahe(ff, fovm, polar_mod.PolarClaheParams()),
            }
            row = {"image": stem}
            L_in = cv2.cvtColor(ff, cv2.COLOR_RGB2LAB)[:, :, 0].astype(np.float64)
            for name, v in variants.items():
                row[name] = metrics(v, fov, les, L_in)
            rows.append(row)
            print(stem, {n: round(row[n]["radial_cv"], 4) for n in variants}, flush=True)
    OUT.write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
