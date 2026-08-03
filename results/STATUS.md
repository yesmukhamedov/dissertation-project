# STATUS — experiment status + metrics

Source of numbers: the **2026-08-03** run (`VALUES.md`). Metric priority (descending):
**1) Weighted F1 · 2) ROC-AUC (macro OvR) · 3) Cohen κ (quadratic) · 4) Accuracy**.

> ⚠️ **Provenance.** The numbers in this revision were taken from `VALUES.md`. The raw artifacts of
> the 2026-08-03 run (`summary.json`, `*_results.json`, `metrics.csv`, `predictions.npz`) were
> **absent from `experiments/outputs/`** at the time of the update — the latest files there are dated
> 2026-07-30, and `results/data/*.json` contain numbers from the **previous** run. The source of
> truth must be synchronized before anything is carried into the chapters. See `data/MANIFEST.md`.

## Summary table

| Exp | Hypothesis | Dataset | Status | Verdict |
|-----|----------|---------|--------|---------|
| exp1 | H-1 | EyePACS 100% (n = 35 126), 5-fold | ✅ COMPLETE | `h1_supported=true` — EH-3 met on both backbones |
| exp2 | H-2 | EyePACS 100%, 5-fold | ✅ COMPLETE | PC-2 ✓ (both sweeps); PC-8 — contributions significant, hierarchy flat |
| — | H-3 | 6 external domains | ✅ COMPLETE | `h3_supported=true` — MMD/KL shrink on all 6 |
| exp3 | H-4 | EyePACS → APTOS (n = 3 662) | ✅ COMPLETE | `h4_supported=true` — G_D 0.8976 ≥ 0.85 |
| exp4 | H-5 | EyePACS → IDRiD (54 masks) | ✅ COMPLETE | `h5_alo_supported=true` — 4/4 lesion types significant |
| exp5 | H-7 | EyePACS → IDRiD + Messidor-2 | ✅ COMPLETE | ✗ **not supported as written (0 of 2)**; absolute performance significantly higher on both |
| exp6 | H-6 | EyePACS → 5 camera groups | ✅ COMPLETE | `h6_supported=true` — 5/5 groups; std wF1 −2.4× |
| exp7 | E-7 | IDRiD → Clinical, 5-fold | ✅ COMPLETE | **positive** (+0.080 wF1), preregistered |
| SSL | A1 | EyePACS (unlabeled) | ✅ COMPLETE | SIP ✓; continual-SSL ✓ on both backbones |

Configuration legend: **A** = baseline(3ch)+ResNet-50 · **B** = pipeline(4ch)+ResNet-50 ·
**C** = baseline(3ch)+EffNet-B3 · **D** = pipeline(4ch)+EffNet-B3.

---

## exp1 — 2×2 factorial (H-1) — COMPLETE, CONFIRMED

| Config | Weighted F1 | ROC-AUC | κ (quadratic) | Accuracy | macro-F1 |
|--------|-------------|---------|---------------|----------|----------|
| A (baseline, ResNet-50) | 0.7518 ± 0.0110 | 0.8300 ± 0.0140 | 0.7410 ± 0.0350 | 0.7247 ± 0.0180 | 0.4281 |
| B (pipeline, ResNet-50) | **0.8172 ± 0.0090** | **0.8620 ± 0.0110** | **0.8539 ± 0.0260** | **0.8027 ± 0.0150** | **0.5322** |
| C (baseline, EffNet-B3) | 0.7538 ± 0.0120 | 0.8210 ± 0.0150 | 0.7468 ± 0.0330 | 0.7273 ± 0.0190 | 0.4300 |
| D (pipeline, EffNet-B3) | **0.8193 ± 0.0100** | **0.8570 ± 0.0120** | **0.8571 ± 0.0270** | **0.8052 ± 0.0160** | **0.5355** |

