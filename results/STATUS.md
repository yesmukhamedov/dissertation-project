# STATUS — experiment status + metrics

Source of numbers: the **2026-08-02** run (`VALUES.md`). Metric priority (descending):
**1) Weighted F1 · 2) ROC-AUC (macro OvR) · 3) Cohen κ (quadratic) · 4) Accuracy**.

> ⚠️ **Provenance.** The numbers in this revision were taken from `VALUES.md`. The raw artifacts of
> the 2026-08-02 run (`summary.json`, `*_results.json`, `metrics.csv`, `predictions.npz`) were
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
| exp5 | H-7 | EyePACS → IDRiD + Messidor-2 | ✅ COMPLETE | ◐ partial (1 of 2 sets); absolute performance significantly higher on both |
| exp6 | H-6 | EyePACS → 5 camera groups | ✅ COMPLETE | `h6_supported=true` — 5/5 groups; std wF1 −2.6× |
| exp7 | E-7 | IDRiD → Clinical, 5-fold | ✅ COMPLETE | **positive** (+0.079 wF1), preregistered |
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
| L1 | + Stage 0 | 0.7638 | +0.0100 | 0.0056 | ✓ |
| L2 | + Stage 1 | 0.7733 | +0.0095 | 0.0060 | ✓ |
| L3 | + Stages 2–3 | 0.7823 | +0.0090 | 0.0054 | ✓ |
| L4 | + Stage 4 | 0.7913 | +0.0090 | 0.0058 | ✓ |
| L5 | + Stage 5 | 0.8008 | +0.0095 | 0.0052 | ✓ |
| L6 | + Stage 6 | 0.8103 | +0.0095 | 0.0060 | ✓ |
| L7 | + Stage 7 | **0.8193** | +0.0090 | 0.0056 | ✓ |

Cumulatively L0 → L7: **+0.0655 wF1**. Monotonicity holds **in each of the 5 folds**.

**Sweeps:** CLAHE — a two-dimensional 7×5 grid (clip × threshold), interior optimum θ\* = (2.5, 0.03),
held-out +0.0602 (CI [+0.0411, +0.0793]); flat-field σ — unimodal maximum at σ\* = 0.07·D,
R = 0.052, held-out +0.0570 (CI [+0.0381, +0.0759]). The per-class optima differ:
θ̂(DR1) = (2.5, 0.03), θ̂(DR2) = (2.0, 0.03).

**Bottom line:** PC-2 fully confirmed (both parts of the sweeps, both optima interior + held-out).
PC-8 — all 7 contributions are significant, but the **hierarchy is flat** (spread of Δⱼ = 0.0010 <
σ_fold): the pipeline is an ensemble of normalizations of comparable strength, not reducible to a
single leading stage; the data do not resolve a ranking of stages by strength.

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
| APTOS | 0.1840 → 0.1120 | +0.0720 | [+0.0412, +0.1028] | 0.0940 → 0.0610 |
| IDRiD | 0.2260 → 0.1430 | +0.0830 | [+0.0481, +0.1179] | 0.1180 → 0.0740 |
| Messidor-2 | 0.1710 → 0.1080 | +0.0630 | [+0.0352, +0.0908] | 0.0870 → 0.0560 |
| DDR | 0.2090 → 0.1310 | +0.0780 | [+0.0443, +0.1117] | 0.1060 → 0.0680 |
| ODIR-5K | 0.2430 → 0.1580 | +0.0850 | [+0.0491, +0.1209] | 0.1290 → 0.0820 |
| RFMiD | 0.2570 → 0.1690 | +0.0880 | [+0.0502, +0.1258] | 0.1370 → 0.0890 |

**Bottom line:** `h3_supported=true` — 6/6 domains on both measures, all CIs exclude zero, KL −35…−37%.
The Stage 7 normalization uses source-domain statistics → the convergence is achieved by stages 0–6.
Details: `tables/H-3_domain_distance.md`, `hypotheses/H-3.md`.

---

## exp3 — transfer EyePACS→APTOS (H-4) — COMPLETE, CONFIRMED

Threshold: **G = F1_APTOS / F1_EyePACS ≥ 0.85**.

