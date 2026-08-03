# Conclusions — Experiment 2 (ablation + CLAHE/σ sweeps, H-2) → §4.3

**What was done.** (A) A **cumulative ablation** — 8 levels (baseline + stages added one at a time in
pipeline order) on **EyePACS 100% (n = 35 126), 5 folds, EfficientNet-B3**.
(B) A **two-dimensional CLAHE sweep** — a 7 × 5 grid (clip_factor × global_threshold) on EyePACS,
with separate per-class F1 grids for DR1 and DR2. (C) A **flat-field σ sweep** — 6 values over
0.05–0.10·D_FOV. Source: the **2026-08-03** run.

> The protocol changed fundamentally relative to the previous run (which used a 15% subsample,
> 3 folds, a 6-level individual ablation, a sweep over clip_factor alone on IDRiD, and no σ sweep).
> The numbers are **not comparable** with the previous version; they are now directly comparable with exp1.

## What was found

**1. Every stage of the pipeline makes a significant positive contribution.** wF1 rises monotonically
from L0 = 0.7538 to L7 = 0.8193 (+0.0655), and for all seven transitions |Δⱼ| exceeds 2·σ_fold
(0.0065–0.0143 against 0.0042–0.0060). **Monotonicity holds within each individual fold** — in all
five, the sequence L0 < L1 < … < L7 is observed without a single inversion. PC-8 is established in
the part "the stage contributions are identifiable".

**2. And the hierarchy is resolvable — the photometric stages lead it.** ⚠️ **This reverses the
previous revision**, which had Δⱼ = 0.0090–0.0100 (spread 0.0010 < σ_fold) and reported the hierarchy
as flat and the stages as unrankable. Here the spread is **0.0078 ≈ 3·σ_fold**:

| Rank | Stage | Δⱼ | share of +0.0655 |
|---|---|---:|---:|
| 1 | Stage 4 — flat-field | **0.0143** | 22% |
| 2 | Stage 5 — CLAHE | **0.0125** | 19% |
| 3 | Stage 6 — augmentation | 0.0101 | 15% |
| 4 | Stages 2–3 — FOV crop + mask | 0.0082 | 13% |
| 5 | Stage 0 — canonical flip | 0.0071 | 11% |
| 6 | Stage 1 — OD-fovea rotation | 0.0068 | 10% |
| 7 | Stage 7 — normalize → tensor | 0.0065 | 10% |

The **photometric pair (flat-field + CLAHE) carries 41% of the gain** — as much as the four
geometric/normalization stages combined. This is consistent with PC-2 (both photometric parameters
have sharp interior optima) and with H-3 (domain distance falls mainly through illumination and
contrast). No stage is redundant: the weakest still clears its own 2·σ_fold threshold. What the data
support is the **grouping** — photometric clearly above the rest — not a strict 1-to-7 order:
adjacent ranks (0.0068 vs 0.0065) sit within noise.

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
wF1 0.7538 → 0.8137 (Δ +0.0599, CI [+0.0388, +0.0770]), F1(DR1) 0.0976 → 0.2091,
F1(DR2) 0.5316 → 0.6477.

**5. Flat-field σ: a strictly unimodal profile with high sensitivity.** The maximum is at σ\* = 0.07·D
(interior), with a symmetric decline on both sides, and the range across the sweep, R = 0.0512, is
comparable to the full pipeline effect — i.e. the parameter requires tuning rather than an arbitrary
choice. Held-out: 0.7513 → 0.8087 (Δ +0.0574, CI [+0.0428, +0.0806]). σ\* coincides with the value in
the Stage 4 specification — the sweep confirms the adopted setting.

**6. "Image quality ≠ classification quality" — the thesis holds, in a sharpened form.**
The full pipeline improves both IQ (CNR 20.43 → 24.02, Entropy 5.502 → 5.901) and classification, and
the two now line up better than before: **the only two levels that move the IQ metrics are the two
top-ranked contributors** — L4 (flat-field) jumps CNR 20.38 → 28.60 and ranks 1st (Δⱼ = 0.0143);
L5 (CLAHE) jumps Entropy 5.596 → 5.884 and ranks 2nd (0.0125). Where the IQ metrics see something,
they see the largest effects. They remain **insufficient** all the same: the geometric levels L1–L3
deliver +2.21 pp wF1 with CNR/Entropy **unchanged**, and L6 (augmentation) delivers +1.01 pp with all
three metrics unchanged — 49% of the total gain, invisible to IQ; and the CNR maximum still sits at
L4 while wF1 keeps rising through L7. **Within a single stage** (the σ sweep) CNR and wF1 move
together perfectly — both peak at σ = 0.07. The correct formulation: the IQ metrics track the
photometric part of the mechanism — the largest single part — but do not exhaust it, and they are
insufficient as a predictor of the classification gain.

## The main substantive conclusion (for §4.3 and §5.4)

The ablation on the full corpus at fixed initialization shows that **preprocessing on its own
delivers the entire gain observed in exp1** (+6.55 pp wF1), spread across all eight stages with
**illumination and contrast normalization contributing the largest share (41%)**. Together with the
sweeps (two interior optima confirmed on held-out data, both on those same photometric parameters)
this means: the pipeline is not a set of just-in-case heuristics but a parameterized model component,
each part of which measurably contributes to the result and requires tuning — and its dominant part
is exactly the part that is parameterized and tuned. This is direct empirical support for the central
thesis *model = preprocessing + CNN*.

## Caveats (mandatory in the text)

- The order in which stages are added is fixed (the pipeline order) → Δⱼ is the contribution of a
  stage **given that the preceding ones are already applied**; interactions between stages are not
  measured by this design.
- **Stage 3 (FOV mask) is not isolated**: level L3 adds Stage 2 and Stage 3 jointly (disabling the
  mask requires a 3-channel model variant). This is the remainder of gap G-8, and it now carries more
  weight: rank 4 in the hierarchy belongs to the *pair*, not to either stage separately.
- **The ranking rests on the 2·σ_fold heuristic**, not on a formal paired test. Adjacent ranks are
  within noise; report the grouping (photometric ≫ the rest), not the full permutation.
- The sweep grids were obtained on train folds, one evaluation per point, without std.
- The held-out F1(DR1) at θ\* (0.2091) is substantially below the grid value (0.4693); the
  discrepancy is not explained by the available data — **use the held-out value in the text**.
- The CLAHE and σ sweeps were run independently; no joint three-parameter grid was built.
- The absolute CNR values in `TAB-4.5` (20–29) and in the σ sweep (3.10–3.93) are computed under
  different normalizations — do not compare them across tables.

Tables: `tables/TAB-4.4_exp2_ablation.md`, `TAB-4.5_exp2_image_quality.md`,
`exp2_clahe_sweep.md`, `exp2_flatfield_sigma_sweep.md`. Card: `hypotheses/H-2.md`.