**Dominance criterion EH-3** (all three mandatory): ΔF1 ≥ 5 pp · ΔAUC ≥ 0.02 · no degradation in κ.

| Comparison | ΔF1 | ΔAUC | Δκ | F1≥5pp? | AUC≥0.02? | κ? | Dominates? |
|-----------|-----|------|-----|---------|-----------|-----|-------------|
| B vs A (ResNet-50) | **+6.54 pp** | +0.0320 | +0.1129 | ✓ | ✓ | ✓ | **YES** |
| D vs C (EffNet-B3) | **+6.55 pp** | +0.0360 | +0.1103 | ✓ | ✓ | ✓ | **YES** |

Significance: DeLong p = 0.0041 / 0.0028; McNemar p = 0.0057 / 0.0041; Holm (4 configs)
0.0082 / 0.0056. Mixed-effects ANOVA: the "arm × backbone" interaction p = 0.31 → the effect is the
same on both architectures. The cross-validation CIs of baseline and pipeline **do not overlap on
any** of the four primary metrics.

In addition: calibration **improves** (ECE 0.0712 → 0.0418; 0.0691 → 0.0402);
referable Sens +11.2 pp with rising Spec; loss gap 0.052 → 0.021 (regularizing effect);
F1(DR1) doubles (0.0999 → 0.2141).

**Bottom line:** `h1_supported=true`. Details: `tables/TAB-4.2_exp1_factorial.md`, `TAB-4.3_exp1_calibration.md`,
`exp1_per_class.md`, `exp1_clinical_indomain.md`, `exp1_convergence_ci.md`, `TAB-5.1_statistical.md`.

---

## exp2 — cumulative ablation + sweeps (H-2) — COMPLETE

Protocol: **EyePACS 100% (n = 35 126), 5 folds, EfficientNet-B3**, a single initialization at all
levels. The sweeps were run on EyePACS.

**Cumulative ablation, 8 levels:**

| Level | Stages | wF1 | ΔwF1 | 2·σ_fold | significant? |
|---------|--------|-----|------|----------|---------|
| L0 | baseline | 0.7538 | — | — | — |
| L1 | + Stage 0 | 0.7609 | +0.0071 | 0.0048 | ✓ |
| L2 | + Stage 1 | 0.7677 | +0.0068 | 0.0042 | ✓ |
| L3 | + Stages 2–3 | 0.7759 | +0.0082 | 0.0048 | ✓ |
| L4 | + Stage 4 | 0.7902 | **+0.0143** | 0.0060 | ✓ |
| L5 | + Stage 5 | 0.8027 | **+0.0125** | 0.0056 | ✓ |
| L6 | + Stage 6 | 0.8128 | +0.0101 | 0.0054 | ✓ |
| L7 | + Stage 7 | **0.8193** | +0.0065 | 0.0042 | ✓ |

Cumulatively L0 → L7: **+0.0655 wF1**. Monotonicity holds **in each of the 5 folds**.

**Sweeps:** CLAHE — a two-dimensional 7×5 grid (clip × threshold), interior optimum θ\* = (2.5, 0.03),
held-out +0.0599 (CI [+0.0388, +0.0770]); flat-field σ — unimodal maximum at σ\* = 0.07·D,
R = 0.0512, held-out +0.0574 (CI [+0.0428, +0.0806]). The per-class optima differ:
θ̂(DR1) = (2.5, 0.03), θ̂(DR2) = (2.0, 0.03).

**Bottom line:** PC-2 fully confirmed (both parts of the sweeps, both optima interior + held-out).
PC-8 — all 7 contributions are significant **and the hierarchy is resolvable** (spread of
Δⱼ = 0.0078 ≈ 3·σ_fold): **flat-field (0.0143) and CLAHE (0.0125) lead**, together 41% of the total
gain; then augmentation (0.0101), FOV crop+mask (0.0082), flip (0.0071), rotation (0.0068),
normalize (0.0065). ⚠️ **This reverses the previous revision**, which reported the hierarchy as flat
and the stages as unrankable. The data resolve the *grouping* (photometric ≫ the rest), not a strict
1-to-7 order — adjacent ranks are within noise.

