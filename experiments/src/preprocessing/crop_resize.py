"""
Stage 1: FOV Crop + Isotropic Resize + FOV Mask generation.

Replaces Hough-circle FOV detection (``fov.py``) with connected-component
foreground segmentation: the background level is estimated from the frame
corners, the largest bright component is kept, and enclosed holes are filled.
That one mask yields both the crop region (its bounding box) and the 4th input
channel, so the two cannot drift apart.

Isotropic scaling preserves the fundus circle geometry: the cropped region is
scaled to fit within ``target_size`` while maintaining aspect ratio, then
centered on a zero-padded canvas.  A binary FOV mask is returned alongside the
image: 1.0 inside the actual (roughly circular) field of view, 0.0 on the dark
camera surround AND on the zero padding.  The mask is segmented from the image,
not taken as the non-padding rectangle, so the dark corners between the fundus
circle and its bounding box are correctly excluded.

Images whose fundus already fills the frame (no dark surround) segment to an
all-ones mask and are therefore passed through uncropped, rather than being
centre-square cropped — that fallback cuts ~25% of the retina off a 4:3 frame
and now triggers only if segmentation collapses outright.

Input/output images are RGB uint8 NumPy arrays.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image, ImageFilter


@dataclass
class CropResizeTransform:
    """Geometric transform applied by :func:`crop_and_resize`.

    Maps a point from pre-crop (oriented) image space into the padded
    ``target_size`` × ``target_size`` output canvas. Used to project
    OD/fovea coordinates (detected in pre-crop space) into analysis space
    for visualization.

    Attributes:
        bbox: ``(left, upper, right, lower)`` crop box in source pixels.
        scale: Isotropic scale factor applied after cropping.
        x_off: Horizontal padding offset on the output canvas.
        y_off: Vertical padding offset on the output canvas.
        new_w: Width of the resized (pre-pad) region.
        new_h: Height of the resized (pre-pad) region.
        target_size: Output canvas side length.
    """

    bbox: tuple[int, int, int, int]
    scale: float
    x_off: int
    y_off: int
    new_w: int
    new_h: int
    target_size: int

    def apply(self, x: float, y: float) -> tuple[float, float]:
        """Project a pre-crop point ``(x, y)`` into output-canvas pixels."""
        left, upper = self.bbox[0], self.bbox[1]
        return (
            (x - left) * self.scale + self.x_off,
            (y - upper) * self.scale + self.y_off,
        )


def detect_fov_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    """
    Detect the fundus FOV bounding box using PIL-based foreground detection.

    .. deprecated::
        Legacy heuristic, no longer used by :func:`crop_and_resize`, which now
        derives the crop box from :func:`_fov_foreground_mask` so the box and
        the 4th-channel mask come from one segmentation. Retained only because
        it is part of the module's published API.

        It estimates the background from the *maximum* of the leftmost and
        rightmost ``w // 32`` columns, which silently fails on frames where the
        fundus reaches the horizontal edges (APTOS, and any already-cropped
        image): the edge columns are retina, so ``max_bg`` saturates, the
        foreground test admits nothing, and the caller falls back to a
        centre-square crop that discards ~25% of the retina.

    Samples the leftmost and rightmost ``w // 32`` columns to estimate the
    background level per channel, then finds the bounding box of all pixels
    that exceed ``max_bg + 10``.  Detection is only attempted for landscape
    images (``w > 1.2 * h``); returns ``None`` for square/portrait images.

    Args:
        image: PIL Image in RGB mode.

    Returns:
        ``(left, upper, right, lower)`` bounding box, or ``None`` if
        detection fails or the detected region is too small (< 0.8 × h in
        either dimension).
    """
    blurred = image.filter(ImageFilter.BLUR)
    ba = np.array(blurred)          # (H, W, 3) uint8
    h, w, _ = ba.shape

    if w > 1.2 * h:
        left_max = ba[:, : w // 32, :].max(axis=(0, 1)).astype(int)   # (3,)
        right_max = ba[:, -w // 32 :, :].max(axis=(0, 1)).astype(int) # (3,)
        max_bg = np.maximum(left_max, right_max)                       # (3,)

        # Foreground: any channel exceeds background + 10
        foreground = (ba > max_bg + 10).any(axis=2).astype(np.uint8)  # (H, W)

        bbox = Image.fromarray(foreground).getbbox()

        if bbox is not None:
            left, upper, right, lower = bbox
            if (right - left) < 0.8 * h or (lower - upper) < 0.8 * h:
                bbox = None

        return bbox  # may be None after the size check

    return None


def detect_is_cropped(image: np.ndarray) -> bool:
    """Detect whether the fundus circle is cropped by the camera frame.

    Uses three concordant checks:
    1. Circle fit test — max inscribed circle extends beyond image bounds.
    2. Border touch test — foreground mask touches image edges.
    3. Arc coverage test — contour arc length < 90% of expected circumference.

    Final decision: is_cropped = (not fits) OR touches_border OR (coverage < 0.9).

    Args:
        image: RGB uint8 NumPy array of shape (H, W, 3).

    Returns:
        True if the fundus circle appears cropped.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Threshold to separate fundus from background
    _, binary = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)

    h, w = binary.shape

    # Check 1: Circle fit test via distance transform
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, max_r, _, max_loc = cv2.minMaxLoc(dist)
    cx, cy = max_loc
    margin = 2
    fits = (cx - max_r >= -margin and cx + max_r <= w + margin and
            cy - max_r >= -margin and cy + max_r <= h + margin)

    # Check 2: Border touch test
    touches_border = (
        binary[0, :].any() or           # top row
        binary[-1, :].any() or          # bottom row
        binary[:, 0].any() or           # left column
        binary[:, -1].any()             # right column
    )

    # Check 3: Arc coverage test
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    coverage = 1.0  # default: assume full circle
    if contours and max_r > 10:
        largest = max(contours, key=cv2.contourArea)
        arc_length = cv2.arcLength(largest, closed=False)
        expected_circumference = 2.0 * np.pi * max_r
        coverage = arc_length / expected_circumference if expected_circumference > 0 else 1.0

    return (not fits) or touches_border or (coverage < 0.9)


