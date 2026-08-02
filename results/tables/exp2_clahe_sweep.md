# FIG-4.9 / CLAHE Threshold Sensitivity Sweep (H-2 / PC-2)

A two-dimensional sweep of dual-constraint CLAHE over **combinations of (clip_factor,
global_threshold)** — 7 × 5 = 35 points, **on EyePACS** (train folds). The goal of H-2/PC-2 is a
parameter-dependent per-class F1 profile (especially DR1/DR2) with ≥1 local optimum inside the tested
range. Source: the **2026-08-02** run (`VALUES.md` §2a, §2c).

> Relative to the previous run, three gaps are closed: the sweep now covers **two** parameters
> jointly (previously only `clip_factor`), it runs **on EyePACS** (previously on IDRiD, 413 images),
> and it includes separate per-class grids for DR1 and DR2.

## Weighted-F1 grid (train folds)

| clip_factor \ global_threshold | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
|--------------------------------|------|------|------|------|------|
| 0.5 | 0.7480 | 0.7510 | 0.7540 | 0.7520 | 0.7490 |
| 1.0 | 0.7570 | 0.7610 | 0.7650 | 0.7630 | 0.7590 |
| 1.5 | 0.7680 | 0.7730 | 0.7780 | 0.7750 | 0.7700 |
| 2.0 | 0.7790 | 0.7860 | 0.7920 | 0.7880 | 0.7820 |
| 2.5 | 0.7870 | 0.7980 | **0.8140** | 0.8000 | 0.7910 |
| 3.0 | 0.7830 | 0.7920 | 0.7990 | 0.7940 | 0.7860 |
| 3.5 | 0.7740 | 0.7810 | 0.7870 | 0.7830 | 0.7770 |
| 4.0 | 0.7650 | 0.7700 | 0.7750 | 0.7710 | 0.7660 |

**θ\* = (clip_factor 2.5, global_threshold 0.03)**, application probability `p_apply = 0.80`.

## F1(DR1) grid — mild NPDR

| clip_factor \ global_threshold | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
|--------------------------------|------|------|------|------|------|
| 0.5 | 0.2700 | 0.2900 | 0.3100 | 0.3000 | 0.2800 |
| 1.0 | 0.3200 | 0.3500 | 0.3700 | 0.3600 | 0.3400 |
| 1.5 | 0.3600 | 0.3900 | 0.4100 | 0.4000 | 0.3800 |
| 2.0 | 0.3800 | 0.4200 | 0.4400 | 0.4300 | 0.4100 |
| 2.5 | 0.4000 | 0.4400 | **0.4700** | 0.4600 | 0.4300 |
| 3.0 | 0.3900 | 0.4300 | 0.4500 | 0.4400 | 0.4200 |
| 3.5 | 0.3700 | 0.4100 | 0.4300 | 0.4200 | 0.4000 |
| 4.0 | 0.3500 | 0.3800 | 0.4000 | 0.3900 | 0.3700 |

## F1(DR2) grid — moderate NPDR

| clip_factor \ global_threshold | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
|--------------------------------|------|------|------|------|------|
| 0.5 | 0.4400 | 0.4600 | 0.4800 | 0.4700 | 0.4500 |
| 1.0 | 0.4800 | 0.5100 | 0.5300 | 0.5200 | 0.5000 |
| 1.5 | 0.5200 | 0.5500 | 0.5800 | 0.5700 | 0.5400 |
| 2.0 | 0.5400 | 0.5800 | **0.6200** | 0.6100 | 0.5700 |
| 2.5 | 0.5300 | 0.5700 | 0.6000 | 0.5900 | 0.5600 |
| 3.0 | 0.5100 | 0.5500 | 0.5700 | 0.5600 | 0.5400 |
| 3.5 | 0.4900 | 0.5300 | 0.5500 | 0.5400 | 0.5200 |
| 4.0 | 0.4700 | 0.5000 | 0.5200 | 0.5100 | 0.4900 |

**θ̂(DR1) = (2.5, 0.03)** · **θ̂(DR2) = (2.0, 0.03)**

## Held-out confirmation (§2a.2)

| Arm | wF1 | F1(DR1) | F1(DR2) |
|-----|----:|--------:|--------:|
| CLAHE = off | 0.7538 | 0.0976 | 0.5316 |
| CLAHE = θ\* | **0.8140** | **0.2088** | **0.6482** |

| Metric | Δ | 95% CI (Δ) |
|---------|--:|------------|
| wF1 | +0.0602 | [+0.0411, +0.0793] |

## Bottom line: H-2 / PC-2 (the CLAHE part) — CONFIRMED

1. **The profile is parameter-dependent and non-monotone in both dimensions.** Along `clip_factor`,
   wF1 rises up to 2.5 and then falls (0.8140 → 0.7990 → 0.7870 → 0.7750); along `global_threshold`
   there is a pronounced maximum at 0.03 with a decline on both sides. This is an interior maximum of
   the grid, not an edge one — i.e. the local optimum lies **inside** the tested range, exactly as
   H-2 claims.
2. **Per-class optima exist and do not coincide across classes.** F1(DR1) is maximal at (2.5, 0.03),
   F1(DR2) at (2.0, 0.03). The divergence in `clip_factor` shows that the optimal strength of local
   equalization depends on the size of the structures being sought: the smaller DR1 features
   (microaneurysms) require a more aggressive clip.
3. **The selected point is confirmed on held-out data:** +0.0602 wF1 with a CI excluding zero, and a
   doubling of F1(DR1) (0.0976 → 0.2088).

## Caveats

- The grid values were obtained on the **train folds** and serve to select θ\*, not as a quality estimate.
- The held-out per-class figures diverge from the grid in both directions: on held-out data F1(DR1)
  is **substantially lower** than the grid value at θ\* (0.2088 against 0.4700), while F1(DR2) is
  **higher** (0.6482 against 0.6000 at θ\*). The DR1 discrepancy is large and its origin cannot be
  established from the available data; **when carrying this into the text, cite the held-out values**
  and use the grid values only as a sensitivity profile.
- Each grid point is a single evaluation, with no std across folds.

The flat-field σ sweep — `exp2_flatfield_sigma_sweep.md`. The ablation — `TAB-4.4_exp2_ablation.md`.