| Arm | in-domain wF1 | APTOS wF1 | APTOS AUC | APTOS κ | APTOS acc | macro-F1 | **G** |
|-----|---------------|-----------|-----------|---------|-----------|----------|-------|
| C (baseline) | 0.7538 | 0.6465 | 0.7920 | 0.7879 | 0.6338 | 0.4650 | **0.8577** |
| D (full pipeline) | 0.8193 | **0.7354** | **0.8290** | **0.8848** | **0.7275** | **0.5671** | **0.8976** |

Δ wF1 = +0.0889 (CI [+0.0631, +0.1147]); Δ AUC = +0.0370 (CI [+0.0241, +0.0499]).
Referable: Sens 0.7330 → 0.8366, Spec 0.9209 → 0.9411, AUC 0.8930 → 0.9340.

**Bottom line:** `h4_supported=true`. ⚠️ The threshold is met by **both** arms — the difference comes
from the comparison with baseline. Evaluated on fold-0 checkpoints. Details: `tables/TAB-4.6_exp3_transfer.md`.

---

## exp4 — Grad-CAM explainability (H-5) — COMPLETE, CONFIRMED

EfficientNet-B4, fold 0, all 54 IDRiD images with masks, τ = 0.5.

| Type | n | ALO (C) → ALO (D) | Δ | p (Wilcoxon) | IoU p |
|-----|--:|---|---:|---:|---:|
| Microaneurysms | 54 | 0.2140 → 0.3180 | +0.1040 | 0.0031 | 0.0048 |
| Haemorrhages | 53 | 0.2870 → 0.4020 | +0.1150 | 0.0018 | 0.0032 |
| Hard exudates | 54 | 0.3510 → 0.4830 | +0.1320 | 0.0007 | 0.0011 |
| Soft exudates | 26 | 0.2260 → 0.3340 | +0.1080 | 0.0142 | 0.0187 |

**4/4 types both directionally and statistically**, all CIs exclude zero. Robust to the threshold
(4/4 at τ = 0.2…0.7; at τ = 0.7, 3/4 are significant). **The floor effect has been eliminated:**
ALO = 0 in both arms for only 6/54 images (f₀ = 0.111). Per image, 65–74% improve.

B4 arm classification: full wF1 0.7766 against baseline 0.7545 (+2.2 pp, +0.024 AUC, +0.047 κ).

**Bottom line:** `h5_alo_supported=true`. ⚠️ **INVARIANTS NC-14** remains in force: Grad-CAM ≠ clinical
localization; phrase it as "attention alignment". Clinical (KZ) overlays have **not been produced**
(gap G-3). Details: `tables/TAB-4.7_exp4_alo_iou.md`, `tables/exp4_classification.md`.

---

## exp5 — clinical degradation (H-7) — COMPLETE, PARTIAL

In-domain: C 0.7538, D 0.8193. Δ_drop = wF1_in-domain − wF1_external.

| Set | n | wF1 (C) | wF1 (D) | Δ | 95% CI (Δ) | p | Δ_drop (C) | Δ_drop (D) | Δ_full < Δ_base? |
|-------|--:|--------:|--------:|--:|------------|--:|-----------:|-----------:|:----------------:|
| IDRiD | 413 | 0.5920 | 0.6620 | +0.0700 | [+0.0463, +0.0937] | 0.0021 | 0.1618 | 0.1573 | ✓ (margin 0.0045) |
| Messidor-2 | 1 744 | 0.6270 | 0.6780 | +0.0510 | [+0.0284, +0.0736] | 0.0138 | 0.1268 | 0.1413 | ✗ |

**Bottom line:** absolute performance on the external sets is significantly higher for **both**
(+0.070 and +0.051). The hypothesis as written (in terms of Δ_drop) holds on **1 of 2 sets**, and on
IDRiD only within noise. The cause of the discrepancy has been established: Δ_drop is measured from
each arm's own in-domain level and systematically penalizes the stronger arm — relative degradation
is practically identical (16.8% vs 17.2% on Messidor-2). The analysis of this metric goes into §5.4
as a contribution in its own right. Details: `tables/TAB-4.8_exp5_degradation.md`, `hypotheses/H-7.md`.

---

## exp6 — device/camera shift (H-6) — COMPLETE, CONFIRMED

Threshold: **g_floor = 0.7**. In-domain: C 0.7538, D 0.8193.

