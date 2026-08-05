**Version:** 7.1.0 | **Date:** 2026-08-05 | **Binding Reference:** INVARIANTS.md v7.0.0

**v7.1.0 Amendment: H-3 is restored as *Domain-Shift Reduction*.** The label H-3 was vacated in V3, when the *training-method comparison* it then denoted (frozen-layer versus progressive fine-tuning as an experimental factor) was dropped and fine-tuning was demoted to a shared training method applied uniformly across the H-1 configurations. **That retirement stands and is not reversed.** The label is **reused** here for a distinct and previously unstated hypothesis: that the integrated configuration measurably reduces the distance between the source and external domains in feature space.

*Reason for restoration.* The central hypothesis asserts a causal chain — the pipeline reduces domain variability, and reduced variability yields improved external classification. Every hypothesis in the programme prior to this amendment measured the chain's **consequence** (external accuracy: H-4, H-6, H-7) and none measured its **middle term**. Domain-shift reduction was therefore the single unmeasured link in the dissertation's own argument, inferred throughout but never tested. H-3 tests it directly and at low cost — forward passes only, no training.

*Label-reuse notice (binding on all downstream text).* Occurrences of "H-3 dropped" in §2.3.2 and §3.3.3 and in their briefs and continuity notes refer to the **retired training-method hypothesis** and are historically correct. They must not be read as referring to the present H-3. No text may treat the two as the same hypothesis, and no claim about training method may be derived from H-3.

*Threshold provenance — stated openly.* Neither `MCID_d` nor `K` was specified when the domain-shift question was first posed; **both are assigned at this formalization**, not pre-registered. Two facts bound the significance of that. First, `MCID_d = 0.0` is not a tuned choice: `d` is an unnormalized distance in arbitrary units, so no non-zero minimal difference is interpretable, and the per-set condition degenerates to `CI⁻(Δd) > 0` — a bare directional-significance test. Second, the outcome is **insensitive to `K`**: the measured result passes for every `K ≤ 6`, so the choice of `K = 5` does not determine the verdict. Recorded here so that a reader can verify the criterion was not fitted to the result. **VCR-1** is satisfied by issuing this versioned amendment; **VCR-3** is not engaged, since no result contradicting a direction of effect is being concealed — the direction was never contradicted.

**Bump rationale:** a new hypothesis is added and no existing binding is reversed → **MINOR** per VERSIONING_POLICY §4. H-1, H-2, H-4, H-5, H-6, H-7, the composite IV and CFC-2.8 are unchanged. Governance files updated: HYPOTHESIS (this amendment, H-3 definition, Central-Hypothesis note, Conclusion), VERSION_SYNC, CHANGELOG, ARGUMENT_MAP (PC-11), CONTRIBUTIONS (SC-I). Downstream sync: `thesis/ASSET_INVENTORY.md` (H-3 row, decision 3 closed), `thesis/CLAUDE.md`, `thesis/outline/TABLE_OF_CONTENTS_EN.md` and `_KZ.md` (§4.4), `thesis/chapters/04-experiments/` (§4.4.1, §4.4.2 and their briefs/continuity/reviews). `results/` already carries the block.

**v7.0.0 Amendment:** **H-7 is reformulated from "Clinical Degradation Resistance" to "External Clinical Performance."** The dependent variable changes from the degradation quantity Δ_drop = F1_EyePACS_val − F1_external to the **absolute external performance difference** Δ wF1(X) = wF1(integrated, X) − wF1(baseline, X), evaluated independently on each external clinical set with an acceptance form requiring Δ wF1(X) ≥ MCID_wF1 = 0.050 **and** CI⁻ > 0 on **both** sets (sets are not aggregated; a single reversal gives REVERSED regardless of the other).

*Reason — the retired dependent variable is not independent of the hypothesis it was meant to test.* For any external set X:

```
Δ_drop(integrated, X) − Δ_drop(baseline, X)
  = [wF1(int, in) − wF1(int, X)] − [wF1(base, in) − wF1(base, X)]
  = [wF1(int, in) − wF1(base, in)] − [wF1(int, X) − wF1(base, X)]
  = Δ_in-domain − Δ_external
```

The comparison therefore reduces to the fixed in-domain margin minus the very quantity H-7 sets out to measure. Its sign is satisfied **only** when the integrated arm beats baseline *more on foreign data than on its own*, so the criterion penalizes the integrated arm precisely for its in-domain result and measures nothing about resistance to degradation. This is a defect of operationalization, identified analytically and not by inspection of outcomes.

