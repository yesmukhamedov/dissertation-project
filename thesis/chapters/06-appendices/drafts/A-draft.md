> Ported from the superseded appendices, re-lettered, with the provenance banner,
> section signs and internal codes removed and cross-references renumbered to the
> four-chapter body. Transcription content is unchanged. Provenance: `outline/REWRITE_MAP.md`.

# Appendix A – Source code of the preprocessing pipeline

---

## PART 1: SECTION TEXT

Section 3.1 undertook to reproduce the preprocessing and training code here, so that the
transformation applied to every image is recoverable as source rather than described only in prose.
This appendix discharges that undertaking. Its inclusion is not incidental documentation. Under the
central thesis of this work, that the model is the composition of preprocessing and the
convolutional network, the preprocessing source is part of the model specification. Reproducing it
is what makes that thesis auditable rather than merely asserted.

The code is organized as a Python package under `experiments/src/`. The preprocessing stack lives in
`experiments/src/preprocessing/`, whose public interface is exported from its `__init__.py` and
whose orchestrator, `PreprocessingPipeline` in `pipeline.py`, chains the eight stages in the order
specified in chapter 2.

The remaining apparatus is distributed across sibling subpackages. `data/` holds the dataset
loaders, the patient-level stratified splitter, unified augmentation and label harmonization;
`models/` the two backbone factories and the two-stage fine-tuning utility; `training/` the training
loop, the weighted focal loss and checkpoint management.

`evaluation/` holds the metrics, calibration and statistical tests, `explainability/` the attention
maps and overlay rendering, `experiments/` the experiment drivers, and `utils/` the configuration
handling, the reproducibility seed utility and the image-quality metrics. The catalogue below is
confined to the preprocessing package; the wider tree is named only so the reproduction is locatable
in full.

Table A.1 maps each pipeline stage of chapter 2 to the module that implements it. Every path is
given relative to the repository root and corresponds to a file present in the versioned source
tree.

**Table A.1 – Pipeline stage → implementing module (`experiments/src/preprocessing/`).**

| Stage | Description (chapter 2) | Implementing module |
|-------|--------------------|---------------------|
| 0 | Canonical flip (left→right eye orientation) | `canonical_flip.py`, `canonical_orientation.py` |
| 1 | OD–fovea rotation normalization | `od_fovea_detect.py`, `canonical_orientation.py` |
| 2 | FOV crop + isotropic resize to 512×512 (centered zero-padding) | `crop_resize.py` |
| 3 | FOV mask generation (binary → 4th channel) | `crop_resize.py` (mask returned with the resized image) |
| 4 | Flat-field correction (adaptive σ = 0.07·D, inside mask) | `flat_field.py` |
| 5 | Dual-constraint CLAHE (LAB L-channel; stochastic at train) | `upgraded_clahe.py`, `polar_clahe.py`, `clahe.py` |
| 6 | Augmentation (unified affine + ColorJitter + Gaussian noise + JPEG compression; train only) | `experiments/src/data/augmentation_unified.py` |
| 7 | Dataset-specific normalize → tensor (always last) | `imagenet_normalize.py` |
| — | Configuration surface (baseline vs full-pipeline presets) | `config.py` (`PreprocessingConfig`, `PIPELINE_PRESETS`) |
| — | Stage orchestration (fixed execution order) | `pipeline.py` (`PreprocessingPipeline`) |

Stage 5 is implemented by more than one module because the pipeline ships with a polar variant of
the dual-constraint CLAHE as its current default (`polar_clahe.py`), alongside the rectilinear
tile-based formulation (`upgraded_clahe.py`); both are present in the versioned source and are
reproduced as catalogued. Stages 0 to 5 and 7 are applied identically at training and inference,
except that the Stage 5 contrast enhancement is stochastic at training time. Stage 6 augmentation is
applied only during training, and is inserted before the Stage 7 normalization so that it operates
on `uint8` images. The baseline arm bypasses Stages 0 to 6 in favour of a stretch-resize to 512x512
followed by generic normalization on three channels, selected through the configuration preset
rather than by editing the pipeline. The integrated arm runs all eight stages and emits four
channels, the three colour channels plus the field-of-view mask.

To establish that this catalogue reproduces real source rather than a paraphrase of it, the Stage 4
flat-field module is reproduced verbatim from `experiments/src/preprocessing/flat_field.py`:

```python
"""
Stage 4: Flat-Field Correction.

Reduces uneven illumination by subtracting a heavily blurred version of the
image and re-centering at 128:

 corrected = image − GaussianBlur(image, σ) + 128

A large σ captures only the low-frequency illumination gradient, so the
subtraction removes broad brightness variation while preserving local vessel
and lesion detail.

σ is computed adaptively as σ = 0.07 × FOV_diameter. Correction
is applied only inside the FOV mask (padding pixels are left at zero).

Input/output images are RGB uint8 NumPy arrays.
"""

from __future__ import annotations

import cv2
import numpy as np

def apply_flat_field(
 image: np.ndarray,
 sigma: float = 45.0,
 mask: np.ndarray | None = None,
) -> np.ndarray:
 """
 Apply flat-field correction to reduce uneven illumination.

 Algorithm::

 blur = GaussianBlur(image, σ)
 corrected = image − blur + 128

 When *mask* is provided, correction is applied only inside the mask
 (``mask > 0``). Padding areas (``mask == 0``) are left at zero.

 Kernel size is derived automatically from *sigma* (passed as ``(0, 0)``
 to:func:`cv2.GaussianBlur`).

 Args:
 image: RGB uint8 NumPy array of shape ``(H, W, 3)``.
 sigma: Gaussian blur σ controlling the spatial scale of the
 illumination estimate.
 mask: Optional binary mask of shape ``(H, W)`` (float32 or uint8).
 When provided, only pixels where ``mask > 0`` are corrected;
 padding regions remain zero.

 Returns:
 Corrected RGB uint8 NumPy array of shape ``(H, W, 3)``.
 """
 blur = cv2.GaussianBlur(image, (0, 0), sigma)
 corrected = image.astype(np.float32) - blur.astype(np.float32) + 128.0
 corrected = np.clip(corrected, 0, 255).astype(np.uint8)
 if mask is not None:
 mask_3ch = np.expand_dims(mask > 0, axis=-1).astype(np.uint8)
 corrected = corrected * mask_3ch # zero out padding
 return corrected
```

The remaining modules follow the same conventions: type-hinted signatures, `Args`/`Returns`
docstrings, paths resolved from configuration rather than hardcoded, and `pathlib.Path` throughout.
They are reproduced in full from the same package.

The pipeline lineage descends from the candidate's prior published work on contrast enhancement and
on preprocessing-classification integration, cited throughout as prior own work. The source
reproduced here consolidates that line into the single versioned eight-stage system specified in
chapter 2.

The source is reproducible on equivalent hardware, but the computational-efficiency characteristics
it exhibits remain specific to the documented setup, and no claim of performance, accuracy or
deployment readiness is made by reproducing it. With the source catalogued and one module shown to
be the real on-disk implementation, the reproducibility loop opened in section 3.1 closes: the fixed
configuration of Table 3.2, the documented hardware and this versioned code together render the
experimental pipeline recoverable.

---
