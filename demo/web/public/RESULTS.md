# Experimental Results — Canonical Numerical Reference

**Dissertation:** Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification  
**Candidate:** Yesmukhamedov N.S. (IITU)  
**Document type:** Canonical numerical reference  
**Source of truth:** `results/` knowledge base (`results/STATUS.md`, `results/tables/`)  
**Governance:** INVARIANTS | HYPOTHESIS | RESEARCH_ARCHITECTURE  
**Pipeline:** 8-stage preprocessing (isotropic resize + FOV mask + adaptive flat-field + dataset-specific normalization)

---

## 1. Purpose and scope

This document is the **single canonical numerical reference** for all experimental results. All deliverables (chapters, presentations, dashboards, demo repositories) must cite these exact numbers. Any deviation requires updating this document first.

This document records the results for all active dissertation experiments (Experiments 1–7). It serves two purposes: (a) providing presentation-ready charts and numerical values for the committee defense, and (b) establishing a single canonical set of numerical values that all future deliverables must reference to prevent numerical inconsistencies.

---

## 2. Deliverables inventory

This stage produced 28 presentation-quality PNG charts (200 DPI) and one interactive React dashboard (.jsx artifact). The complete inventory:

### 2.1 Original charts (01–21)

| # | Filename | Experiment | Content |
|---|----------|------------|---------|
| 01 | `01_exp1_factorial_f1.png` | Exp 1 | 2×2 factorial weighted F1 with error bars |
| 02 | `02_exp1_all_metrics.png` | Exp 1 | All 4 primary metrics (F1, AUC, κ, Acc) by configuration |
| 03 | `03_exp1_delta.png` | Exp 1 | Preprocessing improvement Δ, ResNet-50 vs EfficientNet-B3 |
| 04 | `04_exp2_ablation.png` | Exp 2 | Cumulative ablation — pipeline stages |
| 05 | `05_exp2_per_stage.png` | Exp 2 | Per-stage marginal contribution to F1 |
| 06 | `06_exp4_alo.png` | Exp 4 | ALO by lesion type, baseline vs preprocessed |
| 07 | `07_exp4_iou.png` | Exp 4 | IoU by lesion type, baseline vs preprocessed |
| 08 | `08_exp5_generalization.png` | Exp 3/5 | Cross-dataset F1 and AUC (dual chart) |
| 09 | `09_exp5_G_ratio.png` | Exp 3/5 | Generalization ratio G with H-4 threshold |
| 10 | `10_exp6_device_shift.png` | Exp 6 | Cross-device F1 by camera manufacturer |
| 11 | `11_summary_radar.png` | Summary | Radar chart — overall baseline vs pipeline |
| 12 | `12_eh3_dominance.png` | Exp 1 | EH-3 dominance criterion check |
| 13 | `13_exp2_clahe_sensitivity.png` | Exp 2 | CLAHE parameter sensitivity heatmap (H-2) |
| 14 | `14_clinical_metrics.png` | Clinical | Sensitivity, Specificity, PPV, NPV for referable DR |
| 15 | `15_calibration.png` | Clinical | ECE, Brier Score, reliability diagram |
| 16 | `16_image_quality.png` | Quality | CNR, Entropy, SSIM at level L0 vs L7 (VVI removed — not implemented) |
| 17 | `17_computational.png` | Compute | Params, GFLOPs, inference latency, GPU memory |
| 18 | `18_per_class_f1.png` | Exp 1 | Per-class F1 breakdown by DR grade (5 classes) |
| 19 | `19_training_curves.png` | Exp 1 | Training curves — validation loss and F1 over epochs |
| 20 | `20_confusion_matrix.png` | Exp 1 | Normalized confusion matrices (baseline vs pipeline) |
| 21 | `21_statistical_tests.png` | Statistical | DeLong, McNemar p-values and bootstrap CI |

### 2.2 Supplementary charts (22–28)

| # | File | Content |
|---|------|---------|
| 22 | `22_exp1_all_6_configs.png` | All 4 configs A–D (preprocessing dominance across both architectures) |
| 23 | `23_exp2_individual_ablation.png` | Per-stage marginal contribution, pipeline order (bar view of Fig 05) |
| 24 | `24_roc_curves.png` | Per-class ROC, baseline vs pipeline |
| 25 | `25_pipeline_stages_real.png` | Real fundus image (43199_right, DR4) through all stages |
| 26 | `26_bilateral_pair.png` | Bilateral pair (both eyes) with canonical flip |
| 27 | `27_gradcam_overlay.png` | Grad-CAM on real image, baseline vs pipeline |
| 28 | `28_attention_consistency.png` | Per-image direction of the ALO effect (improved / worsened / unchanged) |

### 2.3 Interactive dashboard

The React dashboard in `demo/web/` renders every value in this document from `src/data.js`, which mirrors `results/tables/` constant by constant. Each section carries its explanatory notes and caveats inline.

---

## 3. Canonical numerical values

All values below constitute the binding numerical reference for this dissertation. Any future document referencing these results must use exactly these numbers.

### 3.1 Experiment 1 — 2×2 Factorial (H-1: Preprocessing Dominance)

**Setup:** EyePACS 100% (~35,126 images), 5-fold patient-level cross-validation, max 20 epochs, early stopping patience 5 (val_loss) / 3 (val_F1), seed=42, deterministic=true. **Loss function:** Focal Loss (γ=2, α=inverse-frequency class weights). **Input:** 4-channel tensors (3 dataset-specific-normalized RGB + 1 binary FOV mask). **Resize:** Isotropic scaling with centered zero-padding (preserves fundus circle geometry). Both backbone first conv layers modified for 4-channel input (pretrained RGB weights preserved, mask channel = mean of RGB weights).

| Config | Preprocessing | CNN | W. F1 | ROC-AUC | Cohen κ | Accuracy | macro-F1 |
|--------|--------------|-----|-------|---------|---------|----------|----------|
| A | Baseline (3ch, stretch-resize + ImageNet norm) | ResNet-50 | 0.7518 ± 0.0110 | 0.8300 ± 0.0140 | 0.7410 ± 0.0350 | 0.7247 ± 0.0180 | 0.4281 |
| B | Full pipeline (4ch) | ResNet-50 | 0.8172 ± 0.0090 | 0.8620 ± 0.0110 | 0.8539 ± 0.0260 | 0.8027 ± 0.0150 | 0.5322 |
| C | Baseline (3ch, stretch-resize + ImageNet norm) | EfficientNet-B3 | 0.7538 ± 0.0120 | 0.8210 ± 0.0150 | 0.7468 ± 0.0330 | 0.7273 ± 0.0190 | 0.4300 |
| D | Full pipeline (4ch) | EfficientNet-B3 | 0.8193 ± 0.0100 | 0.8570 ± 0.0120 | 0.8571 ± 0.0270 | 0.8052 ± 0.0160 | 0.5355 |

**Paired differences with 95% CI (all six exclude zero):**

| Pair | Metric | Δ | 95% CI |
|------|--------|---|--------|
| B − A | W. F1 | +0.0654 | [+0.0521, +0.0873] |
| B − A | ROC-AUC | +0.0320 | [+0.0175, +0.0419] |
| B − A | Cohen κ | +0.1129 | [+0.0780, +0.1414] |
| D − C | W. F1 | +0.0655 | [+0.0423, +0.0801] |
| D − C | ROC-AUC | +0.0360 | [+0.0204, +0.0462] |
| D − C | Cohen κ | +0.1103 | [+0.0829, +0.1453] |

**EH-3 Dominance Criterion (threshold: ΔF1 ≥ 5pp, ΔAUC ≥ 2pp, Δκ > 0):**

| Comparison | ΔF1 (pp) | ΔAUC (pp) | Δκ (pp) | EH-3 Satisfied |
|-----------|----------|-----------|---------|----------------|
| ResNet-50: B − A | +6.54 | +3.20 | +11.29 | **YES** |
| EfficientNet-B3: D − C | +6.55 | +3.60 | +11.03 | **YES** |

**H-1 confirmed.** All three components of EH-3 are met independently on both architectures, with margin: ΔF1 exceeds the 5pp threshold by ~1.5pp, ΔAUC exceeds the 0.02 threshold, and κ does not merely avoid degradation but rises by +0.11. Significance: DeLong p = 0.0041 (B vs A) and 0.0028 (D vs C); McNemar p = 0.0057 and 0.0041; both survive the Holm correction across the 4 configurations (p_adj = 0.0082 / 0.0056). The mixed-effects ANOVA finds **no** arm × architecture interaction (p = 0.31), which is the statistical form of "on both backbones" — and the numbers agree, with ΔF1 matching to the second decimal (+6.54 vs +6.55pp).

The gain is concentrated on the minority classes: macro-F1 rises further than weighted F1 (+0.1041 for B−A, +0.1055 for D−C), and F1 for DR 1 roughly doubles. Cross-validation confidence intervals for baseline and pipeline **do not overlap on any of the four primary metrics**.

**Decomposition of the CFC-2.8 confound.** The 8-level cumulative ablation (§3.2) runs on the same corpus and split under a **single initialization across all levels**, and reproduces the whole +0.0655: its endpoints coincide numerically with Config C (0.7538) and Config D (0.8193). The preprocessing contribution is therefore measured separately from the SSL-initialization contribution, and H-1 no longer rests on an inseparable composite.

**Convergence and overfitting (best-epoch, per fold):**

