# TAB-4.5 — Experiment 2: Image-Quality Metrics per Ablation Level

Image-quality metrics across the eight levels of the cumulative ablation, sample n = 100 images.
SSIM is computed against the original (unprocessed) frame. Source: the **2026-08-02** run
(`VALUES.md` §2d.3); wF1 comes from `TAB-4.4_exp2_ablation.md`.

| Level | Stages | mean CNR | mean Entropy (bits) | mean SSIM | wF1 (TAB-4.4) |
|-------|--------|---------:|-------------------:|----------:|--------------:|
| L0 | baseline | 20.43 | 5.502 | 1.000 | 0.7538 |
| L1 | + Stage 0 | 20.43 | 5.502 | 0.998 | 0.7638 |
| L2 | + Stage 1 | 20.41 | 5.508 | 0.981 | 0.7733 |
| L3 | + Stages 2–3 | 20.38 | 5.514 | 0.964 | 0.7823 |
| L4 | + Stage 4 (flat-field) | **28.60** | 5.596 | 0.912 | 0.7913 |
| L5 | + Stage 5 (CLAHE) | 24.15 | 5.884 | 0.878 | 0.8008 |
| L6 | + Stage 6 (augmentation) | 24.15 | 5.884 | 0.871 | 0.8103 |
| L7 | + Stage 7 (normalize) | 24.02 | **5.901** | **0.865** | **0.8193** |

## Observations

- **The geometric stages (0–3) do not change intensities.** CNR 20.43 → 20.38 and Entropy
  5.502 → 5.514 — within rounding; only SSIM falls (1.000 → 0.964), which reflects the geometric
  transformation of the frame (flip, rotation, crop) rather than any change in photometry.
  Meanwhile wF1 at these levels rises by +2.85 pp — **the gain comes from geometric canonicalization,
  which the image-quality metrics do not see at all**.
- **Flat-field is the only stage that noticeably raises CNR** (20.38 → 28.60, +40%): equalizing
  illumination directly improves contrast-to-noise.
- **CLAHE lowers CNR (28.60 → 24.15) but produces the largest jump in entropy** (5.596 → 5.884):
  local histogram equalization raises detail at the cost of part of the global "lesion against
  background" contrast on which CNR is built.
- **Augmentation (Stage 6) changes none of the three metrics** (CNR/Entropy are identical to L5) —
  as expected: Stage 6 is active only at train time, while quality is measured on the validation
  configuration of the pipeline. Nonetheless wF1 at this level rises by +0.0095. Another case where a
  classification gain has no reflection in the IQ metrics.
- **SSIM falls monotonically** (1.000 → 0.865) — the pipeline moves progressively further from the
  original image, and this is accompanied by a monotone rise in wF1.

## Key conclusion: the IQ ↔ classification link is partial, not direct

The full pipeline improves both image quality (CNR +18% over baseline, Entropy +0.40 bits) and
classification (+6.55 pp wF1) at the same time. But **there is no level-by-level correspondence**:

- the CNR maximum falls at L4, whereas wF1 keeps rising through L7;
- L1–L3 deliver +2.85 pp wF1 with CNR/Entropy unchanged;
- L6 delivers +0.95 pp with the IQ metrics completely unchanged.

The correct formulation for §4.3.3/§5.4: **image-quality metrics capture part of the pipeline's
mechanism (photometric normalization) but do not exhaust it** — geometric canonicalization and
stochastic augmentation contribute in ways invisible to CNR/Entropy/SSIM. The thesis "better for the
eye ≠ better for the CNN" remains true in its weak form: IQ metrics are not a sufficient predictor of
the classification gain.

## Gaps

1. **VVI is not implemented** in `src/utils/image_quality.py` (the `VVI` value in the demo `data.js`
   has no source in the code and is not used).
2. The metrics were measured on the validation configuration of the pipeline → the contribution of
   Stage 6 is invisible to them in principle.
3. n = 100 images, no std.