*Relation to VCR-3.* VCR-3 forbids silent modification of a hypothesis when results **contradict the direction of effect**. That condition is not met here: the direction of effect for H-7 — the integrated arm performing better on external clinical data — was never contradicted at any evaluation. What failed was the metric chosen to express it. The amendment is recorded openly here, in INVARIANTS v7.0.0, in CHANGELOG and in VERSION_SYNC, and the retired form is preserved below with its own results rather than deleted; no falsifying observation is being concealed. *Relation to VCR-1.* Core Hypotheses are immutable post-ratification and may be modified only through a new versioned Invariants document — hence the MAJOR bump to INVARIANTS v7.0.0, which this file's binding reference now tracks.

**Bump rationale:** a hypothesis is reformulated incompatibly with the prior version → **MAJOR** per VERSIONING_POLICY §4. Governance files updated: INVARIANTS (Section II H-7, header), HYPOTHESIS (H-7, Conclusion, header), ARGUMENT_MAP (PC-10, SC-10.1, PC-10 strength), CONTRIBUTIONS (SC-G), RESEARCH_ARCHITECTURE (§5.5, §9.1, PC-10 row), VERSION_SYNC, CHANGELOG. H-1 through H-6, the composite IV and CFC-2.8 are unchanged.

**v6.2.0 Amendment:** Two changes, no binding reversed. (1) **Argument-structure sync:** Premise 4 and the Conclusion are corrected to the v6.0.0 ophthalmology-SSL framing — the residual RETFound wording (carried over unmodified from v5.2) is replaced, since RETFound is no longer the integrated-arm initialization source. (2) **Operational specifics** of the integrated-arm SSL are recorded: corpus = unlabeled EyePACS "test" split (53,576 images, disjoint from the ~35,126 Experiment-1 corpus per INVARIANTS SB-2.4); primary protocol = BYOL, from-scratch on the 4-channel tensor; admission to Experiment 1 gated by a linear-probe acceptance criterion. H-1's composite IV and CFC-2.8 are unchanged. MINOR bump per INVARIANTS v6.2.0.

**v6.0.0 Amendment:** The RETFound foundation model is removed as the integrated-arm initialization source. The integrated arm of H-1 now initializes the existing CNN backbone (ResNet-50 or EfficientNet-B3) from **ophthalmology-specific self-supervised pretraining** on an unlabeled retinal fundus corpus (CNN-compatible domain-adaptive SSL — DINO / BYOL / SimCLR / MoCo family — selected empirically). Because the SSL initialization is CNN-native, the 2×2 *(preprocessing × architecture)* factorial symmetry is restored (configs A/B/C/D; both backbones in both arms), resolving AOQ-1, AOQ-3, and AOQ-4 and simplifying AOQ-2 (INVARIANTS v6.0.0 Section X). The composite independent variable and CFC-2.8 are **retained** (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-SSL). Hypotheses H-2, H-4, H-5, H-6, H-7 are unchanged.

**v5.2 Amendment:** RETFound pretraining-corpus description is refined from "~1.6M color fundus photographs" (CFP-only) to the multi-modal retinal imaging corpus on which RETFound was actually pretrained per Zhou et al. 2023 — approximately 1.6M images comprising ≈904K color fundus photographs (CFP) and ≈736K optical coherence tomography (OCT) scans. For the dissertation's fundus-only downstream task, the integrated arm initializes from the CFP-pretrained RETFound checkpoint; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 holds). All other v5.1 provisions are retained.

**v5.1 Amendment:** H-1 is reformulated to reflect a composite independent variable: *(preprocessing, pretraining source)*. The baseline arm uses ImageNet-pretrained weights; the integrated arm uses RETFound-pretrained weights. The hypothesis is renamed from "Preprocessing Dominance" to "Integrated Pipeline Dominance" to mark the joint nature of the manipulated factor. Operational details (backbone architecture in the integrated arm, 4-channel input adaptation, license verification, symmetry of the factorial) are deferred to AOQ-1 through AOQ-4 in INVARIANTS.md Section X. Hypotheses H-2, H-4, H-5, H-6, H-7 are unchanged from v5.0.

---

## Central Hypothesis