| Config | Arm | Best epochs | Train loss | Val loss | Loss gap |
|--------|-----|-------------|------------|----------|----------|
| A | baseline, ResNet-50 | 16, 14, 17, 15, 16 | 0.098 | 0.150 | 0.052 |
| B | pipeline, ResNet-50 | 9, 8, 10, 9, 9 | 0.126 | 0.147 | **0.021** |
| C | baseline, EffNet-B3 | 15, 17, 14, 16, 15 | 0.102 | 0.156 | 0.054 |
| D | pipeline, EffNet-B3 | 8, 9, 7, 9, 8 | 0.131 | 0.153 | **0.022** |

The pipeline arms converge ~7 epochs earlier at a 2.5× smaller loss gap — and do so at a **higher** train loss (0.126–0.131 vs 0.098–0.102) with comparable validation loss. They fit the training set less well yet generalize at least as well: regularizer behaviour, not a better fit. The best-epoch spread within an arm is ±1–1.5 epochs, so the regime is reproducible across folds rather than a lucky seed.

### 3.2 Experiment 2 — Preprocessing Component Ablation (H-1 decomposition, H-2)

**Protocol:** EyePACS 100% (n = 35,126), 5 folds, EfficientNet-B3, **a single initialization shared by all 8 levels**. Directly comparable with Experiment 1: level L0 reproduces Config C and level L7 reproduces Config D.

**Cumulative ablation sequence:**

| Level | Pipeline configuration | W. F1 | ROC-AUC | Cohen κ | Accuracy | Δ F1 (pp) | 2·σ_fold (pp) | Exceeds noise |
|-------|----------------------|-------|---------|---------|----------|-----------|---------------|---------------|
| L0 | Baseline (stretch-resize + ImageNet normalize, 3ch) | 0.7538 | 0.8210 | 0.7468 | 0.7273 | — | — | — |
| L1 | + Canonical flip (Stage 0) | 0.7609 | 0.8260 | 0.7590 | 0.7356 | +0.71 | 0.48 | ✓ |
| L2 | + OD-fovea rotation (Stage 1) | 0.7677 | 0.8299 | 0.7701 | 0.7456 | +0.68 | 0.42 | ✓ |
| L3 | + FOV crop + mask (Stages 2–3) | 0.7759 | 0.8360 | 0.7818 | 0.7561 | +0.82 | 0.48 | ✓ |
| L4 | + Flat-field correction (Stage 4) | 0.7902 | 0.8436 | 0.8038 | 0.7738 | **+1.43** | 0.60 | ✓ |
| L5 | + CLAHE enhancement (Stage 5) | 0.8027 | 0.8505 | 0.8267 | 0.7899 | **+1.25** | 0.56 | ✓ |
| L6 | + Augmentation (Stage 6) | 0.8128 | 0.8541 | 0.8426 | 0.7977 | +1.01 | 0.54 | ✓ |
| L7 | + Dataset-specific normalize (Stage 7) | **0.8193** | **0.8570** | **0.8571** | **0.8052** | +0.65 | 0.42 | ✓ |

Cumulative L0 → L7: **ΔF1 = +6.55pp**, ΔAUC = +0.0360, Δκ = +0.1103, ΔAcc = +7.79pp. Monotonicity holds **within every one of the 5 folds**, without a single inversion.

**Per-fold weighted F1 by level:**

| Level | fold 1 | fold 2 | fold 3 | fold 4 | fold 5 |
|-------|--------|--------|--------|--------|--------|
| L0 | 0.7533 | 0.7554 | 0.7562 | 0.7543 | 0.7498 |
| L1 | 0.7593 | 0.7637 | 0.7598 | 0.7632 | 0.7585 |
| L2 | 0.7643 | 0.7692 | 0.7670 | 0.7693 | 0.7687 |
| L3 | 0.7773 | 0.7779 | 0.7758 | 0.7718 | 0.7767 |
| L4 | 0.7955 | 0.7893 | 0.7883 | 0.7894 | 0.7885 |
| L5 | 0.8021 | 0.8052 | 0.8038 | 0.8043 | 0.7981 |
| L6 | 0.8140 | 0.8097 | 0.8103 | 0.8158 | 0.8142 |
| L7 | 0.8182 | 0.8180 | 0.8225 | 0.8174 | 0.8204 |

**Every stage contributes significantly, and the hierarchy is resolvable.** All 7 transitions exceed the 2·σ_fold band, and the contributions span 0.65–1.43pp — a spread of 0.78pp, roughly **3× σ_fold** (0.21–0.30pp), so the stages *can* be ordered against one another from these data:

| Rank | Level | Stage | Δⱼ (pp) | Share of the +6.55pp total |
|---|---|---|---|---|
| 1 | L4 | Stage 4 — flat-field | **+1.43** | 22% |
| 2 | L5 | Stage 5 — CLAHE | **+1.25** | 19% |
| 3 | L6 | Stage 6 — augmentation | +1.01 | 15% |
| 4 | L3 | Stages 2–3 — FOV crop + mask | +0.82 | 13% |
| 5 | L1 | Stage 0 — canonical flip | +0.71 | 11% |
| 6 | L2 | Stage 1 — OD-fovea rotation | +0.68 | 10% |
| 7 | L7 | Stage 7 — normalize → tensor | +0.65 | 10% |

The two **illumination/contrast** stages (flat-field + CLAHE) together account for **41%** of the total gain — about as much as the four geometric/normalization stages combined. No stage is redundant: the weakest still contributes +0.65pp, above its own 0.42pp noise band. But the pipeline is **not** an ensemble of equals — photometric normalization is where most of the effect lives, which is exactly what an H-3 photometric-convergence mechanism predicts.

**Caveats.** The ordering is fixed by the pipeline, so Δⱼ is the contribution of stage j *given* stages 0…j−1 — these are not isolated single-stage effects, and inter-stage interactions are not measured. **Stage 3 (FOV mask) is not isolated**: level L3 adds Stages 2 and 3 together, because disabling the mask would require a 3-channel model variant, so rank 4 belongs to the pair rather than to Stage 2 alone. The 2·σ_fold threshold is a heuristic for the significance of a contribution, not a formal paired test, and **the ranking rests on the same heuristic** — the ordering of adjacent ranks (Stage 1 at +0.68pp against Stage 7 at +0.65pp) is within noise. What the data support is the **grouping** — the two photometric stages clearly above the rest — not a strict 1-to-7 order.

**H-2 CLAHE parameter sensitivity (joint sweep on EyePACS, 8 × 5 = 40 grid points, train folds):**

| Parameter | Overall optimum θ* | DR Grade 1 optimum | DR Grade 2 optimum |
|-----------|-------------------|-------------------|-------------------|
| clip_factor | 2.5 | 2.5 | 2.0 |
| global_threshold | 0.03 | 0.03 | 0.03 |
| p_apply | 0.80 | — | — |

**Held-out confirmation:**

| Arm | W. F1 | F1 (DR 1) | F1 (DR 2) |
|-----|-------|-----------|-----------|
| CLAHE = off | 0.7538 | 0.0976 | 0.5316 |
| CLAHE = θ* | **0.8137** | **0.2091** | **0.6477** |
| Δ | +0.0599, 95% CI [+0.0388, +0.0770] | +0.1115 | +0.1161 |

The surface is non-monotone along **both** axes with an **interior** maximum — exactly what H-2 asserts. The per-class optima differ: DR 1 (subtle microaneurysms) needs a more aggressive clip (2.5) than DR 2 (2.0), i.e. the optimal strength of local equalization depends on lesion size. Over-enhancement (clip_factor > 3.0) degrades both grades by amplifying noise.

> The grids are train-fold values used to *select* θ*, not a performance estimate. On held-out data the per-class figures diverge in both directions — F1(DR 1) is markedly lower than the grid value at θ* (0.2091 vs 0.4693), F1(DR 2) higher (0.6477 vs 0.5968). Quote the held-out numbers.

**Flat-field σ factor sweep (EfficientNet-B3 on EyePACS, Stages 0–4 active):**

| σ / FOV diameter | W. F1 | CNR |
|-----------------|-------|-----|
| 0.05 | 0.7662 | 3.24 |
| 0.06 | 0.7883 | 3.47 |
| **0.07** | **0.8089** | **3.93** |
| 0.08 | 0.7930 | 3.66 |
| 0.09 | 0.7774 | 3.35 |
| 0.10 | 0.7577 | 3.10 |

Held-out: flat-field off 0.7513 → σ* 0.8087, Δ = +0.0574, 95% CI [+0.0428, +0.0806].

The profile is strictly unimodal with an interior maximum at σ* = 0.07·D and symmetric fall-off. The range over the sweep (R = 0.0512) is comparable to the entire pipeline effect, so σ genuinely requires tuning rather than an arbitrary choice. σ* coincides with the value already fixed in the Stage 4 specification — the sweep confirms the existing setting. Within this single stage CNR and F1 are aligned (both peak at 0.07); across different stages they are not (§3.10). Note that the CNR normalization here differs from §3.10, so absolute values are not comparable between the two.

Flat-field is also the **single largest classification contributor** in the cumulative ablation (Δⱼ = +1.43pp, rank 1), so the parameter this sweep tunes governs the largest single part of the pipeline effect. Both halves of H-2 — the CLAHE grid and the σ sweep — are run on EyePACS.

### 3.3 Experiment 4 — Explainability Analysis (H-5)

**Setup:** EfficientNet-B3 (fold 0), Grad-CAM on the final convolutional layer, compared against IDRiD pixel-level lesion masks. Analysed on **all 54** IDRiD images that carry masks, at the canonical binarization threshold τ = 0.5, with a paired one-sided Wilcoxon test and bootstrap CIs of the difference.

**ALO — Attention-Lesion Overlap (primary metric):**

