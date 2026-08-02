# FIG-4.10 / Flat-Field σ Sweep (H-2 / PC-2, part C)

A sweep of the adaptive flat-field parameter: σ as a fraction of the FOV diameter, range 0.05–0.10·D_FOV.
Evaluated on EyePACS (train folds) with CNR monitored in parallel.
Source: the **2026-08-02** run (`VALUES.md` §2b).

> **New in this run.** Before 2026-08-02 the σ sweep had not been run (Part C was absent from
> `exp2_ablation.py` — gap G-5), and the second half of PC-2 remained open. It is now closed.

## Grid (train folds)

| σ / D_FOV | Weighted F1 | CNR |
|-----------|------------:|----:|
| 0.05 | 0.7680 | 3.20 |
| 0.06 | 0.7870 | 3.50 |
| **0.07** | **0.8090** | **3.90** |
| 0.08 | 0.7950 | 3.60 |
| 0.09 | 0.7760 | 3.40 |
| 0.10 | 0.7570 | 3.10 |

**σ\* = 0.07 · D_FOV** · R = 0.0520 (the wF1 range across the sweep).

## Held-out confirmation

| Arm | wF1 |
|-----|----:|
| flat-field = off | 0.7510 |
| flat-field = σ\* | **0.8080** |

| Metric | Δ | 95% CI (Δ) |
|---------|--:|------------|
| wF1 | +0.0570 | [+0.0381, +0.0759] |

## Bottom line: H-2 / PC-2 (the flat-field part) — CONFIRMED

1. **An interior optimum exists.** The profile is strictly unimodal with a maximum at σ = 0.07 and a
   symmetric decline on both sides (0.7680 ← 0.8090 → 0.7570). The optimum is not at an edge, and the
   range across the sweep, R = 0.052, is comparable to the full pipeline effect (+0.0655) — i.e. the
   **sensitivity to σ is high** and the parameter requires tuning rather than an arbitrary choice.
2. **CNR and wF1 move together here.** The CNR maximum (3.90) falls exactly at σ\* = 0.07, and the
   ranking by CNR matches the ranking by wF1 at all six points. This differs from the picture across
   ablation levels (`TAB-4.5`), where there is no correspondence: **within a single stage**
   contrast-to-noise turns out to be a good proxy for quality, **across different stages** it is not.
3. **Held-out data confirm the choice:** +0.0570 wF1, CI excludes zero.
4. The value σ\* = 0.07 coincides with the parameter fixed in the pipeline specification
   (Stage 4, adaptive σ = 0.07·D) — the sweep confirms the already adopted setting rather than changing it.

## Caveats

- The grid is a single evaluation per point, with no std across folds; the step is 0.01·D, and no
  finer grid exists.
- The absolute CNR values in this table (3.1–3.9) are computed under a different normalization than
  the CNR in `TAB-4.5_exp2_image_quality.md` (20–29); **they must not be compared across tables**,
  though the ranking within each table is valid.
- The interaction of σ with the CLAHE parameters was not investigated: the one-dimensional (σ) and
  two-dimensional (clip × threshold) sweeps were performed independently, and no joint three-parameter
  grid was built.

The CLAHE sweep — `exp2_clahe_sweep.md`. The ablation — `TAB-4.4_exp2_ablation.md`.
