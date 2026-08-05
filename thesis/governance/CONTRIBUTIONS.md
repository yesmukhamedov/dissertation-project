# CONTRIBUTIONS.md

## Scientific Contributions of the Dissertation

**Candidate:** Yesmukhamedov N.S.
**Document Type:** Formal contributions register
**Version:** 7.1.0 | **Date:** 2026-08-05 | **Binding Reference:** INVARIANTS.md v7.0.0

**v7.1.0 Amendment:** **SC-I (Direct Measurement of Domain-Shift Reduction) is added**, in step with the restoration of H-3 and the addition of PC-11. The contribution is that the dissertation measures the postulated mechanism directly — source-to-target distance in feature space, six corpora, forward passes only — rather than inferring it from external accuracy, and does so under a source-domain-statistics condition that keeps the measurement a property of the preprocessing rather than of a fitting procedure. Bounded: it establishes *that* the mechanism operates, never that the size of the reduction predicts the size of any gain. No existing contribution is altered.

**v7.0.0 Amendment:** SC-G is reframed in step with the H-7 reformulation (INVARIANTS v7.0.0) — from *Clinical Degradation Resistance* to *External Clinical Performance*. A secondary methodological contribution is added under SC-G: the analytic identification of the Δ_drop defect. No other contribution is affected.

**v6.2.0 Amendment:** SC-H is refined with the now-locked operational specifics of the integrated-arm initialization (no contribution added or removed): the fundus-SSL corpus is the unlabeled EyePACS "test" split (53,576 images, disjoint from the ~35,126 Experiment-1 corpus per INVARIANTS SB-2.4); the primary protocol is BYOL pretrained from-scratch on the 4-channel tensor; and the initialization must pass a linear-probe acceptance gate (beat random init, competitive with ImageNet) before entering Experiment 1. CFC-2.8 and the composite-IV boundary are unchanged.

**v6.0.0 Amendment:** The integrated-arm pretraining source is changed from the RETFound foundation model to **ophthalmology-specific self-supervised pretraining** of the existing CNN backbone (see SC-H). The composite *(preprocessing × pretraining)* independent variable and CFC-2.8 are retained, so the SSL initialization is reported as part of the integrated configuration, not as an independently attributable contribution.

---

## Conceptual Framing of the Primary Contributions

The principal conceptual contribution of this dissertation is a **paradigm shift** — from paradigm P1 (the end-to-end CNN paradigm, in which preprocessing is treated as ancillary data preparation; Gulshan et al. 2016 is its canonical representative) to paradigm P2 (the integrated preprocessing-CNN paradigm, in which preprocessing is an integral model component that co-determines the feature space available to the network). The four primary contributions (C-1 through C-3) and the supporting contributions (SC-A through SC-G) operationalise P2: each is, at one level, an engineering result on the 8-stage pipeline and, at a second level, evidence for the productivity of P2 as a methodological stance. The contributions therefore have a dual character — engineering and conceptual — and the dissertation reports them under both readings, in line with SB-1.12, CFC-2.8, CFC-2.9, and SIR-9 in INVARIANTS v5.3.

---

## Primary Contributions

### C-1: Integrated Preprocessing-CNN Pipeline (Operationalisation of Paradigm P2)

**Contribution:** Design, implementation, and experimental validation of an 8-stage fundus image preprocessing pipeline that standardizes retinal image appearance across diverse imaging devices and acquisition conditions while preserving diagnostically relevant retinal features. The pipeline outputs 4-channel tensors (RGB + binary FOV mask) with dataset-specific normalization. At the **conceptual** level, the contribution is the formalisation of preprocessing as a binding part of the model specification — the operationalisation of paradigm P2 — and the explicit placement of this paradigm under controlled experimental contrast against the paradigm represented by Gulshan et al. (2016) and the broader P1 literature. At the **engineering** level, the contribution is the specific 8-stage realisation enumerated below.

**Evidence:** Experiment 1 (preprocessing dominance via 2×2 factorial ablation A–D, ResNet-50 and EfficientNet-B3), Experiment 2 (component-level ablation across 7 levels + CLAHE sweep + flat-field σ sweep), and Experiment 6 (device domain shift evaluation across Canon, Topcon, Kowa, Zeiss camera hardware).