| Lesion type | n | Baseline | Pipeline | Δ | 95% CI (Δ) | p (Wilcoxon) | Relative Δ |
|-------------|---|----------|----------|---|-----------|--------------|-----------|
| Microaneurysms | 54 | 0.2126 | 0.3160 | +0.1034 | [+0.0331, +0.1587] | **0.0033** | +49% |
| Hemorrhages | 53 | 0.2794 | 0.4011 | +0.1217 | [+0.0485, +0.1739] | **0.0016** | +44% |
| Hard exudates | 54 | 0.3502 | 0.4790 | +0.1288 | [+0.0735, +0.2007] | **0.0007** | +37% |
| Soft exudates | 26 | 0.2318 | 0.3310 | +0.0992 | [+0.0401, +0.1969] | **0.0148** | +43% |

**IoU — Intersection-over-Union (secondary metric):**

| Lesion type | n | Baseline | Pipeline | Δ | 95% CI (Δ) | p (Wilcoxon) | Relative Δ |
|-------------|---|----------|----------|---|-----------|--------------|-----------|
| Microaneurysms | 54 | 0.1065 | 0.1694 | +0.0629 | [+0.0304, +0.1042] | **0.0053** | +59% |
| Hemorrhages | 53 | 0.1516 | 0.2229 | +0.0713 | [+0.0166, +0.1050] | **0.0029** | +47% |
| Hard exudates | 54 | 0.1944 | 0.2830 | +0.0886 | [+0.0318, +0.1256] | **0.0011** | +46% |
| Soft exudates | 26 | 0.1183 | 0.1775 | +0.0592 | [+0.0223, +0.1155] | **0.0189** | +50% |

**H-5 confirmed.** ALO is higher for the preprocessed model on **4 of 4** lesion types (criterion: ≥3/4), and **all four** differences are statistically significant (p 0.0007–0.0148) with CIs excluding zero. IoU agrees on all four types (p 0.0011–0.0189). ALO rises by 37–49% and IoU by 46–59%. ALO ranks lesion types by detectability: hard exudates (bright, well-defined boundaries) > hemorrhages > soft exudates ≈ microaneurysms (tiny, point-like); the largest absolute gain is hard exudates (+0.1288). Soft exudates carry the weakest significance simply because only 26 of the 54 images are annotated for them.

**Per-image direction of the effect:**

| Lesion type | n | ↑ better | ↓ worse | = unchanged | share ↑ |
|-------------|---|----------|---------|-------------|---------|
| Microaneurysms | 54 | 38 | 7 | 9 | 70% |
| Hemorrhages | 53 | 36 | 8 | 9 | 68% |
| Hard exudates | 54 | 41 | 5 | 8 | 76% |
| Soft exudates | 26 | 17 | 4 | 5 | 65% |

**Robustness to the binarization threshold:**

| τ | Types improved | Types significant (p < 0.05) |
|---|----------------|------------------------------|
| 0.2 | 4 / 4 | 4 / 4 |
| 0.3 | 4 / 4 | 4 / 4 |
| **0.5** (canonical) | **4 / 4** | **4 / 4** |
| 0.7 | 4 / 4 | 3 / 4 |

The direction survives at every threshold; significance is lost for exactly one type at the strictest τ = 0.7, where the activated area is smallest. **Floor effect:** ALO = 0 in *both* arms for only 6 of 54 images (f₀ = 0.111), so the measurement operates inside the metric's working range rather than at its sensitivity limit.

> **INVARIANTS NC-14 remains binding.** Grad-CAM activation is **not** clinical localization of pathology. The correct phrasing is "the preprocessed model's attention is significantly better aligned with annotated lesions", not "the model finds lesions" and not "the model is clinically interpretable". Confirming H-5 does not weaken NC-14 — it measures alignment, not diagnostic localization.

**Classification of the two Grad-CAM arms (EfficientNet-B4, fold 0):** baseline W. F1 0.7545 vs pipeline 0.7766 (+2.21pp, +0.0235 AUC, +0.0473 κ). Note this is a different backbone and a single fold, so the magnitude is not comparable with Experiment 1 — it shows direction, not effect size.

**Not closed:** the qualitative Grad-CAM overlays on the Kazakh clinical dataset that the H-5 statement also calls for have not been produced (gap G-3).

### 3.4 Experiment 3 — APTOS 2019 Transferability (H-4)

**Setup:** Models trained on EyePACS (Canon CR-1), evaluated on APTOS 2019 (3,662 images, mixed cameras, Indian population) without retraining (zero-shot transfer). EfficientNet-B3, **fold-0 checkpoints**; Configs A/B were not evaluated on APTOS.

**Full APTOS 2019 metrics:**

| Config | Preprocessing | EyePACS F1 | APTOS F1 | APTOS AUC | APTOS κ | APTOS Acc | macro-F1 | G |
|--------|--------------|------------|----------|-----------|---------|-----------|----------|---|
| C | Baseline (3ch) | 0.7538 | 0.6465 | 0.7940 | 0.7887 | 0.6338 | 0.4649 | 0.8577 |
| D | Pipeline (4ch) | 0.8193 | **0.7354** | **0.8263** | **0.8874** | **0.7272** | **0.5666** | **0.8976** |

**Paired differences:** Δ W. F1 = +0.0889, 95% CI [+0.0681, +0.1197]; Δ AUC = +0.0323, 95% CI [+0.0224, +0.0482]. Both CIs exclude zero.

**Generalization Ratio G = F1_APTOS / F1_EyePACS (H-4 criterion: G ≥ 0.85 and pipeline > baseline):**

| Config | G | G ≥ 0.85 |
|--------|---|----------|
| C (baseline + EfficientNet-B3) | 0.8577 | YES ✓ |
| D (pipeline + EfficientNet-B3) | **0.8976** | **YES** ✓ |

**H-4 confirmed** on both parts: the threshold is cleared with 0.048 to spare, and the pipeline transfers better than the baseline.

> **Caveat that must be carried into the text.** The baseline also clears G ≥ 0.85 (0.8577), so that criterion **on its own does not separate the arms** — the discriminating part of H-4 is "better than baseline". The honest phrasing is that the pipeline does not *rescue* transfer, it improves transfer that was already acceptable.

**Per-class F1 on APTOS:**

| Config | DR 0 | DR 1 | DR 2 | DR 3 | DR 4 | macro-F1 |
|--------|------|------|------|------|------|----------|
| C | 0.8554 | 0.1395 | 0.5747 | 0.2438 | 0.5113 | 0.4649 |
| D | 0.9152 | 0.2720 | 0.6931 | 0.3252 | 0.6275 | 0.5666 |

The gain is present on **all five** grades. macro-F1 rises more than weighted F1 (+0.1017 vs +0.0889), so it is concentrated on the minority grades. The pipeline holds the middle grades in particular — the usual failure point in transfer: in the confusion matrix, DR 2 → DR 1 mass falls from 245 to 192 images and DR 2 → DR 0 from 96 to 33. Remaining errors stay adjacent on the severity scale (DR 0 → DR 4: 2 → 0), which is why κ gains most of all (+0.0987).

**Referable DR on APTOS (grade ≥ 2):**

| Config | Sensitivity | Specificity | PPV | NPV | Referable AUC |
|--------|-------------|-------------|-----|-----|---------------|
| C | 0.7337 | 0.9209 | 0.8638 | 0.8349 | 0.8944 |
| D | 0.8393 | 0.9411 | 0.9070 | 0.8955 | 0.9346 |

Sensitivity +10.56pp **with specificity also rising** — the same pattern as in-domain and across camera groups.

> G is normalized by each arm's own in-domain F1 (C: 0.7538, D: 0.8193), so the stronger arm carries a larger denominator: ΔG (+0.040) is a deliberately conservative view of an absolute APTOS gain of +0.089. Evaluated from fold-0 checkpoints, so there is no between-fold variance and the CIs above are per-instance bootstrap intervals.

### 3.5 Experiment 5 — External Clinical Performance (H-7)

**Setup:** Models trained on EyePACS with full pipeline (Config D) vs baseline (Config C), evaluated on IDRiD (Kowa camera, Indian population) and Messidor-2 (Topcon camera, French population) without retraining.

**Operative criterion (form S, both sets mandatory):**

```
H-7  ⟺  ⋀            PASS_S(wF1, D−C on X) = 1
        X ∈ {IDRiD, Messidor-2}

PASS_S  ⟺  Δ wF1(X) = wF1(D,X) − wF1(C,X)  ≥  MCID_wF1 = 0.050   ∧   CI⁻ > 0
```

The sets are **not aggregated**: a single reversal (CI⁺ < 0) on either would give REVERSED regardless of the other.

**Within-architecture comparison (EfficientNet-B3, fold-0 checkpoints):**

| Dataset | n | Baseline (C) F1 | Pipeline (D) F1 | Δ F1 | 95% CI (Δ) | p (1-sided) |
|---------|---|-----------------|-----------------|------|-----------|-------------|
| EyePACS (in-domain) | 35,126 | 0.7538 | 0.8193 | — | — | — |
| IDRiD | 413 | 0.5938 | **0.6627** | +0.0689 | [+0.0494, +0.0968] | **0.0021** |
| Messidor-2 | 1,744 | 0.6282 | **0.6823** | +0.0541 | [+0.0362, +0.0814] | **0.0138** |

**Element-wise check:**

| Condition | IDRiD | Messidor-2 |
|---|---|---|
| Δ ≥ MCID = 0.050 | +0.0689 ✓ (margin +0.0189) | +0.0541 ✓ (margin +0.0041) |
| CI⁻ > 0 | +0.0494 ✓ | +0.0362 ✓ |
| **PASS_S** | **1** | **1** |

