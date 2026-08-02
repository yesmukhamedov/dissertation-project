# TAB-4.7 — Experiment 4: Attention–Lesion Overlap (ALO, primary) + IoU (secondary) (H-5)

Grad-CAM against the IDRiD pixel-level lesion masks. Backbone EfficientNet-B3, baseline (Config C, 3ch)
against full pipeline (Config D, 4ch). **ALO = area(GradCAM ∩ lesion)/area(lesion)** is the primary
metric; **IoU** is secondary. The heatmap is binarized at the threshold τ = 0.5 (the canonical one).
The analysis covers **all 54** IDRiD images that have lesion masks.
Source: the **2026-08-02** run (`VALUES.md` §5).

## ALO (primary) — paired comparison, τ = 0.5

| Lesion type | n | ALO (C) | ALO (D) | Δ | 95% CI (Δ) | p (Wilcoxon, 1-sided) |
|---|--:|---:|---:|---:|---|---:|
| Microaneurysms (MA) | 54 | 0.2140 | **0.3180** | +0.1040 | [+0.0412, +0.1668] | **0.0031** |
| Haemorrhages (HE) | 53 | 0.2870 | **0.4020** | +0.1150 | [+0.0523, +0.1777] | **0.0018** |
| Hard exudates (EX) | 54 | 0.3510 | **0.4830** | +0.1320 | [+0.0684, +0.1956] | **0.0007** |
| Soft exudates (SE) | 26 | 0.2260 | **0.3340** | +0.1080 | [+0.0296, +0.1864] | **0.0142** |

## IoU (secondary)

| Lesion type | n | IoU (C) | IoU (D) | Δ | 95% CI (Δ) | p (Wilcoxon, 1-sided) |
|---|--:|---:|---:|---:|---|---:|
| Microaneurysms | 54 | 0.1080 | **0.1690** | +0.0610 | [+0.0241, +0.0979] | **0.0048** |
| Haemorrhages | 53 | 0.1520 | **0.2280** | +0.0760 | [+0.0318, +0.1202] | **0.0032** |
| Hard exudates | 54 | 0.1940 | **0.2810** | +0.0870 | [+0.0401, +0.1339] | **0.0011** |
| Soft exudates | 26 | 0.1160 | **0.1780** | +0.0620 | [+0.0154, +0.1086] | **0.0187** |

## Direction of the effect on individual images (§5.3)

| Type | n | ↑ (better with the pipeline) | ↓ (worse) | = (unchanged) | share ↑ |
|---|--:|--:|--:|--:|---:|
| MA | 54 | 38 | 9 | 7 | 70% |
| HE | 53 | 37 | 9 | 7 | 70% |
| EX | 54 | 40 | 8 | 6 | 74% |
| SE | 26 | 17 | 5 | 4 | 65% |

The effect does not rest on individual observations: improvement is seen on 65–74% of images against
15–19% of deteriorations. The mean shifts are the result of a coherent movement of the majority, not
of outliers.

## Floor effect (§5.4)

| Quantity | Value |
|----------|---------:|
| f₀ — share of images with ALO = 0 in **both** arms (τ = 0.5) | 6 / 54 = **0.1111** |

Only 11% of images sit at the floor of the metric. Measurement takes place in the working range of
ALO/IoU, not at the edge of sensitivity.

## Robustness to the binarization threshold (§5.5)

| τ | Types with Δ > 0 | Significant (p < 0.05) |
|---|--------------:|-------------------:|
| 0.2 | 4 / 4 | 4 / 4 |
| 0.3 | 4 / 4 | 4 / 4 |
| **0.5** (canonical) | **4 / 4** | **4 / 4** |
| 0.7 | 4 / 4 | 3 / 4 |

The direction holds at all four thresholds; significance is lost for only one type at the strictest
τ = 0.7 (the smallest activation area). The result is not explained by the threshold.

## Verdict: `h5_alo_supported = true`

The wording of H-5 requires ALO for the preprocessed model to be **significantly** higher. This is met:

- the directional criterion — **4/4** lesion types (≥3/4 required);
- the statistical one — **4/4** types significant (p from 0.0007 to 0.0142), all 95% CIs excluding zero;
- the secondary metric IoU gives the same result on all four types (p 0.0011–0.0187);
- the result is robust to the binarization threshold (4/4 directionally at τ = 0.2…0.7).

Relative effect size: ALO rises by 37–49% (e.g. EX 0.3510 → 0.4830) and IoU by 45–56%. The largest
absolute gain is for hard exudates (+0.1320); the weakest significance is for soft exudates
(p = 0.0142), where the sample is three times smaller (n = 26).

## Mandatory caveats

1. **INVARIANTS NC-14 remains in force:** Grad-CAM activation **is not** clinical localization of
   pathology. The correct formulation is "the model's attention is better aligned with the annotated
   lesions", not "the model finds the lesions".
2. One model per arm (**fold 0**); there is no cross-validation for this analysis.
3. Masks are available only for the IDRiD segmentation subset (54 images); SE is annotated on only 26
   of them.
4. Classification of the same arms — `exp4_classification.md`.
5. **The clinical (KZ) qualitative overlays are still not produced** — the wording of H-5 requires
   them; see gap G-3 in `HYPOTHESIS_COVERAGE.md`.

Hypothesis card — `hypotheses/H-5.md`. Conclusions — `findings/exp4.md`.
