"""
prepare_segmentation_pairs.py — Build the pool of bilateral "patients" behind
the Demo tab's "Random sample" button from the IDRiD **Segmentation** training
set (54 images with pixel-level lesion + optic-disc masks).

Replaces the earlier Localization-based pool (``prepare_idrid_samples.py``).
That subset shipped OD + fovea centre markups; this one ships **masks** instead,
so laterality and the disc circle are measured from the optic-disc mask rather
than read from a CSV:

  * **Laterality** — the optic disc is nasal to the macula, so a disc left of
    the FOV centre means a LEFT eye (OS) and right of it a RIGHT eye (OD).
    The 54 images split exactly 27 / 27, i.e. 27 complete pairs, no leftovers.
  * **Pairing** — the source is monocular (one eye per record, no patient ids),
    so a "patient" is synthetic. To keep a drawn pair looking like one person,
    left and right eyes are matched on **retinal colour**: mean + spread of
    CIE-Lab inside the FOV, paired by the Hungarian algorithm so the total
    mismatch over all pairs is minimal (a greedy nearest-match would strand the
    outliers against each other). The assignment still has to place every eye,
    so the colour outliers collect in the worst pair — ``--drop-worst`` discards
    it, leaving 26 pairs that each read as one person.
  * **No DR grade.** Grades live in the set's "B. Disease Grading" part under a
    different numbering that does not map onto these filenames, so ``grade`` is
    ``null`` — unlike the Localization pool there is no ``dr0..dr4`` split. The
    Random button does not read it: drawn images are inserted as PLAIN uploads.

Each saved file is named ``IDRiD_seg_p{NN}_{L|R}_{src}`` where NN is the patient
number (pairs are numbered best-colour-match first), L/R the eye orientation and
src the source folder (``01``..``54``).

Writes images + a display-frame FOV mask per eye, plus two manifests:
    - demo/web/public/datasets/idrid/segmentation/patients.json (canonical)
    - demo/web/src/tabs/_segmentationSamples.js (imported by Demo.js)

and, for the PDF report's segmentation page, one panel per annotated layer into
    - demo/server/app/segments/  (+ index.json, keyed by image id)

Run from anywhere:

    python demo/web/scripts/prepare_segmentation_pairs.py
        [--src DIR] [--max-size 512] [--drop-worst 1]

Re-running is safe — the output directory is wiped and recreated.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    import cv2
    import numpy as np
    from PIL import Image
    from scipy.optimize import linear_sum_assignment
except ImportError:  # pragma: no cover
    sys.exit(
        "Pillow, OpenCV, NumPy and SciPy are required.\n"
        "Install with: pip install Pillow opencv-python numpy scipy"
    )

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_DIR = SCRIPT_DIR.parent                     # demo/web/ (holds public/ + src/)
PUBLIC_ROOT = DEMO_DIR / "public"

DEFAULT_SRC = Path(r"C:\extras\segmentation\segmentation-54")

OUT_REL = "datasets/idrid/segmentation"          # under public/, also the URL path
OUT_PUBLIC_DIR = PUBLIC_ROOT / OUT_REL
OUT_JSON_PATH = OUT_PUBLIC_DIR / "patients.json"
OUT_JS_PATH = DEMO_DIR / "src" / "tabs" / "_segmentationSamples.js"

# The PDF report is rendered server-side, so the segmentation panels it puts on
# page 2 ship with the server package (``COPY server`` covers them in the image)
# rather than with the web bundle. Keyed by the image id the client files as the
# upload's ``filename``, which is how report.py finds them again.
SEGMENTS_DIR = DEMO_DIR.parent / "server" / "app" / "segments"
SEGMENTS_INDEX_PATH = SEGMENTS_DIR / "index.json"

# Expert fovea centres for the images that are also in IDRiD's Localization part
# (source folder -> Localization id + fovea in source pixels), and the mean
# disc-to-fovea offset in disc diameters (temporal, inferior) measured on them,
# which places the fovea for the rest.
FOVEA_TABLE = SCRIPT_DIR / "idrid_seg_fovea.json"
FOVEA_OFFSET_DD = (2.42, 0.29)

# Retina pixels are those above this grey level; everything darker is the black
# surround the fundus camera leaves around the circular field of view.
FOV_THRESHOLD = 15

# Segmentation layers, in the order the report lists them, with the colour each
# is painted in. The source ships a mask only where annotators found something,
# so a layer missing from an image is normal, not an error.
SEGMENT_LAYERS: tuple[tuple[str, tuple[int, int, int]], ...] = (
    ("optic-disc", (64, 196, 255)),
    ("microaneurysms", (255, 64, 96)),
    ("haemorrhages", (255, 128, 32)),
    ("hard-exudates", (255, 216, 48)),
    ("soft-exudates", (96, 240, 152)),
)

# Panels render ~40 mm wide at 170 dpi in the report's 4-column grid (≈270 px),
# so 320 px carries the grid with headroom and keeps the bundle small.
SEGMENT_PANEL_W = 320
SEGMENT_JPEG_QUALITY = 80
# The unmarked retina is dimmed so the painted layer reads at thumbnail size.
SEGMENT_DIM = 0.45

# Lab descriptor weights: the mean colour is the pairing signal, its spread is a
# secondary cue (it separates a washed-out image from a contrasty one).
LAB_WEIGHTS = np.array([1.0, 1.0, 1.0, 0.5, 0.5, 0.5])


# ---------------------------------------------------------------------------
# Colour
# ---------------------------------------------------------------------------
def _srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """Convert an (N, 3) array of 0..255 sRGB samples to CIE-Lab (D65)."""
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([
        [0.4124, 0.3576, 0.1805],
        [0.2126, 0.7152, 0.0722],
        [0.0193, 0.1192, 0.9505],
    ])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([
        116 * f[:, 1] - 16,
        500 * (f[:, 0] - f[:, 1]),
        200 * (f[:, 1] - f[:, 2]),
    ], axis=1)


def _gen_fov_mask(bgr: np.ndarray) -> np.ndarray:
    """Binary FOV mask (uint8 0/255) from a resized fundus image."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, FOV_THRESHOLD, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return binary


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------
def _measure(src_dir: Path) -> list[dict]:
    """Read every source image + its disc mask → one record per eye.

    Returns records carrying the source paths, the derived side, and the Lab
    colour descriptor used for pairing. Full-resolution pixels are not kept.
    """
    records: list[dict] = []
    folders = sorted(p for p in src_dir.iterdir() if p.is_dir())
    if not folders:
        sys.exit(f"No image folders found under {src_dir}")

    for folder in folders:
        num = folder.name
        fundus = folder / f"{num}_fundus.jpg"
        disc = folder / f"{num}_mask_optic-disc.tif"
        if not fundus.exists() or not disc.exists():
            print(f"  warn: {num} missing fundus or optic-disc mask — skipped")
            continue

        with Image.open(fundus) as im:
            im = im.convert("RGB")
            width, height = im.size
            # A /8 copy is plenty for colour statistics and the FOV bounding box.
            small = np.asarray(
                im.resize((width // 8, height // 8), Image.LANCZOS)
            )

        fov = small.astype(np.float32).mean(axis=2) > FOV_THRESHOLD
        ys, xs = np.nonzero(fov)
        fov_cx = (xs.min() + xs.max()) / 2 * 8

        lab = _srgb_to_lab(small[fov].astype(np.float32))
        descriptor = np.concatenate([lab.mean(axis=0), lab.std(axis=0)])

        with Image.open(disc) as m:
            disc_mask = np.asarray(m.convert("L")) > 0
        my, mx = np.nonzero(disc_mask)
        if my.size == 0:
            print(f"  warn: {num} has an empty optic-disc mask — skipped")
            continue
        od_cx, od_cy = float(mx.mean()), float(my.mean())

        records.append({
            "num": num,
            "path": fundus,
            "width": width,
            "height": height,
            # Disc nasal to the macula: left of the FOV centre ⇒ left eye.
            "side": "left" if od_cx < fov_cx else "right",
            "od_center": (od_cx, od_cy),
            # Disc mask area → equivalent-circle radius (a real measurement,
            # where the Localization pool could only estimate it from width).
            "od_radius": float(np.sqrt(disc_mask.sum() / np.pi)),
            "descriptor": descriptor,
        })
        print(f"  {num}: {records[-1]['side']:5s}  od=({od_cx:.0f},{od_cy:.0f})")

    return records


def _pair_by_colour(records: list[dict]) -> list[tuple[dict, dict, float]]:
    """Match left eyes to right eyes so total colour mismatch is minimal."""
    left = [r for r in records if r["side"] == "left"]
    right = [r for r in records if r["side"] == "right"]
    print(f"\n  {len(left)} left, {len(right)} right "
          f"→ {min(len(left), len(right))} pairs")

    # z-score each descriptor across the whole set so no single Lab axis
    # dominates the distance purely because of its units.
    feats = np.stack([r["descriptor"] for r in records])
    mean, std = feats.mean(axis=0), feats.std(axis=0)
    std[std == 0] = 1.0

    def norm(rec: dict) -> np.ndarray:
        return (rec["descriptor"] - mean) / std * LAB_WEIGHTS

    left_f = np.stack([norm(r) for r in left])
    right_f = np.stack([norm(r) for r in right])
    cost = np.linalg.norm(left_f[:, None, :] - right_f[None, :, :], axis=2)

    rows, cols = linear_sum_assignment(cost)
    pairs = [(left[i], right[j], float(cost[i, j])) for i, j in zip(rows, cols)]
    # Best colour match first, so patient numbering is stable and p01 is the
    # most convincing pair.
    pairs.sort(key=lambda p: p[2])
    return pairs


def _drop_worst(pairs: list[tuple[dict, dict, float]], n: int) -> list:
    """Drop the ``n`` worst-matching pairs (they sort last).

    A minimal-total-cost assignment has to place every eye, so the colour
    outliers end up stranded in the last pair — the run that produced the
    current pool left a dark-orange left eye with a pale right one, which reads
    as two different people. Dropping the tail costs a pair and keeps the rest
    plausible.
    """
    if n <= 0:
        return pairs
    for left, right, dist in pairs[-n:]:
        print(f"  dropped: {left['num']}L + {right['num']}R  d={dist:.2f}")
    return pairs[:-n]


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def _process_eye(rec: dict, side_label: str, patient_no: int, max_side: int) -> dict:
    """Resize the image, write it + a FOV mask, return the eye manifest row."""
    uid = f"IDRiD_seg_p{patient_no:02d}_{side_label}_{rec['num']}"

    with Image.open(rec["path"]) as im:
        im = im.convert("RGB")
        w0, h0 = im.size
        scale = min(1.0, max_side / max(w0, h0))
        new_w, new_h = int(round(w0 * scale)), int(round(h0 * scale))
        resized = im.resize((new_w, new_h), Image.LANCZOS) if scale < 1.0 else im

        img_rel = f"{OUT_REL}/{uid}.jpg"
        resized.save(PUBLIC_ROOT / img_rel, "JPEG", quality=85, optimize=True)

        bgr = cv2.cvtColor(np.array(resized), cv2.COLOR_RGB2BGR)
        mask_rel = f"{OUT_REL}/{uid}_mask.png"
        cv2.imwrite(str(PUBLIC_ROOT / mask_rel), _gen_fov_mask(bgr))

    return {
        "id": uid,
        "source": rec["num"],
        "side": "left" if side_label == "L" else "right",
        "image": img_rel,
        "mask": mask_rel,
        "segments": _segment_panels(rec, uid),
        "segment_stats": _segment_stats(rec["path"].parent, rec["num"], rec["side"]),
        "width": new_w,
        "height": new_h,
        "od_center": [
            round(rec["od_center"][0] * scale, 1),
            round(rec["od_center"][1] * scale, 1),
        ],
        "od_radius": round(rec["od_radius"] * scale, 1),
    }


def _segment_panels(rec: dict, uid: str) -> list[str]:
    """Render one eye's annotated layers as report panels; return layer names.

    Each panel is the fundus dimmed to :data:`SEGMENT_DIM` with the layer
    painted over it. The mask is downscaled first and then dilated, because a
    microaneurysm is ~15 px across in a 4288-px-wide original and would vanish
    entirely at panel size; the optic disc is large enough to need no help.
    """
    folder = rec["path"].parent
    with Image.open(rec["path"]) as im:
        im = im.convert("RGB")
        w0, h0 = im.size
        panel_h = max(1, round(h0 * SEGMENT_PANEL_W / w0))
        base = np.asarray(
            im.resize((SEGMENT_PANEL_W, panel_h), Image.LANCZOS)
        ).astype(np.float32)

    dimmed = base * SEGMENT_DIM
    written: list[str] = []

    for layer, colour in SEGMENT_LAYERS:
        mask_path = folder / f"{rec['num']}_mask_{layer}.tif"
        if not mask_path.exists():
            continue
        with Image.open(mask_path) as m:
            full = (np.asarray(m.convert("L")) > 0).astype(np.uint8) * 255
        # INTER_AREA keeps a trace of every annotated blob; >0 turns that trace
        # back into a mask instead of losing it to nearest-neighbour sampling.
        small = cv2.resize(full, (SEGMENT_PANEL_W, panel_h), interpolation=cv2.INTER_AREA)
        painted = small > 0
        if not painted.any():
            continue
        if layer != "optic-disc":
            painted = cv2.dilate(
                painted.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1
            ).astype(bool)

        panel = dimmed.copy()
        panel[painted] = colour
        out_name = f"{uid}__{layer}.jpg"
        Image.fromarray(panel.astype(np.uint8)).save(
            SEGMENTS_DIR / out_name, "JPEG",
            quality=SEGMENT_JPEG_QUALITY, optimize=True,
        )
        written.append(layer)

    return written


def _fovea(folder: Path, num: str, disc_c: np.ndarray, dd: float, side: str) -> tuple:
    """Fovea centre in source pixels, and where it came from.

    41 of the 54 images are also in IDRiD's Localization part, whose expert
    fovea markups are carried in :data:`FOVEA_TABLE` (matched by thumbnail and
    checked against the disc centre). The rest are placed at the mean
    disc-to-fovea offset measured on those 41 — median error 0.24 DD.
    """
    known = _fovea_table().get(num)
    if known:
        return np.array(known["fovea"], dtype=np.float64), "expert"
    temporal = -1.0 if side == "right" else 1.0  # right eye: fovea left of the disc
    offset = np.array([FOVEA_OFFSET_DD[0] * temporal, FOVEA_OFFSET_DD[1]]) * dd
    return disc_c + offset, "estimated"


_FOVEA_CACHE: dict | None = None


def _fovea_table() -> dict:
    global _FOVEA_CACHE
    if _FOVEA_CACHE is None:
        _FOVEA_CACHE = (
            json.loads(FOVEA_TABLE.read_text(encoding="utf-8")) if FOVEA_TABLE.exists() else {}
        )
    return _FOVEA_CACHE


def _segment_stats(folder: Path, num: str, side: str) -> dict:
    """Measure one eye's annotated layers at full resolution, against its disc.

    Sizes are given in disc units, as an ophthalmologist reads a fundus: the
    disc diameter (DD) for distances and the disc area (DA) for areas, since a
    photograph has no absolute scale. The macula is the 1-DD circle around the
    fovea.

    Args:
        folder: The source folder holding ``{num}_fundus.jpg`` and its masks.
        num: The source folder name (``01``..``54``).
        side: ``"left"`` or ``"right"`` — which way the fovea lies from the disc.

    Returns:
        ``{"fovea": [x, y], "disc_diameter": d, "fovea_source": ..., "layers": {...}}``
        with ``fovea`` as fractions of the image width/height and
        ``disc_diameter`` as a fraction of its width. Each layer carries
        ``area_pct`` (% of the retinal field), ``area_da``, ``count`` (8-connected
        foci), ``quadrants`` (how many fovea-centred quadrants hold a focus),
        ``nearest_dd`` (closest lesion pixel to the fovea) and ``in_macula`` (foci
        reaching within 1 DD of it). Layers without a mask are absent.
    """
    with Image.open(folder / f"{num}_fundus.jpg") as im:
        grey = np.asarray(im.convert("L"))
    h, w = grey.shape
    fov_px = int((grey > FOV_THRESHOLD).sum()) or grey.size

    with Image.open(folder / f"{num}_mask_optic-disc.tif") as m:
        disc = np.asarray(m.convert("L")) > 0
    disc_px = int(disc.sum())
    ys, xs = np.nonzero(disc)
    disc_c = np.array([xs.mean(), ys.mean()])
    dd = 2.0 * float(np.sqrt(disc_px / np.pi))
    fovea, source = _fovea(folder, num, disc_c, dd, side)

    layers: dict[str, dict] = {}
    for layer, _ in SEGMENT_LAYERS:
        mask_path = folder / f"{num}_mask_{layer}.tif"
        if not mask_path.exists():
            continue
        with Image.open(mask_path) as m:
            mask = (np.asarray(m.convert("L")) > 0).astype(np.uint8)
        if not mask.any():
            continue
        n_labels, labels = cv2.connectedComponents(mask, connectivity=8)
        ly, lx = np.nonzero(mask)
        dist = np.hypot(lx - fovea[0], ly - fovea[1]) / dd
        entry: dict = {
            "area_pct": round(100.0 * lx.size / fov_px, 3),
            "area_da": round(lx.size / disc_px, 3),
            "count": int(n_labels - 1),
        }
        if layer != "optic-disc":
            quads = {(bool(x > fovea[0]), bool(y > fovea[1])) for x, y in zip(lx, ly)}
            entry.update({
                "quadrants": len(quads),
                "nearest_dd": round(float(dist.min()), 2),
                "in_macula": int(np.unique(labels[ly[dist <= 1.0], lx[dist <= 1.0]]).size),
            })
        layers[layer] = entry

    return {
        "fovea": [round(fovea[0] / w, 4), round(fovea[1] / h, 4)],
        "disc_diameter": round(dd / w, 4),
        "fovea_source": source,
        "layers": layers,
    }


def _write_js(patients: list[dict]) -> None:
    header = (
        "// Auto-generated by demo/web/scripts/prepare_segmentation_pairs.py.\n"
        "// Edit the script and re-run; do not modify this file by hand.\n"
        "// Source: IDRiD (CC-BY-4.0) — Segmentation sub-challenge, training set.\n"
        "// Synthetic bilateral patients: the source is monocular, so each pair is\n"
        "// one left + one right eye (laterality measured from the optic-disc mask)\n"
        "// matched on retinal colour so a drawn pair reads as one person.\n"
        "// `grade` is null — DR grades are not part of this subset.\n"
        f"// {len(patients)} patients ({len(patients) * 2} images).\n\n"
    )
    body = "export const SEGMENTATION_PATIENTS = " + json.dumps(patients, indent=2) + ";\n"
    OUT_JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_JS_PATH.write_text(header + body, encoding="utf-8")


def _write_attribution(src_dir: Path, n_patients: int) -> None:
    """Carry the dataset's CC-BY attribution next to the images."""
    for name in ("LICENSE.txt", "CC-BY-4.0.txt"):
        srcfile = src_dir / name
        if srcfile.exists():
            shutil.copy2(srcfile, OUT_PUBLIC_DIR / name)
    (OUT_PUBLIC_DIR / "README.md").write_text(
        "# Demo sample pairs\n\n"
        "Fundus images behind the Demo tab's \"Random sample\" button, resized\n"
        f"from the IDRiD Segmentation training set ({n_patients} synthetic\n"
        f"bilateral patients, {n_patients * 2} images). Generated by\n"
        "`demo/web/scripts/prepare_segmentation_pairs.py`; see `patients.json`.\n\n"
        "Dataset (c) Prasanna Porwal, Samiksha Pachade, Manesh Kokare,\n"
        "licensed CC BY 4.0 — see `LICENSE.txt`.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC,
                    help=f"source dataset directory (default: {DEFAULT_SRC})")
    ap.add_argument("--max-size", type=int, default=512,
                    help="max image side in pixels (default: 512)")
    ap.add_argument("--drop-worst", type=int, default=1, metavar="N",
                    help="discard the N worst colour matches (default: 1)")
    args = ap.parse_args()

    if not args.src.exists():
        sys.exit(f"Source not found: {args.src}")

    print(f"Reading {args.src} ...")
    records = _measure(args.src)
    pairs = _drop_worst(_pair_by_colour(records), args.drop_worst)

    for directory in (OUT_PUBLIC_DIR, SEGMENTS_DIR):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    print("\nWriting pairs ...")
    patients = []
    for i, (left, right, dist) in enumerate(pairs, start=1):
        patients.append({
            "patient": f"p{i:02d}",
            "grade": None,  # not available in the segmentation subset
            "colour_distance": round(dist, 3),
            "left": _process_eye(left, "L", i, args.max_size),
            "right": _process_eye(right, "R", i, args.max_size),
        })
        print(f"  p{i:02d}: {left['num']}L + {right['num']}R  d={dist:.2f}")

    # report.py looks an eye up by the filename the client filed it under, so
    # the index is keyed by image id and holds only the layers that exist, each
    # with its measured area and focus count for the report's findings column.
    index = {}
    for p in patients:
        for eye in (p["left"], p["right"]):
            if eye["segments"]:
                stats = eye["segment_stats"]
                stats["layers"] = {k: v for k, v in stats["layers"].items()
                                   if k in eye["segments"]}
                index[eye["id"]] = stats
    for p in patients:
        for side in ("left", "right"):
            p[side].pop("segment_stats", None)
    SEGMENTS_INDEX_PATH.write_text(json.dumps(index, indent=1), encoding="utf-8")

    OUT_JSON_PATH.write_text(json.dumps(patients, indent=2), encoding="utf-8")
    _write_js(patients)
    _write_attribution(args.src, len(patients))

    worst = max(p["colour_distance"] for p in patients)
    panels = sum(len(v["layers"]) for v in index.values())
    print(f"\nDone: {len(patients)} patients, {len(patients) * 2} images.")
    print(f"  colour distance — worst pair {worst:.2f}")
    print(f"  {panels} segmentation panels over {len(index)} eyes")
    print(f"  {OUT_PUBLIC_DIR}")
    print(f"  {OUT_JS_PATH}")
    print(f"  {SEGMENTS_DIR}")


if __name__ == "__main__":
    main()