**Σ PASS = 2 = N → H-7 CONFIRMED (2 of 2).** On both external clinical sets — different hardware, different population, no retraining — the integrated configuration delivers absolute weighted F1 higher than baseline by a clinically meaningful margin, with confidence intervals excluding zero.

**Formulation for the text:** "on transfer to external clinical sets without retraining, the integrated configuration delivers absolute weighted F1 higher than baseline by +0.069 (IDRiD) and +0.054 (Messidor-2), both above the MCID of 0.05 and with intervals excluding zero."

> **Caveat that must be carried into the text.** Form S requires Δ ≥ MCID **and** CI⁻ > 0 — *not* CI⁻ ≥ MCID. On Messidor-2 the lower bound (+0.0362) sits below the 0.050 threshold, which does not block the pass, and the margin on Δ itself is **0.0041**. The Messidor-2 pass is real but not comfortable: a re-run that moves Δ by more than that flips the set.

**Δ_drop — reference only, and retired as a criterion:**

| External dataset | Δ_drop baseline (pp) | Δ_drop pipeline (pp) | Difference (pp) | Relative drop (C / D) |
|-----------------|---------------------|---------------------|-----------------|-----------------------|
| IDRiD | 16.00 | 15.66 | −0.34 | 21.2% / 19.1% |
| Messidor-2 | 12.56 | 13.70 | +1.14 | 16.7% / 16.7% |

**Why Δ_drop was retired — a methodological contribution in its own right.** The quantity is not independent of the hypothesis it was meant to test. Expanding:

```
Δ_drop(D,X) − Δ_drop(C,X)
  = [wF1(D,in) − wF1(D,X)] − [wF1(C,in) − wF1(C,X)]
  = Δ_in-domain − Δ_external
  = 0.0655 − Δ wF1(X)
```

The sign of the comparison is therefore fixed by a single question: *does the external margin exceed the in-domain margin of 6.55pp?* The criterion demands that the pipeline beat the baseline **more on foreign data than on its own**, and penalizes it precisely for its in-domain win. It measures nothing about resistance. The identity checks out on both sets: IDRiD 0.0655 − 0.0689 = −0.0034; Messidor-2 0.0655 − 0.0541 = +0.0114.

**What must not be claimed:** reduced degradation. Once each arm is normalized by its own in-domain level the structural skew almost vanishes — 21.2% vs 19.1% on IDRiD, 16.7% vs 16.7% on Messidor-2. **The same defect recurs in the H-6 g_ratio** (§3.6), so one argument covers both metrics.

**AUC on external datasets:**

| Dataset | Baseline AUC | Pipeline AUC | Δ |
|---------|-------------|-------------|---|
| EyePACS (in-domain) | 0.8210 | 0.8570 | +0.0360 |
| IDRiD | 0.8195 | 0.8627 | +0.0432 |
| Messidor-2 | 0.8407 | 0.8729 | +0.0322 |

> The same two datasets appear in Experiment 6 as the camera groups `kowa_idrid` and `topcon_messidor2` — the numbers are identical.

### 3.6 Experiment 6 — Device Domain Shift (H-6)

**Weighted F1 across camera groups (generalization floor g_floor = 0.70):**

| Camera group | Camera(s) | n | Baseline | Pipeline | Δ (pp) | g (base) | g (pipe) | ≥ 0.70 |
|--------------|-----------|---|----------|----------|--------|----------|----------|--------|
| EyePACS (in-domain) | Canon CR-1 | 35,126 | 0.7538 | 0.8193 | +6.55 | — | — | — |
| kowa_idrid | Kowa | 413 | 0.5938 | 0.6627 | +6.89 | 0.7877 | 0.8089 | ✓ / ✓ |
| mixed_ddr | Canon, Topcon | 1,200 | 0.6154 | 0.6671 | +5.17 | 0.8164 | 0.8142 | ✓ / ✓ |
| mixed_odir5k | Canon, Zeiss | 950 | 0.5700 | 0.6581 | +8.81 | 0.7562 | 0.8032 | ✓ / ✓ |
| topcon_messidor2 | Topcon | 1,744 | 0.6282 | 0.6823 | +5.41 | 0.8334 | 0.8328 | ✓ / ✓ |
| mixed_rfmid | Topcon, Kowa | 640 | 0.5434 | 0.6421 | +9.87 | 0.7209 | 0.7837 | ✓ / ✓ |

**Between-device spread (over the 5 external camera groups, excluding EyePACS):**

| Spread measure | Baseline | Pipeline | Δ | 95% CI (Δ) | Factor |
|----------------|----------|----------|---|-----------|--------|
| std (weighted F1) | 0.0306 | **0.0130** | −0.0176 | [−0.0253, −0.0062] | 2.4× |
| std (ROC-AUC) | 0.0214 | **0.0070** | −0.0144 | [−0.0233, −0.0072] | 3.1× |

**H-6 confirmed.** All 5 groups clear the floor for **both** arms (pipeline minimum 0.7837 on RFMiD, a margin of 0.084 over the threshold).

> Since the threshold is cleared by both arms, it does not by itself separate them. **The substantive result is the collapse of the spread**: between-device F1 std falls 2.4× and AUC std 3.1×, both CIs excluding zero. The g-ratio range narrows from 0.7209–0.8334 (span 0.113) to 0.7837–0.8328 (span 0.049).

**Mechanism: the pipeline lifts the floor, not the ceiling.** The gain scales inversely with how well a group already worked — largest on mixed_rfmid (+9.87pp, the baseline's worst group) and mixed_odir5k (+8.81pp), smallest on mixed_ddr (+5.17pp) and topcon_messidor2 (+5.41pp, the baseline's best). That inverse relationship is precisely what produces the narrower spread.

**g_ratio falls marginally in 2 of the 5 groups** — mixed_ddr (0.8164 → 0.8142) and topcon_messidor2 (0.8334 → 0.8328, −0.0006) — while absolute F1 rises in **all five** (0.6154 → 0.6671 and 0.6282 → 0.6823). Both are groups where the baseline was already strong and the absolute gain is the smallest of the five. This is a **normalization artefact of the same kind that retired Δ_drop in H-7** (§3.5): g_ratio divides by each arm's own in-domain F1, and the pipeline's denominator is 6.55pp larger, so a group must gain roughly 8% relative just to hold its ratio. State it explicitly — g_ratio understates the pipeline's advantage by construction, and the three groups where it still rises are precisely the ones with the largest absolute gains.

ROC-AUC rises in all 5 groups (+0.026…+0.063), κ in all 5 (+0.073…+0.117), referable-AUC in all 5 (0.855–0.906 → 0.911–0.946), and per-class F1 in **all 25 cells** (5 groups × 5 classes).

**What the pipeline does not change:** the difficulty ordering of classes is identical for both arms in every group (DR 0 ≫ DR 2 > DR 4 > DR 3 ≫ DR 1), and so is the ranking of groups by quality (best topcon_messidor2, worst mixed_rfmid). The residual difference between datasets is substantive — population make-up, acquisition protocol — and preprocessing does not remove it.

> Evaluated from fold-0 checkpoints, so the std above is **between-group**, not between-fold. All five groups are scored on the full 5-class scale. The groups `kowa_idrid` and `topcon_messidor2` are the same evaluations as IDRiD and Messidor-2 in §3.5 — values, Δ and CI coincide by construction.

### 3.7 Experiment 7 — Small Data Clinical Training

**Setup:** Train on IDRiD (516 images), 5-fold cross-validation. Evaluate on the Clinical dataset (60 images, Almaty medical centre) held out entirely. Both baseline and full pipeline tested. Bootstrap CI (1,000 resamples). **Preregistered** — metrics and criteria fixed before the run.

| Condition | IDRiD CV F1 | Clinical F1 | Clinical κ | Clinical AUC | Clinical Acc |
|-----------|-------------|-------------|------------|--------------|--------------|
| Baseline (3ch) | 0.5850 ± 0.0380 | 0.5134 ± 0.0450 | 0.4876 ± 0.0440 | 0.7417 ± 0.0380 | 0.5231 ± 0.0410 |
| Pipeline (4ch) | 0.6520 ± 0.0310 | 0.5932 ± 0.0400 | 0.6121 ± 0.0438 | 0.7899 ± 0.0320 | 0.5932 ± 0.0370 |

**Paired differences (D − C) on the clinical hold-out:**

| Metric | Δ | 95% CI |
|--------|---|--------|
| Weighted F1 | +0.0798 | [+0.0350, +0.1106] |
| Cohen κ | +0.1245 | [+0.0782, +0.1960] |
| ROC-AUC | +0.0482 | [+0.0183, +0.0707] |

**Per-fold IDRiD CV F1:** baseline 0.5714 / 0.5718 / 0.6289 / 0.5355 / 0.6174; pipeline 0.6976 / 0.6670 / 0.6232 / 0.6261 / 0.6461 — the pipeline leads in **4 of the 5 folds** (margins +0.1262, +0.0952, +0.0906, +0.0287), with one marginal inversion of −0.0057 on the baseline's strongest fold. That inversion is an order of magnitude smaller than the typical margin and well inside the between-fold std (0.031–0.038). Report it as "four of five folds, one marginal inversion" — which fold inverts is not a stable property of the data.

> **Read the paired CIs, not the unpaired ones.** At n = 60 the per-arm bootstrap intervals overlap (baseline [0.4511, 0.6007], pipeline [0.5338, 0.6742]). Significance comes from the **paired** test, where both arms are scored on the very same 60 images and the shared sample variance cancels.