def _fov_foreground_mask(image_rgb: np.ndarray) -> np.ndarray:
    """Segment the actual field of view (the bright fundus disc) from background.

    The fundus occupies a roughly circular region; the rest of the frame is the
    camera's near-black surround. The background level is estimated from the four
    image corners, the image is thresholded above it, the largest connected
    component is kept (dropping speckle), and enclosed holes are filled so dark
    interior structures (macula, lesions) stay inside the FOV.

    If a plausible FOV cannot be isolated — e.g. an already tightly-cropped image
    with no dark surround, where the corners are as bright as the fundus — the
    whole frame is treated as valid data (safe fallback to the old behaviour).

    Args:
        image_rgb: RGB uint8 array of shape (H, W, 3).

    Returns:
        uint8 array of shape (H, W) with 255 inside the FOV and 0 outside.
    """
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape

    # Background estimate from the corners (camera surround / zero padding).
    c = max(2, min(h, w) // 32)
    corners = np.concatenate([
        gray[:c, :c].ravel(), gray[:c, -c:].ravel(),
        gray[-c:, :c].ravel(), gray[-c:, -c:].ravel(),
    ])
    thr = max(int(corners.max()) + 10, 12)

    fg = np.where(gray > thr, 255, 0).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel)

    # Keep the largest connected component (the fundus), drop speckle.
    num, labels, stats, _ = cv2.connectedComponentsWithStats(fg, connectivity=8)
    if num > 1:
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        fg = np.where(labels == largest, 255, 0).astype(np.uint8)

    # Fill enclosed holes: flood the background inward from a guaranteed-background
    # 1px border, then OR back whatever the flood could not reach (the interior).
    bordered = cv2.copyMakeBorder(fg, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    flood = bordered.copy()
    cv2.floodFill(flood, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 255)
    holes = cv2.bitwise_not(flood)[1:-1, 1:-1]
    fg = cv2.bitwise_or(fg, holes)

    # Defensive fallback: a real fundus circle covers ~78% of its bounding box;
    # if we isolated implausibly little, assume the whole frame is valid data.
    if int((fg > 0).sum()) < 0.30 * h * w:
        fg = np.full((h, w), 255, np.uint8)
    return fg


def _bbox_from_mask(
    mask: np.ndarray,
    min_frac: float = 0.15,
) -> tuple[int, int, int, int] | None:
    """Tight bounding box of a binary FOV mask.

    Args:
        mask: ``(H, W)`` array, non-zero (>127) inside the FOV.
        min_frac: Reject boxes narrower/shorter than this fraction of the
            frame in either dimension — such a box means the segmentation
            collapsed, and cropping to it would throw away retina.

    Returns:
        ``(left, upper, right, lower)``, or ``None`` if the mask is empty or
        the box is implausibly small.
    """
    binary = np.asarray(mask) > 127
    ys, xs = np.nonzero(binary)
    if ys.size == 0:
        return None

    h, w = binary.shape[:2]
    left, right = int(xs.min()), int(xs.max()) + 1
    upper, lower = int(ys.min()), int(ys.max()) + 1
    if (right - left) < min_frac * w or (lower - upper) < min_frac * h:
        return None
    return (left, upper, right, lower)


def crop_and_resize(
    image: np.ndarray,
    target_size: int = 512,
    return_transform: bool = False,
    fov_mask: np.ndarray | None = None,
) -> (
    tuple[np.ndarray, np.ndarray]
    | tuple[np.ndarray, np.ndarray, CropResizeTransform]
):
    """Crop to the FOV region and resize to target_size × target_size.

    Uses isotropic scaling with centered padding to preserve the fundus
    circle geometry. Returns a binary mask indicating real pixel data
    (1.0) vs padding (0.0).

    The crop box and the FOV mask are derived from a **single** segmentation,
    so the box can never disagree with the mask it is cropped against:

    - If *fov_mask* is supplied (the recommended path), it is assumed to already
      be in the **same geometry as** *image* (i.e. flipped + rotated by the
      caller with ``BORDER_CONSTANT``). Deriving the box from it also keeps the
      reflected ``BORDER_REFLECT`` corners the RGB rotation introduces from
      inflating the box.
    - Otherwise the mask is segmented from the full frame via
      :func:`_fov_foreground_mask`, whose dark surround gives a clean background
      estimate, and which falls back to an all-ones mask when the fundus fills
      the frame (already-cropped images).

    A centre-square crop is used only if that segmentation collapses entirely;
    it discards real retina on wide frames, so it is a last resort rather than
    the routine path for non-landscape images.

    Args:
        image: RGB uint8 NumPy array of shape (H, W, 3).
        target_size: Output spatial resolution in pixels (square).
        return_transform: If ``True``, also return the
            :class:`CropResizeTransform` describing the crop/scale/pad so
            callers can project source-space points into the output canvas.
        fov_mask: Optional pre-built FOV mask (``(H, W)``, either 0/255 uint8
            or 0.0/1.0 float, same geometry as *image*) used for both the crop
            box and the output mask instead of segmenting *image*.

    Returns:
        Tuple of:
          - image: RGB uint8 NumPy array of shape (target_size, target_size, 3).
          - mask: float32 NumPy array of shape (target_size, target_size)
                  with 1.0 inside the FOV and 0.0 outside (camera surround +
                  zero padding).
          - transform (only when ``return_transform``): the
            :class:`CropResizeTransform` used.
    """
    pil_img = Image.fromarray(image)
    w, h = pil_img.size  # PIL: (width, height)

    # One segmentation drives both the crop box and the 4th-channel mask, so the
    # two can never disagree. Either the caller's mask (already in this image's
    # geometry, BORDER_CONSTANT-rotated so the RGB's reflected corners are
    # excluded) or a fresh segmentation of the full frame — full frame, not the
    # crop, so the dark surround is available for the background estimate.
    if fov_mask is not None:
        supplied = np.asarray(fov_mask)
        # Accept both conventions the signature advertises: 0/255 uint8 and
        # 0.0/1.0 float. Thresholding a float mask at 127 would empty it, and
        # the box now derives from this mask, so the crop would silently
        # degrade to the lossy centre-square fallback.
        cutoff = 127 if supplied.max() > 1 else 0
        source_mask = (supplied > cutoff).astype(np.uint8) * 255
    else:
        source_mask = _fov_foreground_mask(image)

    bbox = _bbox_from_mask(source_mask)

    if bbox is None:
        # Segmentation collapsed. Centre-square crop is the last resort; it is
        # lossy by construction, so it must not be reachable merely because the
        # fundus fills the frame (that case yields an all-ones mask above).
        left = max((w - h) // 2, 0)
        upper = 0
        right = min(w - (w - h) // 2, w)
        lower = h
        bbox = (left, upper, right, lower)

    cropped = pil_img.crop(bbox)
    crop_w, crop_h = cropped.size

    # Isotropic resize: scale to fit within target_size, then pad
    scale = target_size / max(crop_h, crop_w)
    new_w = int(crop_w * scale)
    new_h = int(crop_h * scale)

    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    resized_arr = np.array(resized, dtype=np.uint8)

    # Create canvas with zero padding
    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    y_off = (target_size - new_h) // 2
    x_off = (target_size - new_w) // 2
    canvas[y_off : y_off + new_h, x_off : x_off + new_w] = resized_arr

    # FOV mask: 1.0 inside the actual (roughly circular) field of view, 0.0 on
    # the dark camera surround AND on the zero padding. Either crop+resize the
    # caller-supplied mask (built in the same geometry, BORDER_CONSTANT-rotated
    # so reflected corners are excluded), or — when none is given — segment it
    # from the cropped RGB. Never a plain non-padding rectangle, whose corners
    # would falsely mark background as valid data.
    left, upper, right, lower = bbox
    fov_full = source_mask[upper:lower, left:right]
    fov_resized = cv2.resize(fov_full, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
    mask = np.zeros((target_size, target_size), dtype=np.float32)
    mask[y_off : y_off + new_h, x_off : x_off + new_w] = (fov_resized > 127).astype(np.float32)

    if return_transform:
        transform = CropResizeTransform(
            bbox=tuple(bbox), scale=scale, x_off=x_off, y_off=y_off,
            new_w=new_w, new_h=new_h, target_size=target_size,
        )
        return canvas, mask, transform

    return canvas, mask