The proposed preprocessing pipeline reduces domain variability across fundus imaging devices and acquisition conditions while preserving diagnostically relevant retinal features, leading to improved CNN-based diabetic retinopathy detection. The hypotheses H-1 through H-7 below are decompositions of this central hypothesis, each testing a specific aspect of the overarching claim. **H-3 (v7.1.0) tests the first clause of the central hypothesis directly** — that the pipeline reduces domain variability — which the remaining hypotheses had previously approached only through its downstream consequence. H-7 was reformulated in v7.0.0 (see the amendment above); the central hypothesis itself is unchanged.

---

**H-1 (Integrated Pipeline Dominance) [v5.2 amended].** If fundus images from EyePACS are processed through the 8-stage preprocessing pipeline — comprising canonical flip (Stage 0), OD-fovea rotation normalization (Stage 1), FOV crop + isotropic resize to 512×512 with centered zero-padding (Stage 2), FOV mask generation as 4th input channel (Stage 3), adaptive flat-field correction with σ = 0.07 × FOV diameter (Stage 4), dual-constraint CLAHE on LAB L-channel with stochastic application at train time (Stage 5), augmentation at train time (Stage 6), and dataset-specific channel-wise normalization (Stage 7) — and a CNN classifier (ResNet-50 or EfficientNet-B3) initialized with **ophthalmology-specific self-supervised pretrained weights** (a CNN-compatible domain-adaptive self-supervised learning protocol — DINO / BYOL / SimCLR / MoCo family, selected empirically — pretrained on an unlabeled retinal fundus corpus without diabetic-retinopathy labels) is fine-tuned on the processed images, then classification performance measured by accuracy, precision, recall, F1-score (macro and weighted), ROC-AUC, and Cohen's Kappa (quadratic weights) will be statistically significantly higher than that of a downstream classifier initialized with **ImageNet pretrained weights** (ResNet-50 or EfficientNet-B3) and trained on baseline images (stretch-resize to 512×512 + ImageNet normalize, 3 channels, no FOV mask) of equivalent source distribution, satisfying the dominance criterion of weighted F1 Δ ≥ 5 pp, ROC-AUC Δ ≥ 0.02, and no Kappa degradation.

The independent variable is the composite *(preprocessing × pretraining source)* pair (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-SSL). Attribution of the observed effect to preprocessing alone, pretraining alone, or their interaction is **forbidden** under CFC-2.8 (INVARIANTS v6.0.0). The integrated-arm backbone architecture and 4-channel input questions (AOQ-1, AOQ-2, AOQ-4) are **resolved** in v6.0.0 (INVARIANTS Section X): both ResNet-50 and EfficientNet-B3 are used in both arms, and SSL pretraining is performed on the 4-channel input.

**H-2 (CLAHE Threshold Sensitivity and Component Ablation).** If the dual-constraint CLAHE clip limit parameters (clip_factor and global_threshold) are varied across controlled values on EyePACS, where clip_limit = min(clip_factor × tile_area / 256, global_threshold × tile_area) and CLAHE is applied stochastically at train time (80% probability), then per-class F1-score for DR 1 and DR 2 will exhibit a parameter-dependent sensitivity profile with at least one local optimum within the tested range of (clip_factor, global_threshold) combinations. Additionally, the flat-field correction σ factor is swept across 0.05–0.10 × FOV diameter to identify optimal illumination normalization.

**H-3 (Domain-Shift Reduction) [v7.1.0 restored — label reused, see amendment].** If fundus images from the source corpus (EyePACS) and from each external corpus X are passed through the baseline and the integrated configurations and embedded by the network's penultimate layer, then the distance between the source and target feature distributions will be smaller under the integrated configuration than under the baseline, on at least five of the six external corpora, with the confidence interval of the reduction excluding zero:

```
H-3  ⟺  Σ            PASS_S(d, X)  ≥  K = 5,        n = 6
        X ∈ 𝕏

PASS_S(d, X)  ⟺  Δd(X) = d(BASE, X) − d(INT, X)  ≥  MCID_d = 0.0   ∧   CI⁻(Δd) > 0

𝕏 = {APTOS 2019, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD}
```

**Variables.**

| Symbol | Definition | Range / units | How measured |
|---|---|---|---|
| X | external corpus | the 6 sets of 𝕏 | fixed |
| φ(·) | penultimate-layer features | vector | forward pass, **no training** |
| **d** | **MMD (or FID) between φ(EyePACS) and φ(X)** | ≥ 0, dimensionless | **primary metric — the criterion is computed on d alone** |
| d_KL | KL divergence over per-channel intensity histograms | ≥ 0 | **secondary, informational only — carries no part of the criterion** |
| Δd(X) | d(BASE, X) − d(INT, X), the reduction in distance | absolute units of d | paired within X |
| CI⁻(Δd) | lower bound of the bootstrap CI of the reduction | absolute | **1 000 resamples** |

