---
name: stage2-fov-crop-fix
description: "Stage 2 FOV crop discarded ~21% of the retina on frames with no dark surround (APTOS); fixed 2026-07-19 by deriving the crop box from the FOV mask"
metadata:
  type: project
---

**Fixed 2026-07-19** in `experiments/src/preprocessing/crop_resize.py`.

**The bug.** `detect_fov_bbox()` estimated the background from the **maximum** of
the leftmost/rightmost `w//32` columns. On frames where the fundus reaches the
horizontal edges — every APTOS image, and any already-cropped fundus — those
columns *are* retina, so `max_bg` saturated (up to 255), the `> max_bg + 10`
foreground test admitted nothing, `getbbox()` returned `None`, and
`crop_and_resize` fell back to a **centre-square crop that cut ~25% off a 4:3
frame, frequently removing the optic disc**. The 0.8·h size guard did not catch
it. Measured retina loss (12 imgs/dataset, vs a corner-percentile reference):
APTOS 20.75% mean / 25.47% max, IDRiD 0.41%/3.12%, all other datasets 0.00%.
The FOV **mask** itself was never the culprit — it was correct (all-ones on
APTOS); Stage 2's box was.

**The fix.** The crop box now comes from `_bbox_from_mask()` applied to the same
segmentation that becomes the 4th input channel — the caller's `fov_mask` when
supplied (which also stops the RGB rotation's `BORDER_REFLECT` "ears" from
inflating the box), else `_fov_foreground_mask()` on the full frame. Box and
mask are consistent by construction, and the centre-square path is now reachable
only if segmentation collapses outright. After: retina loss 0.00% on all eight
datasets. `detect_fov_bbox()` kept but marked deprecated and no longer called.

**The existing Config D checkpoint stays valid — no retraining needed.** EyePACS
boxes moved only 1–2 px (mean |ΔRGB| 1.22/255). Running the real
`config_d_fold0.pt` through the demo path on 40 labelled EyePACS images, old vs
new: exact-match **35/40 → 37/40**, within-1 grade 39/40 both, old-vs-new
agreement 37/40, and all three disagreements moved *toward* ground truth. See
[[demo-stack]], [[exp1-run-mechanics-512-cache]].

**Exp 3 RE-DERIVED 2026-07-28 — the verdict is unchanged.** The concern was well founded (on APTOS
the old `detect_fov_bbox` returned `None` on 5 of 6 sampled frames → the centre-square fallback cut
480×480 out of 640×480, full arm only), but re-running exp3 on the fixed code moved nothing:
**G_full 0.7617 → 0.7619**, APTOS wF1 0.60567 → 0.60584, AUC 0.7978 → 0.8000, while the baseline arm
reproduced bit-for-bit (0.7207529797486972 — eval determinism confirmed). So `h4_supported=false`
stands on its own and exp3's numbers can be trusted. Side finding worth citing: losing ~25% of the
frame periphery barely moves transfer metrics → the model leans on central/global frame statistics
rather than peripheral lesions (converges with the H-5 refutation, see [[results-knowledge-base]]).
Runner `experiments/outputs/run_exp3_postfix.sh` (setsid-detached, 42 min); pre-fix JSON kept as
`outputs/exp3/transferability_results_prefix_20260717.json`.

**Still to regenerate (not done):** the 512² Stage 0–4 cache. Exp 5/6/7 touch IDRiD (≤3% max) and
datasets at 0%, so impact there is small but non-zero (exp6 was already recomputed post-fix).

**Three FOV detectors still coexist** — `crop_resize.py` (fixed),
`od_fovea_net/geometry.py::detect_fov_bbox` (independent, already robust: median
corners, largest CC, no landscape restriction), and the offline illustration
helper `demo/web/public/pipeline/helpers/s2_crop_resize.py` (works around the
same bug with its own `detect_fov_bbox_square`). Only the first is on the live
train/inference path. Consolidating them is unfinished work.

Regression tests: `experiments/tests/test_crop_resize.py` (7 tests;
`test_full_frame_fundus_is_not_cropped` fails against the old code).