**Key consequence — decomposition of CFC-2.8:** L0 = 0.7538 = Config C, L7 = 0.8193 = Config D under
a single initialization → the entire exp1 gain is reproduced by preprocessing alone, separately from
the SSL init.

**Caveats:** the stage order is fixed (each stage's contribution is measured with the preceding ones
already applied); **Stage 3 is not isolated** (L3 = Stage 2 + 3 jointly); the sweep grids use train
folds, one evaluation per point. Details: `tables/TAB-4.4_exp2_ablation.md`, `TAB-4.5_exp2_image_quality.md`,
`exp2_clahe_sweep.md`, `exp2_flatfield_sigma_sweep.md`.

---

## H-3 — domain distance (MMD / KL) — COMPLETE, CONFIRMED

| Domain | MMD: BASE → INT | Δd | 95% CI (Δd) | KL: BASE → INT |
|---|---|---:|---|---|
| APTOS | 0.1910 → 0.1178 | +0.0732 | [+0.0380, +0.0996] | 0.0894 → 0.0588 |
| IDRiD | 0.2211 → 0.1395 | +0.0816 | [+0.0530, +0.1228] | 0.1171 → 0.0725 |
| Messidor-2 | 0.1768 → 0.1068 | +0.0700 | [+0.0475, +0.1031] | 0.0905 → 0.0575 |
| DDR | 0.2098 → 0.1314 | +0.0784 | [+0.0387, +0.1061] | 0.1067 → 0.0658 |
| ODIR-5K | 0.2387 → 0.1599 | +0.0788 | [+0.0371, +0.1089] | 0.1282 → 0.0817 |
| RFMiD | 0.2606 → 0.1675 | +0.0931 | [+0.0489, +0.1245] | 0.1370 → 0.0899 |

**Bottom line:** `h3_supported=true` — 6/6 domains on both measures, all CIs exclude zero, KL −34…−38%.
⚠️ The size of the reduction **no longer tracks** the size of the transfer gain across domains
(ρ ≈ 0.49); only the RFMiD extreme matches. Report direction, not magnitude correspondence.
The Stage 7 normalization uses source-domain statistics → the convergence is achieved by stages 0–6.
Details: `tables/H-3_domain_distance.md`, `hypotheses/H-3.md`.

---

## exp3 — transfer EyePACS→APTOS (H-4) — COMPLETE, CONFIRMED

Threshold: **G = F1_APTOS / F1_EyePACS ≥ 0.85**.

| Arm | in-domain wF1 | APTOS wF1 | APTOS AUC | APTOS κ | APTOS acc | macro-F1 | **G** |
|-----|---------------|-----------|-----------|---------|-----------|----------|-------|
| C (baseline) | 0.7538 | 0.6465 | 0.7940 | 0.7887 | 0.6338 | 0.4649 | **0.8577** |
| D (full pipeline) | 0.8193 | **0.7354** | **0.8263** | **0.8874** | **0.7272** | **0.5666** | **0.8976** |

Δ wF1 = +0.0889 (CI [+0.0681, +0.1197]); Δ AUC = +0.0323 (CI [+0.0224, +0.0482]).
Referable: Sens 0.7337 → 0.8393, Spec 0.9209 → 0.9411, AUC 0.8944 → 0.9346.

**Bottom line:** `h4_supported=true`.  The threshold is met by **both** arms — the difference comes
from the comparison with baseline. Evaluated on fold-0 checkpoints. Details: `tables/TAB-4.6_exp3_transfer.md`.

---

## exp4 — Grad-CAM explainability (H-5) — COMPLETE, CONFIRMED

EfficientNet-B4, fold 0, all 54 IDRiD images with masks, τ = 0.5.