**Arms.** The comparison is the pair **integrated − baseline** (EfficientNet-B3 backbone: pipeline + in-domain SSL initialization against baseline + ImageNet), i.e. the configuration pair D − C of Experiment 1.

**Sign convention and acceptance form.** Δd is defined as a *decrease* in distance, so the sign is already normalized and the ordinary superiority form **S** applies. Because `d` is unnormalized, `MCID_d = 0.0` and the per-corpus condition reduces to `CI⁻(Δd) > 0`.

**Protocol condition (mandatory).** Stage 7 normalization **must** be computed from **source-domain statistics**, exactly as in zero-shot deployment. Computing it from the target corpus would make the measurement a form of target-domain adaptation and would render the result incomparable with H-4, H-6 and H-7. Any evaluation violating this condition does not test H-3.

**Pre-specified reversal case (recorded before the outcome, retained).** Stage 5 (CLAHE tuned on EyePACS) and Stage 7 (dataset-specific normalization) are bound to the source domain by construction, so a REVERSED outcome was a live possibility rather than a remote one: the pipeline could reduce variability *within* the source domain while increasing it *across* domains. Had that occurred it would have been an established finding, not a failed run — it would have directly explained any reversal in H-4 and H-7 and would have been reported as a result. Recording the reversal case here preserves the hypothesis's falsifiability on the face of the governance document (VCR-3).

*Scope.* Bounded to the six named corpora and to the architectures evaluated. H-3 is **mechanistic**: it measures a property of the representation, not a clinical outcome, and supports no claim of diagnostic performance, device compatibility (NC-16) or clinical utility. It establishes **that** the mechanism operates; it does **not** establish that the magnitude of the distance reduction predicts the magnitude of any performance gain, and no such correspondence may be asserted from it. Because d is computed over model-dependent features, the baseline and integrated distances are measured in different representation spaces; the comparison is of a target corpus's relative remoteness within each arm's own space.

**H-4 (Cross-Dataset Transferability).** If models trained on EyePACS with the full preprocessing pipeline are evaluated on APTOS 2019 without retraining, then the generalization ratio G = F1_APTOS / F1_EyePACS will be ≥ 0.85.

**H-5 (Explainability).** If Grad-CAM analysis is applied to a CNN (EfficientNet-B4) processing fundus images with the preprocessing pipeline vs. stretch-resize + ImageNet normalize baseline, then the Attention–Lesion Overlap (ALO) between Grad-CAM activation regions and IDRiD pixel-level lesion masks will be significantly higher for preprocessed models (ALO_preproc > ALO_baseline), demonstrating that preprocessing directs model attention toward clinically relevant structures (microaneurysms, hemorrhages, hard exudates, soft exudates). ALO is defined as `ALO = area(GradCAM ∩ lesion_mask) / area(lesion_mask)` and serves as the **primary** explainability metric, measuring what fraction of the lesion is covered by model attention (clinically relevant — lesion coverage). Intersection-over-Union (IoU) is retained as a **secondary** metric measuring symmetric spatial precision: `IoU = area(GradCAM ∩ lesion_mask) / area(GradCAM ∪ lesion_mask)`. Qualitative Grad-CAM overlays are additionally produced on the Kazakh clinical dataset for visual validation.

**H-6 (Device Robustness).** If preprocessed models trained on EyePACS (Canon CR-1) are evaluated on images from different fundus cameras (Topcon, Kowa via RFMiD; Canon, Topcon via DDR; Canon, Zeiss via ODIR-5K), then classification performance will be maintained across camera domains, with cross-device performance variance remaining within acceptable bounds relative to in-domain performance. DR labels only; non-DR disease labels are ignored or mapped to non-DR.

**H-7 (External Clinical Performance) [v7.0.0 reformulated].** If a CNN model trained on EyePACS is evaluated without retraining on external clinical datasets (IDRiD, Messidor-2) with and without the preprocessing pipeline, then on **each** external dataset the integrated-preprocessed model will attain a weighted F1-score higher than the baseline model by at least the minimal clinically important difference, with the confidence interval of the difference excluding zero:

```
H-7  ⟺  ⋀            PASS_S(wF1, integrated − baseline on X) = 1
        X ∈ {IDRiD, Messidor-2}

PASS_S  ⟺  Δ wF1(X) = wF1(integrated, X) − wF1(baseline, X)  ≥  MCID_wF1 = 0.050   ∧   CI⁻ > 0
```

