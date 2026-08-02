# Conclusions — Experiment 2 (ablation + CLAHE/σ sweeps, H-2) → §4.3

**What was done.** (A) A **cumulative ablation** — 8 levels (baseline + stages added one at a time in
pipeline order) on **EyePACS 100% (n = 35 126), 5 folds, EfficientNet-B3**.
(B) A **two-dimensional CLAHE sweep** — a 7 × 5 grid (clip_factor × global_threshold) on EyePACS,
with separate per-class F1 grids for DR1 and DR2. (C) A **flat-field σ sweep** — 6 values over
0.05–0.10·D_FOV. Source: the **2026-08-02** run.

> The protocol changed fundamentally relative to the previous run (which used a 15% subsample,
> 3 folds, a 6-level individual ablation, a sweep over clip_factor alone on IDRiD, and no σ sweep).
> The numbers are **not comparable** with the previous version; they are now directly comparable with exp1.

## What was found

**1. Every stage of the pipeline makes a significant positive contribution.** wF1 rises monotonically
from L0 = 0.7538 to L7 = 0.8193 (+0.0655), and for all seven transitions |Δⱼ| exceeds 2·σ_fold
(0.0090–0.0100 against 0.0052–0.0060). **Monotonicity holds within each individual fold** — in all
five, the sequence L0 < L1 < … < L7 is observed without a single inversion. PC-8 is established in
the part "the stage contributions are identifiable".

**2. But the contribution hierarchy is flat — the stages cannot be ranked.** The spread of Δⱼ is
0.0010, which is smaller than σ_fold (≈0.0028). No stage dominates; the contribution is distributed
almost evenly and adds up additively. This is a substantive result in itself: the pipeline works as
an **ensemble of normalizations of comparable strength**, not as "one useful stage plus scaffolding".
For the thesis this is stronger than an ordinary hierarchy — any stage may be removed, and each one
costs roughly 1 pp of wF1. Formulations of the form "the leading stage is …" are **incorrect**.

**3. The main consequence: the CFC-2.8 confound has been decomposed.** The endpoints of the ablation
reproduce exp1 exactly — L0 = 0.7538 = Config C, L7 = 0.8193 = Config D — under **a single
initialization at all eight levels**. Hence the entire D-vs-C gain (+0.0655) belongs to preprocessing,
not to the SSL initialization. The former conclusion that "preprocessing on its own does not improve
classification; the exp1 effect is an indivisible composite" is **refuted** by this run. This is the
most important change in exp2.

**4. CLAHE: an interior optimum in both parameters, with differing per-class optima.** The profile is
non-monotone in both dimensions, with an interior maximum: θ\* = (clip_factor 2.5, global_threshold
0.03), p_apply = 0.80. F1(DR1) is maximal at (2.5, 0.03), F1(DR2) at (2.0, 0.03): the finer DR1
features (microaneurysms) require more aggressive local equalization. Held-out data confirm this:
wF1 0.7538 → 0.8140 (Δ +0.0602, CI [+0.0411, +0.0793]), F1(DR1) 0.0976 → 0.2088,
F1(DR2) 0.5316 → 0.6482.

**5. Flat-field σ: a strictly unimodal profile with high sensitivity.** The maximum is at σ\* = 0.07·D
(interior), with a symmetric decline on both sides, and the range across the sweep, R = 0.0520, is
comparable to the full pipeline effect — i.e. the parameter requires tuning rather than an arbitrary
choice. Held-out: 0.7510 → 0.8080 (Δ +0.0570, CI [+0.0381, +0.0759]). σ\* coincides with the value in
the Stage 4 specification — the sweep confirms the adopted setting.

**6. "Image quality ≠ classification quality" — the thesis holds, but in its weak form.**
The full pipeline improves both IQ (CNR 20.43 → 24.02, Entropy 5.502 → 5.901) and classification. But
there is no **level-by-level** correspondence: the CNR maximum falls at L4 (flat-field, 28.60),
whereas wF1 keeps rising through L7; the geometric levels L1–L3 deliver +2.85 pp wF1 with CNR/Entropy
**unchanged**; level L6 (augmentation) delivers +0.95 pp with the IQ metrics completely unchanged.
**Within a single stage**, however (the σ sweep), CNR and wF1 move together perfectly — both peak at
σ = 0.07. The correct formulation: the IQ metrics capture the photometric part of the mechanism but
do not exhaust it, and they are insufficient as a predictor of the classification gain.

## The main substantive conclusion (for §4.3 and §5.4)

The ablation on the full corpus at fixed initialization shows that **preprocessing on its own
delivers the entire gain observed in exp1** (+6.55 pp wF1), distributed evenly across the eight
stages. Together with the sweeps (two interior optima confirmed on held-out data) this means: the
pipeline is not a set of just-in-case heuristics but a parameterized model component, each part of
which measurably contributes to the result and requires tuning. This is direct empirical support for
the central thesis *model = preprocessing + CNN*.

## Caveats (mandatory in the text)

- The order in which stages are added is fixed (the pipeline order) → Δⱼ is the contribution of a
  stage **given that the preceding ones are already applied**; interactions between stages are not
  measured by this design.
- **Stage 3 (FOV mask) is not isolated**: level L3 adds Stage 2 and Stage 3 jointly (disabling the
  mask requires a 3-channel model variant). This is the remainder of gap G-8.
- The sweep grids were obtained on train folds, one evaluation per point, without std.
- The held-out F1(DR1) at θ\* (0.2088) is substantially below the grid value (0.4700); the
  discrepancy is not explained by the available data — **use the held-out value in the text**.
- The CLAHE and σ sweeps were run independently; no joint three-parameter grid was built.
- The absolute CNR values in `TAB-4.5` (20–29) and in the σ sweep (3.1–3.9) are computed under
  different normalizations — do not compare them across tables.

Tables: `tables/TAB-4.4_exp2_ablation.md`, `TAB-4.5_exp2_image_quality.md`,
`exp2_clahe_sweep.md`, `exp2_flatfield_sigma_sweep.md`. Card: `hypotheses/H-2.md`.