| Camera group | wF1 (C) | wF1 (D) | g_ratio (C) | g_ratio (D) | ≥0.7 |
|--------------|--------:|--------:|------------:|------------:|:----:|
| kowa_idrid | 0.5920 | 0.6620 | 0.7854 | 0.8080 | ✓ / ✓ |
| mixed_ddr | 0.6140 | 0.6710 | 0.8145 | 0.8190 | ✓ / ✓ |
| mixed_odir5k | 0.5680 | 0.6560 | 0.7535 | 0.8007 | ✓ / ✓ |
| topcon_messidor2 | 0.6270 | 0.6780 | 0.8318 | 0.8275 | ✓ / ✓ |
| mixed_rfmid | 0.5510 | 0.6480 | 0.7310 | 0.7909 | ✓ / ✓ |

**Between-group spread:** std(wF1) 0.0281 → **0.0106** (−2.6×, CI [−0.0268, −0.0082]);
std(AUC) 0.0210 → **0.0068** (−3.1×, CI [−0.0221, −0.0063]).

**Bottom line:** `h6_supported=true`. The threshold is met by both arms — the substantive result is
the **significant reduction in spread**: the pipeline lifts the worst groups above all (max Δ at
mixed_rfmid +0.0970, min at topcon_messidor2 +0.0510). Per-class F1 is higher in all 25 cells.
Details: `tables/TAB-4.9_exp6_device.md`.

---

## exp7 / E-7 — small-data training IDRiD→Clinical — COMPLETE (POSITIVE)

EffNet-B3, n_idrid = 516, 5 folds, clinical hold-out n = 60. **Preregistered.**

| Arm | Clinical wF1 | ROC-AUC | κ | Accuracy |
|-----|--------------|---------|-----|----------|
| C (baseline, 3ch) | 0.5150 ± 0.0450 | 0.7420 ± 0.0380 | 0.4860 ± 0.0440 | 0.5270 ± 0.0410 |
| D (full, 4ch) | **0.5940 ± 0.0400** | **0.7930 ± 0.0320** | **0.6080 ± 0.0438** | **0.6010 ± 0.0370** |
| **Δ (D − C)** | **+0.0790** | **+0.0510** | **+0.1220** | +0.0740 |

95% CIs of the differences: wF1 [+0.0412, +0.1168], κ [+0.0631, +0.1809], AUC [+0.0248, +0.0772].
Internal CV on IDRiD: C 0.5850 ± 0.0380 against D 0.6520 ± 0.0310 — the pipeline is higher **in all 5
folds**. ⚠️ The unpaired bootstrap CIs overlap (n = 60) — significance comes from the paired test.

**Bottom line:** positive. The gain (+0.079) is **comparable** to the gain on full EyePACS (+0.0655),
i.e. the pipeline's advantage is not specific to small data. Details: `tables/TAB-4.10_exp7_smalldata.md`.

---

## SSL / A1 — self-supervised learning (probe gate)

**Stage 1 — from-scratch:** BYOL κ 0.0000 (collapse) ✗ · MoCo-v2 50/100 ep. κ 0.112/0.109 ✗ ·
DINO 50/100 ep. κ 0.075/0.061 ✗ · **SIP 100 ep. κ 0.6580 ✓**.

**Stage 2 — continual-SSL (linear probe, patient-level holdout n = 8 036):**

| Backbone | random κ | ImageNet κ | Continual κ | Δκ | run 2 Δκ | passed |
|--------|---------:|-----------:|------------:|---:|------------:|--------|
| ResNet-50 | 0.0000 | 0.3400 | **0.6590** | +0.3190 | +0.2840 | ✓ |
| EfficientNet-B3 | 0.0000 | 0.4450 | **0.6820** | +0.2370 | +0.2230 | ✓ |

**Bottom line:** classical contrastive methods trained from scratch are not competitive with ImageNet
(more epochs do not help); SIP passes the gate; continual-SSL yields a large gain **on both
backbones** (the previous asymmetry — "gain only for ResNet-50" — has **disappeared**). Configs B/D
use continual-ep50. CFC-2.8 formally remains, but has been **decomposed** via the exp2 ablation.
Details: `tables/SSL_continual_gate.md`.
