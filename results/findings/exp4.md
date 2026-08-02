# Conclusions — Experiment 4 (Grad-CAM explainability, H-5) → §4.5 / §5.1

**What was done.** Two EfficientNet-B4 arms (baseline 3ch against full pipeline 4ch, fold 0), with
Grad-CAM maps compared against the IDRiD pixel-level lesion masks over **all 54** images that have
masks. The primary metric is ALO (the share of a lesion covered by attention), the secondary is IoU.
A paired test (Wilcoxon, 1-sided), bootstrap CIs of the difference, and a sweep of the heatmap
binarization threshold. Source: the **2026-08-02** run.

## What was found

**1. H-5 is confirmed on both parts of the criterion.** ALO is higher for the preprocessed model on
**4 of 4** lesion types (≥3/4 required), and on **all four** the difference is statistically
significant: MA p = 0.0031, HE p = 0.0018, EX p = 0.0007, SE p = 0.0142; all 95% CIs exclude zero.
The secondary metric IoU gives the same result on all four types (p = 0.0011…0.0187).
`h5_alo_supported = true`.

**2. The effect size is substantive, not marginal.** ALO rises by 37–49% relative to baseline (e.g.
hard exudates 0.3510 → 0.4830) and IoU by 45–56%. The absolute ALO levels (0.21–0.48) lie in the
working range of the metric.

**3. The floor effect has been eliminated.** ALO = 0 in both arms is observed for only **6 of 54**
images (f₀ = 0.1111). This is essential: measurement takes place in the working range rather than at
the edge of the metric's sensitivity — the former caveat that "ALO/IoU are uninformative here because
of the floor" is withdrawn.

**4. The result rests on individual observations, not on outliers.** Per image, improvement is seen
on 65–74% (MA 38↑/9↓/7=, HE 37/9/7, EX 40/8/6, SE 17/5/4) and deterioration on 15–19%. The mean
shifts reflect a coherent movement of the majority of images.

**5. It is not explained by the threshold.** The directional criterion is met at **all**
τ ∈ {0.2, 0.3, 0.5, 0.7} (4/4); significance is lost for only one type at the strictest τ = 0.7,
where the activation area is smallest. The choice of the canonical τ = 0.5 does not manufacture the
result.

**6. The classification of the same arms is consistent.** full B4 wF1 0.7766 against baseline 0.7545
(+2.2 pp F1, +0.024 AUC, +0.047 κ). The gain appears **simultaneously** along the discriminative and
the localizational channel — the interpretation is coherent. ⚠️ The gain here is noticeably smaller
than on B3 in exp1 (+6.55 pp): a different backbone, **one fold instead of five**, and a separate
training configuration → the magnitudes are not directly comparable; the table shows the direction,
not the size, of the effect.

## Main conclusion (for §4.5 / §5.1)

The hypothesis that preprocessing aligns the model's attention with clinically meaningful structures
**is confirmed on the full set of masks** — across all four lesion types, both metrics, and robustly
with respect to the threshold. The pipeline's advantage therefore runs **both** through discrimination
(exp1, exp3, exp6) **and** through the spatial anchoring of attention.

## Mandatory boundary — INVARIANTS NC-14

Grad-CAM activation **is not** clinical localization of pathology. The correct formulation is: "the
attention of the model with preprocessing is significantly better aligned with the annotated lesions
(4/4 types, p ≤ 0.0142; the same for IoU)", and **not** "the model finds the lesions" or "the model
is clinically interpretable". Confirmation of H-5 does not weaken NC-14 — it measures alignment, not
diagnostic localization. This distinction must be present in the text of §4.5 and §5.1.

## Caveats (mandatory in the text)

- One model per arm (**fold 0**); there is no cross-validation for this analysis.
- EfficientNet-B4 (not B3, as in exp1) — per the H-5 specification for Grad-CAM.
- Masks are available only for the IDRiD segmentation subset (54 images); soft exudates are annotated
  on 26 of them — hence the largest p is for SE.
- **The clinical (KZ) qualitative overlays have not been produced** — the wording of H-5 requires
  them. This is the only gap still open for the hypothesis (**G-3**, see `HYPOTHESIS_COVERAGE.md`).

Tables: `tables/TAB-4.7_exp4_alo_iou.md`, `tables/exp4_classification.md`.
Card: `hypotheses/H-5.md`.
