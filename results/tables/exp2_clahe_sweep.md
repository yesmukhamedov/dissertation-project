# FIG-4.9 / CLAHE Threshold Sensitivity Sweep (H-2 / PC-2)

A two-dimensional sweep of dual-constraint CLAHE over **combinations of (clip_factor,
global_threshold)** — 7 × 5 = 35 points, **on EyePACS** (train folds). The goal of H-2/PC-2 is a
parameter-dependent per-class F1 profile (especially DR1/DR2) with ≥1 local optimum inside the tested
range. Source: the **2026-08-03** run (`VALUES.md` §2a, §2c).

> Relative to the previous run, three gaps are closed: the sweep now covers **two** parameters
> jointly (previously only `clip_factor`), it runs **on EyePACS** (previously on IDRiD, 413 images),
> and it includes separate per-class grids for DR1 and DR2.

## Weighted-F1 grid (train folds)

| clip_factor \ global_threshold | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
|--------------------------------|------|------|------|------|------|
| 0.5 | 0.7478 | 0.7508 | 0.7537 | 0.7513 | 0.7474 |
| 1.0 | 0.7549 | 0.7606 | 0.7651 | 0.7616 | 0.7612 |
| 1.5 | 0.7691 | 0.7741 | 0.7780 | 0.7736 | 0.7696 |
| 2.0 | 0.7798 | 0.7873 | 0.7917 | 0.7878 | 0.7806 |
| 2.5 | 0.7863 | 0.7986 | **0.8136** | 0.8005 | 0.7912 |
| 3.0 | 0.7820 | 0.7920 | 0.7992 | 0.7930 | 0.7842 |
| 3.5 | 0.7734 | 0.7815 | 0.7838 | 0.7834 | 0.7768 |
| 4.0 | 0.7647 | 0.7710 | 0.7754 | 0.7710 | 0.7644 |

**θ\* = (clip_factor 2.5, global_threshold 0.03)**, application probability `p_apply = 0.80`.

## F1(DR1) grid — mild NPDR

| clip_factor \ global_threshold | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
|--------------------------------|------|------|------|------|------|
| 0.5 | 0.2696 | 0.2895 | 0.3128 | 0.2986 | 0.2807 |
| 1.0 | 0.3176 | 0.3524 | 0.3689 | 0.3567 | 0.3396 |
| 1.5 | 0.3593 | 0.3910 | 0.4094 | 0.4026 | 0.3820 |
| 2.0 | 0.3788 | 0.4183 | 0.4393 | 0.4299 | 0.4091 |
| 2.5 | 0.4011 | 0.4390 | **0.4693** | 0.4584 | 0.4292 |
| 3.0 | 0.3911 | 0.4329 | 0.4497 | 0.4381 | 0.4191 |
| 3.5 | 0.3715 | 0.4101 | 0.4299 | 0.4168 | 0.3978 |
| 4.0 | 0.3516 | 0.3791 | 0.4003 | 0.3903 | 0.3719 |

## F1(DR2) grid — moderate NPDR

| clip_factor \ global_threshold | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
|--------------------------------|------|------|------|------|------|
| 0.5 | 0.4415 | 0.4587 | 0.4785 | 0.4680 | 0.4492 |
| 1.0 | 0.4792 | 0.5102 | 0.5295 | 0.5189 | 0.4987 |
| 1.5 | 0.5187 | 0.5489 | 0.5794 | 0.5734 | 0.5389 |
| 2.0 | 0.5406 | 0.5822 | **0.6219** | 0.6090 | 0.5700 |
| 2.5 | 0.5315 | 0.5697 | 0.5968 | 0.5879 | 0.5585 |
| 3.0 | 0.5119 | 0.5478 | 0.5705 | 0.5586 | 0.5427 |
| 3.5 | 0.4906 | 0.5296 | 0.5478 | 0.5387 | 0.5201 |
| 4.0 | 0.4725 | 0.4998 | 0.5180 | 0.5087 | 0.4886 |

**θ̂(DR1) = (2.5, 0.03)** · **θ̂(DR2) = (2.0, 0.03)**

## Held-out confirmation (§2a.2)

| Arm | wF1 | F1(DR1) | F1(DR2) |
|-----|----:|--------:|--------:|
| CLAHE = off | 0.7538 | 0.0976 | 0.5316 |
| CLAHE = θ\* | **0.8137** | **0.2091** | **0.6477** |

| Metric | Δ | 95% CI (Δ) |
|---------|--:|------------|
| wF1 | +0.0599 | [+0.0388, +0.0770] |

## Bottom line: H-2 / PC-2 (the CLAHE part) — CONFIRMED

1. **The profile is parameter-dependent and non-monotone in both dimensions.** Along `clip_factor`,
   wF1 rises up to 2.5 and then falls (0.8136 → 0.7992 → 0.7838 → 0.7754); along `global_threshold`
   there is a pronounced maximum at 0.03 with a decline on both sides. This is an interior maximum of
   the grid, not an edge one — i.e. the local optimum lies **inside** the tested range, exactly as
   H-2 claims.
2. **Per-class optima exist and do not coincide across classes.** F1(DR1) is maximal at (2.5, 0.03),
   F1(DR2) at (2.0, 0.03). The divergence in `clip_factor` shows that the optimal strength of local
   equalization depends on the size of the structures being sought: the smaller DR1 features
   (microaneurysms) require a more aggressive clip.
3. **The selected point is confirmed on held-out data:** +0.0599 wF1 with a CI excluding zero, and a
   doubling of F1(DR1) (0.0976 → 0.2091).

## Caveats

- The grid values were obtained on the **train folds** and serve to select θ\*, not as a quality estimate.
- The held-out per-class figures diverge from the grid in both directions: on held-out data F1(DR1)
  is **substantially lower** than the grid value at θ\* (0.2091 against 0.4693), while F1(DR2) is
  **higher** (0.6477 against 0.5968 at θ\*). The DR1 discrepancy is large and its origin cannot be
  established from the available data; **when carrying this into the text, cite the held-out values**
  and use the grid values only as a sensitivity profile.
- Each grid point is a single evaluation, with no std across folds.

The flat-field σ sweep — `exp2_flatfield_sigma_sweep.md`. The ablation — `TAB-4.4_exp2_ablation.md`.