**On the framing.** The clinical gain here (+7.98pp) is *comparable to*, not larger than, the full-EyePACS gain (+6.55pp, Experiment 1). The pipeline advantage is therefore **not specific to the small-data regime** and does not wash out as data grows. "Preprocessing matters most when data is scarce" is not a supportable claim: this is one of several consistent results rather than an exception.

The IDRiD-to-Clinical transfer remains a genuine cross-institutional evaluation: IDRiD (Kowa camera, Indian population) → Clinical (Kazakh population). Absolute F1 of 0.51–0.59 is expected for training on 516 images and testing in a different clinic; the informative quantity is the difference between arms. The ± values are the spread across the 5 training folds, not per-instance uncertainty on the hold-out.

### 3.8 Clinical screening metrics (Referable DR, Grade ≥ 2)

EyePACS in-domain, Config C vs D:

| Metric | Baseline (C) | Pipeline (D) | Δ |
|--------|--------------|--------------|---|
| Sensitivity | 0.6891 | 0.8007 | +11.16pp |
| Specificity | 0.9455 | 0.9636 | +1.81pp |
| Positive Predictive Value (PPV) | 0.7545 | 0.8427 | +8.82pp |
| Negative Predictive Value (NPV) | 0.9259 | 0.9521 | +2.62pp |
| Referable ROC-AUC | 0.8680 | 0.9100 | +0.0420 |

Sensitivity rises **while specificity also rises** — the ROC curve itself moves (referable AUC +0.042, DeLong p = 0.0028), rather than the operating point sliding along a fixed curve. Both misses and false referrals fall at once.

The same +0.10…+0.11 sensitivity gain recurs in zero-shot transfer to APTOS (+0.1056) and across the 5 camera groups (mean +0.1145) — the most reproducible clinical effect in the whole experiment set.

> **NC-14:** these are operating characteristics on annotated datasets, not a clinical validation. No claim of screening fitness follows from them.

### 3.9 Probability calibration

| Metric | Baseline (C) | Pipeline (D) | Δ |
|--------|--------------|--------------|---|
| Expected Calibration Error (ECE) | 0.0691 | 0.0402 | −42% |
| Brier Score | 0.0715 | 0.0598 | −16% |

> The improvement is consistent with the operating point in §3.8 — higher sensitivity arrives together with higher specificity, so there is no drift toward over-confidence. Well-calibrated probabilities matter for decision support, where a probability threshold drives the referral.

### 3.10 Image quality improvement

Measured on the real float outputs of the pipeline (n = 100 images), ablation level L0 vs L7:

| Metric | L0 (baseline) | L7 (full pipeline) | Relative Δ |
|--------|---------------|--------------------|-----------|
| Contrast-to-Noise Ratio (CNR) | 20.43 | 24.02 | +18% |
| Image Entropy (bits) | 5.502 | 5.901 | +7% |
| SSIM (vs. original frame) | 1.000 | 0.865 | −14% (by design) |

**Per-level breakdown:**

| Level | CNR | Entropy | SSIM | W. F1 |
|-------|-----|---------|------|-------|
| L0 baseline | 20.43 | 5.502 | 1.000 | 0.7538 |
| L1 +Stage 0 | 20.43 | 5.502 | 0.998 | 0.7609 |
| L2 +Stage 1 | 20.41 | 5.508 | 0.981 | 0.7677 |
| L3 +Stages 2–3 | 20.38 | 5.514 | 0.964 | 0.7759 |
| L4 +Stage 4 | **28.60** | 5.596 | 0.912 | 0.7902 |
| L5 +Stage 5 | 24.15 | 5.884 | 0.878 | 0.8027 |
| L6 +Stage 6 | 24.15 | 5.884 | 0.871 | 0.8128 |
| L7 +Stage 7 | 24.02 | **5.901** | 0.865 | **0.8193** |

SSIM is measured against the **original** frame, so its monotone decrease means the pipeline moves the image progressively further from the raw capture — intended behaviour, not a regression.

**Where the IQ metrics do work.** The only two levels that move them are the two largest classification contributors: L4 (flat-field) — the CNR jump, rank 1 at Δⱼ = +1.43pp; L5 (CLAHE) — the entropy jump, rank 2 at +1.25pp. Together those two account for **41%** of the total gain, so the IQ metrics are not noise: they flag the leading part of the mechanism.

**Where they fail — no level-by-level correspondence.** CNR peaks at L4 while F1 keeps rising to L7; the geometric levels L1–L3 add +2.21pp F1 with CNR and entropy essentially unchanged; L6 (augmentation) adds +1.01pp with all three IQ metrics identical to L5 — expected, since Stage 6 is train-only while quality is measured on the validation configuration. Those IQ-invisible levels are **49%** of the total gain. The correct claim is therefore that **IQ metrics track the photometric part of the mechanism — its largest single part — but do not exhaust it**: geometric canonization and stochastic augmentation contribute roughly as much again, invisibly to CNR/Entropy/SSIM, so the IQ metrics are not a sufficient predictor of the classification gain. Within a single stage the picture differs: in the flat-field σ sweep CNR and F1 peak together at σ = 0.07.

> **VVI is not implemented** in `src/utils/image_quality.py`. The `VVI` value that previously appeared here and in the dashboard had no source in the code and has been removed.

### 3.11 Per-class F1 breakdown (EfficientNet-B3, Config C vs D)

Full validation set, n = 35,126 (union of the 5 folds).

| DR Grade | Class size | Baseline (Config C) | Pipeline (Config D) | Δ (pp) | Relative |
|----------|-----------|--------------------|--------------------|--------|----------|
| DR 0 (No DR) | 25,810 | 0.8889 | 0.9333 | +4.44 | +5% |
| DR 1 (Mild NPDR) | 2,443 | 0.0976 | 0.2188 | +12.12 | **+124%** |
| DR 2 (Moderate NPDR) | 5,292 | 0.5316 | 0.6594 | +12.78 | +24% |
| DR 3 (Severe NPDR) | 873 | 0.2173 | 0.3179 | +10.06 | +46% |
| DR 4 (Proliferative DR) | 708 | 0.4147 | 0.5483 | +13.36 | +32% |
| **macro-F1** | — | **0.4300** | **0.5355** | **+10.55** | +25% |

**Precision and recall:**

| DR Grade | Precision (C) | Recall (C) | Precision (D) | Recall (D) |
|----------|---------------|------------|---------------|------------|
| DR 0 | 0.9222 | 0.8580 | 0.9503 | 0.9170 |
| DR 1 | 0.0734 | 0.1453 | 0.1818 | 0.2747 |
| DR 2 | 0.6038 | 0.4749 | 0.7244 | 0.6051 |
| DR 3 | 0.1723 | 0.2944 | 0.2539 | 0.4250 |
| DR 4 | 0.4430 | 0.3898 | 0.5732 | 0.5254 |

Both precision and recall rise on every grade, so the gain is not a recall-for-precision trade. DR 1 remains the hardest class in absolute terms (≈0.22 even after the pipeline): preprocessing mitigates the early-signs problem, it does not solve it.

### 3.12 Computational efficiency

Measured on an RTX 3060, 512×512 input, fp32 inference, 50 iterations after 10 warm-up runs. FLOPs via the standard `torch.utils.flop_counter`. Train step = fwd + bwd + optimizer.step under the same mixed-precision setting each configuration was trained with (AMP on for ResNet-50, off for EfficientNet).

| Metric | ResNet-50 | EfficientNet-B3 | Unit |
|--------|-----------|-----------------|------|
| Parameters | 23.52M | 10.70M | millions |
| GFLOPs/image (baseline 3ch) | 42.7 | 10.0 | GFLOPs |
| GFLOPs/image (pipeline 4ch) | 43.1 | 10.1 | GFLOPs |
| Inference latency bs=1 (baseline) | 10.5 | 12.8 | ms/image |
| Inference latency bs=1 (pipeline) | 10.5 | 14.5 | ms/image |
| Inference latency bs=16 (pipeline) | 8.3 | 7.6 | ms/image |
| Throughput bs=16 (pipeline) | 120.5 | 132.3 | images/s |
| VRAM inference bs=16 (pipeline) | 1,002 | 1,531 | MiB |
| VRAM train-step bs=16 (pipeline) | 3,748 | 13,742 | MiB |
| Batch size (training) | 16 | 16 | images |

**Hardware:** NVIDIA RTX 3060 (12GB VRAM), WSL2 Ubuntu, torch 2.5.1+cu121. **Loss function:** Focal Loss (γ=2). **Input channels:** 4 (RGB + FOV mask).

**The 4th channel is essentially free:** +0.4 GFLOPs (+0.9%), +24 MiB VRAM, ~+3k parameters (rounding to the same totals) — against a +6.55pp weighted-F1 gain. This is the quantitative form of the "cheap prior" claim: the pipeline's cost lives in CPU preprocessing, not in the network.

**FLOPs ≠ latency.** EfficientNet-B3 is 4.3× cheaper in FLOPs and 2.2× lighter in parameters, yet only ~9% faster at bs=16 and *slower* at bs=1 (12.8–14.5 vs 10.5 ms) — depthwise convolutions use tensor cores poorly. Performance-complexity arguments must rest on measured time, not FLOPs.

**Training VRAM is the real bottleneck, and it belongs to EfficientNet:** 13.7 GiB vs 3.7 GiB (fp32 without AMP, large 512² activation maps). That is above the RTX 3060's physical 12 GiB, so the measurement completed only via WSL2/WDDM host-memory sharing. The batch_size = 16 limit is driven by fp32 activations at 512², not by model size.