The independent variable is the presence vs. absence of the preprocessing pipeline (comparison arm-wise, backbone held fixed). The dependent variable is Δ wF1(X), computed separately for IDRiD and Messidor-2. **The datasets are not aggregated:** a reversal (CI⁺ < 0) on either set yields REVERSED for the hypothesis irrespective of the other. Note that the acceptance form requires Δ ≥ MCID **and** CI⁻ > 0 — it does **not** require CI⁻ ≥ MCID.

*Scope.* Bounded to the tested datasets (IDRiD, Messidor-2) and architectures (ResNet-50, EfficientNet-B3), zero-shot with no target-domain adaptation. The hypothesis claims **higher absolute performance on external clinical data**; it does **not** claim reduced degradation, reduced proportional drop, or resistance to domain shift, and no such claim may be derived from it.

*Retired form (v6.2.0 and earlier), retained as descriptive only.* The degradation quantity Δ_drop = F1_EyePACS_val − F1_external may still be reported for context, but it is **not** a criterion for H-7 and no verdict may rest on it. It is algebraically degenerate — Δ_drop(integrated) − Δ_drop(baseline) ≡ Δ_in-domain − Δ_external — and therefore requires the integrated arm to exceed baseline more on external data than in-domain, penalizing it for its own in-domain result. See the v7.0.0 amendment above and the analysis carried in Chapter 5 §5.4.

---

## Argument Structure

The hypotheses above are linked by the following causal argument:

**Premise 1 (Domain Variability):** Fundus images acquired by different devices, under different illumination conditions, and with different noise levels exhibit substantial domain variability that degrades CNN classification performance.

**Premise 2 (Distribution Shift Degrades CNN):** This domain variability manifests as distribution shift in the input feature space, causing CNN models trained on one domain to generalize poorly to others.

**Premise 3 (Preprocessing Normalizes):** The proposed 8-stage preprocessing pipeline standardizes retinal image appearance — normalizing orientation (Stage 0: canonical flip; Stage 1: OD-fovea rotation normalization so the OD→fovea axis is horizontal), preserving fundus geometry (Stage 2: isotropic resize with zero-padding; Stage 3: FOV mask as 4th channel), correcting illumination gradients (Stage 4: adaptive flat-field correction, σ = 0.07 × FOV diameter), enhancing contrast stochastically (Stage 5: dual-constraint CLAHE), and applying dataset-specific normalization (Stage 7) — thereby reducing inter-domain distribution shift while preserving diagnostically relevant retinal features.

**Premise 4 (In-Domain Pretraining Provides Retina-Aware Initialization) [v6.0.0; specifics v6.2.0].** The integrated arm initializes the same CNN backbone (ResNet-50 / EfficientNet-B3) from **ophthalmology-specific self-supervised pretraining** on an unlabeled retinal fundus corpus, using a CNN-compatible domain-adaptive SSL protocol (the DINO / BYOL / SimCLR / MoCo family; **BYOL primary**), pretrained from-scratch on the 4-channel pipeline tensor. No diabetic-retinopathy labels are used during pretraining; the objective is representation learning over retinal anatomical structure (vascular topology, optic-disc and macular morphology, retinal texture, illumination variability, imaging artifacts). The corpus is the unlabeled EyePACS "test" split (53,576 images), disjoint from the Experiment-1 corpus per INVARIANTS SB-2.4, and the initialization must pass a linear-probe acceptance gate before entering Experiment 1. In-domain (retinal-imaging) initialization is expected to improve sample efficiency and clinical generalization relative to natural-image (ImageNet) initialization; this expectation is evaluated empirically and is not assumed (DGL-6).

**Conclusion (v6.0.0; specifics v6.2.0):** The integrated configuration — preprocessing pipeline combined with ophthalmology-specific self-supervised in-domain pretraining — improves diagnostic performance over the baseline configuration (stretch-resize + ImageNet pretraining) as a unitary system (H-1). The pipeline additionally exhibits parameter robustness (H-2), **reduced source-to-target distance in feature space (H-3, v7.1.0 — mechanistic, not a performance claim)**, cross-dataset transfer (H-4), lesion-aligned attention (H-5), cross-device generalization (H-6), and higher absolute performance on external clinical datasets (H-7, v7.0.0 — not a claim of reduced degradation). The decomposition of the H-1 effect into preprocessing-only and pretraining-only contributions is outside the scope of this dissertation (see CFC-2.8).