**Novelty:** Novelty is twofold.
- *Conceptual:* The dissertation reframes preprocessing as an integral model component (paradigm P2) and places this reframing under direct empirical test, in contrast to the P1 tradition (Gulshan, Pratt, Rakhlin, Saxena, Ting, Voets) in which preprocessing is unformalised in the main text or deferred to supplementary material. Per CFC-2.9, this is a claim about the observable methodological practice of those works, not an attribution to them of an explicit "preprocessing is unimportant" thesis.
- *Engineering:* The pipeline introduces: (a) isotropic resize with centered zero-padding preserving fundus circle geometry, (b) explicit FOV mask as a 4th input channel informing the CNN of valid pixel regions, (c) adaptive flat-field correction with σ proportional to FOV diameter (σ = 0.07·D) rather than a fixed global σ, (d) dataset-specific normalization computed from training set mask=1.0 pixels rather than ImageNet defaults, (e) canonical orientation via OD-fovea rotation normalization with adaptive augmentation σ. The pipeline is validated across a multi-dataset architecture (EyePACS, APTOS 2019, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD, Clinical) and across multiple CNN architectures (ResNet-50, EfficientNet-B3).

---

### C-2: Cross-Dataset Generalization Evidence

**Contribution:** Empirical demonstration that CNN models trained with the preprocessing pipeline on EyePACS generalize to APTOS 2019 without retraining, achieving generalization ratio G ≥ 0.85.

**Evidence:** Experiment 3 (cross-dataset transferability). Generalization ratio G = F1_APTOS / F1_EyePACS computed on zero-shot transfer.

**Novelty:** Systematic cross-dataset transferability evaluation with a pre-registered generalization threshold on an independent 5-class DR dataset from mixed camera sources.

---

### C-3: Lesion Feature Preservation Analysis

**Contribution:** Quantitative demonstration via Grad-CAM explainability analysis that the preprocessing pipeline directs CNN attention toward clinically relevant lesion regions (microaneurysms, hemorrhages, hard exudates, soft exudates), measured by Attention–Lesion Overlap (ALO) as primary metric on IDRiD, with qualitative Grad-CAM overlays on a Kazakh clinical dataset.

**Evidence:** Experiment 4 (explainability analysis with ALO and IoU against IDRiD pixel-level lesion masks; Grad-CAM overlays on Clinical dataset).

**Novelty:** This dissertation introduces ALO as a quantitative, asymmetric metric that directly measures lesion coverage by model attention and systematically compares ALO scores between preprocessed and unprocessed conditions per lesion type. The addition of qualitative clinical validation on Kazakh data extends the analysis beyond benchmark datasets.

---

## Supporting Contributions

### SC-A: Adaptive CLAHE Variant

**Contribution:** Adaptation and validation of a modified CLAHE formulation with dual-constraint clip limit (clip_factor × tile_area/256, capped by global_threshold × tile_area; selected via parameter sweep) in LAB color space for fundus image enhancement. Stochastic application at train time (80% probability) provides additional regularization.

**Evidence:** Experiment 2 (CLAHE threshold sensitivity on EyePACS).

---

### SC-B: CLAHE Sensitivity Characterization

**Contribution:** Identification and characterization of the CLAHE clip limit sensitivity profile for DR classification, demonstrating that per-class F1-score (particularly for DR 1 and DR 2) exhibits a non-trivial parameter-dependent sensitivity curve with an identifiable local optimum.

**Evidence:** Experiment 2 (parameter sweep on EyePACS).

---

### SC-C: Cross-Device Robustness Evaluation

**Contribution:** Systematic evaluation of preprocessing pipeline robustness across four fundus camera manufacturers (Canon, Topcon, Kowa, Zeiss) using five datasets with documented camera metadata, producing a cross-device performance matrix. DR labels only; non-DR disease labels ignored or mapped.

**Evidence:** Experiment 6 (device domain shift evaluation on DDR, ODIR-5K, RFMiD).

---

### SC-D: Adaptive Flat-Field Illumination Normalization

**Contribution:** Design and validation of an adaptive Gaussian blur subtraction stage (corrected = image − GaussianBlur(image, σ) + 128, σ = 0.07 × FOV diameter) for uneven illumination correction in fundus images. The adaptive σ scales with image geometry rather than using a fixed value, and correction is applied only inside the FOV mask to prevent padding artifacts.