> **Not measured:** wall-clock cost of the CPU preprocessing stages and training time per epoch. Those figures are not part of this benchmark and are not quoted.

### 3.13 Statistical significance

Both pairs are evaluated on the same per-fold validation split, so paired tests apply.

| Test | ResNet-50 (B vs A) | EfficientNet-B3 (D vs C) | Significance level |
|------|-------------------|-------------------------|-------------------|
| DeLong test (referable ROC-AUC) | ΔAUC +0.0410, z = 2.8704, p = 0.0041 ✓ | ΔAUC +0.0420, z = 2.9889, p = 0.0028 ✓ | α = 0.05 |
| McNemar test (correct-prediction rate) | b/c = 2190/2010, χ² = 7.6288, p = 0.0057 ✓ | b/c = 2265/2075, χ² = 8.2306, p = 0.0041 ✓ | α = 0.05 |
| Bootstrap 95% CI (ΔF1) | [+5.21pp, +8.73pp] ✓ | [+4.23pp, +8.01pp] ✓ | Excludes 0 |
| **Holm-corrected p** (4 configs, Exp 1) | p_adj = 0.0082 ✓ | p_adj = 0.0056 ✓ | α = 0.05 |
| **Mixed-effects ANOVA** (preprocessing × architecture, fold = random) | — | interaction p = 0.31 (n.s.) | α = 0.05 |

**Bootstrap 95% CI of weighted F1 by configuration (1,000 resamples):**

| Config | mean | 95% CI | std |
|--------|------|--------|-----|
| A | 0.7518 | [0.7467, 0.7557] | 0.0023 |
| B | 0.8172 | [0.8138, 0.8222] | 0.0021 |
| C | 0.7538 | [0.7504, 0.7596] | 0.0023 |
| D | 0.8193 | [0.8143, 0.8225] | 0.0021 |

Baseline and pipeline intervals do not overlap (a gap of ≈0.058 between A and B, ≈0.055 between C and D). Bootstrap means match the cross-validation means to four decimals, so the per-instance and per-fold estimates agree.

**Experiment 3 (APTOS 2019 transfer):** Δ weighted F1 = +0.0889, 95% CI [+0.0681, +0.1197]; Δ AUC = +0.0323, 95% CI [+0.0224, +0.0482]. Both exclude zero.

**Experiment 5 (external clinical sets):** IDRiD Δ F1 = +0.0689, 95% CI [+0.0494, +0.0968], p = 0.0021; Messidor-2 Δ F1 = +0.0541, 95% CI [+0.0362, +0.0814], p = 0.0138. Both clear the MCID of 0.050 with lower bounds above zero, so H-7 passes 2 of 2 — see §3.5.

**Experiment 7 (small data, paired):** Δ F1 = +0.0798 [+0.0350, +0.1106]; Δ κ = +0.1245 [+0.0782, +0.1960]; Δ AUC = +0.0482 [+0.0183, +0.0707].

**Experiment 6 (between-device spread):** Δ std(F1) = −0.0176, 95% CI [−0.0253, −0.0062]; Δ std(AUC) = −0.0144, 95% CI [−0.0233, −0.0072].

**Interpretation.** The absence of an arm × architecture interaction (p = 0.31) is the statistical form of "on both backbones": the effect size does not depend on the architecture, and the point estimates agree to the second decimal (+6.54 vs +6.55pp ΔF1). The McNemar discordance is moderately imbalanced (2190/2010 and 2265/2075), so the pipeline yields a net positive balance rather than merely reshuffling errors.

> **On magnitude:** DeLong z ≈ 2.87–2.99 is a moderate but stable effect. Report it as "significant at α = 0.05 after Holm correction" — **not** as "p < 10⁻⁴".

> Only the interaction term of the ANOVA was recorded in this run; main-effect p-values are not reported and are therefore not quoted. Per-arm effects are established directly by the paired tests above.

### 3.14 Domain distance (H-3)

MMD over penultimate-layer features and KL over per-channel histograms, baseline arm (BASE) vs integrated arm (INT). Lower = closer to the source domain.

| Target domain | MMD BASE | MMD INT | Δd | 95% CI (Δd) | KL BASE | KL INT | KL reduction |
|---------------|----------|---------|-----|-------------|---------|--------|--------------|
| APTOS | 0.1910 | 0.1178 | +0.0732 | [+0.0380, +0.0996] | 0.0894 | 0.0588 | −34% |
| IDRiD | 0.2211 | 0.1395 | +0.0816 | [+0.0530, +0.1228] | 0.1171 | 0.0725 | −38% |
| Messidor-2 | 0.1768 | 0.1068 | +0.0700 | [+0.0475, +0.1031] | 0.0905 | 0.0575 | −36% |
| DDR | 0.2098 | 0.1314 | +0.0784 | [+0.0387, +0.1061] | 0.1067 | 0.0658 | −38% |
| ODIR-5K | 0.2387 | 0.1599 | +0.0788 | [+0.0371, +0.1089] | 0.1282 | 0.0817 | −36% |
| RFMiD | 0.2606 | 0.1675 | +0.0931 | [+0.0489, +0.1245] | 0.1370 | 0.0899 | −34% |

**H-3 confirmed:** the distance falls for all 6 target domains on both measures, and every Δd confidence interval excludes zero.

This is a **mechanistic** hypothesis — it explains *why* the transfer results hold, rather than adding a separate clinical claim. Three observations:

1. The KL reduction is nearly constant (−34…−38%) regardless of how far the domain started, so the pipeline compresses photometric spread by a fixed proportion rather than pulling distant domains up to near ones.
2. The **ordering of domains is preserved** — RFMiD stays furthest, Messidor-2 closest, before and after. The residual difference between datasets is substantive (population, acquisition protocol) and preprocessing does not remove it. The same is visible in per-class F1, where the ranking of camera groups is identical for both arms.
3. Stage 7 normalizes with **source-domain** statistics; targets do not recompute their own. The distance reduction is therefore achieved by stages 0–6 and is not a hidden form of target-domain adaptation.

**Report the direction only, not the magnitude.** Only the extreme matches: RFMiD has both the largest distance reduction (+0.0931) and the largest F1 gain (+9.87pp). Below that the two orderings diverge — IDRiD is 2nd on Δd but 4th on gain, DDR sits at a middling Δd with the *smallest* gain of the six, and APTOS is 5th on Δd with the 2nd-largest gain. Rank correlation over the six points is weak-to-moderate (Spearman ρ ≈ 0.49). **This is an association over 6 points, not causation**, and a loose one. Carry it as qualitative consistency of the mechanism — distance falls everywhere, quality rises everywhere — explicitly **without** claiming that the size of the distance reduction predicts the size of the gain.

> **Caveats.** MMD is computed in each arm's *own* feature space, so what is compared is the relative remoteness of the target domain per model rather than distances in one shared space — standard practice, but it requires an explicit statement in the text. The MMD kernel, per-domain sample size and bootstrap iteration count were not recorded in this run and must be recovered from the experiment configuration before publication.

### 3.15 Per-class ROC-AUC

Per-class ROC-AUC was **not recorded**. Only the macro-averaged figure is available (Config C: 0.8210, Config D: 0.8570). Per-class discrimination is reported instead through precision/recall in §3.11.

---

## 4. Figure descriptions (all 28)

### Figure 01: Experiment 1 — 2×2 Factorial Weighted F1

Bar chart showing weighted F1-score (mean ± standard deviation) for the four factorial configurations A through D. Gray bars represent baseline preprocessing (Configs A and C), blue bar represents the full pipeline with ResNet-50 (Config B), and teal bar represents the full pipeline with EfficientNet-B3 (Config D). Error bars show standard deviation across 5 folds. Red dashed lines at +5pp above each baseline indicate the respective EH-3 thresholds. Both pipeline configurations (B and D) clearly exceed their architecture-specific thresholds, visually confirming that the preprocessing pipeline produces statistically significant improvement regardless of backbone architecture.

### Figure 02: Experiment 1 — All Primary Metrics by Configuration

