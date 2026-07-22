"""Unit tests for Stage 2/3 FOV crop + resize + mask generation."""

import numpy as np
import pytest

from src.preprocessing.crop_resize import (
    _bbox_from_mask,
    _fov_foreground_mask,
    crop_and_resize,
)


def _fundus_on_surround(w: int, h: int, radius_frac: float = 0.48) -> np.ndarray:
    """Bright elliptical fundus centred on a near-black camera surround."""
    yy, xx = np.mgrid[0:h, 0:w]
    ry = radius_frac * h
    rx = radius_frac * h  # circular, as a real fundus is
    disc = (((xx - w / 2) / rx) ** 2 + ((yy - h / 2) / ry) ** 2) <= 1.0

    img = np.zeros((h, w, 3), np.uint8)
    img[..., 0] = np.where(disc, 180, 4)
    img[..., 1] = np.where(disc, 110, 4)
    img[..., 2] = np.where(disc, 60, 4)
    return img


def _full_frame_fundus(w: int, h: int) -> np.ndarray:
    """Retina filling the entire frame — no dark surround (APTOS-style)."""
    img = np.empty((h, w, 3), np.uint8)
    img[..., 0] = 190
    img[..., 1] = 120
    img[..., 2] = 70
    return img


def test_crop_tightens_to_fundus_on_dark_surround() -> None:
    """A fundus on a black surround is cropped to its bounding box."""
    img = _fundus_on_surround(1200, 800)
    _canvas, _mask, tf = crop_and_resize(img, 256, return_transform=True)

    left, upper, right, lower = tf.bbox
    # The disc spans 0.96*h ≈ 768 px, centred: the box must hug it, not the frame.
    assert right - left == pytest.approx(768, abs=12)
    assert lower - upper == pytest.approx(768, abs=12)
    assert left > 100 and right < 1100


def test_full_frame_fundus_is_not_cropped() -> None:
    """Regression: a frame with no dark surround must not be centre-square cropped.

    The old detect_fov_bbox estimated background from the *max* of the edge
    columns; when those columns are retina it admitted no foreground, and the
    centre-square fallback discarded ~25% of a 4:3 retina (measured 20.8% mean
    on APTOS, taking the optic disc with it).
    """
    w, h = 640, 480
    img = _full_frame_fundus(w, h)
    _canvas, mask, tf = crop_and_resize(img, 256, return_transform=True)

    assert tf.bbox == (0, 0, w, h), "whole-frame retina must survive Stage 2 intact"
    # Every real pixel stays inside the FOV; only the letterbox padding is 0.
    assert mask.sum() > 0
    assert mask[mask > 0].size == tf.new_w * tf.new_h


def test_mask_excludes_surround_but_keeps_dark_interior() -> None:
    """Mask covers the disc, drops the surround, and fills interior dark spots."""
    img = _fundus_on_surround(1000, 1000)
    # A dark lesion inside the fundus must not punch a hole in the FOV.
    img[480:520, 480:520] = 3

    _canvas, mask, _tf = crop_and_resize(img, 256, return_transform=True)
    cov = float((mask > 0).mean())
    assert 0.6 < cov < 0.9, f"expected a disc inscribed in the canvas, got {cov:.2f}"
    assert mask[128, 128] == 1.0, "interior dark lesion was excluded from the FOV"
    assert mask[0, 0] == 0.0, "corner surround leaked into the FOV"


def test_supplied_mask_drives_the_box_in_both_conventions() -> None:
    """A caller mask is honoured whether it is 0/255 uint8 or 0.0/1.0 float."""
    img = _full_frame_fundus(900, 900)
    m = np.zeros((900, 900), np.uint8)
    m[200:700, 300:800] = 255

    _c1, _m1, t_u8 = crop_and_resize(img, 256, return_transform=True, fov_mask=m)
    _c2, _m2, t_f32 = crop_and_resize(
        img, 256, return_transform=True, fov_mask=(m > 0).astype(np.float32)
    )

    assert t_u8.bbox == (300, 200, 800, 700)
    assert t_f32.bbox == t_u8.bbox, "float 0.0/1.0 mask must not empty the box"


def test_bbox_from_mask_rejects_collapsed_segmentation() -> None:
    """An empty or implausibly small mask yields None, not a degenerate box."""
    assert _bbox_from_mask(np.zeros((100, 100), np.uint8)) is None

    speck = np.zeros((100, 100), np.uint8)
    speck[50:53, 50:53] = 255
    assert _bbox_from_mask(speck) is None


def test_foreground_mask_falls_back_to_full_frame() -> None:
    """With no isolable dark surround the whole frame counts as valid data."""
    mask = _fov_foreground_mask(_full_frame_fundus(300, 300))
    assert (mask > 0).all()


def test_output_geometry_and_aspect_are_preserved() -> None:
    """Output is a square canvas; the fundus keeps its aspect ratio."""
    img = _fundus_on_surround(1200, 800)
    canvas, mask, tf = crop_and_resize(img, 512, return_transform=True)

    assert canvas.shape == (512, 512, 3)
    assert mask.shape == (512, 512)
    assert mask.dtype == np.float32
    assert set(np.unique(mask)) <= {0.0, 1.0}
    assert max(tf.new_w, tf.new_h) == 512

    src_ar = (tf.bbox[2] - tf.bbox[0]) / (tf.bbox[3] - tf.bbox[1])
    assert tf.new_w / tf.new_h == pytest.approx(src_ar, rel=0.02)