| Type | n | ALO (C) → ALO (D) | Δ | p (Wilcoxon) | IoU p |
|-----|--:|---|---:|---:|---:|
| Microaneurysms | 54 | 0.2126 → 0.3160 | +0.1034 | 0.0033 | 0.0053 |
| Haemorrhages | 53 | 0.2794 → 0.4011 | +0.1217 | 0.0016 | 0.0029 |
| Hard exudates | 54 | 0.3502 → 0.4790 | +0.1288 | 0.0007 | 0.0011 |
| Soft exudates | 26 | 0.2318 → 0.3310 | +0.0992 | 0.0148 | 0.0189 |

**4/4 types both directionally and statistically**, all CIs exclude zero. Robust to the threshold
(4/4 at τ = 0.2…0.7; at τ = 0.7, 3/4 are significant). **The floor effect has been eliminated:**
ALO = 0 in both arms for only 6/54 images (f₀ = 0.111). Per image, 65–76% improve.

B4 arm classification: full wF1 0.7766 against baseline 0.7545 (+2.2 pp, +0.024 AUC, +0.047 κ).

**Bottom line:** `h5_alo_supported=true`.  **INVARIANTS NC-14** remains in force: Grad-CAM ≠ clinical
localization; phrase it as "attention alignment". Clinical (KZ) overlays have **not been produced**
(gap G-3). Details: `tables/TAB-4.7_exp4_alo_iou.md`, `tables/exp4_classification.md`.

---

## exp5 — clinical degradation (H-7) — COMPLETE, PARTIAL

In-domain: C 0.7538, D 0.8193. Δ_drop = wF1_in-domain − wF1_external.

| Set | n | wF1 (C) | wF1 (D) | Δ | 95% CI (Δ) | p | Δ_drop (C) | Δ_drop (D) | Δ_full < Δ_base? |
|-------|--:|--------:|--------:|--:|------------|--:|-----------:|-----------:|:----------------:|
| IDRiD | 413 | 0.5957 | 0.6592 | +0.0635 | [+0.0445, +0.0919] | 0.0021 | **0.1581** | 0.1601 | ✗ |
| Messidor-2 | 1 744 | 0.6283 | 0.6809 | +0.0526 | [+0.0264, +0.0716] | 0.0138 | **0.1255** | 0.1384 | ✗ |

**Bottom line:** absolute performance on the external sets is significantly higher for **both**
(+0.064 and +0.053). ⚠️ But the hypothesis as written (in terms of Δ_drop) now fails on **both**
sets — the previous revision had IDRiD passing by −0.0045; it flips to +0.0020 here. Verdict:
**0/2, not supported as written.** The cause has been established: Δ_drop is measured from
each arm's own in-domain level and structurally penalizes the stronger arm — in relative terms the
arms degrade almost identically (21.0% vs 19.5% on IDRiD, favouring the pipeline; 16.6% vs 16.9% on
Messidor-2, favouring baseline). The analysis of this metric goes into §5.4
as a contribution in its own right. Details: `tables/TAB-4.8_exp5_degradation.md`, `hypotheses/H-7.md`.

---

## exp6 — device/camera shift (H-6) — COMPLETE, CONFIRMED

Threshold: **g_floor = 0.7**. In-domain: C 0.7538, D 0.8193.

| Camera group | wF1 (C) | wF1 (D) | g_ratio (C) | g_ratio (D) | ≥0.7 |
|--------------|--------:|--------:|------------:|------------:|:----:|
| kowa_idrid | 0.5957 | 0.6592 | 0.7903 | 0.8046 | ✓ / ✓ |
| mixed_ddr | 0.6154 | 0.6671 | 0.8164 | 0.8142 | ✓ / ✓ |
| mixed_odir5k | 0.5700 | 0.6581 | 0.7562 | 0.8032 | ✓ / ✓ |
| topcon_messidor2 | 0.6283 | 0.6809 | 0.8335 | 0.8311 | ✓ / ✓ |
| mixed_rfmid | 0.5434 | 0.6421 | 0.7209 | 0.7837 | ✓ / ✓ |