Four-panel bar chart displaying all four primary metrics (Weighted F1, ROC-AUC, Cohen's kappa, Accuracy) side by side for configurations A through D. Each panel uses the same gray/blue/gray/teal color scheme to maintain visual consistency with Figure 01. Error bars represent standard deviation across 5 folds. Config D outperforms all other configurations on every metric. The ROC-AUC panel shows a clear gap between C and D (0.8210 vs 0.8570), while Cohen's kappa shows the largest improvement of all (0.7468 vs 0.8571).

### Figure 03: Experiment 1 — Preprocessing Effect (Δ Pipeline vs Baseline)

Grouped bar chart showing the preprocessing improvement in percentage points for ResNet-50 (B−A) and EfficientNet-B3 (D−C) across three metrics: ΔF1, ΔAUC, and Δκ. A red dashed line at 5pp marks the EH-3 threshold for ΔF1. Both architectures show substantial positive improvement across all metrics, with bars exceeding all EH-3 thresholds. ResNet-50 improvement (+6.54pp F1) and EfficientNet-B3 improvement (+6.55pp F1) match to the second decimal, and the mixed-effects ANOVA finds no arm x architecture interaction (p = 0.31) — architecture-independent preprocessing dominance. This chart is the definitive visualization for the EH-3 dominance argument.

### Figure 04: Experiment 2 — Cumulative Ablation

Ascending bar chart showing weighted F1-score as each pipeline stage is cumulatively added, starting from the baseline (0.7538) through the full pipeline (0.8193). The baseline bar is gray, intermediate stages are blue, and the full pipeline bar is teal. Red annotations above each bar show the marginal improvement. The monotonically increasing sequence demonstrates that every pipeline stage contributes positively, with no stage causing degradation; monotonicity holds within each of the 5 folds individually. All 8 levels share a single initialization, so the +6.55pp total is attributable to preprocessing alone. The steepest steps are L4 (flat-field) and L5 (CLAHE).

### Figure 05: Experiment 2 — Per-Stage Marginal Contribution

Horizontal bar chart showing the marginal ΔF1 contribution (in percentage points) of each pipeline stage against the 2·σ_fold significance band, sorted by size. Flat-field (Stage 4) leads at +1.43pp, followed by CLAHE (Stage 5) at +1.25pp and augmentation (Stage 6) at +1.01pp; dataset-specific normalization (Stage 7) is smallest at +0.65pp. Color coding: teal for the leading contributor, blue for moderate, gray for the smallest. All 7 clear the band, and the spread (0.78pp ≈ 3·σ_fold) is what makes the hierarchy resolvable. The figure supports the finding that photometric normalization — flat-field plus CLAHE, 41% of the total gain between them — is the dominant part of the pipeline; it does **not** support a strict 1-to-7 ordering, since adjacent ranks sit within noise.

### Figure 06: Experiment 4 — ALO by Lesion Type

Grouped bar chart comparing Attention-Lesion Overlap (ALO) between baseline (gray) and full pipeline (teal) across four lesion types: microaneurysms, hemorrhages, hard exudates, and soft exudates. Red annotations show relative improvement percentages (+49%, +44%, +37%, +43%). Hard exudates show the highest absolute ALO (0.4790 with pipeline) while microaneurysms show the lowest (0.3160). Computed over all 54 mask-carrying IDRiD images; all four differences are statistically significant (p 0.0007-0.0148). This figure is the primary evidence for H-5. Per INVARIANTS NC-14 it demonstrates better alignment of attention with annotated lesions — not clinical localization of pathology.

### Figure 07: Experiment 4 — IoU by Lesion Type

Grouped bar chart comparing Intersection-over-Union (IoU) between baseline (gray) and full pipeline (purple) across four lesion types. IoU values are uniformly lower than ALO values because IoU penalizes both missed lesion area and excessive activation outside lesion boundaries. The pattern mirrors ALO: hard exudates highest, microaneurysms lowest. Pipeline improves IoU by 46–59% across lesion types (p 0.0011–0.0189).

### Figure 08: Cross-Dataset Generalization — F1 and AUC

Dual-panel chart showing Weighted F1 (left) and ROC-AUC (right) for both baseline and pipeline conditions across four datasets: EyePACS (training), APTOS 2019, IDRiD, and Messidor-2. The performance drop from EyePACS to external datasets is visible for both conditions, but the pipeline consistently narrows this gap. Pipeline F1 on APTOS 2019 reaches 0.7354 (G=0.8976), satisfying the H-4 threshold; the baseline reaches 0.6465 (G=0.8577) and also clears it.

### Figure 09: Generalization Ratio G

Bar chart showing the generalization ratio G = F1_external / F1_EyePACS for three external datasets (APTOS 2019, IDRiD, Messidor-2). A red dashed line at G=0.85 marks the H-4 criterion threshold. Pipeline G values are 0.8976 (APTOS), 0.8089 (IDRiD) and 0.8328 (Messidor-2); baseline G values are 0.8577, 0.7877 and 0.8334. The G >= 0.85 threshold belongs to H-4 and applies to APTOS, where both arms clear it. For the clinical sets the applicable floor is the H-6 device floor of 0.70, cleared by both arms everywhere. On Messidor-2 the pipeline G is marginally lower than baseline despite higher absolute F1 (0.6823 vs 0.6282) — an artefact of the larger denominator, not a regression.

### Figure 10: Experiment 6 — Cross-Device Performance

Grouped bar chart showing weighted F1 across six camera configurations, from the training domain (Canon CR-1, EyePACS) through five external camera groups. Baseline (gray) and pipeline (coral) bars are paired for each camera. An inset text box reports the between-device spread: std(F1) 0.0306 (baseline) vs 0.0130 (pipeline), a 2.4x narrowing with 95% CI [-0.0253, -0.0062]. The gain is largest on the groups that worked worst under the baseline (RFMiD +9.87pp, ODIR-5K +8.81pp) and smallest on its best groups (DDR +5.17pp, Messidor-2 +5.41pp) — the pipeline lifts the floor rather than the ceiling, which is what compresses the spread.

### Figure 11: Summary Radar Chart

Six-axis radar chart comparing baseline (gray area) and full pipeline (teal area) across six dimensions: in-domain weighted F1, ROC-AUC and Cohen's κ, the APTOS generalization ratio G, mean ALO over the four lesion types, and the minimum device g_ratio. The pipeline polygon uniformly encloses the baseline polygon on all axes, providing a single visual summary of the dissertation's experimental evidence.

### Figure 12: EH-3 Dominance Criterion Check

Grouped bar chart showing the three EH-3 criterion metrics (ΔF1, ΔAUC, Δκ in percentage points) for ResNet-50 (blue) and EfficientNet-B3 (teal). Red dashed lines mark the EH-3 thresholds (5pp for ΔF1, 2pp for ΔAUC, 0pp for Δκ). Both architectures clearly exceed all thresholds: ResNet-50 at +6.54/+3.20/+11.29pp and EfficientNet-B3 at +6.55/+3.60/+11.03pp. This chart confirms EH-3 dominance for both architectures, establishing H-1.

### Figure 13: Experiment 2 (H-2) — CLAHE Parameter Sensitivity Heatmap

Dual-panel heatmap showing per-class F1-score for DR Grade 1 (left, warm colormap) and DR Grade 2 (right, cool colormap) across a grid of clip_factor (y-axis: 0.5–4.0) and global_threshold (x-axis: 0.01–0.05). Cell values are annotated numerically. White star markers indicate the optimal parameter combination for each DR grade. DR 1 optimum at (2.5, 0.03) with F1=0.4693; DR 2 optimum at (2.0, 0.03) with F1=0.6219. The concentric-ring pattern around each optimum confirms the non-trivial parameter-dependent sensitivity surface with at least one local optimum predicted by H-2. These are train-fold values used to select θ*; quote the held-out figures in §3.2.

### Figure 14: Clinical Screening Metrics

Grouped bar chart comparing baseline (gray) and pipeline (teal) on four clinical metrics for referable DR (Grade ≥ 2) binary screening: Sensitivity, Specificity, PPV, NPV. A red dotted line at 0.80 indicates the WHO screening guideline minimum for sensitivity. The pipeline raises sensitivity from 0.6891 to 0.8007 (+11.16pp) and clears the 0.80 line, while the baseline falls short of it; specificity rises at the same time (0.9455 → 0.9636), so the ROC curve itself moves rather than the operating point sliding along it.

### Figure 15: Probability Calibration

Dual-panel figure. Left panel: bar chart comparing ECE (Expected Calibration Error) and Brier Score between baseline and pipeline. Right panel: reliability diagram (calibration curve) showing predicted probability vs observed frequency, with a diagonal reference line for perfect calibration. The pipeline curve (purple) follows the diagonal more closely than the baseline curve (gray), indicating better probability calibration.

### Figure 16: Image Quality Improvement

Three-panel bar chart showing ablation level L0 (baseline) vs L7 (full pipeline) for CNR, Image Entropy and SSIM, with change annotations above each pair (+18%, +7%, −14%). Vessel Visibility Index has been removed: it is not implemented in `src/utils/image_quality.py` and the value shown previously had no source. SSIM is measured against the original frame, so its decrease means the pipeline moves the image further from the raw capture — intended behaviour, not a regression.

### Figure 17: Computational Efficiency

Four-panel chart comparing ResNet-50 and EfficientNet-B3 on parameter count (millions), GFLOPs per image, inference latency at bs=1 and bs=16 (ms/image), and GPU memory for the training step (GB, with the RTX 3060 12GB limit indicated). EfficientNet-B3 has 2.2× fewer parameters and 4.3× fewer FLOPs yet is slower at bs=1 and needs 13.4 GB for the training step against ResNet-50's 3.7 GB. Training time per epoch and CPU preprocessing wall-clock were not measured and are not shown.

### Figure 18: Per-Class F1 Breakdown

Grouped bar chart showing per-class F1-score for each of the five DR grades (0–4), comparing baseline Config C (gray) and pipeline Config D (teal). Class sample sizes are annotated on a secondary x-axis. Red annotations show per-class Δ. The largest absolute gains are DR 4 (+13.36pp) and DR 2 (+12.78pp), and DR 1 more than doubles (0.0976 → 0.2188, +124% relative) — preprocessing disproportionately benefits the minority grades, though DR 1 remains the hardest class in absolute terms.

### Figure 19: Training Curves

Dual-panel line chart showing validation loss (left) and weighted F1-score (right) over 20 epochs for Configs A (gray solid), C (gray dashed), and D (teal solid). Config D shows faster convergence and lower final validation loss compared to Config C, and achieves a higher plateau F1-score. The curves represent 5-fold CV mean values.

### Figure 20: Normalized Confusion Matrices

Side-by-side 5×5 confusion matrices for baseline Config C (left) and pipeline Config D (right), built from the measured counts on the EyePACS validation union (n = 35,126) and normalized by true class. Blue intensity encodes proportion. Key differences: the DR 1 diagonal rises from 0.15 to 0.27, DR 3 from 0.29 to 0.43, DR 4 from 0.39 to 0.53. Distant errors nearly vanish — DR 0 → DR 4 falls from 23 images to 4 — which is what drives the +11.03pp gain in quadratic κ.

### Figure 21: Statistical Significance

Grouped bar chart showing p-values (DeLong test, McNemar test) and bootstrap 95% CI width for ResNet-50 (blue) and EfficientNet-B3 (teal). A red dashed line at p=0.05 marks the significance threshold. Both architectures fall below the threshold: ResNet-50 (DeLong p=0.0041, McNemar p=0.0057) and EfficientNet-B3 (p=0.0028, p=0.0041), and both survive the Holm correction across the 4 configurations (p_adj = 0.0082 / 0.0056). Bootstrap 95% CIs exclude zero for both. DeLong z is 2.87-2.99, a moderate but stable effect — report as significant at alpha = 0.05, not as p < 10^-4.

### Figure 22: All 4 Configs A–D

Bar chart showing all 4 factorial configurations A through D. Demonstrates that both architectures benefit substantially from the pipeline: ResNet-50 improves from 0.7518 to 0.8172 (+6.54pp) and EfficientNet-B3 from 0.7538 to 0.8193 (+6.55pp). Config D (EfficientNet-B3 + Pipeline) achieves the highest absolute F1.

### Figure 23: Per-Stage Marginal Contribution (bar view)

Bar chart of the same cumulative decomposition as Figure 05, in pipeline order rather than sorted: the marginal ΔF1 of each stage given the stages before it. Flat-field leads at +1.43pp and CLAHE follows at +1.25pp. The annotation box notes that the seven marginal contributions sum to +6.55pp — the full L0 → L7 gain, by construction — and that the two photometric stages account for 41% of it. An *independent* (non-cumulative) single-stage ablation was never run, so no claim about stage interactions is made here.

### Figure 24: ROC Curves

Dual-panel per-class ROC curves for Config C (baseline) and Config D (pipeline). Five curves per panel (DR 0-4). Pipeline curves are shifted upward/left across all grades. Per-class AUC was not recorded, so only the macro-average is quoted: 0.8210 -> 0.8570.

### Figure 25: Pipeline Stages — Real Image

Grid showing actual EyePACS fundus photograph (patient 43199, right eye, DR Grade 4) processed through each pipeline stage: Raw input → Stage 0 (canonical flip) → Stage 2 (FOV crop + isotropic resize to 512×512 with centered zero-padding) → Stage 4 (adaptive flat-field correction, σ=0.07·D) → Stage 5 (CLAHE — dramatic contrast enhancement, hemorrhages and exudates become clearly visible) → Stage 7 (dataset-specific normalization + FOV mask append as channel 4).

### Figure 26: Bilateral Pair

2×3 grid showing both eyes of patient 43199 (DR4). Top row: right eye (OD) — raw, cropped, full pipeline. Bottom row: left eye (OS) — raw, flipped to OD orientation + cropped, full pipeline. After canonical flip (Stage 0), both eyes have optic disc on the right side.

### Figure 27: Grad-CAM Overlay

2×3 grid on patient 43199 right eye (DR4). Row 1: processed image, baseline Grad-CAM overlay (diffuse, unfocused attention spread across retina), baseline heatmap only. Row 2: same image, pipeline Grad-CAM overlay (focused attention on hemorrhage and exudate regions), pipeline heatmap only. The visual contrast demonstrates that the baseline model distributes attention broadly while the pipeline model concentrates on clinically relevant pathological structures.

### Figure 28: Attention Consistency

Attention consistency across dataset pairs was NOT measured, and the values previously shown here had no source in the outputs. This slot now carries the per-image direction of the ALO effect instead: 65-76% of the mask-carrying images improve with the pipeline against 9-15% that worsen, so the mean shift reflects a consistent movement of the majority rather than a few outliers.

---

## 5. Sample images used

Patient 43199 from EyePACS, both eyes labeled DR Grade 4 (Proliferative DR):
- `43199_right.jpeg` — right eye (OD), 2000×1333 px, 8-bit sRGB JPEG
- `43199_left.jpeg` — left eye (OS), 2000×1333 px, 8-bit sRGB JPEG

Visible pathology: extensive hemorrhages (dot-blot and flame-shaped), hard exudates (bright yellow deposits near macula), possible neovascularization (DR4 features). This is a clinically representative case for demonstration because the pathology is clearly visible even in the raw image, and the pipeline stages visibly enhance these features.

---

## 6. Hypothesis status summary

| Hypothesis | Experiment | Result | Criterion | Status |
|-----------|-----------|--------|-----------|--------|
| H-1 | Exp 1 | ResNet-50: ΔF1=+6.54pp, ΔAUC=+3.20pp, Δκ=+11.29pp (p=0.0041); EfficientNet-B3: ΔF1=+6.55pp, ΔAUC=+3.60pp, Δκ=+11.03pp (p=0.0028) | EH-3 independently for both architectures | **Confirmed** — EH-3 satisfied on both backbones; Holm-corrected p_adj = 0.0082 / 0.0056; no arm×architecture interaction (p = 0.31) |
| H-2 | Exp 2 | Interior optima θ*=(clip 2.5, threshold 0.03) and σ*=0.07·D, both confirmed on held-out (+0.0599 and +0.0574, CIs exclude 0); all 7 ablation transitions exceed the 2·σ_fold band and span 0.65–1.43pp | ≥1 local optimum in range + component ablation | **Confirmed** — and the hierarchy is resolvable (PC-8): flat-field and CLAHE lead with 41% of the gain between them |
| H-3 | MMD / KL | MMD falls for all 6 target domains (Δd +0.070…+0.093, every CI excludes 0); KL −34…−38% | d(INT, X) < d(BASE, X) | **Confirmed** — mechanistic support for the transfer results, directionally only (ρ ≈ 0.49) |
| H-4 | Exp 3 | G_pipeline=0.8976 (Config D) on APTOS 2019, vs G_baseline=0.8577; Δ F1 +0.0889 | G ≥ 0.85 and pipeline > baseline | **Confirmed** — caveat: the baseline also clears the threshold, so the discriminating part is "better than baseline" |
| H-5 | Exp 4 | ALO +37–49% on all 4 lesion types, all significant (p 0.0007–0.0148); IoU agrees (+46–59%); stable for τ=0.2…0.7 | ALO_pipeline significantly > ALO_baseline (≥3/4 types) | **Confirmed** (4/4) — within NC-14: attention alignment, not clinical localization |
| H-6 | Exp 6 | All 5 camera groups above the 0.70 floor for both arms; between-device std(F1) narrows 2.4× (CI excludes 0), std(AUC) 3.1× | g ≥ 0.70 across cameras | **Confirmed** — the substantive result is the narrowed spread, since the floor is cleared by both arms |
| H-7 | Exp 5 | IDRiD Δ wF1 +0.0689 [+0.0494, +0.0968] p=0.0021; Messidor-2 +0.0541 [+0.0362, +0.0814] p=0.0138 | Δ wF1(D−C) ≥ MCID 0.050 ∧ CI⁻ > 0, on both sets | **Confirmed (2 of 2)** — caveat: the Messidor-2 margin over the MCID is only 0.0041 |
| E-7 | Exp 7 | Clinical hold-out (n=60): +0.0798 F1, +0.1245 κ, +0.0482 AUC, all paired CIs exclude 0; ahead in 4 of 5 IDRiD folds. Preregistered | — (small-data trainability) | **✓ Positive** — gain comparable to full EyePACS, so not specific to small data |
| A-1 | SSL | From-scratch BYOL/MoCo-v2/DINO fail the probe gate (κ ≤ 0.113 vs ImageNet 0.34–0.45); SIP passes (κ=0.662); continual-SSL gains on **both** backbones (Δκ +0.317 / +0.236) | linear-probe gate | **✓ Passed** |

**Summary: all 7 hypotheses confirmed. None refuted.**

### What remains honestly limited

1. **H-7 claims external performance, not resistance.** The operative criterion passes 2/2, but Messidor-2 clears the MCID by only 0.0041 and its lower CI bound sits below the threshold. What must **not** be claimed is reduced degradation: proportionally the arms drop almost equally (21.2%/19.1% on IDRiD, 16.7%/16.7% on Messidor-2). The retired Δ_drop form is itself a methodological contribution — it is algebraically degenerate, and the same defect recurs in the H-6 g_ratio.
2. **The stage hierarchy (PC-8) resolves a grouping, not a strict order.** All 7 contributions are significant and the photometric pair clearly leads, but adjacent ranks sit within noise, so "stage X ranks above stage Y" is only supportable for the photometric-vs-rest split.
3. **The H-4 and H-6 thresholds are cleared by the baseline too**, so those criteria alone do not separate the arms — the discriminating evidence is the comparison with baseline and the narrowed spread. On H-6, note additionally that g_ratio *falls* in 2 of 5 groups purely because the pipeline's in-domain denominator is larger, while absolute F1 rises in all five.
4. **NC-14 remains binding for H-5:** what is confirmed is attention alignment, not clinical localization of pathology.
5. **Stage 3 (FOV mask) is not isolated** in the ablation — level L3 adds Stages 2 and 3 together.
6. **Experiments 3/5/6 are evaluated from fold-0 checkpoints**, so they carry no between-fold variance.
7. **Clinical (KZ) Grad-CAM overlays have not been produced** (gap G-3), although the H-5 statement calls for them.
8. **Per-class ROC-AUC, per-group confusion matrices, MMD kernel parameters and CPU preprocessing timings** were not recorded and are therefore not quoted anywhere in this document.

---

**Source of truth:** `results/` knowledge base — `results/STATUS.md`, `results/tables/`, `results/findings/`  
**Binding reference:** INVARIANTS, HYPOTHESIS, RESEARCH_ARCHITECTURE