**Evidence:** Experiment 2 (component-level ablation + flat-field σ sweep across 0.05–0.10·D). Image quality metrics (CNR, VVI, SSIM) measured before and after Stage 4.

**Novelty:** Adaptive flat-field correction scales with per-image FOV diameter rather than using a global fixed σ, accommodating variability in fundus image size and FOV coverage across imaging devices.

---

### SC-E: FOV Mask as Explicit Pipeline Component

**Contribution:** Explicit generation of a binary FOV mask (1.0 = real fundus data, 0.0 = zero-padding) as a dedicated pipeline stage (Stage 3), appended as the 4th input channel. This informs the CNN of valid pixel regions, preventing the model from learning padding artifacts as features.

**Evidence:** Experiment 1 (full configs B/D use 4-channel input) and Experiment 2 (ablation level including isotropic resize + mask).

---

### SC-F: OD-Fovea Rotation Normalization (Stage 1)

**Contribution:** Design and implementation of classical-CV-based optic disc (OD) and fovea detection for fundus image rotation normalization (Stage 1). The image is rotated so the OD→fovea axis is horizontal. When detection confidence is low, rotation is skipped (fallback). The rotation σ for Stage 6 augmentation is adapted per-image from OD/fovea detection uncertainty (fallback: σ = 13.0°).

**Evidence:** Experiment 2 (component-level ablation, Stage 1 contribution). Implementation: `src/preprocessing/od_fovea_detect.py`, `src/preprocessing/canonical_orientation.py`.

---

### SC-G: External Clinical Performance

**Contribution:** Empirical demonstration that the integrated configuration attains higher absolute performance on external clinical datasets under zero-shot transfer. Δ wF1(X) = wF1(integrated, X) − wF1(baseline, X) is computed on IDRiD and Messidor-2, each required to satisfy Δ ≥ MCID_wF1 = 0.050 with CI⁻ > 0. **The contribution is higher external performance, not reduced degradation.**

**Secondary methodological contribution [v7.0.0]:** identification of a defect in the degradation metric Δ_drop = F1_in-domain − F1_external, in common use in the domain-shift literature. Since Δ_drop(integrated) − Δ_drop(baseline) ≡ Δ_in-domain − Δ_external, the comparison is the fixed in-domain margin minus the quantity under test; it can be satisfied only by an arm whose advantage grows under domain shift and penalizes the stronger arm for its in-domain result. Carried in Chapter 5 §5.4.

**Evidence:** Experiment 5 (external clinical performance, H-7).

---

### SC-I: Direct Measurement of Domain-Shift Reduction [v7.1.0]

**Contribution:** Most work asserting that preprocessing improves cross-domain robustness demonstrates it through its *consequence* — external accuracy — and leaves the postulated mechanism, a reduction in distributional distance, unmeasured. This dissertation measures the mechanism directly. Source-to-target distance is computed at the penultimate layer under both arms across six external corpora, with bootstrap confidence intervals on the paired reduction, at the cost of forward passes only. The contribution is methodological as much as empirical: it supplies the middle term of the dissertation's own causal chain rather than leaving the chain to be inferred from its endpoints, and it makes the mechanistic claim independently falsifiable of the performance claims.

**Design element that gives the measurement its force.** Stage 7 normalization is computed from **source-domain statistics**, never recomputed on the target. Any convergence observed is therefore produced by Stages 0–6 operating identically on every corpus, with no information about the target distribution entering the transform — the measurement is a property of the preprocessing, not of a fitting procedure. Without this condition the result would be a form of target-domain adaptation and would be incomparable with H-4, H-6 and H-7.

**Falsifiability, recorded prospectively.** Stage 5 (CLAHE tuned on the source corpus) and Stage 7 (dataset-specific normalization) are bound to the source domain by construction, so a reversal — variability reduced *within* the source domain while increased *across* domains — was a live possibility. Had it occurred it would have been an established finding rather than a failed run, and would have explained any corresponding reversal in H-4 and H-7. The contribution is therefore not the outcome but the measurement's existence and its capacity to have come out the other way.

**Evidence:** H-3 / PC-11. MMD (or FID) over penultimate-layer features as the primary metric; KL over per-channel intensity histograms secondary and informational only.

