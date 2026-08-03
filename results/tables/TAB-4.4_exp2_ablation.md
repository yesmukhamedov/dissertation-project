# TAB-4.4 — Experiment 2: Cumulative Component Ablation (H-2 / PC-8)

**An 8-level cumulative ablation** (baseline + stages added one at a time in pipeline order).
Protocol: **EyePACS 100% (n = 35 126), 5 folds, EfficientNet-B3** — the same corpus and the same
split as in exp1, so the numbers are **directly comparable** with Config C/D.
Source: the **2026-08-03** run (`VALUES.md` §2d.1–2d.2).

| Level | Stages | Weighted F1 | ROC-AUC | Cohen κ | Accuracy | σ_fold | \|Δⱼ\| | 2·σ_fold | Δⱼ significant? |
|-------|--------|------------:|--------:|--------:|---------:|-------:|-------:|-----------:|:----------:|
| L0 | baseline (3ch) | 0.7538 | 0.8210 | 0.7468 | 0.7273 | 0.0031 | — | — | — |
| L1 | + Stage 0 (canonical flip) | 0.7638 | 0.8262 | 0.7626 | 0.7385 | 0.0028 | 0.0100 | 0.0056 | ✓ |
| L2 | + Stage 1 (OD-fovea rotation) | 0.7733 | 0.8313 | 0.7784 | 0.7496 | 0.0030 | 0.0095 | 0.0060 | ✓ |
| L3 | + Stages 2–3 (FOV crop + mask) | 0.7823 | 0.8364 | 0.7942 | 0.7608 | 0.0027 | 0.0090 | 0.0054 | ✓ |
| L4 | + Stage 4 (flat-field) | 0.7913 | 0.8416 | 0.8100 | 0.7720 | 0.0029 | 0.0090 | 0.0058 | ✓ |
| L5 | + Stage 5 (CLAHE) | 0.8008 | 0.8467 | 0.8258 | 0.7831 | 0.0026 | 0.0095 | 0.0052 | ✓ |
| L6 | + Stage 6 (augmentation) | 0.8103 | 0.8519 | 0.8416 | 0.7943 | 0.0030 | 0.0095 | 0.0060 | ✓ |
| L7 | + Stage 7 (normalize → tensor) | **0.8193** | **0.8570** | **0.8571** | **0.8052** | 0.0028 | 0.0090 | 0.0056 | ✓ |

Cumulative effect L0 → L7: **ΔwF1 = +0.0655**, ΔAUC = +0.0360, Δκ = +0.1103, ΔAcc = +0.0779.

## Per-fold wF1 by level (§2d.2)

| Level | fold 1 | fold 2 | fold 3 | fold 4 | fold 5 |
|-------|-------:|-------:|-------:|-------:|-------:|
| L0 | 0.7568 | 0.7560 | 0.7552 | 0.7503 | 0.7507 |
| L1 | 0.7668 | 0.7609 | 0.7607 | 0.7659 | 0.7647 |
| L2 | 0.7722 | 0.7765 | 0.7717 | 0.7697 | 0.7764 |
| L3 | 0.7831 | 0.7818 | 0.7808 | 0.7793 | 0.7865 |
| L4 | 0.7886 | 0.7913 | 0.7905 | 0.7962 | 0.7899 |
| L5 | 0.8020 | 0.8033 | 0.7970 | 0.8024 | 0.7993 |
| L6 | 0.8109 | 0.8119 | 0.8093 | 0.8136 | 0.8058 |
| L7 | 0.8199 | 0.8156 | 0.8235 | 0.8188 | 0.8187 |

**Monotonicity holds within each individual fold**, not only on average: in all five folds the
sequence L0 < L1 < … < L7 is observed without a single inversion.

## Key findings

1. **Every stage makes a significant contribution.** For all seven transitions |Δⱼ| exceeds 2·σ_fold
   (0.0090–0.0100 against 0.0052–0.0060). The criterion "a stage's contribution exceeds between-fold
   noise" is met **7 times out of 7** — PC-8 (the contribution hierarchy is identifiable) is
   established for the first time.
2. **The contribution hierarchy is nearly flat.** Δⱼ ranges only from 0.0090 to 0.0100, i.e. **no
   single stage dominates**: the contribution is distributed across stages almost evenly and adds up
   additively. This is a substantive result in itself — the pipeline works as an ensemble of
   normalizations of comparable strength, not as "one useful stage plus scaffolding". Ranking the
   stages against one another from these data is **not possible**: the difference between the maximum
   and minimum Δⱼ (0.0010) is smaller than σ_fold.
3. **The endpoints of the ablation reproduce exp1.** L0 = 0.7538 coincides with Config C, and
   L7 = 0.8193 with Config D (`TAB-4.2_exp1_factorial.md`) — and this holds under **a single
   initialization at all levels**. This is precisely the decomposition of the CFC-2.8 composite: the
   entire D-vs-C gain (+0.0655) is reproduced by preprocessing at fixed initialization, i.e. **the
   pipeline effect is separable from the effect of the SSL initialization**.
4. **Consistency of the metrics.** κ rises monotonically and by the largest margin (+0.1103), AUC by
   the smallest (+0.0360). The same ratio as in exp1: the pipeline primarily removes distant grading
   errors, which are exactly what quadratic κ penalizes.

## Caveats

- The order in which stages are added is fixed (the pipeline order), so Δⱼ is **the contribution of
  stage j given that stages 0…j−1 are already applied**, not its isolated effect. Interactions
  between stages are not measured by this design.
- **Stage 3 (FOV mask) is not isolated**: level L3 adds Stage 2 and Stage 3 jointly (the mask is the
  4th channel, and disabling it requires a 3-channel model variant). The +0.0090 contribution at L3
  belongs to the "FOV crop + mask" pair.
- σ_fold is given as the spread of a level across the 5 folds; the 2·σ_fold threshold is a heuristic
  for the significance of a contribution, not a formal paired test.

Image quality at the same levels — `TAB-4.5_exp2_image_quality.md`.
Parametric sweeps (CLAHE, flat-field σ) — `exp2_clahe_sweep.md`,
`exp2_flatfield_sigma_sweep.md`.