**Between-group spread:** std(wF1) 0.0307 → **0.0127** (−2.4×, CI [−0.0253, −0.0062]);
std(AUC) 0.0214 → **0.0070** (−3.1×, CI [−0.0233, −0.0072]).

**Bottom line:** `h6_supported=true`. The threshold is met by both arms — the substantive result is
the **significant reduction in spread**: the pipeline lifts the worst groups above all (max Δ at
mixed_rfmid +0.0987, min at mixed_ddr +0.0517). Per-class F1 is higher in all 25 cells and the
between-group spread now contracts on all five classes. ⚠️ g_ratio **falls** in 2 of 5 groups
(mixed_ddr, topcon_messidor2) — a normalization artifact of the larger in-domain denominator, not a
performance drop; absolute wF1 rises in both.
Details: `tables/TAB-4.9_exp6_device.md`.

---

## exp7 / E-7 — small-data training IDRiD→Clinical — COMPLETE (POSITIVE)

EffNet-B3, n_idrid = 516, 5 folds, clinical hold-out n = 60. **Preregistered.**

| Arm | Clinical wF1 | ROC-AUC | κ | Accuracy |
|-----|--------------|---------|-----|----------|
| C (baseline, 3ch) | 0.5134 ± 0.0450 | 0.7417 ± 0.0380 | 0.4876 ± 0.0440 | 0.5231 ± 0.0410 |
| D (full, 4ch) | **0.5932 ± 0.0400** | **0.7899 ± 0.0320** | **0.6121 ± 0.0438** | **0.5932 ± 0.0370** |
| **Δ (D − C)** | **+0.0798** | **+0.0482** | **+0.1245** | +0.0701 |

95% CIs of the differences: wF1 [+0.0350, +0.1106], κ [+0.0782, +0.1960], AUC [+0.0183, +0.0707].
Internal CV on IDRiD: C 0.5850 ± 0.0380 against D 0.6520 ± 0.0310 — the pipeline is higher **in 4 of
5 folds** (one marginal inversion, −0.0057; which fold differs between runs). ⚠️ The unpaired
bootstrap CIs overlap (n = 60) — significance comes from the paired test.

**Bottom line:** positive. The gain (+0.080) is **comparable** to the gain on full EyePACS (+0.0655),
i.e. the pipeline's advantage is not specific to small data. Details: `tables/TAB-4.10_exp7_smalldata.md`.

---

## SSL / A1 — self-supervised learning (probe gate)

**Stage 1 — from-scratch:** BYOL κ 0.0018 (collapse) ✗ · MoCo-v2 50/100 ep. κ 0.113/0.110 ✗ ·
DINO 50/100 ep. κ 0.076/0.060 ✗ · **SIP 100 ep. κ 0.6616 ✓**.

**Stage 2 — continual-SSL (linear probe, patient-level holdout n = 8 036):**

| Backbone | random κ | ImageNet κ | Continual κ | Δκ | run 2 Δκ | passed |
|--------|---------:|-----------:|------------:|---:|------------:|--------|
| ResNet-50 | 0.0040 | 0.3381 | **0.6552** | +0.3171 | +0.2883 | ✓ |
| EfficientNet-B3 | 0.0047 | 0.4450 | **0.6807** | +0.2357 | +0.2336 | ✓ |

**Bottom line:** classical contrastive methods trained from scratch are not competitive with ImageNet
(more epochs do not help); SIP passes the gate; continual-SSL yields a large gain **on both
backbones** (the previous asymmetry — "gain only for ResNet-50" — has **disappeared**). Configs B/D
use continual-ep50. CFC-2.8 formally remains, but has been **decomposed** via the exp2 ablation.
Details: `tables/SSL_continual_gate.md`.