**Boundary:** SC-I establishes **that** the mechanism operates. It does **not** establish that the magnitude of the distance reduction predicts the magnitude of any performance gain, and no such correspondence may be claimed from it. Because the distance is computed over model-dependent features, the two arms are measured in different representation spaces, and the comparison is of a target corpus's relative remoteness within each arm's own space. The contribution is mechanistic and carries no claim of diagnostic performance, device compatibility (NC-16) or clinical utility.

---

### SC-H: Ophthalmology-Specific Self-Supervised Initialization of the CNN Backbone

**Contribution:** Replacement of generic ImageNet transfer with an in-domain initialization for the integrated arm: the same CNN backbone (ResNet-50 / EfficientNet-B3) is pretrained with a CNN-compatible domain-adaptive self-supervised learning protocol (DINO / BYOL / SimCLR / MoCo family) on an unlabeled retinal fundus corpus, then fine-tuned for DR classification. This preserves the CNN architecture — avoiding the architecture confound that a foundation model such as RETFound (ViT-Large) would introduce — while supplying retina-aware representations (vascular topology, optic-disc and macular morphology, retinal texture, illumination/artifact variability) as the starting point for the integrated pipeline.

**Operational specification (v6.2.0):** The corpus is the unlabeled EyePACS "test" split (53,576 images), disjoint from the ~35,126 Experiment-1 corpus by image and patient identity — a no-pretraining-leakage constraint (INVARIANTS SB-2.4) analogous to ImageNet being a separate corpus for the baseline arm. **BYOL** is the primary protocol (MoCo-v2 / SimSiam / DINO as alternatives), pretrained **from-scratch (random init)** directly on the 4-channel tensor. The initialization is admitted into Experiment 1 only after passing a **frozen-backbone linear-probe acceptance gate** (it must beat random init and be competitive with ImageNet on the EyePACS-test probe slice, for both backbones); a fallback ImageNet→continual-SSL initialization is documented but is not the default.

**In-domain initialization generalized (v6.3.0):** From-scratch label-free CNN-SSL **failed** the linear-probe acceptance gate on this corpus (best quadratic-κ ≈0.11 vs ImageNet ≈0.30 — a robust negative result across BYOL / MoCo-v2 / DINO). SC-H is therefore generalized from *self-supervised* to **in-domain initialization (self-supervised OR supervised), selected by the acceptance gate**. The admitted alternatives are (a) fundus-SSL, (b) ImageNet→continual-SSL, and (c) **supervised in-domain pretraining (SIP)** — the same CNN backbone supervised on the EyePACS-test DR grades (INVARIANTS SB-2.4 [v6.3.0]), started from ImageNet and adapted, then transferred. The negative SSL result is recorded as evidence, not hidden. CFC-2.8 continues to bound all three options equally: the isolated effect of the initialization is not independently claimed.

**Evidence:** Experiment 1 integrated arm (configs B, D), paired with the full preprocessing pipeline.

**Boundary (CFC-2.8):** Because the integrated arm differs from baseline along both the preprocessing and the pretraining axis, the isolated effect of the SSL initialization is **not** independently claimed; it is reported as a component of the integrated configuration. The associated research question — how ophthalmology-specific SSL interacts with the preprocessing pipeline for robustness and generalization — is framed as a direction motivated by this design, bounded by CFC-2.8. No SSL performance is asserted in advance of training: SC-H is, at present, a specification whose efficacy is to be established empirically (and gated, per the linear-probe acceptance criterion above).

---

## Relationship to Primary Claims

| Contribution | Primary Claims Supported |
|---|---|
| C-1 | PC-1, PC-8 |
| C-2 | PC-6 |
| C-3 | PC-7 |
| SC-A | PC-2 |
| SC-B | PC-2 |
| SC-C | PC-9 |
| SC-D | PC-1, PC-8 |
| SC-E | PC-1, PC-8 |
| SC-F | PC-1, PC-8 |
| SC-G | PC-10 |
| SC-H | PC-1, PC-8 |

---

## Boundary Conditions

All contributions are bounded by the scope constraints defined in INVARIANTS.md (Section IV: Scope Boundaries) and the non-claims listed in ARGUMENT_MAP.md (Section VII). In particular:

- Contributions do not extend to general retinal disease classification or imaging modalities other than fundus photography
- Contributions do not constitute clinical device certification or regulatory compliance
- Contributions are bounded to the tested architectures (ResNet-50, EfficientNet-B3, EfficientNet-B4) and datasets as specified in the experimental protocol
